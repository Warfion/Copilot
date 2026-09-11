import { existsSync, readFileSync } from 'node:fs';
import { basename, dirname, resolve } from 'node:path';
import { parse } from 'yaml';
import { expect, it } from 'vitest';

const skillPath = resolve('SKILL.md');
const skill = readFileSync(skillPath, 'utf8');

it('has valid discoverable frontmatter and a matching folder name', () => {
  const frontmatter = /^---\r?\n([\s\S]*?)\r?\n---/u.exec(skill);
  expect(frontmatter).not.toBeNull();
  const metadata = parse(frontmatter![1]!);
  expect(metadata.name).toBe(basename(dirname(skillPath)));
  expect(metadata.description).toMatch(/draft an email.*Outlook Drafts/u);
  expect(metadata.description).toContain('German');
  expect(metadata.description.length).toBeLessThan(1024);
});

it('requires preview, explicit approval, context honesty, and no sending', () => {
  for (const text of ['To:', 'CC:', 'BCC:', 'Subject:', 'Body:', 'Context sources used:',
    'Assumptions:', 'Missing information:', 'Would you like me to create this message in Outlook Drafts?',
    'prior approval is invalid', 'Never send an email', 'Do not call any mailbox-changing tool before approval',
    'does not independently access Microsoft 365 data', 'The email was saved as a draft and was not sent.',
  ]) expect(skill).toContain(text);
  expect(skill).not.toContain('\u2014');
});

it.each(['customer-follow-up', 'internal-update', 'german-email'])('includes a complete %s preview', (name) => {
  const example = readFileSync(`examples/${name}.md`, 'utf8');
  for (const label of ['Integration: Microsoft 365 Mail MCP', 'Target:', 'Body type: Text',
    'To:', 'CC:', 'BCC:', 'Subject:', 'Body:', 'Context sources used:', 'Assumptions:', 'Missing information:',
    'Would you like me to create this message in Outlook Drafts?',
  ]) expect(example).toContain(label);
  expect(example).not.toContain('\u2014');
  expect(example).toContain('contentType: Text');
  expect(example).not.toMatch(/bodyType|approval\s+form/iu);
});

it('documents an HTTP MCP connection without credentials or tenant-specific values', () => {
  const readme = readFileSync('README.md', 'utf8');
  const jsonBlock = /```json\r?\n([\s\S]*?)\r?\n```/u.exec(readme);
  expect(jsonBlock).not.toBeNull();
  expect(JSON.parse(jsonBlock![1]!)).toEqual({ servers: {
    'Outlook Mail': {
      type: 'http',
      url: 'https://agent365.svc.cloud.microsoft/agents/tenants/{tenant_id}/servers/mcp_MailTools',
    },
  } });
  for (const text of ['MCP: Open User Configuration', 'MCP: List Servers',
    'Configure Tools', 'MCP: Add Server', 'Preserve every other entry',
    'placeholder is not resolved automatically', 'without creating a message',
  ]) expect(readme).toContain(text);
});

it('keeps English documentation separate from German and English email output', () => {
  const normalized = skill.replace(/\s+/gu, ' ');
  expect(normalized).toContain('Project documentation, instructions, and code are written in English.');
  expect(normalized).toContain('support German and English emails');
  expect(normalized).toContain('An explicit requested email language takes precedence');
  expect(normalized).toContain("otherwise use the language of the user's request");
  const germanExample = readFileSync('examples/german-email.md', 'utf8');
  expect(germanExample).toContain('# German Email Draft');
  expect(germanExample).toContain('Fictional context:');
  expect(germanExample).toContain('Guten Tag,');
  expect(germanExample).toContain('Subject: Nachbesprechung:');
  expect(readFileSync('examples/customer-follow-up.md', 'utf8')).toContain('Hello,');
});

it('has development-only tooling and uses only the remote draft workflow', () => {
  const manifest = JSON.parse(readFileSync('package.json', 'utf8'));
  expect(manifest.dependencies ?? {}).toEqual({});
  expect(manifest.scripts).toEqual({ test: 'vitest run', lint: 'eslint tests' });
  const lockfile = JSON.parse(readFileSync('package-lock.json', 'utf8'));
  expect(lockfile.packages[''].dependencies ?? {}).toEqual({});
  expect(lockfile.packages[''].devDependencies).toEqual(manifest.devDependencies);
  for (const removed of ['src', 'dist', '.env.example', '.vscode/mcp.json',
    'tsconfig.json', 'docs/architecture-decision.md']) {
    expect(existsSync(removed), `Obsolete path: ${removed}`).toBe(false);
  }
  expect(skill).toContain('No automatic fallback');
});

