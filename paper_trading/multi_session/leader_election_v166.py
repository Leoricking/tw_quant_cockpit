"""
paper_trading/multi_session/leader_election_v166.py — Leader Election v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Local deterministic simulation only. No network election. No Raft/Paxos.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import ElectionStatus, SessionPriority
from paper_trading.multi_session.models_v166 import ElectionRecord, SessionDescriptor
from paper_trading.multi_session.virtual_clock_v166 import VirtualClock

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_NETWORK_ELECTION = True
NO_EXTERNAL_CONSENSUS = True
NO_RAFT_PAXOS = True
NO_PRODUCTION_FAILOVER = True


class LeaderElection:
    """
    Local deterministic leader election simulation.
    No network. No external coordinator. No production failover.
    Single active leader invariant enforced.
    """

    def __init__(self, clock: Optional[VirtualClock] = None) -> None:
        self._clock = clock or VirtualClock()
        self._current_election: Optional[ElectionRecord] = None
        self._generation: int = 0

    def elect(
        self,
        candidates: List[SessionDescriptor],
        lease_ttl_seconds: float = 30.0,
        seed: int = 0,
    ) -> ElectionRecord:
        # Eligibility: not FAILED/CANCELLED/COMPLETED
        from paper_trading.multi_session.enums_v166 import SessionLifecycleState
        eligible = [
            c for c in candidates
            if c.lifecycle_state not in (
                SessionLifecycleState.FAILED,
                SessionLifecycleState.CANCELLED,
                SessionLifecycleState.COMPLETED,
            )
        ]
        if not eligible:
            return ElectionRecord(
                election_id=str(uuid.uuid4()),
                candidates=[c.session_id for c in candidates],
                winner_session_id=None,
                status=ElectionStatus.FAILED,
                started_at=self._clock.now,
                decided_at=self._clock.now,
                lease_id=None,
                generation=self._generation,
            )
        # Deterministic: highest priority, then session_id alpha
        winner = sorted(eligible, key=lambda s: (-s.priority.value, s.session_id))[0]
        self._generation += 1
        lease_id = str(uuid.uuid4())
        record = ElectionRecord(
            election_id=str(uuid.uuid4()),
            candidates=[c.session_id for c in eligible],
            winner_session_id=winner.session_id,
            status=ElectionStatus.ELECTED,
            started_at=self._clock.now,
            decided_at=self._clock.now,
            lease_id=lease_id,
            generation=self._generation,
        )
        self._current_election = record
        return record

    def detect_split_brain(self, elections: List[ElectionRecord]) -> bool:
        winners = {e.winner_session_id for e in elections if e.status == ElectionStatus.ELECTED and e.winner_session_id}
        return len(winners) > 1

    def is_leader_valid(self, election: ElectionRecord, now: Optional[datetime] = None) -> bool:
        if election.status != ElectionStatus.ELECTED:
            return False
        return True

    def simulate_failover(
        self,
        failed_leader_id: str,
        remaining_candidates: List[SessionDescriptor],
        seed: int = 0,
    ) -> ElectionRecord:
        filtered = [c for c in remaining_candidates if c.session_id != failed_leader_id]
        return self.elect(filtered, seed=seed)
