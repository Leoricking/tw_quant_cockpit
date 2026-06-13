"""
data_onboarding/onboarding_health.py — OnboardingHealthCheck for TW Quant Cockpit v1.1.1.

Health check for the onboarding system. Returns PASS/WARN/FAIL for each item.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import importlib
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class OnboardingHealthCheck:
    """Health check for the onboarding system. Returns PASS/WARN/FAIL for each item.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    CHECKS = [
        "package_import",
        "schema_import",
        "file_discovery_available",
        "schema_detector_available",
        "file_validator_available",
        "duplicate_detector_available",
        "import_planner_available",
        "batch_executor_available",
        "retry_manifest_available",
        "dry_run_default",
        "replace_explicit_blocked",
        "conflict_auto_overwrite_disabled",
        "destructive_import_disabled",
        "mock_formal_conclusion_disabled",
        "xq_importer_compatible",
        "universe_coverage_refresh_available",
        "output_gitignored",
        "no_broker_execution",
        "no_forbidden_actions",
    ]

    def run(self) -> dict:
        """Returns {'results': {check: 'PASS'/'WARN'/'FAIL'}, 'total': N, 'passed': N}"""
        results: Dict[str, str] = {}

        # 1. package_import
        try:
            import data_onboarding
            no_orders = getattr(data_onboarding, "NO_REAL_ORDERS", False)
            results["package_import"] = "PASS" if no_orders else "WARN"
        except Exception as exc:
            results["package_import"] = "FAIL"

        # 2. schema_import
        try:
            from data_onboarding.onboarding_schema import (
                ImportPlan, ImportPlanItem, ImportResult, BatchImportSummary, RetryManifest
            )
            results["schema_import"] = "PASS"
        except Exception:
            results["schema_import"] = "FAIL"

        # 3. file_discovery_available
        try:
            from data_onboarding.file_discovery import ImportFileDiscovery
            d = ImportFileDiscovery()
            results["file_discovery_available"] = "PASS"
        except Exception:
            results["file_discovery_available"] = "FAIL"

        # 4. schema_detector_available
        try:
            from data_onboarding.schema_detector import ColumnMappingDetector
            results["schema_detector_available"] = "PASS"
        except Exception:
            results["schema_detector_available"] = "FAIL"

        # 5. file_validator_available
        try:
            from data_onboarding.file_validator import ImportFileValidator
            results["file_validator_available"] = "PASS"
        except Exception:
            results["file_validator_available"] = "FAIL"

        # 6. duplicate_detector_available
        try:
            from data_onboarding.duplicate_detector import DuplicateDetector
            results["duplicate_detector_available"] = "PASS"
        except Exception:
            results["duplicate_detector_available"] = "FAIL"

        # 7. import_planner_available
        try:
            from data_onboarding.import_planner import ImportPlanner
            results["import_planner_available"] = "PASS"
        except Exception:
            results["import_planner_available"] = "FAIL"

        # 8. batch_executor_available
        try:
            from data_onboarding.batch_executor import BatchImportExecutor
            results["batch_executor_available"] = "PASS"
        except Exception:
            results["batch_executor_available"] = "FAIL"

        # 9. retry_manifest_available
        try:
            from data_onboarding.retry_manifest import RetryManifestBuilder
            results["retry_manifest_available"] = "PASS"
        except Exception:
            results["retry_manifest_available"] = "FAIL"

        # 10. dry_run_default
        try:
            import data_onboarding
            drd = getattr(data_onboarding, "DRY_RUN_DEFAULT", None)
            results["dry_run_default"] = "PASS" if drd is True else "FAIL"
        except Exception:
            results["dry_run_default"] = "FAIL"

        # 11. replace_explicit_blocked
        try:
            import data_onboarding
            blocked = getattr(data_onboarding, "REPLACE_EXPLICIT_BLOCKED_BY_DEFAULT", None)
            results["replace_explicit_blocked"] = "PASS" if blocked is True else "FAIL"
        except Exception:
            results["replace_explicit_blocked"] = "FAIL"

        # 12. conflict_auto_overwrite_disabled
        try:
            import data_onboarding
            enabled = getattr(data_onboarding, "CONFLICT_AUTO_OVERWRITE_ENABLED", True)
            results["conflict_auto_overwrite_disabled"] = "PASS" if enabled is False else "FAIL"
        except Exception:
            results["conflict_auto_overwrite_disabled"] = "FAIL"

        # 13. destructive_import_disabled
        try:
            import data_onboarding
            dis = getattr(data_onboarding, "DESTRUCTIVE_IMPORT_DISABLED", None)
            results["destructive_import_disabled"] = "PASS" if dis is True else "FAIL"
        except Exception:
            results["destructive_import_disabled"] = "FAIL"

        # 14. mock_formal_conclusion_disabled
        try:
            import data_onboarding
            mock_ok = getattr(data_onboarding, "MOCK_DATA_FORMAL_CONCLUSION_ALLOWED", True)
            results["mock_formal_conclusion_disabled"] = "PASS" if mock_ok is False else "FAIL"
        except Exception:
            results["mock_formal_conclusion_disabled"] = "FAIL"

        # 15. xq_importer_compatible
        try:
            from data.xq_export_importer import XQExportImporter
            results["xq_importer_compatible"] = "PASS"
        except Exception:
            results["xq_importer_compatible"] = "WARN"

        # 16. universe_coverage_refresh_available
        try:
            from universe.universe_coverage_analyzer import UniverseCoverageAnalyzer
            results["universe_coverage_refresh_available"] = "PASS"
        except Exception:
            results["universe_coverage_refresh_available"] = "WARN"

        # 17. output_gitignored — check .gitignore has data/import_reports/
        try:
            import os
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            gi_path = os.path.join(base, ".gitignore")
            if os.path.isfile(gi_path):
                with open(gi_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "data/import_reports/" in content or "import_reports" in content:
                    results["output_gitignored"] = "PASS"
                else:
                    results["output_gitignored"] = "WARN"
            else:
                results["output_gitignored"] = "WARN"
        except Exception:
            results["output_gitignored"] = "WARN"

        # 18. no_broker_execution
        try:
            import data_onboarding
            broker_dis = getattr(data_onboarding, "BROKER_DISABLED", None)
            results["no_broker_execution"] = "PASS" if broker_dis is True else "FAIL"
        except Exception:
            results["no_broker_execution"] = "FAIL"

        # 19. no_forbidden_actions
        try:
            import data_onboarding
            no_orders = getattr(data_onboarding, "NO_REAL_ORDERS", False)
            prod_blk  = getattr(data_onboarding, "PRODUCTION_TRADING_BLOCKED", False)
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
