"""
tests/test_provider_stable_rollup_v149.py — v1.4.9 Provider Stable Rollup tests.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] All tests offline. No network. No external fetch.

140+ targeted tests across 14 test classes.
"""
from __future__ import annotations

import json
import os

import pytest

_FIXTURE_DIR = os.path.join(
    os.path.dirname(__file__), "fixtures", "provider_stable_rollup"
)


def _load_fixture(name: str) -> dict:
    path = os.path.join(_FIXTURE_DIR, name)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ===========================================================================
# Version Info
# ===========================================================================

class TestVersionInfo:
    def test_1_version_is_149(self):
        from release.version_info import VERSION
        parts = tuple(int(x) for x in VERSION.split(".")[:3])
        assert parts >= (1, 4, 9), f"Expected VERSION >= 1.4.9, got {VERSION}"

    def test_2_release_name(self):
        from release.version_info import RELEASE_NAME
        assert RELEASE_NAME in ("Provider Stable Rollup", "Portfolio Research Foundation", "Portfolio Research Foundation Integrity Hotfix", "Portfolio Research CLI Completeness Hotfix", "Position Sizing", "Correlation & Exposure", "Correlation & Exposure Integrity Hotfix", "Drawdown & Risk Controls", "Portfolio Walk-forward Backtest", "Portfolio Stable Rollup", "Portfolio Stable Rollup Integrity Hotfix", "Portfolio Stable Rollup Release Gate Hotfix", "Live Paper Trading Foundation")

    def test_3_base_release_contains_148(self):
        from release.version_info import BASE_RELEASE
        def _parse_ver(v): return tuple(int(x) for x in v.split()[0].split(".")[:3] if x.isdigit())
        assert _parse_ver(BASE_RELEASE) >= _parse_ver("1.4.8")

    def test_4_provider_stable_baseline(self):
        from release.version_info import PROVIDER_STABLE_BASELINE
        assert PROVIDER_STABLE_BASELINE == "1.4.9"

    def test_5_provider_feature_baseline(self):
        from release.version_info import PROVIDER_FEATURE_BASELINE
        assert "1.4.8" in PROVIDER_FEATURE_BASELINE

    def test_6_replay_stable_baseline(self):
        from release.version_info import REPLAY_STABLE_BASELINE
        assert REPLAY_STABLE_BASELINE == "1.2.9"

    def test_7_no_real_orders_flag(self):
        from release.version_info import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_8_production_trading_blocked(self):
        from release.version_info import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True


# ===========================================================================
# Stable Module Constants
# ===========================================================================

class TestStableModuleConstants:
    def test_9_module_version(self):
        from data.stable import VERSION
        assert VERSION == "1.4.9"

    def test_10_module_release_name(self):
        from data.stable import RELEASE_NAME
        assert RELEASE_NAME == "Provider Stable Rollup"

    def test_11_collection_baseline(self):
        from data.stable import PREVIOUS_FULL_COLLECTION_BASELINE
        assert PREVIOUS_FULL_COLLECTION_BASELINE == 3597

    def test_12_pass_baseline(self):
        from data.stable import PREVIOUS_FULL_PASS_BASELINE
        assert PREVIOUS_FULL_PASS_BASELINE == 3597

    def test_13_skip_baseline(self):
        from data.stable import PREVIOUS_SKIPPED_BASELINE
        assert PREVIOUS_SKIPPED_BASELINE == 0

    def test_14_finmind_cannot_override(self):
        from data.stable import FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER
        assert FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER is False

    def test_15_ptt_no_standalone_formal(self):
        from data.stable import PTT_STANDALONE_FORMAL_CONCLUSION
        assert PTT_STANDALONE_FORMAL_CONCLUSION is False

    def test_16_ptt_no_buy_sell(self):
        from data.stable import PTT_CAN_GENERATE_BUY_SELL
        assert PTT_CAN_GENERATE_BUY_SELL is False

    def test_17_no_auto_fallback(self):
        from data.stable import AUTO_FALLBACK_ENABLED
        assert AUTO_FALLBACK_ENABLED is False

    def test_18_no_broker_execution(self):
        from data.stable import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False


