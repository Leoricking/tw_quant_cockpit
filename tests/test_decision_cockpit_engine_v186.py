"""
tests/test_decision_cockpit_engine_v186.py
Tests for decision_cockpit_engine_v186 module.
[!] Research Only. Paper Only. Decision Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_cockpit_engine_v186 import (
    ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_COCKPIT_GRADES,
    CAPITAL_STAGES, DECISION_CYCLES, ABC_BUY_POINTS,
    CANDIDATE_EVALUATION_CRITERIA, BLOCKED_REGIMES,
    validate_action, validate_grade, run_decision_cockpit,
    build_decision_dashboard, get_engine_info,
    run_regime_decision, run_risk_decision, run_monte_carlo_decision,
    run_portfolio_decision, run_theme_decision, run_buy_point_decision,
    run_candidate_decision, run_position_sizing_decision,
)
from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import (
    DecisionCockpitInput, CandidateDecisionInput,
)


# ── ALLOWED_OUTPUT_ACTIONS ───────────────────────────────────────────────────
def test_allowed_actions_count():
    assert len(ALLOWED_OUTPUT_ACTIONS) == 17

def test_allowed_action_decision_only():
    assert "DECISION_ONLY" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_action_observe():
    assert "OBSERVE" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_action_wait():
    assert "WAIT" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_action_paper_plan_ready():
    assert "PAPER_PLAN_READY" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_action_paper_entry_allowed():
    assert "PAPER_ENTRY_ALLOWED" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_action_paper_add_allowed():
    assert "PAPER_ADD_ALLOWED" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_action_reduce_risk():
    assert "REDUCE_RISK" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_action_blocked():
    assert "BLOCKED" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_action_no_trade():
    assert "NO_TRADE" in ALLOWED_OUTPUT_ACTIONS

def test_allowed_action_research_only():
    assert "RESEARCH_ONLY" in ALLOWED_OUTPUT_ACTIONS

# ── FORBIDDEN_OUTPUT_WORDS ───────────────────────────────────────────────────
def test_forbidden_words_count():
    assert len(FORBIDDEN_OUTPUT_WORDS) == 9

def test_forbidden_buy():
    assert "BUY" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_sell():
    assert "SELL" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_order():
    assert "ORDER" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_execute():
    assert "EXECUTE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_submit_order():
    assert "SUBMIT_ORDER" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_auto_trade():
    assert "AUTO_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_real_trade():
    assert "REAL_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_live_trade():
    assert "LIVE_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_broker_order():
    assert "BROKER_ORDER" in FORBIDDEN_OUTPUT_WORDS

# ── VALID_COCKPIT_GRADES ─────────────────────────────────────────────────────
def test_valid_grades_count():
    assert len(VALID_COCKPIT_GRADES) == 6

def test_grade_ready():
    assert "READY" in VALID_COCKPIT_GRADES

def test_grade_watch():
    assert "WATCH" in VALID_COCKPIT_GRADES

def test_grade_wait():
    assert "WAIT" in VALID_COCKPIT_GRADES

def test_grade_reduce_risk():
    assert "REDUCE_RISK" in VALID_COCKPIT_GRADES

def test_grade_blocked():
    assert "BLOCKED" in VALID_COCKPIT_GRADES

def test_grade_review_required():
    assert "REVIEW_REQUIRED" in VALID_COCKPIT_GRADES

# ── CAPITAL_STAGES ───────────────────────────────────────────────────────────
def test_capital_stages_count():
    assert len(CAPITAL_STAGES) == 4

def test_capital_stage_300k():
    assert 300000 in CAPITAL_STAGES

def test_capital_stage_500k():
    assert 500000 in CAPITAL_STAGES

def test_capital_stage_1m():
    assert 1000000 in CAPITAL_STAGES

def test_capital_stage_3m():
    assert 3000000 in CAPITAL_STAGES

# ── DECISION_CYCLES ──────────────────────────────────────────────────────────
def test_decision_cycles_count():
    assert len(DECISION_CYCLES) == 8

def test_cycle_daily_check():
    assert "daily_check" in DECISION_CYCLES

def test_cycle_weekly_review():
    assert "weekly_review" in DECISION_CYCLES

def test_cycle_pre_market():
    assert "pre_market_review" in DECISION_CYCLES

def test_cycle_post_market():
    assert "post_market_review" in DECISION_CYCLES

def test_cycle_watchlist_review():
    assert "watchlist_review" in DECISION_CYCLES

def test_cycle_portfolio_review():
    assert "portfolio_review" in DECISION_CYCLES

def test_cycle_risk_review():
    assert "risk_review" in DECISION_CYCLES

def test_cycle_blocked_market():
    assert "blocked_market_review" in DECISION_CYCLES

# ── ABC_BUY_POINTS ───────────────────────────────────────────────────────────
def test_abc_buy_points_count():
    assert len(ABC_BUY_POINTS) == 3

def test_abc_a_10ma():
    assert "A_10MA_PULLBACK" in ABC_BUY_POINTS

def test_abc_b_breakout():
    assert "B_BREAKOUT" in ABC_BUY_POINTS

def test_abc_c_20ma():
    assert "C_20MA_RECLAIM" in ABC_BUY_POINTS

# ── CANDIDATE_EVALUATION_CRITERIA ────────────────────────────────────────────
def test_criteria_count():
    assert len(CANDIDATE_EVALUATION_CRITERIA) == 14

def test_criteria_theme_strength():
    assert "theme_strength" in CANDIDATE_EVALUATION_CRITERIA

def test_criteria_final_action():
    assert "final_decision_action" in CANDIDATE_EVALUATION_CRITERIA

# ── validate_action ───────────────────────────────────────────────────────────
def test_validate_action_decision_only():
    assert validate_action("DECISION_ONLY") is True

def test_validate_action_blocked():
    assert validate_action("BLOCKED") is True

def test_validate_action_buy_false():
    assert validate_action("BUY") is False

def test_validate_action_sell_false():
    assert validate_action("SELL") is False

# ── validate_grade ────────────────────────────────────────────────────────────
def test_validate_grade_ready():
    assert validate_grade("READY") is True

def test_validate_grade_blocked():
    assert validate_grade("BLOCKED") is True

def test_validate_grade_invalid():
    assert validate_grade("OVEREXPOSED") is False

# ── run_regime_decision ───────────────────────────────────────────────────────
def test_regime_bull_not_blocked():
    inp = DecisionCockpitInput(market_regime="BULL")
    result = run_regime_decision(inp)
    assert result.regime_blocked is False

def test_regime_blocked():
    inp = DecisionCockpitInput(market_regime="BLOCKED")
    result = run_regime_decision(inp)
    assert result.regime_blocked is True
    assert result.action == "BLOCKED"

def test_regime_bear_blocked():
    inp = DecisionCockpitInput(market_regime="BEAR")
    result = run_regime_decision(inp)
    assert result.regime_blocked is True

def test_regime_risk_off_blocked():
    inp = DecisionCockpitInput(market_regime="RISK_OFF")
    result = run_regime_decision(inp)
    assert result.regime_blocked is True

def test_regime_bull_entry_permitted():
    inp = DecisionCockpitInput(market_regime="BULL")
    result = run_regime_decision(inp)
    assert result.entry_permitted is True

# ── run_monte_carlo_decision ──────────────────────────────────────────────────
def test_mc_low_ruin():
    result = run_monte_carlo_decision(2.0)
    assert result.ruin_risk_level == "LOW"
    assert result.entry_allowed is True
    assert result.add_allowed is True

def test_mc_medium_ruin():
    result = run_monte_carlo_decision(12.0)
    assert result.entry_allowed is True
    assert result.add_allowed is False

def test_mc_high_ruin_blocked():
    result = run_monte_carlo_decision(25.0)
    assert result.ruin_risk_level == "HIGH"
    assert result.entry_allowed is False
    assert "monte_carlo_ruin_probability_too_high" in result.block_reasons

# ── run_buy_point_decision ────────────────────────────────────────────────────
def test_buy_point_a_entry_allowed():
    c = CandidateDecisionInput(ticker="A", abc_buy_point="A_10MA_PULLBACK",
                                above_10ma=True, volume_contracting=True,
                                kd_below_50=True, market_regime="BULL",
                                stop_loss_defined=True)
    result = run_buy_point_decision(c)
    assert result.action in ("PAPER_ENTRY_ALLOWED", "PAPER_PLAN_READY")

def test_buy_point_a_blocked_regime():
    c = CandidateDecisionInput(ticker="A", abc_buy_point="A_10MA_PULLBACK",
                                above_10ma=True, market_regime="BLOCKED",
                                stop_loss_defined=True)
    result = run_buy_point_decision(c)
    assert result.action == "BLOCKED"

def test_buy_point_a_below_10ma():
    c = CandidateDecisionInput(ticker="A", abc_buy_point="A_10MA_PULLBACK",
                                above_10ma=False, market_regime="BULL",
                                stop_loss_defined=True)
    result = run_buy_point_decision(c)
    assert result.condition_met is False

def test_buy_point_b_breakout():
    c = CandidateDecisionInput(ticker="B", abc_buy_point="B_BREAKOUT",
                                above_10ma=True, above_20ma=True,
                                volume_breakout=True, market_regime="BULL",
                                stop_loss_defined=True)
    result = run_buy_point_decision(c)
    assert result.action in ("PAPER_ENTRY_ALLOWED", "PAPER_PLAN_READY")

def test_buy_point_b_no_volume():
    c = CandidateDecisionInput(ticker="B", abc_buy_point="B_BREAKOUT",
                                above_10ma=True, volume_breakout=False,
                                market_regime="BULL", stop_loss_defined=True)
    result = run_buy_point_decision(c)
    assert result.condition_met is False

def test_buy_point_no_stop_loss():
    c = CandidateDecisionInput(ticker="A", abc_buy_point="A_10MA_PULLBACK",
                                above_10ma=True, market_regime="BULL",
                                stop_loss_defined=False)
    result = run_buy_point_decision(c)
    assert "missing_stop_loss" in result.block_reasons

def test_buy_point_c_reclaim():
    c = CandidateDecisionInput(ticker="C", abc_buy_point="C_20MA_RECLAIM",
                                above_20ma=True, volume_contracting=True,
                                kd_recovering=True, market_regime="BULL",
                                stop_loss_defined=True)
    result = run_buy_point_decision(c)
    assert result.action in ("PAPER_ENTRY_ALLOWED", "PAPER_PLAN_READY", "WAIT")

# ── run_candidate_decision ────────────────────────────────────────────────────
def test_candidate_blocked_regime():
    c = CandidateDecisionInput(ticker="X", market_regime="BLOCKED")
    result = run_candidate_decision(c)
    assert result.final_action == "BLOCKED"
    assert "market_regime_blocked" in result.block_reasons

def test_candidate_no_stop_loss_blocked():
    c = CandidateDecisionInput(ticker="X", market_regime="BULL",
                                stop_loss_defined=False)
    result = run_candidate_decision(c)
    assert "missing_stop_loss" in result.block_reasons

def test_candidate_high_margin_risk():
    c = CandidateDecisionInput(ticker="X", market_regime="BULL",
                                margin_balance_risk=80.0, stop_loss_defined=True)
    result = run_candidate_decision(c)
    assert "high_margin_risk" in result.block_reasons

# ── run_decision_cockpit ──────────────────────────────────────────────────────
def test_cockpit_empty_input_wait():
    inp = DecisionCockpitInput(capital=300000.0, market_regime="BULL")
    result = run_decision_cockpit(inp)
    assert result.final_cockpit_grade in ("WAIT", "WATCH", "READY")

def test_cockpit_regime_blocked():
    inp = DecisionCockpitInput(capital=300000.0, market_regime="BLOCKED")
    result = run_decision_cockpit(inp)
    assert result.final_cockpit_grade == "BLOCKED"
    assert "market_regime_blocked" in result.block_reasons

def test_cockpit_high_ruin_blocked():
    inp = DecisionCockpitInput(capital=300000.0, market_regime="BULL",
                                monte_carlo_ruin_risk_pct=25.0)
    result = run_decision_cockpit(inp)
    assert result.final_cockpit_grade == "BLOCKED"

def test_cockpit_low_cash_blocked():
    inp = DecisionCockpitInput(capital=300000.0, market_regime="BULL",
                                cash_reserve_pct=3.0)
    result = run_decision_cockpit(inp)
    assert result.final_cockpit_grade == "BLOCKED"

def test_cockpit_paper_only():
    inp = DecisionCockpitInput()
    result = run_decision_cockpit(inp)
    assert result.paper_only is True

def test_cockpit_decision_only():
    inp = DecisionCockpitInput()
    result = run_decision_cockpit(inp)
    assert result.decision_only is True

def test_cockpit_no_real_orders():
    inp = DecisionCockpitInput()
    result = run_decision_cockpit(inp)
    assert result.no_real_orders is True

def test_cockpit_cockpit_version():
    inp = DecisionCockpitInput()
    result = run_decision_cockpit(inp)
    assert result.cockpit_version == "1.8.6"

def test_cockpit_with_a_candidate_ready():
    inp = DecisionCockpitInput(capital=300000.0, market_regime="BULL")
    c = CandidateDecisionInput(ticker="2330", abc_buy_point="A_10MA_PULLBACK",
                                above_10ma=True, volume_contracting=True,
                                kd_below_50=True, market_regime="BULL",
                                stop_loss_defined=True, liquidity_ok=True)
    result = run_decision_cockpit(inp, [c])
    assert result.candidate_count == 1

def test_cockpit_blocked_candidate_counted():
    inp = DecisionCockpitInput(capital=300000.0, market_regime="BULL")
    c = CandidateDecisionInput(ticker="X", market_regime="BLOCKED")
    result = run_decision_cockpit(inp, [c])
    assert result.blocked_candidate_count == 1

# ── build_decision_dashboard ──────────────────────────────────────────────────
def test_dashboard_paper_only():
    inp = DecisionCockpitInput()
    result = build_decision_dashboard(inp)
    assert result.paper_only is True

def test_dashboard_decision_only():
    inp = DecisionCockpitInput()
    result = build_decision_dashboard(inp)
    assert result.decision_only is True

def test_dashboard_has_regime_decision():
    inp = DecisionCockpitInput()
    result = build_decision_dashboard(inp)
    assert result.regime_decision is not None

def test_dashboard_has_risk_decision():
    inp = DecisionCockpitInput()
    result = build_decision_dashboard(inp)
    assert result.risk_decision is not None

def test_dashboard_has_checklist():
    inp = DecisionCockpitInput()
    result = build_decision_dashboard(inp)
    assert result.checklist is not None

# ── get_engine_info ───────────────────────────────────────────────────────────
def test_engine_info_returns_dict():
    assert isinstance(get_engine_info(), dict)

def test_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True

def test_engine_info_decision_only():
    assert get_engine_info()["decision_only"] is True

def test_engine_info_version():
    assert get_engine_info()["version"] == "1.8.6"

def test_engine_info_no_buy_in_actions():
    assert "BUY" not in get_engine_info()["allowed_output_actions"]
