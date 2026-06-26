"""
release/provider_stable_health_v149.py — Provider Stable Rollup health check v1.4.9.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Dict, Tuple


class ProviderStableRollupHealthCheck:
    """
    Health check for Provider Stable Rollup v1.4.9.
    Covers: Version, Stable Manifest, Provider Registry, Compatibility,
            Schemas, Policies, Baseline, Collection Integrity, Safety.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def run(self) -> Dict[str, Tuple[str, str]]:
        checks: Dict[str, Tuple[str, str]] = {}
        self._check_version(checks)
        self._check_stable_manifest(checks)
        self._check_provider_registry(checks)
        self._check_compatibility_contracts(checks)
        self._check_schema_registry(checks)
        self._check_policy_registry(checks)
        self._check_baseline_snapshot(checks)
        self._check_test_manifest(checks)
        self._check_collection_integrity(checks)
        self._check_provider_stable_profiles(checks)
        self._check_provider_integration_baseline(checks)
        self._check_safety(checks)
        return checks

    def _check_version(self, checks: dict) -> None:
        try:
            from release.version_info import VERSION
            parts = tuple(int(x) for x in VERSION.split(".")[:3])
            ok = parts >= (1, 4, 9)
            checks["version_is_149"] = ("PASS" if ok else "FAIL", f"VERSION={VERSION}")
        except Exception as exc:
            checks["version_is_149"] = ("FAIL", str(exc))

        try:
            from release.version_info import RELEASE_NAME
            _KNOWN_NAMES = {"Provider Stable Rollup", "Portfolio Research Foundation",
                            "Portfolio Research Foundation Integrity Hotfix",
                            "Portfolio Research CLI Completeness Hotfix",
                            "Position Sizing", "Correlation & Exposure",
                            "Correlation & Exposure Integrity Hotfix",
                            "Drawdown & Risk Controls", "Portfolio Walk-forward Backtest",
                            "Portfolio Stable Rollup",
                            "Portfolio Stable Rollup Integrity Hotfix",
                            "Portfolio Stable Rollup Release Gate Hotfix",
                            "Live Paper Trading Foundation",
                             "Market Data Session Adapter",
                             "Market Data Session Warning Hygiene Hotfix",
                             "Paper Strategy Orchestration",
                             "Paper Strategy Orchestration Integrity Hotfix",
                             "Session Operations & Observability"}
            ok = RELEASE_NAME in _KNOWN_NAMES
            checks["release_name_correct"] = ("PASS" if ok else "FAIL",
                                               f"RELEASE_NAME={RELEASE_NAME}")
        except Exception as exc:
            checks["release_name_correct"] = ("FAIL", str(exc))

        try:
            from release.version_info import BASE_RELEASE
            def _parse_ver(v): return tuple(int(x) for x in v.split()[0].split(".")[:3] if x.isdigit())
            ok = _parse_ver(BASE_RELEASE) >= _parse_ver("1.4.8")
            checks["base_release_correct"] = ("PASS" if ok else "FAIL",
                                               f"BASE_RELEASE={BASE_RELEASE}")
        except Exception as exc:
            checks["base_release_correct"] = ("FAIL", str(exc))

        try:
            from release.version_info import REPLAY_STABLE_BASELINE
            ok = REPLAY_STABLE_BASELINE == "1.2.9"
            checks["replay_baseline_correct"] = ("PASS" if ok else "FAIL",
                                                  f"REPLAY_STABLE_BASELINE={REPLAY_STABLE_BASELINE}")
        except Exception as exc:
            checks["replay_baseline_correct"] = ("FAIL", str(exc))

        try:
            from release.version_info import PROVIDER_STABLE_BASELINE
            ok = PROVIDER_STABLE_BASELINE == "1.4.9"
            checks["provider_stable_baseline_correct"] = (
                "PASS" if ok else "FAIL",
                f"PROVIDER_STABLE_BASELINE={PROVIDER_STABLE_BASELINE}"
            )
        except Exception as exc:
            checks["provider_stable_baseline_correct"] = ("FAIL", str(exc))

    def _check_stable_manifest(self, checks: dict) -> None:
        try:
            from data.stable.capability_manifest_v149 import StableCapabilityManifest
            result = StableCapabilityManifest().validate()
            ok = result["valid"] and result["stable_count"] >= 20
            checks["stable_manifest_valid"] = (
                "PASS" if ok else "FAIL",
                f"stable={result['stable_count']} non_stable={result['non_stable']}"
            )
        except Exception as exc:
            checks["stable_manifest_valid"] = ("FAIL", str(exc))

    def _check_provider_registry(self, checks: dict) -> None:
        try:
            from data.stable.provider_registry_v149 import StableProviderRegistry
            result = StableProviderRegistry().validate()
            ok = result["valid"]
            checks["provider_registry_valid"] = (
                "PASS" if ok else "FAIL",
                f"providers={result['total_providers']} primary={result['primary_official']}"
            )
        except Exception as exc:
            checks["provider_registry_valid"] = ("FAIL", str(exc))

    def _check_compatibility_contracts(self, checks: dict) -> None:
        try:
            from data.stable.compatibility_contract_v149 import CompatibilityContractRegistry
            result = CompatibilityContractRegistry().validate()
            ok = result["valid"]
            checks["compatibility_contracts_valid"] = (
                "PASS" if ok else "FAIL",
                f"contracts={result['total_contracts']} breaking={result['breaking_changes_allowed']}"
            )
        except Exception as exc:
            checks["compatibility_contracts_valid"] = ("FAIL", str(exc))

    def _check_schema_registry(self, checks: dict) -> None:
        try:
            from data.stable.schema_version_registry_v149 import SchemaVersionRegistry
            result = SchemaVersionRegistry().validate()
            ok = result["valid"]
            checks["schema_registry_valid"] = (
                "PASS" if ok else "FAIL",
                f"schemas={result['total_schemas']} drift={result['drift_detected']}"
            )
        except Exception as exc:
            checks["schema_registry_valid"] = ("FAIL", str(exc))

    def _check_policy_registry(self, checks: dict) -> None:
        try:
            from data.stable.policy_version_registry_v149 import PolicyVersionRegistry
            result = PolicyVersionRegistry().validate()
            ok = result["valid"]
            checks["policy_registry_valid"] = (
                "PASS" if ok else "FAIL",
                f"policies={result['total_policies']} breaking={result['breaking_changes']}"
            )
        except Exception as exc:
            checks["policy_registry_valid"] = ("FAIL", str(exc))

    def _check_baseline_snapshot(self, checks: dict) -> None:
        try:
            from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
            snap = StableBaselineSnapshot().get()
            ok = snap["full_collection_baseline"] >= 3597 and snap["full_fail_baseline"] == 0
            checks["baseline_snapshot_valid"] = (
                "PASS" if ok else "FAIL",
                f"collection={snap['full_collection_baseline']} fail={snap['full_fail_baseline']}"
            )
        except Exception as exc:
            checks["baseline_snapshot_valid"] = ("FAIL", str(exc))

    def _check_test_manifest(self, checks: dict) -> None:
        try:
            from data.stable.test_manifest_v149 import ProviderTestManifest
            result = ProviderTestManifest().validate()
            ok = result["valid"]
            checks["test_manifest_valid"] = (
                "PASS" if ok else "FAIL",
                f"issues={result['issues']}"
            )
        except Exception as exc:
            checks["test_manifest_valid"] = ("FAIL", str(exc))

    def _check_collection_integrity(self, checks: dict) -> None:
        try:
            from data.stable.collection_integrity_v149 import StableCollectionIntegrityCheck
            result = StableCollectionIntegrityCheck().get_summary()
            ok = result["valid"]
            checks["collection_integrity_valid"] = (
                "PASS" if ok else "FAIL",
                f"passed={result['passed']}/{result['total']}"
            )
        except Exception as exc:
            checks["collection_integrity_valid"] = ("FAIL", str(exc))

    def _check_provider_stable_profiles(self, checks: dict) -> None:
        try:
            from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
            result = ProviderStableProfileRegistry().validate()
            ok = result["valid"]
            checks["provider_stable_profiles_valid"] = (
                "PASS" if ok else "FAIL",
                f"profiles={result['total_profiles']} non_stable={result['non_stable']}"
            )
        except Exception as exc:
            checks["provider_stable_profiles_valid"] = ("FAIL", str(exc))

    def _check_provider_integration_baseline(self, checks: dict) -> None:
        try:
            from data.integration.health_v148 import ProviderIntegrationHardeningHealthCheck
            summary = ProviderIntegrationHardeningHealthCheck().get_health_summary()
            failures = [item for item in summary.get("items", []) if item[1] == "FAIL"]
            ok = len(failures) == 0
            checks["provider_integration_baseline"] = (
                "PASS" if ok else "FAIL",
                f"v1.4.8 integration health failures={len(failures)}"
            )
        except Exception as exc:
            checks["provider_integration_baseline"] = ("FAIL", str(exc))

    def _check_safety(self, checks: dict) -> None:
        try:
            from data.stable import (
                NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
                AUTO_FALLBACK_ENABLED, MOCK_FALLBACK_ENABLED,
                FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER,
                PTT_STANDALONE_FORMAL_CONCLUSION, PTT_CAN_GENERATE_BUY_SELL,
            )
            ok = (
                NO_REAL_ORDERS
                and not BROKER_EXECUTION_ENABLED
                and PRODUCTION_TRADING_BLOCKED
                and not AUTO_FALLBACK_ENABLED
                and not MOCK_FALLBACK_ENABLED
                and not FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER
                and not PTT_STANDALONE_FORMAL_CONCLUSION
                and not PTT_CAN_GENERATE_BUY_SELL
            )
            checks["safety_invariants"] = (
                "PASS" if ok else "FAIL",
                f"NO_REAL_ORDERS={NO_REAL_ORDERS} BROKER={BROKER_EXECUTION_ENABLED} "
                f"PROD_BLOCKED={PRODUCTION_TRADING_BLOCKED}"
            )
        except Exception as exc:
            checks["safety_invariants"] = ("FAIL", str(exc))
