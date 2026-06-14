"""
data_freshness/freshness_prioritizer.py — Freshness record prioritization for v1.1.3.
[!] Research Only. No Real Orders.
[!] Priority is based on data integrity risk, NOT stock popularity or trading signals.
[!] NOT based on expected returns, analyst ratings, or market signals.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from data_freshness.freshness_schema import (
    DATASET_CHIPS, DATASET_DAILY_PRICE, DATASET_FUNDAMENTALS, DATASET_MARGIN,
    DATASET_SHORT_INTEREST, DATASET_VOLUME,
    SEVERITY_CRITICAL, SEVERITY_HIGH,
    STATUS_DELAYED, STATUS_FUTURE_DATE, STATUS_INTERRUPTED,
    STATUS_MISSING, STATUS_STALE,
    DatasetFreshnessRecord,
)

logger = logging.getLogger(__name__)

# Safety invariants
NO_REAL_ORDERS  = True
RESEARCH_ONLY   = True

# Priority levels
P0 = 0   # Critical — data integrity / formal validation blocker
P1 = 1   # High — core tier SLA breach
P2 = 2   # Medium — research tier degraded / secondary datasets
P3 = 3   # Low — non-blocking metadata / optional datasets

# Tier names
_CORE_TIERS     = {"core10", "core_10", "CORE10", "CORE_10"}
_RESEARCH_TIERS = {"research30", "research_30", "RESEARCH30", "RESEARCH_30"}
_BROAD_TIERS    = {"broad100", "broad_100", "BROAD100", "BROAD_100"}


class FreshnessPrioritizer:
    """
    Priority scorer for freshness records.

    [!] Priority is based solely on data integrity risk to research pipeline.
    [!] NOT based on stock popularity, expected returns, or trading signals.
    [!] P0: formal validation blockers; P1: core SLA breach; P2: research degraded; P3: low-impact.
    """

    def score(
        self,
        record: DatasetFreshnessRecord,
        context: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Score a record with a priority level P0–P3.

        P0 (0): future date, date regression, source interruption affecting validity,
                invalid latest row, formal validation blocker.
        P1 (1): CORE_10 daily price or volume stale/interrupted; lag > SLA for core datasets.
        P2 (2): RESEARCH_30 stale; chips/margin/short interest delayed; partial update.
        P3 (3): optional fundamentals, broad100 datasets, non-blocking metadata.
        """
        # --- P0: data integrity issues ---
        if record.future_date_detected:
            return P0
        if record.date_regression_detected:
            return P0
        if not record.latest_row_valid:
            return P0
        if record.status == STATUS_INTERRUPTED and record.severity == SEVERITY_CRITICAL:
            # Widespread source interruption on core tier
            if record.tier.lower() in _CORE_TIERS:
                return P0
        # Source interruption flag from context
        if context and context.get("source_interrupted"):
            return P0

        tier_lower = record.tier.lower()
        dataset = record.dataset

        # --- P1: core tier, price/volume stale ---
        if tier_lower in {t.lower() for t in _CORE_TIERS}:
            if dataset in (DATASET_DAILY_PRICE, DATASET_VOLUME):
                if record.status in (STATUS_STALE, STATUS_INTERRUPTED, STATUS_MISSING):
                    return P1
                if record.status == STATUS_DELAYED:
                    return P1
            # Core tier, any dataset stale
            if record.status in (STATUS_STALE, STATUS_INTERRUPTED, STATUS_MISSING):
                return P1

        # --- P2: research tier stale; secondary datasets delayed ---
        if tier_lower in {t.lower() for t in _RESEARCH_TIERS}:
            if record.status in (STATUS_STALE, STATUS_INTERRUPTED, STATUS_MISSING):
                return P2

        if dataset in (DATASET_CHIPS, DATASET_MARGIN, DATASET_SHORT_INTEREST):
            if record.status in (STATUS_DELAYED, STATUS_STALE, STATUS_INTERRUPTED):
                return P2

        # Partial update flag from context
        if context and context.get("partial_update"):
            return P2

        # --- P3: broad tier, fundamentals, non-blocking ---
        if tier_lower in {t.lower() for t in _BROAD_TIERS}:
            return P3
        if dataset == DATASET_FUNDAMENTALS:
            return P3

        # Default: assign by severity
        if record.severity == SEVERITY_CRITICAL:
            return P1
        if record.severity == SEVERITY_HIGH:
            return P2
        return P3

    def prioritize(
        self, records: List[DatasetFreshnessRecord]
    ) -> List[DatasetFreshnessRecord]:
        """Return records sorted by priority score ascending (P0 first)."""
        return sorted(records, key=lambda r: self.score(r))

    def explain_priority(self, record: DatasetFreshnessRecord) -> str:
        """Return a human-readable explanation of the assigned priority."""
        p = self.score(record)
        if p == P0:
            reasons = []
            if record.future_date_detected:
                reasons.append("future date detected — NOT counted as fresh")
            if record.date_regression_detected:
                reasons.append("date regression detected")
            if not record.latest_row_valid:
                reasons.append("latest row is invalid")
            if record.status == STATUS_INTERRUPTED and record.tier.lower() in _CORE_TIERS:
                reasons.append("source interruption on core tier")
            return "P0 (critical): " + ("; ".join(reasons) if reasons else record.reason)

        if p == P1:
            return (
                f"P1 (high): core tier ({record.tier}) {record.dataset} "
                f"status={record.status}, lag={record.trading_day_lag}d"
            )
        if p == P2:
            return (
                f"P2 (medium): {record.tier} {record.dataset} "
                f"status={record.status}"
            )
        return (
            f"P3 (low): {record.tier} {record.dataset} "
            f"status={record.status} (non-blocking)"
        )

    def group_by_priority(
        self, records: List[DatasetFreshnessRecord]
    ) -> Dict[str, List[DatasetFreshnessRecord]]:
        """
        Group records by priority level.
        Returns dict with keys 'P0', 'P1', 'P2', 'P3'.
        """
        groups: Dict[str, List[DatasetFreshnessRecord]] = {
            "P0": [],
            "P1": [],
            "P2": [],
            "P3": [],
        }
        for record in records:
            p = self.score(record)
            key = f"P{p}"
            if key in groups:
                groups[key].append(record)
            else:
                groups["P3"].append(record)
        return groups
