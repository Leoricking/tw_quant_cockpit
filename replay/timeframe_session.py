"""
replay/timeframe_session.py — MultiTimeframeReplaySession v1.2.5

Multi-timeframe replay session management. If M1 missing: trigger fallback to M5
(shown explicitly, no fake M1 generated).

Session defaults: primary_timeframe=M5, context_timeframes=[D1,M60,M20],
trigger_timeframe=M1 (fallback M5 if M1 missing),
allow_partial_bar_view=True, indicators_use_completed_bars_only=True,
timezone=Asia/Taipei.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
[!] M1 missing → trigger fallback M5 (explicit, no fake M1).
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

SESSION_ID_PREFIX = "MTF-"

# Default session configuration
DEFAULT_CONFIG = {
    "enabled_timeframes": ["D1", "M60", "M20", "M5", "M1"],
    "required_timeframes": ["D1", "M5"],
    "optional_timeframes": ["M60", "M20", "M1"],
    "primary_timeframe": "M5",
    "context_timeframes": ["D1", "M60", "M20"],
    "trigger_timeframe": "M1",
    "fallback_trigger_timeframe": "M5",
    "allow_partial_bar_view": True,
    "indicators_use_completed_bars_only": True,
    "timezone": "Asia/Taipei",
}


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_session_id() -> str:
    return f"{SESSION_ID_PREFIX}{uuid.uuid4().hex[:12].upper()}"


class MultiTimeframeReplaySession:
    """
    Multi-timeframe replay session.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] M1 missing → trigger fallback to M5 (explicit, no fake M1).
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(
        self,
        session_id: Optional[str] = None,
        symbol: str = "TST",
        config: Optional[Dict[str, Any]] = None,
        bars_by_tf: Optional[Dict[str, List[Dict[str, Any]]]] = None,
    ) -> None:
        self._session_id = session_id or _new_session_id()
        self._symbol     = symbol
        self._config     = {**DEFAULT_CONFIG, **(config or {})}
        self._bars_by_tf = bars_by_tf or {}
        self._current_timestamp: Optional[str] = None
        self._checkpoints: List[Dict[str, Any]] = []
        self._status     = "ACTIVE"

        # Resolve trigger timeframe (fallback if M1 missing)
        self._resolve_trigger_timeframe()

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def enable_timeframes(self, timeframes: List[str]) -> None:
        """Enable additional timeframes."""
        enabled = set(self._config["enabled_timeframes"])
        enabled.update(timeframes)
        self._config["enabled_timeframes"] = list(enabled)
        self._resolve_trigger_timeframe()

    def disable_timeframe(self, timeframe: str) -> None:
        """Disable a timeframe."""
        self._config["enabled_timeframes"] = [
            tf for tf in self._config["enabled_timeframes"] if tf != timeframe
        ]
        self._resolve_trigger_timeframe()

    def required_timeframes(self) -> List[str]:
        return self._config.get("required_timeframes", [])

    def optional_timeframes(self) -> List[str]:
        return self._config.get("optional_timeframes", [])

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def current_snapshot(self) -> Dict[str, Any]:
        """Return current multi-timeframe snapshot."""
        if not self._current_timestamp:
            return {"status": "NO_TIMESTAMP", "session_id": self._session_id}

        try:
            from replay.timeframe_context_builder import MultiTimeframeContextBuilder
            builder = MultiTimeframeContextBuilder()
            context = builder.build(
                self._session_id,
                self._current_timestamp,
                self._symbol,
                self._bars_by_tf,
                self._config,
            )
            return context
        except Exception as e:
            return {
                "session_id": self._session_id,
                "timestamp": self._current_timestamp,
                "status": "ERROR",
                "error": str(e),
            }

    def move_next(self, timeframe: Optional[str] = None) -> Dict[str, Any]:
        """Advance to next bar boundary."""
        from replay.timeframe_clock import ReplayTimeframeClock
        clock = self._get_clock()
        result = clock.next_bar(timeframe or self._config.get("trigger_timeframe", "M5"))
        self._current_timestamp = result.get("timestamp", self._current_timestamp)
        return {"timestamp": self._current_timestamp, "status": result.get("status")}

    def move_previous(self, timeframe: Optional[str] = None) -> Dict[str, Any]:
        """Move to previous bar boundary."""
        from replay.timeframe_clock import ReplayTimeframeClock
        clock = self._get_clock()
        result = clock.previous_bar(timeframe or self._config.get("trigger_timeframe", "M5"))
        self._current_timestamp = result.get("timestamp", self._current_timestamp)
        return {"timestamp": self._current_timestamp, "status": result.get("status")}

    def jump(self, timestamp: str) -> Dict[str, Any]:
        """Jump to specific timestamp."""
        clock = self._get_clock()
        result = clock.jump(timestamp)
        self._current_timestamp = result.get("timestamp", timestamp)
        return {"timestamp": self._current_timestamp, "status": result.get("status")}

    # ------------------------------------------------------------------
    # Checkpoints
    # ------------------------------------------------------------------

    def create_checkpoint(self, label: str = "") -> Dict[str, Any]:
        """Create checkpoint at current state."""
        checkpoint = {
            "checkpoint_id": f"CKP-{uuid.uuid4().hex[:12].upper()}",
            "session_id": self._session_id,
            "replay_timestamp": self._current_timestamp,
            "enabled_timeframes": self._config.get("enabled_timeframes", []),
            "primary_timeframe": self._config.get("primary_timeframe"),
            "trigger_timeframe": self._config.get("trigger_timeframe"),
            "label": label,
            "created_at": _now_utc(),
            "research_only": True,
            "no_post_checkpoint_data": True,
        }
        self._checkpoints.append(checkpoint)
        return checkpoint

    def resume(self, checkpoint_id: str) -> Dict[str, Any]:
        """Resume from checkpoint."""
        for cp in self._checkpoints:
            if cp["checkpoint_id"] == checkpoint_id:
                self._current_timestamp = cp.get("replay_timestamp")
                return {"status": "RESUMED", "checkpoint": cp}
        return {"status": "NOT_FOUND", "checkpoint_id": checkpoint_id}

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        trigger_tf = self._config.get("trigger_timeframe", "M5")
        m1_available = "M1" in self._bars_by_tf and bool(self._bars_by_tf.get("M1"))
        trigger_fallback = not m1_available and trigger_tf == "M5"

        return {
            "session_id": self._session_id,
            "symbol": self._symbol,
            "status": self._status,
            "current_timestamp": self._current_timestamp,
            "enabled_timeframes": self._config.get("enabled_timeframes", []),
            "required_timeframes": self._config.get("required_timeframes", []),
            "optional_timeframes": self._config.get("optional_timeframes", []),
            "primary_timeframe": self._config.get("primary_timeframe"),
            "trigger_timeframe": trigger_tf,
            "trigger_fallback_to_m5": trigger_fallback,
            "m1_available": m1_available,
            "allow_partial_bar_view": self._config.get("allow_partial_bar_view", True),
            "indicators_use_completed_bars_only": self._config.get("indicators_use_completed_bars_only", True),
            "timezone": self._config.get("timezone", "Asia/Taipei"),
            "checkpoint_count": len(self._checkpoints),
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def current_timestamp(self) -> Optional[str]:
        return self._current_timestamp

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _resolve_trigger_timeframe(self) -> None:
        """Resolve trigger timeframe — fallback to M5 if M1 missing."""
        m1_available = "M1" in self._bars_by_tf and bool(self._bars_by_tf.get("M1"))
        if not m1_available:
            # Show explicitly that trigger is M5 fallback
            self._config["trigger_timeframe"] = "M5"
            logger.info(
                "[MTFSession] M1 data not available — trigger_timeframe set to M5 (explicit fallback, no fake M1)"
            )
        else:
            self._config["trigger_timeframe"] = "M1"

    def _get_clock(self):
        """Get or create replay clock."""
        from replay.timeframe_clock import ReplayTimeframeClock
        # Determine session bounds from bar data
        all_timestamps = []
        for bars in self._bars_by_tf.values():
            all_timestamps.extend(b.get("timestamp", "") for b in bars)
        if all_timestamps:
            session_start = min(all_timestamps)
            session_end   = max(all_timestamps)
        else:
            session_start = "2023-01-06T09:00:00"
            session_end   = "2023-01-06T13:30:00"

        clock = ReplayTimeframeClock(
            session_start=session_start,
            session_end=session_end,
            initial_timestamp=self._current_timestamp or session_start,
        )
        return clock
