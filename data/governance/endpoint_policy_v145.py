"""
data/governance/endpoint_policy_v145.py — Endpoint Request Policy Registry v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from data.governance.models_v145 import EndpointRequestPolicy

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class EndpointPolicyRegistry:
    """Registry of per-endpoint request policies."""

    def __init__(self) -> None:
        self._policies: Dict[str, EndpointRequestPolicy] = {}

    def _key(self, provider_id: str, endpoint_family: str, dataset: str) -> str:
        return f"{provider_id}::{endpoint_family}::{dataset}"

    def get_policy(
        self,
        provider_id: str,
        endpoint_family: str,
        dataset: str,
    ) -> Optional[EndpointRequestPolicy]:
        return self._policies.get(self._key(provider_id, endpoint_family, dataset))

    def register_policy(self, policy: EndpointRequestPolicy) -> None:
        key = self._key(policy.provider_id, policy.endpoint_family, policy.dataset)
        self._policies[key] = policy

    def is_allowed(
        self,
        provider_id: str,
        endpoint_family: str,
        dataset: str,
        symbol_count: int = 1,
        date_range_days: int = 1,
    ) -> Dict[str, Any]:
        policy = self.get_policy(provider_id, endpoint_family, dataset)
        if policy is None:
            return {"allowed": True, "reason": "no policy registered (default allow)", "policy": None}
        if not policy.enabled:
            return {"allowed": False, "reason": "endpoint disabled", "policy": policy.to_dict()}
        if symbol_count > policy.maximum_symbols:
            return {
                "allowed": False,
                "reason": f"symbol_count {symbol_count} exceeds maximum {policy.maximum_symbols}",
                "policy": policy.to_dict(),
            }
        if date_range_days > policy.maximum_date_span:
            return {
                "allowed": False,
                "reason": f"date_range_days {date_range_days} exceeds maximum {policy.maximum_date_span}",
                "policy": policy.to_dict(),
            }
        return {"allowed": True, "reason": "within policy", "policy": policy.to_dict()}
