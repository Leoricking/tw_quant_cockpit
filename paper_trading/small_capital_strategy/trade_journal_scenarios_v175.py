"""
paper_trading/small_capital_strategy/trade_journal_scenarios_v175.py
Scenarios for Small Account Trade Journal v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

_SCHEMA  = "175"
_POLICY  = "1.7.5-small-account-trade-journal"

MIN_SCENARIOS = 55


def _sc(sid, name, desc, regime, abc, outcome, eq, xq, mistakes):
    return {
        "id":                 sid,
        "name":               name,
        "description":        desc,
        "regime":             regime,
        "abc_pattern":        abc,
        "outcome":            outcome,
        "entry_quality":      eq,
        "exit_quality":       xq,
        "mistake_categories": mistakes,
        "paper_only":         True,
        "research_only":      True,
        "no_real_orders":     True,
        "no_broker":          True,
        "not_investment_advice": True,
        "demo_only":          True,
        "not_for_production": True,
        "schema_version":     _SCHEMA,
        "policy_version":     _POLICY,
    }


SCENARIOS: List[Dict[str, Any]] = [
    # --- Entry Quality Scenarios (10) ---
    _sc("SC175-001", "ideal_entry_bull_b_breakout",
        "Perfect entry: BULL regime, B breakout pattern, tier-1 watchlist, stop loss set.",
        "BULL", "B_BREAKOUT", "WIN", "IDEAL", "IDEAL", ["NONE"]),
    _sc("SC175-002", "acceptable_entry_range_c_reclaim",
        "Acceptable entry: RANGE regime, C-reclaim, tier-2 watchlist.",
        "RANGE", "C_RECLAIM", "WIN", "ACCEPTABLE", "TOO_EARLY", ["NONE"]),
    _sc("SC175-003", "marginal_entry_bull_a_pullback",
        "Marginal entry: BULL, A pullback, not on watchlist.",
        "BULL", "A_PULLBACK", "WIN", "MARGINAL", "IDEAL", ["WATCHLIST_MISS"]),
    _sc("SC175-004", "poor_entry_bear_fomo",
        "Poor entry: BEAR regime, FOMO, no stop loss.",
        "BEAR", "UNKNOWN", "LOSS", "POOR", "PANIC", ["FOMO", "NO_STOP_LOSS", "REGIME_MISMATCH"]),
    _sc("SC175-005", "entry_no_stop_loss",
        "Entry with no stop loss set — critical risk violation.",
        "BULL", "B_BREAKOUT", "LOSS", "POOR", "PANIC", ["NO_STOP_LOSS"]),
    _sc("SC175-006", "entry_oversize_position",
        "Entry with oversized position > 30% capital.",
        "BULL", "B_BREAKOUT", "LOSS", "POOR", "TOO_LATE", ["OVERSIZE"]),
    _sc("SC175-007", "entry_regime_mismatch",
        "Entry during RISK_OFF regime — regime mismatch violation.",
        "RISK_OFF", "UNKNOWN", "LOSS", "POOR", "PANIC", ["REGIME_MISMATCH"]),
    _sc("SC175-008", "entry_chased_breakout",
        "Entry after chasing an extended breakout.",
        "BULL", "B_BREAKOUT", "LOSS", "MARGINAL", "TOO_LATE", ["CHASED_BREAKOUT"]),
    _sc("SC175-009", "entry_tier1_watchlist_ideal",
        "Entry from tier-1 watchlist with full ABC confirmation.",
        "BULL", "C_RECLAIM", "WIN", "IDEAL", "IDEAL", ["NONE"]),
    _sc("SC175-010", "entry_no_trigger",
        "Entry without clear ABC trigger — FOMO trade.",
        "RANGE", "UNKNOWN", "LOSS", "POOR", "PANIC", ["FOMO"]),

    # --- Exit Quality Scenarios (10) ---
    _sc("SC175-011", "ideal_exit_target_reached",
        "Exit at 10%+ target gain — ideal exit timing.",
        "BULL", "B_BREAKOUT", "WIN", "IDEAL", "IDEAL", ["NONE"]),
    _sc("SC175-012", "exit_too_early",
        "Exit too early at 3% gain before target.",
        "BULL", "C_RECLAIM", "WIN", "ACCEPTABLE", "TOO_EARLY", ["EARLY_EXIT"]),
    _sc("SC175-013", "exit_too_late_held_loser",
        "Held losing position too long, exit at -15%.",
        "BEAR", "UNKNOWN", "LOSS", "POOR", "TOO_LATE", ["HELD_LOSER", "REGIME_MISMATCH"]),
    _sc("SC175-014", "exit_stop_triggered",
        "Stop loss triggered at -5% — disciplined exit.",
        "BULL", "A_PULLBACK", "LOSS", "ACCEPTABLE", "IDEAL", ["NONE"]),
    _sc("SC175-015", "exit_panic_no_stop",
        "Panic exit at -12%, no stop loss was set.",
        "BEAR", "UNKNOWN", "LOSS", "POOR", "PANIC", ["NO_STOP_LOSS", "HELD_LOSER"]),
    _sc("SC175-016", "exit_breakeven",
        "Exit at breakeven — neutral outcome.",
        "RANGE", "B_BREAKOUT", "BREAKEVEN", "MARGINAL", "TOO_EARLY", ["EARLY_EXIT"]),
    _sc("SC175-017", "exit_partial_profit",
        "Partial exit at +5%, held remainder.",
        "BULL", "C_RECLAIM", "WIN", "IDEAL", "TOO_EARLY", ["NONE"]),
    _sc("SC175-018", "exit_after_regime_change",
        "Exit after market shifted to BEAR regime.",
        "BEAR", "B_BREAKOUT", "LOSS", "MARGINAL", "TOO_LATE", ["REGIME_MISMATCH"]),
    _sc("SC175-019", "exit_revenge_reentry",
        "Exited at loss, re-entered immediately — revenge trade.",
        "BULL", "UNKNOWN", "LOSS", "POOR", "PANIC", ["REVENGE"]),
    _sc("SC175-020", "exit_ideal_b_breakout",
        "Perfect exit after B-breakout confirmation target.",
        "BULL", "B_BREAKOUT", "WIN", "IDEAL", "IDEAL", ["NONE"]),

    # --- ABC Execution Scenarios (8) ---
    _sc("SC175-021", "abc_c_reclaim_full_execution",
        "Full C-reclaim execution: A valid, B clean, C confirmed, position sized correctly.",
        "BULL", "C_RECLAIM", "WIN", "IDEAL", "IDEAL", ["NONE"]),
    _sc("SC175-022", "abc_b_breakout_only",
        "B-breakout without C-reclaim confirmation.",
        "BULL", "B_BREAKOUT", "WIN", "ACCEPTABLE", "TOO_EARLY", ["NONE"]),
    _sc("SC175-023", "abc_a_pullback_oversized",
        "A-pullback entry with oversized position.",
        "BULL", "A_PULLBACK", "LOSS", "POOR", "PANIC", ["OVERSIZE"]),
    _sc("SC175-024", "abc_no_pattern_fomo",
        "No ABC pattern — pure FOMO entry.",
        "BULL", "UNKNOWN", "LOSS", "POOR", "PANIC", ["FOMO"]),
    _sc("SC175-025", "abc_pattern_regime_mismatch",
        "ABC pattern valid but regime is RISK_OFF.",
        "RISK_OFF", "B_BREAKOUT", "LOSS", "MARGINAL", "PANIC", ["REGIME_MISMATCH"]),
    _sc("SC175-026", "abc_c_reclaim_no_stop",
        "C-reclaim entry without stop loss.",
        "BULL", "C_RECLAIM", "LOSS", "MARGINAL", "PANIC", ["NO_STOP_LOSS"]),
    _sc("SC175-027", "abc_b_breakout_watchlist_miss",
        "B-breakout but symbol not on watchlist.",
        "BULL", "B_BREAKOUT", "WIN", "MARGINAL", "IDEAL", ["WATCHLIST_MISS"]),
    _sc("SC175-028", "abc_full_compliance",
        "All ABC checks pass: A, B, C, sized correctly, tier-1 watchlist.",
        "BULL", "C_RECLAIM", "WIN", "IDEAL", "IDEAL", ["NONE"]),

    # --- Watchlist Conversion Scenarios (6) ---
    _sc("SC175-029", "watchlist_tier1_converted",
        "Tier-1 watchlist candidate successfully converted to trade.",
        "BULL", "C_RECLAIM", "WIN", "IDEAL", "IDEAL", ["NONE"]),
    _sc("SC175-030", "watchlist_tier2_converted",
        "Tier-2 watchlist candidate converted to trade.",
        "RANGE", "B_BREAKOUT", "WIN", "ACCEPTABLE", "TOO_EARLY", ["NONE"]),
    _sc("SC175-031", "watchlist_tier1_excluded",
        "Tier-1 candidate excluded due to regime being RISK_OFF.",
        "RISK_OFF", "UNKNOWN", "OPEN", "UNKNOWN", "UNKNOWN", ["NONE"]),
    _sc("SC175-032", "watchlist_miss_not_on_list",
        "Trade taken on symbol not in watchlist — watchlist miss.",
        "BULL", "UNKNOWN", "LOSS", "POOR", "PANIC", ["WATCHLIST_MISS"]),
    _sc("SC175-033", "watchlist_high_conversion_rate",
        "Portfolio with 70%+ watchlist-to-trade conversion rate.",
        "BULL", "C_RECLAIM", "WIN", "IDEAL", "IDEAL", ["NONE"]),
    _sc("SC175-034", "watchlist_low_conversion_rate",
        "Portfolio with <30% conversion rate — watchlist quality low.",
        "RANGE", "UNKNOWN", "LOSS", "POOR", "TOO_LATE", ["FOMO", "WATCHLIST_MISS"]),

    # --- Risk Violation Scenarios (7) ---
    _sc("SC175-035", "risk_no_violation_compliant",
        "Fully compliant trade: no violations.",
        "BULL", "B_BREAKOUT", "WIN", "IDEAL", "IDEAL", ["NONE"]),
    _sc("SC175-036", "risk_oversize_violation",
        "Position size exceeds 30% of capital.",
        "BULL", "B_BREAKOUT", "LOSS", "POOR", "PANIC", ["OVERSIZE"]),
    _sc("SC175-037", "risk_no_stop_loss_violation",
        "Trade entered without stop loss — critical violation.",
        "BULL", "C_RECLAIM", "LOSS", "POOR", "PANIC", ["NO_STOP_LOSS"]),
    _sc("SC175-038", "risk_regime_mismatch_violation",
        "Trade during BEAR regime — regime mismatch.",
        "BEAR", "UNKNOWN", "LOSS", "POOR", "PANIC", ["REGIME_MISMATCH"]),
    _sc("SC175-039", "risk_multiple_violations",
        "Multiple violations: oversize + no stop loss + regime mismatch.",
        "RISK_OFF", "UNKNOWN", "LOSS", "POOR", "PANIC",
        ["OVERSIZE", "NO_STOP_LOSS", "REGIME_MISMATCH"]),
    _sc("SC175-040", "risk_abc_plan_violated",
        "ABC execution plan ignored — entered without B or C confirmation.",
        "BULL", "UNKNOWN", "LOSS", "POOR", "PANIC", ["FOMO"]),
    _sc("SC175-041", "risk_compliant_loss",
        "Risk-compliant trade that resulted in a loss — stop triggered.",
        "BULL", "A_PULLBACK", "LOSS", "ACCEPTABLE", "IDEAL", ["NONE"]),

    # --- Regime Outcome Scenarios (6) ---
    _sc("SC175-042", "regime_bull_high_win_rate",
        "BULL regime with 65% win rate across multiple trades.",
        "BULL", "B_BREAKOUT", "WIN", "IDEAL", "IDEAL", ["NONE"]),
    _sc("SC175-043", "regime_range_moderate_win_rate",
        "RANGE regime with 50% win rate.",
        "RANGE", "C_RECLAIM", "WIN", "ACCEPTABLE", "TOO_EARLY", ["NONE"]),
    _sc("SC175-044", "regime_bear_low_win_rate",
        "BEAR regime with 20% win rate — trades should be avoided.",
        "BEAR", "UNKNOWN", "LOSS", "POOR", "PANIC", ["REGIME_MISMATCH"]),
    _sc("SC175-045", "regime_risk_off_no_trades",
        "RISK_OFF regime — no trades should be taken.",
        "RISK_OFF", "UNKNOWN", "OPEN", "UNKNOWN", "UNKNOWN", ["NONE"]),
    _sc("SC175-046", "regime_bull_to_bear_transition",
        "Trade entered in BULL that transitioned to BEAR.",
        "BEAR", "B_BREAKOUT", "LOSS", "MARGINAL", "TOO_LATE", ["REGIME_MISMATCH"]),
    _sc("SC175-047", "regime_unknown_cautious",
        "UNKNOWN regime — cautious position sizing.",
        "UNKNOWN", "A_PULLBACK", "WIN", "MARGINAL", "IDEAL", ["NONE"]),

    # --- Mistake Taxonomy Scenarios (8) ---
    _sc("SC175-048", "mistake_none_compliant",
        "No mistakes — fully compliant trade.",
        "BULL", "C_RECLAIM", "WIN", "IDEAL", "IDEAL", ["NONE"]),
    _sc("SC175-049", "mistake_fomo_entry",
        "FOMO entry without trigger confirmation.",
        "BULL", "UNKNOWN", "LOSS", "POOR", "PANIC", ["FOMO"]),
    _sc("SC175-050", "mistake_revenge_trade",
        "Revenge trade after previous loss.",
        "BULL", "UNKNOWN", "LOSS", "POOR", "PANIC", ["REVENGE"]),
    _sc("SC175-051", "mistake_oversize_fomo",
        "Both FOMO and oversize in same trade.",
        "BULL", "UNKNOWN", "LOSS", "POOR", "PANIC", ["FOMO", "OVERSIZE"]),
    _sc("SC175-052", "mistake_held_loser",
        "Held losing position instead of cutting at stop.",
        "BEAR", "UNKNOWN", "LOSS", "POOR", "TOO_LATE", ["HELD_LOSER", "REGIME_MISMATCH"]),
    _sc("SC175-053", "mistake_early_exit",
        "Exited too early at 3% instead of holding to target.",
        "BULL", "B_BREAKOUT", "WIN", "IDEAL", "TOO_EARLY", ["EARLY_EXIT"]),
    _sc("SC175-054", "mistake_watchlist_miss_win",
        "Won despite watchlist miss — lucky outcome.",
        "BULL", "B_BREAKOUT", "WIN", "MARGINAL", "IDEAL", ["WATCHLIST_MISS"]),
    _sc("SC175-055", "mistake_all_categories",
        "Trade with multiple mistake categories — worst case.",
        "RISK_OFF", "UNKNOWN", "LOSS", "POOR", "PANIC",
        ["FOMO", "REVENGE", "OVERSIZE", "NO_STOP_LOSS", "REGIME_MISMATCH"]),
]


def get_scenarios() -> List[Dict[str, Any]]:
    """Return all scenarios."""
    return list(SCENARIOS)


def get_scenario_by_id(sid: str) -> Optional[Dict[str, Any]]:
    """Return scenario by id, or None."""
    for s in SCENARIOS:
        if s["id"] == sid:
            return s
    return None


def count_scenarios() -> int:
    """Return total number of scenarios."""
    return len(SCENARIOS)
