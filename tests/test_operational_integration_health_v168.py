"""
tests/test_operational_integration_health_v168.py — Health Check tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.health_v168 import (
    OperationalIntegrationHealthCheck, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)


class TestHealthSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestHealthCheckCore:
    def setup_method(self):
        self.health = OperationalIntegrationHealthCheck()
        self._result = None

    def _get_result(self):
        if self._result is None:
            self._result = self.health.run()
        return self._result

    def test_run_returns_dict(self):
        result = self._get_result()
        assert isinstance(result, dict)

    def test_run_status_pass(self):
        result = self._get_result()
        assert result["status"] == "PASS", (
            f"Health check failed. Failed checks: "
            f"{[c for c in result.get('checks', []) if c['status'] == 'FAIL']}"
        )

    def test_run_failed_zero(self):
        result = self._get_result()
        assert result["failed"] == 0, (
            f"Expected 0 failures, got {result['failed']}. "
            f"Failed: {[c['check'] for c in result.get('checks', []) if c['status'] == 'FAIL']}"
        )

    def test_run_passed_at_least_145(self):
        result = self._get_result()
        assert result["passed"] >= 145, f"Expected >=145 passed, got {result['passed']}"

    def test_run_has_checks(self):
        result = self._get_result()
        assert "checks" in result
        assert isinstance(result["checks"], list)

    def test_run_paper_only(self):
        result = self._get_result()
        assert result["paper_only"] is True

    def test_run_research_only(self):
        result = self._get_result()
        assert result["research_only"] is True

    def test_run_has_total(self):
        result = self._get_result()
        assert "total" in result
        assert result["total"] > 0

    def test_total_equals_passed_plus_failed(self):
        result = self._get_result()
        assert result["total"] == result["passed"] + result["failed"]

    def test_all_checks_have_status(self):
        result = self._get_result()
        for check in result["checks"]:
            assert "status" in check
            assert check["status"] in ("PASS", "FAIL")

    def test_all_checks_have_check_name(self):
        result = self._get_result()
        for check in result["checks"]:
            assert "check" in check
            assert len(check["check"]) > 0

    def test_version_check_passes(self):
        result = self._get_result()
        version_checks = [c for c in result["checks"] if "version" in c["check"]]
        assert len(version_checks) > 0
        for vc in version_checks:
            assert vc["status"] == "PASS", f"Version check failed: {vc}"

    def test_safety_checks_pass(self):
        result = self._get_result()
        safety_checks = [c for c in result["checks"] if "safety" in c["check"]]
        for sc in safety_checks:
            assert sc["status"] == "PASS", f"Safety check failed: {sc}"

    def test_pipeline_check_present(self):
        result = self._get_result()
        pipeline_checks = [c for c in result["checks"] if "pipeline" in c["check"].lower()]
        assert len(pipeline_checks) > 0

    def test_contract_check_present(self):
        result = self._get_result()
        contract_checks = [c for c in result["checks"] if "contract" in c["check"].lower()]
        assert len(contract_checks) > 0

    def test_scorecard_check_present(self):
        result = self._get_result()
        scorecard_checks = [c for c in result["checks"] if "scorecard" in c["check"].lower()]
        assert len(scorecard_checks) > 0

    def test_health_check_deterministic(self):
        h1 = OperationalIntegrationHealthCheck()
        h2 = OperationalIntegrationHealthCheck()
        r1 = h1.run()
        r2 = h2.run()
        assert r1["status"] == r2["status"]
        assert r1["passed"] == r2["passed"]

    def test_gui_check_present(self):
        result = self._get_result()
        gui_checks = [c for c in result["checks"] if "gui" in c["check"].lower()]
        assert len(gui_checks) > 0

    def test_scenarios_check_present(self):
        result = self._get_result()
        scenario_checks = [c for c in result["checks"] if "scenario" in c["check"].lower()]
        assert len(scenario_checks) > 0

    def test_fixture_check_present(self):
        result = self._get_result()
        fixture_checks = [c for c in result["checks"] if "fixture" in c["check"].lower()]
        assert len(fixture_checks) > 0

    def test_cli_check_present(self):
        result = self._get_result()
        cli_checks = [c for c in result["checks"] if "cli" in c["check"].lower()]
        assert len(cli_checks) > 0

    def test_total_at_least_145(self):
        result = self._get_result()
        assert result["total"] >= 145
