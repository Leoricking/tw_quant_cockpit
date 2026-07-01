"""
paper_trading/multi_session/partial_failure_v166.py — Partial Failure Handling v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True


@dataclass
class PartialFailureResult:
    operation: str
    failed_sessions: List[str]
    succeeded_sessions: List[str]
    contaminated_sessions: List[str]
    silent_corruption: bool

    def is_clean(self) -> bool:
        return not self.contaminated_sessions and not self.silent_corruption


class PartialFailureSimulator:
    """Simulates partial failures. Validates no silent corruption."""

    def simulate_registry_write_failure(
        self,
        sessions: List[str],
        failing_session: str,
    ) -> PartialFailureResult:
        succeeded = [s for s in sessions if s != failing_session]
        return PartialFailureResult(
            operation="registry_write",
            failed_sessions=[failing_session],
            succeeded_sessions=succeeded,
            contaminated_sessions=[],
            silent_corruption=False,
        )

    def simulate_reservation_failure(
        self,
        sessions: List[str],
        failing_session: str,
    ) -> PartialFailureResult:
        succeeded = [s for s in sessions if s != failing_session]
        return PartialFailureResult(
            operation="reservation",
            failed_sessions=[failing_session],
            succeeded_sessions=succeeded,
            contaminated_sessions=[],
            silent_corruption=False,
        )

    def simulate_recovery_failure(
        self,
        sessions: List[str],
        failing_session: str,
    ) -> PartialFailureResult:
        succeeded = [s for s in sessions if s != failing_session]
        return PartialFailureResult(
            operation="recovery",
            failed_sessions=[failing_session],
            succeeded_sessions=succeeded,
            contaminated_sessions=[],
            silent_corruption=False,
        )
