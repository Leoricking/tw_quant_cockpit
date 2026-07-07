"""tests/test_abc_gate_v172.py — Release gate tests for v1.7.2."""
import pytest
from release.abc_buy_point_execution_plan_release_gate_v172 import (
    run_release_gate, ABCBuyPointExecutionPlanReleaseGate, GATE_VERSION, MIN_CHECKS,
)


def test_gate_version():
    assert GATE_VERSION == "1.7.2"


def test_min_checks_at_least_70():
    assert MIN_CHECKS >= 70


def test_run_release_gate_returns_dict():
    result = run_release_gate()
    assert isinstance(result, dict)


def test_run_release_gate_passes():
    result = run_release_gate()
    assert result["gate_passed"] is True


def test_run_release_gate_status_pass():
    result = run_release_gate()
    assert result["status"] == "PASS"


def test_run_release_gate_no_failures():
    result = run_release_gate()
    assert result["failed_count"] == 0


def test_run_release_gate_at_least_70_checks():
    result = run_release_gate()
    assert result["total_count"] >= 70


def test_run_release_gate_passed_equals_total():
    result = run_release_gate()
    assert result["passed"] == result["total_count"]


def test_gate_class_instantiates():
    gate = ABCBuyPointExecutionPlanReleaseGate()
    assert gate is not None


def test_gate_has_checks_key():
    result = run_release_gate()
    assert "checks" in result


def test_gate_all_checks_pass():
    result = run_release_gate()
    for c in result["checks"]:
        assert c["passed"] is True, f"Gate check failed: {c['name']}: {c.get('detail')}"
