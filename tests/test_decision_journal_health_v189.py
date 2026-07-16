"""
tests/test_decision_journal_health_v189.py
Tests for decision_journal_health_v189 — Paper Decision Journal & Review Loop v1.8.9.
[!] Research Only. Paper Only. Journal Only. Review Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_journal_health_v189 import (
    DecisionJournalHealthCheck, run_health_check,
)
from paper_trading.small_capital_strategy.decision_journal_models_v189 import JournalHealthSummary


def test_run_health_check_returns_health_summary():
    result = run_health_check()
    assert isinstance(result, JournalHealthSummary)


def test_health_check_all_passed():
    result = run_health_check()
    assert result.all_passed is True


def test_health_check_status_pass():
    result = run_health_check()
    assert result.status == "PASS"


def test_health_check_zero_failures():
    result = run_health_check()
    assert result.failed == 0


def test_health_check_total_at_least_60():
    result = run_health_check()
    assert result.total >= 60


def test_health_check_passed_equals_total():
    result = run_health_check()
    assert result.passed == result.total


def test_health_check_paper_only():
    result = run_health_check()
    assert result.paper_only is True


def test_health_check_journal_only():
    result = run_health_check()
    assert result.journal_only is True


def test_health_check_no_real_orders():
    result = run_health_check()
    assert result.no_real_orders is True


def test_health_check_not_investment_advice():
    result = run_health_check()
    assert result.not_investment_advice is True


def test_health_check_production_trading_blocked():
    result = run_health_check()
    assert result.production_trading_blocked is True


def test_health_check_instance_run():
    checker = DecisionJournalHealthCheck()
    result = checker.run()
    assert isinstance(result, JournalHealthSummary)


def test_health_check_instance_all_passed():
    checker = DecisionJournalHealthCheck()
    result = checker.run()
    assert result.all_passed is True


def test_health_check_schema_version():
    result = run_health_check()
    assert result.schema_version == "189"


def test_health_check_passed_not_zero():
    result = run_health_check()
    assert result.passed > 0


def test_health_check_multiple_runs_consistent():
    r1 = run_health_check()
    r2 = run_health_check()
    assert r1.passed == r2.passed
    assert r1.total == r2.total
    assert r1.status == r2.status


def test_health_check_audit_only():
    result = run_health_check()
    assert result.audit_only is True


def test_health_check_no_broker():
    result = run_health_check()
    assert result.no_broker is True
