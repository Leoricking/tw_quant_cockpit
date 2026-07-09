"""
paper_trading/small_capital_strategy/risk_dashboard_scenario_registry_v174.py
Scenario registry for Small Account Risk Dashboard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "174"
_POLICY  = "1.7.4-small-account-risk-dashboard"
_LINEAGE = "paper_trading.small_capital_strategy.risk_dashboard_scenario_registry_v174"

MIN_SCENARIOS      = 65
DETERMINISTIC_SEED = 174

SCENARIO_CATEGORIES = [
    "single_trade_risk",
    "portfolio_exposure",
    "cash_ratio",
    "drawdown",
    "losing_streak",
    "concentration",
    "theme_exposure",
    "position_count",
    "stop_loss_coverage",
    "abc_cascade",
    "watchlist_cascade",
    "regime_cascade",
    "scorecard",
    "report",
    "safety",
]


def _s(sid, name, cat, fid, exp_status, exp_regime="BULL"):
    return {
        "scenario_id": sid,
        "name": name,
        "category": cat,
        "fixture_id": fid,
        "expected_status": exp_status,
        "expected_regime": exp_regime,
        "deterministic_seed": DETERMINISTIC_SEED,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
        "paper_only": True,
        "no_real_orders": True,
    }


_SCENARIOS: List[Dict[str, Any]] = [
    # --- single_trade_risk (8) ---
    _s("S174-001", "default_300k_pass",                    "single_trade_risk",  "F174-001", "PASS"),
    _s("S174-002", "single_trade_loss_3000_pass",          "single_trade_risk",  "F174-002", "PASS"),
    _s("S174-003", "single_trade_loss_4000_warning",       "single_trade_risk",  "F174-003", "WARNING"),
    _s("S174-004", "single_trade_loss_4500_warning",       "single_trade_risk",  "F174-004", "WARNING"),
    _s("S174-005", "single_trade_loss_5000_blocked",       "single_trade_risk",  "F174-005", "BLOCKED"),
    _s("S174-006", "risk_pct_above_1_5_blocked",           "single_trade_risk",  "F174-006", "BLOCKED"),
    _s("S174-007", "no_stop_loss_blocked",                 "single_trade_risk",  "F174-007", "BLOCKED"),
    _s("S174-008", "stop_loss_pct_zero_blocked",           "single_trade_risk",  "F174-008", "BLOCKED"),
    # --- portfolio_exposure (10) ---
    _s("S174-009", "bull_exposure_30_pass",                "portfolio_exposure", "F174-009", "PASS", "BULL"),
    _s("S174-010", "bull_exposure_95_pass",                "portfolio_exposure", "F174-010", "PASS", "BULL"),
    _s("S174-011", "range_exposure_75_pass",               "portfolio_exposure", "F174-011", "PASS", "RANGE"),
    _s("S174-012", "bear_exposure_50_pass",                "portfolio_exposure", "F174-012", "PASS", "BEAR"),
    _s("S174-013", "risk_off_exposure_40_pass",            "portfolio_exposure", "F174-013", "PASS", "RISK_OFF"),
    _s("S174-014", "unknown_exposure_60_pass",             "portfolio_exposure", "F174-014", "PASS", "UNKNOWN"),
    _s("S174-015", "cash_too_low_blocked",                 "portfolio_exposure", "F174-015", "BLOCKED"),
    _s("S174-016", "bull_over_invested_blocked",           "portfolio_exposure", "F174-016", "BLOCKED", "BULL"),
    _s("S174-017", "bear_over_invested_blocked",           "portfolio_exposure", "F174-017", "BLOCKED", "BEAR"),
    _s("S174-018", "risk_off_over_invested_blocked",       "portfolio_exposure", "F174-018", "BLOCKED", "RISK_OFF"),
    # --- cash_ratio (5) ---
    _s("S174-019", "cash_bull_5pct_pass",                  "cash_ratio",         "F174-019", "PASS", "BULL"),
    _s("S174-020", "cash_range_25pct_pass",                "cash_ratio",         "F174-020", "PASS", "RANGE"),
    _s("S174-021", "cash_bear_50pct_pass",                 "cash_ratio",         "F174-021", "PASS", "BEAR"),
    _s("S174-022", "cash_risk_off_60pct_pass",             "cash_ratio",         "F174-022", "PASS", "RISK_OFF"),
    _s("S174-023", "cash_too_low_for_regime_blocked",      "cash_ratio",         "F174-023", "BLOCKED"),
    # --- drawdown (6) ---
    _s("S174-024", "drawdown_2pct_pass",                   "drawdown",           "F174-024", "PASS"),
    _s("S174-025", "drawdown_5pct_pass",                   "drawdown",           "F174-025", "PASS"),
    _s("S174-026", "drawdown_6pct_watch",                  "drawdown",           "F174-026", "WATCH"),
    _s("S174-027", "drawdown_8pct_watch",                  "drawdown",           "F174-027", "WATCH"),
    _s("S174-028", "drawdown_10pct_warning",               "drawdown",           "F174-028", "WARNING"),
    _s("S174-029", "drawdown_13pct_blocked",               "drawdown",           "F174-029", "BLOCKED"),
    # --- losing_streak (5) ---
    _s("S174-030", "losing_streak_0_pass",                 "losing_streak",      "F174-030", "PASS"),
    _s("S174-031", "losing_streak_2_pass",                 "losing_streak",      "F174-031", "PASS"),
    _s("S174-032", "losing_streak_3_watch",                "losing_streak",      "F174-032", "WATCH"),
    _s("S174-033", "losing_streak_4_warning",              "losing_streak",      "F174-033", "WARNING"),
    _s("S174-034", "losing_streak_5_blocked",              "losing_streak",      "F174-034", "BLOCKED"),
    # --- concentration (5) ---
    _s("S174-035", "single_position_20pct_pass",           "concentration",      "F174-035", "PASS"),
    _s("S174-036", "single_position_35pct_pass",           "concentration",      "F174-036", "PASS"),
    _s("S174-037", "single_position_36pct_blocked",        "concentration",      "F174-037", "BLOCKED"),
    _s("S174-038", "sector_55pct_warning",                 "concentration",      "F174-038", "WARNING"),
    _s("S174-039", "sector_61pct_blocked",                 "concentration",      "F174-039", "BLOCKED"),
    # --- theme_exposure (5) ---
    _s("S174-040", "theme_30pct_pass",                     "theme_exposure",     "F174-040", "PASS"),
    _s("S174-041", "theme_50pct_pass_edge",                "theme_exposure",     "F174-041", "PASS"),
    _s("S174-042", "theme_51pct_blocked",                  "theme_exposure",     "F174-042", "BLOCKED"),
    _s("S174-043", "training_15000_pass",                  "theme_exposure",     "F174-043", "PASS"),
    _s("S174-044", "training_cap_exceeded_blocked",        "theme_exposure",     "F174-044", "BLOCKED"),
    # --- position_count (4) ---
    _s("S174-045", "holdings_0_idle_watch",                "position_count",     "F174-045", "WATCH"),
    _s("S174-046", "holdings_2_pass",                      "position_count",     "F174-046", "PASS"),
    _s("S174-047", "holdings_4_pass",                      "position_count",     "F174-047", "PASS"),
    _s("S174-048", "holdings_5_blocked",                   "position_count",     "F174-048", "BLOCKED"),
    # --- stop_loss_coverage (4) ---
    _s("S174-049", "stop_loss_covered_pass",               "stop_loss_coverage", "F174-049", "PASS"),
    _s("S174-050", "stop_loss_missing_blocked",            "stop_loss_coverage", "F174-050", "BLOCKED"),
    _s("S174-051", "stop_loss_pct_zero_blocked",           "stop_loss_coverage", "F174-051", "BLOCKED"),
    _s("S174-052", "abc_plan_no_stop_blocked",             "stop_loss_coverage", "F174-052", "BLOCKED"),
    # --- abc_cascade (3) ---
    _s("S174-053", "abc_blocked_cascades_risk_blocked",    "abc_cascade",        "F174-053", "BLOCKED"),
    _s("S174-054", "abc_allowed_no_cascade",               "abc_cascade",        "F174-054", "PASS"),
    _s("S174-055", "abc_blocked_watchlist_excluded",       "abc_cascade",        "F174-055", "BLOCKED"),
    # --- watchlist_cascade (3) ---
    _s("S174-056", "watchlist_excluded_risk_blocked",      "watchlist_cascade",  "F174-056", "BLOCKED"),
    _s("S174-057", "watchlist_included_no_block",          "watchlist_cascade",  "F174-057", "PASS"),
    _s("S174-058", "watchlist_excluded_override",          "watchlist_cascade",  "F174-058", "BLOCKED"),
    # --- regime_cascade (3) ---
    _s("S174-059", "risk_off_increases_cash_req",          "regime_cascade",     "F174-059", "BLOCKED", "RISK_OFF"),
    _s("S174-060", "real_order_blocked",                   "regime_cascade",     "F174-060", "BLOCKED"),
    _s("S174-061", "broker_requested_blocked",             "regime_cascade",     "F174-061", "BLOCKED"),
    # --- report (4) ---
    _s("S174-062", "markdown_report_pass",                 "report",             "F174-062", "PASS"),
    _s("S174-063", "json_report_pass",                     "report",             "F174-063", "PASS"),
    _s("S174-064", "csv_report_pass",                      "report",             "F174-064", "PASS"),
    _s("S174-065", "not_investment_advice_marker",         "report",             "F174-065", "PASS"),
    # --- safety (3) ---
    _s("S174-066", "safety_no_real_orders",                "safety",             "F174-066", "PASS"),
    _s("S174-067", "safety_no_broker",                     "safety",             "F174-067", "PASS"),
    _s("S174-068", "safety_no_margin",                     "safety",             "F174-068", "PASS"),
]

assert len(_SCENARIOS) >= MIN_SCENARIOS, f"Need >= {MIN_SCENARIOS} scenarios, got {len(_SCENARIOS)}"


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Return all scenario dicts."""
    return list(_SCENARIOS)


def count_scenarios() -> int:
    """Return number of registered scenarios."""
    return len(_SCENARIOS)


def validate_registry() -> Dict[str, Any]:
    """Validate all scenarios. Returns {valid, errors, count}."""
    errors = []
    required = ["scenario_id", "name", "category", "fixture_id",
                "expected_status", "paper_only", "no_real_orders"]
    for s in _SCENARIOS:
        for f in required:
            if f not in s:
                errors.append(f"{s.get('scenario_id', '?')}: missing_{f}")
        if not s.get("paper_only"):
            errors.append(f"{s.get('scenario_id', '?')}: paper_only_false")
    if len(_SCENARIOS) < MIN_SCENARIOS:
        errors.append(f"count_too_low: {len(_SCENARIOS)} < {MIN_SCENARIOS}")
    return {"valid": len(errors) == 0, "errors": errors, "count": len(_SCENARIOS)}


def get_scenarios_by_category(category: str) -> List[Dict[str, Any]]:
    """Return scenarios filtered by category."""
    return [s for s in _SCENARIOS if s.get("category") == category]
