"""
gui/replay_timeframe_compare_dialog.py — ReplayTimeframeCompareDialog v1.2.5

Compare two timestamps, timeframes, or sessions. No future reveal.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
NO_FUTURE_REVEAL = True

FORBIDDEN_COMPARE_FIELDS = [
    "forward_return", "realized_pnl", "final_result",
    "future_high", "future_low", "hindsight_score",
    "outcome", "final_session_high", "final_session_low",
]


class ReplayTimeframeCompareDialog:
    """
    Compare two timestamps, timeframes, or sessions side-by-side.
    No future reveal. Research only.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    NO_FUTURE_REVEAL = True

    COMPARE_MODES = ["TIMESTAMP", "TIMEFRAME", "SESSION"]

    def __init__(self, parent=None) -> None:
        self._parent = parent
        self._mode: str = "TIMESTAMP"
        self._left: Optional[Dict[str, Any]] = None
        self._right: Optional[Dict[str, Any]] = None
        self._result: Optional[Dict[str, Any]] = None

    def set_mode(self, mode: str) -> None:
        if mode in self.COMPARE_MODES:
            self._mode = mode

    def set_left(self, data: Dict[str, Any]) -> None:
        self._left = self._strip_forbidden(data)

    def set_right(self, data: Dict[str, Any]) -> None:
        self._right = self._strip_forbidden(data)

    def set_result(self, result: Dict[str, Any]) -> None:
        self._result = self._strip_forbidden(result)

    def _strip_forbidden(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in data.items() if k not in FORBIDDEN_COMPARE_FIELDS}

    def get_display_data(self) -> Dict[str, Any]:
        return {
            "mode": self._mode,
            "left": self._left or {},
            "right": self._right or {},
            "result": self._result or {},
            "no_future_reveal": True,
            "research_only": True,
        }

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "widget": "ReplayTimeframeCompareDialog",
            "version": "v1.2.5",
            "mode": self._mode,
            "no_future_reveal": True,
            "research_only": True,
        }
