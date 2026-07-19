"""
tests/test_governance_stack_health_v1910.py
v1.9.10 Paper Governance Stack Consolidation & Release Audit — Health Tests
[!] Paper Only. Research Only. Consolidation Only. Release Audit Only.
[!] No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.governance_stack_health_v1910 import (
    run_health_check,
    HEALTH_VERSION,
)


def test_health_version_is_1910():
    assert HEALTH_VERSION == "1.9.10"

def test_run_health_check_returns_dict():
    assert isinstance(run_health_check(), dict)

def test_run_health_check_all_passed_true():
    assert run_health_check()["all_passed"] is True

def test_run_health_check_status_pass():
    assert run_health_check()["status"] == "PASS"

def test_run_health_check_failed_is_0():
    assert run_health_check()["failed"] == 0

def test_run_health_check_total_gt_0():
    assert run_health_check()["total"] > 0

def test_run_health_check_passed_equals_total():
    result = run_health_check()
    assert result["passed"] == result["total"]

def test_run_health_check_has_checks():
    assert "checks" in run_health_check()
    assert isinstance(run_health_check()["checks"], list)

def test_run_health_check_checks_not_empty():
    assert len(run_health_check()["checks"]) > 0

def test_run_health_check_paper_only():
    assert run_health_check()["paper_only"] is True

def test_run_health_check_not_investment_advice():
    assert run_health_check()["not_investment_advice"] is True

def test_run_health_check_production_trading_blocked():
    assert run_health_check()["production_trading_blocked"] is True

def test_run_health_check_consolidation_only():
    assert run_health_check()["consolidation_only"] is True

def test_run_health_check_release_audit_only():
    assert run_health_check()["release_audit_only"] is True

def test_run_health_check_health_version_field():
    assert run_health_check().get("health_version") == "1.9.10"

def test_run_health_check_passed_gt_0():
    assert run_health_check()["passed"] > 0

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
