"""
paper_trading/multi_session/resource_reservation_v166.py — Resource Reservation helpers v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import ReservationStatus, ResourceType
from paper_trading.multi_session.models_v166 import ResourceReservation

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True


def is_reservation_valid(reservation: ResourceReservation, now: Optional[datetime] = None) -> bool:
    if now is None:
        now = datetime.now(timezone.utc)
    if reservation.status not in (ReservationStatus.GRANTED, ReservationStatus.PARTIAL):
        return False
    if reservation.expires_at and now >= reservation.expires_at:
        return False
    return True


def reservation_summary(reservations: List[ResourceReservation]) -> Dict[str, Any]:
    total = len(reservations)
    by_status: Dict[str, int] = {}
    by_type: Dict[str, float] = {}
    for r in reservations:
        by_status[r.status.value] = by_status.get(r.status.value, 0) + 1
        by_type[r.resource_type.value] = by_type.get(r.resource_type.value, 0.0) + r.quantity
    return {"total": total, "by_status": by_status, "by_resource_type": by_type}
