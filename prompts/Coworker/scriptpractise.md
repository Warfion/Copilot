# Practice Builder
## Purpose
A structured, interactive workflow that transforms a presentation script into a
local, browser-based rehearsal tool — designed to help me practice delivery,
pacing, emphasis, and flow for a live session at <event>.

Best used with: Microsoft 365 Copilot Cowork

## Prompt
You are an expert front-end developer and presentation coach.
Your task is to build a lightweight interactive Script Practice Builder web app
that helps me rehearse a presentation using my provided script as the single
source of truth.
Execute the following workflow exactly as instructed.

## ROLE
You are an expert **front-end developer** and **presentation coach**. Build a rehearsal-focused tool that improves pacing, emphasis, and flow.

---

## GOAL
Create an **Interactive Script Practice Builder** web app that lets me practice my presentation script for **<EVENT_NAME>**.

---

## CONTEXT
I need a simple rehearsal tool that runs **locally in a browser** (no backend). It must support multiple practice styles (teleprompter, chunking, cueing), help with pacing (WPM + time estimates), and track progress across practice sessions.

---

## SOURCE (Single Source of Truth)
Use the script provided below as the **authoritative** content.  
- **Do not rewrite, summarize, or change wording.**
- Preserve the original order and wording exactly.
- You may **split into sections** for practice, but do not alter text.

### <SCRIPT>
Paste my full script here.
</SCRIPT>

---

## EXPECTATIONS / OUTPUT FORMAT
Deliver **ONE self-contained HTML file** (HTML + CSS + JavaScript) that I can open locally in a browser.

### Deliverables
1. A single code block containing the full HTML file.
2. A short **Usage** section at the top of the file (as comments) explaining:
   - How to paste/replace the script
   - How to run locally
   - Keyboard shortcuts

---

## STEP-BY-STEP WORKFLOW

### STEP 1 — Parse & Structure Script
- Split the script into **logical rehearsal sections** (natural speaking chunks).
- Assign each section a unique **Section ID**.
- Compute per-section:
  - Word count
  - Estimated speaking time (assume **140 WPM** default; adjustable)
- Preserve exact wording; **no content loss**.

### STEP 2 — Build Practice Modes
Implement these REQUIRED modes:

1) **Teleprompter Mode**
- Auto-scroll with adjustable speed
- Highlight current section/line
- Start/Pause/Resume
- Speed controls (fine + coarse)
- Visible progress indicator

2) **Chunk Practice Mode**
- Show one section at a time
- Manual next/previous section navigation
- Optional “Hide/Reveal” toggle for memorization
- Restart current section

3) **Cue Mode**
- Show only section titles or first line as a cue
- “Reveal” button to show full section text
- Randomize cues option (toggle)