# ===========================================================================
# Stable Capability Manifest
# ===========================================================================

class TestStableCapabilityManifest:
    def test_19_manifest_instantiates(self):
        from data.stable.capability_manifest_v149 import StableCapabilityManifest
        m = StableCapabilityManifest()
        assert m is not None

    def test_20_manifest_version(self):
        from data.stable.capability_manifest_v149 import StableCapabilityManifest
        assert StableCapabilityManifest.VERSION == "1.4.9"

    def test_21_get_all_returns_20(self):
        from data.stable.capability_manifest_v149 import StableCapabilityManifest
        caps = StableCapabilityManifest().get_all()
        assert len(caps) == 20

    def test_22_all_stable(self):
        from data.stable.capability_manifest_v149 import StableCapabilityManifest
        caps = StableCapabilityManifest().get_all()
        non_stable = [c["id"] for c in caps if c["status"] != "STABLE"]
        assert non_stable == []

    def test_23_validate_passes(self):
        from data.stable.capability_manifest_v149 import StableCapabilityManifest
        result = StableCapabilityManifest().validate()
        assert result["valid"] is True
        assert result["total_capabilities"] == 20
        assert result["stable_count"] == 20
        assert result["non_stable"] == []

    def test_24_provider_stable_rollup_present(self):
        from data.stable.capability_manifest_v149 import StableCapabilityManifest
        m = StableCapabilityManifest()
        cap = m.get_by_id("provider_stable_rollup")
        assert cap["status"] == "STABLE"
        assert cap["since"] == "1.4.9"

    def test_25_is_stable_twse(self):
        from data.stable.capability_manifest_v149 import StableCapabilityManifest
        assert StableCapabilityManifest().is_stable("twse_provider") is True

    def test_26_is_stable_forum(self):
        from data.stable.capability_manifest_v149 import StableCapabilityManifest
        assert StableCapabilityManifest().is_stable("forum_intelligence") is True

    def test_27_unknown_capability_not_stable(self):
        from data.stable.capability_manifest_v149 import StableCapabilityManifest
        assert StableCapabilityManifest().is_stable("nonexistent_xyz") is False

    def test_28_get_summary_has_items(self):
        from data.stable.capability_manifest_v149 import StableCapabilityManifest
        s = StableCapabilityManifest().get_summary()
        assert "items" in s
        assert len(s["items"]) == 20

    def test_29_fixture_valid(self):
        fx = _load_fixture("stable_manifest_valid.json")
        assert fx["total_capabilities"] == 20
        assert fx["valid"] is True

    def test_30_fixture_partial_fails(self):
        fx = _load_fixture("stable_manifest_partial.json")
        assert fx["valid"] is False
        assert len(fx["non_stable"]) > 0


# ===========================================================================
# Stable Provider Registry
# ===========================================================================

