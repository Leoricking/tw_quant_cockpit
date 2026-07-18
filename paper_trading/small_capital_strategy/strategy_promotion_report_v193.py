"""
paper_trading/small_capital_strategy/strategy_promotion_report_v193.py
Report / export functions for Paper Strategy Promotion Package & Rollback Plan Lab v1.9.3.
[!] Research Only. Paper Only. Promotion Package Only. Rollback Plan Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json as _json
from typing import Any, Dict, List

_SCHEMA = "193"
_SAFE = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "promotion_package_only": True,
    "rollback_plan_only": True, "review_only": True, "report_only": True,
    "audit_only": True, "no_real_orders": True, "no_broker": True,
    "no_margin": True, "no_leverage": True,
    "no_production_strategy_mutation": True,
    "no_live_strategy_activation": True, "not_investment_advice": True,
    "demo_only": True, "not_for_production": True,
    "production_trading_blocked": True,
}


def export_promotion_summary_as_json(summary: Dict[str, Any]) -> str:
    """Export promotion package summary as JSON string."""
    payload = {
        "report_type": "strategy_promotion_summary",
        "version": "1.9.3",
        "schema_version": _SCHEMA,
        **_SAFE,
        "summary": summary,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_promotion_package_as_json(package: Dict[str, Any]) -> str:
    """Export promotion package as JSON string."""
    payload = {
        "report_type": "promotion_package_report",
        "version": "1.9.3",
        "schema_version": _SCHEMA,
        **_SAFE,
        "package": package,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_rollback_plan_as_json(plan: Dict[str, Any]) -> str:
    """Export rollback plan as JSON string."""
    payload = {
        "report_type": "rollback_plan_report",
        "version": "1.9.3",
        "schema_version": _SCHEMA,
        **_SAFE,
        "rollback_plan": plan,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_promotion_checklist_as_json(checklist: Dict[str, Any]) -> str:
    """Export promotion approval checklist as JSON string."""
    payload = {
        "report_type": "promotion_approval_checklist",
        "version": "1.9.3",
        "schema_version": _SCHEMA,
        **_SAFE,
        "checklist": checklist,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_promotion_evidence_pack_as_json(pack: Dict[str, Any]) -> str:
    """Export promotion evidence pack as JSON string."""
    payload = {
        "report_type": "promotion_evidence_pack",
        "version": "1.9.3",
        "schema_version": _SCHEMA,
        **_SAFE,
        "evidence_pack": pack,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_promotion_audit_trail_as_json(trail: Dict[str, Any]) -> str:
    """Export promotion audit trail as JSON string."""
    payload = {
        "report_type": "promotion_audit_trail",
        "version": "1.9.3",
        "schema_version": _SCHEMA,
        **_SAFE,
        "audit_trail": trail,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_promotion_dashboard_as_json(dashboard: Dict[str, Any]) -> str:
    """Export promotion dashboard as JSON string."""
    payload = {
        "report_type": "promotion_dashboard",
        "version": "1.9.3",
        "schema_version": _SCHEMA,
        **_SAFE,
        "dashboard": dashboard,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_promotion_recommendations_as_json(
    recommendations: List[Dict[str, Any]],
) -> str:
    """Export promotion recommendations as JSON string."""
    payload = {
        "report_type": "promotion_recommendations",
        "version": "1.9.3",
        "schema_version": _SCHEMA,
        **_SAFE,
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_rollback_plan_as_markdown(
    plan: Dict[str, Any],
    period_label: str = "promotion_period",
) -> str:
    """Export rollback plan as Markdown."""
    lines = [
        f"# Rollback Plan — {period_label}",
        "",
        "> [!] Research Only. Paper Only. Promotion Package Only. Rollback Plan Only. Not Investment Advice.",
        "",
        f"**Version:** 1.9.3  **Schema:** {_SCHEMA}  **paper_only:** True",
        "",
        "## Rollback Plan Details",
        "",
    ]
    for key, val in plan.items():
        lines.append(f"- **{key}:** {val}")
    lines.append("")
    lines.append("---")
    lines.append(
        "*Research Only | Paper Only | Promotion Package Only | Rollback Plan Only"
        " | No Real Orders | Not Investment Advice*"
    )
    return "\n".join(lines)


def export_promotion_console_summary(
    promotion_summary: Dict[str, Any],
    period_label: str = "promotion_period",
) -> str:
    """Export a console-friendly summary string for the promotion run."""
    approval_state = promotion_summary.get("approval_state", "DRAFT")
    regression_detected = promotion_summary.get("regression_detected", False)
    rollback_plan_present = promotion_summary.get("rollback_plan_present", False)
    return (
        f"[Strategy Promotion v1.9.3 | {period_label}] "
        f"approval_state={approval_state} "
        f"regression_detected={regression_detected} "
        f"rollback_plan_present={rollback_plan_present} "
        f"paper_only=True no_real_orders=True not_investment_advice=True"
    )


def get_report_info() -> Dict[str, Any]:
    """Return report module metadata."""
    return {
        "module": "strategy_promotion_report_v193",
        "version": "1.9.3",
        "schema_version": _SCHEMA,
        "functions": [
            "export_promotion_summary_as_json",
            "export_promotion_package_as_json",
            "export_rollback_plan_as_json",
            "export_promotion_checklist_as_json",
            "export_promotion_evidence_pack_as_json",
            "export_promotion_audit_trail_as_json",
            "export_promotion_dashboard_as_json",
            "export_promotion_recommendations_as_json",
            "export_rollback_plan_as_markdown",
            "export_promotion_console_summary",
        ],
        **_SAFE,
    }
