# ESA Scoping Closeout

A standalone agent skill that turns a customer's ESA scoping meeting into a
reviewed Outlook draft, with all supplied assessment files and the original
Microsoft signature logo. It never sends mail.

## Use

Ask the agent:

> Create an ESA scoping closeout draft for CUSTOMER.

Or provide a date, meeting title, or Teams link:

> Draft the ESA scoping follow-up for CUSTOMER from our meeting on DATE, in German.

If the customer is missing, the skill asks. It searches the previous 14 days by
default and asks you to select among plausible meetings. It retrieves available
recap and transcript, resolves conflicts with you, and previews the complete
email before requesting permission to save it.

The email is a new standalone message using Template 2's detailed structure.
The language follows your explicit request, otherwise the meeting. Recipients
are the union of verified attendees and invitees: Microsoft people in CC, all
other people in To, excluding the sender. No addresses or commitments are guessed.

If neither recap nor transcript is usable, it first shows the information from
the invitation/chat, then asks for your notes before drafting.

## Installation and configuration

The repository configures `skills\` for VS Code Local discovery. Other hosts may
require copying this **entire folder**, including `Knowledge`, references,
scripts, and private settings, to their supported skill location.
On Windows, a personal Copilot CLI location is
`%USERPROFILE%\.copilot\skills\esa-scoping-closeout`.
Do not install it or restart a session automatically.

Required:

- Python 3.10+ for the local asset-preflight helper; no Python packages needed.
- Connected, authenticated Teams, Calendar, Mail, and WorkIQ MCP tools.
- OneDrive MCP is optional for file discovery/access checks; WorkIQ already
  supports that route. Being configured in a catalog is not the same as loaded.
- Local reference assets and the user's `settings.local.json`.

This worktree has the owner's confirmed settings already populated. For another
installation, copy `settings.example.json` to `settings.local.json` and replace
every placeholder with the approved attachment-folder URL and signature details.
The local settings are intentionally gitignored: a sharing link can grant access.
They are not included in a normal git clone and must be configured there.
Never include this source link in the customer email or change its permissions.

The current owner's chosen signature email is `thomas.brundl@microsoft.com`,
intentionally different from some example sender headers. The logo is
`Knowledge\Templates\Microsoft.png`; it is not retrieved from Outlook settings.
No mailbox search is needed to generate the signature.

## Included assets

| Location | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Runtime workflow and approval boundaries |
| [Content guide](references/content-guide.md) | Distilled templates and sourced service facts |
| [Integration contract](references/integrations.md) | Discovered MCP contracts, preflight, and failure behavior |
| `Knowledge\Templates\Template1.msg` | Short German reference email |
| `Knowledge\Templates\Template2.msg` | Detailed English reference email |
| `Knowledge\Templates\Microsoft.png` | Original inline signature logo |
| `Knowledge\Attachments` | Three required PDFs and the data-gathering ZIP |
| [Asset helper](scripts/prepare_assets.py) | Local metadata, cloud/download hash checks, and small logo payload |

The original MSG files contain real example customer information; do not publish
them indiscriminately. The PDFs carry distribution restrictions. Their owner
confirmed approval for these ESA customer engagements, not unrestricted reuse.
The agent must not execute the supplied PowerShell/KQL files inside the ZIP.

## Access and approval

Every run resolves the configured cloud folder, lists its contents, and reads
each expected file item before any draft or attachment write. Local/cloud sizes
and hashes must match. Missing access, missing files, and changed versions stop
the workflow. Additional local files must also appear in the approval inventory.

The customer gets actual file attachments, not cloud-sharing links. The logo is
an additional inline attachment. If file or logo delivery fails or cannot be
verified, the result is incomplete, even if an Outlook draft already exists.
The skill preserves that draft and does not automatically retry or delete it.

The preview includes recipients, subject, full readable body and exact HTML,
signature/logo, attachment names/sizes, source evidence, and any integration
uncertainty. Explicit approval of that exact preview is required in a subsequent
response. Changes invalidate approval. Sending remains manual in Outlook.

## Offline verification

From the repository root:

```powershell
python -m unittest discover -s .\skills\esa-scoping-closeout\tests -v
```

From the skill directory:

```powershell
python .\scripts\prepare_assets.py
python .\scripts\prepare_assets.py --cloud-metadata C:\absolute\session\cloud-files.json
python .\scripts\prepare_assets.py --attachment-download C:\absolute\session\attachment-download.json
```

Tests use the Python standard library. They cover local inventory, hash
calculation/comparison, downloaded-byte integrity, signature escaping, logo encoding, failure cases, and
document contracts. They do not contact Microsoft 365, execute the ZIP, create
drafts, or prove remote permissions.

The baseline-file and logo tests pin the supplied assets' hashes. When deliberately
replacing those materials, first confirm the new files and their distribution
approval, then update the corresponding test expectations. Do not change expected
hashes just to conceal an unexplained local/cloud mismatch.

The complete fresh-draft workflow was verified on 2026-09-25: Mail
`CreateDraftMessage` created a second draft, Mail `UpdateDraft` with only
`messageId` and `attachmentUris` added all three PDFs and the ZIP using authenticated
SharePoint file `webUrl` values, and WorkIQ added the inline logo. No pinned repair
allowance or local-byte substitution was used for these writes. Downloads of all
five attachments matched local byte lengths and SHA-256 hashes.

Use that single URI-based connector route for non-inline ESA files, not a
permanent mixture of providers. The new message matched the source draft's subject,
recipients, content and presentation styles; only Outlook's diagnostic image-trace
attribute differed. The original stayed unchanged and neither message was sent.
This establishes the baseline workflow, not a guarantee for all future files,
permissions or service changes. Every run still needs explicit approval and
complete readback. No duplicate upload is allowed just to test it.

Earlier `AddDraftAttachments` calls with Graph drive-item URIs failed with an
upload-session minimum-size error, even for the large Scoping PDF; direct Mail
base64 upload of the Data Gathering PDF hit HTTP 413. These are not the successful
combination. See the integration contract for the precise payload and evidence.

Readback must verify actual downloaded bytes, not merely Outlook's attachment
`size`, which can include overhead. The helper's repeatable `--attachment-download`
option checks complete Mail/Graph download JSON against local sizes and SHA-256.
Keep those responses in session scratch storage. Truncated logs, input hydration,
matching names, or successful metadata checks are not proof of complete delivery.
