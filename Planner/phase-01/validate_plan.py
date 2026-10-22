"""Check schedule constraints, source references and the usable resource links."""
from pathlib import Path
import json,hashlib,re
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[2]
plan=json.loads((ROOT/'Planner/phase-01/plan.json').read_text())
pool=json.loads((ROOT/'Resources/phase-01/pool.json').read_text())
errors=[];seen=set();assigned=set();links=set()
for d in plan['days']:
 end=0;focus=0
 for s in d['slots']:
  if s['id'] in seen:errors.append('Duplicate block '+s['id'])
  seen.add(s['id'])
  if s['start_minute']!=end:errors.append('Gap or overlap on '+d['date'])
  end=s['end_minute']
  if end<=s['start_minute']:errors.append('Nonpositive block '+s['id'])
  if s['start_minute']%15 or end%15:errors.append('Non-round time '+s['id'])
  if s['kind']=='study':
   focus+=s['duration_minutes']
   if s['start_minute']<690 or end>1440:errors.append('Outside allowed study window '+s['id'])
   if s['start_minute']<1290 and end>900:errors.append('Protected-time collision '+s['id'])
   if sum(t[1] for t in s['budget'])!=s['duration_minutes']:errors.append('Time budget mismatch '+s['id'])
   if not s['resources'] or not all(s.get(k) for k in ['learn','practice','output']):errors.append('Incomplete instructions '+s['id'])
  assigned.update(s.get('pool_practice_ids',[]))
  for r in s.get('resources',[]):
   links.add(r['url'])
   if not r['url'].startswith('http'):
    path=unquote(r['url'].split('#')[0])
    if not (ROOT/path).is_file():errors.append('Missing linked file '+path)
  if s.get('video'):
   v=s['video'];resource=next(x for x in pool['resources'] if x['id']==v['resource_id'])
   if not 0<=v['start_seconds']<v['end_seconds']<=resource['duration_seconds']:errors.append('Invalid playback window '+s['id'])
 if end!=1440:errors.append('Day not fully labelled '+d['date'])
 if focus!=300:errors.append('Focus total incorrect '+d['date'])
 for kind,start,end in [('personal',900,1200),('dinner',1200,1290)]:
  if not any(s['kind']==kind and s['start_minute']==start and s['end_minute']==end for s in d['slots']):errors.append('Protected block missing '+d['date'])
missing=[p['id'] for p in pool['practice_sets'] if p['priority']=='core' and p['id'] not in assigned]
if missing:errors.append('Unassigned core practice '+str(missing))
for field,path in [('roadmap_sha256','ROADMAP.md'),('pool_sha256','Resources/phase-01/pool.json')]:
 if plan[field]!=hashlib.sha256((ROOT/path).read_bytes()).hexdigest():errors.append('Changed source '+path)
text=(ROOT/'planner.html').read_text();payload=re.search(r'<script id="plannerData" type="application/json">(.*?)</script>',text,re.S)
if not payload or json.loads(payload[1])!=plan:errors.append('HTML and plan.json disagree')
report=dict(passed=not errors,days=len(plan['days']),labelled_blocks=len(seen),focused_hours=plan['total_study_minutes']/60,optional_buffer_hours=plan['total_buffer_minutes']/60,core_practice_sets_covered=sum(p['priority']=='core' for p in pool['practice_sets']),unique_resource_links=len(links),checks=['no gaps or overlaps','quarter-hour clock boundaries','study only 11:30 AM–midnight','lunch/gym and dinner protected','all core practice referenced','resource files exist','video windows within verified runtimes','source fingerprints unchanged','HTML matches structured plan'],errors=errors)
(ROOT/'Planner/phase-01/validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if errors:raise SystemExit(1)
