"""
features/indicators.py - Core technical indicators.

All calculations use pure pandas/numpy – no TA-Lib dependency.
Each function operates on a single-stock OHLCV DataFrame and returns
additional columns.  The main entry point ``compute_indicators`` accepts a
multi-stock DataFrame grouped by ``stock_id``.
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

# Lazy imports to avoid circular dependency errors when individual modules
# are run standalone.  Failures are caught and logged so the main indicator
# pipeline continues even if volume_profile or microstructure imports fail.
def _import_volume_profile():
    try:
        from features.volume_profile import compute_volume_profile
        return compute_volume_profile
    except Exception as exc:
        logger.warning("Could not import volume_profile: %s", exc)
        return None

def _import_microstructure():
    try:
        from features.microstructure import compute_microstructure
        return compute_microstructure
    except Exception as exc:
        logger.warning("Could not import microstructure: %s", exc)
        return None


def _import_kd_advanced():
    try:
        from features.kd_advanced import compute_kd_advanced
        return compute_kd_advanced
    except Exception as exc:
        logger.warning("Could not import kd_advanced: %s", exc)
        return None


def _import_short_interest():
    try:
        from features.short_interest_features import compute_short_interest
        return compute_short_interest
    except Exception as exc:
        logger.warning("Could not import short_interest_features: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Single-series helpers
# ---------------------------------------------------------------------------

def _rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Compute Relative Strength Index for a price series."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def _macd(
    series: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> tuple:
    """
    Compute MACD line, signal line, and histogram.

    Returns
    -------
    tuple of (macd_line, signal_line, histogram) pd.Series
    """
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def _sma(series: pd.Series, period: int) -> pd.Series:
    """Simple moving average."""
    return series.rolling(window=period, min_periods=max(1, period // 2)).mean()


def _ema(series: pd.Series, span: int) -> pd.Series:
    """Exponential moving average."""
    return series.ewm(span=span, adjust=False).mean()


def _volume_spike(volume: pd.Series, period: int = 20) -> pd.Series:
    """Volume relative to its N-day simple moving average (ratio)."""
    avg_vol = volume.rolling(window=period, min_periods=max(1, period // 2)).mean()
    return volume / avg_vol.replace(0, np.nan)


def _bollinger_bands(
    series: pd.Series, period: int = 20, num_std: float = 2.0
) -> tuple:
    """
    Compute Bollinger Bands.

    Returns
    -------
    tuple of (upper_band, middle_band, lower_band, bandwidth) pd.Series
    """
    middle = series.rolling(window=period, min_periods=max(1, period // 2)).mean()
    std = series.rolling(window=period, min_periods=max(1, period // 2)).std()
    upper = middle + num_std * std
    lower = middle - num_std * std
    bandwidth = (upper - lower) / middle.replace(0, np.nan)
    return upper, middle, lower, bandwidth


# ---------------------------------------------------------------------------
# Per-stock indicator computation
# ---------------------------------------------------------------------------

def compute_indicators_single(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute all technical indicators for a single stock's OHLCV DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: date, open, high, low, close, volume.
        Rows should be sorted by date ascending.

    Returns
    -------
    pd.DataFrame
        Original columns plus all indicator columns.
    """
    if df.empty or "close" not in df.columns:
        return df

    df = df.sort_values("date").copy()
    close = df["close"]
    volume = df["volume"]

    # ---- RSI ---------------------------------------------------------------
    df["rsi_14"] = _rsi(close, period=config.RSI_PERIOD)

    # ---- MACD --------------------------------------------------------------
    macd_line, signal_line, histogram = _macd(
        close,
        fast=config.MACD_FAST,
        slow=config.MACD_SLOW,
        signal=config.MACD_SIGNAL,
    )
    df["macd"] = macd_line
    df["macd_signal"] = signal_line
    df["macd_hist"] = histogram

    # ---- Simple Moving Averages --------------------------------------------
    for period in config.SMA_PERIODS:
        df[f"sma_{period}"] = _sma(close, period)

    # ---- Exponential Moving Averages ---------------------------------------
    for span in config.EMA_PERIODS:
        df[f"ema_{span}"] = _ema(close, span)

    # ---- Volume spike ------------------------------------------------------
    df["volume_spike"] = _volume_spike(volume, period=20)

    # ---- Bollinger Bands ---------------------------------------------------
    bb_upper, bb_mid, bb_lower, bb_width = _bollinger_bands(
        close, period=config.BB_PERIOD, num_std=config.BB_STD
    )
    df["bb_upper"] = bb_upper
    df["bb_middle"] = bb_mid
    df["bb_lower"] = bb_lower
    df["bb_width"] = bb_width

    # Price position within Bollinger Bands: (close - lower) / (upper - lower)
    band_range = (bb_upper - bb_lower).replace(0, np.nan)
    df["bb_position"] = (close - bb_lower) / band_range

    # ---- Price vs MAs (binary signals) -------------------------------------
    df["price_above_sma20"] = (close > df["sma_20"]).astype(int)
    df["price_above_sma60"] = (close > df["sma_60"]).astype(int)
    df["sma20_above_sma60"] = (df["sma_20"] > df["sma_60"]).astype(int)

    # ---- KD Advanced (v0.3.6 Phase 2) — append last-row scalar values ----
    kd_fn = _import_kd_advanced()
    if kd_fn is not None:
        try:
            kd_res = kd_fn(df)
            # Only store scalar signals on the last row; pad NaN for earlier rows
            import numpy as _np
            for col, val in [
                ("kd_k",                kd_res.get("kd_k")),
                ("kd_d",                kd_res.get("kd_d")),
                ("kd_low_golden_cross", int(kd_res.get("kd_low_golden_cross", False))),
                ("kd_high_death_cross", int(kd_res.get("kd_high_death_cross", False))),
                ("kd_mid_noise_cross",  int(kd_res.get("kd_mid_noise_cross",  False))),
                ("kd_high_sticky_days", kd_res.get("kd_high_sticky_days", 0)),
            ]:
                if col not in df.columns:
                    df[col] = _np.nan
                    df.loc[df.index[-1], col] = val
        except Exception as exc:
            logger.debug("kd_advanced single-row annotation skipped: %s", exc)

    return df


