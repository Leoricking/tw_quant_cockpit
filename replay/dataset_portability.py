"""
replay/dataset_portability.py — ReplayDatasetPortability v1.2.8

Portable package type definitions and portability utilities.
All portable packages use RELATIVE_ONLY path mode.
Absolute paths must NOT appear in portable manifests.

Package types:
- MANIFEST_ONLY:  manifest, session registry, lineage, hashes, relative paths
- METADATA_ONLY:  above + journal/score/strategy/review/challenge references
- FULL_PORTABLE:  above + explicitly allowlisted dataset files

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] Package must not contain secrets, .env, API tokens, broker credentials.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Package type constants
MANIFEST_ONLY  = "MANIFEST_ONLY"
METADATA_ONLY  = "METADATA_ONLY"
FULL_PORTABLE  = "FULL_PORTABLE"

VALID_PACKAGE_TYPES = {MANIFEST_ONLY, METADATA_ONLY, FULL_PORTABLE}

# Path mode
RELATIVE_ONLY  = "RELATIVE_ONLY"

# Secret / sensitive file patterns (must never be included)
SECRET_PATTERNS = [
    ".env", ".env.", "secret", "credential", "token",
    "api_key", "password", "broker", "shioaji", "megabroker",
    ".db", ".sqlite",
]

# Safe cache allowlist patterns (may be included if explicitly listed)
SAFE_CACHE_ALLOWLIST: List[str] = []


class ReplayDatasetPortability:
    """
    Portability utilities for replay datasets.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def is_safe_file(self, filename: str) -> bool:
        """Return True if this file is safe to include in a portable package."""
        fn_lower = filename.lower()
        for pattern in SECRET_PATTERNS:
            if pattern.lower() in fn_lower:
                return False
        return True

    def contains_absolute_path(self, path_str: str) -> bool:
        """Return True if the path string looks like an absolute path."""
        if os.path.isabs(path_str):
            return True
        if ":\\" in path_str or ":/" in path_str:
            return True
        return False

    def scan_for_secrets(self, file_list: List[str]) -> List[str]:
        """Return list of files that look like secrets/credentials."""
        return [f for f in file_list if not self.is_safe_file(f)]

    def scan_for_absolute_paths(self, paths: List[str]) -> List[str]:
        """Return list of paths that are absolute."""
        return [p for p in paths if self.contains_absolute_path(p)]

    def normalize_for_package(self, paths: List[str]) -> List[str]:
        """Convert paths to relative form for portable package."""
        result = []
        for p in paths:
            p = p.replace("\\", "/")
            if self.contains_absolute_path(p):
                # Strip drive/root, keep only relative part
                import re
                p = re.sub(r'^[A-Za-z]:[/\\]', '', p)
                p = p.lstrip("/\\")
            result.append(p)
        return result

    def validate_package_paths(self, paths: List[str]) -> Dict[str, Any]:
        """Validate that all paths in a package are relative."""
        absolute = self.scan_for_absolute_paths(paths)
        return {
            "ok":             len(absolute) == 0,
            "absolute_paths": absolute,
            "total":          len(paths),
        }
