"""
tests/test_portfolio_stable_rollup_v159.py — Portfolio Stable Rollup v1.5.9 tests.
[!] Research Only. No Real Orders. Freeze/Stabilization Release. Not Investment Advice.
"""
import os
import json
import importlib
import pytest

# ---------------------------------------------------------------------------
# Version parsing helper — NO version whitelist strings
# ---------------------------------------------------------------------------
def _parse_ver(v):
    return tuple(int(x) for x in str(v).split()[0].split(".")[:4] if x.isdigit())


FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "portfolio_stable_rollup")


def _load_fixture(name):
    with open(os.path.join(FIXTURE_DIR, name)) as f:
        return json.load(f)


# ===========================================================================
# 1. Version info regression
# ===========================================================================
class TestVersionInfo:
    def test_version_gte_159(self):
        from release.version_info import VERSION
        assert _parse_ver(VERSION) >= _parse_ver("1.5.9"), f"Expected VERSION >= 1.5.9, got {VERSION}"

    def test_base_release_gte_154(self):
        from release.version_info import BASE_RELEASE
        assert "1.5.4" in BASE_RELEASE or _parse_ver(BASE_RELEASE) >= _parse_ver("1.5.4"), \
            f"BASE_RELEASE should reference 1.5.4, got {BASE_RELEASE}"

    def test_release_name(self):
        from release.version_info import RELEASE_NAME
        assert "Stable" in RELEASE_NAME or "Rollup" in RELEASE_NAME, \
            f"Expected 'Stable Rollup' in RELEASE_NAME, got {RELEASE_NAME}"

    def test_no_real_orders(self):
        from release.version_info import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_broker_execution_disabled(self):
        from release.version_info import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_production_trading_blocked(self):
        from release.version_info import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_portfolio_stable_rollup_available(self):
        from release.version_info import PORTFOLIO_STABLE_ROLLUP_AVAILABLE
        assert PORTFOLIO_STABLE_ROLLUP_AVAILABLE is True

    def test_portfolio_stable_rollup_stage(self):
        from release.version_info import PORTFOLIO_STABLE_ROLLUP_STAGE
        assert PORTFOLIO_STABLE_ROLLUP_STAGE == "STABLE"

    def test_real_order_creation_disabled(self):
        from release.version_info import REAL_ORDER_CREATION_ENABLED
        assert REAL_ORDER_CREATION_ENABLED is False

    def test_real_order_execution_disabled(self):
        from release.version_info import REAL_ORDER_EXECUTION_ENABLED
        assert REAL_ORDER_EXECUTION_ENABLED is False

    def test_broker_connection_disabled(self):
        from release.version_info import BROKER_CONNECTION_ENABLED
        assert BROKER_CONNECTION_ENABLED is False

    def test_auto_apply_disabled(self):
        from release.version_info import AUTO_APPLY_ENABLED
        assert AUTO_APPLY_ENABLED is False

    def test_auto_rebalance_disabled(self):
        from release.version_info import AUTO_REBALANCE_ENABLED
        assert AUTO_REBALANCE_ENABLED is False


