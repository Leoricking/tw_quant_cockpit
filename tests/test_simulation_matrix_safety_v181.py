"""
tests/test_simulation_matrix_safety_v181.py
Tests for simulation_matrix_safety_v181 — safety flags and audit.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.simulation_matrix_safety_v181 import (
    SAFETY_FLAGS, _MUST_BE_TRUE, _MUST_BE_FALSE,
    get_safety_flags, run_safety_audit, assert_safe,
)


# ── SAFETY_FLAGS content ───────────────────────────────────────────────────────

def test_safety_flags_is_dict():
    assert isinstance(SAFETY_FLAGS, dict)

def test_safety_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True

def test_safety_research_only():
    assert SAFETY_FLAGS["research_only"] is True

def test_safety_simulate_only():
    assert SAFETY_FLAGS["simulate_only"] is True

def test_safety_stress_test_only():
    assert SAFETY_FLAGS["stress_test_only"] is True

def test_safety_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True

def test_safety_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True

def test_safety_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True

def test_safety_production_trading_blocked():
    assert SAFETY_FLAGS["production_trading_blocked"] is True

def test_safety_real_order_is_false():
    assert SAFETY_FLAGS["real_order"] is False

def test_safety_real_trading_is_false():
    assert SAFETY_FLAGS["real_trading"] is False

def test_safety_real_account_is_false():
    assert SAFETY_FLAGS["real_account"] is False

def test_safety_broker_execution_is_false():
    assert SAFETY_FLAGS["broker_execution"] is False

def test_safety_no_margin():
    assert SAFETY_FLAGS["no_margin"] is True

def test_safety_no_leverage():
    assert SAFETY_FLAGS["no_leverage"] is True

def test_safety_no_production_db_writes():
    assert SAFETY_FLAGS["no_production_db_writes"] is True

def test_safety_deterministic():
    assert SAFETY_FLAGS["deterministic"] is True

def test_safety_demo_only():
    assert SAFETY_FLAGS["demo_only"] is True

def test_safety_not_for_production():
    assert SAFETY_FLAGS["not_for_production"] is True


# ── _MUST_BE_TRUE / _MUST_BE_FALSE lists ──────────────────────────────────────

def test_must_be_true_is_list():
    assert isinstance(_MUST_BE_TRUE, list)

def test_must_be_false_is_list():
    assert isinstance(_MUST_BE_FALSE, list)

def test_must_be_true_contains_paper_only():
    assert "paper_only" in _MUST_BE_TRUE

def test_must_be_true_contains_research_only():
    assert "research_only" in _MUST_BE_TRUE

def test_must_be_true_contains_stress_test_only():
    assert "stress_test_only" in _MUST_BE_TRUE

def test_must_be_true_contains_no_real_orders():
    assert "no_real_orders" in _MUST_BE_TRUE

def test_must_be_false_contains_real_order():
    assert "real_order" in _MUST_BE_FALSE

def test_must_be_false_contains_real_trading():
    assert "real_trading" in _MUST_BE_FALSE

def test_must_be_false_contains_broker_execution():
    assert "broker_execution" in _MUST_BE_FALSE

def test_must_be_true_ge_10():
    assert len(_MUST_BE_TRUE) >= 10

def test_must_be_false_ge_3():
    assert len(_MUST_BE_FALSE) >= 3


# ── get_safety_flags() ─────────────────────────────────────────────────────────

def test_get_safety_flags_is_dict():
    assert isinstance(get_safety_flags(), dict)

def test_get_safety_flags_returns_copy():
    flags = get_safety_flags()
    flags["paper_only"] = False
    assert SAFETY_FLAGS["paper_only"] is True

def test_get_safety_flags_paper_only():
    assert get_safety_flags()["paper_only"] is True

def test_get_safety_flags_stress_test_only():
    assert get_safety_flags()["stress_test_only"] is True

def test_get_safety_flags_real_order_false():
    assert get_safety_flags()["real_order"] is False


# ── run_safety_audit() ─────────────────────────────────────────────────────────

def test_run_safety_audit_returns_dict():
    assert isinstance(run_safety_audit(), dict)

def test_run_safety_audit_all_safe():
    assert run_safety_audit()["all_safe"] is True

def test_run_safety_audit_issues_empty():
    assert run_safety_audit()["issues"] == []

def test_run_safety_audit_paper_only():
    assert run_safety_audit()["paper_only"] is True

def test_run_safety_audit_research_only():
    assert run_safety_audit()["research_only"] is True

def test_run_safety_audit_no_real_orders():
    assert run_safety_audit()["no_real_orders"] is True

def test_run_safety_audit_not_investment_advice():
    assert run_safety_audit()["not_investment_advice"] is True

def test_run_safety_audit_checked_true_key():
    result = run_safety_audit()
    assert "checked_true" in result

def test_run_safety_audit_checked_false_key():
    result = run_safety_audit()
    assert "checked_false" in result

def test_run_safety_audit_checked_true_is_list():
    assert isinstance(run_safety_audit()["checked_true"], list)

def test_run_safety_audit_checked_false_is_list():
    assert isinstance(run_safety_audit()["checked_false"], list)

def test_run_safety_audit_checked_true_contains_paper_only():
    assert "paper_only" in run_safety_audit()["checked_true"]

def test_run_safety_audit_checked_false_contains_real_order():
    assert "real_order" in run_safety_audit()["checked_false"]


# ── assert_safe() ──────────────────────────────────────────────────────────────

def test_assert_safe_does_not_raise():
    assert_safe()

def test_assert_safe_returns_none():
    assert assert_safe() is None
