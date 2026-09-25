# Prompt Collection

A personal collection of prompts and skills for Copilot, Copilot Cowork,
Researcher, and other agents.

Browse the `prompts/` folder for ready-to-use prompts organized by agent.

## What's Inside

| Agent | Prompt | Description |
| --- | --- | --- |
| Copilot Cowork | [Achievement Synthesizer](prompts/Coworker/achievement_synthesizer.md) | Gathers evidence of your accomplishments and synthesizes them into an executive-quality package |
| Copilot Cowork | [Postmaster](prompts/Coworker/postmaster.md) | Scans your inbox, identifies workload themes, and recommends email rules to reduce noise |
| Copilot Cowork | [Script Practice Builder](prompts/Coworker/scriptpractise.md) | Turns a presentation script into a browser-based rehearsal app with 5 practice modes |
| Copilot Cowork | [OneDrive Organizer](prompts/Coworker/onedrive_organizer.md) | Scans your entire OneDrive, produces an interactive HTML dashboard, inventory table, and reorganization plan |
| Copilot Cowork | [Weekly Status Report](prompts/Coworker/weekly_status_report.md) | Generates a fact-based weekly status report from your Outlook, Teams, and Calendar activity |
| Copilot Cowork | [Focus Time Planner](prompts/Coworker/focus_time_planner.md) | Reviews upcoming weeks and proposes focus-time blocks, without calendar changes until approval |
| Copilot Cowork | [Capacity Report](prompts/Coworker/capacity_report.md) | Reviews two upcoming work weeks, classifies meetings by category, and drafts an HTML capacity summary email |
| Any LLM | [Prompt Techniques Toolkit](prompts/VSCode/prompt_techniques.md) | Four reusable prompt strategies: Guided Q&A, Pros & Cons, Stepwise Chain of Thought, and Role-Based Teaching |

## Skills

Each skill lives in its own folder under `skills/` as a self-contained `SKILL.md`.
Skill-specific workflow, safeguards, and usage examples are kept in that file
rather than in separate skill READMEs or supporting folders.

| Skill | Description |
| --- | --- |
| [Outlook Email Draft](skills/outlook-email-draft/SKILL.md) | Uses Agency-provided Microsoft 365 Mail MCP to save reviewed emails as Outlook drafts; never sends |
| [Git Commit and Push](skills/git-commit-push/SKILL.md) | Stages, commits, and pushes changes with confirmation and repository safety checks |

The workspace configures `skills/` for VS Code Local agent discovery. Other agent
hosts may require installation in a standard project or personal skill location.
See each skill's documentation for setup.

## Language

Project documentation, instructions, and code are maintained in English. Outlook
Email Draft supports German and English emails independently of the project's
language. An explicit requested email language takes precedence over the source
language; otherwise the email follows the language of the user's request.
