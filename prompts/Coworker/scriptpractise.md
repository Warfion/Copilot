# Script Practice Builder

## Purpose
A structured, interactive workflow that transforms a presentation script into a local, browser-based rehearsal tool — designed to help me practice delivery, pacing, emphasis, and flow for a live session at **<event>**.

Best used with: Microsoft 365 Copilot Cowork

---

## Prompt

You are an expert **front-end developer** and **presentation coach**.

Your task is to build an interactive **Script Practice Builder** web app that helps me rehearse a presentation using my provided script as the **single source of truth**.

Execute the following workflow **exactly as instructed**.

---

## INPUTS

**Event:**  
`<event>`

**Script:**  
`<script pasted in full below — treat as authoritative content>`

---

## STEP 1 — SCRIPT INGESTION & STRUCTURING

Parse the script and prepare **two versions** for rehearsal use.

### TWO SCRIPT VERSIONS

1. **Full Script (camera-ready)** — the original script preserved word-for-word
2. **Quick Version (conversational)** — a condensed, conversational rewrite of the same content (fewer words, natural spoken tone, shorter segments)

Both versions share the same UI and all five practice modes. The user switches between them via a **toggle** at the top of the app (two equal-width tabs).

### PROCESS (for both versions)
- Split each version into logical segments using:
  - Headings (if present)
  - Paragraph breaks
  - Natural speaking chunks (3–6 sentences max for Full; 1–3 sentences for Quick)
- Assign each segment:
  - A unique **segment number** (displayed as a numbered badge, e.g., ①②③)
  - **Estimated word count**
  - **Estimated speaking time** (default **140 WPM**)

### QUALITY CHECKS
- Full Script: zero content loss or rewording — preserve the original exactly
- Quick Version: must cover the same ideas but in fewer, more conversational sentences
- Segment order must match the original script precisely

---

## STEP 2 — PRACTICE MODES

Implement **five** practice modes, accessible via a horizontal pill-shaped tab bar. Each mode has an **info box** at the top (light blue/gray background, left blue border) that explains how the mode works.

---

### Mode 1: Read Along

**Tab label:** 📖 Read Along

**Info box text:** "Read Along — Click any segment to highlight it, or use ← / → arrows to step through. Great for first read-throughs and pacing practice."

**Behavior:**
- All segments visible at once, each prefixed with its numbered badge (①②③…)
- Clicking a segment highlights it with a light blue background
- Arrow keys (← →) move the highlight to the previous/next segment
- Space bar advances to the next segment

**Bottom controls:**
← Prev | **Next →** (primary blue button) | ↻ Reset
Right-aligned: segment counter (e.g., "1 / 6")

---

### Mode 2: Teleprompter

**Tab label:** 📺 Teleprompter

**Info box text:** "Teleprompter — Script scrolls like a real prompter. Adjust speed to match your natural delivery pace. Highlighted line = where you are."

