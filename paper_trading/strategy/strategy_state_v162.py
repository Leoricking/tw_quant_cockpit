"""
paper_trading/strategy/strategy_state_v162.py — Runtime state tracker for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import threading
from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Deque, Dict, List, Optional

from paper_trading.strategy.enums_v162 import StrategyStatus
from paper_trading.strategy.models_v162 import _now_iso


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class StrategyState:
    """
    Thread-safe runtime state for a single paper strategy instance.

    Tracks:
    - Lifecycle status
    - Cooldown map (ticker → last decision time)
    - Rate-limit window (rolling signal timestamps)
    - Open proposals (set of proposal_ids)
    - Counters
    """

    def __init__(
        self,
        strategy_id: str,
        max_signals_per_minute: int = 10,
        cooldown_seconds: int = 60,
        max_open_proposals: int = 5,
    ) -> None:
        self.strategy_id = strategy_id
        self.max_signals_per_minute = max_signals_per_minute
        self.cooldown_seconds = cooldown_seconds
        self.max_open_proposals = max_open_proposals

        self._lock = threading.Lock()
        self._status = StrategyStatus.REGISTERED

        # Cooldown: ticker → last decision UTC timestamp
        self._cooldown_map: Dict[str, datetime] = {}

        # Rate limit: rolling window of signal timestamps (max 60 s)
        self._signal_window: Deque[datetime] = deque()

        # Open proposals
        self._open_proposals: List[str] = []

        # Counters
        self.signal_count: int = 0
        self.decision_count: int = 0
        self.proposal_count: int = 0
        self.approved_count: int = 0
        self.rejected_count: int = 0
        self.error_count: int = 0

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    @property
    def status(self) -> StrategyStatus:
        with self._lock:
            return self._status

    def set_status(self, status: StrategyStatus) -> None:
        with self._lock:
            self._status = status

    # ------------------------------------------------------------------
    # Cooldown
    # ------------------------------------------------------------------

    def is_on_cooldown(self, ticker: str) -> bool:
        """Return True if ticker is still within the cooldown window."""
        with self._lock:
            last = self._cooldown_map.get(ticker)
            if last is None:
                return False
            elapsed = (_utcnow() - last).total_seconds()
            return elapsed < self.cooldown_seconds

    def record_decision(self, ticker: str) -> None:
        """Record a decision for ticker, starting its cooldown."""
        with self._lock:
            self._cooldown_map[ticker] = _utcnow()
            self.decision_count += 1

    def cooldown_remaining(self, ticker: str) -> float:
        """Seconds remaining in cooldown for ticker. 0.0 if not on cooldown."""
        with self._lock:
            last = self._cooldown_map.get(ticker)
            if last is None:
                return 0.0
            elapsed = (_utcnow() - last).total_seconds()
            remaining = self.cooldown_seconds - elapsed
            return max(0.0, remaining)

    def cooldown_snapshot(self) -> Dict[str, str]:
        """Return {ticker: last_decision_iso} for checkpointing."""
        with self._lock:
            return {
                ticker: dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
                for ticker, dt in self._cooldown_map.items()
            }

    def restore_cooldown(self, snapshot: Dict[str, str]) -> None:
        """Restore cooldown map from a checkpoint snapshot."""
        with self._lock:
            self._cooldown_map = {}
            for ticker, iso in snapshot.items():
                try:
                    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
                    self._cooldown_map[ticker] = dt
                except ValueError:
                    pass

    # ------------------------------------------------------------------
    # Rate limiting
    # ------------------------------------------------------------------

    def _prune_signal_window(self) -> None:
        """Remove entries older than 60 seconds. Must hold lock."""
        cutoff = _utcnow() - timedelta(seconds=60)
        while self._signal_window and self._signal_window[0] < cutoff:
            self._signal_window.popleft()

    def is_rate_limited(self) -> bool:
        """Return True if signals-per-minute limit is exceeded."""
        with self._lock:
            self._prune_signal_window()
            return len(self._signal_window) >= self.max_signals_per_minute

    def record_signal(self) -> None:
        """Record a new signal timestamp for rate-limit tracking."""
        with self._lock:
            self._prune_signal_window()
            self._signal_window.append(_utcnow())
            self.signal_count += 1

    def rate_window_snapshot(self) -> List[str]:
        """Return list of signal timestamps for checkpointing."""
        with self._lock:
            return [
                dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
                for dt in self._signal_window
            ]

    def restore_rate_window(self, snapshot: List[str]) -> None:
        """Restore rate-limit window from a checkpoint snapshot."""
        with self._lock:
            self._signal_window = deque()
            for iso in snapshot:
                try:
                    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
                    self._signal_window.append(dt)
                except ValueError:
                    pass

    # ------------------------------------------------------------------
    # Open proposals
    # ------------------------------------------------------------------

    def add_open_proposal(self, proposal_id: str) -> bool:
        """
        Track an open proposal. Returns True if added, False if at capacity.
        """
        with self._lock:
            if len(self._open_proposals) >= self.max_open_proposals:
                return False
            if proposal_id not in self._open_proposals:
                self._open_proposals.append(proposal_id)
                self.proposal_count += 1
            return True

    def close_proposal(self, proposal_id: str) -> bool:
        """Remove proposal from open set. Returns True if removed."""
        with self._lock:
            if proposal_id in self._open_proposals:
                self._open_proposals.remove(proposal_id)
                return True
            return False

    def open_proposal_count(self) -> int:
        with self._lock:
            return len(self._open_proposals)

    def open_proposals_snapshot(self) -> List[str]:
        with self._lock:
            return list(self._open_proposals)

    def at_proposal_capacity(self) -> bool:
        with self._lock:
            return len(self._open_proposals) >= self.max_open_proposals

    # ------------------------------------------------------------------
    # Counter helpers
    # ------------------------------------------------------------------

    def increment_approved(self) -> None:
        with self._lock:
            self.approved_count += 1

    def increment_rejected(self) -> None:
        with self._lock:
            self.rejected_count += 1

    def increment_error(self) -> None:
        with self._lock:
            self.error_count += 1

    def summary(self) -> Dict:
        with self._lock:
            return {
                "strategy_id": self.strategy_id,
                "status": self._status.value,
                "signal_count": self.signal_count,
                "decision_count": self.decision_count,
                "proposal_count": self.proposal_count,
                "approved_count": self.approved_count,
                "rejected_count": self.rejected_count,
                "error_count": self.error_count,
                "open_proposals": len(self._open_proposals),
                "rate_window_size": len(self._signal_window),
                "cooldown_tickers": list(self._cooldown_map.keys()),
            }
