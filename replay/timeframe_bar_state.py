"""
replay/timeframe_bar_state.py — ReplayBarStateEvaluator v1.2.5

Evaluates whether a bar is complete or partial at a given replay timestamp.

Partial bar rules:
- Indicators default use completed bars only.
- GUI may show partial current bar — clearly marked.
- Partial close never treated as confirmed.
- Partial high/low never used for confirmed breakout.
- Strategy using partial bar → qualification=PARTIAL_OBSERVATION, not CONFIRMED.

[!] Research Only. No Real Orders. Replay Training Only. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

QUALIFICATION_CONFIRMED           = "CONFIRMED"
QUALIFICATION_PARTIAL_OBSERVATION = "PARTIAL_OBSERVATION"
QUALIFICATION_UNAVAILABLE         = "UNAVAILABLE"
QUALIFICATION_UNVERIFIED          = "UNVERIFIED"


class ReplayBarStateEvaluator:
    """
    Evaluates bar completeness for replay point-in-time integrity.

    Rules:
    - is_complete: bar close time <= replay_timestamp (strict).
    - is_partial: bar started but not yet closed at replay_timestamp.
    - Partial bar indicators: partial_observation field only.
    - Partial close: never treated as confirmed close.
    - Partial high/low: never used for confirmed breakout.
    - Strategy on partial bar → qualification=PARTIAL_OBSERVATION.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def evaluate(
        self,
        bar: Dict[str, Any],
        replay_timestamp: str,
        timeframe: str,
    ) -> Dict[str, Any]:
        """
        Evaluate bar state at replay_timestamp.
        Returns dict with: is_complete, is_partial, qualification, warnings.
        """
        warnings = []
        if not bar:
            return {
                "is_complete": False,
                "is_partial": False,
                "qualification": QUALIFICATION_UNAVAILABLE,
                "completed_portion": 0.0,
                "warnings": ["No bar data"],
            }

        bar_ts = bar.get("timestamp", "")
        bar_is_complete = bool(bar.get("is_complete", False))
        bar_is_partial  = bool(bar.get("is_partial", False))

        # Check against replay_timestamp
        complete = self.is_complete(bar, replay_timestamp, timeframe)
        partial  = self.is_partial(bar, replay_timestamp, timeframe)
        portion  = self.completed_portion(bar, replay_timestamp, timeframe)

        # Determine qualification
        if complete:
            qualification = QUALIFICATION_CONFIRMED
        elif partial:
            qualification = QUALIFICATION_PARTIAL_OBSERVATION
            warnings.append(f"Partial bar at {bar_ts} — not confirmed for breakout/strategy signals")
        else:
            qualification = QUALIFICATION_UNAVAILABLE

        # Safety checks
        if bar_is_complete and not complete:
            warnings.append(
                f"Bar marked is_complete=True but close time > replay_timestamp — treating as PARTIAL"
            )
            qualification = QUALIFICATION_PARTIAL_OBSERVATION
            complete = False
            partial = True

        return {
            "is_complete": complete,
            "is_partial": partial,
            "qualification": qualification,
            "completed_portion": portion,
            "warnings": warnings,
            "bar_timestamp": bar_ts,
            "timeframe": timeframe,
            "research_only": True,
        }

    def is_complete(
        self, bar: Dict[str, Any], replay_timestamp: str, timeframe: str
    ) -> bool:
        """Return True if bar is fully closed as of replay_timestamp."""
        try:
            from replay.timeframe_calendar import TaiwanReplayTradingCalendar
            cal = TaiwanReplayTradingCalendar()
            bar_ts = bar.get("timestamp", "")
            return cal.is_bar_complete(bar_ts, replay_timestamp, timeframe)
        except Exception:
            # Fallback: compare timestamps directly
            bar_ts = bar.get("timestamp", "")
            return bar_ts < replay_timestamp

    def is_partial(
        self, bar: Dict[str, Any], replay_timestamp: str, timeframe: str
    ) -> bool:
        """Return True if bar has started but not yet completed at replay_timestamp."""
        try:
            bar_ts = bar.get("timestamp", "")
            if not bar_ts:
                return False
            # Bar started: bar_ts <= replay_timestamp
            # Bar not complete: not is_complete
            started = bar_ts <= replay_timestamp
            complete = self.is_complete(bar, replay_timestamp, timeframe)
            return started and not complete
        except Exception:
            return False

    def completed_portion(
        self, bar: Dict[str, Any], replay_timestamp: str, timeframe: str
    ) -> float:
        """Return fraction of bar elapsed (0.0–1.0)."""
        try:
            from datetime import datetime, timedelta
            bar_ts = bar.get("timestamp", "")
            if not bar_ts:
                return 0.0
            tf_map = {"D1": 270, "M60": 60, "M20": 20, "M5": 5, "M1": 1}
            tf_upper = timeframe.upper()
            minutes = tf_map.get(tf_upper, 1)
            # Parse
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M"):
                try:
                    bar_dt    = datetime.strptime(bar_ts[:19], fmt[:19])
                    replay_dt = datetime.strptime(replay_timestamp[:19], fmt[:19])
                    elapsed   = (replay_dt - bar_dt).total_seconds()
                    total     = minutes * 60.0
                    return max(0.0, min(1.0, elapsed / total))
                except ValueError:
                    continue
        except Exception:
            pass
        return 0.0

    def visible_ohlcv(
        self, bar: Dict[str, Any], replay_timestamp: str, timeframe: str
    ) -> Dict[str, Any]:
        """
        Return OHLCV visible at replay_timestamp.
        For partial bars: high/low/close are as-of, not confirmed.
        """
        state = self.evaluate(bar, replay_timestamp, timeframe)
        result = {
            "open":     bar.get("open"),
            "high":     bar.get("high"),
            "low":      bar.get("low"),
            "close":    bar.get("close"),
            "volume":   bar.get("volume"),
            "amount":   bar.get("amount"),
            "is_complete":   state["is_complete"],
            "is_partial":    state["is_partial"],
            "qualification": state["qualification"],
            "warnings":      state["warnings"],
        }
        if state["is_partial"]:
            result["partial_observation"] = True
            result["confirmed_close"]     = False
            result["confirmed_breakout"]  = False
        return result

    def safe_partial_bar(self, bar: Dict[str, Any]) -> Dict[str, Any]:
        """Return safe partial bar dict with warnings attached."""
        return {
            **bar,
            "is_partial": True,
            "is_complete": False,
            "qualification": QUALIFICATION_PARTIAL_OBSERVATION,
            "confirmed_close": False,
            "confirmed_breakout": False,
            "warning": "Partial bar — high/low/close not confirmed",
        }

    def warning(self, bar: Dict[str, Any], replay_timestamp: str, timeframe: str) -> List[str]:
        """Return list of warnings for bar at replay_timestamp."""
        state = self.evaluate(bar, replay_timestamp, timeframe)
        return state.get("warnings", [])
