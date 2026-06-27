"""
paper_trading/failure_validation/alert_v165.py — Alert generation validation v1.6.5.
[!] Research Only. No Real Orders. Not Investment Advice. No external notification.
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.failure_validation.enums_v165 import FailureSeverity

PAPER_ONLY = True
RESEARCH_ONLY = True
EXTERNAL_NOTIFICATION_ENABLED = False


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class SimulatedAlert:
    alert_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    severity: FailureSeverity = FailureSeverity.LOW
    scenario_id: str = ""
    generated_at: datetime = field(default_factory=_utcnow)
    acknowledged: bool = False
    acknowledged_at: Optional[datetime] = None

    def acknowledge(self) -> None:
        self.acknowledged = True
        self.acknowledged_at = _utcnow()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "title": self.title,
            "severity": self.severity.value,
            "scenario_id": self.scenario_id,
            "acknowledged": self.acknowledged,
        }


class AlertRegistry:
    """In-memory alert registry for simulated failure alerts."""

    def __init__(self) -> None:
        self._alerts: List[SimulatedAlert] = []

    def add(self, alert: SimulatedAlert) -> None:
        self._alerts.append(alert)

    def all(self) -> List[SimulatedAlert]:
        return list(self._alerts)

    def unacknowledged(self) -> List[SimulatedAlert]:
        return [a for a in self._alerts if not a.acknowledged]

    def count(self) -> int:
        return len(self._alerts)

    def acknowledge_all(self) -> int:
        count = 0
        for a in self._alerts:
            if not a.acknowledged:
                a.acknowledge()
                count += 1
        return count


def generate_alert(scenario_id: str, title: str, severity: FailureSeverity) -> SimulatedAlert:
    assert not EXTERNAL_NOTIFICATION_ENABLED, "External notification must never be enabled"
    return SimulatedAlert(title=title, severity=severity, scenario_id=scenario_id)
