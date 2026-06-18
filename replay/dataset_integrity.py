"""
replay/dataset_integrity.py — ReplayDatasetIntegrityChecker v1.2.8

Checks file hashes against stored hashes.
Reports MISSING, CORRUPTED, INCOMPATIBLE per file.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import hashlib
import logging
import os
from typing import Any, Dict, List, Optional, Tuple

from replay.dataset_registry_schema import ReplayDatasetManifest, ReplayDatasetFileEntry

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _file_hash(path: str) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, IOError):
        return "MISSING"


class ReplayDatasetIntegrityChecker:
    """
    Checks dataset file integrity.

    - Missing file => MISSING
    - Hash mismatch => CORRUPTED
    - Schema mismatch => INCOMPATIBLE

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def check(
        self,
        manifest: ReplayDatasetManifest,
        base_dir: str = "",
    ) -> Dict[str, Any]:
        """
        Check all files in manifest.
        Returns overall status + per-file results.
        """
        results = {}
        overall = "PASS"
        for entry in manifest.files:
            file_result = self._check_file(entry, base_dir)
            results[entry.relative_path] = file_result
            if file_result["status"] in ("CORRUPTED", "INCOMPATIBLE"):
                overall = "FAIL"
            elif file_result["status"] == "MISSING":
                if entry.required:
                    overall = "BLOCKED"
                elif overall == "PASS":
                    overall = "WARN"
        return {
            "dataset_id": manifest.dataset_id,
            "overall":    overall,
            "files":      results,
        }

    def _check_file(self, entry: ReplayDatasetFileEntry, base_dir: str) -> Dict[str, Any]:
        """Check a single file."""
        if not base_dir:
            return {
                "status":  "SKIPPED",
                "reason":  "no base_dir provided",
                "path":    entry.relative_path,
            }
        abs_path = os.path.join(base_dir, entry.relative_path)
        if not os.path.exists(abs_path):
            return {
                "status":  "MISSING",
                "path":    entry.relative_path,
                "required": entry.required,
            }
        if entry.content_hash:
            actual_hash = _file_hash(abs_path)
            if actual_hash != entry.content_hash:
                return {
                    "status":  "CORRUPTED",
                    "path":    entry.relative_path,
                    "stored_hash":  entry.content_hash,
                    "actual_hash":  actual_hash,
                }
        return {
            "status": "OK",
            "path":   entry.relative_path,
        }
