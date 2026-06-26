"""
Session Registry v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import (
    ManagedSessionType, OperationalStatus, HealthStatus,
)
from paper_trading.operations.models_v163 import ManagedSessionRecord, _new_id, _now_utc
from paper_trading.operations.validation_v163 import (
    validate_session_type, validate_managed_session_id, validate_version,
    validate_no_broker_session, validate_parent_exists, validate_no_circular_dependency,
)

BLOCKED = "BLOCKED"
OK      = "OK"


class SessionRegistry:
    """Registry for managed paper-only sessions."""

    def __init__(self, registry_id: Optional[str] = None):
        self.registry_id   = registry_id or _new_id("reg_")
        self._sessions:    Dict[str, ManagedSessionRecord] = {}
        self._parent_map:  Dict[str, Optional[str]]        = {}  # child → parent

    # ------------------------------------------------------------------
    def register(
        self,
        session_id:   str,
        session_type: str,
        version:      str,
        display_name: str = "",
        source_session_id: str = "",
        parent_session_id: Optional[str] = None,
        supervisor_id: Optional[str] = None,
        metadata:     Optional[dict] = None,
    ) -> Tuple[str, str]:
        meta = metadata or {}

        ok, msg = validate_managed_session_id(session_id, set(self._sessions.keys()))
        if not ok:
            return BLOCKED, msg

        ok, msg = validate_session_type(session_type)
        if not ok:
            return BLOCKED, msg

        ok, msg = validate_version(version)
        if not ok:
            return BLOCKED, msg

        ok, msg = validate_no_broker_session(meta)
        if not ok:
            return BLOCKED, msg

        ok, msg = validate_parent_exists(parent_session_id, set(self._sessions.keys()))
        if not ok:
            return BLOCKED, msg

        ok, msg = validate_no_circular_dependency(session_id, parent_session_id, self._parent_map)
        if not ok:
            return BLOCKED, msg

        record = ManagedSessionRecord(
            managed_session_id=session_id,
            session_type=ManagedSessionType(session_type),
            source_session_id=source_session_id or session_id,
            display_name=display_name or session_id,
            version=version,
            supervisor_id=supervisor_id,
            parent_session_id=parent_session_id,
            metadata=meta,
        )
        self._sessions[session_id] = record
        self._parent_map[session_id] = parent_session_id

        if parent_session_id and parent_session_id in self._sessions:
            parent = self._sessions[parent_session_id]
            if session_id not in parent.child_session_ids:
                parent.child_session_ids.append(session_id)

        return OK, session_id

    # ------------------------------------------------------------------
    def get(self, session_id: str) -> Optional[ManagedSessionRecord]:
        return self._sessions.get(session_id)

    def list_all(self) -> List[ManagedSessionRecord]:
        return list(self._sessions.values())

    def list_by_type(self, session_type: ManagedSessionType) -> List[ManagedSessionRecord]:
        return [s for s in self._sessions.values() if s.session_type == session_type]

    def count(self) -> int:
        return len(self._sessions)

    def update_status(self, session_id: str, status: OperationalStatus) -> bool:
        rec = self._sessions.get(session_id)
        if rec is None:
            return False
        rec.status      = status
        rec.last_event_at = _now_utc()
        if status == OperationalStatus.PAUSED:
            rec.paused_at = _now_utc()
        elif status == OperationalStatus.HALTED:
            rec.halted_at = _now_utc()
        elif status == OperationalStatus.COMPLETED:
            rec.completed_at = _now_utc()
        return True

    def update_health(self, session_id: str, health: HealthStatus) -> bool:
        rec = self._sessions.get(session_id)
        if rec is None:
            return False
        rec.health_status = health
        if health == HealthStatus.HEALTHY:
            rec.last_healthy_at = _now_utc()
        return True

    def dependency_graph(self) -> Dict[str, Optional[str]]:
        return dict(self._parent_map)

    def children_of(self, session_id: str) -> List[str]:
        rec = self._sessions.get(session_id)
        return list(rec.child_session_ids) if rec else []


__all__ = ["SessionRegistry", "BLOCKED", "OK"]
