"""
paper_trading/failure_validation/analytics_v165.py — Failure injection analytics v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from paper_trading.failure_validation.enums_v165 import FailureDomain, FailureSeverity

PAPER_ONLY = True
RESEARCH_ONLY = True


class FailureInjectionAnalytics:
    """Analytics aggregator for failure injection & recovery results."""

    def __init__(self) -> None:
        self._results: List[Dict[str, Any]] = []

    def record(self, result: Dict[str, Any]) -> None:
        self._results.append(result)

    def total_injections(self) -> int:
        return len(self._results)

    def detection_rate(self) -> Optional[float]:
        if not self._results:
            return None
        detected = sum(1 for r in self._results if r.get("detected"))
        return detected / len(self._results)

    def containment_rate(self) -> Optional[float]:
        if not self._results:
            return None
        contained = sum(1 for r in self._results if r.get("contained"))
        return contained / len(self._results)

    def recovery_rate(self) -> Optional[float]:
        if not self._results:
            return None
        recovered = sum(1 for r in self._results if r.get("recovered"))
        return recovered / len(self._results)

    def summary(self) -> Dict[str, Any]:
        return {
            "total_injections": self.total_injections(),
            "detection_rate": self.detection_rate(),
            "containment_rate": self.containment_rate(),
            "recovery_rate": self.recovery_rate(),
            "paper_only": PAPER_ONLY,
            "research_only": RESEARCH_ONLY,
        }
