"""
replay/challenge_clock.py — ReplayChallengeClock v1.2.7

Monotonic clock for duration. Wall clock for display only.
Pause does not count active elapsed. Timeout only marks status.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayChallengeClock:
    """
    Challenge clock.

    - Monotonic clock for duration measurement.
    - Wall clock for display only.
    - Pause does not count active elapsed time.
    - Timeout only marks status; never executes a decision.
    - Cancelled/failed attempts still preserve elapsed time.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    TIMEOUT_EXECUTES_DECISION = False

    def __init__(self, max_duration_seconds: Optional[float] = None) -> None:
        self.max_duration_seconds = max_duration_seconds
        self._start_mono: Optional[float] = None
        self._pause_mono: Optional[float] = None
        self._active_elapsed: float = 0.0
        self._paused_elapsed: float = 0.0
        self._decision_start_mono: Optional[float] = None
        self._decision_elapsed: float = 0.0
        self._status: str = "NOT_STARTED"
        self._start_wall: Optional[str] = None
        self._end_wall: Optional[str] = None

    def start(self) -> None:
        """Start the clock."""
        self._start_mono = time.monotonic()
        self._start_wall = datetime.now(timezone.utc).isoformat()
        self._status = "RUNNING"
        self._decision_start_mono = self._start_mono

    def pause(self) -> None:
        """Pause the clock. Paused time does not count as active elapsed."""
        if self._status != "RUNNING":
            return
        now = time.monotonic()
        if self._start_mono is not None:
            # Add elapsed since last resume/start to active
            if self._pause_mono is None:
                self._active_elapsed += now - self._start_mono
                self._start_mono = None
        self._pause_mono = now
        self._status = "PAUSED"

    def resume(self) -> None:
        """Resume the clock after pause."""
        if self._status != "PAUSED":
            return
        now = time.monotonic()
        if self._pause_mono is not None:
            self._paused_elapsed += now - self._pause_mono
        self._pause_mono = None
        self._start_mono = now
        self._status = "RUNNING"

    def tick(self) -> None:
        """Update active elapsed (call periodically)."""
        if self._status == "RUNNING" and self._start_mono is not None:
            now = time.monotonic()
            # Check timeout
            current_active = self._active_elapsed + (now - self._start_mono)
            if self.max_duration_seconds is not None and current_active >= self.max_duration_seconds:
                self.timeout()

    def active_elapsed(self) -> float:
        """Return active elapsed seconds (excludes paused time)."""
        if self._status == "RUNNING" and self._start_mono is not None:
            return self._active_elapsed + (time.monotonic() - self._start_mono)
        return self._active_elapsed

    def paused_elapsed(self) -> float:
        """Return total paused seconds."""
        if self._status == "PAUSED" and self._pause_mono is not None:
            return self._paused_elapsed + (time.monotonic() - self._pause_mono)
        return self._paused_elapsed

    def decision_elapsed(self) -> float:
        """Return elapsed from start to first decision action."""
        return self._decision_elapsed

    def remaining_seconds(self) -> Optional[float]:
        """Return remaining seconds, or None if no time limit."""
        if self.max_duration_seconds is None:
            return None
        remaining = self.max_duration_seconds - self.active_elapsed()
        return max(0.0, remaining)

    def timeout(self) -> None:
        """Mark as timed out. Does NOT execute any decision."""
        if self._status == "RUNNING" and self._start_mono is not None:
            now = time.monotonic()
            self._active_elapsed += now - self._start_mono
            self._start_mono = None
        self._end_wall = datetime.now(timezone.utc).isoformat()
        self._status = "TIMEOUT"
        # IMPORTANT: timeout only marks status — no decision is executed

    def finish(self) -> None:
        """Mark as finished."""
        if self._status == "RUNNING" and self._start_mono is not None:
            now = time.monotonic()
            self._active_elapsed += now - self._start_mono
            self._start_mono = None
        self._end_wall = datetime.now(timezone.utc).isoformat()
        self._status = "FINISHED"

    def cancel(self) -> None:
        """Cancel. Preserves elapsed time."""
        if self._status == "RUNNING" and self._start_mono is not None:
            now = time.monotonic()
            self._active_elapsed += now - self._start_mono
            self._start_mono = None
        elif self._status == "PAUSED" and self._pause_mono is not None:
            now = time.monotonic()
            self._paused_elapsed += now - self._pause_mono
            self._pause_mono = None
        self._end_wall = datetime.now(timezone.utc).isoformat()
        self._status = "CANCELLED"
        # Elapsed time preserved even on cancel

    def record_decision(self) -> None:
        """Record the elapsed time at the moment of decision."""
        self._decision_elapsed = self.active_elapsed()

    def summary(self) -> Dict[str, Any]:
        return {
            "status":                self._status,
            "active_elapsed":        round(self.active_elapsed(), 2),
            "paused_elapsed":        round(self.paused_elapsed(), 2),
            "decision_elapsed":      round(self._decision_elapsed, 2),
            "remaining_seconds":     self.remaining_seconds(),
            "max_duration_seconds":  self.max_duration_seconds,
            "start_wall":            self._start_wall,
            "end_wall":              self._end_wall,
            "timeout_executes_decision": False,
            "research_only":         True,
            "no_real_orders":        True,
        }
