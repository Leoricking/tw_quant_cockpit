"""
tests/test_paper_cockpit_safety_v201.py
v2.0.1 Paper Cockpit — Safety Tests (25+ tests)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from paper_trading.small_capital_strategy.paper_cockpit_v201 import (
    NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    SAFETY_FLAGS, FORBIDDEN_ACTIONS, DAILY_FINAL_ACTIONS,
    run_daily_workflow, DailyWorkflowInput, build_enhanced_ticket,
    get_cockpit_summary_v201, verify_version,
)


# --- Module-level safety constants ---

def test_no_real_orders_is_true():
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_is_false():
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_is_true():
    assert PRODUCTION_TRADING_BLOCKED is True


# --- SAFETY_FLAGS ---

def test_safety_flags_paper_only():
    assert SAFETY_FLAGS["paper_only"] is True

def test_safety_flags_research_only():
    assert SAFETY_FLAGS["research_only"] is True

def test_safety_flags_simulate_only():
    assert SAFETY_FLAGS["simulate_only"] is True

def test_safety_flags_no_real_orders():
    assert SAFETY_FLAGS["no_real_orders"] is True

def test_safety_flags_no_broker():
    assert SAFETY_FLAGS["no_broker"] is True

def test_safety_flags_no_margin():
    assert SAFETY_FLAGS["no_margin"] is True

def test_safety_flags_no_leverage():
    assert SAFETY_FLAGS["no_leverage"] is True

def test_safety_flags_not_investment_advice():
    assert SAFETY_FLAGS["not_investment_advice"] is True

def test_safety_flags_human_review_required():
    assert SAFETY_FLAGS["human_review_required"] is True

def test_safety_flags_production_trading_blocked():
    assert SAFETY_FLAGS["production_trading_blocked"] is True

def test_safety_flags_cockpit_executes_order_false():
    assert SAFETY_FLAGS["cockpit_executes_order"] is False

def test_safety_flags_cockpit_mutates_strategy_false():
    assert SAFETY_FLAGS["cockpit_mutates_strategy"] is False

def test_safety_flags_broker_execution_enabled_false():
    assert SAFETY_FLAGS["broker_execution_enabled"] is False

def test_safety_flags_no_automatic_rebalance():
    assert SAFETY_FLAGS["no_automatic_rebalance"] is True

def test_safety_flags_no_real_account_sync():
    assert SAFETY_FLAGS["no_real_account_sync"] is True


# --- FORBIDDEN_ACTIONS ---

def test_forbidden_actions_contains_buy():
    assert "BUY" in FORBIDDEN_ACTIONS

def test_forbidden_actions_contains_sell():
    assert "SELL" in FORBIDDEN_ACTIONS

def test_forbidden_actions_contains_order():
    assert "ORDER" in FORBIDDEN_ACTIONS

def test_forbidden_actions_contains_execute():
    assert "EXECUTE" in FORBIDDEN_ACTIONS

def test_forbidden_actions_contains_submit_order():
    assert "SUBMIT_ORDER" in FORBIDDEN_ACTIONS

def test_forbidden_actions_contains_auto_trade():
    assert "AUTO_TRADE" in FORBIDDEN_ACTIONS

def test_forbidden_actions_contains_real_trade():
    assert "REAL_TRADE" in FORBIDDEN_ACTIONS

def test_forbidden_actions_contains_live_trade():
    assert "LIVE_TRADE" in FORBIDDEN_ACTIONS

def test_forbidden_actions_contains_broker_order():
    assert "BROKER_ORDER" in FORBIDDEN_ACTIONS


# --- Allowed PLAN actions are not forbidden ---

def test_paper_buy_plan_not_forbidden():
    assert "PAPER_BUY_PLAN" not in FORBIDDEN_ACTIONS

def test_paper_add_plan_not_forbidden():
    assert "PAPER_ADD_PLAN" not in FORBIDDEN_ACTIONS

def test_paper_reduce_plan_not_forbidden():
    assert "PAPER_REDUCE_PLAN" not in FORBIDDEN_ACTIONS

def test_paper_exit_plan_not_forbidden():
    assert "PAPER_EXIT_PLAN" not in FORBIDDEN_ACTIONS


# --- Workflow safety ---

def test_workflow_result_cockpit_executes_order_false():
    result = run_daily_workflow()
    assert result.cockpit_executes_order is False

def test_workflow_result_paper_only():
    result = run_daily_workflow()
    assert result.paper_only is True

def test_workflow_result_no_broker():
    result = run_daily_workflow()
    assert result.no_broker is True

def test_workflow_result_human_review_required():
    result = run_daily_workflow()
    assert result.human_review_required is True

def test_workflow_candidate_human_review_requirement():
    inp = DailyWorkflowInput(candidates=["2330"])
    result = run_daily_workflow(inp)
    for cr in result.candidate_results:
        assert cr.human_review_requirement is True

def test_ticket_triggers_broker_false():
    t = build_enhanced_ticket("2330")
    assert t.ticket_triggers_broker is False

def test_ticket_executes_order_false():
    t = build_enhanced_ticket("2330")
    assert t.ticket_executes_order is False

def test_cockpit_summary_no_real_orders():
    summary = get_cockpit_summary_v201()
    assert summary["NO_REAL_ORDERS"] is True

def test_cockpit_summary_broker_disabled():
    summary = get_cockpit_summary_v201()
    assert summary["BROKER_EXECUTION_ENABLED"] is False

def test_cockpit_summary_production_blocked():
    summary = get_cockpit_summary_v201()
    assert summary["PRODUCTION_TRADING_BLOCKED"] is True

def test_verify_version_returns_true():
    assert verify_version() is True

def test_daily_final_actions_no_bare_buy():
    for action in DAILY_FINAL_ACTIONS:
        assert action != "BUY", "BUY is a forbidden action"

def test_daily_final_actions_no_bare_sell():
    for action in DAILY_FINAL_ACTIONS:
        assert action != "SELL", "SELL is a forbidden action"
