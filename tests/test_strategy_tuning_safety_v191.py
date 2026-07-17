"""tests/test_strategy_tuning_safety_v191.py
Tests for strategy tuning safety v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_tuning_safety_v191 import (
    SAFETY_FLAGS, FORBIDDEN_TUNING_ACTIONS, ALLOWED_TUNING_ACTIONS,
    HARD_BLOCK_CONDITIONS,
    run_safety_audit, is_safe_output_path, is_forbidden_action,
    is_allowed_action, validate_tuning_action, has_forbidden_words,
    validate_tuning_input_safe, get_safety_flags,
    get_hard_block_conditions, get_forbidden_tuning_actions,
    get_allowed_tuning_actions,
)


# ── SAFETY_FLAGS ──────────────────────────────────────────────────────────────

def test_safety_flag_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True

def test_safety_flag_research_only():
    assert SAFETY_FLAGS["research_only"] is True

def test_safety_flag_tuning_only():
    assert SAFETY_FLAGS["tuning_only"] is True

def test_safety_flag_guardrail_only():
    assert SAFETY_FLAGS["guardrail_only"] is True

def test_safety_flag_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True

def test_safety_flag_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True

def test_safety_flag_no_margin():
    assert SAFETY_FLAGS["no_margin"] is True

def test_safety_flag_no_leverage():
    assert SAFETY_FLAGS["no_leverage"] is True

def test_safety_flag_no_production_mutation():
    assert SAFETY_FLAGS["no_production_strategy_mutation"] is True

def test_safety_flag_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True

def test_safety_flag_production_trading_blocked():
    assert SAFETY_FLAGS["production_trading_blocked"] is True

def test_safety_flag_broker_execution_false():
    assert SAFETY_FLAGS["broker_execution"] is False

def test_safety_flag_real_order_false():
    assert SAFETY_FLAGS["real_order"] is False

def test_safety_flag_live_trade_false():
    assert SAFETY_FLAGS["live_trade"] is False

def test_safety_flag_margin_enabled_false():
    assert SAFETY_FLAGS["margin_enabled"] is False

def test_safety_flag_leverage_enabled_false():
    assert SAFETY_FLAGS["leverage_enabled"] is False

def test_safety_flag_production_db_write_false():
    assert SAFETY_FLAGS["production_db_write"] is False

def test_safety_flag_production_strategy_mutation_false():
    assert SAFETY_FLAGS["production_strategy_mutation"] is False


# ── run_safety_audit ──────────────────────────────────────────────────────────

def test_run_safety_audit_returns_dict():
    assert isinstance(run_safety_audit(), dict)

def test_run_safety_audit_all_safe():
    assert run_safety_audit()["all_safe"] is True

def test_run_safety_audit_no_issues():
    result = run_safety_audit()
    assert result["issues"] == []

def test_run_safety_audit_paper_only():
    assert run_safety_audit()["paper_only"] is True

def test_run_safety_audit_no_real_orders():
    assert run_safety_audit()["no_real_orders"] is True

def test_run_safety_audit_schema_191():
    assert run_safety_audit()["schema_version"] == "191"


# ── is_safe_output_path ───────────────────────────────────────────────────────

def test_safe_path_reports():
    assert is_safe_output_path("reports/") is True

def test_safe_path_exports():
    assert is_safe_output_path("exports/") is True

def test_safe_path_paper_reports():
    assert is_safe_output_path("paper_reports/") is True

def test_unsafe_path_production_db():
    assert is_safe_output_path("production_db/") is False

def test_unsafe_path_prod_db():
    assert is_safe_output_path("prod_db/reports/") is False

def test_unsafe_path_broker():
    assert is_safe_output_path("broker/orders/") is False

def test_unsafe_path_production_strategy():
    assert is_safe_output_path("production_strategy/") is False

def test_unsafe_path_real_orders():
    assert is_safe_output_path("real_orders/") is False

def test_safe_path_empty_returns_false():
    assert is_safe_output_path("") is False


# ── is_forbidden_action ───────────────────────────────────────────────────────

def test_forbidden_action_buy():
    assert is_forbidden_action("BUY") is True

def test_forbidden_action_sell():
    assert is_forbidden_action("SELL") is True

def test_forbidden_action_order():
    assert is_forbidden_action("ORDER") is True

def test_forbidden_action_execute():
    assert is_forbidden_action("EXECUTE") is True

def test_forbidden_action_submit_order():
    assert is_forbidden_action("SUBMIT_ORDER") is True

def test_forbidden_action_auto_trade():
    assert is_forbidden_action("AUTO_TRADE") is True

def test_forbidden_action_real_trade():
    assert is_forbidden_action("REAL_TRADE") is True

def test_forbidden_action_live_trade():
    assert is_forbidden_action("LIVE_TRADE") is True

def test_forbidden_action_broker_order():
    assert is_forbidden_action("BROKER_ORDER") is True

def test_forbidden_action_case_insensitive_buy():
    assert is_forbidden_action("buy") is True


# ── is_allowed_action ─────────────────────────────────────────────────────────

def test_allowed_action_tune():
    assert is_allowed_action("TUNE") is True

def test_allowed_action_review():
    assert is_allowed_action("REVIEW") is True

def test_allowed_action_analyze():
    assert is_allowed_action("ANALYZE") is True

def test_allowed_action_report():
    assert is_allowed_action("REPORT") is True

def test_allowed_action_guardrail_check():
    assert is_allowed_action("GUARDRAIL_CHECK") is True

def test_allowed_action_rule_tuning():
    assert is_allowed_action("RULE_TUNING") is True

def test_allowed_action_guardrail_review():
    assert is_allowed_action("GUARDRAIL_REVIEW") is True

def test_allowed_action_health_check():
    assert is_allowed_action("HEALTH_CHECK") is True

def test_not_allowed_action_buy():
    assert is_allowed_action("BUY") is False

def test_allowed_action_case_insensitive():
    assert is_allowed_action("tune") is True


# ── validate_tuning_action ────────────────────────────────────────────────────

def test_validate_action_allowed():
    result = validate_tuning_action("TUNE")
    assert result["valid"] is True
    assert result["blocked"] is False

def test_validate_action_forbidden():
    result = validate_tuning_action("BUY")
    assert result["valid"] is False
    assert result["blocked"] is True

def test_validate_action_unknown():
    result = validate_tuning_action("UNKNOWN_ACTION")
    assert result["valid"] is False
    assert result["blocked"] is False

def test_validate_action_paper_only_in_result():
    assert validate_tuning_action("TUNE")["paper_only"] is True

def test_validate_action_no_real_orders_in_result():
    assert validate_tuning_action("BUY")["no_real_orders"] is True


# ── has_forbidden_words ───────────────────────────────────────────────────────

def test_has_forbidden_words_buy():
    assert has_forbidden_words("this contains BUY signal") is True

def test_has_forbidden_words_submit_order():
    assert has_forbidden_words("SUBMIT_ORDER now") is True

def test_has_forbidden_words_clean_text():
    assert has_forbidden_words("this is a safe review text") is False

def test_has_forbidden_words_case_insensitive():
    assert has_forbidden_words("execute this") is True

def test_has_forbidden_words_empty():
    assert has_forbidden_words("") is False


# ── validate_tuning_input_safe ────────────────────────────────────────────────

def test_validate_tuning_input_valid():
    result = validate_tuning_input_safe("tuning_001", "perf_source", "journal_source")
    assert result["valid"] is True
    assert result["errors"] == []

def test_validate_tuning_input_missing_id():
    result = validate_tuning_input_safe("", "perf", "journal")
    assert result["valid"] is False
    assert "missing_tuning_id" in result["errors"]

def test_validate_tuning_input_missing_performance_source():
    result = validate_tuning_input_safe("t1", "", "journal")
    assert result["valid"] is False
    assert "missing_performance_source" in result["errors"]

def test_validate_tuning_input_missing_journal_source():
    result = validate_tuning_input_safe("t1", "perf", "")
    assert result["valid"] is False
    assert "missing_journal_source" in result["errors"]

def test_validate_tuning_input_forbidden_word_in_id():
    result = validate_tuning_input_safe("BUY_SIGNALS", "perf", "journal")
    assert result["valid"] is False
    assert "forbidden_action_words" in result["errors"]

def test_validate_tuning_input_paper_only_in_result():
    result = validate_tuning_input_safe("t1", "p1", "j1")
    assert result["paper_only"] is True

def test_validate_tuning_input_no_production_mutation_in_result():
    result = validate_tuning_input_safe("t1", "p1", "j1")
    assert result["no_production_strategy_mutation"] is True


# ── getter functions ──────────────────────────────────────────────────────────

def test_get_safety_flags_returns_dict():
    assert isinstance(get_safety_flags(), dict)

def test_get_safety_flags_not_same_object():
    assert get_safety_flags() is not SAFETY_FLAGS

def test_get_hard_block_conditions_count():
    assert len(get_hard_block_conditions()) == 17

def test_get_hard_block_conditions_has_real_order():
    assert "real_order_requested" in get_hard_block_conditions()

def test_get_forbidden_tuning_actions_count():
    assert len(get_forbidden_tuning_actions()) == 9

def test_get_allowed_tuning_actions_count():
    assert len(get_allowed_tuning_actions()) == 16
