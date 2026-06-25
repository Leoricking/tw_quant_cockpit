"""
paper_trading/strategy/signal_dedup_v162.py — Signal deduplication for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
import threading
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

from paper_trading.strategy.models_v162 import PaperSignal

logger = logging.getLogger(__name__)

_DEFAULT_WINDOW_SECONDS = 30
_DEFAULT_MAX_CACHE = 500


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SignalDeduplicator:
    """
    Deduplicates paper signals within a rolling time window.

    A signal is considered a duplicate if another signal with the same
    dedup_key was seen within the last `window_seconds` seconds.

    Thread-safe. LRU-bounded cache (max_cache entries).
    """

    def __init__(
        self,
        window_seconds: int = _DEFAULT_WINDOW_SECONDS,
        max_cache: int = _DEFAULT_MAX_CACHE,
    ) -> None:
        self.window_seconds = window_seconds
        self.max_cache = max_cache
        self._lock = threading.Lock()
        # dedup_key → (first_seen UTC, count)
        self._cache: OrderedDict[str, Tuple[datetime, int]] = OrderedDict()

    def is_duplicate(self, signal: PaperSignal) -> bool:
        """Return True if signal's dedup_key was seen within the window."""
        key = signal.dedup_key
        if not key:
            return False
        with self._lock:
            self._evict_expired()
            return key in self._cache

    def record(self, signal: PaperSignal) -> bool:
        """
        Record a signal. Returns True if it was a duplicate.
        Marks signal.is_duplicate accordingly.
        """
        key = signal.dedup_key
        if not key:
            signal.is_duplicate = False
            return False

        with self._lock:
            self._evict_expired()
            if key in self._cache:
                ts, count = self._cache[key]
                self._cache[key] = (ts, count + 1)
                self._cache.move_to_end(key)
                signal.is_duplicate = True
                logger.debug(
                    "[v1.6.2][dedup] Duplicate signal key=%s ticker=%s count=%d",
                    key[:8], signal.ticker, count + 1
                )
                return True

            # New entry
            self._cache[key] = (_utcnow(), 1)
            if len(self._cache) > self.max_cache:
                self._cache.popitem(last=False)
            signal.is_duplicate = False
            return False

    def filter_duplicates(self, signals: List[PaperSignal]) -> List[PaperSignal]:
        """
        Process a batch. Records all and returns only non-duplicates.
        Duplicate signals have is_duplicate=True but are excluded from result.
        """
        result: List[PaperSignal] = []
        for sig in signals:
            is_dup = self.record(sig)
            if not is_dup:
                result.append(sig)
        return result

    def _evict_expired(self) -> None:
        """Remove entries older than window_seconds. Must hold lock."""
        cutoff = _utcnow() - timedelta(seconds=self.window_seconds)
        expired = [k for k, (ts, _) in self._cache.items() if ts < cutoff]
        for k in expired:
            del self._cache[k]

    def cache_size(self) -> int:
        with self._lock:
            return len(self._cache)

    def reset(self) -> None:
        with self._lock:
            self._cache.clear()

    def snapshot(self) -> Dict[str, str]:
        """Return {key: first_seen_iso} for diagnostics."""
        with self._lock:
            return {
                k: ts.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
                for k, (ts, _) in self._cache.items()
            }
