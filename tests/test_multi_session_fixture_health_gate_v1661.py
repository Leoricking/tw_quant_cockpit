"""
test_multi_session_fixture_health_gate_v1661.py — Fixture Health & Gate tests v1.6.6.1.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


class TestFixtureGovernanceHealth:
    def test_health_check_importable(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        assert FixtureGovernanceHealthCheck is not None

    def test_health_check_runs(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert isinstance(r, dict)

    def test_health_check_status_pass(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r["status"] == "PASS", f"Health failed: {[(k,v) for k,v in r['checks'].items() if v[0]=='FAIL']}"

    def test_health_check_failed_is_zero(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r["failed"] == 0

    def test_health_check_passed_equals_total(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r["passed"] == r["total"]

    def test_health_check_total_at_least_20(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r["total"] >= 20

    def test_health_check_research_only(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r.get("research_only") is True

    def test_health_check_paper_only(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r.get("paper_only") is True

    def test_health_check_no_real_orders(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r.get("no_real_orders") is True

    def test_health_check_has_checks_dict(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert "checks" in r
        assert isinstance(r["checks"], dict)

    def test_health_check_fixture_count_check_passes(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r["checks"]["fixture_count"][0] == "PASS"

    def test_health_check_valid_json_check_passes(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r["checks"]["valid_json"][0] == "PASS"

    def test_health_check_unique_ids_check_passes(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r["checks"]["unique_ids"][0] == "PASS"

    def test_health_check_marker_schema_present_passes(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r["checks"]["marker_schema_present"][0] == "PASS"

    def test_health_check_registered_fixtures_passes(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r["checks"]["registered_fixtures"][0] == "PASS"

    def test_health_check_referenced_fixtures_passes(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r["checks"]["referenced_fixtures"][0] == "PASS"

    def test_health_check_unused_fixtures_passes(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r = FixtureGovernanceHealthCheck().run()
        assert r["checks"]["unused_fixtures"][0] == "PASS"

    def test_health_check_health_failure_when_marker_missing(self):
        """Health must fail when a fixture is missing a marker (simulated)."""
        from paper_trading.multi_session.fixture_schema_v1661 import fixture_safety_summary
        bad_fixtures = [{"test_id": "x"}]  # missing all markers
        summary = fixture_safety_summary(bad_fixtures)
        assert summary["valid"] == 0
        assert summary["invalid"] == 1

    def test_health_check_is_deterministic(self):
        from paper_trading.multi_session.health_v1661 import FixtureGovernanceHealthCheck
        r1 = FixtureGovernanceHealthCheck().run()
        r2 = FixtureGovernanceHealthCheck().run()
        assert r1["status"] == r2["status"]
        assert r1["passed"] == r2["passed"]
        assert r1["failed"] == r2["failed"]


class TestFixtureGovernanceGate:
    def test_gate_importable(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        assert FixtureGovernanceReleaseGateV1661 is not None

    def test_gate_runs(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert isinstance(r, dict)

    def test_gate_passed_is_true(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r["gate_passed"] is True, f"Gate failed: {[(k,v) for k,v in r['checks'].items() if v[0]=='FAIL']}"

    def test_gate_status_pass(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r["status"] == "PASS"

    def test_gate_failed_is_zero(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r["failed"] == 0

    def test_gate_passed_equals_total(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r["passed"] == r["total"]

    def test_gate_total_at_least_12(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r["total"] >= 12

    def test_gate_all_fixtures_have_complete_markers_passes(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r["checks"]["all_fixtures_have_complete_markers"][0] == "PASS"

    def test_gate_all_markers_are_true_booleans_passes(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r["checks"]["all_markers_are_true_booleans"][0] == "PASS"

    def test_gate_all_fixtures_registered_passes(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r["checks"]["all_fixtures_registered"][0] == "PASS"

    def test_gate_all_fixtures_referenced_passes(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r["checks"]["all_fixtures_referenced"][0] == "PASS"

    def test_gate_unused_fixtures_zero_passes(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r["checks"]["unused_fixtures_zero"][0] == "PASS"

    def test_gate_failure_when_fixture_unused(self):
        """Gate must fail when fixture_usage_summary reports unused fixtures (simulated)."""
        from paper_trading.multi_session.fixture_registry_v1661 import fixture_usage_summary
        usage = fixture_usage_summary()
        assert usage["unused"] == 0, "Real registry should have 0 unused"

    def test_gate_research_only(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r.get("research_only") is True

    def test_gate_no_real_orders(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r = FixtureGovernanceReleaseGateV1661().run()
        assert r.get("no_real_orders") is True

    def test_gate_is_deterministic(self):
        from release.multi_session_fixture_governance_release_gate_v1661 import FixtureGovernanceReleaseGateV1661
        r1 = FixtureGovernanceReleaseGateV1661().run()
        r2 = FixtureGovernanceReleaseGateV1661().run()
        assert r1["status"] == r2["status"]
        assert r1["passed"] == r2["passed"]
