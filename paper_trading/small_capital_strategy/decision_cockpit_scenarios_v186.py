"""
paper_trading/small_capital_strategy/decision_cockpit_scenarios_v186.py
75 Decision Cockpit scenarios for End-to-End Small Capital Decision Cockpit v1.8.6.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Decision Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Dict, Any

_SAFETY_META = {
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "decision_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
}

_SCENARIOS: List[Dict[str, Any]] = [
    # ── Strong market scenarios (10) ────────────────────────────────────────
    {"id": "DC186-001", "category": "strong_market_a_buy_point",
     "description": "Strong BULL market + A_10MA_PULLBACK buy point ready → PAPER_ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "DC186-002", "category": "strong_market_b_breakout",
     "description": "Strong BULL market + B_BREAKOUT with volume surge → PAPER_ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "DC186-003", "category": "strong_market_c_reclaim",
     "description": "Strong BULL market + C_20MA_RECLAIM with KD turning → PAPER_PLAN_READY", **_SAFETY_META},
    {"id": "DC186-004", "category": "strong_market_multi_candidate",
     "description": "BULL market 3 candidates all A buy point → READY grade", **_SAFETY_META},
    {"id": "DC186-005", "category": "strong_market_300k",
     "description": "300K BULL A buy point, 1 holding, entry readiness high → READY", **_SAFETY_META},
    {"id": "DC186-006", "category": "strong_market_500k",
     "description": "500K BULL B breakout, 2 holdings, entry allowed → READY", **_SAFETY_META},
    {"id": "DC186-007", "category": "strong_market_1m",
     "description": "1M BULL C reclaim, 3 holdings diversified → WATCH", **_SAFETY_META},
    {"id": "DC186-008", "category": "strong_market_3m",
     "description": "3M BULL A buy point, 5 holdings, max positions not reached → READY", **_SAFETY_META},
    {"id": "DC186-009", "category": "strong_market_weekly_review",
     "description": "BULL weekly review all candidates healthy → PAPER_PLAN_READY weekly", **_SAFETY_META},
    {"id": "DC186-010", "category": "strong_market_pre_market",
     "description": "BULL pre-market review, A candidate confirmed → PAPER_PLAN_READY", **_SAFETY_META},

    # ── Weak market scenarios (10) ──────────────────────────────────────────
    {"id": "DC186-011", "category": "weak_market_a_buy_blocked",
     "description": "Weak BEAR market + A buy point → BLOCKED (regime blocked)", **_SAFETY_META},
    {"id": "DC186-012", "category": "weak_market_breakout_blocked",
     "description": "BEAR market + B breakout signal → BLOCKED (no trade allowed)", **_SAFETY_META},
    {"id": "DC186-013", "category": "weak_market_c_reclaim_blocked",
     "description": "BEAR market + C reclaim → BLOCKED (regime blocked)", **_SAFETY_META},
    {"id": "DC186-014", "category": "weak_market_risk_off",
     "description": "RISK_OFF regime → all candidates BLOCKED", **_SAFETY_META},
    {"id": "DC186-015", "category": "weak_market_neutral",
     "description": "NEUTRAL market, A buy point, reduced exposure → WAIT", **_SAFETY_META},
    {"id": "DC186-016", "category": "weak_market_sideways",
     "description": "SIDEWAYS market, no clear setup → WAIT", **_SAFETY_META},
    {"id": "DC186-017", "category": "weak_market_watchlist_only",
     "description": "BEAR market, daily watchlist review only → BLOCKED grade", **_SAFETY_META},
    {"id": "DC186-018", "category": "weak_market_portfolio_review",
     "description": "BEAR market, portfolio review required → REDUCE_RISK", **_SAFETY_META},
    {"id": "DC186-019", "category": "weak_market_post_market",
     "description": "Weak market post-market review, no new entries → NO_TRADE", **_SAFETY_META},
    {"id": "DC186-020", "category": "weak_market_blocked_market_review",
     "description": "Blocked market review, all actions BLOCKED → BLOCKED grade", **_SAFETY_META},

    # ── Risk scenarios (10) ─────────────────────────────────────────────────
    {"id": "DC186-021", "category": "high_concentration_risk",
     "description": "High concentration risk (score>70) → REDUCE_RISK", **_SAFETY_META},
    {"id": "DC186-022", "category": "high_ruin_risk",
     "description": "Monte Carlo ruin > 20% → BLOCKED, add not allowed", **_SAFETY_META},
    {"id": "DC186-023", "category": "low_cash_reserve",
     "description": "Cash < 5% → BLOCKED entry and add", **_SAFETY_META},
    {"id": "DC186-024", "category": "overexposed_portfolio",
     "description": "Total exposure > 95% → BLOCKED (hard limit)", **_SAFETY_META},
    {"id": "DC186-025", "category": "no_stop_loss",
     "description": "Candidate missing stop loss → BLOCKED (hard rule)", **_SAFETY_META},
    {"id": "DC186-026", "category": "high_margin_risk",
     "description": "Margin balance risk > 70% → BLOCKED candidate", **_SAFETY_META},
    {"id": "DC186-027", "category": "theme_overcrowded",
     "description": "3+ candidates same theme → concentration BLOCKED for same-theme entry", **_SAFETY_META},
    {"id": "DC186-028", "category": "drawdown_budget_exceeded",
     "description": "Drawdown budget 100% used → BLOCKED", **_SAFETY_META},
    {"id": "DC186-029", "category": "behavior_risk_blocked",
     "description": "Behavior risk flag → BLOCKED (discipline rule)", **_SAFETY_META},
    {"id": "DC186-030", "category": "high_ruin_no_add",
     "description": "MC ruin 12% → entry allowed but add NOT allowed", **_SAFETY_META},

    # ── Portfolio state scenarios (10) ──────────────────────────────────────
    {"id": "DC186-031", "category": "reduce_risk_required",
     "description": "Exposure 80%, ruin 8% → REDUCE_RISK grade", **_SAFETY_META},
    {"id": "DC186-032", "category": "wait_only",
     "description": "No clear buy point, neutral regime, 0 candidates → WAIT", **_SAFETY_META},
    {"id": "DC186-033", "category": "no_trade_day",
     "description": "All candidates failed criteria → NO_TRADE daily", **_SAFETY_META},
    {"id": "DC186-034", "category": "weekly_review_reduce_exposure",
     "description": "Weekly review, total exposure 75% → reduce to target", **_SAFETY_META},
    {"id": "DC186-035", "category": "daily_watchlist_only",
     "description": "Daily watchlist review only, no entry signal → OBSERVE", **_SAFETY_META},
    {"id": "DC186-036", "category": "portfolio_rebalance_required",
     "description": "Portfolio drift > 10%, rebalance needed → REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "DC186-037", "category": "candidate_replacement_required",
     "description": "2 holdings below 20MA, replacement candidates → REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "DC186-038", "category": "all_candidates_blocked",
     "description": "All candidates blocked (regime, risk, etc.) → BLOCKED grade", **_SAFETY_META},
    {"id": "DC186-039", "category": "partial_candidates_ready",
     "description": "2 of 5 candidates ready, 3 blocked → WATCH grade", **_SAFETY_META},
    {"id": "DC186-040", "category": "empty_watchlist",
     "description": "No candidates, BULL market, clean portfolio → WAIT grade", **_SAFETY_META},

    # ── A buy point detailed scenarios (5) ─────────────────────────────────
    {"id": "DC186-041", "category": "a_buy_point_300k",
     "description": "A_10MA_PULLBACK: above 10MA, volume contracting, KD<50, BULL → PAPER_ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "DC186-042", "category": "a_buy_point_kd_above_50",
     "description": "A buy: above 10MA, volume contracting, KD>50 → PAPER_PLAN_READY", **_SAFETY_META},
    {"id": "DC186-043", "category": "a_buy_point_below_10ma",
     "description": "A buy: below 10MA → WAIT (condition not met)", **_SAFETY_META},
    {"id": "DC186-044", "category": "a_buy_point_kd_recovering",
     "description": "A buy: above 10MA, volume contracting, KD recovering → PAPER_ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "DC186-045", "category": "a_buy_point_regime_neutral",
     "description": "A buy: conditions met, NEUTRAL regime → PAPER_PLAN_READY", **_SAFETY_META},

    # ── B breakout detailed scenarios (5) ───────────────────────────────────
    {"id": "DC186-046", "category": "b_breakout_volume_surge",
     "description": "B_BREAKOUT: volume breakout True, above 10MA, above 20MA → PAPER_ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "DC186-047", "category": "b_breakout_no_volume",
     "description": "B breakout: no volume breakout → REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "DC186-048", "category": "b_breakout_regime_blocked",
     "description": "B breakout: BULL volume surge but regime BLOCKED → BLOCKED", **_SAFETY_META},
    {"id": "DC186-049", "category": "b_breakout_institutional_ok",
     "description": "B breakout: institutional flow positive, volume surge → PAPER_ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "DC186-050", "category": "b_breakout_no_stop_loss",
     "description": "B breakout: conditions met but no stop loss → BLOCKED", **_SAFETY_META},

    # ── C reclaim detailed scenarios (5) ────────────────────────────────────
    {"id": "DC186-051", "category": "c_reclaim_above_20ma",
     "description": "C_20MA_RECLAIM: above 20MA, volume contracting, KD recovering → PAPER_ENTRY_ALLOWED", **_SAFETY_META},
    {"id": "DC186-052", "category": "c_reclaim_below_20ma",
     "description": "C reclaim: below 20MA → WAIT (not reclaimed)", **_SAFETY_META},
    {"id": "DC186-053", "category": "c_reclaim_institutional_neg_3plus",
     "description": "C reclaim: above 20MA but institutional consecutive neg 3d → WAIT", **_SAFETY_META},
    {"id": "DC186-054", "category": "c_reclaim_kd_not_recovering",
     "description": "C reclaim: above 20MA, no KD recovery → PAPER_PLAN_READY", **_SAFETY_META},
    {"id": "DC186-055", "category": "c_reclaim_multi_criteria",
     "description": "C reclaim: all criteria met including institutional ok → PAPER_ENTRY_ALLOWED", **_SAFETY_META},

    # ── Multi-cycle scenarios (5) ────────────────────────────────────────────
    {"id": "DC186-056", "category": "pre_market_review_300k",
     "description": "Pre-market review: check regime, watchlist, candidates → action determined", **_SAFETY_META},
    {"id": "DC186-057", "category": "post_market_review",
     "description": "Post-market review: portfolio update, risk check → OBSERVE or REDUCE", **_SAFETY_META},
    {"id": "DC186-058", "category": "risk_review_cycle",
     "description": "Risk review: exposure 65%, ruin 8% → REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "DC186-059", "category": "portfolio_review_cycle",
     "description": "Portfolio review: rebalance drift 15% → REVIEW_REQUIRED", **_SAFETY_META},
    {"id": "DC186-060", "category": "weekly_review_300k",
     "description": "Weekly review 300K: portfolio health, regime, candidates → weekly grade", **_SAFETY_META},

    # ── Capital stage scenarios (5) ─────────────────────────────────────────
    {"id": "DC186-061", "category": "capital_300k_entry",
     "description": "300K stage: max 3 positions, A buy ready → READY", **_SAFETY_META},
    {"id": "DC186-062", "category": "capital_500k_entry",
     "description": "500K stage: max 4 positions, B breakout ready → READY", **_SAFETY_META},
    {"id": "DC186-063", "category": "capital_1m_entry",
     "description": "1M stage: max 5 positions, C reclaim ready → WATCH", **_SAFETY_META},
    {"id": "DC186-064", "category": "capital_3m_entry",
     "description": "3M stage: max 6 positions, multiple A buy points → READY", **_SAFETY_META},
    {"id": "DC186-065", "category": "capital_300k_blocked",
     "description": "300K stage: BLOCKED regime → BLOCKED regardless of capital", **_SAFETY_META},

    # ── Edge/safety scenarios (10) ──────────────────────────────────────────
    {"id": "DC186-066", "category": "empty_input_default",
     "description": "Default empty cockpit input → WAIT grade (no candidates)", **_SAFETY_META},
    {"id": "DC186-067", "category": "all_safety_flags_true",
     "description": "All safety flags verified → paper_only, decision_only, no_real_orders", **_SAFETY_META},
    {"id": "DC186-068", "category": "forbidden_words_not_in_output",
     "description": "No BUY/SELL/ORDER in any output action", **_SAFETY_META},
    {"id": "DC186-069", "category": "grade_is_valid",
     "description": "All cockpit grades are from valid grade set", **_SAFETY_META},
    {"id": "DC186-070", "category": "action_is_valid",
     "description": "All output actions are from allowed action set", **_SAFETY_META},
    {"id": "DC186-071", "category": "backward_compat_v170",
     "description": "Backward compat with v1.7.0 small capital strategy", **_SAFETY_META},
    {"id": "DC186-072", "category": "backward_compat_v185",
     "description": "Backward compat with v1.8.5 portfolio construction", **_SAFETY_META},
    {"id": "DC186-073", "category": "decision_report_paper_only",
     "description": "Decision report always has paper_only=True", **_SAFETY_META},
    {"id": "DC186-074", "category": "decision_dashboard_no_broker",
     "description": "Decision dashboard always has no_broker=True", **_SAFETY_META},
    {"id": "DC186-075", "category": "decision_cockpit_deterministic",
     "description": "Same input always produces same cockpit grade (deterministic)", **_SAFETY_META},
]


def count_scenarios() -> int:
    """Return number of scenarios."""
    return len(_SCENARIOS)


def get_scenarios() -> list:
    """Return all scenario dicts."""
    return list(_SCENARIOS)


def get_scenario_by_id(scenario_id: str) -> dict:
    """Return scenario by id, or empty dict."""
    for s in _SCENARIOS:
        if s["id"] == scenario_id:
            return dict(s)
    return {}


def get_scenarios_by_category(category: str) -> list:
    """Return scenarios matching category."""
    return [dict(s) for s in _SCENARIOS if s["category"] == category]
