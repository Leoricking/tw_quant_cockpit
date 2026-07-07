"""
tests/test_market_regime_gate_v173.py
Tests for Market Regime Position Control release gate v1.7.3.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from release.market_regime_position_control_release_gate_v173 import (
    run_release_gate, MarketRegimePositionControlReleaseGate, GATE_VERSION, MIN_CHECKS,
)


class TestRunReleaseGate:
    def test_gate_passed_true(self):
        result = run_release_gate()
        assert result["gate_passed"] is True

    def test_failed_count_zero(self):
        result = run_release_gate()
        assert result["failed_count"] == 0

    def test_total_count_ge_65(self):
        result = run_release_gate()
        assert result["total_count"] >= 65

    def test_passed_equals_total(self):
        result = run_release_gate()
        assert result["passed"] == result["total_count"]

    def test_gate_version_173(self):
        result = run_release_gate()
        assert result["gate_version"] == "1.7.3"

    def test_paper_only(self):
        result = run_release_gate()
        assert result["paper_only"] is True

    def test_no_real_orders(self):
        result = run_release_gate()
        assert result["no_real_orders"] is True

    def test_not_investment_advice(self):
        result = run_release_gate()
        assert result["not_investment_advice"] is True

    def test_checks_list_not_empty(self):
        result = run_release_gate()
        assert len(result["checks"]) > 0

    def test_all_checks_passed(self):
        result = run_release_gate()
        for check in result["checks"]:
            assert check["passed"] is True, f"Gate check failed: {check['name']}: {check.get('detail')}"


class TestGateConstants:
    def test_gate_version_173(self):
        assert GATE_VERSION == "1.7.3"

    def test_min_checks_65(self):
        assert MIN_CHECKS == 65


class TestGateClass:
    def test_run_returns_dict(self):
        gate = MarketRegimePositionControlReleaseGate()
        result = gate.run()
        assert isinstance(result, dict)

    def test_gate_passed_key(self):
        gate = MarketRegimePositionControlReleaseGate()
        result = gate.run()
        assert "gate_passed" in result
