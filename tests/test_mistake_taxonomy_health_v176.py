"""tests/test_mistake_taxonomy_health_v176.py — v1.7.6 health check tests."""
import pytest
from paper_trading.small_capital_strategy.mistake_taxonomy_health_v176 import (
    run_health_check,
)


class TestHealthCheck:
    def test_all_passed(self):
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

    def test_passed_equals_total(self):
        result = run_health_check()
        assert result.passed == result.total

    def test_paper_only(self):
        result = run_health_check()
        assert result.paper_only is True

    def test_schema_version_176(self):
        result = run_health_check()
        assert result.schema_version == "176"

    def test_checks_list_not_empty(self):
        result = run_health_check()
        assert len(result.checks) > 0

    def test_no_checks_with_errors(self):
        result = run_health_check()
        assert all(c["error"] is None for c in result.checks if c["passed"])

    def test_source_lineage_set(self):
        result = run_health_check()
        assert "v176" in result.source_lineage
