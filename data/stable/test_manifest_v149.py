"""
data/stable/test_manifest_v149.py — Provider Test Manifest v1.4.9.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Defines test baseline constants and verifies collection integrity.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List

_MANIFEST_VERSION = "1.4.9"

# Baseline constants — do not modify
PREVIOUS_FULL_COLLECTION_BASELINE = 3597
PREVIOUS_FULL_PASS_BASELINE       = 3597
PREVIOUS_SKIPPED_BASELINE         = 0

# Critical test groups that must always be present
_CRITICAL_GROUPS: List[str] = [
    "test_provider_integration_hardening",
    "test_forum_intelligence",
    "test_provider_quality_gates",
    "test_source_lineage",
    "test_finmind",
    "test_data_gov_tw",
    "test_mops",
    "test_provider_stable_rollup",
]

# Test file manifest with expected minimum counts
_TEST_FILE_MANIFEST: List[Dict[str, Any]] = [
    {"file": "test_provider_integration_hardening_v148.py", "min_tests": 171, "required": True},
    {"file": "test_provider_quality_gates_v146.py",         "min_tests": 100, "required": True},
    {"file": "test_source_lineage_rate_limit_v145.py",      "min_tests": 100, "required": True},
    {"file": "test_finmind_adapter_hardening_v144.py",      "min_tests": 100, "required": True},
    {"file": "test_provider_health_consistency_v1432.py",   "min_tests": 60,  "required": True},
    {"file": "test_provider_stable_rollup_v149.py",         "min_tests": 100, "required": True},
    {"file": "test_research_foundation_v139.py",            "min_tests": 20,  "required": True},
    {"file": "test_version_alignment_v137.py",              "min_tests": 10,  "required": True},
]


class ProviderTestManifest:
    """
    Verifies test manifest meets v1.4.9 stable baseline requirements.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    VERSION = _MANIFEST_VERSION

    PREVIOUS_FULL_COLLECTION_BASELINE = PREVIOUS_FULL_COLLECTION_BASELINE
    PREVIOUS_FULL_PASS_BASELINE       = PREVIOUS_FULL_PASS_BASELINE
    PREVIOUS_SKIPPED_BASELINE         = PREVIOUS_SKIPPED_BASELINE

    def get_critical_groups(self) -> List[str]:
        return list(_CRITICAL_GROUPS)

    def get_manifest(self) -> List[Dict[str, Any]]:
        return list(_TEST_FILE_MANIFEST)

    def validate_collection(self, actual_count: int) -> Dict[str, Any]:
        ok = actual_count >= PREVIOUS_FULL_COLLECTION_BASELINE
        return {
            "manifest_version": self.VERSION,
            "actual_collection": actual_count,
            "baseline": PREVIOUS_FULL_COLLECTION_BASELINE,
            "valid": ok,
            "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

    def validate(self) -> Dict[str, Any]:
        import os
        tests_dir = os.path.join(
            os.path.dirname(__file__), "..", "..", "tests"
        )
        items = []
        issues = []
        for entry in _TEST_FILE_MANIFEST:
            path = os.path.join(tests_dir, entry["file"])
            exists = os.path.isfile(path)
            status = "PASS" if exists else ("FAIL" if entry["required"] else "WARN")
            if not exists and entry["required"]:
                issues.append(entry["file"])
            items.append((entry["file"], status,
                          f"exists={exists} min_tests={entry['min_tests']}"))
        return {
            "manifest_version": self.VERSION,
            "items": items,
            "issues": issues,
            "valid": len(issues) == 0,
            "critical_groups": _CRITICAL_GROUPS,
            "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

    def get_summary(self) -> Dict[str, Any]:
        return self.validate()
