"""
tests/test_optimization_safety_v182.py
Tests for optimization safety module v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.optimization_safety_v182 import (
    SAFETY_FLAGS, _MUST_BE_TRUE, _MUST_BE_FALSE,
    get_safety_flags, run_safety_audit, assert_safe,
)


# --- SAFETY_FLAGS ---
def test_safety_flags_is_dict():
    assert isinstance(SAFETY_FLAGS, dict)

def test_safety_flags_count_18():
    assert len(SAFETY_FLAGS) == 18

def test_safety_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True

def test_safety_research_only():
    assert SAFETY_FLAGS["research_only"] is True

def test_safety_simulate_only():
    assert SAFETY_FLAGS["simulate_only"] is True

def test_safety_validation_only():
    assert SAFETY_FLAGS["validation_only"] is True

def test_safety_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True

def test_safety_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True

def test_safety_no_margin():
    assert SAFETY_FLAGS["no_margin"] is True

def test_safety_no_leverage():
    assert SAFETY_FLAGS["no_leverage"] is True

def test_safety_no_auto_trade():
    assert SAFETY_FLAGS["no_auto_trade"] is True

def test_safety_no_live_session():
    assert SAFETY_FLAGS["no_live_session"] is True

def test_safety_no_production_db_writes():
    assert SAFETY_FLAGS["no_production_db_writes"] is True

def test_safety_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True

def test_safety_demo_only():
    assert SAFETY_FLAGS["demo_only"] is True

def test_safety_not_for_production():
    assert SAFETY_FLAGS["not_for_production"] is True

def test_safety_production_trading_blocked():
    assert SAFETY_FLAGS["production_trading_blocked"] is True

def test_safety_broker_execution_false():
    assert SAFETY_FLAGS["broker_execution"] is False

def test_safety_stress_test_only():
    assert SAFETY_FLAGS["stress_test_only"] is True

def test_safety_optimization_only():
    assert SAFETY_FLAGS["optimization_only"] is True


# --- _MUST_BE_TRUE ---
def test_must_be_true_is_list():
    assert isinstance(_MUST_BE_TRUE, list)

def test_must_be_true_count_17():
    assert len(_MUST_BE_TRUE) == 17

def test_must_be_true_contains_paper_only():
    assert "paper_only" in _MUST_BE_TRUE

def test_must_be_true_contains_validation_only():
    assert "validation_only" in _MUST_BE_TRUE

def test_must_be_true_contains_optimization_only():
    assert "optimization_only" in _MUST_BE_TRUE

def test_must_be_true_contains_stress_test_only():
    assert "stress_test_only" in _MUST_BE_TRUE

def test_must_be_true_all_true():
    for key in _MUST_BE_TRUE:
        assert SAFETY_FLAGS[key] is True, f"{key} should be True"


# --- _MUST_BE_FALSE ---
def test_must_be_false_is_list():
    assert isinstance(_MUST_BE_FALSE, list)

def test_must_be_false_count_1():
    assert len(_MUST_BE_FALSE) == 1

def test_must_be_false_contains_broker_execution():
    assert "broker_execution" in _MUST_BE_FALSE

def test_must_be_false_all_false():
    for key in _MUST_BE_FALSE:
        assert SAFETY_FLAGS[key] is False, f"{key} should be False"


# --- get_safety_flags() ---
def test_get_safety_flags_returns_dict():
    assert isinstance(get_safety_flags(), dict)

def test_get_safety_flags_count_18():
    assert len(get_safety_flags()) == 18

def test_get_safety_flags_paper_only():
    assert get_safety_flags()["paper_only"] is True

def test_get_safety_flags_returns_copy():
    flags = get_safety_flags()
    flags["paper_only"] = False
    assert SAFETY_FLAGS["paper_only"] is True

def test_get_safety_flags_broker_false():
    assert get_safety_flags()["broker_execution"] is False

def test_get_safety_flags_optimization_only():
    assert get_safety_flags()["optimization_only"] is True


# --- run_safety_audit() ---
def test_run_safety_audit_returns_dict():
    assert isinstance(run_safety_audit(), dict)

def test_run_safety_audit_all_safe():
    assert run_safety_audit()["all_safe"] is True

def test_run_safety_audit_no_violations():
    assert len(run_safety_audit()["violations"]) == 0

def test_run_safety_audit_total_flags():
    assert run_safety_audit()["total_flags"] == 18

def test_run_safety_audit_must_be_true_count():
    assert run_safety_audit()["must_be_true_count"] == 17

def test_run_safety_audit_must_be_false_count():
    assert run_safety_audit()["must_be_false_count"] == 1

def test_run_safety_audit_paper_only():
    assert run_safety_audit()["paper_only"] is True

def test_run_safety_audit_validation_only():
    assert run_safety_audit()["validation_only"] is True

def test_run_safety_audit_schema_version():
    assert run_safety_audit()["schema_version"] == "182"


# --- assert_safe() ---
def test_assert_safe_no_exception():
    assert_safe()

def test_assert_safe_returns_none():
    assert assert_safe() is None


# --- Cross-checks ---
def test_all_must_be_true_keys_in_flags():
    for key in _MUST_BE_TRUE:
        assert key in SAFETY_FLAGS

def test_all_must_be_false_keys_in_flags():
    for key in _MUST_BE_FALSE:
        assert key in SAFETY_FLAGS

def test_total_must_checks_equal_18():
    assert len(_MUST_BE_TRUE) + len(_MUST_BE_FALSE) == 18
