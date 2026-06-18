"""
gui/replay_registry_audit_panel.py — Registry Audit Log panel v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayRegistryAuditPanel:
    """
    Displays append-only registry audit log events.
    Filters by event_type, dataset_id, session_id, status.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    COLUMNS = ["timestamp", "event_type", "dataset_id", "session_id",
               "fingerprint", "status", "elapsed_seconds"]

    def __init__(self) -> None:
        self._events: Optional[Any] = None

    def _get_events(self) -> Optional[Any]:
        if self._events is None:
            try:
                from replay.registry_events import ReplayRegistryEvents
                self._events = ReplayRegistryEvents()
            except Exception as exc:
                logger.warning("RegistryEvents unavailable: %s", exc)
        return self._events

    def list_events(self, **kwargs) -> List[Dict[str, Any]]:
        ev = self._get_events()
        if ev is None:
            return []
        try:
            return ev.list_events(**kwargs)
        except Exception as exc:
            logger.warning("list_events failed: %s", exc)
            return []

    def filter_by_dataset(self, dataset_id: str) -> List[Dict[str, Any]]:
        return self.list_events(dataset_id=dataset_id)

    def filter_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        return self.list_events(session_id=session_id)

    def filter_by_event_type(self, event_type: str) -> List[Dict[str, Any]]:
        return self.list_events(event_type=event_type)

    def summary(self) -> str:
        ev = self._get_events()
        if ev is None:
            return "Audit log unavailable."
        try:
            return ev.summary()
        except Exception as exc:
            logger.warning("summary failed: %s", exc)
            return f"Audit summary failed: {exc}"
