"""
intraday/vwap_features.py — VWAP feature builder (v0.3.27).
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
    logger.warning("pandas not available — VWAPFeatureBuilder will be limited")

try:
    import numpy as np
    _NUMPY_OK = True
except ImportError:
    _NUMPY_OK = False


def _empty_result(reason: str = "NO_DATA") -> dict:
    """Return a fully-keyed dict with all VWAP feature values set to None."""
    return {
        "status": reason,
        "intraday_vwap": None,
        "price_vs_vwap_pct": None,
        "vwap_slope": None,
        "above_vwap_ratio": None,
        "vwap_reclaim": None,
        "vwap_lost": None,
        "vwap_support_score": None,
    }


class VWAPFeatureBuilder:
    """
    Builds VWAP-based features from intraday 1-minute bar data.

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

    def __init__(self):
        pass

    def build(self, df) -> dict:
        """
        Build VWAP features from a standard 1min DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Must have columns: close, volume (and optionally: date, datetime)

        Returns
        -------
        dict with all VWAP feature keys; None values where data is insufficient
        """
        if not _PANDAS_OK:
            return _empty_result("NO_PANDAS")

        if df is None or (hasattr(df, "empty") and df.empty):
            return _empty_result("NO_DATA")

        try:
            df = df.copy()
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

            if "close" not in df.columns or "volume" not in df.columns:
                return _empty_result("MISSING_COLUMNS")

            close_vals = df["close"].ffill()
            vol_vals = df["volume"].fillna(0).clip(lower=0)

            # Compute VWAP per day if date column available, else session VWAP
            if "date" in df.columns:
                vwap_series = pd.Series(index=df.index, dtype=float)
                for _date, grp in df.groupby("date", sort=False):
                    grp_close = close_vals.loc[grp.index]
                    grp_vol = vol_vals.loc[grp.index]
                    cum_cv = (grp_close * grp_vol).cumsum()
                    cum_v = grp_vol.cumsum()
                    vwap_grp = cum_cv / cum_v.replace(0, float("nan"))
                    vwap_series.loc[grp.index] = vwap_grp
            else:
                cum_cv = (close_vals * vol_vals).cumsum()
                cum_v = vol_vals.cumsum()
                vwap_series = cum_cv / cum_v.replace(0, float("nan"))

            df["_vwap"] = vwap_series

            # Last valid VWAP
            vwap_vals = df["_vwap"].dropna()
            intraday_vwap: Optional[float] = None
            if len(vwap_vals) > 0:
                intraday_vwap = float(vwap_vals.iloc[-1])

            # Latest close
            latest_close: Optional[float] = None
            close_nn = close_vals.dropna()
            if len(close_nn) > 0:
                latest_close = float(close_nn.iloc[-1])

            # Price vs VWAP %
            price_vs_vwap_pct: Optional[float] = None
            if latest_close is not None and intraday_vwap is not None and intraday_vwap > 0:
                price_vs_vwap_pct = round(
                    (latest_close - intraday_vwap) / intraday_vwap * 100, 4
                )

            # VWAP slope: linear regression over last 30 bars
            vwap_slope: Optional[float] = None
            try:
                last_30 = df["_vwap"].dropna().tail(30)
                if len(last_30) >= 3:
                    if _NUMPY_OK:
                        x = np.arange(len(last_30))
                        y = last_30.values.astype(float)
                        coeffs = np.polyfit(x, y, 1)
                        vwap_slope = round(float(coeffs[0]), 6)
                    else:
                        # Manual slope from first/last
                        y_vals = list(last_30)
                        vwap_slope = round((y_vals[-1] - y_vals[0]) / max(len(y_vals) - 1, 1), 6)
            except Exception as exc:
                logger.warning("vwap_slope computation: %s", exc)

            # Above VWAP ratio: fraction of bars where close > vwap
            above_vwap_ratio: Optional[float] = None
            try:
                merged = df[["close", "_vwap"]].copy()
                merged["close"] = pd.to_numeric(merged["close"], errors="coerce")
                valid_mask = merged["_vwap"].notna() & merged["close"].notna()
                if valid_mask.sum() > 0:
                    above = (merged.loc[valid_mask, "close"] > merged.loc[valid_mask, "_vwap"]).sum()
                    above_vwap_ratio = round(float(above) / float(valid_mask.sum()), 4)
            except Exception as exc:
                logger.warning("above_vwap_ratio: %s", exc)

            # VWAP reclaim and lost
            vwap_reclaim: Optional[bool] = None
            vwap_lost: Optional[bool] = None
            try:
                if len(df) >= 2:
                    closes = df["close"].dropna().values
                    vwaps = df["_vwap"].dropna()
                    if len(vwaps) >= 2:
                        vwap_arr = vwap_series.dropna().values
                        # Align by position
                        min_len = min(len(closes), len(vwap_arr))
                        closes_aligned = closes[:min_len]
                        vwaps_aligned = vwap_arr[:min_len]
                        above_arr = closes_aligned > vwaps_aligned
                        if min_len >= 2:
                            currently_above = bool(above_arr[-1])
                            was_ever_below = not bool(above_arr[0]) or not all(above_arr)
                            was_ever_above = bool(above_arr[0]) or any(above_arr[:-1])
                            # Reclaim: was below at some point, now above
                            vwap_reclaim = currently_above and any(~above_arr[:-1])
                            # Lost: was above at some point, now below
                            vwap_lost = (not currently_above) and any(above_arr[:-1])
            except Exception as exc:
                logger.warning("vwap_reclaim/lost: %s", exc)

            # VWAP support score (0–100)
            vwap_support_score: Optional[float] = None
            try:
                score = 50.0
                if above_vwap_ratio is not None:
                    score += (above_vwap_ratio - 0.5) * 60.0  # +/- 30
                if vwap_slope is not None:
                    # Normalize slope contribution
                    if intraday_vwap and intraday_vwap > 0:
                        pct_slope = vwap_slope / intraday_vwap * 100
                    else:
                        pct_slope = vwap_slope
                    slope_contribution = min(max(pct_slope * 500, -20.0), 20.0)
                    score += slope_contribution
                if vwap_reclaim:
                    score += 10.0
                if vwap_lost:
                    score -= 10.0
                vwap_support_score = round(max(0.0, min(100.0, score)), 2)
            except Exception as exc:
                logger.warning("vwap_support_score: %s", exc)

            return {
                "status": "OK",
                "intraday_vwap": intraday_vwap,
                "price_vs_vwap_pct": price_vs_vwap_pct,
                "vwap_slope": vwap_slope,
                "above_vwap_ratio": above_vwap_ratio,
                "vwap_reclaim": vwap_reclaim,
                "vwap_lost": vwap_lost,
                "vwap_support_score": vwap_support_score,
                # v0.3.28: governance rule_id references (metadata only)
                "feature_rule_id": "INTRADAY.VWAP.RECLAIM.V1",
            }

        except Exception as exc:
            logger.exception("VWAPFeatureBuilder.build error: %s", exc)
            result = _empty_result("ERROR")
            result["warning"] = str(exc)
            return result
