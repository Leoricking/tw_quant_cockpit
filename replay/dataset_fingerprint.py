"""
replay/dataset_fingerprint.py — ReplayDatasetFingerprint v1.2.8

Deterministic fingerprint calculation for replay datasets.
Fingerprints are based on normalized relative paths, schema, file hashes,
symbol/timeframe/field coverage, row counts, source type, and qualification.

Fingerprint MUST NOT include: absolute paths, machine names, usernames,
temporary directories, generated report paths, cache paths.

Same content on two machines => same fingerprint.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Fields excluded from fingerprint (machine/path-specific)
_EXCLUDED_KEYS = {
    "created_at", "updated_at", "frozen_at", "archived_at",
    "fingerprint", "manifest_hash", "content_hash",
    "source_reference",  # may contain absolute path
    "warnings",
}


class ReplayDatasetFingerprint:
    """
    Deterministic fingerprint for replay datasets.

    Two datasets with identical content, schema, coverage, and qualification
    will produce the same fingerprint regardless of machine or path.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def calculate_file_hash(self, file_path: str) -> str:
        """SHA-256 of a single file's content."""
        h = hashlib.sha256()
        try:
            with open(file_path, "rb") as fh:
                for chunk in iter(lambda: fh.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()
        except (OSError, IOError):
            return "MISSING"

    def calculate_content_hash(self, relative_paths: List[str], base_dir: str = "") -> str:
        """Hash of all file contents combined (sorted by relative path)."""
        h = hashlib.sha256()
        for rel in sorted(relative_paths):
            h.update(rel.encode("utf-8"))
            if base_dir:
                abs_path = os.path.join(base_dir, rel)
                fh = self.calculate_file_hash(abs_path)
            else:
                fh = "UNKNOWN"
            h.update(fh.encode("utf-8"))
        return h.hexdigest()

    def normalize_paths(self, paths: List[str]) -> List[str]:
        """Normalize path separators and sort."""
        normalized = []
        for p in paths:
            p = p.replace("\\", "/")
            # Strip absolute components
            if os.path.isabs(p):
                p = p.lstrip("/").lstrip("\\")
            normalized.append(p)
        return sorted(normalized)

    def normalize_manifest(self, manifest_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Return a copy of manifest with machine-specific fields removed.
        Absolute paths replaced with relative equivalents.
        """
        result: Dict[str, Any] = {}
        for k, v in manifest_dict.items():
            if k in _EXCLUDED_KEYS:
                continue
            if k == "relative_paths" and isinstance(v, list):
                result[k] = self.normalize_paths(v)
            elif k == "files" and isinstance(v, list):
                result[k] = self._normalize_file_entries(v)
            else:
                result[k] = v
        return result

    def calculate_manifest_fingerprint(self, manifest_dict: Dict[str, Any]) -> str:
        """SHA-256 of normalized manifest JSON (sorted keys)."""
        normalized = self.normalize_manifest(manifest_dict)
        canonical = json.dumps(normalized, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def calculate_dataset_fingerprint(
        self,
        manifest_dict: Dict[str, Any],
        file_hashes: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Master fingerprint combining manifest + file hashes.
        Deterministic and path-independent.
        """
        parts: Dict[str, Any] = {
            "manifest": self.normalize_manifest(manifest_dict),
            "file_hashes": {
                k: v for k, v in sorted((file_hashes or {}).items())
            },
        }
        canonical = json.dumps(parts, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def verify(
        self,
        fingerprint: str,
        manifest_dict: Dict[str, Any],
        file_hashes: Optional[Dict[str, str]] = None,
    ) -> bool:
        """Return True if computed fingerprint matches stored fingerprint."""
        computed = self.calculate_dataset_fingerprint(manifest_dict, file_hashes)
        return computed == fingerprint

    def explain_difference(
        self,
        fp1: str,
        fp2: str,
        manifest1: Dict[str, Any],
        manifest2: Dict[str, Any],
    ) -> str:
        """Return human-readable explanation of why two fingerprints differ."""
        if fp1 == fp2:
            return "Fingerprints are identical."
        lines = ["Fingerprints differ. Changed fields:"]
        n1 = self.normalize_manifest(manifest1)
        n2 = self.normalize_manifest(manifest2)
        for key in sorted(set(list(n1.keys()) + list(n2.keys()))):
            v1 = n1.get(key)
            v2 = n2.get(key)
            if v1 != v2:
                lines.append(f"  {key}: {v1!r} -> {v2!r}")
        return "\n".join(lines) if len(lines) > 1 else "Difference in file hashes only."

    # ------------------------------------------------------------------ #
    # Internals
    # ------------------------------------------------------------------ #

    def _normalize_file_entries(self, files: List[Any]) -> List[Dict[str, Any]]:
        """Normalize file entries: relative paths only, sorted."""
        result = []
        excluded = {"modified_at", "warnings", "content_hash"}
        for f in files:
            if not isinstance(f, dict):
                try:
                    f = f.__dict__
                except Exception:
                    continue
            entry: Dict[str, Any] = {}
            for k, v in f.items():
                if k in excluded:
                    continue
                if k == "relative_path" and isinstance(v, str):
                    v = v.replace("\\", "/")
                entry[k] = v
            result.append(entry)
        return sorted(result, key=lambda x: x.get("relative_path", ""))
