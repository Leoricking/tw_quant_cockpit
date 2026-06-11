"""
maintenance/data_report_hygiene_query.py — DataReportHygieneQuery for v1.0.2.

Query interface for hygiene inventory, report manifests, and gitignore coverage.
Review-only — no modification of data.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Data Cleanup is Review Only. Archive Suggestions Only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from maintenance.data_report_hygiene_schema import (
    HygieneInventoryItem,
    HygieneReportManifest,
    SEV_HIGH, SEV_MEDIUM, SEV_BLOCKED,
)
from maintenance.data_report_hygiene_store import DataReportHygieneStore
from maintenance.data_report_hygiene_engine import (
    DataReportHygieneEngine, _STALE_DAYS, _LARGE_BYTES,
)

logger = logging.getLogger(__name__)


class DataReportHygieneQuery:
    """Query interface for hygiene scan results.

    [!] Research Only. No Real Orders. Review Only.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    review_only        = True

    def __init__(
        self,
        store: Optional[DataReportHygieneStore] = None,
        engine: Optional[DataReportHygieneEngine] = None,
    ) -> None:
        self._store  = store  or DataReportHygieneStore()
        self._engine = engine or DataReportHygieneEngine()

    def list_inventory(
        self,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        git_tracked: Optional[bool] = None,
    ) -> List[HygieneInventoryItem]:
        """List inventory items, with optional filters."""
        items = self._store.load_latest_inventory()
        if category:
            items = [i for i in items if i.category == category]
        if severity:
            items = [i for i in items if i.severity == severity]
        if git_tracked is not None:
            items = [i for i in items if i.is_git_tracked == git_tracked]
        return items

    def list_reports(
        self,
        module: Optional[str] = None,
        latest_only: bool = False,
    ) -> List[HygieneReportManifest]:
        """List report manifests, with optional filters."""
        manifests = self._store.load_latest_report_manifest()
        if module:
            manifests = [m for m in manifests if module.lower() in m.module.lower()]
        if latest_only:
            manifests = [m for m in manifests if m.is_latest]
        return manifests

    def list_tracked_runtime_outputs(self) -> List[str]:
        """List git-tracked runtime output files."""
        return self._engine.scan_git_tracked_runtime_outputs()

    def list_missing_gitignore_rules(self) -> List[str]:
        """List key patterns not covered by .gitignore."""
        coverage = self._engine.scan_gitignore_coverage()
        return [pattern for pattern, covered in coverage.items() if not covered]

    def list_stale_reports(self, limit: int = 20) -> List[HygieneInventoryItem]:
        """List stale report files (older than 30 days), newest first."""
        from maintenance.data_report_hygiene_schema import CATEGORY_REPORT
        items = self._store.load_latest_inventory()
        stale = [i for i in items if i.category == CATEGORY_REPORT and i.age_days > _STALE_DAYS]
        stale.sort(key=lambda x: x.age_days, reverse=True)
        return stale[:limit]

    def list_large_files(self, limit: int = 20) -> List[HygieneInventoryItem]:
        """List large files (>5MB), largest first."""
        items = self._store.load_latest_inventory()
        large = [i for i in items if i.size_bytes > _LARGE_BYTES]
        large.sort(key=lambda x: x.size_bytes, reverse=True)
        return large[:limit]

    def explain_item(self, item_id: str) -> Dict[str, Any]:
        """Explain why an item was flagged and what the suggested review action is."""
        items = self._store.load_latest_inventory()
        item  = next((i for i in items if i.item_id == item_id), None)
        if item is None:
            return {
                "item_id":              item_id,
                "found":                False,
                "why_flagged":          "Item not found in latest inventory",
                "suggested_review_action": "Run hygiene scan first",
                "no_auto_delete_note":  "Data Cleanup is Review Only — no automatic deletion",
                "no_real_orders":       True,
                "review_only":          True,
            }
        return {
            "item_id":              item.item_id,
            "found":                True,
            "path":                 item.path,
            "category":             item.category,
            "severity":             item.severity,
            "action_hint":          item.action_hint,
            "why_flagged":          item.reason,
            "is_runtime_output":    item.is_runtime_output,
            "is_git_tracked":       item.is_git_tracked,
            "is_git_ignored":       item.is_git_ignored,
            "should_be_ignored":    item.should_be_ignored,
            "age_days":             item.age_days,
            "size_bytes":           item.size_bytes,
            "suggested_review_action": (
                f"Review this file: {item.reason}. "
                "No automatic action will be taken."
            ),
            "no_auto_delete_note":  "Data Cleanup is Review Only — no automatic deletion, no archive, no file moves",
            "no_real_orders":       True,
            "production_blocked":   True,
            "review_only":          True,
            "data_cleanup_review_only": True,
        }
