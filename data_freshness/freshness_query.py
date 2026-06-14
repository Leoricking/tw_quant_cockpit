"""
data_freshness/freshness_query.py — Query interface for freshness reports v1.1.3.
[!] Research Only. No Real Orders.
[!] Read-only query layer — does NOT modify data or trigger repair.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from data_freshness.freshness_schema import (
    SEVERITY_CRITICAL,
    SOURCE_STATUS_INTERRUPTED,
    STATUS_DELAYED, STATUS_MISSING, STATUS_STALE,
    DatasetFreshnessRecord, FreshnessAlert, FreshnessSummary,
    SourceFreshnessStatus,
    ALERT_STATUS_OPEN,
)

logger = logging.getLogger(__name__)

# Safety invariants
NO_REAL_ORDERS  = True
RESEARCH_ONLY   = True


class FreshnessQuery:
    """
    Read-only query interface over freshness store outputs.
    Does NOT modify any data or trigger repair actions.
    """

    def __init__(self, store=None):
        """
        store: FreshnessStore instance (optional).
        If None, attempts to create a default FreshnessStore.
        """
        if store is not None:
            self._store = store
        else:
            try:
                from data_freshness.freshness_store import FreshnessStore  # type: ignore
                self._store = FreshnessStore()
            except Exception as exc:
                logger.warning(
                    "FreshnessQuery: could not create default FreshnessStore: %s", exc
                )
                self._store = None

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def latest_summary(self) -> Optional[FreshnessSummary]:
        """Return the latest persisted FreshnessSummary, or None."""
        if self._store is None:
            return None
        try:
            return self._store.load_latest_summary()
        except Exception as exc:
            logger.warning("latest_summary() failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Records
    # ------------------------------------------------------------------

    def list_records(self, status: Optional[str] = None) -> List[DatasetFreshnessRecord]:
        """Return all records, optionally filtered by status."""
        if self._store is None:
            return []
        try:
            records = self._store.load_latest_records()
            if status is not None:
                records = [r for r in records if r.status == status]
            return records
        except Exception as exc:
            logger.warning("list_records() failed: %s", exc)
            return []

    def list_stale(self) -> List[DatasetFreshnessRecord]:
        """Return all records with STALE status."""
        return self.list_records(status=STATUS_STALE)

    def list_delayed(self) -> List[DatasetFreshnessRecord]:
        """Return all records with DELAYED status."""
        return self.list_records(status=STATUS_DELAYED)

    def list_missing(self) -> List[DatasetFreshnessRecord]:
        """Return all records with MISSING status."""
        return self.list_records(status=STATUS_MISSING)

    def list_critical(self) -> List[DatasetFreshnessRecord]:
        """Return all records with CRITICAL severity."""
        if self._store is None:
            return []
        try:
            records = self._store.load_latest_records()
            return [r for r in records if r.severity == SEVERITY_CRITICAL]
        except Exception as exc:
            logger.warning("list_critical() failed: %s", exc)
            return []

    def list_by_symbol(self, symbol: str) -> List[DatasetFreshnessRecord]:
        """Return all records for a given symbol."""
        if self._store is None:
            return []
        try:
            records = self._store.load_latest_records()
            return [r for r in records if r.symbol == symbol]
        except Exception as exc:
            logger.warning("list_by_symbol(%s) failed: %s", symbol, exc)
            return []

    def list_by_dataset(self, dataset: str) -> List[DatasetFreshnessRecord]:
        """Return all records for a given dataset type."""
        if self._store is None:
            return []
        try:
            records = self._store.load_latest_records()
            return [r for r in records if r.dataset == dataset]
        except Exception as exc:
            logger.warning("list_by_dataset(%s) failed: %s", dataset, exc)
            return []

    def list_by_source(self, source: str) -> List[DatasetFreshnessRecord]:
        """Return all records for a given source."""
        if self._store is None:
            return []
        try:
            records = self._store.load_latest_records()
            return [r for r in records if r.source == source]
        except Exception as exc:
            logger.warning("list_by_source(%s) failed: %s", source, exc)
            return []

    # ------------------------------------------------------------------
    # Source health
    # ------------------------------------------------------------------

    def list_source_interruptions(self) -> List[SourceFreshnessStatus]:
        """
        Return all sources currently flagged as INTERRUPTED.
        Reads from current records and re-derives source health.
        """
        if self._store is None:
            return []
        try:
            from data_freshness.source_monitor import DataSourceFreshnessMonitor
            records = self._store.load_latest_records()
            monitor = DataSourceFreshnessMonitor()
            all_sources = monitor.summarize_sources(records)
            return [s for s in all_sources if s.status == SOURCE_STATUS_INTERRUPTED]
        except Exception as exc:
            logger.warning("list_source_interruptions() failed: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Alerts
    # ------------------------------------------------------------------

    def list_open_alerts(self) -> List[FreshnessAlert]:
        """Return all alerts with OPEN status."""
        if self._store is None:
            return []
        try:
            alerts = self._store.load_alerts()
            return [a for a in alerts if a.status == ALERT_STATUS_OPEN]
        except Exception as exc:
            logger.warning("list_open_alerts() failed: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Cross-run comparison
    # ------------------------------------------------------------------

    def compare_runs(
        self,
        run_a_records: List[DatasetFreshnessRecord],
        run_b_records: List[DatasetFreshnessRecord],
    ) -> Dict[str, Any]:
        """
        Compare two sets of freshness records.
        Returns diff dict: improved, degraded, new, resolved, unchanged_count.
        """
        try:
            from data_freshness.source_monitor import DataSourceFreshnessMonitor
            monitor = DataSourceFreshnessMonitor()
            return monitor.compare_with_previous_run(run_a_records, run_b_records)
        except Exception as exc:
            logger.warning("compare_runs() failed: %s", exc)
            return {
                "improved": [],
                "degraded": [],
                "new": [],
                "resolved": [],
                "unchanged_count": 0,
                "error": str(exc),
            }

    # ------------------------------------------------------------------
    # History
    # ------------------------------------------------------------------

    def freshness_history(
        self, symbol: str, dataset: str
    ) -> List[Dict[str, Any]]:
        """
        Return historical freshness records for a (symbol, dataset) pair.
        Reads from the history CSV file.
        """
        if self._store is None:
            return []
        try:
            import csv
            import os

            history_path = os.path.join(
                self._store.output_dir, "freshness_history.csv"
            )
            if not os.path.isfile(history_path):
                return []

            results: List[Dict[str, Any]] = []
            with open(history_path, newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (
                        row.get("symbol", "") == symbol
                        and row.get("dataset", "") == dataset
                    ):
                        results.append(dict(row))
            # Sort by detected_at ascending
            results.sort(key=lambda r: r.get("detected_at", ""))
            return results
        except Exception as exc:
            logger.warning(
                "freshness_history(%s, %s) failed: %s", symbol, dataset, exc
            )
            return []
