"""
gui/replay_timeframe_selector.py — ReplayTimeframeSelector v1.2.5

Displays D1/60m/20m/5m/1m with status badges.
Emits signal on selection change.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

TIMEFRAME_LABELS = {
    "D1": "Daily", "M60": "60m", "M20": "20m", "M5": "5m", "M1": "1m"
}
STATUS_BADGES = {
    "AVAILABLE": "✓", "UNAVAILABLE": "✗", "PARTIAL": "~", "STALE": "⚠", "BLOCKED": "🚫"
}


class ReplayTimeframeSelector:
    """
    Timeframe selector widget for multi-timeframe replay.
    Displays D1/60m/20m/5m/1m with availability status badges.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    TIMEFRAME_ORDER = ["D1", "M60", "M20", "M5", "M1"]

    def __init__(self, parent=None) -> None:
        self._parent = parent
        self._selected: Optional[str] = "M5"
        self._statuses: Dict[str, str] = {tf: "UNAVAILABLE" for tf in self.TIMEFRAME_ORDER}
        self._callbacks: List[Callable] = []

    def update_statuses(self, statuses: Dict[str, str]) -> None:
        """Update timeframe availability statuses."""
        self._statuses.update(statuses)

    def select(self, timeframe: str) -> None:
        """Select a timeframe and emit signal."""
        if timeframe in self.TIMEFRAME_ORDER:
            self._selected = timeframe
            for cb in self._callbacks:
                cb(timeframe)

    def on_selection_changed(self, callback: Callable) -> None:
        """Register callback for selection changes."""
        self._callbacks.append(callback)

    def get_selected(self) -> Optional[str]:
        """Return currently selected timeframe."""
        return self._selected

    def get_display_items(self) -> List[Dict[str, Any]]:
        """Return list of display items with labels and badges."""
        items = []
        for tf in self.TIMEFRAME_ORDER:
            status = self._statuses.get(tf, "UNAVAILABLE")
            badge  = STATUS_BADGES.get(status, "?")
            items.append({
                "timeframe": tf,
                "label": TIMEFRAME_LABELS.get(tf, tf),
                "status": status,
                "badge": badge,
                "selected": tf == self._selected,
            })
        return items

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "widget": "ReplayTimeframeSelector",
            "version": "v1.2.5",
            "timeframes": self.TIMEFRAME_ORDER,
            "selected": self._selected,
            "research_only": True,
        }
