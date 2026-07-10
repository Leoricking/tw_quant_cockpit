"""
tests/test_integrated_strategy_safety_v178.py
Tests for integrated_strategy_safety_v178.py — v1.7.8 Small Capital Strategy Integration.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.

Safety invariants:
    paper_only=True, no_real_orders=True, no_broker=True, not_investment_advice=True
"""
import pytest
from paper_trading.small_capital_strategy.integrated_strategy_safety_v178 import (
    SAFETY_FLAGS,
    get_safety_flags,
    run_safety_audit,
    assert_safe,
    INTEGRATED_STRATEGY_AVAILABLE,
    INTEGRATED_STRATEGY_RESEARCH_ONLY,
    INTEGRATED_STRATEGY_PAPER_ONLY,
    real_trading,
    real_account,
    real_order,
    broker_execution,
    production_trading_blocked,
)

# ---------------------------------------------------------------------------
# Safety invariants (module-level constants)
# ---------------------------------------------------------------------------
paper_only = True
no_real_orders = True
no_broker = True
not_investment_advice = True


# ---------------------------------------------------------------------------
# SAFETY_FLAGS — True flags
# ---------------------------------------------------------------------------

def test_safety_flags_paper_only_is_true():
    assert SAFETY_FLAGS["paper_only"] is True


def test_safety_flags_research_only_is_true():
    assert SAFETY_FLAGS["research_only"] is True


def test_safety_flags_no_real_orders_is_true():
    assert SAFETY_FLAGS["no_real_orders"] is True


def test_safety_flags_no_broker_is_true():
    assert SAFETY_FLAGS["no_broker"] is True


def test_safety_flags_not_investment_advice_is_true():
    assert SAFETY_FLAGS["not_investment_advice"] is True


def test_safety_flags_production_trading_blocked_is_true():
    assert SAFETY_FLAGS["production_trading_blocked"] is True


def test_safety_flags_no_margin_is_true():
    assert SAFETY_FLAGS["no_margin"] is True


def test_safety_flags_no_leverage_is_true():
    assert SAFETY_FLAGS["no_leverage"] is True


def test_safety_flags_no_production_db_writes_is_true():
    assert SAFETY_FLAGS["no_production_db_writes"] is True


def test_safety_flags_deterministic_is_true():
    assert SAFETY_FLAGS["deterministic"] is True


def test_safety_flags_demo_only_is_true():
    assert SAFETY_FLAGS["demo_only"] is True


def test_safety_flags_not_for_production_is_true():
    assert SAFETY_FLAGS["not_for_production"] is True


# ---------------------------------------------------------------------------
# SAFETY_FLAGS — False flags (real trading disabled)
# ---------------------------------------------------------------------------

def test_safety_flags_real_trading_is_false():
    assert SAFETY_FLAGS["real_trading"] is False


def test_safety_flags_real_account_is_false():
    assert SAFETY_FLAGS["real_account"] is False


def test_safety_flags_real_order_is_false():
    assert SAFETY_FLAGS["real_order"] is False


def test_safety_flags_broker_execution_is_false():
    assert SAFETY_FLAGS["broker_execution"] is False


# ---------------------------------------------------------------------------
# SAFETY_FLAGS — key count
# ---------------------------------------------------------------------------

def test_safety_flags_has_at_least_16_keys():
    assert len(SAFETY_FLAGS) >= 16


def test_safety_flags_is_a_dict():
    assert isinstance(SAFETY_FLAGS, dict)


# ---------------------------------------------------------------------------
# run_safety_audit
# ---------------------------------------------------------------------------

def test_run_safety_audit_all_safe_is_true():
    audit = run_safety_audit()
    assert audit["all_safe"] is True


def test_run_safety_audit_issues_is_empty_list():
    audit = run_safety_audit()
    assert audit["issues"] == []


def test_run_safety_audit_flags_paper_only_is_true():
    audit = run_safety_audit()
    assert audit["flags"]["paper_only"] is True


def test_run_safety_audit_returns_all_safe_key():
    audit = run_safety_audit()
    assert "all_safe" in audit


def test_run_safety_audit_returns_issues_key():
    audit = run_safety_audit()
    assert "issues" in audit


def test_run_safety_audit_returns_flags_key():
    audit = run_safety_audit()
    assert "flags" in audit


def test_run_safety_audit_result_has_exactly_3_top_keys():
    audit = run_safety_audit()
    assert set(audit.keys()) == {"all_safe", "issues", "flags"}


def test_run_safety_audit_is_deterministic():
    audit1 = run_safety_audit()
    audit2 = run_safety_audit()
    assert audit1["all_safe"] == audit2["all_safe"]
    assert audit1["issues"] == audit2["issues"]
    assert audit1["flags"] == audit2["flags"]


def test_run_safety_audit_flags_no_real_orders_is_true():
    audit = run_safety_audit()
    assert audit["flags"]["no_real_orders"] is True


def test_run_safety_audit_flags_no_broker_is_true():
    audit = run_safety_audit()
    assert audit["flags"]["no_broker"] is True


def test_run_safety_audit_flags_real_trading_is_false():
    audit = run_safety_audit()
    assert audit["flags"]["real_trading"] is False


# ---------------------------------------------------------------------------
# assert_safe
# ---------------------------------------------------------------------------

def test_assert_safe_does_not_raise():
    assert_safe()


def test_assert_safe_returns_none():
    result = assert_safe()
    assert result is None


# ---------------------------------------------------------------------------
# get_safety_flags
# ---------------------------------------------------------------------------

def test_get_safety_flags_returns_dict():
    result = get_safety_flags()
    assert isinstance(result, dict)


def test_get_safety_flags_no_real_orders_is_true():
    assert get_safety_flags()["no_real_orders"] is True


def test_get_safety_flags_no_broker_is_true():
    assert get_safety_flags()["no_broker"] is True


def test_get_safety_flags_paper_only_is_true():
    assert get_safety_flags()["paper_only"] is True


def test_get_safety_flags_returns_copy_not_same_object():
    flags_copy = get_safety_flags()
    assert flags_copy is not SAFETY_FLAGS


def test_get_safety_flags_copy_mutation_does_not_affect_original():
    flags_copy = get_safety_flags()
    flags_copy["paper_only"] = False
    assert SAFETY_FLAGS["paper_only"] is True


def test_get_safety_flags_values_match_safety_flags():
    flags_copy = get_safety_flags()
    for key, val in SAFETY_FLAGS.items():
        assert flags_copy[key] == val


# ---------------------------------------------------------------------------
# Module-level boolean variables
# ---------------------------------------------------------------------------

def test_integrated_strategy_available_is_true():
    assert INTEGRATED_STRATEGY_AVAILABLE is True


def test_integrated_strategy_research_only_is_true():
    assert INTEGRATED_STRATEGY_RESEARCH_ONLY is True


def test_integrated_strategy_paper_only_is_true():
    assert INTEGRATED_STRATEGY_PAPER_ONLY is True


def test_module_real_trading_is_false():
    assert real_trading is False


def test_module_real_account_is_false():
    assert real_account is False


def test_module_real_order_is_false():
    assert real_order is False


def test_module_broker_execution_is_false():
    assert broker_execution is False


def test_module_production_trading_blocked_is_true():
    assert production_trading_blocked is True
