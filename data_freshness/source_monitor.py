"""
data_freshness/source_monitor.py — Data source freshness monitoring for v1.1.3.
[!] Research Only. No Real Orders.
[!] Interruption requires >= 5 symbols AND > 50% stale/interrupted.
[!] Single suspended symbol does NOT trigger source interruption.
[!] No automatic repair or external refresh triggered.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from data_freshness.freshness_schema import (
    SEVERITY_CRITICAL, SEVERITY_HIGH, SEVERITY_INFO, SEVERITY_LOW, SEVERITY_MEDIUM,
    SOURCE_STATUS_DEGRADED, SOURCE_STATUS_HEALTHY, SOURCE_STATUS_INTERRUPTED,
    SOURCE_STATUS_UNKNOWN,
    STATUS_DELAYED, STATUS_FRESH, STATUS_ACCEPTABLE,
    STATUS_INTERRUPTED, STATUS_MISSING, STATUS_STALE,
    DatasetFreshnessRecord, SourceFreshnessStatus,
)

logger = logging.getLogger(__name__)

# Safety invariants
NO_REAL_ORDERS                 = True
RESEARCH_ONLY                  = True
AUTO_EXTERNAL_REFRESH_ENABLED  = False
STALE_DATA_AUTO_REPAIR_ENABLED = False

# Interruption detection thresholds
MINIMUM_INTERRUPTION_SAMPLE = 5    # need at least 5 symbols to declare interruption
INTERRUPTION_STALE_THRESHOLD = 0.5  # > 50% stale/interrupted


class DataSourceFreshnessMonitor:
    """
    Aggregates freshness records by data source and detects source-level interruptions.

    [!] Does NOT trigger repair or external data refresh.
    [!] A single suspended symbol does NOT cause source interruption classification.
    [!] Requires >= 5 symbols with > 50% stale/interrupted to flag INTERRUPTED.
    """

    # ------------------------------------------------------------------
    # Aggregation
    # ------------------------------------------------------------------

    def aggregate_by_source(
        self, records: List[DatasetFreshnessRecord]
    ) -> Dict[str, List[DatasetFreshnessRecord]]:
        """Group records by (source, dataset) key."""
        grouped: Dict[str, List[DatasetFreshnessRecord]] = {}
        for rec in records:
            key = f"{rec.source}::{rec.dataset}"
            grouped.setdefault(key, []).append(rec)
        return grouped

    def aggregate_by_source_only(
        self, records: List[DatasetFreshnessRecord]
    ) -> Dict[str, List[DatasetFreshnessRecord]]:
        """Group records by source name only (across all datasets)."""
        grouped: Dict[str, List[DatasetFreshnessRecord]] = {}
        for rec in records:
            grouped.setdefault(rec.source, []).append(rec)
        return grouped

    # ------------------------------------------------------------------
    # Source status builder
    # ------------------------------------------------------------------

    def build_source_status(
        self,
        source_id: str,
        source_name: str,
        dataset: str,
        records: List[DatasetFreshnessRecord],
    ) -> SourceFreshnessStatus:
        """Build a SourceFreshnessStatus from a set of records for one source/dataset."""
        if not records:
            return SourceFreshnessStatus(
                source_id=source_id,
                source_name=source_name,
                dataset=dataset,
                symbols_expected=0,
                symbols_fresh=0,
                symbols_delayed=0,
                symbols_stale=0,
                symbols_missing=0,
                latest_seen_at=None,
                interruption_suspected=False,
                interruption_started_at=None,
                status=SOURCE_STATUS_UNKNOWN,
                severity=SEVERITY_INFO,
                reason="No records provided",
            )

        total = len(records)
        fresh_count = sum(
            1 for r in records if r.status in (STATUS_FRESH, STATUS_ACCEPTABLE)
        )
        delayed_count = sum(1 for r in records if r.status == STATUS_DELAYED)
        stale_count = sum(
            1 for r in records if r.status in (STATUS_STALE, STATUS_INTERRUPTED)
        )
        missing_count = sum(1 for r in records if r.status == STATUS_MISSING)

        # Latest seen_at from detected_at timestamps
        detected_times = [r.detected_at for r in records if r.detected_at]
        latest_seen_at = max(detected_times) if detected_times else None

        # Interruption detection
        stale_ratio = stale_count / total if total > 0 else 0.0
        interruption_suspected = (
            total >= MINIMUM_INTERRUPTION_SAMPLE
            and stale_ratio > INTERRUPTION_STALE_THRESHOLD
        )

        # Determine status
        if interruption_suspected:
            status = SOURCE_STATUS_INTERRUPTED
            severity = SEVERITY_CRITICAL
            reason = (
                f"Interruption suspected: {stale_count}/{total} symbols stale/interrupted "
                f"({stale_ratio:.0%} > {INTERRUPTION_STALE_THRESHOLD:.0%} threshold)"
            )
            interruption_started_at = latest_seen_at
        elif stale_count > 0 or missing_count > 0:
            status = SOURCE_STATUS_DEGRADED
            severity = SEVERITY_HIGH if stale_count > 0 else SEVERITY_MEDIUM
            reason = (
                f"Degraded: {stale_count} stale, {missing_count} missing, "
                f"{delayed_count} delayed out of {total} symbols"
            )
            interruption_started_at = None
        elif delayed_count > 0:
            status = SOURCE_STATUS_DEGRADED
            severity = SEVERITY_MEDIUM
            reason = f"Degraded: {delayed_count}/{total} symbols delayed"
            interruption_started_at = None
        else:
            status = SOURCE_STATUS_HEALTHY
            severity = SEVERITY_INFO
            reason = f"All {total} symbols fresh/acceptable"
            interruption_started_at = None

        return SourceFreshnessStatus(
            source_id=source_id,
            source_name=source_name,
            dataset=dataset,
            symbols_expected=total,
            symbols_fresh=fresh_count,
            symbols_delayed=delayed_count,
            symbols_stale=stale_count,
            symbols_missing=missing_count,
            latest_seen_at=latest_seen_at,
            interruption_suspected=interruption_suspected,
            interruption_started_at=interruption_started_at,
            status=status,
            severity=severity,
            reason=reason,
        )

    # ------------------------------------------------------------------
    # Interruption detection
    # ------------------------------------------------------------------

    def detect_source_interruption(
        self, records: List[DatasetFreshnessRecord]
    ) -> List[SourceFreshnessStatus]:
        """
        Detect source interruptions across all records.

        Interruption criteria (ALL must be true):
          - Same source AND dataset combination
          - >= 5 symbols in the group
          - > 50% stale/interrupted

        [!] Single symbol suspended does NOT trigger INTERRUPTED.
        [!] < 5 symbols → DEGRADED or UNKNOWN at most.
        """
        if not records:
            return []

        grouped = self.aggregate_by_source(records)
        results: List[SourceFreshnessStatus] = []

        for key, group_records in grouped.items():
            parts = key.split("::", 1)
            source_name = parts[0]
            dataset = parts[1] if len(parts) > 1 else "UNKNOWN"

            status_obj = self.build_source_status(
                source_id=key,
                source_name=source_name,
                dataset=dataset,
                records=group_records,
            )

            # Enforce minimum sample rule: downgrade INTERRUPTED if < threshold
            if (
                status_obj.status == SOURCE_STATUS_INTERRUPTED
                and status_obj.symbols_expected < MINIMUM_INTERRUPTION_SAMPLE
            ):
                status_obj.interruption_suspected = False
                status_obj.status = SOURCE_STATUS_DEGRADED
                status_obj.severity = SEVERITY_HIGH
                status_obj.reason = (
                    f"Insufficient sample ({status_obj.symbols_expected} < "
                    f"{MINIMUM_INTERRUPTION_SAMPLE}): status capped at DEGRADED"
                )

            results.append(status_obj)

        return results

    # ------------------------------------------------------------------
    # Partial source failure
    # ------------------------------------------------------------------

    def detect_partial_source_failure(
        self, records: List[DatasetFreshnessRecord]
    ) -> List[SourceFreshnessStatus]:
        """
        Detect partial source failures: some but not all symbols stale for same source/dataset.
        Returns DEGRADED status objects for affected sources.
        """
        if not records:
            return []

        grouped = self.aggregate_by_source(records)
        results: List[SourceFreshnessStatus] = []

        for key, group_records in grouped.items():
            parts = key.split("::", 1)
            source_name = parts[0]
            dataset = parts[1] if len(parts) > 1 else "UNKNOWN"

            total = len(group_records)
            stale = sum(
                1
                for r in group_records
                if r.status in (STATUS_STALE, STATUS_INTERRUPTED, STATUS_MISSING)
            )
            fresh = total - stale

            if stale == 0 or fresh == 0:
                continue  # Not partial — either all stale or all fresh

            stale_ratio = stale / total
            if stale_ratio >= INTERRUPTION_STALE_THRESHOLD:
                continue  # Full interruption territory, skip here

            # Partial failure: some stale, some fresh
            detected_times = [r.detected_at for r in group_records if r.detected_at]
            latest_seen_at = max(detected_times) if detected_times else None

            results.append(
                SourceFreshnessStatus(
                    source_id=key,
                    source_name=source_name,
                    dataset=dataset,
                    symbols_expected=total,
                    symbols_fresh=fresh,
                    symbols_delayed=0,
                    symbols_stale=stale,
                    symbols_missing=0,
                    latest_seen_at=latest_seen_at,
                    interruption_suspected=False,
                    interruption_started_at=None,
                    status=SOURCE_STATUS_DEGRADED,
                    severity=SEVERITY_MEDIUM,
                    reason=(
                        f"Partial failure: {stale}/{total} symbols stale "
                        f"({stale_ratio:.0%}), {fresh} symbols still fresh"
                    ),
                )
            )

        return results

    # ------------------------------------------------------------------
    # Run comparison
    # ------------------------------------------------------------------

    def compare_with_previous_run(
        self,
        current: List[DatasetFreshnessRecord],
        previous: List[DatasetFreshnessRecord],
    ) -> Dict[str, Any]:
        """
        Compare current and previous run records.
        Returns a diff dict with improved, degraded, new, resolved lists.
        """
        def _key(r: DatasetFreshnessRecord) -> str:
            return f"{r.symbol}::{r.dataset}"

        current_map = {_key(r): r for r in current}
        previous_map = {_key(r): r for r in previous}

        all_keys = set(current_map) | set(previous_map)

        _STATUS_ORDER = {
            STATUS_FRESH: 0,
            STATUS_ACCEPTABLE: 1,
            STATUS_DELAYED: 2,
            STATUS_STALE: 3,
            STATUS_INTERRUPTED: 4,
            STATUS_MISSING: 5,
        }

        improved: List[Dict] = []
        degraded: List[Dict] = []
        new_symbols: List[Dict] = []
        resolved: List[Dict] = []
        unchanged: List[str] = []

        for key in all_keys:
            cur = current_map.get(key)
            prev = previous_map.get(key)

            if cur is None and prev is not None:
                resolved.append({"key": key, "previous_status": prev.status})
            elif cur is not None and prev is None:
                new_symbols.append({"key": key, "current_status": cur.status})
            elif cur is not None and prev is not None:
                cur_ord = _STATUS_ORDER.get(cur.status, 3)
                prev_ord = _STATUS_ORDER.get(prev.status, 3)
                if cur_ord < prev_ord:
                    improved.append(
                        {"key": key, "from": prev.status, "to": cur.status}
                    )
                elif cur_ord > prev_ord:
                    degraded.append(
                        {"key": key, "from": prev.status, "to": cur.status}
                    )
                else:
                    unchanged.append(key)

        return {
            "improved": improved,
            "degraded": degraded,
            "new": new_symbols,
            "resolved": resolved,
            "unchanged_count": len(unchanged),
            "total_current": len(current),
            "total_previous": len(previous),
        }

    # ------------------------------------------------------------------
    # Summarize all sources
    # ------------------------------------------------------------------

    def summarize_sources(
        self, records: List[DatasetFreshnessRecord]
    ) -> List[SourceFreshnessStatus]:
        """Summarize freshness status for all detected sources/datasets."""
        return self.detect_source_interruption(records)
