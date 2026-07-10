"""tests/test_integrated_strategy_health_v178.py — v1.7.8 integrated strategy health check tests."""
import pytest
from paper_trading.small_capital_strategy.integrated_strategy_health_v178 import (
    run_health_check,
    MIN_HEALTH_CHECKS,
)


class TestMinHealthChecksConstant:
    def test_min_health_checks_equals_70(self):
        assert MIN_HEALTH_CHECKS == 70


class TestRunHealthCheckReturnType:
    def test_returns_object(self):
        result = run_health_check()
        assert result is not None

    def test_returns_integrated_health_summary(self):
        from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import IntegratedHealthSummary
        result = run_health_check()
        assert isinstance(result, IntegratedHealthSummary)


class TestRunHealthCheckPassedStatus:
    def test_all_passed_is_true(self):
        result = run_health_check()
        failed = [c for c in result.checks if not c["passed"]]
        assert result.all_passed is True, f"Failed checks: {failed}"

    def test_failed_equals_zero(self):
        result = run_health_check()
        assert result.failed == 0

    def test_status_is_pass(self):
        result = run_health_check()
        assert result.status == "PASS"

    def test_total_ge_70(self):
        result = run_health_check()
        assert result.total >= 70

    def test_passed_ge_70(self):
        result = run_health_check()
        assert result.passed >= 70

    def test_passed_equals_total(self):
        result = run_health_check()
        assert result.passed == result.total


class TestRunHealthCheckSafetyFlags:
    def test_paper_only_is_true(self):
        result = run_health_check()
        assert result.paper_only is True

    def test_research_only_is_true(self):
        result = run_health_check()
        assert result.research_only is True

    def test_no_real_orders_is_true(self):
        result = run_health_check()
        assert result.no_real_orders is True

    def test_no_broker_is_true(self):
        result = run_health_check()
        assert result.no_broker is True

    def test_not_investment_advice_is_true(self):
        result = run_health_check()
        assert result.not_investment_advice is True


class TestRunHealthCheckVersionFields:
    def test_schema_version_is_178(self):
        result = run_health_check()
        assert result.schema_version == "178"

    def test_policy_version_correct(self):
        result = run_health_check()
        assert result.policy_version == "1.7.8-small-capital-strategy-integration"


class TestRunHealthCheckChecks:
    def test_checks_is_list(self):
        result = run_health_check()
        assert isinstance(result.checks, list)

    def test_checks_len_ge_70(self):
        result = run_health_check()
        assert len(result.checks) >= 70

    def test_every_check_has_name_key(self):
        result = run_health_check()
        for c in result.checks:
            assert "name" in c, f"Check missing 'name' key: {c}"

    def test_every_check_has_passed_key(self):
        result = run_health_check()
        for c in result.checks:
            assert "passed" in c, f"Check missing 'passed' key: {c}"

    def test_every_check_has_error_key(self):
        result = run_health_check()
        for c in result.checks:
            assert "error" in c, f"Check missing 'error' key: {c}"

    def test_all_checks_passed(self):
        result = run_health_check()
        for c in result.checks:
            assert c["passed"] is True, f"Check '{c['name']}' failed"

    def test_all_check_errors_are_none(self):
        result = run_health_check()
        for c in result.checks:
            assert c["error"] is None, f"Check '{c['name']}' has error: {c['error']}"

    def test_failed_check_list_is_empty(self):
        result = run_health_check()
        failed = [c for c in result.checks if not c["passed"]]
        assert failed == []


class TestRunHealthCheckNamedChecks:
    def _get_check(self, name):
        result = run_health_check()
        for c in result.checks:
            if c["name"] == name:
                return c
        return None

    def test_version_178_check_passes(self):
        c = self._get_check("version_178")
        assert c is not None, "Check 'version_178' not found"
        assert c["passed"] is True

    def test_safety_audit_all_safe_passes(self):
        c = self._get_check("safety_audit_all_safe")
        assert c is not None, "Check 'safety_audit_all_safe' not found"
        assert c["passed"] is True

    def test_model_input_paper_only_passes(self):
        c = self._get_check("model_input_paper_only")
        assert c is not None, "Check 'model_input_paper_only' not found"
        assert c["passed"] is True

    def test_scenarios_min_70_passes(self):
        c = self._get_check("scenarios_min_70")
        assert c is not None, "Check 'scenarios_min_70' not found"
        assert c["passed"] is True

    def test_fixtures_min_70_passes(self):
        c = self._get_check("fixtures_min_70")
        assert c is not None, "Check 'fixtures_min_70' not found"
        assert c["passed"] is True

    def test_cli_integrated_cmds_ge_17_passes(self):
        c = self._get_check("cli_integrated_cmds_ge_17")
        assert c is not None, "Check 'cli_integrated_cmds_ge_17' not found"
        assert c["passed"] is True

    def test_gui_panel_version_178_passes(self):
        c = self._get_check("gui_panel_version_178")
        assert c is not None, "Check 'gui_panel_version_178' not found"
        assert c["passed"] is True

    def test_backward_compat_v177_passes(self):
        c = self._get_check("backward_compat_v177")
        assert c is not None, "Check 'backward_compat_v177' not found"
        assert c["passed"] is True

    def test_backward_compat_v176_passes(self):
        c = self._get_check("backward_compat_v176")
        assert c is not None, "Check 'backward_compat_v176' not found"
        assert c["passed"] is True

    def test_no_broker_check_passes(self):
        c = self._get_check("no_broker")
        assert c is not None, "Check 'no_broker' not found"
        assert c["passed"] is True

    def test_no_real_account_check_passes(self):
        c = self._get_check("no_real_account")
        assert c is not None, "Check 'no_real_account' not found"
        assert c["passed"] is True


class TestRunHealthCheckDeterminism:
    def test_result_is_deterministic(self):
        result1 = run_health_check()
        result2 = run_health_check()
        assert result1.total == result2.total
        assert result1.passed == result2.passed
        assert result1.failed == result2.failed
        assert result1.status == result2.status
        assert result1.all_passed == result2.all_passed
