"""
release/provider_stable_release_gate_v149.py — Provider Stable Rollup release gate v1.4.9.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List


def _gate(name: str, status: str, evidence: str, blocking: bool,
          warnings: list, remediation: str) -> dict:
    return {
        "gate_name":   name,
        "status":      status,
        "evidence":    evidence,
        "blocking":    blocking,
        "warnings":    warnings,
        "remediation": remediation,
        "checked_at":  datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
    }


class ProviderStableReleaseGate:
    """
    Release gate for Provider Stable Rollup v1.4.9.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    def run(self) -> List[Dict[str, Any]]:
        gates = []
        gates.append(self._version_gate())
        gates.append(self._stable_manifest_gate())
        gates.append(self._provider_registry_gate())
        gates.append(self._compatibility_contract_gate())
        gates.append(self._schema_registry_gate())
        gates.append(self._policy_registry_gate())
        gates.append(self._baseline_snapshot_gate())
        gates.append(self._test_manifest_gate())
        gates.append(self._collection_integrity_gate())
        gates.append(self._provider_stable_profiles_gate())
        gates.append(self._provider_integration_baseline_gate())
        gates.append(self._six_providers_stable_gate())
        gates.append(self._safety_gate())
        gates.append(self._no_authority_drift_gate())
        gates.append(self._no_fallback_gate())
        return gates

    def _version_gate(self) -> dict:
        try:
            from release.version_info import (VERSION, RELEASE_NAME, BASE_RELEASE,
                                               REPLAY_STABLE_BASELINE, PROVIDER_STABLE_BASELINE)
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
            parts = tuple(int(x) for x in VERSION.split(".")[:3])
            ok = (
                parts >= (1, 4, 9)
                and RELEASE_NAME in _KNOWN_NAMES
                and (lambda v: tuple(int(x) for x in v.split()[0].split(".")[:3] if x.isdigit()))(BASE_RELEASE) >= (1, 4, 8)
                and REPLAY_STABLE_BASELINE == "1.2.9"
                and PROVIDER_STABLE_BASELINE == "1.4.9"
            )
            evidence = (f"VERSION={VERSION}, RELEASE_NAME={RELEASE_NAME}, "
                        f"BASE_RELEASE={BASE_RELEASE}")
            return _gate("version_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, [], "" if ok else "Update VERSION to 1.4.9")
        except Exception as exc:
            return _gate("version_gate", "FAIL", str(exc), True, [],
                         "Fix version_info import")

    def _stable_manifest_gate(self) -> dict:
        try:
            from data.stable.capability_manifest_v149 import StableCapabilityManifest
            result = StableCapabilityManifest().validate()
            ok = result["valid"]
            evidence = f"stable={result['stable_count']} total={result['total_capabilities']}"
            return _gate("stable_manifest_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, result["non_stable"],
                         "" if ok else "All capabilities must be STABLE")
        except Exception as exc:
            return _gate("stable_manifest_gate", "FAIL", str(exc), True, [],
                         "Fix StableCapabilityManifest import")

    def _provider_registry_gate(self) -> dict:
        try:
            from data.stable.provider_registry_v149 import StableProviderRegistry
            result = StableProviderRegistry().validate()
            ok = result["valid"]
            evidence = (f"providers={result['total_providers']} "
                        f"primary={result['primary_official']}")
            return _gate("provider_registry_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, [], "" if ok else "Fix provider registry")
        except Exception as exc:
            return _gate("provider_registry_gate", "FAIL", str(exc), True, [],
                         "Fix StableProviderRegistry import")

    def _compatibility_contract_gate(self) -> dict:
        try:
            from data.stable.compatibility_contract_v149 import CompatibilityContractRegistry
            result = CompatibilityContractRegistry().validate()
            ok = result["valid"]
            evidence = f"contracts={result['total_contracts']}"
            return _gate("compatibility_contract_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, result["breaking_changes_allowed"],
                         "" if ok else "No breaking changes allowed in stable contracts")
        except Exception as exc:
            return _gate("compatibility_contract_gate", "FAIL", str(exc), True, [],
                         "Fix CompatibilityContractRegistry import")

    def _schema_registry_gate(self) -> dict:
        try:
            from data.stable.schema_version_registry_v149 import SchemaVersionRegistry
            result = SchemaVersionRegistry().validate()
            ok = result["valid"]
            evidence = f"schemas={result['total_schemas']} drift={result['drift_detected']}"
            return _gate("schema_registry_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, result["drift_detected"],
                         "" if ok else "No schema drift allowed in stable rollup")
        except Exception as exc:
            return _gate("schema_registry_gate", "FAIL", str(exc), True, [],
                         "Fix SchemaVersionRegistry import")

    def _policy_registry_gate(self) -> dict:
        try:
            from data.stable.policy_version_registry_v149 import PolicyVersionRegistry
            result = PolicyVersionRegistry().validate()
            ok = result["valid"]
            evidence = f"policies={result['total_policies']}"
            return _gate("policy_registry_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, result["breaking_changes"],
                         "" if ok else "No policy breaking changes in stable rollup")
        except Exception as exc:
            return _gate("policy_registry_gate", "FAIL", str(exc), True, [],
                         "Fix PolicyVersionRegistry import")

    def _baseline_snapshot_gate(self) -> dict:
        try:
            from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
            snap = StableBaselineSnapshot().get()
            ok = (snap["full_collection_baseline"] >= 3597
                  and snap["full_fail_baseline"] == 0
                  and snap["full_skip_baseline"] == 0)
            evidence = (f"collection={snap['full_collection_baseline']} "
                        f"fail={snap['full_fail_baseline']} "
                        f"skip={snap['full_skip_baseline']}")
            return _gate("baseline_snapshot_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, [], "" if ok else "Baseline snapshot must match v1.4.8.1")
        except Exception as exc:
            return _gate("baseline_snapshot_gate", "FAIL", str(exc), True, [],
                         "Fix StableBaselineSnapshot import")

    def _test_manifest_gate(self) -> dict:
        try:
            from data.stable.test_manifest_v149 import ProviderTestManifest
            result = ProviderTestManifest().validate()
            ok = result["valid"]
            evidence = f"issues={result['issues']}"
            return _gate("test_manifest_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, result["issues"],
                         "" if ok else "All required test files must exist")
        except Exception as exc:
            return _gate("test_manifest_gate", "FAIL", str(exc), True, [],
                         "Fix ProviderTestManifest import")

    def _collection_integrity_gate(self) -> dict:
        try:
            from data.stable.collection_integrity_v149 import StableCollectionIntegrityCheck
            result = StableCollectionIntegrityCheck().get_summary()
            ok = result["valid"]
            evidence = f"passed={result['passed']}/{result['total']}"
            return _gate("collection_integrity_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, [], "" if ok else "All collection integrity checks must pass")
        except Exception as exc:
            return _gate("collection_integrity_gate", "FAIL", str(exc), True, [],
                         "Fix StableCollectionIntegrityCheck import")

    def _provider_stable_profiles_gate(self) -> dict:
        try:
            from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
            result = ProviderStableProfileRegistry().validate()
            ok = result["valid"]
            evidence = (f"profiles={result['total_profiles']} "
                        f"ptt_ok={result['ptt_constraints_enforced']} "
                        f"finmind_ok={result['finmind_constraints_enforced']}")
            return _gate("provider_stable_profiles_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, result["non_stable"],
                         "" if ok else "All six provider profiles must be STABLE")
        except Exception as exc:
            return _gate("provider_stable_profiles_gate", "FAIL", str(exc), True, [],
                         "Fix ProviderStableProfileRegistry import")

    def _provider_integration_baseline_gate(self) -> dict:
        try:
            from data.integration.health_v148 import ProviderIntegrationHardeningHealthCheck
            summary = ProviderIntegrationHardeningHealthCheck().get_health_summary()
            failures = [item for item in summary.get("items", []) if item[1] == "FAIL"]
            ok = len(failures) == 0
            evidence = f"v1.4.8 integration health failures={len(failures)}"
            return _gate("provider_integration_baseline_gate", "PASS" if ok else "FAIL",
                         evidence, not ok, [],
                         "" if ok else "v1.4.8 Provider Integration baseline must be PASS")
        except Exception as exc:
            return _gate("provider_integration_baseline_gate", "FAIL", str(exc), True, [],
                         "Fix ProviderIntegrationHardeningHealthCheck import")

    def _six_providers_stable_gate(self) -> dict:
        try:
            from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
            reg = ProviderStableProfileRegistry()
            profiles = reg.get_all()
            non_stable = [p.provider_id for p in profiles if p.stability_status != "STABLE"]
            ok = len(profiles) == 6 and not non_stable
            evidence = f"providers={len(profiles)} non_stable={non_stable}"
            return _gate("six_providers_stable_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, non_stable,
                         "" if ok else "All six providers must reach STABLE status")
        except Exception as exc:
            return _gate("six_providers_stable_gate", "FAIL", str(exc), True, [],
                         "Fix provider profiles")

    def _safety_gate(self) -> dict:
        try:
            from data.stable import (
                NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
                AUTO_FALLBACK_ENABLED, MOCK_FALLBACK_ENABLED,
            )
            ok = (NO_REAL_ORDERS and not BROKER_EXECUTION_ENABLED
                  and PRODUCTION_TRADING_BLOCKED
                  and not AUTO_FALLBACK_ENABLED and not MOCK_FALLBACK_ENABLED)
            evidence = (f"NO_REAL_ORDERS={NO_REAL_ORDERS} "
                        f"BROKER={BROKER_EXECUTION_ENABLED} "
                        f"PROD_BLOCKED={PRODUCTION_TRADING_BLOCKED}")
            return _gate("safety_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, [], "" if ok else "Fix safety invariants")
        except Exception as exc:
            return _gate("safety_gate", "FAIL", str(exc), True, [],
                         "Fix data.stable safety flags")

    def _no_authority_drift_gate(self) -> dict:
        try:
            from data.integration.health_v148 import ProviderIntegrationHardeningHealthCheck
            summary = ProviderIntegrationHardeningHealthCheck().get_health_summary()
            drift_item = next(
                (item for item in summary.get("items", [])
                 if "authority_drift" in item[0]), None
            )
            ok = drift_item is None or drift_item[1] == "PASS"
            evidence = f"authority_drift={'none' if ok else 'DETECTED'}"
            return _gate("no_authority_drift_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, [], "" if ok else "No authority drift tolerated")
        except Exception as exc:
            return _gate("no_authority_drift_gate", "FAIL", str(exc), True, [],
                         "Fix authority drift check")

    def _no_fallback_gate(self) -> dict:
        try:
            from data.stable import AUTO_FALLBACK_ENABLED, AUTO_OVERRIDE_ENABLED
            ok = not AUTO_FALLBACK_ENABLED and not AUTO_OVERRIDE_ENABLED
            evidence = (f"AUTO_FALLBACK={AUTO_FALLBACK_ENABLED} "
                        f"AUTO_OVERRIDE={AUTO_OVERRIDE_ENABLED}")
            return _gate("no_fallback_gate", "PASS" if ok else "FAIL", evidence,
                         not ok, [], "" if ok else "Auto fallback and override must be disabled")
        except Exception as exc:
            return _gate("no_fallback_gate", "FAIL", str(exc), True, [],
                         "Fix fallback flags")
