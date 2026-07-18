"""
tests/test_strategy_monitoring_gate_v194.py
Tests for strategy_monitoring_release_gate_v194.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only. No Real Orders. Not Investment Advice.
"""
import pytest
from release.strategy_monitoring_release_gate_v194 import (
    StrategyMonitoringReleaseGate, run_release_gate,
)


@pytest.fixture(scope="module")
def gate_result():
    return run_release_gate()


def test_gate_result_is_dict(gate_result):
    assert isinstance(gate_result, dict)


def test_gate_passed(gate_result):
    assert gate_result["gate_passed"] is True


def test_gate_version(gate_result):
    assert gate_result["version"] == "1.9.4"


def test_gate_paper_only(gate_result):
    assert gate_result["paper_only"] is True


def test_gate_no_real_orders(gate_result):
    assert gate_result["no_real_orders"] is True


def test_gate_monitoring_only(gate_result):
    assert gate_result["monitoring_only"] is True


def test_gate_drift_detection_only(gate_result):
    assert gate_result["drift_detection_only"] is True


def test_gate_not_investment_advice(gate_result):
    assert gate_result["not_investment_advice"] is True


def test_gate_schema_version(gate_result):
    assert gate_result["schema_version"] == "194"


def test_gate_failed_zero(gate_result):
    assert gate_result["failed"] == 0


def test_gate_passed_count_positive(gate_result):
    assert gate_result["passed"] > 0


def test_gate_total_positive(gate_result):
    assert gate_result["total"] > 0


def test_gate_results_is_list(gate_result):
    assert isinstance(gate_result["results"], list)


def test_gate_all_results_passed(gate_result):
    for r in gate_result["results"]:
        assert r["passed"] is True, f"Gate check failed: {r['name']} — {r.get('error')}"


def test_gate_research_only(gate_result):
    assert gate_result["research_only"] is True


def test_gate_no_broker(gate_result):
    assert gate_result["no_broker"] is True


def test_gate_no_auto_rollback(gate_result):
    assert gate_result.get("no_auto_rollback") is True


def test_gate_class_version():
    assert StrategyMonitoringReleaseGate.VERSION == "1.9.4"


def test_gate_class_release_name():
    assert StrategyMonitoringReleaseGate.RELEASE_NAME == "Paper Strategy Monitoring & Drift Detection Lab"


def test_gate_class_min_scenarios():
    assert StrategyMonitoringReleaseGate.MIN_SCENARIOS == 75


def test_gate_class_min_fixtures():
    assert StrategyMonitoringReleaseGate.MIN_FIXTURES == 75


def test_gate_class_baseline_tests():
    assert StrategyMonitoringReleaseGate.BASELINE_TESTS == 28407


def test_gate_class_min_new_tests():
    assert StrategyMonitoringReleaseGate.MIN_NEW_TESTS == 400
