"""tests/test_abc_health_v172.py — Health check tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_execution_health_v172 import (
    run_health_check, ABCExecutionHealthCheck, HEALTH_VERSION,
)


def test_health_version():
    assert HEALTH_VERSION == "1.7.2"


def test_run_health_check_returns_dict():
    result = run_health_check()
    assert isinstance(result, dict)


def test_run_health_check_passes():
    result = run_health_check()
    assert result["all_passed"] is True


def test_run_health_check_status_pass():
    result = run_health_check()
    assert result["status"] == "PASS"


def test_run_health_check_no_failures():
    result = run_health_check()
    assert result["failed"] == 0


def test_run_health_check_at_least_75_checks():
    result = run_health_check()
    assert result["total"] >= 75


def test_run_health_check_passed_equals_total():
    result = run_health_check()
    assert result["passed"] == result["total"]


def test_health_check_class_instantiates():
    hc = ABCExecutionHealthCheck()
    assert hc is not None


def test_health_check_run_method():
    hc = ABCExecutionHealthCheck()
    result = hc.run()
    assert "all_passed" in result


def test_health_check_checks_list_nonempty():
    result = run_health_check()
    assert "checks" in result
    assert len(result["checks"]) > 0


def test_health_check_all_checks_pass():
    result = run_health_check()
    for c in result["checks"]:
        assert c["status"] == "PASS", f"Health check failed: {c['name']}: {c.get('detail')}"
