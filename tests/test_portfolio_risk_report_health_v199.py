"""
tests/test_portfolio_risk_report_health_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Health Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.portfolio_risk_report_health_v199 import (
    run_health_check,
    HEALTH_VERSION,
)


def test_run_health_check_returns_dict():
    assert isinstance(run_health_check(), dict)


def test_run_health_check_all_passed_True():
    assert run_health_check()["all_passed"] is True


def test_run_health_check_status_is_PASS():
    assert run_health_check()["status"] == "PASS"


def test_run_health_check_failed_is_0():
    assert run_health_check()["failed"] == 0


def test_run_health_check_total_gt_0():
    assert run_health_check()["total"] > 0


def test_run_health_check_passed_equals_total():
    result = run_health_check()
    assert result["passed"] == result["total"]


def test_run_health_check_has_checks_list():
    result = run_health_check()
    assert "checks" in result
    assert isinstance(result["checks"], list)


def test_run_health_check_paper_only_True():
    assert run_health_check()["paper_only"] is True


def test_run_health_check_not_investment_advice_True():
    assert run_health_check()["not_investment_advice"] is True


def test_run_health_check_production_trading_blocked_True():
    assert run_health_check()["production_trading_blocked"] is True


def test_all_checks_have_name():
    for c in run_health_check()["checks"]:
        assert "name" in c
        assert isinstance(c["name"], str)


def test_all_checks_have_status():
    for c in run_health_check()["checks"]:
        assert "status" in c


def test_all_check_status_values_are_pass_or_fail():
    for c in run_health_check()["checks"]:
        assert c["status"] in ("PASS", "FAIL"), f"Unexpected status: {c['status']}"


def test_all_checks_pass():
    for c in run_health_check()["checks"]:
        assert c["status"] == "PASS", f"Health check failed: {c['name']} {c.get('detail', '')}"


def test_health_version_constant_is_1_9_9():
    assert HEALTH_VERSION == "1.9.9"


def test_run_health_check_health_version_field():
    result = run_health_check()
    assert result.get("health_version") == "1.9.9"


def test_run_health_check_checks_not_empty():
    assert len(run_health_check()["checks"]) > 0


def test_run_health_check_passed_gt_0():
    assert run_health_check()["passed"] > 0
