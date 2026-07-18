"""tests/test_strategy_promotion_health_v193.py — v1.9.3 health check tests."""
import pytest
from paper_trading.small_capital_strategy.strategy_promotion_health_v193 import (
    run_health_check,
)


def test_health_check_runs():
    result = run_health_check()
    assert result is not None

def test_health_status_pass():
    assert run_health_check().status == "PASS"

def test_health_failed_zero():
    assert run_health_check().failed == 0

def test_health_total_at_least_60():
    assert run_health_check().total >= 60

def test_health_passed_equals_total():
    h = run_health_check()
    assert h.passed == h.total

def test_health_all_passed_true():
    assert run_health_check().all_passed is True

def test_health_checks_is_list():
    assert isinstance(run_health_check().checks, list)

def test_health_checks_not_empty():
    assert len(run_health_check().checks) > 0

def test_health_paper_only():
    assert run_health_check().paper_only is True

def test_health_no_real_orders():
    assert run_health_check().no_real_orders is True

def test_health_promotion_package_only():
    assert run_health_check().promotion_package_only is True

def test_health_rollback_plan_only():
    assert run_health_check().rollback_plan_only is True

def test_health_schema_version():
    assert run_health_check().schema_version == "193"

def test_health_checks_all_passed():
    checks = run_health_check().checks
    assert all(c["passed"] for c in checks)

def test_health_check_names_unique():
    checks = run_health_check().checks
    names = [c["name"] for c in checks]
    assert len(names) == len(set(names))

def test_health_check_has_version_check():
    checks = run_health_check().checks
    names = [c["name"] for c in checks]
    assert any("version" in n for n in names)

def test_health_check_has_safety_check():
    checks = run_health_check().checks
    names = [c["name"] for c in checks]
    assert any("safety" in n for n in names)

def test_health_check_has_model_check():
    checks = run_health_check().checks
    names = [c["name"] for c in checks]
    assert any("model" in n for n in names)

def test_health_check_has_engine_check():
    checks = run_health_check().checks
    names = [c["name"] for c in checks]
    assert any("engine" in n for n in names)

def test_health_check_has_scenario_check():
    checks = run_health_check().checks
    names = [c["name"] for c in checks]
    assert any("scenario" in n for n in names)

def test_health_check_has_fixture_check():
    checks = run_health_check().checks
    names = [c["name"] for c in checks]
    assert any("fixture" in n for n in names)

def test_health_no_production_mutation():
    assert run_health_check().no_production_strategy_mutation is True

def test_health_not_investment_advice():
    assert run_health_check().not_investment_advice is True
