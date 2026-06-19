"""coverage_repair/health.py — CoverageRepairHealthV133 for v1.3.3.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Health check does NOT repair, execute, or enable trading.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class CoverageRepairHealthV133:
    """Health check for all v1.3.3 Coverage Repair Workflow components.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Health check does NOT repair, execute, or enable trading.
    """

    no_real_orders = True
    production_trading_blocked = True

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Run all health checks. Returns {check_name: ("PASS"|"FAIL", detail)}."""
        results: Dict[str, Tuple[str, str]] = {}

        results["package_import"] = self._check("coverage_repair package import",
            lambda: __import__("coverage_repair"))

        results["models_v133_import"] = self._check("models_v133 import",
            lambda: __import__("coverage_repair.models_v133", fromlist=["CoverageRepairTask"]))

        results["issue_mapper_import"] = self._check("issue_mapper import",
            lambda: __import__("coverage_repair.issue_mapper", fromlist=["CoverageRepairIssueMapper"]))

        results["priority_engine_import"] = self._check("priority_engine import",
            lambda: __import__("coverage_repair.priority_engine", fromlist=["CoverageRepairPriorityEngine"]))

        results["queue_import"] = self._check("queue import",
            lambda: __import__("coverage_repair.queue", fromlist=["CoverageRepairQueue"]))

        results["planner_import"] = self._check("planner import",
            lambda: __import__("coverage_repair.planner", fromlist=["CoverageRepairPlanner"]))

        results["executor_import"] = self._check("executor import",
            lambda: __import__("coverage_repair.executor", fromlist=["CoverageRepairExecutor"]))

        results["store_v133_import"] = self._check("store v1.3.3 import",
            lambda: __import__("coverage_repair.store", fromlist=["CoverageRepairStore"]))

        results["query_import"] = self._check("query import",
            lambda: __import__("coverage_repair.query", fromlist=["CoverageRepairQueryService"]))

        results["report_import"] = self._check("report import",
            lambda: __import__("coverage_repair.report", fromlist=["CoverageRepairReport"]))

        results["health_self_check"] = ("PASS", "CoverageRepairHealthV133 self-check OK")

        # Integration checks
        results["provider_integration"] = self._check("provider registry import",
            lambda: __import__("data.providers.real_data_provider_registry_v132",
                               fromlist=["RealDataProviderRegistryV132"]))

        results["quality_integration"] = self._check("dq_schema import",
            lambda: __import__("real_data_quality.dq_schema", fromlist=["*"]))

        results["coverage_integration"] = self._check("UniverseCoverageRecord import",
            lambda: __import__("universe.models", fromlist=["UniverseCoverageRecord"]))

        results["retry_integration"] = self._check("ProviderRetryPolicy import",
            lambda: __import__("data.providers.real_data_provider_retry",
                               fromlist=["ProviderRetryPolicy"]))

        # Safety flag checks
        results["no_mock_fallback"] = self._flag_check(
            "COVERAGE_REPAIR_MOCK_FALLBACK_ENABLED", False,
            "coverage_repair.models_v133", "COVERAGE_REPAIR_MOCK_FALLBACK_ENABLED"
        )

        results["no_destructive_action"] = self._flag_check(
            "COVERAGE_REPAIR_DESTRUCTIVE_ACTIONS_ENABLED", False,
            "coverage_repair.models_v133", "COVERAGE_REPAIR_DESTRUCTIVE_ACTIONS_ENABLED"
        )

        results["no_broker_action"] = self._flag_check(
            "BROKER_EXECUTION_ENABLED", False,
            "coverage_repair.models_v133", "BROKER_EXECUTION_ENABLED"
        )

        results["no_forbidden_trade_actions"] = self._forbidden_actions_check()

        results["version_1_3_3"] = self._check("version 1.3.3 in release info",
            lambda: self._check_version())

        return results

    def get_health_summary(self) -> Dict[str, Any]:
        """Return health summary dict."""
        results = self.run()
        passed = sum(1 for s, _ in results.values() if s == "PASS")
        failed = sum(1 for s, _ in results.values() if s == "FAIL")
        total = len(results)
        return {
            "schema_version": "1.3.3",
            "all_pass": failed == 0,
            "total_checks": total,
            "passed": passed,
            "failed": failed,
            "results": {k: {"status": s, "detail": d} for k, (s, d) in results.items()},
            "no_real_orders": True,
            "broker_execution_enabled": False,
            "production_trading_blocked": True,
            "coverage_repair_auto_execution_enabled": False,
            "coverage_repair_destructive_actions_enabled": False,
            "coverage_repair_mock_fallback_enabled": False,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _check(self, name: str, fn) -> Tuple[str, str]:
        try:
            fn()
            return ("PASS", f"{name} OK")
        except Exception as exc:
            return ("FAIL", f"{name} FAILED: {exc}")

    def _flag_check(self, flag_name: str, expected: bool, module: str, attr: str) -> Tuple[str, str]:
        try:
            mod = __import__(module, fromlist=[attr])
            val = getattr(mod, attr, None)
            if val == expected:
                return ("PASS", f"{flag_name} = {val} (expected {expected})")
            return ("FAIL", f"{flag_name} = {val} (expected {expected})")
        except Exception as exc:
            return ("FAIL", f"{flag_name} check error: {exc}")

    def _forbidden_actions_check(self) -> Tuple[str, str]:
        try:
            from coverage_repair.models_v133 import RepairActionType
            forbidden = RepairActionType._FORBIDDEN
            bad_found = []
            # Check no forbidden action is in the non-forbidden action set
            safe_actions = [v for k, v in RepairActionType.__dict__.items()
                            if not k.startswith("_") and isinstance(v, str)]
            for a in safe_actions:
                if RepairActionType.is_forbidden(a):
                    bad_found.append(a)
            if bad_found:
                return ("FAIL", f"Forbidden actions found in action set: {bad_found}")
            return ("PASS", f"No forbidden trade actions in action set. Forbidden set: {forbidden}")
        except Exception as exc:
            return ("FAIL", f"forbidden actions check error: {exc}")

    def _check_version(self) -> None:
        from release.version_info import VERSION
        if VERSION != "1.3.3":
            raise ValueError(f"Expected VERSION=1.3.3, got {VERSION}")
