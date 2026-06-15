"""
governance_alerts.alert_query — Alert query functions for Governance Alerts v1.1.7

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _get_store():
    try:
        from governance_alerts.alert_store import GovernanceAlertStore
        return GovernanceAlertStore()
    except Exception as exc:
        logger.warning("alert_query: cannot load store: %s", exc)
        return None


def latest_alerts() -> List:
    store = _get_store()
    if store is None:
        return []
    return store.list_all_alerts()


def open_alerts() -> List:
    store = _get_store()
    if store is None:
        return []
    return store.list_open_alerts()


def alerts_by_priority(priority: str) -> List:
    store = _get_store()
    if store is None:
        return []
    return store.query_alerts(priority=priority)


def alerts_by_status(status: str) -> List:
    store = _get_store()
    if store is None:
        return []
    return store.query_alerts(status=status)


def alerts_by_type(alert_type: str) -> List:
    store = _get_store()
    if store is None:
        return []
    return store.query_alerts(alert_type=alert_type)


def alerts_by_symbol(symbol: str) -> List:
    store = _get_store()
    if store is None:
        return []
    return store.query_alerts(symbol=symbol)


def alerts_by_source(source: str) -> List:
    store = _get_store()
    if store is None:
        return []
    return store.query_alerts(source=source)


def p0_alerts() -> List:
    return alerts_by_priority("P0")


def p1_alerts() -> List:
    return alerts_by_priority("P1")


def escalated_alerts() -> List:
    return alerts_by_status("ESCALATED")


def snoozed_alerts() -> List:
    return alerts_by_status("SNOOZED")


def reopened_alerts() -> List:
    return alerts_by_status("REOPENED")


def latest_digest(digest_type: Optional[str] = None):
    store = _get_store()
    if store is None:
        return None
    return store.latest_digest(digest_type=digest_type)


def latest_checklist():
    store = _get_store()
    if store is None:
        return None
    return store.latest_checklist()


def alert_history(alert_id: str) -> List:
    store = _get_store()
    if store is None:
        return []
    return store.list_transitions(alert_id=alert_id)


def trend(days: int = 7) -> List[Dict]:
    """Return daily alert trend for the past N days."""
    all_alerts = latest_alerts()
    result = []
    now = datetime.now(timezone.utc)
    for i in range(days - 1, -1, -1):
        day = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        day_alerts = []
        for a in all_alerts:
            first = (a.first_detected_at or "")[:10]
            if first == day:
                day_alerts.append(a)
        result.append({
            "date": day,
            "total": len(day_alerts),
            "p0": sum(1 for a in day_alerts if a.priority == "P0"),
            "p1": sum(1 for a in day_alerts if a.priority == "P1"),
            "critical": sum(1 for a in day_alerts if a.severity == "CRITICAL"),
            "audit_failures": sum(1 for a in day_alerts if a.alert_type == "AUDIT_CHAIN_FAILURE"),
        })
    return result


def compare_days(date_a: str, date_b: str) -> Dict:
    """Compare alert state on two different dates."""
    all_alerts = latest_alerts()

    def _filter(date_str):
        return [a for a in all_alerts if (a.first_detected_at or "")[:10] == date_str]

    a_alerts = _filter(date_a)
    b_alerts = _filter(date_b)

    return {
        "date_a": date_a,
        "date_b": date_b,
        "a_total": len(a_alerts),
        "b_total": len(b_alerts),
        "a_p0": sum(1 for a in a_alerts if a.priority == "P0"),
        "b_p0": sum(1 for a in b_alerts if a.priority == "P0"),
        "a_p1": sum(1 for a in a_alerts if a.priority == "P1"),
        "b_p1": sum(1 for a in b_alerts if a.priority == "P1"),
        "delta_total": len(b_alerts) - len(a_alerts),
        "delta_p0": sum(1 for a in b_alerts if a.priority == "P0") - sum(1 for a in a_alerts if a.priority == "P0"),
        "research_only": True,
        "no_real_orders": True,
    }
