"""
features/short_interest_features.py - Short interest / margin short squeeze analysis.

Rules (老王教學):
- Strong stock surges + short balance increases → bears squeezed → continued strength fuel
- Limit-up + short balance up → short_squeeze_fuel_score high
- Weak stock + short increase ≠ bullish signal → mark weak_stock_short_increase
- Short covering but price cannot continue higher → short_covering_warning
- No short data → fallback gracefully, do not crash
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def compute_short_interest(
    df: pd.DataFrame,
    margin_df: pd.DataFrame = None,
) -> dict:
    """
    Analyze short interest / margin-short squeeze risk.

    Parameters
    ----------
    df : pd.DataFrame
        Daily OHLCV. Must contain: close, volume. Sorted ascending.
    margin_df : pd.DataFrame, optional
        Margin trading data.  Expected columns (any subset):
          short_balance  — outstanding short shares
          short_sell     — new short positions opened today
          short_cover    — short positions covered today
          date
        If None or empty, all outputs fallback to 0 / False.

    Returns
    -------
    dict
        short_balance_change_3d    : float | None  (positive = increase)
        short_balance_change_5d    : float | None
        price_up_short_balance_up  : bool
        limit_up_short_balance_up  : bool
        short_squeeze_fuel_score   : float  0.0–1.0
        short_covering_warning     : bool
        weak_stock_short_increase  : bool
        short_interest_signal      : str   "SQUEEZE_FUEL" | "SHORT_COVER" | "WEAK_SHORT" | "WATCH" | "UNAVAILABLE"
        short_interest_reason      : str
    """
    result = {
        "short_balance_change_3d":   None,
        "short_balance_change_5d":   None,
        "price_up_short_balance_up": False,
        "limit_up_short_balance_up": False,
        "short_squeeze_fuel_score":  0.0,
        "short_covering_warning":    False,
        "weak_stock_short_increase": False,
        "short_interest_signal":     "UNAVAILABLE",
        "short_interest_reason":     "",
    }

    # ── Check price data ─────────────────────────────────────────────────
    if df is None or len(df) < 3:
        result["short_interest_reason"] = "價格資料不足，無法分析融券"
        return result

    df = df.copy().reset_index(drop=True)
    close  = df["close"]
    last   = len(df) - 1
    c      = close.iloc[last]

    ma5  = close.rolling(5).mean().iloc[last]
    ma20 = close.rolling(20).mean().iloc[last] if len(df) >= 20 else np.nan

    # Determine if stock is strong or weak by MA position
    stock_is_strong = (not np.isnan(ma5)) and c > ma5

    # ── Check margin data ────────────────────────────────────────────────
    has_short_data = False
    sb_series = None

    if margin_df is not None and len(margin_df) > 0:
        mdf = margin_df.copy()
        if "date" in mdf.columns:
            mdf = mdf.sort_values("date").reset_index(drop=True)
        if "short_balance" in mdf.columns:
            sb_series = mdf["short_balance"].astype(float)
            has_short_data = True

    if not has_short_data:
        result["short_interest_signal"]  = "UNAVAILABLE"
        result["short_interest_reason"]  = "缺融券資料，無法分析軋空風險"
        return result

    # ── Short balance changes ────────────────────────────────────────────
    if len(sb_series) >= 4:
        sb_last = sb_series.iloc[-1]
        sb_3ago = sb_series.iloc[-4]
        result["short_balance_change_3d"] = round(
            (sb_last - sb_3ago) / max(abs(sb_3ago), 1), 4
        )
    if len(sb_series) >= 6:
        sb_last = sb_series.iloc[-1]
        sb_5ago = sb_series.iloc[-6]
        result["short_balance_change_5d"] = round(
            (sb_last - sb_5ago) / max(abs(sb_5ago), 1), 4
        )

    sb_change_3d = result["short_balance_change_3d"] or 0.0

    # ── Price-up + short-balance-up (squeeze fuel) ───────────────────────
    price_3d_pct = 0.0
    if last >= 3:
        price_3d_pct = (c - close.iloc[last - 3]) / close.iloc[last - 3] if close.iloc[last - 3] > 0 else 0.0

    price_up   = price_3d_pct > 0.02
    short_up   = sb_change_3d > 0.05   # short balance grew > 5%

    result["price_up_short_balance_up"] = price_up and short_up

    # ── Limit-up check (approximation: daily gain >= 9.5%) ───────────────
    daily_gain = 0.0
    if last >= 1 and close.iloc[last - 1] > 0:
        daily_gain = (c - close.iloc[last - 1]) / close.iloc[last - 1]
    near_limit_up = daily_gain >= 0.095

    result["limit_up_short_balance_up"] = near_limit_up and short_up

    # ── Short squeeze fuel score ─────────────────────────────────────────
    score = 0.0
    if stock_is_strong:
        if price_up and short_up:
            score += 0.5
        if near_limit_up and short_up:
            score += 0.4
        if sb_change_3d > 0.15:    # aggressive short build
            score += 0.2
    score = min(1.0, score)
    result["short_squeeze_fuel_score"] = round(score, 3)

    # ── Short covering warning ────────────────────────────────────────────
    # Short balance decreased (covering) but price didn't surge
    sb_declining = sb_change_3d < -0.05
    price_flat   = abs(price_3d_pct) < 0.02
    if sb_declining and price_flat:
        result["short_covering_warning"] = True

    # ── Weak stock + short increase (not bullish) ─────────────────────────
    if not stock_is_strong and short_up:
        result["weak_stock_short_increase"] = True

    # ── Signal and reason ─────────────────────────────────────────────────
    reasons = []
    signal  = "WATCH"

    if result["weak_stock_short_increase"]:
        signal = "WEAK_SHORT"
        reasons.append("弱勢股融券增加，不視為多方訊號")
    elif result["short_covering_warning"]:
        signal = "SHORT_COVER"
        reasons.append("融券回補但股價無法續強，追漲需謹慎")
    elif score >= 0.4:
        signal = "SQUEEZE_FUEL"
        if near_limit_up:
            reasons.append("漲停附近 + 融券增加，軋空燃料強")
        else:
            reasons.append("強勢股大漲 + 融券增加，可能散戶放空被軋，續強燃料")
    else:
        reasons.append(
            f"融券無明確訊號 (3日變化 {sb_change_3d:+.1%})"
        )

    result["short_interest_signal"]  = signal
    result["short_interest_reason"]  = "；".join(reasons)
    return result
