"""
paper_trading/failure_validation/incident_v165.py — Incident management simulation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. Simulation only.
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.failure_validation.enums_v165 import FailureSeverity

PAPER_ONLY = True
RESEARCH_ONLY = True


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class SimulatedIncident:
    incident_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    severity: FailureSeverity = FailureSeverity.MEDIUM
    scenario_id: str = ""
    alert_id: str = ""
    status: str = "OPEN"
    created_at: datetime = field(default_factory=_utcnow)
    resolved_at: Optional[datetime] = None
    timeline: List[Dict[str, Any]] = field(default_factory=list)

    def resolve(self, reason: str = "") -> None:
        self.status = "RESOLVED"
        self.resolved_at = _utcnow()
        self.timeline.append({"event": "RESOLVED", "reason": reason, "ts": _utcnow().isoformat()})

    def add_event(self, event: str, detail: str = "") -> None:
        self.timeline.append({"event": event, "detail": detail, "ts": _utcnow().isoformat()})

    def as_dict(self) -> Dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "title": self.title,
            "severity": self.severity.value,
            "status": self.status,
            "scenario_id": self.scenario_id,
            "timeline_events": len(self.timeline),
        }


class IncidentRegistry:
    """In-memory incident registry for simulated incidents."""

    def __init__(self) -> None:
        self._incidents: List[SimulatedIncident] = []

    def create(self, title: str, severity: FailureSeverity, scenario_id: str = "",
               alert_id: str = "") -> SimulatedIncident:
        inc = SimulatedIncident(title=title, severity=severity,
                                scenario_id=scenario_id, alert_id=alert_id)
        self._incidents.append(inc)
        return inc

    def open_incidents(self) -> List[SimulatedIncident]:
        return [i for i in self._incidents if i.status == "OPEN"]

    def count(self) -> int:
        return len(self._incidents)

    def all(self) -> List[SimulatedIncident]:
        return list(self._incidents)
