# Practice Builder

## Purpose
A structured, interactive workflow that transforms a presentation script into a local, browser-based rehearsal tool — designed to help me practice delivery, pacing, emphasis, and flow for a live session at **<event>**.

Best used with: Microsoft 365 Copilot Cowork

---

## Prompt

You are an expert **front-end developer** and **presentation coach**.

Your task is to build a lightweight, interactive **Script Practice Builder** web app that helps me rehearse a presentation using my provided script as the **single source of truth**.

Execute the following workflow **exactly as instructed**.

---

## INPUTS

**Event:**  
`<event>`

**Script:**  
`<script pasted in full below — treat as authoritative content>`

---

## STEP 1 — SCRIPT INGESTION & STRUCTURING

Parse the script and prepare it for rehearsal use.

### PROCESS
- Preserve the original wording **exactly** — do **not** rewrite or summarize
- Split the script into logical sections using:
  - Headings (if present)
  - Paragraph breaks
  - Natural speaking chunks (3–6 sentences max)

- Assign each section:
  - A unique **Section ID**
  - **Estimated word count**
  - **Estimated speaking time** (default **140 WPM**)

### OUTPUT
- Internal structured representation of the script
- Section order must match the original script **precisely**

### QUALITY CHECKS
- No content loss or rewording
- Sections must be suitable for on-stage rehearsal
- Section boundaries must be clearly identifiable

---

## STEP 2 — PRACTICE MODES DESIGN

Design multiple rehearsal modes that support different practice styles.

### REQUIRED MODES

#### Teleprompter Mode
- Auto-scroll
- Adjustable speed
- Highlight current line or section

#### Chunk Practice Mode
- One section visible at a time
- Manual **Next / Previous** controls

#### Cue Mode
- Show only section titles or first line
- Reveal full content on demand

### COMMON CONTROLS
- Start / Pause / Stop
- Speed increase / decrease
- Next / Previous section
- Restart current section

---

## STEP 3 — PRESENTER EXPERIENCE & ACCESSIBILITY

Optimize the app for real rehearsal conditions.

### REQUIREMENTS
- Large-text presenter view (distance-readable)
- High-contrast color scheme
- Fully responsive (desktop + tablet)
- Keyboard shortcuts for all major actions
- Clear visual indicators for:
  - Current section
  - Progress through script
  - Elapsed and remaining time

---

## STEP 4 — TIMING & PROGRESS TRACKING (LOCAL ONLY)

Add lightweight feedback to support improvement over time.

### TRACK LOCALLY (Browser Only)
- Practice session date
- Total duration
- Sections completed
- Average WPM used

### CONSTRAINTS
- Use `localStorage` only
- No external services
- No analytics, tracking pixels, or network calls

---

## STEP 5 — DELIVERY FORMAT

Produce the final solution as a **single self-contained HTML file**.

### DELIVERABLES
One HTML file containing:
- HTML
- CSS
- JavaScript

Include:
- Clear inline comments explaining key logic
- A short **Usage** section at the top of the file explaining:
  - How to paste a new script
  - How to adjust practice settings
  - How to run the app locally

---

## STANDING CONSTRAINTS (Apply Throughout)

- Do **not** use external libraries, CDNs, or frameworks
- Do **not** require a build step or server
- Keep all data local to the browser
- Optimize for clarity, rehearsal flow, and reliability
- Assume the script may contain confidential information — do **not** log or export it
