"""
tests/test_paper_cockpit_gate_v200.py
v2.0.0 Paper Cockpit — Release Gate Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from release.paper_cockpit_release_gate_v200 import (
    run_release_gate, run_gate, GATE_VERSION, GATE_RELEASE,
    BASELINE_TESTS, MIN_NEW_TESTS, EXPECTED_PANEL_VERSIONS,
)


def test_gate_version_is_200():
    assert GATE_VERSION == "2.0.0"

def test_gate_release_name():
    assert "Cockpit" in GATE_RELEASE or "Console" in GATE_RELEASE

def test_baseline_tests_31925():
    assert BASELINE_TESTS == 31925

def test_min_new_tests_500():
    assert MIN_NEW_TESTS == 500

def test_expected_panel_versions_includes_200():
    assert "2.0.0" in EXPECTED_PANEL_VERSIONS

def test_run_release_gate_returns_dict():
    result = run_release_gate()
    assert isinstance(result, dict)

def test_run_release_gate_passed():
    result = run_release_gate()
    assert result["gate_passed"] is True

def test_run_release_gate_zero_failed():
    result = run_release_gate()
    assert result["failed_count"] == 0

def test_run_release_gate_passed_equals_total():
    result = run_release_gate()
    assert result["passed_count"] == result["total_count"]

def test_run_release_gate_passed_positive():
    result = run_release_gate()
    assert result["passed_count"] > 0

def test_run_release_gate_no_errors():
    result = run_release_gate()
    assert result["errors"] == []

def test_run_release_gate_has_version():
    result = run_release_gate()
    assert result["gate_version"] == "2.0.0"

def test_run_gate_alias_works():
    result = run_gate()
    assert result["gate_passed"] is True

def test_gate_is_idempotent():
    r1 = run_release_gate()
    r2 = run_release_gate()
    assert r1["gate_passed"] == r2["gate_passed"]
    assert r1["passed_count"] == r2["passed_count"]

def test_gate_result_keys():
    result = run_release_gate()
    for key in ["gate_passed", "passed_count", "failed_count", "total_count",
                "errors", "gate_version", "gate_release"]:
        assert key in result, f"Missing key '{key}'"

def test_gate_total_checks_positive():
    result = run_release_gate()
    assert result["total_count"] > 40

def test_run_gate_is_same_as_run_release_gate():
    r1 = run_release_gate()
    r2 = run_gate()
    assert r1["gate_passed"] == r2["gate_passed"]
    assert r1["passed_count"] == r2["passed_count"]
