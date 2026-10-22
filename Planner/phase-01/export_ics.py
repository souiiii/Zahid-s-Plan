"""Export the approved plan as a local iCalendar file; never call a calendar API."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
from uuid import NAMESPACE_URL, uuid5

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUTPUT = ROOT / 'phase-01-23-31-october-2026.ics'
PLAN = json.loads((HERE / 'plan.json').read_text())
POOL = json.loads((ROOT / PLAN['resource_pool']).read_text())
RESOURCES = {r['id']: r for r in POOL['resources']}
PACKS = json.loads((ROOT / 'Resources/phase-01/pack-manifest.json').read_text())
DOWNLOADS = json.loads((ROOT / 'Sources/PYQ/download_report.json').read_text())
ARCHIVES = {r['paper'].split()[0]: r['url'] for r in DOWNLOADS
            if r['paper'].endswith('2026 Main')}
SUBJECTS = {'maths': 'Maths', 'organic': 'Chemistry / Organic base',
            'physics': 'Physics', 'solutions': 'Chemistry / Solutions',
            'revision': 'Continuous revision'}
NOTES = {n['id']: n for n in PLAN['notes']}
bridge = (ROOT / 'Resources/phase-01/organic-bridge-check.md').read_text()
question_text, answer_text = bridge.split('\n---\n', 1)
QUESTIONS = dict((int(n), text.replace('**', '')) for n, text in
                 re.findall(r'^(\d+)\. (.*)$', question_text, re.M))
ANSWERS = dict((int(n), text.replace('**', '')) for n, text in
               re.findall(r'^(\d+)\. (.*)$', answer_text, re.M))


def escape(text):
    """RFC 5545 TEXT, before content-line folding."""
    return (str(text).replace('\\', '\\\\').replace('\r\n', '\n')
            .replace('\r', '\n').replace('\n', '\\n')
            .replace(';', '\\;').replace(',', '\\,'))


def fold(line):
    """Fold at 75 UTF-8 octets, without splitting a Unicode character."""
    chunks, part, size = [], '', 0
    for character in line:
        length = len(character.encode('utf-8'))
        if size + length > 75:
            chunks.append(part)
            part, size = ' ', 1
        part += character
        size += length
    chunks.append(part)
    return '\r\n'.join(chunks)


def clock(value):
    if value == '24:00':
        return 'midnight (start of the next date)'
    hours, minutes = map(int, value.split(':'))
    return f'{hours % 12 or 12}:{minutes:02} {"PM" if hours >= 12 else "AM"}'


def summary(slot):
    if slot['kind'] == 'study':
        prefix = 'REVISION' if slot['subject'] == 'revision' else 'STUDY · ' + SUBJECTS[slot['subject']]
        title = slot['title'].removeprefix('Spaced revision · ')
        return prefix + ' — ' + title
    return {
        'offclock': 'OFF-CLOCK — Sleep & personal time',
        'rest': 'REST — ' + slot['title'].split(' · ', 1)[-1],
        'personal': 'LUNCH + GYM — Protected',
        'dinner': 'DINNER — Protected',
        'buffer': 'BUFFER / REST — Repair only if needed',
    }[slot['kind']]


def local_file(url):
    path, _, fragment = url.partition('#')
    page = fragment.removeprefix('page=') if fragment.startswith('page=') else None
    return path, page


def original_paper(path, page):
    """Use only archive URLs already recorded with the supplied papers."""
    subject = path.split('/')[2]
    return [f'Original paper: {Path(path).name}' + (f' · PDF page {page}' if page else ''),
            'Official download (ZIP; extract and open the filename above):', ARCHIVES[subject]]


def resource_lines(slot):
    result, seen = [], set()
    for link in slot['resources']:
        url = link.get('public_url') or link['url']
        if url in seen:
            continue
        seen.add(url)
        result.append(link['label'])
        if url.startswith('https://'):
            result.extend([url, ''])
            continue
        path, page = local_file(url)
        result.append(f'Saved file: {path}' + (f' · PDF page {page}' if page else ''))
        if path.startswith('Sources/PYQ/'):
            result.extend(original_paper(path, page))
        pack = next((p for p in PACKS if p['output'] == path), None)
        if pack and page:
            # Preserve pack page references and also identify the original page.
            pages = [(source, p) for source in pack['sources'] for p in source['pages']]
            source, original_page = pages[int(page) - 1]
            resource = RESOURCES[source['resource_id']]
            if resource.get('url'):
                result.extend([f'Online equivalent of pack page {page} · original PDF page {original_page}:',
                               resource['url'] + f'#page={original_page}'])
            else:
                result.extend(original_paper(source['path'], original_page))
        if path.endswith('organic-bridge-check.html'):
            result.append('The assigned bridge questions and answer checks are included below.')
        result.append('')
    return result


def bridge_numbers(slot):
    if slot['subject'] == 'organic':
        ranges = re.findall(r'\bQ(\d+)(?:[–-](\d+))?', slot['practice'])
    elif slot['subject'] == 'revision':
        ranges = re.findall(r'organic (?:check )?Q(\d+)(?:[–-](\d+))?', slot['recall_new'], re.I)
    else:
        return []
    numbers = []
    for start, end in ranges:
        for n in range(int(start), int(end or start) + 1):
            if n not in numbers:
                numbers.append(n)
    return numbers


def description(slot, day):
    lines = [f'CBSE XII · Phase 1 · Day {day["day_number"]}/9 · {day["date"]}',
             f'{clock(slot["start"])}–{clock(slot["end"])} · {slot["duration_minutes"]} minutes · Asia/Kolkata (IST)', '']
    if slot['kind'] != 'study':
        lines.extend([slot['learn'], '', slot['output']])
        if slot['kind'] == 'buffer':
            lines.extend(['', 'Use the Needs repair queue in the HTML planner. If nothing is flagged, rest.',
                          'No new lesson is assigned to this optional block.'])
        return '\n'.join(lines)

    lines.append('TIME BUDGET')
    lines.extend(f'{minutes} min — {name}' for name, minutes in slot['budget'])
    if slot.get('execution_rule'):
        lines.extend(['', 'WORK ORDER', slot['execution_rule']])
    lines.extend(['', '1. LEARN / RECALL', slot['learn'],
                  '', '2. INDEPENDENT PRACTICE', slot['practice'],
                  '', '3. CHECK & FINISH', slot['output']])
    if slot.get('video_instruction'):
        lines.extend(['', 'VIDEO USE', slot['video_instruction']])
    lines.extend(['', 'RESOURCES', 'PDF page numbers count from the first file page.',
                  *resource_lines(slot)])
    if slot['subject'] == 'revision':
        lines.extend(['RECALL PROMPTS — try before opening the reference cards'])
        for note_id in slot['note_ids']:
            note = NOTES[note_id]
            lines.append(f'{note["title"]}: {note["prompt"]}')
        lines.extend(['', 'Reference cards: Notes/REVISION_NOTES.md or Revision notes in planner.html.',
                      'Log at most three useful corrections in the HTML planner. Export progress for AI updates.'])
    numbers = bridge_numbers(slot)
    if numbers:
        lines.extend(['', 'ORGANIC BRIDGE — original prerequisite questions, not CBSE PYQs'])
        lines.extend(f'Q{n}. {QUESTIONS[n]}' for n in numbers)
        lines.extend(['', 'ANSWER CHECK — read only after attempting the questions'])
        lines.extend(f'Q{n}. {ANSWERS[n]}' for n in numbers)
    lines.extend(['', 'IF UNFINISHED',
                  'Reserve the checking time. Record the exact question or step and flag Needs repair in the HTML planner. Use the 11:45 PM buffer if needed; stop at midnight. Remaining work carries into the next same-subject block, using explanation/replay time first.',
                  '', 'SAVED FILES & PROGRESS',
                  'Open planner.html from the project folder for saved PDFs, reference cards and progress tracking. Saved files are not uploaded or embedded in this calendar; local file links do not reliably open from Google Calendar. Public links above work independently. Calendar events do not sync completion back to the HTML planner.'])
    return '\n'.join(lines).rstrip()


def build():
    now = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    lines = ['BEGIN:VCALENDAR', 'VERSION:2.0',
             'PRODID:-//Zahid Study Planner//CBSE XII Phase 1//EN',
             'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
             'X-WR-CALNAME:' + escape('CBSE XII · Phase 1 · 23–31 October 2026'),
             'X-WR-TIMEZONE:Asia/Kolkata',
             'X-WR-CALDESC:' + escape('45 study hours including 9 revision hours; 108 labelled blocks. Protected meals/gym; optional 15-minute daily buffer. Export only.'),
             'BEGIN:VTIMEZONE', 'TZID:Asia/Kolkata', 'X-LIC-LOCATION:Asia/Kolkata',
             'BEGIN:STANDARD', 'DTSTART:19700101T000000', 'TZOFFSETFROM:+0530',
             'TZOFFSETTO:+0530', 'TZNAME:IST', 'END:STANDARD', 'END:VTIMEZONE']
    for day in PLAN['days']:
        for slot in day['slots']:
            uid = str(uuid5(NAMESPACE_URL, 'urn:zahid-plan:cbse-xii:phase-01:' + slot['id'])) + '@zahid-plan.local'
            lines.extend(['BEGIN:VEVENT', 'UID:' + uid, 'DTSTAMP:' + now,
                          'DTSTART;TZID=Asia/Kolkata:' + datetime.fromisoformat(slot['start_iso']).strftime('%Y%m%dT%H%M%S'),
                          'DTEND;TZID=Asia/Kolkata:' + datetime.fromisoformat(slot['end_iso']).strftime('%Y%m%dT%H%M%S'),
                          'SUMMARY:' + escape(summary(slot)),
                          'DESCRIPTION:' + escape(description(slot, day)),
                          'CATEGORIES:' + escape('CBSE XII') + ',' + escape(SUBJECTS.get(slot['subject'], slot['kind'].upper())),
                          'STATUS:CONFIRMED',
                          'TRANSP:' + ('TRANSPARENT' if slot['kind'] in ['offclock', 'buffer'] else 'OPAQUE'),
                          'SEQUENCE:0', 'X-ZAHID-SLOT-ID:' + escape(slot['id']), 'END:VEVENT'])
    lines.append('END:VCALENDAR')
    OUTPUT.write_bytes(('\r\n'.join(fold(line) for line in lines) + '\r\n').encode('utf-8'))
    metadata = {'file': OUTPUT.name, 'plan_sha256': hashlib.sha256((HERE / 'plan.json').read_bytes()).hexdigest(),
                'events': sum(len(d['slots']) for d in PLAN['days']),
                'calendar_reference': 'Read-only samples from the existing placement planners: explicit task titles, protected breaks/meals, named attempts and direct resource links.',
                'calendar_changes': False, 'uploaded_files': False,
                'resource_policy': 'Existing public textbook/video/MS links; saved pack references with original page mapping and recorded official CBSE archive links. Assigned organic bridge items and answers inline.'}
    (HERE / 'ics-export.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'Created {OUTPUT.name}: {metadata["events"]} events, {OUTPUT.stat().st_size:,} bytes. No calendar changes.')


if __name__ == '__main__':
    build()
