"""
analysis/exit_point_analyzer.py - Short-term sell-high and re-entry analyzer.

Based on: 20201028 如何短線賣高點回檔不急著買

Covers Spec G: previous high exit, failed breakout, chip-linked exit,
and pullback re-entry conditions.
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def analyze_exit_point(
    df: pd.DataFrame,
    entry_price: float = None,
    take_profit_price: float = None,
    previous_high: float = None,
    institution_type: str = "none",
    institution_net: float = 0.0,
    half_sold: bool = False,
) -> dict:
    """
    Determine exit signals, chip-linked sell conditions, and re-entry criteria.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain: close, open, high, low, volume. Sorted ascending by date.
    entry_price : float, optional
        Average cost basis.
    take_profit_price : float, optional
        Pre-computed take-profit target (from position_sizing or manual input).
    previous_high : float, optional
        Most recent significant high acting as resistance.
        If None, computed as the rolling max over the last 20 bars.
    institution_type : str
        Institutional driver for this stock:
        "foreign" (外資) | "trust" (投信) | "none".
    institution_net : float
        Today's institutional net buy volume (positive = buy, negative = sell).
    half_sold : bool
        True if the first half of the position was already sold.

    Returns
    -------
    dict
        relative_high_exit_signal  : bool
        failed_breakout_exit_signal: bool
        chip_linked_exit_reason    : str
        pullback_rebuy_condition   : str
        do_not_rebuy_yet_reason    : str
    """
    result = {
        "relative_high_exit_signal":   False,
        "failed_breakout_exit_signal": False,
        "chip_linked_exit_reason":     "",
        "pullback_rebuy_condition":    "",
        "do_not_rebuy_yet_reason":     "",
    }

    if df is None or len(df) < 3:
        return result

    df = df.copy().reset_index(drop=True)
    close  = df["close"]
    high   = df["high"]   if "high"   in df.columns else close
    low    = df["low"]    if "low"    in df.columns else close
    volume = df["volume"] if "volume" in df.columns else pd.Series([0] * len(df))

    last = len(df) - 1
    c    = close.iloc[last]
    h    = high.iloc[last]
    o    = df["open"].iloc[last] if "open" in df.columns else c

    ma5  = close.rolling(5).mean().iloc[last]
    ma10 = close.rolling(10).mean().iloc[last]  if len(df) >= 10 else np.nan
    ma20 = close.rolling(20).mean().iloc[last]  if len(df) >= 20 else np.nan

    # Auto-detect previous high from last 20 bars if not supplied
    if previous_high is None and len(df) >= 5:
        lookback = min(20, len(df))
        previous_high = high.iloc[-lookback:].max()

    # ── 1. previous_high_pressure_exit ───────────────────────────────────
    at_prev_high   = bool(previous_high and h >= previous_high * 0.99)
    at_take_profit = bool(take_profit_price and c >= take_profit_price * 0.99)
    if at_prev_high or at_take_profit:
        result["relative_high_exit_signal"] = True

    # ── 2. failed_breakout_exit ───────────────────────────────────────────
    prev_close = close.iloc[last - 1] if last >= 1 else c
    # "Opened low next day after touching resistance" proxy:
    opened_low_after_touch = (
        at_prev_high
        and prev_close >= (previous_high or 0) * 0.97
        and o < prev_close * 0.99
    )
    institution_selling_hard = institution_net < -1_000
    if (at_prev_high and opened_low_after_touch) or (at_prev_high and institution_selling_hard):
        result["failed_breakout_exit_signal"] = True

    # ── 3. chip_linked_exit ───────────────────────────────────────────────
    if institution_type == "foreign":
        if institution_net < -1_000:
            result["chip_linked_exit_reason"] = (
                "外資大賣 → 該股習慣跟外資，短線轉弱，考慮出場或降低持股"
            )
        else:
            result["chip_linked_exit_reason"] = "外資未大賣，持股觀察中"

    elif institution_type == "trust":
        if institution_net > 0:
            result["chip_linked_exit_reason"] = (
                "投信仍買超 → 不急著賣；"
                "若跌破 MA5 但 MA10 很近，不急砍避免砍在 MA10 支撐"
            )
        elif institution_net < -1_000:
            result["chip_linked_exit_reason"] = (
                "投信轉賣 → 若同時跌破 MA10，應出場；轉弱警訊提高"
            )
        else:
            result["chip_linked_exit_reason"] = "投信中性，按均線停利規則操作"

    else:
        result["chip_linked_exit_reason"] = "無主力慣性偏好，按均線 / 前高規則操作"

    # ── 4. pullback_not_rebuy_yet ─────────────────────────────────────────
    if half_sold or result["relative_high_exit_signal"]:
        conds = []
        if not np.isnan(ma5):
            conds.append(f"回測 MA5 ({ma5:.2f}) 不破後站穩")
        if not np.isnan(ma10):
            conds.append(f"回測 MA10 ({ma10:.2f}) 不破後站穩")
        if not np.isnan(ma20):
            conds.append(f"回測 MA20 ({ma20:.2f}) 不破後站穩")
        if previous_high:
            conds.append(f"重新站上前高 ({previous_high:.2f})")
        result["pullback_rebuy_condition"] = (
            " / ".join(conds) if conds else "等待明確支撐確認後再買回"
        )

        vol_ma5 = volume.rolling(5).mean().iloc[last]
        vol_shrinking = (
            volume.iloc[last] < vol_ma5 * 0.8
            if (not np.isnan(vol_ma5) and vol_ma5 > 0) else False
        )
        reasons = ["短線賣高點後，不因第一天回檔就急著買回"]
        if vol_shrinking:
            reasons.append("量縮中，尚未形成有效支撐")
        result["do_not_rebuy_yet_reason"] = "；".join(reasons)

    return result
