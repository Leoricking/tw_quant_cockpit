"""
intraday/intraday_volume_profile.py — Intraday volume profile (v0.3.27).
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
    logger.warning("pandas not available — IntradayVolumeProfile will be limited")

try:
    import numpy as np
    _NUMPY_OK = True
except ImportError:
    _NUMPY_OK = False


def _empty_result(reason: str = "NO_DATA") -> dict:
    """Return a fully-keyed dict with all volume profile values set to None."""
    return {
        "status": reason,
        "intraday_poc_price": None,
        "intraday_value_area_high": None,
        "intraday_value_area_low": None,
        "intraday_price_vs_poc_pct": None,
        "intraday_volume_cluster_strength": None,
        "intraday_support_pressure_score": None,
    }


class IntradayVolumeProfile:
    """
    Builds an intraday volume profile (POC, value area) from 1-minute bar data.

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

    def __init__(
        self,
        price_bin_size: Optional[float] = None,
        value_area_pct: float = 0.7,
    ):
        self.price_bin_size = price_bin_size
        self.value_area_pct = value_area_pct

    def build(self, df) -> dict:
        """
        Build a volume profile from a standard 1min DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Must have columns: close, volume (high and low used for bin range)

        Returns
        -------
        dict with all volume profile feature keys; None where data is insufficient
        """
        if not _PANDAS_OK:
            return _empty_result("NO_PANDAS")

        if df is None or (hasattr(df, "empty") and df.empty):
            return _empty_result("NO_DATA")

        if len(df) < 10:
            return _empty_result("INSUFFICIENT_DATA")

        try:
            df = df.copy()
            for col in ["open", "high", "low", "close", "volume"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

            if "close" not in df.columns or "volume" not in df.columns:
                return _empty_result("MISSING_COLUMNS")

            close_vals = df["close"].dropna()
            vol_vals = df["volume"].fillna(0).clip(lower=0)

            if len(close_vals) < 10:
                return _empty_result("INSUFFICIENT_DATA")

            # Price range from high/low if available, else close
            if "high" in df.columns and "low" in df.columns:
                max_price = float(df["high"].dropna().max())
                min_price = float(df["low"].dropna().min())
            else:
                max_price = float(close_vals.max())
                min_price = float(close_vals.min())

            price_range = max_price - min_price
            if price_range <= 0:
                return _empty_result("ZERO_PRICE_RANGE")

            # Auto-compute bin size
            bin_size = self.price_bin_size
            if bin_size is None or bin_size <= 0:
                bin_size = price_range / 20.0

            # Build bins
            bins = []
            current = min_price
            while current < max_price + bin_size:
                bins.append(current)
                current += bin_size
            if len(bins) < 2:
                return _empty_result("BIN_ERROR")

            # Use close price to assign each bar to a bin; weight by volume
            bin_labels = pd.cut(
                df["close"].ffill(),
                bins=bins,
                include_lowest=True,
            )
            volume_profile = df.groupby(bin_labels, observed=True)["volume"].sum()

            if volume_profile.empty:
                return _empty_result("EMPTY_PROFILE")

            total_volume = float(volume_profile.sum())
            if total_volume <= 0:
                return _empty_result("ZERO_VOLUME")

            # POC: bin with maximum volume
            poc_bin = volume_profile.idxmax()
            if poc_bin is None or pd.isna(poc_bin):
                return _empty_result("NO_POC")

            # Mid-price of POC bin
            intraday_poc_price = round(
                (poc_bin.left + poc_bin.right) / 2.0, 4
            )

            # Value area: expand from POC to cover value_area_pct of total volume
            sorted_profile = volume_profile.sort_values(ascending=False)
            accumulated = 0.0
            value_area_bins = []
            for interval, vol in sorted_profile.items():
                if accumulated >= total_volume * self.value_area_pct:
                    break
                value_area_bins.append(interval)
                accumulated += float(vol)

            if value_area_bins:
                va_low_bounds = [b.left for b in value_area_bins]
                va_high_bounds = [b.right for b in value_area_bins]
                intraday_value_area_high = round(float(max(va_high_bounds)), 4)
                intraday_value_area_low = round(float(min(va_low_bounds)), 4)
            else:
                intraday_value_area_high = max_price
                intraday_value_area_low = min_price

            # Latest close vs POC
            latest_close: Optional[float] = None
            close_nn = df["close"].dropna()
            if len(close_nn) > 0:
                latest_close = float(close_nn.iloc[-1])

            intraday_price_vs_poc_pct: Optional[float] = None
            if latest_close is not None and intraday_poc_price > 0:
                intraday_price_vs_poc_pct = round(
                    (latest_close - intraday_poc_price) / intraday_poc_price * 100, 4
                )

            # Cluster strength: top 3 bins as fraction of total volume
            top3_vol = float(sorted_profile.head(3).sum())
            intraday_volume_cluster_strength = round(
                min(top3_vol / total_volume * 100.0, 100.0), 2
            )

            # Support pressure score (0–100)
            intraday_support_pressure_score: Optional[float] = None
            try:
                score = 50.0

                # Position relative to value area
                if (latest_close is not None and intraday_value_area_high is not None
                        and intraday_value_area_low is not None):
                    va_range = intraday_value_area_high - intraday_value_area_low
                    if va_range > 0:
                        va_position = (latest_close - intraday_value_area_low) / va_range
                        # Being in upper half of VA is bullish: +/- up to 30
                        score += (va_position - 0.5) * 60.0
                    elif latest_close >= intraday_value_area_high:
                        score += 20.0
                    elif latest_close <= intraday_value_area_low:
                        score -= 20.0

                # Cluster strength contribution: highly clustered = more reliable levels
                score += (intraday_volume_cluster_strength - 50.0) * 0.4

                intraday_support_pressure_score = round(max(0.0, min(100.0, score)), 2)
            except Exception as exc:
                logger.warning("support_pressure_score: %s", exc)

            return {
                "status": "OK",
                "intraday_poc_price": intraday_poc_price,
                "intraday_value_area_high": intraday_value_area_high,
                "intraday_value_area_low": intraday_value_area_low,
                "intraday_price_vs_poc_pct": intraday_price_vs_poc_pct,
                "intraday_volume_cluster_strength": intraday_volume_cluster_strength,
                "intraday_support_pressure_score": intraday_support_pressure_score,
            }

        except Exception as exc:
            logger.exception("IntradayVolumeProfile.build error: %s", exc)
            result = _empty_result("ERROR")
            result["warning"] = str(exc)
            return result
