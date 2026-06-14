"""
data_freshness/freshness_policy.py — Dataset-specific SLA policies for v1.1.3.
[!] Research Only. No Real Orders.
[!] Revenue uses monthly SLA. Fundamentals uses quarterly SLA.
[!] Do not apply daily SLA to monthly/quarterly datasets.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from data_freshness.freshness_schema import (
    DATASET_CHIPS, DATASET_CORPORATE_ACTION, DATASET_DAILY_PRICE,
    DATASET_FUNDAMENTALS, DATASET_MARGIN, DATASET_REVENUE,
    DATASET_SHORT_INTEREST, DATASET_UNKNOWN, DATASET_VOLUME,
    SEVERITY_CRITICAL, SEVERITY_HIGH, SEVERITY_INFO, SEVERITY_LOW,
    SEVERITY_MEDIUM,
    STATUS_ACCEPTABLE, STATUS_DELAYED, STATUS_FRESH, STATUS_INTERRUPTED,
    STATUS_MISSING, STATUS_STALE, STATUS_UNKNOWN,
)

logger = logging.getLogger(__name__)

# SLA definitions per dataset
# daily datasets: fresh/acceptable/delayed/stale thresholds are trading-day lags
# monthly/quarterly: announcement_window_days
_DAILY_SLA: Dict[str, Dict[str, Any]] = {
    DATASET_DAILY_PRICE: dict(
        freq="daily", fresh=0, acceptable=1, delayed=2, stale=5, interrupted=5
    ),
    DATASET_VOLUME: dict(
        freq="daily", fresh=0, acceptable=1, delayed=2, stale=5, interrupted=5
    ),
    DATASET_CHIPS: dict(
        freq="daily", fresh=1, acceptable=2, delayed=3, stale=4, interrupted=5
    ),
    DATASET_MARGIN: dict(
        freq="daily", fresh=1, acceptable=2, delayed=3, stale=4, interrupted=5
    ),
    DATASET_SHORT_INTEREST: dict(
        freq="daily", fresh=1, acceptable=2, delayed=3, stale=4, interrupted=5
    ),
    DATASET_CORPORATE_ACTION: dict(
        freq="event", fresh=0, acceptable=3, delayed=7, stale=30, interrupted=60
    ),
    DATASET_REVENUE: dict(
        freq="monthly", fresh_days=10, announcement_window_days=30
    ),
    DATASET_FUNDAMENTALS: dict(
        freq="quarterly", fresh_days=30, announcement_window_days=90
    ),
    DATASET_UNKNOWN: dict(freq="unknown"),
}

_SEVERITY_MAP: Dict[str, str] = {
    STATUS_FRESH:       SEVERITY_INFO,
    STATUS_ACCEPTABLE:  SEVERITY_LOW,
    STATUS_DELAYED:     SEVERITY_MEDIUM,
    STATUS_STALE:       SEVERITY_HIGH,
    STATUS_INTERRUPTED: SEVERITY_CRITICAL,
    STATUS_MISSING:     SEVERITY_CRITICAL,
    STATUS_UNKNOWN:     SEVERITY_MEDIUM,
}


class FreshnessPolicy:
    """
    Dataset-specific freshness SLA definitions.

    [!] Revenue and Fundamentals have their own frequency policies.
    [!] Do NOT apply trading-day lag SLA to monthly/quarterly data.
    [!] When announcement timing is unknown, display 'approximate'.
    """

    def get_policy(self, dataset: str) -> Dict[str, Any]:
        return _DAILY_SLA.get(dataset, _DAILY_SLA[DATASET_UNKNOWN])

    def classify(
        self,
        dataset: str,
        trading_day_lag: Optional[int],
        context: Optional[Dict] = None,
    ) -> str:
        """Classify freshness status for daily-frequency datasets."""
        if trading_day_lag is None:
            return STATUS_MISSING
        policy = self.get_policy(dataset)
        freq = policy.get("freq", "unknown")
        if freq in ("monthly", "quarterly", "event", "unknown"):
            # Delegate to specialized methods; return UNKNOWN if called directly
            return STATUS_UNKNOWN
        if trading_day_lag < 0:
            return "FUTURE_DATE"
        if trading_day_lag <= policy.get("fresh", 0):
            return STATUS_FRESH
        if trading_day_lag <= policy.get("acceptable", 1):
            return STATUS_ACCEPTABLE
        if trading_day_lag <= policy.get("delayed", 2):
            return STATUS_DELAYED
        if trading_day_lag <= policy.get("stale", 5):
            return STATUS_STALE
        return STATUS_INTERRUPTED

    def classify_monthly(
        self,
        dataset: str,
        calendar_days_since_month_end: Optional[int],
        timing_approximate: bool = True,
    ) -> str:
        """
        Classify freshness for monthly datasets (e.g., REVENUE).
        calendar_days_since_month_end: days since end of reporting month.
        timing_approximate: True if announcement date is uncertain.
        [!] Do NOT judge as stale before expected announcement window.
        """
        if calendar_days_since_month_end is None:
            return STATUS_MISSING
        policy = self.get_policy(dataset)
        window = policy.get("announcement_window_days", 30)
        if calendar_days_since_month_end < 0:
            return "FUTURE_DATE"
        if calendar_days_since_month_end <= window:
            return STATUS_FRESH if not timing_approximate else STATUS_ACCEPTABLE
        if calendar_days_since_month_end <= window + 15:
            return STATUS_DELAYED
        if calendar_days_since_month_end <= window + 45:
            return STATUS_STALE
        return STATUS_INTERRUPTED

    def classify_quarterly(
        self,
        dataset: str,
        calendar_days_since_quarter_end: Optional[int],
        timing_approximate: bool = True,
    ) -> str:
        """
        Classify freshness for quarterly datasets (e.g., FUNDAMENTALS).
        [!] Do NOT require daily update frequency.
        [!] If announcement date unknown, mark timing_approximate=True.
        """
        if calendar_days_since_quarter_end is None:
            return STATUS_MISSING
        policy = self.get_policy(dataset)
        window = policy.get("announcement_window_days", 90)
        if calendar_days_since_quarter_end < 0:
            return "FUTURE_DATE"
        if calendar_days_since_quarter_end <= window:
            return STATUS_FRESH if not timing_approximate else STATUS_ACCEPTABLE
        if calendar_days_since_quarter_end <= window + 30:
            return STATUS_DELAYED
        if calendar_days_since_quarter_end <= window + 90:
            return STATUS_STALE
        return STATUS_INTERRUPTED

    def severity_for(self, status: str) -> str:
        return _SEVERITY_MAP.get(status, SEVERITY_MEDIUM)

    def explain_status(
        self,
        dataset: str,
        status: str,
        trading_day_lag: Optional[int] = None,
    ) -> str:
        policy = self.get_policy(dataset)
        freq = policy.get("freq", "unknown")
        lag_str = f" (lag={trading_day_lag}d)" if trading_day_lag is not None else ""
        if status == STATUS_FRESH:
            return f"{dataset} is fresh{lag_str}"
        if status == STATUS_ACCEPTABLE:
            return f"{dataset} is within acceptable range{lag_str}"
        if status == STATUS_DELAYED:
            return f"{dataset} is delayed beyond SLA{lag_str}"
        if status == STATUS_STALE:
            return f"{dataset} is stale{lag_str}"
        if status == STATUS_INTERRUPTED:
            return f"{dataset} appears interrupted{lag_str} (no update > SLA threshold)"
        if status == STATUS_MISSING:
            return f"{dataset} data file not found"
        if status == "FUTURE_DATE":
            return f"{dataset} has a future date — not counted as fresh"
        if status == "DATE_REGRESSION":
            return f"{dataset} latest date has regressed vs previous monitoring run"
        if freq in ("monthly", "quarterly"):
            return f"{dataset} ({freq} frequency): status={status}"
        return f"{dataset}: status={status}"
