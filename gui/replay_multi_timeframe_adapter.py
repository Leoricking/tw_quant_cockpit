"""
gui/replay_multi_timeframe_adapter.py — MultiTimeframeReplayAdapter v1.2.5

Bridges MultiTimeframeReplaySession with GUI. Thread-safe signal emission.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class MultiTimeframeReplayAdapter:
    """
    Adapter bridging MultiTimeframeReplaySession to GUI components.
    Thread-safe signal emission via worker thread pattern.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self) -> None:
        self._session = None
        self._current_context: Optional[Dict[str, Any]] = None

    def set_session(self, session) -> None:
        """Set the multi-timeframe replay session."""
        self._session = session

    def get_current_snapshot(self) -> Optional[Dict[str, Any]]:
        """Get current multi-timeframe snapshot from session."""
        if not self._session:
            return None
        try:
            return self._session.current_snapshot()
        except Exception as e:
            logger.warning("[MTFAdapter] get_current_snapshot error: %s", e)
            return None

    def move_next(self, timeframe: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Advance to next bar. Thread-safe."""
        if not self._session:
            return None
        return self._session.move_next(timeframe)

    def move_previous(self, timeframe: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Move to previous bar. Thread-safe."""
        if not self._session:
            return None
        return self._session.move_previous(timeframe)

    def jump(self, timestamp: str) -> Optional[Dict[str, Any]]:
        """Jump to timestamp. Thread-safe."""
        if not self._session:
            return None
        return self._session.jump(timestamp)

    def get_session_summary(self) -> Dict[str, Any]:
        """Return session summary for GUI display."""
        if not self._session:
            return {"status": "NO_SESSION", "research_only": True}
        return self._session.summary()

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "adapter": "MultiTimeframeReplayAdapter",
            "version": "v1.2.5",
            "thread_safe": True,
            "research_only": True,
            "no_real_orders": True,
        }
