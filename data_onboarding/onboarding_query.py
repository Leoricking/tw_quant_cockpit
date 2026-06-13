"""
data_onboarding/onboarding_query.py — OnboardingQuery for TW Quant Cockpit v1.1.1.

Read-only queries over saved onboarding data.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

from data_onboarding.onboarding_schema import (
    ImportResult, ImportPlanItem, BatchImportSummary, RetryManifest,
)
from data_onboarding.onboarding_store import OnboardingStore


class OnboardingQuery:
    """Read-only queries over saved onboarding data.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def __init__(self, store: Optional[OnboardingStore] = None) -> None:
        self._store = store or OnboardingStore()

    def list_failed(self) -> List[ImportResult]:
        summary = self._store.load_latest_summary()
        if not summary:
            return []
        return [r for r in summary.results if r.status == "FAILED"]

    def list_conflicts(self) -> List[ImportResult]:
        summary = self._store.load_latest_summary()
        if not summary:
            return []
        return [r for r in summary.results if r.conflicts_detected > 0]

    def list_blocked(self) -> List[ImportPlanItem]:
        plan = self._store.load_latest_plan()
        if not plan:
            return []
        return [i for i in plan.items if i.action == "BLOCKED"]

    def list_succeeded(self) -> List[ImportResult]:
        summary = self._store.load_latest_summary()
        if not summary:
            return []
        return [r for r in summary.results if r.status in ("OK", "DRY_RUN")]

    def get_latest_summary(self) -> Optional[BatchImportSummary]:
        return self._store.load_latest_summary()

    def get_retry_manifest(self) -> Optional[RetryManifest]:
        return self._store.load_retry_manifest()

    def summarize_status(self) -> dict:
        summary = self._store.load_latest_summary()
        if not summary:
            return {
                "status": "no_data",
                "research_only": True, "no_real_orders": True,
            }
        return {
            "batch_id":    summary.batch_id,
            "total_files": summary.total_files,
            "succeeded":   summary.succeeded,
            "failed":      summary.failed,
            "skipped":     summary.skipped,
            "blocked":     summary.blocked,
            "dry_run":     summary.dry_run,
            "research_only":  True,
            "no_real_orders": True,
        }
