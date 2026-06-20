"""
data/providers/data_gov_tw/freshness_policy_v143.py — Freshness policy v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Freshness calculated per dataset based on update_frequency and source_timestamp.
[!] UNKNOWN frequency cannot claim freshness.
[!] fetched_at ≠ data source timestamp.
[!] date-stable: clock is injectable.
"""
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, Optional

from data.providers.data_gov_tw.models_v143 import FreshnessStatus, UpdateFrequency

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Grace periods by frequency
_GRACE_PERIODS: Dict[str, int] = {
    UpdateFrequency.DAILY.value: 2,       # 2 days
    UpdateFrequency.WEEKLY.value: 10,     # 10 days
    UpdateFrequency.MONTHLY.value: 35,    # 35 days
    UpdateFrequency.QUARTERLY.value: 95,  # 95 days
    UpdateFrequency.YEARLY.value: 370,    # 370 days
    UpdateFrequency.IRREGULAR.value: 90,
    UpdateFrequency.UNSCHEDULED.value: 90,
}

_NEAR_STALE_FRACTION = 0.75  # Warn when >75% of grace period elapsed


def _parse_iso(ts: str) -> Optional[datetime.datetime]:
    try:
        return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


class DataGovTwFreshnessPolicy:
    """
    Calculates freshness status for data.gov.tw datasets.

    Rules:
    - Freshness depends on dataset's update_frequency metadata
    - source_timestamp takes priority over fetched_at
    - fetched_at is NOT the data timestamp
    - UNKNOWN frequency → UNKNOWN freshness (never fresh)
    - Removed dataset → BLOCKED
    - Clock injectable for deterministic tests
    """

    def __init__(self, clock: Optional[Callable[[], datetime.datetime]] = None) -> None:
        self._clock = clock or (lambda: datetime.datetime.now(datetime.timezone.utc))

    def evaluate(
        self,
        update_frequency: Optional[str],
        source_timestamp: Optional[str],
        fetched_at: Optional[str] = None,
        dataset_status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Evaluate freshness for a dataset. Returns FreshnessStatus and details."""
        now = self._clock()
        if not now.tzinfo:
            now = now.replace(tzinfo=datetime.timezone.utc)

        # Removed/blocked datasets
        from data.providers.data_gov_tw.models_v143 import DatasetStatus
        if dataset_status in (DatasetStatus.REMOVED.value, DatasetStatus.BLOCKED.value):
            return {
                "status": FreshnessStatus.BLOCKED.value,
                "reason": f"Dataset status is {dataset_status}",
                "formal_freshness": False,
            }

        # Unknown frequency → cannot claim freshness
        freq = (update_frequency or UpdateFrequency.UNKNOWN.value).upper()
        if freq in (UpdateFrequency.UNKNOWN.value, UpdateFrequency.REAL_TIME_METADATA_ONLY.value):
            return {
                "status": FreshnessStatus.UNKNOWN.value,
                "reason": f"Update frequency is {freq} — cannot determine freshness",
                "formal_freshness": False,
            }

        # Determine reference timestamp (source_timestamp preferred)
        ref_ts_str = source_timestamp or fetched_at
        if not ref_ts_str:
            return {
                "status": FreshnessStatus.UNKNOWN.value,
                "reason": "No source_timestamp or fetched_at available",
                "formal_freshness": False,
            }

        ref_ts = _parse_iso(ref_ts_str)
        if ref_ts is None:
            return {
                "status": FreshnessStatus.UNKNOWN.value,
                "reason": f"Cannot parse timestamp: {ref_ts_str}",
                "formal_freshness": False,
            }

        if not ref_ts.tzinfo:
            ref_ts = ref_ts.replace(tzinfo=datetime.timezone.utc)

        age_days = (now - ref_ts).total_seconds() / 86400
        grace_days = _GRACE_PERIODS.get(freq, 90)

        if age_days < 0:
            return {
                "status": FreshnessStatus.UNKNOWN.value,
                "reason": "Reference timestamp is in the future",
                "formal_freshness": False,
            }

        if age_days <= grace_days * _NEAR_STALE_FRACTION:
            status = FreshnessStatus.FRESH.value
            formal_freshness = True
        elif age_days <= grace_days:
            status = FreshnessStatus.NEAR_STALE.value
            formal_freshness = True
        else:
            # Check if delayed or stale
            if age_days <= grace_days * 1.5:
                status = FreshnessStatus.DELAYED.value
            else:
                status = FreshnessStatus.STALE.value
            formal_freshness = False

        return {
            "status": status,
            "age_days": round(age_days, 2),
            "grace_days": grace_days,
            "update_frequency": freq,
            "source_timestamp": source_timestamp,
            "fetched_at_is_not_source": source_timestamp is None,
            "reason": f"Age {age_days:.1f}d vs grace {grace_days}d",
            "formal_freshness": formal_freshness,
        }
