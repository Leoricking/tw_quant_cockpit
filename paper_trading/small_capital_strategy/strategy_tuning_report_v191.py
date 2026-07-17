"""
paper_trading/small_capital_strategy/strategy_tuning_report_v191.py
Report / export functions for Paper Strategy Rule Tuning & Guardrail Lab v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json as _json
from typing import Any, Dict, List, Optional

_SCHEMA = "191"
_SAFE = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "tuning_only": True, "guardrail_only": True,
    "review_only": True, "report_only": True, "audit_only": True,
    "no_real_orders": True, "no_broker": True, "no_margin": True,
    "no_leverage": True, "no_production_strategy_mutation": True,
    "not_investment_advice": True, "demo_only": True,
    "not_for_production": True, "production_trading_blocked": True,
}


def export_tuning_summary_as_json(summary: Dict[str, Any]) -> str:
    """Export rule tuning summary as JSON string."""
    payload = {
        "report_type": "strategy_rule_tuning_summary",
        "version": "1.9.1",
        "schema_version": _SCHEMA,
        **_SAFE,
        "summary": summary,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_guardrail_report_as_json(guardrails: List[Dict[str, Any]]) -> str:
    """Export guardrail review report as JSON string."""
    payload = {
        "report_type": "guardrail_review_report",
        "version": "1.9.1",
        "schema_version": _SCHEMA,
        **_SAFE,
        "guardrail_count": len(guardrails),
        "guardrails": guardrails,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_recommendations_as_json(recommendations: List[Dict[str, Any]]) -> str:
    """Export rule tuning recommendations as JSON string."""
    payload = {
        "report_type": "rule_tuning_recommendations",
        "version": "1.9.1",
        "schema_version": _SCHEMA,
        **_SAFE,
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_recommendations_as_markdown(
    recommendations: List[Dict[str, Any]],
    period_label: str = "tuning_period",
) -> str:
    """Export rule tuning recommendations as Markdown."""
    lines = [
        f"# Rule Tuning Recommendations — {period_label}",
        "",
        "> [!] Research Only. Paper Only. Tuning Only. Guardrail Only. Not Investment Advice.",
        "",
        f"**Version:** 1.9.1  **Schema:** {_SCHEMA}  **paper_only:** True",
        "",
        f"## Recommendations ({len(recommendations)})",
        "",
    ]
    for i, r in enumerate(recommendations, 1):
        rtype = r.get("recommendation_type", "NO_CHANGE")
        target = r.get("rule_target", "unknown")
        priority = r.get("priority", "LOW")
        lines.append(f"### {i}. [{priority}] {rtype} — {target}")
        lines.append("")
        lines.append(f"**Rationale:** {r.get('rationale', '')}")
        lines.append("")
    lines.append("---")
    lines.append("*Research Only | Paper Only | Tuning Only | No Real Orders | Not Investment Advice*")
    return "\n".join(lines)


def export_dashboard_as_json(dashboard: Dict[str, Any]) -> str:
    """Export rule tuning dashboard as JSON string."""
    payload = {
        "report_type": "rule_tuning_dashboard",
        "version": "1.9.1",
        "schema_version": _SCHEMA,
        **_SAFE,
        "dashboard": dashboard,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_evidence_pack_as_json(pack: Dict[str, Any]) -> str:
    """Export evidence pack as JSON string."""
    payload = {
        "report_type": "rule_tuning_evidence_pack",
        "version": "1.9.1",
        "schema_version": _SCHEMA,
        **_SAFE,
        "evidence_pack": pack,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_audit_trail_as_json(trail: Dict[str, Any]) -> str:
    """Export audit trail as JSON string."""
    payload = {
        "report_type": "rule_tuning_audit_trail",
        "version": "1.9.1",
        "schema_version": _SCHEMA,
        **_SAFE,
        "audit_trail": trail,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_manifest_as_json(manifest: Dict[str, Any]) -> str:
    """Export export manifest as JSON string."""
    payload = {
        "report_type": "rule_tuning_export_manifest",
        "version": "1.9.1",
        "schema_version": _SCHEMA,
        **_SAFE,
        "manifest": manifest,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_abc_analysis_as_json(abc_data: Dict[str, Any]) -> str:
    """Export A/B/C buy point analysis as JSON string."""
    payload = {
        "report_type": "abc_buy_point_analysis",
        "version": "1.9.1",
        "schema_version": _SCHEMA,
        **_SAFE,
        "abc_analysis": abc_data,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_position_sizing_report_as_json(ps_data: Dict[str, Any]) -> str:
    """Export position sizing tuning report as JSON string."""
    payload = {
        "report_type": "position_sizing_tuning_report",
        "version": "1.9.1",
        "schema_version": _SCHEMA,
        **_SAFE,
        "position_sizing": ps_data,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_console_summary(
    tuning_summary: Dict[str, Any],
    period_label: str = "tuning_period",
) -> str:
    """Export a console-friendly summary string."""
    total = tuning_summary.get("total_rules_reviewed", 0)
    tighten = tuning_summary.get("rules_to_tighten", 0)
    guardrails = tuning_summary.get("guardrails_triggered", 0)
    return (
        f"[Rule Tuning v1.9.1 | {period_label}] "
        f"RulesReviewed={total} ToTighten={tighten} GuardrailsTriggered={guardrails} "
        f"paper_only=True no_real_orders=True not_investment_advice=True"
    )


def get_report_info() -> Dict[str, Any]:
    """Return report module metadata."""
    return {
        "module": "strategy_tuning_report_v191",
        "version": "1.9.1",
        "schema_version": _SCHEMA,
        "functions": [
            "export_tuning_summary_as_json",
            "export_guardrail_report_as_json",
            "export_recommendations_as_json",
            "export_recommendations_as_markdown",
            "export_dashboard_as_json",
            "export_evidence_pack_as_json",
            "export_audit_trail_as_json",
            "export_manifest_as_json",
            "export_abc_analysis_as_json",
            "export_position_sizing_report_as_json",
            "export_console_summary",
        ],
        **_SAFE,
    }
