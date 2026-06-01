"""replay/volume_profile_replay.py — Volume Profile Replay overlay (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice."""
from __future__ import annotations

import logging
from collections import defaultdict
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

AT_POC = "AT_POC"
ABOVE_POC = "ABOVE_POC"
BELOW_POC = "BELOW_POC"
IN_VALUE_AREA = "IN_VALUE_AREA"
OUTSIDE_VALUE_AREA = "OUTSIDE_VALUE_AREA"
UNKNOWN = "UNKNOWN"


class VolumeProfileReplay:
    """Builds volume profile from visible bars only.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    """

    read_only = True
    no_real_orders = True

    def __init__(self, price_bins: int = 20):
        self._price_bins = price_bins

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

    def _build_price_vol_map(self, visible_df) -> Optional[dict]:
        """Build {price_bin: volume} dict from visible_df."""
        close_col = self._find_col(visible_df, ("close", "c", "price"))
        volume_col = self._find_col(visible_df, ("volume", "vol", "v"))

        if close_col is None:
            return None

        try:
            closes = visible_df[close_col].astype(float).tolist()
            if volume_col:
                volumes = visible_df[volume_col].astype(float).tolist()
            else:
                volumes = [1.0] * len(closes)

            if len(closes) == 0:
                return None

            price_min = min(closes)
            price_max = max(closes)
            if price_max <= price_min:
                # all same price
                return {round(price_min, 2): sum(volumes)}

            bin_size = (price_max - price_min) / self._price_bins

            price_vol: dict = defaultdict(float)
            for c, v in zip(closes, volumes):
                bin_idx = int((c - price_min) / bin_size)
                bin_idx = max(0, min(self._price_bins - 1, bin_idx))
                bin_price = round(price_min + bin_idx * bin_size, 4)
                price_vol[bin_price] += v

            return dict(price_vol)
        except Exception as exc:
            logger.warning("[VolumeProfileReplay] build_price_vol_map error: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def build_profile_so_far(self, visible_df) -> dict:
        """Build volume distribution across price bins from visible_df."""
        empty = {
            "poc_price_so_far": None,
            "value_area_high_so_far": None,
            "value_area_low_so_far": None,
            "price_vs_poc_pct": None,
            "volume_cluster_strength": 0.0,
            "support_pressure_state": UNKNOWN,
            "price_bins": {},
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

        price_vol = self._build_price_vol_map(visible_df)
        if price_vol is None or len(price_vol) == 0:
            return empty

        poc = self.current_poc(visible_df)
        vah, val = self.value_area(visible_df)

        close_col = self._find_col(visible_df, ("close", "c", "price"))
        current_close = None
        if close_col:
            try:
                current_close = float(visible_df.iloc[-1][close_col])
            except Exception:
                pass

        price_vs_poc_pct = None
        if poc is not None and current_close is not None and poc > 0:
            price_vs_poc_pct = round((current_close - poc) / poc * 100.0, 4)

        # volume cluster strength: ratio of POC volume to total volume (0-100)
        total_vol = sum(price_vol.values())
        poc_vol = price_vol.get(poc, 0) if poc is not None else 0
        cluster_strength = (poc_vol / total_vol * 100.0) if total_vol > 0 else 0.0

        state = self.support_pressure_state(visible_df)

        return {
            "poc_price_so_far": poc,
            "value_area_high_so_far": vah,
            "value_area_low_so_far": val,
            "price_vs_poc_pct": price_vs_poc_pct,
            "volume_cluster_strength": round(cluster_strength, 2),
            "support_pressure_state": state,
            "price_bins": {str(k): round(v, 2) for k, v in sorted(price_vol.items())},
            "research_only": True,
            "no_real_orders": True,
        }

    def current_poc(self, visible_df) -> Optional[float]:
        """Return price level with highest cumulative volume so far."""
        if visible_df is None:
            return None
        try:
            if len(visible_df) == 0:
                return None
        except Exception:
            return None

        price_vol = self._build_price_vol_map(visible_df)
        if price_vol is None or len(price_vol) == 0:
            return None
        return max(price_vol, key=lambda p: price_vol[p])

    def value_area(self, visible_df) -> Tuple[Optional[float], Optional[float]]:
        """Return (value_area_high, value_area_low) — price range containing 70% of volume."""
        if visible_df is None:
            return None, None
        try:
            if len(visible_df) == 0:
                return None, None
        except Exception:
            return None, None

        price_vol = self._build_price_vol_map(visible_df)
        if price_vol is None or len(price_vol) == 0:
            return None, None

        total_vol = sum(price_vol.values())
        target_vol = total_vol * 0.70

        sorted_prices = sorted(price_vol.keys())
        poc_price = max(price_vol, key=lambda p: price_vol[p])

        # Expand from POC outward to capture 70% of volume
        poc_idx = sorted_prices.index(poc_price) if poc_price in sorted_prices else 0
        accumulated = price_vol.get(poc_price, 0)

        lo_idx = poc_idx
        hi_idx = poc_idx

        while accumulated < target_vol:
            can_expand_lo = lo_idx > 0
            can_expand_hi = hi_idx < len(sorted_prices) - 1

            if not can_expand_lo and not can_expand_hi:
                break

            vol_below = price_vol.get(sorted_prices[lo_idx - 1], 0) if can_expand_lo else 0
            vol_above = price_vol.get(sorted_prices[hi_idx + 1], 0) if can_expand_hi else 0

            if can_expand_hi and (vol_above >= vol_below or not can_expand_lo):
                hi_idx += 1
                accumulated += price_vol.get(sorted_prices[hi_idx], 0)
            else:
                lo_idx -= 1
                accumulated += price_vol.get(sorted_prices[lo_idx], 0)

        return sorted_prices[hi_idx], sorted_prices[lo_idx]

    def support_pressure_state(self, visible_df) -> str:
        """Classify current price position vs volume profile."""
        if visible_df is None:
            return UNKNOWN
        try:
            if len(visible_df) == 0:
                return UNKNOWN
        except Exception:
            return UNKNOWN

        poc = self.current_poc(visible_df)
        vah, val = self.value_area(visible_df)

        close_col = self._find_col(visible_df, ("close", "c", "price"))
        if close_col is None or poc is None:
            return UNKNOWN

        try:
            current_close = float(visible_df.iloc[-1][close_col])
        except Exception:
            return UNKNOWN

        poc_threshold = poc * 0.005  # 0.5% threshold for AT_POC
        if abs(current_close - poc) <= poc_threshold:
            return AT_POC

        if vah is not None and val is not None:
            if val <= current_close <= vah:
                return IN_VALUE_AREA
            else:
                if current_close > poc:
                    return ABOVE_POC
                else:
                    return BELOW_POC

        return ABOVE_POC if current_close > poc else BELOW_POC
