"""
tests/test_strategy_review_safety_v195.py
Tests for strategy review safety module v1.9.5.
[!] Research Only. Paper Only. Review Only. Human Approval Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_review_safety_v195 import (
    SAFETY_FLAGS, run_safety_audit,
    is_safe_output_path, is_forbidden_action, is_allowed_action,
    validate_review_action,
    FORBIDDEN_REVIEW_ACTIONS, ALLOWED_REVIEW_ACTIONS,
    HARD_BLOCK_CONDITIONS,
)


# ── safety audit ──────────────────────────────────────────────────────────────

def test_safety_audit_all_safe():
    assert run_safety_audit()["all_safe"] is True


def test_safety_audit_returns_dict():
    assert isinstance(run_safety_audit(), dict)


def test_safety_audit_paper_only():
    assert run_safety_audit()["paper_only"] is True


# ── safety flags ─────────────────────────────────────────────────────────────

def test_safety_flag_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True


def test_safety_flag_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True


def test_safety_flag_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True


def test_safety_flag_review_only():
    assert SAFETY_FLAGS["review_only"] is True


def test_safety_flag_human_approval_only():
    assert SAFETY_FLAGS["human_approval_only"] is True


def test_safety_flag_rollback_review_only():
    assert SAFETY_FLAGS["rollback_review_only"] is True


def test_safety_flag_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True


def test_safety_flag_no_production_mutation():
    assert SAFETY_FLAGS["no_production_strategy_mutation"] is True


def test_safety_flag_no_live_activation():
    assert SAFETY_FLAGS["no_live_strategy_activation"] is True


def test_safety_flag_broker_execution_false():
    assert SAFETY_FLAGS["broker_execution"] is False


def test_safety_flag_live_strategy_activation_false():
    assert SAFETY_FLAGS["live_strategy_activation"] is False


def test_safety_flag_auto_approval_false():
    assert SAFETY_FLAGS["auto_approval"] is False


def test_safety_flag_auto_rollback_false():
    assert SAFETY_FLAGS["auto_rollback"] is False


# ── forbidden actions ─────────────────────────────────────────────────────────

def test_forbidden_review_actions_count():
    assert len(FORBIDDEN_REVIEW_ACTIONS) == 9


def test_forbidden_action_buy():
    assert is_forbidden_action("BUY") is True


def test_forbidden_action_sell():
    assert is_forbidden_action("SELL") is True


def test_forbidden_action_broker_connect():
    assert is_forbidden_action("BROKER_ORDER") is True


def test_not_forbidden_action_review():
    assert is_forbidden_action("REVIEW") is False


# ── allowed actions ───────────────────────────────────────────────────────────

def test_allowed_review_actions_count():
    assert len(ALLOWED_REVIEW_ACTIONS) == 18


def test_allowed_action_review():
    assert is_allowed_action("REVIEW") is True


def test_allowed_action_human_approval():
    assert is_allowed_action("HUMAN_APPROVAL") is True


def test_allowed_action_monitor():
    assert is_allowed_action("MONITOR") is True


def test_not_allowed_action_buy():
    assert is_allowed_action("BUY") is False


# ── validate_review_action ────────────────────────────────────────────────────

def test_validate_review_action_allowed():
    result = validate_review_action("REVIEW")
    assert result["valid"] is True
    assert result["blocked"] is False


def test_validate_review_action_forbidden():
    result = validate_review_action("BUY")
    assert result["blocked"] is True
    assert result["valid"] is False


def test_validate_review_action_returns_dict():
    assert isinstance(validate_review_action("MONITOR"), dict)


# ── hard block conditions ─────────────────────────────────────────────────────

def test_hard_block_conditions_count():
    assert len(HARD_BLOCK_CONDITIONS) == 19


def test_hard_block_has_real_order():
    assert "real_order_requested" in HARD_BLOCK_CONDITIONS


def test_hard_block_has_live_activation():
    assert "live_strategy_activation_attempted" in HARD_BLOCK_CONDITIONS


def test_hard_block_has_missing_human_approval_checklist():
    assert "missing_human_approval_checklist" in HARD_BLOCK_CONDITIONS


def test_hard_block_has_automatic_rollback():
    assert "automatic_rollback_attempted" in HARD_BLOCK_CONDITIONS


def test_hard_block_has_missing_review_evidence():
    assert "missing_review_evidence" in HARD_BLOCK_CONDITIONS


# ── safe output path ──────────────────────────────────────────────────────────

def test_safe_output_path_reports():
    assert is_safe_output_path("reports/") is True


def test_safe_output_path_production_blocked():
    assert is_safe_output_path("production_strategy/") is False


def test_safe_output_path_live_blocked():
    assert is_safe_output_path("live_trading/") is False
