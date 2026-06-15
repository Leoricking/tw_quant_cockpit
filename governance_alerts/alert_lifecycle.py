"""
governance_alerts.alert_lifecycle — GovernanceAlertLifecycle v1.1.7

Manages alert status transitions with append-only audit trail.

Rules:
- ALL transitions: append-only audit, no delete history
- RESOLVED = alert metadata resolved only; if source issue remains → next scan reopens
- P0 cannot be permanently suppressed
- FUTURE_DATE and AUDIT_CHAIN_FAILURE cannot be permanently suppressed
- Does NOT mean data is fixed; does NOT execute any source commands

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Valid transitions: from_status → allowed to_statuses
_VALID_TRANSITIONS: Dict[str, List[str]] = {
    "OPEN": ["ACKNOWLEDGED", "SNOOZED", "ESCALATED", "RESOLVED", "SUPPRESSED"],
    "ACKNOWLEDGED": ["SNOOZED", "ESCALATED", "RESOLVED", "REOPENED", "SUPPRESSED"],
    "SNOOZED": ["OPEN", "ESCALATED", "RESOLVED"],
    "ESCALATED": ["ACKNOWLEDGED", "RESOLVED", "REOPENED"],
    "RESOLVED": ["REOPENED"],
    "SUPPRESSED": ["OPEN"],
    "REOPENED": ["ACKNOWLEDGED", "SNOOZED", "ESCALATED", "RESOLVED", "SUPPRESSED"],
    "BLOCKED": ["OPEN"],
}

# Types that can never be permanently suppressed
_NEVER_PERMANENT_SUPPRESS = {"AUDIT_CHAIN_FAILURE", "FUTURE_DATE", "DATE_REGRESSION"}


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


class GovernanceAlertLifecycle:
    """Manages alert state transitions with audit trail.

    [!] Metadata only. Does NOT fix source data. Does NOT execute commands.
    [!] Research Only. No Real Orders.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, store=None):
        self._store = store

    def _get_store(self):
        if self._store:
            return self._store
        try:
            from governance_alerts.alert_store import GovernanceAlertStore
            return GovernanceAlertStore()
        except Exception:
            return None

    def acknowledge(self, alert_id: str, actor: str = "user", note: str = ""):
        """Acknowledge an open alert. Metadata only."""
        return self.transition(
            alert_id, to_status="ACKNOWLEDGED", actor=actor,
            reason=f"Acknowledged by {actor}. {note}".strip(),
        )

    def snooze(self, alert_id: str, until: str, actor: str = "user", reason: str = ""):
        """Snooze an alert until a given ISO timestamp. P0 cannot be snoozed indefinitely."""
        alert = self._load_alert(alert_id)
        if alert is None:
            logger.warning("snooze: alert_id %s not found", alert_id)
            return None

        # P0 snooze limit enforcement
        if alert.priority == "P0":
            from governance_alerts.alert_policy import GovernanceAlertPolicy
            policy = GovernanceAlertPolicy()
            limit = policy.snooze_limit(alert.alert_type)
            if limit is None:
                logger.warning("P0 alert %s cannot be snoozed (no limit)", alert_id)
                return alert

        import copy
        updated = copy.copy(alert)
        updated.status = "SNOOZED"
        updated.snoozed_until = until
        self._save_alert(updated)

        self._record_transition(
            alert_id=alert_id,
            from_status=alert.status,
            to_status="SNOOZED",
            actor=actor,
            reason=reason or f"Snoozed until {until}",
        )
        return updated

    def escalate(self, alert_id: str, actor: str = "system", reason: str = ""):
        """Escalate an alert to the next escalation level."""
        return self.transition(
            alert_id, to_status="ESCALATED", actor=actor,
            reason=reason or "Escalated",
        )

    def resolve(self, alert_id: str, actor: str = "user", note: str = ""):
        """Resolve an alert. Note: resolution is metadata only; if source issue persists, next scan will reopen."""
        alert = self._load_alert(alert_id)
        if alert is None:
            return None

        import copy
        updated = copy.copy(alert)
        updated.status = "RESOLVED"
        updated.resolved_at = _now_utc()
        updated.resolution_note = note
        self._save_alert(updated)

        self._record_transition(
            alert_id=alert_id,
            from_status=alert.status,
            to_status="RESOLVED",
            actor=actor,
            reason=f"Resolved by {actor}. Note: {note}. [!] Metadata only — if source issue persists, alert will reopen on next scan.",
        )
        return updated

    def suppress(self, alert_id: str, actor: str = "user", reason: str = "", expires_at: Optional[str] = None):
        """Suppress an alert. P0 cannot be permanently suppressed."""
        alert = self._load_alert(alert_id)
        if alert is None:
            return None

        # P0 suppression rules
        if alert.priority == "P0":
            if expires_at is None:
                logger.warning("P0 alert %s cannot be permanently suppressed", alert_id)
                return alert
        # Never permanent suppress for critical types
        if alert.alert_type in _NEVER_PERMANENT_SUPPRESS and expires_at is None:
            logger.warning("Alert type %s cannot be permanently suppressed", alert.alert_type)
            return alert

        import copy
        updated = copy.copy(alert)
        updated.status = "SUPPRESSED"
        self._save_alert(updated)

        self._record_transition(
            alert_id=alert_id,
            from_status=alert.status,
            to_status="SUPPRESSED",
            actor=actor,
            reason=reason,
            note=f"Expires: {expires_at}" if expires_at else "No expiry set",
        )
        return updated

    def reopen(self, alert_id: str, reason: str = ""):
        """Reopen a resolved alert (e.g., source issue recurred)."""
        return self.transition(
            alert_id, to_status="REOPENED", actor="system",
            reason=reason or "Source issue recurred; alert reopened by scan.",
        )

    def transition(self, alert_id: str, to_status: str, actor: str = "", reason: str = "", note: str = ""):
        """Apply a state transition to an alert."""
        alert = self._load_alert(alert_id)
        if alert is None:
            logger.warning("transition: alert_id %s not found", alert_id)
            return None

        if not self.validate_transition(alert.status, to_status):
            logger.warning(
                "Invalid transition %s → %s for alert %s",
                alert.status, to_status, alert_id
            )
            return alert

        import copy
        updated = copy.copy(alert)
        from_status = alert.status
        updated.status = to_status

        if to_status == "RESOLVED":
            updated.resolved_at = _now_utc()
        if to_status == "ACKNOWLEDGED":
            updated.acknowledged_at = _now_utc()
            updated.acknowledged_by = actor
        if to_status == "REOPENED":
            updated.reopened_count = alert.reopened_count + 1
        if to_status in ("ESCALATED",):
            levels = ["L0", "L1", "L2", "L3"]
            idx = levels.index(alert.escalation_level) if alert.escalation_level in levels else 0
            updated.escalation_level = levels[min(idx + 1, 3)]

        self._save_alert(updated)
        self._record_transition(
            alert_id=alert_id,
            from_status=from_status,
            to_status=to_status,
            actor=actor,
            reason=reason,
            note=note,
        )
        return updated

    def validate_transition(self, from_status: str, to_status: str) -> bool:
        allowed = _VALID_TRANSITIONS.get(from_status, [])
        return to_status in allowed

    def list_allowed_transitions(self, status: str) -> List[str]:
        return _VALID_TRANSITIONS.get(status, [])

    def _load_alert(self, alert_id: str):
        store = self._get_store()
        if store is None:
            return None
        try:
            return store.get_alert(alert_id)
        except Exception as exc:
            logger.warning("_load_alert %s: %s", alert_id, exc)
            return None

    def _save_alert(self, alert) -> None:
        store = self._get_store()
        if store is None:
            return
        try:
            store.upsert_alert(alert)
        except Exception as exc:
            logger.warning("_save_alert: %s", exc)

    def _record_transition(
        self,
        alert_id: str,
        from_status: str,
        to_status: str,
        actor: str,
        reason: str,
        note: str = "",
    ) -> None:
        from governance_alerts.alert_schema import AlertStateTransition
        transition = AlertStateTransition(
            transition_id=_new_uuid(),
            alert_id=alert_id,
            from_status=from_status,
            to_status=to_status,
            actor=actor or "system",
            reason=reason,
            timestamp=_now_utc(),
            metadata={"note": note} if note else {},
        )
        store = self._get_store()
        if store is None:
            return
        try:
            store.append_transition(transition)
        except Exception as exc:
            logger.warning("_record_transition: %s", exc)
