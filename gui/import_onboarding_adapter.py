"""
gui/import_onboarding_adapter.py — ImportOnboardingAdapter for TW Quant Cockpit v1.1.1.

Adapter between GUI and data_onboarding package.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True by default. Destructive import disabled.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ImportOnboardingAdapter:
    """Adapter between GUI and data_onboarding package.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def discover(self, path: str) -> List[dict]:
        """Discover importable files in path. Returns list of DiscoveredFile dicts."""
        try:
            from data_onboarding.file_discovery import ImportFileDiscovery
            discovery = ImportFileDiscovery()
            files = discovery.discover(path)
            return [f.to_dict() for f in files]
        except Exception as exc:
            logger.warning("ImportOnboardingAdapter.discover: %s", exc)
            return []

    def validate(self, path: str) -> List[dict]:
        """Validate all files in path. Returns list of FileValidationResult dicts."""
        try:
            from data_onboarding.file_discovery import ImportFileDiscovery
            from data_onboarding.file_validator import ImportFileValidator
            discovery = ImportFileDiscovery()
            validator = ImportFileValidator()
            files = discovery.discover(path)
            results = []
            for f in files:
                val = validator.validate(f.file_path, f.detected_symbol, f.detected_dataset or 'daily')
                results.append(val.to_dict())
            return results
        except Exception as exc:
            logger.warning("ImportOnboardingAdapter.validate: %s", exc)
            return []

    def build_plan(self, path: str, mode: str = "MERGE_SAFE", dry_run: bool = True) -> dict:
        """Build an ImportPlan for path. Returns plan dict."""
        try:
            from data_onboarding.import_planner import ImportPlanner
            planner = ImportPlanner()
            plan = planner.build_plan(path, mode=mode, dry_run=dry_run, allow_replace=False)
            return plan.to_dict()
        except Exception as exc:
            logger.warning("ImportOnboardingAdapter.build_plan: %s", exc)
            return {"error": str(exc), "research_only": True}

    def execute(self, plan_id: str, allow_write: bool = False) -> dict:
        """Execute a stored plan. Returns summary dict."""
        try:
            from data_onboarding.onboarding_store import OnboardingStore
            from data_onboarding.batch_executor import BatchImportExecutor
            store = OnboardingStore()
            plan = store.load_latest_plan()
            if plan is None:
                return {"error": "No plan found", "research_only": True}
            if plan.plan_id != plan_id and plan_id:
                return {"error": f"Plan {plan_id} not found", "research_only": True}
            executor = BatchImportExecutor()
            summary = executor.execute(plan, allow_write=allow_write)
            store.save_summary(summary)
            return summary.to_dict()
        except Exception as exc:
            logger.warning("ImportOnboardingAdapter.execute: %s", exc)
            return {"error": str(exc), "research_only": True}

    def get_retry_manifest(self) -> dict:
        """Get latest retry manifest."""
        try:
            from data_onboarding.onboarding_store import OnboardingStore
            store = OnboardingStore()
            manifest = store.load_retry_manifest()
            if manifest:
                return manifest.to_dict()
            return {"status": "no_manifest", "research_only": True}
        except Exception as exc:
            logger.warning("ImportOnboardingAdapter.get_retry_manifest: %s", exc)
            return {"error": str(exc), "research_only": True}

    def build_report(self, mode: str = "real") -> str:
        """Build and save onboarding report. Returns file path."""
        try:
            from data_onboarding.onboarding_store import OnboardingStore
            from reports.data_import_onboarding_report import DataImportOnboardingReportBuilder
            store = OnboardingStore()
            plan = store.load_latest_plan()
            summary = store.load_latest_summary()
            builder = DataImportOnboardingReportBuilder(plan=plan, summary=summary, mode=mode)
            return builder.save()
        except Exception as exc:
            logger.warning("ImportOnboardingAdapter.build_report: %s", exc)
            return ""

    def refresh_coverage(self, tier: str = "research30") -> dict:
        """Refresh universe coverage after import."""
        try:
            from universe.universe_coverage_analyzer import UniverseCoverageAnalyzer
            analyzer = UniverseCoverageAnalyzer()
            result = analyzer.analyze()
            return result if isinstance(result, dict) else {"status": "refreshed", "tier": tier}
        except Exception as exc:
            logger.warning("ImportOnboardingAdapter.refresh_coverage: %s", exc)
            return {"status": "unavailable", "error": str(exc), "tier": tier}
