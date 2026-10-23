"""Assign only four study/revision blocks per day; personal time stays unshown."""
from pathlib import Path
from datetime import datetime,timedelta
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
p=json.loads((OUT/'assignments.json').read_text())
routine=[('11:30','13:15','Maths'),('13:15','15:00','Physics / Solutions'),('21:30','23:00','Organic'),('23:15','24:00','Revision')]
def minute(t):
 h,m=map(int,t.split(':'));return h*60+m
for d in p['days']:
 d['slots']=d.pop('tasks')
 for slot,(start,end,label) in zip(d['slots'],routine):
  a,b=minute(start),minute(end)
  slot.update(start=start,end=end,start_minute=a,end_minute=b,duration_minutes=b-a,
              start_iso=(datetime.fromisoformat(d['date'])+timedelta(minutes=a)).isoformat()+'+05:30',
              end_iso=(datetime.fromisoformat(d['date'])+timedelta(minutes=b)).isoformat()+'+05:30',
              budget=[[st['title'],st['minutes']] for st in slot['steps']])
p.update(routine=[dict(start=a,end=b,title=t,kind='study') for a,b,t in routine],study_minutes_per_day=345,
         revision_minutes_per_day=45,pause_minutes_per_day=15,buffer_minutes_per_day=0,total_study_minutes=345*len(p['days']),
         total_buffer_minutes=0,calendar_filename='phase-01-26-october-04-november-2026.ics',
         protected_windows=[dict(start='00:00',end='11:30'),dict(start='15:00',end='21:30'),dict(start='23:00',end='23:15')],
         roadmap_sha256=hashlib.sha256((ROOT/'ROADMAP.md').read_bytes()).hexdigest(),
         pool_sha256=hashlib.sha256((ROOT/'Resources/phase-01/pool.json').read_bytes()).hexdigest(),
         notes=json.loads((ROOT/'Notes/notes.json').read_text()),
         calendar_reference='Existing calendar style retained: named study tasks with direct resources; only study/revision events in this revision.')
(OUT/'plan.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
print(f'Plan: {len(p["days"])} days; {sum(len(d["slots"]) for d in p["days"])} study/revision blocks; 5h45 per day.')
