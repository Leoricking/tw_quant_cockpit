"""
tests/test_paper_attribution_health_gate_v167.py
Tests for paper attribution health check and release gate v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from paper_trading.performance_attribution.health_v167 import PaperAttributionHealthCheck
from release.paper_performance_attribution_release_gate_v167 import PaperAttributionReleaseGate


class TestHealthCheck:
    def setup_method(self):
        self.hc = PaperAttributionHealthCheck()
        self.result = self.hc.run()

    def test_returns_dict(self):
        assert isinstance(self.result, dict)

    def test_has_status_key(self):
        assert "status" in self.result

    def test_has_checks_list(self):
        assert "checks" in self.result
        assert isinstance(self.result["checks"], list)

    def test_has_passed_count(self):
        assert "passed" in self.result

    def test_has_failed_count(self):
        assert "failed" in self.result

    def test_has_total_count(self):
        assert "total" in self.result

    def test_at_least_60_checks(self):
        assert self.result["total"] >= 60, \
            f"Expected >=60 health checks, got {self.result['total']}"

    def test_all_checks_pass(self):
        failed = [c for c in self.result["checks"] if c.get("status") == "FAIL"]
        assert len(failed) == 0, \
            f"Failed health checks: {[c['check'] for c in failed]}"

    def test_status_is_pass(self):
        assert self.result["status"] == "PASS", \
            f"Health check FAIL: {[c for c in self.result['checks'] if c['status']=='FAIL']}"

    def test_paper_only_in_result(self):
        assert self.result["paper_only"] is True

    def test_research_only_in_result(self):
        assert self.result["research_only"] is True

    def test_component_is_paper_attribution(self):
        component = self.result.get("component", "")
        assert "paper" in component and "attribution" in component

    def test_version_is_1_6_7(self):
        assert self.result.get("version") == "1.6.7"

    def test_passed_plus_failed_equals_total(self):
        assert (self.result["passed"] + self.result["failed"]) == self.result["total"]

    def test_each_check_has_status(self):
        for c in self.result["checks"]:
            assert "status" in c, f"Check missing status: {c}"
            assert c["status"] in ("PASS", "FAIL")

    def test_each_check_has_name(self):
        for c in self.result["checks"]:
            assert "check" in c, f"Check missing name: {c}"


class TestReleaseGate:
    def setup_method(self):
        self.gate = PaperAttributionReleaseGate()
        self.result = self.gate.run()

    def test_returns_dict(self):
        assert isinstance(self.result, dict)

    def test_has_status_key(self):
        assert "status" in self.result

    def test_has_checks_list(self):
        assert isinstance(self.result.get("checks"), list)

    def test_at_least_50_checks(self):
        assert self.result["total"] >= 50, \
            f"Expected >=50 gate checks, got {self.result['total']}"

    def test_all_checks_pass(self):
        failed = [c for c in self.result["checks"] if c.get("status") == "FAIL"]
        assert len(failed) == 0, \
            f"Failed gate checks: {[c['check'] for c in failed]}"

    def test_status_is_pass(self):
        assert self.result["status"] == "PASS", \
            f"Gate FAIL: {[c for c in self.result['checks'] if c['status']=='FAIL']}"

    def test_paper_only_in_result(self):
        assert self.result["paper_only"] is True

    def test_target_version_is_1_6_7(self):
        assert self.result.get("target_version") == "1.6.7"

    def test_release_name_correct(self):
        assert self.result.get("release_name") == "Paper Performance Attribution"

    def test_passed_plus_failed_equals_total(self):
        assert (self.result["passed"] + self.result["failed"]) == self.result["total"]

    def test_gate_name_in_result(self):
        assert "gate" in self.result
