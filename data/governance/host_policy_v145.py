"""
data/governance/host_policy_v145.py — Host Rate Limit Policy Registry v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Conservative defaults. No rate bypass. No proxy rotation.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from data.governance.models_v145 import HostRateLimitPolicy

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
RATE_LIMIT_AUTO_BYPASS_ENABLED = False

# Built-in conservative policies for known hosts
_BUILT_IN_POLICIES: List[Dict[str, Any]] = [
    {
        "policy_id": "twse_openapi",
        "host": "openapi.twse.com.tw",
        "provider_id": "twse",
        "requests_per_minute": 30.0,
        "minimum_interval_ms": 2000,
        "concurrency_limit": 1,
        "source": "CONSERVATIVE_DEFAULT",
        "confidence": "LOW",
    },
    {
        "policy_id": "twse_legacy",
        "host": "www.twse.com.tw",
        "provider_id": "twse",
        "requests_per_minute": 20.0,
        "minimum_interval_ms": 3000,
        "concurrency_limit": 1,
        "source": "CONSERVATIVE_DEFAULT",
        "confidence": "LOW",
    },
    {
        "policy_id": "twse_primary",
        "host": "primary.twse.gov.tw",
        "provider_id": "twse",
        "requests_per_minute": 20.0,
        "minimum_interval_ms": 3000,
        "concurrency_limit": 1,
        "source": "CONSERVATIVE_DEFAULT",
        "confidence": "LOW",
    },
    {
        "policy_id": "tpex",
        "host": "www.tpex.org.tw",
        "provider_id": "tpex",
        "requests_per_minute": 20.0,
        "minimum_interval_ms": 3000,
        "concurrency_limit": 1,
        "source": "CONSERVATIVE_DEFAULT",
        "confidence": "LOW",
    },
    {
        "policy_id": "mops",
        "host": "mops.twse.com.tw",
        "provider_id": "mops",
        "requests_per_minute": 15.0,
        "minimum_interval_ms": 4000,
        "concurrency_limit": 1,
        "source": "CONSERVATIVE_DEFAULT",
        "confidence": "LOW",
    },
    {
        "policy_id": "data_gov_tw_catalog",
        "host": "data.gov.tw",
        "provider_id": "data_gov_tw",
        "requests_per_minute": 30.0,
        "minimum_interval_ms": 2000,
        "concurrency_limit": 1,
        "source": "CONSERVATIVE_DEFAULT",
        "confidence": "LOW",
    },
    {
        "policy_id": "finmind",
        "host": "api.finmindtrade.com",
        "provider_id": "finmind",
        "requests_per_minute": 10.0,
        "minimum_interval_ms": 6000,
        "concurrency_limit": 1,
        "source": "CONSERVATIVE_DEFAULT",
        "confidence": "LOW",
    },
]


class HostPolicyRegistry:
    """
    Registry of host-level rate limit policies.
    [!] Conservative defaults. No rate bypass.
    """

    def __init__(self) -> None:
        self._policies: Dict[str, HostRateLimitPolicy] = {}
        for p in _BUILT_IN_POLICIES:
            policy = HostRateLimitPolicy(
                policy_id=p["policy_id"],
                host=p["host"],
                provider_id=p["provider_id"],
                requests_per_minute=p.get("requests_per_minute"),
                minimum_interval_ms=p.get("minimum_interval_ms", 2000),
                concurrency_limit=p.get("concurrency_limit", 1),
                source=p.get("source", "DEFAULT"),
                confidence=p.get("confidence", "LOW"),
            )
            self._policies[p["host"]] = policy

    def get_policy(self, host: str) -> Optional[HostRateLimitPolicy]:
        return self._policies.get(host)

    def register_policy(self, policy: HostRateLimitPolicy) -> None:
        self._policies[policy.host] = policy

    def update_from_response(
        self,
        host: str,
        response_headers: Dict[str, str],
        payload: Any,
    ) -> None:
        """Update policy from response headers. Increases confidence."""
        policy = self._policies.get(host)
        if policy is None:
            return
        # Extract rate limit info from allowlisted headers only
        allowlisted = {k: v for k, v in response_headers.items()
                       if any(k.lower().startswith(p) for p in (
                           "x-ratelimit-", "x-quota-", "ratelimit-", "retry-after",
                       ))}
        if allowlisted:
            policy.confidence = "MEDIUM"
            policy.metadata["last_response_headers"] = allowlisted

    def list_unknown_hosts(self) -> List[str]:
        """Return hosts with no policy registered (empty since all built-ins are registered)."""
        return []

    def list_all(self) -> List[Dict[str, Any]]:
        return [p.to_dict() for p in self._policies.values()]
