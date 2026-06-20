"""
data/providers/data_gov_tw/store_v143.py — Storage layer v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Additive migration only. No destructive migration.
[!] Does not overwrite existing TWSE/TPEx/MOPS market data tables.
[!] Immutable revisions. Transaction safety.
"""
from __future__ import annotations

import datetime
import sqlite3
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS data_gov_tw_datasets (
    dataset_id TEXT PRIMARY KEY,
    title TEXT,
    provider_agency TEXT,
    agency_code TEXT,
    category TEXT,
    research_domain TEXT,
    status TEXT,
    official INTEGER DEFAULT 1,
    allowlisted INTEGER DEFAULT 0,
    approved INTEGER DEFAULT 0,
    authoritative_level TEXT,
    license_name TEXT,
    license_url TEXT,
    update_frequency TEXT,
    fetched_at TEXT,
    content_hash TEXT,
    metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS data_gov_tw_resources (
    resource_id TEXT,
    dataset_id TEXT,
    title TEXT,
    format TEXT,
    download_url TEXT,
    encoding TEXT,
    size_bytes INTEGER,
    last_modified TEXT,
    source_timestamp TEXT,
    fetched_at TEXT,
    enabled INTEGER DEFAULT 1,
    metadata_json TEXT,
    PRIMARY KEY (resource_id, dataset_id)
);

CREATE TABLE IF NOT EXISTS data_gov_tw_schema_contracts (
    schema_id TEXT PRIMARY KEY,
    dataset_id TEXT,
    version TEXT,
    contract_hash TEXT,
    required_fields_json TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS data_gov_tw_revisions (
    revision_id TEXT PRIMARY KEY,
    dataset_id TEXT,
    resource_id TEXT,
    detected_at TEXT,
    old_content_hash TEXT,
    new_content_hash TEXT,
    schema_changed INTEGER DEFAULT 0,
    license_changed INTEGER DEFAULT 0,
    metadata_changed INTEGER DEFAULT 0,
    severity TEXT,
    review_required INTEGER DEFAULT 0,
    metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS data_gov_tw_records (
    record_id TEXT,
    dataset_id TEXT,
    resource_id TEXT,
    schema_id TEXT,
    reporting_period TEXT,
    observation_date TEXT,
    published_at TEXT,
    available_from TEXT,
    values_json TEXT,
    unit TEXT,
    quality_status TEXT,
    freshness_status TEXT,
    formal_use_allowed INTEGER DEFAULT 0,
    content_hash TEXT,
    fetched_at TEXT,
    PRIMARY KEY (record_id, dataset_id)
);

CREATE TABLE IF NOT EXISTS data_gov_tw_fetch_runs (
    run_id TEXT PRIMARY KEY,
    dataset_id TEXT,
    resource_id TEXT,
    mode TEXT,
    dry_run INTEGER DEFAULT 1,
    started_at TEXT,
    finished_at TEXT,
    records_received INTEGER,
    records_valid INTEGER,
    records_rejected INTEGER,
    cache_hit INTEGER DEFAULT 0,
    rate_limited INTEGER DEFAULT 0,
    blocked INTEGER DEFAULT 0,
    database_updated INTEGER DEFAULT 0,
    metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS government_observations (
    obs_id TEXT PRIMARY KEY,
    domain TEXT,
    indicator_code TEXT,
    indicator_name TEXT,
    observation_date TEXT,
    reporting_period TEXT,
    value REAL,
    unit TEXT,
    geography TEXT,
    industry_code TEXT,
    published_at TEXT,
    available_from TEXT,
    dataset_id TEXT,
    resource_id TEXT,
    provider_agency TEXT,
    authoritative_level TEXT,
    quality_status TEXT,
    freshness_status TEXT,
    formal_use_allowed INTEGER DEFAULT 0,
    fetched_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_data_gov_tw_datasets_domain ON data_gov_tw_datasets(research_domain);
CREATE INDEX IF NOT EXISTS idx_data_gov_tw_revisions_dataset ON data_gov_tw_revisions(dataset_id);
CREATE INDEX IF NOT EXISTS idx_data_gov_tw_records_dataset ON data_gov_tw_records(dataset_id);
CREATE INDEX IF NOT EXISTS idx_gov_obs_domain ON government_observations(domain, indicator_code);
"""


class DataGovTwStore:
    """
    SQLite-backed storage for data.gov.tw provider data.

    Rules:
    - Additive migration only — never destructive
    - Does not touch TWSE/TPEx/MOPS tables
    - Immutable revisions (never deleted)
    - Transaction safety
    - Unique key constraints
    - Indexed for query performance
    - Runtime DB is gitignored
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()

    def _init_db(self) -> None:
        self._conn = sqlite3.connect(self._db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        for stmt in _SCHEMA_SQL.strip().split(";"):
            stmt = stmt.strip()
            if stmt:
                self._conn.execute(stmt)
        self._conn.commit()

    def upsert_dataset(self, dataset: Dict[str, Any]) -> None:
        import json
        self._conn.execute(
            """INSERT OR REPLACE INTO data_gov_tw_datasets
               (dataset_id, title, provider_agency, agency_code, category,
                research_domain, status, official, allowlisted, approved,
                authoritative_level, license_name, license_url, update_frequency,
                fetched_at, content_hash, metadata_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                dataset.get("dataset_id"),
                dataset.get("title"),
                dataset.get("provider_agency"),
                dataset.get("agency_code"),
                dataset.get("category"),
                dataset.get("research_domain"),
                dataset.get("status"),
                int(bool(dataset.get("official", True))),
                int(bool(dataset.get("allowlisted", False))),
                int(bool(dataset.get("approved", False))),
                dataset.get("authoritative_level"),
                dataset.get("license_name"),
                dataset.get("license_url"),
                dataset.get("update_frequency"),
                dataset.get("fetched_at"),
                dataset.get("content_hash"),
                json.dumps(dataset.get("metadata", {})),
            )
        )
        self._conn.commit()

    def get_dataset(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        import json
        row = self._conn.execute(
            "SELECT * FROM data_gov_tw_datasets WHERE dataset_id=?", (dataset_id,)
        ).fetchone()
        if not row:
            return None
        return dict(row)

    def upsert_resource(self, resource: Dict[str, Any]) -> None:
        import json
        self._conn.execute(
            """INSERT OR REPLACE INTO data_gov_tw_resources
               (resource_id, dataset_id, title, format, download_url, encoding,
                size_bytes, last_modified, source_timestamp, fetched_at, enabled, metadata_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                resource.get("resource_id"),
                resource.get("dataset_id"),
                resource.get("title"),
                resource.get("format"),
                resource.get("download_url"),
                resource.get("encoding"),
                resource.get("size_bytes"),
                resource.get("last_modified"),
                resource.get("source_timestamp"),
                resource.get("fetched_at"),
                int(bool(resource.get("enabled", True))),
                json.dumps(resource.get("metadata", {})),
            )
        )
        self._conn.commit()

    def insert_revision(self, revision: Dict[str, Any]) -> None:
        """Immutable — revision records are never updated or deleted."""
        import json
        self._conn.execute(
            """INSERT OR IGNORE INTO data_gov_tw_revisions
               (revision_id, dataset_id, resource_id, detected_at,
                old_content_hash, new_content_hash, schema_changed,
                license_changed, metadata_changed, severity, review_required, metadata_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                revision.get("revision_id"),
                revision.get("dataset_id"),
                revision.get("resource_id"),
                revision.get("detected_at"),
                revision.get("old_content_hash"),
                revision.get("new_content_hash"),
                int(bool(revision.get("schema_changed", False))),
                int(bool(revision.get("license_changed", False))),
                int(bool(revision.get("metadata_changed", False))),
                revision.get("severity", "INFO"),
                int(bool(revision.get("review_required", False))),
                json.dumps(revision.get("metadata", {})),
            )
        )
        self._conn.commit()

    def get_revisions(self, dataset_id: str) -> List[Dict[str, Any]]:
        rows = self._conn.execute(
            "SELECT * FROM data_gov_tw_revisions WHERE dataset_id=? ORDER BY detected_at",
            (dataset_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    def summarize_coverage(self) -> Dict[str, Any]:
        counts: Dict[str, Any] = {}
        for table in ("data_gov_tw_datasets", "data_gov_tw_resources", "data_gov_tw_revisions",
                      "data_gov_tw_records", "government_observations"):
            try:
                row = self._conn.execute(f"SELECT COUNT(*) as n FROM {table}").fetchone()
                counts[table] = row["n"] if row else 0
            except Exception:
                counts[table] = -1
        approved = self._conn.execute(
            "SELECT COUNT(*) as n FROM data_gov_tw_datasets WHERE approved=1"
        ).fetchone()
        counts["approved_datasets"] = approved["n"] if approved else 0
        return counts

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
