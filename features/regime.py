"""
features/regime.py - Market regime detection.

Detects bull / bear / sideways price regimes using MA crossovers,
and high / low volatility regimes using realised volatility ratios.

Rules
-----
Bull    : SMA20 > SMA60 AND close > SMA20
Bear    : SMA20 < SMA60 AND close < SMA20
Sideways: everything else

Volatility High : 20-day vol > 1.2 × 60-day vol
Volatility Low  : otherwise
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Per-stock regime detection
# ---------------------------------------------------------------------------

def detect_regime_single(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect price and volatility regime for a single stock.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain at minimum: date, close.
        If sma_20, sma_60, vol_short, vol_long are already present they are
        re-used; otherwise they are computed here.

    Returns
    -------
    pd.DataFrame
        Input DataFrame with columns added:
        - regime: str  ("bull", "bear", "sideways")
        - vol_regime: str  ("high", "low")
        - regime_code: int  (1 = bull, -1 = bear, 0 = sideways)
    """
    if df.empty:
        return df

    df = df.sort_values("date").copy()
    close = df["close"]

    # ---- Moving averages ---------------------------------------------------
    if "sma_20" not in df.columns:
        df["sma_20"] = close.rolling(window=20, min_periods=10).mean()
    if "sma_60" not in df.columns:
        df["sma_60"] = close.rolling(window=60, min_periods=30).mean()

    sma20 = df["sma_20"]
    sma60 = df["sma_60"]

    # ---- Price regime ------------------------------------------------------
    bull_cond = (sma20 > sma60) & (close > sma20)
    bear_cond = (sma20 < sma60) & (close < sma20)

    regime = pd.Series("sideways", index=df.index, dtype=str)
    regime[bull_cond] = "bull"
    regime[bear_cond] = "bear"
    # Where we lack sufficient data for either MA, mark as unknown
    regime[sma20.isna() | sma60.isna()] = "unknown"
    df["regime"] = regime

    df["regime_code"] = regime.map({"bull": 1, "sideways": 0, "bear": -1, "unknown": 0})

    # ---- Volatility regime -------------------------------------------------
    if "vol_short" not in df.columns or "vol_long" not in df.columns:
        log_ret = np.log(close / close.shift(1))
        df["vol_short"] = (
            log_ret.rolling(window=config.VOL_SHORT_PERIOD, min_periods=10).std() * np.sqrt(252)
        )
        df["vol_long"] = (
            log_ret.rolling(window=config.VOL_LONG_PERIOD, min_periods=30).std() * np.sqrt(252)
        )

    vol_ratio = df["vol_short"] / df["vol_long"].replace(0, np.nan)
    df["vol_regime"] = vol_ratio.apply(
        lambda r: "high" if (pd.notna(r) and r > 1.2) else "low"
    )

    # ---- Trend strength (ADX-like proxy using directional moves) -----------
    if "high" in df.columns and "low" in df.columns:
        high = df["high"]
        low = df["low"]
        prev_high = high.shift(1)
        prev_low = low.shift(1)

        dm_plus = (high - prev_high).clip(lower=0)
        dm_minus = (prev_low - low).clip(lower=0)
        # Zero out days where the other direction is stronger
        dm_plus[dm_plus <= dm_minus] = 0
        dm_minus[dm_minus <= dm_plus] = 0

        atr = _simple_atr(df)
        di_plus = 100 * dm_plus.rolling(14, min_periods=7).mean() / atr.replace(0, np.nan)
        di_minus = 100 * dm_minus.rolling(14, min_periods=7).mean() / atr.replace(0, np.nan)
        dx = 100 * (di_plus - di_minus).abs() / (di_plus + di_minus).replace(0, np.nan)
        df["adx_proxy"] = dx.rolling(14, min_periods=7).mean()
    else:
        df["adx_proxy"] = np.nan

    return df


def _simple_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Compute ATR without importing from volatility module to avoid circulars."""
    high = df["high"]
    low = df["low"]
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [(high - low), (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    return tr.ewm(com=period - 1, min_periods=period).mean()


# ---------------------------------------------------------------------------
# Multi-stock wrapper
# ---------------------------------------------------------------------------

def detect_regime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect price and volatility regimes for all stocks in a multi-stock DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain: date, stock_id, close.

    Returns
    -------
    pd.DataFrame
        Input rows with regime columns appended.
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
            enriched = detect_regime_single(group)
            results.append(enriched)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Regime detection failed for %s: %s", stock_id, exc)
            results.append(group)

    if not results:
        return df

    combined = pd.concat(results, ignore_index=True)
    combined = combined.sort_values(["stock_id", "date"]).reset_index(drop=True)
    return combined


# ---------------------------------------------------------------------------
# Market-level regime (aggregate across all stocks)
# ---------------------------------------------------------------------------

def get_market_regime(feature_df: pd.DataFrame, date: Optional[str] = None) -> dict:
    """
    Determine the overall market regime on a given date by aggregating
    individual stock regimes.

    Parameters
    ----------
    feature_df : pd.DataFrame
        Multi-stock DataFrame that already contains ``regime`` and
        ``vol_regime`` columns.
    date : str, optional
        Date to evaluate (YYYY-MM-DD).  If None, uses the latest available date.

    Returns
    -------
    dict
        Keys: regime (str), vol_regime (str), bull_pct (float), bear_pct (float)
    """
    if feature_df.empty or "regime" not in feature_df.columns:
        return {"regime": "unknown", "vol_regime": "low", "bull_pct": 0.0, "bear_pct": 0.0}

    if date is None:
        date = feature_df["date"].max()

    day_df = feature_df[feature_df["date"] == pd.Timestamp(date)]

    if day_df.empty:
        # Fall back to most recent available
        day_df = feature_df[feature_df["date"] == feature_df["date"].max()]

    total = len(day_df)
    if total == 0:
        return {"regime": "unknown", "vol_regime": "low", "bull_pct": 0.0, "bear_pct": 0.0}

    bull_pct = (day_df["regime"] == "bull").sum() / total
    bear_pct = (day_df["regime"] == "bear").sum() / total
    high_vol_pct = (day_df.get("vol_regime", pd.Series(dtype=str)) == "high").sum() / total

    if bull_pct > 0.5:
        market_regime = "bull"
    elif bear_pct > 0.5:
        market_regime = "bear"
    else:
        market_regime = "sideways"

    vol_regime = "high" if high_vol_pct > 0.4 else "low"

    return {
        "regime": market_regime,
        "vol_regime": vol_regime,
        "bull_pct": float(bull_pct),
        "bear_pct": float(bear_pct),
    }
