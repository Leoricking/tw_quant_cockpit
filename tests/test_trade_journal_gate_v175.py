"""
tests/test_trade_journal_gate_v175.py
Tests for Trade Journal release gate v1.7.5.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from release.small_account_trade_journal_release_gate_v175 import (
    run_gate, SmallAccountTradeJournalReleaseGate, GATE_VERSION, MIN_CHECKS,
)


class TestGateConstants:
    def test_gate_version_175(self):
        assert GATE_VERSION == "1.7.5"

    def test_min_checks_65(self):
        assert MIN_CHECKS >= 65


class TestRunGate:
    @classmethod
    def setup_class(cls):
        cls.result = run_gate()

    def test_gate_passed_true(self):
        failed = [c for c in self.result["checks"] if not c["passed"]]
        assert self.result["gate_passed"] is True, f"Failed checks: {failed}"

    def test_failed_zero(self):
        assert self.result["failed"] == 0

    def test_total_ge_65(self):
        assert self.result["total"] >= 65

    def test_passed_ge_65(self):
        assert self.result["passed"] >= 65

    def test_returns_dict(self):
        assert isinstance(self.result, dict)

    def test_gate_version_in_result(self):
        assert self.result["gate_version"] == "1.7.5"

    def test_checks_list_nonempty(self):
        assert len(self.result["checks"]) > 0

    def test_all_checks_have_name(self):
        assert all("name" in c for c in self.result["checks"])

    def test_all_checks_have_passed(self):
        assert all("passed" in c for c in self.result["checks"])

    def test_health_checks_pass(self):
        health = [c for c in self.result["checks"] if c["name"].startswith("health")]
        assert len(health) > 0
        assert all(c["passed"] for c in health)

    def test_safety_checks_pass(self):
        safety = [c for c in self.result["checks"] if c["name"].startswith("safety")]
        assert len(safety) > 0
        assert all(c["passed"] for c in safety)

    def test_version_checks_pass(self):
        version = [c for c in self.result["checks"] if c["name"].startswith("gate_version")]
        assert len(version) > 0
        assert all(c["passed"] for c in version)

    def test_scenario_check_passes(self):
        sc = [c for c in self.result["checks"] if "scenario" in c["name"]]
        assert len(sc) > 0
        assert all(c["passed"] for c in sc)

    def test_fixture_check_passes(self):
        fx = [c for c in self.result["checks"] if "fixture" in c["name"]]
        assert len(fx) > 0
        assert all(c["passed"] for c in fx)


class TestGateClass:
    def test_gate_class_instantiation(self):
        gate = SmallAccountTradeJournalReleaseGate()
        assert gate is not None

    def test_gate_class_run_returns_dict(self):
        result = SmallAccountTradeJournalReleaseGate().run()
        assert isinstance(result, dict)

    def test_gate_class_gate_passed(self):
        result = SmallAccountTradeJournalReleaseGate().run()
        assert result["gate_passed"] is True
