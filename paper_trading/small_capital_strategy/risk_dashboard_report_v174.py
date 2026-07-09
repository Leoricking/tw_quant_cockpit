"""
paper_trading/small_capital_strategy/risk_dashboard_report_v174.py
Report generator for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import csv
import io
import json
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import (
    SmallAccountRiskDashboard, RiskDashboardScorecard, RiskDashboardReport,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"

REPORT_SECTION_NAMES: List[str] = [
    "small_account_risk_summary",
    "capital_profile",
    "single_trade_risk",
    "portfolio_exposure",
    "cash_ratio",
    "position_count",
    "drawdown",
    "losing_streak",
    "concentration_risk",
    "theme_exposure",
    "stop_loss_coverage",
    "abc_execution_risk",
    "watchlist_risk",
    "market_regime_risk",
    "scorecard",
    "safety",
    "not_investment_advice",
]


def get_section_names() -> List[str]:
    """Return list of report section names."""
    return list(REPORT_SECTION_NAMES)


def build_report(
    dashboard: SmallAccountRiskDashboard,
    scorecard: RiskDashboardScorecard,
    fmt: str = "JSON",
) -> RiskDashboardReport:
    """Build RiskDashboardReport from dashboard + scorecard."""
    sections = {
        "small_account_risk_summary": {
            "overall_status": dashboard.overall_status.value,
            "block_count": len(dashboard.all_block_reasons),
            "block_reasons": [r.value for r in dashboard.all_block_reasons],
            "summary": dashboard.summary,
        },
        "capital_profile": {
            "capital_twd": dashboard.single_trade.source_lineage and 300_000,
            "paper_only": True,
        },
        "single_trade_risk": {
            "status": dashboard.single_trade.status.value,
            "loss_amount": dashboard.single_trade.single_trade_loss_amount,
            "risk_pct": dashboard.single_trade.risk_pct,
            "has_stop_loss": dashboard.single_trade.has_stop_loss,
        },
        "portfolio_exposure": {
            "status": dashboard.exposure.status.value,
            "invested_pct": dashboard.exposure.invested_pct,
            "cash_pct": dashboard.exposure.cash_pct,
            "regime": dashboard.exposure.market_regime,
        },
        "cash_ratio": {
            "status": dashboard.cash_ratio.status.value,
            "cash_pct": dashboard.cash_ratio.cash_pct,
            "min_cash_pct": dashboard.cash_ratio.min_cash_pct,
        },
        "position_count": {
            "status": dashboard.position_count.status.value,
            "holdings_count": dashboard.position_count.holdings_count,
            "max_holdings": dashboard.position_count.max_holdings,
        },
        "drawdown": {
            "status": dashboard.drawdown.status.value,
            "drawdown_pct": dashboard.drawdown.drawdown_pct,
            "level": dashboard.drawdown.level.value,
        },
        "losing_streak": {
            "status": dashboard.losing_streak.status.value,
            "losing_streak_count": dashboard.losing_streak.losing_streak_count,
            "level": dashboard.losing_streak.level.value,
        },
        "concentration_risk": {
            "status": dashboard.concentration.status.value,
            "max_single_position_pct": dashboard.concentration.max_single_position_pct,
            "sector_exposure_pct": dashboard.concentration.sector_exposure_pct,
        },
        "theme_exposure": {
            "status": dashboard.theme_exposure.status.value,
            "theme_pct": dashboard.theme_exposure.theme_exposure_pct,
            "training_amount": dashboard.theme_exposure.training_amount,
        },
        "stop_loss_coverage": {
            "status": dashboard.stop_loss_coverage.status.value,
            "all_covered": dashboard.stop_loss_coverage.all_positions_covered,
            "missing_count": dashboard.stop_loss_coverage.missing_stop_loss_count,
        },
        "abc_execution_risk": {
            "abc_plan_blocked": len([r for r in dashboard.stop_loss_coverage.block_reasons]) > 0,
        },
        "watchlist_risk": {
            "candidate_excluded": False,
        },
        "market_regime_risk": {
            "regime": dashboard.exposure.market_regime,
            "exposure_status": dashboard.exposure.status.value,
        },
        "scorecard": {
            "total_score": scorecard.total_score,
            "grade": scorecard.grade.value,
            "weights_sum": scorecard.weights_sum,
        },
        "safety": {
            "no_real_orders": True,
            "paper_only": True,
            "research_only": True,
        },
        "not_investment_advice": {
            "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
            "not_investment_advice": True,
        },
    }

    return RiskDashboardReport(
        sections=sections,
        report_format=fmt,
    )


def render_markdown(report: RiskDashboardReport) -> str:
    """Render report as Markdown string."""
    lines = [
        "# Small Account Risk Dashboard Report",
        "",
        "> Research Only | Paper Only | No Real Orders | Not Investment Advice",
        "",
    ]
    for section, data in report.sections.items():
        lines.append(f"## {section.replace('_', ' ').title()}")
        lines.append("")
        for k, v in data.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
    return "\n".join(lines)


def render_json(report: RiskDashboardReport) -> str:
    """Render report as JSON string."""
    payload = {
        "sections": report.sections,
        "report_format": report.report_format,
        "schema_version": report.schema_version,
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }
    return json.dumps(payload, indent=2, default=str)


def render_csv(report: RiskDashboardReport) -> str:
    """Render report as CSV string."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["section", "key", "value"])
    for section, data in report.sections.items():
        for k, v in data.items():
            writer.writerow([section, k, str(v)])
    return buf.getvalue()


def render_console_summary(report: RiskDashboardReport) -> str:
    """Render a brief console summary."""
    summary_data = report.sections.get("small_account_risk_summary", {})
    scorecard_data = report.sections.get("scorecard", {})
    lines = [
        "=" * 60,
        "  Small Account Risk Dashboard v1.7.4",
        "=" * 60,
        f"  Status:  {summary_data.get('overall_status', 'N/A')}",
        f"  Score:   {scorecard_data.get('total_score', 0):.1f} / 100  (Grade: {scorecard_data.get('grade', 'N/A')})",
        f"  Blocks:  {summary_data.get('block_count', 0)}",
        "  [!] Research Only | Paper Only | No Real Orders | Not Investment Advice",
        "=" * 60,
    ]
    return "\n".join(lines)
