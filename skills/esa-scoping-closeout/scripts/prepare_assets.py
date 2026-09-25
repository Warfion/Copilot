"""Prepare ESA assets and verify cloud metadata or downloaded attachment bytes."""

import argparse
import base64
import binascii
import hashlib
import html
import json
import mimetypes
import re
import struct
import sys
import zlib
from pathlib import Path
from urllib.parse import urlsplit


REQUIRED_ATTACHMENTS = (
    "Enterprise Security Assessment - Data Gathering.pdf",
    "Enterprise Security Assessment - Power BI Refresh.pdf",
    "Enterprise Security Assessment - Scoping.pdf",
    "ESA Data Gathering Tool.zip",
)
LOGO_CID = "esa-signature-logo"
SKILL_ROOT = Path(__file__).resolve().parents[1]


class AssetError(ValueError):
    """An asset or metadata requirement was not satisfied."""


def quick_xor_hash(data: bytes) -> str:
    columns = bytearray(160)
    for index, value in enumerate(data):
        columns[index % 160] ^= value
    bits = 0
    for index, value in enumerate(columns):
        bits ^= value << ((index * 11) % 160)
    # Fold the circular 160-bit shift, then XOR the little-endian byte length.
    bits = (bits & ((1 << 160) - 1)) ^ (bits >> 160)
    bits ^= len(data) << 96
    return base64.b64encode(bits.to_bytes(20, "little")).decode("ascii")


def hashes(data: bytes) -> dict[str, str]:
    return {
        "sha256Hash": hashlib.sha256(data).hexdigest(),
        "sha1Hash": hashlib.sha1(data, usedforsecurity=False).hexdigest(),
        "quickXorHash": quick_xor_hash(data),
    }


def read_local_file(path: Path, root: Path) -> bytes:
    if not path.resolve().is_relative_to(root.resolve()):
        raise AssetError(f"Asset resolves outside the skill directory: {path.name}")
    relative = path.relative_to(root)
    if any((root / parent).is_symlink() for parent in (relative, *relative.parents)):
        raise AssetError(f"Linked assets are not allowed: {relative}")
    if not path.is_file():
        raise AssetError(f"Required file is missing: {relative}")
    data = path.read_bytes()
    if not data:
        raise AssetError(f"File is empty: {relative}")
    return data


def load_settings(root: Path) -> dict:
    raw = read_local_file(root / "settings.local.json", root)
    settings = json.loads(raw.decode("utf-8"))
    if not isinstance(settings, dict):
        raise AssetError("settings.local.json must contain an object.")
    if set(settings) != {"attachmentFolderUrl", "signature"}:
        raise AssetError("Settings require attachmentFolderUrl and signature only.")
    url = settings["attachmentFolderUrl"]
    if not isinstance(url, str) or not url or url != url.strip():
        raise AssetError("attachmentFolderUrl must be a nonempty URL without whitespace.")
    if any(character.isspace() for character in url) or "REPLACE_" in url:
        raise AssetError("Replace the attachment folder placeholder with the approved URL.")
    parsed = urlsplit(url)
    host = parsed.hostname or ""
    allowed_host = host in {
        "onedrive.cloud.microsoft", "onedrive.live.com", "1drv.ms",
    } or host.endswith(".sharepoint.com")
    if (
        parsed.scheme != "https"
        or not allowed_host
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port not in (None, 443)
        or not parsed.path
    ):
        raise AssetError("Use an HTTPS OneDrive/SharePoint folder URL without credentials.")

    signature = settings["signature"]
    if not isinstance(signature, dict) or set(signature) != {"name", "role", "phone", "email"}:
        raise AssetError("Signature requires exactly name, role, phone, and email.")
    for field, value in signature.items():
        if (
            not isinstance(value, str)
            or not value.strip()
            or value != value.strip()
            or any(ord(character) < 32 for character in value)
            or "REPLACE_" in value
        ):
            raise AssetError(f"Provide a nonempty, single-line signature {field}.")
    atom = r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
    label = r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    email = signature["email"]
    if not re.fullmatch(rf"{atom}(?:\.{atom})*@{label}(?:\.{label})+", email):
        raise AssetError("Signature email must be a plain syntactically valid address.")
    if len(email) > 254 or len(email.split("@")[0]) > 64:
        raise AssetError("Signature email exceeds standard address length limits.")
    return settings


