"""
tests/test_monte_carlo_health_v183.py
Tests for Monte Carlo health check module v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.monte_carlo_health_v183 import run_health_check
from paper_trading.small_capital_strategy.monte_carlo_models_v183 import MonteCarloHealthSummary


# ---------------------------------------------------------------------------
# Fixture: single health check run shared across all tests
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def health_result():
    return run_health_check()


# ---------------------------------------------------------------------------
# Return type
# ---------------------------------------------------------------------------

def test_run_health_check_returns_monte_carlo_health_summary(health_result):
    assert isinstance(health_result, MonteCarloHealthSummary)


# ---------------------------------------------------------------------------
# Counts and pass/fail
# ---------------------------------------------------------------------------

def test_health_result_total_ge_60(health_result):
    assert health_result.total >= 60


def test_health_result_passed_equals_total(health_result):
    assert health_result.passed == health_result.total


def test_health_result_failed_equals_0(health_result):
    assert health_result.failed == 0


def test_health_result_all_passed_true(health_result):
    assert health_result.all_passed is True


def test_health_result_status_pass(health_result):
    assert health_result.status == "PASS"


# ---------------------------------------------------------------------------
# Safety flags on the summary
# ---------------------------------------------------------------------------

def test_health_result_paper_only(health_result):
    assert health_result.paper_only is True


def test_health_result_monte_carlo_only(health_result):
    assert health_result.monte_carlo_only is True


def test_health_result_schema_version(health_result):
    assert health_result.schema_version == "183"


# ---------------------------------------------------------------------------
# checks list structure
# ---------------------------------------------------------------------------

def test_health_result_checks_is_list(health_result):
    assert isinstance(health_result.checks, list)


def test_health_result_checks_length_ge_60(health_result):
    assert len(health_result.checks) >= 60


def test_health_checks_all_have_name_key(health_result):
    for c in health_result.checks:
        assert "name" in c, f"check missing 'name': {c}"


def test_health_checks_all_have_passed_key(health_result):
    for c in health_result.checks:
        assert "passed" in c, f"check missing 'passed': {c}"


def test_health_checks_all_have_error_key(health_result):
    for c in health_result.checks:
        assert "error" in c, f"check missing 'error': {c}"


def test_health_checks_no_failed_checks(health_result):
    failed_checks = [c for c in health_result.checks if not c["passed"]]
    assert failed_checks == [], f"Unexpected failed checks: {[c['name'] for c in failed_checks]}"


# ---------------------------------------------------------------------------
# Specific check names present
# ---------------------------------------------------------------------------

def test_health_check_version_is_183_present(health_result):
    names = [c["name"] for c in health_result.checks]
    assert "version_is_183" in names


def test_health_check_safety_paper_only_present(health_result):
    names = [c["name"] for c in health_result.checks]
    assert "safety_paper_only" in names


def test_health_check_model_monte_carlo_input_present(health_result):
    names = [c["name"] for c in health_result.checks]
    assert "model_monte_carlo_input" in names


def test_health_check_allowed_output_actions_15_present(health_result):
    names = [c["name"] for c in health_result.checks]
    assert "allowed_output_actions_15" in names


def test_health_check_scenarios_count_ge_75_present(health_result):
    names = [c["name"] for c in health_result.checks]
    assert "scenarios_count_ge_75" in names


def test_health_check_fixtures_count_ge_75_present(health_result):
    names = [c["name"] for c in health_result.checks]
    assert "fixtures_count_ge_75" in names


# ---------------------------------------------------------------------------
# Passed checks have error == None
# ---------------------------------------------------------------------------

def test_health_checks_passed_have_no_error(health_result):
    for c in health_result.checks:
        if c["passed"]:
            assert c["error"] is None, f"check '{c['name']}' passed but has error: {c['error']}"
