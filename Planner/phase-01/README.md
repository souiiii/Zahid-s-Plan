# Phase 1 HTML planner

Open [planner.html](../../planner.html) in a browser. It embeds all schedule data and works without a server. Keep it with the Sources, Resources and Notes folders so saved PDF links continue to work. Internet is needed for YouTube and public resource links.

Dates: **23–31 October 2026**, Asia/Kolkata. The user confirmed that the earliest study time is **11:30 AM**, not PM. No study extends beyond midnight.

| Daily time | Label |
|---|---|
| Midnight–11:30 AM | Off-clock: sleep and personal time; no study |
| 11:30 AM–12:45 PM | Maths: learning, NCERT and board questions |
| 12:45–1 PM | Rest |
| 1–2 PM | Organic foundation: gradual learning and prerequisite practice |
| 2–2:15 PM | Rest |
| 2:15–3 PM | Physics: learning, derivations and questions |
| 3–8 PM | Protected lunch, gym, travel and recovery |
| 8–9:30 PM | Protected dinner/personal time |
| 9:30–10:30 PM | Solutions: learning and numerical/reasoning practice |
| 10:30–10:45 PM | Rest |
| 10:45–11:45 PM | Continuous revision: older chapters and spaced returns |
| 11:45 PM–midnight | Optional repair buffer; rest if clear |

The total is **45 focused hours**, including **9 revision hours**, plus **2h15 of optional buffer**. A buffer is not counted as completed study or prefilled with another compulsory task. All clock boundaries use quarter-hour increments.

Google Calendar was read for design reference: clear task labels, protected meals/recovery and descriptions naming actions/resources/outputs. Unrelated appointments and personal identifiers were not copied into the planner. No calendar events were created or changed.

The planner provides week and day views, details for all 108 blocks, direct resource links, checklists, completion/repair status, a buffer queue, 10 starter revision cards, browser-saved corrections, progress export and a print view covering all nine days. Study-only filtering is optional; every block is labelled in the default view.

Resource IDs and selections inherit [the resource pool](../../Resources/phase-01/pool.json). The NCERT question selection is the learning target. For the three videos without publisher topic timestamps, the linked windows are explicitly **sequential playback slices**, not claimed topic markers; the learner can stop for the book attempts rather than complete every minute. Physics uses publisher-verified topic links. No fresh recommendation or unverifiable “high quality” guarantee has been added.

The initial Notes files are AI-maintained reference cards. Browser-entered corrections are personal observations, not automatically edits to those files. Export progress and supply it for the next AI update. Opening a card or watching a lesson does not automatically mark learning complete.

If a task runs over, record the exact question/step, mark Needs repair, and use the final buffer. If more remains, the next same-subject task shows the carry-in; use explanation/replay time first. Major overruns need explicit replanning rather than quietly removing meals, breaks, core practice or sleep. The organic readiness check flags specific prerequisites for repair before Haloalkanes if needed.

The structured schedule is [plan.json](plan.json), suitable as the eventual `.ics` source. No `.ics` has been generated. The underlying approved roadmap is unchanged.

Rebuild after changing the content using `build_content.py`, `build_plan.py`, then `render_html.py`. Run `notes_seed.py` only when intentionally regenerating the initial reference cards. Browser progress is separate and is not overwritten by an HTML rebuild.
