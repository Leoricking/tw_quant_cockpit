"""tests/test_paper_simulation_safety_v180.py — v1.8.0 Paper Simulation safety tests"""
from __future__ import annotations
import pytest
from paper_trading.small_capital_strategy.paper_simulation_safety_v180 import (
    SAFETY_FLAGS, run_safety_audit, assert_safe, get_safety_flags,
)


# ---------------------------------------------------------------------------
# SAFETY_FLAGS — must-be-True flags
# ---------------------------------------------------------------------------

def test_safety_flags_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True


def test_safety_flags_research_only():
    assert SAFETY_FLAGS["research_only"] is True


def test_safety_flags_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True


def test_safety_flags_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True


def test_safety_flags_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True


def test_safety_flags_production_trading_blocked():
    assert SAFETY_FLAGS["production_trading_blocked"] is True


def test_safety_flags_no_margin():
    assert SAFETY_FLAGS["no_margin"] is True


def test_safety_flags_no_leverage():
    assert SAFETY_FLAGS["no_leverage"] is True


def test_safety_flags_no_production_db_writes():
    assert SAFETY_FLAGS["no_production_db_writes"] is True


def test_safety_flags_deterministic():
    assert SAFETY_FLAGS["deterministic"] is True


def test_safety_flags_demo_only():
    assert SAFETY_FLAGS["demo_only"] is True


def test_safety_flags_not_for_production():
    assert SAFETY_FLAGS["not_for_production"] is True


def test_safety_flags_simulate_only():
    assert SAFETY_FLAGS["simulate_only"] is True


# ---------------------------------------------------------------------------
# SAFETY_FLAGS — must-be-False flags
# ---------------------------------------------------------------------------

def test_safety_flags_real_trading_is_false():
    assert SAFETY_FLAGS["real_trading"] is False


def test_safety_flags_real_order_is_false():
    assert SAFETY_FLAGS["real_order"] is False


def test_safety_flags_broker_execution_is_false():
    assert SAFETY_FLAGS["broker_execution"] is False


def test_safety_flags_real_account_is_false():
    assert SAFETY_FLAGS["real_account"] is False


# ---------------------------------------------------------------------------
# SAFETY_FLAGS — key presence checks
# ---------------------------------------------------------------------------

def test_safety_flags_is_dict():
    assert isinstance(SAFETY_FLAGS, dict)


def test_safety_flags_real_order_key_present():
    assert "real_order" in SAFETY_FLAGS


def test_safety_flags_no_buy_string():
    assert "BUY" not in str(SAFETY_FLAGS)


def test_safety_flags_no_sell_string():
    assert "SELL" not in str(SAFETY_FLAGS)


# ---------------------------------------------------------------------------
# run_safety_audit()
# ---------------------------------------------------------------------------

def test_run_safety_audit_returns_dict():
    result = run_safety_audit()
    assert isinstance(result, dict)


def test_run_safety_audit_all_safe_is_true():
    result = run_safety_audit()
    assert result["all_safe"] is True


def test_run_safety_audit_issues_is_empty_list():
    result = run_safety_audit()
    assert result["issues"] == []


def test_run_safety_audit_paper_only():
    result = run_safety_audit()
    assert result["paper_only"] is True


def test_run_safety_audit_checked_true_length():
    result = run_safety_audit()
    assert len(result["checked_true"]) >= 10


def test_run_safety_audit_checked_false_length():
    result = run_safety_audit()
    assert len(result["checked_false"]) >= 4


def test_run_safety_audit_checked_true_is_list():
    result = run_safety_audit()
    assert isinstance(result["checked_true"], list)


def test_run_safety_audit_checked_false_is_list():
    result = run_safety_audit()
    assert isinstance(result["checked_false"], list)


def test_run_safety_audit_research_only():
    result = run_safety_audit()
    assert result["research_only"] is True


def test_run_safety_audit_no_real_orders():
    result = run_safety_audit()
    assert result["no_real_orders"] is True


# ---------------------------------------------------------------------------
# assert_safe()
# ---------------------------------------------------------------------------

def test_assert_safe_does_not_raise():
    assert_safe()


def test_assert_safe_returns_none():
    result = assert_safe()
    assert result is None


# ---------------------------------------------------------------------------
# get_safety_flags()
# ---------------------------------------------------------------------------

def test_get_safety_flags_returns_dict():
    flags = get_safety_flags()
    assert isinstance(flags, dict)


def test_get_safety_flags_is_separate_copy():
    flags = get_safety_flags()
    assert flags is not SAFETY_FLAGS


def test_get_safety_flags_paper_only():
    flags = get_safety_flags()
    assert flags["paper_only"] is True


def test_get_safety_flags_no_real_orders():
    flags = get_safety_flags()
    assert flags["no_real_orders"] is True


def test_get_safety_flags_same_values_as_safety_flags():
    flags = get_safety_flags()
    for key, value in SAFETY_FLAGS.items():
        assert flags[key] == value


def test_get_safety_flags_mutating_copy_does_not_affect_original():
    flags = get_safety_flags()
    flags["paper_only"] = False
    assert SAFETY_FLAGS["paper_only"] is True
