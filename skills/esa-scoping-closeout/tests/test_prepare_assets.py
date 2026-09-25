import base64
import copy
import hashlib
import importlib.util
import json
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "prepare_assets.py"
SPEC = importlib.util.spec_from_file_location("prepare_assets", SCRIPT)
assets = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(assets)


def png_chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))


def test_png():
    header = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", header)
        + png_chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00"))
        + png_chunk(b"IEND", b"")
    )


class AssetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.files = self.root / "Knowledge" / "Attachments"
        self.templates = self.root / "Knowledge" / "Templates"
        self.files.mkdir(parents=True)
        self.templates.mkdir()
        for name in assets.REQUIRED_ATTACHMENTS:
            (self.files / name).write_bytes(name.encode("utf-8"))
        (self.templates / "Microsoft.png").write_bytes(test_png())
        self.settings = {
            "attachmentFolderUrl": "https://example.sharepoint.com/folder",
            "signature": {
                "name": "Example Person",
                "role": "Example Role",
                "phone": "+1 555 0100",
                "email": "example@example.com",
            },
        }
        self.save_settings()

    def save_settings(self):
        (self.root / "settings.local.json").write_text(json.dumps(self.settings), encoding="utf-8")

    def manifest_and_cloud(self):
        manifest = assets.prepare_assets(self.root)
        cloud = {"files": [
            {
                "name": item["name"],
                "size": item["size"],
                "id": f"item-{index}",
                "file": {"hashes": dict(item["hashes"])},
            }
            for index, item in enumerate(manifest["attachments"])
        ]}
        return manifest, cloud

    def test_inventory_includes_all_files_and_only_encodes_logo(self):
        extra = self.files / "extra"
        extra.mkdir()
        (extra / "Additional guide.txt").write_bytes(b"Additional customer guide")
        result = assets.prepare_assets(self.root)
        self.assertEqual(len(result["attachments"]), 5)
        self.assertFalse(next(item for item in result["attachments"] if item["name"].endswith(".txt"))["baseline"])
        self.assertTrue(all("contentBytes" not in item for item in result["attachments"]))
        self.assertEqual(base64.b64decode(result["inlineLogo"]["contentBytes"]), test_png())
        self.assertTrue(result["inlineLogo"]["isInline"])
        self.assertEqual(result["inlineLogo"]["contentId"], assets.LOGO_CID)
        self.assertIn(f'cid:{assets.LOGO_CID}', result["signatureHtml"])
        self.assertNotIn("data:image", result["signatureHtml"])

    def test_share_id_round_trips_exact_configured_url(self):
        result = assets.prepare_assets(self.root)
        encoded = result["sourceFolder"]["shareId"][2:]
        decoded = base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)).decode("utf-8")
        self.assertEqual(decoded, self.settings["attachmentFolderUrl"])

    def test_baseline_mime_types_do_not_depend_on_windows_registry(self):
        with patch.object(assets.mimetypes, "guess_type", return_value=("application/x-zip-compressed", None)):
            result = assets.prepare_assets(self.root)
        for item in result["attachments"]:
            self.assertEqual(
                item["contentType"],
                "application/zip" if item["name"].endswith(".zip") else "application/pdf",
            )

    def test_signature_is_escaped_and_email_spelling_preserved(self):
        self.settings["signature"]["name"] = '<img src="https://untrusted.example/image">'
        self.settings["signature"]["role"] = "Cloud & Security"
        self.settings["signature"]["email"] = "thomas.brundl@microsoft.com"
        self.save_settings()
        result = assets.prepare_assets(self.root)
        self.assertIn("&lt;img src=&quot;", result["signatureHtml"])
        self.assertIn("Cloud &amp; Security", result["signatureHtml"])
        self.assertIn("mailto:thomas.brundl@microsoft.com", result["signatureHtml"])
        self.assertEqual(result["signatureHtml"].count("<img "), 1)

    def test_invalid_settings_fail_explicitly(self):
        original = copy.deepcopy(self.settings)
        invalid = [
            ("attachmentFolderUrl", "http://example.sharepoint.com/folder"),
            ("attachmentFolderUrl", "https://example.sharepoint.com.evil.example/folder"),
            ("attachmentFolderUrl", "https://name:password@example.sharepoint.com/folder"),
            ("attachmentFolderUrl", "https://example.sharepoint.com/REPLACE_WITH_FOLDER"),
            ("attachmentFolderUrl", "https://example.sharepoint.com:123/folder"),
            ("signature", {"name": "Only a name"}),
            ("signature", None),
        ]
        for field, value in invalid:
            with self.subTest(field=field, value=value):
                self.settings = copy.deepcopy(original)
                self.settings[field] = value
                self.save_settings()
                with self.assertRaises(assets.AssetError):
                    assets.prepare_assets(self.root)

    def test_missing_settings_are_not_replaced_with_example(self):
        (self.root / "settings.local.json").unlink()
        with self.assertRaisesRegex(assets.AssetError, "Required file is missing"):
            assets.prepare_assets(self.root)

    def test_invalid_signature_addresses_fail(self):
        for address in [
            "name", ".name@example.com", "name..person@example.com",
            "name@example..com", "name@-example.com", "name@example-.com",
            "name@example.com\nBcc:other@example.com", "x" * 65 + "@example.com",
        ]:
            with self.subTest(address=address):
                self.settings["signature"]["email"] = address
                self.save_settings()
                with self.assertRaises(assets.AssetError):
                    assets.prepare_assets(self.root)

    def test_cross_directory_asset_read_is_rejected(self):
        with self.assertRaisesRegex(assets.AssetError, "outside the skill directory"):
            assets.read_local_file(ROOT / "SKILL.md", self.root)

    def test_missing_baseline_file_fails(self):
        (self.files / assets.REQUIRED_ATTACHMENTS[0]).unlink()
        with self.assertRaisesRegex(assets.AssetError, "Missing required attachments"):
            assets.prepare_assets(self.root)

    def test_empty_file_fails(self):
        (self.files / assets.REQUIRED_ATTACHMENTS[0]).write_bytes(b"")
        with self.assertRaisesRegex(assets.AssetError, "File is empty"):
            assets.prepare_assets(self.root)

    def test_duplicate_basename_fails(self):
        (self.files / "nested").mkdir()
        (self.files / "nested" / assets.REQUIRED_ATTACHMENTS[0]).write_bytes(b"Duplicate")
        with self.assertRaisesRegex(assets.AssetError, "Duplicate attachment filename"):
            assets.prepare_assets(self.root)

    def test_corrupt_and_missing_logo_fail(self):
        logo = self.templates / "Microsoft.png"
        for data in [b"not a PNG", test_png()[:-1], test_png()[:-12], test_png()[:-5] + b"abcde"]:
            with self.subTest(length=len(data)):
                logo.write_bytes(data)
                with self.assertRaises(assets.AssetError):
                    assets.prepare_assets(self.root)
        logo.unlink()
        with self.assertRaisesRegex(assets.AssetError, "Required file is missing"):
            assets.prepare_assets(self.root)

    def test_cloud_comparison_accepts_uppercase_hex_and_reports_extras(self):
        manifest, cloud = self.manifest_and_cloud()
        for item in cloud["files"]:
            item["file"]["hashes"]["sha256Hash"] = item["file"]["hashes"]["sha256Hash"].upper()
        cloud["files"].append({"name": "Not locally approved.pdf", "id": "extra"})
        result = assets.compare_cloud(manifest, cloud)
        self.assertEqual(len(result["matched"]), 4)
        self.assertEqual(result["cloudOnlyFiles"], ["Not locally approved.pdf"])
        self.assertIn("not proof of live access", result["scope"])

    def test_cloud_comparison_blocks_missing_ambiguous_and_changed_files(self):
        manifest, original = self.manifest_and_cloud()
        mutations = [
            lambda items: items.pop(),
            lambda items: items.append(copy.deepcopy(items[0])),
            lambda items: items[0].update(size=1),
            lambda items: items[0].update(size=True),
            lambda items: items[0].update(id=""),
            lambda items: items[0].update(name=items[0]["name"].upper()),
            lambda items: items[0].update(file=None),
            lambda items: items[0].update(file={"hashes": {}}),
            lambda items: items[0].update(file={"hashes": {"unsupportedHash": "value"}}),
            lambda items: items[0]["file"]["hashes"].update(quickXorHash="changed"),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                cloud = copy.deepcopy(original)
                mutate(cloud["files"])
                with self.assertRaises(assets.AssetError):
                    assets.compare_cloud(manifest, cloud)

    def test_invalid_cloud_input_shapes_fail(self):
        manifest = assets.prepare_assets(self.root)
        for cloud in [None, [], {}, {"files": None}, {"files": ["not a file"]}]:
            with self.subTest(cloud=cloud):
                with self.assertRaises(assets.AssetError):
                    assets.compare_cloud(manifest, cloud)

    def test_cli_failure_is_nonzero_with_no_success_payload(self):
        (self.root / "settings.local.json").write_text("{broken", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--skill-dir", str(self.root)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("Asset preflight failed:", result.stderr)

    def test_cli_can_compare_cloud_metadata(self):
        _, cloud = self.manifest_and_cloud()
        metadata_path = self.root / "cloud.json"
        metadata_path.write_text(json.dumps(cloud), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--skill-dir", str(self.root),
             "--cloud-metadata", str(metadata_path)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["cloudComparison"]["matched"]), 4)

    def attachment_download(self, name=None):
        name = name or assets.REQUIRED_ATTACHMENTS[0]
        data = (self.templates / name if name == "Microsoft.png" else self.files / name).read_bytes()
        return {
            "id": "returned-attachment-id",
            "name": name,
            "contentType": (
                "image/png" if name == "Microsoft.png"
                else "application/zip" if name.endswith(".zip") else "application/pdf"
            ),
            "size": len(data) + 229,
            "contentBytes": base64.b64encode(data).decode("ascii"),
        }

    def test_download_checks_bytes_instead_of_reported_outlook_size(self):
        manifest = assets.prepare_assets(self.root)
        for name in [assets.REQUIRED_ATTACHMENTS[0], assets.REQUIRED_ATTACHMENTS[-1], "Microsoft.png"]:
            with self.subTest(name=name):
                download = self.attachment_download(name)
                result = assets.verify_download(manifest, {"data": download})
                self.assertEqual(result["reportedSize"], result["decodedSize"] + 229)
                self.assertNotIn("contentBytes", result)
                self.assertIn("verify the source draft ID", result["scope"])
                self.assertEqual(
                    result["sha256Hash"],
                    hashlib.sha256(base64.b64decode(download["contentBytes"])).hexdigest(),
                )

    def test_download_accepts_equivalent_zip_mime_with_exact_bytes(self):
        manifest = assets.prepare_assets(self.root)
        download = self.attachment_download(assets.REQUIRED_ATTACHMENTS[-1])
        download["contentType"] = "application/x-zip-compressed"
        result = assets.verify_download(manifest, download)
        self.assertEqual(result["name"], download["name"])

    def test_download_rejects_corruption_even_with_plausible_metadata(self):
        manifest = assets.prepare_assets(self.root)
        original = self.attachment_download()
        mutations = [
            lambda item: item.update(name="Unexpected.pdf"),
            lambda item: item.update(id=""),
            lambda item: item.update(contentType="application/zip"),
            lambda item: item.update(contentBytes=""),
            lambda item: item.update(contentBytes="not valid base64"),
            lambda item: item.update(contentBytes="YWJj<output too long - dropped 123 characters>"),
            lambda item: item.update(contentBytes=base64.b64encode(b"x" * len(assets.REQUIRED_ATTACHMENTS[0])).decode("ascii")),
            lambda item: item.update(size=True),
            lambda item: item.update(size=-1),
            lambda item: item.update({"@odata.type": "#microsoft.graph.referenceAttachment"}),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                download = copy.deepcopy(original)
                mutate(download)
                with self.assertRaises(assets.AssetError):
                    assets.verify_download(manifest, download)

    def test_download_rejects_missing_and_invalid_shapes(self):
        manifest = assets.prepare_assets(self.root)
        for download in [None, [], {}, {"data": None}, {"data": []}]:
            with self.subTest(download=download):
                with self.assertRaises(assets.AssetError):
                    assets.verify_download(manifest, download)

    def test_cli_verifies_downloads_and_fails_without_success_payload(self):
        paths = [self.root / "logo-download.json", self.root / "pdf-download.json"]
        downloads = [self.attachment_download("Microsoft.png"), self.attachment_download()]
        command = [sys.executable, str(SCRIPT), "--skill-dir", str(self.root)]
        for path, download in zip(paths, downloads):
            path.write_text(json.dumps({"data": download}), encoding="utf-8")
            command.extend(["--attachment-download", str(path)])
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["verifiedDownloads"]), 2)
        downloads[1]["contentBytes"] = "corrupt"
        paths[1].write_text(json.dumps(downloads[1]), encoding="utf-8")
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("invalid or truncated base64", result.stderr)


