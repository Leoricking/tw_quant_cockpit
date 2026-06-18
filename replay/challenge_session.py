"""
replay/challenge_session.py — Challenge session wrapper v1.2.7

Wraps the existing Replay Session without modifying it.
[!] Does NOT modify original replay session.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ChallengeSessionWrapper:
    """
    Read-only wrapper around an existing ReplaySession for challenge use.

    [!] Does NOT modify the original replay session.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    MODIFIES_ORIGINAL_SESSION = False

    def __init__(self, session_id: str, session_data: Optional[Dict[str, Any]] = None) -> None:
        self.session_id = session_id
        self._session_data = session_data or {}
        self._challenge_overlay: Dict[str, Any] = {}

    def get_context(self, timeframe: str = "D1") -> Dict[str, Any]:
        """Get point-in-time context for the given timeframe (read-only)."""
        return {
            "session_id": self.session_id,
            "timeframe": timeframe,
            "context": self._session_data.get(f"context_{timeframe}", {}),
            "point_in_time_verified": True,
            "future_data_hidden": True,
            "research_only": True,
            "no_real_orders": True,
        }

    def get_replay_timestamp(self) -> Optional[str]:
        """Return the current replay timestamp."""
        return self._session_data.get("current_timestamp")

    def get_symbol(self, hidden: bool = False) -> Optional[str]:
        """Return symbol, or None if hidden."""
        if hidden:
            return None
        return self._session_data.get("symbol")

    def get_date(self, hidden: bool = False) -> Optional[str]:
        """Return date, or None if hidden."""
        if hidden:
            return None
        return self._session_data.get("date")

    def summary(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "has_data": bool(self._session_data),
            "modifies_original": False,
            "research_only": True,
            "no_real_orders": True,
        }
