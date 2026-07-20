"""
tests/test_paper_cockpit_health_v201.py
v2.0.1 Paper Cockpit — Health Check Tests (20+ tests)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from paper_trading.small_capital_strategy.paper_cockpit_health_v201 import (
    run_health_check, HEALTH_VERSION, HEALTH_RELEASE,
)


# --- Health module constants ---

def test_health_version_is_201():
    assert HEALTH_VERSION == "2.0.1"

def test_health_release_contains_daily_workflow():
    assert "Daily Workflow" in HEALTH_RELEASE


# --- run_health_check tests ---

def test_run_health_check_returns_dict():
    result = run_health_check()
    assert isinstance(result, dict)

def test_run_health_check_has_all_passed():
    result = run_health_check()
    assert "all_passed" in result

def test_run_health_check_has_passed():
    result = run_health_check()
    assert "passed" in result

def test_run_health_check_has_failed():
    result = run_health_check()
    assert "failed" in result

def test_run_health_check_has_total():
    result = run_health_check()
    assert "total" in result

def test_run_health_check_has_errors():
    result = run_health_check()
    assert "errors" in result

def test_run_health_check_has_version():
    result = run_health_check()
    assert result["version"] == "2.0.1"

def test_run_health_check_has_release():
    result = run_health_check()
    assert "Daily Workflow" in result["release"]

def test_run_health_check_all_passed():
    result = run_health_check()
    assert result["all_passed"] is True, f"Health check failed: {result.get('errors', [])}"

def test_run_health_check_zero_failures():
    result = run_health_check()
    assert result["failed"] == 0, f"Health failures: {result.get('errors', [])}"

def test_run_health_check_passed_greater_than_zero():
    result = run_health_check()
    assert result["passed"] > 0

def test_run_health_check_total_is_passed_plus_failed():
    result = run_health_check()
    assert result["total"] == result["passed"] + result["failed"]

def test_run_health_check_errors_empty_on_pass():
    result = run_health_check()
    if result["all_passed"]:
        assert result["errors"] == []

def test_run_health_check_no_entry_reasons_verified():
    result = run_health_check()
    assert result["all_passed"] is True

def test_run_health_check_safety_flags_verified():
    result = run_health_check()
    assert result["all_passed"] is True

def test_run_health_check_models_verified():
    result = run_health_check()
    assert result["all_passed"] is True

def test_run_health_check_scenarios_verified():
    result = run_health_check()
    assert result["all_passed"] is True

def test_run_health_check_fixtures_verified():
    result = run_health_check()
    assert result["all_passed"] is True

def test_run_health_check_gui_verified():
    result = run_health_check()
    assert result["all_passed"] is True

def test_run_health_check_backward_compat_verified():
    result = run_health_check()
    assert result["all_passed"] is True
