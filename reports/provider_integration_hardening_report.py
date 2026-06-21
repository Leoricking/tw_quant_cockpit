"""
reports/provider_integration_hardening_report.py — Provider Integration Hardening Report v1.4.8.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Runtime report must not be committed.
"""
from __future__ import annotations

import datetime
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

_VERSION = "1.4.8"
_RELEASE = "Provider Integration Hardening"


class ProviderIntegrationHardeningReport:
    """Builds the Provider Integration Hardening Report."""

    VERSION = _VERSION

    def build_contracts_section(self) -> Dict[str, Any]:
        from data.integration.provider_contract_v148 import ProviderContractValidator
        summary = ProviderContractValidator().get_summary()
        return {
            "title": "Provider Contracts",
            "providers": summary.get("providers", []),
            "total": summary.get("total", 0),
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
        }

    def build_e2e_section(self) -> Dict[str, Any]:
        from data.integration.cross_provider_e2e_v148 import CrossProviderE2EValidator
        summary = CrossProviderE2EValidator().get_summary()
        return {
            "title": "Cross-Provider E2E Scenarios",
            "scenarios": summary.get("scenarios", []),
            "total": summary.get("total", 0),
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
        }

    def build_pit_section(self) -> Dict[str, Any]:
        from data.integration.cross_provider_pit_v148 import CrossProviderPITValidator
        summary = CrossProviderPITValidator().get_summary()
        return {
            "title": "PIT Hardening",
            "future_leakage_blocking": summary.get("future_leakage_blocking", True),
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
        }

    def build_lineage_section(self) -> Dict[str, Any]:
        from data.integration.cross_provider_lineage_v148 import CrossProviderLineageValidator
        summary = CrossProviderLineageValidator().get_summary()
        return {
            "title": "Lineage Hardening",
            "orphan_blocking": summary.get("orphan_records_blocking", True),
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
        }

    def build_conflict_section(self) -> Dict[str, Any]:
        from data.integration.cross_provider_conflict_v148 import CrossProviderConflictValidator
        summary = CrossProviderConflictValidator().get_summary()
        return {
            "title": "Conflict Hardening",
            "conflict_pairs_covered": summary.get("conflict_pairs_covered", 0),
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
        }

    def build_migration_section(self) -> Dict[str, Any]:
        from data.integration.storage_migration_v148 import StorageMigrationHardeningService
        summary = StorageMigrationHardeningService().get_summary()
        return {
            "title": "Storage/Migration",
            "migrations": summary.get("migrations", []),
            "total": summary.get("total", 0),
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
        }

    def build_recovery_section(self) -> Dict[str, Any]:
        from data.integration.partial_failure_v148 import PartialFailureRecoveryService
        from data.integration.lock_recovery_v148 import LockRecoveryService
        from data.integration.rate_limit_recovery_v148 import RateLimitRecoveryService
        from data.integration.runtime_recovery_v148 import RuntimeCorruptionRecoveryService
        return {
            "title": "Recovery",
            "partial_failure": PartialFailureRecoveryService().get_summary(),
            "lock_recovery":   LockRecoveryService().get_summary(),
            "rate_recovery":   RateLimitRecoveryService().get_summary(),
            "corruption":      RuntimeCorruptionRecoveryService().get_summary(),
        }

    def build_cli_gui_section(self) -> Dict[str, Any]:
        from data.integration.cli_gui_consistency_v148 import CliGuiConsistencyValidator
        summary = CliGuiConsistencyValidator().get_summary()
        return {
            "title": "CLI/GUI Consistency",
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
        }

    def build_performance_section(self) -> Dict[str, Any]:
        from data.integration.performance_budget_v148 import PerformanceBudgetService
        summary = PerformanceBudgetService().get_summary()
        return {
            "title": "Performance/Memory",
            "operations": summary.get("operations", []),
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
        }

    def build_memory_section(self) -> Dict[str, Any]:
        from data.integration.memory_budget_v148 import MemoryBudgetService
        summary = MemoryBudgetService().get_summary()
        return {
            "title": "Memory",
            "operations": summary.get("operations", []),
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
        }

    def build_collection_section(self) -> Dict[str, Any]:
        from data.integration.collection_integrity_v148 import (
            ProviderIntegrationCollectionIntegrityCheck, BASELINE_COLLECTION_COUNT
        )
        summary = ProviderIntegrationCollectionIntegrityCheck().get_summary()
        return {
            "title": "Collection Integrity",
            "baseline": BASELINE_COLLECTION_COUNT,
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
        }

    def build_safety_section(self) -> Dict[str, Any]:
        from data.integration import (
            NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED,
            PRODUCTION_TRADING_BLOCKED,
            PROVIDER_INTEGRATION_AUTO_FALLBACK_ENABLED,
            PROVIDER_INTEGRATION_AUTO_OVERRIDE_ENABLED,
            PROVIDER_INTEGRATION_AUTO_REPAIR_ENABLED,
        )
        return {
            "title": "Safety",
            "authority_preserved":  True,
            "no_fallback":          not PROVIDER_INTEGRATION_AUTO_FALLBACK_ENABLED,
            "no_override":          not PROVIDER_INTEGRATION_AUTO_OVERRIDE_ENABLED,
            "no_auto_repair":       not PROVIDER_INTEGRATION_AUTO_REPAIR_ENABLED,
            "no_broker":            not BROKER_EXECUTION_ENABLED,
            "no_real_orders":       NO_REAL_ORDERS,
            "production_blocked":   PRODUCTION_TRADING_BLOCKED,
        }

    def build_full_report(self) -> Dict[str, Any]:
        from data.integration.health_v148 import ProviderIntegrationHardeningHealthCheck
        health = ProviderIntegrationHardeningHealthCheck().get_health_summary()
        return {
            "title": "Provider Integration Hardening Report v1.4.8",
            "overview": {
                "version":     _VERSION,
                "release":     _RELEASE,
                "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
                "overall":     health.get("overall"),
            },
            "contracts":    self.build_contracts_section(),
            "e2e":          self.build_e2e_section(),
            "pit":          self.build_pit_section(),
            "lineage":      self.build_lineage_section(),
            "conflict":     self.build_conflict_section(),
            "migration":    self.build_migration_section(),
            "recovery":     self.build_recovery_section(),
            "cli_gui":      self.build_cli_gui_section(),
            "performance":  self.build_performance_section(),
            "memory":       self.build_memory_section(),
            "collection":   self.build_collection_section(),
            "safety":       self.build_safety_section(),
        }

    def render_markdown(self) -> str:
        data = self.build_full_report()
        ov = data["overview"]
        lines = [
            f"# Provider Integration Hardening Report v{ov['version']}",
            f"",
            f"**Release:** {ov['release']}  ",
            f"**Generated:** {ov['generated_at']}  ",
            f"**Overall:** {ov['overall']}",
            f"",
            f"## Safety",
            f"",
        ]
        safety = data["safety"]
        for k, v in safety.items():
            if k != "title":
                lines.append(f"- {k}: {v}")
        lines.append("")
        lines.append("*Runtime report — do not commit.*")
        return "\n".join(lines)
