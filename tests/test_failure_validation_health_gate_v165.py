"""
tests/test_failure_validation_health_gate_v165.py — Health Check & Release Gate tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from paper_trading.failure_validation.health_v165 import (
    FailureInjectionRecoveryHealthCheck,
    PAPER_ONLY,
    PRODUCTION_CHAOS_ENABLED,
    REAL_FAILURE_INJECTION_ENABLED,
    RESEARCH_ONLY,
)
from release.failure_injection_recovery_release_gate_v165 import (
    FailureInjectionRecoveryReleaseGateV165,
    PAPER_ONLY as GATE_PAPER_ONLY,
    PRODUCTION_CHAOS_ENABLED as GATE_PC,
    REAL_FAILURE_INJECTION_ENABLED as GATE_RFI,
    RESEARCH_ONLY as GATE_RESEARCH_ONLY,
)


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestHealthGateSafetyFlags:
    def test_health_real_injection_disabled(self):
        assert REAL_FAILURE_INJECTION_ENABLED is False

    def test_health_production_chaos_disabled(self):
        assert PRODUCTION_CHAOS_ENABLED is False

    def test_health_paper_only(self):
        assert PAPER_ONLY is True

    def test_health_research_only(self):
        assert RESEARCH_ONLY is True

    def test_gate_real_injection_disabled(self):
        assert GATE_RFI is False

    def test_gate_production_chaos_disabled(self):
        assert GATE_PC is False

    def test_gate_paper_only(self):
        assert GATE_PAPER_ONLY is True

    def test_gate_research_only(self):
        assert GATE_RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# FailureInjectionRecoveryHealthCheck
# ---------------------------------------------------------------------------

class TestHealthCheck:
    def test_health_check_instantiates(self):
        hc = FailureInjectionRecoveryHealthCheck()
        assert hc is not None

    def test_health_check_has_expected_total(self):
        assert FailureInjectionRecoveryHealthCheck.EXPECTED_TOTAL >= 50

    def test_health_check_runs(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert summary is not None

    def test_health_check_returns_dict(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert isinstance(summary, dict)

    def test_health_check_has_total_key(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert "total" in summary

    def test_health_check_has_passed_key(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert "passed" in summary

    def test_health_check_has_failed_key(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert "failed" in summary

    def test_health_check_has_overall_key(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert "overall" in summary

    def test_health_check_has_checks_key(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert "checks" in summary

    def test_health_check_total_at_least_50(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert summary["total"] >= 50

    def test_health_check_passed_plus_failed_equals_total(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert summary["passed"] + summary["failed"] == summary["total"]

    def test_health_check_overall_is_pass_or_fail(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert summary["overall"] in {"PASS", "FAIL"}

    def test_health_check_all_checks_pass(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert summary["overall"] == "PASS", (
            f"Health check FAILED: {summary['failed']} failures: "
            + str({k: v for k, v in summary["checks"].items() if v["status"] == "FAIL"})
        )

    def test_health_check_zero_failures(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert summary["failed"] == 0

    def test_health_check_each_check_has_status(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        for name, check in summary["checks"].items():
            assert "status" in check, f"Check {name} missing status"

    def test_health_check_each_status_is_pass_or_fail(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        for name, check in summary["checks"].items():
            assert check["status"] in {"PASS", "FAIL"}, f"Check {name} has invalid status: {check['status']}"

    def test_health_check_safety_flags_pass(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert summary["checks"]["real_failure_injection_disabled"]["status"] == "PASS"
        assert summary["checks"]["production_chaos_disabled"]["status"] == "PASS"

    def test_health_check_import_checks_pass(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert summary["checks"]["import_enums"]["status"] == "PASS"
        assert summary["checks"]["import_models"]["status"] == "PASS"
        assert summary["checks"]["import_injector"]["status"] == "PASS"

    def test_health_check_scenario_count_passes(self):
        hc = FailureInjectionRecoveryHealthCheck()
        summary = hc.get_health_summary()
        assert summary["checks"]["scenario_count_ge_60"]["status"] == "PASS"


# ---------------------------------------------------------------------------
# FailureInjectionRecoveryReleaseGateV165
# ---------------------------------------------------------------------------

class TestReleaseGate:
    def test_gate_instantiates(self):
        gate = FailureInjectionRecoveryReleaseGateV165()
        assert gate is not None

    def test_gate_expected_checks_45(self):
        assert FailureInjectionRecoveryReleaseGateV165.EXPECTED_CHECKS == 45

    def test_gate_runs(self):
        gate = FailureInjectionRecoveryReleaseGateV165()
        result = gate.run()
        assert result is not None

    def test_gate_returns_dict(self):
        gate = FailureInjectionRecoveryReleaseGateV165()
        result = gate.run()
        assert isinstance(result, dict)

    def test_gate_result_has_total(self):
        gate = FailureInjectionRecoveryReleaseGateV165()
        result = gate.run()
        assert "total" in result

    def test_gate_result_has_passed(self):
        gate = FailureInjectionRecoveryReleaseGateV165()
        result = gate.run()
        assert "passed" in result

    def test_gate_result_has_gate_passed(self):
        gate = FailureInjectionRecoveryReleaseGateV165()
        result = gate.run()
        assert "gate_passed" in result

    def test_gate_total_is_45(self):
        gate = FailureInjectionRecoveryReleaseGateV165()
        result = gate.run()
        assert result["total"] == 45

    def test_gate_passed_plus_failed_equals_total(self):
        gate = FailureInjectionRecoveryReleaseGateV165()
        result = gate.run()
        assert result["passed"] + result["failed"] == result["total"]

    def test_gate_passes_45_45(self):
        gate = FailureInjectionRecoveryReleaseGateV165()
        result = gate.run()
        assert result["gate_passed"] is True, (
            f"Gate FAILED: {result['failed']}/45 failures: "
            + str({k: v for k, v in result.get("checks", {}).items() if v.get("status") == "FAIL"})
        )

    def test_gate_45_passed(self):
        gate = FailureInjectionRecoveryReleaseGateV165()
        result = gate.run()
        assert result["passed"] == 45

    def test_gate_zero_failed(self):
        gate = FailureInjectionRecoveryReleaseGateV165()
        result = gate.run()
        assert result["failed"] == 0
