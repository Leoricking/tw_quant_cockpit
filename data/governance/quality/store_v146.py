"""
data/governance/quality/store_v146.py — Quality Gate Store v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SQLite, additive migration, idempotent.
[!] Does NOT modify existing governance tables (data/governance/store_v145.py).
[!] Append-only audit. Temp DB for tests.
"""
from __future__ import annotations

import json
import sqlite3
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS quality_gate_definitions (
    gate_id TEXT PRIMARY KEY,
    gate_name TEXT NOT NULL,
    scope TEXT NOT NULL,
    category TEXT NOT NULL,
    mandatory INTEGER NOT NULL DEFAULT 1,
    blocking INTEGER NOT NULL DEFAULT 1,
    severity TEXT NOT NULL DEFAULT 'CRITICAL',
    policy_version TEXT NOT NULL DEFAULT '1.4.6',
    definition_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_gate_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gate_id TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    scope TEXT NOT NULL,
    status TEXT NOT NULL,
    passed INTEGER NOT NULL,
    blocking INTEGER NOT NULL,
    evidence TEXT,
    evaluated_at TEXT NOT NULL,
    policy_version TEXT NOT NULL DEFAULT '1.4.6',
    result_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_decisions (
    decision_id TEXT PRIMARY KEY,
    scope TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    quality_state TEXT NOT NULL,
    formal_research_allowed INTEGER NOT NULL,
    backtest_allowed INTEGER NOT NULL,
    report_allowed INTEGER NOT NULL,
    ingestion_allowed INTEGER NOT NULL,
    quality_score REAL,
    decided_at TEXT NOT NULL,
    policy_version TEXT NOT NULL DEFAULT '1.4.6',
    decision_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS provider_quality_profiles (
    provider_id TEXT PRIMARY KEY,
    quality_state TEXT NOT NULL,
    authority_level TEXT NOT NULL,
    formal_research_allowed INTEGER NOT NULL,
    backtest_allowed INTEGER NOT NULL,
    report_allowed INTEGER NOT NULL,
    ingestion_allowed INTEGER NOT NULL,
    quality_score REAL,
    evaluated_at TEXT NOT NULL,
    policy_version TEXT NOT NULL DEFAULT '1.4.6',
    profile_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dataset_quality_profiles (
    dataset_key TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    provider_id TEXT NOT NULL,
    quality_state TEXT NOT NULL,
    admitted INTEGER NOT NULL,
    formal_use_allowed INTEGER NOT NULL,
    evaluated_at TEXT NOT NULL,
    policy_version TEXT NOT NULL DEFAULT '1.4.6',
    profile_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quarantine_records (
    quarantine_id TEXT PRIMARY KEY,
    provider_id TEXT NOT NULL,
    quality_state TEXT NOT NULL,
    auto_release_allowed INTEGER NOT NULL DEFAULT 0,
    released INTEGER NOT NULL DEFAULT 0,
    quarantined_at TEXT NOT NULL,
    policy_version TEXT NOT NULL DEFAULT '1.4.6',
    record_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_decision_audit (
    audit_id TEXT PRIMARY KEY,
    decision_id TEXT NOT NULL,
    provider_id TEXT NOT NULL,
    scope TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    quality_state TEXT NOT NULL,
    evidence_hash TEXT NOT NULL,
    audited_at TEXT NOT NULL,
    policy_version TEXT NOT NULL DEFAULT '1.4.6',
    audit_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_policy_versions (
    policy_version TEXT PRIMARY KEY,
    description TEXT,
    effective_from TEXT NOT NULL,
    policy_json TEXT NOT NULL
);
"""


class QualityGateStore:
    """
    SQLite-backed store for quality gate data.
    Additive migrations, idempotent setup.
    Does NOT touch existing governance tables.
    """

    def __init__(self) -> None:
        self._conn: Optional[sqlite3.Connection] = None
        self.mode = "uninitialized"

    def setup(self, db_path: Optional[str] = None) -> None:
        """Set up the store. db_path=None → in-memory (for tests)."""
        if db_path is None:
            self._conn = sqlite3.connect(":memory:")
            self.mode = "memory"
        else:
            self._conn = sqlite3.connect(db_path)
            self.mode = "file"
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        assert self._conn is not None
        self._conn.executescript(_SCHEMA_SQL)
        self._conn.commit()

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    # ------------------------------------------------------------------
    # Provider Quality Profiles
    # ------------------------------------------------------------------

    def upsert_provider_profile(self, profile_dict: Dict[str, Any]) -> None:
        assert self._conn is not None
        import datetime
        evaluated_at = profile_dict.get("evaluated_at", datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z')
        self._conn.execute(
            """
            INSERT OR REPLACE INTO provider_quality_profiles
            (provider_id, quality_state, authority_level, formal_research_allowed,
             backtest_allowed, report_allowed, ingestion_allowed, quality_score,
             evaluated_at, policy_version, profile_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                profile_dict["provider_id"],
                profile_dict["quality_state"],
                profile_dict.get("authority_level", "UNKNOWN"),
                1 if profile_dict.get("formal_research_allowed") else 0,
                1 if profile_dict.get("backtest_allowed") else 0,
                1 if profile_dict.get("report_allowed") else 0,
                1 if profile_dict.get("ingestion_allowed") else 0,
                profile_dict.get("quality_score"),
                evaluated_at,
                profile_dict.get("policy_version", "1.4.6"),
                json.dumps(profile_dict),
            )
        )
        self._conn.commit()

    def get_provider_profile(self, provider_id: str) -> Optional[Dict[str, Any]]:
        assert self._conn is not None
        row = self._conn.execute(
            "SELECT profile_json FROM provider_quality_profiles WHERE provider_id = ?",
            (provider_id,)
        ).fetchone()
        if row:
            return json.loads(row["profile_json"])
        return None

    def list_provider_profiles(self) -> List[Dict[str, Any]]:
        assert self._conn is not None
        rows = self._conn.execute(
            "SELECT profile_json FROM provider_quality_profiles"
        ).fetchall()
        return [json.loads(r["profile_json"]) for r in rows]

    # ------------------------------------------------------------------
    # Quality Decisions
    # ------------------------------------------------------------------

    def save_decision(self, decision_dict: Dict[str, Any]) -> None:
        assert self._conn is not None
        self._conn.execute(
            """
            INSERT OR REPLACE INTO quality_decisions
            (decision_id, scope, subject_id, decision, quality_state,
             formal_research_allowed, backtest_allowed, report_allowed,
             ingestion_allowed, quality_score, decided_at, policy_version, decision_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                decision_dict["decision_id"],
                decision_dict["scope"],
                decision_dict["subject_id"],
                decision_dict["decision"],
                decision_dict["quality_state"],
                1 if decision_dict.get("formal_research_allowed") else 0,
                1 if decision_dict.get("backtest_allowed") else 0,
                1 if decision_dict.get("report_allowed") else 0,
                1 if decision_dict.get("ingestion_allowed") else 0,
                decision_dict.get("quality_score"),
                decision_dict.get("decided_at", ""),
                decision_dict.get("policy_version", "1.4.6"),
                json.dumps(decision_dict),
            )
        )
        self._conn.commit()

    def get_decision(self, decision_id: str) -> Optional[Dict[str, Any]]:
        assert self._conn is not None
        row = self._conn.execute(
            "SELECT decision_json FROM quality_decisions WHERE decision_id = ?",
            (decision_id,)
        ).fetchone()
        if row:
            return json.loads(row["decision_json"])
        return None

    # ------------------------------------------------------------------
    # Audit (append-only)
    # ------------------------------------------------------------------

    def append_audit(self, audit_dict: Dict[str, Any]) -> None:
        """Append audit record. Cannot be modified after insertion."""
        assert self._conn is not None
        self._conn.execute(
            """
            INSERT INTO quality_decision_audit
            (audit_id, decision_id, provider_id, scope, subject_id,
             decision, quality_state, evidence_hash, audited_at, policy_version, audit_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                audit_dict["audit_id"],
                audit_dict["decision_id"],
                audit_dict.get("provider_id", ""),
                audit_dict["scope"],
                audit_dict["subject_id"],
                audit_dict["decision"],
                audit_dict["quality_state"],
                audit_dict["evidence_hash"],
                audit_dict["audited_at"],
                audit_dict.get("policy_version", "1.4.6"),
                json.dumps(audit_dict),
            )
        )
        self._conn.commit()

    def list_audit(self) -> List[Dict[str, Any]]:
        assert self._conn is not None
        rows = self._conn.execute(
            "SELECT audit_json FROM quality_decision_audit ORDER BY audited_at"
        ).fetchall()
        return [json.loads(r["audit_json"]) for r in rows]
