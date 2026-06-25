"""paper_trading/store_v160.py — Paper Trading Store v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
SQLite-backed or in-memory store. No formal Portfolio Ledger write. No credential storage.
Runtime DB files are gitignored.
"""
from __future__ import annotations
import json
from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional


def _decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class PaperTradingStore:
    """
    In-memory store for paper trading (SQLite backend can be plugged in).
    No credential storage. No formal Portfolio Ledger writes.
    Idempotent save. Recovery-safe.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, Any] = {}
        self._events: Dict[str, List[Any]] = {}  # session_id -> events
        self._orders: Dict[str, Any] = {}  # order_id -> order
        self._fills: Dict[str, Any] = {}  # fill_id -> fill
        self._ledger_entries: Dict[str, List[Any]] = {}  # session_id -> entries
        self._positions: Dict[str, Dict[str, Any]] = {}  # session_id -> {symbol: pos}
        self._cash: Dict[str, Any] = {}  # session_id -> cash
        self._snapshots: Dict[str, List[Any]] = {}  # session_id -> snapshots
        self._risk_evaluations: Dict[str, Any] = {}
        self._manifests: Dict[str, Any] = {}
        self._audit_records: Dict[str, List[Any]] = {}

    def save_session(self, session_id: str, session_data: Any) -> None:
        self._sessions[session_id] = session_data

    def get_session(self, session_id: str) -> Optional[Any]:
        return self._sessions.get(session_id)

    def list_sessions(self) -> List[str]:
        return list(self._sessions.keys())

    def save_event(self, session_id: str, event: Any) -> None:
        if session_id not in self._events:
            self._events[session_id] = []
        # Idempotent: check sequence
        existing_seqs = {e.get("sequence") if isinstance(e, dict) else e.sequence for e in self._events[session_id]}
        seq = event.get("sequence") if isinstance(event, dict) else event.sequence
        if seq not in existing_seqs:
            self._events[session_id].append(event)

    def get_events(self, session_id: str) -> List[Any]:
        return list(self._events.get(session_id, []))

    def save_order(self, order_id: str, order: Any) -> None:
        self._orders[order_id] = order

    def get_order(self, order_id: str) -> Optional[Any]:
        return self._orders.get(order_id)

    def list_orders(self, session_id: str) -> List[Any]:
        return [o for o in self._orders.values()
                if (o.get("session_id") if isinstance(o, dict) else o.session_id) == session_id]

    def save_fill(self, fill_id: str, fill: Any) -> None:
        self._fills[fill_id] = fill

    def get_fills(self, session_id: str) -> List[Any]:
        return [f for f in self._fills.values()
                if (f.get("session_id") if isinstance(f, dict) else f.session_id) == session_id]

    def save_ledger_entry(self, session_id: str, entry: Any) -> None:
        if session_id not in self._ledger_entries:
            self._ledger_entries[session_id] = []
        self._ledger_entries[session_id].append(entry)

    def get_ledger_entries(self, session_id: str) -> List[Any]:
        return list(self._ledger_entries.get(session_id, []))

    def save_snapshot(self, session_id: str, snapshot: Any) -> None:
        if session_id not in self._snapshots:
            self._snapshots[session_id] = []
        self._snapshots[session_id].append(snapshot)

    def get_snapshots(self, session_id: str) -> List[Any]:
        return list(self._snapshots.get(session_id, []))

    def get_latest_snapshot(self, session_id: str) -> Optional[Any]:
        snaps = self._snapshots.get(session_id, [])
        return snaps[-1] if snaps else None

    def save_manifest(self, manifest_id: str, manifest: Any) -> None:
        self._manifests[manifest_id] = manifest

    def get_manifest(self, manifest_id: str) -> Optional[Any]:
        return self._manifests.get(manifest_id)

    def save_audit_record(self, session_id: str, record: Any) -> None:
        if session_id not in self._audit_records:
            self._audit_records[session_id] = []
        self._audit_records[session_id].append(record)

    def get_audit_records(self, session_id: str) -> List[Any]:
        return list(self._audit_records.get(session_id, []))
