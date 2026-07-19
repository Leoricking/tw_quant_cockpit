"""
paper_trading/small_capital_strategy/portfolio_risk_report_report_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Report Module
[!] Paper Only. Research Only. Position Sizing Policy Only. Portfolio Risk Report Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List, Any

REPORT_SECTIONS = [
    "capital_profile",
    "risk_budget",
    "position_sizing_summary",
    "entry_sizing_rules",
    "stop_distance_analysis",
    "cash_buffer_status",
    "exposure_limits",
    "theme_concentration",
    "industry_concentration",
    "risk_off_status",
    "no_entry_conditions",
    "recommendations",
]

_PAPER_HEADER = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "portfolio_risk_report_only": True,
    "position_sizing_policy_only": True,
    "dashboard_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "not_investment_advice": True,
    "production_trading_blocked": True,
    "sizing_executes_order": False,
    "sizing_mutates_strategy": False,
    "sizing_rebalances_real_portfolio": False,
    "dashboard_mutates_strategy": False,
    "dashboard_places_real_order": False,
    "export_triggers_real_order": False,
    "report_triggers_rebalance": False,
}


def _with_header(data: dict) -> dict:
    result = dict(_PAPER_HEADER)
    result.update(data)
    return result


def export_capital_profile(capital_base: float = 300_000.0) -> dict:
    from .portfolio_risk_report_version_v199 import CAPITAL_PROFILE_300K
    return _with_header({
        "section": "capital_profile",
        "schema_version": "199",
        "capital_base": capital_base,
        "profile": dict(CAPITAL_PROFILE_300K),
    })


def export_risk_budget(
    capital_base: float = 300_000.0,
    used_risk_budget: float = 0.0,
    max_portfolio_risk_pct: float = 0.20,
) -> dict:
    total = capital_base * max_portfolio_risk_pct
    remaining = max(0.0, total - used_risk_budget)
    pct_used = used_risk_budget / total if total > 0 else 0.0
    return _with_header({
        "section": "risk_budget",
        "schema_version": "199",
        "capital_base": capital_base,
        "total_risk_budget": round(total, 2),
        "used_risk_budget": round(used_risk_budget, 2),
        "remaining_risk_budget": round(remaining, 2),
        "risk_budget_pct_used": round(pct_used, 4),
        "risk_budget_exceeded": pct_used >= 1.0,
    })


def export_position_sizing_summary(sizing_result: dict) -> dict:
    return _with_header({
        "section": "position_sizing_summary",
        "schema_version": "199",
        "sizing_result": sizing_result,
    })


def export_entry_sizing_rules() -> dict:
    from .portfolio_risk_report_version_v199 import ENTRY_SIZE_MULTIPLIERS
    rules = []
    descriptions = {
        "A_PULLBACK_10MA": "Pullback to 10MA support — normal size (1.0x)",
        "B_BREAKOUT_BASE": "Base breakout — reduced size (0.7x)",
        "C_RECLAIM_20MA": "Reclaim 20MA — half size (0.5x)",
        "TEST_POSITION": "Test / probe position — small size (0.3x)",
        "ADD_POSITION": "Add to existing winner — half size (0.5x)",
        "REDUCE_POSITION": "Reduce exposure — no new entry (0.0x)",
        "NO_ENTRY": "No entry condition triggered — blocked (0.0x)",
    }
    for et, mult in ENTRY_SIZE_MULTIPLIERS.items():
        rules.append({
            "entry_type": et,
            "size_multiplier": mult,
            "description": descriptions.get(et, ""),
        })
    return _with_header({
        "section": "entry_sizing_rules",
        "schema_version": "199",
        "rules": rules,
        "rules_count": len(rules),
    })


def export_stop_distance_analysis(stop_distance_pct: float) -> dict:
    from .portfolio_risk_report_version_v199 import CAPITAL_PROFILE_300K
    capital = CAPITAL_PROFILE_300K["capital_base"]
    max_risk = CAPITAL_PROFILE_300K["normal_single_trade_risk_pct_max"]
    if stop_distance_pct <= 0:
        return _with_header({
            "section": "stop_distance_analysis",
            "schema_version": "199",
            "blocked": True,
            "block_reason": "missing_stop_distance",
        })
    max_loss = capital * max_risk
    position_size = max_loss / stop_distance_pct
    blocked = stop_distance_pct > 0.15
    return _with_header({
        "section": "stop_distance_analysis",
        "schema_version": "199",
        "stop_distance_pct": stop_distance_pct,
        "max_loss_amount": round(max_loss, 2),
        "implied_position_size": round(position_size, 2),
        "blocked": blocked,
        "block_reason": "stop_distance_too_wide" if blocked else "",
    })


def export_cash_buffer_status(
    current_cash_pct: float,
    weak_market_mode: bool = False,
) -> dict:
    from .portfolio_risk_report_version_v199 import CAPITAL_PROFILE_300K
    min_cash = CAPITAL_PROFILE_300K["min_cash_buffer_pct"]
    weak_cash = CAPITAL_PROFILE_300K["weak_market_cash_buffer_pct"]
    required = weak_cash if weak_market_mode else min_cash
    ok = current_cash_pct >= required
    return _with_header({
        "section": "cash_buffer_status",
        "schema_version": "199",
        "current_cash_pct": current_cash_pct,
        "required_cash_pct": required,
        "cash_buffer_ok": ok,
        "weak_market_mode": weak_market_mode,
        "block_new_entry": not ok,
    })


def export_exposure_limits(
    theme_exposures: dict,
    industry_exposures: dict,
    symbol_weights: dict,
    high_correlation_cluster_weight: float = 0.0,
) -> dict:
    from .portfolio_risk_report_version_v199 import CAPITAL_PROFILE_300K
    theme_violations = {k: v for k, v in theme_exposures.items()
                        if v >= CAPITAL_PROFILE_300K["max_single_theme_weight"]}
    industry_violations = {k: v for k, v in industry_exposures.items()
                           if v >= CAPITAL_PROFILE_300K["max_single_industry_weight"]}
    symbol_violations = {k: v for k, v in symbol_weights.items()
                         if v >= CAPITAL_PROFILE_300K["max_single_symbol_weight"]}
    corr_exceeded = high_correlation_cluster_weight >= CAPITAL_PROFILE_300K["max_high_correlation_cluster_weight"]
    return _with_header({
        "section": "exposure_limits",
        "schema_version": "199",
        "theme_violations": theme_violations,
        "industry_violations": industry_violations,
        "symbol_violations": symbol_violations,
        "correlation_cluster_weight": high_correlation_cluster_weight,
        "correlation_limit_exceeded": corr_exceeded,
        "any_limit_exceeded": bool(theme_violations or industry_violations or symbol_violations or corr_exceeded),
    })


def export_no_entry_conditions(conditions: list) -> dict:
    triggered = [c for c in conditions if c.get("triggered")]
    return _with_header({
        "section": "no_entry_conditions",
        "schema_version": "199",
        "conditions": conditions,
        "triggered_count": len(triggered),
        "any_triggered": len(triggered) > 0,
    })


def export_risk_off_status(risk_off_active: bool) -> dict:
    from .portfolio_risk_report_version_v199 import CAPITAL_PROFILE_300K
    return _with_header({
        "section": "risk_off_status",
        "schema_version": "199",
        "risk_off_active": risk_off_active,
        "risk_off_max_risk_pct": CAPITAL_PROFILE_300K["risk_off_single_trade_risk_pct_max"],
        "risk_off_cash_buffer_pct": CAPITAL_PROFILE_300K["weak_market_cash_buffer_pct"],
        "paper_action": "PAPER_RISK_OFF_MODE" if risk_off_active else "PAPER_KEEP_CASH",
    })


def export_recommendations(recommendations: list) -> dict:
    return _with_header({
        "section": "recommendations",
        "schema_version": "199",
        "recommendations": recommendations,
        "count": len(recommendations),
    })


def export_full_risk_report(inp: dict, sizing_result: dict, no_entry_conditions: list) -> dict:
    sections = {
        "capital_profile": export_capital_profile(inp.get("capital_base", 300_000)),
        "risk_budget": export_risk_budget(inp.get("capital_base", 300_000)),
        "position_sizing_summary": export_position_sizing_summary(sizing_result),
        "entry_sizing_rules": export_entry_sizing_rules(),
        "stop_distance_analysis": export_stop_distance_analysis(inp.get("stop_distance_pct", 0.05)),
        "cash_buffer_status": export_cash_buffer_status(
            inp.get("current_cash_pct", 1.0),
            inp.get("market_risk_off", False),
        ),
        "exposure_limits": export_exposure_limits(
            inp.get("theme_exposures", {}),
            inp.get("industry_exposures", {}),
            inp.get("symbol_weights", {}),
            inp.get("high_correlation_cluster_weight", 0.0),
        ),
        "no_entry_conditions": export_no_entry_conditions(no_entry_conditions),
        "risk_off_status": export_risk_off_status(inp.get("market_risk_off", False)),
    }
    return _with_header({
        "section": "full_risk_report",
        "schema_version": "199",
        "sections": sections,
        "sections_count": len(sections),
        "report_sections_defined": list(REPORT_SECTIONS),
    })
