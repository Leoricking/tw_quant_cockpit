"""
tests/test_monte_carlo_safety_v183.py
Tests for Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3 safety flags.
[!] Research Only. Paper Only. Monte Carlo Only.
"""
from paper_trading.small_capital_strategy.monte_carlo_safety_v183 import (
    SAFETY_FLAGS,
    get_safety_flags,
    run_safety_audit,
    assert_safe,
)


# --- SAFETY_FLAGS structure ---

def test_safety_flags_is_dict():
    assert isinstance(SAFETY_FLAGS, dict)


def test_safety_flags_len_at_least_19():
    assert len(SAFETY_FLAGS) >= 19


def test_safety_flags_has_broker_execution_key():
    assert "broker_execution" in SAFETY_FLAGS


# --- SAFETY_FLAGS True flags ---

def test_safety_flags_paper_only_is_true():
    assert SAFETY_FLAGS["paper_only"] is True


def test_safety_flags_research_only_is_true():
    assert SAFETY_FLAGS["research_only"] is True


def test_safety_flags_simulate_only_is_true():
    assert SAFETY_FLAGS["simulate_only"] is True


def test_safety_flags_validation_only_is_true():
    assert SAFETY_FLAGS["validation_only"] is True


def test_safety_flags_monte_carlo_only_is_true():
    assert SAFETY_FLAGS["monte_carlo_only"] is True


def test_safety_flags_no_real_orders_is_true():
    assert SAFETY_FLAGS["no_real_orders"] is True


def test_safety_flags_no_broker_is_true():
    assert SAFETY_FLAGS["no_broker"] is True


def test_safety_flags_no_margin_is_true():
    assert SAFETY_FLAGS["no_margin"] is True


def test_safety_flags_no_leverage_is_true():
    assert SAFETY_FLAGS["no_leverage"] is True


def test_safety_flags_no_auto_trade_is_true():
    assert SAFETY_FLAGS["no_auto_trade"] is True


def test_safety_flags_no_live_session_is_true():
    assert SAFETY_FLAGS["no_live_session"] is True


def test_safety_flags_no_production_db_writes_is_true():
    assert SAFETY_FLAGS["no_production_db_writes"] is True


def test_safety_flags_not_investment_advice_is_true():
    assert SAFETY_FLAGS["not_investment_advice"] is True


def test_safety_flags_demo_only_is_true():
    assert SAFETY_FLAGS["demo_only"] is True


def test_safety_flags_not_for_production_is_true():
    assert SAFETY_FLAGS["not_for_production"] is True


def test_safety_flags_production_trading_blocked_is_true():
    assert SAFETY_FLAGS["production_trading_blocked"] is True


def test_safety_flags_stress_test_only_is_true():
    assert SAFETY_FLAGS["stress_test_only"] is True


def test_safety_flags_monte_carlo_simulation_only_is_true():
    assert SAFETY_FLAGS["monte_carlo_simulation_only"] is True


# --- SAFETY_FLAGS False flags ---

def test_safety_flags_broker_execution_is_false():
    assert SAFETY_FLAGS["broker_execution"] is False


# --- Forbidden words not in flags ---

def test_buy_not_in_safety_flags_str():
    assert "BUY" not in str(SAFETY_FLAGS)


def test_sell_not_in_safety_flags_str():
    assert "SELL" not in str(SAFETY_FLAGS)


# --- get_safety_flags() ---

def test_get_safety_flags_returns_dict():
    result = get_safety_flags()
    assert isinstance(result, dict)


def test_get_safety_flags_paper_only_is_true():
    assert get_safety_flags()["paper_only"] is True


def test_get_safety_flags_is_copy_not_same_object():
    result = get_safety_flags()
    assert result is not SAFETY_FLAGS


# --- run_safety_audit() ---

def test_run_safety_audit_returns_dict():
    result = run_safety_audit()
    assert isinstance(result, dict)


def test_run_safety_audit_all_safe_is_true():
    assert run_safety_audit()["all_safe"] is True


def test_run_safety_audit_violations_is_empty_list():
    assert run_safety_audit()["violations"] == []


def test_run_safety_audit_paper_only_is_true():
    assert run_safety_audit()["paper_only"] is True


def test_run_safety_audit_monte_carlo_only_is_true():
    assert run_safety_audit()["monte_carlo_only"] is True


def test_run_safety_audit_total_flags_at_least_19():
    assert run_safety_audit()["total_flags"] >= 19


# --- assert_safe() ---

def test_assert_safe_runs_without_raising():
    assert_safe()  # Must not raise
