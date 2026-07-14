"""
tests/test_decision_report_safety_v187.py
Tests for decision_report_safety_v187 — v1.8.7 Decision Report Export & Evidence Pack.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_report_safety_v187 import (
    SAFETY_FLAGS, _MUST_BE_TRUE, _MUST_BE_FALSE,
    FORBIDDEN_REPORT_ACTIONS, ALLOWED_REPORT_ACTIONS,
    UNSAFE_OUTPUT_PATHS, HARD_BLOCK_CONDITIONS,
    get_safety_flags, run_safety_audit, assert_safe,
    is_safe_output_path, is_forbidden_action, is_allowed_action,
    validate_report_action,
)


def test_safety_flag_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True


def test_safety_flag_research_only():
    assert SAFETY_FLAGS["research_only"] is True


def test_safety_flag_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True


def test_safety_flag_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True


def test_safety_flag_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True


def test_safety_flag_production_trading_blocked():
    assert SAFETY_FLAGS["production_trading_blocked"] is True


def test_safety_flag_report_only():
    assert SAFETY_FLAGS["report_only"] is True


def test_safety_flag_audit_only():
    assert SAFETY_FLAGS["audit_only"] is True


def test_safety_flag_broker_execution_false():
    assert SAFETY_FLAGS["broker_execution"] is False


def test_safety_flag_real_order_false():
    assert SAFETY_FLAGS["real_order"] is False


def test_safety_flag_real_trading_false():
    assert SAFETY_FLAGS["real_trading"] is False


def test_safety_flag_real_account_false():
    assert SAFETY_FLAGS["real_account"] is False


def test_run_safety_audit_all_safe():
    audit = run_safety_audit()
    assert audit["all_safe"] is True


def test_run_safety_audit_no_violations():
    audit = run_safety_audit()
    assert len(audit["violations"]) == 0


def test_run_safety_audit_schema_version():
    audit = run_safety_audit()
    assert audit["schema_version"] == "187"


def test_run_safety_audit_paper_only():
    audit = run_safety_audit()
    assert audit["paper_only"] is True


def test_run_safety_audit_forbidden_count():
    audit = run_safety_audit()
    assert audit["forbidden_actions_count"] >= 8


def test_run_safety_audit_allowed_count():
    audit = run_safety_audit()
    assert audit["allowed_actions_count"] >= 10


def test_assert_safe_does_not_raise():
    assert_safe()  # should not raise


def test_get_safety_flags_is_copy():
    flags = get_safety_flags()
    assert flags["paper_only"] is True
    # modify copy should not affect original
    flags["paper_only"] = False
    assert SAFETY_FLAGS["paper_only"] is True


def test_is_safe_output_path_reports_dir():
    assert is_safe_output_path("reports/daily_report.json") is True


def test_is_safe_output_path_export_dir():
    assert is_safe_output_path("export/output.md") is True


def test_is_safe_output_path_production_db():
    assert is_safe_output_path("production_db") is False


def test_is_safe_output_path_credentials():
    assert is_safe_output_path("credentials/secret.json") is False


def test_is_safe_output_path_live_session():
    assert is_safe_output_path("live_session/broker_conn") is False


def test_is_forbidden_action_buy():
    assert is_forbidden_action("BUY") is True


def test_is_forbidden_action_sell():
    assert is_forbidden_action("SELL") is True


def test_is_forbidden_action_execute():
    assert is_forbidden_action("EXECUTE") is True


def test_is_forbidden_action_order():
    assert is_forbidden_action("ORDER") is True


def test_is_forbidden_action_wait_not_forbidden():
    assert is_forbidden_action("WAIT") is False


def test_is_allowed_action_wait():
    assert is_allowed_action("WAIT") is True


def test_is_allowed_action_paper_plan_ready():
    assert is_allowed_action("PAPER_PLAN_READY") is True


def test_is_allowed_action_decision_only():
    assert is_allowed_action("DECISION_ONLY") is True


def test_is_allowed_action_buy_not_allowed():
    assert is_allowed_action("BUY") is False


def test_validate_report_action_wait():
    assert validate_report_action("WAIT") is True


def test_validate_report_action_paper_entry_allowed():
    assert validate_report_action("PAPER_ENTRY_ALLOWED") is True


def test_validate_report_action_buy_rejected():
    assert validate_report_action("BUY") is False


def test_validate_report_action_sell_rejected():
    assert validate_report_action("SELL") is False


def test_forbidden_report_actions_count():
    assert len(FORBIDDEN_REPORT_ACTIONS) >= 8


def test_allowed_report_actions_count():
    assert len(ALLOWED_REPORT_ACTIONS) >= 10


def test_hard_block_conditions_count():
    assert len(HARD_BLOCK_CONDITIONS) >= 10


def test_hard_block_conditions_includes_real_order():
    assert "real_order_requested" in HARD_BLOCK_CONDITIONS


def test_hard_block_conditions_includes_broker():
    assert "broker_requested" in HARD_BLOCK_CONDITIONS


def test_hard_block_conditions_includes_missing_audit():
    assert "missing_audit_trail" in HARD_BLOCK_CONDITIONS


def test_must_be_true_count():
    assert len(_MUST_BE_TRUE) >= 10


def test_must_be_false_count():
    assert len(_MUST_BE_FALSE) >= 4
