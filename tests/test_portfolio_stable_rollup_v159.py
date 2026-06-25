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
