"""
paper_trading/multi_session/failure_propagation_v166.py — Failure Propagation v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Default: isolated failure. No default cascade.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_DEFAULT_CASCADE = True
ISOLATED_FAILURE_DEFAULT = True


@dataclass
class PropagationEvent:
    source_session_id: str
    affected_sessions: List[str]
    unaffected_sessions: List[str]
    failure_type: str
    propagation_path: List[str]
    blocked_by_isolation: List[str]


class FailurePropagationSimulator:
    """
    Simulates failure propagation. Failures are isolated by default.
    Shared dependencies must be explicitly declared for propagation.
    """

    def __init__(self) -> None:
        self._dependencies: Dict[str, List[str]] = {}

    def declare_dependency(self, session_id: str, depends_on: str) -> None:
        self._dependencies.setdefault(session_id, []).append(depends_on)

    def simulate_propagation(
        self,
        failed_session: str,
        all_sessions: List[str],
    ) -> PropagationEvent:
        affected = []
        unaffected = []
        blocked = []

        for sid in all_sessions:
            if sid == failed_session:
                continue
            deps = self._dependencies.get(sid, [])
            if failed_session in deps:
                affected.append(sid)
            else:
                unaffected.append(sid)

        # Isolated by default: sessions not in dependencies are unaffected
        not_affected_by_isolation = [s for s in all_sessions if s not in affected and s != failed_session]
        blocked = not_affected_by_isolation

        return PropagationEvent(
            source_session_id=failed_session,
            affected_sessions=affected,
            unaffected_sessions=unaffected,
            failure_type="simulated",
            propagation_path=[failed_session] + affected,
            blocked_by_isolation=blocked,
        )
