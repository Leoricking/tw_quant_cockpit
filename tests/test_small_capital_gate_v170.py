"""tests/test_small_capital_gate_v170.py — release gate tests for v1.7.0."""
import pytest
from release.small_capital_growth_strategy_release_gate_v170 import (
    SmallCapitalGrowthStrategyReleaseGate, run_release_gate, GATE_VERSION, MIN_CHECKS,
)


def test_gate_version():
    assert GATE_VERSION == "1.7.0"


def test_min_checks_70():
    assert MIN_CHECKS == 70


def test_run_release_gate_returns_dict():
    result = run_release_gate()
    assert isinstance(result, dict)


def test_run_release_gate_passed():
    result = run_release_gate()
    assert result["gate_passed"] is True


def test_run_release_gate_failed_count_zero():
    result = run_release_gate()
    assert result["failed_count"] == 0


def test_run_release_gate_total_gte_70():
    result = run_release_gate()
    assert result["total_count"] >= 70


def test_run_release_gate_passed_count_gte_70():
    result = run_release_gate()
    assert result["passed_count"] >= 70


def test_run_release_gate_checks_list():
    result = run_release_gate()
    assert isinstance(result["checks"], list)


def test_run_release_gate_all_checks_pass():
    result = run_release_gate()
    failed = [c for c in result["checks"] if not c["passed"]]
    assert failed == [], f"Failed gate checks: {[c['name'] for c in failed]}"


def test_run_release_gate_paper_only():
    result = run_release_gate()
    assert result["paper_only"] is True


def test_run_release_gate_no_real_orders():
    result = run_release_gate()
    assert result["no_real_orders"] is True


def test_gate_class_run():
    gate = SmallCapitalGrowthStrategyReleaseGate()
    result = gate.run()
    assert result["gate_passed"] is True


def test_gate_version_in_result():
    result = run_release_gate()
    assert result["gate_version"] == "1.7.0"
