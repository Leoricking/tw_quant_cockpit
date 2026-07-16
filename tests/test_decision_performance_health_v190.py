"""tests/test_decision_performance_health_v190.py
Tests for decision performance health check v1.9.0.
[!] Research Only. Paper Only.
"""
import pytest
from paper_trading.small_capital_strategy.decision_performance_health_v190 import (
    run_health_check,
)


def test_run_health_check_returns_object():
    result = run_health_check()
    assert result is not None


def test_run_health_check_status_pass():
    assert run_health_check().status == "PASS"


def test_run_health_check_all_passed():
    assert run_health_check().all_passed is True


def test_run_health_check_failed_zero():
    assert run_health_check().failed == 0


def test_run_health_check_passed_ge_60():
    assert run_health_check().passed >= 60


def test_run_health_check_total_ge_60():
    assert run_health_check().total >= 60


def test_run_health_check_passed_equals_total():
    assert run_health_check().passed == run_health_check().total


def test_run_health_check_checks_is_list():
    assert isinstance(run_health_check().checks, list)


def test_run_health_check_checks_count_ge_60():
    assert len(run_health_check().checks) >= 60


def test_run_health_check_all_checks_passed():
    assert all(c["passed"] for c in run_health_check().checks)


def test_run_health_check_all_checks_have_name():
    assert all("name" in c for c in run_health_check().checks)


def test_run_health_check_all_checks_have_passed_field():
    assert all("passed" in c for c in run_health_check().checks)


def test_run_health_check_version_is_190_present():
    assert any(c["name"] == "version_is_190" for c in run_health_check().checks)


def test_run_health_check_safety_audit_present():
    assert any(c["name"] == "safety_audit_all_safe" for c in run_health_check().checks)


def test_run_health_check_scenarios_count_75_present():
    assert any(c["name"] == "scenarios_count_75" for c in run_health_check().checks)


def test_run_health_check_fixtures_count_75_present():
    assert any(c["name"] == "fixtures_count_75" for c in run_health_check().checks)


def test_run_health_check_gui_panel_version_190_present():
    assert any(c["name"] == "gui_panel_version_190" for c in run_health_check().checks)
