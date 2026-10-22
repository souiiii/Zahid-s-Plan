"""Independent iCalendar-parser validation against the approved JSON schedule.

Requires the `icalendar` package (it may be supplied via PYTHONPATH).
"""
from collections import Counter
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import re

from icalendar import Calendar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
path = ROOT / 'phase-01-23-31-october-2026.ics'
raw = path.read_bytes()
plan = json.loads((HERE / 'plan.json').read_text())
manifest = json.loads((HERE / 'ics-export.json').read_text())
assert manifest['plan_sha256'] == hashlib.sha256((HERE / 'plan.json').read_bytes()).hexdigest()
assert raw.endswith(b'\r\n') and b'\n' not in raw.replace(b'\r\n', b'')
assert max(len(line) for line in raw.split(b'\r\n')) <= 75
for line in raw.split(b'\r\n'):
    line.decode('utf-8')  # Folding must never split a UTF-8 character.

calendar = Calendar.from_ical(raw)
assert str(calendar['VERSION']) == '2.0'
assert str(calendar['X-WR-TIMEZONE']) == plan['timezone']
assert len(calendar.walk('VTIMEZONE')) == 1
events = calendar.walk('VEVENT')
slots = {s['id']: s for d in plan['days'] for s in d['slots']}
assert len(events) == len(slots) == 108
uids, seen_slots, focus, buffers, descriptions = set(), set(), Counter(), Counter(), {}

for event in events:
    assert not event.errors, event.errors
    uid, slot_id = str(event['UID']), str(event['X-ZAHID-SLOT-ID'])
    assert uid not in uids and slot_id not in seen_slots
    uids.add(uid)
    seen_slots.add(slot_id)
    slot = slots[slot_id]
    start, end = event.decoded('DTSTART'), event.decoded('DTEND')
    assert isinstance(start, datetime) and isinstance(end, datetime)
    assert start == datetime.fromisoformat(slot['start_iso'])
    assert end == datetime.fromisoformat(slot['end_iso'])
    assert start.utcoffset() == end.utcoffset() == timedelta(hours=5, minutes=30)
    assert event['DTSTART'].params['TZID'] == event['DTEND'].params['TZID'] == plan['timezone']
    assert (end - start).total_seconds() / 60 == slot['duration_minutes']
    assert all(event.get(key) is None for key in ['ATTENDEE', 'ORGANIZER', 'RRULE'])
    assert not event.walk('VALARM')
    assert str(event['SUMMARY']).strip()
    body = str(event['DESCRIPTION'])
    descriptions[uid] = body
    for key in ['learn', 'practice', 'output']:
        assert slot[key] in body, (slot_id, key)
    if slot['kind'] == 'study':
        focus[slot['date']] += slot['duration_minutes']
        assert all(label in body for label in ['TIME BUDGET', '1. LEARN / RECALL',
                                               '2. INDEPENDENT PRACTICE', '3. CHECK & FINISH'])
        for link in slot['resources']:
            target = link.get('public_url') or link['url']
            assert target in body if target.startswith('https://') else target.split('#')[0] in body
        if slot['subject'] == 'organic':
            assert 'ORGANIC BRIDGE' in body and 'ANSWER CHECK' in body
        assert not re.search(r'(?<!https:)//www\.', body)
    elif slot['kind'] == 'buffer':
        buffers[slot['date']] += slot['duration_minutes']
        assert 'midnight' in body

assert seen_slots == set(slots)
assert len(focus) == len(buffers) == 9
assert set(focus.values()) == {300} and set(buffers.values()) == {15}
assert sum(focus.values()) == 2700 and sum(buffers.values()) == 135
for day in plan['days']:
    daily = sorted((e for e in events if str(e['X-ZAHID-SLOT-ID']) in
                    {s['id'] for s in day['slots']}), key=lambda e: e.decoded('DTSTART'))
    assert all(a.decoded('DTEND') == b.decoded('DTSTART') for a, b in zip(daily, daily[1:]))
    for kind, start_hour, end_hour, end_minute in [('personal', 15, 20, 0), ('dinner', 20, 21, 30)]:
        slot = next(s for s in day['slots'] if s['kind'] == kind)
        assert slot['start'] == f'{start_hour:02}:00' and slot['end'] == f'{end_hour:02}:{end_minute:02}'

round_trip = Calendar.from_ical(calendar.to_ical())
assert descriptions == {str(e['UID']): str(e['DESCRIPTION']) for e in round_trip.walk('VEVENT')}
report = {'passed': True, 'file': path.name, 'parser': 'icalendar',
          'events': len(events), 'study_blocks': sum(s['kind'] == 'study' for s in slots.values()),
          'study_hours': sum(focus.values()) / 60, 'revision_hours': 9,
          'optional_buffer_hours': sum(buffers.values()) / 60,
          'timezone': plan['timezone'], 'largest_description_characters': max(map(len, descriptions.values())),
          'checks': ['independent parser and serialization round-trip', 'CRLF and 75-octet UTF-8 folding',
                     'unique event and slot IDs', 'all dates/times match plan.json', '108 blocks without gaps or overlaps',
                     'protected meals and gym', 'complete instructions and resource references',
                     'organic questions and answers inline', 'no attendees, invitations or alarms'],
          'calendar_changes': False}
(HERE / 'ics-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
