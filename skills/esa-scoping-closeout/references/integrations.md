# MCP integration contract

Discover tools before calling them. Names below are observed operation names,
not guaranteed prefixes. Read the actual schemas and do not invent arguments.
This document grants no permission to create a draft without the skill's full
preview and subsequent approval.

## Calendar and Teams

| Operation | Use and important constraints |
| --- | --- |
| Calendar `ListCalendarView` | Explicit start/end and time zone; expanded recurring instances; subject filtering |
| Calendar `ListEvents` | Title/attendee discovery; returns recurring masters, not sufficient for selecting an occurrence |
| Calendar `GetOnlineMeetingAiInsights` | Selected join URL, actual organizer ID when known, specific insight ID when needed |
| Calendar `GetOnlineMeetingTranscripts` | Same meeting, specific transcript IDs for matching recording segments |
| Calendar `GetOnlineMeetingAttendanceReports` | Select the matching report/occurrence; inspect truncation and supported limits |
| Teams `SearchTeamMessagesQueryParameters` | Precise KQL with customer keywords and date bounds; paginate within the window |
| Teams `SearchTeamsMessages` | Natural-language discovery when precise terms are unknown |
| Teams `ListChatMessages` / `GetChatMessage` | Read the selected meeting conversation and relevant attachments/links |

Use join URLs and organizer IDs returned by authenticated records, not guessed
values. If the organizer is unknown, disclose the default-user lookup limitation;
do not call the current user's ID the organizer's ID. A permission error is not
proof that a recap/transcript does not exist.

Honor result limits and continuation links. Attendance reports can be capped;
channel/recurring meetings can expose records from other sessions. The default
"latest" transcript/insight/report is not necessarily the chosen occurrence.

## Local assets and configuration

`settings.local.json` contains the user's approved attachment-source URL and
signature. It is ignored by git because a sharing URL can be access-bearing.
Do not put it in the customer email, publish it, or copy it into tracked examples.
Copy `settings.example.json` only as a starting point; placeholders block use.

From the skill directory:

```powershell
python .\scripts\prepare_assets.py
```

The JSON contains:

- `sourceFolder.url` and its `shareId` (the Graph `u!` base64url encoding);
- every local `attachments` entry with name, relative path, size, MIME type,
  SHA-256, SHA-1, and QuickXorHash;
- `signatureHtml`, containing only escaped configured text and a CID image;
- `inlineLogo`, a `#microsoft.graph.fileAttachment` payload with `contentBytes`,
  `contentId`, `contentType`, `isInline: true`, and name.

Only the 2.5 KB logo is encoded for transport. Do not emit megabytes of PDF/ZIP
base64 into model context. QuickXorHash is OneDrive's non-cryptographic version
comparison hash, not proof of authenticity or safe contents.

After reading the cloud items, save their actual metadata in a session scratch
JSON file, outside the repository, with this shape:

```json
{
  "files": [
    {
      "id": "ACTUAL_ITEM_ID",
      "name": "ACTUAL_FILENAME",
      "size": 123,
      "file": {
        "hashes": {
          "quickXorHash": "ACTUAL_RETURNED_HASH"
        }
      }
    }
  ]
}
```

Include every relevant item from the fully paginated folder listing. Do not
fabricate, recompute as if remote, or replace returned cloud hashes with local
hashes. Preserve IDs and version metadata separately for the attachment calls.

```powershell
python .\scripts\prepare_assets.py --cloud-metadata C:\absolute\session\cloud-files.json
```

The helper fails nonzero on missing/duplicate items, size/hash mismatches, or
missing supported hashes. `cloudComparison` confirms only metadata comparison,
not live access, binary download, or attachment delivery; those need actual tool
results. Extra cloud-only files are reported and not automatically attached.

## OneDrive or WorkIQ read-only preflight

If a connected dedicated OneDrive MCP exposes the needed read operations,
discover its schemas and use them. No specific dedicated OneDrive tool names
have been verified here. If unavailable/not capable, use connected WorkIQ.
Do not bypass an authorization denial through another provider or identity.

For WorkIQ:

1. Use `search_paths` to discover shared-folder and drive-item read paths and
   `get_schema` where needed. Do not call permission-grant or redeem actions.
