"""
data/governance/quality/query_v146.py — Provider Quality Query Service v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] JSON-safe results. No secret leakage.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class ProviderQualityQueryService:
    """Query service for provider quality data. All results JSON-safe."""

    POLICY_VERSION = "1.4.6"

    def __init__(self, store=None, engine=None, quarantine_mgr=None,
                 audit_svc=None) -> None:
        self._store = store
        self._engine = engine
        self._quarantine_mgr = quarantine_mgr
        self._audit_svc = audit_svc

    def get_provider_quality_state(self, provider_id: str) -> Dict[str, Any]:
        """Get current quality state for a provider."""
        if self._store:
            profile = self._store.get_provider_profile(provider_id)
            if profile:
                return {"provider_id": provider_id, **profile, "no_real_orders": True}
        return {
            "provider_id": provider_id,
            "quality_state": "UNKNOWN",
            "formal_research_allowed": False,
            "backtest_allowed": False,
            "no_real_orders": True,
            "policy_version": self.POLICY_VERSION,
        }

    def list_provider_profiles(self) -> List[Dict[str, Any]]:
        """List all provider quality profiles."""
        if self._store:
            return self._store.list_provider_profiles()
        return []

    def get_dataset_quality_state(self, dataset_id: str,
                                   provider_id: str) -> Dict[str, Any]:
        """Get quality state for a dataset."""
        return {
            "dataset_id": dataset_id,
            "provider_id": provider_id,
            "quality_state": "UNKNOWN",
            "no_real_orders": True,
            "policy_version": self.POLICY_VERSION,
        }

    def list_blocked_providers(self) -> List[Dict[str, Any]]:
        """List all blocked providers."""
        if self._quarantine_mgr:
            return [r.to_dict() for r in self._quarantine_mgr.list_quarantined()]
        return []

    def list_quarantined_providers(self) -> List[Dict[str, Any]]:
        """List quarantined providers."""
        if self._quarantine_mgr:
            return [
                r.to_dict() for r in self._quarantine_mgr.list_quarantined()
                if r.quality_state == "QUARANTINED"
            ]
        return []

    def get_quality_decision(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """Get a quality decision by ID."""
        if self._store:
            return self._store.get_decision(decision_id)
        return None

    def get_audit_trail(self, provider_id: str) -> List[Dict[str, Any]]:
        """Get audit trail for a provider."""
        if self._audit_svc:
            return [a.to_dict() for a in self._audit_svc.get_by_provider(provider_id)]
        return []

    def quality_summary_report(self) -> Dict[str, Any]:
        """Generate summary quality report."""
        profiles = self.list_provider_profiles()
        blocked = self.list_blocked_providers()
        quarantined = self.list_quarantined_providers()

        active = [p for p in profiles if p.get("quality_state") == "ACTIVE"]
        degraded = [p for p in profiles if p.get("quality_state") == "DEGRADED"]
        restricted = [p for p in profiles if p.get("quality_state") == "RESTRICTED"]

        return {
            "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
            "policy_version": self.POLICY_VERSION,
            "no_real_orders": True,
            "research_only": True,
            "summary": {
                "total_providers": len(profiles),
                "active": len(active),
                "degraded": len(degraded),
                "restricted": len(restricted),
                "quarantined": len(quarantined),
                "blocked": len(blocked),
            },
            "providers": profiles,
        }

    def explain_decision(self, decision_id: str) -> Dict[str, Any]:
        """Explain a quality decision."""
        decision = self.get_quality_decision(decision_id)
        if not decision:
            return {"error": f"Decision '{decision_id}' not found"}
        return {
            "decision_id": decision_id,
            "decision": decision.get("decision"),
            "quality_state": decision.get("quality_state"),
            "blocking_failures": decision.get("blocking_failures", []),
            "warnings": decision.get("warnings", []),
            "score_overrode_blocking": False,
            "explanation": (
                "Blocking failures prevent formal use. "
                "Score cannot override blocking failures."
            ) if decision.get("blocking_failures") else "All gates passed.",
            "no_real_orders": True,
        }
