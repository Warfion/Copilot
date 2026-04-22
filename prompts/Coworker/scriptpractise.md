Goal:
Build an interactive web app that helps me practice and rehearse my presentation script for the event: <event>.

Context:
I will present this session live and want a lightweight practice tool that improves pacing, confidence, and flow. 
The app is for personal rehearsal only and must run locally in a browser with no backend or external services.

Source:
Use the following presentation script as the single source of truth:
<script>

Expectations / Output:
- Produce a single, self-contained HTML file (HTML + CSS + JavaScript in one file).
- The file must run locally by opening it in a browser (no build step, no network calls).

App Features:
1. Script Practice
   - Display the script in clear, readable sections.
   - Highlight the current line or section being practiced.
   - Allow moving forward/backward between sections.

2. Practice Modes
   - Teleprompter mode with adjustable auto-scroll speed.
   - Chunk practice mode (one section at a time, hide/reveal text).
   - Timer showing total practice time and estimated words-per-minute.

3. Presenter Support
   - Optional pause markers and emphasis markers within the script.
   - Large-text “presenter view” for distance reading.
   - Keyboard shortcuts for start/stop, next/previous section, speed control.

4. Progress Tracking (Local Only)
   - Store practice history (date, duration, completed sections) in browser localStorage.
   - No external storage or analytics.

5. Accessibility & Usability
   - Responsive layout (desktop/tablet).
   - High-contrast, readable design.
   - Clear inline comments in the code explaining key parts.

Deliverables:
- The complete HTML code in one block.
- A short usage section at the top of the file explaining how to:
  - Paste a new script
  - Adjust practice settings
  - Run the app locally
