"""
paper_trading/market_data/freshness_v161.py — Freshness Classifier v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Classifies event freshness. Future date NOT counted as fresh.
"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from typing import Optional

from paper_trading.market_data.enums_v161 import FreshnessStatus, SourceClass

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
FUTURE_DATE_COUNTS_AS_FRESH: bool = False  # Key invariant

# Default SLA thresholds
DEFAULT_FRESH_THRESHOLD_SECONDS: int = 5
DEFAULT_DELAYED_THRESHOLD_SECONDS: int = 60
DEFAULT_STALE_THRESHOLD_SECONDS: int = 300


class FreshnessClassifier:
    """
    Classifies a canonical event's freshness relative to wall-clock time.
    FUTURE_DATE_COUNTS_AS_FRESH=False: future timestamps → UNKNOWN.
    REPLAY/FIXTURE/OFFLINE sources → NOT_APPLICABLE.
    """

    def __init__(
        self,
        fresh_threshold_s: int = DEFAULT_FRESH_THRESHOLD_SECONDS,
        delayed_threshold_s: int = DEFAULT_DELAYED_THRESHOLD_SECONDS,
        stale_threshold_s: int = DEFAULT_STALE_THRESHOLD_SECONDS,
        clock_now_utc: Optional[callable] = None,
    ) -> None:
        self._fresh_t = fresh_threshold_s
        self._delayed_t = delayed_threshold_s
        self._stale_t = stale_threshold_s
        self._clock = clock_now_utc or (lambda: datetime.now(timezone.utc))

    def classify(self, event_timestamp_utc: str, source_class: SourceClass) -> FreshnessStatus:
        # Non-live sources are not subject to freshness
        if source_class in (SourceClass.REPLAY, SourceClass.FIXTURE, SourceClass.OFFLINE, SourceClass.SIMULATION):
            return FreshnessStatus.NOT_APPLICABLE

        if source_class == SourceClass.UNKNOWN:
            return FreshnessStatus.UNKNOWN

        try:
            event_dt = datetime.fromisoformat(event_timestamp_utc.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return FreshnessStatus.UNKNOWN

        now = self._clock()
        if not event_dt.tzinfo:
            event_dt = event_dt.replace(tzinfo=timezone.utc)

        # Future date check — not counted as fresh
        if event_dt > now:
            return FreshnessStatus.UNKNOWN

        age_seconds = (now - event_dt).total_seconds()

        if age_seconds <= self._fresh_t:
            return FreshnessStatus.FRESH
        if age_seconds <= self._delayed_t:
            return FreshnessStatus.DELAYED
        if age_seconds <= self._stale_t:
            return FreshnessStatus.STALE
        return FreshnessStatus.EXPIRED