def png_dimensions(data: bytes) -> tuple[int, int]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise AssetError("Microsoft.png is not a PNG file.")
    offset = 8
    dimensions = None
    saw_pixels = False
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        end = offset + length + 12
        if end > len(data):
            raise AssetError("Microsoft.png has a truncated chunk.")
        payload = data[offset + 8:end - 4]
        crc = struct.unpack(">I", data[end - 4:end])[0]
        if zlib.crc32(kind + payload) != crc:
            raise AssetError("Microsoft.png has a corrupt chunk checksum.")
        if offset == 8 and kind != b"IHDR":
            raise AssetError("Microsoft.png is missing its initial IHDR chunk.")
        if kind == b"IHDR":
            if dimensions is not None or length != 13:
                raise AssetError("Microsoft.png has an invalid IHDR chunk.")
            dimensions = struct.unpack(">II", payload[:8])
            if not all(dimensions):
                raise AssetError("Microsoft.png has invalid dimensions.")
        elif kind == b"IDAT":
            saw_pixels = saw_pixels or length > 0
        elif kind == b"IEND":
            if length != 0 or end != len(data) or dimensions is None or not saw_pixels:
                raise AssetError("Microsoft.png has an invalid ending or missing image data.")
            return dimensions
        offset = end
    raise AssetError("Microsoft.png is incomplete.")


def attachment_inventory(root: Path) -> list[dict]:
    folder = root / "Knowledge" / "Attachments"
    if not folder.is_dir():
        raise AssetError("Knowledge\\Attachments is missing.")
    entries = []
    names = set()
    for path in sorted(folder.rglob("*"), key=lambda item: str(item).casefold()):
        if path.is_symlink():
            raise AssetError(f"Linked assets are not allowed: {path.relative_to(root)}")
        if path.is_dir():
            continue
        data = read_local_file(path, root)
        if path.name.casefold() in names:
            raise AssetError(f"Duplicate attachment filename: {path.name}")
        names.add(path.name.casefold())
        content_type = {".pdf": "application/pdf", ".zip": "application/zip"}.get(path.suffix.lower())
        if content_type is None:
            content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        entries.append({
            "name": path.name,
            "relativePath": str(path.relative_to(root)),
            "size": len(data),
            "contentType": content_type,
            "hashes": hashes(data),
            "baseline": path.name in REQUIRED_ATTACHMENTS,
        })
    missing = set(REQUIRED_ATTACHMENTS) - {entry["name"] for entry in entries}
    if missing:
        raise AssetError("Missing required attachments: " + ", ".join(sorted(missing)))
    return entries


def prepare_assets(root: Path = SKILL_ROOT) -> dict:
    root = root.resolve()
    settings = load_settings(root)
    attachments = attachment_inventory(root)
    logo = read_local_file(root / "Knowledge" / "Templates" / "Microsoft.png", root)
    width, height = png_dimensions(logo)
    signature = {key: html.escape(value, quote=True) for key, value in settings["signature"].items()}
    signature_html = (
        f'<p><img src="cid:{LOGO_CID}" alt="Microsoft Logo" width="114" height="27"></p>'
        f'<p><strong>{signature["name"]}</strong><br>'
        f'{signature["role"]}<br>Mobile: {signature["phone"]}<br>'
        f'<a href="mailto:{signature["email"]}">{signature["email"]}</a></p>'
    )
    folder_url = settings["attachmentFolderUrl"]
    share_id = "u!" + base64.urlsafe_b64encode(folder_url.encode("utf-8")).decode("ascii").rstrip("=")
    return {
        "sourceFolder": {"url": folder_url, "shareId": share_id},
        "attachments": attachments,
        "signatureHtml": signature_html,
        "inlineLogo": {
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": "Microsoft.png",
            "contentType": "image/png",
            "contentId": LOGO_CID,
            "isInline": True,
            "contentBytes": base64.b64encode(logo).decode("ascii"),
        },
        "logoMetadata": {
            "size": len(logo),
            "width": width,
            "height": height,
            "sha256Hash": hashlib.sha256(logo).hexdigest(),
        },
        "scope": "Local preparation only; no live access or delivery has been verified.",
    }


