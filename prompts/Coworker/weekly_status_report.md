# Weekly Status Report

## Purpose
A fact-based weekly status report generator that reviews your Outlook, Teams, and Calendar activity — then synthesizes it into an executive-ready Word document and a draft email to your manager. Only uses real activity; nothing is inferred or invented.

Best used with: Microsoft 365 Copilot Cowork

---

## Prompt

Generate a concise, executive-ready weekly status report based on my actual Microsoft 365 activity.

I want a fact-based weekly report derived only from my Outlook, Teams, and Calendar activity, covering the period from [WEEK_STARTING_DATE] to [WEEK_ENDING_DATE] (local timezone).

---

### Sources to review

**1. Outlook (Inbox and Sent Items):**
- Limit to emails sent or received during the date range
- Prioritize threads where I am the sender, primary recipient, or explicitly asked for input
- Extract:
  - Key topics
  - Decisions explicitly stated or agreed
  - Open issues, risks, or blockers

**2. Microsoft Teams:**

- **Chats:**
  - Review 1:1 and group chats where I actively participated
  - Extract explicit decisions, commitments, or assigned actions
- **Channels:**
  - Review [TEAMS_CHANNEL_NAME] and other channels where I posted or was @mentioned
  - Capture announcements, deliverables, or decisions I was involved in
- **Meetings:**
  - Review Teams meeting recaps or transcripts within the date range
  - For each relevant meeting, capture:
    - Meeting name
    - Key outcomes
    - Decisions made
    - Action items assigned to me

**3. Outlook Calendar:**
- Identify meetings during the date range not covered by Teams recaps
- Summarize purpose and outcomes only if clearly evident from notes or follow-up emails

---

### Synthesis Instructions

- Do not infer or invent outcomes, decisions, or blockers
- If information is unclear, note it explicitly
- Prioritize impact over activity
- Limit total length to approximately one page

---

### Output Format

Create content for a Word document with these sections:
- Accomplishments
- In Progress
- Blockers & Risks
- Key Decisions & Outcomes
- Upcoming Next Week

**Style:**
- Executive-appropriate
- Concise bullet points
- No jargon, no internal chat language

---

### Execution

- Name the document: "Status Report – [WEEK_STARTING_DATE].docx"
- Draft an Outlook email to [MANAGER_EMAIL]:
  - Subject: "Weekly Status – [WEEK_STARTING_DATE]"
  - Body: one-paragraph executive summary referencing the attached report

If any step cannot be completed due to access or data limitations, clearly state what was not available instead of guessing.
