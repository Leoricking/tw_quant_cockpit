"""
replay/replay_timeline.py — ReplayTimeline v1.2.0

Controls date navigation through replay session.
Rules:
- previous() at first day: returns current, does NOT go negative
- next() at last day: marks completed, does NOT crash
- jump(): uses calendar to normalize non-trading days
- Cannot jump outside start/end
- Each date change produces an event
- Does NOT auto-play beyond last day

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayTimeline:
    """
    Controls date navigation through replay session.
    """

    def __init__(self, calendar=None):
        self.calendar = calendar
        self._dates: List[str] = []
        self._index: int = 0
        self._completed: bool = False

    def initialize(self, dates: List[str], initial_date: Optional[str] = None) -> None:
        """Set up timeline with sorted list of trading date strings."""
        self._dates = sorted(set(d for d in dates if d))
        self._completed = False
        if initial_date and initial_date in self._dates:
            self._index = self._dates.index(initial_date)
        else:
            self._index = 0

    def current(self) -> Optional[str]:
        """Returns current date string."""
        if not self._dates:
            return None
        if 0 <= self._index < len(self._dates):
            return self._dates[self._index]
        return None

    def previous(self) -> Tuple[Optional[str], bool]:
        """
        Move to previous date.
        Returns (prev_date, changed: bool).
        At first day: returns current, does NOT go negative.
        """
        if not self._dates:
            return None, False
        if self._index <= 0:
            return self._dates[0], False
        self._index -= 1
        self._completed = False
        return self._dates[self._index], True

    def next(self) -> Tuple[Optional[str], bool, bool]:
        """
        Move to next date.
        Returns (next_date, changed: bool, completed: bool).
        At last day: marks completed, does NOT crash.
        """
        if not self._dates:
            return None, False, False
        if self._index >= len(self._dates) - 1:
            self._completed = True
            return self._dates[-1], False, True
        self._index += 1
        completed = (self._index == len(self._dates) - 1)
        if completed:
            self._completed = True
        return self._dates[self._index], True, self._completed

    def jump(self, date: str) -> Tuple[Optional[str], bool]:
        """
        Jump to a date. Uses calendar to normalize non-trading days.
        Cannot jump outside available dates.
        Returns (actual_date, normalized: bool).
        """
        if not self._dates:
            return None, False

        # Clamp to range
        normalized = False
        if date < self._dates[0]:
            logger.warning("[ReplayTimeline] jump(%s) before first date %s — clamping", date, self._dates[0])
            date = self._dates[0]
            normalized = True
        elif date > self._dates[-1]:
            logger.warning("[ReplayTimeline] jump(%s) after last date %s — clamping", date, self._dates[-1])
            date = self._dates[-1]
            normalized = True

        actual_date = date
        if date not in self._dates:
            # Find nearest previous trading day
            if self.calendar:
                self.calendar._dates = self._dates
                nearest = self.calendar.nearest_previous_trading_day(date)
                if nearest:
                    actual_date = nearest
                else:
                    actual_date = self._dates[0]
            else:
                # Find nearest previous in list
                prev = [d for d in self._dates if d <= date]
                actual_date = prev[-1] if prev else self._dates[0]
            normalized = True

        if actual_date in self._dates:
            self._index = self._dates.index(actual_date)
            self._completed = (self._index == len(self._dates) - 1)
        return actual_date, normalized

    def jump_index(self, index: int) -> Tuple[Optional[str], bool]:
        """Jump to a specific index. Returns (date, changed)."""
        if not self._dates:
            return None, False
        idx = max(0, min(index, len(self._dates) - 1))
        changed = (idx != self._index)
        self._index = idx
        self._completed = (self._index == len(self._dates) - 1)
        return self._dates[self._index], changed

    def progress(self) -> Tuple[int, int]:
        """Returns (current_index, total_steps)."""
        return self._index, len(self._dates)

    def remaining(self) -> int:
        """Returns number of remaining steps."""
        if not self._dates:
            return 0
        return max(0, len(self._dates) - 1 - self._index)

    def completed(self) -> bool:
        """Returns True if at last step."""
        return self._completed

    def reset(self) -> None:
        """Reset to first date."""
        self._index = 0
        self._completed = False

    def serialize(self) -> dict:
        """Returns dict representation of timeline state."""
        return {
            "dates": self._dates,
            "index": self._index,
            "completed": self._completed,
            "current": self.current(),
            "total": len(self._dates),
        }

    def restore(self, data: dict) -> None:
        """Restore timeline state from dict."""
        self._dates = data.get("dates", [])
        self._index = int(data.get("index", 0))
        self._completed = bool(data.get("completed", False))
