"""
paper_trading/small_capital_strategy/decision_report_export_v187.py
Export functions for Decision Report Export & Evidence Pack v1.8.7.
Supports: JSON, Markdown, CSV-like rows, console summary, dashboard payload.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json as _json
from typing import List, Dict, Any, Optional

EXPORT_SCHEMA_VERSION = "187"

_SAFE_EXPORT_PATH_KEYWORDS = ["report", "fixture", "test", "export", "output", "temp"]
_UNSAFE_PATH_KEYWORDS = ["runtime_db", "production_db", "credentials", "tokens",
                          "live_session", "broker_session", "real_account", "cache"]


def _is_safe_path(path: str) -> bool:
    """Return True if the output path appears safe (non-production)."""
    path_lower = path.lower() if path else ""
    return not any(kw in path_lower for kw in _UNSAFE_PATH_KEYWORDS)


def _sanitize_action(action: str) -> str:
    """Return safe action string, replacing forbidden words with REPORT_ONLY."""
    forbidden = {"BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
                 "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER"}
    return action if action not in forbidden else "REPORT_ONLY"


def export_as_json(result, indent: int = 2) -> str:
    """Export DecisionReportResult as deterministic JSON string."""
    def _to_dict(obj) -> Any:
        if hasattr(obj, "__dataclass_fields__"):
            d = {}
            for f in obj.__dataclass_fields__:
                val = getattr(obj, f)
                d[f] = _to_dict(val)
            return d
        if isinstance(obj, list):
            return [_to_dict(i) for i in obj]
        if isinstance(obj, dict):
            return {k: _to_dict(v) for k, v in sorted(obj.items())}
        return obj

    payload = _to_dict(result) if hasattr(result, "__dataclass_fields__") else dict(result)
    payload.setdefault("export_format", "json")
    payload.setdefault("schema_version", EXPORT_SCHEMA_VERSION)
    payload.setdefault("paper_only", True)
    payload.setdefault("report_only", True)
    payload.setdefault("audit_only", True)
    payload.setdefault("no_real_orders", True)
    payload.setdefault("not_investment_advice", True)
    payload.setdefault("production_trading_blocked", True)
    return _json.dumps(payload, sort_keys=True, indent=indent, ensure_ascii=False)


def export_as_markdown(result) -> str:
    """Export DecisionReportResult as Markdown report."""
    lines = []
    lines.append("# Decision Report Export — v1.8.7")
    lines.append("")
    lines.append("> **[!] Research Only | Paper Only | Report Only | Audit Only**")
    lines.append("> No Real Orders | No Broker | Not Investment Advice")
    lines.append("")

    report_type = getattr(result, "report_type", "decision_report")
    capital_stage = getattr(result, "capital_stage", "300K")
    market_regime = getattr(result, "market_regime", "BULL")
    daily_action = _sanitize_action(getattr(result, "daily_action", "DECISION_ONLY"))
    weekly_action = _sanitize_action(getattr(result, "weekly_action", "DECISION_ONLY"))
    final_grade = getattr(result, "final_cockpit_grade", "WAIT")
    report_grade = getattr(result, "final_report_grade", "COMPLETE")

    lines.append(f"## Report Type: `{report_type}`")
    lines.append("")
    lines.append(f"| Field | Value |")
    lines.append(f"|-------|-------|")
    lines.append(f"| Capital Stage | {capital_stage} |")
    lines.append(f"| Market Regime | {market_regime} |")
    lines.append(f"| Daily Action | {daily_action} |")
    lines.append(f"| Weekly Action | {weekly_action} |")
    lines.append(f"| Final Cockpit Grade | {final_grade} |")
    lines.append(f"| Final Report Grade | **{report_grade}** |")
    lines.append(f"| Total Exposure | {getattr(result, 'total_exposure_pct', 0.0):.1f}% |")
    lines.append(f"| Cash Reserve | {getattr(result, 'cash_reserve_pct', 100.0):.1f}% |")
    lines.append(f"| Monte Carlo Ruin Risk | {getattr(result, 'monte_carlo_ruin_risk', 0.0):.2f}% |")
    lines.append("")

    lines.append("## Candidates")
    lines.append("")
    lines.append(f"- Total: {getattr(result, 'candidate_count', 0)}")
    lines.append(f"- Ready (Paper Entry): {getattr(result, 'ready_candidate_count', 0)}")
    lines.append(f"- Watch (Paper Plan): {getattr(result, 'watch_candidate_count', 0)}")
    lines.append(f"- Blocked: {getattr(result, 'blocked_candidate_count', 0)}")
    lines.append(f"- Reduce Risk: {getattr(result, 'reduce_risk_candidate_count', 0)}")
    lines.append("")

    ready_list = getattr(result, "paper_plan_ready_candidates", [])
    if ready_list:
        lines.append("### Paper Plan Ready")
        for t in ready_list:
            lines.append(f"- `{t}` — PAPER_PLAN_READY")
        lines.append("")

    blocked_list = getattr(result, "blocked_candidates", [])
    if blocked_list:
        lines.append("### Blocked Candidates")
        for t in blocked_list:
            lines.append(f"- `{t}` — BLOCKED")
        lines.append("")

    block_reasons = getattr(result, "block_reasons", [])
    if block_reasons:
        lines.append("### Block Reasons")
        for r in block_reasons:
            lines.append(f"- `{r}`")
        lines.append("")

    audit_trail = getattr(result, "audit_trail", [])
    if audit_trail:
        lines.append("## Audit Trail")
        lines.append("")
        for entry in audit_trail:
            if isinstance(entry, dict):
                step = entry.get("step", "")
                value = entry.get("value", "")
                action = _sanitize_action(entry.get("action", "REPORT_ONLY"))
                lines.append(f"- **{step}**: `{value}` → `{action}`")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*[!] This report is for research, paper simulation, and audit purposes only.*")
    lines.append("*No real orders. No broker. No margin. No leverage. Not investment advice.*")
    lines.append("")
    return "\n".join(lines)


def export_as_csv_rows(result) -> List[str]:
    """Export DecisionReportResult as deterministic CSV-like rows (list of strings)."""
    rows = []
    rows.append("field,value,paper_only,report_only")
    rows.append(f"report_type,{getattr(result, 'report_type', 'decision_report')},true,true")
    rows.append(f"report_version,{getattr(result, 'report_version', '1.8.7')},true,true")
    rows.append(f"capital_stage,{getattr(result, 'capital_stage', '300K')},true,true")
    rows.append(f"market_regime,{getattr(result, 'market_regime', 'BULL')},true,true")
    rows.append(f"daily_action,{_sanitize_action(getattr(result, 'daily_action', 'DECISION_ONLY'))},true,true")
    rows.append(f"weekly_action,{_sanitize_action(getattr(result, 'weekly_action', 'DECISION_ONLY'))},true,true")
    rows.append(f"final_cockpit_grade,{getattr(result, 'final_cockpit_grade', 'WAIT')},true,true")
    rows.append(f"final_report_grade,{getattr(result, 'final_report_grade', 'COMPLETE')},true,true")
    rows.append(f"candidate_count,{getattr(result, 'candidate_count', 0)},true,true")
    rows.append(f"ready_candidate_count,{getattr(result, 'ready_candidate_count', 0)},true,true")
    rows.append(f"watch_candidate_count,{getattr(result, 'watch_candidate_count', 0)},true,true")
    rows.append(f"blocked_candidate_count,{getattr(result, 'blocked_candidate_count', 0)},true,true")
    rows.append(f"reduce_risk_candidate_count,{getattr(result, 'reduce_risk_candidate_count', 0)},true,true")
    rows.append(f"total_exposure_pct,{getattr(result, 'total_exposure_pct', 0.0):.2f},true,true")
    rows.append(f"cash_reserve_pct,{getattr(result, 'cash_reserve_pct', 100.0):.2f},true,true")
    rows.append(f"monte_carlo_ruin_risk,{getattr(result, 'monte_carlo_ruin_risk', 0.0):.4f},true,true")
    rows.append(f"concentration_risk_score,{getattr(result, 'concentration_risk_score', 0.0):.2f},true,true")
    rows.append(f"diversification_score,{getattr(result, 'diversification_score', 100.0):.2f},true,true")
    rows.append(f"max_drawdown_budget_usage_pct,{getattr(result, 'max_drawdown_budget_usage_pct', 0.0):.2f},true,true")
    rows.append(f"no_real_orders,true,true,true")
    rows.append(f"no_broker,true,true,true")
    rows.append(f"not_investment_advice,true,true,true")
    rows.append(f"production_trading_blocked,true,true,true")
    return rows


def export_as_console_summary(result) -> str:
    """Export DecisionReportResult as compact console summary string."""
    daily_action = _sanitize_action(getattr(result, "daily_action", "DECISION_ONLY"))
    final_grade = getattr(result, "final_cockpit_grade", "WAIT")
    report_grade = getattr(result, "final_report_grade", "COMPLETE")
    market = getattr(result, "market_regime", "BULL")
    capital = getattr(result, "capital_stage", "300K")
    exposure = getattr(result, "total_exposure_pct", 0.0)
    cash = getattr(result, "cash_reserve_pct", 100.0)
    ruin = getattr(result, "monte_carlo_ruin_risk", 0.0)
    candidates = getattr(result, "candidate_count", 0)
    ready = getattr(result, "ready_candidate_count", 0)
    blocked = getattr(result, "blocked_candidate_count", 0)

    lines = [
        f"[Decision Report v1.8.7] {report_grade}",
        f"  Type: {getattr(result, 'report_type', 'decision_report')}",
        f"  Capital: {capital} | Regime: {market}",
        f"  Grade: {final_grade} | Action: {daily_action}",
        f"  Exposure: {exposure:.1f}% | Cash: {cash:.1f}% | Ruin: {ruin:.2f}%",
        f"  Candidates: {candidates} | Ready: {ready} | Blocked: {blocked}",
        f"  [!] Research Only | Paper Only | No Real Orders | Not Investment Advice",
    ]
    return "\n".join(lines)


def export_as_dashboard_payload(result) -> Dict[str, Any]:
    """Export DecisionReportResult as compact dashboard payload dict."""
    return {
        "report_version": getattr(result, "report_version", "1.8.7"),
        "report_type": getattr(result, "report_type", "decision_report"),
        "capital_stage": getattr(result, "capital_stage", "300K"),
        "market_regime": getattr(result, "market_regime", "BULL"),
        "daily_action": _sanitize_action(getattr(result, "daily_action", "DECISION_ONLY")),
        "weekly_action": _sanitize_action(getattr(result, "weekly_action", "DECISION_ONLY")),
        "final_cockpit_grade": getattr(result, "final_cockpit_grade", "WAIT"),
        "final_report_grade": getattr(result, "final_report_grade", "COMPLETE"),
        "candidate_count": getattr(result, "candidate_count", 0),
        "ready_candidate_count": getattr(result, "ready_candidate_count", 0),
        "watch_candidate_count": getattr(result, "watch_candidate_count", 0),
        "blocked_candidate_count": getattr(result, "blocked_candidate_count", 0),
        "reduce_risk_candidate_count": getattr(result, "reduce_risk_candidate_count", 0),
        "total_exposure_pct": getattr(result, "total_exposure_pct", 0.0),
        "cash_reserve_pct": getattr(result, "cash_reserve_pct", 100.0),
        "monte_carlo_ruin_risk": getattr(result, "monte_carlo_ruin_risk", 0.0),
        "concentration_risk_score": getattr(result, "concentration_risk_score", 0.0),
        "paper_plan_ready_candidates": list(getattr(result, "paper_plan_ready_candidates", [])),
        "blocked_candidates": list(getattr(result, "blocked_candidates", [])),
        "block_reasons": list(getattr(result, "block_reasons", [])),
        "paper_only": True,
        "research_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "schema_version": "187",
    }


def run_all_exports(result) -> Dict[str, Any]:
    """Run all export formats and return a dict with all outputs + manifest."""
    from paper_trading.small_capital_strategy.decision_report_engine_v187 import build_export_manifest

    json_out = export_as_json(result)
    md_out = export_as_markdown(result)
    rows_out = export_as_csv_rows(result)
    console_out = export_as_console_summary(result)
    dashboard_out = export_as_dashboard_payload(result)

    exports = [
        {"format": "json", "size": len(json_out), "safe": True},
        {"format": "markdown", "size": len(md_out), "safe": True},
        {"format": "csv_rows", "size": len(rows_out), "safe": True},
        {"format": "console_summary", "size": len(console_out), "safe": True},
        {"format": "dashboard_payload", "size": len(str(dashboard_out)), "safe": True},
    ]
    manifest = build_export_manifest(exports)

    return {
        "json": json_out,
        "markdown": md_out,
        "csv_rows": rows_out,
        "console_summary": console_out,
        "dashboard_payload": dashboard_out,
        "manifest": manifest,
        "paper_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "schema_version": "187",
    }


def get_export_info() -> dict:
    """Return export module metadata."""
    return {
        "version": "1.8.7",
        "supported_formats": ["json", "markdown", "csv_rows", "console_summary", "dashboard_payload"],
        "schema_version": EXPORT_SCHEMA_VERSION,
        "paper_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_production_db_writes": True,
        "deterministic_output": True,
    }
