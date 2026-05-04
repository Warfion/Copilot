# OneDrive Organizer

## Purpose
A read-only inventory and cleanup workflow that scans your entire OneDrive, categorizes files by age, relevance, customer, and product — then produces an interactive HTML dashboard, a detailed inventory table, and a reorganization plan. Nothing is modified until you explicitly approve.

Best used with: Microsoft 365 Copilot Cowork

---

## Prompt

Create a read-only inventory and cleanup/reorg proposal for my ENTIRE OneDrive, then produce (1) an executive-style interactive HTML summary and (2) a detailed reorganization plan. Do NOT modify, rename, move, or delete anything until I explicitly approve.

---

### Scope (ENTIRE OneDrive)

Analyze all folders and files in my OneDrive, except:
- Any folder whose name includes: Legal, HR, Payroll, Private, Confidential, PII, Personal, Medical
- Any file whose name includes: password, credentials, secret, key, token

If you cannot access certain areas due to permissions, clearly list what you couldn't scan.

---

### Method (important for "whole OneDrive")

Because the dataset may be large, do this in stages:

**Stage A — Inventory pass:**
- Build an inventory by scanning top-level folders first, then recursively scanning subfolders.
- If you hit limits, continue by sampling systematically: for each top-level folder, sample the newest 50 and oldest 50 items plus the 50 largest items (if size available), and explain that you sampled.
- Always label whether results are COMPLETE or SAMPLED.

**Stage B — Categorization & scoring:**

For each file, compute:
- **Age bucket:** <90 days, 3–12 months, 1–2 years, 2–5 years, >5 years
- **File type:** extension
- **Relevance score (0–100)** using:
  - +30 modified in last 90 days
  - +20 shared/linked recently (if available)
  - +20 appears to be "active work" (folder contains FY/Q/Project/Customer/Eng/Architecture/Security/SOC)
  - +10 belongs to templates/standards/reference
  - -30 older than 2 years AND not shared AND not recently modified
- **Customer detection (confidence 0–1):**
  Prefer folder names and filename prefixes (CustomerName_, CUST-, Account-, "-" separators).
  If content inspection is available, only use headings/first page; do not extract sensitive content.
- **Product detection (confidence 0–1):**
  Use folder/filename keywords. If uncertain, leave blank rather than guessing.
- **Duplicates:**
  Flag likely duplicates by name similarity (v1/v2/final/final2), and same size/date patterns (if available).

---

### Deliverable 1 — Inventory Table (pasteable)

Output a table with:

Path | File name | Type | Size (if available) | Created | Modified | Age bucket | Customer (conf) | Product (conf) | Relevance score | Duplicate group | Recommended action (Keep/Archive/Review/Delete-candidate)

---

### Deliverable 2 — Executive HTML Dashboard (copy-paste single file)

Create ONE self-contained HTML file (no external libraries) with 6 "screens" (sections) and light animations:

1. **Executive overview:** totals, key risks, quick wins
2. **Age distribution chart** (hover tooltips)
3. **File type distribution chart**
4. **Customer & product breakdown** (filter chips)
5. **Hotspots:** largest folders, duplicate clusters, "stale but shared" items (if available)
6. **Prioritized recommendations:** Top 10 actions ranked by Impact/Effort

Keep it:
- Under 5 scrolling screens for the overview + a 6th for recommendations
- Accessible colors, keyboard navigable, and readable (no gimmicks)
- Works offline (no CDN)

---

### Deliverable 3 — Reorganization Plan (written)

Include:
- **Proposed folder structure** (with rationale and naming conventions)
- **Move/consolidate plan:** from → to (grouped by customer/product/topic)
- **Delete candidates:** list the exact paths that SHOULD be renamed with prefix "DELETE_" IF I approve
  (Do NOT rename anything now; just produce the list.)
- **Archive plan:** Archive/YYYY/Customer/Product (or similar)
- **Risks/mitigations:** retention, legal hold, shared links, and "do-not-touch" categories

---

### Approval Gate

Stop after providing Deliverables 1–3. Ask me to approve before any changes. Do not perform modifications.
