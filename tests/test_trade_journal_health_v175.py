"""
tests/test_trade_journal_health_v175.py
Tests for Trade Journal health check v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.trade_journal_health_v175 import (
    run_health_check, MIN_HEALTH_CHECKS,
)
from paper_trading.small_capital_strategy.trade_journal_models_v175 import TradeJournalHealthSummary


class TestRunHealthCheck:
    @classmethod
    def setup_class(cls):
        cls.result = run_health_check()

    def test_returns_health_summary(self):
        assert isinstance(self.result, TradeJournalHealthSummary)

    def test_all_passed_true(self):
        failed = [c for c in self.result.checks if not c["passed"]]
        assert self.result.all_passed is True, f"Failed checks: {failed}"

    def test_status_pass(self):
        assert self.result.status == "PASS"

    def test_failed_zero(self):
        assert self.result.failed == 0

    def test_total_ge_70(self):
        assert self.result.total >= 70

    def test_passed_ge_70(self):
        assert self.result.passed >= 70

    def test_paper_only_true(self):
        assert self.result.paper_only is True

    def test_no_broker_true(self):
        assert self.result.no_broker is True

    def test_not_investment_advice_true(self):
        assert self.result.not_investment_advice is True

    def test_schema_version(self):
        assert self.result.schema_version == "175"

    def test_checks_list_nonempty(self):
        assert len(self.result.checks) > 0

    def test_all_checks_have_name(self):
        assert all("name" in c for c in self.result.checks)

    def test_all_checks_have_passed(self):
        assert all("passed" in c for c in self.result.checks)

    def test_min_health_checks_70(self):
        assert MIN_HEALTH_CHECKS >= 70

    def test_total_meets_min_health_checks(self):
        assert self.result.total >= MIN_HEALTH_CHECKS

    def test_version_check_passed(self):
        version_checks = [c for c in self.result.checks if "version" in c["name"]]
        assert len(version_checks) > 0
        assert all(c["passed"] for c in version_checks)

    def test_safety_check_passed(self):
        safety_checks = [c for c in self.result.checks if "safety" in c["name"]]
        assert len(safety_checks) > 0
        assert all(c["passed"] for c in safety_checks)

    def test_model_check_passed(self):
        model_checks = [c for c in self.result.checks if "model" in c["name"]]
        assert len(model_checks) > 0
        assert all(c["passed"] for c in model_checks)

    def test_scenario_check_passed(self):
        sc_checks = [c for c in self.result.checks if "scenario" in c["name"]]
        assert len(sc_checks) > 0
        assert all(c["passed"] for c in sc_checks)

    def test_fixture_check_passed(self):
        fx_checks = [c for c in self.result.checks if "fixture" in c["name"]]
        assert len(fx_checks) > 0
        assert all(c["passed"] for c in fx_checks)

    def test_cli_check_passed(self):
        cli_checks = [c for c in self.result.checks if "cli" in c["name"]]
        assert len(cli_checks) > 0
        assert all(c["passed"] for c in cli_checks)