it.each(['../../README.md', 'README.md', 'SKILL.md', 'docs/tool-discovery.md',
  'examples/customer-follow-up.md', 'examples/internal-update.md', 'examples/german-email.md',
])('keeps %s links valid and free of obsolete setup instructions', (document) => {
  const content = readFileSync(document, 'utf8');
  expect(content).not.toMatch(/create_outlook_draft|OUTLOOK_DRAFT_BACKEND|OUTLOOK_CLASSIC_MAILBOX|npm run (?:build|login|logout)|Retained local|\.github\/skills\/outlook-email-draft/iu);
  for (const match of content.matchAll(/\[[^\]]*\]\(([^)]+)\)/gu)) {
    const target = match[1]!;
    if (URL.canParse(target) || target.startsWith('#')) continue;
    const linkPath = resolve(dirname(resolve(document)), decodeURIComponent(target.split('#')[0]!));
    expect(existsSync(linkPath), `Broken link in ${document}: ${target}`).toBe(true);
  }
  if (document === '../../README.md') {
    expect(content.match(/^# Prompt Collection$/gmu)).toHaveLength(1);
  }
});

it('maps exactly the six remote input fields without local metadata', () => {
  const contract = skill.split('## Remote draft contract')[1]!.split('## Confirmation')[0]!;
  const fields = [...contract.matchAll(/^\| `([^\n]+?)` \|/gmu)].flatMap((match) => match[1]!.split('`, `'));
  expect(fields).toEqual(['to', 'cc', 'bcc', 'subject', 'body', 'contentType']);
  expect(skill).toContain('Default to Text. Use HTML only when requested.');
  expect(contract).toContain('Do not pass `bodyType`, `contextSources`, `assumptions`,');
  expect(contract).toContain('Review metadata must not be appended to the email body');
});

it('allows disclosed server-side name resolution with post-creation recipient review', () => {
  expect(skill).toMatch(/Pass approved names unchanged to `CreateDraftMessage`/u);
  expect(skill).not.toContain('Never pass names to `CreateDraftMessage`');
  for (const text of ['address unresolved; resolved when saving',
    'A separate lookup tool is not required.', 'Do not include preview-only labels in tool arguments.',
    'Approval covers the exact', 'Server-resolved does not mean identity-verified.',
    'show all returned To, CC, and BCC addresses', 'list input names and returned',
    'Explicit\naddresses must be preserved', 'missing, extra, misplaced',
    'recipient verification as incomplete', 'Never infer successful resolution from creation success alone.',
    'do not update, delete, or recreate',
  ]) expect(skill.replaceAll('\r\n', '\n')).toContain(text);
});

it('handles known ambiguity and pre-save verification without dropping recipients', () => {
  for (const text of ['read-only recipient lookup tool',
    'never select the first match', 'ask for the address', 'only after the user agrees',
    'user requires address verification before saving', 'Do not silently drop requested recipients.',
  ]) expect(skill).toContain(text);
});

it('prefers evidenced addresses and reports incomplete recipients without masking them', () => {
  const normalized = skill.replace(/\s+/gu, ' ');
  for (const text of ['Prefer an address already established for the intended person',
    'Show the address and its source in the preview before approval.',
    'A prior server-resolved address alone is not proof of identity.',
    'never silently replace an approved name with an address.',
    'Matching recipient counts alone do not establish correct identities.',
    'Draft saved; recipient verification incomplete',
    'identify specific missing recipients only where evidence supports it.',
    'verify or correct the existing draft manually in Outlook.',
    'Do not describe the overall task as fully successful',
    'must not replace an incomplete-recipient warning.',
  ]) expect(normalized).toContain(text);
  expect(normalized).toContain('only one recipient without warning.');
  expect(normalized).not.toContain('has not yet been live-tested');
});

it('distinguishes remote permissions from workflow controls and uncertain results', () => {
  for (const text of ['No separate organizational approval is required by this skill.', '`SendDraftMessage`',
    'do not revoke OAuth permissions', 'do not enable automatic approval',
    'Never retry automatically', 'empty or ambiguous result is not proof of creation',
    'different recipients',
  ]) expect(skill).toContain(text);
  expect(skill).not.toMatch(/Require organizational approval|only when organizational approval/iu);
});