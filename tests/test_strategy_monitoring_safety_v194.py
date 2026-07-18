"""
tests/test_strategy_monitoring_safety_v194.py
Tests for strategy_monitoring_safety_v194.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_monitoring_safety_v194 import (
    SAFETY_FLAGS, FORBIDDEN_MONITORING_ACTIONS, ALLOWED_MONITORING_ACTIONS,
    HARD_BLOCK_CONDITIONS, run_safety_audit, is_safe_output_path,
    is_forbidden_action, is_allowed_action, validate_monitoring_action,
    has_forbidden_words, validate_monitoring_input_safe,
)


# ── SAFETY_FLAGS positive flags ───────────────────────────────────────────────

def test_safety_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True


def test_safety_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True


def test_safety_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True


def test_safety_monitoring_only():
    assert SAFETY_FLAGS["monitoring_only"] is True


def test_safety_drift_detection_only():
    assert SAFETY_FLAGS["drift_detection_only"] is True


def test_safety_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True


def test_safety_no_production_strategy_mutation():
    assert SAFETY_FLAGS["no_production_strategy_mutation"] is True


def test_safety_no_live_strategy_activation():
    assert SAFETY_FLAGS["no_live_strategy_activation"] is True


def test_safety_rollback_trigger_only():
    assert SAFETY_FLAGS["rollback_trigger_only"] is True


def test_safety_requires_manual_review():
    assert SAFETY_FLAGS["requires_manual_review"] is True


def test_safety_no_auto_rollback():
    assert SAFETY_FLAGS["no_auto_rollback"] is True


def test_safety_no_margin():
    assert SAFETY_FLAGS["no_margin"] is True


def test_safety_no_leverage():
    assert SAFETY_FLAGS["no_leverage"] is True


def test_safety_research_only():
    assert SAFETY_FLAGS["research_only"] is True


def test_safety_simulate_only():
    assert SAFETY_FLAGS["simulate_only"] is True


def test_safety_demo_only():
    assert SAFETY_FLAGS["demo_only"] is True


def test_safety_report_only():
    assert SAFETY_FLAGS["report_only"] is True


def test_safety_audit_only():
    assert SAFETY_FLAGS["audit_only"] is True


def test_safety_review_only():
    assert SAFETY_FLAGS["review_only"] is True


def test_safety_not_for_production():
    assert SAFETY_FLAGS["not_for_production"] is True


# ── SAFETY_FLAGS negative flags ───────────────────────────────────────────────

def test_safety_broker_execution_false():
    assert SAFETY_FLAGS["broker_execution"] is False


def test_safety_live_strategy_activation_false():
    assert SAFETY_FLAGS["live_strategy_activation"] is False


def test_safety_auto_rollback_false():
    assert SAFETY_FLAGS["auto_rollback"] is False


def test_safety_production_trading_false():
    assert SAFETY_FLAGS["production_trading"] is False


def test_safety_real_order_false():
    assert SAFETY_FLAGS["real_order"] is False


def test_safety_margin_trading_false():
    assert SAFETY_FLAGS["margin_trading"] is False


def test_safety_leverage_trading_false():
    assert SAFETY_FLAGS["leverage_trading"] is False


def test_safety_live_broker_connection_false():
    assert SAFETY_FLAGS["live_broker_connection"] is False


# ── forbidden actions ─────────────────────────────────────────────────────────

def test_forbidden_actions_count():
    assert len(FORBIDDEN_MONITORING_ACTIONS) == 9


def test_buy_is_forbidden():
    assert is_forbidden_action("BUY") is True


def test_sell_is_forbidden():
    assert is_forbidden_action("SELL") is True


def test_broker_order_is_forbidden():
    assert is_forbidden_action("BROKER_ORDER") is True


def test_monitor_is_not_forbidden():
    assert is_forbidden_action("MONITOR") is False


def test_drift_check_is_not_forbidden():
    assert is_forbidden_action("DRIFT_CHECK") is False


# ── allowed actions ───────────────────────────────────────────────────────────

def test_allowed_actions_count():
    assert len(ALLOWED_MONITORING_ACTIONS) == 16


def test_monitor_is_allowed():
    assert is_allowed_action("MONITOR") is True


def test_drift_check_is_allowed():
    assert is_allowed_action("DRIFT_CHECK") is True


def test_rollback_alert_is_allowed():
    assert is_allowed_action("ROLLBACK_ALERT") is True


def test_buy_is_not_allowed():
    assert is_allowed_action("BUY") is False


# ── hard block conditions ─────────────────────────────────────────────────────

def test_hard_block_conditions_count():
    assert len(HARD_BLOCK_CONDITIONS) == 20


def test_missing_promotion_package_source_in_hard_blocks():
    assert "missing_promotion_package_source" in HARD_BLOCK_CONDITIONS


def test_missing_rollback_plan_source_in_hard_blocks():
    assert "missing_rollback_plan_source" in HARD_BLOCK_CONDITIONS


def test_missing_baseline_monitoring_snapshot_in_hard_blocks():
    assert "missing_baseline_monitoring_snapshot" in HARD_BLOCK_CONDITIONS


def test_missing_current_monitoring_snapshot_in_hard_blocks():
    assert "missing_current_monitoring_snapshot" in HARD_BLOCK_CONDITIONS


def test_missing_monitoring_window_in_hard_blocks():
    assert "missing_monitoring_window" in HARD_BLOCK_CONDITIONS


def test_real_order_requested_in_hard_blocks():
    assert "real_order_requested" in HARD_BLOCK_CONDITIONS


def test_live_strategy_activation_attempted_in_hard_blocks():
    assert "live_strategy_activation_attempted" in HARD_BLOCK_CONDITIONS


def test_auto_rollback_attempted_in_hard_blocks():
    assert "auto_rollback_attempted" in HARD_BLOCK_CONDITIONS


# ── run_safety_audit ──────────────────────────────────────────────────────────

def test_safety_audit_returns_dict():
    assert isinstance(run_safety_audit(), dict)


def test_safety_audit_all_safe():
    assert run_safety_audit()["all_safe"] is True


def test_safety_audit_paper_only():
    assert run_safety_audit()["paper_only"] is True


def test_safety_audit_no_real_orders():
    assert run_safety_audit()["no_real_orders"] is True


def test_safety_audit_schema_version():
    assert run_safety_audit()["schema_version"] == "194"


# ── is_safe_output_path ───────────────────────────────────────────────────────

def test_safe_output_path_reports():
    assert is_safe_output_path("reports/") is True


def test_safe_output_path_exports():
    assert is_safe_output_path("exports/") is True


def test_unsafe_output_path_production():
    assert is_safe_output_path("production_strategy/") is False


def test_unsafe_output_path_live():
    assert is_safe_output_path("live_trading/") is False


# ── validate_monitoring_action ────────────────────────────────────────────────

def test_validate_monitoring_action_monitor():
    result = validate_monitoring_action("MONITOR")
    assert result["valid"] is True


def test_validate_monitoring_action_buy_blocked():
    result = validate_monitoring_action("BUY")
    assert result["blocked"] is True


def test_validate_monitoring_action_drift_check():
    result = validate_monitoring_action("DRIFT_CHECK")
    assert result["valid"] is True


# ── has_forbidden_words ───────────────────────────────────────────────────────

def test_has_forbidden_words_clean():
    assert has_forbidden_words("monitoring drift check") is False


def test_has_forbidden_words_buy():
    assert has_forbidden_words("please BUY now") is True


def test_has_forbidden_words_sell():
    assert has_forbidden_words("SELL order") is True


# ── validate_monitoring_input_safe ────────────────────────────────────────────

def test_validate_monitoring_input_safe_valid():
    inp = {"paper_only": True, "no_real_orders": True, "no_broker": True,
           "not_investment_advice": True, "monitoring_only": True}
    result = validate_monitoring_input_safe(inp)
    assert result["valid"] is True


def test_validate_monitoring_input_safe_missing_paper_only():
    inp = {"no_real_orders": True, "no_broker": True,
           "not_investment_advice": True, "monitoring_only": True}
    result = validate_monitoring_input_safe(inp)
    assert result["blocked"] is True


def test_validate_monitoring_input_safe_missing_no_real_orders():
    inp = {"paper_only": True, "no_broker": True,
           "not_investment_advice": True, "monitoring_only": True}
    result = validate_monitoring_input_safe(inp)
    assert result["blocked"] is True


def test_validate_monitoring_input_safe_missing_no_broker():
    inp = {"paper_only": True, "no_real_orders": True,
           "not_investment_advice": True, "monitoring_only": True}
    result = validate_monitoring_input_safe(inp)
    assert result["blocked"] is True


def test_validate_monitoring_input_safe_empty_dict():
    result = validate_monitoring_input_safe({})
    assert result["blocked"] is True
