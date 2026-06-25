"""
paper_trading/strategy/cooldown_v162.py — Cooldown manager for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
import threading
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class CooldownManager:
    """
    Per-ticker cooldown tracker for paper strategy decisions.

    After a decision is recorded for a ticker, that ticker is on cooldown
    for `cooldown_seconds`. No new signals for that ticker are processed
    until the cooldown expires.

    Thread-safe. Separate from StrategyState for modularity.
    """

    def __init__(self, cooldown_seconds: int = 60) -> None:
        assert cooldown_seconds >= 0, "cooldown_seconds must be non-negative"
        self.cooldown_seconds = cooldown_seconds
        self._lock = threading.Lock()
        self._last_decision: Dict[str, datetime] = {}
        self._cooldown_count: int = 0
        self._record_count: int = 0

    def is_on_cooldown(self, ticker: str) -> bool:
        with self._lock:
            last = self._last_decision.get(ticker)
            if last is None:
                return False
            elapsed = (_utcnow() - last).total_seconds()
            return elapsed < self.cooldown_seconds

    def seconds_remaining(self, ticker: str) -> float:
        with self._lock:
            last = self._last_decision.get(ticker)
            if last is None:
                return 0.0
            elapsed = (_utcnow() - last).total_seconds()
            return max(0.0, self.cooldown_seconds - elapsed)

    def record(self, ticker: str) -> None:
        """Record a decision for ticker, resetting its cooldown."""
        with self._lock:
            was_on = ticker in self._last_decision
            self._last_decision[ticker] = _utcnow()
            self._record_count += 1
            logger.debug(
                "[v1.6.2][cooldown] Recorded %s (was_on=%s cooldown=%ds)",
                ticker, was_on, self.cooldown_seconds
            )

    def check_and_record(self, ticker: str) -> bool:
        """
        Combined check + record.
        Returns True if ticker is on cooldown (should be blocked).
        If NOT on cooldown, records immediately and returns False.
        """
        with self._lock:
            last = self._last_decision.get(ticker)
            if last is not None:
                elapsed = (_utcnow() - last).total_seconds()
                if elapsed < self.cooldown_seconds:
                    self._cooldown_count += 1
                    logger.debug(
                        "[v1.6.2][cooldown] %s on cooldown (%.1fs remaining)",
                        ticker, self.cooldown_seconds - elapsed
                    )
                    return True  # blocked
            # Not on cooldown — record and allow
            self._last_decision[ticker] = _utcnow()
            self._record_count += 1
            return False  # allowed

    def clear(self, ticker: str) -> None:
        with self._lock:
            self._last_decision.pop(ticker, None)

    def clear_all(self) -> None:
        with self._lock:
            self._last_decision.clear()

    def snapshot(self) -> Dict[str, str]:
        """Return {ticker: last_decision_iso} for checkpointing."""
        with self._lock:
            return {
                t: dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
                for t, dt in self._last_decision.items()
            }

    def restore(self, snapshot: Dict[str, str]) -> None:
        """Restore from a checkpoint snapshot."""
        with self._lock:
            self._last_decision = {}
            for ticker, iso in snapshot.items():
                try:
                    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
                    self._last_decision[ticker] = dt
                except ValueError:
                    pass

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "cooldown_seconds": self.cooldown_seconds,
                "tracked_tickers": len(self._last_decision),
                "cooldown_count": self._cooldown_count,
                "record_count": self._record_count,
                "paper_only": True,
            }
