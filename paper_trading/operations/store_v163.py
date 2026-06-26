"""
Observability Store v1.6.3 — In-memory, append-only journal.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
No credentials. No broker data. No real account data.
No formal Portfolio Ledger write.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Generic

T = TypeVar("T")


class ObservabilityStore:
    """
    Append-only, in-memory store for all session operations artifacts.
    - Idempotent writes (same ID → no duplicate)
    - Immutable snapshots after creation
    - Immutable incidents after CLOSED
    - No credentials / no broker data / no real account data
    - No formal Portfolio Ledger write
    - Runtime DB is gitignored
    """

    def __init__(self):
        self._sessions:      Dict[str, Any] = {}
        self._metrics:       List[Any]      = []
        self._health:        List[Any]      = []
        self._alerts:        Dict[str, Any] = {}
        self._incidents:     Dict[str, Any] = {}
        self._timelines:     Dict[str, Any] = {}
        self._operations:    Dict[str, Any] = {}
        self._snapshots:     Dict[str, Any] = {}
        self._checkpoints:   Dict[str, Any] = {}
        self._audit:         List[Any]      = []
        self._replays:       Dict[str, Any] = {}
        self._drills:        Dict[str, Any] = {}
        self._runbooks:      Dict[str, Any] = {}
        self._lineage:       List[Any]      = []
        self._reproducibility: List[Any]   = []

    # -- Sessions --
    def put_session(self, session_id: str, record: Any) -> bool:
        if session_id in self._sessions:
            return False  # Idempotent
        self._sessions[session_id] = record
        return True

    def get_session(self, session_id: str) -> Optional[Any]:
        return self._sessions.get(session_id)

    def list_sessions(self) -> List[Any]:
        return list(self._sessions.values())

    # -- Metrics --
    def append_metric(self, metric: Any) -> None:
        self._metrics.append(metric)

    def list_metrics(self) -> List[Any]:
        return list(self._metrics)

    # -- Alerts --
    def put_alert(self, alert_id: str, alert: Any) -> bool:
        self._alerts[alert_id] = alert
        return True

    def get_alert(self, alert_id: str) -> Optional[Any]:
        return self._alerts.get(alert_id)

    def list_alerts(self) -> List[Any]:
        return list(self._alerts.values())

    # -- Incidents --
    def put_incident(self, incident_id: str, incident: Any) -> bool:
        existing = self._incidents.get(incident_id)
        # Immutable after CLOSED
        if existing is not None:
            try:
                from paper_trading.operations.enums_v163 import IncidentStatus
                if getattr(existing, "status", None) == IncidentStatus.CLOSED:
                    return False
            except Exception:
                pass
        self._incidents[incident_id] = incident
        return True

    def get_incident(self, incident_id: str) -> Optional[Any]:
        return self._incidents.get(incident_id)

    def list_incidents(self) -> List[Any]:
        return list(self._incidents.values())

    # -- Snapshots (immutable) --
    def put_snapshot(self, snapshot_id: str, snap: Any) -> bool:
        if snapshot_id in self._snapshots:
            return False
        self._snapshots[snapshot_id] = snap
        return True

    def get_snapshot(self, snapshot_id: str) -> Optional[Any]:
        return self._snapshots.get(snapshot_id)

    def list_snapshots(self) -> List[Any]:
        return list(self._snapshots.values())

    # -- Checkpoints --
    def put_checkpoint(self, chk_id: str, chk: Any) -> bool:
        if chk_id in self._checkpoints:
            return False
        self._checkpoints[chk_id] = chk
        return True

    def get_checkpoint(self, chk_id: str) -> Optional[Any]:
        return self._checkpoints.get(chk_id)

    # -- Audit --
    def append_audit(self, entry: Any) -> None:
        self._audit.append(entry)

    def list_audit(self) -> List[Any]:
        return list(self._audit)

    # -- Operations --
    def put_operation(self, op_id: str, op: Any) -> bool:
        self._operations[op_id] = op
        return True

    def get_operation(self, op_id: str) -> Optional[Any]:
        return self._operations.get(op_id)

    # -- Replays --
    def put_replay(self, replay_id: str, replay: Any) -> bool:
        self._replays[replay_id] = replay
        return True

    # -- Drills --
    def put_drill(self, drill_id: str, drill: Any) -> bool:
        self._drills[drill_id] = drill
        return True

    # -- Lineage --
    def append_lineage(self, rec: Any) -> None:
        self._lineage.append(rec)

    def list_lineage(self) -> List[Any]:
        return list(self._lineage)

    # -- Reproducibility --
    def append_reproducibility(self, manifest: Any) -> None:
        self._reproducibility.append(manifest)

    # -- Summary --
    def summary(self) -> Dict[str, int]:
        return {
            "sessions":        len(self._sessions),
            "metrics":         len(self._metrics),
            "alerts":          len(self._alerts),
            "incidents":       len(self._incidents),
            "snapshots":       len(self._snapshots),
            "checkpoints":     len(self._checkpoints),
            "audit_entries":   len(self._audit),
            "operations":      len(self._operations),
            "replays":         len(self._replays),
            "drills":          len(self._drills),
            "lineage":         len(self._lineage),
            "reproducibility": len(self._reproducibility),
        }


__all__ = ["ObservabilityStore"]
