"""tests/test_decision_performance_gate_v190.py
Tests for decision performance release gate v1.9.0.
[!] Research Only. Paper Only.
"""
import pytest
from release.decision_performance_release_gate_v190 import (
    DecisionPerformanceReleaseGate, run_release_gate,
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


def test_release_gate_passed_at_least_70():
    result = run_release_gate()
    assert result["passed"] >= 70


def test_release_gate_total_at_least_70():
    result = run_release_gate()
    assert result["total"] >= 70


def test_release_gate_version():
    result = run_release_gate()
    assert result["version"] == "1.9.0"


def test_release_gate_release_name():
    result = run_release_gate()
    assert result["release_name"] == "Paper Trading Performance Review & Strategy Improvement Lab"


def test_release_gate_paper_only():
    result = run_release_gate()
    assert result["paper_only"] is True


def test_release_gate_no_real_orders():
    result = run_release_gate()
    assert result["no_real_orders"] is True


def test_release_gate_performance_review_only():
    result = run_release_gate()
    assert result["performance_review_only"] is True


def test_release_gate_strategy_improvement_only():
    result = run_release_gate()
    assert result["strategy_improvement_only"] is True


def test_release_gate_no_broker():
    result = run_release_gate()
    assert result["no_broker"] is True


def test_release_gate_not_investment_advice():
    result = run_release_gate()
    assert result["not_investment_advice"] is True


def test_release_gate_production_trading_blocked():
    result = run_release_gate()
    assert result["production_trading_blocked"] is True


def test_release_gate_research_only():
    result = run_release_gate()
    assert result["research_only"] is True


def test_release_gate_audit_only():
    result = run_release_gate()
    assert result["audit_only"] is True


def test_release_gate_review_only():
    result = run_release_gate()
    assert result["review_only"] is True


def test_release_gate_all_results_passed():
    result = run_release_gate()
    for r in result["results"]:
        assert r["passed"] is True, f"Gate check failed: {r['name']} — {r.get('error', '')}"


def test_release_gate_results_key_present():
    result = run_release_gate()
    assert "results" in result


def test_release_gate_results_is_list():
    result = run_release_gate()
    assert isinstance(result["results"], list)


def test_release_gate_version_constant():
    assert DecisionPerformanceReleaseGate.VERSION == "1.9.0"


def test_release_gate_min_scenarios_constant():
    assert DecisionPerformanceReleaseGate.MIN_SCENARIOS == 75


def test_release_gate_min_fixtures_constant():
    assert DecisionPerformanceReleaseGate.MIN_FIXTURES == 75


def test_release_gate_min_cli_constant():
    assert DecisionPerformanceReleaseGate.MIN_CLI == 18


def test_release_gate_baseline_tests_constant():
    assert DecisionPerformanceReleaseGate.BASELINE_TESTS == 26157


def test_release_gate_min_new_tests_constant():
    assert DecisionPerformanceReleaseGate.MIN_NEW_TESTS == 400


def test_release_gate_min_scenarios():
    result = run_release_gate()
    assert result["min_scenarios"] == 75


def test_release_gate_min_fixtures():
    result = run_release_gate()
    assert result["min_fixtures"] == 75


def test_release_gate_min_cli():
    result = run_release_gate()
    assert result["min_cli"] == 18
