"""
paper_trading/market_data/deduplication_v161.py — Deduplication v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Deduplicates raw market data events by event_id. Bounded cache.
"""
from __future__ import annotations
from collections import OrderedDict
from typing import Set

from paper_trading.market_data.models_v161 import RawMarketDataEvent

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True

DEFAULT_MAX_CACHE_SIZE: int = 10_000


class MarketDataDeduplicator:
    """
    Tracks seen event_ids to detect and drop duplicates.
    Bounded LRU-style cache to avoid unbounded memory growth.
    """

    def __init__(self, max_cache_size: int = DEFAULT_MAX_CACHE_SIZE) -> None:
        self._seen: OrderedDict = OrderedDict()
        self._max_size = max_cache_size
        self._duplicate_count: int = 0
        self._total_checked: int = 0

    def is_duplicate(self, event: RawMarketDataEvent) -> bool:
        """Returns True if this event_id was already seen (duplicate)."""
        self._total_checked += 1
        eid = event.event_id

        if eid in self._seen:
            self._duplicate_count += 1
            return True

        # Add to seen cache
        self._seen[eid] = True
        # Evict oldest if over limit
        if len(self._seen) > self._max_size:
            self._seen.popitem(last=False)
        return False

    def filter_batch(self, events: list) -> list:
        """Return only non-duplicate events."""
        return [e for e in events if not self.is_duplicate(e)]

    @property
    def duplicate_count(self) -> int:
        return self._duplicate_count

    @property
    def total_checked(self) -> int:
        return self._total_checked

    def reset(self) -> None:
        self._seen.clear()
        self._duplicate_count = 0
        self._total_checked = 0
