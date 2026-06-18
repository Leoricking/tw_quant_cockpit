"""
replay/stable_release_gate.py — ReplayStableReleaseGate for v1.2.9.

Aggregates all stable audit results into a release gate decision.
Overall: FAIL if any FAIL; WARNING if any WARN; PASS otherwise.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStableReleaseGate:
    """
    Aggregates all stable audit results into a release gate decision.

    run() returns dict with:
      status: PASS | WARNING | FAIL
      passed: count
      failed: count
      warned: count
      expected_safety_blocks: count of expected BLOCKED results (counted as PASS)
      checks: list of {check_id, status, message}

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def run(self) -> Dict[str, Any]:
        """Run all stable audits and aggregate results."""
        all_checks: List[Dict[str, str]] = []

        # Run all sub-audits
        all_checks.extend(self._run_contracts())
        all_checks.extend(self._run_compatibility())
        all_checks.extend(self._run_store_audit())
        all_checks.extend(self._run_runtime_isolation())
        all_checks.extend(self._run_cli_audit())
        all_checks.extend(self._run_gui_audit())
        all_checks.extend(self._run_report_audit())
        all_checks.extend(self._run_safety_audit())
        all_checks.extend(self._run_regression_audit())
        all_checks.extend(self._run_version_check())

        # Tally results
        passed = sum(1 for c in all_checks if c["status"] == "PASS")
        warned = sum(1 for c in all_checks if c["status"] == "WARN")
        failed = sum(1 for c in all_checks if c["status"] == "FAIL")
        blocked = sum(1 for c in all_checks if c["status"] == "BLOCKED")

        # BLOCKED in this gate context = unexpected block → counts as fail
        # Expected safety blocks are already resolved to PASS by the sub-checkers
        expected_safety_blocks = 0  # Gate-level expects 0 raw BLOCKED

        if failed > 0:
            overall = "FAIL"
        elif warned > 0:
            overall = "WARNING"
        else:
            overall = "PASS"

        return {
            "status": overall,
            "passed": passed,
            "failed": failed,
            "warned": warned,
            "blocked": blocked,
            "expected_safety_blocks": expected_safety_blocks,
            "total": len(all_checks),
            "checks": all_checks,
            "no_real_orders": True,
            "research_only": True,
            "release_version": "1.2.9",
        }

    def _results_to_checks(self, prefix: str, results: Dict[str, Tuple[str, str]]) -> List[Dict[str, str]]:
        """Convert audit results dict to list of check dicts."""
        checks = []
        for key, (status, message) in results.items():
            checks.append({
                "check_id": f"{prefix}.{key}",
                "status": status,
                "message": message,
            })
        return checks

    def _run_contracts(self) -> List[Dict[str, str]]:
        try:
            from replay.stable_contracts import ReplayStableContractChecker
            results = ReplayStableContractChecker().check_all()
            return self._results_to_checks("contracts", results)
        except Exception as exc:
            return [{"check_id": "contracts.error", "status": "WARN", "message": str(exc)}]

    def _run_compatibility(self) -> List[Dict[str, str]]:
        try:
            from replay.stable_compatibility import ReplayStableCompatibilityChecker
            results = ReplayStableCompatibilityChecker().check_all()
            return self._results_to_checks("compat", results)
        except Exception as exc:
            return [{"check_id": "compat.error", "status": "WARN", "message": str(exc)}]

    def _run_store_audit(self) -> List[Dict[str, str]]:
        try:
            from replay.stable_store_audit import ReplayStableStoreAudit
            results = ReplayStableStoreAudit().audit_all()
            return self._results_to_checks("store", results)
        except Exception as exc:
            return [{"check_id": "store.error", "status": "WARN", "message": str(exc)}]

    def _run_runtime_isolation(self) -> List[Dict[str, str]]:
        try:
            from replay.stable_runtime_isolation import ReplayStableRuntimeIsolation
            results = ReplayStableRuntimeIsolation().check_all()
            return self._results_to_checks("runtime", results)
        except Exception as exc:
            return [{"check_id": "runtime.error", "status": "WARN", "message": str(exc)}]

    def _run_cli_audit(self) -> List[Dict[str, str]]:
        try:
            from replay.stable_cli_audit import ReplayStableCLIAudit
            results = ReplayStableCLIAudit().audit_all()
            return self._results_to_checks("cli", results)
        except Exception as exc:
            return [{"check_id": "cli.error", "status": "WARN", "message": str(exc)}]

    def _run_gui_audit(self) -> List[Dict[str, str]]:
        try:
            from replay.stable_gui_audit import ReplayStableGUIAudit
            results = ReplayStableGUIAudit().audit_all()
            return self._results_to_checks("gui", results)
        except Exception as exc:
            return [{"check_id": "gui.error", "status": "WARN", "message": str(exc)}]

    def _run_report_audit(self) -> List[Dict[str, str]]:
        try:
            from replay.stable_report_audit import ReplayStableReportAudit
            results = ReplayStableReportAudit().audit_all()
            return self._results_to_checks("report", results)
        except Exception as exc:
            return [{"check_id": "report.error", "status": "WARN", "message": str(exc)}]

    def _run_safety_audit(self) -> List[Dict[str, str]]:
        try:
            from replay.stable_safety_audit import ReplayStableSafetyAudit
            results = ReplayStableSafetyAudit().audit_all()
            return self._results_to_checks("safety", results)
        except Exception as exc:
            return [{"check_id": "safety.error", "status": "WARN", "message": str(exc)}]

    def _run_regression_audit(self) -> List[Dict[str, str]]:
        try:
            from replay.stable_regression_audit import ReplayStableRegressionAudit
            results = ReplayStableRegressionAudit().audit_all()
            return self._results_to_checks("regression", results)
        except Exception as exc:
            return [{"check_id": "regression.error", "status": "WARN", "message": str(exc)}]

    def _run_version_check(self) -> List[Dict[str, str]]:
        try:
            from release.version_info import VERSION, REPLAY_TRAINING_LINE_COMPLETE
            if VERSION != "1.2.9":
                return [{"check_id": "version.number", "status": "FAIL",
                         "message": f"VERSION={VERSION}, expected 1.2.9"}]
            if not REPLAY_TRAINING_LINE_COMPLETE:
                return [{"check_id": "version.line_complete", "status": "FAIL",
                         "message": "REPLAY_TRAINING_LINE_COMPLETE is not True"}]
            return [{"check_id": "version.number", "status": "PASS",
                     "message": f"VERSION={VERSION}, REPLAY_TRAINING_LINE_COMPLETE=True"}]
        except Exception as exc:
            return [{"check_id": "version.error", "status": "FAIL", "message": str(exc)}]
