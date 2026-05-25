"""
features/volatility.py - Volatility-related features.

Computes ATR, historical realised volatility, and Bollinger Band width for
use in model training and risk management.
"""

import logging

import numpy as np
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Single-stock helpers
# ---------------------------------------------------------------------------

def _true_range(df: pd.DataFrame) -> pd.Series:
    """
    Compute True Range: max of (H-L), |H-prev_C|, |L-prev_C|.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: high, low, close.

    Returns
    -------
    pd.Series
        True range series.
    """
    high = df["high"]
    low = df["low"]
    prev_close = df["close"].shift(1)

    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr


def compute_atr(df: pd.DataFrame, period: int = None) -> pd.Series:
    """
    Compute Average True Range (ATR) using Wilder's smoothing.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain: high, low, close.
    period : int, optional
        ATR look-back period.  Defaults to ``config.ATR_PERIOD``.

    Returns
    -------
    pd.Series
        ATR values indexed like ``df``.
    """
    if period is None:
        period = config.ATR_PERIOD

    tr = _true_range(df)
    atr = tr.ewm(com=period - 1, min_periods=period).mean()
    return atr


def compute_historical_volatility(
    close: pd.Series,
    short_period: int = None,
    long_period: int = None,
) -> pd.DataFrame:
    """
    Compute short-window and long-window realised (historical) volatility
    as the annualised standard deviation of log returns.

    Parameters
    ----------
    close : pd.Series
        Closing prices.
    short_period : int, optional
        Short volatility window.  Defaults to ``config.VOL_SHORT_PERIOD``.
    long_period : int, optional
        Long volatility window.  Defaults to ``config.VOL_LONG_PERIOD``.

    Returns
    -------
    pd.DataFrame
        Columns: vol_short, vol_long, vol_ratio.
    """
    if short_period is None:
        short_period = config.VOL_SHORT_PERIOD
    if long_period is None:
        long_period = config.VOL_LONG_PERIOD

    log_ret = np.log(close / close.shift(1))

    vol_short = (
        log_ret.rolling(window=short_period, min_periods=max(1, short_period // 2)).std()
        * np.sqrt(252)
    )
    vol_long = (
        log_ret.rolling(window=long_period, min_periods=max(1, long_period // 2)).std()
        * np.sqrt(252)
    )
    vol_ratio = vol_short / vol_long.replace(0, np.nan)

    return pd.DataFrame(
        {"vol_short": vol_short, "vol_long": vol_long, "vol_ratio": vol_ratio},
        index=close.index,
    )


def compute_volatility_single(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute all volatility features for a single stock OHLCV DataFrame.

    Adds columns:
    - atr: Average True Range
    - atr_pct: ATR as percentage of close price
    - vol_short: 20-day realised volatility (annualised)
    - vol_long: 60-day realised volatility (annualised)
    - vol_ratio: vol_short / vol_long
    - vol_regime: "high" if vol_ratio > 1.2 else "low"

    Parameters
    ----------
    df : pd.DataFrame
        Single-stock OHLCV data sorted by date.

    Returns
    -------
    pd.DataFrame
        Input DataFrame with volatility columns added.
    """
    if df.empty:
        return df

    df = df.sort_values("date").copy()

    # ATR
    df["atr"] = compute_atr(df)
    df["atr_pct"] = df["atr"] / df["close"].replace(0, np.nan)

    # Historical volatility
    vol_df = compute_historical_volatility(df["close"])
    df["vol_short"] = vol_df["vol_short"].values
    df["vol_long"] = vol_df["vol_long"].values
    df["vol_ratio"] = vol_df["vol_ratio"].values

    # Volatility regime label
    df["vol_regime"] = df["vol_ratio"].apply(
        lambda r: "high" if (pd.notna(r) and r > 1.2) else "low"
    )

    # Parkinson volatility estimator (using H/L)
    hl_ratio = np.log(df["high"] / df["low"].replace(0, np.nan))
    park_var = (hl_ratio ** 2) / (4 * np.log(2))
    df["parkinson_vol"] = (
        park_var.rolling(window=20, min_periods=10).mean().apply(np.sqrt) * np.sqrt(252)
    )

    return df


# ---------------------------------------------------------------------------
# Multi-stock wrapper
# ---------------------------------------------------------------------------

def compute_volatility(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute volatility features for all stocks in a multi-stock DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain: date, stock_id, open, high, low, close, volume.

    Returns
    -------
    pd.DataFrame
        Input rows with volatility columns appended.
    """
    if df.empty:
        return df

    required = {"date", "stock_id", "high", "low", "close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame missing columns: {missing}")

    results = []
    for stock_id, group in df.groupby("stock_id"):
        try:
            enriched = compute_volatility_single(group)
            results.append(enriched)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Volatility computation failed for %s: %s", stock_id, exc)
            results.append(group)

    if not results:
        return df

    combined = pd.concat(results, ignore_index=True)
    combined = combined.sort_values(["stock_id", "date"]).reset_index(drop=True)
    return combined
