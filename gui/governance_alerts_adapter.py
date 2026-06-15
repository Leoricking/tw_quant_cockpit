"""
gui/governance_alerts_adapter.py — GovernanceAlertsAdapter for TW Quant Cockpit v1.1.7

Lightweight adapter connecting the governance_alerts subsystem to the GUI.
Uses navigation registry — does NOT duplicate Alert Center logic.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] External Notification Send DISABLED. No broker. No trading.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
EXTERNAL_NOTIFICATION_SEND_ENABLED = False


class GovernanceAlertsAdapter:
    """Adapter between governance_alerts subsystem and GUI panels.

    Provides safe read-only data for display without triggering any
    writes, repairs, imports, or external notifications.

    [!] Research Only. No Real Orders.
    """

    no_real_orders = True
    research_only = True
    external_notification_send_enabled = False

    def __init__(self) -> None:
        self._query = None
        self._policy = None
        self._loaded = False
        self._load_error: Optional[str] = None

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        try:
            from governance_alerts.alert_query import (
                latest_alerts, alerts_by_priority, alerts_by_status,
                alert_history, open_alert_count,
            )
            self._query = {
                "latest_alerts": latest_alerts,
                "alerts_by_priority": alerts_by_priority,
                "alerts_by_status": alerts_by_status,
                "alert_history": alert_history,
                "open_alert_count": open_alert_count,
            }
            from governance_alerts.alert_policy import GovernanceAlertPolicy
            self._policy = GovernanceAlertPolicy()
            self._loaded = True
        except Exception as exc:
            self._load_error = str(exc)
            logger.warning("GovernanceAlertsAdapter: failed to load: %s", exc)

    def summary(self) -> Dict[str, Any]:
        """Return summary counts for the governance alerts summary bar."""
        self._ensure_loaded()
        result: Dict[str, Any] = {
            "open": 0,
            "p0": 0,
            "p1": 0,
            "escalated": 0,
            "snoozed": 0,
            "reopened_today": 0,
            "checklist_completion": 0.0,
            "latest_digest": "N/A",
            "available": self._loaded,
            "error": self._load_error or "",
            "no_real_orders": True,
            "research_only": True,
        }
        if not self._loaded:
            return result
        try:
            q = self._query
            open_alerts = q["alerts_by_status"]("OPEN", limit=200)
            escalated = q["alerts_by_status"]("ESCALATED", limit=200)
            snoozed = q["alerts_by_status"]("SNOOZED", limit=200)
            reopened = q["alerts_by_status"]("REOPENED", limit=200)
            p0 = q["alerts_by_priority"]("P0", status="OPEN", limit=200)
            p1 = q["alerts_by_priority"]("P1", status="OPEN", limit=200)

            result["open"] = len(open_alerts)
            result["p0"] = len(p0)
            result["p1"] = len(p1)
            result["escalated"] = len(escalated)
            result["snoozed"] = len(snoozed)
            result["reopened_today"] = len(reopened)
        except Exception as exc:
            logger.warning("GovernanceAlertsAdapter.summary failed: %s", exc)
            result["error"] = str(exc)
        return result

    def open_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Return list of open alert dicts for display."""
        self._ensure_loaded()
        if not self._loaded:
            return []
        try:
            alerts = self._query["latest_alerts"](status="OPEN", limit=limit)
            return [a.to_dict() if hasattr(a, "to_dict") else a for a in alerts]
        except Exception as exc:
            logger.warning("GovernanceAlertsAdapter.open_alerts failed: %s", exc)
            return []

    def escalated_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Return list of escalated alert dicts for display."""
        self._ensure_loaded()
        if not self._loaded:
            return []
        try:
            alerts = self._query["alerts_by_status"]("ESCALATED", limit=limit)
            return [a.to_dict() if hasattr(a, "to_dict") else a for a in alerts]
        except Exception as exc:
            logger.warning("GovernanceAlertsAdapter.escalated_alerts failed: %s", exc)
            return []

    def latest_digest_summary(self) -> str:
        """Return a one-line summary of the latest digest, or 'N/A'."""
        try:
            from governance_alerts.alert_store import GovernanceAlertStore
            store = GovernanceAlertStore()
            digests = store.load_digests(limit=1)
            if digests:
                d = digests[0]
                return (
                    f"[{d.get('digest_type', 'DAILY')}] "
                    f"P0={d.get('p0_count', 0)} P1={d.get('p1_count', 0)} "
                    f"New={d.get('new_alerts', 0)} "
                    f"Status={d.get('overall_status', 'UNKNOWN')}"
                )
        except Exception as exc:
            logger.debug("GovernanceAlertsAdapter.latest_digest_summary: %s", exc)
        return "N/A"

    def checklist_completion(self) -> float:
        """Return latest daily checklist completion rate (0.0–1.0)."""
        try:
            from governance_alerts.alert_store import GovernanceAlertStore
            store = GovernanceAlertStore()
            checklists = store.load_checklists(limit=1)
            if checklists:
                return float(checklists[0].get("completion_rate", 0.0))
        except Exception as exc:
            logger.debug("GovernanceAlertsAdapter.checklist_completion: %s", exc)
        return 0.0
