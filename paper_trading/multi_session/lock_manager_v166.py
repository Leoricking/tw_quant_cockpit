"""
paper_trading/multi_session/lock_manager_v166.py — Lock Manager v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] In-memory logical locks only. No OS file lock. No Redis. No network lock.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set
from paper_trading.multi_session.enums_v166 import LockType, LockStatus
from paper_trading.multi_session.models_v166 import LockRecord
from paper_trading.multi_session.virtual_clock_v166 import VirtualClock

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_OS_FILE_LOCK = True
NO_REDIS_LOCK = True
NO_NETWORK_LOCK = True
NO_DISTRIBUTED_LOCK_SERVER = True
IN_MEMORY_LOGICAL_LOCK_ONLY = True


class LockManager:
    """In-memory logical lock manager. No OS resource. No distributed coordination."""

    def __init__(self, clock: Optional[VirtualClock] = None) -> None:
        self._clock = clock or VirtualClock()
        self._locks: Dict[str, LockRecord] = {}
        self._wait_for: Dict[str, List[str]] = {}

    def acquire(
        self,
        resource_key: str,
        lock_type: LockType,
        owner_session_id: str,
        ttl_seconds: float = 60.0,
        lease_id: Optional[str] = None,
    ) -> Optional[LockRecord]:
        now = self._clock.now
        # Check for conflicting locks
        for lock in self._locks.values():
            if lock.resource_key == resource_key and lock.status == LockStatus.HELD:
                not_expired = (lock.expires_at is None) or (now < lock.expires_at)
                if not_expired:
                    if lock_type == LockType.EXCLUSIVE or lock.lock_type == LockType.EXCLUSIVE:
                        # Record wait-for
                        self._wait_for.setdefault(owner_session_id, []).append(lock.owner_session_id)
                        return None  # Denied

        record = LockRecord(
            lock_id=str(uuid.uuid4()),
            resource_key=resource_key,
            lock_type=lock_type,
            owner_session_id=owner_session_id,
            acquired_at=now,
            expires_at=now + timedelta(seconds=ttl_seconds),
            status=LockStatus.HELD,
            lease_id=lease_id,
        )
        self._locks[record.lock_id] = record
        return record

    def release(self, lock_id: str) -> bool:
        lock = self._locks.get(lock_id)
        if lock is None:
            return True  # idempotent
        lock.status = LockStatus.RELEASED
        # Remove from wait-for
        for sid in list(self._wait_for.keys()):
            if lock.owner_session_id in self._wait_for[sid]:
                self._wait_for[sid].remove(lock.owner_session_id)
        return True

    def check_expired(self, now: Optional[datetime] = None) -> List[str]:
        t = now or self._clock.now
        expired = []
        for lid, lock in self._locks.items():
            if lock.expires_at and t >= lock.expires_at and lock.status == LockStatus.HELD:
                lock.status = LockStatus.EXPIRED
                expired.append(lid)
        return expired

    def get_wait_for_graph(self) -> Dict[str, List[str]]:
        return dict(self._wait_for)

    def held_locks(self) -> List[LockRecord]:
        return [l for l in self._locks.values() if l.status == LockStatus.HELD]

    def validate_owner(self, lock_id: str, session_id: str) -> bool:
        lock = self._locks.get(lock_id)
        if lock is None:
            return False
        return lock.owner_session_id == session_id

    def cleanup_session(self, session_id: str) -> int:
        released = 0
        for lock in list(self._locks.values()):
            if lock.owner_session_id == session_id and lock.status == LockStatus.HELD:
                self.release(lock.lock_id)
                released += 1
        if session_id in self._wait_for:
            del self._wait_for[session_id]
        return released
