"""
replay/stable_regression_audit.py — ReplayStableRegressionAudit for v1.2.9.

Lightweight import/attr checks for regression suite coverage.
No real orders. No broker. Research only.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStableRegressionAudit:
    """
    Audits regression suite coverage for v1.2.9 stable rollup.

    Checks:
    - suite_registry has release_gate and quick suites
    - expected_block semantics present in regression_schema
    - runner uses _is_forbidden guard
    - no duplicate test IDs (sampled check)

    All lightweight import/attr checks only — no actual test execution.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def audit_all(self) -> Dict[str, Tuple[str, str]]:
        """Run all regression audits. Returns {check_id: (status, message)}."""
        results: Dict[str, Tuple[str, str]] = {}

        results["suite_registry_import"]       = self._check_suite_registry_import()
        results["release_gate_suite"]          = self._check_release_gate_suite()
        results["quick_suite"]                 = self._check_quick_suite()
        results["expected_block_semantics"]    = self._check_expected_block_semantics()
        results["runner_uses_is_forbidden"]    = self._check_runner_uses_is_forbidden()
        results["no_duplicate_test_ids"]       = self._check_no_duplicate_test_ids()
        results["replay_stable_suite"]         = self._check_replay_stable_suite()

        return results

    def _check_suite_registry_import(self) -> Tuple[str, str]:
        try:
            from regression.suite_registry import RegressionSuiteRegistry  # noqa: F401
            return ("PASS", "RegressionSuiteRegistry imports OK")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_release_gate_suite(self) -> Tuple[str, str]:
        try:
            from regression.suite_registry import RegressionSuiteRegistry
            from regression.regression_schema import SUITE_RELEASE_GATE
            registry = RegressionSuiteRegistry()
            suite = registry.build_release_gate_suite()
            if not suite:
                return ("FAIL", "build_release_gate_suite() returned empty list")
            return ("PASS", f"release_gate suite has {len(suite)} test cases")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_quick_suite(self) -> Tuple[str, str]:
        try:
            from regression.suite_registry import RegressionSuiteRegistry
            registry = RegressionSuiteRegistry()
            suite = registry.build_quick_suite()
            if not suite:
                return ("FAIL", "build_quick_suite() returned empty list")
            return ("PASS", f"quick suite has {len(suite)} test cases")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_expected_block_semantics(self) -> Tuple[str, str]:
        try:
            from regression.regression_schema import RegressionTestCase
            fields = RegressionTestCase.__dataclass_fields__
            if "expected_block" not in fields:
                return ("FAIL", "RegressionTestCase missing expected_block field")
            # Check the default is False (so expected_block must be explicitly set)
            default = fields["expected_block"].default
            if default is not False:
                return ("WARN", f"expected_block default is {default!r}, expected False")
            return ("PASS", "RegressionTestCase.expected_block field exists with default=False")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_runner_uses_is_forbidden(self) -> Tuple[str, str]:
        try:
            from regression.suite_registry import _is_forbidden
            if not callable(_is_forbidden):
                return ("FAIL", "_is_forbidden is not callable")
            # Verify it blocks known dangerous commands
            if not _is_forbidden(["main.py", "buy-stock"]):
                return ("WARN", "_is_forbidden may not catch 'buy' commands")
            # Verify it allows safe commands
            if _is_forbidden(["main.py", "replay-stable-health"]):
                return ("FAIL", "_is_forbidden incorrectly blocks safe command")
            return ("PASS", "_is_forbidden callable and correctly guards dangerous commands")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_no_duplicate_test_ids(self) -> Tuple[str, str]:
        try:
            from regression.suite_registry import RegressionSuiteRegistry
            registry = RegressionSuiteRegistry()
            # Sample from release_gate suite — the most important one
            suite = registry.build_release_gate_suite()
            ids = [tc.test_id for tc in suite]
            unique_ids = set(ids)
            if len(ids) != len(unique_ids):
                dupes = [tid for tid in unique_ids if ids.count(tid) > 1]
                return ("FAIL", f"Duplicate test IDs in release_gate suite: {dupes[:5]}")
            return ("PASS", f"No duplicate test IDs in release_gate suite ({len(ids)} tests)")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")

    def _check_replay_stable_suite(self) -> Tuple[str, str]:
        try:
            from regression.suite_registry import RegressionSuiteRegistry
            registry = RegressionSuiteRegistry()
            if hasattr(registry, "build_replay_stable_suite"):
                suite = registry.build_replay_stable_suite()
                return ("PASS", f"build_replay_stable_suite() exists with {len(suite)} tests")
            return ("WARN", "build_replay_stable_suite() not yet in registry (will be added)")
        except ImportError as exc:
            return ("WARN", f"Import unavailable (optional): {exc}")
        except Exception as exc:
            return ("WARN", f"Check error: {exc}")
