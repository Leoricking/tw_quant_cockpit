"""
tests/test_position_sizing_engine_v184.py
Tests for position_sizing_engine_v184 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.position_sizing_engine_v184 import (
    ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
    CAPITAL_STAGES, SIZING_METHODS, ABC_SIZING_RULES,
    validate_action, validate_grade, run_position_sizing,
    build_position_sizing_dashboard, get_engine_info,
)
from paper_trading.small_capital_strategy.position_sizing_models_v184 import (
    PositionSizingInput,
)


def _safe_input(**kwargs):
    defaults = dict(capital=300000.0, per_trade_risk_pct=1.0,
                    stop_loss_distance_pct=7.0, has_stop_loss=True,
                    market_regime="BULL")
    defaults.update(kwargs)
    return PositionSizingInput(**defaults)


# ── Constants ─────────────────────────────────────────────────────────────────
def test_allowed_actions_count():
    assert len(ALLOWED_OUTPUT_ACTIONS) == 15

def test_forbidden_words_count():
    assert len(FORBIDDEN_OUTPUT_WORDS) == 9

def test_valid_grades_count():
    assert len(VALID_FINAL_GRADES) == 5

def test_capital_stages_count():
    assert len(CAPITAL_STAGES) == 4

def test_capital_stages_contains_300k():
    assert 300000 in CAPITAL_STAGES

def test_capital_stages_contains_500k():
    assert 500000 in CAPITAL_STAGES

def test_capital_stages_contains_1m():
    assert 1000000 in CAPITAL_STAGES

def test_capital_stages_contains_3m():
    assert 3000000 in CAPITAL_STAGES

def test_sizing_methods_count():
    assert len(SIZING_METHODS) == 10

def test_abc_rules_count():
    assert len(ABC_SIZING_RULES) == 3

def test_forbidden_BUY():
    assert "BUY" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_SELL():
    assert "SELL" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_ORDER():
    assert "ORDER" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_EXECUTE():
    assert "EXECUTE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_SUBMIT_ORDER():
    assert "SUBMIT_ORDER" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_AUTO_TRADE():
    assert "AUTO_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_REAL_TRADE():
    assert "REAL_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_LIVE_TRADE():
    assert "LIVE_TRADE" in FORBIDDEN_OUTPUT_WORDS

def test_forbidden_BROKER_ORDER():
    assert "BROKER_ORDER" in FORBIDDEN_OUTPUT_WORDS

def test_valid_grade_SAFE():
    assert "SAFE" in VALID_FINAL_GRADES

def test_valid_grade_ACCEPTABLE():
    assert "ACCEPTABLE" in VALID_FINAL_GRADES

def test_valid_grade_CAUTION():
    assert "CAUTION" in VALID_FINAL_GRADES

def test_valid_grade_HIGH_RISK():
    assert "HIGH_RISK" in VALID_FINAL_GRADES

def test_valid_grade_BLOCKED():
    assert "BLOCKED" in VALID_FINAL_GRADES


# ── validate_action ───────────────────────────────────────────────────────────
def test_validate_action_paper_entry_allowed():
    assert validate_action("PAPER_ENTRY_ALLOWED") is True

def test_validate_action_blocked():
    assert validate_action("BLOCKED") is True

def test_validate_action_allocation_only():
    assert validate_action("ALLOCATION_ONLY") is True

def test_validate_action_BUY_false():
    assert validate_action("BUY") is False

def test_validate_action_SELL_false():
    assert validate_action("SELL") is False

def test_validate_action_ORDER_false():
    assert validate_action("ORDER") is False


# ── validate_grade ────────────────────────────────────────────────────────────
def test_validate_grade_SAFE():
    assert validate_grade("SAFE") is True

def test_validate_grade_BLOCKED():
    assert validate_grade("BLOCKED") is True

def test_validate_grade_invalid():
    assert validate_grade("RUIN_RISK") is False


# ── run_position_sizing ───────────────────────────────────────────────────────
def test_run_ps_returns_result():
    result = run_position_sizing(_safe_input())
    from paper_trading.small_capital_strategy.position_sizing_models_v184 import PositionSizingResult
    assert isinstance(result, PositionSizingResult)

def test_run_ps_paper_only():
    assert run_position_sizing(_safe_input()).paper_only is True

def test_run_ps_allocation_only():
    assert run_position_sizing(_safe_input()).allocation_only is True

def test_run_ps_no_real_orders():
    assert run_position_sizing(_safe_input()).no_real_orders is True

def test_run_ps_no_broker():
    assert run_position_sizing(_safe_input()).no_broker is True

def test_run_ps_risk_amount_correct():
    result = run_position_sizing(_safe_input(capital=300000.0, per_trade_risk_pct=1.0))
    assert result.per_trade_risk_amount == 3000.0

def test_run_ps_position_value_gt0():
    assert run_position_sizing(_safe_input()).suggested_position_value > 0

def test_run_ps_safe_grade():
    assert run_position_sizing(_safe_input()).final_position_grade == "SAFE"

def test_run_ps_initial_entry_positive():
    assert run_position_sizing(_safe_input()).initial_entry_value > 0

def test_run_ps_add_value_positive():
    assert run_position_sizing(_safe_input()).add_position_value > 0

def test_run_ps_cash_after_entry_positive():
    assert run_position_sizing(_safe_input()).cash_after_entry > 0

def test_run_ps_concentration_score_range():
    r = run_position_sizing(_safe_input())
    assert 0 <= r.concentration_risk_score <= 100

def test_run_ps_drawdown_usage_zero():
    r = run_position_sizing(_safe_input(current_drawdown_pct=0.0, max_drawdown_budget_pct=20.0))
    assert r.drawdown_budget_usage_pct == 0.0

def test_run_ps_ruin_adjustment_default():
    assert run_position_sizing(_safe_input()).ruin_risk_adjustment == 1.0


# ── Hard blocks ───────────────────────────────────────────────────────────────
def test_block_no_stop_loss():
    r = run_position_sizing(_safe_input(has_stop_loss=False))
    assert r.final_position_grade == "BLOCKED"

def test_block_zero_stop_distance():
    r = run_position_sizing(_safe_input(stop_loss_distance_pct=0.0))
    assert r.final_position_grade == "BLOCKED"

def test_block_high_risk_pct():
    r = run_position_sizing(_safe_input(per_trade_risk_pct=6.0))
    assert r.final_position_grade == "BLOCKED"

def test_block_drawdown_exceeded():
    r = run_position_sizing(_safe_input(current_drawdown_pct=20.0, max_drawdown_budget_pct=20.0))
    assert r.final_position_grade == "BLOCKED"

def test_block_ruin_risk_high():
    r = run_position_sizing(_safe_input(ruin_risk_pct=25.0))
    assert r.final_position_grade == "BLOCKED"

def test_block_market_regime_blocked():
    r = run_position_sizing(_safe_input(market_regime="BLOCKED"))
    assert r.final_position_grade == "BLOCKED"

def test_block_action_is_blocked():
    r = run_position_sizing(_safe_input(has_stop_loss=False))
    assert r.action == "BLOCKED"


# ── ABC staged sizing ─────────────────────────────────────────────────────────
def test_abc_a_initial_40pct():
    r = run_position_sizing(_safe_input(abc_buy_point="A_10MA_PULLBACK"))
    ratio = r.initial_entry_value / r.suggested_position_value
    assert abs(ratio - 0.4) < 0.01

def test_abc_b_initial_50pct():
    r = run_position_sizing(_safe_input(abc_buy_point="B_BREAKOUT"))
    ratio = r.initial_entry_value / r.suggested_position_value
    assert abs(ratio - 0.5) < 0.01

def test_abc_c_initial_30pct():
    r = run_position_sizing(_safe_input(abc_buy_point="C_20MA_RECLAIM"))
    ratio = r.initial_entry_value / r.suggested_position_value
    assert abs(ratio - 0.3) < 0.01


# ── Volatility adjustment ─────────────────────────────────────────────────────
def test_high_vol_reduces_size():
    high_vol = run_position_sizing(_safe_input(volatility_pct=35.0))
    low_vol  = run_position_sizing(_safe_input(volatility_pct=10.0))
    assert high_vol.suggested_position_value <= low_vol.suggested_position_value

def test_high_ruin_reduces_adjustment():
    r = run_position_sizing(_safe_input(ruin_risk_pct=12.0))
    assert r.ruin_risk_adjustment < 1.0


# ── Capital stage outputs ─────────────────────────────────────────────────────
def test_500k_risk_amount():
    r = run_position_sizing(_safe_input(capital=500000.0, per_trade_risk_pct=1.0))
    assert r.per_trade_risk_amount == 5000.0

def test_1m_risk_amount():
    r = run_position_sizing(_safe_input(capital=1000000.0, per_trade_risk_pct=1.0))
    assert r.per_trade_risk_amount == 10000.0

def test_3m_position_value_larger():
    r300k = run_position_sizing(_safe_input(capital=300000.0))
    r3m   = run_position_sizing(_safe_input(capital=3000000.0))
    assert r3m.suggested_position_value > r300k.suggested_position_value


# ── Dashboard ─────────────────────────────────────────────────────────────────
def test_dashboard_callable():
    dash = build_position_sizing_dashboard(_safe_input())
    assert dash.paper_only is True

def test_dashboard_no_real_orders():
    assert build_position_sizing_dashboard(_safe_input()).no_real_orders is True

def test_dashboard_capital_profile_present():
    assert build_position_sizing_dashboard(_safe_input()).capital_profile is not None

def test_dashboard_risk_budget_present():
    assert build_position_sizing_dashboard(_safe_input()).risk_budget is not None

def test_dashboard_sizing_result_present():
    assert build_position_sizing_dashboard(_safe_input()).sizing_result is not None


# ── Engine info ───────────────────────────────────────────────────────────────
def test_engine_info_returns_dict():
    assert isinstance(get_engine_info(), dict)

def test_engine_info_paper_only():
    assert get_engine_info()["paper_only"] is True

def test_engine_info_allocation_only():
    assert get_engine_info()["allocation_only"] is True
