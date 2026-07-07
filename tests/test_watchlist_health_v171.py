"""tests/test_watchlist_health_v171.py — watchlist health check tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_health_v171 import (
    run_health_check, WatchlistHealthCheck, HEALTH_VERSION,
)


def test_health_version_constant():
    assert HEALTH_VERSION == "1.7.1"


def test_run_health_check_returns_dict():
    result = run_health_check()
    assert isinstance(result, dict)


def test_run_health_check_all_passed():
    result = run_health_check()
    assert result["all_passed"] is True, (
        f"Health checks failed: {[c for c in result['checks'] if c['status'] != 'PASS']}"
    )


def test_run_health_check_status_pass():
    result = run_health_check()
    assert result["status"] == "PASS"


def test_run_health_check_failed_zero():
    result = run_health_check()
    assert result["failed"] == 0


def test_run_health_check_total_ge_70():
    result = run_health_check()
    assert result["total"] >= 70


def test_run_health_check_version_key():
    result = run_health_check()
    assert result["version"] == "1.7.1"


def test_run_health_check_checks_is_list():
    result = run_health_check()
    assert isinstance(result["checks"], list)


def test_run_health_check_paper_only():
    result = run_health_check()
    assert result["paper_only"] is True


def test_run_health_check_not_investment_advice():
    result = run_health_check()
    assert result["not_investment_advice"] is True


def test_run_health_check_no_real_orders():
    result = run_health_check()
    assert result["no_real_orders"] is True


def test_run_health_check_passed_plus_failed_equals_total():
    result = run_health_check()
    assert result["passed"] + result["failed"] == result["total"]


def test_all_checks_have_name():
    result = run_health_check()
    for check in result["checks"]:
        assert "name" in check, f"Check missing 'name': {check}"


def test_all_checks_have_status():
    result = run_health_check()
    for check in result["checks"]:
        assert "status" in check, f"Check missing 'status': {check}"


def test_all_checks_status_pass():
    result = run_health_check()
    failed = [c for c in result["checks"] if c["status"] != "PASS"]
    assert failed == [], f"Failed checks: {failed}"


def test_health_check_class_instantiatable():
    hc = WatchlistHealthCheck()
    assert hc is not None


def test_health_check_class_run_returns_dict():
    hc = WatchlistHealthCheck()
    result = hc.run()
    assert isinstance(result, dict)
