"""
data/governance/rate_limit_manager_v145.py — Central Rate Limit Manager v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No rate bypass. No proxy rotation. No token rotation. Injectable clock for tests.
"""
from __future__ import annotations

import threading
import time
from typing import Any, Callable, Dict, Optional

from data.governance.models_v145 import QuotaEvidence
from data.governance.host_policy_v145 import HostPolicyRegistry
from data.governance.provider_budget_v145 import ProviderBudgetRegistry
from data.governance.endpoint_policy_v145 import EndpointPolicyRegistry

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
RATE_LIMIT_AUTO_BYPASS_ENABLED = False


class CentralRateLimitManager:
    """
    Central rate limit manager.
    [!] No rate bypass. No proxy rotation. No token rotation.
    [!] Injectable clock for tests.
    """

    def __init__(
        self,
        host_policy_registry: Optional[HostPolicyRegistry] = None,
        provider_budget_registry: Optional[ProviderBudgetRegistry] = None,
        endpoint_policy_registry: Optional[EndpointPolicyRegistry] = None,
        clock: Optional[Callable[[], float]] = None,
    ) -> None:
        self._host_policy = host_policy_registry or HostPolicyRegistry()
        self._provider_budget = provider_budget_registry or ProviderBudgetRegistry()
        self._endpoint_policy = endpoint_policy_registry or EndpointPolicyRegistry()
        self._clock = clock or time.time
        self._lock = threading.Lock()

        # Per-host state: last request time, cooldown until, retry-after until
        self._host_state: Dict[str, Dict[str, Any]] = {}
        # Per-provider state
        self._provider_state: Dict[str, Dict[str, Any]] = {}
        # Per-endpoint state
        self._endpoint_state: Dict[str, Dict[str, Any]] = {}
        # Quota evidence
        self._quota_evidence: Dict[str, QuotaEvidence] = {}

    def _host_key(self, host: str) -> str:
        return host

    def _provider_key(self, provider_id: str) -> str:
        return provider_id

    def _endpoint_key(self, provider_id: str, endpoint_family: str) -> str:
        return f"{provider_id}::{endpoint_family}"

    def _get_host_state(self, host: str) -> Dict[str, Any]:
        k = self._host_key(host)
        if k not in self._host_state:
            self._host_state[k] = {
                "host": host,
                "last_request_at": 0.0,
                "cooldown_until": 0.0,
                "retry_after_until": 0.0,
                "concurrent": 0,
            }
        return self._host_state[k]

    def _get_provider_state(self, provider_id: str) -> Dict[str, Any]:
        k = self._provider_key(provider_id)
        if k not in self._provider_state:
            self._provider_state[k] = {
                "provider_id": provider_id,
                "session_requests": 0,
            }
        return self._provider_state[k]

    def acquire(
        self,
        provider_id: str,
        host: str,
        endpoint_family: str,
        dataset: str,
    ) -> bool:
        """Acquire a request slot. Returns True if allowed."""
        with self._lock:
            now = self._clock()
            hs = self._get_host_state(host)
            policy = self._host_policy.get_policy(host)

            # Check cooldown
            if now < hs["cooldown_until"]:
                return False

            # Check retry-after
            if now < hs["retry_after_until"]:
                return False

            # Check concurrency
            max_concurrent = 1
            if policy:
                max_concurrent = policy.concurrency_limit
            if hs["concurrent"] >= max_concurrent:
                return False

            # Check minimum interval
            min_interval_ms = 1000
            if policy:
                min_interval_ms = policy.minimum_interval_ms
            elapsed_ms = (now - hs["last_request_at"]) * 1000
            if elapsed_ms < min_interval_ms and hs["last_request_at"] > 0:
                return False

            # Check provider budget
            budget_check = self._provider_budget.check_budget(provider_id, 1)
            if not budget_check["allowed"]:
                return False

            # All checks passed
            hs["concurrent"] += 1
            hs["last_request_at"] = now
            self._provider_budget.consume(provider_id, 1)
            return True

    def release(self, provider_id: str, host: str) -> None:
        with self._lock:
            hs = self._get_host_state(host)
            hs["concurrent"] = max(0, hs["concurrent"] - 1)

    def can_request(
        self,
        provider_id: str,
        host: str,
        endpoint_family: str,
    ) -> Dict[str, Any]:
        """Check if a request would be allowed without actually acquiring."""
        with self._lock:
            now = self._clock()
            hs = self._get_host_state(host)
            policy = self._host_policy.get_policy(host)

            if now < hs["cooldown_until"]:
                wait_ms = (hs["cooldown_until"] - now) * 1000
                return {"allowed": False, "wait_ms": wait_ms, "reason": "cooldown"}

            if now < hs["retry_after_until"]:
                wait_ms = (hs["retry_after_until"] - now) * 1000
                return {"allowed": False, "wait_ms": wait_ms, "reason": "retry_after"}

            budget_check = self._provider_budget.check_budget(provider_id, 1)
            if not budget_check["allowed"]:
                return {"allowed": False, "wait_ms": 0, "reason": budget_check["reason"]}

            min_interval_ms = 1000
            if policy:
                min_interval_ms = policy.minimum_interval_ms
            elapsed_ms = (now - hs["last_request_at"]) * 1000
            if elapsed_ms < min_interval_ms and hs["last_request_at"] > 0:
                wait_ms = min_interval_ms - elapsed_ms
                return {"allowed": False, "wait_ms": wait_ms, "reason": "minimum_interval"}

            return {"allowed": True, "wait_ms": 0, "reason": "ok"}

    def estimate_wait(self, provider_id: str, host: str) -> float:
        """Estimate seconds until next request is allowed."""
        result = self.can_request(provider_id, host, "")
        if result["allowed"]:
            return 0.0
        return result.get("wait_ms", 0) / 1000.0

    def record_response(
        self,
        provider_id: str,
        host: str,
        status: str,
        duration_ms: float,
    ) -> None:
        with self._lock:
            hs = self._get_host_state(host)
            ps = self._get_provider_state(provider_id)
            ps["last_status"] = status
            ps["last_duration_ms"] = duration_ms

    def record_rate_limit(
        self,
        provider_id: str,
        host: str,
        retry_after_seconds: Optional[float] = None,
    ) -> None:
        with self._lock:
            hs = self._get_host_state(host)
            now = self._clock()
            if retry_after_seconds is not None:
                hs["retry_after_until"] = now + retry_after_seconds
            else:
                hs["retry_after_until"] = now + 60.0  # Default 60s

    def record_quota(self, provider_id: str, evidence: QuotaEvidence) -> None:
        with self._lock:
            key = f"{provider_id}::{evidence.host}"
            self._quota_evidence[key] = evidence

    def apply_retry_after(self, provider_id: str, host: str, seconds: float) -> None:
        with self._lock:
            hs = self._get_host_state(host)
            hs["retry_after_until"] = self._clock() + seconds

    def start_cooldown(self, provider_id: str, host: str, seconds: float) -> None:
        with self._lock:
            hs = self._get_host_state(host)
            hs["cooldown_until"] = self._clock() + seconds

    def get_host_state(self, host: str) -> Dict[str, Any]:
        with self._lock:
            return dict(self._get_host_state(host))

    def get_provider_state(self, provider_id: str) -> Dict[str, Any]:
        with self._lock:
            return dict(self._get_provider_state(provider_id))

    def get_endpoint_state(self, provider_id: str, endpoint_family: str) -> Dict[str, Any]:
        k = self._endpoint_key(provider_id, endpoint_family)
        with self._lock:
            return dict(self._endpoint_state.get(k, {}))

    def get_budget_state(self, provider_id: str) -> Dict[str, Any]:
        budget = self._provider_budget.get_budget(provider_id)
        return budget.to_dict()

    def reset_expired_windows(self) -> None:
        """Reset expired rate limit windows."""
        with self._lock:
            now = self._clock()
            for hs in self._host_state.values():
                if hs["retry_after_until"] < now:
                    hs["retry_after_until"] = 0.0
                if hs["cooldown_until"] < now:
                    hs["cooldown_until"] = 0.0
