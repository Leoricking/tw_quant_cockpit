"""
tests/test_operational_integration_release_gate_v168.py — Release Gate tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from release.operational_integration_hardening_release_gate_v168 import (
    OperationalIntegrationReleaseGate, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
    TARGET_VERSION, RELEASE_NAME, BASE_RELEASE,
)


class TestReleaseGateSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestReleaseGateCore:
    def setup_method(self):
        self.gate = OperationalIntegrationReleaseGate()
        self._result = None

    def _get_result(self):
        if self._result is None:
            self._result = self.gate.run()
        return self._result

    def test_target_version(self):
        assert TARGET_VERSION == "1.6.8"

    def test_release_name(self):
        assert RELEASE_NAME == "Operational Integration Hardening"

    def test_base_release(self):
        assert "1.6.7" in BASE_RELEASE

    def test_run_returns_dict(self):
        result = self._get_result()
        assert isinstance(result, dict)

    def test_gate_passed_true(self):
        result = self._get_result()
        assert result["gate_passed"] is True, (
            f"Release gate failed. Failed checks: "
            f"{[c for c in result.get('checks', []) if c['status'] == 'FAIL']}"
        )

    def test_failed_zero(self):
        result = self._get_result()
        assert result["failed"] == 0, (
            f"Expected 0 failures, got {result['failed']}. "
            f"Failed: {[c['check'] for c in result.get('checks', []) if c['status'] == 'FAIL']}"
        )

    def test_passed_at_least_150(self):
        result = self._get_result()
        assert result["passed"] >= 150, f"Expected >=150 passed, got {result['passed']}"

    def test_status_pass(self):
        result = self._get_result()
        assert result["status"] == "PASS"

    def test_has_checks(self):
        result = self._get_result()
        assert "checks" in result
        assert isinstance(result["checks"], list)

    def test_has_total(self):
        result = self._get_result()
        assert "total" in result
        assert result["total"] > 0

    def test_total_equals_passed_plus_failed(self):
        result = self._get_result()
        assert result["total"] == result["passed"] + result["failed"]

    def test_gate_name_in_result(self):
        result = self._get_result()
        assert "gate" in result
        assert "168" in result["gate"]

    def test_target_version_in_result(self):
        result = self._get_result()
        assert result["target_version"] == "1.6.8"

    def test_all_checks_have_status(self):
        result = self._get_result()
        for check in result["checks"]:
            assert "status" in check
            assert check["status"] in ("PASS", "FAIL")

    def test_all_checks_have_name(self):
        result = self._get_result()
        for check in result["checks"]:
            assert "check" in check

    def test_safety_checks_pass(self):
        result = self._get_result()
        safety_checks = [c for c in result["checks"] if "safety" in c["check"].lower()]
        for sc in safety_checks:
            assert sc["status"] == "PASS", f"Safety check failed: {sc}"

    def test_version_checks_pass(self):
        result = self._get_result()
        version_checks = [c for c in result["checks"] if "version" in c["check"].lower()]
        for vc in version_checks:
            assert vc["status"] == "PASS", f"Version check failed: {vc}"

    def test_release_gate_deterministic(self):
        g1 = OperationalIntegrationReleaseGate()
        g2 = OperationalIntegrationReleaseGate()
        r1 = g1.run()
        r2 = g2.run()
        assert r1["gate_passed"] == r2["gate_passed"]
        assert r1["passed"] == r2["passed"]

    def test_total_at_least_150(self):
        result = self._get_result()
        assert result["total"] >= 150

    def test_release_name_in_result(self):
        result = self._get_result()
        assert result["release_name"] == "Operational Integration Hardening"
