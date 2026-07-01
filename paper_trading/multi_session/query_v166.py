"""
paper_trading/multi_session/query_v166.py — Coordination Query v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.store_v166 import CoordinationStore

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True


class CoordinationQuery:
    """Query interface for coordination store."""

    def __init__(self, store: CoordinationStore) -> None:
        self._store = store

    def get_decisions(self) -> List[Dict[str, Any]]:
        return self._store.query("decision")

    def get_conflicts(self) -> List[Dict[str, Any]]:
        return self._store.query("conflict")

    def get_reservations(self) -> List[Dict[str, Any]]:
        return self._store.query("reservation")

    def get_snapshots(self) -> List[Dict[str, Any]]:
        return self._store.query("snapshot")

    def get_for_session(self, session_id: str) -> List[Dict[str, Any]]:
        return [r for r in self._store.query() if r.get("session_id") == session_id]

    def summary(self) -> Dict[str, int]:
        return self._store.summary()
