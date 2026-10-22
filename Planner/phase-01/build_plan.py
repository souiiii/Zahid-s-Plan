from pathlib import Path
from datetime import datetime,timedelta
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'assignments.json').read_text())
routine=[
 ('00:00','11:30','offclock','Off-clock · sleep & personal time',None),
 ('11:30','12:45','study','Maths','maths'),
 ('12:45','13:00','rest','Rest · move, water, reset',None),
 ('13:00','14:00','study','Organic foundation','organic'),
 ('14:00','14:15','rest','Rest · eyes off screen',None),
 ('14:15','15:00','study','Physics','physics'),
 ('15:00','20:00','personal','Lunch + gym · protected',None),
 ('20:00','21:30','dinner','Dinner · protected',None),
 ('21:30','22:30','study','Solutions','solutions'),
 ('22:30','22:45','rest','Rest · decompress',None),
 ('22:45','23:45','study','Spaced revision','revision'),
 ('23:45','24:00','buffer','Buffer · repair or rest',None)]
desc={
 'offclock':('Keep this period free of planned study. Sleep, breakfast and personal commitments fit here; the planner does not prescribe a wake-up time.','No studying before 11:30 AM.'),
 'rest':('Close the lesson. Stand up, drink water and look away from the screen. Stop studying until the next block starts.','A real break; do not fill it with another video.'),
 'personal':('Protected 3–8 PM block for lunch, gym, travel and recovery. No reading, practice or catch-up is assigned. The exact lunch/gym split remains your personal arrangement.','Return ready for dinner; no study overlap.'),
 'dinner':('Eat and take personal downtime. No study or hidden catch-up work is assigned until 9:30 PM.','Restart at 9:30 PM.'),
 'buffer':('Use at most 15 minutes for the first flagged unfinished step from today, prioritising organic prerequisites, then maths, physics and Solutions. If nothing is flagged, rest. Stop at midnight.','If more remains, record the exact step and begin the next same-subject slot with it; replace repeated video time before removing practice. If it cannot fit, flag the day for AI replanning rather than squeezing meals or sleep.')}
for day in data['days']:
 day['slots']=[];mapping={t['subject']:t for t in day.pop('tasks')}
 for start,end,kind,title,subject in routine:
  def minute(s):h,m=map(int,s.split(':'));return h*60+m
  slot=dict(start=start,end=end,start_minute=minute(start),end_minute=minute(end),duration_minutes=minute(end)-minute(start),kind=kind)
  if kind=='study':slot.update(mapping[subject])
  else:
   d,o=desc[kind];slot.update(id=day['date']+'-'+kind+'-'+start.replace(':',''),date=day['date'],subject=kind,title=title,learn=d,practice='',output=o,resources=[],pool_practice_ids=[])
  s=datetime.fromisoformat(day['date'])+timedelta(minutes=slot['start_minute']);e=datetime.fromisoformat(day['date'])+timedelta(minutes=slot['end_minute'])
  slot['start_iso']=s.isoformat()+'+05:30';slot['end_iso']=e.isoformat()+'+05:30'
  day['slots'].append(slot)
data.update(time_window_confirmation='User confirmed 11:30 AM–midnight on 22 October 2026',routine=[dict(start=a,end=b,kind=k,title=t,subject=s) for a,b,k,t,s in routine],study_minutes_per_day=300,buffer_minutes_per_day=15,total_study_minutes=2700,total_buffer_minutes=135,calendar_reference='Read-only review: explicit study, meal, recovery and buffer labels; named tasks with direct resources and expected outputs. No unrelated appointments imported.',roadmap_sha256=hashlib.sha256((ROOT/'ROADMAP.md').read_bytes()).hexdigest(),pool_sha256=hashlib.sha256((ROOT/'Resources/phase-01/pool.json').read_bytes()).hexdigest(),notes=json.loads((ROOT/'Notes/notes.json').read_text()))
(OUT/'plan.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print('Plan:',len(data['days']),'days;',sum(len(d['slots']) for d in data['days']),'labelled blocks; 45 focused study hours + 2h15 buffer.')
