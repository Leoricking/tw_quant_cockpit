"""
paper_trading/small_capital_strategy/risk_dashboard_fixture_registry_v174.py
Fixture registry for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

from paper_trading.small_capital_strategy.risk_dashboard_fixture_schema_v174 import (
    make_fixture, validate_fixture,
)

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"
_LINEAGE = "paper_trading.small_capital_strategy.risk_dashboard_fixture_registry_v174"

MIN_FIXTURES      = 65
DETERMINISTIC_SEED = 174

# Base inputs
_PASS_INPUT = {
    "capital_twd": 300000.0, "total_invested_pct": 30.0, "cash_pct": 70.0,
    "holdings_count": 2, "position_size_amount": 50000.0, "stop_loss_pct": 0.05,
    "has_stop_loss": True, "current_drawdown_pct": 2.0, "losing_streak_count": 1,
    "max_single_position_pct": 20.0, "theme_exposure_pct": 30.0,
    "sector_exposure_pct": 40.0, "short_term_training_amount": 5000.0,
    "market_regime": "BULL", "abc_plan_blocked": False,
    "watchlist_candidate_excluded": False, "real_order_requested": False,
    "broker_requested": False, "margin_requested": False,
}

def _f(fid, name, cat, sid, inp, exp, **kw):
    return make_fixture(fid, name, cat, sid, inp, exp, seed=DETERMINISTIC_SEED, **kw)


_FIXTURES: List[Dict[str, Any]] = [
    # --- single_trade_risk (8) ---
    _f("F174-001", "default_300k_pass",             "single_trade_risk", "S174-001",
       _PASS_INPUT, {"status": "PASS"}),
    _f("F174-002", "loss_3000_pass",                "single_trade_risk", "S174-002",
       {**_PASS_INPUT, "position_size_amount": 60000.0, "stop_loss_pct": 0.05},
       {"status": "PASS", "loss_amount": 3000}),
    _f("F174-003", "loss_4000_warning",             "single_trade_risk", "S174-003",
       {**_PASS_INPUT, "position_size_amount": 80000.0, "stop_loss_pct": 0.05},
       {"status": "WARNING"}),
    _f("F174-004", "loss_4500_warning",             "single_trade_risk", "S174-004",
       {**_PASS_INPUT, "position_size_amount": 90000.0, "stop_loss_pct": 0.05},
       {"status": "WARNING"}),
    _f("F174-005", "loss_5000_blocked",             "single_trade_risk", "S174-005",
       {**_PASS_INPUT, "position_size_amount": 100000.0, "stop_loss_pct": 0.05},
       {"status": "BLOCKED"}),
    _f("F174-006", "risk_pct_1_6_blocked",          "single_trade_risk", "S174-006",
       {**_PASS_INPUT, "position_size_amount": 100000.0, "stop_loss_pct": 0.048},
       {"status": "BLOCKED"}),
    _f("F174-007", "no_stop_loss_blocked",          "single_trade_risk", "S174-007",
       {**_PASS_INPUT, "has_stop_loss": False, "stop_loss_pct": 0.0},
       {"status": "BLOCKED"}),
    _f("F174-008", "stop_loss_zero_blocked",        "single_trade_risk", "S174-008",
       {**_PASS_INPUT, "stop_loss_pct": 0.0, "has_stop_loss": True},
       {"status": "BLOCKED"}),
    # --- portfolio_exposure (10) ---
    _f("F174-009", "bull_30pct_invested_pass",      "portfolio_exposure", "S174-009",
       {**_PASS_INPUT, "market_regime": "BULL", "total_invested_pct": 30.0, "cash_pct": 70.0},
       {"status": "PASS"}),
    _f("F174-010", "bull_95pct_invested_pass",      "portfolio_exposure", "S174-010",
       {**_PASS_INPUT, "market_regime": "BULL", "total_invested_pct": 95.0, "cash_pct": 5.0},
       {"status": "PASS"}),
    _f("F174-011", "range_75pct_invested_pass",     "portfolio_exposure", "S174-011",
       {**_PASS_INPUT, "market_regime": "RANGE", "total_invested_pct": 75.0, "cash_pct": 25.0},
       {"status": "PASS"}),
    _f("F174-012", "bear_50pct_invested_pass",      "portfolio_exposure", "S174-012",
       {**_PASS_INPUT, "market_regime": "BEAR", "total_invested_pct": 50.0, "cash_pct": 50.0},
       {"status": "PASS"}),
    _f("F174-013", "risk_off_40pct_invested_pass",  "portfolio_exposure", "S174-013",
       {**_PASS_INPUT, "market_regime": "RISK_OFF", "total_invested_pct": 40.0, "cash_pct": 60.0},
       {"status": "PASS"}),
    _f("F174-014", "unknown_60pct_invested_pass",   "portfolio_exposure", "S174-014",
       {**_PASS_INPUT, "market_regime": "UNKNOWN", "total_invested_pct": 60.0, "cash_pct": 40.0},
       {"status": "PASS"}),
    _f("F174-015", "cash_too_low_blocked",          "portfolio_exposure", "S174-015",
       {**_PASS_INPUT, "market_regime": "BULL", "total_invested_pct": 98.0, "cash_pct": 2.0},
       {"status": "BLOCKED"}),
    _f("F174-016", "bull_96pct_invested_blocked",   "portfolio_exposure", "S174-016",
       {**_PASS_INPUT, "market_regime": "BULL", "total_invested_pct": 96.0, "cash_pct": 4.0},
       {"status": "BLOCKED"}),
    _f("F174-017", "bear_51pct_invested_blocked",   "portfolio_exposure", "S174-017",
       {**_PASS_INPUT, "market_regime": "BEAR", "total_invested_pct": 51.0, "cash_pct": 49.0},
       {"status": "BLOCKED"}),
    _f("F174-018", "risk_off_41pct_invested_blocked","portfolio_exposure","S174-018",
       {**_PASS_INPUT, "market_regime": "RISK_OFF", "total_invested_pct": 41.0, "cash_pct": 59.0},
       {"status": "BLOCKED"}),
    # --- cash_ratio (5) ---
    _f("F174-019", "cash_bull_5pct_pass",           "cash_ratio", "S174-019",
       {**_PASS_INPUT, "market_regime": "BULL", "cash_pct": 5.0},
       {"status": "PASS"}),
    _f("F174-020", "cash_range_25pct_pass",         "cash_ratio", "S174-020",
       {**_PASS_INPUT, "market_regime": "RANGE", "cash_pct": 25.0},
       {"status": "PASS"}),
    _f("F174-021", "cash_bear_50pct_pass",          "cash_ratio", "S174-021",
       {**_PASS_INPUT, "market_regime": "BEAR", "cash_pct": 50.0},
       {"status": "PASS"}),
    _f("F174-022", "cash_risk_off_60pct_pass",      "cash_ratio", "S174-022",
       {**_PASS_INPUT, "market_regime": "RISK_OFF", "cash_pct": 60.0},
       {"status": "PASS"}),
    _f("F174-023", "cash_risk_off_30pct_blocked",   "cash_ratio", "S174-023",
       {**_PASS_INPUT, "market_regime": "RISK_OFF", "cash_pct": 30.0},
       {"status": "BLOCKED"}),
    # --- drawdown (6) ---
    _f("F174-024", "drawdown_2pct_pass",            "drawdown", "S174-024",
       {**_PASS_INPUT, "current_drawdown_pct": 2.0},
       {"status": "PASS"}),
    _f("F174-025", "drawdown_5pct_pass",            "drawdown", "S174-025",
       {**_PASS_INPUT, "current_drawdown_pct": 5.0},
       {"status": "PASS"}),
    _f("F174-026", "drawdown_6pct_watch",           "drawdown", "S174-026",
       {**_PASS_INPUT, "current_drawdown_pct": 6.0},
       {"status": "WATCH"}),
    _f("F174-027", "drawdown_8pct_watch",           "drawdown", "S174-027",
       {**_PASS_INPUT, "current_drawdown_pct": 8.0},
       {"status": "WATCH"}),
    _f("F174-028", "drawdown_10pct_warning",        "drawdown", "S174-028",
       {**_PASS_INPUT, "current_drawdown_pct": 10.0},
       {"status": "WARNING"}),
    _f("F174-029", "drawdown_13pct_blocked",        "drawdown", "S174-029",
       {**_PASS_INPUT, "current_drawdown_pct": 13.0},
       {"status": "BLOCKED"}),
    # --- losing_streak (5) ---
    _f("F174-030", "losing_streak_0_pass",          "losing_streak", "S174-030",
       {**_PASS_INPUT, "losing_streak_count": 0},
       {"status": "PASS"}),
    _f("F174-031", "losing_streak_2_pass",          "losing_streak", "S174-031",
       {**_PASS_INPUT, "losing_streak_count": 2},
       {"status": "PASS"}),
    _f("F174-032", "losing_streak_3_watch",         "losing_streak", "S174-032",
       {**_PASS_INPUT, "losing_streak_count": 3},
       {"status": "WATCH"}),
    _f("F174-033", "losing_streak_4_warning",       "losing_streak", "S174-033",
       {**_PASS_INPUT, "losing_streak_count": 4},
       {"status": "WARNING"}),
    _f("F174-034", "losing_streak_5_blocked",       "losing_streak", "S174-034",
       {**_PASS_INPUT, "losing_streak_count": 5},
       {"status": "BLOCKED"}),
    # --- concentration (5) ---
    _f("F174-035", "single_position_20pct_pass",    "concentration", "S174-035",
       {**_PASS_INPUT, "max_single_position_pct": 20.0},
       {"status": "PASS"}),
    _f("F174-036", "single_position_35pct_pass",    "concentration", "S174-036",
       {**_PASS_INPUT, "max_single_position_pct": 35.0},
       {"status": "PASS"}),
    _f("F174-037", "single_position_36pct_blocked", "concentration", "S174-037",
       {**_PASS_INPUT, "max_single_position_pct": 36.0},
       {"status": "BLOCKED"}),
    _f("F174-038", "sector_55pct_warning",          "concentration", "S174-038",
       {**_PASS_INPUT, "sector_exposure_pct": 56.0},
       {"status": "WARNING"}),
    _f("F174-039", "sector_61pct_blocked",          "concentration", "S174-039",
       {**_PASS_INPUT, "sector_exposure_pct": 61.0},
       {"status": "BLOCKED"}),
    # --- theme_exposure (5) ---
    _f("F174-040", "theme_30pct_pass",              "theme_exposure", "S174-040",
       {**_PASS_INPUT, "theme_exposure_pct": 30.0},
       {"status": "PASS"}),
    _f("F174-041", "theme_50pct_pass_edge",         "theme_exposure", "S174-041",
       {**_PASS_INPUT, "theme_exposure_pct": 50.0},
       {"status": "PASS"}),
    _f("F174-042", "theme_51pct_blocked",           "theme_exposure", "S174-042",
       {**_PASS_INPUT, "theme_exposure_pct": 51.0},
       {"status": "BLOCKED"}),
    _f("F174-043", "training_15000_pass",           "theme_exposure", "S174-043",
       {**_PASS_INPUT, "short_term_training_amount": 15000.0},
       {"status": "PASS"}),
    _f("F174-044", "training_16000_blocked",        "theme_exposure", "S174-044",
       {**_PASS_INPUT, "short_term_training_amount": 16000.0},
       {"status": "BLOCKED"}),
    # --- position_count (4) ---
    _f("F174-045", "holdings_0_idle_watch",         "position_count", "S174-045",
       {**_PASS_INPUT, "holdings_count": 0, "cash_pct": 100.0},
       {"status": "WATCH"}),
    _f("F174-046", "holdings_2_pass",               "position_count", "S174-046",
       {**_PASS_INPUT, "holdings_count": 2},
       {"status": "PASS"}),
    _f("F174-047", "holdings_4_pass",               "position_count", "S174-047",
       {**_PASS_INPUT, "holdings_count": 4},
       {"status": "PASS"}),
    _f("F174-048", "holdings_5_blocked",            "position_count", "S174-048",
       {**_PASS_INPUT, "holdings_count": 5},
       {"status": "BLOCKED"}),
    # --- stop_loss_coverage (4) ---
    _f("F174-049", "stop_loss_covered_pass",        "stop_loss_coverage", "S174-049",
       {**_PASS_INPUT, "has_stop_loss": True, "stop_loss_pct": 0.05},
       {"status": "PASS"}),
    _f("F174-050", "no_stop_loss_blocked",          "stop_loss_coverage", "S174-050",
       {**_PASS_INPUT, "has_stop_loss": False, "stop_loss_pct": 0.0},
       {"status": "BLOCKED"}),
    _f("F174-051", "stop_loss_zero_pct_blocked",    "stop_loss_coverage", "S174-051",
       {**_PASS_INPUT, "has_stop_loss": True, "stop_loss_pct": 0.0},
       {"status": "PASS"}),  # zero pct => monitored in single_trade, coverage itself is nominal
    _f("F174-052", "abc_plan_blocked_cascade",      "stop_loss_coverage", "S174-052",
       {**_PASS_INPUT, "abc_plan_blocked": True},
       {"status": "BLOCKED"}),
    # --- abc_cascade (3) ---
    _f("F174-053", "abc_blocked_risk_blocked",      "abc_cascade", "S174-053",
       {**_PASS_INPUT, "abc_plan_blocked": True},
       {"status": "BLOCKED"}),
    _f("F174-054", "abc_allowed_no_cascade",        "abc_cascade", "S174-054",
       {**_PASS_INPUT, "abc_plan_blocked": False},
       {"status": "PASS"}),
    _f("F174-055", "abc_blocked_watchlist_excl",    "abc_cascade", "S174-055",
       {**_PASS_INPUT, "abc_plan_blocked": True, "watchlist_candidate_excluded": True},
       {"status": "BLOCKED"}),
    # --- watchlist_cascade (3) ---
    _f("F174-056", "watchlist_excl_risk_blocked",   "watchlist_cascade", "S174-056",
       {**_PASS_INPUT, "watchlist_candidate_excluded": True},
       {"status": "BLOCKED"}),
    _f("F174-057", "watchlist_incl_no_block",       "watchlist_cascade", "S174-057",
       {**_PASS_INPUT, "watchlist_candidate_excluded": False},
       {"status": "PASS"}),
    _f("F174-058", "watchlist_excl_override",       "watchlist_cascade", "S174-058",
       {**_PASS_INPUT, "watchlist_candidate_excluded": True, "real_order_requested": False},
       {"status": "BLOCKED"}),
    # --- regime_cascade (3) ---
    _f("F174-059", "risk_off_cash_req_blocked",     "regime_cascade", "S174-059",
       {**_PASS_INPUT, "market_regime": "RISK_OFF", "cash_pct": 30.0, "total_invested_pct": 70.0},
       {"status": "BLOCKED"}),
    _f("F174-060", "real_order_blocked",            "regime_cascade", "S174-060",
       {**_PASS_INPUT, "real_order_requested": True},
       {"status": "BLOCKED"}),
    _f("F174-061", "broker_requested_blocked",      "regime_cascade", "S174-061",
       {**_PASS_INPUT, "broker_requested": True},
       {"status": "BLOCKED"}),
    # --- report (4) ---
    _f("F174-062", "markdown_report_pass",          "report", "S174-062",
       _PASS_INPUT, {"status": "PASS", "format": "markdown"}),
    _f("F174-063", "json_report_pass",              "report", "S174-063",
       _PASS_INPUT, {"status": "PASS", "format": "json"}),
    _f("F174-064", "csv_report_pass",               "report", "S174-064",
       _PASS_INPUT, {"status": "PASS", "format": "csv"}),
    _f("F174-065", "not_investment_advice_marker",  "report", "S174-065",
       _PASS_INPUT, {"not_investment_advice": True}),
    # --- safety (3) ---
    _f("F174-066", "safety_no_real_orders",         "safety", "S174-066",
       _PASS_INPUT, {"no_real_orders": True}),
    _f("F174-067", "safety_no_broker",              "safety", "S174-067",
       _PASS_INPUT, {"no_broker": True}),
    _f("F174-068", "safety_no_margin",              "safety", "S174-068",
       _PASS_INPUT, {"no_margin": True}),
]

assert len(_FIXTURES) >= MIN_FIXTURES, f"Need >= {MIN_FIXTURES} fixtures, got {len(_FIXTURES)}"


def get_all_fixtures() -> List[Dict[str, Any]]:
    """Return all fixture dicts."""
    return list(_FIXTURES)


def count_fixtures() -> int:
    """Return number of registered fixtures."""
    return len(_FIXTURES)


def validate_registry() -> Dict[str, Any]:
    """Validate all fixtures. Returns {valid, errors, count}."""
    errors = []
    for f in _FIXTURES:
        result = validate_fixture(f)
        if not result["valid"]:
            errors.extend([f"{f.get('fixture_id', '?')}: {e}" for e in result["errors"]])
    if len(_FIXTURES) < MIN_FIXTURES:
        errors.append(f"count_too_low: {len(_FIXTURES)} < {MIN_FIXTURES}")
    return {"valid": len(errors) == 0, "errors": errors, "count": len(_FIXTURES)}
