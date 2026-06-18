"""
gui/replay_challenge_clock_widget.py — Challenge clock widget v1.2.7

Live timer. Monotonic for duration. Wall clock for display. No freeze.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, Optional
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

class ReplayChallengeClockWidget:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    def __init__(self) -> None:
        self._clock: Optional[Any] = None
    def attach_clock(self, clock: Any) -> None:
        self._clock = clock
    def get_display(self) -> Dict[str, Any]:
        if self._clock is None:
            return {"active_elapsed": 0.0, "remaining": None, "status": "NOT_STARTED"}
        return {
            "active_elapsed": round(self._clock.active_elapsed(), 1),
            "paused_elapsed": round(self._clock.paused_elapsed(), 1),
            "remaining": self._clock.remaining_seconds(),
            "status": self._clock._status,
            "research_only": True,
        }
