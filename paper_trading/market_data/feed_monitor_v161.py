"""
paper_trading/market_data/feed_monitor_v161.py — Feed Monitor v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Monitors feed health: heartbeat liveness, gap detection, failure classification.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from paper_trading.market_data.enums_v161 import FeedFailureType, MarketDataSessionStatus

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True

DEFAULT_HEARTBEAT_TIMEOUT_SECONDS: int = 30
DEFAULT_MAX_GAP_COUNT: int = 10


class FeedHealthReport:
    def __init__(
        self,
        adapter_id: str,
        is_alive: bool,
        last_heartbeat_utc: Optional[str],
        failure_type: Optional[FeedFailureType],
        gap_count: int,
        message: str,
    ) -> None:
        self.adapter_id = adapter_id
        self.is_alive = is_alive
        self.last_heartbeat_utc = last_heartbeat_utc
        self.failure_type = failure_type
        self.gap_count = gap_count
        self.message = message


class FeedMonitor:
    """
    Monitors market data feed health.
    Tracks heartbeats, gap counts, and classifies failures.
    No trading action — monitoring only.
    """

    def __init__(
        self,
        heartbeat_timeout_s: int = DEFAULT_HEARTBEAT_TIMEOUT_SECONDS,
        max_gap_count: int = DEFAULT_MAX_GAP_COUNT,
        clock_now_utc: Optional[callable] = None,
    ) -> None:
        self._heartbeat_timeout = heartbeat_timeout_s
        self._max_gap_count = max_gap_count
        self._clock = clock_now_utc or (lambda: datetime.now(timezone.utc))
        self._last_heartbeat: Dict[str, str] = {}
        self._gap_counts: Dict[str, int] = {}
        self._failure_types: Dict[str, Optional[FeedFailureType]] = {}

    def record_heartbeat(self, adapter_id: str) -> None:
        self._last_heartbeat[adapter_id] = self._clock().isoformat()

    def record_gap(self, adapter_id: str) -> None:
        self._gap_counts[adapter_id] = self._gap_counts.get(adapter_id, 0) + 1

    def record_failure(self, adapter_id: str, failure_type: FeedFailureType) -> None:
        self._failure_types[adapter_id] = failure_type

    def clear_failure(self, adapter_id: str) -> None:
        self._failure_types.pop(adapter_id, None)

    def get_health(self, adapter_id: str) -> FeedHealthReport:
        last_hb = self._last_heartbeat.get(adapter_id)
        gap_count = self._gap_counts.get(adapter_id, 0)
        failure = self._failure_types.get(adapter_id)

        is_alive = True
        message = "OK"

        if failure:
            is_alive = False
            message = f"Feed failure: {failure.value}"
        elif last_hb:
            try:
                hb_dt = datetime.fromisoformat(last_hb.replace("Z", "+00:00"))
                now = self._clock()
                if not hb_dt.tzinfo:
                    hb_dt = hb_dt.replace(tzinfo=timezone.utc)
                age = (now - hb_dt).total_seconds()
                if age > self._heartbeat_timeout:
                    is_alive = False
                    message = f"Heartbeat timeout: {age:.1f}s > {self._heartbeat_timeout}s"
            except Exception:
                is_alive = False
                message = "Cannot parse heartbeat timestamp"
        else:
            is_alive = False
            message = "No heartbeat received"

        if gap_count > self._max_gap_count:
            is_alive = False
            message += f"; excessive gaps: {gap_count}"

        return FeedHealthReport(
            adapter_id=adapter_id,
            is_alive=is_alive,
            last_heartbeat_utc=last_hb,
            failure_type=failure,
            gap_count=gap_count,
            message=message,
        )

    def reset(self, adapter_id: str) -> None:
        self._last_heartbeat.pop(adapter_id, None)
        self._gap_counts.pop(adapter_id, None)
        self._failure_types.pop(adapter_id, None)
