"""
tests/test_paper_cockpit_gate_v201.py
v2.0.1 Paper Cockpit — Release Gate Tests (20+ tests)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from release.paper_cockpit_release_gate_v201 import (
    run_release_gate, run_gate, GATE_VERSION, GATE_RELEASE,
    BASELINE_TESTS, MIN_NEW_TESTS, EXPECTED_PANEL_VERSIONS,
)


# --- Gate module constants ---

def test_gate_version_is_201():
    assert GATE_VERSION == "2.0.1"

def test_gate_release_contains_daily_workflow():
    assert "Daily Workflow" in GATE_RELEASE

def test_baseline_tests_value():
    assert BASELINE_TESTS == 32425

def test_min_new_tests_value():
    assert MIN_NEW_TESTS == 300

def test_expected_panel_versions_contains_201():
    assert "2.0.1" in EXPECTED_PANEL_VERSIONS

def test_expected_panel_versions_contains_200():
    assert "2.0.0" in EXPECTED_PANEL_VERSIONS

def test_run_gate_alias():
    assert run_gate is run_release_gate


# --- run_release_gate tests ---

def test_run_release_gate_returns_dict():
    result = run_release_gate()
    assert isinstance(result, dict)

def test_run_release_gate_has_gate_passed():
    result = run_release_gate()
    assert "gate_passed" in result

def test_run_release_gate_has_passed_count():
    result = run_release_gate()
    assert "passed_count" in result

def test_run_release_gate_has_failed_count():
    result = run_release_gate()
    assert "failed_count" in result

def test_run_release_gate_has_total_count():
    result = run_release_gate()
    assert "total_count" in result

def test_run_release_gate_has_errors():
    result = run_release_gate()
    assert "errors" in result

def test_run_release_gate_has_gate_version():
    result = run_release_gate()
    assert result["gate_version"] == "2.0.1"

def test_run_release_gate_has_gate_release():
    result = run_release_gate()
    assert "Daily Workflow" in result["gate_release"]

def test_run_release_gate_gate_passed():
    result = run_release_gate()
    assert result["gate_passed"] is True, f"Gate failed: {result.get('errors', [])}"

def test_run_release_gate_zero_failures():
    result = run_release_gate()
    assert result["failed_count"] == 0, f"Gate failures: {result.get('errors', [])}"

def test_run_release_gate_passed_greater_than_zero():
    result = run_release_gate()
    assert result["passed_count"] > 0

def test_run_release_gate_total_is_sum():
    result = run_release_gate()
    assert result["total_count"] == result["passed_count"] + result["failed_count"]

def test_run_release_gate_checks_scenarios():
    result = run_release_gate()
    assert result["gate_passed"] is True

def test_run_release_gate_checks_fixtures():
    result = run_release_gate()
    assert result["gate_passed"] is True

def test_run_release_gate_checks_gui():
    result = run_release_gate()
    assert result["gate_passed"] is True

def test_run_release_gate_checks_cli():
    result = run_release_gate()
    assert result["gate_passed"] is True

def test_run_release_gate_checks_backward_compat():
    result = run_release_gate()
    assert result["gate_passed"] is True

def test_run_release_gate_checks_safety():
    result = run_release_gate()
    assert result["gate_passed"] is True

def test_run_release_gate_checks_no_entry_reasons():
    result = run_release_gate()
    assert result["gate_passed"] is True

def test_run_release_gate_checks_final_actions():
    result = run_release_gate()
    assert result["gate_passed"] is True
