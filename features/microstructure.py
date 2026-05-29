"""
features/microstructure.py - Market microstructure features (盤口微觀).

Two operating modes:

1. **Daily OHLCV only** (default):
   Approximates microstructure signals from end-of-day data.
   All features are best-effort proxies; they are labelled with ``_proxy``
   in name or set to NaN where reliable estimation is impossible.

2. **Intraday / Tick data** (optional ``intraday_df``):
   When a per-minute or per-tick DataFrame is provided, computes proper
   opening 15-minute features, actual buy/sell pressure, and large trade ratio.

Features produced:
    opening_return_15m      : return from open to 15-min high proxy (daily: uses open vs high/low)
    opening_volume_ratio    : opening volume relative to average (daily: first-bar proxy)
    opening_high_break      : 1 if price breaks above previous day's high in opening
    opening_low_break       : 1 if price breaks below previous day's low in opening
    large_trade_ratio       : fraction of volume in large bars (daily: volume spike proxy)
    buy_sell_pressure       : (close - low) / (high - low) — 0=full sell, 1=full buy
    microstructure_score    : composite [0, 1] score; higher = stronger buy-side pressure
    ms_fake_breakout_risk   : 1 if price gapped up but closed near open (potential fake)
    ms_no_chase_flag        : 1 if microstructure_score < 0.4 yet same-day return > 2%
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Single-stock computation (daily OHLCV)
# ---------------------------------------------------------------------------

def compute_microstructure_single(
    df: pd.DataFrame,
    intraday_df: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """
    Compute microstructure features for a single stock.

    Parameters
    ----------
    df : pd.DataFrame
        Daily OHLCV.  Must contain: date, open, high, low, close, volume.
        Sorted ascending by date.
    intraday_df : pd.DataFrame, optional
        Per-minute or per-tick DataFrame with columns:
        datetime, open, high, low, close, volume, [buy_volume, sell_volume].
        If provided, proper opening 15-min features are computed.
        If None, daily proxies are used.

    Returns
    -------
    pd.DataFrame
        Original columns plus microstructure feature columns.
    """
    required_daily = {"date", "open", "high", "low", "close", "volume"}
    if df.empty or not required_daily.issubset(df.columns):
        return df

    df = df.sort_values("date").copy()
    n = len(df)

    # ---- Pre-allocate -------------------------------------------------------
    opening_ret_15m = np.full(n, np.nan)
    opening_vol_ratio = np.full(n, np.nan)
    opening_high_break = np.full(n, np.nan)
    opening_low_break = np.full(n, np.nan)
    large_trade_ratio = np.full(n, np.nan)
    buy_sell_pressure = np.full(n, np.nan)
    ms_score = np.full(n, np.nan)
    fake_breakout = np.full(n, np.nan)
    no_chase_flag = np.full(n, np.nan)

    open_arr = df["open"].values
    high_arr = df["high"].values
    low_arr = df["low"].values
    close_arr = df["close"].values
    vol_arr = df["volume"].values

    # 20-day average volume
    avg_vol_20 = pd.Series(vol_arr).rolling(20, min_periods=5).mean().values

    # ---- Intraday path (if available) ---------------------------------------
    intraday_lookup: dict = {}
    if intraday_df is not None and not intraday_df.empty:
        _check_intraday_cols(intraday_df)
        if "datetime" in intraday_df.columns:
            intraday_df = intraday_df.copy()
            intraday_df["datetime"] = pd.to_datetime(intraday_df["datetime"])
            intraday_df["_date"] = intraday_df["datetime"].dt.date
        elif "date" in intraday_df.columns:
            intraday_df = intraday_df.copy()
            intraday_df["_date"] = pd.to_datetime(intraday_df["date"]).dt.date
        else:
            intraday_df = None

        if intraday_df is not None:
            for _d, grp in intraday_df.groupby("_date"):
                intraday_lookup[str(_d)] = grp

    # ---- Row-by-row computation ---------------------------------------------
    for i in range(n):
        o = open_arr[i]
        h = high_arr[i]
        lo = low_arr[i]
        c = close_arr[i]
        v = vol_arr[i]
        avg_v = avg_vol_20[i]
        date_str = str(df["date"].iloc[i])[:10]

        if np.isnan(o) or np.isnan(h) or np.isnan(lo) or np.isnan(c):
            continue

        # ---- Buy/sell pressure (Williams %R style) --------------------------
        bar_range = h - lo
        bsp = (c - lo) / bar_range if bar_range > 1e-9 else 0.5
        buy_sell_pressure[i] = bsp

        # ---- Large trade ratio proxy (volume spike relative to 20-day avg) --
        if not np.isnan(avg_v) and avg_v > 0:
            ltr = min(v / avg_v / 2.0, 1.0)  # normalise so 2× avg → 1.0
        else:
            ltr = 0.5
        large_trade_ratio[i] = ltr

        # ---- High/low break from previous day -------------------------------
        if i > 0:
            prev_h = high_arr[i - 1]
            prev_lo = low_arr[i - 1]
            if not np.isnan(prev_h) and not np.isnan(prev_lo):
                opening_high_break[i] = 1.0 if o > prev_h else 0.0
                opening_low_break[i] = 1.0 if o < prev_lo else 0.0
        else:
            opening_high_break[i] = 0.0
            opening_low_break[i] = 0.0

        # ---- Opening features -----------------------------------------------
        if date_str in intraday_lookup:
            # Use actual intraday data for the opening 15 minutes
            iday = intraday_lookup[date_str]
            if "datetime" in iday.columns:
                iday = iday.sort_values("datetime")
                open_time = iday["datetime"].iloc[0]
                cutoff = open_time + pd.Timedelta(minutes=15)
                opening_bars = iday[iday["datetime"] <= cutoff]
            else:
                opening_bars = iday.head(3)  # assume first 3 bars ≈ 15 min

            if not opening_bars.empty:
                first_open = opening_bars["open"].iloc[0]
                opening_high = opening_bars["high"].max()
                opening_low = opening_bars["low"].min()
                opening_vol = opening_bars["volume"].sum()

                if not np.isnan(first_open) and first_open > 0:
                    opening_ret_15m[i] = (opening_high - first_open) / first_open

                if not np.isnan(avg_v) and avg_v > 0:
                    # Scale opening volume to full-day equivalent
                    full_day_equiv = opening_vol * (390 / 15)  # Taiwan market ~390min
                    opening_vol_ratio[i] = full_day_equiv / avg_v
                else:
                    opening_vol_ratio[i] = 1.0

                # Refined buy/sell pressure from intraday if buy/sell columns present
                if "buy_volume" in opening_bars.columns and "sell_volume" in opening_bars.columns:
                    buy_v = opening_bars["buy_volume"].sum()
                    sell_v = opening_bars["sell_volume"].sum()
                    total_v = buy_v + sell_v
                    if total_v > 0:
                        buy_sell_pressure[i] = buy_v / total_v
        else:
            # Daily proxy: use open vs close position within bar
            if o > 0:
                opening_ret_15m[i] = (h - o) / o * 0.5  # rough proxy: half of bar range
            if not np.isnan(avg_v) and avg_v > 0:
                opening_vol_ratio[i] = v / avg_v
            else:
                opening_vol_ratio[i] = 1.0

        # ---- Fake breakout risk ---------------------------------------------
        # Condition: gap up from previous close, but close is near open
        if i > 0:
            prev_c = close_arr[i - 1]
            if not np.isnan(prev_c) and prev_c > 0:
                gap_up = (o - prev_c) / prev_c > 0.01  # gap > 1%
                close_near_open = abs(c - o) / o < 0.005 if o > 0 else False
                daily_ret = (c - prev_c) / prev_c
                # Fake breakout: gap up, but closed near open AND volume not confirming
                if gap_up and close_near_open and ltr < 0.5:
                    fake_breakout[i] = 1.0
                else:
                    fake_breakout[i] = 0.0

                # No-chase flag: price surged today but microstructure is weak
                # (computed after ms_score is set below)
                no_chase_flag[i] = 0.0  # will update below

        # ---- Composite microstructure score [0, 1] --------------------------
        # Components: buy_sell_pressure, large_trade_ratio, opening_vol_ratio
        # (normalised to [0,1])
        ovr = opening_vol_ratio[i]
        ovr_norm = min(ovr / 2.0, 1.0) if not np.isnan(ovr) else 0.5

        score = (
            0.40 * bsp
            + 0.30 * ltr
            + 0.30 * ovr_norm
        )
        ms_score[i] = float(np.clip(score, 0.0, 1.0))

    # ---- No-chase flag (needs ms_score to be computed first) ----------------
    ret_1d = np.full(n, np.nan)
    for i in range(1, n):
        prev_c = close_arr[i - 1]
        if not np.isnan(prev_c) and prev_c > 0:
            ret_1d[i] = (close_arr[i] - prev_c) / prev_c

    for i in range(n):
        if not np.isnan(ms_score[i]) and not np.isnan(ret_1d[i]):
            if ms_score[i] < 0.4 and ret_1d[i] > 0.02:
                no_chase_flag[i] = 1.0
            else:
                no_chase_flag[i] = 0.0

    # ---- Write to DataFrame -------------------------------------------------
    df["opening_return_15m"] = opening_ret_15m
    df["opening_volume_ratio"] = opening_vol_ratio
    df["opening_high_break"] = opening_high_break
    df["opening_low_break"] = opening_low_break
    df["large_trade_ratio"] = large_trade_ratio
    df["buy_sell_pressure"] = buy_sell_pressure
    df["microstructure_score"] = ms_score
    df["ms_fake_breakout_risk"] = fake_breakout
    df["ms_no_chase_flag"] = no_chase_flag

    # v0.3.9: tag data source for microstructure features
    has_intraday = bool(intraday_lookup)
    if has_intraday:
        df["microstructure_source"] = "INTRADAY_1MIN"
    elif not df.empty:
        df["microstructure_source"] = "DAILY_PROXY"
    else:
        df["microstructure_source"] = "UNAVAILABLE"

    return df


# ---------------------------------------------------------------------------
# Multi-stock wrapper
# ---------------------------------------------------------------------------

def compute_microstructure(
    df: pd.DataFrame,
    intraday_df: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """
    Compute microstructure features for all stocks in a multi-stock DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain: date, stock_id, open, high, low, close, volume.
    intraday_df : pd.DataFrame, optional
        Must contain: stock_id, datetime (or date), open, high, low, close, volume.
        When provided, proper intraday opening features are computed per stock.

    Returns
    -------
    pd.DataFrame
        Same rows with microstructure feature columns appended.
    """
    if df.empty:
        return df

    required = {"date", "stock_id", "open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        logger.warning("compute_microstructure: missing columns %s — skipping.", missing)
        return df

    # Build per-stock intraday lookup
    intraday_by_stock: dict = {}
    if intraday_df is not None and not intraday_df.empty and "stock_id" in intraday_df.columns:
        for sid, grp in intraday_df.groupby("stock_id"):
            intraday_by_stock[sid] = grp

    results = []
    for stock_id, group in df.groupby("stock_id"):
        try:
            iday = intraday_by_stock.get(stock_id, None)
            enriched = compute_microstructure_single(group, intraday_df=iday)
            results.append(enriched)
        except Exception as exc:
            logger.error("Microstructure failed for %s: %s", stock_id, exc)
            results.append(group)

    if not results:
        return df

    combined = pd.concat(results, ignore_index=True)
    combined = combined.sort_values(["stock_id", "date"]).reset_index(drop=True)
    return combined


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _check_intraday_cols(iday: pd.DataFrame) -> None:
    """Log a warning if expected intraday columns are missing."""
    expected = {"open", "high", "low", "close", "volume"}
    missing = expected - set(iday.columns)
    if missing:
        logger.warning("Intraday DataFrame missing columns: %s", missing)


def get_microstructure_columns() -> list:
    """Return the list of column names produced by this module."""
    return [
        "opening_return_15m",
        "opening_volume_ratio",
        "opening_high_break",
        "opening_low_break",
        "large_trade_ratio",
        "buy_sell_pressure",
        "microstructure_score",
        "ms_fake_breakout_risk",
        "ms_no_chase_flag",
    ]
