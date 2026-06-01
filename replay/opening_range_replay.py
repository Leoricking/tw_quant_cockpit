"""replay/opening_range_replay.py — Opening Range Replay overlay (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice."""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# State constants
BUILDING_RANGE = "BUILDING_RANGE"
INSIDE_RANGE = "INSIDE_RANGE"
BREAK_HIGH = "BREAK_HIGH"
BREAK_LOW = "BREAK_LOW"
FAILED_BREAK_HIGH = "FAILED_BREAK_HIGH"
FAILED_BREAK_LOW = "FAILED_BREAK_LOW"
UNKNOWN = "UNKNOWN"


class OpeningRangeReplay:
    """Computes and tracks opening range overlay from visible bars only.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    Never uses future bars.
    """

    read_only = True
    no_real_orders = True

    def __init__(self, opening_minutes: int = 15):
        self._opening_minutes = opening_minutes

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

    def _safe_float(self, val, default=0.0) -> float:
        try:
            return float(val)
        except Exception:
            return default

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def build_overlay(self, visible_df) -> dict:
        """Compute opening range overlay from visible_df.

        Returns dict with opening range stats. No crash if df is empty/None.
        """
        empty = {
            "opening_high": None,
            "opening_low": None,
            "opening_range_pct": None,
            "current_position_in_range": None,
            "range_break_status": UNKNOWN,
            "opening_strength_so_far": 0.0,
            "bars_in_range": 0,
            "opening_bars_count": 0,
            "research_only": True,
            "no_real_orders": True,
        }

        if visible_df is None:
            return empty
        try:
            n_total = len(visible_df)
        except Exception:
            return empty

        if n_total == 0:
            return empty

        high_col = self._find_col(visible_df, ("high", "h"))
        low_col = self._find_col(visible_df, ("low", "l"))
        close_col = self._find_col(visible_df, ("close", "c", "price"))

        if high_col is None or low_col is None:
            return empty

        n_opening = min(self._opening_minutes, n_total)
        opening_df = visible_df.iloc[:n_opening]

        try:
            or_high = self._safe_float(opening_df[high_col].max())
            or_low = self._safe_float(opening_df[low_col].min())
        except Exception as exc:
            logger.warning("[OpeningRangeReplay] build_overlay error: %s", exc)
            return empty

        or_range = or_high - or_low
        or_range_pct = (or_range / or_low * 100.0) if or_low > 0 else 0.0

        # current price
        current_close = None
        if close_col:
            try:
                current_close = self._safe_float(visible_df.iloc[-1][close_col])
            except Exception:
                pass

        # position within range (0 = at low, 1 = at high)
        position_in_range = None
        if current_close is not None and or_range > 0:
            position_in_range = max(0.0, min(1.0, (current_close - or_low) / or_range))

        # range break status
        break_status = self.calculate_current_range_state(visible_df)

        # how many bars price stayed inside range after opening
        bars_in_range = 0
        if close_col:
            try:
                post_opening = visible_df.iloc[n_opening:]
                for _, row in post_opening.iterrows():
                    c = self._safe_float(row[close_col])
                    if or_low <= c <= or_high:
                        bars_in_range += 1
            except Exception:
                pass

        # opening strength: range tightness as a score (tighter = higher score)
        opening_strength = 0.0
        if or_range_pct > 0:
            # smaller range pct = tighter = stronger opening setup (inverted scale)
            opening_strength = max(0.0, min(100.0, 100.0 - or_range_pct * 10))

        return {
            "opening_high": or_high,
            "opening_low": or_low,
            "opening_range_pct": round(or_range_pct, 4),
            "current_position_in_range": round(position_in_range, 4) if position_in_range is not None else None,
            "range_break_status": break_status,
            "opening_strength_so_far": round(opening_strength, 2),
            "bars_in_range": bars_in_range,
            "opening_bars_count": n_opening,
            "research_only": True,
            "no_real_orders": True,
        }

    def calculate_current_range_state(self, visible_df) -> str:
        """Classify current price position relative to opening range."""
        if visible_df is None:
            return UNKNOWN
        try:
            if len(visible_df) == 0:
                return UNKNOWN
        except Exception:
            return UNKNOWN

        n_total = len(visible_df)
        n_opening = min(self._opening_minutes, n_total)

        if n_total < n_opening:
            return BUILDING_RANGE

        high_col = self._find_col(visible_df, ("high", "h"))
        low_col = self._find_col(visible_df, ("low", "l"))
        close_col = self._find_col(visible_df, ("close", "c", "price"))

        if high_col is None or low_col is None:
            return UNKNOWN

        opening_df = visible_df.iloc[:n_opening]

        try:
            or_high = self._safe_float(opening_df[high_col].max())
            or_low = self._safe_float(opening_df[low_col].min())
        except Exception:
            return UNKNOWN

        if close_col is None or n_total <= n_opening:
            return INSIDE_RANGE

        try:
            current_close = self._safe_float(visible_df.iloc[-1][close_col])
            prev_close = self._safe_float(visible_df.iloc[-2][close_col]) if n_total >= 2 else current_close
        except Exception:
            return UNKNOWN

        if current_close > or_high:
            # check if prev bar was also above — if yes: BREAK_HIGH; if now below — FAILED_BREAK_HIGH
            if prev_close <= or_high:
                return BREAK_HIGH
            return BREAK_HIGH
        elif current_close < or_low:
            if prev_close >= or_low:
                return BREAK_LOW
            return BREAK_LOW
        elif or_low <= current_close <= or_high:
            # check if previously broke
            if prev_close > or_high:
                return FAILED_BREAK_HIGH
            elif prev_close < or_low:
                return FAILED_BREAK_LOW
            return INSIDE_RANGE

        return UNKNOWN
