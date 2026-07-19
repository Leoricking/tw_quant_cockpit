"""
paper_trading/small_capital_strategy/portfolio_risk_report_engine_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Engine
[!] Paper Only. Research Only. Position Sizing Policy Only. Portfolio Risk Report Only.
[!] No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, List, Any, Optional
from .portfolio_risk_report_version_v199 import (
    VERSION, SCHEMA_VERSION, ENTRY_SIZE_MULTIPLIERS,
    HARD_BLOCK_CONDITIONS, FORBIDDEN_ACTIONS, PAPER_ACTIONS,
    CAPITAL_PROFILE_300K, RISK_GRADES, RECOMMENDATIONS,
)

GRADE_THRESHOLDS = {
    "LOW": (0.0, 0.2),
    "MODERATE": (0.2, 0.4),
    "ELEVATED": (0.4, 0.6),
    "HIGH": (0.6, 0.8),
    "CRITICAL": (0.8, 1.0),
}


def _blocked(reason: str) -> dict:
    return {
        "allowed": False,
        "blocked": True,
        "block_reason": reason,
        "paper_only": True,
        "no_real_orders": True,
        "production_trading_blocked": True,
        "sizing_executes_order": False,
    }


def _ok(**extra) -> dict:
    base = {
        "allowed": True,
        "blocked": False,
        "block_reason": "",
        "paper_only": True,
        "no_real_orders": True,
        "production_trading_blocked": True,
        "sizing_executes_order": False,
    }
    base.update(extra)
    return base


def validate_sizing_input(inp: dict) -> dict:
    if not inp:
        return _blocked("malformed_sizing_input: empty input")
    if not inp.get("paper_only", False):
        return _blocked("missing_paper_only_flags")
    if not inp.get("no_real_orders", False):
        return _blocked("missing_no_broker_flags")
    if not inp.get("not_investment_advice", False):
        return _blocked("missing_not_investment_advice_flags")
    if not inp.get("capital_base"):
        return _blocked("missing_capital_profile")
    entry_type = inp.get("entry_type", "")
    if not entry_type:
        return _blocked("missing_entry_type")
    stop_dist = inp.get("stop_distance_pct")
    if stop_dist is None:
        return _blocked("missing_stop_distance")
    if stop_dist <= 0:
        return _blocked("missing_stop_distance: stop_distance_pct must be > 0")
    for fa in FORBIDDEN_ACTIONS:
        if fa in str(inp):
            return _blocked(f"forbidden_action_words: {fa}")
    return _ok()


def compute_entry_size_multiplier(entry_type: str) -> float:
    return ENTRY_SIZE_MULTIPLIERS.get(entry_type, 0.0)


def compute_risk_grade(risk_score: float) -> str:
    if risk_score < 0 or risk_score > 1:
        return "INVALID"
    for grade, (lo, hi) in GRADE_THRESHOLDS.items():
        if lo <= risk_score < hi:
            return grade
    return "CRITICAL"


def compute_position_size(
    capital_base: float,
    risk_pct: float,
    stop_distance_pct: float,
    size_multiplier: float,
    risk_off: bool = False,
    capital_profile: Optional[dict] = None,
) -> dict:
    if capital_profile is None:
        capital_profile = CAPITAL_PROFILE_300K
    if risk_off:
        risk_pct = min(risk_pct, capital_profile.get("risk_off_single_trade_risk_pct_max", 0.005))
    max_loss = capital_base * risk_pct
    if stop_distance_pct <= 0:
        return _blocked("missing_stop_distance: stop_distance_pct <= 0")
    raw_size = max_loss / stop_distance_pct
    adjusted_size = raw_size * size_multiplier
    position_pct = adjusted_size / capital_base if capital_base > 0 else 0.0
    return _ok(
        raw_position_amount=round(raw_size, 2),
        adjusted_position_amount=round(adjusted_size, 2),
        position_pct_of_capital=round(position_pct, 4),
        max_loss_amount=round(max_loss, 2),
        risk_pct=risk_pct,
    )


def check_cash_buffer(
    current_cash_pct: float,
    min_cash_buffer_pct: float = 0.05,
    weak_market_cash_buffer_pct: float = 0.50,
    weak_market_mode: bool = False,
) -> dict:
    required = weak_market_cash_buffer_pct if weak_market_mode else min_cash_buffer_pct
    ok = current_cash_pct >= required
    return {
        "cash_buffer_ok": ok,
        "current_cash_pct": current_cash_pct,
        "required_cash_pct": required,
        "weak_market_mode": weak_market_mode,
        "block_new_entry": not ok,
        "paper_only": True,
    }


def check_theme_exposure(
    theme: str,
    theme_exposures: dict,
    max_theme_weight: float = 0.35,
) -> dict:
    current = theme_exposures.get(theme, 0.0)
    exceeded = current >= max_theme_weight
    return {
        "theme": theme,
        "current_weight": current,
        "max_weight": max_theme_weight,
        "limit_exceeded": exceeded,
        "block_new_entry": exceeded,
        "paper_only": True,
    }


def check_industry_exposure(
    industry: str,
    industry_exposures: dict,
    max_industry_weight: float = 0.40,
) -> dict:
    current = industry_exposures.get(industry, 0.0)
    exceeded = current >= max_industry_weight
    return {
        "industry": industry,
        "current_weight": current,
        "max_weight": max_industry_weight,
        "limit_exceeded": exceeded,
        "reduce_size": exceeded,
        "paper_only": True,
    }


def check_symbol_weight(
    symbol: str,
    symbol_weights: dict,
    max_symbol_weight: float = 0.20,
) -> dict:
    current = symbol_weights.get(symbol, 0.0)
    exceeded = current >= max_symbol_weight
    return {
        "symbol": symbol,
        "current_weight": current,
        "max_weight": max_symbol_weight,
        "limit_exceeded": exceeded,
        "block_new_entry": exceeded,
        "paper_only": True,
    }


def check_correlation_cluster(
    cluster_weight: float,
    max_cluster_weight: float = 0.45,
) -> dict:
    exceeded = cluster_weight >= max_cluster_weight
    return {
        "cluster_weight": cluster_weight,
        "max_cluster_weight": max_cluster_weight,
        "limit_exceeded": exceeded,
        "reduce_size": exceeded,
        "paper_only": True,
    }


def evaluate_no_entry_conditions(inp: dict) -> List[dict]:
    conditions = []
    risk_grade = inp.get("portfolio_risk_grade", "LOW")
    if risk_grade in ("CRITICAL", "HIGH"):
        conditions.append({
            "condition_name": "portfolio_risk_exceeded",
            "triggered": True,
            "reason": f"Portfolio risk grade is {risk_grade}",
            "paper_action": "PAPER_BLOCK_NEW_ENTRY",
        })
    cash_pct = inp.get("current_cash_pct", 1.0)
    market_risk_off = inp.get("market_risk_off", False)
    min_cash = CAPITAL_PROFILE_300K["min_cash_buffer_pct"]
    weak_cash = CAPITAL_PROFILE_300K["weak_market_cash_buffer_pct"]
    required_cash = weak_cash if market_risk_off else min_cash
    if cash_pct < required_cash:
        conditions.append({
            "condition_name": "cash_buffer_too_low",
            "triggered": True,
            "reason": f"Cash {cash_pct:.1%} < required {required_cash:.1%}",
            "paper_action": "PAPER_BLOCK_NEW_ENTRY",
        })
    stop_dist = inp.get("stop_distance_pct", 0.05)
    if stop_dist > 0.15:
        conditions.append({
            "condition_name": "stop_distance_too_wide",
            "triggered": True,
            "reason": f"Stop distance {stop_dist:.1%} exceeds 15%",
            "paper_action": "PAPER_REQUIRE_TIGHTER_STOP",
        })
    if market_risk_off:
        conditions.append({
            "condition_name": "market_risk_off_no_edge",
            "triggered": True,
            "reason": "Market risk-off mode active",
            "paper_action": "PAPER_RISK_OFF_MODE",
        })
    theme = inp.get("candidate_theme", "")
    theme_exposures = inp.get("theme_exposures", {})
    if theme and theme_exposures.get(theme, 0.0) >= CAPITAL_PROFILE_300K["max_single_theme_weight"]:
        conditions.append({
            "condition_name": "theme_exposure_exceeded",
            "triggered": True,
            "reason": f"Theme {theme} exposure exceeded",
            "paper_action": "PAPER_BLOCK_NEW_ENTRY",
        })
    return conditions


def compute_recommendation(inp: dict, no_entry_conditions: List[dict]) -> tuple:
    blocked_conditions = [c for c in no_entry_conditions if c.get("triggered")]
    if blocked_conditions:
        first = blocked_conditions[0]
        pa = first.get("paper_action", "PAPER_BLOCK_NEW_ENTRY")
        if pa == "PAPER_RISK_OFF_MODE":
            return "RISK_OFF_MODE", "PAPER_RISK_OFF_MODE"
        if pa == "PAPER_REQUIRE_TIGHTER_STOP":
            return "REQUIRE_TIGHTER_STOP", "PAPER_REQUIRE_HUMAN_REVIEW"
        return "BLOCK_NEW_ENTRY", "PAPER_BLOCK_NEW_ENTRY"
    risk_grade = inp.get("portfolio_risk_grade", "LOW")
    entry_type = inp.get("entry_type", "A_PULLBACK_10MA")
    multiplier = compute_entry_size_multiplier(entry_type)
    if risk_grade == "ELEVATED":
        return "ALLOW_REDUCED_SIZE", "PAPER_ALLOW_REDUCED_SIZE"
    if multiplier <= 0.3:
        return "TEST_POSITION_ONLY", "PAPER_TEST_POSITION_ONLY"
    if multiplier < 1.0:
        return "ALLOW_REDUCED_SIZE", "PAPER_ALLOW_REDUCED_SIZE"
    return "ALLOW_NORMAL_SIZE", "PAPER_ALLOW_NORMAL_SIZE"


def run_position_sizing_report(inp: dict) -> dict:
    validation = validate_sizing_input(inp)
    if not validation.get("allowed", False):
        return {
            "schema_version": SCHEMA_VERSION,
            "paper_only": True,
            "allowed": False,
            "recommendation": "BLOCK_NEW_ENTRY",
            "paper_action": "PAPER_BLOCK_NEW_ENTRY",
            "block_reasons": [validation.get("block_reason", "validation_failed")],
            "position_size_amount": 0.0,
            "max_loss_amount": 0.0,
            "not_investment_advice": True,
            "production_trading_blocked": True,
            "sizing_executes_order": False,
            "sizing_mutates_strategy": False,
        }
    capital_base = float(inp.get("capital_base", 300_000))
    entry_type = inp.get("entry_type", "A_PULLBACK_10MA")
    stop_dist = float(inp.get("stop_distance_pct", 0.05))
    risk_off = inp.get("market_risk_off", False)
    multiplier = compute_entry_size_multiplier(entry_type)
    risk_pct = CAPITAL_PROFILE_300K["normal_single_trade_risk_pct_max"]
    if risk_off:
        risk_pct = CAPITAL_PROFILE_300K["risk_off_single_trade_risk_pct_max"]
    no_entry = evaluate_no_entry_conditions(inp)
    recommendation, paper_action = compute_recommendation(inp, no_entry)
    block_reasons = [c["reason"] for c in no_entry if c.get("triggered")]
    if block_reasons:
        return {
            "schema_version": SCHEMA_VERSION,
            "paper_only": True,
            "allowed": False,
            "recommendation": recommendation,
            "paper_action": paper_action,
            "block_reasons": block_reasons,
            "position_size_amount": 0.0,
            "max_loss_amount": 0.0,
            "not_investment_advice": True,
            "production_trading_blocked": True,
            "sizing_executes_order": False,
            "sizing_mutates_strategy": False,
        }
    sizing = compute_position_size(capital_base, risk_pct, stop_dist, multiplier, risk_off)
    if recommendation == "ALLOW_REDUCED_SIZE":
        sizing["adjusted_position_amount"] = round(sizing.get("adjusted_position_amount", 0) * 0.7, 2)
    return {
        "schema_version": SCHEMA_VERSION,
        "paper_only": True,
        "allowed": True,
        "recommendation": recommendation,
        "paper_action": paper_action,
        "block_reasons": [],
        "position_size_amount": sizing.get("adjusted_position_amount", 0.0),
        "max_loss_amount": sizing.get("max_loss_amount", 0.0),
        "position_pct_of_capital": sizing.get("position_pct_of_capital", 0.0),
        "size_multiplier": multiplier,
        "risk_pct": risk_pct,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "sizing_executes_order": False,
        "sizing_mutates_strategy": False,
        "sizing_rebalances_real_portfolio": False,
    }
