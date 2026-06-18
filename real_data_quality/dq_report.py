"""
real_data_quality/dq_report.py — Report/CLI output formatter v1.3.0
Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] MOCK mode always labeled DEMO_ONLY. REAL mode labeled REAL_DATA.
"""
from __future__ import annotations

import logging

from real_data_quality.dq_schema import DataMode, DataQualityStatus, DataQualityReport

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
MOCK_FALLBACK_ENABLED = False


def _mode_label(data_mode: str) -> str:
    """Return display label for data mode. MOCK always shows DEMO_ONLY."""
    if data_mode == DataMode.REAL:
        return "REAL_DATA"
    if data_mode == DataMode.MOCK:
        return "DEMO_ONLY"
    return "UNAVAILABLE"


def format_quality_report_text(report: DataQualityReport) -> str:
    """
    Human-readable text for CLI output.
    Shows: symbol, mode (REAL_DATA or DEMO_ONLY), source, status, score,
    latest timestamp, missing fields, stale fields, blocking reasons,
    precise prices allowed, backtest allowed.
    """
    mode_label = _mode_label(report.data_mode)
    lines = [
        "=" * 60,
        "  TW Quant Cockpit — Data Quality Report",
        f"  [!] Research Only. No Real Orders. Not Investment Advice.",
        "=" * 60,
        f"  Symbol              : {report.symbol}",
        f"  Market              : {report.market}",
        f"  Data Mode           : {mode_label}",
        f"  Source(s)           : {', '.join(report.source_names) if report.source_names else 'None'}",
        f"  Quality Status      : {report.status}",
        f"  Quality Score       : {report.score}/100",
        f"  Latest Market Time  : {report.latest_market_timestamp or 'N/A'}",
        f"  Checked At          : {report.checked_at}",
        "-" * 60,
    ]

    if report.missing_fields:
        lines.append(f"  Missing Fields      : {', '.join(report.missing_fields)}")
    if report.stale_fields:
        lines.append(f"  Stale Fields        : {', '.join(report.stale_fields)}")
    if report.invalid_fields:
        lines.append(f"  Invalid Fields      : {', '.join(report.invalid_fields)}")
    if report.inconsistent_fields:
        lines.append(f"  Inconsistent Fields : {', '.join(report.inconsistent_fields)}")

    lines.append("-" * 60)
    lines.append(f"  Precise Prices OK   : {'YES' if report.can_generate_precise_prices else 'NO'}")
    lines.append(f"  Backtest OK         : {'YES' if report.can_run_backtest else 'NO'}")
    lines.append(f"  Analysis OK         : {'YES' if report.can_generate_analysis else 'NO'}")

    if report.blocking_reasons:
        lines.append("-" * 60)
        lines.append("  BLOCKING REASONS:")
        for reason in report.blocking_reasons:
            lines.append(f"    [!] {reason}")

    if report.warnings:
        lines.append("-" * 60)
        lines.append("  WARNINGS:")
        for warn in report.warnings:
            lines.append(f"    [~] {warn}")

    if report.issues:
        critical_issues = [i for i in report.issues if i.severity == "CRITICAL"]
        if critical_issues:
            lines.append("-" * 60)
            lines.append("  CRITICAL ISSUES:")
            for iss in critical_issues:
                lines.append(f"    [{iss.severity}] {iss.field}: {iss.message}")

    lines.append("=" * 60)
    return "\n".join(lines)


def format_quality_summary_for_stock_report(report: DataQualityReport) -> str:
    """
    Markdown section to prepend to stock analysis reports.
    Includes: mode, source, quality status, quality score, market timestamp,
    analysis limitations, blocked sections.
    """
    mode_label = _mode_label(report.data_mode)
    lines = [
        "## Data Quality Summary",
        "",
        f"> **Research Only. No Real Orders. Not Investment Advice.**",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Data Mode | `{mode_label}` |",
        f"| Source(s) | {', '.join(report.source_names) if report.source_names else 'None'} |",
        f"| Quality Status | **{report.status}** |",
        f"| Quality Score | {report.score}/100 |",
        f"| Market Timestamp | {report.latest_market_timestamp or 'N/A'} |",
        f"| Checked At | {report.checked_at} |",
        "",
    ]

    if report.status == DataQualityStatus.BLOCKED:
        lines.append("### BLOCKED — Sections Unavailable")
        lines.append("")
        lines.append("The following are **BLOCKED** due to data quality:")
        lines.append("- Precise price analysis")
        lines.append("- Formal buy/sell recommendations")
        if report.blocking_reasons:
            lines.append("")
            lines.append("**Blocking Reasons:**")
            for r in report.blocking_reasons:
                lines.append(f"- {r}")
        lines.append("")

    elif report.status == DataQualityStatus.UNAVAILABLE:
        lines.append("### REAL DATA UNAVAILABLE")
        lines.append("")
        lines.append("Real data is not available. No mock fallback. Not Investment Advice.")
        lines.append("")

    if report.warnings:
        lines.append("### Warnings")
        for w in report.warnings:
            lines.append(f"- {w}")
        lines.append("")

    if mode_label == "DEMO_ONLY":
        lines.append("> **DEMO_ONLY**: This data is mock/demo. "
                     "Do not use for real trading decisions. Not Investment Advice.")
        lines.append("")

    return "\n".join(lines)


def make_blocked_output(report: DataQualityReport) -> str:
    """
    Output for BLOCKED status.
    Shows DATA QUALITY BLOCKED + reasons.
    """
    lines = [
        "=" * 60,
        "  [!] DATA QUALITY BLOCKED",
        "  [!] Research Only. No Real Orders. Not Investment Advice.",
        "=" * 60,
        f"  Symbol : {report.symbol}",
        f"  Market : {report.market}",
        f"  Score  : {report.score}/100",
        "",
        "  BLOCKING REASONS:",
    ]
    if report.blocking_reasons:
        for reason in report.blocking_reasons:
            lines.append(f"    [!] {reason}")
    else:
        lines.append("    [!] Data quality score below threshold or critical issue detected")

    lines += [
        "",
        "  Precise prices: BLOCKED",
        "  Formal recommendations: BLOCKED",
        "  Backtest: BLOCKED",
        "=" * 60,
    ]
    return "\n".join(lines)


def make_unavailable_output(symbol: str) -> str:
    """
    Output for UNAVAILABLE status.
    Shows REAL DATA UNAVAILABLE. No mock fallback. Not Investment Advice.
    """
    lines = [
        "=" * 60,
        "  REAL DATA UNAVAILABLE",
        "  [!] Research Only. No Real Orders. Not Investment Advice.",
        "=" * 60,
        f"  Symbol         : {symbol}",
        "  Data Mode      : UNAVAILABLE",
        "  Mock Fallback  : DISABLED",
        "",
        "  No real data source is connected or available.",
        "  No mock data will be substituted.",
        "  Please provide a real data source to proceed.",
        "=" * 60,
    ]
    return "\n".join(lines)
