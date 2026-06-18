"""
replay/dataset_package.py — ReplayDatasetPackage v1.2.8

Creates and validates portable replay packages.
All packages use RELATIVE_ONLY path mode.
Packages must NOT contain secrets, .env, API tokens, broker credentials,
absolute paths, raw market data (unless FULL_PORTABLE allowlist).

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import hashlib
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from replay.dataset_portability import (
    ReplayDatasetPortability, MANIFEST_ONLY, METADATA_ONLY, FULL_PORTABLE,
    RELATIVE_ONLY, SECRET_PATTERNS,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

_PORTABILITY = ReplayDatasetPortability()


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_manifest(manifest: Dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(manifest, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


class ReplayDatasetPackage:
    """
    Creates, validates, and exports portable replay packages.

    Package types:
    - MANIFEST_ONLY: manifest + registry + lineage + hashes + relative paths
    - METADATA_ONLY: + journal/score/strategy/review/challenge references
    - FULL_PORTABLE: + explicitly allowlisted dataset files

    Rules:
    - All paths RELATIVE_ONLY
    - No secrets, no .env, no broker data, no absolute paths
    - No runtime cache
    - package hash computed and stored

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def build_manifest(
        self,
        dataset_ids: List[str],
        session_ids: List[str],
        package_type: str = MANIFEST_ONLY,
        source_repo_version: str = "1.2.8",
        included_files: Optional[List[str]] = None,
        excluded_files: Optional[List[str]] = None,
        qualification: str = "MOCK_DEMO_ONLY",
        warnings: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Build a package manifest dict."""
        files = included_files or []
        # Scan for secrets and absolute paths
        secrets = _PORTABILITY.scan_for_secrets(files)
        abs_paths = _PORTABILITY.scan_for_absolute_paths(files)
        warns = list(warnings or [])
        if secrets:
            warns.append(f"SECRET_DETECTED: {secrets}")
        if abs_paths:
            warns.append(f"ABSOLUTE_PATH_DETECTED: {abs_paths}")

        manifest = {
            "package_id":          str(uuid.uuid4())[:12],
            "package_version":     "1.0",
            "package_type":        package_type,
            "source_repo_version": source_repo_version,
            "created_at":          _now_utc(),
            "dataset_ids":         dataset_ids,
            "session_ids":         session_ids,
            "included_files":      [f for f in files if f not in secrets],
            "excluded_files":      list(excluded_files or []) + secrets,
            "total_size":          0,
            "path_mode":           RELATIVE_ONLY,
            "qualification":       qualification,
            "warnings":            warns,
            "research_only":       True,
            "no_real_orders":      True,
        }
        manifest["package_hash"] = _hash_manifest({
            k: v for k, v in manifest.items()
            if k not in ("package_hash", "created_at")
        })
        return manifest

    def validate(self, package_manifest: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a package manifest. Returns status + issues."""
        issues = []
        # Check no absolute paths
        all_files = (
            package_manifest.get("included_files", [])
            + package_manifest.get("excluded_files", [])
        )
        abs_paths = _PORTABILITY.scan_for_absolute_paths(all_files)
        if abs_paths:
            issues.append(f"ABSOLUTE_PATH_LEAK: {abs_paths}")
        # Check no secrets
        secrets = _PORTABILITY.scan_for_secrets(package_manifest.get("included_files", []))
        if secrets:
            issues.append(f"SECRET_DETECTED: {secrets}")
        # Check path mode
        if package_manifest.get("path_mode") != RELATIVE_ONLY:
            issues.append("PATH_MODE must be RELATIVE_ONLY")
        # Check hash
        stored_hash = package_manifest.get("package_hash", "")
        check_manifest = {
            k: v for k, v in package_manifest.items()
            if k not in ("package_hash", "created_at")
        }
        expected_hash = _hash_manifest(check_manifest)
        if stored_hash and stored_hash != expected_hash:
            issues.append("PACKAGE_HASH_MISMATCH")
        return {
            "ok":     len(issues) == 0,
            "issues": issues,
            "package_id": package_manifest.get("package_id"),
        }
