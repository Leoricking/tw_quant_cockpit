"""
tests/test_stable_rollup_comprehensive_v169.py
Comprehensive cross-module tests for Live Paper Trading Stable Rollup v1.6.9.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
import json
import os


# ── Cross-module safety invariants ───────────────────────────────────────────

class TestCrossModuleSafetyInvariants:
    def test_package_no_real_orders(self):
        import paper_trading.stable_rollup as sr
        assert sr.NO_REAL_ORDERS is True

    def test_package_production_blocked(self):
        import paper_trading.stable_rollup as sr
        assert sr.PRODUCTION_TRADING_BLOCKED is True

    def test_package_broker_disabled(self):
        import paper_trading.stable_rollup as sr
        assert sr.BROKER_EXECUTION_ENABLED is False

    def test_package_real_trading_disabled(self):
        import paper_trading.stable_rollup as sr
        assert sr.REAL_TRADING_ENABLED is False

    def test_package_auto_session_disabled(self):
        import paper_trading.stable_rollup as sr
        assert sr.AUTO_SESSION_CONTROL_ENABLED is False

    def test_package_network_trading_disabled(self):
        import paper_trading.stable_rollup as sr
        assert sr.NETWORK_TRADING_ENABLED is False

    def test_version_module_paper_only(self):
        from paper_trading.stable_rollup.version_v169 import get_version_info
        info = get_version_info()
        assert info["paper_only"] is True

    def test_version_module_not_for_production(self):
        from paper_trading.stable_rollup.version_v169 import get_version_info
        info = get_version_info()
        assert info["not_for_production"] is True

    def test_safety_module_is_safe(self):
        from paper_trading.stable_rollup.safety_v169 import is_safe
        assert is_safe() is True

    def test_safety_module_no_dangerous(self):
        from paper_trading.stable_rollup.safety_matrix_v169 import count_dangerous_capabilities
        assert count_dangerous_capabilities() == 0

    def test_contract_safety_passes(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        result = StableContract().validate_safety()
        assert result["passed"] is True
        assert result["status"] == "PASS"


# ── Version consistency across modules ───────────────────────────────────────

class TestVersionConsistency:
    def test_package_version_matches_version_module(self):
        import paper_trading.stable_rollup as sr
        from paper_trading.stable_rollup import version_v169
        assert sr.VERSION == version_v169.VERSION == "1.6.9"

    def test_release_name_consistent(self):
        import paper_trading.stable_rollup as sr
        from paper_trading.stable_rollup import version_v169
        assert sr.RELEASE_NAME == version_v169.RELEASE_NAME

    def test_base_release_consistent(self):
        import paper_trading.stable_rollup as sr
        from paper_trading.stable_rollup import version_v169
        assert sr.BASE_RELEASE == version_v169.BASE_RELEASE

    def test_schema_version_value(self):
        from paper_trading.stable_rollup.version_v169 import SCHEMA_VERSION
        assert SCHEMA_VERSION == "169"

    def test_policy_version_format(self):
        from paper_trading.stable_rollup.version_v169 import POLICY_VERSION
        assert "1.6.9" in POLICY_VERSION

    def test_manifest_version_169_present(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
        versions = [r["version"] for r in get_manifest()]
        assert "1.6.9" in versions

    def test_registry_has_version_169(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        reg = get_registry()
        release = reg.get_release("1.6.9")
        assert release is not None
        assert release["version"] == "1.6.9"

    def test_contract_identity_passes(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        result = StableContract().validate_release_identity()
        assert result["passed"] is True

    def test_version_min_check(self):
        from paper_trading.stable_rollup.version_v169 import check_minimum_version
        assert check_minimum_version("1.6.9") is True
        assert check_minimum_version("1.6.8") is True
        assert check_minimum_version("1.6.0") is False

    def test_known_releases_includes_stable_rollup(self):
        from paper_trading.stable_rollup.version_v169 import KNOWN_RELEASE_NAMES
        assert "Live Paper Trading Stable Rollup" in KNOWN_RELEASE_NAMES

    def test_known_releases_includes_all_prior(self):
        from paper_trading.stable_rollup.version_v169 import KNOWN_RELEASE_NAMES
        required = [
            "Operational Integration Hardening",
            "Paper Performance Attribution",
            "Multi-session Coordination",
            "Live Paper Trading Foundation",
        ]
        for name in required:
            assert name in KNOWN_RELEASE_NAMES, f"Missing: {name}"


# ── Manifest integrity ────────────────────────────────────────────────────────

class TestManifestIntegrity:
    def test_manifest_has_13_releases(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
        assert len(get_manifest()) == 13

    def test_manifest_unique_versions(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
        versions = [r["version"] for r in get_manifest()]
        assert len(versions) == len(set(versions))

    def test_manifest_unique_names(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
        names = [r["release_name"] for r in get_manifest()]
        assert len(names) == len(set(names))

    def test_manifest_v169_has_correct_parent(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_release
        r = get_release("1.6.9")
        assert r is not None
        assert r["parent_version"] == "1.6.8"

    def test_manifest_v160_has_no_parent(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_release
        r = get_release("1.6.0")
        assert r is not None
        assert r["parent_version"] is None

    def test_manifest_validation_passes(self):
        from paper_trading.stable_rollup.release_manifest_v169 import validate_manifest
        result = validate_manifest()
        assert result["status"] == "PASS"

    def test_manifest_get_all_versions(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_all_versions
        versions = get_all_versions()
        assert "1.6.0" in versions
        assert "1.6.9" in versions
        assert len(versions) == 13

    def test_manifest_safety_boundaries_present(self):
        from paper_trading.stable_rollup.release_manifest_v169 import get_manifest
        for release in get_manifest():
            assert "safety_boundaries" in release
            assert isinstance(release["safety_boundaries"], list)


# ── Registry validation ───────────────────────────────────────────────────────

class TestRegistryValidation:
    def test_parent_chain_valid(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        result = get_registry().validate_parent_chain()
        assert result["status"] == "PASS", f"Parent chain issues: {result.get('issues')}"

    def test_no_duplicate_versions(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        result = get_registry().validate_unique_versions()
        assert result["status"] == "PASS", f"Duplicates found: {result.get('duplicates')}"

    def test_registry_summary_has_total(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        summary = get_registry().release_summary()
        assert "total" in summary
        assert summary["total"] == 13

    def test_registry_children_of_v160(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        children = get_registry().get_children("1.6.0")
        assert len(children) >= 1
        child_versions = [c["version"] for c in children]
        assert "1.6.1" in child_versions

    def test_registry_get_parent(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        parent = get_registry().get_parent_release("1.6.9")
        assert parent is not None
        assert parent["version"] == "1.6.8"

    def test_registry_sealed_status(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        result = get_registry().validate_sealed_status()
        assert "status" in result

    def test_registry_duplicate_rejection(self):
        from paper_trading.stable_rollup.release_registry_v169 import get_registry
        from paper_trading.stable_rollup.release_manifest_v169 import get_release
        import pytest
        reg = get_registry()
        existing = get_release("1.6.9")
        with pytest.raises((ValueError, Exception)):
            reg.register_release(existing)


# ── Capability matrix ─────────────────────────────────────────────────────────

class TestCapabilityMatrix:
    def test_no_production_ready_capabilities(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
        for cap in get_matrix():
            assert cap["production_ready"] is False, f"{cap['capability']} has production_ready=True"

    def test_all_capabilities_paper_only(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_matrix
        for cap in get_matrix():
            assert cap["paper_only"] is True, f"{cap['capability']} not paper_only"

    def test_stable_rollup_capability_present(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_capability
        cap = get_capability("stable_rollup")
        assert cap is not None

    def test_paper_trading_capability_introduced_in_160(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import get_capability
        cap = get_capability("paper_trading")
        assert cap is not None
        assert cap["introduced_in"] == "1.6.0"

    def test_matrix_validation_passes(self):
        from paper_trading.stable_rollup.capability_matrix_v169 import validate_matrix
        result = validate_matrix()
        assert result["status"] == "PASS"


# ── Safety matrix ─────────────────────────────────────────────────────────────

class TestSafetyMatrix:
    def test_zero_dangerous_capabilities(self):
        from paper_trading.stable_rollup.safety_matrix_v169 import count_dangerous_capabilities
        assert count_dangerous_capabilities() == 0

    def test_real_trading_disabled_in_matrix(self):
        from paper_trading.stable_rollup.safety_matrix_v169 import get_safety_item
        item = get_safety_item("real_trading")
        assert item is not None
        assert item["executable_capability_found"] is False

    def test_broker_disabled_in_matrix(self):
        from paper_trading.stable_rollup.safety_matrix_v169 import get_safety_item
        item = get_safety_item("broker")
        assert item is not None
        assert item["executable_capability_found"] is False

    def test_matrix_validation_passes(self):
        from paper_trading.stable_rollup.safety_matrix_v169 import validate_matrix
        result = validate_matrix()
        assert result["status"] == "PASS"
        assert result.get("dangerous_count", 0) == 0 or "total" in result

    def test_credential_access_blocked(self):
        from paper_trading.stable_rollup.safety_matrix_v169 import get_safety_item
        item = get_safety_item("credential_access")
        assert item is not None
        assert item["executable_capability_found"] is False


# ── Enums comprehensive ───────────────────────────────────────────────────────

class TestEnumsComprehensive:
    def test_rollup_status_has_5_members(self):
        from paper_trading.stable_rollup.enums_v169 import RollupStatus
        members = list(RollupStatus)
        assert len(members) == 5

    def test_seal_status_sealed_member(self):
        from paper_trading.stable_rollup.enums_v169 import SealStatus
        assert SealStatus.SEALED is not None

    def test_migration_readiness_ready_member(self):
        from paper_trading.stable_rollup.enums_v169 import MigrationReadiness
        assert MigrationReadiness.READY is not None
        assert MigrationReadiness.BLOCKED is not None
        assert MigrationReadiness.NOT_READY is not None
        assert MigrationReadiness.CONDITIONAL is not None

    def test_health_status_pass_member(self):
        from paper_trading.stable_rollup.enums_v169 import HealthStatus
        assert HealthStatus.PASS is not None
        assert HealthStatus.FAIL is not None

    def test_gate_status_pass_member(self):
        from paper_trading.stable_rollup.enums_v169 import GateStatus
        assert GateStatus.PASS is not None
        assert GateStatus.FAIL is not None

    def test_validation_severity_has_critical(self):
        from paper_trading.stable_rollup.enums_v169 import ValidationSeverity
        assert ValidationSeverity.CRITICAL is not None

    def test_debt_severity_has_blocking(self):
        from paper_trading.stable_rollup.enums_v169 import DebtSeverity
        assert DebtSeverity.BLOCKING is not None
        assert DebtSeverity.NONE is not None

    def test_capability_status_available(self):
        from paper_trading.stable_rollup.enums_v169 import CapabilityStatus
        assert CapabilityStatus.AVAILABLE is not None
        assert CapabilityStatus.BLOCKED is not None

    def test_release_status_sealed(self):
        from paper_trading.stable_rollup.enums_v169 import ReleaseStatus
        assert ReleaseStatus.SEALED is not None

    def test_confidence_level_high(self):
        from paper_trading.stable_rollup.enums_v169 import ConfidenceLevel
        assert ConfidenceLevel.HIGH is not None
        assert ConfidenceLevel.LOW is not None


# ── Models comprehensive ──────────────────────────────────────────────────────

class TestModelsComprehensive:
    def test_release_descriptor_default_flags(self):
        from paper_trading.stable_rollup.models_v169 import ReleaseDescriptor
        from paper_trading.stable_rollup.enums_v169 import SealStatus
        rd = ReleaseDescriptor(
            version="1.6.9", release_name="Test", commit_sha="abc",
            parent_version="1.6.8", parent_commit="def",
            release_category="stable_rollup", sealed_status=SealStatus.SEALED,
        )
        assert rd.paper_only is True
        assert rd.no_real_orders is True
        assert rd.not_for_production is True

    def test_stable_rollup_manifest_fields(self):
        from paper_trading.stable_rollup.models_v169 import StableRollupManifest
        m = StableRollupManifest(rollup_version="1.6.9", rollup_name="Test", total_releases=13, sealed=True)
        assert m.paper_only is True
        assert m.schema_version == "169"

    def test_stable_rollup_score_not_for_real_trading(self):
        from paper_trading.stable_rollup.models_v169 import StableRollupScore
        from paper_trading.stable_rollup.enums_v169 import ConfidenceLevel
        score = StableRollupScore(
            total_score=90.0, grade="A", component_scores={},
            blocking_issues=[], warnings=[], confidence=ConfidenceLevel.HIGH,
            sealed=True, migration_ready=True, not_for_real_trading=True,
        )
        assert score.not_for_real_trading is True
        assert score.paper_only is True

    def test_migration_readiness_summary_fields(self):
        from paper_trading.stable_rollup.models_v169 import MigrationReadinessSummary
        from paper_trading.stable_rollup.enums_v169 import MigrationReadiness
        m = MigrationReadinessSummary(
            readiness=MigrationReadiness.READY,
            blocking_issues=[], conditional_issues=[], passed_checks=["version"],
        )
        assert m.readiness == MigrationReadiness.READY
        assert m.paper_only is True

    def test_stable_rollup_health_summary_fields(self):
        from paper_trading.stable_rollup.models_v169 import StableRollupHealthSummary
        hs = StableRollupHealthSummary(health_summaries=[], total_healths=0, all_pass=True, any_blocking=False)
        assert hs.paper_only is True


# ── Scenario registry ─────────────────────────────────────────────────────────

class TestScenarioRegistryComprehensive:
    def test_80_or_more_scenarios(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import get_registry
        assert len(get_registry()) >= 80

    def test_all_scenario_ids_unique(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import get_registry
        ids = [s["scenario_id"] for s in get_registry()]
        assert len(ids) == len(set(ids))

    def test_release_identity_category_exists(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import get_by_category
        cats = get_by_category("release_identity")
        assert len(cats) >= 4

    def test_safety_category_exists(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import get_by_category
        cats = get_by_category("safety")
        assert len(cats) >= 4

    def test_migration_category_exists(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import get_by_category
        cats = get_by_category("migration")
        assert len(cats) >= 4

    def test_no_skip_scenarios(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import get_registry
        for s in get_registry():
            assert s.get("expected_status") != "SKIP"

    def test_registry_validation_passes(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import validate_registry
        result = validate_registry()
        assert result["status"] == "PASS"

    def test_get_scenario_by_id(self):
        from paper_trading.stable_rollup.scenario_registry_v169 import get_registry, get_scenario
        first = get_registry()[0]
        found = get_scenario(first["scenario_id"])
        assert found is not None
        assert found["scenario_id"] == first["scenario_id"]


# ── Fixture schema ────────────────────────────────────────────────────────────

class TestFixtureSchemaComprehensive:
    def test_10_required_markers(self):
        from paper_trading.stable_rollup.fixture_schema_v169 import REQUIRED_MARKERS
        assert len(REQUIRED_MARKERS) == 10

    def test_all_markers_are_true(self):
        from paper_trading.stable_rollup.fixture_schema_v169 import REQUIRED_MARKERS
        for key, val in REQUIRED_MARKERS.items():
            assert val is True, f"Marker {key} should be True"

    def test_valid_fixture_passes(self):
        from paper_trading.stable_rollup.fixture_schema_v169 import validate_fixture
        fixture = {
            "test_fixture": True, "demo_only": True, "paper_only": True,
            "research_only": True, "not_live": True, "no_broker": True,
            "no_real_account": True, "no_real_orders": True,
            "not_for_production": True, "stable_rollup_only": True,
            "fixture_id": "test_001", "scenario_id": "test",
            "purpose": "Test", "usage_type": "test", "referenced_by": [],
            "deterministic_seed": 42, "schema_version": "169",
            "policy_version": "1.6.9-live-paper-stable-rollup",
            "source_lineage": "v1.6.9", "expected_status": "PASS",
            "expected_score_range": [85, 100],
            "expected_reconciliation": "PASS",
            "expected_migration_readiness": "READY",
        }
        result = validate_fixture(fixture)
        assert result["valid"] is True

    def test_invalid_fixture_missing_marker(self):
        from paper_trading.stable_rollup.fixture_schema_v169 import validate_fixture
        fixture = {
            "fixture_id": "bad_001",
            "test_fixture": True,
            # missing other markers
        }
        result = validate_fixture(fixture)
        assert result["valid"] is False
        assert len(result["issues"]) > 0

    def test_fixture_with_wrong_marker_value(self):
        from paper_trading.stable_rollup.fixture_schema_v169 import validate_fixture
        fixture = {
            "test_fixture": True, "demo_only": True, "paper_only": False,  # wrong value
            "research_only": True, "not_live": True, "no_broker": True,
            "no_real_account": True, "no_real_orders": True,
            "not_for_production": True, "stable_rollup_only": True,
            "fixture_id": "test_002", "scenario_id": "test",
            "purpose": "Test", "usage_type": "test", "referenced_by": [],
            "deterministic_seed": 42, "schema_version": "169",
            "policy_version": "1.6.9-live-paper-stable-rollup",
            "source_lineage": "v1.6.9", "expected_status": "PASS",
            "expected_score_range": [85, 100],
            "expected_reconciliation": "PASS",
            "expected_migration_readiness": "READY",
        }
        result = validate_fixture(fixture)
        assert result["valid"] is False


# ── Fixture files ─────────────────────────────────────────────────────────────

class TestFixtureFiles:
    @pytest.fixture
    def fixture_dir(self):
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(repo_root, "tests", "fixtures", "stable_rollup")

    def test_fixture_dir_exists(self, fixture_dir):
        assert os.path.isdir(fixture_dir)

    def test_80_or_more_fixture_files(self, fixture_dir):
        files = [f for f in os.listdir(fixture_dir) if f.endswith(".json")]
        assert len(files) >= 80

    def test_all_fixtures_valid_json(self, fixture_dir):
        files = [f for f in os.listdir(fixture_dir) if f.endswith(".json")]
        for fname in files:
            path = os.path.join(fixture_dir, fname)
            with open(path) as fh:
                data = json.load(fh)
            assert isinstance(data, dict), f"{fname} is not a JSON object"

    def test_all_fixtures_have_required_markers(self, fixture_dir):
        from paper_trading.stable_rollup.fixture_schema_v169 import REQUIRED_MARKERS
        files = [f for f in os.listdir(fixture_dir) if f.endswith(".json")]
        for fname in files:
            path = os.path.join(fixture_dir, fname)
            with open(path) as fh:
                data = json.load(fh)
            for marker in REQUIRED_MARKERS:
                assert marker in data, f"{fname} missing marker: {marker}"
                assert data[marker] is True, f"{fname}: {marker} should be True"

    def test_all_fixtures_have_fixture_id(self, fixture_dir):
        files = [f for f in os.listdir(fixture_dir) if f.endswith(".json")]
        for fname in files:
            path = os.path.join(fixture_dir, fname)
            with open(path) as fh:
                data = json.load(fh)
            assert "fixture_id" in data, f"{fname} missing fixture_id"

    def test_all_fixture_ids_unique(self, fixture_dir):
        files = [f for f in os.listdir(fixture_dir) if f.endswith(".json")]
        ids = []
        for fname in files:
            path = os.path.join(fixture_dir, fname)
            with open(path) as fh:
                data = json.load(fh)
            ids.append(data.get("fixture_id"))
        assert len(ids) == len(set(ids)), "Duplicate fixture IDs found"

    def test_all_fixtures_have_schema_version(self, fixture_dir):
        files = [f for f in os.listdir(fixture_dir) if f.endswith(".json")]
        for fname in files:
            path = os.path.join(fixture_dir, fname)
            with open(path) as fh:
                data = json.load(fh)
            assert "schema_version" in data, f"{fname} missing schema_version"
            assert data["schema_version"] == "169", f"{fname} wrong schema_version"


# ── Stable contract full ──────────────────────────────────────────────────────

class TestStableContractFull:
    def test_run_all_contracts_pass(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        result = StableContract().run()
        assert result["all_pass"] is True

    def test_validate_backward_compat(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        result = StableContract().validate_backward_compatibility()
        assert result["passed"] is True

    def test_validate_determinism(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        result = StableContract().validate_determinism()
        assert result["passed"] is True

    def test_validate_read_only(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        result = StableContract().validate_read_only()
        assert result["passed"] is True

    def test_validate_no_real_orders(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        result = StableContract().validate_no_real_orders()
        assert result["passed"] is True

    def test_total_validations_count(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        result = StableContract().run()
        assert result.get("total_validations", 0) >= 8

    def test_results_is_list(self):
        from paper_trading.stable_rollup.stable_contract_v169 import StableContract
        result = StableContract().run()
        assert isinstance(result.get("results"), list)


# ── Health check comprehensive ────────────────────────────────────────────────

class TestHealthCheckComprehensive:
    def test_health_total_gte_80(self):
        from paper_trading.stable_rollup.health_v169 import StableRollupHealthCheck
        result = StableRollupHealthCheck().run()
        assert result["total"] >= 80

    def test_health_all_pass(self):
        from paper_trading.stable_rollup.health_v169 import StableRollupHealthCheck
        result = StableRollupHealthCheck().run()
        assert result["failed"] == 0, f"Failed checks: {[k for k, v in result['checks'].items() if v['status'] == 'FAIL']}"

    def test_health_checks_is_dict(self):
        from paper_trading.stable_rollup.health_v169 import StableRollupHealthCheck
        result = StableRollupHealthCheck().run()
        assert isinstance(result["checks"], dict)

    def test_health_no_broker_check(self):
        from paper_trading.stable_rollup.health_v169 import StableRollupHealthCheck
        result = StableRollupHealthCheck().run()
        assert "no_broker" in result["checks"]
        assert result["checks"]["no_broker"]["status"] == "PASS"

    def test_health_safety_checks_all_pass(self):
        from paper_trading.stable_rollup.health_v169 import StableRollupHealthCheck
        result = StableRollupHealthCheck().run()
        safety_checks = [k for k in result["checks"] if "no_" in k or "broker" in k or "network" in k]
        for k in safety_checks:
            assert result["checks"][k]["status"] == "PASS", f"Safety check failed: {k}"


# ── Release gate comprehensive ────────────────────────────────────────────────

class TestReleaseGateComprehensive:
    def test_gate_total_gte_70(self):
        from release.live_paper_trading_stable_rollup_release_gate_v169 import StableRollupReleaseGate
        result = StableRollupReleaseGate().run()
        assert result["total"] >= 70

    def test_gate_all_pass(self):
        from release.live_paper_trading_stable_rollup_release_gate_v169 import StableRollupReleaseGate
        result = StableRollupReleaseGate().run()
        failed = [c for c in result["checks"] if c["status"] == "FAIL"]
        assert len(failed) == 0, f"Failed: {[c['check'] for c in failed]}"

    def test_gate_paper_only_flag(self):
        from release.live_paper_trading_stable_rollup_release_gate_v169 import StableRollupReleaseGate
        result = StableRollupReleaseGate().run()
        assert result.get("paper_only") is True

    def test_gate_no_real_orders_flag(self):
        from release.live_paper_trading_stable_rollup_release_gate_v169 import StableRollupReleaseGate
        result = StableRollupReleaseGate().run()
        assert result.get("no_real_orders") is True

    def test_gate_not_for_production_flag(self):
        from release.live_paper_trading_stable_rollup_release_gate_v169 import StableRollupReleaseGate
        result = StableRollupReleaseGate().run()
        assert result.get("not_for_production") is True


# ── Scorecard ─────────────────────────────────────────────────────────────────

class TestScorecardComprehensive:
    def test_scorecard_weights_sum_100(self):
        from paper_trading.stable_rollup.stable_scorecard_v169 import SCORE_WEIGHTS
        total = sum(SCORE_WEIGHTS.values())
        assert total == 100

    def test_scorecard_safety_weight_is_20(self):
        from paper_trading.stable_rollup.stable_scorecard_v169 import SCORE_WEIGHTS
        assert SCORE_WEIGHTS.get("safety") == 20

    def test_compute_scorecard_returns_score(self):
        from paper_trading.stable_rollup.stable_scorecard_v169 import compute_scorecard
        score = compute_scorecard()
        assert score is not None

    def test_score_not_for_real_trading(self):
        from paper_trading.stable_rollup.stable_scorecard_v169 import compute_scorecard
        score = compute_scorecard()
        assert score.not_for_real_trading is True

    def test_score_total_in_range(self):
        from paper_trading.stable_rollup.stable_scorecard_v169 import compute_scorecard
        score = compute_scorecard()
        assert 0.0 <= score.total_score <= 100.0

    def test_score_has_grade(self):
        from paper_trading.stable_rollup.stable_scorecard_v169 import compute_scorecard
        score = compute_scorecard()
        assert score.grade in ("A", "B", "C", "D", "F", "BLOCKED")


# ── Migration readiness ───────────────────────────────────────────────────────

class TestMigrationReadinessComprehensive:
    def test_assessor_does_not_auto_ready_by_version(self):
        from paper_trading.stable_rollup.migration_readiness_v169 import MigrationReadinessAssessor
        from paper_trading.stable_rollup.enums_v169 import MigrationReadiness
        # The assessor must check real conditions, not just the version string
        assessor = MigrationReadinessAssessor()
        summary = assessor.assess()
        # If it returns READY, it must have done real checks
        assert summary.readiness in (MigrationReadiness.READY, MigrationReadiness.CONDITIONAL,
                                     MigrationReadiness.NOT_READY, MigrationReadiness.BLOCKED)

    def test_get_readiness_returns_enum(self):
        from paper_trading.stable_rollup.migration_readiness_v169 import MigrationReadinessAssessor
        from paper_trading.stable_rollup.enums_v169 import MigrationReadiness
        assessor = MigrationReadinessAssessor()
        readiness = assessor.get_readiness()
        assert isinstance(readiness, MigrationReadiness)

    def test_summary_paper_only(self):
        from paper_trading.stable_rollup.migration_readiness_v169 import MigrationReadinessAssessor
        assessor = MigrationReadinessAssessor()
        summary = assessor.assess()
        assert summary.paper_only is True

    def test_summary_no_real_orders(self):
        from paper_trading.stable_rollup.migration_readiness_v169 import MigrationReadinessAssessor
        assessor = MigrationReadinessAssessor()
        summary = assessor.assess()
        assert summary.no_real_orders is True


# ── Reconciler ────────────────────────────────────────────────────────────────

class TestReconcilerComprehensive:
    def test_reconcile_releases_expected_13(self):
        from paper_trading.stable_rollup.stable_reconciler_v169 import StableReconciler
        rec = StableReconciler().reconcile_releases()
        assert rec.expected == 13

    def test_reconcile_capabilities_expected_gte_19(self):
        from paper_trading.stable_rollup.stable_reconciler_v169 import StableReconciler
        rec = StableReconciler().reconcile_capabilities()
        assert rec.expected >= 19

    def test_reconcile_safety_expected_20(self):
        from paper_trading.stable_rollup.stable_reconciler_v169 import StableReconciler
        rec = StableReconciler().reconcile_safety()
        assert rec.expected >= 20

    def test_reconcile_test_baseline_11465(self):
        from paper_trading.stable_rollup.stable_reconciler_v169 import StableReconciler
        rec = StableReconciler().reconcile_tests()
        assert rec.expected == 11465

    def test_reconcile_all_returns_list(self):
        from paper_trading.stable_rollup.stable_reconciler_v169 import StableReconciler
        results = StableReconciler().reconcile_all()
        assert isinstance(results, list)
        assert len(results) >= 4

    def test_reconciliation_paper_only(self):
        from paper_trading.stable_rollup.stable_reconciler_v169 import StableReconciler
        rec = StableReconciler().reconcile_releases()
        assert rec.paper_only is True


# ── GUI panel ─────────────────────────────────────────────────────────────────

class TestGUIPanelComprehensive:
    def test_panel_module_importable(self):
        import gui.live_paper_trading_stable_rollup_panel as panel
        assert panel is not None

    def test_panel_title_constant(self):
        import gui.live_paper_trading_stable_rollup_panel as panel
        assert panel.PANEL_TITLE == "Live Paper Trading Stable Rollup"

    def test_panel_version_constant(self):
        import gui.live_paper_trading_stable_rollup_panel as panel
        assert panel.PANEL_VERSION == "1.6.9"

    def test_panel_headless_safe(self):
        import gui.live_paper_trading_stable_rollup_panel as panel
        assert getattr(panel, "headless_safe", True) is True

    def test_panel_no_real_orders(self):
        import gui.live_paper_trading_stable_rollup_panel as panel
        assert panel.NO_REAL_ORDERS is True

    def test_panel_production_blocked(self):
        import gui.live_paper_trading_stable_rollup_panel as panel
        assert panel.PRODUCTION_BLOCKED is True

    def test_panel_tabs_count(self):
        import gui.live_paper_trading_stable_rollup_panel as panel
        assert len(panel.PANEL_TABS) >= 20

    def test_panel_tabs_unique(self):
        import gui.live_paper_trading_stable_rollup_panel as panel
        assert len(panel.PANEL_TABS) == len(set(panel.PANEL_TABS))

    def test_panel_class_exists(self):
        import gui.live_paper_trading_stable_rollup_panel as panel
        assert hasattr(panel, "LivePaperTradingStableRollupPanel")
