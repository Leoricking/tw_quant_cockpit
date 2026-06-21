"""
data/integration/query_v148.py — Integration Query Service v1.4.8.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Read-only queries. No auto repair. No fetch trigger.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class IntegrationQueryService:
    """Read-only query service for provider integration status."""

    VERSION = "1.4.8"
    READ_ONLY = True
    AUTO_FETCH_ENABLED = False
    AUTO_REPAIR_ENABLED = False

    def query_provider_status(self, provider_id: Optional[str] = None) -> Dict[str, Any]:
        from .provider_contract_v148 import ProviderContractValidator, PROVIDER_IDS
        validator = ProviderContractValidator()
        if provider_id:
            result = validator.validate_provider(provider_id)
            return {
                "provider_id": result.provider_id,
                "authority": result.authority,
                "status": result.status,
                "errors": result.errors,
            }
        results = validator.validate_all()
        return {
            "providers": [
                {"provider_id": r.provider_id, "authority": r.authority, "status": r.status}
                for r in results
            ]
        }

    def query_e2e_status(self, scenario_id: Optional[str] = None) -> Dict[str, Any]:
        from .cross_provider_e2e_v148 import CrossProviderE2EValidator
        validator = CrossProviderE2EValidator()
        if scenario_id:
            result = validator.run_scenario(scenario_id)
            return {
                "scenario_id": result.scenario_id,
                "name": result.name,
                "status": result.status,
                "detail": result.detail,
            }
        return validator.get_summary()

    def query_migration_status(self) -> Dict[str, Any]:
        from .storage_migration_v148 import StorageMigrationHardeningService
        return StorageMigrationHardeningService().get_summary()

    def query_health(self) -> Dict[str, Any]:
        from .health_v148 import ProviderIntegrationHardeningHealthCheck
        return ProviderIntegrationHardeningHealthCheck().get_health_summary()

    def query_pit_status(self) -> Dict[str, Any]:
        from .cross_provider_pit_v148 import CrossProviderPITValidator
        return CrossProviderPITValidator().get_summary()

    def query_lineage_status(self) -> Dict[str, Any]:
        from .cross_provider_lineage_v148 import CrossProviderLineageValidator
        return CrossProviderLineageValidator().get_summary()

    def query_conflict_status(self) -> Dict[str, Any]:
        from .cross_provider_conflict_v148 import CrossProviderConflictValidator
        return CrossProviderConflictValidator().get_summary()

    def query_recovery_status(self) -> Dict[str, Any]:
        from .partial_failure_v148 import PartialFailureRecoveryService
        from .lock_recovery_v148 import LockRecoveryService
        from .rate_limit_recovery_v148 import RateLimitRecoveryService
        from .runtime_recovery_v148 import RuntimeCorruptionRecoveryService
        return {
            "partial_failure": PartialFailureRecoveryService().get_summary(),
            "lock_recovery":   LockRecoveryService().get_summary(),
            "rate_recovery":   RateLimitRecoveryService().get_summary(),
            "corruption":      RuntimeCorruptionRecoveryService().get_summary(),
        }

    def query_cli_gui_consistency(self) -> Dict[str, Any]:
        from .cli_gui_consistency_v148 import CliGuiConsistencyValidator
        return CliGuiConsistencyValidator().get_summary()

    def query_performance(self) -> Dict[str, Any]:
        from .performance_budget_v148 import PerformanceBudgetService
        return PerformanceBudgetService().get_summary()

    def query_memory(self) -> Dict[str, Any]:
        from .memory_budget_v148 import MemoryBudgetService
        return MemoryBudgetService().get_summary()

    def query_collection(self) -> Dict[str, Any]:
        from .collection_integrity_v148 import ProviderIntegrationCollectionIntegrityCheck
        return ProviderIntegrationCollectionIntegrityCheck().get_summary()
