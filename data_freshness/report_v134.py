"""data_freshness/report_v134.py — v1.3.4 Freshness Report Generator.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from data_freshness.models_v134 import (
    FreshnessRecord, ProviderSLARecord, FreshnessAlert,
    DailyFreshnessSummary, FreshnessSeverity, FreshnessStatus,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class DataFreshnessReport:
    """Generate freshness reports in dict, text, and markdown formats.

    [!] Research Only. Report does not trigger any action.
    """

    def generate(
        self,
        records: List[FreshnessRecord],
        sla_records: List[ProviderSLARecord],
        alerts: List[FreshnessAlert],
        summary: Optional[DailyFreshnessSummary],
    ) -> Dict[str, Any]:
        """Generate a structured report dict."""
        active_alerts = [a for a in alerts if not a.resolved]
        critical = [r for r in records if r.freshness_status == FreshnessStatus.CRITICALLY_STALE]
        stale = [r for r in records if r.freshness_status == FreshnessStatus.STALE]
        fresh = [r for r in records if r.freshness_status == FreshnessStatus.FRESH]
        near_stale = [r for r in records if r.freshness_status == FreshnessStatus.NEAR_STALE]
        never_received = [r for r in records if r.freshness_status == FreshnessStatus.NEVER_RECEIVED]
        blocked = [r for r in records if r.blocks_analysis]
        breached_sla = [s for s in sla_records if s.breached]

        return {
            "schema_version": "1.3.4",
            "safety": {
                "no_real_orders": True,
                "broker_execution_enabled": False,
                "production_trading_blocked": True,
                "auto_refresh_enabled": False,
                "auto_repair_enabled": False,
                "mock_fallback_enabled": False,
            },
            "summary": summary.to_dict() if summary else {},
            "totals": {
                "records": len(records),
                "fresh": len(fresh),
                "near_stale": len(near_stale),
                "stale": len(stale),
                "critically_stale": len(critical),
                "never_received": len(never_received),
                "blocked": len(blocked),
            },
            "sla": {
                "total": len(sla_records),
                "breached": len(breached_sla),
            },
            "alerts": {
                "total": len(alerts),
                "active": len(active_alerts),
                "critical": sum(1 for a in active_alerts if a.severity == FreshnessSeverity.CRITICAL),
            },
            "critical_records": [
                {"symbol": r.symbol, "dataset_type": r.dataset_type,
                 "status": r.freshness_status, "age_seconds": r.age_seconds}
                for r in critical[:20]
            ],
            "active_alerts": [
                {"alert_id": a.alert_id, "symbol": a.symbol,
                 "dataset_type": a.dataset_type, "severity": a.severity,
                 "title": a.title}
                for a in active_alerts[:20]
            ],
        }

    def format_text(self, report_dict: Dict[str, Any]) -> str:
        """Format report as plain text."""
        lines = [
            "=" * 60,
            "  Data Freshness Report — v1.3.4",
            "  [!] Research Only. No Real Orders. Production BLOCKED.",
            "=" * 60,
        ]
        totals = report_dict.get("totals", {})
        lines.append(f"  Records:          {totals.get('records', 0)}")
        lines.append(f"  Fresh:            {totals.get('fresh', 0)}")
        lines.append(f"  Near-Stale:       {totals.get('near_stale', 0)}")
        lines.append(f"  Stale:            {totals.get('stale', 0)}")
        lines.append(f"  Critically Stale: {totals.get('critically_stale', 0)}")
        lines.append(f"  Never Received:   {totals.get('never_received', 0)}")
        lines.append(f"  Blocked:          {totals.get('blocked', 0)}")

        sla = report_dict.get("sla", {})
        lines.append(f"  SLA Records:      {sla.get('total', 0)}")
        lines.append(f"  SLA Breached:     {sla.get('breached', 0)}")

        alerts = report_dict.get("alerts", {})
        lines.append(f"  Active Alerts:    {alerts.get('active', 0)}")
        lines.append(f"  Critical Alerts:  {alerts.get('critical', 0)}")

        lines.append("-" * 60)
        critical_recs = report_dict.get("critical_records", [])
        if critical_recs:
            lines.append("  CRITICALLY STALE:")
            for rec in critical_recs[:5]:
                lines.append(f"    {rec['symbol']}/{rec['dataset_type']} age={rec.get('age_seconds', '?')}s")

        lines.append("=" * 60)
        return "\n".join(lines)

    def format_markdown(self, report_dict: Dict[str, Any]) -> str:
        """Format report as Markdown."""
        totals = report_dict.get("totals", {})
        sla = report_dict.get("sla", {})
        alerts_info = report_dict.get("alerts", {})

        lines = [
            "# Data Freshness Report — v1.3.4",
            "",
            "> [!] Research Only. No Real Orders. Production Trading: BLOCKED.",
            "> Auto Refresh DISABLED. Auto Repair DISABLED. Mock Fallback DISABLED.",
            "",
            "## Summary",
            "",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Records | {totals.get('records', 0)} |",
            f"| Fresh | {totals.get('fresh', 0)} |",
            f"| Near-Stale | {totals.get('near_stale', 0)} |",
            f"| Stale | {totals.get('stale', 0)} |",
            f"| Critically Stale | {totals.get('critically_stale', 0)} |",
            f"| Never Received | {totals.get('never_received', 0)} |",
            f"| Blocked | {totals.get('blocked', 0)} |",
            f"| SLA Breached | {sla.get('breached', 0)} |",
            f"| Active Alerts | {alerts_info.get('active', 0)} |",
            "",
            "## Safety",
            "",
            "- No Real Orders: True",
            "- Broker Execution Enabled: False",
            "- Production Trading Blocked: True",
            "- Auto Refresh Enabled: False",
            "- Auto Repair Enabled: False",
            "- Mock Fallback Enabled: False",
            "",
            "_Not Investment Advice._",
        ]
        return "\n".join(lines)
