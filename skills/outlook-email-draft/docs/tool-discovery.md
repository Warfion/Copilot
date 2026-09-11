# Microsoft 365 Mail MCP: Discovery and Evidence

Updated 2026-09-12. This records the active remote integration and observed tests,
not a guaranteed schema or capability set for every future session.

## Integration

- Registration: existing VS Code user-level `Outlook Mail`, HTTP endpoint
  `https://agent365.svc.cloud.microsoft/agents/tenants/{tenant_id}/servers/mcp_MailTools`.
  Keep tenant and account identifiers out of this repository. Reuse the existing
  registration rather than adding a duplicate.
- Official catalog: [Microsoft MCP servers](https://github.com/microsoft/mcp).
- Observed identifier: `mcp_microsoft_mcp_CreateDraftMessage`. Discover the actual
  session-qualified tool and verify server identity and schema before invocation.
- Description: creates a draft in the signed-in user's mailbox without sending.
- Inputs: optional strings `subject`, `body`, `contentType`, and optional string
  arrays `to`, `cc`, `bcc`. Content type is Text or HTML. The skill supplies all
  six fields, requires subject/body, and defaults to Text.
- Name resolution: advertised during creation. No separate authenticated read-only
  resolver was found; one is optional. Prefer identity-established addresses with
  sources in the preview. Disclose unresolved names before approval, then review
  returned recipients. Matching counts alone do not establish correct identities.
- Other exposed operations include sending, updates, forwarding, replies, and
  attachments. None is permitted in this skill.
- Authentication and technical mailbox access are required, but the skill does
  not require a separate organizational attestation. Broader server permissions
  never authorize sending. Actual OAuth grants and additional server-side approval
  enforcement are unverified. Application-only authentication is outside scope.
  Tool filtering and skill instructions are not a server-side security boundary.

## Live Acceptance Tests

Five drafts were created on 2026-09-11, each after its own full preview and explicit
subsequent approval. Every response reported `data.draft: true` and `data.sent: false`.
No send, update, deletion, or attachment operation was performed.

| Test | Observed result |
| --- | --- |
| Text, no recipients | Empty To/CC/BCC; screenshot confirmed content and Drafts location |
| HTML, no recipients | Empty To/CC/BCC; screenshot confirmed bold/italic text, lists, paragraphs, umlauts, and escaped characters; folder and recipient fields were not visible |
| One recipient name | Expected To address returned; screenshot confirmed displayed recipient and content |
| Two names, one misspelled | Creation reported success but only one recipient was returned, without warning; omission was flagged and draft left unchanged |
| Two corrected names | New preview and approval; both expected To addresses returned; screenshot confirmed displayed recipients and content |

The responses included `data.messageId`, `data.webLink`, recipient arrays, and
untruncated bodies. The HTML body was wrapped in document elements while preserving
approved content. The name tests used Text with empty CC/BCC. Outlook display names
alone do not reveal addresses; address comparison used the returned values and
available user-provided identity evidence.

These observations demonstrate silent omission and successful resolution for the
tested names, not general ambiguity handling or automatic identity verification.
Nonempty CC/BCC resolution, broad limits/error behavior, and actual OAuth grants
remain unverified. Inspect every response rather than assuming these fields.

## Required Result Handling

Compare approved inputs and returned To/CC/BCC separately. If recipients are
missing, conflicting, or unverified, lead with "Draft saved; recipient verification
incomplete" when saving is confirmed. List inputs and returned addresses, explain
uncertainty without inventing mappings, and direct manual review/correction in
Outlook. Do not conceal the warning behind creation success or automatically
retry, update, delete, or recreate a draft.

[SKILL.md](../SKILL.md) defines the active contract. Automated tests check these
documents and packaging only, not remote execution or model compliance. Every
further live mailbox test requires a full preview and explicit approval.
