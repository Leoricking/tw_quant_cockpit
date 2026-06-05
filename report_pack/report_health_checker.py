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
    STATUS_ENV_LIMITED, STATUS_NOT_GENERATED, STATUS_MISSING_OPT, STATUS_MISSING_REQ,
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
        failed  = pack.failed_count

        # Detailed missing breakdown
        env_limited     = sum(1 for i in pack.items if i.status == STATUS_ENV_LIMITED)
        not_generated   = sum(1 for i in pack.items if i.status == STATUS_NOT_GENERATED)
        missing_optional = sum(1 for i in pack.items if i.status in (STATUS_MISSING_OPT,))
        # Required missing: only STATUS_MISSING counts as critical
        required_missing_count = sum(1 for i in pack.items if i.status == STATUS_MISSING)
        # Legacy total missing for display
        missing = pack.missing_count + env_limited + not_generated + missing_optional

        # Score based on ready out of total
        score = (ready / total * 100.0) if total > 0 else 0.0

        # Health is determined by required missing and failed only
        critical_missing = self._critical_missing(pack.items)
        if failed == 0 and required_missing_count == 0 and not critical_missing:
            health_label = "HEALTHY"
        else:
            health_label = self._label(score)

        return {
            "pack_type":              pack.pack_type,
            "report_date":            pack.report_date,
            "health_label":           health_label,
            "health_score":           round(score, 1),
            "total_reports":          total,
            "ready_count":            ready,
            "missing_count":          missing,
            "required_missing_count": required_missing_count,
            "env_limited_count":      env_limited,
            "not_generated_count":    not_generated,
            "failed_count":           failed,
            "critical_missing":       critical_missing,
            "recommendation":         self._recommendation(health_label, critical_missing, env_limited, not_generated),
            "no_real_orders":         True,
            "production_blocked":     True,
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
        """Return list of critical (required) report types that are missing.

        Only STATUS_MISSING (not ENV_LIMITED or NOT_GENERATED) counts as critical.
        """
        _CRITICAL_TYPES = [
            "daily_market", "auto_report", "data_quality",
            "signal_quality",
        ]
        return [
            i.report_type
            for i in items
            if i.status == STATUS_MISSING and i.report_type in _CRITICAL_TYPES
        ]

    def _recommendation(
        self,
        health_label: str,
        critical_missing: List[str],
        env_limited: int = 0,
        not_generated: int = 0,
    ) -> str:
        parts = []
        if health_label == "HEALTHY" and not critical_missing:
            parts.append("All required reports ready. Pack is healthy.")
        elif critical_missing:
            parts.append(
                f"Critical reports missing: {', '.join(critical_missing)}. "
                "Run auto-report daily profile to regenerate."
            )
        elif health_label == "DEGRADED":
            parts.append("Some required reports missing. Run report commands for missing types.")
        else:
            parts.append("Many reports missing or failed. Run full auto-report to restore.")

        if env_limited:
            parts.append(
                f"{env_limited} report(s) are ENV_LIMITED — set provider token to enable."
            )
        if not_generated:
            parts.append(
                f"{not_generated} optional report(s) not yet generated — not a release failure."
            )
        return " ".join(parts)
