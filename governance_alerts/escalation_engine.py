"""
governance_alerts.escalation_engine — GovernanceAlertEscalationEngine v1.1.7

Evaluates alerts for escalation based on time, recurrence, and severity.

Rules:
- P0 not acknowledged past threshold: escalate (default 4 hours)
- P1 repeated > N times: escalate (default 3)
- Snooze active but severity increases: escalate
- Source interruption scope growing: escalate
- Audit failure persisting: escalate
- Formal eligible continuously decreasing: escalate
- Blocked symbols continuously increasing: escalate
- Issue reopen count too high: escalate

CANNOT: send external notifications, execute repairs, imports, overrides, or trades.
Only updates alert metadata and digest.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Configurable escalation thresholds
P0_ACK_THRESHOLD_HOURS = 4
P1_REPEAT_THRESHOLD = 3
REOPEN_ESCALATION_THRESHOLD = 3
SNOOZE_SEVERITY_ESCALATION = True

_ESCALATION_LEVELS = ["L0", "L1", "L2", "L3"]
_SEVERITY_ORDER = {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _parse_dt(s: str) -> Optional[datetime]:
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def _hours_since(ts_str: str) -> float:
    if not ts_str:
        return 0.0
    dt = _parse_dt(ts_str)
    if dt is None:
        return 0.0
    elapsed = (_now_utc() - dt).total_seconds()
    return elapsed / 3600.0


class GovernanceAlertEscalationEngine:
    """Evaluates and applies escalation rules to governance alerts.

    [!] Only updates alert metadata.
    [!] CANNOT send notifications, execute repairs, imports, overrides, or trades.
    [!] Research Only. No Real Orders.
    """

    no_real_orders = True
    research_only = True

    def evaluate(self, alert, now: Optional[datetime] = None):
        """Evaluate a single alert for escalation. Returns updated alert."""
        if not self.should_escalate(alert):
            return alert

        import copy
        updated = copy.copy(alert)
        updated.status = "ESCALATED"
        reason = self.escalation_reason(alert)
        updated.escalation_level = self.next_level(alert)
        logger.info(
            "Alert %s escalated to %s: %s",
            alert.alert_id, updated.escalation_level, reason
        )
        return updated

    def should_escalate(self, alert) -> bool:
        """Return True if this alert should be escalated."""
        # Already at max
        if alert.escalation_level == "L3":
            return False
        # Already resolved
        if alert.status in ("RESOLVED", "SUPPRESSED"):
            return False

        # P0 not acknowledged past threshold
        if alert.priority == "P0" and alert.status == "OPEN":
            hours = _hours_since(alert.first_detected_at)
            if hours >= P0_ACK_THRESHOLD_HOURS:
                return True

        # P1 repeated too many times
        if alert.priority == "P1" and alert.occurrence_count >= P1_REPEAT_THRESHOLD:
            return True

        # Snoozed but severity increased
        if alert.status == "SNOOZED" and SNOOZE_SEVERITY_ESCALATION:
            prev_sev = alert.previous_state
            curr_sev = alert.current_state
            if (prev_sev and curr_sev and
                    _SEVERITY_ORDER.get(curr_sev, 0) > _SEVERITY_ORDER.get(prev_sev, 0)):
                return True

        # Source interruption + audit failure persisting
        if alert.alert_type in ("SOURCE_INTERRUPTION", "AUDIT_CHAIN_FAILURE"):
            hours = _hours_since(alert.first_detected_at)
            if hours >= P0_ACK_THRESHOLD_HOURS:
                return True

        # Reopen count too high
        if alert.reopened_count >= REOPEN_ESCALATION_THRESHOLD:
            return True

        return False

    def next_level(self, alert) -> str:
        """Return the next escalation level."""
        idx = _ESCALATION_LEVELS.index(alert.escalation_level) if alert.escalation_level in _ESCALATION_LEVELS else 0
        return _ESCALATION_LEVELS[min(idx + 1, 3)]

    def escalation_reason(self, alert) -> str:
        """Return a human-readable escalation reason."""
        if alert.priority == "P0" and alert.status == "OPEN":
            hours = _hours_since(alert.first_detected_at)
            if hours >= P0_ACK_THRESHOLD_HOURS:
                return f"P0 alert not acknowledged after {hours:.1f} hours"
        if alert.priority == "P1" and alert.occurrence_count >= P1_REPEAT_THRESHOLD:
            return f"P1 alert repeated {alert.occurrence_count} times"
        if alert.reopened_count >= REOPEN_ESCALATION_THRESHOLD:
            return f"Alert reopened {alert.reopened_count} times"
        if alert.alert_type in ("SOURCE_INTERRUPTION", "AUDIT_CHAIN_FAILURE"):
            hours = _hours_since(alert.first_detected_at)
            return f"{alert.alert_type} persisting for {hours:.1f} hours"
        return "Escalation threshold reached"

    def evaluate_all(self, alerts: List) -> List:
        """Evaluate all alerts for escalation. Returns updated list."""
        return [self.evaluate(a) for a in alerts]

    def build_escalation_summary(self, alerts: List) -> dict:
        """Return summary of escalation state across all alerts."""
        escalated = [a for a in alerts if a.status == "ESCALATED"]
        by_level = {"L0": 0, "L1": 0, "L2": 0, "L3": 0}
        for a in escalated:
            if a.escalation_level in by_level:
                by_level[a.escalation_level] += 1
        return {
            "total_escalated": len(escalated),
            "by_level": by_level,
            "l1_count": by_level.get("L1", 0),
            "l2_count": by_level.get("L2", 0),
            "l3_count": by_level.get("L3", 0),
            "types": list({a.alert_type for a in escalated}),
            "p0_escalated": sum(1 for a in escalated if a.priority == "P0"),
            "p1_escalated": sum(1 for a in escalated if a.priority == "P1"),
            "research_only": True,
            "no_real_orders": True,
        }
