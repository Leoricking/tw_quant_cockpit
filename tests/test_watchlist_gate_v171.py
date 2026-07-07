"""tests/test_watchlist_gate_v171.py — watchlist release gate tests for v1.7.1."""
import pytest
from release.watchlist_strategy_layer_release_gate_v171 import (
    run_release_gate, WatchlistStrategyLayerReleaseGate,
    GATE_VERSION, MIN_CHECKS,
)


def test_gate_version_constant():
    assert GATE_VERSION == "1.7.1"


def test_min_checks_constant():
    assert MIN_CHECKS == 65


def test_run_release_gate_returns_dict():
    result = run_release_gate()
    assert isinstance(result, dict)


def test_run_release_gate_passed():
    result = run_release_gate()
    assert result["gate_passed"] is True, (
        f"Gate failed: {[c for c in result['checks'] if not c['passed']]}"
    )


def test_run_release_gate_status_pass():
    result = run_release_gate()
    assert result["status"] == "PASS"


def test_run_release_gate_failed_zero():
    result = run_release_gate()
    assert result["failed_count"] == 0


def test_run_release_gate_total_ge_65():
    result = run_release_gate()
    assert result["total_count"] >= 65


def test_run_release_gate_version_key():
    result = run_release_gate()
    assert result["gate_version"] == "1.7.1"


def test_run_release_gate_checks_is_list():
    result = run_release_gate()
    assert isinstance(result["checks"], list)


def test_run_release_gate_paper_only():
    result = run_release_gate()
    assert result["paper_only"] is True


def test_run_release_gate_not_investment_advice():
    result = run_release_gate()
    assert result["not_investment_advice"] is True


def test_run_release_gate_no_real_orders():
    result = run_release_gate()
    assert result["no_real_orders"] is True


def test_run_release_gate_passed_plus_failed_equals_total():
    result = run_release_gate()
    assert result["passed_count"] + result["failed_count"] == result["total_count"]


def test_all_gate_checks_have_name():
    result = run_release_gate()
    for check in result["checks"]:
        assert "name" in check, f"Gate check missing 'name': {check}"


def test_all_gate_checks_have_passed():
    result = run_release_gate()
    for check in result["checks"]:
        assert "passed" in check, f"Gate check missing 'passed': {check}"


def test_all_gate_checks_passed_true():
    result = run_release_gate()
    failed = [c for c in result["checks"] if not c["passed"]]
    assert failed == [], f"Failed gate checks: {failed}"


def test_gate_class_instantiatable():
    gate = WatchlistStrategyLayerReleaseGate()
    assert gate is not None


def test_gate_class_run_returns_dict():
    gate = WatchlistStrategyLayerReleaseGate()
    result = gate.run()
    assert isinstance(result, dict)
    assert result["gate_passed"] is True
