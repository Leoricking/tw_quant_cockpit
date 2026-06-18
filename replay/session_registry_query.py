"""
replay/session_registry_query.py — ReplaySessionRegistryQuery v1.2.8

Query interface for the session registry.

[!] Research Only. No Real Orders. Session Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplaySessionRegistryQuery:
    """
    Query interface for the session registry.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, registry=None):
        self._registry = registry

    def sessions(self, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.list(filters)

    def session(self, session_id: str) -> Optional[Any]:
        if self._registry is None:
            return None
        return self._registry.get(session_id)

    def bindings(self, session_id: str) -> List[Any]:
        return []  # via session_dataset_binding

    def lineage(self, session_id: str) -> Dict[str, Any]:
        if self._registry is None:
            return {"session_id": session_id}
        return self._registry.lineage(session_id)

    def orphaned(self) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.detect_orphans()

    def broken_references(self) -> List[Dict[str, Any]]:
        if self._registry is None:
            return []
        return self._registry.detect_broken_references()

    def by_dataset(self, dataset_id: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.filter(dataset_id=dataset_id)

    def by_scenario(self, scenario_id: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.filter(scenario_id=scenario_id)

    def by_challenge(self, challenge_id: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.filter(challenge_id=challenge_id)

    def by_symbol(self, symbol: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.filter(symbol=symbol)

    def by_status(self, status: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.filter(session_status=status)

    def by_mode(self, mode: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.filter(mode=mode)

    def search(self, query: str) -> List[Any]:
        if self._registry is None:
            return []
        return self._registry.search(query)