2. Resolve `/shares/{shareId}/driveItem` with `$select=id,name,folder,parentReference,webUrl`.
   Encode the full configured URL; the helper supplies the `shareId`.
3. Require a folder result and returned drive/item IDs. Read
   `/drives/{driveId}/items/{folderId}/children` with a bounded `$top` and
   `$select=id,name,size,file,folder,parentReference,webUrl,eTag`.
   Follow returned continuation links and relevant subfolders.
4. Read each selected `/drives/{driveId}/items/{itemId}` individually with the
   same necessary metadata. Check status, hashes and versions; record the live
   ETag rather than using historical IDs as evidence of access.
5. Compare against current local assets with the helper. If an ETag changes
   between reads, re-read and reconcile rather than mixing snapshots.

Use relative paths with WorkIQ and only the fields required. Do not request
signed download URLs or large binary responses for a metadata check. Reject
unexpected hosts or credential-bearing links as attachment sources.

## Mail draft and file attachments

Only after approval, call `CreateDraftMessage` once with:

```json
{
  "to": ["APPROVED_EXPLICIT_ADDRESS"],
  "cc": [],
  "bcc": [],
  "subject": "APPROVED_SUBJECT",
  "body": "EXACT_APPROVED_HTML",
  "contentType": "HTML"
}
```

Use all approved recipients in their approved fields. Require a nonempty,
single-line subject and nonempty body. Keep the inherited workflow limits of
255 subject characters, 100,000 body characters, and 100 addresses per field;
these are workflow bounds, not independently established server limits.
Review metadata and sender/mailbox overrides are not input fields.

Once draft creation and recipient readback succeed, use the tested Mail
`UpdateDraft` attachment-only operation. Its payload must contain exactly:

```json
{
  "messageId": "EXACT_RETURNED_DRAFT_ID",
  "attachmentUris": ["AUTHENTICATED_FILE_WEB_URL"]
}
```

Populate the list from each approved drive item's returned HTTPS `webUrl`, using
the verified SharePoint/OneDrive file URLs. Never use the folder URI, a signed
download URL, or a fabricated link. Omit all other optional fields, especially
body, subject, to, cc, bcc, sensitivity and directAttachments. Do not pass empty
strings or arrays for fields intended to stay unchanged.

This exact combination succeeded for all four baseline files in one call on a
fresh draft, including the 33,137-byte ZIP, both sub-3-MB PDFs and the
3,897,972-byte Scoping PDF. All were real non-inline file attachments and passed
downloaded-byte verification. The inline PNG was added separately through WorkIQ.
An approved repair must read the inventory first and include only missing approved
files; preserve existing IDs and never repeat the upload just to test another file.

The desired result is **real file attachments**, not reference attachments.
The tool's URI input does not prove which type it creates: check the result and
read back every attachment. If it creates only links, stop and report the draft
as incomplete. Do not quietly substitute body links or claim delivery succeeded.

`UploadAttachment` and `UploadLargeAttachment` expose base64 inputs (the latter
for 3-150 MB), but a multi-megabyte string is not a practical model-context
fallback. Do not fabricate a local-path argument, upload files elsewhere, or
switch transport automatically when the approved cloud-source route fails.

Account for both Graph's file-size limits and the MCP request-body limit.
Base64 alone requires `4 * ceil(fileBytes / 3)` bytes, before JSON overhead.
A chunked Graph upload does not solve a front-end HTTP 413 if the MCP still
requires the entire base64 file in one request. Do not retry the same payload
or route it to `UploadLargeAttachment` merely because the small tool returned
413. The tool name is not evidence of streaming from the agent to the MCP.

The live URI attachment operation failed with "Attachment size must be greater
than the minimum size" both for the mixed baseline set and for a separately
approved test containing only the 3,897,972-byte Scoping PDF. Both used Graph
drive-item URIs accepted by the advertised tool schema. This disproves the
assumption that only small source files cause this failure; it does not establish
the connector's underlying defect. A later, separately approved test succeeded
with `UpdateDraft` and returned SharePoint web URLs. Both the operation and URI
representation changed, so success does not isolate which difference fixed the
earlier failure. Do not treat the two combinations as interchangeable.

