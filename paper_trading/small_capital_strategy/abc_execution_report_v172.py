"""
paper_trading/small_capital_strategy/abc_execution_report_v172.py
Execution report for A/B/C Buy Point Execution Plan v1.7.2.
16 fixed sections. Markdown / JSON / CSV / console / GUI output.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
import csv
import io
from typing import Any, Dict, List, Optional

from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
    ABCExecutionPlan, ABCExecutionReport,
)

SECTION_NAMES: List[str] = [
    "abc_execution_summary",
    "candidate_watchlist_tier",
    "buy_point_type",
    "required_conditions",
    "missing_conditions",
    "entry_plan",
    "add_plan",
    "stop_loss_plan",
    "take_profit_plan",
    "position_sizing",
    "market_regime_compatibility",
    "forbidden_rule_checks",
    "paper_order_intent",
    "scorecard",
    "safety",
    "not_investment_advice",
]

_DISCLAIMER = (
    "Research Only. Paper Only. No Real Orders. Not Investment Advice. "
    "This output is for simulation and research purposes only. "
    "Not financial advice. Not for production use."
)


def _plan_to_sections(plan: ABCExecutionPlan) -> Dict[str, Any]:
    """Extract all 16 sections from an execution plan."""
    sections: Dict[str, Any] = {}

    sections["abc_execution_summary"] = {
        "symbol": plan.symbol,
        "buy_point_type": plan.buy_point_type.value if plan.buy_point_type else "N/A",
        "status": plan.status.value if plan.status else "N/A",
        "tier": plan.tier,
        "grade": plan.scorecard.grade.value if plan.scorecard else "N/A",
        "total_score": plan.scorecard.total_score if plan.scorecard else 0.0,
        "paper_only": True,
        "research_only": True,
    }

    sections["candidate_watchlist_tier"] = {
        "tier": plan.tier,
        "symbol": plan.symbol,
        "compatibility": (
            plan.watchlist_bridge.compatibility.value
            if plan.watchlist_bridge else "N/A"
        ),
        "allowed_buy_points": [
            b.value for b in (
                plan.watchlist_bridge.allowed_buy_points
                if plan.watchlist_bridge else []
            )
        ],
    }

    sections["buy_point_type"] = {
        "buy_point_type": plan.buy_point_type.value if plan.buy_point_type else "N/A",
        "description": str(plan.buy_point_type) if plan.buy_point_type else "N/A",
    }

    all_conditions = [
        {"name": c.condition_name, "status": c.status.value, "detail": c.detail}
        for c in plan.conditions_checked
    ]
    met_conditions = [c for c in plan.conditions_checked if c.status.value == "MET"]
    missing_conditions = [c for c in plan.conditions_checked if c.status.value != "MET"]

    sections["required_conditions"] = {
        "total": len(all_conditions),
        "met": len(met_conditions),
        "conditions": all_conditions,
    }

    sections["missing_conditions"] = {
        "count": len(missing_conditions),
        "conditions": [
            {"name": c.condition_name, "detail": c.detail, "blocking": c.is_blocking}
            for c in missing_conditions
        ],
    }

    ep = plan.entry_plan
    sections["entry_plan"] = {
        "entry_mode": ep.entry_mode.value if ep else "N/A",
        "entry_price": ep.entry_price if ep else 0.0,
        "status": ep.status.value if ep else "N/A",
        "note": ep.entry_price_note if ep else "",
        "paper_only": True,
    }

    ap = plan.add_plan
    sections["add_plan"] = {
        "add_mode": ap.add_mode.value if ap else "N/A",
        "add_price": ap.add_price if ap else 0.0,
        "max_add_units": ap.max_add_units if ap else 0,
        "note": ap.add_price_note if ap else "",
        "paper_only": True,
    }

    sl = plan.stop_loss_plan
    sections["stop_loss_plan"] = {
        "stop_loss_mode": sl.stop_loss_mode.value if sl else "N/A",
        "stop_loss_price": sl.stop_loss_price if sl else 0.0,
        "stop_loss_pct": sl.stop_loss_pct_from_entry if sl else 0.0,
        "note": sl.stop_loss_note if sl else "",
        "paper_only": True,
    }

    tp = plan.take_profit_plan
    sections["take_profit_plan"] = {
        "take_profit_mode": tp.take_profit_mode.value if tp else "N/A",
        "references": tp.take_profit_references if tp else [],
        "partial_pct_first": tp.partial_pct_first if tp else 0.0,
        "swing_pct_target": tp.swing_pct_target if tp else 0.0,
        "note": tp.take_profit_note if tp else "",
        "paper_only": True,
    }

    ps = plan.position_sizing
    sections["position_sizing"] = {
        "capital_twd": ps.capital_twd if ps else 0.0,
        "position_amount": ps.position_amount if ps else 0.0,
        "quantity_estimate": ps.quantity_estimate if ps else 0,
        "max_loss_amount": ps.max_loss_amount if ps else 0.0,
        "risk_pct": ps.risk_pct if ps else 0.0,
        "training_cap_applied": ps.training_cap_applied if ps else False,
        "risk_permission": ps.risk_permission.value if ps else "N/A",
        "paper_only": True,
    }

    rb = plan.regime_bridge
    sections["market_regime_compatibility"] = {
        "market_regime": rb.market_regime if rb else "N/A",
        "compatibility": rb.compatibility.value if rb else "N/A",
        "block_reasons": [r.value for r in (rb.block_reasons if rb else [])],
        "warnings": [w.value for w in (rb.warnings if rb else [])],
    }

    sections["forbidden_rule_checks"] = {
        "total": len(plan.forbidden_checks),
        "passed": sum(1 for c in plan.forbidden_checks if c.passed),
        "rules": [
            {"rule": c.rule_name, "passed": c.passed, "detail": c.detail}
            for c in plan.forbidden_checks
        ],
    }

    pi = plan.paper_intent
    sections["paper_order_intent"] = {
        "action": pi.action.value if pi else "N/A",
        "reference_price": pi.reference_price if pi else 0.0,
        "quantity_estimate": pi.quantity_estimate if pi else 0,
        "stop_loss_price": pi.stop_loss_price if pi else 0.0,
        "paper_only": True,
        "no_real_orders": True,
        "broker_execution_enabled": False,
    }

    sc = plan.scorecard
    sections["scorecard"] = {
        "total_score": sc.total_score if sc else 0.0,
        "grade": sc.grade.value if sc else "N/A",
        "weights_sum": sc.weights_sum if sc else 100,
        "components": {
            "buy_point_condition": sc.buy_point_condition_score if sc else 0.0,
            "risk_sizing":         sc.risk_sizing_score if sc else 0.0,
            "watchlist_tier":      sc.watchlist_tier_score if sc else 0.0,
            "market_regime":       sc.market_regime_score if sc else 0.0,
            "stop_loss":           sc.stop_loss_score if sc else 0.0,
            "take_profit":         sc.take_profit_score if sc else 0.0,
            "safety":              sc.safety_score if sc else 0.0,
        },
    }

    sections["safety"] = {
        "all_safe": not bool(plan.block_reasons),
        "block_reasons": [r.value for r in plan.block_reasons],
        "warnings": [w.value for w in plan.warnings],
        "paper_only": True,
        "no_real_orders": True,
        "safety_capabilities": 0,
    }

    sections["not_investment_advice"] = {
        "disclaimer": _DISCLAIMER,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }

    return sections


def build_report(plan: ABCExecutionPlan, report_format: str = "JSON") -> ABCExecutionReport:
    """Build execution report from plan."""
    sections = _plan_to_sections(plan)
    return ABCExecutionReport(
        symbol=plan.symbol,
        buy_point_type=plan.buy_point_type,
        plan=plan,
        sections=sections,
        report_format=report_format,
    )


def render_markdown(report: ABCExecutionReport) -> str:
    """Render report as Markdown string."""
    lines = [
        f"# ABC Execution Report — {report.symbol}",
        "",
        "> Research Only. Paper Only. No Real Orders. Not Investment Advice.",
        "",
    ]
    for name in SECTION_NAMES:
        data = report.sections.get(name, {})
        lines.append(f"## {name.replace('_', ' ').title()}")
        lines.append("")
        for k, v in data.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
    return "\n".join(lines)


def render_json(report: ABCExecutionReport) -> str:
    """Render report as JSON string."""
    payload = {
        "symbol": report.symbol,
        "buy_point_type": report.buy_point_type.value if report.buy_point_type else "N/A",
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "sections": report.sections,
    }
    return json.dumps(payload, default=str, indent=2)


def render_csv(report: ABCExecutionReport) -> str:
    """Render report as CSV string (summary row)."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["symbol", "buy_point_type", "status", "grade", "total_score",
                     "tier", "paper_only", "not_investment_advice"])
    summary = report.sections.get("abc_execution_summary", {})
    writer.writerow([
        report.symbol,
        summary.get("buy_point_type", "N/A"),
        summary.get("status", "N/A"),
        summary.get("grade", "N/A"),
        summary.get("total_score", 0.0),
        summary.get("tier", "N/A"),
        True,
        True,
    ])
    return buf.getvalue()


def render_console_summary(report: ABCExecutionReport) -> str:
    """Render compact console summary."""
    s = report.sections.get("abc_execution_summary", {})
    sc = report.sections.get("scorecard", {})
    return (
        f"[ABC] {report.symbol} | {s.get('buy_point_type','N/A')} "
        f"| {s.get('status','N/A')} | Grade={s.get('grade','N/A')} "
        f"| Score={sc.get('total_score',0)} "
        f"| PaperOnly=True | NoRealOrders=True"
    )


def get_section_names() -> List[str]:
    """Return the 16 fixed section names."""
    return list(SECTION_NAMES)
