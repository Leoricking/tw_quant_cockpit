"""tests/test_theme_rotation_health_v177.py — v1.7.7 health check tests."""
import pytest
from paper_trading.small_capital_strategy.theme_rotation_health_v177 import run_health_check


class TestRunHealthCheck:
    def test_returns_health_summary(self):
        from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeRotationHealthSummary
        result = run_health_check()
        assert isinstance(result, ThemeRotationHealthSummary)

    def test_all_passed(self):
        result = run_health_check()
        assert result.all_passed is True, f"Failed checks: {[c for c in result.checks if not c['passed']]}"

    def test_status_pass(self):
        result = run_health_check()
        assert result.status == "PASS"

    def test_failed_zero(self):
        result = run_health_check()
        assert result.failed == 0

    def test_total_ge_70(self):
        result = run_health_check()
        assert result.total >= 70

    def test_passed_ge_70(self):
        result = run_health_check()
        assert result.passed >= 70

    def test_checks_is_list(self):
        result = run_health_check()
        assert isinstance(result.checks, list)

    def test_paper_only_true(self):
        result = run_health_check()
        assert result.paper_only is True

    def test_schema_version_177(self):
        result = run_health_check()
        assert result.schema_version == "177"

    def test_all_checks_have_name(self):
        result = run_health_check()
        for c in result.checks:
            assert "name" in c
            assert len(c["name"]) > 0
