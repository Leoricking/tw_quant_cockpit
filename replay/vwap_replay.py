"""replay/vwap_replay.py — VWAP Replay overlay (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice."""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

ABOVE_VWAP = "ABOVE_VWAP"
BELOW_VWAP = "BELOW_VWAP"
AT_VWAP = "AT_VWAP"
UNKNOWN = "UNKNOWN"


class VWAPReplay:
    """Cumulative VWAP overlay computed from visible bars only.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
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

    def _compute_vwap_series(self, visible_df) -> Optional[list]:
        """Return list of cumulative VWAP values, one per bar."""
        close_col = self._find_col(visible_df, ("close", "c", "price"))
        volume_col = self._find_col(visible_df, ("volume", "vol", "v"))

        if close_col is None:
            return None

        try:
            closes = visible_df[close_col].astype(float).tolist()
            if volume_col:
                volumes = visible_df[volume_col].astype(float).tolist()
            else:
                # fallback: equal weights
                volumes = [1.0] * len(closes)

            cumvol = 0.0
            cumtpvol = 0.0
            vwaps = []
            for c, v in zip(closes, volumes):
                v = max(v, 1e-9)
                cumvol += v
                cumtpvol += c * v
                vwaps.append(cumtpvol / cumvol)
            return vwaps
        except Exception as exc:
            logger.warning("[VWAPReplay] vwap series error: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def build_overlay(self, visible_df) -> dict:
        """Compute cumulative VWAP overlay. No crash if df empty/None."""
        empty = {
            "current_vwap": None,
            "price_vs_vwap_pct": None,
            "above_vwap": False,
            "above_vwap_ratio_so_far": 0.0,
            "vwap_reclaim": False,
            "vwap_lost": False,
            "vwap_state": UNKNOWN,
            "research_only": True,
            "no_real_orders": True,
        }

        if visible_df is None:
            return empty
        try:
            if len(visible_df) == 0:
                return empty
        except Exception:
            return empty

        vwaps = self._compute_vwap_series(visible_df)
        if vwaps is None or len(vwaps) == 0:
            return empty

        close_col = self._find_col(visible_df, ("close", "c", "price"))
        if close_col is None:
            return empty

        try:
            closes = visible_df[close_col].astype(float).tolist()
            current_vwap = vwaps[-1]
            current_close = closes[-1]

            above_vwap = current_close >= current_vwap
            at_threshold = abs(current_close - current_vwap) / max(current_vwap, 1e-9) < 0.001
            vwap_state = AT_VWAP if at_threshold else (ABOVE_VWAP if above_vwap else BELOW_VWAP)

            price_vs_vwap_pct = (current_close - current_vwap) / max(current_vwap, 1e-9) * 100.0

            above_count = sum(1 for c, v in zip(closes, vwaps) if c >= v)
            above_ratio = above_count / len(closes)

            return {
                "current_vwap": round(current_vwap, 4),
                "price_vs_vwap_pct": round(price_vs_vwap_pct, 4),
                "above_vwap": above_vwap,
                "above_vwap_ratio_so_far": round(above_ratio, 4),
                "vwap_reclaim": self.detect_reclaim(visible_df),
                "vwap_lost": self.detect_lost(visible_df),
                "vwap_state": vwap_state,
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as exc:
            logger.error("[VWAPReplay] build_overlay error: %s", exc)
            return empty

    def current_vwap_state(self, visible_df) -> str:
        """Return ABOVE_VWAP / BELOW_VWAP / AT_VWAP / UNKNOWN."""
        if visible_df is None:
            return UNKNOWN
        try:
            if len(visible_df) == 0:
                return UNKNOWN
        except Exception:
            return UNKNOWN

        vwaps = self._compute_vwap_series(visible_df)
        if vwaps is None or len(vwaps) == 0:
            return UNKNOWN

        close_col = self._find_col(visible_df, ("close", "c", "price"))
        if close_col is None:
            return UNKNOWN

        try:
            current_close = float(visible_df.iloc[-1][close_col])
            current_vwap = vwaps[-1]
            at_threshold = abs(current_close - current_vwap) / max(current_vwap, 1e-9) < 0.001
            if at_threshold:
                return AT_VWAP
            return ABOVE_VWAP if current_close >= current_vwap else BELOW_VWAP
        except Exception:
            return UNKNOWN

    def detect_reclaim(self, visible_df) -> bool:
        """True if last 3 bars crossed from below to above VWAP."""
        if visible_df is None or len(visible_df) < 3:
            return False
        vwaps = self._compute_vwap_series(visible_df)
        if vwaps is None or len(vwaps) < 3:
            return False
        close_col = self._find_col(visible_df, ("close", "c", "price"))
        if close_col is None:
            return False
        try:
            closes = visible_df[close_col].astype(float).tolist()
            # last bar above, 2 prior bars below
            return (
                closes[-1] >= vwaps[-1]
                and closes[-2] < vwaps[-2]
                and closes[-3] < vwaps[-3]
            )
        except Exception:
            return False

    def detect_lost(self, visible_df) -> bool:
        """True if last 3 bars crossed from above to below VWAP."""
        if visible_df is None or len(visible_df) < 3:
            return False
        vwaps = self._compute_vwap_series(visible_df)
        if vwaps is None or len(vwaps) < 3:
            return False
        close_col = self._find_col(visible_df, ("close", "c", "price"))
        if close_col is None:
            return False
        try:
            closes = visible_df[close_col].astype(float).tolist()
            return (
                closes[-1] < vwaps[-1]
                and closes[-2] >= vwaps[-2]
                and closes[-3] >= vwaps[-3]
            )
        except Exception:
            return False
