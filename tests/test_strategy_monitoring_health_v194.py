"""
tests/test_strategy_monitoring_health_v194.py
Tests for strategy_monitoring_health_v194.
[!] Research Only. Paper Only. Monitoring Only. Drift Detection Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.strategy_monitoring_health_v194 import (
    run_health_check,
)


def test_health_check_returns_dict():
    assert isinstance(run_health_check(), dict)


def test_health_check_all_passed():
    assert run_health_check()["all_passed"] is True


def test_health_check_status_pass():
    assert run_health_check()["status"] == "PASS"


def test_health_check_failed_zero():
    assert run_health_check()["failed"] == 0


def test_health_check_min_60_checks():
    assert run_health_check()["total"] >= 60


def test_health_check_passed_ge_total_minus_failed():
    result = run_health_check()
    assert result["passed"] == result["total"] - result["failed"]


def test_health_check_has_checks_list():
    result = run_health_check()
    assert "checks" in result
    assert isinstance(result["checks"], list)


def test_health_check_paper_only():
    assert run_health_check()["paper_only"] is True


def test_health_check_no_real_orders():
    assert run_health_check()["no_real_orders"] is True


def test_health_check_schema_version():
    assert run_health_check()["schema_version"] == "194"
