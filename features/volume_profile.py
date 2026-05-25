"""
features/volume_profile.py - Volume Profile (分價量) analysis.

Computes the distribution of traded volume across price levels for a given
lookback window.  All features use only historical data up to and including
the current bar (no forward-looking data).

Features produced:
    vp_peak_price          : price level with maximum accumulated volume
    vp_peak_volume         : volume at the peak level
    vp_distance_to_peak    : (close - peak_price) / close  — positive = above peak
    vp_cluster_strength    : peak_volume / total_volume in window (concentration)
    vp_support_score       : score for support below close (volume below close / total)
    vp_pressure_score      : score for resistance above close (volume above close / total)
    support_pressure_score : net score = support_score - pressure_score
    vp_poc_pct             : Point of Control as % of 52-week price range
    vp_value_area_high     : upper bound of Value Area (70% of volume)
    vp_value_area_low      : lower bound of Value Area (70% of volume)
    vp_price_in_value_area : 1 if close is within Value Area, else 0
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Default number of price buckets for volume distribution
DEFAULT_N_BINS = 20
# Default lookback window in trading days
DEFAULT_LOOKBACK = 60
# Value Area covers this fraction of total volume
VALUE_AREA_PCT = 0.70


def compute_volume_profile_single(
    df: pd.DataFrame,
    n_bins: int = DEFAULT_N_BINS,
    lookback: int = DEFAULT_LOOKBACK,
) -> pd.DataFrame:
    """
    Compute Volume Profile features for a single stock.

    Uses a rolling window so each row only sees past data.  The window for
    row T includes rows [T-lookback+1 … T].

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: date, high, low, close, volume.
        Sorted ascending by date.
    n_bins : int
        Number of price buckets for the volume distribution.
    lookback : int
        Number of bars to include in each rolling volume profile.

    Returns
    -------
    pd.DataFrame
        Original columns plus Volume Profile feature columns.
    """
    if df.empty or not {"high", "low", "close", "volume"}.issubset(df.columns):
        return df

    df = df.sort_values("date").copy()
    n = len(df)

    # Pre-allocate output arrays
    peak_price_arr = np.full(n, np.nan)
    peak_volume_arr = np.full(n, np.nan)
    dist_to_peak_arr = np.full(n, np.nan)
    cluster_strength_arr = np.full(n, np.nan)
    support_score_arr = np.full(n, np.nan)
    pressure_score_arr = np.full(n, np.nan)
    net_score_arr = np.full(n, np.nan)
    poc_pct_arr = np.full(n, np.nan)
    va_high_arr = np.full(n, np.nan)
    va_low_arr = np.full(n, np.nan)
    in_va_arr = np.full(n, np.nan)

    high_arr = df["high"].values
    low_arr = df["low"].values
    close_arr = df["close"].values
    volume_arr = df["volume"].values

    for i in range(n):
        start = max(0, i - lookback + 1)
        w_high = high_arr[start : i + 1]
        w_low = low_arr[start : i + 1]
        w_close = close_arr[start : i + 1]
        w_vol = volume_arr[start : i + 1]

        if len(w_high) < 5:
            continue

        price_min = float(np.nanmin(w_low))
        price_max = float(np.nanmax(w_high))
        if price_max <= price_min:
            continue

        # Build price bins
        bin_edges = np.linspace(price_min, price_max, n_bins + 1)
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        bin_volumes = np.zeros(n_bins)

        # Distribute each bar's volume across the price bins it spans
        for j in range(len(w_high)):
            bar_low = w_low[j]
            bar_high = w_high[j]
            bar_vol = w_vol[j]
            if np.isnan(bar_low) or np.isnan(bar_high) or np.isnan(bar_vol):
                continue
            bar_range = bar_high - bar_low
            if bar_range < 1e-9:
                # Point bar — assign all volume to closest bin
                idx = int(np.searchsorted(bin_edges[1:], (bar_low + bar_high) / 2))
                idx = min(idx, n_bins - 1)
                bin_volumes[idx] += bar_vol
            else:
                for k in range(n_bins):
                    overlap_low = max(bin_edges[k], bar_low)
                    overlap_high = min(bin_edges[k + 1], bar_high)
                    if overlap_high > overlap_low:
                        fraction = (overlap_high - overlap_low) / bar_range
                        bin_volumes[k] += bar_vol * fraction

        total_vol = bin_volumes.sum()
        if total_vol < 1e-9:
            continue

        peak_idx = int(np.argmax(bin_volumes))
        peak_price = float(bin_centers[peak_idx])
        peak_vol = float(bin_volumes[peak_idx])
        cur_close = float(close_arr[i])

        # Value Area: find contiguous range of bins covering VALUE_AREA_PCT of volume
        va_target = total_vol * VALUE_AREA_PCT
        # Start from peak and expand outward
        va_bins = set([peak_idx])
        va_vol = bin_volumes[peak_idx]
        lo_ptr, hi_ptr = peak_idx, peak_idx
        while va_vol < va_target:
            can_go_low = lo_ptr > 0
            can_go_high = hi_ptr < n_bins - 1
            if not can_go_low and not can_go_high:
                break
            if can_go_low and can_go_high:
                if bin_volumes[lo_ptr - 1] >= bin_volumes[hi_ptr + 1]:
                    lo_ptr -= 1
                    va_bins.add(lo_ptr)
                    va_vol += bin_volumes[lo_ptr]
                else:
                    hi_ptr += 1
                    va_bins.add(hi_ptr)
                    va_vol += bin_volumes[hi_ptr]
            elif can_go_low:
                lo_ptr -= 1
                va_bins.add(lo_ptr)
                va_vol += bin_volumes[lo_ptr]
            else:
                hi_ptr += 1
                va_bins.add(hi_ptr)
                va_vol += bin_volumes[hi_ptr]

        va_high = float(bin_edges[hi_ptr + 1])
        va_low = float(bin_edges[lo_ptr])

        # Volume below and above current close (support vs pressure)
        vol_below = float(bin_volumes[bin_centers <= cur_close].sum())
        vol_above = float(bin_volumes[bin_centers > cur_close].sum())
        support_score = vol_below / total_vol
        pressure_score = vol_above / total_vol

        # POC position within 52-week price range (use full history if < 252 bars)
        hist_start = max(0, i - 251)
        hist_min = float(np.nanmin(low_arr[hist_start : i + 1]))
        hist_max = float(np.nanmax(high_arr[hist_start : i + 1]))
        poc_pct = (
            (peak_price - hist_min) / (hist_max - hist_min)
            if hist_max > hist_min
            else 0.5
        )

        peak_price_arr[i] = peak_price
        peak_volume_arr[i] = peak_vol
        dist_to_peak_arr[i] = (cur_close - peak_price) / cur_close if cur_close != 0 else np.nan
        cluster_strength_arr[i] = peak_vol / total_vol
        support_score_arr[i] = support_score
        pressure_score_arr[i] = pressure_score
        net_score_arr[i] = support_score - pressure_score
        poc_pct_arr[i] = poc_pct
        va_high_arr[i] = va_high
        va_low_arr[i] = va_low
        in_va_arr[i] = 1.0 if va_low <= cur_close <= va_high else 0.0

    df["vp_peak_price"] = peak_price_arr
    df["vp_peak_volume"] = peak_volume_arr
    df["vp_distance_to_peak"] = dist_to_peak_arr
    df["vp_cluster_strength"] = cluster_strength_arr
    df["vp_support_score"] = support_score_arr
    df["vp_pressure_score"] = pressure_score_arr
    df["support_pressure_score"] = net_score_arr
    df["vp_poc_pct"] = poc_pct_arr
    df["vp_value_area_high"] = va_high_arr
    df["vp_value_area_low"] = va_low_arr
    df["vp_price_in_value_area"] = in_va_arr

    return df


def compute_volume_profile(
    df: pd.DataFrame,
    n_bins: int = DEFAULT_N_BINS,
    lookback: int = DEFAULT_LOOKBACK,
) -> pd.DataFrame:
    """
    Compute Volume Profile features for all stocks in a multi-stock DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: date, stock_id, high, low, close, volume.
    n_bins : int
    lookback : int

    Returns
    -------
    pd.DataFrame
        Same rows with Volume Profile feature columns appended.
    """
    if df.empty:
        return df

    required = {"date", "stock_id", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        logger.warning("compute_volume_profile: missing columns %s — skipping.", missing)
        return df

    results = []
    for stock_id, group in df.groupby("stock_id"):
        try:
            enriched = compute_volume_profile_single(group, n_bins=n_bins, lookback=lookback)
            results.append(enriched)
        except Exception as exc:
            logger.error("Volume profile failed for %s: %s", stock_id, exc)
            results.append(group)

    if not results:
        return df

    combined = pd.concat(results, ignore_index=True)
    combined = combined.sort_values(["stock_id", "date"]).reset_index(drop=True)
    return combined


def get_volume_profile_columns() -> list:
    """Return the list of column names produced by this module."""
    return [
        "vp_peak_price",
        "vp_peak_volume",
        "vp_distance_to_peak",
        "vp_cluster_strength",
        "vp_support_score",
        "vp_pressure_score",
        "support_pressure_score",
        "vp_poc_pct",
        "vp_value_area_high",
        "vp_value_area_low",
        "vp_price_in_value_area",
    ]
