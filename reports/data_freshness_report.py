"""
reports/data_freshness_report.py — Data Freshness Monitor Report Builder for v1.1.3.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Auto External Refresh: DISABLED. Stale Auto Repair: DISABLED.
[!] Future Date does not count as Fresh.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Safety invariants — MUST NOT be changed
NO_REAL_ORDERS             = True
AUTO_DOWNLOAD_DISABLED     = True
AUTO_REPAIR_DISABLED       = True
RESEARCH_ONLY              = True
MOCK_FORMAL_FRESHNESS_DISABLED = True

VERSION = "1.1.3"

# Dataset display order
_DATASET_ORDER = [
    "DAILY_PRICE", "VOLUME", "CHIPS", "MARGIN",
    "SHORT_INTEREST", "REVENUE", "FUNDAMENTALS",
]

# Status display order
_STATUS_ORDER = [
    "FRESH", "ACCEPTABLE", "DELAYED", "STALE",
    "INTERRUPTED", "MISSING", "FUTURE_DATE", "DATE_REGRESSION",
]


class DataFreshnessReportBuilder:
    """
    Builds Markdown freshness reports for v1.1.3.

    [!] Report is read-only output. Does NOT modify data.
    [!] Does NOT download data, connect to brokers, or execute repairs.
    [!] Not Investment Advice.
    """

    def build(
        self,
        records: List[Any],
        alerts: List[Any],
        source_statuses: List[Any],
        summary: Optional[Any],
        output_dir: str = "reports",
        tier: Optional[str] = None,
        mode: str = "real",
    ) -> str:
        """
        Build and save a Markdown freshness report.

        Returns the path to the saved report file.
        [!] Does NOT auto-download or auto-repair data.
        """
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filename = f"data_freshness_report_{date_str}.md"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        text = self.build_text(
            records=records,
            alerts=alerts,
            source_statuses=source_statuses,
            summary=summary,
            tier=tier,
            mode=mode,
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)

        logger.info("DataFreshnessReportBuilder: saved report to %s", filepath)
        return filepath

    def build_text(
        self,
        records: List[Any],
        alerts: List[Any],
        source_statuses: List[Any],
        summary: Optional[Any],
        tier: Optional[str] = None,
        mode: str = "real",
    ) -> str:
        """
        Build and return the full Markdown report text.

        [!] Research Only. No Real Orders.
        """
        parts: List[str] = []

        parts.append(self._section_header())
        parts.append(self._section_overview(summary, tier, mode))
        parts.append(self._section_freshness_status(records, summary))
        parts.append(self._section_critical_alerts(alerts))
        parts.append(self._section_dataset_coverage(records))
        parts.append(self._section_source_health(source_statuses))
        parts.append(self._section_stale_symbols(records))
        parts.append(self._section_partial_updates(records, alerts))
        parts.append(self._section_repair_handoff(alerts))
        parts.append(self._section_limitations())
        parts.append(self._section_safety())

        return "\n\n".join(parts) + "\n"

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _section_header(self) -> str:
        lines = [
            "# Data Freshness Monitor Report v1.1.3",
            "",
            "> [!] Research Only. No Real Orders. Production Trading: BLOCKED.",
            "> [!] Auto External Refresh: DISABLED. Stale Auto Repair: DISABLED.",
            "> [!] Future Date does not count as Fresh.",
            "> [!] Not Investment Advice.",
        ]
        return "\n".join(lines)

    def _section_overview(
        self,
        summary: Optional[Any],
        tier: Optional[str],
        mode: str,
    ) -> str:
        from data_freshness.trading_calendar import TradingCalendar

        cal = TradingCalendar()
        # Determine expected latest trading date
        today = datetime.now(timezone.utc).date()
        expected_date = today
        while not cal.is_trading_day(expected_date):
            from datetime import timedelta, timezone
            expected_date = expected_date - timedelta(days=1)

        overall_status = "UNKNOWN"
        if summary is not None:
            overall_status = _safe_attr(summary, "overall_status", "UNKNOWN")

        tier_display = tier or (_safe_attr(summary, "tier", None) if summary else None) or "(all)"

        lines = [
            "## 一、總覽",
            "",
            f"- Version: {VERSION}",
            f"- Research Only: True",
            f"- No Real Orders: True",
            f"- Mode: {mode}",
            f"- Tier: {tier_display}",
            f"- Expected Latest Trading Date: {expected_date}",
            f"- Trading Calendar Source: {cal.calendar_source()}",
            f"- Calendar Approximate: {cal.is_approximate()}",
            f"- Overall Status: {overall_status}",
        ]
        if summary is not None:
            generated_at = _safe_attr(summary, "generated_at", "")
            confidence = _safe_attr(summary, "confidence", "")
            lines.append(f"- Generated At: {generated_at}")
            lines.append(f"- Confidence: {confidence}")
            symbols = _safe_attr(summary, "symbols", [])
            datasets = _safe_attr(summary, "datasets", [])
            lines.append(f"- Symbols Scanned: {len(symbols)}")
            lines.append(f"- Datasets Scanned: {', '.join(datasets) if datasets else '—'}")
        return "\n".join(lines)

    def _section_freshness_status(
        self,
        records: List[Any],
        summary: Optional[Any],
    ) -> str:
        counts: Dict[str, int] = {s: 0 for s in _STATUS_ORDER}

        if summary is not None:
            counts["FRESH"]          = _safe_attr(summary, "fresh_count", 0)
            counts["ACCEPTABLE"]     = _safe_attr(summary, "acceptable_count", 0)
            counts["DELAYED"]        = _safe_attr(summary, "delayed_count", 0)
            counts["STALE"]          = _safe_attr(summary, "stale_count", 0)
            counts["INTERRUPTED"]    = _safe_attr(summary, "interrupted_count", 0)
            counts["MISSING"]        = _safe_attr(summary, "missing_count", 0)
        # Always count FUTURE_DATE and DATE_REGRESSION directly from records
        counts["FUTURE_DATE"]      = sum(
            1 for r in records if _safe_attr(r, "status", "") == "FUTURE_DATE"
        )
        counts["DATE_REGRESSION"]  = sum(
            1 for r in records if _safe_attr(r, "status", "") == "DATE_REGRESSION"
        )

        # If no summary, count everything from records
        if summary is None:
            for status in _STATUS_ORDER:
                counts[status] = sum(
                    1 for r in records if _safe_attr(r, "status", "") == status
                )

        lines = [
            "## 二、Freshness Status",
            "",
            "| Status | Count |",
            "|--------|-------|",
        ]
        for status in _STATUS_ORDER:
            lines.append(f"| {status} | {counts[status]} |")

        total = sum(counts.values())
        lines.append(f"| **Total** | **{total}** |")
        return "\n".join(lines)

    def _section_critical_alerts(self, alerts: List[Any]) -> str:
        lines = ["## 三、Critical Alerts"]
        lines.append("")
        lines.append("P0 / P1 alerts, future dates, date regressions, source interruptions.")
        lines.append("")

        if not alerts:
            lines.append("_No alerts._")
            return "\n".join(lines)

        critical_types = {
            "FUTURE_DATE", "DATE_REGRESSION", "SOURCE_INTERRUPTION",
            "DATA_MISSING", "DATA_STALE",
        }
        critical_severities = {"CRITICAL", "HIGH"}

        critical = [
            a for a in alerts
            if _safe_attr(a, "severity", "") in critical_severities
            or _safe_attr(a, "alert_type", "") in critical_types
        ]

        if not critical:
            lines.append("_No critical alerts._")
            return "\n".join(lines)

        lines.append(
            "| Severity | Alert Type | Symbol | Dataset | Source | "
            "First Detected | Occurrences | Repair Issue |"
        )
        lines.append(
            "|----------|-----------|--------|---------|--------|"
            "----------------|-------------|--------------|"
        )
        for a in critical:
            severity     = _safe_attr(a, "severity", "")
            alert_type   = _safe_attr(a, "alert_type", "")
            symbol       = _safe_attr(a, "symbol", "")
            dataset      = _safe_attr(a, "dataset", "")
            source       = _safe_attr(a, "source", "")
            first_det    = _safe_attr(a, "first_detected_at", "")
            occ          = _safe_attr(a, "occurrence_count", 1)
            repair_id    = _safe_attr(a, "repair_issue_id", "") or "—"
            lines.append(
                f"| {severity} | {alert_type} | {symbol} | {dataset} | "
                f"{source} | {first_det} | {occ} | {repair_id} |"
            )
        return "\n".join(lines)

    def _section_dataset_coverage(self, records: List[Any]) -> str:
        lines = ["## 四、Dataset Coverage"]
        lines.append("")

        if not records:
            lines.append("_No records._")
            return "\n".join(lines)

        # Gather datasets
        datasets_seen = sorted({_safe_attr(r, "dataset", "UNKNOWN") for r in records})
        display_order = [d for d in _DATASET_ORDER if d in datasets_seen]
        other = [d for d in datasets_seen if d not in display_order]
        display_order.extend(other)

        lines.append(
            "| Dataset | Total | FRESH | ACCEPTABLE | DELAYED | STALE | "
            "INTERRUPTED | MISSING | FUTURE_DATE | DATE_REGRESSION |"
        )
        lines.append(
            "|---------|-------|-------|------------|---------|-------|"
            "-------------|---------|-------------|-----------------|"
        )

        for ds in display_order:
            ds_records = [r for r in records if _safe_attr(r, "dataset", "") == ds]
            total  = len(ds_records)
            fresh  = sum(1 for r in ds_records if _safe_attr(r, "status", "") == "FRESH")
            acc    = sum(1 for r in ds_records if _safe_attr(r, "status", "") == "ACCEPTABLE")
            delay  = sum(1 for r in ds_records if _safe_attr(r, "status", "") == "DELAYED")
            stale  = sum(1 for r in ds_records if _safe_attr(r, "status", "") == "STALE")
            inter  = sum(1 for r in ds_records if _safe_attr(r, "status", "") == "INTERRUPTED")
            miss   = sum(1 for r in ds_records if _safe_attr(r, "status", "") == "MISSING")
            fut    = sum(1 for r in ds_records if _safe_attr(r, "status", "") == "FUTURE_DATE")
            reg    = sum(1 for r in ds_records if _safe_attr(r, "status", "") == "DATE_REGRESSION")
            lines.append(
                f"| {ds} | {total} | {fresh} | {acc} | {delay} | {stale} | "
                f"{inter} | {miss} | {fut} | {reg} |"
            )

        return "\n".join(lines)

    def _section_source_health(self, source_statuses: List[Any]) -> str:
        lines = ["## 五、Source Health"]
        lines.append("")

        if not source_statuses:
            lines.append("_No source data._")
            return "\n".join(lines)

        from data_freshness.freshness_schema import (
            SOURCE_STATUS_HEALTHY, SOURCE_STATUS_DEGRADED,
            SOURCE_STATUS_INTERRUPTED, SOURCE_STATUS_UNKNOWN,
        )
        status_counts = {
            SOURCE_STATUS_HEALTHY:     0,
            SOURCE_STATUS_DEGRADED:    0,
            SOURCE_STATUS_INTERRUPTED: 0,
            SOURCE_STATUS_UNKNOWN:     0,
        }
        for s in source_statuses:
            st = _safe_attr(s, "status", SOURCE_STATUS_UNKNOWN)
            if st in status_counts:
                status_counts[st] += 1
            else:
                status_counts[SOURCE_STATUS_UNKNOWN] += 1

        lines.append("**Summary:**")
        lines.append("")
        for status, count in status_counts.items():
            lines.append(f"- {status}: {count}")
        lines.append("")

        lines.append(
            "| Source | Dataset | Expected | Fresh | Delayed | Stale | "
            "Missing | Status | Interruption | Reason |"
        )
        lines.append(
            "|--------|---------|----------|-------|---------|-------|"
            "---------|--------|--------------|--------|"
        )
        for s in source_statuses:
            src_name    = _safe_attr(s, "source_name", "")
            dataset     = _safe_attr(s, "dataset", "")
            expected    = _safe_attr(s, "symbols_expected", 0)
            fresh       = _safe_attr(s, "symbols_fresh", 0)
            delayed     = _safe_attr(s, "symbols_delayed", 0)
            stale       = _safe_attr(s, "symbols_stale", 0)
            missing     = _safe_attr(s, "symbols_missing", 0)
            status      = _safe_attr(s, "status", "")
            interrupted = _safe_attr(s, "interruption_suspected", False)
            reason      = _safe_attr(s, "reason", "")
            lines.append(
                f"| {src_name} | {dataset} | {expected} | {fresh} | {delayed} | "
                f"{stale} | {missing} | {status} | {interrupted} | {reason} |"
            )

        return "\n".join(lines)

    def _section_stale_symbols(self, records: List[Any]) -> str:
        lines = ["## 六、Stale Symbols"]
        lines.append("")

        stale_statuses = {"STALE", "INTERRUPTED", "MISSING", "DATE_REGRESSION", "FUTURE_DATE"}
        stale_records = [
            r for r in records
            if _safe_attr(r, "status", "") in stale_statuses
        ]

        if not stale_records:
            lines.append("_No stale or problematic symbols._")
            return "\n".join(lines)

        lines.append(
            "| Symbol | Tier | Dataset | Source | Last Date | "
            "Lag (days) | SLA | Status | Severity | Reason |"
        )
        lines.append(
            "|--------|------|---------|--------|-----------|"
            "------------|-----|--------|----------|--------|"
        )
        for r in stale_records:
            symbol      = _safe_attr(r, "symbol", "")
            tier        = _safe_attr(r, "tier", "")
            dataset     = _safe_attr(r, "dataset", "")
            source      = _safe_attr(r, "source", "")
            last_date   = _safe_attr(r, "actual_latest_date", "") or "—"
            lag         = _safe_attr(r, "trading_day_lag", "") or "—"
            sla         = _safe_attr(r, "sla_name", "") or "—"
            status      = _safe_attr(r, "status", "")
            severity    = _safe_attr(r, "severity", "")
            reason      = _safe_attr(r, "reason", "")
            lines.append(
                f"| {symbol} | {tier} | {dataset} | {source} | {last_date} | "
                f"{lag} | {sla} | {status} | {severity} | {reason} |"
            )

        return "\n".join(lines)

    def _section_partial_updates(
        self, records: List[Any], alerts: List[Any]
    ) -> str:
        lines = ["## 七、Partial Updates"]
        lines.append("")
        lines.append(
            "Partial update = DAILY_PRICE updated but VOLUME missing, "
            "partial source failure, or coverage not refreshed."
        )
        lines.append("")

        partial_alerts = [
            a for a in alerts
            if _safe_attr(a, "alert_type", "") in {"PARTIAL_UPDATE", "COVERAGE_NOT_REFRESHED"}
        ]

        # Detect partial updates from records: DAILY_PRICE present, VOLUME missing/stale
        symbols_daily: Dict[str, Any] = {}
        symbols_volume: Dict[str, Any] = {}
        for r in records:
            ds = _safe_attr(r, "dataset", "")
            sym = _safe_attr(r, "symbol", "")
            if ds == "DAILY_PRICE":
                symbols_daily[sym] = r
            elif ds == "VOLUME":
                symbols_volume[sym] = r

        partial_rows = []
        for sym, daily_rec in symbols_daily.items():
            daily_status = _safe_attr(daily_rec, "status", "")
            if daily_status in {"FRESH", "ACCEPTABLE"}:
                vol_rec = symbols_volume.get(sym)
                if vol_rec is None:
                    partial_rows.append((sym, "VOLUME_MISSING", "DAILY_PRICE fresh, VOLUME not found"))
                else:
                    vol_status = _safe_attr(vol_rec, "status", "")
                    if vol_status in {"STALE", "MISSING", "INTERRUPTED", "DELAYED"}:
                        partial_rows.append((
                            sym,
                            f"VOLUME_{vol_status}",
                            f"DAILY_PRICE {daily_status}, VOLUME {vol_status}",
                        ))

        if not partial_rows and not partial_alerts:
            lines.append("_No partial update issues detected._")
            return "\n".join(lines)

        if partial_rows:
            lines.append("**Price/Volume Mismatch:**")
            lines.append("")
            lines.append("| Symbol | Issue | Detail |")
            lines.append("|--------|-------|--------|")
            for sym, issue, detail in partial_rows:
                lines.append(f"| {sym} | {issue} | {detail} |")
            lines.append("")

        if partial_alerts:
            lines.append("**Coverage / Partial Alerts:**")
            lines.append("")
            lines.append("| Alert Type | Symbol | Dataset | Source | Message |")
            lines.append("|-----------|--------|---------|--------|---------|")
            for a in partial_alerts:
                alert_type = _safe_attr(a, "alert_type", "")
                symbol     = _safe_attr(a, "symbol", "")
                dataset    = _safe_attr(a, "dataset", "")
                source     = _safe_attr(a, "source", "")
                message    = _safe_attr(a, "message", "")
                lines.append(f"| {alert_type} | {symbol} | {dataset} | {source} | {message} |")

        return "\n".join(lines)

    def _section_repair_handoff(self, alerts: List[Any]) -> str:
        lines = ["## 八、Repair Handoff"]
        lines.append("")

        repair_alert_types = {
            "DATA_STALE", "DATA_MISSING", "SOURCE_INTERRUPTION",
            "FUTURE_DATE", "DATE_REGRESSION", "COVERAGE_NOT_REFRESHED",
        }
        repair_alerts = [
            a for a in alerts
            if _safe_attr(a, "alert_type", "") in repair_alert_types
        ]

        if not repair_alerts:
            lines.append("_No repair handoff items._")
            return "\n".join(lines)

        # Mapping table
        lines.append("**Alert → Repair Mapping:**")
        lines.append("")
        lines.append(
            "| Alert Type | Issue Type | Action | Auto-Safe | Priority |"
        )
        lines.append(
            "|-----------|-----------|--------|-----------|----------|"
        )
        _mapping = {
            "DATA_STALE":            ("STALE_DATA",           "REVIEW",             False, "P1"),
            "DATA_MISSING":          ("MISSING_SYMBOL_DATA",  "INVESTIGATE",        False, "P1"),
            "SOURCE_INTERRUPTION":   ("SOURCE_INTERRUPTION",  "SOURCE_REQUIRED",    False, "P0"),
            "FUTURE_DATE":           ("FUTURE_DATE_ANOMALY",  "REVIEW",             False, "P0"),
            "DATE_REGRESSION":       ("DATE_REGRESSION_ANOMALY", "REVIEW",          False, "P0"),
            "COVERAGE_NOT_REFRESHED": ("COVERAGE_STALE",     "REFRESH_COVERAGE",   True,  "P2"),
        }
        for alert_type, (issue_type, action, auto_safe, priority) in _mapping.items():
            auto_safe_str = "Yes (metadata only)" if auto_safe else "No — manual required"
            lines.append(
                f"| {alert_type} | {issue_type} | {action} | {auto_safe_str} | {priority} |"
            )
        lines.append("")

        # Detailed list
        lines.append("**Handoff Items:**")
        lines.append("")
        lines.append(
            "| # | Alert Type | Symbol | Dataset | Source | Priority | Blocked | Source Required |"
        )
        lines.append(
            "|---|-----------|--------|---------|--------|----------|---------|-----------------|"
        )
        for i, a in enumerate(repair_alerts, start=1):
            alert_type   = _safe_attr(a, "alert_type", "")
            symbol       = _safe_attr(a, "symbol", "")
            dataset      = _safe_attr(a, "dataset", "")
            source       = _safe_attr(a, "source", "")
            _, _, auto_safe, priority = _mapping.get(
                alert_type, ("", "REVIEW", False, "P2")
            )
            blocked          = "No"
            source_required  = "Yes" if alert_type in {
                "DATA_STALE", "DATA_MISSING", "SOURCE_INTERRUPTION"
            } else "No"
            lines.append(
                f"| {i} | {alert_type} | {symbol} | {dataset} | "
                f"{source} | {priority} | {blocked} | {source_required} |"
            )

        lines.append("")
        lines.append(
            "> [!] Repair Handoff creates task list ONLY. "
            "Does NOT execute repair. Does NOT download data. Research Only."
        )
        return "\n".join(lines)

    def _section_limitations(self) -> str:
        lines = [
            "## 九、Limitations",
            "",
            "- **Approximate holiday calendar**: No official TWSE holiday list loaded. "
            "Uses Mon-Fri weekday heuristic. Taiwan national holidays are NOT accounted for. "
            "Trading-day lag may be understated on holiday weeks.",
            "- **Suspension metadata unavailable**: If a symbol is suspended/halted, "
            "stale data may be falsely flagged; suspension status is not available.",
            "- **Announcement date uncertainty**: Revenue and earnings release dates "
            "vary by company; SLA is approximate.",
            "- **No external automatic refresh**: External data sources are NOT "
            "automatically fetched. Data must be manually imported.",
            "- **Mock data excluded**: mock mode data is labelled DEMO_ONLY and is "
            "NOT used for formal freshness conclusions or confidence scoring.",
            "- **Intraday not covered**: Only end-of-day data freshness is monitored.",
        ]
        return "\n".join(lines)

    def _section_safety(self) -> str:
        lines = [
            "## 十、安全聲明",
            "",
            "> [!] Research Only. No Real Orders. Production Trading: BLOCKED.",
            "",
            "- **No Real Orders**: This system does NOT place, submit, or route "
            "any buy or sell orders.",
            "- **No broker execution**: No broker API connection. No live trading.",
            "- **No automatic data download**: External data sources are NOT "
            "automatically fetched or refreshed.",
            "- **No automatic repair**: Stale data is NOT automatically overwritten "
            "or repaired. Repair Handoff creates task lists only.",
            "- **Mock data not used for formal freshness**: mock mode outputs are "
            "labelled DEMO_ONLY and excluded from all formal freshness conclusions.",
            "- **Not Investment Advice**: All outputs are for research purposes only. "
            "Nothing in this report constitutes financial or investment advice.",
            "- research_only = True",
            "- no_real_orders = True",
            "- auto_download_disabled = True",
            "- auto_repair_disabled = True",
            "",
            f"_Report generated: {datetime.now(timezone.utc).isoformat()} UTC_",
        ]
        return "\n".join(lines)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _safe_attr(obj: Any, attr: str, default: Any = None) -> Any:
    """Safely get attribute from dataclass or dict-like object."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)
