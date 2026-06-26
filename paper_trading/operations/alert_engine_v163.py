"""
Alert Engine v1.6.3 — Deterministic, idempotent, dedup, suppression.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
No external notification. No PagerDuty.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import AlertSeverity, AlertStatus
from paper_trading.operations.models_v163 import SessionAlert, _new_id, _now_utc
from paper_trading.operations.alert_rule_v163 import AlertRule


class AlertEngine:
    """
    Rules:
    - Same dedup_key: if active alert exists → do not re-create
    - Severity upgrade allowed on active alert
    - Resolved alert: new event can re-open
    - Suppression is journaled
    - No duplicate critical storm
    - No infinite alert generation
    """

    def __init__(self, clock: Optional[Callable[[], datetime]] = None):
        self._clock   = clock or _now_utc
        self._alerts: Dict[str, SessionAlert] = {}      # alert_id → alert
        self._dedup:  Dict[str, str]          = {}      # dedup_key → alert_id
        self._suppression_journal: List[dict] = []

    # ------------------------------------------------------------------
    def fire(
        self,
        rule: AlertRule,
        session_id:    str,
        message:       str = "",
        metric_ids:    Optional[List[str]] = None,
    ) -> Tuple[str, SessionAlert]:
        """
        Returns (action, alert):
          action in {'created', 'upgraded', 'suppressed', 'deduped'}
        """
        if not rule.enabled:
            return "suppressed", self._make_dummy(rule, session_id, message)

        dedup_key = f"{rule.dedup_key}:{session_id}"

        # Check suppression window
        existing_id = self._dedup.get(dedup_key)
        if existing_id and existing_id in self._alerts:
            existing = self._alerts[existing_id]
            status = existing.status

            if status == AlertStatus.SUPPRESSED:
                return "suppressed", existing

            if status in (AlertStatus.OPEN, AlertStatus.ACKNOWLEDGED):
                # Severity upgrade
                if AlertSeverity.severity_rank(rule.severity) > AlertSeverity.severity_rank(existing.severity):
                    existing.severity = rule.severity
                    return "upgraded", existing
                return "deduped", existing

            if status in (AlertStatus.RESOLVED, AlertStatus.EXPIRED):
                # Can re-open
                pass  # fall through to create new

        alert = SessionAlert(
            alert_id=_new_id("alt_"),
            rule_id=rule.rule_id,
            severity=rule.severity,
            status=AlertStatus.OPEN,
            session_id=session_id,
            category=rule.category,
            title=rule.name,
            message=message,
            opened_at=self._clock(),
            dedup_key=dedup_key,
            source_metric_ids=metric_ids or [],
            research_only=True,
        )
        self._alerts[alert.alert_id] = alert
        self._dedup[dedup_key] = alert.alert_id
        return "created", alert

    def acknowledge(self, alert_id: str, reason: str = "") -> bool:
        alert = self._alerts.get(alert_id)
        if alert is None or alert.status != AlertStatus.OPEN:
            return False
        alert.status = AlertStatus.ACKNOWLEDGED
        alert.acknowledged_at = self._clock()
        return True

    def resolve(self, alert_id: str) -> bool:
        alert = self._alerts.get(alert_id)
        if alert is None or alert.status in (AlertStatus.RESOLVED, AlertStatus.EXPIRED):
            return False
        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = self._clock()
        return True

    def suppress(self, alert_id: str, reason: str = "") -> bool:
        alert = self._alerts.get(alert_id)
        if alert is None:
            return False
        alert.status = AlertStatus.SUPPRESSED
        self._suppression_journal.append({
            "alert_id": alert_id,
            "reason":   reason,
            "at":       self._clock().isoformat(),
        })
        return True

    def list_open(self) -> List[SessionAlert]:
        return [a for a in self._alerts.values() if a.status == AlertStatus.OPEN]

    def list_critical(self) -> List[SessionAlert]:
        return [a for a in self._alerts.values()
                if a.status == AlertStatus.OPEN and a.severity == AlertSeverity.CRITICAL]

    def get(self, alert_id: str) -> Optional[SessionAlert]:
        return self._alerts.get(alert_id)

    def count(self) -> int:
        return len(self._alerts)

    def suppression_journal(self) -> List[dict]:
        return list(self._suppression_journal)

    # ------------------------------------------------------------------
    def _make_dummy(self, rule: AlertRule, session_id: str, message: str) -> SessionAlert:
        return SessionAlert(
            alert_id=_new_id("alt_"),
            rule_id=rule.rule_id,
            severity=rule.severity,
            status=AlertStatus.SUPPRESSED,
            session_id=session_id,
            message=message,
            research_only=True,
        )


# Patch AlertSeverity with severity_rank helper
def _sev_rank(sev: AlertSeverity) -> int:
    return {"INFO": 0, "WARNING": 1, "ERROR": 2, "CRITICAL": 3}.get(sev.value, 0)

AlertSeverity.severity_rank = staticmethod(_sev_rank)


__all__ = ["AlertEngine"]