# ---------------------------------------------------------------------------
# Multi-stock wrapper
# ---------------------------------------------------------------------------

def compute_indicators(
    df: pd.DataFrame,
    intraday_df: Optional[pd.DataFrame] = None,
    include_volume_profile: bool = True,
    include_microstructure: bool = True,
) -> pd.DataFrame:
    """
    Compute technical indicators for all stocks in a multi-stock DataFrame.

    Also optionally computes Volume Profile (分價量) and Market Microstructure
    (盤口微觀) features.  If the required columns or modules are unavailable,
    those feature groups are silently skipped — the core RSI/MACD/MA/volume
    features are never affected.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: date, stock_id, open, high, low, close, volume.
    intraday_df : pd.DataFrame, optional
        Per-minute or tick data for microstructure opening features.
        When None, daily OHLCV proxies are used.
    include_volume_profile : bool
        Whether to compute Volume Profile features (default True).
    include_microstructure : bool
        Whether to compute Microstructure features (default True).

    Returns
    -------
    pd.DataFrame
        Same rows with all indicator columns appended.
        Rows with insufficient history retain NaN values for long-period
        indicators.
    """
    if df.empty:
        logger.warning("compute_indicators received empty DataFrame.")
        return df

    required = {"date", "stock_id", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame missing required columns: {missing}")

    # ---- Core technical indicators (per-stock) ------------------------------
    results = []
    for stock_id, group in df.groupby("stock_id"):
        try:
            enriched = compute_indicators_single(group)
            results.append(enriched)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Failed to compute indicators for %s: %s", stock_id, exc)
            results.append(group)

    if not results:
        return df

    combined = pd.concat(results, ignore_index=True)
    combined = combined.sort_values(["stock_id", "date"]).reset_index(drop=True)

    # ---- Volume Profile (分價量) -------------------------------------------
    if include_volume_profile:
        vp_fn = _import_volume_profile()
        if vp_fn is not None:
            has_ohlcv = {"high", "low"}.issubset(combined.columns)
            if has_ohlcv:
                try:
                    combined = vp_fn(combined)
                    logger.debug("Volume profile features computed.")
                except Exception as exc:
                    logger.warning("Volume profile computation failed: %s", exc)
            else:
                logger.debug("Skipping volume profile: high/low columns missing.")

    # ---- Market Microstructure (盤口微觀) -----------------------------------
    if include_microstructure:
        ms_fn = _import_microstructure()
        if ms_fn is not None:
            has_open = "open" in combined.columns
            if has_open:
                try:
                    combined = ms_fn(combined, intraday_df=intraday_df)
                    logger.debug("Microstructure features computed.")
                except Exception as exc:
                    logger.warning("Microstructure computation failed: %s", exc)
            else:
                logger.debug("Skipping microstructure: open column missing.")

    return combined
