"""
tests/test_simulation_matrix_health_v181.py
Tests for simulation_matrix_health_v181 — health checks.
[!] Research Only. Paper Only. Simulate Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.simulation_matrix_health_v181 import (
    run_health_check, MIN_HEALTH_CHECKS,
)
from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import ScenarioMatrixHealthSummary


# ── MIN_HEALTH_CHECKS constant ─────────────────────────────────────────────────

def test_min_health_checks_ge_60():
    assert MIN_HEALTH_CHECKS >= 60

def test_min_health_checks_is_int():
    assert isinstance(MIN_HEALTH_CHECKS, int)


# ── run_health_check() — return type ──────────────────────────────────────────

def test_health_check_returns_summary():
    assert isinstance(run_health_check(), ScenarioMatrixHealthSummary)

def test_health_check_status_pass():
    assert run_health_check().status == "PASS"

def test_health_check_all_passed():
    assert run_health_check().all_passed is True

def test_health_check_failed_zero():
    assert run_health_check().failed == 0

def test_health_check_total_ge_60():
    assert run_health_check().total >= 60

def test_health_check_passed_ge_60():
    assert run_health_check().passed >= 60

def test_health_check_passed_equals_total():
    result = run_health_check()
    assert result.passed == result.total

def test_health_check_paper_only():
    assert run_health_check().paper_only is True

def test_health_check_no_real_orders():
    assert run_health_check().no_real_orders is True

def test_health_check_not_investment_advice():
    assert run_health_check().not_investment_advice is True

def test_health_check_schema_version():
    assert run_health_check().schema_version == "181"


# ── checks list ───────────────────────────────────────────────────────────────

def test_health_checks_list_is_list():
    assert isinstance(run_health_check().checks, list)

def test_health_checks_all_have_name():
    checks = run_health_check().checks
    assert all("name" in c for c in checks)

def test_health_checks_all_have_passed():
    checks = run_health_check().checks
    assert all("passed" in c for c in checks)

def test_health_checks_all_passed_true():
    checks = run_health_check().checks
    assert all(c["passed"] is True for c in checks)

def test_health_checks_no_failures():
    checks = run_health_check().checks
    failures = [c for c in checks if not c["passed"]]
    assert failures == [], f"Failed checks: {failures}"

def test_health_checks_names_unique():
    names = [c["name"] for c in run_health_check().checks]
    assert len(names) == len(set(names))

def test_health_checks_count_matches_total():
    result = run_health_check()
    assert len(result.checks) == result.total
