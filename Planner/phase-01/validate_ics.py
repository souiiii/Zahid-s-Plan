"""Validate with an independent icalendar parser, supplied via PYTHONPATH if needed."""
from pathlib import Path
from datetime import datetime,timedelta
from collections import Counter
import hashlib,json
from icalendar import Calendar
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
p=json.loads((HERE/'plan.json').read_text());path=ROOT/p['calendar_filename'];raw=path.read_bytes()
assert raw.endswith(b'\r\n') and b'\n' not in raw.replace(b'\r\n',b'')
assert max(map(len,raw.split(b'\r\n')))<=75
for line in raw.split(b'\r\n'):line.decode()
cal=Calendar.from_ical(raw);events=cal.walk('VEVENT');slots={s['id']:s for d in p['days'] for s in d['slots']}
assert len(events)==len(slots)==40 and str(cal['X-WR-TIMEZONE'])=='Asia/Kolkata'
seen=set();uids=set();count=Counter();totals=Counter();descriptions={}
for e in events:
 assert not e.errors
 sid=str(e['X-ZAHID-SLOT-ID']);uid=str(e['UID']);assert sid not in seen and uid not in uids
 seen.add(sid);uids.add(uid);s=slots[sid];a=e.decoded('DTSTART');b=e.decoded('DTEND')
 assert a==datetime.fromisoformat(s['start_iso']) and b==datetime.fromisoformat(s['end_iso'])
 assert a.utcoffset()==b.utcoffset()==timedelta(hours=5,minutes=30)
 assert e['DTSTART'].params['TZID']==e['DTEND'].params['TZID']=='Asia/Kolkata'
 assert all(e.get(k) is None for k in ['ATTENDEE','ORGANIZER','RRULE']) and not e.walk('VALARM')
 assert a.date().isoformat()>='2026-10-26' and s['kind']=='study'
 body=str(e['DESCRIPTION']);descriptions[uid]=body
 for i,step in enumerate(s['steps'],1):
  assert f'{i}. {step["title"]} · {step["minutes"]} min' in body
  assert step['instruction'] in body
  for r in step.get('resources',[]):
   target=r.get('public_url') or r['url'];assert (target if target.startswith('https://') else target.split('#')[0]) in body
 count[s['date']]+=1;totals[s['date']]+=int((b-a).total_seconds()/60)
assert len(count)==10 and set(count.values())=={4} and set(totals.values())=={345}
assert seen==set(slots)
again=Calendar.from_ical(cal.to_ical());assert descriptions=={str(e['UID']):str(e['DESCRIPTION']) for e in again.walk('VEVENT')}
assert json.loads((HERE/'ics-export.json').read_text())['plan_sha256']==hashlib.sha256((HERE/'plan.json').read_bytes()).hexdigest()
report=dict(passed=True,file=path.name,events=len(events),study_only=True,start=p['start'],end=p['end'],timezone=p['timezone'],scheduled_hours_per_day=5.75,largest_description_characters=max(map(len,descriptions.values())),checks=['independent parser/round-trip','UTF-8 folding and CRLF','unique IDs','all times match plan.json','4 study/revision events per day','step instructions and inline resource links','no attendees, alarms or invitations'],calendar_changes=False)
(HERE/'ics-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
