"""tests/test_strategy_tuning_gate_v191.py
Tests for strategy tuning release gate v1.9.1.
[!] Research Only. Paper Only. Tuning Only. Guardrail Only.
"""
import pytest
from release.strategy_tuning_release_gate_v191 import (
    StrategyTuningReleaseGate, run_release_gate,
)


def test_run_release_gate_returns_dict():
    result = run_release_gate()
    assert isinstance(result, dict)

def test_release_gate_passed():
    result = run_release_gate()
    assert result["gate_passed"] is True

def test_release_gate_status_pass():
    result = run_release_gate()
    assert result["status"] == "PASS"

def test_release_gate_zero_failures():
    result = run_release_gate()
    assert result["failed"] == 0

def test_release_gate_passed_at_least_80():
    result = run_release_gate()
    assert result["passed"] >= 80

def test_release_gate_total_at_least_80():
    result = run_release_gate()
    assert result["total"] >= 80

def test_release_gate_version():
    result = run_release_gate()
    assert result["version"] == "1.9.1"

def test_release_gate_release_name():
    result = run_release_gate()
    assert result["release_name"] == "Paper Strategy Rule Tuning & Guardrail Lab"

def test_release_gate_paper_only():
    result = run_release_gate()
    assert result["paper_only"] is True

def test_release_gate_no_real_orders():
    result = run_release_gate()
    assert result["no_real_orders"] is True

def test_release_gate_tuning_only():
    result = run_release_gate()
    assert result["tuning_only"] is True

def test_release_gate_guardrail_only():
    result = run_release_gate()
    assert result["guardrail_only"] is True

def test_release_gate_no_production_mutation():
    result = run_release_gate()
    assert result["no_production_strategy_mutation"] is True

def test_release_gate_not_investment_advice():
    result = run_release_gate()
    assert result["not_investment_advice"] is True

def test_release_gate_no_broker():
    result = run_release_gate()
    assert result["no_broker"] is True

def test_release_gate_production_blocked():
    result = run_release_gate()
    assert result["production_trading_blocked"] is True

def test_release_gate_results_is_list():
    result = run_release_gate()
    assert isinstance(result["results"], list)

def test_release_gate_min_scenarios():
    result = run_release_gate()
    assert result["min_scenarios"] == 75

def test_release_gate_min_fixtures():
    result = run_release_gate()
    assert result["min_fixtures"] == 75

def test_release_gate_min_cli():
    result = run_release_gate()
    assert result["min_cli"] == 18

def test_release_gate_baseline_tests():
    result = run_release_gate()
    assert result["baseline_tests"] == 26649

def test_release_gate_min_new_tests():
    result = run_release_gate()
    assert result["min_new_tests"] == 400

def test_release_gate_all_results_have_name():
    result = run_release_gate()
    assert all("name" in r for r in result["results"])

def test_release_gate_all_results_have_passed():
    result = run_release_gate()
    assert all("passed" in r for r in result["results"])

def test_release_gate_class_version():
    assert StrategyTuningReleaseGate.VERSION == "1.9.1"

def test_release_gate_class_release_name():
    assert StrategyTuningReleaseGate.RELEASE_NAME == "Paper Strategy Rule Tuning & Guardrail Lab"

def test_release_gate_class_min_scenarios():
    assert StrategyTuningReleaseGate.MIN_SCENARIOS == 75

def test_release_gate_class_min_fixtures():
    assert StrategyTuningReleaseGate.MIN_FIXTURES == 75
