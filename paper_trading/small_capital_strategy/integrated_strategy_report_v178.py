"""
paper_trading/small_capital_strategy/integrated_strategy_report_v178.py
Report generation for Small Capital Strategy Integration v1.7.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
    IntegratedStrategyDecision,
    IntegratedScorecard,
    IntegratedDashboard,
    IntegratedStrategyReport,
)
from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedDecisionAction,
)

_SCHEMA  = "178"
_POLICY  = "1.7.8-small-capital-strategy-integration"
_LINEAGE = "paper_trading.small_capital_strategy.integrated_strategy_report_v178"

_REPORT_SECTIONS = [
    "executive_summary",
    "scorecard_detail",
    "subsystem_status",
    "no_trade_reasons",
    "paper_plan_summary",
    "safety_disclaimer",
]


def get_report_sections() -> List[str]:
    """Return list of report section names."""
    return list(_REPORT_SECTIONS)


def build_report(dashboard: IntegratedDashboard) -> IntegratedStrategyReport:
    """Build integrated strategy report from dashboard."""
    decision = dashboard.decision
    scorecard = dashboard.scorecard

    if decision is None:
        action = IntegratedDecisionAction.OBSERVE
        final_score = 0.0
        grade_value = "BLOCKED"
        summary = "No decision available."
    else:
        action = decision.action
        final_score = decision.final_score
        grade_value = decision.grade.value
        summary = decision.summary

    scorecard_scores = {}
    if scorecard is not None:
        scorecard_scores = {
            "theme": scorecard.theme_score,
            "watchlist": scorecard.watchlist_score,
            "abc": scorecard.abc_score,
            "regime": scorecard.regime_score,
            "risk": scorecard.risk_score,
            "behavior": scorecard.behavior_score,
            "journal": scorecard.journal_quality_score,
            "final": scorecard.final_score,
        }

    sections: List[Dict[str, Any]] = [
        {
            "name": "executive_summary",
            "action": action.value,
            "final_score": final_score,
            "grade": grade_value,
            "summary": summary,
            "paper_only": True,
            "research_only": True,
            "not_investment_advice": True,
        },
        {
            "name": "scorecard_detail",
            "scores": scorecard_scores,
            "paper_only": True,
        },
        {
            "name": "subsystem_status",
            "watchlist": (dashboard.watchlist_decision.status.value
                          if dashboard.watchlist_decision else "UNKNOWN"),
            "theme": (dashboard.theme_decision.theme_status.value
                      if dashboard.theme_decision else "UNKNOWN"),
            "abc": (dashboard.abc_decision.abc_status.value
                    if dashboard.abc_decision else "NOT_READY"),
            "risk": (dashboard.risk_decision.risk_level.value
                     if dashboard.risk_decision else "SAFE"),
            "behavior": (dashboard.behavior_decision.behavior_status.value
                         if dashboard.behavior_decision else "CLEAN"),
            "paper_only": True,
        },
        {
            "name": "no_trade_reasons",
            "reasons": [r.value for r in dashboard.no_trade_reasons],
            "block_reasons": [b.value for b in dashboard.block_reasons],
            "paper_only": True,
        },
        {
            "name": "paper_plan_summary",
            "plan_valid": dashboard.paper_plan.plan_valid if dashboard.paper_plan else False,
            "buy_point_type": (dashboard.paper_plan.buy_point_type
                               if dashboard.paper_plan else "N/A"),
            "broker_execution_enabled": False,
            "no_real_orders": True,
            "paper_only": True,
        },
        {
            "name": "safety_disclaimer",
            "disclaimer": (
                "PAPER ONLY. RESEARCH ONLY. NO REAL ORDERS. NO BROKER. "
                "NOT INVESTMENT ADVICE. DEMO ONLY. NOT FOR PRODUCTION."
            ),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
            "demo_only": True,
            "not_for_production": True,
        },
    ]

    return IntegratedStrategyReport(
        date=dashboard.date,
        symbol=dashboard.symbol,
        source_lineage=_LINEAGE,
        action=action,
        final_score=final_score,
        grade=(decision.grade if decision else __import__(
            "paper_trading.small_capital_strategy.integrated_strategy_enums_v178",
            fromlist=["IntegratedScoreGrade"]
        ).IntegratedScoreGrade.BLOCKED),
        sections=sections,
        summary=summary,
        report_format="text",
    )
