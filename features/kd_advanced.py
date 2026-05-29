"""
features/kd_advanced.py - Advanced KD (Stochastic) strategy signals.

Rules (老王教學):
- Golden cross below 20: stronger buy signal
- Death cross above 80: stronger sell signal
- Mid-range (20-80) crossovers: noise, do not over-weight
- Sticky high (KD >= 80 for multiple bars): overbought but strong trend
- Divergence: warning only, not standalone buy/sell signal
- No look-ahead: only uses past data
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _stochastic_k(high: pd.Series, low: pd.Series, close: pd.Series,
                  period: int = 9) -> pd.Series:
    """Raw %K stochastic."""
    lowest  = low.rolling(period, min_periods=1).min()
    highest = high.rolling(period, min_periods=1).max()
    denom = (highest - lowest).replace(0, np.nan)
    return (close - lowest) / denom * 100.0


def _smooth(series: pd.Series, n: int = 3) -> pd.Series:
    return series.ewm(com=n - 1, min_periods=1).mean()


def compute_kd_advanced(df: pd.DataFrame) -> dict:
    """
    Compute advanced KD signals.

    Accepts a DataFrame that may already contain 'k' / 'd' columns (from XQ
    or other importers), or falls back to computing stochastic from
    high / low / close.

    Parameters
    ----------
    df : pd.DataFrame
        Sorted ascending. Must contain at least 'close'. 'high' and 'low' are
        used for stochastic calculation if 'k'/'d' are absent.

    Returns
    -------
    dict
        kd_k                  : float  last K value
        kd_d                  : float  last D value
        kd_low_golden_cross   : bool   golden cross when both K & D < 25
        kd_high_death_cross   : bool   death cross when both K & D > 75
        kd_mid_noise_cross    : bool   crossover in 25-75 — unreliable
        kd_high_sticky_days   : int    consecutive days with K >= 80
        kd_high_sticky_trend  : bool   K >= 80 for >= 3 days → strong trend
        kd_bullish_divergence  : bool   price lower-low but K higher-low
        kd_bearish_divergence  : bool   price higher-high but K lower-high
        kd_signal             : str   "BUY" | "SELL" | "STICKY_BULL" | "NOISE" | "WATCH"
        kd_strategy_reason    : str   human-readable
    """
    result = {
        "kd_k":                  None,
        "kd_d":                  None,
        "kd_low_golden_cross":   False,
        "kd_high_death_cross":   False,
        "kd_mid_noise_cross":    False,
        "kd_high_sticky_days":   0,
        "kd_high_sticky_trend":  False,
        "kd_bullish_divergence":  False,
        "kd_bearish_divergence":  False,
        "kd_signal":             "WATCH",
        "kd_strategy_reason":    "",
    }

    if df is None or len(df) < 9:
        result["kd_strategy_reason"] = "資料不足 (<9 bars)，無法計算 KD"
        return result

    df = df.copy().reset_index(drop=True)

    # ── Use existing K/D columns or compute from scratch ─────────────────
    if "k" in df.columns and "d" in df.columns:
        k_series = df["k"].astype(float)
        d_series = df["d"].astype(float)
    elif {"high", "low", "close"}.issubset(df.columns):
        raw_k    = _stochastic_k(df["high"], df["low"], df["close"], period=9)
        k_series = _smooth(raw_k, 3)
        d_series = _smooth(k_series, 3)
    elif "close" in df.columns:
        # Fallback: use close as both high and low (degenerate but non-crashing)
        raw_k    = _stochastic_k(df["close"], df["close"], df["close"], period=9)
        k_series = _smooth(raw_k, 3)
        d_series = _smooth(k_series, 3)
        result["kd_strategy_reason"] = "缺 high/low，KD 由 close 估算，精度降低"
    else:
        result["kd_strategy_reason"] = "資料缺 close，無法計算 KD"
        return result

    last  = len(df) - 1
    k_now = k_series.iloc[last]
    d_now = d_series.iloc[last]
    k_prev = k_series.iloc[last - 1] if last >= 1 else k_now
    d_prev = d_series.iloc[last - 1] if last >= 1 else d_now

    result["kd_k"] = round(float(k_now), 2)
    result["kd_d"] = round(float(d_now), 2)

    if np.isnan(k_now) or np.isnan(d_now):
        result["kd_strategy_reason"] = "KD 值為 NaN，資料不足"
        return result

    # ── Cross detection ──────────────────────────────────────────────────
    golden = (k_prev < d_prev) and (k_now > d_now)   # K crosses above D
    death  = (k_prev > d_prev) and (k_now < d_now)   # K crosses below D

    LOW_ZONE  = 25.0
    HIGH_ZONE = 75.0

    if golden:
        if k_now < LOW_ZONE and d_now < LOW_ZONE:
            result["kd_low_golden_cross"] = True
        elif LOW_ZONE <= k_now <= HIGH_ZONE:
            result["kd_mid_noise_cross"] = True

    if death:
        if k_now > HIGH_ZONE and d_now > HIGH_ZONE:
            result["kd_high_death_cross"] = True
        elif LOW_ZONE <= k_now <= HIGH_ZONE:
            result["kd_mid_noise_cross"] = True

    # ── High sticky (overbought persistence) ────────────────────────────
    sticky_days = 0
    for i in range(last, max(-1, last - 20), -1):
        if k_series.iloc[i] >= 80:
            sticky_days += 1
        else:
            break
    result["kd_high_sticky_days"]  = sticky_days
    result["kd_high_sticky_trend"] = sticky_days >= 3

    # ── Divergence (only use past data, no look-ahead) ───────────────────
    # Bullish divergence: price makes lower low but K makes higher low
    # Only look at last 20 bars
    if last >= 10 and "close" in df.columns:
        window = 20
        start  = max(0, last - window)
        c_slice = df["close"].iloc[start: last + 1]
        k_slice = k_series.iloc[start: last + 1]

        c_min_prev_idx = c_slice.iloc[:-1].idxmin()
        k_min_prev_idx = k_slice.iloc[:-1].idxmin()

        c_prev_low = c_slice.loc[c_min_prev_idx]
        k_prev_low = k_slice.loc[k_min_prev_idx]

        if c_slice.iloc[-1] < c_prev_low and k_slice.iloc[-1] > k_prev_low:
            result["kd_bullish_divergence"] = True

        c_max_prev_idx = c_slice.iloc[:-1].idxmax()
        k_max_prev_idx = k_slice.iloc[:-1].idxmax()

        c_prev_high = c_slice.loc[c_max_prev_idx]
        k_prev_high = k_slice.loc[k_max_prev_idx]

        if c_slice.iloc[-1] > c_prev_high and k_slice.iloc[-1] < k_prev_high:
            result["kd_bearish_divergence"] = True

    # ── Signal and reason ────────────────────────────────────────────────
    reasons = []
    signal  = "WATCH"

    if result["kd_low_golden_cross"]:
        signal = "BUY"
        reasons.append(f"低檔黃金交叉 (K={k_now:.0f}/D={d_now:.0f})，有效低檔買進訊號")
    elif result["kd_high_death_cross"]:
        signal = "SELL"
        reasons.append(f"高檔死亡交叉 (K={k_now:.0f}/D={d_now:.0f})，有效高檔賣出訊號")
    elif result["kd_high_sticky_trend"]:
        signal = "STICKY_BULL"
        reasons.append(f"KD 高檔鈍化 {sticky_days} 日，強勢股不因一次高檔交叉就立刻賣")
    elif result["kd_mid_noise_cross"]:
        signal = "NOISE"
        reasons.append(f"中間區域交叉 (K={k_now:.0f}/D={d_now:.0f})，視為雜訊，不加分")

    if result["kd_bullish_divergence"]:
        reasons.append("KD 低背離（警示）— 不可單獨當買進訊號")
    if result["kd_bearish_divergence"]:
        reasons.append("KD 高背離（警示）— 不可單獨當賣出訊號")

    if not reasons:
        reasons.append(f"KD 無明確訊號 (K={k_now:.0f}/D={d_now:.0f})")

    result["kd_signal"]          = signal
    result["kd_strategy_reason"] = "；".join(reasons)
    return result
