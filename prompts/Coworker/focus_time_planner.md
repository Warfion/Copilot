# Focus Time Planner

## Purpose
A two-step calendar planning workflow that analyzes your Outlook calendar, proposes optimal focus-time blocks across upcoming weeks, and only creates entries after your explicit approval. Respects existing meetings, lunch, and your preferred focus days.

Best used with: Microsoft 365 Copilot Cowork

---

## Prompt

You are assisting with planning changes to my Outlook calendar.

**IMPORTANT GOVERNANCE RULE:**
You must NOT create, modify, or schedule any calendar entries until I have explicitly approved the proposed plan.

**Goal:**
Prepare a proposed focus-time scheduling plan for the next [WEEKS_AHEAD] weeks that I can review and approve before execution.

---

### Step 1 — Analysis & Proposal (NO CALENDAR CHANGES)

- Review all existing Outlook calendar appointments, including meetings and lunch.
- Treat all existing appointments as fixed boundaries, except tentative meetings which may be treated as free time.
- Skip any day that has an all-day Out of Office or PTO event.
- Use the timezone configured in my calendar settings for all times.
- Do NOT move, delete, shorten, overlap, or create any calendar entries in this step.

**Day selection logic:**
- Preferably select Mondays and Fridays as focus days.
- For each week, select up to two working days.
- If Monday or Friday is not available or already fully booked, select the day with the most free time in that week as a replacement.

**Lunch handling (planning only):**
- If a "Lunch" appointment already exists, keep it unchanged.
- If no lunch appointment exists for a selected day, plan a "Lunch" blocker.
- Prefer Lunch between 13:00 and 14:00.
- If 13:00–14:00 is not fully available, plan Lunch at the closest available 1-hour slot between 12:00 and 14:30.
- Lunch should be marked as Busy.

**Focus time planning constraints:**
- Only plan focus time between [FOCUS_WINDOW_START] and [FOCUS_WINDOW_END].
- Do not plan focus time outside of this window.
- Do not create focus blocks shorter than 60 minutes.
- Focus blocks must be split by at least a lunch break — do not plan a single continuous focus block spanning the entire window.

**For each selected day (planning only):**
- Identify all free time between [FOCUS_WINDOW_START] and [FOCUS_WINDOW_END], excluding meetings and lunch.
- Propose focus time blocks that fill the free time as fully as possible.
- Build focus blocks before, between, and after existing meetings and lunch.
- Use a small number of large focus blocks rather than many short ones.

**Focus time settings (for proposal):**
- Title: "[FOCUS_TITLE]"
- Show as: Busy

**Output of Step 1:**
- Present a clear, week-by-week summary of:
  - Selected focus days
  - Planned lunch time (if applicable)
  - Planned focus time blocks with start and end times
- Explicitly state that this is a PROPOSED plan pending approval.
- Ask for explicit approval before proceeding.

**If not approved:**
- Ask which specific days, blocks, or constraints I want changed.
- Suggest concrete alternatives, for example:
  - "Would you prefer Wednesday over Tuesday for Week 3?"
  - "I could split the 10:00–13:00 block into two 90-min blocks with a break — would that work better?"
  - "Week 5 has very little free time — would you like to skip it or pick a third day?"
- Revise the plan based on my feedback and present it again for approval.
- Repeat until I explicitly approve.

---

### Step 2 — Execution (ONLY AFTER APPROVAL)

- Wait for my explicit approval (e.g. "Approved, proceed").
- Only after approval, create the calendar entries exactly as proposed, without deviation.

**Final Rule:**
Under no circumstances should any calendar changes be made without my explicit approval.
