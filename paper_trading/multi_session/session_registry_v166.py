"""
paper_trading/multi_session/session_registry_v166.py — Session Registry v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import SessionType, SessionLifecycleState, SessionPriority
from paper_trading.multi_session.models_v166 import SessionDescriptor
from paper_trading.multi_session.validation_v166 import validate_session_descriptor, validate_no_duplicate_session

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_BROKER = True


@dataclass
class RegistrationRecord:
    session_id: str
    registered_at: datetime
    descriptor: SessionDescriptor
    history: List[Dict[str, Any]] = field(default_factory=list)


class SessionRegistry:
    """
    Local in-memory session registry. No network. No external DB.
    Enforces unique IDs, owner/type requirements, immutable history.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, RegistrationRecord] = {}
        self._history: List[Dict[str, Any]] = []

    def register(self, descriptor: SessionDescriptor) -> None:
        v = validate_session_descriptor(descriptor)
        if not v.valid:
            raise ValueError(f"Invalid descriptor: {v.violations}")
        dup = validate_no_duplicate_session(list(self._sessions.keys()), descriptor.session_id)
        if not dup.valid:
            raise ValueError(f"Duplicate registration: {dup.violations}")
        now = datetime.now(timezone.utc)
        descriptor.registered_at = now
        rec = RegistrationRecord(
            session_id=descriptor.session_id,
            registered_at=now,
            descriptor=descriptor,
        )
        self._sessions[descriptor.session_id] = rec
        self._history.append({"event": "register", "session_id": descriptor.session_id, "at": now.isoformat()})

    def unregister(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise KeyError(f"Session not found: {session_id}")
        now = datetime.now(timezone.utc)
        self._history.append({"event": "unregister", "session_id": session_id, "at": now.isoformat()})
        del self._sessions[session_id]

    def lookup(self, session_id: str) -> SessionDescriptor:
        if session_id not in self._sessions:
            raise KeyError(f"Session not found: {session_id}")
        return self._sessions[session_id].descriptor

    def list_sessions(self) -> List[SessionDescriptor]:
        return [rec.descriptor for rec in self._sessions.values()]

    def filter_by_type(self, session_type: SessionType) -> List[SessionDescriptor]:
        return [d for d in self.list_sessions() if d.session_type == session_type]

    def filter_by_state(self, state: SessionLifecycleState) -> List[SessionDescriptor]:
        return [d for d in self.list_sessions() if d.lifecycle_state == state]

    def update_state(self, session_id: str, new_state: SessionLifecycleState) -> None:
        desc = self.lookup(session_id)
        old = desc.lifecycle_state
        desc.lifecycle_state = new_state
        now = datetime.now(timezone.utc)
        self._sessions[session_id].history.append(
            {"event": "state_change", "from": old.value, "to": new_state.value, "at": now.isoformat()}
        )
        self._history.append({"event": "state_update", "session_id": session_id, "at": now.isoformat()})

    def update_capabilities(self, session_id: str, capabilities: List[str]) -> None:
        desc = self.lookup(session_id)
        desc.capabilities = list(capabilities)
        now = datetime.now(timezone.utc)
        self._history.append({"event": "capability_update", "session_id": session_id, "at": now.isoformat()})

    def update_heartbeat(self, session_id: str, ts: datetime) -> None:
        if session_id not in self._sessions:
            raise KeyError(f"Session not found: {session_id}")
        self._sessions[session_id].history.append({"event": "heartbeat", "at": ts.isoformat()})

    def snapshot(self) -> Dict[str, Any]:
        return {
            sid: {
                "lifecycle_state": rec.descriptor.lifecycle_state.value,
                "session_type": rec.descriptor.session_type.value,
                "priority": rec.descriptor.priority.value,
                "owner": rec.descriptor.owner,
            }
            for sid, rec in self._sessions.items()
        }

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self._history)

    def count(self) -> int:
        return len(self._sessions)

    def detect_stale_sessions(self, stale_threshold_seconds: float, now: Optional[datetime] = None) -> List[str]:
        if now is None:
            now = datetime.now(timezone.utc)
        stale = []
        for sid, rec in self._sessions.items():
            heartbeats = [e for e in rec.history if e.get("event") == "heartbeat"]
            if not heartbeats:
                continue
            last_ts = datetime.fromisoformat(heartbeats[-1]["at"])
            diff = (now - last_ts).total_seconds()
            if diff > stale_threshold_seconds:
                stale.append(sid)
        return stale
