"""
tests/test_paper_cockpit_v201.py
v2.0.1 Paper Cockpit — Main Test Suite (50+ tests)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
    VERSION, SCHEMA_VERSION, RELEASE_NAME, BASELINE_TESTS, MIN_NEW_TESTS,
    NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    NO_ENTRY_REASONS, DAILY_FINAL_ACTIONS, CLI_COMMANDS_V201, GUI_TABS_V201,
    ENHANCED_TICKET_FIELDS, FORBIDDEN_ACTIONS, SAFETY_FLAGS, COVERED_VERSIONS,
    _ALL_MODEL_NAMES_V201,
    DailyWorkflowInput, CandidateRankEntry, NoEntryReasonDetail,
    EnhancedDecisionTicket, RiskBudgetStatus, CLIDisplayRow, CLIDisplayOutput,
    DailyWorkflowCandidateResult, DailyWorkflowSummary, DailyWorkflowResult,
    V201HealthSummary, V201ReleaseSummary,
    run_daily_workflow, classify_final_action, evaluate_no_entry_reasons,
    build_enhanced_ticket, build_cli_display, build_candidate_ranking,
    get_risk_budget_status, get_version_info, verify_version, get_cockpit_summary_v201,
)


# --- Version tests ---

def test_version_is_201():
    assert VERSION == "2.0.1"

def test_schema_version_is_201():
    assert SCHEMA_VERSION == "201"

def test_release_name_contains_daily_workflow():
    assert "Daily Workflow" in RELEASE_NAME

def test_baseline_tests_value():
    assert BASELINE_TESTS == 32425

def test_min_new_tests_value():
    assert MIN_NEW_TESTS == 300

def test_verify_version_returns_true():
    assert verify_version() is True

def test_get_version_info_returns_dict():
    info = get_version_info()
    assert isinstance(info, dict)
    assert info["version"] == "2.0.1"
    assert info["schema_version"] == "201"
    assert info["paper_only"] is True
    assert info["no_real_orders"] is True
    assert info["NO_REAL_ORDERS"] is True
    assert info["BROKER_EXECUTION_ENABLED"] is False
    assert info["PRODUCTION_TRADING_BLOCKED"] is True


# --- Safety constants ---

def test_no_real_orders_true():
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_false():
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_true():
    assert PRODUCTION_TRADING_BLOCKED is True

def test_safety_flags_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True

def test_safety_flags_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True

def test_safety_flags_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True

def test_safety_flags_cockpit_executes_order_false():
    assert SAFETY_FLAGS["cockpit_executes_order"] is False

def test_safety_flags_broker_execution_enabled_false():
    assert SAFETY_FLAGS["broker_execution_enabled"] is False

def test_safety_flags_no_automatic_rebalance():
    assert SAFETY_FLAGS["no_automatic_rebalance"] is True

def test_safety_flags_no_real_account_sync():
    assert SAFETY_FLAGS["no_real_account_sync"] is True

def test_safety_flags_count():
    assert len(SAFETY_FLAGS) == 20

def test_forbidden_actions_contains_buy():
    assert "BUY" in FORBIDDEN_ACTIONS

def test_forbidden_actions_contains_sell():
    assert "SELL" in FORBIDDEN_ACTIONS

def test_forbidden_actions_contains_order():
    assert "ORDER" in FORBIDDEN_ACTIONS

def test_forbidden_actions_count():
    assert len(FORBIDDEN_ACTIONS) == 9

def test_paper_buy_plan_not_forbidden():
    assert "PAPER_BUY_PLAN" not in FORBIDDEN_ACTIONS


# --- NO_ENTRY_REASONS ---

def test_no_entry_reasons_count():
    assert len(NO_ENTRY_REASONS) == 13

def test_no_entry_reasons_contains_trend_broken():
    assert "trend_broken" in NO_ENTRY_REASONS

def test_no_entry_reasons_contains_human_review_required():
    assert "human_review_required" in NO_ENTRY_REASONS

def test_no_entry_reasons_all_strings():
    assert all(isinstance(r, str) for r in NO_ENTRY_REASONS)


# --- DAILY_FINAL_ACTIONS ---

def test_daily_final_actions_count():
    assert len(DAILY_FINAL_ACTIONS) == 7

def test_daily_final_actions_contains_watch():
    assert "WATCH" in DAILY_FINAL_ACTIONS

def test_daily_final_actions_contains_wait():
    assert "WAIT" in DAILY_FINAL_ACTIONS

def test_daily_final_actions_contains_paper_buy_plan():
    assert "PAPER_BUY_PLAN" in DAILY_FINAL_ACTIONS

def test_daily_final_actions_contains_paper_add_plan():
    assert "PAPER_ADD_PLAN" in DAILY_FINAL_ACTIONS

def test_daily_final_actions_contains_paper_reduce_plan():
    assert "PAPER_REDUCE_PLAN" in DAILY_FINAL_ACTIONS

def test_daily_final_actions_contains_paper_exit_plan():
    assert "PAPER_EXIT_PLAN" in DAILY_FINAL_ACTIONS

def test_daily_final_actions_contains_no_entry():
    assert "NO_ENTRY" in DAILY_FINAL_ACTIONS


# --- CLI/GUI constants ---

def test_cli_commands_count():
    assert len(CLI_COMMANDS_V201) == 10

def test_cli_commands_contains_daily_workflow():
    assert "paper-cockpit-daily-workflow" in CLI_COMMANDS_V201

def test_gui_tabs_count():
    assert len(GUI_TABS_V201) == 3

def test_gui_tabs_contains_daily_workflow():
    assert "daily_workflow_v201" in GUI_TABS_V201

def test_enhanced_ticket_fields_count():
    assert len(ENHANCED_TICKET_FIELDS) == 22

def test_covered_versions_count():
    assert len(COVERED_VERSIONS) == 30

def test_covered_versions_includes_200():
    assert "2.0.0" in COVERED_VERSIONS

def test_covered_versions_includes_170():
    assert "1.7.0" in COVERED_VERSIONS


# --- Models ---

def test_all_model_names_count():
    assert len(_ALL_MODEL_NAMES_V201) == 12

def test_daily_workflow_input_default():
    m = DailyWorkflowInput()
    assert m.schema_version == "201"
    assert m.paper_only is True
    assert m.no_real_orders is True
    assert m.capital_twd == 300000.0

def test_candidate_rank_entry_default():
    m = CandidateRankEntry()
    assert m.schema_version == "201"
    assert m.paper_only is True
    assert m.human_review_required is True

def test_no_entry_reason_detail_default():
    m = NoEntryReasonDetail()
    assert m.schema_version == "201"
    assert m.paper_only is True
    assert m.is_valid_reason is False

def test_no_entry_reason_detail_valid_reason():
    m = NoEntryReasonDetail(reason_code="trend_broken")
    assert m.is_valid_reason is True

def test_enhanced_decision_ticket_default():
    m = EnhancedDecisionTicket()
    assert m.schema_version == "201"
    assert m.paper_only is True
    assert m.ticket_triggers_broker is False
    assert m.ticket_executes_order is False
    assert m.human_review_required is True

def test_risk_budget_status_default():
    m = RiskBudgetStatus()
    assert m.schema_version == "201"
    assert m.paper_only is True
    assert m.human_review_required is True

def test_cli_display_row_default():
    m = CLIDisplayRow()
    assert m.schema_version == "201"
    assert m.paper_only is True
    assert m.human_review_flag is True

def test_cli_display_output_default():
    m = CLIDisplayOutput()
    assert m.schema_version == "201"
    assert m.paper_only is True
    assert m.no_real_orders is True
    assert m.human_review_required is True

def test_daily_workflow_candidate_result_default():
    m = DailyWorkflowCandidateResult()
    assert m.schema_version == "201"
    assert m.paper_only is True
    assert m.human_review_requirement is True

def test_daily_workflow_summary_default():
    m = DailyWorkflowSummary()
    assert m.schema_version == "201"
    assert m.paper_only is True

def test_daily_workflow_result_default():
    m = DailyWorkflowResult()
    assert m.schema_version == "201"
    assert m.paper_only is True
    assert m.cockpit_executes_order is False
    assert m.human_review_required is True

def test_v201_health_summary_default():
    m = V201HealthSummary()
    assert m.schema_version == "201"
    assert m.version == "2.0.1"
    assert m.no_entry_reasons_count == 13

def test_v201_release_summary_default():
    m = V201ReleaseSummary()
    assert m.schema_version == "201"
    assert m.version == "2.0.1"
    assert m.scenarios_count == 80
    assert m.fixtures_count == 80


# --- Engine functions ---

def test_run_daily_workflow_returns_result():
    result = run_daily_workflow()
    assert result is not None
    assert isinstance(result, DailyWorkflowResult)

def test_run_daily_workflow_paper_only():
    result = run_daily_workflow()
    assert result.paper_only is True

def test_run_daily_workflow_no_order():
    result = run_daily_workflow()
    assert result.cockpit_executes_order is False

def test_get_cockpit_summary_v201():
    summary = get_cockpit_summary_v201()
    assert isinstance(summary, dict)
    assert summary["version"] == "2.0.1"
    assert summary["paper_only"] is True
    assert summary["no_real_orders"] is True
    assert summary["NO_REAL_ORDERS"] is True
    assert summary["BROKER_EXECUTION_ENABLED"] is False
    assert summary["PRODUCTION_TRADING_BLOCKED"] is True
