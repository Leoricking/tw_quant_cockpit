"""
paper_trading/failure_validation/audit_v165.py — Failure injection audit trail v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List

PAPER_ONLY = True
RESEARCH_ONLY = True
APPEND_ONLY = True


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class AuditEntry:
    audit_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    actor: str = "test_harness"
    scenario_id: str = ""
    detail: Dict[str, Any] = field(default_factory=dict)
    ts: datetime = field(default_factory=_utcnow)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "event_type": self.event_type,
            "actor": self.actor,
            "scenario_id": self.scenario_id,
            "ts": self.ts.isoformat(),
        }


class AuditTrail:
    """Append-only audit trail for failure injection operations."""

    def __init__(self) -> None:
        assert APPEND_ONLY
        self._entries: List[AuditEntry] = []

    def record(self, event_type: str, scenario_id: str = "", actor: str = "test_harness",
               detail: Dict[str, Any] = None) -> AuditEntry:
        entry = AuditEntry(event_type=event_type, actor=actor,
                           scenario_id=scenario_id, detail=detail or {})
        self._entries.append(entry)
        return entry

    def all(self) -> List[AuditEntry]:
        return list(self._entries)

    def count(self) -> int:
        return len(self._entries)

    def tail(self, n: int = 10) -> List[AuditEntry]:
        return list(self._entries[-n:])
