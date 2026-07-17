"""tests/test_strategy_tuning_health_v191.py
Tests for strategy tuning health check v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_tuning_health_v191 import (
    StrategyTuningHealthCheck, run_health_check,
)


def test_run_health_check_returns_summary():
    from paper_trading.small_capital_strategy.strategy_tuning_models_v191 import RuleTuningHealthSummary
    result = run_health_check()
    assert isinstance(result, RuleTuningHealthSummary)

def test_health_check_all_passed():
    result = run_health_check()
    assert result.all_passed is True

def test_health_check_status_pass():
    result = run_health_check()
    assert result.status == "PASS"

def test_health_check_zero_failures():
    result = run_health_check()
    assert result.failed == 0

def test_health_check_total_ge_60():
    result = run_health_check()
    assert result.total >= 60

def test_health_check_passed_equals_total():
    result = run_health_check()
    assert result.passed == result.total

def test_health_check_checks_is_list():
    result = run_health_check()
    assert isinstance(result.checks, list)

def test_health_check_all_checks_have_name():
    result = run_health_check()
    assert all("name" in c for c in result.checks)

def test_health_check_all_checks_have_passed():
    result = run_health_check()
    assert all("passed" in c for c in result.checks)

def test_health_check_paper_only():
    result = run_health_check()
    assert result.paper_only is True

def test_health_check_research_only():
    result = run_health_check()
    assert result.research_only is True

def test_health_check_tuning_only():
    result = run_health_check()
    assert result.tuning_only is True

def test_health_check_no_real_orders():
    result = run_health_check()
    assert result.no_real_orders is True

def test_health_check_schema_191():
    result = run_health_check()
    assert result.schema_version == "191"

def test_health_check_instantiation():
    checker = StrategyTuningHealthCheck()
    assert checker is not None

def test_health_check_run_method():
    checker = StrategyTuningHealthCheck()
    result = checker.run()
    assert result.all_passed is True
