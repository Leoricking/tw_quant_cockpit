"""
gui/replay_timeframe_snapshot_dialog.py — ReplayTimeframeSnapshotDialog v1.2.5
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, Optional
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayTimeframeSnapshotDialog:
    """Shows detailed single-timeframe snapshot. [!] Research Only."""
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, parent=None) -> None:
        self._parent = parent
        self._snapshot: Optional[Dict[str, Any]] = None

    def set_snapshot(self, snapshot: Dict[str, Any]) -> None:
        self._snapshot = snapshot

    def get_display_data(self) -> Dict[str, Any]:
        if not self._snapshot:
            return {"status": "NO_SNAPSHOT", "research_only": True}
        return {
            "timeframe": self._snapshot.get("timeframe"),
            "replay_timestamp": self._snapshot.get("replay_timestamp"),
            "trend_state": self._snapshot.get("trend_state"),
            "volume_state": self._snapshot.get("volume_state"),
            "indicators": self._snapshot.get("indicators", {}),
            "pit_verified": self._snapshot.get("point_in_time_verified"),
            "warnings": self._snapshot.get("warnings", []),
            "research_only": True,
        }
