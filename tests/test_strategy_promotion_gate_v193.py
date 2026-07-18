"""tests/test_strategy_promotion_gate_v193.py — v1.9.3 release gate tests."""
import pytest
from release.strategy_promotion_release_gate_v193 import (
    StrategyPromotionReleaseGate, run_release_gate,
)


def test_gate_runs():
    result = run_release_gate()
    assert result is not None

def test_gate_passed():
    assert run_release_gate()["gate_passed"] is True

def test_gate_failed_zero():
    assert run_release_gate()["failed"] == 0

def test_gate_version():
    assert run_release_gate()["version"] == "1.9.3"

def test_gate_release_name():
    assert run_release_gate()["release_name"] == "Paper Strategy Promotion Package & Rollback Plan Lab"

def test_gate_paper_only():
    assert run_release_gate()["paper_only"] is True

def test_gate_research_only():
    assert run_release_gate()["research_only"] is True

def test_gate_promotion_package_only():
    assert run_release_gate()["promotion_package_only"] is True

def test_gate_rollback_plan_only():
    assert run_release_gate()["rollback_plan_only"] is True

def test_gate_no_real_orders():
    assert run_release_gate()["no_real_orders"] is True

def test_gate_no_broker():
    assert run_release_gate()["no_broker"] is True

def test_gate_not_investment_advice():
    assert run_release_gate()["not_investment_advice"] is True

def test_gate_schema_version():
    assert run_release_gate()["schema_version"] == "193"

def test_gate_results_is_list():
    assert isinstance(run_release_gate()["results"], list)

def test_gate_results_not_empty():
    assert len(run_release_gate()["results"]) > 0

def test_gate_passed_count_positive():
    assert run_release_gate()["passed"] > 0

def test_gate_total_at_least_60():
    assert run_release_gate()["total"] >= 60

def test_gate_all_results_passed():
    results = run_release_gate()["results"]
    assert all(r["passed"] for r in results)

def test_gate_result_names_unique():
    results = run_release_gate()["results"]
    names = [r["name"] for r in results]
    assert len(names) == len(set(names))

def test_gate_class_baseline_tests():
    assert StrategyPromotionReleaseGate.BASELINE_TESTS == 27847

def test_gate_class_min_new_tests():
    assert StrategyPromotionReleaseGate.MIN_NEW_TESTS == 400

def test_gate_class_version():
    assert StrategyPromotionReleaseGate.VERSION == "1.9.3"

def test_gate_class_min_scenarios():
    assert StrategyPromotionReleaseGate.MIN_SCENARIOS == 75

def test_gate_class_min_fixtures():
    assert StrategyPromotionReleaseGate.MIN_FIXTURES == 75

def test_gate_class_min_cli():
    assert StrategyPromotionReleaseGate.MIN_CLI == 18

def test_gate_class_min_health_checks():
    assert StrategyPromotionReleaseGate.MIN_HEALTH_CHECKS == 60

def test_gate_instance_run_returns_dict():
    gate = StrategyPromotionReleaseGate()
    result = gate.run()
    assert isinstance(result, dict)

def test_gate_has_version_gate():
    results = run_release_gate()["results"]
    names = [r["name"] for r in results]
    assert any("version" in n for n in names)

def test_gate_has_safety_gate():
    results = run_release_gate()["results"]
    names = [r["name"] for r in results]
    assert any("safety" in n for n in names)
