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
  if kind=='study':
   for r in slot['resources']:
    if r.get('resource_id')=='O-C01':r['url']='Resources/phase-01/organic-bridge-check.html'
   book_pages={
    'maths':[[13],[14,15],[19],[22],[27,31],[31],[34],[36,37],[41,42]],
    'organic':[[2,3,4,5],[10,11],[13,15],[16,17,18],[18,19],[20],[20,21],[23],[18,20,21]],
    'physics':[[26],[7,8],[11,25,26],[25,26],[15,16,17],[19,20,26],[21,22],[26],[25,26]],
    'solutions':[[4,27,28],[5,28],[28],[28],[28],[17,20,28],[22,29],[25,26,30],[28,29,30]]}
   rid={'maths':'M-N01','organic':'O-N01','physics':'P-N01','solutions':'S-N01'}.get(subject)
   if rid:
    resource=next(r for r in json.loads((ROOT/'Resources/phase-01/pool.json').read_text())['resources'] if r['id']==rid)
    di=day['day_number']-1
    for pg in book_pages[subject][di]:
     url=resource['path']+'#page='+str(pg)
     if not any(r['url']==url for r in slot['resources']):slot['resources'].append(dict(label=f'NCERT practice / worked model · PDF page {pg}',url=url,resource_id=rid))
   # Give each study session an explicit time budget; these sums match its slot.
   budgets={
    'maths':[['Recall the method',5],['Lesson / worked example',30],['Independent attempts',30],['Check and note the error',10]],
    'organic':[['Recall yesterday’s base',5],['Lesson and matching NCERT passage',30],['Attempt the named examples / check items',20],['Check and record one correction',5]],
    'physics':[['Recall / read the stated rule',3],['Named video segment or worked model',23],['Independent attempts',15],['Check the result and signs',4]],
    'solutions':[['Recall formulae and units',5],['Main lesson / worked model',30],['Independent attempts',20],['Check units and corrections',5]],
    'revision':[['Earlier maths recall / questions',15],['Earlier physics recall / questions',15],['The named spaced returns',25],['Correct and log',5]]}
   slot['budget']=budgets[subject]
   if subject=='physics' and day['day_number'] in [1,2]:slot['budget']=[['Named video and matching textbook',32],['Named attempts / sketches',10],['Check and record',3]]
   if subject=='solutions':slot['budget']=[['Main lesson with the named NCERT section',35],['Independent attempts',20],['Check units and corrections',5]]
   if subject=='organic' and day['day_number']==9:slot['budget']=[['Finish remaining lesson only if needed',5],['Closed-book bridge check',40],['Check answers',10],['Record exact prerequisite gaps',5]]
   if subject=='physics' and day['day_number']>=8:slot['budget']=[['Recall the rule',3],['Independent board / NCERT attempts',32],['Check and repair',10]]
   if subject=='maths' and day['day_number']>=7:slot['budget']=[['Recall / worked example if needed',10],['Independent attempts',50],['Check and note the error',15]]
  day['slots'].append(slot)
data.update(time_window_confirmation='User confirmed 11:30 AM–midnight on 22 October 2026',routine=[dict(start=a,end=b,kind=k,title=t,subject=s) for a,b,k,t,s in routine],study_minutes_per_day=300,buffer_minutes_per_day=15,total_study_minutes=2700,total_buffer_minutes=135,calendar_reference='Read-only review: explicit study, meal, recovery and buffer labels; named tasks with direct resources and expected outputs. No unrelated appointments imported.',roadmap_sha256=hashlib.sha256((ROOT/'ROADMAP.md').read_bytes()).hexdigest(),pool_sha256=hashlib.sha256((ROOT/'Resources/phase-01/pool.json').read_bytes()).hexdigest(),notes=json.loads((ROOT/'Notes/notes.json').read_text()))
(OUT/'plan.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print('Plan:',len(data['days']),'days;',sum(len(d['slots']) for d in data['days']),'labelled blocks; 45 focused study hours + 2h15 buffer.')
