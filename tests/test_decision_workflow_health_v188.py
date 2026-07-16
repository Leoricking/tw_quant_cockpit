"""
tests/test_decision_workflow_health_v188.py
Tests for decision_workflow_health_v188 — Paper Decision Workflow Runner v1.8.8.
[!] Research Only. Paper Only. Workflow Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_workflow_health_v188 import (
    DecisionWorkflowHealthCheck, run_health_check,
)
from paper_trading.small_capital_strategy.decision_workflow_models_v188 import (
    WorkflowHealthSummary,
)


def test_run_health_check_returns_summary():
    result = run_health_check()
    assert isinstance(result, WorkflowHealthSummary)


def test_run_health_check_all_passed():
    result = run_health_check()
    assert result.all_passed is True


def test_run_health_check_zero_failures():
    result = run_health_check()
    assert result.failed == 0


def test_run_health_check_status_pass():
    result = run_health_check()
    assert result.status == "PASS"


def test_run_health_check_total_gte_60():
    result = run_health_check()
    assert result.total >= 60


def test_run_health_check_passed_equals_total():
    result = run_health_check()
    assert result.passed == result.total


def test_run_health_check_paper_only():
    result = run_health_check()
    assert result.paper_only is True


def test_run_health_check_no_real_orders():
    result = run_health_check()
    assert result.no_real_orders is True


def test_run_health_check_workflow_only():
    result = run_health_check()
    assert result.workflow_only is True


def test_health_check_class_run_returns_summary():
    hc = DecisionWorkflowHealthCheck()
    result = hc.run()
    assert isinstance(result, WorkflowHealthSummary)


def test_health_check_class_all_passed():
    hc = DecisionWorkflowHealthCheck()
    result = hc.run()
    assert result.all_passed is True


def test_health_check_schema_188():
    result = run_health_check()
    assert result.schema_version == "188"
