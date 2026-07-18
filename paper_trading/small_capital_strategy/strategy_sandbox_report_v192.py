"""
paper_trading/small_capital_strategy/strategy_sandbox_report_v192.py
Report / export functions for Paper Strategy Rule Sandbox & Shadow Validation Lab v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json as _json
from typing import Any, Dict, List, Optional

_SCHEMA = "192"
_SAFE = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "sandbox_only": True, "shadow_only": True,
    "review_only": True, "report_only": True, "audit_only": True,
    "no_real_orders": True, "no_broker": True, "no_margin": True,
    "no_leverage": True, "no_production_strategy_mutation": True,
    "no_live_strategy_activation": True, "not_investment_advice": True,
    "demo_only": True, "not_for_production": True,
    "production_trading_blocked": True,
}


def export_sandbox_summary_as_json(summary: Dict[str, Any]) -> str:
    """Export strategy sandbox summary as JSON string."""
    payload = {
        "report_type": "strategy_sandbox_summary",
        "version": "1.9.2",
        "schema_version": _SCHEMA,
        **_SAFE,
        "summary": summary,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_shadow_comparison_as_json(comparison: Dict[str, Any]) -> str:
    """Export shadow comparison report as JSON string."""
    payload = {
        "report_type": "shadow_comparison_report",
        "version": "1.9.2",
        "schema_version": _SCHEMA,
        **_SAFE,
        "comparison": comparison,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_sandbox_evidence_pack_as_json(pack: Dict[str, Any]) -> str:
    """Export sandbox evidence pack as JSON string."""
    payload = {
        "report_type": "sandbox_evidence_pack",
        "version": "1.9.2",
        "schema_version": _SCHEMA,
        **_SAFE,
        "evidence_pack": pack,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_sandbox_audit_trail_as_json(trail: Dict[str, Any]) -> str:
    """Export sandbox audit trail as JSON string."""
    payload = {
        "report_type": "sandbox_audit_trail",
        "version": "1.9.2",
        "schema_version": _SCHEMA,
        **_SAFE,
        "audit_trail": trail,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_sandbox_dashboard_as_json(dashboard: Dict[str, Any]) -> str:
    """Export sandbox dashboard as JSON string."""
    payload = {
        "report_type": "sandbox_dashboard",
        "version": "1.9.2",
        "schema_version": _SCHEMA,
        **_SAFE,
        "dashboard": dashboard,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_sandbox_manifest_as_json(manifest: Dict[str, Any]) -> str:
    """Export sandbox export manifest as JSON string."""
    payload = {
        "report_type": "sandbox_export_manifest",
        "version": "1.9.2",
        "schema_version": _SCHEMA,
        **_SAFE,
        "manifest": manifest,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_sandbox_recommendations_as_json(
    recommendations: List[Dict[str, Any]],
) -> str:
    """Export sandbox recommendations as JSON string."""
    payload = {
        "report_type": "sandbox_recommendations",
        "version": "1.9.2",
        "schema_version": _SCHEMA,
        **_SAFE,
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_rule_comparison_as_json(comparison: Dict[str, Any]) -> str:
    """Export sandbox rule comparison as JSON string."""
    payload = {
        "report_type": "sandbox_rule_comparison",
        "version": "1.9.2",
        "schema_version": _SCHEMA,
        **_SAFE,
        "rule_comparison": comparison,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_shadow_comparison_as_markdown(
    comparison: Dict[str, Any],
    period_label: str = "sandbox_period",
) -> str:
    """Export shadow validation comparison as Markdown."""
    lines = [
        f"# Shadow Validation Comparison — {period_label}",
        "",
        "> [!] Research Only. Paper Only. Sandbox Only. Shadow Only. Not Investment Advice.",
        "",
        f"**Version:** 1.9.2  **Schema:** {_SCHEMA}  **paper_only:** True",
        "",
        "## Shadow Comparison",
        "",
    ]
    for key, val in comparison.items():
        lines.append(f"- **{key}:** {val}")
    lines.append("")
    lines.append("---")
    lines.append(
        "*Research Only | Paper Only | Sandbox Only | Shadow Only"
        " | No Real Orders | Not Investment Advice*"
    )
    return "\n".join(lines)


def export_sandbox_console_summary(
    sandbox_summary: Dict[str, Any],
    period_label: str = "sandbox_period",
) -> str:
    """Export a console-friendly summary string for the sandbox run."""
    approval_state = sandbox_summary.get("approval_state", "SHADOW_ONLY")
    sandbox_mode = sandbox_summary.get("sandbox_mode", "SHADOW_COMPARE")
    regression_detected = sandbox_summary.get("regression_detected", False)
    return (
        f"[Strategy Sandbox v1.9.2 | {period_label}] "
        f"approval_state={approval_state} "
        f"sandbox_mode={sandbox_mode} "
        f"regression_detected={regression_detected} "
        f"paper_only=True no_real_orders=True not_investment_advice=True"
    )


def get_report_info() -> Dict[str, Any]:
    """Return report module metadata."""
    return {
        "module": "strategy_sandbox_report_v192",
        "version": "1.9.2",
        "schema_version": _SCHEMA,
        "functions": [
            "export_sandbox_summary_as_json",
            "export_shadow_comparison_as_json",
            "export_sandbox_evidence_pack_as_json",
            "export_sandbox_audit_trail_as_json",
            "export_sandbox_dashboard_as_json",
            "export_sandbox_manifest_as_json",
            "export_sandbox_recommendations_as_json",
            "export_rule_comparison_as_json",
            "export_shadow_comparison_as_markdown",
            "export_sandbox_console_summary",
        ],
        **_SAFE,
    }
