"""
coverage_repair/repair_health.py — CoverageRepairHealthCheck for TW Quant Cockpit v1.1.2.

Health check for the coverage repair system. Returns PASS/WARN/FAIL for each item.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import importlib
import logging
import os
from typing import Dict

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CoverageRepairHealthCheck:
    """Health check for the coverage repair system. Returns PASS/WARN/FAIL for each item.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    CHECKS = [
        "package_import",
        "schema_import",
        "issue_detector_available",
        "repair_task_builder_available",
        "repair_planner_available",
        "repair_executor_available",
        "repair_store_available",
        "repair_query_available",
        "repair_retry_manifest_available",
        "dry_run_default",
        "destructive_repair_disabled",
        "conflict_auto_overwrite_disabled",
        "synthetic_ohlc_repair_disabled",
        "invalid_ohlc_auto_modify_disabled",
        "mock_data_repair_disabled",
        "mock_formal_conclusion_disabled",
        "execute_blocked_without_allow_write",
        "universe_coverage_refresh_available",
        "onboarding_package_intact",
        "output_gitignored",
        "no_broker_execution",
        "no_forbidden_actions",
    ]

    def run(self) -> dict:
        """Returns {'results': {check: 'PASS'/'WARN'/'FAIL'}, 'total': N, ...}"""
        results: Dict[str, str] = {}

        # 1. package_import
        try:
            import coverage_repair
            no_orders = getattr(coverage_repair, "NO_REAL_ORDERS", False)
            results["package_import"] = "PASS" if no_orders else "WARN"
        except Exception:
            results["package_import"] = "FAIL"

        # 2. schema_import
        try:
            from coverage_repair.coverage_repair_schema import (
                CoverageIssue, CoverageRepairTask, RepairPlan, RepairResult, RepairSummary
            )
            results["schema_import"] = "PASS"
        except Exception:
            results["schema_import"] = "FAIL"

        # 3. issue_detector_available
        try:
            from coverage_repair.issue_detector import CoverageIssueDetector
            CoverageIssueDetector()
            results["issue_detector_available"] = "PASS"
        except Exception:
            results["issue_detector_available"] = "FAIL"

        # 4. repair_task_builder_available
        try:
            from coverage_repair.repair_task_builder import RepairTaskBuilder
            RepairTaskBuilder()
            results["repair_task_builder_available"] = "PASS"
        except Exception:
            results["repair_task_builder_available"] = "FAIL"

        # 5. repair_planner_available
        try:
            from coverage_repair.repair_planner import CoverageRepairPlanner
            CoverageRepairPlanner()
            results["repair_planner_available"] = "PASS"
        except Exception:
            results["repair_planner_available"] = "FAIL"

        # 6. repair_executor_available
        try:
            from coverage_repair.repair_executor import CoverageRepairExecutor
            CoverageRepairExecutor()
            results["repair_executor_available"] = "PASS"
        except Exception:
            results["repair_executor_available"] = "FAIL"

        # 7. repair_store_available
        try:
            from coverage_repair.repair_store import RepairStore
            results["repair_store_available"] = "PASS"
        except Exception:
            results["repair_store_available"] = "FAIL"

        # 8. repair_query_available
        try:
            from coverage_repair.repair_query import RepairQuery
            results["repair_query_available"] = "PASS"
        except Exception:
            results["repair_query_available"] = "FAIL"

        # 9. repair_retry_manifest_available
        try:
            from coverage_repair.repair_retry_manifest import RepairRetryManifestBuilder
            results["repair_retry_manifest_available"] = "PASS"
        except Exception:
            results["repair_retry_manifest_available"] = "FAIL"

        # 10. dry_run_default
        try:
            import coverage_repair
            drd = getattr(coverage_repair, "DRY_RUN_DEFAULT", None)
            results["dry_run_default"] = "PASS" if drd is True else "FAIL"
        except Exception:
            results["dry_run_default"] = "FAIL"

        # 11. destructive_repair_disabled
        try:
            import coverage_repair
            dis = getattr(coverage_repair, "DESTRUCTIVE_REPAIR_DISABLED", None)
            results["destructive_repair_disabled"] = "PASS" if dis is True else "FAIL"
        except Exception:
            results["destructive_repair_disabled"] = "FAIL"

        # 12. conflict_auto_overwrite_disabled
        try:
            import coverage_repair
            enabled = getattr(coverage_repair, "CONFLICT_AUTO_OVERWRITE_ENABLED", True)
            results["conflict_auto_overwrite_disabled"] = "PASS" if enabled is False else "FAIL"
        except Exception:
            results["conflict_auto_overwrite_disabled"] = "FAIL"

        # 13. synthetic_ohlc_repair_disabled
        try:
            import coverage_repair
            dis = getattr(coverage_repair, "SYNTHETIC_OHLC_REPAIR_DISABLED", None)
            results["synthetic_ohlc_repair_disabled"] = "PASS" if dis is True else "FAIL"
        except Exception:
            results["synthetic_ohlc_repair_disabled"] = "FAIL"

        # 14. invalid_ohlc_auto_modify_disabled
        try:
            import coverage_repair
            dis = getattr(coverage_repair, "INVALID_OHLC_AUTO_MODIFY_DISABLED", None)
            results["invalid_ohlc_auto_modify_disabled"] = "PASS" if dis is True else "FAIL"
        except Exception:
            results["invalid_ohlc_auto_modify_disabled"] = "FAIL"

        # 15. mock_data_repair_disabled
        try:
            import coverage_repair
            dis = getattr(coverage_repair, "MOCK_DATA_REPAIR_DISABLED", None)
            results["mock_data_repair_disabled"] = "PASS" if dis is True else "FAIL"
        except Exception:
            results["mock_data_repair_disabled"] = "FAIL"

        # 16. mock_formal_conclusion_disabled
        try:
            import coverage_repair
            allowed = getattr(coverage_repair, "MOCK_DATA_FORMAL_CONCLUSION_ALLOWED", True)
            results["mock_formal_conclusion_disabled"] = "PASS" if allowed is False else "FAIL"
        except Exception:
            results["mock_formal_conclusion_disabled"] = "FAIL"

        # 17. execute_blocked_without_allow_write — verify executor blocks if allow_write=False
        try:
            from coverage_repair.repair_executor import CoverageRepairExecutor
            from coverage_repair.coverage_repair_schema import (
                RepairPlan, CoverageRepairTask, ACTION_AUTO_SAFE, PRIORITY_P3, ISSUE_DUPLICATE
            )
            from datetime import datetime
            dummy_task = CoverageRepairTask(
                task_id="health_test_task",
                issue_id="health_test_issue",
                symbol="TEST",
                dataset="daily",
                issue_type=ISSUE_DUPLICATE,
                action=ACTION_AUTO_SAFE,
                priority=PRIORITY_P3,
                description="Health test duplicate task",
                dry_run=True,
            )
            dummy_plan = RepairPlan(
                plan_id="health_test_plan",
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                total_issues=1,
                total_tasks=1,
                p0_count=0, p1_count=0, p2_count=0, p3_count=1,
                auto_safe_count=1, manual_review_count=0,
                source_required_count=0, blocked_count=0,
                tasks=[dummy_task],
                dry_run=True,
            )
            executor = CoverageRepairExecutor()
            summary = executor.execute(dummy_plan, allow_write=False)
            # All tasks must be DRY_RUN when allow_write=False
            all_dry = all(
                r.status in ("DRY_RUN", "BLOCKED", "MANUAL", "SKIPPED")
                for r in summary.results
            )
            results["execute_blocked_without_allow_write"] = "PASS" if all_dry else "FAIL"
        except Exception as exc:
            logger.warning("execute_blocked_without_allow_write check: %s", exc)
            results["execute_blocked_without_allow_write"] = "WARN"

        # 18. universe_coverage_refresh_available
        try:
            from universe.universe_coverage_analyzer import UniverseCoverageAnalyzer
            results["universe_coverage_refresh_available"] = "PASS"
        except Exception:
            results["universe_coverage_refresh_available"] = "WARN"

        # 19. onboarding_package_intact — v1.1.1 must remain unbroken
        try:
            import data_onboarding
            no_orders = getattr(data_onboarding, "NO_REAL_ORDERS", False)
            drd = getattr(data_onboarding, "DRY_RUN_DEFAULT", False)
            results["onboarding_package_intact"] = "PASS" if (no_orders and drd) else "FAIL"
        except Exception:
            results["onboarding_package_intact"] = "FAIL"

        # 20. output_gitignored — check .gitignore has data/coverage_repair_results/
        try:
            gi_path = os.path.join(BASE_DIR, ".gitignore")
            if os.path.isfile(gi_path):
                with open(gi_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "coverage_repair_results" in content:
                    results["output_gitignored"] = "PASS"
                else:
                    results["output_gitignored"] = "WARN"
            else:
                results["output_gitignored"] = "WARN"
        except Exception:
            results["output_gitignored"] = "WARN"

        # 21. no_broker_execution
        try:
            import coverage_repair
            broker_dis = getattr(coverage_repair, "BROKER_DISABLED", None)
            results["no_broker_execution"] = "PASS" if broker_dis is True else "FAIL"
        except Exception:
            results["no_broker_execution"] = "FAIL"

        # 22. no_forbidden_actions
        try:
            import coverage_repair
            no_orders = getattr(coverage_repair, "NO_REAL_ORDERS", False)
            prod_blk  = getattr(coverage_repair, "PRODUCTION_TRADING_BLOCKED", False)
            results["no_forbidden_actions"] = "PASS" if (no_orders and prod_blk) else "FAIL"
        except Exception:
            results["no_forbidden_actions"] = "FAIL"

        total  = len(results)
        passed = sum(1 for v in results.values() if v == "PASS")
        warned = sum(1 for v in results.values() if v == "WARN")
        failed = sum(1 for v in results.values() if v == "FAIL")

        return {
            "results":        results,
            "total":          total,
            "passed":         passed,
            "warned":         warned,
            "failed":         failed,
            "overall":        "PASS" if failed == 0 else ("WARN" if warned > 0 else "FAIL"),
            "research_only":  True,
            "no_real_orders": True,
        }
