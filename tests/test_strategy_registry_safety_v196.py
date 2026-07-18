"""
tests/test_strategy_registry_safety_v196.py
Tests for strategy_registry_safety_v196 — Paper Strategy Decision Registry & Governance Lab v1.9.6.
[!] Research Only. Paper Only. Governance Only. Registry Only. Decision Record Only.
[!] No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_registry_safety_v196 import (
    SAFETY_FLAGS, FORBIDDEN_REGISTRY_ACTIONS, ALLOWED_REGISTRY_ACTIONS,
    HARD_BLOCK_CONDITIONS, run_safety_audit, assert_safe,
    is_safe_output_path, is_forbidden_action, is_allowed_action,
    validate_registry_action,
)


# ── safety flags ──────────────────────────────────────────────────────────────

def test_safety_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True

def test_safety_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True

def test_safety_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True

def test_safety_governance_only():
    assert SAFETY_FLAGS["governance_only"] is True

def test_safety_registry_only():
    assert SAFETY_FLAGS["registry_only"] is True

def test_safety_decision_record_only():
    assert SAFETY_FLAGS["decision_record_only"] is True

def test_safety_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True

def test_safety_no_production_mutation():
    assert SAFETY_FLAGS["no_production_strategy_mutation"] is True

def test_safety_no_live_activation():
    assert SAFETY_FLAGS["no_live_strategy_activation"] is True

def test_safety_broker_execution_false():
    assert SAFETY_FLAGS["broker_execution"] is False

def test_safety_auto_approval_false():
    assert SAFETY_FLAGS["auto_approval"] is False

def test_safety_auto_decision_false():
    assert SAFETY_FLAGS["auto_decision"] is False

def test_safety_immutable_decision_record_true():
    assert SAFETY_FLAGS["immutable_decision_record"] is True

def test_safety_no_automatic_rollback():
    assert SAFETY_FLAGS["no_automatic_rollback"] is True


# ── run_safety_audit ──────────────────────────────────────────────────────────

def test_safety_audit_all_safe():
    result = run_safety_audit()
    assert result["all_safe"] is True

def test_safety_audit_returns_dict():
    assert isinstance(run_safety_audit(), dict)

def test_safety_audit_paper_only():
    assert run_safety_audit()["paper_only"] is True


# ── assert_safe ───────────────────────────────────────────────────────────────

def test_assert_safe_no_raise():
    assert_safe()  # should not raise


# ── forbidden / allowed actions ───────────────────────────────────────────────

def test_forbidden_actions_count_9():
    assert len(FORBIDDEN_REGISTRY_ACTIONS) == 9

def test_forbidden_actions_contains_buy():
    assert "BUY" in FORBIDDEN_REGISTRY_ACTIONS

def test_forbidden_actions_contains_sell():
    assert "SELL" in FORBIDDEN_REGISTRY_ACTIONS

def test_forbidden_actions_contains_broker_order():
    assert "BROKER_ORDER" in FORBIDDEN_REGISTRY_ACTIONS

def test_allowed_actions_count_18():
    assert len(ALLOWED_REGISTRY_ACTIONS) == 18

def test_is_forbidden_buy():
    assert is_forbidden_action("BUY") is True

def test_is_forbidden_sell():
    assert is_forbidden_action("SELL") is True

def test_is_forbidden_broker_order():
    assert is_forbidden_action("BROKER_ORDER") is True

def test_is_allowed_register():
    assert any(is_allowed_action(a) for a in ALLOWED_REGISTRY_ACTIONS)

def test_not_forbidden_register_decision():
    assert is_forbidden_action("REGISTER_DECISION") is False


# ── hard block conditions ─────────────────────────────────────────────────────

def test_hard_block_conditions_count_20():
    assert len(HARD_BLOCK_CONDITIONS) == 20

def test_hard_block_conditions_margin_or_leverage():
    assert "margin_or_leverage_requested" in HARD_BLOCK_CONDITIONS


# ── safe output path ──────────────────────────────────────────────────────────

def test_safe_output_path_reports():
    assert is_safe_output_path("reports/") is True

def test_safe_output_path_unsafe():
    assert is_safe_output_path("/etc/passwd") is False


# ── validate_registry_action ──────────────────────────────────────────────────

def test_validate_registry_action_buy_blocked():
    result = validate_registry_action("BUY")
    assert result["blocked"] is True

def test_validate_registry_action_allowed_valid():
    first_allowed = next(iter(ALLOWED_REGISTRY_ACTIONS))
    result = validate_registry_action(first_allowed)
    assert result["blocked"] is False
