"""
tests/test_portfolio_governance_health_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Health Check Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_governance_health_v198 import run_health_check


class TestRunHealthCheck:
    def test_returns_dict(self):
        assert isinstance(run_health_check(), dict)

    def test_all_passed_is_True(self):
        assert run_health_check()["all_passed"] is True

    def test_status_is_PASS(self):
        assert run_health_check()["status"] == "PASS"

    def test_failed_is_0(self):
        assert run_health_check()["failed"] == 0

    def test_passed_gte_60(self):
        assert run_health_check()["passed"] >= 60

    def test_total_gte_60(self):
        assert run_health_check()["total"] >= 60

    def test_paper_only_True(self):
        assert run_health_check()["paper_only"] is True

    def test_no_real_orders_True(self):
        assert run_health_check()["no_real_orders"] is True

    def test_not_investment_advice_True(self):
        assert run_health_check()["not_investment_advice"] is True

    def test_version_is_1_9_8(self):
        assert run_health_check()["version"] == "1.9.8"

    def test_checks_is_list(self):
        assert isinstance(run_health_check()["checks"], list)

    def test_checks_not_empty(self):
        assert len(run_health_check()["checks"]) > 0

    def test_passed_equals_total(self):
        r = run_health_check()
        assert r["passed"] == r["total"]

    def test_all_check_dicts_have_name(self):
        for c in run_health_check()["checks"]:
            assert "name" in c

    def test_all_check_dicts_have_passed(self):
        for c in run_health_check()["checks"]:
            assert "passed" in c

    def test_all_checks_pass(self):
        for c in run_health_check()["checks"]:
            assert c["passed"] is True, f"Failed check: {c['name']}"

    def test_version_check_in_checks(self):
        names = [c["name"] for c in run_health_check()["checks"]]
        assert "version_is_1.9.8" in names

    def test_model_count_check_in_checks(self):
        names = [c["name"] for c in run_health_check()["checks"]]
        assert "model_count_26" in names

    def test_scenarios_count_check_in_checks(self):
        names = [c["name"] for c in run_health_check()["checks"]]
        assert "scenarios_count_75" in names
