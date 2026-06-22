"""
portfolio/correlation/store_v152.py — Correlation Exposure Store v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No ledger modification, no order table, no broker credentials.
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from typing import Any, Dict, List, Optional

from portfolio.correlation.models_v152 import CorrelationExposureAnalysis

RESEARCH_ONLY = True
STORE_VERSION = "1.5.2"


def _to_json(obj: Any) -> str:
    return json.dumps(obj, default=str, sort_keys=True)


def _from_json(s: str) -> Any:
    return json.loads(s)


class CorrelationExposureStore:
    """
    SQLite-backed store for correlation exposure analyses.
    Default: in-memory DB.
    Immutable storage — analyses are never overwritten once saved (idempotent by analysis_id).
    No ledger modification. No order table. No broker credentials.
    """

    RESEARCH_ONLY = True

    def __init__(self, db_path: str = ":memory:"):
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self._conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS correlation_analyses (
                analysis_id   TEXT PRIMARY KEY,
                portfolio_id  TEXT NOT NULL,
                as_of         TEXT NOT NULL,
                generated_at  TEXT NOT NULL,
                content_hash  TEXT NOT NULL,
                payload       TEXT NOT NULL,
                labels        TEXT NOT NULL,
                research_only INTEGER NOT NULL DEFAULT 1
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS correlation_lineage (
                analysis_id  TEXT PRIMARY KEY,
                lineage_json TEXT NOT NULL
            )
        """)
        self._conn.commit()

    def save_analysis(self, analysis: CorrelationExposureAnalysis) -> str:
        """
        Save analysis. Idempotent — if analysis_id already exists, skip (immutable).
        Returns analysis_id.
        """
        cur = self._conn.cursor()
        cur.execute("SELECT analysis_id FROM correlation_analyses WHERE analysis_id = ?",
                    (analysis.analysis_id,))
        if cur.fetchone():
            return analysis.analysis_id  # already stored — immutable

        try:
            payload = _to_json(asdict(analysis))
        except Exception:
            payload = _to_json({"analysis_id": analysis.analysis_id, "error": "serialization_failed"})

        cur.execute("""
            INSERT INTO correlation_analyses
              (analysis_id, portfolio_id, as_of, generated_at, content_hash, payload, labels, research_only)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            analysis.analysis_id,
            analysis.request.portfolio_id,
            analysis.request.as_of,
            analysis.generated_at or "",
            analysis.content_hash or "",
            payload,
            _to_json(analysis.labels),
        ))
        self._conn.commit()
        return analysis.analysis_id

    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Return raw analysis dict or None."""
        cur = self._conn.cursor()
        cur.execute("SELECT payload FROM correlation_analyses WHERE analysis_id = ?",
                    (analysis_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return _from_json(row[0])

    def list_analyses(
        self,
        portfolio_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """List analyses, optionally filtered by portfolio_id."""
        cur = self._conn.cursor()
        if portfolio_id:
            cur.execute("""
                SELECT analysis_id, portfolio_id, as_of, generated_at, content_hash
                FROM correlation_analyses
                WHERE portfolio_id = ?
                ORDER BY as_of DESC, generated_at DESC
                LIMIT ?
            """, (portfolio_id, limit))
        else:
            cur.execute("""
                SELECT analysis_id, portfolio_id, as_of, generated_at, content_hash
                FROM correlation_analyses
                ORDER BY as_of DESC, generated_at DESC
                LIMIT ?
            """, (limit,))
        rows = cur.fetchall()
        return [
            {
                "analysis_id":  r[0],
                "portfolio_id": r[1],
                "as_of":        r[2],
                "generated_at": r[3],
                "content_hash": r[4],
            }
            for r in rows
        ]

    def save_lineage(self, analysis_id: str, lineage: Dict[str, Any]) -> None:
        """Save lineage dict for an analysis."""
        cur = self._conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO correlation_lineage (analysis_id, lineage_json)
            VALUES (?, ?)
        """, (analysis_id, _to_json(lineage)))
        self._conn.commit()

    def get_lineage(self, analysis_id: str) -> Dict[str, Any]:
        """Return lineage dict or empty dict."""
        cur = self._conn.cursor()
        cur.execute("SELECT lineage_json FROM correlation_lineage WHERE analysis_id = ?",
                    (analysis_id,))
        row = cur.fetchone()
        if row is None:
            return {}
        return _from_json(row[0])
