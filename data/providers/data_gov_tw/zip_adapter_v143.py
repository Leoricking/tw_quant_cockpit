"""
data/providers/data_gov_tw/zip_adapter_v143.py — ZIP format adapter v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] ZIP bomb protection: max uncompressed size limit.
[!] Path traversal protection: blocked if member path traverses above extract dir.
[!] Dangerous extensions blocked: .exe, .dll, .bat, .sh, .py, .js, .vbs, .cmd, etc.
[!] Always cleans up extracted files on error.
"""
from __future__ import annotations

import io
import os
import tempfile
import zipfile
from typing import Any, Dict, List, Optional, Tuple

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

MAX_ZIP_UNCOMPRESSED_BYTES = 500 * 1024 * 1024   # 500 MB
MAX_ZIP_MEMBER_BYTES = 100 * 1024 * 1024          # 100 MB per member
MAX_ZIP_MEMBERS = 100

_BLOCKED_EXTENSIONS = frozenset({
    ".exe", ".dll", ".bat", ".sh", ".py", ".js", ".vbs", ".cmd",
    ".ps1", ".jar", ".msi", ".com", ".scr", ".pif", ".wsf",
})

_SUPPORTED_EXTENSIONS = frozenset({
    ".csv", ".json", ".xml", ".txt", ".tsv", ".ods", ".xls", ".xlsx",
    ".md", ".pdf",
})


def _is_path_safe(member_name: str, extract_dir: str) -> bool:
    """Return True if the member does not traverse outside extract_dir."""
    target = os.path.realpath(os.path.join(extract_dir, member_name))
    return target.startswith(os.path.realpath(extract_dir))


def _is_blocked_extension(name: str) -> bool:
    _, ext = os.path.splitext(name.lower())
    return ext in _BLOCKED_EXTENSIONS


class DataGovTwZipAdapter:
    """
    Safely extracts and inspects ZIP resources from data.gov.tw.

    Security:
    - Path traversal: members with .. in path are blocked
    - ZIP bomb: total uncompressed size is checked before extraction
    - Dangerous extensions: blocked
    - Temporary extraction: always cleaned up on error
    - Unsupported formats inside ZIP: blocked

    Returns metadata and parsed contents (does not write to arbitrary paths).
    """

    def inspect(
        self,
        content: bytes,
        max_uncompressed: int = MAX_ZIP_UNCOMPRESSED_BYTES,
    ) -> Dict[str, Any]:
        """Inspect ZIP metadata without extracting. Returns member list."""
        try:
            zf = zipfile.ZipFile(io.BytesIO(content))
        except zipfile.BadZipFile as exc:
            return {
                "success": False,
                "error": f"Bad ZIP file: {exc}",
                "members": [],
                "total_uncompressed": 0,
                "warnings": [str(exc)],
            }

        members = []
        total_uncompressed = 0
        warnings: List[str] = []

        for info in zf.infolist():
            total_uncompressed += info.file_size
            _, ext = os.path.splitext(info.filename.lower())
            blocked = _is_blocked_extension(info.filename)
            traversal = ".." in info.filename.replace("\\", "/")
            members.append({
                "name": info.filename,
                "size_compressed": info.compress_size,
                "size_uncompressed": info.file_size,
                "extension": ext,
                "blocked": blocked,
                "path_traversal": traversal,
            })
            if blocked:
                warnings.append(f"Blocked file in ZIP: {info.filename}")
            if traversal:
                warnings.append(f"Path traversal detected: {info.filename}")

        zf.close()

        oversize = total_uncompressed > max_uncompressed

        return {
            "success": True,
            "members": members,
            "member_count": len(members),
            "total_uncompressed": total_uncompressed,
            "oversize": oversize,
            "warnings": warnings,
            "error": None,
        }

    def safe_extract_to_memory(
        self,
        content: bytes,
        max_uncompressed: int = MAX_ZIP_UNCOMPRESSED_BYTES,
        allowed_extensions: Optional[frozenset] = None,
    ) -> Dict[str, Any]:
        """
        Extract ZIP to memory (not disk). Returns dict of filename → bytes.
        Blocks path traversal, oversize, dangerous extensions.
        """
        if allowed_extensions is None:
            allowed_extensions = _SUPPORTED_EXTENSIONS

        inspection = self.inspect(content, max_uncompressed)
        if not inspection["success"]:
            return {
                "success": False,
                "error": inspection["error"],
                "files": {},
                "warnings": inspection["warnings"],
            }

        if inspection["oversize"]:
            return {
                "success": False,
                "error": f"ZIP too large: {inspection['total_uncompressed']} bytes uncompressed",
                "files": {},
                "warnings": inspection["warnings"] + ["ZIP bomb protection triggered"],
            }

        # Check for blocked members
        blocked = [m for m in inspection["members"] if m["blocked"] or m["path_traversal"]]
        if blocked:
            names = [m["name"] for m in blocked]
            return {
                "success": False,
                "error": f"ZIP contains blocked files: {names}",
                "files": {},
                "warnings": inspection["warnings"],
            }

        files: Dict[str, bytes] = {}
        warnings = list(inspection["warnings"])

        try:
            zf = zipfile.ZipFile(io.BytesIO(content))
            for info in zf.infolist():
                _, ext = os.path.splitext(info.filename.lower())
                if ext not in allowed_extensions:
                    warnings.append(f"Skipping unsupported extension: {info.filename}")
                    continue
                if info.file_size > MAX_ZIP_MEMBER_BYTES:
                    warnings.append(f"Skipping oversized member: {info.filename}")
                    continue
                files[info.filename] = zf.read(info.filename)
            zf.close()
        except Exception as exc:
            return {
                "success": False,
                "error": f"ZIP extraction error: {exc}",
                "files": {},
                "warnings": warnings + [str(exc)],
            }

        return {
            "success": True,
            "files": files,
            "file_count": len(files),
            "warnings": warnings,
            "error": None,
        }
