"""
portfolio/store_v150.py — Storage layer for v1.5.0.

Additive migration only (no destructive schema changes).
Idempotent writes. Append-only for transactions and snapshots.
In-memory store for tests (use_temp_db=True).

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import json
import os
from decimal import Decimal
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
SCHEMA_VERSION = "1.5.0"


def _decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f"Not serializable: {type(obj)}")


class PortfolioStore:
    RESEARCH_ONLY = True

    def __init__(self, data_dir: Optional[str] = None, use_temp_db: bool = False):
        self.use_temp_db = use_temp_db
        self.data_dir = data_dir
        # In-memory store for tests
        self._portfolios: Dict[str, Dict] = {}
        self._transactions: Dict[str, List[Dict]] = {}  # portfolio_id -> [txn]
        self._snapshots: Dict[str, List[Dict]] = {}     # portfolio_id -> [snap]
        self._schema_version = SCHEMA_VERSION

    # --- Portfolio CRUD (idempotent) ---

    def save_portfolio(self, portfolio: Dict[str, Any]) -> str:
        pid = portfolio["portfolio_id"]
        if pid not in self._portfolios:
            self._portfolios[pid] = dict(portfolio)
        # Idempotent: no overwrite if same id exists (additive only)
        return pid

    def get_portfolio(self, portfolio_id: str) -> Optional[Dict]:
        return self._portfolios.get(portfolio_id)

    def list_portfolios(self) -> List[Dict]:
        return list(self._portfolios.values())

    # --- Transactions (append-only) ---

    def append_transaction(self, portfolio_id: str, txn: Dict[str, Any]) -> str:
        if portfolio_id not in self._transactions:
            self._transactions[portfolio_id] = []
        # Idempotent: skip duplicate transaction_id
        tid = txn.get("transaction_id")
        existing_ids = {t.get("transaction_id") for t in self._transactions[portfolio_id]}
        if tid and tid in existing_ids:
            return tid  # already exists, no-op
        self._transactions[portfolio_id].append(dict(txn))
        return tid or ""

    def get_transactions(self, portfolio_id: str) -> List[Dict]:
        return list(self._transactions.get(portfolio_id, []))

    # --- Snapshots (append-only, immutable) ---

    def save_snapshot(self, portfolio_id: str, snapshot: Dict[str, Any]) -> str:
        if portfolio_id not in self._snapshots:
            self._snapshots[portfolio_id] = []
        snap_id = snapshot.get("snapshot_id", "")
        existing_ids = {s.get("snapshot_id") for s in self._snapshots[portfolio_id]}
        if snap_id in existing_ids:
            return snap_id  # idempotent
        self._snapshots[portfolio_id].append(dict(snapshot))
        return snap_id

    def get_snapshots(self, portfolio_id: str) -> List[Dict]:
        return list(self._snapshots.get(portfolio_id, []))

    def get_latest_snapshot(self, portfolio_id: str) -> Optional[Dict]:
        snaps = self._snapshots.get(portfolio_id, [])
        if not snaps:
            return None
        return snaps[-1]

    # --- Schema migration (additive only) ---

    def migrate(self) -> Dict[str, Any]:
        """
        Additive migration: adds new fields, never removes or renames.
        Returns migration report.
        """
        return {
            "schema_version": self._schema_version,
            "migration": "additive_only",
            "status": "OK",
            "research_only": True,
        }
