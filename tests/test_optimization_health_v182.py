"""
tests/test_optimization_health_v182.py
Tests for optimization health check v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest

from paper_trading.small_capital_strategy.optimization_health_v182 import run_health_check
from paper_trading.small_capital_strategy.optimization_models_v182 import OptimizationHealthSummary


def test_health_returns_model():
    result = run_health_check()
    assert isinstance(result, OptimizationHealthSummary)

def test_health_all_passed():
    result = run_health_check()
    assert result.all_passed is True

def test_health_status_pass():
    result = run_health_check()
    assert result.status == "PASS"

def test_health_failed_0():
    result = run_health_check()
    assert result.failed == 0

def test_health_total_ge_60():
    result = run_health_check()
    assert result.total >= 60

def test_health_passed_eq_total():
    result = run_health_check()
    assert result.passed == result.total

def test_health_checks_list():
    result = run_health_check()
    assert isinstance(result.checks, list)
    assert len(result.checks) >= 60

def test_health_paper_only():
    result = run_health_check()
    assert result.paper_only is True

def test_health_schema_version():
    result = run_health_check()
    assert result.schema_version == "182"

def test_health_all_checks_passed():
    result = run_health_check()
    for check in result.checks:
        assert check["passed"] is True, f"Health check '{check['name']}' failed: {check.get('error')}"

def test_health_checks_have_names():
    result = run_health_check()
    for check in result.checks:
        assert "name" in check
        assert isinstance(check["name"], str)
        assert len(check["name"]) > 0

def test_health_checks_no_errors():
    result = run_health_check()
    for check in result.checks:
        assert check["error"] is None, f"Health check '{check['name']}' had error: {check['error']}"

def test_health_check_names_unique():
    result = run_health_check()
    names = [c["name"] for c in result.checks]
    assert len(names) == len(set(names))

def test_health_version_check_present():
    result = run_health_check()
    names = [c["name"] for c in result.checks]
    assert "version_is_182" in names

def test_health_safety_check_present():
    result = run_health_check()
    names = [c["name"] for c in result.checks]
    assert "safety_paper_only" in names

def test_health_model_check_present():
    result = run_health_check()
    names = [c["name"] for c in result.checks]
    assert "model_optimization_input" in names

def test_health_scenario_check_present():
    result = run_health_check()
    names = [c["name"] for c in result.checks]
    assert "scenarios_count_ge_75" in names

def test_health_gui_check_present():
    result = run_health_check()
    names = [c["name"] for c in result.checks]
    assert "gui_panel_version_182" in names

def test_health_cli_check_present():
    result = run_health_check()
    names = [c["name"] for c in result.checks]
    assert "cli_optimization_commands_17" in names
