import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
NORMALIZED = re.sub(r"\s+", " ", SKILL)


class SkillContractTests(unittest.TestCase):
    def test_discoverable_frontmatter(self):
        match = re.match(r"---\nname: ([^\n]+)\ndescription: '([^\n]+)'\n---", SKILL)
        self.assertIsNotNone(match)
        self.assertEqual(match[1], ROOT.name)
        self.assertLess(len(match[2]), 1024)
        self.assertIn("ESA", match[2])
        self.assertIn("German and English", match[2])
        self.assertIn("never sends", match[2])

    def test_meeting_and_evidence_requirements(self):
        for text in [
            "Ask for the customer name", "the past 14 days", "expanded recurring instances",
            "Multiple plausible matches", "No supported match", "both",
            "neither recap nor transcript is usable", "before drafting the closeout email",
            "union of verified attendees and invitees", "Microsoft people",
            "before drafting", "otherwise use the selected customer meeting's language",
        ]:
            with self.subTest(text=text):
                self.assertIn(text, NORMALIZED)

    def test_approval_and_no_send_boundaries(self):
        for text in [
            "Never send an email", "Do not call any mailbox-changing tool before approval",
            "subsequent user response", "prior approval is invalid",
            "Would you like me to create this message in Outlook Drafts?",
            "Never call sending", "No automatic retries", "do not delete or recreate",
            "Draft saved; verification incomplete",
            "The email was saved as a draft and was not sent.",
        ]:
            with self.subTest(text=text):
                self.assertIn(text, NORMALIZED)
        for field in [
            "Integration:", "Target:", "Customer:", "Meeting:", "To:", "CC:", "BCC:",
            "Subject:", "Body type:", "Body:", "Inline logo:", "File attachments:",
            "Preflight:", "Context sources used:", "Assumptions:", "Missing information:",
            "Unverified integration capabilities:",
        ]:
            self.assertIn(field, SKILL)

    def test_attachment_logo_and_access_gates(self):
        for text in [
            "every run, before creating the draft or attaching any files",
            "actual file attachments", "read each item", "name, byte size",
            "signature logo is separate", "matching Content-ID", "not proof of visual rendering",
            "thomas.brundl@microsoft.com", "No scripts, remote images, data-URI images",
        ]:
            with self.subTest(text=text):
                self.assertIn(text.lower(), NORMALIZED.lower())
        self.assertIn("Microsoft.png", SKILL)

    def test_provider_and_failure_contracts(self):
        contract = (ROOT / "references" / "integrations.md").read_text(encoding="utf-8")
        normalized = re.sub(r"\s+", " ", contract)
        for text in [
            "CreateDraftMessage", "AddDraftAttachments", "GetOnlineMeetingAiInsights",
            "GetOnlineMeetingTranscripts", "GetOnlineMeetingAttendanceReports",
            "create_entity", "contentId", "contentBytes", "isInline",
            "inline-logo operation succeeded", "fresh-draft attachment workflow was verified",
            "not a binary download", "Do not restart", "metadata comparison",
            "reference attachments", "same draft", "exact returned Mail draft ID",
        ]:
            with self.subTest(text=text):
                self.assertIn(text, normalized)

    def test_transport_and_byte_verification_requirements(self):
        contract = (ROOT / "references" / "integrations.md").read_text(encoding="utf-8")
        normalized = re.sub(r"\s+", " ", contract)
        for text in [
            "HTTP 413", "4 * ceil(fileBytes / 3)", "MCP request-body limit",
            "Do not retry the same payload", "original message remained a draft",
            "--attachment-download", "SHA-256", "not a shortened `sessionLog`",
            "not an exact universal transport limit", "explicit approval",
        ]:
            with self.subTest(text=text):
                self.assertIn(text, normalized)
        self.assertIn("Known-incompatible routes block creation", NORMALIZED)
        self.assertIn("Download each attachment from this exact draft", NORMALIZED)

    def test_uniform_route_retains_failure_history_and_bounded_evidence(self):
        contract = (ROOT / "references" / "integrations.md").read_text(encoding="utf-8")
        normalized = re.sub(r"\s+", " ", contract)
        self.assertIn("one validated URI-based connector route", NORMALIZED)
        self.assertIn("all four baseline files to a fresh draft", NORMALIZED)
        for text in [
            "only the 3,897,972-byte Scoping PDF",
            "does not establish the connector's underlying defect",
            "No PDF was added", "No further writes were attempted",
            "not for arbitrary future files or changed service behavior",
            "Do not duplicate existing attachments",
        ]:
            with self.subTest(text=text):
                self.assertIn(text, normalized)

    def test_fresh_draft_evidence_covers_zip_logo_and_original_preservation(self):
        contract = (ROOT / "references" / "integrations.md").read_text(encoding="utf-8")
        normalized = re.sub(r"\s+", " ", contract)
        for text in [
            "33,137-byte ZIP", "added all four verified SharePoint file URLs",
            "No pinned repair allowance or local-byte substitution",
            "All five downloaded attachments matched",
            "both messages remained drafts",
            "original draft and attachments remained unchanged",
            "not a pixel-level rendering test",
        ]:
            with self.subTest(text=text):
                self.assertIn(text, normalized)

    def test_successful_route_is_attachment_only_and_keeps_approval(self):
        contract = (ROOT / "references" / "integrations.md").read_text(encoding="utf-8")
        normalized = re.sub(r"\s+", " ", contract)
        for text in [
            "`UpdateDraft` attachment-only operation",
            "returned HTTPS `webUrl`",
            "body, subject, to, cc, bcc, sensitivity and directAttachments",
            "same draft ID, subject, sender and To/CC/BCC",
            "Fresh downloads of all five files",
            "on-disk single-use record",
            "Both the operation and URI representation changed",
            "Future runs still require current access checks and explicit approval",
        ]:
            with self.subTest(text=text):
                self.assertIn(text, normalized)
        payload = json.loads(re.search(
            r"payload must contain exactly:\s*```json\s*(\{.*?\})\s*```",
            contract, re.DOTALL,
        )[1])
        self.assertEqual(set(payload), {"messageId", "attachmentUris"})
        self.assertIn("only missing files", NORMALIZED)

    def test_private_settings_are_not_in_tracked_examples(self):
        self.assertIn("settings.local.json", (ROOT / ".gitignore").read_text(encoding="utf-8"))
        example = json.loads((ROOT / "settings.example.json").read_text(encoding="utf-8"))
        self.assertIn("REPLACE_", example["attachmentFolderUrl"])
        self.assertIn("REPLACE_", example["signature"]["email"])
        for path in [ROOT / "SKILL.md", ROOT / "README.md", *ROOT.glob("references/*.md")]:
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"https://onedrive\.cloud\.microsoft/:f:/[^\s`]+")
            self.assertNotRegex(text, r"/drives/b![A-Za-z0-9_-]{40,}")

    def test_markdown_relative_links_exist(self):
        documents = [ROOT / "SKILL.md", ROOT / "README.md", ROOT.parents[1] / "README.md"]
        documents.extend(ROOT.glob("references/*.md"))
        for document in documents:
            text = document.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if urlsplit(target).scheme or target.startswith("#"):
                    continue
                path = document.parent / unquote(target.split("#", 1)[0])
                self.assertTrue(path.exists(), f"Broken link in {document.name}: {target}")

    def test_skill_is_documented_without_changing_outlook_contract(self):
        readme = (ROOT.parents[1] / "README.md").read_text(encoding="utf-8")
        self.assertIn("ESA Scoping Closeout", readme)
        old_skill = (ROOT.parent / "outlook-email-draft" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Only `CreateDraftMessage` is allowed to change the mailbox.", old_skill)
        self.assertIn("No attachments, reply", old_skill)


if __name__ == "__main__":
    unittest.main()