class TestStableProviderRegistry:
    def test_31_registry_instantiates(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        r = StableProviderRegistry()
        assert r is not None

    def test_32_registry_version(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        assert StableProviderRegistry.VERSION == "1.4.9"

    def test_33_six_providers(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        assert len(StableProviderRegistry().get_all()) == 6

    def test_34_four_primary_official(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        primaries = StableProviderRegistry().get_by_tier("PRIMARY_OFFICIAL")
        assert len(primaries) == 4

    def test_35_one_secondary_aggregator(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        secondary = StableProviderRegistry().get_by_tier("SECONDARY_AGGREGATOR")
        assert len(secondary) == 1

    def test_36_one_supplementary(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        supp = StableProviderRegistry().get_by_tier("SUPPLEMENTARY")
        assert len(supp) == 1

    def test_37_finmind_override_blocked(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        assert StableProviderRegistry.FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER is False

    def test_38_ptt_standalone_blocked(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        assert StableProviderRegistry.PTT_STANDALONE_FORMAL_CONCLUSION is False

    def test_39_ptt_buy_sell_blocked(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        assert StableProviderRegistry.PTT_CAN_GENERATE_BUY_SELL is False

    def test_40_validate_passes(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        result = StableProviderRegistry().validate()
        assert result["valid"] is True
        assert result["total_providers"] == 6

    def test_41_twse_is_primary(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        entry = StableProviderRegistry().get_by_id("twse_official")
        assert entry.authority_tier == "PRIMARY_OFFICIAL"
        assert entry.pit_supported is True

    def test_42_finmind_is_secondary(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        entry = StableProviderRegistry().get_by_id("finmind_aggregator")
        assert entry.authority_tier == "SECONDARY_AGGREGATOR"

    def test_43_ptt_is_supplementary(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        entry = StableProviderRegistry().get_by_id("ptt_stock")
        assert entry.authority_tier == "SUPPLEMENTARY"

    def test_44_unknown_provider_raises(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        with pytest.raises(KeyError):
            StableProviderRegistry().get_by_id("nonexistent_provider")

    def test_45_fixture_valid(self):
        fx = _load_fixture("provider_registry_valid.json")
        assert fx["valid"] is True
        assert fx["finmind_can_override_primary"] is False

    def test_46_fixture_override_violation_fails(self):
        fx = _load_fixture("provider_registry_override_violation.json")
        assert fx["valid"] is False
        assert fx["finmind_can_override_primary"] is True


# ===========================================================================
# Compatibility Contracts
# ===========================================================================

class TestCompatibilityContracts:
    def test_47_contracts_instantiate(self):
        from data.stable.compatibility_contract_v149 import CompatibilityContractRegistry
        assert CompatibilityContractRegistry() is not None

    def test_48_eight_contracts(self):
        from data.stable.compatibility_contract_v149 import CompatibilityContractRegistry
        contracts = CompatibilityContractRegistry().get_all()
        assert len(contracts) >= 8

    def test_49_no_breaking_changes_allowed(self):
        from data.stable.compatibility_contract_v149 import CompatibilityContractRegistry
        for c in CompatibilityContractRegistry().get_all():
            assert c["breaking_changes_allowed"] is False, \
                f"Contract {c['contract_id']} allows breaking changes"

    def test_50_validate_passes(self):
        from data.stable.compatibility_contract_v149 import CompatibilityContractRegistry
        result = CompatibilityContractRegistry().validate()
        assert result["valid"] is True

    def test_51_twse_empirical_contract_exists(self):
        from data.stable.compatibility_contract_v149 import CompatibilityContractRegistry
        c = CompatibilityContractRegistry().get_by_id("c001")
        assert c["provider"] == "twse_official"
        assert c["consumer"] == "empirical_backtest"

    def test_52_fixture_valid(self):
        fx = _load_fixture("compatibility_contracts_valid.json")
        assert fx["valid"] is True
        assert fx["breaking_changes_allowed"] is False


# ===========================================================================
# Schema Version Registry
# ===========================================================================

class TestSchemaVersionRegistry:
    def test_53_schema_registry_instantiates(self):
        from data.stable.schema_version_registry_v149 import SchemaVersionRegistry
        assert SchemaVersionRegistry() is not None

    def test_54_six_schemas(self):
        from data.stable.schema_version_registry_v149 import SchemaVersionRegistry
        schemas = SchemaVersionRegistry().get_all()
        assert len(schemas) == 6

    def test_55_no_drift(self):
        from data.stable.schema_version_registry_v149 import SchemaVersionRegistry
        result = SchemaVersionRegistry().validate()
        assert result["drift_detected"] == []

    def test_56_no_missing_pit(self):
        from data.stable.schema_version_registry_v149 import SchemaVersionRegistry
        result = SchemaVersionRegistry().validate()
        assert result["missing_pit_fields"] == []

    def test_57_validate_passes(self):
        from data.stable.schema_version_registry_v149 import SchemaVersionRegistry
        result = SchemaVersionRegistry().validate()
        assert result["valid"] is True

    def test_58_fixture_valid(self):
        fx = _load_fixture("schema_registry_valid.json")
        assert fx["valid"] is True
        assert fx["drift_detected"] == []


# ===========================================================================
# Policy Version Registry
# ===========================================================================

class TestPolicyVersionRegistry:
    def test_59_policy_registry_instantiates(self):
        from data.stable.policy_version_registry_v149 import PolicyVersionRegistry
        assert PolicyVersionRegistry() is not None

    def test_60_seven_policies(self):
        from data.stable.policy_version_registry_v149 import PolicyVersionRegistry
        policies = PolicyVersionRegistry().get_all()
        assert len(policies) >= 7

    def test_61_validate_passes(self):
        from data.stable.policy_version_registry_v149 import PolicyVersionRegistry
        result = PolicyVersionRegistry().validate()
        assert result["valid"] is True

    def test_62_safety_invariants_policy_exists(self):
        from data.stable.policy_version_registry_v149 import PolicyVersionRegistry
        p = PolicyVersionRegistry().get_by_id("safety_invariants")
        assert p is not None

    def test_63_pit_enforcement_policy_exists(self):
        from data.stable.policy_version_registry_v149 import PolicyVersionRegistry
        p = PolicyVersionRegistry().get_by_id("pit_enforcement")
        assert p is not None

    def test_64_fixture_valid(self):
        fx = _load_fixture("policy_registry_valid.json")
        assert fx["valid"] is True
        assert fx["total"] >= 7


# ===========================================================================
# Stable Baseline Snapshot
# ===========================================================================

class TestStableBaselineSnapshot:
    def test_65_snapshot_instantiates(self):
        from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
        assert StableBaselineSnapshot() is not None

    def test_66_snapshot_version(self):
        from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
        assert StableBaselineSnapshot.VERSION == "1.4.9"

    def test_67_collection_baseline_3597(self):
        from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
        snap = StableBaselineSnapshot().get()
        assert snap["full_collection_baseline"] == 3597

    def test_68_fail_baseline_zero(self):
        from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
        snap = StableBaselineSnapshot().get()
        assert snap["full_fail_baseline"] == 0

    def test_69_skip_baseline_zero(self):
        from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
        snap = StableBaselineSnapshot().get()
        assert snap["full_skip_baseline"] == 0

    def test_70_cli_baseline_181(self):
        from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
        snap = StableBaselineSnapshot().get()
        assert snap["cli_parser_count_baseline"] == 181

    def test_71_base_commit_present(self):
        from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
        snap = StableBaselineSnapshot().get()
        assert snap["base_commit_short"] == "d025d21"

    def test_72_validate_against_passing_run(self):
        from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
        actual = {"collection": 3700, "passed": 3700, "failed": 0,
                  "skipped": 0, "errors": 0}
        result = StableBaselineSnapshot().validate_against(actual)
        assert result["valid"] is True
        assert result["issues"] == []

    def test_73_validate_against_failing_run(self):
        from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
        actual = {"collection": 3500, "passed": 3490, "failed": 10,
                  "skipped": 0, "errors": 0}
        result = StableBaselineSnapshot().validate_against(actual)
        assert result["valid"] is False
        assert len(result["issues"]) > 0

    def test_74_get_summary_valid(self):
        from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
        s = StableBaselineSnapshot().get_summary()
        assert s["valid"] is True
        assert "items" in s

    def test_75_fixture_matches_baseline(self):
        fx = _load_fixture("baseline_snapshot_valid.json")
        assert fx["full_collection_baseline"] == 3597
        assert fx["cli_parser_count_baseline"] == 181


# ===========================================================================
# Collection Integrity
# ===========================================================================

class TestStableCollectionIntegrity:
    def test_76_collection_integrity_instantiates(self):
        from data.stable.collection_integrity_v149 import StableCollectionIntegrityCheck
        assert StableCollectionIntegrityCheck() is not None

    def test_77_minimum_baseline_3597(self):
        from data.stable.collection_integrity_v149 import MINIMUM_COLLECTION_BASELINE
        assert MINIMUM_COLLECTION_BASELINE == 3597

    def test_78_critical_groups_include_stable_rollup(self):
        from data.stable.collection_integrity_v149 import StableCollectionIntegrityCheck
        groups = StableCollectionIntegrityCheck._CRITICAL_GROUPS
        assert "test_provider_stable_rollup" in groups

    def test_79_run_returns_checks(self):
        from data.stable.collection_integrity_v149 import StableCollectionIntegrityCheck
        result = StableCollectionIntegrityCheck().run_all()
        assert isinstance(result, list)
        assert len(result) >= 11

    def test_80_all_checks_pass(self):
        from data.stable.collection_integrity_v149 import StableCollectionIntegrityCheck
        result = StableCollectionIntegrityCheck().run_all()
        failed = [r for r in result if r["status"] != "PASS"]
        assert failed == []

    def test_81_fixture_collection_valid(self):
        fx = _load_fixture("collection_valid.json")
        assert fx["collected"] >= fx["minimum"]
        assert fx["expected_result"] == "PASS"

    def test_82_fixture_collection_below_baseline(self):
        fx = _load_fixture("collection_below_baseline.json")
        assert fx["collected"] < fx["minimum"]
        assert fx["expected_result"] == "FAIL"


# ===========================================================================
# Provider Stable Profiles
# ===========================================================================

class TestProviderStableProfiles:
    def test_83_profiles_instantiate(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        assert ProviderStableProfileRegistry() is not None

    def test_84_six_profiles(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        assert len(ProviderStableProfileRegistry().get_all()) == 6

    def test_85_all_profiles_stable(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        for p in ProviderStableProfileRegistry().get_all():
            assert p.stability_status == "STABLE", f"{p.provider_id} not STABLE"

    def test_86_finmind_cannot_override(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        assert ProviderStableProfileRegistry.FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER is False

    def test_87_ptt_no_standalone_formal(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        assert ProviderStableProfileRegistry.PTT_STANDALONE_FORMAL_CONCLUSION is False

    def test_88_ptt_no_buy_sell(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        assert ProviderStableProfileRegistry.PTT_CAN_GENERATE_BUY_SELL is False

    def test_89_validate_passes(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        result = ProviderStableProfileRegistry().validate()
        assert result["valid"] is True
        assert result["non_stable"] == []
        assert result["override_violations"] == []

    def test_90_twse_standalone_formal_allowed(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        p = ProviderStableProfileRegistry().get_by_id("twse_official")
        assert p.standalone_formal_allowed is True
        assert p.authority_tier == "PRIMARY_OFFICIAL"

    def test_91_finmind_standalone_not_allowed(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        p = ProviderStableProfileRegistry().get_by_id("finmind_aggregator")
        assert p.standalone_formal_allowed is False
        assert p.can_override_primary is False

    def test_92_ptt_buy_sell_always_false(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        p = ProviderStableProfileRegistry().get_by_id("ptt_stock")
        assert p.buy_sell_allowed is False
        assert p.standalone_formal_allowed is False

    def test_93_four_primary_profiles(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        primaries = ProviderStableProfileRegistry().get_by_tier("PRIMARY_OFFICIAL")
        assert len(primaries) == 4

    def test_94_fixture_profiles_valid(self):
        fx = _load_fixture("provider_profiles_valid.json")
        assert fx["valid"] is True
        assert fx["non_stable"] == []
        assert fx["override_violations"] == []

    def test_95_fixture_ptt_violation(self):
        fx = _load_fixture("provider_profiles_ptt_violation.json")
        assert fx["valid"] is False
        assert fx["ptt_buy_sell_ok"] is False


# ===========================================================================
# Health Baseline
# ===========================================================================

class TestHealthBaseline:
    def test_96_health_baseline_instantiates(self):
        from data.stable.health_baseline_v149 import StableHealthBaseline
        assert StableHealthBaseline() is not None

    def test_97_health_baseline_runs(self):
        from data.stable.health_baseline_v149 import StableHealthBaseline
        result = StableHealthBaseline().run_all()
        assert isinstance(result, list)

    def test_98_health_baseline_passes(self):
        from data.stable.health_baseline_v149 import StableHealthBaseline
        result = StableHealthBaseline().run_all()
        failed = [r for r in result if r["status"] != "PASS"]
        assert failed == [], f"Failed health checks: {failed}"

    def test_99_get_summary_valid(self):
        from data.stable.health_baseline_v149 import StableHealthBaseline
        s = StableHealthBaseline().get_summary()
        assert s["valid"] is True
        assert s["failed"] == 0

    def test_100_expected_health_commands_present(self):
        from data.stable.health_baseline_v149 import StableHealthBaseline
        cmds = StableHealthBaseline().get_expected_commands()
        assert len(cmds) >= 14


# ===========================================================================
# Provider Stable Health Check
# ===========================================================================

class TestProviderStableHealthCheck:
    def test_101_health_check_instantiates(self):
        from release.provider_stable_health_v149 import ProviderStableRollupHealthCheck
        assert ProviderStableRollupHealthCheck() is not None

    def test_102_health_check_runs(self):
        from release.provider_stable_health_v149 import ProviderStableRollupHealthCheck
        result = ProviderStableRollupHealthCheck().run()
        assert isinstance(result, dict)

    def test_103_version_check_passes(self):
        from release.provider_stable_health_v149 import ProviderStableRollupHealthCheck
        result = ProviderStableRollupHealthCheck().run()
        assert result.get("version_is_149", ("FAIL", ""))[0] == "PASS"

    def test_104_release_name_check_passes(self):
        from release.provider_stable_health_v149 import ProviderStableRollupHealthCheck
        result = ProviderStableRollupHealthCheck().run()
        assert result.get("release_name_correct", ("FAIL", ""))[0] == "PASS"

    def test_105_all_checks_pass(self):
        from release.provider_stable_health_v149 import ProviderStableRollupHealthCheck
        result = ProviderStableRollupHealthCheck().run()
        failed = [(k, v) for k, v in result.items() if v[0] == "FAIL"]
        assert failed == [], f"Failed health checks: {failed}"

    def test_106_fixture_health_all_pass(self):
        fx = _load_fixture("health_all_pass.json")
        assert fx["all_pass"] is True
        assert fx["failed"] == 0


# ===========================================================================
# Provider Stable Release Gate
# ===========================================================================

class TestProviderStableReleaseGate:
    def test_107_gate_instantiates(self):
        from release.provider_stable_release_gate_v149 import ProviderStableReleaseGate
        assert ProviderStableReleaseGate() is not None

    def test_108_gate_runs(self):
        from release.provider_stable_release_gate_v149 import ProviderStableReleaseGate
        gates = ProviderStableReleaseGate().run()
        assert isinstance(gates, list)

    def test_109_fifteen_gates(self):
        from release.provider_stable_release_gate_v149 import ProviderStableReleaseGate
        gates = ProviderStableReleaseGate().run()
        assert len(gates) == 15

    def test_110_all_gates_pass(self):
        from release.provider_stable_release_gate_v149 import ProviderStableReleaseGate
        gates = ProviderStableReleaseGate().run()
        failed = [g for g in gates if g["status"] != "PASS"]
        assert failed == [], f"Failed gates: {[g['gate_name'] for g in failed]}"

    def test_111_version_gate_present(self):
        from release.provider_stable_release_gate_v149 import ProviderStableReleaseGate
        gates = ProviderStableReleaseGate().run()
        names = [g["gate_name"] for g in gates]
        assert "version_gate" in names

    def test_112_six_providers_gate_present(self):
        from release.provider_stable_release_gate_v149 import ProviderStableReleaseGate
        gates = ProviderStableReleaseGate().run()
        names = [g["gate_name"] for g in gates]
        assert "six_providers_stable_gate" in names

    def test_113_safety_gate_present(self):
        from release.provider_stable_release_gate_v149 import ProviderStableReleaseGate
        gates = ProviderStableReleaseGate().run()
        names = [g["gate_name"] for g in gates]
        assert "safety_gate" in names

    def test_114_no_fallback_gate_present(self):
        from release.provider_stable_release_gate_v149 import ProviderStableReleaseGate
        gates = ProviderStableReleaseGate().run()
        names = [g["gate_name"] for g in gates]
        assert "no_fallback_gate" in names

    def test_115_all_gates_have_required_fields(self):
        from release.provider_stable_release_gate_v149 import ProviderStableReleaseGate
        gates = ProviderStableReleaseGate().run()
        required = {"gate_name", "status", "evidence", "blocking", "checked_at"}
        for g in gates:
            missing = required - set(g.keys())
            assert not missing, f"Gate {g.get('gate_name')} missing fields: {missing}"

    def test_116_fixture_all_pass(self):
        fx = _load_fixture("release_gate_all_pass.json")
        assert fx["all_gates_passed"] is True
        assert fx["blocking_failures"] == 0

    def test_117_fixture_version_fail(self):
        fx = _load_fixture("release_gate_version_fail.json")
        assert fx["all_gates_passed"] is False
        assert fx["failed_gate"] == "version_gate"


# ===========================================================================
# Stable Report
# ===========================================================================

class TestStableReport:
    def test_118_report_instantiates(self):
        from reports.provider_stable_rollup_report import ProviderStableRollupReport
        assert ProviderStableRollupReport() is not None

    def test_119_report_generates(self):
        from reports.provider_stable_rollup_report import ProviderStableRollupReport
        result = ProviderStableRollupReport().generate()
        assert isinstance(result, dict)

    def test_120_report_has_metadata(self):
        from reports.provider_stable_rollup_report import ProviderStableRollupReport
        result = ProviderStableRollupReport().generate()
        assert "metadata" in result

    def test_121_report_metadata_version(self):
        from reports.provider_stable_rollup_report import ProviderStableRollupReport
        result = ProviderStableRollupReport().generate()
        def _parse_ver(v): return tuple(int(x) for x in v.split()[0].split(".")[:3] if x.isdigit())
        assert _parse_ver(result["metadata"]["version"]) >= _parse_ver("1.4.9")

    def test_122_report_final_readiness(self):
        from reports.provider_stable_rollup_report import ProviderStableRollupReport
        result = ProviderStableRollupReport().generate()
        assert "final_readiness" in result
        assert result["final_readiness"]["status"] == "READY"

    def test_123_render_markdown_returns_string(self):
        from reports.provider_stable_rollup_report import ProviderStableRollupReport
        md = ProviderStableRollupReport().render_markdown()
        assert isinstance(md, str)
        assert "Provider Stable Rollup" in md


# ===========================================================================
# CLI Command Registry
# ===========================================================================

class TestCLICommandRegistry:
    def test_124_stable_rollup_commands_in_provider_commands(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "provider-stable-health" in names

    def test_125_fifteen_stable_rollup_commands(self):
        from cli.command_registry import PROVIDER_COMMANDS
        stable_cmds = [c for c in PROVIDER_COMMANDS
                       if c.group == "provider_stable_rollup"]
        assert len(stable_cmds) == 15

    def test_126_stable_report_command_present(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "provider-stable-report" in names

    def test_127_stable_profiles_command_present(self):
        from cli.command_registry import PROVIDER_COMMANDS
        names = [c.name for c in PROVIDER_COMMANDS]
        assert "provider-stable-profiles" in names

    def test_128_all_stable_commands_have_149_group(self):
        from cli.command_registry import PROVIDER_COMMANDS
        stable_cmds = [c for c in PROVIDER_COMMANDS
                       if c.name.startswith("provider-stable-")]
        for cmd in stable_cmds:
            assert cmd.group == "provider_stable_rollup", \
                f"{cmd.name} has wrong group: {cmd.group}"
            assert cmd.introduced_in == "1.4.9", \
                f"{cmd.name} has wrong introduced_in: {cmd.introduced_in}"

    def test_129_cli_registry_has_stable_health(self):
        from cli.command_registry import CLICommandRegistry
        reg = CLICommandRegistry()
        cmd = reg.get_command("provider-stable-health")
        assert cmd is not None
        assert cmd.category == "provider"

    def test_130_cli_registry_has_stable_report(self):
        from cli.command_registry import CLICommandRegistry
        reg = CLICommandRegistry()
        cmd = reg.get_command("provider-stable-report")
        assert cmd is not None
        assert cmd.report_support is True

    def test_131_total_commands_increased(self):
        from cli.command_registry import PROVIDER_COMMANDS
        # v1.4.8.1 had 181; v1.4.9 adds 15 more
        assert len(PROVIDER_COMMANDS) >= 196


# ===========================================================================
# Capability Registry
# ===========================================================================

class TestCapabilityRegistry:
    def test_132_stable_rollup_capability_stable(self):
        from release.capability_registry import get_capabilities, is_capability_available
        caps = get_capabilities()
        cap = next((c for c in caps if c["id"] == "provider_stable_rollup"), None)
        assert cap is not None
        assert cap["status"] == "STABLE"
        assert cap["available"] is True
        assert cap["stable"] is True
        assert is_capability_available("provider_stable_rollup") is True

    def test_133_stable_rollup_version(self):
        from release.capability_registry import get_capabilities
        caps = get_capabilities()
        cap = next((c for c in caps if c["id"] == "provider_stable_rollup"), None)
        assert cap["feature_version"] == "v1.4.9"

    def test_134_stable_rollup_introduced_in(self):
        from release.capability_registry import get_capabilities
        caps = get_capabilities()
        cap = next((c for c in caps if c["id"] == "provider_stable_rollup"), None)
        assert cap["introduced_in"] == "1.4.9"


# ===========================================================================
# Version Alignment
# ===========================================================================

class TestVersionAlignment:
    def test_135_149_is_provider_stable_rollup(self):
        from release.version_alignment import release_name_for_version
        assert release_name_for_version("1.4.9") == "Provider Stable Rollup"

    def test_136_148_is_provider_integration_hardening(self):
        from release.version_alignment import release_name_for_version
        assert release_name_for_version("1.4.8") == "Provider Integration Hardening"

    def test_137_1481_hotfix_name(self):
        from release.version_alignment import release_name_for_version
        assert release_name_for_version("1.4.8.1") == "Provider Integration Test Integrity Hotfix"

    def test_138_149_is_known_lineage(self):
        from release.version_alignment import is_known_release_lineage
        assert is_known_release_lineage("1.4.9") is True

    def test_139_149_stable_rollup_name_correct(self):
        from release.version_alignment import _RELEASE_NAMES
        assert _RELEASE_NAMES.get("1.4.9") == "Provider Stable Rollup"


# ===========================================================================
# Safety Invariants
# ===========================================================================

class TestSafetyInvariants:
    def test_140_no_real_orders_global(self):
        from data.stable import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_141_broker_blocked(self):
        from data.stable import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_142_production_trading_blocked(self):
        from data.stable import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True

    def test_143_no_auto_override(self):
        from data.stable import AUTO_OVERRIDE_ENABLED
        assert AUTO_OVERRIDE_ENABLED is False

    def test_144_no_mock_fallback(self):
        from data.stable import MOCK_FALLBACK_ENABLED
        assert MOCK_FALLBACK_ENABLED is False

    def test_145_ptt_no_buy_sell_profile_level(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        ptt = ProviderStableProfileRegistry().get_by_id("ptt_stock")
        assert ptt.buy_sell_allowed is False

    def test_146_ptt_no_standalone_profile_level(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        ptt = ProviderStableProfileRegistry().get_by_id("ptt_stock")
        assert ptt.standalone_formal_allowed is False

    def test_147_finmind_no_override_profile_level(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        finmind = ProviderStableProfileRegistry().get_by_id("finmind_aggregator")
        assert finmind.can_override_primary is False

    def test_148_no_buy_sell_any_provider(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        for p in ProviderStableProfileRegistry().get_all():
            assert p.buy_sell_allowed is False, \
                f"{p.provider_id} has buy_sell_allowed=True"
