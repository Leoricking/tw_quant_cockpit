"""
gui/replay_session_registry_panel.py — Session Registry panel v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplaySessionRegistryPanel:
    """
    Displays the session registry with status, bindings, and orphan detection.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    COLUMNS = [
        "session_id", "scenario_id", "challenge_id", "mode",
        "status", "dataset_id", "dataset_version", "binding_status",
        "session_fingerprint",
    ]

    def __init__(self) -> None:
        self._registry: Optional[Any] = None
        self._query: Optional[Any] = None

    def _get_query(self) -> Optional[Any]:
        if self._query is None:
            try:
                from replay.session_registry_v128 import ReplaySessionRegistryV128
                from replay.session_registry_query import ReplaySessionRegistryQuery
                self._registry = ReplaySessionRegistryV128()
                self._query = ReplaySessionRegistryQuery(self._registry)
            except Exception as exc:
                logger.warning("SessionRegistryQuery unavailable: %s", exc)
        return self._query

    def get_all_sessions(self) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.sessions()
        except Exception as exc:
            logger.warning("get_all_sessions failed: %s", exc)
            return []

    def search_sessions(self, query: str) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.search(query)
        except Exception as exc:
            logger.warning("search_sessions failed: %s", exc)
            return []

    def get_orphaned_sessions(self) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.orphaned()
        except Exception as exc:
            logger.warning("get_orphaned_sessions failed: %s", exc)
            return []

    def get_broken_references(self) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.broken_references()
        except Exception as exc:
            logger.warning("get_broken_references failed: %s", exc)
            return []

    def filter_by_dataset(self, dataset_id: str) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.by_dataset(dataset_id)
        except Exception as exc:
            logger.warning("filter_by_dataset failed: %s", exc)
            return []

    def filter_by_status(self, status: str) -> List[Dict[str, Any]]:
        q = self._get_query()
        if q is None:
            return []
        try:
            return q.by_status(status)
        except Exception as exc:
            logger.warning("filter_by_status failed: %s", exc)
            return []

    def summary(self) -> Dict[str, Any]:
        sessions  = self.get_all_sessions()
        orphaned  = self.get_orphaned_sessions()
        broken    = self.get_broken_references()
        return {
            "total":          len(sessions),
            "orphaned_count": len(orphaned),
            "broken_count":   len(broken),
            "research_only":  True,
            "no_real_orders": True,
        }
