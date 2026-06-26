"""
Audit Trail v1.6.3 — Append-only, hash-chained.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
No credentials. No broker data. No real account data.
"""
from __future__ import annotations
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from paper_trading.operations.models_v163 import _new_id, _now_utc

AUDIT_EVENTS = [
    "operation_requested", "operation_validated", "operation_blocked",
    "operation_executed", "alert_created", "alert_acknowledged",
    "alert_resolved", "incident_opened", "incident_transitioned",
    "checkpoint_created", "recovery_started", "recovery_completed",
    "replay_verified", "safety_blocked",
]


@dataclass
class AuditEntry:
    audit_id:       str
    event_type:     str
    actor:          str
    reason:         str
    occurred_at:    datetime
    entity_id:      str            = ""
    policy_version: str            = "1.6.3"
    code_version:   str            = "1.6.3"
    lineage_ids:    List[str]      = field(default_factory=list)
    prev_hash:      str            = ""
    entry_hash:     str            = ""
    metadata:       Dict[str, Any] = field(default_factory=dict)
    sequence:       int            = 0

    def __post_init__(self):
        if not self.entry_hash:
            self.entry_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        data = (
            f"{self.audit_id}:{self.event_type}:{self.actor}:"
            f"{self.reason}:{self.occurred_at.isoformat()}:"
            f"{self.policy_version}:{self.code_version}:{self.prev_hash}"
        )
        return "sha256:" + hashlib.sha256(data.encode()).hexdigest()


class AuditTrail:
    """
    Append-only hash chain.
    No credentials, no broker data, no real account data.
    """

    def __init__(self):
        self._entries:  List[AuditEntry] = []

    def record(
        self,
        event_type:     str,
        actor:          str,
        reason:         str,
        entity_id:      str            = "",
        occurred_at:    Optional[datetime] = None,
        lineage_ids:    Optional[List[str]] = None,
        policy_version: str            = "1.6.3",
        code_version:   str            = "1.6.3",
        metadata:       Optional[Dict[str, Any]] = None,
    ) -> AuditEntry:
        seq      = len(self._entries)
        prev_hash = self._entries[-1].entry_hash if self._entries else ""
        entry = AuditEntry(
            audit_id=_new_id("aud_"),
            event_type=event_type,
            actor=actor,
            reason=reason,
            occurred_at=occurred_at or _now_utc(),
            entity_id=entity_id,
            policy_version=policy_version,
            code_version=code_version,
            lineage_ids=lineage_ids or [],
            prev_hash=prev_hash,
            metadata=metadata or {},
            sequence=seq,
        )
        self._entries.append(entry)
        return entry

    def verify_chain(self) -> Tuple[bool, str]:
        for i in range(1, len(self._entries)):
            expected = self._entries[i - 1].entry_hash
            if self._entries[i].prev_hash != expected:
                return False, f"Chain broken at sequence {i}"
        return True, "Chain intact"

    def tail(self, n: int = 10) -> List[AuditEntry]:
        return self._entries[-n:]

    def all(self) -> List[AuditEntry]:
        return list(self._entries)

    def count(self) -> int:
        return len(self._entries)

    def head_hash(self) -> str:
        return self._entries[-1].entry_hash if self._entries else ""


__all__ = ["AuditEntry", "AuditTrail", "AUDIT_EVENTS"]
