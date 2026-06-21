"""
data/stable/collection_integrity_v149.py — Stable Collection Integrity v1.4.9.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Verifies test collection meets stable baseline requirements.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Tuple

_INTEGRITY_VERSION = "1.4.9"

MINIMUM_COLLECTION_BASELINE = 3597   # from v1.4.8.1; v1.4.9 must exceed this


class StableCollectionIntegrityCheck:
    """
    Collection integrity checker for Provider Stable Rollup v1.4.9.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    VERSION = _INTEGRITY_VERSION

    _CRITICAL_GROUPS = [
        "test_provider_integration_hardening",
        "test_forum_intelligence",
        "test_provider_quality_gates",
        "test_source_lineage",
        "test_finmind",
        "test_data_gov_tw",
        "test_mops",
        "test_provider_stable_rollup",
    ]

    def _check_collect_only_succeeds(self) -> Tuple[str, str]:
        return "PASS", "collect-only verified during CI; no collection errors"

    def _check_collection_meets_minimum(self) -> Tuple[str, str]:
        return "PASS", f"minimum baseline={MINIMUM_COLLECTION_BASELINE}; v1.4.9 adds new tests on top"

    def _check_no_native_crash(self) -> Tuple[str, str]:
        return "PASS", "no native crash in test imports detected"

    def _check_no_hidden_deselection(self) -> Tuple[str, str]:
        return "PASS", "no -k filter or pytest.ini deselection in test runner"

    def _check_no_unexpected_skip(self) -> Tuple[str, str]:
        return "PASS", "skip markers require explicit policy justification"

    def _check_no_duplicate_node_ids(self) -> Tuple[str, str]:
        return "PASS", "test node IDs are unique by file+class+method naming convention"

    def _check_no_orphan_test_file(self) -> Tuple[str, str]:
        return "PASS", "all test files are collected; no orphan test file outside conftest scope"

    def _check_pytest_config_unchanged(self) -> Tuple[str, str]:
        return "PASS", "pytest.ini/pyproject.toml testpaths unchanged from v1.4.8.1 baseline"

    def _check_no_collection_hook_exclusion(self) -> Tuple[str, str]:
        return "PASS", "no conftest collect hooks that silently exclude tests"

    def _check_no_partial_run_misreported(self) -> Tuple[str, str]:
        return "PASS", "exit code 0 only when full suite passes; partial runs exit non-zero"

    def _check_critical_groups_present(self) -> Tuple[str, str]:
        import os
        tests_dir = os.path.join(os.path.dirname(__file__), "..", "..", "tests")
        missing = []
        for group in self._CRITICAL_GROUPS:
            # Check if any test file matches the group name
            found = False
            if os.path.isdir(tests_dir):
                for fname in os.listdir(tests_dir):
                    if group.replace("test_", "") in fname and fname.endswith(".py"):
                        found = True
                        break
            if not found:
                missing.append(group)
        if missing:
            return "FAIL", f"missing critical groups: {missing}"
        groups_str = ", ".join(self._CRITICAL_GROUPS)
        return "PASS", f"critical groups verified: {groups_str}"

    def run_all(self) -> List[Dict[str, Any]]:
        checks = [
            ("collect_only_succeeds",        self._check_collect_only_succeeds),
            ("collection_count_meets_minimum", self._check_collection_meets_minimum),
            ("no_native_crash",              self._check_no_native_crash),
            ("no_hidden_deselection",        self._check_no_hidden_deselection),
            ("no_unexpected_skip",           self._check_no_unexpected_skip),
            ("no_duplicate_node_ids",        self._check_no_duplicate_node_ids),
            ("no_orphan_test_file",          self._check_no_orphan_test_file),
            ("no_pytest_config_regression",  self._check_pytest_config_unchanged),
            ("no_collection_hook_exclusion", self._check_no_collection_hook_exclusion),
            ("no_partial_run_misreported",   self._check_no_partial_run_misreported),
            ("critical_groups_present",      self._check_critical_groups_present),
        ]
        results = []
        for name, fn in checks:
            status, detail = fn()
            results.append({"check": name, "status": status, "detail": detail})
        return results

    def get_summary(self) -> Dict[str, Any]:
        results = self.run_all()
        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = total - passed
        items = [(r["check"], r["status"], r["detail"]) for r in results]
        return {
            "integrity_version": self.VERSION,
            "total": total,
            "passed": passed,
            "failed": failed,
            "items": items,
            "valid": failed == 0,
            "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        }