def compare_cloud(manifest: dict, cloud_metadata: object) -> dict:
    if not isinstance(cloud_metadata, dict) or not isinstance(cloud_metadata.get("files"), list):
        raise AssetError('Cloud metadata must be an object containing a "files" array.')
    cloud_by_name = {}
    for item in cloud_metadata["files"]:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not item["name"]:
            raise AssetError("Every cloud file record needs a name.")
        key = item["name"].casefold()
        if key in cloud_by_name:
            raise AssetError(f"Ambiguous cloud filename: {item['name']}")
        cloud_by_name[key] = item

    matched = []
    for local in manifest["attachments"]:
        name = local["name"]
        remote = cloud_by_name.pop(name.casefold(), None)
        if remote is None:
            raise AssetError(f"Cloud file is missing: {name}")
        if remote["name"] != name:
            raise AssetError(f"Cloud filename differs from local filename: {name}")
        if not isinstance(remote.get("id"), str) or not remote["id"].strip():
            raise AssetError(f"Cloud file has no returned item ID: {name}")
        if type(remote.get("size")) is not int or remote["size"] != local["size"]:
            raise AssetError(f"Cloud/local byte size mismatch: {name}")
        file_info = remote.get("file")
        remote_hashes = file_info.get("hashes") if isinstance(file_info, dict) else None
        if not isinstance(remote_hashes, dict):
            raise AssetError(f"Cloud file has no usable file hashes: {name}")
        checked = []
        for hash_type, local_hash in local["hashes"].items():
            remote_hash = remote_hashes.get(hash_type)
            if remote_hash in (None, ""):
                continue
            if not isinstance(remote_hash, str):
                raise AssetError(f"Invalid cloud {hash_type}: {name}")
            if hash_type != "quickXorHash":
                remote_hash = remote_hash.lower()
            if remote_hash != local_hash:
                raise AssetError(f"Cloud/local {hash_type} mismatch: {name}")
            checked.append(hash_type)
        if not checked:
            raise AssetError(f"Cloud file has no supported content hash: {name}")
        matched.append({"name": name, "id": remote["id"], "verifiedHashTypes": checked})
    return {
        "matched": matched,
        "cloudOnlyFiles": sorted(item["name"] for item in cloud_by_name.values()),
        "scope": "Metadata comparison only; not proof of live access or attachment delivery.",
    }


def verify_download(manifest: dict, download: object) -> dict:
    if not isinstance(download, dict):
        raise AssetError("Attachment download must be a JSON object.")
    attachment = download.get("data", download)
    if not isinstance(attachment, dict):
        raise AssetError("Attachment download data must be an object.")
    name = attachment.get("name")
    expected = next(
        (item for item in manifest["attachments"] if item["name"] == name), None,
    )
    if name == manifest["inlineLogo"]["name"]:
        expected = {
            "size": manifest["logoMetadata"]["size"],
            "contentType": manifest["inlineLogo"]["contentType"],
            "hashes": {"sha256Hash": manifest["logoMetadata"]["sha256Hash"]},
        }
    if expected is None:
        raise AssetError(f"Downloaded attachment is not an approved asset: {name}")
    attachment_id = attachment.get("id")
    if not isinstance(attachment_id, str) or not attachment_id.strip():
        raise AssetError(f"Downloaded attachment has no returned ID: {name}")
    allowed_content_types = (
        ("application/zip", "application/x-zip-compressed")
        if expected["contentType"] == "application/zip" else (expected["contentType"],)
    )
    if attachment.get("contentType") not in allowed_content_types:
        raise AssetError(f"Downloaded attachment MIME type mismatch: {name}")
    if attachment.get("@odata.type", "#microsoft.graph.fileAttachment") != "#microsoft.graph.fileAttachment":
        raise AssetError(f"Downloaded attachment is not a file attachment: {name}")
    content = attachment.get("contentBytes")
    if not isinstance(content, str) or not content:
        raise AssetError(f"Downloaded attachment has no complete contentBytes: {name}")
    try:
        data = base64.b64decode(content, validate=True)
    except (ValueError, binascii.Error) as error:
        raise AssetError(f"Downloaded attachment has invalid or truncated base64: {name}") from error
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != expected["size"] or digest != expected["hashes"]["sha256Hash"]:
        raise AssetError(f"Downloaded attachment byte size or SHA-256 mismatch: {name}")
    reported_size = attachment.get("size")
    if reported_size is not None and (type(reported_size) is not int or reported_size < 0):
        raise AssetError(f"Downloaded attachment has invalid reported size: {name}")
    return {
        "id": attachment_id,
        "name": name,
        "decodedSize": len(data),
        "reportedSize": reported_size,
        "sha256Hash": digest,
        "scope": (
            "Supplied download bytes match the local asset; verify the source draft ID, "
            "current attachment inventory, draft state and inline Content-ID separately."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, default=SKILL_ROOT)
    parser.add_argument("--cloud-metadata", type=Path)
    parser.add_argument("--attachment-download", type=Path, action="append", default=[])
    args = parser.parse_args()
    try:
        manifest = prepare_assets(args.skill_dir)
        if args.cloud_metadata is not None:
            cloud = json.loads(args.cloud_metadata.read_text(encoding="utf-8"))
            manifest["cloudComparison"] = compare_cloud(manifest, cloud)
        if args.attachment_download:
            manifest["verifiedDownloads"] = [
                verify_download(manifest, json.loads(path.read_text(encoding="utf-8")))
                for path in args.attachment_download
            ]
    except (ValueError, OSError, UnicodeError) as error:
        print(f"Asset preflight failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(manifest, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
