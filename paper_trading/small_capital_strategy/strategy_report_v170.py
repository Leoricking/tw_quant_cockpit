"""
paper_trading/small_capital_strategy/strategy_report_v170.py
Strategy report for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
Outputs: Markdown, JSON, CSV, console summary.
"""
from __future__ import annotations
import json
from typing import Any, Dict, Optional

from paper_trading.small_capital_strategy.models_v170 import (
    SmallCapitalReport, SmallCapitalScorecard,
)
from paper_trading.small_capital_strategy.version_v170 import VERSION, RELEASE_NAME

_DISCLAIMER = (
    "\nResearch Only | Paper Only | No Real Orders | Not Investment Advice\n"
)

_SECTIONS = [
    "capital_profile",
    "risk_budget",
    "allocation_template",
    "market_regime",
    "watchlist_ranking",
    "abc_buy_point_signals",
    "position_sizing",
    "entry_plan",
    "exit_plan",
    "forbidden_trade_checks",
    "cash_control",
    "scorecard",
    "paper_simulation_notes",
    "safety",
    "not_investment_advice",
]


def build_report(
    template_id: str,
    scorecard: SmallCapitalScorecard,
    sections: Optional[Dict[str, Any]] = None,
) -> SmallCapitalReport:
    """Build a SmallCapitalReport for the given template and scorecard."""
    report_sections = {}
    for s in _SECTIONS:
        report_sections[s] = (sections or {}).get(s, {})
    # Always include disclaimer
    report_sections["not_investment_advice"] = {
        "disclaimer": "Research Only. Paper Only. No Real Orders. Not Investment Advice.",
        "paper_only": True,
        "no_real_orders": True,
    }
    return SmallCapitalReport(
        template_id=template_id,
        sections=report_sections,
        scorecard=scorecard,
    )


def to_markdown(report: SmallCapitalReport) -> str:
    """Render report as Markdown string."""
    lines = [
        f"# Small Capital Growth Strategy Report",
        f"",
        f"**Version:** {VERSION}  ",
        f"**Release:** {RELEASE_NAME}  ",
        f"**Template:** {report.template_id}  ",
        f"",
        _DISCLAIMER,
        f"",
        f"## Scorecard",
        f"- Score: {report.scorecard.score}/100",
        f"- Grade: {report.scorecard.grade.value}",
        f"- Safety Blocked: {report.scorecard.safety_blocked}",
        f"",
    ]
    for section_name in _SECTIONS:
        lines.append(f"## {section_name.replace('_', ' ').title()}")
        section_data = report.sections.get(section_name, {})
        if section_data:
            for k, v in section_data.items():
                lines.append(f"- **{k}**: {v}")
        else:
            lines.append("_(no data)_")
        lines.append("")

    lines.append(_DISCLAIMER)
    return "\n".join(lines)


def to_json(report: SmallCapitalReport) -> str:
    """Render report as JSON string."""
    return json.dumps(report.to_dict(), indent=2, default=str)


def to_csv(report: SmallCapitalReport) -> str:
    """Render scorecard as CSV string."""
    sc = report.scorecard
    rows = [
        "field,value",
        f"template_id,{report.template_id}",
        f"score,{sc.score}",
        f"grade,{sc.grade.value}",
        f"risk_budget_compliance,{sc.risk_budget_compliance}",
        f"position_sizing_correctness,{sc.position_sizing_correctness}",
        f"buy_point_quality,{sc.buy_point_quality}",
        f"market_regime_alignment,{sc.market_regime_alignment}",
        f"watchlist_quality,{sc.watchlist_quality}",
        f"exit_plan_completeness,{sc.exit_plan_completeness}",
        f"safety_compliance,{sc.safety_compliance}",
        f"safety_blocked,{sc.safety_blocked}",
        f"paper_only,{report.paper_only}",
        f"research_only,{report.research_only}",
        f"no_real_orders,{report.no_real_orders}",
        f"not_investment_advice,{report.not_investment_advice}",
    ]
    return "\n".join(rows)


def to_console_summary(report: SmallCapitalReport) -> str:
    """Render compact console summary."""
    sc = report.scorecard
    return (
        f"[Small Capital Strategy v{VERSION}] {report.template_id}\n"
        f"  Score: {sc.score}/100  Grade: {sc.grade.value}"
        f"  Safety Blocked: {sc.safety_blocked}\n"
        + _DISCLAIMER
    )


def get_section_names() -> list:
    """Return the list of standard report section names."""
    return list(_SECTIONS)
