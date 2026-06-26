"""
Session Operations Validation v1.6.3

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from typing import Tuple

from paper_trading.operations.enums_v163 import (
    ManagedSessionType, OperationalStatus, IncidentStatus,
    VALID_INCIDENT_TRANSITIONS, FORBIDDEN_ALERT_CHANNELS,
)


def validate_session_type(session_type) -> Tuple[bool, str]:
    try:
        ManagedSessionType(session_type)
        return True, "ok"
    except (ValueError, KeyError):
        return False, f"Unknown session type: {session_type} — BLOCKED"


def validate_managed_session_id(session_id: str, existing_ids: set) -> Tuple[bool, str]:
    if not session_id:
        return False, "Missing session ID — BLOCKED"
    if session_id in existing_ids:
        return False, f"Duplicate managed session ID: {session_id} — BLOCKED"
    return True, "ok"


def validate_version(version: str) -> Tuple[bool, str]:
    if not version:
        return False, "Missing version — BLOCKED"
    return True, "ok"


def validate_no_broker_session(metadata: dict) -> Tuple[bool, str]:
    if metadata.get("broker_session"):
        return False, "Broker session not allowed — BLOCKED"
    if metadata.get("real_account_session"):
        return False, "Real account session not allowed — BLOCKED"
    if metadata.get("production_session"):
        return False, "Production session not allowed — BLOCKED"
    return True, "ok"


def validate_parent_exists(parent_id, known_ids: set) -> Tuple[bool, str]:
    if parent_id is None:
        return True, "ok"
    if parent_id not in known_ids:
        return False, f"Missing parent session: {parent_id} — BLOCKED"
    return True, "ok"


def validate_no_circular_dependency(session_id: str, parent_id, ancestry: dict) -> Tuple[bool, str]:
    if parent_id is None:
        return True, "ok"
    visited = set()
    current = parent_id
    while current is not None:
        if current == session_id:
            return False, f"Circular dependency detected for {session_id} — BLOCKED"
        if current in visited:
            break
        visited.add(current)
        current = ancestry.get(current)
    return True, "ok"


def validate_incident_transition(current: IncidentStatus, target: IncidentStatus) -> Tuple[bool, str]:
    allowed = VALID_INCIDENT_TRANSITIONS.get(current, set())
    if target not in allowed:
        return False, f"Invalid transition {current} → {target} — BLOCKED"
    return True, "ok"


def validate_alert_channel(channel: str) -> Tuple[bool, str]:
    if channel in FORBIDDEN_ALERT_CHANNELS:
        return False, f"Forbidden alert channel: {channel} — BLOCKED"
    return True, "ok"


def validate_threshold_ordering(warning, degraded, critical) -> Tuple[bool, str]:
    try:
        w, d, c = float(warning), float(degraded), float(critical)
        if not (w <= d <= c):
            return False, f"Invalid threshold ordering: {w} <= {d} <= {c} must hold — BLOCKED"
        return True, "ok"
    except (TypeError, ValueError) as e:
        return False, f"Threshold values must be numeric: {e} — BLOCKED"


def validate_no_future_timestamp(ts, clock) -> Tuple[bool, str]:
    if ts is None:
        return True, "ok"
    if ts > clock:
        return False, f"Future timestamp blocked: {ts} > {clock}"
    return True, "ok"


def validate_incident_has_affected_session(affected_sessions: list) -> Tuple[bool, str]:
    if not affected_sessions:
        return False, "Incident must have at least one affected session — BLOCKED"
    return True, "ok"


def validate_incident_has_alert_lineage(alert_ids: list) -> Tuple[bool, str]:
    if not alert_ids:
        return False, "Incident must have alert lineage — BLOCKED"
    return True, "ok"


__all__ = [
    "validate_session_type", "validate_managed_session_id", "validate_version",
    "validate_no_broker_session", "validate_parent_exists", "validate_no_circular_dependency",
    "validate_incident_transition", "validate_alert_channel", "validate_threshold_ordering",
    "validate_no_future_timestamp", "validate_incident_has_affected_session",
    "validate_incident_has_alert_lineage",
]
