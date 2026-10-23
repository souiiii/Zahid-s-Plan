"""Validate the revised study-only plan and its dependency/resource references."""
from pathlib import Path
from datetime import date
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[2]
p=json.loads((ROOT/'Planner/phase-01/plan.json').read_text());pool=json.loads((ROOT/'Resources/phase-01/pool.json').read_text())
errors=[];seen=set();assigned=set();links=set()
def check(condition,message):
 if not condition:errors.append(message)
check(p['start']=='2026-10-26' and p['end']=='2026-11-04','Wrong restart window')
check(len(p['days'])==10,'Expected ten days')
for i,d in enumerate(p['days']):
 check((date.fromisoformat(d['date'])-date.fromisoformat(p['start'])).days==i,'Nonconsecutive dates')
 check(len(d['slots'])==4,'Expected 3 subject blocks + revision')
 check([s['subject'] for s in d['slots']]==['maths','physics' if i%2==0 else 'solutions','organic','revision'],'Wrong daily subjects')
 check(sum(s['duration_minutes'] for s in d['slots'])==345,'Wrong daily total')
 last=0
 for s in d['slots']:
  check(s['id'] not in seen,'Duplicate slot');seen.add(s['id'])
  check(s['kind']=='study','Non-study highlighted block')
  check(s['start_minute']>=last,'Overlap');last=s['end_minute']
  check(s['start_minute']>=690 and s['end_minute']<=1440,'Outside study window')
  check(not(s['start_minute']<1290 and s['end_minute']>900),'Protected time collision')
  check(s['start_minute']%15==s['end_minute']%15==0,'Non-round boundary')
  check(sum(st['minutes'] for st in s['steps'])==s['duration_minutes'],'Step budget mismatch')
  check(all(st['instruction'] for st in s['steps']),'Missing step instruction')
  check(sum(s2['duration_minutes'] for s2 in d['slots'] if s2['subject']=='revision')==45,'Wrong revision duration')
  assigned.update(s.get('pool_practice_ids',[]))
  for st in s['steps']:
   for r in st.get('resources',[]):
    links.add(r['url'])
    if not r['url'].startswith('http'):check((ROOT/r['url'].split('#')[0]).is_file(),'Missing file '+r['url'])
  if s['subject']=='revision':check(all(x<d['date'] for x in s['return_dates']),'Revision references an untaught future date')
 check(not any(s['title'] in ['Current · Ohm, resistivity & graphs','Organic base · structures & bonds'] for s in d['slots']),'Full completed lesson repeated')
for prior in p['reported_completed']:assigned.update(prior['pool_practice_ids'])
check(all(x['id'] in assigned for x in pool['practice_sets'] if x['priority']=='core'),'Missing core practice set')
for field,path in [('roadmap_sha256','ROADMAP.md'),('pool_sha256','Resources/phase-01/pool.json')]:check(p[field]==hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'Stale fingerprint '+path)
check(pool['roadmap_sha256']==p['roadmap_sha256'],'Pool/roadmap mismatch')
html=(ROOT/'planner.html').read_text();payload=re.search(r'<script id="plannerData" type="application/json">(.*?)</script>',html,re.S)
check(bool(payload) and json.loads(payload[1])==p,'HTML differs from plan')
check('Resources for the steps above' not in html and 'resource-links' not in html,'Old separate resource section remains')
check('class="step-card"' in html and 'stepLinks(step)' in html,'Resources not integrated with steps')
report=dict(passed=not errors,start=p['start'],end=p['end'],days=10,study_blocks=len(seen),scheduled_hours_per_day=5.75,total_scheduled_hours=57.5,revision_hours=7.5,core_practice_sets_covered=sum(x['priority']=='core' for x in pool['practice_sets']),unique_resource_links=len(links),checks=['restart on 26 October','three subjects plus revision','completed lessons preserved separately','only study events','protected times and round boundaries','step budgets and resource files','revision after teaching dates','all core practice retained','HTML/data/source consistency'],errors=errors)
(ROOT/'Planner/phase-01/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if errors:raise SystemExit(1)
