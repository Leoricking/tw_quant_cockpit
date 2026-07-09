"""
tests/test_risk_dashboard_health_v174.py
Tests for risk dashboard health checks v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_health_v174 import (
    run_health_check, MIN_HEALTH_CHECKS,
)
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import RiskDashboardHealthSummary


class TestHealthConstants:
    def test_min_health_checks_70(self):
        assert MIN_HEALTH_CHECKS == 70


class TestRunHealthCheck:
    def setup_method(self):
        self.result = run_health_check()

    def test_returns_health_summary(self):
        assert isinstance(self.result, RiskDashboardHealthSummary)

    def test_all_passed_true(self):
        assert self.result.all_passed is True

    def test_status_pass(self):
        assert self.result.status == "PASS"

    def test_failed_zero(self):
        assert self.result.failed == 0

    def test_passed_ge_70(self):
        assert self.result.passed >= 70

    def test_total_ge_70(self):
        assert self.result.total >= 70

    def test_total_ge_min_health_checks(self):
        assert self.result.total >= MIN_HEALTH_CHECKS

    def test_checks_list(self):
        assert isinstance(self.result.checks, list)

    def test_checks_not_empty(self):
        assert len(self.result.checks) > 0

    def test_paper_only(self):
        assert self.result.paper_only is True

    def test_no_real_orders(self):
        assert self.result.no_real_orders is True

    def test_not_investment_advice(self):
        assert self.result.not_investment_advice is True


class TestHealthCheckItems:
    def setup_method(self):
        self.checks = run_health_check().checks

    def test_each_check_has_name(self):
        for c in self.checks:
            assert "name" in c

    def test_each_check_has_passed(self):
        for c in self.checks:
            assert "passed" in c

    def test_each_check_has_error_key(self):
        for c in self.checks:
            assert "error" in c

    def test_all_checks_passed(self):
        failed = [c for c in self.checks if not c["passed"]]
        assert failed == [], f"Failed checks: {[c['name'] for c in failed]}"

    def test_version_check_present(self):
        names = [c["name"] for c in self.checks]
        assert "version_is_174" in names

    def test_safety_check_present(self):
        names = [c["name"] for c in self.checks]
        assert "safety_audit_all_safe" in names

    def test_enum_check_present(self):
        names = [c["name"] for c in self.checks]
        assert "enum_risk_status_5_values" in names
