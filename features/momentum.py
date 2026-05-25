"""
features/momentum.py - Price momentum and rate-of-change features.

Computes N-day return, momentum scores, and rate of change for use in
both strategy signal generation and ML model features.
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

def _return(close: pd.Series, period: int) -> pd.Series:
    """Compute N-period simple return: (close / close.shift(period)) - 1."""
    return (close / close.shift(period).replace(0, np.nan)) - 1


def _roc(close: pd.Series, period: int) -> pd.Series:
    """
    Rate of Change: percentage change over N periods.
    Identical to simple return but expressed as a percentage.
    """
    return _return(close, period) * 100


def _momentum_score(df: pd.DataFrame, weights: dict = None) -> pd.Series:
    """
    Compute a composite momentum score as a weighted sum of period returns.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns ``ret_1d``, ``ret_5d``, ``ret_20d``.
    weights : dict, optional
        Mapping of column name to weight.  Defaults to
        {ret_1d: 0.2, ret_5d: 0.3, ret_20d: 0.5}.

    Returns
    -------
    pd.Series
        Composite momentum score.
    """
    if weights is None:
        weights = {"ret_1d": 0.2, "ret_5d": 0.3, "ret_20d": 0.5}

    score = pd.Series(0.0, index=df.index)
    for col, w in weights.items():
        if col in df.columns:
            score += df[col].fillna(0) * w

    return score


def compute_momentum_single(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute momentum features for a single stock.

    Adds columns:
    - ret_1d, ret_5d, ret_20d: simple N-day returns
    - roc_1d, roc_5d, roc_20d: rate of change (percentage)
    - momentum_score: weighted composite of period returns
    - ret_fwd_5d: 5-day forward return (used as ML target label)
    - up_5d: binary, 1 if ret_fwd_5d > 0 else 0

    Parameters
    ----------
    df : pd.DataFrame
        Single-stock OHLCV data sorted by date.

    Returns
    -------
    pd.DataFrame
        Input DataFrame with momentum columns added.
    """
    if df.empty or "close" not in df.columns:
        return df

    df = df.sort_values("date").copy()
    close = df["close"]

    # Period returns
    for period in config.MOMENTUM_PERIODS:
        df[f"ret_{period}d"] = _return(close, period)
        df[f"roc_{period}d"] = _roc(close, period)

    # Composite momentum score
    df["momentum_score"] = _momentum_score(df)

    # Forward return labels for model training
    fwd = config.FORWARD_RETURN_DAYS
    df[f"ret_fwd_{fwd}d"] = _return(close, -fwd)  # negative shift = look forward
    df[f"up_{fwd}d"] = (df[f"ret_fwd_{fwd}d"] > 0).astype(float)
    # Mark last `fwd` rows as NaN (no forward data available)
    df.loc[df.index[-fwd:], f"ret_fwd_{fwd}d"] = np.nan
    df.loc[df.index[-fwd:], f"up_{fwd}d"] = np.nan

    # Additional momentum indicators
    # 52-week high ratio
    high_52w = close.rolling(window=252, min_periods=126).max()
    df["price_to_52w_high"] = close / high_52w.replace(0, np.nan)

    # Distance from 20-day high / low
    high_20d = df["high"].rolling(window=20, min_periods=10).max() if "high" in df.columns else close.rolling(20).max()
    low_20d  = df["low"].rolling(window=20, min_periods=10).min()  if "low"  in df.columns else close.rolling(20).min()
    df["dist_from_20d_high"] = (close - high_20d) / high_20d.replace(0, np.nan)
    df["dist_from_20d_low"]  = (close - low_20d)  / low_20d.replace(0, np.nan)

    return df


# ---------------------------------------------------------------------------
# Multi-stock wrapper
# ---------------------------------------------------------------------------

def compute_momentum(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute momentum features for all stocks in a multi-stock DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain: date, stock_id, close (and optionally high, low).

    Returns
    -------
    pd.DataFrame
        Input rows with momentum feature columns appended.
    """
    if df.empty:
        return df

    required = {"date", "stock_id", "close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame missing columns: {missing}")

    results = []
    for stock_id, group in df.groupby("stock_id"):
        try:
            enriched = compute_momentum_single(group)
            results.append(enriched)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Momentum computation failed for %s: %s", stock_id, exc)
            results.append(group)

    if not results:
        return df

    combined = pd.concat(results, ignore_index=True)
    combined = combined.sort_values(["stock_id", "date"]).reset_index(drop=True)
    return combined
