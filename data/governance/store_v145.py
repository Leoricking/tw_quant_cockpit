"""
data/governance/store_v145.py — Source Governance Store v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] In-memory mode for tests. SQLite optional for runtime (gitignored).
[!] Additive migrations only. Backward compatible.
"""
from __future__ import annotations

from typing import Any, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_TABLES = [
    "source_identities",
    "source_lineage",
    "request_ledger",
    "fetch_run_audit",
    "host_rate_limit_policy",
    "provider_request_budget",
    "endpoint_request_policy",
    "quota_evidence",
    "retry_evidence",
    "cache_lineage",
    "conflict_lineage",
]


class SourceGovernanceStore:
    """
    Pluggable storage backend.
    - In-memory mode: for tests, offline, no SQLite required.
    - SQLite mode: for runtime (db path gitignored).
    [!] Additive migrations only. No schema breaking changes.
    """

    def __init__(self) -> None:
        self._db_path: Optional[str] = None
        self._mode: str = "memory"
        self._store: dict = {t: {} for t in _TABLES}

    def setup(self, db_path: Optional[str] = None) -> None:
        """Setup store. None = in-memory mode."""
        self._db_path = db_path
        if db_path is None:
            self._mode = "memory"
            return
        self._mode = "sqlite"
        self._setup_sqlite(db_path)

    def _setup_sqlite(self, db_path: str) -> None:
        """Initialize SQLite tables. Additive migrations only."""
        import sqlite3
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        for table in _TABLES:
            c.execute(
                f"CREATE TABLE IF NOT EXISTS {table} "
                f"(id TEXT PRIMARY KEY, data TEXT NOT NULL)"
            )
        conn.commit()
        conn.close()

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def tables(self) -> list:
        return list(_TABLES)

    def get_info(self) -> dict:
        return {
            "mode": self._mode,
            "db_path": self._db_path,
            "tables": _TABLES,
            "research_only": True,
            "no_real_orders": True,
        }
