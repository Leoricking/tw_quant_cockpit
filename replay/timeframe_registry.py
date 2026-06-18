"""
replay/timeframe_registry.py — ReplayTimeframeRegistry v1.2.5

Built-in D1→M60→M20→M5→M1 hierarchy with alias support.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Multi-timeframe Replay Only. No Auto Decision. No Auto Execution.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from replay.timeframe_schema import TimeframeDefinition, Timeframe

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# ---------------------------------------------------------------------------
# Alias map — normalizes user input to canonical Timeframe ID
# ---------------------------------------------------------------------------
_ALIAS_MAP: Dict[str, str] = {
    # D1 aliases
    "daily": "D1", "day": "D1", "1d": "D1", "d1": "D1",
    # M60 aliases
    "60m": "M60", "1h": "M60", "m60": "M60", "60min": "M60",
    # M20 aliases
    "20m": "M20", "m20": "M20", "20min": "M20",
    # M5 aliases
    "5m": "M5", "m5": "M5", "5min": "M5",
    # M1 aliases
    "1m": "M1", "m1": "M1", "1min": "M1",
}

# ---------------------------------------------------------------------------
# Built-in hierarchy definitions
# ---------------------------------------------------------------------------
_BUILTIN_DEFINITIONS = [
    TimeframeDefinition(
        timeframe_id="D1",
        label="Daily",
        minutes=390,            # 09:00–13:30 = 270 min for TW market; 390 is conventional
        parent_timeframe=None,
        child_timeframe="M60",
        enabled=True,
        formal_supported=True,
        partial_bar_supported=True,
        indicator_supported=True,
        strategy_supported=True,
        source_priority=1,
        research_only=True,
    ),
    TimeframeDefinition(
        timeframe_id="M60",
        label="60m",
        minutes=60,
        parent_timeframe="D1",
        child_timeframe="M20",
        enabled=True,
        formal_supported=True,
        partial_bar_supported=True,
        indicator_supported=True,
        strategy_supported=True,
        source_priority=2,
        research_only=True,
    ),
    TimeframeDefinition(
        timeframe_id="M20",
        label="20m",
        minutes=20,
        parent_timeframe="M60",
        child_timeframe="M5",
        enabled=True,
        formal_supported=True,
        partial_bar_supported=True,
        indicator_supported=True,
        strategy_supported=True,
        source_priority=3,
        research_only=True,
    ),
    TimeframeDefinition(
        timeframe_id="M5",
        label="5m",
        minutes=5,
        parent_timeframe="M20",
        child_timeframe="M1",
        enabled=True,
        formal_supported=True,
        partial_bar_supported=True,
        indicator_supported=True,
        strategy_supported=True,
        source_priority=4,
        research_only=True,
    ),
    TimeframeDefinition(
        timeframe_id="M1",
        label="1m",
        minutes=1,
        parent_timeframe="M5",
        child_timeframe=None,
        enabled=True,
        formal_supported=True,
        partial_bar_supported=True,
        indicator_supported=True,
        strategy_supported=True,
        source_priority=5,
        research_only=True,
    ),
]

# Ordered from highest to lowest
_HIERARCHY_ORDER = ["D1", "M60", "M20", "M5", "M1"]


class ReplayTimeframeRegistry:
    """
    Registry of supported timeframes with D1→M60→M20→M5→M1 hierarchy.

    [!] Research Only. No Real Orders. Replay Training Only.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self) -> None:
        self._defs: Dict[str, TimeframeDefinition] = {}
        for td in _BUILTIN_DEFINITIONS:
            self._defs[td.timeframe_id] = td

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def list_timeframes(self) -> List[str]:
        """Return timeframes in hierarchy order (highest to lowest)."""
        return [tid for tid in _HIERARCHY_ORDER if tid in self._defs]

    def get(self, timeframe_id: str) -> Optional[TimeframeDefinition]:
        """Get definition by ID or alias. Returns None if not found."""
        tid = self.normalize(timeframe_id)
        return self._defs.get(tid)

    def parent(self, timeframe_id: str) -> Optional[str]:
        """Return parent timeframe ID, or None if at top."""
        td = self.get(timeframe_id)
        return td.parent_timeframe if td else None

    def child(self, timeframe_id: str) -> Optional[str]:
        """Return child timeframe ID, or None if at bottom."""
        td = self.get(timeframe_id)
        return td.child_timeframe if td else None

    def higher_timeframes(self, timeframe_id: str) -> List[str]:
        """Return all timeframes strictly higher than given (closest first)."""
        tid = self.normalize(timeframe_id)
        if tid not in _HIERARCHY_ORDER:
            return []
        idx = _HIERARCHY_ORDER.index(tid)
        return [t for t in _HIERARCHY_ORDER[:idx] if t in self._defs]

    def lower_timeframes(self, timeframe_id: str) -> List[str]:
        """Return all timeframes strictly lower than given (closest first)."""
        tid = self.normalize(timeframe_id)
        if tid not in _HIERARCHY_ORDER:
            return []
        idx = _HIERARCHY_ORDER.index(tid)
        return [t for t in _HIERARCHY_ORDER[idx + 1:] if t in self._defs]

    def validate(self, timeframe_id: str) -> bool:
        """Return True if timeframe_id (or alias) is registered."""
        return self.normalize(timeframe_id) in self._defs

    def normalize(self, timeframe_id: str) -> str:
        """Normalize alias to canonical ID. Returns original if not an alias."""
        if not timeframe_id:
            return ""
        lower = timeframe_id.strip().lower()
        # Check alias map
        canonical = _ALIAS_MAP.get(lower)
        if canonical:
            return canonical
        # Return upper-cased if it looks like a canonical ID
        upper = timeframe_id.strip().upper()
        if upper in self._defs:
            return upper
        # Return as-is (validation will fail)
        return timeframe_id.strip()

    def supports_partial(self, timeframe_id: str) -> bool:
        """Return True if this timeframe supports partial bar display."""
        td = self.get(timeframe_id)
        return td.partial_bar_supported if td else False

    def source_priority(self, timeframe_id: str) -> int:
        """Return source priority for this timeframe (lower = higher priority)."""
        td = self.get(timeframe_id)
        return td.source_priority if td else 99

    def is_higher_than(self, tf_a: str, tf_b: str) -> bool:
        """Return True if tf_a is higher (longer period) than tf_b."""
        a = self.normalize(tf_a)
        b = self.normalize(tf_b)
        if a not in _HIERARCHY_ORDER or b not in _HIERARCHY_ORDER:
            return False
        return _HIERARCHY_ORDER.index(a) < _HIERARCHY_ORDER.index(b)

    def summary(self) -> Dict[str, object]:
        return {
            "timeframes": self.list_timeframes(),
            "count": len(self._defs),
            "hierarchy": "D1→M60→M20→M5→M1",
            "research_only": self.RESEARCH_ONLY,
            "no_real_orders": self.NO_REAL_ORDERS,
        }
