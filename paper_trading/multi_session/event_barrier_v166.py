"""
paper_trading/multi_session/event_barrier_v166.py — Event Barrier v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] No real waiting. No sleep. Deterministic result.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from paper_trading.multi_session.enums_v166 import BarrierType, BarrierStatus
from paper_trading.multi_session.models_v166 import BarrierRecord
from paper_trading.multi_session.virtual_clock_v166 import VirtualClock

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_REAL_WAIT = True
NO_SLEEP = True


class EventBarrier:
    """
    Virtual event barrier. No real blocking. No sleep. Deterministic.
    Supports ALL_OF and QUORUM barriers.
    """

    def __init__(self, clock: Optional[VirtualClock] = None) -> None:
        self._clock = clock or VirtualClock()
        self._barriers: dict = {}

    def create(
        self,
        required_sessions: List[str],
        barrier_type: BarrierType = BarrierType.ALL_OF,
        quorum: Optional[int] = None,
        timeout_seconds: Optional[float] = None,
    ) -> BarrierRecord:
        now = self._clock.now
        if quorum is None:
            quorum = len(required_sessions) if barrier_type == BarrierType.ALL_OF else max(1, len(required_sessions) // 2 + 1)
        timeout_at = (self._clock.now.__class__(
            self._clock.now.year, self._clock.now.month, self._clock.now.day,
            self._clock.now.hour, self._clock.now.minute, self._clock.now.second + int(timeout_seconds),
            tzinfo=self._clock.now.tzinfo
        )) if timeout_seconds else None
        import datetime as dt_mod
        timeout_at = (now + dt_mod.timedelta(seconds=timeout_seconds)) if timeout_seconds else None
        record = BarrierRecord(
            barrier_id=str(uuid.uuid4()),
            barrier_type=barrier_type,
            required_sessions=list(required_sessions),
            arrived_sessions=[],
            quorum=quorum,
            status=BarrierStatus.WAITING,
            created_at=now,
            released_at=None,
            timeout_at=timeout_at,
        )
        self._barriers[record.barrier_id] = record
        return record

    def arrive(self, barrier_id: str, session_id: str) -> BarrierRecord:
        record = self._barriers[barrier_id]
        if session_id not in record.arrived_sessions:
            record.arrived_sessions.append(session_id)
        self._check_release(record)
        return record

    def _check_release(self, record: BarrierRecord) -> None:
        if record.status != BarrierStatus.WAITING:
            return
        if len(record.arrived_sessions) >= record.quorum:
            record.status = BarrierStatus.RELEASED
            record.released_at = self._clock.now

    def check_timeout(self, barrier_id: str) -> BarrierRecord:
        record = self._barriers[barrier_id]
        if record.timeout_at and self._clock.is_expired(record.timeout_at):
            if record.status == BarrierStatus.WAITING:
                record.status = BarrierStatus.TIMEOUT
        return record

    def abort(self, barrier_id: str, reason: str = "") -> BarrierRecord:
        record = self._barriers[barrier_id]
        record.status = BarrierStatus.ABORTED
        return record

    def get(self, barrier_id: str) -> BarrierRecord:
        return self._barriers[barrier_id]