The standard must use one validated URI-based connector route for all non-inline
ESA files, with size-dependent handling inside the connector, not a permanent
mixture of providers in the skill. Select the tested `UpdateDraft` plus file
`webUrl` combination, and keep per-file verification mandatory. The complete
fresh-draft attachment workflow was verified for the baseline inventory, not for
arbitrary future files or changed service behavior. Do not duplicate existing
attachments to test a route or silently downgrade to links. Never fabricate chunks
or split a customer PDF into separate attachments to get around a transport limit.

## Inline logo via WorkIQ

Mail's observed upload schemas do not expose `isInline` or `contentId`.
Use WorkIQ only for the approved logo and readback, not a send operation.

Discover `/me/messages/{message-id}/attachments` with `search_paths`, then its
create schema with `get_schema`. The observed schema exposes the Graph base
attachment type, including `isInline` and `@odata.type`. Microsoft's
[fileAttachment contract](https://learn.microsoft.com/en-us/graph/api/resources/fileattachment?view=graph-rest-1.0)
documents the derived `contentBytes` and `contentId` properties.

The inline-logo operation succeeded during the live troubleshooting run below.
A base-type schema alone is still not evidence that another provider or version
accepts every derived field. If current validation/capabilities rule out the
payload, stop before creation. Disclose any unverified step in the preview and
verify the actual result after approval. Never label unsupported fields as verified.

Before writing, use a discovered WorkIQ read path for the **exact returned Mail
draft ID** in `/me/messages`. Confirm the subject, complete recipient lists,
body and `isDraft` agree with the approved draft. If WorkIQ cannot read that draft
or account identity conflicts, stop before cross-provider mutation.

Use `create_entity` with the discovered attachment collection as `parentUrl`,
and the helper's `inlineLogo` object as `jsonBody`. The body already references
`cid:esa-signature-logo`; its file attachment must have exactly that `contentId`,
`image/png`, and `isInline: true`. Normal name-only attachment upload is not an
inline substitute. Do not place raw base64 in an HTML data URI.

No changes to the email body should be needed after creation. Do not use
`UpdateDraft` to silently repair a changed signature or body.

## Final readback and partial failures

Use Mail `GetMessage`/`GetAttachments`, or discovered WorkIQ read operations, to
inspect the same draft. Start with metadata; download the attachments separately
for byte verification without placing large binary payloads in model context.

Require:

- `isDraft` or an equivalent explicit draft indicator, with no contradictory
  sent state; absence of a send call alone is not response-level verification;
- exact approved subject, recipients by To/CC/BCC, and semantically unchanged
  HTML (provider normalization is acceptable, missing content is not);
- every approved non-inline file with its expected name and evidence of
  `#microsoft.graph.fileAttachment` (or provider-equivalent real file type);
- one inline PNG with the correct name and the Content-ID used in the body,
  established by the creation result or subsequent readback;
- decoded byte length and SHA-256 matching each approved local file, including
  the inline PNG, from downloads of the exact returned attachment IDs;
- no unexpected attachment, reference-only substitute, or unresolved recipient.

Outlook attachment `size` is not necessarily the original file's byte length.
In this run it reported 2,714 bytes for the 2,485-byte PNG and 33,389 bytes for
the 33,137-byte ZIP; both downloaded files matched their original SHA-256.
Keep that reported value as metadata; compare **decoded content**, not a guessed
overhead subtraction. This exception does not weaken drive-item size comparison:
the cloud-source preflight must still match local file sizes and hashes.

Save the complete actual `DownloadAttachment` response as session scratch JSON,
outside the repository. The helper accepts its `{"data": {...}}` envelope or a
Graph file-attachment object containing `id`, `name`, `contentType`, and
`contentBytes`. Repeated flags verify multiple files:

```powershell
python .\scripts\prepare_assets.py --attachment-download C:\absolute\session\logo-download.json --attachment-download C:\absolute\session\zip-download.json
```

This is local verification of supplied evidence, not a new authenticated read.
Bind the downloaded IDs to the current draft's attachment inventory separately.
Never substitute local file bytes for the returned `contentBytes`. Use the full
structured response or raw tool content, not a shortened `sessionLog` or preview:
large logs may insert `<output too long - dropped ...>` inside base64.
Invalid, missing, truncated, or mismatched content fails nonzero. Do not remove
truncation markers or disable strict base64 validation to make a check pass.

If response fields are absent, read them through a discovered operation if
available. If they still cannot be established, report verification incomplete.
Never infer complete delivery from matching counts or from creation success.
Report an actual returned HTTPS Outlook link only after validating its host.
Known public hosts are exactly `outlook.office.com`, `outlook.office365.com`,
`outlook.live.com`, and the live-verified Outlook host `emea.mail.microsoft.com`;
reject credentials, lookalike suffixes, and unexpected
ports. An unfamiliar sovereign-cloud host requires explicit verification.

On any ambiguous mutation result, stop without retrying; the operation may have
succeeded remotely. Preserve the existing draft. Repairs or a new attempt need
inspection of its current state, a new complete preview, and fresh user approval.
Do not delete an incomplete draft as cleanup.

## Evidence and limitations

On 2026-09-25, WorkIQ resolved the owner's configured folder, listed the four
files, and read each item with HTTP 200. All local/cloud sizes and QuickXorHashes
matched. This was a read-only metadata check, not a binary download or a draft
creation/attachment test. It is historical evidence only; repeat preflight.

The OneDrive MCP was configured for a future session but was not loaded during
authoring. Do not restart the user's session to activate it.

Later on 2026-09-25, the live draft contained the original inline PNG and ZIP.
Read-only downloads confirmed their exact byte lengths and SHA-256 hashes;
the PNG's returned Content-ID matched the HTML and `isInline` was true.
This proves those bytes and metadata, not visual rendering in Outlook.
The 1,766,938-byte Data Gathering PDF upload through Mail failed with HTTP 413
"Payload Too Large"; this establishes a failure at that payload size, not an
exact universal transport limit. Readback confirmed all three PDFs were absent
and the original message remained a draft.

At 16:00 UTC on 2026-09-25, a newly approved `AddDraftAttachments` test supplied
only the Scoping PDF's authenticated Graph drive-item URI. Source access, size
and hash were rechecked before the call. It again failed while creating the
upload session with "Attachment size must be greater than the minimum size."
Subsequent readback confirmed the same draft ID, unchanged subject, body and
recipients, and the same two attachment IDs (PNG and ZIP). No PDF was added.
No further writes were attempted after this failure. This is a failed uniform
route qualification test, not an attachment repair or proof of a size-only cause.

At 19:11 UTC on 2026-09-25, after explicit user approval, the temporary session
adapter allowed one attachment-only `UpdateDraft` call for the existing draft
and the three exact verified SharePoint PDF URLs. Its on-disk single-use record
prevents reloading the extension from restoring that allowance. The normal
tool permission checks, no-send, no-delete, and no-content-change guards remained
active. The local adapter is not a required installation component of this skill.

The call succeeded. Readback established the same draft ID, subject, sender and
To/CC/BCC; HTML text, links and logo reference were unchanged, with provider-only
formatting normalization. All three PDFs were real non-inline file attachments.
The existing PNG and ZIP retained their IDs. Fresh downloads of all five files
matched their local byte lengths and SHA-256 hashes, and the message remained a
draft. That repair verified the three-PDF route but did not yet exercise ZIP
delivery via `UpdateDraft`; the subsequent fresh-draft run below did.

At 19:23-19:26 UTC on 2026-09-25, the user explicitly requested a second identical
draft. A normal `CreateDraftMessage` call created it, one attachment-only
`UpdateDraft` call added all four verified SharePoint file URLs, and an ordinary
WorkIQ `create_entity` call added the original PNG bytes with the matching CID.
No pinned repair allowance or local-byte substitution was used for the new draft's
writes. All five downloaded attachments matched their local byte lengths and
SHA-256 hashes. Subject and To/CC/BCC matched the original. The HTML matched exactly
after ignoring only Outlook's diagnostic `data-outlook-trace` attribute, including
all presentation styles and content. The original draft and attachments remained
unchanged, and both messages remained drafts.

This verifies complete fresh creation and attachment delivery for the baseline
materials, including the ZIP and inline logo. It is not a pixel-level rendering
test in every Outlook client or a guarantee of future permissions/service health.
Future runs still require current access checks and explicit approval.

Further repairs require inspection, a complete preview and explicit approval.
An unavailable user or an instruction to continue autonomously is not that
specific approval. Preserve an incomplete draft and stop writes after failure;
offline tests and a hash-verified upload input do not establish delivery.
