---
name: nightly-planner
description: Amelie's end-of-day planning agent. ALWAYS trigger this skill when she asks to plan tomorrow, wants a nightly check-in, says "plan my day tomorrow", "what should I do tomorrow", "nightly planner", "check my email and calendar for tomorrow", "make me a schedule for tomorrow", or "give me tomorrow's to-do list". Reads unread/important Gmail and her Google Calendar, surfaces anything time-sensitive or actionable for the next calendar day, builds a prioritized to-do list, drafts a realistic hour-by-hour schedule around any fixed commitments, and generates a downloadable .ics file so the plan lands directly on her calendar. Runs best at night, after the day's email has settled.
---

# Nightly Planner

Amelie's last stop before bed: know exactly what tomorrow requires before she's in it. Every run ends with three things in hand — a prioritized to-do list, a realistic schedule, and an .ics file she can import.

## Workflow

1. **Establish "tomorrow."** Take today's date from context and compute the next calendar day. All output is scoped to that single day.

2. **Scan email for anything that bears on tomorrow.**
   - Search: `is:unread in:inbox newer_than:3d` and `is:important in:inbox newer_than:5d` via Gmail.
   - Look specifically for: hard deadlines, check-in/check-out times, travel or logistics confirmations, meeting/interview requests, anything from school (Fairfield), work (CVS Health), housing/ResLife/Bursar, or financial accounts that names a date or time.
   - Pull the full thread (`get_thread`) only for messages that look time-sensitive or ambiguous from the snippet — don't burn tool calls opening newsletters, marketing, or LinkedIn digests. Those get silently excluded from the to-do list, not itemized.
   - If a full thread is too large to read in one call, work from what loads and say so rather than guessing at the missing part.

3. **Check the calendar for tomorrow.** Use Google Calendar search for the target date and obvious keywords tied to her known contexts (CVS, class, appointment, call, flight, etc.) since search is semantic rather than a plain date-range listing. Treat consistently empty results as "no calendar events found," not as a tool failure — say so plainly rather than inventing placeholder events.

4. **Build the to-do list**, split into:
   - **Time-critical** — has a hard deadline or window tomorrow (e.g., a checkout time, a scheduled call).
   - **Should happen tomorrow** — no fixed time, but sensible to do given what's active right now.
   - **Can wait** — flagged for awareness (e.g., "still pending their reply") but explicitly not on tomorrow's plate. Say why it's waiting.
   - Skip promotional/newsletter noise entirely — don't list it just to say it's skippable.

5. **Draft an hour-by-hour schedule for tomorrow** anchored on any real fixed commitments (calendar events, deadlines pulled from email). Where there's no fixed commitment to anchor to, build a reasonable draft and say plainly that it's a draft she should adjust — never present invented plans as facts about her day.

6. **Generate the .ics file.** Use `scripts/generate_ics.py` (or equivalent inline logic) to turn the finalized schedule into a calendar file: one VEVENT per schedule block, plus a VALARM 30 minutes ahead of anything with a hard deadline (checkouts, calls, flights). Write it somewhere the user can retrieve it (scratchpad or wherever the session's file-send tool expects), then deliver it as a file, not just a description.

7. **Deliver.** In chat: the to-do list (grouped as above), the draft schedule, and a one-line pointer to the attached .ics. Keep it tight — this is a nightly habit, not a report.

## Notes

- Never fabricate calendar events, email content, or deadlines. If calendar search comes back empty or a source is inaccessible, say so and plan around what's actually known.
- Weekend vs. weekday matters — don't schedule "reply to office" tasks for a Saturday if the office won't be open.
- This is a personal planning tool touching Amelie's real inbox and calendar — read-only access is enough for every step above. Never send email, create calendar events directly, or reply to anything as part of this skill; the .ics file is the only artifact produced.
