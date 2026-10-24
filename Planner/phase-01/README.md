# Revised Phase 1 · 26 October–4 November 2026

Open [planner.html](../../planner.html). Download [the revised .ics](../../phase-01-26-october-04-november-2026.ics). The [roadmap](../../ROADMAP.md) is the planning authority; [pool.json](../../Resources/phase-01/pool.json) holds resource provenance.

The formal schedule starts **26 October**. **24–25 October are unscheduled maths catch-up**, using the [essential prerequisite guide](../../Resources/phase-01/maths-precalculus-bridge.html). Continuity starts on the 26th. The first Ohm/resistivity and organic structures/bonds lessons reported covered on 23 October are recorded in [progress.json](../../Notes/progress.json) and retained for revision. No other completed work or mastery is assumed.

| Time, IST | Study block |
|---|---|
| 11:30 AM–1:15 PM | Maths · 105 minutes |
| 1:15–3 PM | Physics / Solutions on alternate days · 105 minutes |
| 9:30–11 PM | Organic foundation · 90 minutes |
| 11:15 PM–midnight | Continuous revision · 45 minutes |

This is **three subject slots plus revision**, **5h45 scheduled daily**, including five-minute pauses inside the three long blocks. Scheduled time is 57h30 across ten days; 7h30 is revision. Actual work time excludes those pauses. Lunch/gym, dinner, rest and buffers are not calendar events or highlighted website blocks. The 3–9:30 PM window and 11–11:15 PM gap remain clear; study stops at midnight.

Maths and organic appear daily; Physics and Solutions alternate. Phase 1 now ends on 4 November so the missed start is not recovered by rushing every chapter into October. Future roadmap windows remain provisional within the 31 December completion target.

Each session has numbered steps containing the exact action, its time budget, and the links needed for that step. The previous separate instructions/video warning/resource catalogue has been removed. Existing videos remain optional explanations for the named topic. For maths, organic and Solutions, no unverified timestamp is presented as a topic locator; use the exact NCERT section if the main video is on another topic. Physics retains the previously checked publisher chapter links. Practice still prioritises the selected NCERT and board questions.

Revision refers to previously scheduled teaching dates and the reported 23 October work. It uses 20 minutes for earlier maths/physics, 20 minutes for spaced returns, and 5 minutes for checking/logging. The next phase adds later 14/30-day returns. Unfinished work goes to the start of the next same-subject block, replacing replay time; it does not create a late buffer or invade protected time.

The website works locally without a server. Official textbook links open online; saved packs need the Sources/Resources folders alongside the HTML. Personal notes/progress are saved in the browser and exported for AI updates; they do not sync from calendar completion or rewrite disk notes automatically. The new browser progress key separates this revised schedule from the old one; prior personal note corrections are preserved. Reported completed lessons are historical entries, not artificially completed sessions in the new schedule.

The .ics contains **40 study/revision events**, explicit Asia/Kolkata time-zone information, short step-by-step descriptions, and inline resource links. Its last event ends at midnight at the start of 5 November. Original saved pack pages map to official SQPs or recorded CBSE ZIP downloads where possible. Saved notes, bridge checks and packs are not uploaded or embedded as cloud attachments. There are no attendees, invitations, alarms or Google Calendar writes.

The previous 23–31 October calendar and structured plan are under [archive/2026-10-22](archive/2026-10-22). They are superseded. A previous calendar import is not changed by this file; do not layer the revised schedule over old imported events. `topic-library.json` is a frozen source of the original question selections, not the active schedule.

Rebuild from the repository root:

```sh
python3 Planner/phase-01/build_content.py
python3 Planner/phase-01/build_plan.py
python3 Planner/phase-01/render_html.py
python3 Planner/phase-01/export_ics.py
python3 Planner/phase-01/validate_plan.py
```

`validate_ics.py` also checks the export against `plan.json` using the independent `icalendar` Python parser. Browser QA covers desktop/mobile, inline step resources, navigation across October/November, completion persistence, repairs, notes and printing. See the validation JSON files. Do not run `notes_seed.py` unless intentionally resetting the starter reference cards.

## Visual design

The interface retains monospace type and a dark workspace, with a strict three-colour palette: charcoal `#17191c`, off-white `#f0f1ed` and sage `#c7e29a`. The two neutrals handle surfaces, text and rules; the accent marks selected states, resource links and primary actions. There are no gradients, tinted subject backgrounds or additional status colours.

Typography and whitespace provide the hierarchy: larger semibold session titles, readable body instructions, full-contrast metadata, a consistent spacing scale, fewer panel borders and a focused reading layout for slot details. Progress tools are grouped with progress, and general navigation remains in the header. Slot content, resource links, schedule data, notes, roadmap and .ics are unchanged by these visual changes.

`planner.css` is embedded into `planner.html` by `render_html.py`; `reading.css` supplies both reading-page designs. IBM Plex Mono is bundled in `assets/fonts/` under the included SIL Open Font License. Keep that folder alongside the HTML for the exact offline typography; system monospace is the fallback.
