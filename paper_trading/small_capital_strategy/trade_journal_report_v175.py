"""
paper_trading/small_capital_strategy/trade_journal_report_v175.py
Report generator for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.trade_journal_models_v175 import (
    TradeJournalDashboard, TradeJournalReport,
)

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"

REPORT_SECTION_NAMES: List[str] = [
    "trade_journal_summary",
    "version_info",
    "safety_disclaimer",
    "entry_review_summary",
    "exit_review_summary",
    "abc_execution_summary",
    "watchlist_conversion_summary",
    "risk_violation_summary",
    "regime_outcome_summary",
    "mistake_taxonomy_summary",
    "scorecard_summary",
    "win_loss_analysis",
    "pnl_summary",
    "open_positions",
    "closed_positions",
    "improvement_recommendations",
    "not_investment_advice",
]


def get_report_sections() -> List[str]:
    """Return list of report section names. At least 13 sections."""
    return list(REPORT_SECTION_NAMES)


def build_report(dashboard: TradeJournalDashboard, fmt: str = "JSON") -> TradeJournalReport:
    """Build a TradeJournalReport from a dashboard."""
    sections: Dict[str, Any] = {
        "trade_journal_summary": {
            "entries_count":   dashboard.entries_count,
            "open_count":      dashboard.open_count,
            "closed_count":    dashboard.closed_count,
            "win_rate_pct":    dashboard.win_rate_pct,
            "total_pnl_twd":   dashboard.total_pnl_twd,
            "paper_only":      True,
        },
        "version_info": {
            "schema_version": _SCHEMA,
            "policy_version": _POLICY,
            "version":        "1.7.5",
            "release_name":   "Small Account Trade Journal",
        },
        "safety_disclaimer": {
            "paper_only":          True,
            "research_only":       True,
            "no_real_orders":      True,
            "no_broker":           True,
            "not_investment_advice": True,
        },
        "entry_review_summary": {
            "note": "Entry quality review based on trigger, regime, watchlist, and stop loss.",
        },
        "exit_review_summary": {
            "note": "Exit quality review based on target reached, stop triggered, and panic exit.",
        },
        "abc_execution_summary": {
            "note": "ABC buy-point execution quality: A-pullback, B-breakout, C-reclaim.",
        },
        "watchlist_conversion_summary": {
            "note": "Conversion rate from watchlist candidates to actual trades.",
        },
        "risk_violation_summary": {
            "violations_count": dashboard.violations_count,
            "note": "Risk violations: oversize, no stop loss, regime mismatch, ABC plan violated.",
        },
        "regime_outcome_summary": {
            "regime_reviews_count": len(dashboard.regime_reviews),
            "regimes": [r.regime for r in dashboard.regime_reviews],
        },
        "mistake_taxonomy_summary": {
            "note": "Common mistakes: FOMO, revenge, oversize, no stop loss, etc.",
        },
        "scorecard_summary": {
            "total_score": dashboard.scorecard.total_score,
            "grade":       dashboard.scorecard.grade,
            "win_rate":    dashboard.scorecard.win_rate_pct,
        },
        "win_loss_analysis": {
            "win_count":     dashboard.win_count,
            "loss_count":    dashboard.loss_count,
            "win_rate_pct":  dashboard.win_rate_pct,
            "avg_return_pct": dashboard.avg_return_pct,
        },
        "pnl_summary": {
            "total_pnl_twd":   dashboard.total_pnl_twd,
            "avg_return_pct":  dashboard.avg_return_pct,
        },
        "open_positions": {
            "open_count": dashboard.open_count,
        },
        "closed_positions": {
            "closed_count": dashboard.closed_count,
        },
        "improvement_recommendations": {
            "note": "Review entry quality, stop loss discipline, regime alignment, and ABC execution.",
        },
        "not_investment_advice": {
            "disclaimer":          "Research Only | Paper Only | No Real Orders | Not Investment Advice",
            "not_investment_advice": True,
        },
    }

    return TradeJournalReport(
        sections=sections,
        report_format=fmt,
    )


def render_json(report: TradeJournalReport) -> str:
    """Render report as JSON string."""
    payload = {
        "sections":       report.sections,
        "report_format":  report.report_format,
        "schema_version": report.schema_version,
        "paper_only":     True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }
    return json.dumps(payload, indent=2, default=str)


def render_markdown(report: TradeJournalReport) -> str:
    """Render report as Markdown string."""
    lines = [
        "# Small Account Trade Journal Report",
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