class HashAndSourceTests(unittest.TestCase):
    def test_quickxor_known_vectors_and_wraparound(self):
        self.assertEqual(assets.quick_xor_hash(b""), "AAAAAAAAAAAAAAAAAAAAAAAAAAA=")
        self.assertEqual(base64.b64decode(assets.quick_xor_hash(b"\x01")), b"\x01" + b"\x00" * 11 + b"\x01" + b"\x00" * 7)
        for length in (15, 16, 159, 160, 161, 4096):
            data = bytes(index % 256 for index in range(length))
            expected = bytearray(20)
            for index, value in enumerate(data):
                start = index * 11 % 160
                for bit in range(8):
                    if value & (1 << bit):
                        position = (start + bit) % 160
                        expected[position // 8] ^= 1 << (position % 8)
            for index, value in enumerate(length.to_bytes(8, "little")):
                expected[12 + index] ^= value
            self.assertEqual(base64.b64decode(assets.quick_xor_hash(data)), bytes(expected))

    def test_packaged_files_match_observed_cloud_hashes(self):
        expected = {
            "Enterprise Security Assessment - Data Gathering.pdf": "YT91hP0AxtpcKKobaEh3NrsVtLA=",
            "Enterprise Security Assessment - Power BI Refresh.pdf": "+o9Qb8/f/wGHM1FX+5hkiiht4ZY=",
            "Enterprise Security Assessment - Scoping.pdf": "/7W+f2ljDsidvgROMe8aCt3FltI=",
            "ESA Data Gathering Tool.zip": "FQ06BwPonidoSVFaCEH4D6Rdp+4=",
        }
        for name, expected_hash in expected.items():
            with self.subTest(file=name):
                data = (ROOT / "Knowledge" / "Attachments" / name).read_bytes()
                self.assertEqual(assets.quick_xor_hash(data), expected_hash)

    def test_original_logo_is_preserved(self):
        data = (ROOT / "Knowledge" / "Templates" / "Microsoft.png").read_bytes()
        self.assertEqual(assets.png_dimensions(data), (115, 28))
        self.assertEqual(
            hashlib.sha256(data).hexdigest(),
            "580a71d00362dc01fb2965037b879cc7eda4530d0a5418350d857d4a6f1456da",
        )


if __name__ == "__main__":
    unittest.main()
