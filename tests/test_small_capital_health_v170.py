"""tests/test_small_capital_health_v170.py — health check tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.health_v170 import (
    SmallCapitalHealthCheck, run_health_check, HEALTH_VERSION,
)


def test_health_version():
    assert HEALTH_VERSION == "1.7.0"


def test_run_health_check_returns_dict():
    result = run_health_check()
    assert isinstance(result, dict)


def test_run_health_check_all_passed():
    result = run_health_check()
    assert result["all_passed"] is True


def test_run_health_check_failed_zero():
    result = run_health_check()
    assert result["failed"] == 0


def test_run_health_check_passed_gte_80():
    result = run_health_check()
    assert result["passed"] >= 80


def test_run_health_check_total_gte_80():
    result = run_health_check()
    assert result["total"] >= 80


def test_run_health_check_checks_list():
    result = run_health_check()
    assert isinstance(result["checks"], list)


def test_run_health_check_all_checks_pass():
    result = run_health_check()
    failed = [c for c in result["checks"] if c["status"] == "FAIL"]
    assert failed == [], f"Failed checks: {[c['name'] for c in failed]}"


def test_run_health_check_paper_only():
    result = run_health_check()
    assert result["paper_only"] is True


def test_run_health_check_no_real_orders():
    result = run_health_check()
    assert result["no_real_orders"] is True


def test_run_health_check_research_only():
    result = run_health_check()
    assert result["research_only"] is True


def test_health_check_class_run():
    hc = SmallCapitalHealthCheck()
    result = hc.run()
    assert result["all_passed"] is True


def test_health_check_version_in_result():
    result = run_health_check()
    assert result["health_version"] == "1.7.0"
