"""
gui/coverage_repair_adapter.py — CoverageRepairAdapter for TW Quant Cockpit v1.1.2.

Adapter between GUI and coverage_repair package.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True by default. Destructive repair disabled.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CoverageRepairAdapter:
    """Adapter between GUI and coverage_repair package.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def detect(self, symbols: Optional[List[str]] = None) -> List[dict]:
        """Detect coverage issues. Returns list of CoverageIssue dicts."""
        try:
            from coverage_repair.issue_detector import CoverageIssueDetector
            detector = CoverageIssueDetector()
            issues = detector.detect_all(symbols=symbols)
            return [i.to_dict() for i in issues]
        except Exception as exc:
            logger.warning("CoverageRepairAdapter.detect: %s", exc)
            return []

    def build_plan(self, symbols: Optional[List[str]] = None, dry_run: bool = True) -> dict:
        """Build a RepairPlan. Returns plan dict."""
        try:
            from coverage_repair.repair_planner import CoverageRepairPlanner
            planner = CoverageRepairPlanner()
            plan = planner.build_plan(symbols=symbols, dry_run=dry_run)
            return plan.to_dict()
        except Exception as exc:
            logger.warning("CoverageRepairAdapter.build_plan: %s", exc)
            return {"error": str(exc), "research_only": True}

    def execute(self, allow_write: bool = False) -> dict:
        """Execute the latest stored plan. Returns RepairSummary dict."""
        try:
            from coverage_repair.repair_store import RepairStore
            from coverage_repair.repair_executor import CoverageRepairExecutor
            store = RepairStore()
            plan = store.load_latest_plan()
            if plan is None:
                return {"error": "No plan found", "research_only": True}
            executor = CoverageRepairExecutor()
            summary = executor.execute(plan, allow_write=allow_write)
            store.save_summary(summary)
            return summary.to_dict()
        except Exception as exc:
            logger.warning("CoverageRepairAdapter.execute: %s", exc)
            return {"error": str(exc), "research_only": True}

    def get_health(self) -> dict:
        """Run coverage repair health check."""
        try:
            from coverage_repair.repair_health import CoverageRepairHealthCheck
            checker = CoverageRepairHealthCheck()
            return checker.run()
        except Exception as exc:
            logger.warning("CoverageRepairAdapter.get_health: %s", exc)
            return {"error": str(exc), "overall": "FAIL", "research_only": True}

    def build_report(self, mode: str = "real") -> str:
        """Build and save coverage repair report. Returns file path."""
        try:
            from coverage_repair.repair_store import RepairStore
            from reports.coverage_repair_report import CoverageRepairReportBuilder
            store = RepairStore()
            plan = store.load_latest_plan()
            summary = store.load_latest_summary()
            builder = CoverageRepairReportBuilder(plan=plan, summary=summary, mode=mode)
            return builder.save()
        except Exception as exc:
            logger.warning("CoverageRepairAdapter.build_report: %s", exc)
            return ""

    def get_retry_manifest(self) -> dict:
        """Get latest retry manifest."""
        try:
            from coverage_repair.repair_store import RepairStore
            store = RepairStore()
            manifest = store.load_latest_retry_manifest()
            if manifest:
                return manifest.to_dict()
            return {"status": "no_manifest", "research_only": True}
        except Exception as exc:
            logger.warning("CoverageRepairAdapter.get_retry_manifest: %s", exc)
            return {"error": str(exc), "research_only": True}

    def refresh_coverage(self, tier: str = "research30") -> dict:
        """Refresh universe coverage."""
        try:
            from universe.universe_coverage_analyzer import UniverseCoverageAnalyzer
            analyzer = UniverseCoverageAnalyzer()
            result = analyzer.analyze()
            return result if isinstance(result, dict) else {"status": "refreshed", "tier": tier}
        except Exception as exc:
            logger.warning("CoverageRepairAdapter.refresh_coverage: %s", exc)
            return {"status": "unavailable", "error": str(exc), "tier": tier}
