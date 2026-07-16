"""
paper_trading/small_capital_strategy/decision_performance_report_v190.py
Report / export functions for Paper Trading Performance Review & Strategy Improvement Lab v1.9.0.
[!] Research Only. Paper Only. Performance Review Only. Strategy Improvement Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json as _json
from typing import Any, Dict, List, Optional

_SCHEMA = "190"
_SAFE = {
    "paper_only": True, "research_only": True, "simulate_only": True,
    "validation_only": True, "review_only": True, "performance_review_only": True,
    "strategy_improvement_only": True, "report_only": True, "audit_only": True,
    "no_real_orders": True, "no_broker": True, "no_margin": True,
    "no_leverage": True, "not_investment_advice": True, "demo_only": True,
    "not_for_production": True, "production_trading_blocked": True,
}


def export_strategy_summary_as_json(summary: Dict[str, Any]) -> str:
    """Export strategy performance summary as JSON string."""
    payload = {
        "report_type": "strategy_performance_summary",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        **_SAFE,
        "summary": summary,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_setup_analytics_as_json(setups: List[Dict[str, Any]]) -> str:
    """Export setup analytics as JSON string."""
    payload = {
        "report_type": "setup_analytics",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        **_SAFE,
        "setup_count": len(setups),
        "setups": setups,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_r_multiple_as_json(r_summary: Dict[str, Any]) -> str:
    """Export R-multiple summary as JSON string."""
    payload = {
        "report_type": "r_multiple_summary",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        **_SAFE,
        "r_multiple": r_summary,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_drawdown_as_json(drawdown: Dict[str, Any]) -> str:
    """Export drawdown review as JSON string."""
    payload = {
        "report_type": "drawdown_review",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        **_SAFE,
        "drawdown": drawdown,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_expectancy_as_json(expectancy: Dict[str, Any]) -> str:
    """Export expectancy summary as JSON string."""
    payload = {
        "report_type": "expectancy_summary",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        **_SAFE,
        "expectancy": expectancy,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_improvement_report_as_json(suggestions: List[Dict[str, Any]]) -> str:
    """Export strategy improvement suggestions as JSON string."""
    payload = {
        "report_type": "strategy_improvement_report",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        **_SAFE,
        "suggestion_count": len(suggestions),
        "suggestions": suggestions,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_improvement_report_as_markdown(
    suggestions: List[Dict[str, Any]],
    period_label: str = "review_period",
) -> str:
    """Export strategy improvement suggestions as Markdown."""
    lines = [
        f"# Strategy Improvement Report — {period_label}",
        "",
        "> [!] Research Only. Paper Only. Performance Review Only. Not Investment Advice.",
        "",
        f"**Version:** 1.9.0  **Schema:** {_SCHEMA}  **paper_only:** True",
        "",
        f"## Suggestions ({len(suggestions)})",
        "",
    ]
    for i, s in enumerate(suggestions, 1):
        stype = s.get("suggestion_type", "NO_CHANGE")
        target = s.get("rule_target", "unknown")
        priority = s.get("priority", "LOW")
        lines.append(f"### {i}. [{priority}] {stype} — {target}")
        lines.append("")
        lines.append(f"**Rationale:** {s.get('rationale', '')}")
        lines.append("")
    lines.append("---")
    lines.append("*Research Only | Paper Only | No Real Orders | Not Investment Advice*")
    return "\n".join(lines)


def export_dashboard_as_json(dashboard: Dict[str, Any]) -> str:
    """Export performance review dashboard as JSON string."""
    payload = {
        "report_type": "performance_review_dashboard",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        **_SAFE,
        "dashboard": dashboard,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_manifest_as_json(manifest: Dict[str, Any]) -> str:
    """Export export manifest as JSON string."""
    payload = {
        "report_type": "performance_review_export_manifest",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        **_SAFE,
        "manifest": manifest,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_evidence_pack_as_json(pack: Dict[str, Any]) -> str:
    """Export evidence pack as JSON string."""
    payload = {
        "report_type": "performance_review_evidence_pack",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        **_SAFE,
        "evidence_pack": pack,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_audit_trail_as_json(trail: Dict[str, Any]) -> str:
    """Export audit trail as JSON string."""
    payload = {
        "report_type": "performance_review_audit_trail",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        **_SAFE,
        "audit_trail": trail,
    }
    return _json.dumps(payload, indent=2, default=str)


def export_console_summary(
    strategy_summary: Dict[str, Any],
    period_label: str = "review_period",
) -> str:
    """Export a console-friendly summary string."""
    total = strategy_summary.get("total_paper_decisions", 0)
    win_rate = strategy_summary.get("win_rate", 0.0)
    mistake_rate = strategy_summary.get("mistake_rate", 0.0)
    return (
        f"[Performance Review v1.9.0 | {period_label}] "
        f"Decisions={total} WinRate={win_rate:.1%} MistakeRate={mistake_rate:.1%} "
        f"paper_only=True no_real_orders=True not_investment_advice=True"
    )


def get_report_info() -> Dict[str, Any]:
    """Return report module metadata."""
    return {
        "module": "decision_performance_report_v190",
        "version": "1.9.0",
        "schema_version": _SCHEMA,
        "functions": [
            "export_strategy_summary_as_json",
            "export_setup_analytics_as_json",
            "export_r_multiple_as_json",
            "export_drawdown_as_json",
            "export_expectancy_as_json",
            "export_improvement_report_as_json",
            "export_improvement_report_as_markdown",
            "export_dashboard_as_json",
            "export_manifest_as_json",
            "export_evidence_pack_as_json",
            "export_audit_trail_as_json",
            "export_console_summary",
        ],
        **_SAFE,
    }
