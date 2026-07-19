"""
tests/test_paper_cockpit_health_v200.py
v2.0.0 Paper Cockpit — Health Check Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.paper_cockpit_health_v200 import (
    run_health_check, HEALTH_VERSION, HEALTH_RELEASE,
)


def test_health_version_is_200():
    assert HEALTH_VERSION == "2.0.0"

def test_health_release_name():
    assert "Cockpit" in HEALTH_RELEASE or "Console" in HEALTH_RELEASE

def test_run_health_check_returns_dict():
    result = run_health_check()
    assert isinstance(result, dict)

def test_run_health_check_all_passed():
    result = run_health_check()
    assert result["all_passed"] is True

def test_run_health_check_zero_failed():
    result = run_health_check()
    assert result["failed"] == 0

def test_run_health_check_passed_equals_total():
    result = run_health_check()
    assert result["passed"] == result["total"]

def test_run_health_check_passed_positive():
    result = run_health_check()
    assert result["passed"] > 0

def test_run_health_check_no_errors():
    result = run_health_check()
    assert result["errors"] == []

def test_run_health_check_has_version():
    result = run_health_check()
    assert result["version"] == "2.0.0"

def test_run_health_check_has_release():
    result = run_health_check()
    assert "Cockpit" in result["release"] or "Console" in result["release"]

def test_health_check_is_idempotent():
    r1 = run_health_check()
    r2 = run_health_check()
    assert r1["all_passed"] == r2["all_passed"]
    assert r1["passed"] == r2["passed"]

def test_health_check_total_is_positive():
    result = run_health_check()
    assert result["total"] > 50

def test_health_check_result_keys():
    result = run_health_check()
    for key in ["all_passed", "passed", "failed", "total", "errors", "version", "release"]:
        assert key in result, f"Missing key '{key}'"
