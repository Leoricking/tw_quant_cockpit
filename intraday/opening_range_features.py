"""
intraday/opening_range_features.py — Opening range feature builder (v0.3.27).
[!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import pandas as pd
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False
    logger.warning("pandas not available — OpeningRangeFeatureBuilder will be limited")

try:
    import numpy as np
    _NUMPY_OK = True
except ImportError:
    _NUMPY_OK = False


def _empty_result(reason: str = "NO_DATA") -> dict:
    """Return a fully-keyed dict with all feature values set to None."""
    return {
        "status": reason,
        "opening_return_5m": None,
        "opening_return_15m": None,
        "opening_return_30m": None,
        "opening_volume_ratio_15m": None,
        "opening_high": None,
        "opening_low": None,
        "opening_range_pct": None,
        "opening_high_break": None,
        "opening_low_break": None,
        "opening_range_position": None,
        "opening_strength_score": None,
    }


class OpeningRangeFeatureBuilder:
    """
    Builds opening range features from intraday 1-minute bar data.

    [!] Research / Intraday Research Only. No Real Orders. Production Trading: BLOCKED.

    Safety flags
    ------------
    read_only           : True
    no_real_orders      : True
    production_blocked  : True
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(self, opening_minutes: int = 15, extended_minutes: int = 30):
        self.opening_minutes = opening_minutes
        self.extended_minutes = extended_minutes

    def build(self, df) -> dict:
        """
        Build opening range features from a standard 1min DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Must have columns: datetime (or date+time), open, high, low, close, volume

        Returns
        -------
        dict with all opening range features; None values where data is insufficient
        """
        if not _PANDAS_OK:
            result = _empty_result("NO_PANDAS")
            return result

        if df is None or (hasattr(df, "empty") and df.empty):
            return _empty_result("NO_DATA")

        try:
            df = df.copy()
            # Coerce numeric columns
            for col in ["open", "high", "low", "close", "volume"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

            # Sort by datetime / time
            if "datetime" in df.columns:
                df["_sort_dt"] = pd.to_datetime(df["datetime"], errors="coerce")
                df = df.sort_values("_sort_dt").reset_index(drop=True)
            elif "time" in df.columns:
                df = df.sort_values("time").reset_index(drop=True)

            if len(df) == 0:
                return _empty_result("NO_DATA")

            first_open = df["open"].iloc[0] if "open" in df.columns else None
            if first_open is None or (isinstance(first_open, float) and pd.isna(first_open)):
                return _empty_result("NO_OPEN_PRICE")

            total_bars = len(df)

            # Helper to safely get subset
            def safe_slice(n: int):
                return df.iloc[:min(n, total_bars)]

            bars_5m = safe_slice(5)
            bars_15m = safe_slice(self.opening_minutes)
            bars_30m = safe_slice(self.extended_minutes)

            def last_close(subset):
                if subset.empty or "close" not in subset.columns:
                    return None
                val = subset["close"].dropna()
                return float(val.iloc[-1]) if len(val) > 0 else None

            def compute_return(subset) -> Optional[float]:
                lc = last_close(subset)
                if lc is None or first_open == 0:
                    return None
                return round((lc - first_open) / first_open, 6)

            opening_return_5m = compute_return(bars_5m)
            opening_return_15m = compute_return(bars_15m)
            opening_return_30m = compute_return(bars_30m)

            # Opening high / low from 15m period
            opening_high: Optional[float] = None
            opening_low: Optional[float] = None
            if "high" in bars_15m.columns and "low" in bars_15m.columns:
                h_vals = bars_15m["high"].dropna()
                l_vals = bars_15m["low"].dropna()
                opening_high = float(h_vals.max()) if len(h_vals) > 0 else None
                opening_low = float(l_vals.min()) if len(l_vals) > 0 else None

            opening_range_pct: Optional[float] = None
            if opening_high is not None and opening_low is not None and opening_low > 0:
                opening_range_pct = round((opening_high - opening_low) / opening_low, 6)

            # Volume ratio
            opening_volume_ratio_15m: Optional[float] = None
            if "volume" in df.columns:
                opening_vol = bars_15m["volume"].dropna().sum()
                all_vol = df["volume"].dropna()
                if len(all_vol) > 0:
                    mean_per_bar = float(all_vol.mean())
                    expected_vol = mean_per_bar * min(self.opening_minutes, total_bars)
                    if expected_vol > 0:
                        opening_volume_ratio_15m = round(float(opening_vol) / expected_vol, 4)

            # Post-opening period (after opening_minutes)
            post_opening = df.iloc[self.opening_minutes:] if total_bars > self.opening_minutes else pd.DataFrame()

            latest_close: Optional[float] = None
            if not post_opening.empty and "close" in post_opening.columns:
                lc_vals = post_opening["close"].dropna()
                if len(lc_vals) > 0:
                    latest_close = float(lc_vals.iloc[-1])
            elif "close" in df.columns:
                lc_vals = df["close"].dropna()
                if len(lc_vals) > 0:
                    latest_close = float(lc_vals.iloc[-1])

            opening_high_break: Optional[bool] = None
            opening_low_break: Optional[bool] = None
            if latest_close is not None and opening_high is not None:
                opening_high_break = bool(latest_close > opening_high)
            if latest_close is not None and opening_low is not None:
                opening_low_break = bool(latest_close < opening_low)

            opening_range_position: Optional[float] = None
            if (latest_close is not None and opening_high is not None
                    and opening_low is not None):
                rng = opening_high - opening_low
                if rng > 0:
                    opening_range_position = round(
                        (latest_close - opening_low) / rng, 4
                    )
                else:
                    opening_range_position = 0.5

            # Opening strength score (0–100)
            opening_strength_score: Optional[float] = None
            try:
                score = 50.0  # neutral baseline

                # Return component: +/- up to 30 points
                if opening_return_15m is not None:
                    # Normalize: 2% return ≈ max contribution
                    ret_contribution = min(max(opening_return_15m / 0.02, -1.0), 1.0) * 30.0
                    score += ret_contribution

                # Volume component: +20 if ratio > 1.5
                if opening_volume_ratio_15m is not None:
                    if opening_volume_ratio_15m > 1.5:
                        score += 20.0
                    elif opening_volume_ratio_15m > 1.0:
                        score += 10.0

                # Range position component: +/- up to 20 points
                if opening_range_position is not None:
                    # 1.0 = at top of range = positive; 0.0 = bottom = negative
                    range_contribution = (opening_range_position - 0.5) * 40.0
                    score += range_contribution

                opening_strength_score = round(max(0.0, min(100.0, score)), 2)
            except Exception as exc:
                logger.warning("opening_strength_score computation error: %s", exc)
                opening_strength_score = None

            return {
                "status": "OK",
                "opening_return_5m": opening_return_5m,
                "opening_return_15m": opening_return_15m,
                "opening_return_30m": opening_return_30m,
                "opening_volume_ratio_15m": opening_volume_ratio_15m,
                "opening_high": opening_high,
                "opening_low": opening_low,
                "opening_range_pct": opening_range_pct,
                "opening_high_break": opening_high_break,
                "opening_low_break": opening_low_break,
                "opening_range_position": opening_range_position,
                "opening_strength_score": opening_strength_score,
                # v0.3.28: governance rule_id reference (metadata only)
                "feature_rule_id": "INTRADAY.OPENING.RANGE_STRENGTH.V1",
            }

        except Exception as exc:
            logger.exception("OpeningRangeFeatureBuilder.build error: %s", exc)
            result = _empty_result("ERROR")
            result["warning"] = str(exc)
            return result