**Behavior:**
- **Dark background** (near-black, #1a1a2e) with light text (#e0e0e0) for authentic prompter feel
- All segments displayed; the current segment is highlighted with a brighter background
- Auto-scroll when playing; highlighted segment advances automatically
- Manual scroll also moves the highlight

**Bottom controls:**
▶ Play / ⏸ Pause | ↻ Reset | 🐢 speed slider 🐇 | speed value (number) | A− | A+

- Speed slider adjusts scroll/advance speed
- A− / A+ buttons decrease/increase font size

---

### Mode 3: Guided Practice

**Tab label:** 🎯 Guided Practice

**Info box text:** "Guided Practice — Lines are hidden. Say each line out loud from memory, then click **Reveal** to check yourself. Build confidence one segment at a time."

**Behavior:**
- All segments listed, but their content is **hidden** (show "— hidden —" in gray centered text)
- The first segment shows a hint: "Say this line…" in italic
- User clicks a **Reveal** button to show that segment's actual text
- After revealing, the next segment becomes the active prompt
- Revealed segments stay visible with their full text

**Bottom controls:**
**Reveal Line X of Y** (primary red/pink button, #E53935) | ↻ Start Over
Right-aligned: "0 / 6 revealed" counter

---

### Mode 4: Fill in the Blanks

**Tab label:** ✏️ Fill in Blanks

**Info box text:** "Fill in the Blanks — Key phrases are hidden. Type what you remember, then hit **Check Answers**. Use **Hint** if you get stuck."

**Behavior:**
- Display the full script text, but **blank out 2–4 key phrases per segment**
- Blanked phrases are replaced with underlined **text input fields** (sized to roughly match the missing phrase length)
- Key phrases to blank: important nouns, verbs, and domain-specific terms — not filler words
- **Check Answers** button: compare inputs against originals; highlight correct (green) and incorrect (red)
- **Hint** button: briefly reveal the first letter(s) of a blank

**Bottom controls:**
**Check Answers** (primary blue button) | Hint | ↻ Reset

---

### Mode 5: Memory Test

**Tab label:** 🧠 Memory Test

**Info box text:** "Memory Test — Close your notes and type the script from memory. Then compare side-by-side with the original. Timer tracks your delivery speed."

**Behavior:**
- Label: **"Your attempt:"** with live word count right-aligned (e.g., "0 words")
- A large **textarea** with placeholder text "Start typing the script from memory…"
- **Compare** button: shows a side-by-side or inline diff of the user's attempt vs. the original script, highlighting differences
- **Clear** button: resets the textarea

**Bottom controls:**
**Compare** (primary blue button) | ↻ Clear

---

## STEP 3 — APP LAYOUT & VISUAL DESIGN

### Header Bar
- **Blue gradient** background (#1976D2 → #1565C0)
- Left side: app icon (pencil/notepad emoji ✏️) + **"Script Practice Builder"** title (bold, white, large) + subtitle line showing event name and script label (smaller, light/white text)
- Right side: **live session timer** (green dot ● + time in MM:SS format, white text) + **↻ Reset** button (white outlined)

### Script Version Toggle
- Directly below the header, full width
- Two equal-width tabs: **"📄 Full Script (camera-ready)"** and **"💬 Quick Version (conversational)"**
- Active tab: filled blue background, white text
- Inactive tab: white/light background, gray text

### Practice Mode Tab Bar
- Below the version toggle
- Five horizontally arranged **pill-shaped buttons** with emoji icons: 📖 Read Along, 📺 Teleprompter, 🎯 Guided Practice, ✏️ Fill in Blanks, 🧠 Memory Test
- Active tab: filled blue (or mode-specific accent color), white text
- Inactive tabs: outlined/light, gray text

### Stats Bar
- Below the mode tabs, single row of small info badges:
  - 📄 **X words** | 📑 **Y segments** | ⏱ **~Z.Z min delivery**
  - Right side: keyboard shortcut hints — **← → next  prev   Space reveal**

### Mode Info Box
- Light blue/gray background, left blue border (4px solid #1976D2)
- Mode emoji + **bold mode name** + explanation text

### Content Area
- White background
- Segments in Read Along: left blue border, numbered badge (filled blue circle with white number), comfortable padding between segments
- Active/highlighted segment: light blue background (#E3F2FD)

### Bottom Control Bar
- Below content area
- Left-aligned action buttons (primary action uses filled blue or red button), right-aligned counters/progress indicators

### Color Palette
- Primary blue: #1976D2
- Header gradient: #1976D2 → #1565C0
- Highlight: #E3F2FD (light blue)
- Guided Practice reveal button: #E53935 (red/pink)
- Teleprompter background: #1a1a2e, text: #e0e0e0, highlighted segment: brighter/cyan tint
- Success: green | Error: red
- Body text: dark gray (#333) on white backgrounds

---

## STEP 4 — KEYBOARD SHORTCUTS

| Key | Action |
|-----|--------|
| → (Right Arrow) | Next segment |
| ← (Left Arrow) | Previous segment |
| Space | Reveal / advance (context-dependent per mode) |
| Escape | Reset / stop current action |

Display shortcut hints in the stats bar so users discover them naturally.

---

## STEP 5 — TIMING & PROGRESS TRACKING (LOCAL ONLY)

### Session Timer
- Starts automatically when the user begins interacting (first click/keypress in a mode)
- Displayed in the header bar as a green dot ● + MM:SS (white text)
- Reset button in header resets the timer to 0:00

### Track Locally (Browser Only via localStorage)
- Practice session date
- Total duration
- Segments completed
- Average WPM used

### CONSTRAINTS
- Use `localStorage` only
- No external services
- No analytics, tracking pixels, or network calls

---

## STEP 6 — RESPONSIVE DESIGN & ACCESSIBILITY

- Fully responsive: desktop, tablet, and large mobile
- Large-text presenter view (minimum 18px body text, 24px+ in Teleprompter mode)
- High-contrast in all modes
- All interactive elements keyboard-accessible
- Visible focus indicators on all buttons and inputs

---

## STEP 7 — DELIVERY FORMAT

Produce the final solution as a **single self-contained HTML file**.

### DELIVERABLES
One HTML file containing:
- HTML
- CSS
- JavaScript

Include:
- Clear inline comments explaining key logic
- A short **Usage** section at the top of the file (as an HTML comment) explaining:
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
