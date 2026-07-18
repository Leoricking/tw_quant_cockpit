"""tests/test_strategy_sandbox_safety_v192.py
Tests for strategy sandbox safety flags and audit v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_sandbox_safety_v192 import (
    SAFETY_FLAGS, FORBIDDEN_SANDBOX_ACTIONS, ALLOWED_SANDBOX_ACTIONS,
    HARD_BLOCK_CONDITIONS,
    run_safety_audit, is_safe_output_path, is_forbidden_action,
    is_allowed_action, validate_sandbox_action, has_forbidden_words,
    validate_sandbox_input_safe, get_safety_flags, get_hard_block_conditions,
    get_forbidden_sandbox_actions, get_allowed_sandbox_actions,
)


# ── SAFETY_FLAGS (positive) ───────────────────────────────────────────────────

def test_safety_flag_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True

def test_safety_flag_sandbox_only():
    assert SAFETY_FLAGS["sandbox_only"] is True

def test_safety_flag_shadow_only():
    assert SAFETY_FLAGS["shadow_only"] is True

def test_safety_flag_no_live_strategy_activation():
    assert SAFETY_FLAGS["no_live_strategy_activation"] is True

def test_safety_flag_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True

def test_safety_flag_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True

def test_safety_flag_no_margin():
    assert SAFETY_FLAGS["no_margin"] is True

def test_safety_flag_no_leverage():
    assert SAFETY_FLAGS["no_leverage"] is True

def test_safety_flag_no_production_strategy_mutation():
    assert SAFETY_FLAGS["no_production_strategy_mutation"] is True

def test_safety_flag_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True

def test_safety_flag_production_trading_blocked():
    assert SAFETY_FLAGS["production_trading_blocked"] is True


# ── SAFETY_FLAGS (negative) ───────────────────────────────────────────────────

def test_safety_flag_broker_execution_false():
    assert SAFETY_FLAGS["broker_execution"] is False

def test_safety_flag_live_strategy_activation_false():
    assert SAFETY_FLAGS["live_strategy_activation"] is False

def test_safety_flag_production_strategy_mutation_false():
    assert SAFETY_FLAGS["production_strategy_mutation"] is False


# ── run_safety_audit ──────────────────────────────────────────────────────────

def test_run_safety_audit_all_safe():
    result = run_safety_audit()
    assert result["all_safe"] is True

def test_run_safety_audit_paper_only():
    result = run_safety_audit()
    assert result["paper_only"] is True

def test_run_safety_audit_sandbox_only():
    result = run_safety_audit()
    assert result["sandbox_only"] is True

def test_run_safety_audit_no_issues():
    result = run_safety_audit()
    assert result["issues"] == []

def test_run_safety_audit_schema_192():
    result = run_safety_audit()
    assert result["schema_version"] == "192"


# ── is_safe_output_path ───────────────────────────────────────────────────────

def test_is_safe_output_path_reports_true():
    assert is_safe_output_path("reports/") is True

def test_is_safe_output_path_empty_false():
    assert is_safe_output_path("") is False

def test_is_safe_output_path_production_strategy_false():
    assert is_safe_output_path("production_strategy/foo") is False

def test_is_safe_output_path_broker_false():
    assert is_safe_output_path("broker/orders") is False

def test_is_safe_output_path_live_orders_false():
    assert is_safe_output_path("live_orders/") is False

def test_is_safe_output_path_sandbox_reports_true():
    assert is_safe_output_path("sandbox_reports/2024/") is True

def test_is_safe_output_path_real_orders_false():
    assert is_safe_output_path("real_orders/submit") is False


# ── is_forbidden_action ───────────────────────────────────────────────────────

def test_is_forbidden_action_buy_true():
    assert is_forbidden_action("BUY") is True

def test_is_forbidden_action_sell_true():
    assert is_forbidden_action("SELL") is True

def test_is_forbidden_action_broker_order_true():
    assert is_forbidden_action("BROKER_ORDER") is True

def test_is_forbidden_action_auto_trade_true():
    assert is_forbidden_action("AUTO_TRADE") is True

def test_is_forbidden_action_live_trade_true():
    assert is_forbidden_action("LIVE_TRADE") is True


# ── is_allowed_action ─────────────────────────────────────────────────────────

def test_is_allowed_action_sandbox_run_true():
    assert is_allowed_action("SANDBOX_RUN") is True

def test_is_allowed_action_shadow_compare_true():
    assert is_allowed_action("SHADOW_COMPARE") is True

def test_is_allowed_action_safety_audit_true():
    assert is_allowed_action("SAFETY_AUDIT") is True

def test_is_allowed_action_review_true():
    assert is_allowed_action("REVIEW") is True

def test_is_allowed_action_buy_false():
    assert is_allowed_action("BUY") is False

def test_is_allowed_action_sell_false():
    assert is_allowed_action("SELL") is False


# ── validate_sandbox_action ───────────────────────────────────────────────────

def test_validate_sandbox_action_sandbox_run_valid():
    result = validate_sandbox_action("SANDBOX_RUN")
    assert result["valid"] is True

def test_validate_sandbox_action_buy_blocked():
    result = validate_sandbox_action("BUY")
    assert result["blocked"] is True

def test_validate_sandbox_action_buy_not_valid():
    result = validate_sandbox_action("BUY")
    assert result["valid"] is False

def test_validate_sandbox_action_paper_only_preserved():
    result = validate_sandbox_action("SANDBOX_RUN")
    assert result["paper_only"] is True


# ── has_forbidden_words ───────────────────────────────────────────────────────

def test_has_forbidden_words_buy_signal_true():
    assert has_forbidden_words("some BUY signal") is True

def test_has_forbidden_words_research_only_false():
    assert has_forbidden_words("research only paper sandbox") is False

def test_has_forbidden_words_sell_true():
    assert has_forbidden_words("candidate has a SELL rule") is True

def test_has_forbidden_words_order_true():
    assert has_forbidden_words("submit ORDER now") is True

def test_has_forbidden_words_clean_text_false():
    assert has_forbidden_words("shadow compare baseline vs candidate") is False


# ── validate_sandbox_input_safe ───────────────────────────────────────────────

def test_validate_sandbox_input_safe_valid():
    result = validate_sandbox_input_safe("sid_001", "base_snap", "cand_snap")
    assert result["valid"] is True

def test_validate_sandbox_input_safe_missing_sandbox_id():
    result = validate_sandbox_input_safe("", "base_snap", "cand_snap")
    assert result["valid"] is False

def test_validate_sandbox_input_safe_missing_baseline():
    result = validate_sandbox_input_safe("sid_001", "", "cand_snap")
    assert result["valid"] is False

def test_validate_sandbox_input_safe_missing_candidate():
    result = validate_sandbox_input_safe("sid_001", "base_snap", "")
    assert result["valid"] is False

def test_validate_sandbox_input_safe_paper_only():
    result = validate_sandbox_input_safe("sid_001", "base_snap", "cand_snap")
    assert result["paper_only"] is True

def test_validate_sandbox_input_safe_no_real_orders():
    result = validate_sandbox_input_safe("sid_001", "base_snap", "cand_snap")
    assert result["no_real_orders"] is True


# ── get_safety_flags ──────────────────────────────────────────────────────────

def test_get_safety_flags_returns_dict():
    result = get_safety_flags()
    assert isinstance(result, dict)

def test_get_safety_flags_paper_only():
    result = get_safety_flags()
    assert result["paper_only"] is True

def test_get_safety_flags_is_copy():
    result = get_safety_flags()
    result["paper_only"] = False
    assert SAFETY_FLAGS["paper_only"] is True


# ── get_hard_block_conditions ─────────────────────────────────────────────────

def test_get_hard_block_conditions_count_17():
    assert len(get_hard_block_conditions()) == 17

def test_get_hard_block_conditions_returns_list():
    assert isinstance(get_hard_block_conditions(), list)

def test_hard_block_has_live_strategy_activation():
    assert "live_strategy_activation_attempted" in HARD_BLOCK_CONDITIONS

def test_hard_block_has_real_order_requested():
    assert "real_order_requested" in HARD_BLOCK_CONDITIONS


# ── Constants counts ──────────────────────────────────────────────────────────

def test_forbidden_sandbox_actions_count_9():
    assert len(FORBIDDEN_SANDBOX_ACTIONS) == 9

def test_allowed_sandbox_actions_count_16():
    assert len(ALLOWED_SANDBOX_ACTIONS) == 16

def test_hard_block_conditions_count_17():
    assert len(HARD_BLOCK_CONDITIONS) == 17
