"""
gui/replay_timeframe_chart_grid.py — ReplayTimeframeChartGrid v1.2.5

2x2 chart grid with synchronized cursor and independent zoom.
Partial bar markers. No future K-lines.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayTimeframeChartGrid:
    """
    2x2 chart grid for multi-timeframe replay.
    D1 (top-left), 60m (top-right), 20m (bottom-left), 5m (bottom-right).
    Switchable 1m. Synchronized cursor. Independent zoom.
    Partial bar markers. No future K-lines.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    DEFAULT_LAYOUT = {
        "top_left":     "D1",
        "top_right":    "M60",
        "bottom_left":  "M20",
        "bottom_right": "M5",
    }

    def __init__(self, parent=None) -> None:
        self._parent = parent
        self._layout = dict(self.DEFAULT_LAYOUT)
        self._show_1m = False
        self._replay_timestamp: Optional[str] = None

    def set_replay_timestamp(self, timestamp: str) -> None:
        """Set current replay timestamp. No bars after this will be shown."""
        self._replay_timestamp = timestamp

    def toggle_1m(self, show: bool = True) -> None:
        """Toggle 1m chart visibility."""
        self._show_1m = show

    def get_layout(self) -> Dict[str, str]:
        """Return current layout configuration."""
        layout = dict(self._layout)
        if self._show_1m:
            layout["1m_visible"] = True
        return layout

    def get_chart_config(self, timeframe: str) -> Dict[str, Any]:
        """Return chart configuration for a specific timeframe."""
        return {
            "timeframe": timeframe,
            "replay_timestamp": self._replay_timestamp,
            "synchronized_cursor": True,
            "independent_zoom": True,
            "show_partial_bar_marker": True,
            "no_future_klines": True,
            "indicators": {
                "ma_lines": ["MA5", "MA10", "MA20", "MA60"],
                "volume_panel": True,
                "oscillator_tabs": ["KD", "MACD", "RSI"],
            },
            "support_resistance": True,
            "research_only": True,
        }

    def validate_no_future_klines(self, bars: List[Dict[str, Any]]) -> List[str]:
        """Validate no bars after replay_timestamp are displayed."""
        if not self._replay_timestamp:
            return []
        violations = []
        for bar in bars:
            ts = bar.get("timestamp", "")
            if ts and ts > self._replay_timestamp:
                violations.append(f"Future K-line: {ts} > replay {self._replay_timestamp}")
        return violations

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "widget": "ReplayTimeframeChartGrid",
            "version": "v1.2.5",
            "layout": self._layout,
            "show_1m": self._show_1m,
            "no_future_klines": True,
            "partial_bar_marker": True,
            "research_only": True,
        }
