"""
reports/provider_stable_rollup_report.py — Provider Stable Rollup Report v1.4.9.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Runtime report — do not commit generated output.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict


class ProviderStableRollupReport:
    """
    Generates the Provider Stable Rollup report for v1.4.9.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    VERSION = "1.4.9"

    def generate(self) -> Dict[str, Any]:
        return {
            "metadata": self._metadata(),
            "stable_manifest": self._stable_manifest_section(),
            "provider_registry": self._provider_registry_section(),
            "compatibility_contracts": self._compatibility_section(),
            "schema_registry": self._schema_section(),
            "policy_registry": self._policy_section(),
            "baseline_snapshot": self._baseline_section(),
            "test_manifest": self._test_manifest_section(),
            "collection_integrity": self._collection_integrity_section(),
            "provider_stable_profiles": self._profiles_section(),
            "health_summary": self._health_summary_section(),
            "release_gate_summary": self._release_gate_section(),
            "safety_declaration": self._safety_section(),
            "final_readiness": self._final_readiness_section(),
        }

    def render_markdown(self) -> str:
        data = self.generate()
        meta = data["metadata"]
        lines = [
            f"# Provider Stable Rollup Report — v{meta['version']}",
            "",
            f"> Generated: {meta['generated_at']}",
            f"> Base: {meta['base_release']}",
            "",
            "---",
            "",
            "## Safety Declaration",
            "",
            "**[!] Research Only. No Real Orders. Production Trading: BLOCKED.**",
            "",
            "---",
            "",
            "## Stable Capability Manifest",
            "",
        ]
        manifest = data["stable_manifest"]
        lines.append(f"- Total capabilities: {manifest.get('total_capabilities', 'N/A')}")
        lines.append(f"- Stable: {manifest.get('stable_count', 'N/A')}")
        lines.append(f"- Valid: {manifest.get('valid', 'N/A')}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Provider Registry")
        lines.append("")
        registry = data["provider_registry"]
        lines.append(f"- Total providers: {registry.get('total_providers', 'N/A')}")
        lines.append(f"- Primary Official: {registry.get('primary_official', 'N/A')}")
        lines.append(f"- Secondary Aggregator: {registry.get('secondary_aggregator', 'N/A')}")
        lines.append(f"- Supplementary: {registry.get('supplementary', 'N/A')}")
        lines.append(f"- FinMind override blocked: {registry.get('finmind_override_blocked', True)}")
        lines.append(f"- PTT standalone blocked: {registry.get('ptt_standalone_blocked', True)}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Provider Stable Profiles")
        lines.append("")
        profiles = data["provider_stable_profiles"]
        for item in profiles.get("items", []):
            lines.append(f"- {item[0]}: **{item[1]}** — {item[2]}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Health Summary")
        lines.append("")
        health = data["health_summary"]
        lines.append(f"- Checks: {health.get('passed', 'N/A')}/{health.get('total', 'N/A')} PASS")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Release Gate Summary")
        lines.append("")
        gate = data["release_gate_summary"]
        lines.append(f"- Gates: {gate.get('passed', 'N/A')}/{gate.get('total', 'N/A')} PASS")
        lines.append(f"- Blocking failures: {gate.get('blocking_failures', 0)}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Final Readiness")
        lines.append("")
        readiness = data["final_readiness"]
        lines.append(f"- Status: **{readiness.get('status', 'UNKNOWN')}**")
        lines.append(f"- All gates passed: {readiness.get('all_gates_passed', False)}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*Runtime report — do not commit.*")
        return "\n".join(lines)

    def _metadata(self) -> Dict[str, Any]:
        try:
            from release.version_info import VERSION, RELEASE_NAME, BASE_RELEASE
        except Exception:
            VERSION, RELEASE_NAME, BASE_RELEASE = "1.4.9", "Provider Stable Rollup", "unknown"
        return {
            "version":      VERSION,
            "release_name": RELEASE_NAME,
            "base_release": BASE_RELEASE,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
            "report_type":  "provider_stable_rollup",
        }

    def _stable_manifest_section(self) -> Dict[str, Any]:
        try:
            from data.stable.capability_manifest_v149 import StableCapabilityManifest
            return StableCapabilityManifest().validate()
        except Exception as exc:
            return {"error": str(exc), "valid": False}

    def _provider_registry_section(self) -> Dict[str, Any]:
        try:
            from data.stable.provider_registry_v149 import StableProviderRegistry
            return StableProviderRegistry().validate()
        except Exception as exc:
            return {"error": str(exc), "valid": False}

    def _compatibility_section(self) -> Dict[str, Any]:
        try:
            from data.stable.compatibility_contract_v149 import CompatibilityContractRegistry
            return CompatibilityContractRegistry().validate()
        except Exception as exc:
            return {"error": str(exc), "valid": False}

    def _schema_section(self) -> Dict[str, Any]:
        try:
            from data.stable.schema_version_registry_v149 import SchemaVersionRegistry
            return SchemaVersionRegistry().validate()
        except Exception as exc:
            return {"error": str(exc), "valid": False}

    def _policy_section(self) -> Dict[str, Any]:
        try:
            from data.stable.policy_version_registry_v149 import PolicyVersionRegistry
            return PolicyVersionRegistry().validate()
        except Exception as exc:
            return {"error": str(exc), "valid": False}

    def _baseline_section(self) -> Dict[str, Any]:
        try:
            from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
            return StableBaselineSnapshot().get_summary()
        except Exception as exc:
            return {"error": str(exc), "valid": False}

    def _test_manifest_section(self) -> Dict[str, Any]:
        try:
            from data.stable.test_manifest_v149 import ProviderTestManifest
            return ProviderTestManifest().validate()
        except Exception as exc:
            return {"error": str(exc), "valid": False}

    def _collection_integrity_section(self) -> Dict[str, Any]:
        try:
            from data.stable.collection_integrity_v149 import StableCollectionIntegrityCheck
            return StableCollectionIntegrityCheck().get_summary()
        except Exception as exc:
            return {"error": str(exc), "valid": False}

    def _profiles_section(self) -> Dict[str, Any]:
        try:
            from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
            return ProviderStableProfileRegistry().get_summary()
        except Exception as exc:
            return {"error": str(exc), "valid": False}

    def _health_summary_section(self) -> Dict[str, Any]:
        try:
            from release.provider_stable_health_v149 import ProviderStableRollupHealthCheck
            checks = ProviderStableRollupHealthCheck().run()
            passed = sum(1 for v in checks.values() if v[0] == "PASS")
            total = len(checks)
            return {"passed": passed, "total": total, "failed": total - passed}
        except Exception as exc:
            return {"error": str(exc), "passed": 0, "total": 0}

    def _release_gate_section(self) -> Dict[str, Any]:
        try:
            from release.provider_stable_release_gate_v149 import ProviderStableReleaseGate
            gates = ProviderStableReleaseGate().run()
            passed = sum(1 for g in gates if g["status"] == "PASS")
            blocking = sum(1 for g in gates if g["status"] == "FAIL" and g["blocking"])
            return {
                "total": len(gates),
                "passed": passed,
                "failed": len(gates) - passed,
                "blocking_failures": blocking,
            }
        except Exception as exc:
            return {"error": str(exc), "passed": 0, "total": 0, "blocking_failures": 1}

    def _safety_section(self) -> Dict[str, Any]:
        try:
            from data.stable import (
                NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED,
                PRODUCTION_TRADING_BLOCKED, AUTO_FALLBACK_ENABLED,
            )
            return {
                "no_real_orders":             NO_REAL_ORDERS,
                "broker_execution_enabled":   BROKER_EXECUTION_ENABLED,
                "production_trading_blocked": PRODUCTION_TRADING_BLOCKED,
                "auto_fallback_enabled":      AUTO_FALLBACK_ENABLED,
            }
        except Exception as exc:
            return {"error": str(exc)}

    def _final_readiness_section(self) -> Dict[str, Any]:
        gate_summary = self._release_gate_section()
        health_summary = self._health_summary_section()
        all_gates = gate_summary.get("blocking_failures", 1) == 0
        all_health = health_summary.get("failed", 1) == 0
        status = "READY" if (all_gates and all_health) else "NOT_READY"
        return {
            "status":           status,
            "all_gates_passed": all_gates,
            "all_health_pass":  all_health,
        }
