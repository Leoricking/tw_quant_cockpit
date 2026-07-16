"""
paper_trading/small_capital_strategy/decision_workflow_report_v188.py
Report output for Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Workflow Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
from typing import Dict, List, Any

from paper_trading.small_capital_strategy.decision_workflow_models_v188 import (
    WorkflowResult, WorkflowDashboard, WorkflowExportManifest,
)
from paper_trading.small_capital_strategy.decision_workflow_version_v188 import (
    VERSION, RELEASE_NAME,
)


def export_as_json(result: WorkflowResult) -> str:
    """Serialize WorkflowResult to JSON string."""
    data = {
        "workflow_version": result.workflow_version,
        "release_name": result.release_name,
        "workflow_type": result.workflow_type,
        "deterministic_timestamp_policy": result.deterministic_timestamp_policy,
        "capital_stage": result.capital_stage,
        "market_regime": result.market_regime,
        "workflow_action": result.workflow_action,
        "final_workflow_grade": result.final_workflow_grade,
        "candidate_count": result.candidate_count,
        "watch_candidate_count": result.watch_candidate_count,
        "paper_plan_ready_count": result.paper_plan_ready_count,
        "paper_entry_allowed_count": result.paper_entry_allowed_count,
        "reduce_risk_count": result.reduce_risk_count,
        "blocked_count": result.blocked_count,
        "total_exposure_pct": result.total_exposure_pct,
        "cash_reserve_pct": result.cash_reserve_pct,
        "concentration_risk_score": result.concentration_risk_score,
        "diversification_score": result.diversification_score,
        "monte_carlo_ruin_risk": result.monte_carlo_ruin_risk,
        "drawdown_budget_usage_pct": result.drawdown_budget_usage_pct,
        "block_reasons": result.block_reasons,
        "final_summary": result.final_summary,
        "paper_only": result.paper_only,
        "research_only": result.research_only,
        "workflow_only": result.workflow_only,
        "no_real_orders": result.no_real_orders,
        "no_broker": result.no_broker,
        "not_investment_advice": result.not_investment_advice,
        "production_trading_blocked": result.production_trading_blocked,
        "schema_version": result.schema_version,
    }
    return json.dumps(data, indent=2)


def export_as_markdown(result: WorkflowResult) -> str:
    """Serialize WorkflowResult to Markdown string."""
    lines = [
        f"# Decision Workflow Report v{result.workflow_version}",
        f"",
        f"**Release:** {result.release_name}",
        f"**Workflow Type:** {result.workflow_type}",
        f"**Capital Stage:** {result.capital_stage}",
        f"**Market Regime:** {result.market_regime}",
        f"",
        f"## Result",
        f"- **Workflow Action:** {result.workflow_action}",
        f"- **Final Workflow Grade:** {result.final_workflow_grade}",
        f"- **Candidate Count:** {result.candidate_count}",
        f"- **Blocked Count:** {result.blocked_count}",
        f"- **Total Exposure %:** {result.total_exposure_pct}",
        f"- **Cash Reserve %:** {result.cash_reserve_pct}",
        f"- **Monte Carlo Ruin Risk:** {result.monte_carlo_ruin_risk}",
        f"",
        f"## Block Reasons",
    ]
    if result.block_reasons:
        for r in result.block_reasons:
            lines.append(f"- {r}")
    else:
        lines.append("None")
    lines += [
        f"",
        f"## Summary",
        f"{result.final_summary}",
        f"",
        f"---",
        f"[!] Research Only. Paper Only. Workflow Only. No Real Orders. Not Investment Advice.",
    ]
    return "\n".join(lines)


def export_as_console_summary(result: WorkflowResult) -> str:
    """Return a concise console summary string."""
    return (
        f"Decision Workflow v{result.workflow_version} | {result.workflow_type} | "
        f"Regime={result.market_regime} | Action={result.workflow_action} | "
        f"Grade={result.final_workflow_grade} | "
        f"Candidates={result.candidate_count} | "
        f"Exposure={result.total_exposure_pct:.1f}% | Cash={result.cash_reserve_pct:.1f}% | "
        f"Blocks={len(result.block_reasons)} | "
        f"[PAPER ONLY | NO REAL ORDERS]"
    )


def export_as_dashboard_payload(result: WorkflowResult) -> Dict[str, Any]:
    """Return dict suitable for dashboard rendering."""
    return {
        "workflow_version": result.workflow_version,
        "release_name": result.release_name,
        "workflow_type": result.workflow_type,
        "market_regime": result.market_regime,
        "capital_stage": result.capital_stage,
        "workflow_action": result.workflow_action,
        "final_workflow_grade": result.final_workflow_grade,
        "candidate_count": result.candidate_count,
        "paper_plan_ready_count": result.paper_plan_ready_count,
        "blocked_count": result.blocked_count,
        "total_exposure_pct": result.total_exposure_pct,
        "cash_reserve_pct": result.cash_reserve_pct,
        "monte_carlo_ruin_risk": result.monte_carlo_ruin_risk,
        "block_reasons": result.block_reasons,
        "final_summary": result.final_summary,
        "paper_only": result.paper_only,
        "no_real_orders": result.no_real_orders,
        "no_broker": result.no_broker,
        "not_investment_advice": result.not_investment_advice,
        "production_trading_blocked": result.production_trading_blocked,
        "schema_version": result.schema_version,
    }


def get_report_info() -> Dict[str, Any]:
    """Return report module metadata."""
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "export_formats": ["json", "markdown", "console_summary", "dashboard_payload"],
        "paper_only": True,
        "research_only": True,
        "workflow_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "188",
    }
