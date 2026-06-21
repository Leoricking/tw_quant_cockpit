"""
data/governance/provider_budget_v145.py — Provider Request Budget Registry v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Unknown quota → block large batch. Retry consumes budget. Cache hit → no network budget.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from data.governance.models_v145 import BudgetStatus, ProviderRequestBudget

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_BUILT_IN_BUDGETS: Dict[str, Dict[str, Any]] = {
    "twse": {"provider_id": "twse", "session_limit": 50, "hourly_limit": 200, "daily_limit": 500},
    "twse_official": {"provider_id": "twse_official", "session_limit": 50, "hourly_limit": 200, "daily_limit": 500},
    "tpex": {"provider_id": "tpex", "session_limit": 50, "hourly_limit": 150, "daily_limit": 400},
    "tpex_official": {"provider_id": "tpex_official", "session_limit": 50, "hourly_limit": 150, "daily_limit": 400},
    "mops": {"provider_id": "mops", "session_limit": 30, "hourly_limit": 100, "daily_limit": 300},
    "mops_official": {"provider_id": "mops_official", "session_limit": 30, "hourly_limit": 100, "daily_limit": 300},
    "data_gov_tw": {"provider_id": "data_gov_tw", "session_limit": 50, "hourly_limit": 200, "daily_limit": 500},
    "data_gov_tw_official": {"provider_id": "data_gov_tw_official", "session_limit": 50, "hourly_limit": 200, "daily_limit": 500},
    "finmind": {"provider_id": "finmind", "session_limit": 20, "hourly_limit": 60, "daily_limit": 200},
}


class ProviderBudgetRegistry:
    """
    Registry of per-provider request budgets.
    Rules:
    - Unknown quota → block large batch
    - Retry consumes budget
    - Cache hit → no network budget consumed
    """

    def __init__(self) -> None:
        self._budgets: Dict[str, ProviderRequestBudget] = {}
        self._session_counts: Dict[str, int] = {}
        for pid, cfg in _BUILT_IN_BUDGETS.items():
            b = ProviderRequestBudget(**cfg)
            self._budgets[pid] = b
            self._session_counts[pid] = 0

    def get_budget(self, provider_id: str) -> ProviderRequestBudget:
        if provider_id not in self._budgets:
            return ProviderRequestBudget(provider_id=provider_id)
        return self._budgets[provider_id]

    def check_budget(
        self,
        provider_id: str,
        request_count: int,
        is_batch: bool = False,
    ) -> Dict[str, Any]:
        budget = self.get_budget(provider_id)
        used = self._session_counts.get(provider_id, 0)
        remaining = budget.session_limit - used

        if remaining <= 0:
            return {
                "allowed": False,
                "status": BudgetStatus.EXHAUSTED.value,
                "reason": "session budget exhausted",
                "remaining": 0,
            }
        if request_count > remaining:
            return {
                "allowed": False,
                "status": BudgetStatus.LOW.value,
                "reason": f"request_count {request_count} exceeds remaining {remaining}",
                "remaining": remaining,
            }
        if is_batch and budget.confidence == "LOW" and request_count > 10:
            return {
                "allowed": False,
                "status": BudgetStatus.BLOCKED.value,
                "reason": "unknown quota: blocking large batch (confidence=LOW)",
                "remaining": remaining,
            }
        return {
            "allowed": True,
            "status": BudgetStatus.AVAILABLE.value,
            "reason": "within budget",
            "remaining": remaining,
        }

    def consume(
        self,
        provider_id: str,
        requests: int = 1,
        is_retry: bool = False,
    ) -> None:
        """Retry also consumes budget. Cache hits do NOT call this."""
        current = self._session_counts.get(provider_id, 0)
        self._session_counts[provider_id] = current + requests

    def reset_session(self, provider_id: str) -> None:
        self._session_counts[provider_id] = 0
