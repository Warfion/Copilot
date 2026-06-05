# Capacity Report

## Purpose
A calendar-analysis workflow that reviews two upcoming full work weeks, classifies every meeting by category, calculates planned vs. available hours, and drafts an HTML-formatted email summary — saved as an Outlook draft, never sent automatically.

Best used with: Microsoft 365 Copilot Cowork

---

## Prompt

Review my Outlook calendar for the next two full work weeks using this selection logic:

- **If today is Monday or Tuesday:** the current week counts as Week 1; Week 2 is the following week.
- **If today is Wednesday–Friday (or later):** skip the remainder of the current week. Week 1 is the next full Monday–Friday week; Week 2 is the week after that.

Always cover exactly two complete Monday–Friday work weeks.

---

### SCOPE & TIMEZONE

- **Working hours:** `[WORK_START — default 09:00]` – `[WORK_END — default 17:00]`, Monday–Friday
- **Timezone:** `[TIMEZONE — default W. Europe Standard Time]`
- **Weekly budget:** `[WEEKLY_HOURS — default 40]` hours per week (before OOF deductions)

---

### RULES FOR COUNTING PLANNED HOURS

1. **Accepted or organized meetings** — add the full duration to planned hours.
2. **Tentative meetings** — do NOT add to planned hours. Track only the total tentative hours as a single number per week. Do NOT list individual tentative meetings anywhere in the output.
3. **"Resource Assigned" entries** — if a calendar entry contains "Resource Assigned" in the description or body, count it as planned regardless of its show-as / free-busy status (even if it shows as free).
4. **Full-day OOF blockers** — if an out-of-office entry spans an entire working day, categorize it as "OOF" and deduct `[DAY_HOURS — default 8]` hours from that week's budget for each OOF day.

---

### MEETING CATEGORIZATION

Classify each planned meeting into the most appropriate category based on its title, attendees, and context. Use these categories (or similar sensible groupings derived from the calendar):

| Category | Examples |
|---|---|
| Internal Meetings | Team syncs, 1:1s, org-wide calls |
| Customer Meetings | External customer calls, partner sessions, EBCs |
| Focus / Prep Time | Focus blocks, prep sessions, deep-work holds |
| Personal / Break | Lunch, personal appointments, breaks |
| Training / Learning | Training sessions, certifications, learning blocks |
| OOF | Out-of-office, PTO, public holidays |

If a meeting does not fit any category above, assign the closest match and note it.

---

### OUTPUT — HTML EMAIL DRAFT

Create an Outlook draft email with the following properties:

- **To:** `[RECIPIENT]`
- **Subject:** `Capacity Report — Week of [START_DATE_WEEK_1] & [START_DATE_WEEK_2]`
- **Body:** clean, readable HTML using tables only — no detailed meeting lists, no inline styles beyond basic table formatting.

#### For EACH of the two weeks, include:

**1. Weekly Overview Block**
A table showing the categorized breakdown of planned hours:

| Category | Hours |
|---|---|
| Internal Meetings | _n_ h |
| Customer Meetings | _n_ h |
| Focus / Prep Time | _n_ h |
| Personal / Break | _n_ h |
| Training / Learning | _n_ h |
| OOF | _n_ h |
| **Total Planned** | **_n_ h** |

**2. Capacity Table**

| Metric | Hours |
|---|---|
| Weekly Budget | _40 h (or adjusted)_ |
| Planned Hours | _n_ h |
| Available Hours | _(budget − planned)_ |
| Tentative Hours (total) | _n_ h |

---

#### After both weeks, include:

**3. Two-Week Summary Table**

| Week | Budget | Planned | Available | Tentative |
|---|---|---|---|---|
| Week of [DATE] | _n_ h | _n_ h | _n_ h | _n_ h |
| Week of [DATE] | _n_ h | _n_ h | _n_ h | _n_ h |
| **Total** | **_n_ h** | **_n_ h** | **_n_ h** | **_n_ h** |

---

### EXECUTION

- Save the email as a **draft** in Outlook. Do **not** send it.
- Do not list individual tentative meetings anywhere.
- Ensure all hour values are rounded to one decimal place.
