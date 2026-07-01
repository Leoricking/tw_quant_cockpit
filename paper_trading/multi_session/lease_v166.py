"""
paper_trading/multi_session/lease_v166.py — Lease Management v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Virtual clock. Expired lease → reservation/lock/leader invalid.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from paper_trading.multi_session.models_v166 import Lease
from paper_trading.multi_session.virtual_clock_v166 import VirtualClock

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True


class LeaseManager:
    """Manages virtual leases. Idempotent. No auto-restart on expiry."""

    def __init__(self, clock: Optional[VirtualClock] = None) -> None:
        self._clock = clock or VirtualClock()
        self._leases: Dict[str, Lease] = {}
        self._generation: Dict[str, int] = {}

    def issue(
        self,
        owner_session_id: str,
        resource_key: str,
        ttl_seconds: float = 30.0,
    ) -> Lease:
        gen = self._generation.get(resource_key, 0) + 1
        self._generation[resource_key] = gen
        now = self._clock.now
        lease = Lease(
            lease_id=str(uuid.uuid4()),
            owner_session_id=owner_session_id,
            resource_key=resource_key,
            issued_at=now,
            expires_at=now + timedelta(seconds=ttl_seconds),
            generation=gen,
        )
        self._leases[lease.lease_id] = lease
        return lease

    def renew(self, lease_id: str, ttl_seconds: float = 30.0) -> Lease:
        lease = self._leases[lease_id]
        if lease.check_expired(self._clock.now):
            raise ValueError(f"Cannot renew expired lease: {lease_id}")
        lease.expires_at = self._clock.now + timedelta(seconds=ttl_seconds)
        lease.is_expired = False
        return lease

    def expire(self, lease_id: str) -> Lease:
        lease = self._leases[lease_id]
        lease.is_expired = True
        return lease

    def check_all(self) -> Dict[str, bool]:
        return {lid: lease.check_expired(self._clock.now) for lid, lease in self._leases.items()}

    def is_valid(self, lease_id: str) -> bool:
        lease = self._leases.get(lease_id)
        if lease is None:
            return False
        return not lease.check_expired(self._clock.now)

    def get(self, lease_id: str) -> Optional[Lease]:
        return self._leases.get(lease_id)
