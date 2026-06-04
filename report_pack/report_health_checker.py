"""report_pack/report_health_checker.py — ReportHealthChecker for TW Quant Cockpit v0.5.4.

Evaluates health of each report type and the overall pack.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

from report_pack.report_pack_schema import (
    ReportPack, ReportPackItem,
    STATUS_READY, STATUS_PARTIAL, STATUS_MISSING, STATUS_FAILED,
)

logger = logging.getLogger(__name__)

# Health thresholds
_HEALTH_GREEN  = 80.0  # >= 80% → HEALTHY
_HEALTH_YELLOW = 50.0  # >= 50% → DEGRADED
# < 50% → CRITICAL


class ReportHealthChecker:
    """Evaluates health of a ReportPack or individual report items.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def check_pack(self, pack: ReportPack) -> dict:
        """Return health summary dict for the given ReportPack."""
        total   = len(pack.items)
        ready   = pack.ready_count
        missing = pack.missing_count
        failed  = pack.failed_count

        score = (ready / total * 100.0) if total > 0 else 0.0
        health_label = self._label(score)

        critical_missing = self._critical_missing(pack.items)

        return {
            "pack_type":        pack.pack_type,
            "report_date":      pack.report_date,
            "health_label":     health_label,
            "health_score":     round(score, 1),
            "total_reports":    total,
            "ready_count":      ready,
            "missing_count":    missing,
            "failed_count":     failed,
            "critical_missing": critical_missing,
            "recommendation":   self._recommendation(health_label, critical_missing),
            "no_real_orders":   True,
            "production_blocked": True,
        }

    def check_item(self, item: ReportPackItem) -> dict:
        """Return health info for a single ReportPackItem."""
        return {
            "report_type":  item.report_type,
            "status":       item.status,
            "healthy":      item.status == STATUS_READY,
            "path":         item.path,
            "size_bytes":   item.size_bytes,
            "error":        item.error,
            "notes":        item.notes,
        }

    def summary_score(self, pack: ReportPack) -> float:
        """Return 0–100 health score for the pack."""
        total = len(pack.items)
        if total == 0:
            return 0.0
        return round(pack.ready_count / total * 100.0, 1)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _label(self, score: float) -> str:
        if score >= _HEALTH_GREEN:
            return "HEALTHY"
        if score >= _HEALTH_YELLOW:
            return "DEGRADED"
        return "CRITICAL"

    def _critical_missing(self, items: List[ReportPackItem]) -> List[str]:
        """Return list of critical (required) report types that are missing."""
        _CRITICAL_TYPES = [
            "daily_market", "auto_report", "data_quality",
            "provider", "signal_quality",
        ]
        return [
            i.report_type
            for i in items
            if i.status != STATUS_READY and i.report_type in _CRITICAL_TYPES
        ]

    def _recommendation(self, health_label: str, critical_missing: List[str]) -> str:
        if health_label == "HEALTHY" and not critical_missing:
            return "All core reports ready. Pack is healthy."
        if critical_missing:
            return (
                f"Critical reports missing: {', '.join(critical_missing)}. "
                "Run auto-report daily profile to regenerate."
            )
        if health_label == "DEGRADED":
            return "Some reports missing. Run report commands for missing types."
        return "Many reports missing or failed. Run full auto-report to restore."