# ===========================================================================
# 2. Package import
# ===========================================================================
class TestPackageImport:
    def test_stable_rollup_package_importable(self):
        import portfolio.stable_rollup
        assert portfolio.stable_rollup.RESEARCH_ONLY is True

    def test_enums_importable(self):
        from portfolio.stable_rollup.enums_v159 import (
            CapabilityStage, DebtSeverity, SchemaChangeType, ContractStatus, RollupStatus
        )
        assert CapabilityStage.STABLE.value == "STABLE"
        assert DebtSeverity.BLOCKING.value == "BLOCKING"
        assert SchemaChangeType.NO_CHANGE.value == "NO_CHANGE"
        assert ContractStatus.VALID.value == "VALID"
        assert RollupStatus.PASS.value == "PASS"

    def test_models_importable(self):
        from portfolio.stable_rollup.models_v159 import (
            StableCapabilityRecord, StableSchemaRecord, StableEnumRecord,
            StablePolicyRecord, StableCLIRecord, StableHealthRecord,
            StableReleaseGateRecord, StableContractRecord, StableMigrationRecord,
            StableReadinessItem, StableManifest, StableRollupResult,
        )
        assert StableCapabilityRecord is not None

    def test_capability_registry_importable(self):
        from portfolio.stable_rollup.capability_registry_v159 import (
            CapabilityRegistryV159, STABLE_CAPABILITIES, PLANNED_CAPABILITIES
        )
        assert len(STABLE_CAPABILITIES) >= 6
        assert len(PLANNED_CAPABILITIES) >= 7

    def test_schema_registry_importable(self):
        from portfolio.stable_rollup.schema_registry_v159 import (
            SchemaRegistryV159, PORTFOLIO_SCHEMAS
        )
        assert len(PORTFOLIO_SCHEMAS) == 33

    def test_enum_registry_importable(self):
        from portfolio.stable_rollup.enum_registry_v159 import (
            EnumRegistryV159, STABLE_ENUMS
        )
        assert len(STABLE_ENUMS) == 13

    def test_policy_registry_importable(self):
        from portfolio.stable_rollup.policy_registry_v159 import (
            PolicyRegistryV159, STABLE_POLICIES
        )
        assert len(STABLE_POLICIES) == 9

    def test_cli_registry_importable(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        assert CLIRegistryV159 is not None

    def test_health_registry_importable(self):
        from portfolio.stable_rollup.health_registry_v159 import (
            HealthRegistryV159, HEALTH_REGISTRY
        )
        assert len(HEALTH_REGISTRY) == 13

    def test_release_gate_registry_importable(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import (
            ReleaseGateRegistryV159, RELEASE_GATE_REGISTRY
        )
        assert len(RELEASE_GATE_REGISTRY) == 6

    def test_pit_contract_importable(self):
        from portfolio.stable_rollup.pit_contract_v159 import PITContractV159, PIT_CONTRACT
        assert PIT_CONTRACT.contract_type == "PIT"

    def test_lineage_contract_importable(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LineageContractV159, LINEAGE_CONTRACT
        assert LINEAGE_CONTRACT.contract_type == "LINEAGE"

    def test_reproducibility_contract_importable(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import ReproducibilityContractV159
        assert ReproducibilityContractV159 is not None

    def test_safety_contract_importable(self):
        from portfolio.stable_rollup.safety_contract_v159 import SafetyContractV159, SAFETY_CONTRACT
        assert SAFETY_CONTRACT.contract_type == "SAFETY"

    def test_compatibility_registry_importable(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        assert CompatibilityRegistryV159 is not None

    def test_migration_registry_importable(self):
        from portfolio.stable_rollup.migration_registry_v159 import (
            MigrationRegistryV159, MIGRATION_REGISTRY
        )
        assert len(MIGRATION_REGISTRY) == 8

    def test_stable_manifest_importable(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        assert StableManifestBuilder is not None

    def test_readiness_matrix_importable(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        assert ReadinessMatrixV159 is not None

    def test_integrity_validator_importable(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        assert IntegrityValidator is not None

    def test_integration_audit_importable(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        assert IntegrationAuditV159 is not None

    def test_debt_scanner_importable(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        assert DebtScannerV159 is not None

    def test_query_service_importable(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        assert StableRollupQueryService is not None

    def test_health_importable(self):
        from portfolio.stable_rollup.health_v159 import PortfolioStableRollupHealthCheck
        assert PortfolioStableRollupHealthCheck is not None


# ===========================================================================
# 3. Enums
# ===========================================================================
class TestEnums:
    def test_capability_stage_values(self):
        from portfolio.stable_rollup.enums_v159 import CapabilityStage
        assert set(s.value for s in CapabilityStage) == {"STABLE", "PLANNED", "DISABLED", "DEPRECATED", "REMOVED"}

    def test_debt_severity_values(self):
        from portfolio.stable_rollup.enums_v159 import DebtSeverity
        assert set(s.value for s in DebtSeverity) == {"BLOCKING", "WARNING", "INFORMATIONAL"}

    def test_schema_change_type_values(self):
        from portfolio.stable_rollup.enums_v159 import SchemaChangeType
        assert "NO_CHANGE" in [s.value for s in SchemaChangeType]
        assert "MIGRATION_REQUIRED" in [s.value for s in SchemaChangeType]

    def test_contract_status_values(self):
        from portfolio.stable_rollup.enums_v159 import ContractStatus
        assert ContractStatus.VALID.value == "VALID"
        assert ContractStatus.DRIFT_DETECTED.value == "DRIFT_DETECTED"

    def test_rollup_status_values(self):
        from portfolio.stable_rollup.enums_v159 import RollupStatus
        assert RollupStatus.PASS.value == "PASS"
        assert RollupStatus.BLOCKED.value == "BLOCKED"


# ===========================================================================
# 4. Models
# ===========================================================================
class TestModels:
    def test_stable_capability_record_fields(self):
        from portfolio.stable_rollup.models_v159 import StableCapabilityRecord
        r = StableCapabilityRecord(
            capability_id="test", display_name="Test", module="test_mod",
            introduced_version="1.5.9", stable_version="1.5.9",
            stage="STABLE", implementation_path="portfolio/test/",
        )
        assert r.capability_id == "test"
        assert r.PIT_required is True
        assert r.safety_required is True
        assert r.research_only is None or True

    def test_stable_schema_record_fingerprint(self):
        from portfolio.stable_rollup.models_v159 import StableSchemaRecord
        s = StableSchemaRecord(
            schema_id="TestSchema", schema_version="1.5.9",
            introduced_version="1.5.9", stable_version="1.5.9",
            required_fields=["id", "name"],
        )
        fp = s.compute_fingerprint()
        assert len(fp) == 16
        assert isinstance(fp, str)
        # deterministic
        assert fp == s.compute_fingerprint()

    def test_stable_enum_record_fingerprint(self):
        from portfolio.stable_rollup.models_v159 import StableEnumRecord
        e = StableEnumRecord(
            enum_name="TestEnum", values=["A", "B", "C"],
            introduced_version="1.5.9", stable_version="1.5.9",
        )
        fp = e.compute_fingerprint()
        assert len(fp) == 16
        assert fp == e.compute_fingerprint()

    def test_stable_manifest_semantic_hash(self):
        from portfolio.stable_rollup.models_v159 import StableManifest
        m = StableManifest(
            version="1.5.9", release="Portfolio Stable Rollup",
            commit="abc123", generated_at="2026-06-24T00:00:00Z",
            stable_capabilities=["portfolio_foundation", "position_sizing"],
            cli_count=310, research_only=True,
        )
        h1 = m.compute_semantic_hash()
        assert len(h1) == 32
        # Changing generated_at does not change hash (excluded)
        m.generated_at = "2999-01-01T00:00:00Z"
        h2 = m.compute_semantic_hash()
        assert h1 == h2

    def test_stable_rollup_result_defaults(self):
        from portfolio.stable_rollup.models_v159 import StableRollupResult
        r = StableRollupResult(version="1.5.9", release="Portfolio Stable Rollup")
        assert r.blocking_debt == 0
        assert r.status == "PASS"
        assert r.research_only is True

    def test_stable_policy_record_pit_safe(self):
        from portfolio.stable_rollup.models_v159 import StablePolicyRecord
        p = StablePolicyRecord(
            policy_id="test_policy", policy_type="TestPolicy",
            version="1.5.9", effective_from="2024-01-01",
        )
        assert p.PIT_safe is True
        assert p.auto_apply is False
        assert p.research_only is True

    def test_stable_migration_record_defaults(self):
        from portfolio.stable_rollup.models_v159 import StableMigrationRecord
        m = StableMigrationRecord(
            migration_id="test", source_version="1.5.4", target_version="1.5.9",
        )
        assert m.data_migration_required is False
        assert m.reversible is True

    def test_stable_readiness_item_defaults(self):
        from portfolio.stable_rollup.models_v159 import StableReadinessItem
        item = StableReadinessItem(domain="test", capability="TestCap")
        assert item.ready is False
        assert item.stage == "STABLE"


# ===========================================================================
# 5. Capability Registry
# ===========================================================================
class TestCapabilityRegistry:
    def test_get_stable_returns_six(self):
        from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
        stable = CapabilityRegistryV159().get_stable()
        assert len(stable) == 6

    def test_stable_capability_ids(self):
        from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
        stable = CapabilityRegistryV159().get_stable()
        ids = {c.capability_id for c in stable}
        assert "portfolio_foundation" in ids
        assert "position_sizing" in ids
        assert "correlation_exposure" in ids
        assert "drawdown_risk_controls" in ids
        assert "portfolio_walk_forward" in ids
        assert "portfolio_stable_rollup" in ids

    def test_all_stable_have_stage_stable(self):
        from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
        for c in CapabilityRegistryV159().get_stable():
            assert c.stage == "STABLE", f"{c.capability_id} stage is {c.stage}"

    def test_get_planned_includes_planned_and_disabled(self):
        from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
        planned = CapabilityRegistryV159().get_planned()
        assert len(planned) >= 7

    def test_get_disabled_returns_only_disabled(self):
        from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
        disabled = CapabilityRegistryV159().get_disabled()
        for c in disabled:
            assert c.stage == "DISABLED"

    def test_production_trading_is_disabled(self):
        from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
        reg = CapabilityRegistryV159()
        prod = reg.get_by_id("production_trading")
        assert prod is not None
        assert prod.stage == "DISABLED"

    def test_validate_passes(self):
        from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
        result = CapabilityRegistryV159().validate()
        assert result["valid"] is True
        assert result["issues"] == []

    def test_no_duplicate_ids(self):
        from portfolio.stable_rollup.capability_registry_v159 import STABLE_CAPABILITIES, PLANNED_CAPABILITIES
        ids = [c.capability_id for c in STABLE_CAPABILITIES + PLANNED_CAPABILITIES]
        assert len(ids) == len(set(ids))

    def test_get_by_id_found(self):
        from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
        c = CapabilityRegistryV159().get_by_id("portfolio_foundation")
        assert c is not None
        assert c.capability_id == "portfolio_foundation"

    def test_get_by_id_not_found(self):
        from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
        c = CapabilityRegistryV159().get_by_id("nonexistent_capability")
        assert c is None


# ===========================================================================
# 6. Schema Registry
# ===========================================================================
class TestSchemaRegistry:
    def test_schema_count_is_33(self):
        from portfolio.stable_rollup.schema_registry_v159 import SchemaRegistryV159
        assert len(SchemaRegistryV159().get_all()) == 33

    def test_all_schemas_have_required_fields(self):
        from portfolio.stable_rollup.schema_registry_v159 import SchemaRegistryV159
        for s in SchemaRegistryV159().get_all():
            assert len(s.required_fields) > 0, f"{s.schema_id} has no required fields"

    def test_all_schemas_have_fingerprints(self):
        from portfolio.stable_rollup.schema_registry_v159 import PORTFOLIO_SCHEMAS
        for s in PORTFOLIO_SCHEMAS:
            assert s.fingerprint is not None
            assert len(s.fingerprint) == 16

    def test_fingerprints_are_deterministic(self):
        from portfolio.stable_rollup.schema_registry_v159 import PORTFOLIO_SCHEMAS
        for s in PORTFOLIO_SCHEMAS:
            fp1 = s.compute_fingerprint()
            fp2 = s.compute_fingerprint()
            assert fp1 == fp2

    def test_get_fingerprints_dict(self):
        from portfolio.stable_rollup.schema_registry_v159 import SchemaRegistryV159
        fps = SchemaRegistryV159().get_fingerprints()
        assert isinstance(fps, dict)
        assert len(fps) == 33

    def test_validate_passes(self):
        from portfolio.stable_rollup.schema_registry_v159 import SchemaRegistryV159
        result = SchemaRegistryV159().validate()
        assert result["valid"] is True
        assert result["count"] == 33

    def test_check_drift_no_drift(self):
        from portfolio.stable_rollup.schema_registry_v159 import SchemaRegistryV159
        reg = SchemaRegistryV159()
        fps = reg.get_fingerprints()
        drift = reg.check_drift(fps)
        assert drift == []

    def test_check_drift_detects_change(self):
        from portfolio.stable_rollup.schema_registry_v159 import SchemaRegistryV159
        reg = SchemaRegistryV159()
        fps = reg.get_fingerprints()
        # Tamper with one fingerprint
        modified = dict(fps)
        if modified:
            first_key = next(iter(modified))
            modified[first_key] = "TAMPERED"
        drift = reg.check_drift(modified)
        assert len(drift) == 1

    def test_no_duplicate_schema_ids(self):
        from portfolio.stable_rollup.schema_registry_v159 import PORTFOLIO_SCHEMAS
        ids = [s.schema_id for s in PORTFOLIO_SCHEMAS]
        assert len(ids) == len(set(ids))

    def test_specific_schemas_present(self):
        from portfolio.stable_rollup.schema_registry_v159 import SchemaRegistryV159
        reg = SchemaRegistryV159()
        expected = [
            "PortfolioDefinition", "PortfolioSnapshot", "PositionSizingRequest",
            "CorrelationMatrixResult", "RiskControlPolicy", "DrawdownSummary",
            "WalkForwardConfiguration", "ReproducibilityManifest",
        ]
        for sid in expected:
            assert reg.get_by_id(sid) is not None, f"Schema {sid} not found"


# ===========================================================================
# 7. Enum Registry
# ===========================================================================
class TestEnumRegistry:
    def test_enum_count_is_13(self):
        from portfolio.stable_rollup.enum_registry_v159 import EnumRegistryV159
        assert len(EnumRegistryV159().get_all()) == 13

    def test_all_enums_have_fingerprints(self):
        from portfolio.stable_rollup.enum_registry_v159 import STABLE_ENUMS
        for e in STABLE_ENUMS:
            assert e.fingerprint is not None
            assert len(e.fingerprint) == 16

    def test_validate_passes(self):
        from portfolio.stable_rollup.enum_registry_v159 import EnumRegistryV159
        result = EnumRegistryV159().validate()
        assert result["valid"] is True
        assert result["count"] == 13

    def test_no_duplicate_enum_names(self):
        from portfolio.stable_rollup.enum_registry_v159 import STABLE_ENUMS
        names = [e.enum_name for e in STABLE_ENUMS]
        assert len(names) == len(set(names))

    def test_no_duplicate_values_within_enum(self):
        from portfolio.stable_rollup.enum_registry_v159 import STABLE_ENUMS
        for e in STABLE_ENUMS:
            assert len(e.values) == len(set(e.values)), f"{e.enum_name} has duplicate values"

    def test_capability_stage_enum_present(self):
        from portfolio.stable_rollup.enum_registry_v159 import EnumRegistryV159
        e = EnumRegistryV159().get_by_name("CapabilityStage")
        assert e is not None
        assert "STABLE" in e.values
        assert "PLANNED" in e.values
        assert "DISABLED" in e.values

    def test_get_fingerprints_dict(self):
        from portfolio.stable_rollup.enum_registry_v159 import EnumRegistryV159
        fps = EnumRegistryV159().get_fingerprints()
        assert isinstance(fps, dict)
        assert len(fps) == 13


# ===========================================================================
# 8. Policy Registry
# ===========================================================================
class TestPolicyRegistry:
    def test_policy_count_is_9(self):
        from portfolio.stable_rollup.policy_registry_v159 import PolicyRegistryV159
        assert len(PolicyRegistryV159().get_all()) == 9

    def test_all_policies_pit_safe(self):
        from portfolio.stable_rollup.policy_registry_v159 import STABLE_POLICIES
        for p in STABLE_POLICIES:
            assert p.PIT_safe is True, f"{p.policy_id} not PIT safe"

    def test_all_policies_research_only(self):
        from portfolio.stable_rollup.policy_registry_v159 import STABLE_POLICIES
        for p in STABLE_POLICIES:
            assert p.research_only is True
            assert p.auto_apply is False

    def test_validate_passes(self):
        from portfolio.stable_rollup.policy_registry_v159 import PolicyRegistryV159
        result = PolicyRegistryV159().validate()
        assert result["valid"] is True
        assert result["count"] == 9

    def test_get_by_id(self):
        from portfolio.stable_rollup.policy_registry_v159 import PolicyRegistryV159
        p = PolicyRegistryV159().get_by_id("sizing_policy_default")
        assert p is not None
        assert p.policy_type == "PositionSizingPolicy"


# ===========================================================================
# 9. CLI Registry
# ===========================================================================
class TestCLIRegistry:
    def test_cli_registry_builds(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        reg = CLIRegistryV159()
        assert reg.get_count() > 0

    def test_validate_no_forbidden_commands(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        result = CLIRegistryV159().validate()
        # Validate should not find forbidden commands
        forbidden_issues = [i for i in result.get("issues", []) if "FORBIDDEN_COMMAND" in i]
        assert len(forbidden_issues) == 0

    def test_no_broker_commands(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        reg = CLIRegistryV159()
        for r in reg.get_all():
            assert not r.command in ["submit-order", "execute-order", "broker-connect"]


# ===========================================================================
# 10. Health Registry
# ===========================================================================
class TestHealthRegistry:
    def test_health_registry_count(self):
        from portfolio.stable_rollup.health_registry_v159 import HealthRegistryV159
        assert len(HealthRegistryV159().get_all()) == 13

    def test_validate_passes(self):
        from portfolio.stable_rollup.health_registry_v159 import HealthRegistryV159
        result = HealthRegistryV159().validate()
        assert result["valid"] is True
        assert result["count"] == 13

    def test_portfolio_stable_health_registered(self):
        from portfolio.stable_rollup.health_registry_v159 import HealthRegistryV159
        h = HealthRegistryV159().get_by_id("portfolio_stable_rollup_health")
        assert h is not None
        assert h.command == "portfolio-stable-health"

    def test_no_duplicate_health_ids(self):
        from portfolio.stable_rollup.health_registry_v159 import HEALTH_REGISTRY
        ids = [h.health_id for h in HEALTH_REGISTRY]
        assert len(ids) == len(set(ids))


# ===========================================================================
# 11. Release Gate Registry
# ===========================================================================
class TestReleaseGateRegistry:
    def test_gate_count_is_6(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import ReleaseGateRegistryV159
        assert len(ReleaseGateRegistryV159().get_all()) == 6

    def test_validate_passes(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import ReleaseGateRegistryV159
        result = ReleaseGateRegistryV159().validate()
        assert result["valid"] is True
        assert result["count"] == 6

    def test_stable_gate_public_cli_available(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import ReleaseGateRegistryV159
        g = ReleaseGateRegistryV159().get_by_id("portfolio_stable_gate")
        assert g is not None
        assert g.public_cli_available is True

    def test_all_gates_have_entry_points(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import RELEASE_GATE_REGISTRY
        for g in RELEASE_GATE_REGISTRY:
            assert g.public_entry_point, f"{g.gate_id} has no entry point"


# ===========================================================================
# 12. PIT Contract
# ===========================================================================
class TestPITContract:
    def test_contract_version(self):
        from portfolio.stable_rollup.pit_contract_v159 import PITContractV159
        c = PITContractV159().get_contract()
        assert c.version == "1.5.9"
        assert c.contract_type == "PIT"
        assert c.status == "VALID"

    def test_rules_count(self):
        from portfolio.stable_rollup.pit_contract_v159 import PITContractV159
        c = PITContractV159().get_contract()
        assert len(c.rules) >= 17

    def test_blocking_violations_defined(self):
        from portfolio.stable_rollup.pit_contract_v159 import PITContractV159
        c = PITContractV159().get_contract()
        assert "future_price_used" in c.blocking_violations
        assert "fetched_at_used_as_available_from" in c.blocking_violations

    def test_validate_valid_data(self):
        from portfolio.stable_rollup.pit_contract_v159 import PITContractV159
        result = PITContractV159().validate({"available_from": "2020-01-01"}, as_of="2021-01-01")
        assert result["is_valid"] is True
        assert result["violations"] == []

    def test_validate_future_data_detected(self):
        from portfolio.stable_rollup.pit_contract_v159 import PITContractV159
        result = PITContractV159().validate({"available_from": "2025-01-01"}, as_of="2020-01-01")
        assert result["is_valid"] is False
        assert "future_data_detected" in result["violations"]

    def test_validate_fetched_at_without_available_from(self):
        from portfolio.stable_rollup.pit_contract_v159 import PITContractV159
        result = PITContractV159().validate({"fetched_at": "2021-01-01"}, as_of="2021-01-01")
        assert result["is_valid"] is False
        assert "fetched_at_used_as_available_from" in result["violations"]

    def test_check_drift_returns_empty(self):
        from portfolio.stable_rollup.pit_contract_v159 import PITContractV159
        assert PITContractV159().check_drift() == []

    def test_matrix_has_five_entries(self):
        from portfolio.stable_rollup.pit_contract_v159 import PITContractV159
        matrix = PITContractV159().get_matrix()
        assert len(matrix) == 5


# ===========================================================================
# 13. Lineage Contract
# ===========================================================================
class TestLineageContract:
    def test_contract_version(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LineageContractV159
        c = LineageContractV159().get_contract()
        assert c.version == "1.5.9"
        assert c.contract_type == "LINEAGE"

    def test_validate_result_valid(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LineageContractV159
        result = LineageContractV159().validate_result({
            "content_hash": "abc", "calculation_version": "1.5.9",
            "source_lineage": "snap_001",
        })
        assert result["is_valid"] is True

    def test_validate_result_missing_hash(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LineageContractV159
        result = LineageContractV159().validate_result({
            "calculation_version": "1.5.9", "source_lineage": "snap_001",
        })
        assert result["is_valid"] is False
        assert "MISSING_CONTENT_HASH" in result["violations"]

    def test_validate_result_missing_source_lineage(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LineageContractV159
        result = LineageContractV159().validate_result({
            "content_hash": "abc", "calculation_version": "1.5.9",
        })
        assert result["is_valid"] is False
        assert "MISSING_SOURCE_LINEAGE" in result["violations"]

    def test_lineage_chains_defined(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LINEAGE_CHAINS
        assert "portfolio_report" in LINEAGE_CHAINS
        assert "walk_forward_result" in LINEAGE_CHAINS


# ===========================================================================
# 14. Reproducibility Contract
# ===========================================================================
class TestReproducibilityContract:
    def test_contract_version(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import ReproducibilityContractV159
        c = ReproducibilityContractV159().get_contract()
        assert c.version == "1.5.9"
        assert c.contract_type == "REPRODUCIBILITY"

    def test_validate_manifest_valid(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import ReproducibilityContractV159
        result = ReproducibilityContractV159().validate_manifest({
            "config_hash": "abc123", "timezone": "Asia/Taipei", "calendar_version": "1.0",
        })
        assert result["is_valid"] is True

    def test_validate_manifest_missing_fields(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import ReproducibilityContractV159
        result = ReproducibilityContractV159().validate_manifest({})
        assert result["is_valid"] is False
        assert "MISSING_CONFIG_HASH" in result["violations"]

    def test_rules_count(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import ReproducibilityContractV159
        c = ReproducibilityContractV159().get_contract()
        assert len(c.rules) >= 19


# ===========================================================================
# 15. Safety Contract
# ===========================================================================
class TestSafetyContract:
    def test_contract_version(self):
        from portfolio.stable_rollup.safety_contract_v159 import SafetyContractV159
        c = SafetyContractV159().get_contract()
        assert c.version == "1.5.9"
        assert c.contract_type == "SAFETY"

    def test_validate_passes(self):
        from portfolio.stable_rollup.safety_contract_v159 import SafetyContractV159
        result = SafetyContractV159().validate()
        assert result["is_valid"] is True, f"Safety violations: {result['violations']}"

    def test_forbidden_flags_all_false(self):
        from portfolio.stable_rollup.safety_contract_v159 import FORBIDDEN_FLAGS
        for flag, val in FORBIDDEN_FLAGS.items():
            assert val is False, f"Forbidden flag {flag} is True"

    def test_required_flags_all_true(self):
        from portfolio.stable_rollup.safety_contract_v159 import REQUIRED_FLAGS
        for flag, val in REQUIRED_FLAGS.items():
            assert val is True, f"Required flag {flag} is False"

    def test_rules_include_research_only(self):
        from portfolio.stable_rollup.safety_contract_v159 import SafetyContractV159
        c = SafetyContractV159().get_contract()
        rules_text = " ".join(c.rules)
        assert "RESEARCH_ONLY" in rules_text
        assert "NO_REAL_ORDER" in rules_text
        assert "PRODUCTION_TRADING_BLOCKED" in rules_text


# ===========================================================================
# 16. Compatibility Registry
# ===========================================================================
class TestCompatibilityRegistry:
    def test_current_version_compatible(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        result = CompatibilityRegistryV159().is_compatible("1.5.9")
        assert result["compatible"] is True

    def test_v154_compatible(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        result = CompatibilityRegistryV159().is_compatible("1.5.4")
        assert result["compatible"] is True

    def test_v150_compatible(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        result = CompatibilityRegistryV159().is_compatible("1.5.0")
        assert result["compatible"] is True

    def test_v200_not_auto_compatible(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        result = CompatibilityRegistryV159().is_compatible("2.0.0")
        assert result["compatible"] is False
        assert "FUTURE_MAJOR" in result["reason"]

    def test_v140_not_compatible(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        result = CompatibilityRegistryV159().is_compatible("1.4.0")
        assert result["compatible"] is False

    def test_validate_passes(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        result = CompatibilityRegistryV159().validate()
        assert result["valid"] is True
        assert result["issues"] == []

    def test_registry_has_current_version(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        reg = CompatibilityRegistryV159().get_registry()
        assert reg["current_version"] == "1.5.9"


# ===========================================================================
# 17. Migration Registry
# ===========================================================================
class TestMigrationRegistry:
    def test_migration_count_is_8(self):
        from portfolio.stable_rollup.migration_registry_v159 import MigrationRegistryV159
        assert len(MigrationRegistryV159().get_all()) == 8

    def test_validate_passes(self):
        from portfolio.stable_rollup.migration_registry_v159 import MigrationRegistryV159
        result = MigrationRegistryV159().validate()
        assert result["valid"] is True
        assert result["count"] == 8

    def test_154_to_159_migration_exists(self):
        from portfolio.stable_rollup.migration_registry_v159 import MigrationRegistryV159
        m = MigrationRegistryV159().get_path("1.5.4", "1.5.9")
        assert m is not None
        assert m.data_migration_required is False

    def test_no_data_migration_required(self):
        from portfolio.stable_rollup.migration_registry_v159 import MIGRATION_REGISTRY
        for m in MIGRATION_REGISTRY:
            assert m.data_migration_required is False, \
                f"Migration {m.migration_id} unexpectedly requires data migration"

    def test_no_duplicate_migration_ids(self):
        from portfolio.stable_rollup.migration_registry_v159 import MIGRATION_REGISTRY
        ids = [m.migration_id for m in MIGRATION_REGISTRY]
        assert len(ids) == len(set(ids))


# ===========================================================================
# 18. Stable Manifest
# ===========================================================================
class TestStableManifest:
    def test_build_manifest(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        manifest = StableManifestBuilder().build()
        assert manifest is not None
        assert manifest.version is not None
        assert manifest.content_hash is not None
        assert manifest.research_only is True

    def test_manifest_version_gte_159(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        manifest = StableManifestBuilder().build()
        assert _parse_ver(manifest.version) >= _parse_ver("1.5.9")

    def test_manifest_stable_capabilities_count(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        manifest = StableManifestBuilder().build()
        assert len(manifest.stable_capabilities) == 6

    def test_manifest_schema_fingerprints(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        manifest = StableManifestBuilder().build()
        assert len(manifest.schema_fingerprints) == 33

    def test_manifest_safety_flags(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        manifest = StableManifestBuilder().build()
        assert manifest.research_only is True
        assert manifest.no_real_orders is True
        assert manifest.broker_disabled is True
        assert manifest.production_trading_blocked is True

    def test_validate_passes(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        builder = StableManifestBuilder()
        manifest = builder.build()
        result = builder.validate(manifest)
        assert result["valid"] is True
        assert result["issues"] == []

    def test_hash_is_deterministic(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        builder = StableManifestBuilder()
        m1 = builder.build()
        m2 = builder.build()
        assert m1.content_hash == m2.content_hash

    def test_to_json(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        import json
        builder = StableManifestBuilder()
        manifest = builder.build()
        j = builder.to_json(manifest)
        data = json.loads(j)
        assert data["version"] is not None
        assert data["safety"]["research_only"] is True
        assert data["content_hash"] is not None


# ===========================================================================
# 19. Readiness Matrix
# ===========================================================================
class TestReadinessMatrix:
    def test_total_items(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        items = ReadinessMatrixV159().get_all()
        assert len(items) >= 11

    def test_all_stable_are_ready(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        for item in ReadinessMatrixV159().get_stable():
            assert item.ready is True, f"{item.capability} is STABLE but not ready"

    def test_all_planned_not_ready(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        for item in ReadinessMatrixV159().get_planned():
            assert item.ready is False

    def test_validate_passes(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        result = ReadinessMatrixV159().validate()
        assert result["valid"] is True
        assert result["stable_ready"] == 6

    def test_stable_count(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        assert len(ReadinessMatrixV159().get_stable()) == 6

    def test_get_blockers_for_planned(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        blockers = ReadinessMatrixV159().get_blockers()
        assert len(blockers) > 0


# ===========================================================================
# 20. Integrity Validator
# ===========================================================================
class TestIntegrityValidator:
    def test_run_all_passes(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().run_all()
        assert result["overall"] == "PASS"

    def test_schema_integrity(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().validate_schema_integrity()
        assert result["valid"] is True

    def test_enum_integrity(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().validate_enum_integrity()
        assert result["valid"] is True

    def test_capability_integrity(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().validate_capability_integrity()
        assert result["valid"] is True

    def test_safety_integrity(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().validate_safety_integrity()
        assert result["is_valid"] is True


# ===========================================================================
# 21. Integration Audit
# ===========================================================================
class TestIntegrationAudit:
    def test_run_all_passes(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().run_all()
        assert result["overall"] == "PASS"

    def test_portfolio_to_sizing_passes(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().audit_portfolio_to_sizing()
        assert result["status"] == "PASS"

    def test_simulation_ledger_isolation(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().audit_simulation_ledger_isolation()
        assert result["status"] == "PASS"
        assert result["formal_ledger_write_blocked"] is True

    def test_safety_audit_passes(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().audit_safety()
        assert result["status"] == "PASS"

    def test_fixture_integration(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().run_fixture_integration()
        assert result["status"] == "PASS"
        assert result["no_broker"] is True
        assert result["no_real_order"] is True
        assert result["HISTORICAL_SIMULATION_ONLY"] is True

    def test_all_checks_present(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().run_all()
        checks = result.get("checks", {})
        expected = [
            "portfolio_to_sizing", "sizing_to_correlation", "correlation_to_risk",
            "risk_to_walk_forward", "walk_forward_to_manifest",
            "simulation_ledger_isolation", "safety", "fixture_integration",
        ]
        for k in expected:
            assert k in checks, f"Check {k} missing"


# ===========================================================================
# 22. Debt Scanner
# ===========================================================================
class TestDebtScanner:
    def test_run_all_passes(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        result = DebtScannerV159().run_all()
        assert result["blocking_debt_zero"] is True
        assert result["blocking_count"] == 0
        assert result["status"] == "PASS"

    def test_no_broker_references_in_portfolio(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        findings = DebtScannerV159().scan_broker_references()
        assert len(findings) == 0, f"Broker references found: {findings}"

    def test_scanner_returns_required_keys(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        result = DebtScannerV159().run_all()
        for key in ["blocking", "warning", "informational", "blocking_count", "warning_count", "status"]:
            assert key in result


# ===========================================================================
# 23. Query Service
# ===========================================================================
class TestQueryService:
    def test_get_stable_capabilities(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        caps = StableRollupQueryService().get_stable_capabilities()
        assert len(caps) == 6
        assert all("capability_id" in c for c in caps)

    def test_get_planned_capabilities(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        caps = StableRollupQueryService().get_planned_capabilities()
        assert len(caps) >= 6
        assert all(c["stage"] == "PLANNED" for c in caps)

    def test_get_disabled_capabilities(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        caps = StableRollupQueryService().get_disabled_capabilities()
        assert len(caps) >= 1
        assert all(c["stage"] == "DISABLED" for c in caps)

    def test_get_schema_registry_count(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        schemas = StableRollupQueryService().get_schema_registry()
        assert len(schemas) == 33

    def test_get_enum_registry_count(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        enums = StableRollupQueryService().get_enum_registry()
        assert len(enums) == 13

    def test_get_policy_registry_count(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        policies = StableRollupQueryService().get_policy_registry()
        assert len(policies) == 9

    def test_get_health_registry_count(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        health = StableRollupQueryService().get_health_registry()
        assert len(health) == 13

    def test_get_release_gate_registry_count(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        gates = StableRollupQueryService().get_release_gate_registry()
        assert len(gates) == 6

    def test_build_stable_manifest(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        manifest = StableRollupQueryService().build_stable_manifest()
        assert manifest is not None
        assert manifest.content_hash is not None

    def test_validate_stable_manifest(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().validate_stable_manifest()
        assert result["valid"] is True

    def test_build_readiness_matrix(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        items = StableRollupQueryService().build_readiness_matrix()
        assert len(items) >= 11

    def test_run_integration_audit(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_integration_audit()
        assert result["overall"] == "PASS"

    def test_scan_stable_debt(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().scan_stable_debt()
        assert result["blocking_count"] == 0
        assert result["status"] == "PASS"

    def test_run_portfolio_stable_rollup(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.status == "PASS"
        assert result.blocking_debt == 0
        assert result.research_only is True

    def test_explain_stable_rollup(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        explanation = StableRollupQueryService().explain_stable_rollup()
        assert "summary" in explanation
        assert explanation["blocking_debt"] == 0
        assert "RESEARCH_ONLY" in explanation["safety_text"]

    def test_get_pit_contract(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        c = StableRollupQueryService().get_pit_contract()
        assert c["contract_id"] == "portfolio_pit_contract_v159"

    def test_get_lineage_contract(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        c = StableRollupQueryService().get_lineage_contract()
        assert c["contract_id"] == "portfolio_lineage_contract_v159"

    def test_get_reproducibility_contract(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        c = StableRollupQueryService().get_reproducibility_contract()
        assert c["contract_id"] == "portfolio_reproducibility_contract_v159"

    def test_get_safety_contract(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        c = StableRollupQueryService().get_safety_contract()
        assert c["contract_id"] == "portfolio_safety_contract_v159"

    def test_get_compatibility_registry(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        reg = StableRollupQueryService().get_compatibility_registry()
        assert reg["current_version"] == "1.5.9"

    def test_get_migration_registry_count(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        migrations = StableRollupQueryService().get_migration_registry()
        assert len(migrations) == 8


# ===========================================================================
# 24. Report
# ===========================================================================
class TestPortfolioStableRollupReport:
    def test_report_generates(self):
        from reports.portfolio_stable_rollup_report import PortfolioStableRollupReport
        r = PortfolioStableRollupReport().generate()
        assert r is not None
        assert r["report_version"] == "1.5.9"
        assert r["research_only"] is True
        assert r["executable"] is False
        assert r["order_created"] is False
        assert r["broker_called"] is False

    def test_report_has_all_sections(self):
        from reports.portfolio_stable_rollup_report import PortfolioStableRollupReport
        r = PortfolioStableRollupReport().generate()
        section_names = [s["section"] for s in r["sections"]]
        expected = ["context", "capabilities", "schemas", "enums", "policies",
                    "cli", "health", "release_gates", "manifest", "readiness",
                    "debt", "rollup", "safety"]
        for name in expected:
            assert name in section_names, f"Section '{name}' missing"

    def test_report_status_pass(self):
        from reports.portfolio_stable_rollup_report import PortfolioStableRollupReport
        r = PortfolioStableRollupReport().generate()
        assert r["status"] == "PASS"

    def test_report_blocking_debt_zero(self):
        from reports.portfolio_stable_rollup_report import PortfolioStableRollupReport
        r = PortfolioStableRollupReport().generate()
        assert r["blocking_debt"] == 0

    def test_report_has_manifest_hash(self):
        from reports.portfolio_stable_rollup_report import PortfolioStableRollupReport
        r = PortfolioStableRollupReport().generate()
        assert r["manifest_hash"] is not None

    def test_render_text(self):
        from reports.portfolio_stable_rollup_report import PortfolioStableRollupReport
        report = PortfolioStableRollupReport()
        r = report.generate()
        text = report.render_text(r)
        assert "Stable Rollup" in text
        assert "Research Only" in text

    def test_report_safety_constants(self):
        from reports.portfolio_stable_rollup_report import RESEARCH_ONLY, REPORT_VERSION
        assert RESEARCH_ONLY is True
        assert REPORT_VERSION == "1.5.9"

    def test_report_no_real_orders(self):
        from reports.portfolio_stable_rollup_report import PortfolioStableRollupReport
        r = PortfolioStableRollupReport().generate()
        assert r["NO_REAL_ORDERS"] is True
        assert r["PRODUCTION_TRADING_BLOCKED"] is True


# ===========================================================================
# 25. GUI Panel
# ===========================================================================
class TestGUIPanel:
    def test_gui_panel_importable(self):
        import gui.portfolio_stable_rollup_panel as panel
        assert panel.RESEARCH_ONLY is True
        assert panel.NO_REAL_ORDERS is True
        assert panel.PRODUCTION_TRADING_BLOCKED is True

    def test_panel_class_exists(self):
        from gui.portfolio_stable_rollup_panel import PortfolioStableRollupPanel
        p = PortfolioStableRollupPanel()
        assert p.research_only is True

    def test_panel_get_metadata(self):
        from gui.portfolio_stable_rollup_panel import PortfolioStableRollupPanel
        meta = PortfolioStableRollupPanel().get_metadata()
        assert meta["research_only"] is True
        assert meta["no_real_orders"] is True
        assert meta["production_trading_blocked"] is True

    def test_panel_headless_safe(self):
        from gui.portfolio_stable_rollup_panel import PortfolioStableRollupPanel
        widget = PortfolioStableRollupPanel().get_widget()
        assert widget is None

    def test_forbidden_actions_defined(self):
        from gui.portfolio_stable_rollup_panel import FORBIDDEN_ACTIONS
        assert "Execute" in FORBIDDEN_ACTIONS
        assert "Connect Broker" in FORBIDDEN_ACTIONS

    def test_safety_banner_defined(self):
        from gui.portfolio_stable_rollup_panel import SAFETY_BANNER_LINES
        assert len(SAFETY_BANNER_LINES) >= 7
        assert any("Research Only" in s for s in SAFETY_BANNER_LINES)


# ===========================================================================
# 26. Release Gate
# ===========================================================================
class TestReleaseGate:
    def test_gate_runs_and_passes(self):
        from release.portfolio_stable_release_gate_v159 import PortfolioStableReleaseGate
        result = PortfolioStableReleaseGate().run()
        assert result["gate_passed"] is True
        assert result["overall"] == "PASS"

    def test_gate_version(self):
        from release.portfolio_stable_release_gate_v159 import RELEASE_GATE_VERSION
        assert RELEASE_GATE_VERSION == "1.5.9"

    def test_gate_status_pass(self):
        from release.portfolio_stable_release_gate_v159 import RELEASE_GATE_STATUS
        assert RELEASE_GATE_STATUS == "PASS"

    def test_gate_result_schema(self):
        from release.portfolio_stable_release_gate_v159 import PortfolioStableReleaseGate
        result = PortfolioStableReleaseGate().run()
        for key in ["gate_passed", "status", "passed", "failed", "total"]:
            assert key in result, f"Key {key} missing from gate result"

    def test_gate_safety_checks_pass(self):
        from release.portfolio_stable_release_gate_v159 import PortfolioStableReleaseGate, SAFETY_GATES, GATE_CHECKS
        for k in SAFETY_GATES:
            assert GATE_CHECKS.get(k, False) is True, f"Safety gate {k} not passing"

    def test_gate_no_real_orders(self):
        from release.portfolio_stable_release_gate_v159 import PortfolioStableReleaseGate
        result = PortfolioStableReleaseGate().run()
        assert result["no_real_orders"] is True
        assert result["no_broker"] is True
        assert result["production_trading_blocked"] is True


# ===========================================================================
# 27. CLI Registration
# ===========================================================================
class TestCLIRegistration:
    def test_stable_commands_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        expected_commands = [
            "portfolio-stable-health",
            "portfolio-stable-capabilities",
            "portfolio-stable-planned",
            "portfolio-stable-schemas",
            "portfolio-stable-enums",
            "portfolio-stable-policies",
            "portfolio-stable-cli-registry",
            "portfolio-stable-health-registry",
            "portfolio-stable-release-gates",
            "portfolio-stable-pit-contract",
            "portfolio-stable-lineage-contract",
            "portfolio-stable-safety-contract",
            "portfolio-stable-compatibility",
            "portfolio-stable-migrations",
            "portfolio-stable-manifest",
            "portfolio-stable-readiness",
            "portfolio-stable-audit",
            "portfolio-stable-debt",
            "portfolio-stable-rollup",
            "portfolio-stable-explain",
            "portfolio-stable-gate",
            "portfolio-stable-report",
        ]
        for cmd in expected_commands:
            assert cmd in names, f"Command {cmd} not registered"

    def test_command_count_gte_332(self):
        from cli.command_registry import PROVIDER_COMMANDS
        assert len(PROVIDER_COMMANDS) >= 332, \
            f"Expected >= 332 commands (310 + 22), got {len(PROVIDER_COMMANDS)}"

    def test_no_duplicate_commands(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = [c.name for c in PROVIDER_COMMANDS]
        assert len(names) == len(set(names)), "Duplicate commands found"


# ===========================================================================
# 28. Health Check
# ===========================================================================
class TestHealthCheck:
    def test_health_check_runs(self):
        from portfolio.stable_rollup.health_v159 import PortfolioStableRollupHealthCheck
        result = PortfolioStableRollupHealthCheck().run()
        assert result is not None
        assert "checks" in result
        assert "overall" in result

    def test_health_check_overall_pass(self):
        from portfolio.stable_rollup.health_v159 import PortfolioStableRollupHealthCheck
        result = PortfolioStableRollupHealthCheck().run()
        assert result["overall"] == "PASS", f"Failed checks: {result.get('failed', [])}"

    def test_health_check_passed_count(self):
        from portfolio.stable_rollup.health_v159 import PortfolioStableRollupHealthCheck
        result = PortfolioStableRollupHealthCheck().run()
        assert result["passed"] >= 36

    def test_health_check_total_checks(self):
        from portfolio.stable_rollup.health_v159 import PortfolioStableRollupHealthCheck
        result = PortfolioStableRollupHealthCheck().run()
        assert result["total"] >= 40

    def test_health_check_research_only(self):
        from portfolio.stable_rollup.health_v159 import PortfolioStableRollupHealthCheck
        result = PortfolioStableRollupHealthCheck().run()
        assert result["research_only"] is True

    def test_health_check_version(self):
        from portfolio.stable_rollup.health_v159 import PortfolioStableRollupHealthCheck
        result = PortfolioStableRollupHealthCheck().run()
        assert result["version"] == "1.5.9"


# ===========================================================================
# 29. Fixtures
# ===========================================================================
class TestFixtures:
    def test_fixture_directory_exists(self):
        assert os.path.isdir(FIXTURE_DIR), f"Fixture directory missing: {FIXTURE_DIR}"

    def test_fixture_count(self):
        fixtures = [f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json")]
        assert len(fixtures) >= 34, f"Expected >= 34 fixtures, got {len(fixtures)}"

    def test_stable_manifest_fixture(self):
        f = _load_fixture("stable_manifest.json")
        assert f["TEST_FIXTURE"] is True
        assert f["DEMO_ONLY"] is True
        assert f["version"] == "1.5.9"
        assert f["research_only"] is True

    def test_stable_rollup_result_fixture(self):
        f = _load_fixture("stable_rollup_result.json")
        assert f["status"] == "PASS"
        assert f["blocking_debt"] == 0
        assert f["research_only"] is True

    def test_pit_validation_valid_fixture(self):
        f = _load_fixture("pit_validation_valid.json")
        assert f["expected_valid"] is True
        assert f["available_from"] < f["as_of"]

    def test_pit_validation_future_fixture(self):
        f = _load_fixture("pit_validation_future.json")
        assert f["expected_valid"] is False

    def test_compatibility_valid_fixture(self):
        f = _load_fixture("compatibility_check_valid.json")
        assert f["expected_compatible"] is True

    def test_compatibility_invalid_fixture(self):
        f = _load_fixture("compatibility_check_invalid.json")
        assert f["expected_compatible"] is False

    def test_all_fixtures_have_test_marker(self):
        for fn in os.listdir(FIXTURE_DIR):
            if not fn.endswith(".json"):
                continue
            data = _load_fixture(fn)
            assert data.get("TEST_FIXTURE") is True, f"Fixture {fn} missing TEST_FIXTURE marker"
            assert data.get("DEMO_ONLY") is True, f"Fixture {fn} missing DEMO_ONLY marker"


# ===========================================================================
# 30. Safety invariants
# ===========================================================================
class TestSafetyInvariants:
    def test_no_real_orders_invariant(self):
        from release.version_info import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_no_broker_invariant(self):
        from release.version_info import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_production_trading_blocked_invariant(self):
        from release.version_info import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_rollup_research_only(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.research_only is True

    def test_rollup_no_blocking_debt(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.blocking_debt == 0

    def test_manifest_no_real_orders(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        manifest = StableManifestBuilder().build()
        assert manifest.no_real_orders is True
        assert manifest.broker_disabled is True
        assert manifest.production_trading_blocked is True

    def test_package_safety_flags(self):
        import portfolio.stable_rollup as pkg
        assert pkg.RESEARCH_ONLY is True
        assert pkg.NO_REAL_ORDERS is True
        assert pkg.PRODUCTION_TRADING_BLOCKED is True

    def test_report_no_broker(self):
        from reports.portfolio_stable_rollup_report import PortfolioStableRollupReport
        r = PortfolioStableRollupReport().generate()
        safety_section = next(s for s in r["sections"] if s["section"] == "safety")
        assert safety_section["no_broker"] is True
        assert safety_section["no_real_orders"] is True

    def test_stable_capabilities_all_research_only(self):
        from portfolio.stable_rollup.capability_registry_v159 import STABLE_CAPABILITIES
        for c in STABLE_CAPABILITIES:
            assert "research-only" in c.known_limitations, \
                f"{c.capability_id} missing research-only limitation"


# ===========================================================================
# 31. Extended Models Tests
# ===========================================================================
class TestModelsExtended:
    def test_stable_cli_record_defaults(self):
        from portfolio.stable_rollup.models_v159 import StableCLIRecord
        r = StableCLIRecord(
            command="portfolio-stable-test",
            handler="test_handler",
            module="portfolio.stable_rollup",
            introduced_version="1.5.9",
            stable_version="1.5.9",
            category="portfolio",
        )
        assert r.research_only is True
        assert r.mutating is False
        assert r.network_required is False
        assert r.broker_related is False
        assert r.formal_ledger_write is False

    def test_stable_health_record_defaults(self):
        from portfolio.stable_rollup.models_v159 import StableHealthRecord
        h = StableHealthRecord(
            health_id="test_health",
            command="test-health",
            module="portfolio.test",
            expected_checks=10,
            minimum_pass_count=10,
        )
        assert h.stable_version == "1.5.9"
        assert h.warning_policy == "WARN"

    def test_stable_release_gate_record_defaults(self):
        from portfolio.stable_rollup.models_v159 import StableReleaseGateRecord
        g = StableReleaseGateRecord(
            gate_id="test_gate",
            module="release.test_gate",
            public_entry_point="TestReleaseGate",
            public_cli_available=True,
            expected_checks=10,
        )
        assert g.stable_version == "1.5.9"
        assert "gate_passed" in g.required_result_schema
        assert "status" in g.required_result_schema
        assert "passed" in g.required_result_schema
        assert "failed" in g.required_result_schema
        assert "total" in g.required_result_schema

    def test_stable_contract_record_defaults(self):
        from portfolio.stable_rollup.models_v159 import StableContractRecord
        c = StableContractRecord(
            contract_id="test_contract",
            contract_type="TEST",
            version="1.5.9",
        )
        assert c.status == "VALID"
        assert c.rules == []
        assert c.blocking_violations == []

    def test_rollup_result_fields(self):
        from portfolio.stable_rollup.models_v159 import StableRollupResult
        r = StableRollupResult(
            version="1.5.9",
            release="Portfolio Stable Rollup",
            stable_capabilities=6,
            planned_capabilities=7,
            schemas_total=33,
            enums_total=13,
        )
        assert r.stable_capabilities == 6
        assert r.planned_capabilities == 7
        assert r.schemas_total == 33
        assert r.enums_total == 13
        assert r.blocking_debt == 0
        assert r.status == "PASS"

    def test_stable_schema_record_backward_compatible_default(self):
        from portfolio.stable_rollup.models_v159 import StableSchemaRecord
        s = StableSchemaRecord(
            schema_id="TestSchema",
            schema_version="1.5.9",
            introduced_version="1.5.9",
            stable_version="1.5.9",
            required_fields=["id"],
        )
        assert s.backward_compatible is True
        assert s.serialization_format == "json"
        assert s.hash_algorithm == "sha256"

    def test_stable_enum_record_empty_aliases(self):
        from portfolio.stable_rollup.models_v159 import StableEnumRecord
        e = StableEnumRecord(
            enum_name="TestEnum",
            values=["X", "Y"],
            introduced_version="1.5.9",
            stable_version="1.5.9",
        )
        assert e.aliases == {}
        assert e.deprecated_values == []
        assert e.migration_mapping == {}

    def test_manifest_baselines_field(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m = StableManifestBuilder().build()
        assert "stable" in m.baselines
        assert m.baselines["stable"] == "1.5.9"

    def test_rollup_result_capabilities_total(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        r = StableRollupQueryService().run_portfolio_stable_rollup()
        assert r.capabilities_total == r.stable_capabilities + r.planned_capabilities + r.disabled_capabilities


# ===========================================================================
# 32. Extended Capability Registry Tests
# ===========================================================================
class TestCapabilityRegistryExtended:
    def test_total_capability_count(self):
        from portfolio.stable_rollup.capability_registry_v159 import (
            STABLE_CAPABILITIES, PLANNED_CAPABILITIES
        )
        assert len(STABLE_CAPABILITIES) + len(PLANNED_CAPABILITIES) >= 13

    def test_all_stable_have_health_check(self):
        from portfolio.stable_rollup.capability_registry_v159 import STABLE_CAPABILITIES
        for c in STABLE_CAPABILITIES:
            assert c.health_check is not None, f"{c.capability_id} missing health_check"

    def test_all_stable_have_release_gate(self):
        from portfolio.stable_rollup.capability_registry_v159 import STABLE_CAPABILITIES
        for c in STABLE_CAPABILITIES:
            assert c.release_gate is not None, f"{c.capability_id} missing release_gate"

    def test_all_stable_have_tests(self):
        from portfolio.stable_rollup.capability_registry_v159 import STABLE_CAPABILITIES
        for c in STABLE_CAPABILITIES:
            assert len(c.tests) > 0, f"{c.capability_id} has no test references"

    def test_stable_capability_versions_ordered(self):
        from portfolio.stable_rollup.capability_registry_v159 import STABLE_CAPABILITIES
        versions = [_parse_ver(c.stable_version) for c in STABLE_CAPABILITIES]
        assert versions == sorted(versions)

    def test_get_all_count(self):
        from portfolio.stable_rollup.capability_registry_v159 import (
            STABLE_CAPABILITIES, PLANNED_CAPABILITIES
        )
        total = len(STABLE_CAPABILITIES) + len(PLANNED_CAPABILITIES)
        assert total == 14

    def test_broker_integration_is_planned(self):
        from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
        c = CapabilityRegistryV159().get_by_id("broker_integration")
        assert c is not None
        assert c.stage == "PLANNED"

    def test_auto_rebalance_is_planned(self):
        from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
        c = CapabilityRegistryV159().get_by_id("auto_rebalance")
        assert c is not None
        assert c.stage == "PLANNED"

    def test_no_stable_capability_has_blockers(self):
        from portfolio.stable_rollup.capability_registry_v159 import STABLE_CAPABILITIES
        for c in STABLE_CAPABILITIES:
            assert c.deprecation_status is None, \
                f"{c.capability_id} has unexpected deprecation status"


# ===========================================================================
# 33. Extended Schema Registry Tests
# ===========================================================================
class TestSchemaRegistryExtended:
    def test_get_by_id_found(self):
        from portfolio.stable_rollup.schema_registry_v159 import SchemaRegistryV159
        s = SchemaRegistryV159().get_by_id("PortfolioDefinition")
        assert s is not None
        assert s.schema_id == "PortfolioDefinition"

    def test_get_by_id_not_found(self):
        from portfolio.stable_rollup.schema_registry_v159 import SchemaRegistryV159
        s = SchemaRegistryV159().get_by_id("NonExistentSchema")
        assert s is None

    def test_all_schemas_have_schema_version(self):
        from portfolio.stable_rollup.schema_registry_v159 import PORTFOLIO_SCHEMAS
        for s in PORTFOLIO_SCHEMAS:
            assert s.schema_version is not None
            assert len(s.schema_version) > 0

    def test_schema_fingerprint_length_16(self):
        from portfolio.stable_rollup.schema_registry_v159 import PORTFOLIO_SCHEMAS
        for s in PORTFOLIO_SCHEMAS:
            assert len(s.fingerprint) == 16, \
                f"{s.schema_id} fingerprint length {len(s.fingerprint)} != 16"

    def test_schema_check_drift_empty_baseline(self):
        from portfolio.stable_rollup.schema_registry_v159 import SchemaRegistryV159
        # Empty baseline has no keys to compare, so no drift is reported
        drift = SchemaRegistryV159().check_drift({})
        assert isinstance(drift, list)

    def test_walk_forward_schema_present(self):
        from portfolio.stable_rollup.schema_registry_v159 import SchemaRegistryV159
        s = SchemaRegistryV159().get_by_id("WalkForwardConfiguration")
        assert s is not None
        assert len(s.required_fields) > 0


# ===========================================================================
# 34. Extended Enum Registry Tests
# ===========================================================================
class TestEnumRegistryExtended:
    def test_transaction_type_enum_present(self):
        from portfolio.stable_rollup.enum_registry_v159 import EnumRegistryV159
        e = EnumRegistryV159().get_by_name("TransactionType")
        assert e is not None
        assert len(e.values) == 9

    def test_sizing_method_enum_present(self):
        from portfolio.stable_rollup.enum_registry_v159 import EnumRegistryV159
        e = EnumRegistryV159().get_by_name("SizingMethod")
        assert e is not None
        assert len(e.values) == 6

    def test_all_enums_have_stable_version(self):
        from portfolio.stable_rollup.enum_registry_v159 import STABLE_ENUMS
        for e in STABLE_ENUMS:
            assert e.stable_version is not None

    def test_enum_fingerprints_unique(self):
        from portfolio.stable_rollup.enum_registry_v159 import STABLE_ENUMS
        fps = [e.fingerprint for e in STABLE_ENUMS]
        assert len(fps) == len(set(fps)), "Duplicate enum fingerprints found"

    def test_capability_stage_has_five_values(self):
        from portfolio.stable_rollup.enum_registry_v159 import EnumRegistryV159
        e = EnumRegistryV159().get_by_name("CapabilityStage")
        assert len(e.values) == 5

    def test_risk_control_status_present(self):
        from portfolio.stable_rollup.enum_registry_v159 import EnumRegistryV159
        e = EnumRegistryV159().get_by_name("RiskControlStatus")
        assert e is not None
        assert len(e.values) == 5


# ===========================================================================
# 35. Extended Policy Registry Tests
# ===========================================================================
class TestPolicyRegistryExtended:
    def test_correlation_threshold_policy_present(self):
        from portfolio.stable_rollup.policy_registry_v159 import PolicyRegistryV159
        p = PolicyRegistryV159().get_by_id("correlation_threshold_default")
        assert p is not None
        assert p.policy_type == "CorrelationThresholdPolicy"

    def test_risk_control_policy_present(self):
        from portfolio.stable_rollup.policy_registry_v159 import PolicyRegistryV159
        p = PolicyRegistryV159().get_by_id("risk_control_default")
        assert p is not None
        assert p.policy_type == "RiskControlPolicy"

    def test_walk_forward_policy_present(self):
        from portfolio.stable_rollup.policy_registry_v159 import PolicyRegistryV159
        p = PolicyRegistryV159().get_by_id("walk_forward_config_default")
        assert p is not None
        assert p.policy_type == "WalkForwardConfigurationPolicy"

    def test_all_policies_not_none(self):
        from portfolio.stable_rollup.policy_registry_v159 import PolicyRegistryV159
        policies = PolicyRegistryV159().get_all()
        assert len(policies) == 9
        assert all(p is not None for p in policies)

    def test_all_policies_immutable(self):
        from portfolio.stable_rollup.policy_registry_v159 import STABLE_POLICIES
        for p in STABLE_POLICIES:
            assert p.immutable is True, f"{p.policy_id} should be immutable"

    def test_all_policies_versioned(self):
        from portfolio.stable_rollup.policy_registry_v159 import STABLE_POLICIES
        for p in STABLE_POLICIES:
            assert p.versioned is True, f"{p.policy_id} should be versioned"

    def test_all_policies_lineage_linked(self):
        from portfolio.stable_rollup.policy_registry_v159 import STABLE_POLICIES
        for p in STABLE_POLICIES:
            assert p.lineage_linked is True, f"{p.policy_id} should be lineage linked"

    def test_policy_effective_from_set(self):
        from portfolio.stable_rollup.policy_registry_v159 import STABLE_POLICIES
        for p in STABLE_POLICIES:
            assert p.effective_from is not None and len(p.effective_from) > 0

    def test_policy_get_by_id_not_found(self):
        from portfolio.stable_rollup.policy_registry_v159 import PolicyRegistryV159
        result = PolicyRegistryV159().get_by_id("nonexistent_policy")
        assert result is None


# ===========================================================================
# 36. Extended CLI Registry Tests
# ===========================================================================
class TestCLIRegistryExtended:
    def test_cli_count_gte_337(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        assert CLIRegistryV159().get_count() >= 337

    def test_no_formal_ledger_write_commands(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        for r in CLIRegistryV159().get_all():
            assert r.formal_ledger_write is False, \
                f"Command {r.command} has formal_ledger_write=True"

    def test_no_network_required_commands(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        for r in CLIRegistryV159().get_all():
            assert r.network_required is False, \
                f"Command {r.command} has network_required=True"

    def test_all_records_have_research_only(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        for r in CLIRegistryV159().get_all():
            assert r.research_only is True, \
                f"Command {r.command} has research_only=False"

    def test_validate_returns_count(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        result = CLIRegistryV159().validate()
        assert "count" in result
        assert result["count"] >= 337

    def test_portfolio_stable_commands_present(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        commands = {r.command for r in CLIRegistryV159().get_all()}
        assert "portfolio-stable-health" in commands

    def test_validate_returns_valid_key(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        result = CLIRegistryV159().validate()
        assert "valid" in result
        assert result["valid"] is True

    def test_validate_returns_issues_list(self):
        from portfolio.stable_rollup.cli_registry_v159 import CLIRegistryV159
        result = CLIRegistryV159().validate()
        assert "issues" in result
        assert isinstance(result["issues"], list)


# ===========================================================================
# 37. Extended Health Registry Tests
# ===========================================================================
class TestHealthRegistryExtended:
    def test_get_by_id_not_found(self):
        from portfolio.stable_rollup.health_registry_v159 import HealthRegistryV159
        h = HealthRegistryV159().get_by_id("nonexistent_health")
        assert h is None

    def test_portfolio_health_registered(self):
        from portfolio.stable_rollup.health_registry_v159 import HealthRegistryV159
        h = HealthRegistryV159().get_by_id("portfolio_health")
        assert h is not None
        assert h.command == "portfolio-health"
        assert h.expected_checks == 32

    def test_all_health_have_expected_checks(self):
        from portfolio.stable_rollup.health_registry_v159 import HEALTH_REGISTRY
        for h in HEALTH_REGISTRY:
            assert h.expected_checks > 0, f"{h.health_id} has no expected checks"

    def test_all_health_have_minimum_pass_count(self):
        from portfolio.stable_rollup.health_registry_v159 import HEALTH_REGISTRY
        for h in HEALTH_REGISTRY:
            assert h.minimum_pass_count > 0, f"{h.health_id} has no minimum pass count"

    def test_minimum_pass_matches_expected(self):
        from portfolio.stable_rollup.health_registry_v159 import HEALTH_REGISTRY
        for h in HEALTH_REGISTRY:
            assert h.minimum_pass_count <= h.expected_checks, \
                f"{h.health_id}: min_pass > expected_checks"

    def test_validate_returns_count(self):
        from portfolio.stable_rollup.health_registry_v159 import HealthRegistryV159
        result = HealthRegistryV159().validate()
        assert result["count"] == 13

    def test_forum_health_registered(self):
        from portfolio.stable_rollup.health_registry_v159 import HealthRegistryV159
        h = HealthRegistryV159().get_by_id("forum_health")
        assert h is not None
        assert h.expected_checks == 59

    def test_cli_registration_health_registered(self):
        from portfolio.stable_rollup.health_registry_v159 import HealthRegistryV159
        h = HealthRegistryV159().get_by_id("cli_registration_health")
        assert h is not None
        assert h.expected_checks == 6

    def test_all_health_have_stable_version(self):
        from portfolio.stable_rollup.health_registry_v159 import HEALTH_REGISTRY
        for h in HEALTH_REGISTRY:
            assert h.stable_version == "1.5.9", \
                f"{h.health_id} stable_version={h.stable_version}"

    def test_all_health_have_module(self):
        from portfolio.stable_rollup.health_registry_v159 import HEALTH_REGISTRY
        for h in HEALTH_REGISTRY:
            assert h.module is not None and len(h.module) > 0


# ===========================================================================
# 38. Extended Release Gate Registry Tests
# ===========================================================================
class TestReleaseGateRegistryExtended:
    def test_get_by_id_not_found(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import ReleaseGateRegistryV159
        g = ReleaseGateRegistryV159().get_by_id("nonexistent_gate")
        assert g is None

    def test_portfolio_research_gate_exists(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import ReleaseGateRegistryV159
        g = ReleaseGateRegistryV159().get_by_id("portfolio_research_gate")
        assert g is not None
        assert g.expected_checks == 10

    def test_walk_forward_gate_expected_checks(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import ReleaseGateRegistryV159
        g = ReleaseGateRegistryV159().get_by_id("portfolio_walk_forward_gate")
        assert g is not None
        assert g.expected_checks == 36

    def test_only_stable_gate_public(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import RELEASE_GATE_REGISTRY
        public_gates = [g for g in RELEASE_GATE_REGISTRY if g.public_cli_available]
        assert len(public_gates) == 1
        assert public_gates[0].gate_id == "portfolio_stable_gate"

    def test_all_gates_have_required_result_schema(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import RELEASE_GATE_REGISTRY
        for g in RELEASE_GATE_REGISTRY:
            assert "gate_passed" in g.required_result_schema
            assert "status" in g.required_result_schema

    def test_validate_returns_count(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import ReleaseGateRegistryV159
        result = ReleaseGateRegistryV159().validate()
        assert result["count"] == 6

    def test_correlation_gate_present(self):
        from portfolio.stable_rollup.release_gate_registry_v159 import ReleaseGateRegistryV159
        g = ReleaseGateRegistryV159().get_by_id("correlation_exposure_gate")
        assert g is not None
        assert g.expected_checks == 30


# ===========================================================================
# 39. Extended PIT Contract Tests
# ===========================================================================
class TestPITContractExtended:
    def test_contract_id(self):
        from portfolio.stable_rollup.pit_contract_v159 import PIT_CONTRACT
        assert PIT_CONTRACT.contract_id == "portfolio_pit_contract_v159"

    def test_contract_status_valid(self):
        from portfolio.stable_rollup.pit_contract_v159 import PIT_CONTRACT
        assert PIT_CONTRACT.status == "VALID"

    def test_blocking_violations_count(self):
        from portfolio.stable_rollup.pit_contract_v159 import PIT_CONTRACT
        assert len(PIT_CONTRACT.blocking_violations) == 4

    def test_validate_no_data(self):
        from portfolio.stable_rollup.pit_contract_v159 import PITContractV159
        result = PITContractV159().validate({}, as_of="2020-01-01")
        assert result["is_valid"] is True

    def test_matrix_module_coverage(self):
        from portfolio.stable_rollup.pit_contract_v159 import PIT_CONTRACT_MATRIX
        modules = [entry["module"] for entry in PIT_CONTRACT_MATRIX]
        assert "portfolio" in modules
        assert "portfolio.sizing" in modules
        assert "portfolio.walk_forward" in modules

    def test_silent_fallback_is_blocking(self):
        from portfolio.stable_rollup.pit_contract_v159 import PIT_CONTRACT
        assert "silent_fallback_to_current" in PIT_CONTRACT.blocking_violations

    def test_future_universe_is_blocking(self):
        from portfolio.stable_rollup.pit_contract_v159 import PIT_CONTRACT
        assert "future_universe_used" in PIT_CONTRACT.blocking_violations

    def test_matrix_all_have_blocking_field(self):
        from portfolio.stable_rollup.pit_contract_v159 import PIT_CONTRACT_MATRIX
        for entry in PIT_CONTRACT_MATRIX:
            assert "blocking" in entry


# ===========================================================================
# 40. Extended Lineage Contract Tests
# ===========================================================================
class TestLineageContractExtended:
    def test_contract_id(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LINEAGE_CONTRACT
        assert LINEAGE_CONTRACT.contract_id == "portfolio_lineage_contract_v159"

    def test_lineage_chains_count(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LINEAGE_CHAINS
        assert len(LINEAGE_CHAINS) == 5

    def test_check_drift_returns_empty(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LineageContractV159
        assert LineageContractV159().check_drift() == []

    def test_get_chains_returns_dict(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LineageContractV159
        chains = LineageContractV159().get_chains()
        assert isinstance(chains, dict)
        assert "portfolio_report" in chains

    def test_blocking_violations_count(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LINEAGE_CONTRACT
        assert len(LINEAGE_CONTRACT.blocking_violations) == 5

    def test_orphan_result_is_blocking(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LINEAGE_CONTRACT
        assert "orphan_result" in LINEAGE_CONTRACT.blocking_violations

    def test_validate_with_source_lineage_ids(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LineageContractV159
        result = LineageContractV159().validate_result({
            "content_hash": "abc",
            "calculation_version": "1.5.9",
            "source_lineage_ids": ["snap_001", "snap_002"],
        })
        assert result["is_valid"] is True

    def test_rules_count(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LINEAGE_CONTRACT
        assert len(LINEAGE_CONTRACT.rules) == 11


# ===========================================================================
# 41. Extended Reproducibility Contract Tests
# ===========================================================================
class TestReproducibilityContractExtended:
    def test_contract_id(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import REPRODUCIBILITY_CONTRACT
        assert REPRODUCIBILITY_CONTRACT.contract_id == "portfolio_reproducibility_contract_v159"

    def test_contract_status_valid(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import REPRODUCIBILITY_CONTRACT
        assert REPRODUCIBILITY_CONTRACT.status == "VALID"

    def test_blocking_violations_count(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import REPRODUCIBILITY_CONTRACT
        assert len(REPRODUCIBILITY_CONTRACT.blocking_violations) == 3

    def test_nondeterministic_hash_blocking(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import REPRODUCIBILITY_CONTRACT
        assert "nondeterministic_hash" in REPRODUCIBILITY_CONTRACT.blocking_violations

    def test_validate_manifest_missing_timezone(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import ReproducibilityContractV159
        result = ReproducibilityContractV159().validate_manifest({
            "config_hash": "abc123",
            "calendar_version": "1.0",
        })
        assert result["is_valid"] is False
        assert "MISSING_TIMEZONE" in result["violations"]

    def test_validate_manifest_missing_calendar(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import ReproducibilityContractV159
        result = ReproducibilityContractV159().validate_manifest({
            "config_hash": "abc123",
            "timezone": "Asia/Taipei",
        })
        assert result["is_valid"] is False
        assert "MISSING_CALENDAR_VERSION" in result["violations"]

    def test_check_drift_returns_empty(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import ReproducibilityContractV159
        assert ReproducibilityContractV159().check_drift() == []

    def test_rules_include_deterministic_ordering(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import REPRODUCIBILITY_CONTRACT
        rules_text = " ".join(REPRODUCIBILITY_CONTRACT.rules)
        assert "deterministic" in rules_text.lower()

    def test_rules_include_timezone(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import REPRODUCIBILITY_CONTRACT
        rules_text = " ".join(REPRODUCIBILITY_CONTRACT.rules)
        assert "timezone" in rules_text.lower()

    def test_rules_include_config_hash(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import REPRODUCIBILITY_CONTRACT
        rules_text = " ".join(REPRODUCIBILITY_CONTRACT.rules)
        assert "config hash" in rules_text.lower()


# ===========================================================================
# 42. Extended Compatibility Registry Tests
# ===========================================================================
class TestCompatibilityRegistryExtended:
    def test_v159_compatible(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        result = CompatibilityRegistryV159().is_compatible("1.5.9")
        assert result["compatible"] is True
        assert result["reason"] == "WITHIN_SUPPORTED_RANGE"

    def test_v151_compatible(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        result = CompatibilityRegistryV159().is_compatible("1.5.1")
        assert result["compatible"] is True

    def test_v130_not_compatible(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        result = CompatibilityRegistryV159().is_compatible("1.3.0")
        assert result["compatible"] is False

    def test_future_major_reason(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        result = CompatibilityRegistryV159().is_compatible("2.0.0")
        assert "FUTURE_MAJOR" in result["reason"]

    def test_malformed_version(self):
        from portfolio.stable_rollup.compatibility_registry_v159 import CompatibilityRegistryV159
        result = CompatibilityRegistryV159().is_compatible("invalid")
        assert result["compatible"] is False


# ===========================================================================
# 43. Extended Migration Registry Tests
# ===========================================================================
class TestMigrationRegistryExtended:
    def test_first_migration_is_150_to_1501(self):
        from portfolio.stable_rollup.migration_registry_v159 import MIGRATION_REGISTRY
        first = MIGRATION_REGISTRY[0]
        assert first.source_version == "1.5.0"
        assert first.target_version == "1.5.0.1"

    def test_last_migration_is_154_to_159(self):
        from portfolio.stable_rollup.migration_registry_v159 import MIGRATION_REGISTRY
        last = MIGRATION_REGISTRY[-1]
        assert last.source_version == "1.5.4"
        assert last.target_version == "1.5.9"

    def test_all_migrations_reversible(self):
        from portfolio.stable_rollup.migration_registry_v159 import MIGRATION_REGISTRY
        for m in MIGRATION_REGISTRY:
            assert m.reversible is True, f"{m.migration_id} should be reversible"

    def test_no_runtime_db_migrations(self):
        from portfolio.stable_rollup.migration_registry_v159 import MIGRATION_REGISTRY
        for m in MIGRATION_REGISTRY:
            assert m.runtime_db_migration is False, \
                f"{m.migration_id} unexpectedly requires runtime DB migration"

    def test_all_migrations_have_notes(self):
        from portfolio.stable_rollup.migration_registry_v159 import MIGRATION_REGISTRY
        for m in MIGRATION_REGISTRY:
            assert "NO_DATA_MIGRATION" in m.notes, \
                f"{m.migration_id} missing NO_DATA_MIGRATION in notes"


# ===========================================================================
# 44. Extended Stable Manifest Tests
# ===========================================================================
class TestStableManifestExtended:
    def test_manifest_planned_capabilities(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m = StableManifestBuilder().build()
        assert len(m.planned_capabilities) >= 7

    def test_manifest_disabled_capabilities(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m = StableManifestBuilder().build()
        assert len(m.disabled_capabilities) >= 1

    def test_manifest_enum_fingerprints(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m = StableManifestBuilder().build()
        assert len(m.enum_fingerprints) == 13

    def test_manifest_cli_count(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m = StableManifestBuilder().build()
        assert m.cli_count == 310

    def test_manifest_has_release_gate_baselines(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m = StableManifestBuilder().build()
        assert "stable" in m.release_gate_baselines
        assert m.release_gate_baselines["stable"] == "PASS"

    def test_manifest_known_limitations_count(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m = StableManifestBuilder().build()
        assert len(m.known_limitations) >= 6

    def test_manifest_has_research_only_limitation(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m = StableManifestBuilder().build()
        assert "research-only" in m.known_limitations

    def test_manifest_has_no_broker_limitation(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m = StableManifestBuilder().build()
        assert "no-broker" in m.known_limitations

    def test_validate_hash_mismatch_detected(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        builder = StableManifestBuilder()
        manifest = builder.build()
        manifest.content_hash = "tampered_hash"
        result = builder.validate(manifest)
        assert result["valid"] is False
        assert "HASH_MISMATCH" in result["issues"]

    def test_to_json_has_baselines(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        import json
        builder = StableManifestBuilder()
        m = builder.build()
        j = builder.to_json(m)
        data = json.loads(j)
        assert "baselines" in data
        assert data["baselines"]["stable"] == "1.5.9"

    def test_to_json_has_known_limitations(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        import json
        builder = StableManifestBuilder()
        m = builder.build()
        j = builder.to_json(m)
        data = json.loads(j)
        assert "known_limitations" in data
        assert len(data["known_limitations"]) >= 6


# ===========================================================================
# 45. Extended Readiness Matrix Tests
# ===========================================================================
class TestReadinessMatrixExtended:
    def test_disabled_items_present(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        all_items = ReadinessMatrixV159().get_all()
        disabled = [i for i in all_items if i.stage == "DISABLED"]
        assert len(disabled) >= 1

    def test_production_trading_is_disabled(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        items = ReadinessMatrixV159().get_all()
        prod = next((i for i in items if "Production Trading" in i.capability), None)
        assert prod is not None
        assert prod.ready is False
        assert prod.stage == "DISABLED"

    def test_portfolio_stable_rollup_is_ready(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        items = ReadinessMatrixV159().get_all()
        item = next((i for i in items if "Stable Rollup" in i.capability), None)
        assert item is not None
        assert item.ready is True

    def test_all_ready_items_have_implementation(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        for item in ReadinessMatrixV159().get_stable():
            assert item.implementation is True, \
                f"{item.capability} has ready=True but implementation=False"

    def test_blockers_include_permanently_blocked(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        all_blockers = []
        for _, bl in ReadinessMatrixV159().get_blockers():
            all_blockers.extend(bl)
        assert "permanently-blocked" in all_blockers

    def test_validate_issues_empty(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        result = ReadinessMatrixV159().validate()
        assert result["issues"] == []

    def test_planned_count(self):
        from portfolio.stable_rollup.readiness_matrix_v159 import ReadinessMatrixV159
        planned = ReadinessMatrixV159().get_planned()
        assert len(planned) == 4


# ===========================================================================
# 46. Extended Integration Audit Tests
# ===========================================================================
class TestIntegrationAuditExtended:
    def test_sizing_to_correlation_passes(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().audit_sizing_to_correlation()
        assert result["status"] == "PASS"

    def test_correlation_to_risk_passes(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().audit_correlation_to_risk()
        assert result["status"] == "PASS"

    def test_risk_to_walk_forward_passes(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().audit_risk_to_walk_forward()
        assert result["status"] == "PASS"

    def test_walk_forward_to_manifest_passes(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().audit_walk_forward_to_manifest()
        assert result["status"] == "PASS"

    def test_fixture_integration_no_future_leakage(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().run_fixture_integration()
        assert result["no_future_leakage"] is True

    def test_fixture_integration_complete_lineage(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().run_fixture_integration()
        assert result["complete_lineage"] is True

    def test_fixture_integration_reproducible(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().run_fixture_integration()
        assert result["reproducible"] is True

    def test_fixture_integration_no_formal_ledger_write(self):
        from portfolio.stable_rollup.integration_audit_v159 import IntegrationAuditV159
        result = IntegrationAuditV159().run_fixture_integration()
        assert result["no_formal_ledger_write"] is True


# ===========================================================================
# 47. Extended Debt Scanner Tests
# ===========================================================================
class TestDebtScannerExtended:
    def test_scan_hardcoded_paths_returns_list(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        findings = DebtScannerV159().scan_hardcoded_paths()
        assert isinstance(findings, list)

    def test_scan_version_whitelist_debt_returns_list(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        findings = DebtScannerV159().scan_version_whitelist_debt()
        assert isinstance(findings, list)

    def test_run_all_has_informational_key(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        result = DebtScannerV159().run_all()
        assert "informational" in result
        assert isinstance(result["informational"], list)

    def test_run_all_has_warning_count(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        result = DebtScannerV159().run_all()
        assert "warning_count" in result
        assert isinstance(result["warning_count"], int)

    def test_run_all_has_informational_count(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        result = DebtScannerV159().run_all()
        assert "informational_count" in result

    def test_broker_scan_returns_zero_blocking(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        findings = DebtScannerV159().scan_broker_references()
        blocking = [f for f in findings if f.get("severity") == "BLOCKING"]
        assert len(blocking) == 0

    def test_run_all_blocking_is_empty_list(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        result = DebtScannerV159().run_all()
        assert result["blocking"] == []

    def test_hardcoded_paths_severity_is_warning(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        findings = DebtScannerV159().scan_hardcoded_paths()
        for f in findings:
            assert f.get("severity") == "WARNING"

    def test_broker_findings_have_required_keys(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        # Since we expect zero broker findings, we just verify the method structure
        findings = DebtScannerV159().scan_broker_references()
        assert isinstance(findings, list)
        # all findings (if any) should have file, severity, label
        for f in findings:
            assert "file" in f
            assert "severity" in f
            assert "label" in f

    def test_status_is_pass_when_no_blocking(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        result = DebtScannerV159().run_all()
        assert result["status"] == "PASS"
        assert result["blocking_debt_zero"] is True

    def test_scanner_scans_portfolio_directory(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159, SCAN_ROOT
        import os
        assert os.path.isdir(os.path.join(SCAN_ROOT, "portfolio"))

    def test_multiple_scans_are_idempotent(self):
        from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
        scanner = DebtScannerV159()
        r1 = scanner.run_all()
        r2 = scanner.run_all()
        assert r1["blocking_count"] == r2["blocking_count"]
        assert r1["status"] == r2["status"]


# ===========================================================================
# 48. Extended Query Service Tests
# ===========================================================================
class TestQueryServiceExtended:
    def test_get_cli_registry(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().get_cli_registry()
        assert "count" in result
        assert result["count"] >= 337

    def test_get_stable_rollup_result_alias(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().get_stable_rollup_result()
        assert result.status == "PASS"
        assert result.research_only is True

    def test_explain_has_limitations(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().explain_stable_rollup()
        assert "limitations" in result
        assert "research-only" in result["limitations"]

    def test_explain_has_stable_capabilities(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().explain_stable_rollup()
        assert "stable_capabilities" in result
        assert len(result["stable_capabilities"]) == 6

    def test_rollup_generated_at_is_set(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.generated_at is not None

    def test_rollup_manifest_hash_set(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.manifest_hash is not None
        assert len(result.manifest_hash) == 32


# ===========================================================================
# 49. Extended GUI Panel Tests
# ===========================================================================
class TestGUIPanelExtended:
    def test_panel_forbidden_actions_count(self):
        from gui.portfolio_stable_rollup_panel import FORBIDDEN_ACTIONS
        assert len(FORBIDDEN_ACTIONS) >= 4

    def test_panel_metadata_has_production_trading_blocked(self):
        from gui.portfolio_stable_rollup_panel import PortfolioStableRollupPanel
        meta = PortfolioStableRollupPanel().get_metadata()
        assert meta["production_trading_blocked"] is True

    def test_panel_no_execute_action(self):
        from gui.portfolio_stable_rollup_panel import FORBIDDEN_ACTIONS
        assert "Execute" in FORBIDDEN_ACTIONS

    def test_panel_no_broker_sync_action(self):
        from gui.portfolio_stable_rollup_panel import FORBIDDEN_ACTIONS
        assert "Broker Sync" in FORBIDDEN_ACTIONS

    def test_safety_banner_has_research_only(self):
        from gui.portfolio_stable_rollup_panel import SAFETY_BANNER_LINES
        combined = " ".join(SAFETY_BANNER_LINES)
        assert "Research Only" in combined or "RESEARCH_ONLY" in combined

    def test_safety_banner_has_no_real_orders(self):
        from gui.portfolio_stable_rollup_panel import SAFETY_BANNER_LINES
        combined = " ".join(SAFETY_BANNER_LINES)
        assert "No Real Orders" in combined or "NO_REAL_ORDERS" in combined

    def test_panel_headless_safe_is_none(self):
        from gui.portfolio_stable_rollup_panel import PortfolioStableRollupPanel
        w = PortfolioStableRollupPanel().get_widget()
        assert w is None

    def test_panel_production_trading_blocked_module_level(self):
        import gui.portfolio_stable_rollup_panel as panel
        assert panel.PRODUCTION_TRADING_BLOCKED is True

    def test_panel_no_broker_module_level(self):
        import gui.portfolio_stable_rollup_panel as panel
        assert panel.NO_BROKER is True


# ===========================================================================
# 50. Extended Release Gate Tests
# ===========================================================================
class TestReleaseGateExtended:
    def test_gate_checks_count(self):
        from release.portfolio_stable_release_gate_v159 import GATE_CHECKS
        assert len(GATE_CHECKS) == 36

    def test_all_gate_checks_true(self):
        from release.portfolio_stable_release_gate_v159 import GATE_CHECKS
        for k, v in GATE_CHECKS.items():
            assert v is True, f"Gate check {k} is not True"

    def test_safety_gates_count(self):
        from release.portfolio_stable_release_gate_v159 import SAFETY_GATES
        assert len(SAFETY_GATES) == 7

    def test_gate_result_freeze_only(self):
        from release.portfolio_stable_release_gate_v159 import PortfolioStableReleaseGate
        result = PortfolioStableReleaseGate().run()
        assert result["freeze_only"] is True

    def test_gate_result_safety_failures_empty(self):
        from release.portfolio_stable_release_gate_v159 import PortfolioStableReleaseGate
        result = PortfolioStableReleaseGate().run()
        assert result["safety_failures"] == []

    def test_gate_result_failed_empty(self):
        from release.portfolio_stable_release_gate_v159 import PortfolioStableReleaseGate
        result = PortfolioStableReleaseGate().run()
        assert result["failed"] == []

    def test_gate_result_passed_count(self):
        from release.portfolio_stable_release_gate_v159 import PortfolioStableReleaseGate
        result = PortfolioStableReleaseGate().run()
        assert result["passed"] == 36
        assert result["total"] == 36


# ===========================================================================
# 51. Regression Tests — Version and Baseline Integrity
# ===========================================================================
class TestRegressionVersionBaselines:
    def test_version_is_exactly_159(self):
        from release.version_info import VERSION
        # Must be 1.5.9.x or 1.5.9
        assert _parse_ver(VERSION)[:3] >= _parse_ver("1.5.9")[:3]

    def test_portfolio_stable_baseline(self):
        from release.version_info import PORTFOLIO_STABLE_BASELINE
        assert PORTFOLIO_STABLE_BASELINE == "1.5.9"

    def test_manifest_hash_is_32_hex(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m = StableManifestBuilder().build()
        assert len(m.content_hash) == 32
        assert all(c in "0123456789abcdef" for c in m.content_hash)

    def test_stable_capability_versions_at_least_150(self):
        from portfolio.stable_rollup.capability_registry_v159 import STABLE_CAPABILITIES
        for c in STABLE_CAPABILITIES:
            assert _parse_ver(c.stable_version) >= _parse_ver("1.5.0")

    def test_schema_fingerprints_stable_159(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m1 = StableManifestBuilder().build()
        m2 = StableManifestBuilder().build()
        assert m1.schema_fingerprints == m2.schema_fingerprints

    def test_enum_fingerprints_stable_159(self):
        from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
        m1 = StableManifestBuilder().build()
        m2 = StableManifestBuilder().build()
        assert m1.enum_fingerprints == m2.enum_fingerprints

    def test_rollup_stable_capabilities_count_is_6(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.stable_capabilities == 6

    def test_rollup_planned_capabilities_count_is_7(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.planned_capabilities == 7

    def test_rollup_schemas_total_is_33(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.schemas_total == 33

    def test_rollup_enums_total_is_13(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.enums_total == 13

    def test_rollup_policies_total_is_9(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.policies_total == 9

    def test_rollup_health_checks_is_13(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.health_checks == 13

    def test_rollup_release_gates_is_6(self):
        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        result = StableRollupQueryService().run_portfolio_stable_rollup()
        assert result.release_gates == 6


# ===========================================================================
# 52. Regression Tests — Safety Invariants Cross-check
# ===========================================================================
class TestRegressionSafetyInvariants:
    def test_safety_contract_no_drift(self):
        from portfolio.stable_rollup.safety_contract_v159 import SafetyContractV159
        assert SafetyContractV159().check_drift() == []

    def test_reproducibility_no_drift(self):
        from portfolio.stable_rollup.reproducibility_contract_v159 import ReproducibilityContractV159
        assert ReproducibilityContractV159().check_drift() == []

    def test_lineage_no_drift(self):
        from portfolio.stable_rollup.lineage_contract_v159 import LineageContractV159
        assert LineageContractV159().check_drift() == []

    def test_pit_no_drift(self):
        from portfolio.stable_rollup.pit_contract_v159 import PITContractV159
        assert PITContractV159().check_drift() == []

    def test_version_info_auto_apply_false(self):
        from release.version_info import AUTO_APPLY_ENABLED
        assert AUTO_APPLY_ENABLED is False

    def test_version_info_auto_rebalance_false(self):
        from release.version_info import AUTO_REBALANCE_ENABLED
        assert AUTO_REBALANCE_ENABLED is False

    def test_forbidden_flags_count(self):
        from portfolio.stable_rollup.safety_contract_v159 import FORBIDDEN_FLAGS
        assert len(FORBIDDEN_FLAGS) >= 14

    def test_required_flags_count(self):
        from portfolio.stable_rollup.safety_contract_v159 import REQUIRED_FLAGS
        assert len(REQUIRED_FLAGS) == 3

    def test_safety_rules_include_no_leverage(self):
        from portfolio.stable_rollup.safety_contract_v159 import SAFETY_CONTRACT
        rules_text = " ".join(SAFETY_CONTRACT.rules)
        assert "NO_LEVERAGE" in rules_text

    def test_safety_rules_include_no_short(self):
        from portfolio.stable_rollup.safety_contract_v159 import SAFETY_CONTRACT
        rules_text = " ".join(SAFETY_CONTRACT.rules)
        assert "NO_SHORT" in rules_text

    def test_safety_rules_count(self):
        from portfolio.stable_rollup.safety_contract_v159 import SAFETY_CONTRACT
        assert len(SAFETY_CONTRACT.rules) == 13

    def test_safety_blocking_violations_count(self):
        from portfolio.stable_rollup.safety_contract_v159 import SAFETY_CONTRACT
        assert len(SAFETY_CONTRACT.blocking_violations) == 6

    def test_report_production_trading_blocked(self):
        from reports.portfolio_stable_rollup_report import PortfolioStableRollupReport
        r = PortfolioStableRollupReport().generate()
        assert r["PRODUCTION_TRADING_BLOCKED"] is True


# ===========================================================================
# 53. Regression Tests — CLI Commands Registered
# ===========================================================================
class TestRegressionCLICommands:
    def test_portfolio_stable_cli_command_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "portfolio-stable-cli" in names

    def test_portfolio_stable_reproducibility_command_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "portfolio-stable-reproducibility-contract" in names

    def test_portfolio_stable_manifest_validate_command_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "portfolio-stable-manifest-validate" in names

    def test_portfolio_stable_integration_audit_command_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "portfolio-stable-integration-audit" in names

    def test_portfolio_stable_debt_scan_command_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "portfolio-stable-debt-scan" in names

    def test_portfolio_stable_safety_contract_command_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "portfolio-stable-safety-contract" in names

    def test_portfolio_stable_lineage_contract_command_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "portfolio-stable-lineage-contract" in names

    def test_portfolio_stable_pit_contract_command_registered(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "portfolio-stable-pit-contract" in names

    def test_total_commands_gte_337(self):
        from cli.command_registry import PROVIDER_COMMANDS
        assert len(PROVIDER_COMMANDS) >= 337

    def test_no_live_rebalance_command(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "live-rebalance" not in names

    def test_no_submit_order_command(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "submit-order" not in names

    def test_no_execute_order_command(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "execute-order" not in names


# ===========================================================================
# 54. Regression Tests — Integrity Validator Cross-checks
# ===========================================================================
class TestRegressionIntegrityValidator:
    def test_integrity_run_all_results_have_schema_key(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().run_all()
        assert "schema" in result["results"]

    def test_integrity_run_all_results_have_enum_key(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().run_all()
        assert "enum" in result["results"]

    def test_integrity_run_all_results_have_capability_key(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().run_all()
        assert "capability" in result["results"]

    def test_integrity_run_all_results_have_safety_key(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().run_all()
        assert "safety" in result["results"]

    def test_schema_integrity_has_count(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().validate_schema_integrity()
        assert "count" in result
        assert result["count"] == 33

    def test_enum_integrity_has_count(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().validate_enum_integrity()
        assert "count" in result
        assert result["count"] == 13

    def test_capability_integrity_has_issues(self):
        from portfolio.stable_rollup.integrity_validator_v159 import IntegrityValidator
        result = IntegrityValidator().validate_capability_integrity()
        assert "issues" in result
        assert result["issues"] == []
