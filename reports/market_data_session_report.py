"""
reports/market_data_session_report.py — Market Data Session Report v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Generates text reports for market data session activity and quality metrics.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
REPORT_VERSION: str = "1.6.1"

_DISCLAIMER = (
    "[!] MARKET DATA ONLY. NO REAL ORDERS. NO BROKER. "
    "RESEARCH ONLY. NOT INVESTMENT ADVICE."
)


class MarketDataSessionReport:
    """
    Generates formatted reports for market data session activity.
    Research only. No real orders.
    """

    def __init__(self) -> None:
        self._generated_at: str = datetime.now(timezone.utc).isoformat()

    def generate_session_report(
        self,
        session_info: Dict[str, Any],
        feed_health: Optional[Dict[str, Any]] = None,
        quality_summary: Optional[Dict[str, Any]] = None,
        lineage_summary: Optional[Dict[str, Any]] = None,
    ) -> str:
        lines = [
            "=" * 62,
            f"Market Data Session Report v{REPORT_VERSION}",
            f"Generated: {self._generated_at}",
            _DISCLAIMER,
            "=" * 62,
            "",
            "SESSION INFO",
            "-" * 40,
            f"  Session ID:   {session_info.get('session_id', 'N/A')}",
            f"  Status:       {session_info.get('status', 'N/A')}",
            f"  Adapter:      {session_info.get('adapter_id', 'N/A')}",
            f"  Source Class: {session_info.get('source_class', 'N/A')}",
            f"  Event Count:  {session_info.get('event_count', 0)}",
            f"  Started At:   {session_info.get('started_at', 'N/A')}",
            f"  Research Only: True",
            f"  No Real Orders: True",
            f"  Market Data Only: True",
            "",
        ]

        if feed_health:
            lines += [
                "FEED HEALTH",
                "-" * 40,
                f"  Alive:     {feed_health.get('is_alive', False)}",
                f"  Gaps:      {feed_health.get('gap_count', 0)}",
                f"  Failure:   {feed_health.get('failure_type', 'None')}",
                f"  Message:   {feed_health.get('message', 'N/A')}",
                "",
            ]

        if quality_summary:
            lines += [
                "DATA QUALITY SUMMARY",
                "-" * 40,
                f"  PASS:    {quality_summary.get('pass_count', 0)}",
                f"  WARN:    {quality_summary.get('warn_count', 0)}",
                f"  FAIL:    {quality_summary.get('fail_count', 0)}",
                f"  BLOCKED: {quality_summary.get('blocked_count', 0)}",
                "",
            ]

        if lineage_summary:
            lines += [
                "LINEAGE SUMMARY",
                "-" * 40,
                f"  Total Records: {lineage_summary.get('total_records', 0)}",
            ]
            for stage, count in lineage_summary.get("by_stage", {}).items():
                lines.append(f"    {stage}: {count}")
            lines.append("")

        lines += [
            "=" * 62,
            _DISCLAIMER,
        ]
        return "\n".join(lines)

    def generate_health_report(self, health_result: Dict[str, Any]) -> str:
        status = health_result.get("status", "?")
        passed = health_result.get("passed", 0)
        failed = health_result.get("failed", 0)
        lines = [
            "=" * 62,
            f"Market Data Session Health Report v{REPORT_VERSION}",
            _DISCLAIMER,
            "=" * 62,
            f"Overall Status: {status}",
            f"Passed: {passed}  Failed: {failed}",
            "",
        ]
        for k, v in health_result.get("results", {}).items():
            tag = "PASS" if v == "PASS" else "FAIL"
            lines.append(f"  [{tag}] {k}")
        lines += ["", _DISCLAIMER]
        return "\n".join(lines)
