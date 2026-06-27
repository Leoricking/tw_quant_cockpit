"""
paper_trading/failure_validation/query_v165.py — Failure injection query API v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Local query only.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from paper_trading.failure_validation.enums_v165 import (
    FailureDomain, FailureSeverity, InjectionStatus
)

PAPER_ONLY = True
RESEARCH_ONLY = True


class FailureInjectionQuery:
    """Local query API for failure injection records."""

    def __init__(self, store: Any) -> None:
        self._store = store

    def latest_results(self, n: int = 10) -> List[Dict[str, Any]]:
        return self._store.query_injection_results(limit=n)

    def results_by_status(self, status: InjectionStatus) -> List[Dict[str, Any]]:
        all_results = self._store.query_injection_results(limit=1000)
        return [r for r in all_results if r.get("status") == status.value]

    def scorecard_summary(self, n: int = 10) -> List[Dict[str, Any]]:
        return self._store.query_scorecards(limit=n)

    def recovery_summary(self, n: int = 10) -> List[Dict[str, Any]]:
        return self._store.query_recovery_validations(limit=n)

    def count_by_status(self) -> Dict[str, int]:
        all_results = self._store.query_injection_results(limit=10000)
        counts: Dict[str, int] = {}
        for r in all_results:
            status = r.get("status", "UNKNOWN")
            counts[status] = counts.get(status, 0) + 1
        return counts
