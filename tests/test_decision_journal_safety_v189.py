"""
tests/test_decision_journal_safety_v189.py
Tests for decision_journal_safety_v189 — Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_journal_safety_v189 import (
    SAFETY_FLAGS, FORBIDDEN_JOURNAL_ACTIONS, ALLOWED_JOURNAL_ACTIONS,
    HARD_BLOCK_CONDITIONS, run_safety_audit, is_safe_output_path,
    is_forbidden_action, is_allowed_action, validate_journal_action,
    has_forbidden_words, validate_journal_entry_safe,
    get_safety_flags, get_hard_block_conditions,
    get_forbidden_journal_actions, get_allowed_journal_actions,
)


def test_safety_flag_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True


def test_safety_flag_research_only():
    assert SAFETY_FLAGS["research_only"] is True


def test_safety_flag_journal_only():
    assert SAFETY_FLAGS["journal_only"] is True


def test_safety_flag_review_only():
    assert SAFETY_FLAGS["review_only"] is True


def test_safety_flag_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True


def test_safety_flag_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True


def test_safety_flag_no_margin():
    assert SAFETY_FLAGS["no_margin"] is True


def test_safety_flag_no_leverage():
    assert SAFETY_FLAGS["no_leverage"] is True


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


def test_run_safety_audit_all_safe():
    result = run_safety_audit()
    assert result["all_safe"] is True


def test_run_safety_audit_no_errors():
    result = run_safety_audit()
    assert result["errors"] == []


def test_run_safety_audit_paper_only():
    assert run_safety_audit()["paper_only"] is True


def test_run_safety_audit_no_real_orders():
    assert run_safety_audit()["no_real_orders"] is True


def test_run_safety_audit_journal_only():
    assert run_safety_audit()["journal_only"] is True


def test_is_safe_output_path_reports():
    assert is_safe_output_path("reports/") is True


def test_is_safe_output_path_journal():
    assert is_safe_output_path("reports/journal/") is True


def test_is_safe_output_path_production_db_false():
    assert is_safe_output_path("production_db") is False


def test_is_safe_output_path_prod_db_false():
    assert is_safe_output_path("prod_db/exports") is False


def test_is_safe_output_path_broker_false():
    assert is_safe_output_path("broker/orders") is False


def test_is_safe_output_path_live_orders_false():
    assert is_safe_output_path("live_orders/") is False


def test_is_forbidden_action_buy():
    assert is_forbidden_action("BUY") is True


def test_is_forbidden_action_sell():
    assert is_forbidden_action("SELL") is True


def test_is_forbidden_action_order():
    assert is_forbidden_action("ORDER") is True


def test_is_forbidden_action_execute():
    assert is_forbidden_action("EXECUTE") is True


def test_is_forbidden_action_broker_order():
    assert is_forbidden_action("BROKER_ORDER") is True


def test_is_forbidden_action_auto_trade():
    assert is_forbidden_action("AUTO_TRADE") is True


def test_is_forbidden_action_real_trade():
    assert is_forbidden_action("REAL_TRADE") is True


def test_is_forbidden_action_live_trade():
    assert is_forbidden_action("LIVE_TRADE") is True


def test_is_forbidden_action_submit_order():
    assert is_forbidden_action("SUBMIT_ORDER") is True


def test_is_allowed_action_observe():
    assert is_allowed_action("OBSERVE") is True


def test_is_allowed_action_wait():
    assert is_allowed_action("WAIT") is True


def test_is_allowed_action_paper_plan_ready():
    assert is_allowed_action("PAPER_PLAN_READY") is True


def test_is_allowed_action_blocked():
    assert is_allowed_action("BLOCKED") is True


def test_is_allowed_action_audit_only():
    assert is_allowed_action("AUDIT_ONLY") is True


def test_is_allowed_action_buy_false():
    assert is_allowed_action("BUY") is False


def test_validate_journal_action_wait():
    assert validate_journal_action("WAIT") is True


def test_validate_journal_action_buy_false():
    assert validate_journal_action("BUY") is False


def test_validate_journal_action_decision_only():
    assert validate_journal_action("DECISION_ONLY") is True


def test_has_forbidden_words_buy():
    assert has_forbidden_words("We want to BUY this stock") is True


def test_has_forbidden_words_sell():
    assert has_forbidden_words("SELL order now") is True


def test_has_forbidden_words_clean_text():
    assert has_forbidden_words("This is a PAPER_PLAN_READY observation") is False


def test_validate_journal_entry_safe_valid():
    entry = {
        "paper_only": True, "no_real_orders": True, "no_broker": True,
        "not_investment_advice": True, "production_trading_blocked": True,
        "journal_only": True,
        "broker_execution": False, "real_order": False,
    }
    assert validate_journal_entry_safe(entry) is True


def test_validate_journal_entry_safe_missing_paper_only():
    entry = {
        "paper_only": False, "no_real_orders": True, "no_broker": True,
        "not_investment_advice": True, "production_trading_blocked": True,
        "journal_only": True,
    }
    assert validate_journal_entry_safe(entry) is False


def test_get_safety_flags_returns_dict():
    assert isinstance(get_safety_flags(), dict)


def test_get_safety_flags_paper_only():
    assert get_safety_flags()["paper_only"] is True


def test_get_hard_block_conditions_returns_list():
    assert isinstance(get_hard_block_conditions(), list)


def test_get_hard_block_conditions_count():
    assert len(get_hard_block_conditions()) == 18


def test_get_forbidden_journal_actions_returns_list():
    assert isinstance(get_forbidden_journal_actions(), list)


def test_get_forbidden_journal_actions_count():
    assert len(get_forbidden_journal_actions()) == 9


def test_get_allowed_journal_actions_returns_list():
    assert isinstance(get_allowed_journal_actions(), list)


def test_get_allowed_journal_actions_count():
    assert len(get_allowed_journal_actions()) == 16
