# Content and evidence guide

## What the examples establish

`Template1.msg` is a short German post-scoping follow-up with the four file
attachments and a signature. `Template2.msg` is a detailed English follow-up
covering the assessment, process, data gathering, scope, and next steps.
Use Template 2's structure in either language, not its literal customer facts.

Both original messages contain real example recipients and dates. They are
reference material, not recipients or evidence for a new engagement. The
template signature address differs from its sender header; the owner explicitly
confirmed the signature spelling in `settings.local.json`.

The standalone `Knowledge\Templates\Microsoft.png` is the same PNG embedded
in both examples: 115 x 28 pixels, originally displayed at 114 x 27. It belongs
above the signature text. Do not substitute a text-only signature, a remote
logo URL, or a normal downloadable PNG attachment.

The structure is distilled here so normal use does not require an Outlook MSG
parser or opening Outlook. Read the original messages only when the user asks
to change the template interpretation or presentation.

## Suggested structure

| Section | Include |
| --- | --- |
| Subject | Scoping result/follow-up, customer, Enterprise Security Assessment (ESA), meeting date; localize the wording |
| Greeting and thanks | Appropriate customer greeting and reference to the actual selected call |
| Assessment overview | Purpose and relevant documented deliverables, without claiming every item was explicitly agreed |
| Agreed scope | Confirmed tenant, subscriptions, applicable data sources, exclusions, and open scope points |
| Process | Data gathering, Microsoft analysis/integration, and presentation of results |
| Data-gathering instructions | Explain the attached guides and ZIP; give only instructions supported by the supplied documentation |
| Required access | Relevant read permissions; distinguish documentation requirements from confirmed customer access |
| Attachments | List every approved file by its exact filename and useful purpose |
| Responsibilities and next steps | Confirmed owners, dates, dependencies, and unresolved items; no invented deadlines |
| Data return | Confirmed secure-transfer instructions, or say details will be arranged separately |
| Closing and signature | Offer the documented support, localized closing, exact configured signature and original inline logo |

Do not fill every section mechanically. Omit irrelevant detail, not material
conflicts or commitments. Dates not agreed can be described as to be arranged.
Do not reuse "last week" or any other relative date from the examples.

## Documented ESA baseline, not customer agreements

The supplied Scoping PDF establishes these general service facts:

- Assessment data sources: Microsoft Cloud Security Benchmark (MCSB), Defender
  for Cloud Secure Score recommendations, Microsoft Secure Score, and Microsoft
  Purview Compliance Manager improvement actions.
- The documented service is single-tenant and data-based; it does not include
  remediation of findings.
- The process is customer data gathering, Microsoft data review and integration
  into a Power BI dashboard, then presentation of findings and recommendations.
- Documented outputs include the Power BI dashboard, prioritized recommendations/
  proposed roadmap, and an executive summary.
- The standard results meeting is described as two hours. This is not an agreed
  appointment or duration for a specific customer unless confirmed.

These facts come from the Scoping PDF pages 7-8 and 14-16. If the actual meeting
appears to promise a different service boundary, ask the user to reconcile it.

The Data Gathering PDF, pages 27-28, specifies four exported files (three CSV
and one Excel file), unmodified, with secure-score values/screenshots and secure
transfer provided by the CSA. Do not simplify this to "four CSV files."
Do not invent output filenames or a claim that every export is automated.
The supplied ZIP contains PowerShell/KQL assets; it is provided to the customer,
not executed by the agent.

Template 2 mentions Azure Reader, Entra Global Reader/Security Reader, and Purview
Compliance Manager Reader. Treat example wording as a guide to what to verify,
not an authoritative minimum-privilege permission specification. Use the current
attached instructions for applicable tasks, or ask if the sources conflict.

## File purposes

| Filename | Purpose |
| --- | --- |
| Enterprise Security Assessment - Data Gathering.pdf | Customer export/data-gathering instructions |
| Enterprise Security Assessment - Power BI Refresh.pdf | Refreshing the resulting Power BI report |
| Enterprise Security Assessment - Scoping.pdf | Service overview, scope, outputs, and next steps |
| ESA Data Gathering Tool.zip | Supplied export/wrapper tooling; never run it while drafting |

All four are attached even when an example email listed fewer. Additional local
attachment files must be inventoried and included in the approval review, not
silently skipped. The logo is an additional inline asset, not one of these four.

## Data handling

Do not ask customers to email secrets or grant broad access. Never claim that
possession of a SAS token restricts a download to a named person. If secure
transfer details are absent, use a neutral statement equivalent to "We will
arrange the secure transfer details separately." Do not invent a URL, account,
token, permission grant, or a transfer commitment with an unconfirmed date.

Customer-facing mail must not contain internal chat assessments or unrelated
commercial discussions. Put evidence citations and uncertainty in the review
notes; put only relevant, confirmed customer-appropriate content in the email.
