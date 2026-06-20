"""
data/providers/data_gov_tw/query_v143.py — Query service v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Point-in-time query: as-of queries respect available_from.
[!] Cannot access records before available_from.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class DataGovTwQueryService:
    """
    Query interface for data.gov.tw stored data.

    Provides:
    - Dataset and resource queries
    - Schema contract lookup
    - Revision history
    - Record queries with point-in-time support
    - Government observations
    - Lineage
    - Coverage summary
    - Blocked/schema-changed/license-issue lists
    """

    def __init__(self, store=None) -> None:
        self._store = store

    def get_dataset(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        if self._store:
            return self._store.get_dataset(dataset_id)
        return None

    def search_datasets(
        self, keyword: str = "", domain: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        if not self._store:
            return []
        try:
            rows = self._store._conn.execute(
                "SELECT * FROM data_gov_tw_datasets LIMIT ?", (limit,)
            ).fetchall()
            results = [dict(r) for r in rows]
            if keyword:
                results = [r for r in results if keyword.lower() in (r.get("title") or "").lower()]
            if domain:
                results = [r for r in results if r.get("research_domain") == domain]
            return results
        except Exception:
            return []

    def list_allowlisted_datasets(self) -> List[Dict[str, Any]]:
        if not self._store:
            return []
        try:
            rows = self._store._conn.execute(
                "SELECT * FROM data_gov_tw_datasets WHERE allowlisted=1"
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []

    def list_approved_datasets(self) -> List[Dict[str, Any]]:
        if not self._store:
            return []
        try:
            rows = self._store._conn.execute(
                "SELECT * FROM data_gov_tw_datasets WHERE approved=1"
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []

    def list_resources(self, dataset_id: str) -> List[Dict[str, Any]]:
        if not self._store:
            return []
        try:
            rows = self._store._conn.execute(
                "SELECT * FROM data_gov_tw_resources WHERE dataset_id=?", (dataset_id,)
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []

    def get_schema_contract(self, schema_id: str) -> Optional[Dict[str, Any]]:
        if not self._store:
            return None
        try:
            row = self._store._conn.execute(
                "SELECT * FROM data_gov_tw_schema_contracts WHERE schema_id=?", (schema_id,)
            ).fetchone()
            return dict(row) if row else None
        except Exception:
            return None

    def get_dataset_revisions(self, dataset_id: str) -> List[Dict[str, Any]]:
        if not self._store:
            return []
        return self._store.get_revisions(dataset_id)

    def get_records(self, dataset_id: str, limit: int = 1000) -> List[Dict[str, Any]]:
        if not self._store:
            return []
        try:
            rows = self._store._conn.execute(
                "SELECT * FROM data_gov_tw_records WHERE dataset_id=? LIMIT ?",
                (dataset_id, limit)
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []

    def get_records_as_of(
        self, dataset_id: str, as_of: str, limit: int = 1000
    ) -> Dict[str, Any]:
        """Point-in-time query: only records with available_from <= as_of."""
        if not self._store:
            return {"records": [], "as_of": as_of, "blocked": False}
        try:
            rows = self._store._conn.execute(
                """SELECT * FROM data_gov_tw_records
                   WHERE dataset_id=?
                   AND (available_from IS NULL OR available_from <= ?)
                   LIMIT ?""",
                (dataset_id, as_of, limit)
            ).fetchall()
            records = [dict(r) for r in rows]
            return {
                "records": records,
                "as_of": as_of,
                "record_count": len(records),
                "blocked": False,
            }
        except Exception as exc:
            return {"records": [], "as_of": as_of, "blocked": True, "error": str(exc)}

    def get_latest_record(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        if not self._store:
            return None
        try:
            row = self._store._conn.execute(
                """SELECT * FROM data_gov_tw_records
                   WHERE dataset_id=?
                   ORDER BY observation_date DESC LIMIT 1""",
                (dataset_id,)
            ).fetchone()
            return dict(row) if row else None
        except Exception:
            return None

    def get_government_observations(
        self, domain: Optional[str] = None, indicator_code: Optional[str] = None, limit: int = 1000
    ) -> List[Dict[str, Any]]:
        if not self._store:
            return []
        try:
            if domain and indicator_code:
                rows = self._store._conn.execute(
                    "SELECT * FROM government_observations WHERE domain=? AND indicator_code=? LIMIT ?",
                    (domain, indicator_code, limit)
                ).fetchall()
            elif domain:
                rows = self._store._conn.execute(
                    "SELECT * FROM government_observations WHERE domain=? LIMIT ?",
                    (domain, limit)
                ).fetchall()
            else:
                rows = self._store._conn.execute(
                    "SELECT * FROM government_observations LIMIT ?", (limit,)
                ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []

    def get_provider_lineage(self, dataset_id: str) -> List[Dict[str, Any]]:
        return []  # Populated by lineage service in full implementation

    def get_last_fetch_status(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        if not self._store:
            return None
        try:
            row = self._store._conn.execute(
                """SELECT * FROM data_gov_tw_fetch_runs
                   WHERE dataset_id=? ORDER BY started_at DESC LIMIT 1""",
                (dataset_id,)
            ).fetchone()
            return dict(row) if row else None
        except Exception:
            return None

    def summarize_coverage(self) -> Dict[str, Any]:
        if not self._store:
            return {"datasets": 0, "resources": 0, "records": 0}
        return self._store.summarize_coverage()

    def list_blocked_datasets(self) -> List[Dict[str, Any]]:
        if not self._store:
            return []
        try:
            rows = self._store._conn.execute(
                "SELECT * FROM data_gov_tw_datasets WHERE status='BLOCKED'"
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []

    def list_schema_changes(self) -> List[Dict[str, Any]]:
        if not self._store:
            return []
        try:
            rows = self._store._conn.execute(
                "SELECT * FROM data_gov_tw_revisions WHERE schema_changed=1"
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []

    def list_license_issues(self) -> List[Dict[str, Any]]:
        if not self._store:
            return []
        try:
            rows = self._store._conn.execute(
                "SELECT * FROM data_gov_tw_revisions WHERE license_changed=1"
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []
