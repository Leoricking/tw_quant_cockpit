"""
paper_trading/small_capital_strategy/mistake_taxonomy_scenarios_v176.py
Test scenarios for Mistake Taxonomy & Weekly Review Dashboard v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SCHEMA  = "176"
_POLICY  = "1.7.6-mistake-taxonomy-weekly-review"


def _sc(
    sid: str,
    name: str,
    desc: str,
    category: str,
    severity: str,
    expected_level: str,
    cost_twd: float = 0.0,
    repeat_count: int = 1,
) -> Dict[str, Any]:
    return {
        "id": sid,
        "name": name,
        "description": desc,
        "mistake_category": category,
        "severity": severity,
        "expected_behavior_level": expected_level,
        "cost_twd": cost_twd,
        "repeat_count": repeat_count,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "schema_version": _SCHEMA,
        "policy_version": _POLICY,
    }


_SCENARIOS: List[Dict[str, Any]] = [
    # NO_STOP_LOSS (HIGH) — 5 scenarios
    _sc("SC176-001", "no_stop_loss_loss", "Entered trade without stop loss, hit large loss", "NO_STOP_LOSS", "HIGH", "WARNING", -8000.0),
    _sc("SC176-002", "no_stop_loss_win", "Entered without stop loss but price went up", "NO_STOP_LOSS", "HIGH", "WARNING", 0.0),
    _sc("SC176-003", "no_stop_loss_repeat_3", "Same week: 3 trades without stop loss", "NO_STOP_LOSS", "HIGH", "WARNING", -12000.0, 3),
    _sc("SC176-004", "no_stop_loss_repeat_5", "Same week: 5 trades without stop loss → BLOCKED", "NO_STOP_LOSS", "HIGH", "BLOCKED", -20000.0, 5),
    _sc("SC176-005", "no_stop_loss_partial", "Stop loss set partially after entry", "NO_STOP_LOSS", "HIGH", "WARNING", -5000.0),

    # MOVED_STOP_LOSS (HIGH) — 4 scenarios
    _sc("SC176-006", "moved_stop_loss_once", "Stop loss widened once after entry", "MOVED_STOP_LOSS", "HIGH", "WARNING", -6000.0),
    _sc("SC176-007", "moved_stop_loss_twice", "Stop loss widened twice, loss doubled", "MOVED_STOP_LOSS", "HIGH", "WARNING", -10000.0, 2),
    _sc("SC176-008", "moved_stop_loss_repeat_3", "Same week: moved stop loss 3 times", "MOVED_STOP_LOSS", "HIGH", "WARNING", -15000.0, 3),
    _sc("SC176-009", "moved_stop_loss_no_loss", "Moved stop loss but trade ended flat", "MOVED_STOP_LOSS", "HIGH", "WARNING", 0.0),

    # OVERSIZED_POSITION (HIGH) — 4 scenarios
    _sc("SC176-010", "oversized_bull", "Position >30% capital in BULL regime", "OVERSIZED_POSITION", "HIGH", "WARNING", -3000.0),
    _sc("SC176-011", "oversized_bear", "Position >50% capital in BEAR regime", "OVERSIZED_POSITION", "HIGH", "WARNING", -15000.0),
    _sc("SC176-012", "oversized_repeat_3", "3 oversized positions same week", "OVERSIZED_POSITION", "HIGH", "WARNING", -9000.0, 3),
    _sc("SC176-013", "oversized_win", "Oversized position but trade won", "OVERSIZED_POSITION", "HIGH", "WATCH", 5000.0),

    # IGNORE_MARKET_REGIME (CRITICAL) — 4 scenarios
    _sc("SC176-014", "regime_bear_entry", "Entered LONG in BEAR regime", "IGNORE_MARKET_REGIME", "CRITICAL", "WARNING", -9000.0),
    _sc("SC176-015", "regime_risk_off_heavy", "Heavy position in RISK_OFF regime", "IGNORE_MARKET_REGIME", "CRITICAL", "WARNING", -12000.0),
    _sc("SC176-016", "regime_mismatch_repeat", "2 regime mismatches same week", "IGNORE_MARKET_REGIME", "CRITICAL", "WARNING", -18000.0, 2),
    _sc("SC176-017", "regime_ok_bull", "Trade in BULL regime — correct", "NONE", "INFO", "PASS", 2000.0),

    # REVENGE_TRADE (CRITICAL) — 4 scenarios
    _sc("SC176-018", "revenge_after_loss", "Revenge trade entered within 1h of loss", "REVENGE_TRADE", "CRITICAL", "WARNING", -7000.0),
    _sc("SC176-019", "revenge_cascading", "Three revenge trades in sequence", "REVENGE_TRADE", "CRITICAL", "WARNING", -21000.0, 3),
    _sc("SC176-020", "revenge_repeat_5", "Five revenge trades same week → BLOCKED", "REVENGE_TRADE", "CRITICAL", "BLOCKED", -35000.0, 5),
    _sc("SC176-021", "revenge_caught_early", "Recognized revenge impulse and cancelled trade", "NONE", "INFO", "PASS", 0.0),

    # FOMO_CHASE (MEDIUM) — 4 scenarios
    _sc("SC176-022", "fomo_chase_breakout", "Chased extended breakout, bought high", "FOMO_CHASE", "MEDIUM", "WATCH", -4000.0),
    _sc("SC176-023", "fomo_news_spike", "Bought on news spike without setup", "FOMO_CHASE", "MEDIUM", "WATCH", -3000.0),
    _sc("SC176-024", "fomo_repeat_3", "3 FOMO chases same week", "FOMO_CHASE", "MEDIUM", "WARNING", -9000.0, 3),
    _sc("SC176-025", "fomo_avoided", "Resisted FOMO, waited for setup", "NONE", "INFO", "PASS", 0.0),

    # MARGIN_OR_LEVERAGE_ATTEMPT (BLOCKING) — 3 scenarios
    _sc("SC176-026", "margin_attempt", "Attempted to use margin", "MARGIN_OR_LEVERAGE_ATTEMPT", "BLOCKING", "BLOCKED", 0.0),
    _sc("SC176-027", "leverage_attempt", "Attempted to use 2x leverage", "MARGIN_OR_LEVERAGE_ATTEMPT", "BLOCKING", "BLOCKED", 0.0),
    _sc("SC176-028", "leverage_blocked", "System blocked leverage attempt correctly", "MARGIN_OR_LEVERAGE_ATTEMPT", "BLOCKING", "BLOCKED", 0.0),

    # BROKER_OR_REAL_ORDER_ATTEMPT (BLOCKING) — 3 scenarios
    _sc("SC176-029", "real_order_attempt", "Attempted real broker order — blocked", "BROKER_OR_REAL_ORDER_ATTEMPT", "BLOCKING", "BLOCKED", 0.0),
    _sc("SC176-030", "broker_api_attempt", "Attempted broker API call — blocked", "BROKER_OR_REAL_ORDER_ATTEMPT", "BLOCKING", "BLOCKED", 0.0),
    _sc("SC176-031", "real_account_attempt", "Attempted to access real account — blocked", "BROKER_OR_REAL_ORDER_ATTEMPT", "BLOCKING", "BLOCKED", 0.0),

    # HOLD_LOSER_TOO_LONG (HIGH) — 4 scenarios
    _sc("SC176-032", "hold_loser_week", "Held losing position for 1 week past stop", "HOLD_LOSER_TOO_LONG", "HIGH", "WARNING", -10000.0),
    _sc("SC176-033", "hold_loser_doubled", "Doubled down on losing position", "HOLD_LOSER_TOO_LONG", "HIGH", "WARNING", -16000.0),
    _sc("SC176-034", "hold_loser_repeat_3", "3 instances of holding losers too long", "HOLD_LOSER_TOO_LONG", "HIGH", "WARNING", -24000.0, 3),
    _sc("SC176-035", "stop_honored", "Stop loss honored, loss cut promptly", "NONE", "INFO", "PASS", -2000.0),

    # IGNORE_ABC_PLAN (HIGH) — 3 scenarios
    _sc("SC176-036", "no_abc_entry", "Entry did not match any ABC pattern", "IGNORE_ABC_PLAN", "HIGH", "WARNING", -5000.0),
    _sc("SC176-037", "abc_plan_ignored_twice", "Ignored ABC plan twice same week", "IGNORE_ABC_PLAN", "HIGH", "WARNING", -8000.0, 2),
    _sc("SC176-038", "abc_plan_followed", "Followed B_BREAKOUT plan correctly", "NONE", "INFO", "PASS", 3000.0),

    # OVERTRADING (MEDIUM) — 3 scenarios
    _sc("SC176-039", "overtrading_5_trades", "5 trades in one week", "OVERTRADING", "MEDIUM", "WATCH", -2000.0, 5),
    _sc("SC176-040", "overtrading_8_trades", "8 trades in one week", "OVERTRADING", "MEDIUM", "WARNING", -6000.0, 8),
    _sc("SC176-041", "disciplined_1_trade", "Only 1 trade this week, well-planned", "NONE", "INFO", "PASS", 2000.0),

    # EARLY_ENTRY (LOW) — 3 scenarios
    _sc("SC176-042", "early_entry_a_not_complete", "Entered before A-pullback completed", "EARLY_ENTRY", "LOW", "WATCH", -2000.0),
    _sc("SC176-043", "early_entry_base_not_formed", "Entered before base consolidation complete", "EARLY_ENTRY", "LOW", "WATCH", -1500.0),
    _sc("SC176-044", "patient_wait_for_setup", "Waited for full setup confirmation", "NONE", "INFO", "PASS", 1000.0),

    # LATE_ENTRY (LOW) — 3 scenarios
    _sc("SC176-045", "late_entry_extended", "Entered 10% above proper buy point", "LATE_ENTRY", "LOW", "WATCH", -3000.0),
    _sc("SC176-046", "late_entry_pullback_missed", "Missed pullback, entered on extension", "LATE_ENTRY", "LOW", "WATCH", -2000.0),
    _sc("SC176-047", "timely_entry", "Entry at correct buy point within 5% of pivot", "NONE", "INFO", "PASS", 2500.0),

    # TAKE_PROFIT_TOO_EARLY (LOW) — 3 scenarios
    _sc("SC176-048", "exit_too_early_10pct", "Sold at 10% gain, stock went to 30%", "TAKE_PROFIT_TOO_EARLY", "LOW", "WATCH", 1000.0),
    _sc("SC176-049", "exit_too_early_fear", "Exited on fear of pullback, no real trigger", "TAKE_PROFIT_TOO_EARLY", "LOW", "WATCH", 500.0),
    _sc("SC176-050", "target_held_correctly", "Held to 20% target as planned", "NONE", "INFO", "PASS", 10000.0),

    # IGNORE_WATCHLIST_RANK (MEDIUM) — 3 scenarios
    _sc("SC176-051", "off_watchlist_entry", "Traded symbol not in watchlist", "IGNORE_WATCHLIST_RANK", "MEDIUM", "WATCH", -3000.0),
    _sc("SC176-052", "tier3_entry", "Traded Tier-3 watchlist symbol against plan", "IGNORE_WATCHLIST_RANK", "MEDIUM", "WATCH", -1500.0),
    _sc("SC176-053", "tier1_entry_correct", "Traded Tier-1 watchlist symbol correctly", "NONE", "INFO", "PASS", 3000.0),

    # NEWS_CHASE (MEDIUM) — 2 scenarios
    _sc("SC176-054", "news_chase_earnings", "Bought on earnings surprise without setup", "NEWS_CHASE", "MEDIUM", "WATCH", -4000.0),
    _sc("SC176-055", "news_ignored_technical", "Ignored news, focused on technical setup", "NONE", "INFO", "PASS", 2000.0),

    # EARNINGS_RISK_IGNORED (HIGH) — 2 scenarios
    _sc("SC176-056", "held_through_earnings", "Held position through earnings report", "EARNINGS_RISK_IGNORED", "HIGH", "WARNING", -8000.0),
    _sc("SC176-057", "earnings_closed_before", "Closed position day before earnings correctly", "NONE", "INFO", "PASS", 500.0),

    # Weekly review scenario — clean week
    _sc("SC176-058", "clean_week_no_mistakes", "Full week with no mistakes, 2 profitable trades", "NONE", "INFO", "PASS", 8000.0),

    # Weekly review scenario — mixed week
    _sc("SC176-059", "mixed_week_2_mistakes", "Week with 1 HIGH and 1 LOW mistake", "NO_STOP_LOSS", "HIGH", "WARNING", -5000.0),

    # Monthly rollup — improving trend
    _sc("SC176-060", "monthly_improving_trend", "Month shows declining mistake count week over week", "NONE", "INFO", "PASS", 5000.0),

    # Monthly rollup — deteriorating trend
    _sc("SC176-061", "monthly_deteriorating_trend", "Month shows increasing mistake severity each week", "REVENGE_TRADE", "CRITICAL", "BLOCKED", -30000.0, 5),

    # Behavior score boundary conditions
    _sc("SC176-062", "score_boundary_watch", "Behavior score exactly at WATCH threshold (20)", "FOMO_CHASE", "MEDIUM", "WATCH", -1000.0),
    _sc("SC176-063", "score_boundary_warning", "Behavior score exactly at WARNING threshold (50)", "NO_STOP_LOSS", "HIGH", "WARNING", -5000.0, 2),
    _sc("SC176-064", "score_boundary_blocked_repeat", "BLOCKED via 5 repeats of same HIGH mistake", "MOVED_STOP_LOSS", "HIGH", "BLOCKED", -20000.0, 5),
]


def get_scenarios() -> List[Dict[str, Any]]:
    """Return all v1.7.6 scenarios."""
    return list(_SCENARIOS)


def count_scenarios() -> int:
    """Return total scenario count."""
    return len(_SCENARIOS)


def get_scenario_by_id(scenario_id: str) -> Dict[str, Any]:
    """Return scenario by ID or empty dict."""
    for s in _SCENARIOS:
        if s["id"] == scenario_id:
            return s
    return {}
