"""
tests/test_portfolio_risk_report_gate_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Release Gate Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from release.portfolio_risk_report_release_gate_v199 import (
    run_release_gate,
    run_gate,
    GATE_VERSION,
    BASELINE_TESTS,
    MIN_NEW_TESTS,
)


def test_run_release_gate_returns_dict():
    assert isinstance(run_release_gate(), dict)


def test_run_release_gate_all_passed_True():
    assert run_release_gate()["all_passed"] is True


def test_run_release_gate_status_is_PASS():
    assert run_release_gate()["status"] == "PASS"


def test_run_release_gate_failed_is_0():
    assert run_release_gate()["failed"] == 0


def test_run_release_gate_total_gt_0():
    assert run_release_gate()["total"] > 0


def test_run_release_gate_paper_only_True():
    assert run_release_gate()["paper_only"] is True


def test_run_release_gate_not_investment_advice_True():
    assert run_release_gate()["not_investment_advice"] is True


def test_run_release_gate_production_trading_blocked_True():
    assert run_release_gate()["production_trading_blocked"] is True


def test_gate_version_is_1_9_9():
    assert GATE_VERSION == "1.9.9"


def test_baseline_tests_31044():
    assert BASELINE_TESTS == 31044


def test_min_new_tests_400():
    assert MIN_NEW_TESTS == 400


def test_run_gate_is_callable():
    assert callable(run_gate)


def test_run_gate_returns_dict():
    assert isinstance(run_gate(), dict)


def test_run_gate_all_passed_True():
    assert run_gate()["all_passed"] is True


def test_run_gate_status_is_PASS():
    assert run_gate()["status"] == "PASS"


def test_run_gate_same_result_as_run_release_gate():
    r1 = run_release_gate()
    r2 = run_gate()
    assert r1["all_passed"] == r2["all_passed"]
    assert r1["total"] == r2["total"]


def test_run_release_gate_has_checks():
    result = run_release_gate()
    assert "checks" in result
    assert isinstance(result["checks"], list)
    assert len(result["checks"]) > 0


def test_run_release_gate_all_checks_have_name():
    for c in run_release_gate()["checks"]:
        assert "name" in c
        assert isinstance(c["name"], str)
        assert len(c["name"]) > 0


def test_run_release_gate_all_checks_have_status():
    for c in run_release_gate()["checks"]:
        assert "status" in c
        assert c["status"] in ("PASS", "FAIL")


def test_run_release_gate_all_checks_pass():
    for c in run_release_gate()["checks"]:
        assert c["status"] == "PASS", f"Gate check failed: {c['name']}"


def test_run_release_gate_passed_equals_total():
    result = run_release_gate()
    assert result["passed"] == result["total"]


def test_run_release_gate_gate_version_in_result():
    result = run_release_gate()
    assert result.get("gate_version") == "1.9.9"
