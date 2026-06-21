"""
data/governance/query_v145.py — Source Governance Query Service v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] All results JSON-safe. No token exposure.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from data.governance.lineage_registry_v145 import SourceLineageRegistry
from data.governance.request_ledger_v145 import RequestLedger
from data.governance.fetch_run_audit_v145 import FetchRunAuditService
from data.governance.rate_limit_manager_v145 import CentralRateLimitManager
from data.governance.host_policy_v145 import HostPolicyRegistry
from data.governance.provider_budget_v145 import ProviderBudgetRegistry
from data.governance.endpoint_policy_v145 import EndpointPolicyRegistry
from data.governance.quota_evidence_v145 import QuotaEvidenceService
from data.governance.retry_evidence_v145 import RetryEvidenceService
from data.governance.cache_lineage_v145 import CacheLineageService
from data.governance.conflict_lineage_v145 import ConflictLineageService

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class SourceGovernanceQueryService:
    """
    Composed query service for all governance data.
    [!] All results JSON-safe. No token exposure.
    """

    def __init__(
        self,
        lineage_registry: Optional[SourceLineageRegistry] = None,
        request_ledger: Optional[RequestLedger] = None,
        fetch_run_audit: Optional[FetchRunAuditService] = None,
        rate_limit_manager: Optional[CentralRateLimitManager] = None,
        host_policy: Optional[HostPolicyRegistry] = None,
        provider_budget: Optional[ProviderBudgetRegistry] = None,
        endpoint_policy: Optional[EndpointPolicyRegistry] = None,
        quota_evidence: Optional[QuotaEvidenceService] = None,
        retry_evidence: Optional[RetryEvidenceService] = None,
        cache_lineage: Optional[CacheLineageService] = None,
        conflict_lineage: Optional[ConflictLineageService] = None,
    ) -> None:
        self.lineage_registry = lineage_registry or SourceLineageRegistry()
        self.request_ledger = request_ledger or RequestLedger()
        self.fetch_run_audit = fetch_run_audit or FetchRunAuditService()
        self.rate_limit_manager = rate_limit_manager or CentralRateLimitManager()
        self.host_policy = host_policy or HostPolicyRegistry()
        self.provider_budget = provider_budget or ProviderBudgetRegistry()
        self.endpoint_policy = endpoint_policy or EndpointPolicyRegistry()
        self.quota_evidence = quota_evidence or QuotaEvidenceService()
        self.retry_evidence = retry_evidence or RetryEvidenceService()
        self.cache_lineage = cache_lineage or CacheLineageService()
        self.conflict_lineage = conflict_lineage or ConflictLineageService()

    # --- Source lineage queries ---

    def list_sources(self, provider_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.lineage_registry.list_sources(provider_id)

    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        identity = self.lineage_registry.get_source(source_id)
        return identity.to_dict() if identity else None

    def get_lineage(self, lineage_id: str) -> Optional[Dict[str, Any]]:
        rec = self.lineage_registry.get_lineage(lineage_id)
        return rec.to_dict() if rec else None

    def trace_lineage(self, lineage_id: str) -> List[str]:
        return self.lineage_registry.trace_to_root(lineage_id)

    def get_record_lineage(self, record_key: str, provider_id: str) -> List[Dict[str, Any]]:
        return self.lineage_registry.get_record_lineage(record_key, provider_id)

    def list_incomplete_lineage(self, provider_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.lineage_registry.list_incomplete_lineage(provider_id)

    # --- Request ledger queries ---

    def list_requests(self, provider_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        if provider_id:
            return self.request_ledger.list_by_provider(provider_id, limit)
        return []

    def get_request(self, request_id: str) -> Optional[Dict[str, Any]]:
        entry = self.request_ledger.get(request_id)
        return entry.to_dict() if entry else None

    # --- Fetch run queries ---

    def list_fetch_runs(self, provider_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        return self.fetch_run_audit.list_runs(provider_id, limit)

    def get_fetch_run(self, fetch_run_id: str) -> Optional[Dict[str, Any]]:
        run = self.fetch_run_audit.get_run(fetch_run_id)
        return run.to_dict() if run else None

    # --- Rate limit queries ---

    def get_rate_limit_host(self, host: str) -> Dict[str, Any]:
        return self.rate_limit_manager.get_host_state(host)

    def get_rate_limit_provider(self, provider_id: str) -> Dict[str, Any]:
        return self.rate_limit_manager.get_provider_state(provider_id)

    def get_rate_limit_endpoint(self, provider_id: str, endpoint_family: str) -> Dict[str, Any]:
        return self.rate_limit_manager.get_endpoint_state(provider_id, endpoint_family)

    def get_budget_state(self, provider_id: str) -> Dict[str, Any]:
        return self.rate_limit_manager.get_budget_state(provider_id)

    # --- Quota evidence queries ---

    def list_quota_evidence(self, provider_id: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for ev in self.quota_evidence._evidence.values():
            if provider_id and ev.provider_id != provider_id:
                continue
            results.append(ev.to_dict())
        return results

    # --- Retry evidence queries ---

    def list_retry_evidence(self, request_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if request_id:
            return self.retry_evidence.list_by_request(request_id)
        return [ev.to_dict() for ev in self.retry_evidence._evidence.values()]

    # --- Cache lineage queries ---

    def get_cache_lineage(self, cache_entry_id: str) -> Dict[str, Any]:
        return self.cache_lineage.trace_to_source(cache_entry_id)

    # --- Conflict lineage queries ---

    def list_conflicts(
        self,
        primary_provider: Optional[str] = None,
        unresolved_only: bool = False,
    ) -> List[Dict[str, Any]]:
        return self.conflict_lineage.list_conflicts(
            primary_provider=primary_provider,
            unresolved_only=unresolved_only,
        )

    def get_conflict(self, conflict_id: str) -> Optional[Dict[str, Any]]:
        c = self.conflict_lineage.get_conflict(conflict_id)
        return c.to_dict() if c else None

    def governance_report(self) -> Dict[str, Any]:
        """Generate a governance summary report."""
        return {
            "sources": len(self.lineage_registry._sources),
            "lineage_records": len(self.lineage_registry._lineage),
            "request_ledger_entries": len(self.request_ledger._entries),
            "fetch_runs": len(self.fetch_run_audit._runs),
            "quota_evidence": len(self.quota_evidence._evidence),
            "retry_evidence": len(self.retry_evidence._evidence),
            "cache_entries": len(self.cache_lineage._entries),
            "conflicts": len(self.conflict_lineage._conflicts),
            "no_real_orders": True,
            "research_only": True,
        }
