"""
tests/test_market_regime_health_v173.py
Tests for Market Regime Position Control health_v173 module.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.market_regime_health_v173 import (
    run_health_check, MIN_HEALTH_CHECKS,
)


class TestRunHealthCheck:
    def test_all_passed_true(self):
        result = run_health_check()
        assert result.all_passed is True

    def test_status_pass(self):
        result = run_health_check()
        assert result.status == "PASS"

    def test_failed_zero(self):
        result = run_health_check()
        assert result.failed == 0

    def test_total_ge_70(self):
        result = run_health_check()
        assert result.total >= 70

    def test_total_ge_min_health_checks(self):
        result = run_health_check()
        assert result.total >= MIN_HEALTH_CHECKS

    def test_passed_equals_total(self):
        result = run_health_check()
        assert result.passed == result.total

    def test_checks_list_not_empty(self):
        result = run_health_check()
        assert len(result.checks) > 0

    def test_all_checks_passed(self):
        result = run_health_check()
        for check in result.checks:
            assert check["passed"] is True, f"Check failed: {check['name']}: {check.get('error')}"

    def test_paper_only(self):
        result = run_health_check()
        assert result.paper_only is True

    def test_no_real_orders(self):
        result = run_health_check()
        assert result.no_real_orders is True

    def test_schema_version(self):
        result = run_health_check()
        assert result.schema_version == "173"


class TestMinHealthChecks:
    def test_min_health_checks_constant(self):
        assert MIN_HEALTH_CHECKS == 70
