"""
Incident Management v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import (
    IncidentStatus, IncidentCategory, AlertSeverity,
    VALID_INCIDENT_TRANSITIONS,
)
from paper_trading.operations.models_v163 import SessionIncident, _new_id, _now_utc
from paper_trading.operations.validation_v163 import (
    validate_incident_transition,
    validate_incident_has_affected_session,
    validate_incident_has_alert_lineage,
)

BLOCKED = "BLOCKED"
OK      = "OK"


class IncidentManager:
    """
    Manages incident lifecycle: OPEN → INVESTIGATING → MITIGATED → RESOLVED → CLOSED
    - CLOSED cannot re-open
    - RESOLVED cannot jump directly to OPEN
    - Each transition requires a reason
    """

    def __init__(self):
        self._incidents: Dict[str, SessionIncident] = {}

    def open(
        self,
        title:             str,
        category:          IncidentCategory,
        severity:          AlertSeverity,
        affected_sessions: List[str],
        alert_ids:         List[str],
        summary:           str = "",
        runbook_id:        str = "",
        incident_id:       Optional[str] = None,
    ) -> Tuple[str, object]:
        ok, msg = validate_incident_has_affected_session(affected_sessions)
        if not ok:
            return BLOCKED, msg

        ok, msg = validate_incident_has_alert_lineage(alert_ids)
        if not ok:
            return BLOCKED, msg

        inc = SessionIncident(
            incident_id=incident_id or _new_id("inc_"),
            category=category,
            severity=severity,
            status=IncidentStatus.OPEN,
            title=title,
            summary=summary,
            affected_sessions=list(affected_sessions),
            opened_at=_now_utc(),
            alert_ids=list(alert_ids),
            runbook_id=runbook_id,
        )
        self._incidents[inc.incident_id] = inc
        return OK, inc

    def transition(
        self,
        incident_id: str,
        target:      IncidentStatus,
        reason:      str,
    ) -> Tuple[str, str]:
        if not reason:
            return BLOCKED, "Transition requires a reason — BLOCKED"

        inc = self._incidents.get(incident_id)
        if inc is None:
            return BLOCKED, f"Incident not found: {incident_id}"

        ok, msg = validate_incident_transition(inc.status, target)
        if not ok:
            return BLOCKED, msg

        now = _now_utc()
        inc.status = target
        if target == IncidentStatus.INVESTIGATING:
            inc.investigating_at = now
        elif target == IncidentStatus.MITIGATED:
            inc.mitigated_at = now
        elif target == IncidentStatus.RESOLVED:
            inc.resolved_at = now
            inc.resolution = reason
        elif target == IncidentStatus.CLOSED:
            inc.closed_at = now

        return OK, f"Incident {incident_id} → {target}"

    def get(self, incident_id: str) -> Optional[SessionIncident]:
        return self._incidents.get(incident_id)

    def list_open(self) -> List[SessionIncident]:
        return [i for i in self._incidents.values()
                if i.status not in (IncidentStatus.RESOLVED, IncidentStatus.CLOSED)]

    def list_all(self) -> List[SessionIncident]:
        return list(self._incidents.values())

    def count(self) -> int:
        return len(self._incidents)


__all__ = ["IncidentManager", "BLOCKED", "OK"]
