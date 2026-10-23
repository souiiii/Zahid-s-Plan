"""Write the revised study-only calendar locally; no calendar API calls."""
from datetime import datetime,timezone
from pathlib import Path
from uuid import uuid5,NAMESPACE_URL
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
PLAN=json.loads((HERE/'plan.json').read_text());OUTPUT=ROOT/PLAN['calendar_filename']
POOL=json.loads((ROOT/PLAN['resource_pool']).read_text());R={r['id']:r for r in POOL['resources']}
PACKS=json.loads((ROOT/'Resources/phase-01/pack-manifest.json').read_text())
ARCHIVES={r['paper'].split()[0]:r['url'] for r in json.loads((ROOT/'Sources/PYQ/download_report.json').read_text()) if r['paper'].endswith('2026 Main')}
LABEL={'maths':'Maths','physics':'Physics','organic':'Organic base','solutions':'Solutions','revision':'Revision'}

def escape(s):return str(s).replace('\\','\\\\').replace('\r\n','\n').replace('\r','\n').replace('\n','\\n').replace(';','\\;').replace(',','\\,')
def fold(s):
 lines=[];part='';length=0
 for c in s:
  n=len(c.encode())
  if length+n>75:lines.append(part);part=' ';length=1
  part+=c;length+=n
 lines.append(part);return '\r\n'.join(lines)
def title(s):return ('REVISION' if s['subject']=='revision' else 'STUDY · '+LABEL[s['subject']])+' — '+s['title'].removeprefix('Revision · ')
def resources(links,seen_archives):
 out=[]
 for r in links:
  url=r.get('public_url') or r['url']
  if url.startswith('https://'):out.extend([r['label']+':',url]);continue
  path,_,fragment=url.partition('#');page=fragment.removeprefix('page=') if fragment.startswith('page=') else None
  out.append(r['label']+': '+path+(f' (PDF p. {page})' if page else ''))
  pack=next((p for p in PACKS if p['output']==path),None)
  if pack and page:
   mapping=[(src,p) for src in pack['sources'] for p in src['pages']];source,pg=mapping[int(page)-1]
   original=R[source['resource_id']]
   if original.get('url'):out.extend([f'Online equivalent · original PDF p. {pg}:',original['url']+f'#page={pg}']);continue
   path=source['path'];page=str(pg)
  if path.startswith('Sources/PYQ/'):
   subject=path.split('/')[2];out.append(f'Original: {Path(path).name}'+(f', PDF p. {page}' if page else ''))
   if subject not in seen_archives:out.extend(['Official ZIP (extract the named paper):',ARCHIVES[subject]]);seen_archives.add(subject)
 return out
def description(s,day):
 lines=[f'Phase 1 · Day {day["day_number"]}/10 · {s["duration_minutes"]} min · IST',''];seen=set()
 for i,st in enumerate(s['steps'],1):
  lines.extend([f'{i}. {st["title"]} · {st["minutes"]} min',st['instruction'],*resources(st.get('resources',[]),seen)])
  if st.get('note_ids'):
   notes={n['id']:n['title'] for n in PLAN['notes']};lines.append('Recall cards: '+', '.join(notes[n] for n in st['note_ids'] if n in notes)+'. Open Notes in planner.html.')
  lines.append('')
 lines+=['Unfinished? Save the exact question; repair it at the next same-subject start. Saved files open from the project folder through planner.html.']
 return '\n'.join(lines)
def build():
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Boards Planner//CBSE XII Phase 1 v2//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH',
 'X-WR-CALNAME:'+escape('CBSE XII · 26 Oct–4 Nov 2026 · Revised'),'X-WR-TIMEZONE:Asia/Kolkata',
 'X-WR-CALDESC:'+escape('3 subject blocks + revision daily; 5h45 scheduled including short pauses. Study-only restart on 26 October. No calendar changes made.'),
 'BEGIN:VTIMEZONE','TZID:Asia/Kolkata','X-LIC-LOCATION:Asia/Kolkata','BEGIN:STANDARD','DTSTART:19700101T000000','TZOFFSETFROM:+0530','TZOFFSETTO:+0530','TZNAME:IST','END:STANDARD','END:VTIMEZONE']
 for d in PLAN['days']:
  for s in d['slots']:
   lines+=['BEGIN:VEVENT','UID:'+str(uuid5(NAMESPACE_URL,'urn:zahid:cbse:phase-01:v2:'+s['id']))+'@zahid-plan.local','DTSTAMP:'+stamp,
           'DTSTART;TZID=Asia/Kolkata:'+datetime.fromisoformat(s['start_iso']).strftime('%Y%m%dT%H%M%S'),
           'DTEND;TZID=Asia/Kolkata:'+datetime.fromisoformat(s['end_iso']).strftime('%Y%m%dT%H%M%S'),
           'SUMMARY:'+escape(title(s)),'DESCRIPTION:'+escape(description(s,d)),
           'CATEGORIES:CBSE XII,'+escape(LABEL[s['subject']]),'STATUS:CONFIRMED','TRANSP:OPAQUE','SEQUENCE:0',
           'X-ZAHID-SLOT-ID:'+escape(s['id']),'END:VEVENT']
 lines+=['END:VCALENDAR'];OUTPUT.write_bytes(('\r\n'.join(fold(l) for l in lines)+'\r\n').encode())
 report=dict(file=OUTPUT.name,plan_sha256=hashlib.sha256((HERE/'plan.json').read_bytes()).hexdigest(),events=40,start=PLAN['start'],end=PLAN['end'],calendar_changes=False,uploaded_files=False,study_only=True,description_style='Numbered steps with the necessary resource links directly below each action.',supersedes='phase-01-23-31-october-2026.ics (archived locally; previous imports are not changed)')
 (HERE/'ics-export.json').write_text(json.dumps(report,indent=2)+'\n');print('Created',OUTPUT.name,'— 40 study/revision events; no calendar changes.')
if __name__=='__main__':build()
