"""
paper_trading/multi_session/resource_manager_v166.py — Resource Manager v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Logical/simulated reservations only. No real OS resource allocation.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import ResourceType, ReservationStatus, SessionPriority
from paper_trading.multi_session.models_v166 import ResourceReservation, CoordinationPolicy

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True
NO_REAL_OS_RESOURCE_ALLOCATION = True
LOGICAL_RESERVATION_ONLY = True


class ResourceManager:
    """
    Manages logical resource reservations for paper sessions.
    No real OS allocation. No network. No Broker. Idempotent release.
    """

    DEFAULT_CAPACITIES: Dict[ResourceType, float] = {
        ResourceType.CPU_SLOT: 16.0,
        ResourceType.MEMORY_BUDGET: 4096.0,
        ResourceType.MARKET_DATA_CHANNEL: 20.0,
        ResourceType.SYMBOL_LOCK: 500.0,
        ResourceType.STRATEGY_SLOT: 50.0,
        ResourceType.EVENT_STREAM: 20.0,
        ResourceType.CHECKPOINT_SLOT: 10.0,
        ResourceType.REPORT_SLOT: 20.0,
        ResourceType.CAPITAL_BUDGET: 1_000_000.0,
        ResourceType.RISK_BUDGET: 100.0,
    }

    def __init__(self) -> None:
        self._reservations: Dict[str, ResourceReservation] = {}
        self._usage: Dict[ResourceType, float] = {rt: 0.0 for rt in ResourceType}

    def request(
        self,
        session_id: str,
        resource_type: ResourceType,
        resource_key: str,
        quantity: float,
        priority: SessionPriority = SessionPriority.NORMAL,
        policy_version: str = "1.6.6",
        ttl_seconds: float = 300.0,
        now: Optional[datetime] = None,
    ) -> ResourceReservation:
        if now is None:
            now = datetime.now(timezone.utc)
        available = self.DEFAULT_CAPACITIES.get(resource_type, 0.0) - self._usage.get(resource_type, 0.0)
        if quantity > available:
            granted = available
            status = ReservationStatus.PARTIAL if granted > 0 else ReservationStatus.DENIED
        else:
            granted = quantity
            status = ReservationStatus.GRANTED

        reservation = ResourceReservation(
            reservation_id=str(uuid.uuid4()),
            session_id=session_id,
            resource_type=resource_type,
            resource_key=resource_key,
            quantity=granted,
            reserved_at=now,
            expires_at=now + timedelta(seconds=ttl_seconds),
            priority=priority,
            status=status,
            lease_id=None,
            policy_version=policy_version,
        )
        if status in (ReservationStatus.GRANTED, ReservationStatus.PARTIAL):
            self._reservations[reservation.reservation_id] = reservation
            self._usage[resource_type] = self._usage.get(resource_type, 0.0) + granted
        return reservation

    def release(self, reservation_id: str) -> bool:
        if reservation_id not in self._reservations:
            return True  # idempotent
        res = self._reservations[reservation_id]
        if res.status == ReservationStatus.RELEASED:
            return True  # idempotent
        self._usage[res.resource_type] = max(0.0, self._usage.get(res.resource_type, 0.0) - res.quantity)
        res.status = ReservationStatus.RELEASED
        del self._reservations[reservation_id]
        return True

    def expire_stale(self, now: Optional[datetime] = None) -> List[str]:
        if now is None:
            now = datetime.now(timezone.utc)
        expired = [
            rid for rid, res in list(self._reservations.items())
            if res.expires_at and now >= res.expires_at
        ]
        for rid in expired:
            self.release(rid)
            if rid in self._reservations:
                self._reservations[rid].status = ReservationStatus.EXPIRED
        return expired

    def get_reservation(self, reservation_id: str) -> Optional[ResourceReservation]:
        return self._reservations.get(reservation_id)

    def list_for_session(self, session_id: str) -> List[ResourceReservation]:
        return [r for r in self._reservations.values() if r.session_id == session_id]

    def available(self, resource_type: ResourceType) -> float:
        return self.DEFAULT_CAPACITIES.get(resource_type, 0.0) - self._usage.get(resource_type, 0.0)

    def allocate_for_sessions(
        self,
        session_ids: List[str],
        resource_state: Dict[str, Any],
        policy: CoordinationPolicy,
    ) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for sid in session_ids:
            result[sid] = {"status": "allocated", "reservations": []}
        return result

    def rollback_session(self, session_id: str) -> int:
        rids = [rid for rid, r in list(self._reservations.items()) if r.session_id == session_id]
        for rid in rids:
            self.release(rid)
        return len(rids)
