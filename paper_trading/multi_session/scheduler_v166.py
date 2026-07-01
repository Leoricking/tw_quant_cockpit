"""
paper_trading/multi_session/scheduler_v166.py — Session Scheduler v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Logical scheduling only. No real process start. No OS scheduler.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import SessionLifecycleState, SessionPriority
from paper_trading.multi_session.models_v166 import SessionDescriptor
from paper_trading.multi_session.priority_engine_v166 import PriorityEngine
from paper_trading.multi_session.fairness_engine_v166 import FairnessEngine

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_REAL_PROCESS_START = True
NO_OS_SCHEDULER = True


@dataclass
class ScheduleEntry:
    session_id: str
    scheduled_at: datetime
    priority: SessionPriority
    round_number: int
    admitted: bool
    reason: str


class SessionScheduler:
    """
    Logical scheduler: orders and admits sessions by priority+fairness.
    No real process control. No auto-start. No OS calls.
    """

    def __init__(
        self,
        max_concurrent: int = 10,
        seed: int = 0,
    ) -> None:
        self._max_concurrent = max_concurrent
        self._seed = seed
        self._priority_engine = PriorityEngine()
        self._fairness_engine = FairnessEngine()
        self._schedule: List[ScheduleEntry] = []
        self._round = 0

    def schedule_round(
        self,
        candidates: List[SessionDescriptor],
        now: Optional[datetime] = None,
    ) -> List[ScheduleEntry]:
        if now is None:
            now = datetime.now(timezone.utc)
        self._round += 1
        aging = {
            sid: self._fairness_engine.get_record(sid).wait_rounds
            for sid in [s.session_id for s in candidates]
        }
        ordered = self._priority_engine.order_sessions(candidates, self._seed, aging)
        entries: List[ScheduleEntry] = []
        admitted_count = 0
        for s in ordered:
            if admitted_count < self._max_concurrent:
                entry = ScheduleEntry(
                    session_id=s.session_id,
                    scheduled_at=now,
                    priority=s.priority,
                    round_number=self._round,
                    admitted=True,
                    reason="admitted_by_priority",
                )
                self._fairness_engine.record_grant(s.session_id)
                admitted_count += 1
            else:
                entry = ScheduleEntry(
                    session_id=s.session_id,
                    scheduled_at=now,
                    priority=s.priority,
                    round_number=self._round,
                    admitted=False,
                    reason="capacity_limit",
                )
                self._fairness_engine.record_denial(s.session_id)
            entries.append(entry)
        self._schedule.extend(entries)
        return entries

    def starvation_warnings(self) -> List[str]:
        return self._fairness_engine.detect_starvation()

    def full_schedule(self) -> List[ScheduleEntry]:
        return list(self._schedule)
