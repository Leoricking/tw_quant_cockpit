"""replay/fake_breakout_replay.py — Fake Breakout detection overlay (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice."""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

LOW = "LOW"
MEDIUM = "MEDIUM"
HIGH = "HIGH"
CRITICAL = "CRITICAL"
UNKNOWN = "UNKNOWN"


class FakeBreakoutReplay:
    """Detects fake breakout patterns from visible bars only.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    Uses only already-visible bars — no future data.
    """

    read_only = True
    no_real_orders = True

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _find_col(df, candidates: tuple) -> Optional[str]:
        if df is None:
            return None
        cols = [c.lower() for c in df.columns]
        for cand in candidates:
            if cand in cols:
                for orig in df.columns:
                    if orig.lower() == cand:
                        return orig
        return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def detect_so_far(self, visible_df) -> dict:
        """Analyse visible bars for breakout attempts and reversals."""
        empty = {
            "breakout_attempt": False,
            "breakout_confirmed": False,
            "breakout_failed_so_far": False,
            "fake_breakout_risk_so_far": UNKNOWN,
            "chase_risk_score_so_far": 0.0,
            "warning_message": "",
            "research_only": True,
            "no_real_orders": True,
        }

        if visible_df is None:
            return empty
        try:
            n = len(visible_df)
        except Exception:
            return empty

        if n < 3:
            return empty

        close_col = self._find_col(visible_df, ("close", "c", "price"))
        high_col = self._find_col(visible_df, ("high", "h"))

        if close_col is None or high_col is None:
            return empty

        try:
            closes = visible_df[close_col].astype(float).tolist()
            highs = visible_df[high_col].astype(float).tolist()

            lookback = min(10, n - 2)
            recent_high = max(highs[-(lookback + 2) : -1]) if lookback > 0 else highs[0]

            current_close = closes[-1]
            prev_close = closes[-2] if n >= 2 else closes[-1]
            prev_prev_close = closes[-3] if n >= 3 else closes[-2]

            # A breakout attempt: prev close broke above recent high
            breakout_attempt = prev_close > recent_high

            # Confirmed: last 2 bars both held above
            breakout_confirmed = breakout_attempt and current_close > recent_high

            # Failed: prev bar broke above but current closed back below
            breakout_failed = breakout_attempt and current_close <= recent_high

            # Chase risk score
            chase_risk_score = 0.0
            if breakout_failed:
                chase_risk_score = 80.0
            elif breakout_attempt and not breakout_confirmed:
                chase_risk_score = 50.0
            elif breakout_attempt and breakout_confirmed:
                # still some chase risk — price may be extended
                extension_pct = (current_close - recent_high) / max(recent_high, 1e-9) * 100
                chase_risk_score = min(60.0, 20.0 + extension_pct * 5)

            risk_level = self.classify_current_risk(visible_df)

            warning = ""
            if breakout_failed:
                warning = (
                    f"[TRAINING] Fake breakout detected. Price broke above {recent_high:.2f} "
                    f"but closed back at {current_close:.2f}. Chasing would have been a mistake."
                )
            elif breakout_attempt and not breakout_confirmed:
                warning = (
                    f"[TRAINING] Breakout attempt above {recent_high:.2f}. Not yet confirmed. "
                    f"Wait for follow-through before acting."
                )

            return {
                "breakout_attempt": breakout_attempt,
                "breakout_confirmed": breakout_confirmed,
                "breakout_failed_so_far": breakout_failed,
                "fake_breakout_risk_so_far": risk_level,
                "chase_risk_score_so_far": round(chase_risk_score, 2),
                "warning_message": warning,
                "recent_high_level": round(recent_high, 4),
                "current_close": round(current_close, 4),
                "research_only": True,
                "no_real_orders": True,
            }

        except Exception as exc:
            logger.error("[FakeBreakoutReplay] detect_so_far error: %s", exc)
            return empty

    def classify_current_risk(self, visible_df) -> str:
        """Classify fake-breakout risk as LOW/MEDIUM/HIGH/CRITICAL/UNKNOWN."""
        if visible_df is None:
            return UNKNOWN
        try:
            n = len(visible_df)
        except Exception:
            return UNKNOWN

        if n < 3:
            return UNKNOWN

        close_col = self._find_col(visible_df, ("close", "c", "price"))
        high_col = self._find_col(visible_df, ("high", "h"))
        volume_col = self._find_col(visible_df, ("volume", "vol", "v"))

        if close_col is None or high_col is None:
            return UNKNOWN

        try:
            closes = visible_df[close_col].astype(float).tolist()
            highs = visible_df[high_col].astype(float).tolist()

            lookback = min(10, n - 2)
            recent_high = max(highs[-(lookback + 2) : -1]) if lookback > 0 else highs[0]
            current_close = closes[-1]
            prev_close = closes[-2]

            broke_out = prev_close > recent_high
            reversed_back = broke_out and current_close <= recent_high

            if reversed_back:
                # check volume: low volume break → CRITICAL risk
                if volume_col:
                    volumes = visible_df[volume_col].astype(float).tolist()
                    avg_vol = sum(volumes[:-2]) / max(len(volumes[:-2]), 1)
                    break_vol = volumes[-2]
                    if break_vol < avg_vol * 0.7:
                        return CRITICAL
                return HIGH
            elif broke_out and not reversed_back:
                return MEDIUM
            elif current_close > recent_high * 0.995:
                return MEDIUM
            else:
                return LOW

        except Exception:
            return UNKNOWN

    def build_warning(self, visible_df) -> dict:
        """Build warning dict with risk level and description."""
        detection = self.detect_so_far(visible_df)
        risk_level = detection.get("fake_breakout_risk_so_far", UNKNOWN)
        warning_message = detection.get("warning_message", "")

        severity_map = {
            LOW: "No significant fake breakout risk detected so far.",
            MEDIUM: "Moderate fake breakout risk — breakout attempt in progress, not yet confirmed.",
            HIGH: "High fake breakout risk — recent break has reversed. Chasing would be dangerous.",
            CRITICAL: "CRITICAL: Low-volume breakout reversed. Classic fake breakout pattern. DO NOT chase.",
            UNKNOWN: "Insufficient data to assess breakout risk.",
        }

        description = warning_message or severity_map.get(risk_level, "")

        return {
            "risk_level": risk_level,
            "description": description,
            "breakout_attempt": detection.get("breakout_attempt", False),
            "breakout_confirmed": detection.get("breakout_confirmed", False),
            "breakout_failed": detection.get("breakout_failed_so_far", False),
            "chase_risk_score": detection.get("chase_risk_score_so_far", 0.0),
            "training_note": "Research Only / Replay Training Only / No Real Orders",
            "research_only": True,
            "no_real_orders": True,
        }
