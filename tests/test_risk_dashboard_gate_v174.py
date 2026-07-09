"""
tests/test_risk_dashboard_gate_v174.py
Tests for release gate v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from release.small_account_risk_dashboard_release_gate_v174 import (
    SmallAccountRiskDashboardReleaseGate, GATE_VERSION, MIN_CHECKS,
)


class TestGateConstants:
    def test_gate_version_174(self):
        assert GATE_VERSION == "1.7.4"

    def test_min_checks_65(self):
        assert MIN_CHECKS == 65


class TestRunGate:
    def setup_method(self):
        gate = SmallAccountRiskDashboardReleaseGate()
        self.result = gate.run()

    def test_returns_dict(self):
        assert isinstance(self.result, dict)

    def test_gate_passed_true(self):
        assert self.result["gate_passed"] is True

    def test_passed_ge_65(self):
        assert self.result["passed"] >= 65

    def test_failed_count_zero(self):
        assert self.result["failed_count"] == 0

    def test_total_count_ge_65(self):
        assert self.result["total_count"] >= 65

    def test_checks_list(self):
        assert isinstance(self.result["checks"], list)

    def test_checks_not_empty(self):
        assert len(self.result["checks"]) > 0


class TestGateCheckItems:
    def setup_method(self):
        gate = SmallAccountRiskDashboardReleaseGate()
        result = gate.run()
        self.checks = result["checks"]

    def test_each_has_name(self):
        for c in self.checks:
            assert "name" in c

    def test_each_has_passed(self):
        for c in self.checks:
            assert "passed" in c

    def test_all_passed(self):
        failed = [c for c in self.checks if not c["passed"]]
        assert failed == [], f"Failed gate checks: {[c['name'] for c in failed]}"

    def test_health_check_present(self):
        names = [c["name"] for c in self.checks]
        assert "health_all_passed" in names

    def test_version_check_present(self):
        names = [c["name"] for c in self.checks]
        assert "gate_version_1_7_4" in names

    def test_safety_check_present(self):
        names = [c["name"] for c in self.checks]
        assert any("safety" in n for n in names)


class TestGateIdempotent:
    def test_two_runs_same_result(self):
        gate = SmallAccountRiskDashboardReleaseGate()
        r1 = gate.run()
        r2 = gate.run()
        assert r1["gate_passed"] == r2["gate_passed"]
        assert r1["passed"] == r2["passed"]
        assert r1["failed_count"] == r2["failed_count"]
