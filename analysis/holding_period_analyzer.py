"""
analysis/holding_period_analyzer.py - Holding period mode and trailing MA selection.

Based on:
  20201119 短線與波段操作的依據
  20201105 大波段不只看 X 日均線

Covers Spec B (short-term vs swing) and Spec H (big swing MA rules).
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Holding mode constants
SHORT_TERM  = "SHORT_TERM"
SWING       = "SWING"
TRUST_TREND = "TRUST_TREND"
UNKNOWN     = "UNKNOWN"

# Trend stage constants
CONSOLIDATING  = "CONSOLIDATING"
BREAKOUT       = "BREAKOUT"
TRUST_BREAKOUT = "TRUST_BREAKOUT"


def analyze_holding_period(
    df: pd.DataFrame,
    entry_price: float = None,
    half_profit_taken: bool = False,
    institution_buying: bool = False,
    trend_stage: str = None,
) -> dict:
    """
    Determine the appropriate holding period mode and trailing MA rule.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain: close (and optionally volume). Sorted ascending.
    entry_price : float, optional
        Average entry / cost basis per share.
    half_profit_taken : bool
        True if the first half of the position was already sold at profit.
    institution_buying : bool
        True if 投信 (trust / fund) has been consistently buying (明顯買超).
    trend_stage : str, optional
        Explicit stage override: "CONSOLIDATING" | "BREAKOUT" | "TRUST_BREAKOUT".
        If None, the function infers from MA relationships.

    Returns
    -------
    dict
        holding_mode                   : str  SHORT_TERM | SWING | TRUST_TREND | UNKNOWN
        primary_trailing_ma            : int  (5, 10, or 20)
        secondary_trailing_ma          : int
        can_hold_for_swing             : bool
        swing_risk_reason              : str
        short_term_exit_reason         : str
        trailing_ma_rule               : str  human-readable description
        trend_stage                    : str
        do_not_sell_at_support_reason  : str
        institution_trailing_reason    : str
    """
    result = {
        "holding_mode":                  UNKNOWN,
        "primary_trailing_ma":           5,
        "secondary_trailing_ma":         20,
        "can_hold_for_swing":            False,
        "swing_risk_reason":             "",
        "short_term_exit_reason":        "",
        "trailing_ma_rule":              "",
        "trend_stage":                   trend_stage or UNKNOWN,
        "do_not_sell_at_support_reason": "",
        "institution_trailing_reason":   "",
    }

    if df is None or len(df) < 5:
        result["trailing_ma_rule"] = "資料不足，無法判斷持股模式"
        return result

    df    = df.copy().reset_index(drop=True)
    close = df["close"]
    last  = len(df) - 1
    c     = close.iloc[last]

    ma5  = close.rolling(5).mean().iloc[last]
    ma10 = close.rolling(10).mean().iloc[last]  if len(df) >= 10  else np.nan
    ma20 = close.rolling(20).mean().iloc[last]  if len(df) >= 20  else np.nan

    # ── Infer trend_stage if not supplied ─────────────────────────────────
    if trend_stage is None:
        if not np.isnan(ma20):
            above_all = (c > ma5 and
                         (np.isnan(ma10) or c > ma10) and
                         c > ma20)
            if above_all and institution_buying:
                trend_stage = TRUST_BREAKOUT
            elif above_all:
                trend_stage = BREAKOUT
            else:
                trend_stage = CONSOLIDATING
        else:
            trend_stage = UNKNOWN
    result["trend_stage"] = trend_stage

    # ── 4. trend_stage_filter → mode & trailing MA (Spec H) ──────────────
    if trend_stage == CONSOLIDATING:
        # Not yet broken out: use MA20 as swing support
        result["holding_mode"]           = SWING
        result["primary_trailing_ma"]    = 20
        result["secondary_trailing_ma"]  = 20
        result["trailing_ma_rule"] = (
            "盤整未噴出 → 以 MA20 / 月均線作波段支撐；"
            "回測 MA20 不破可觀察，不宜用 MA5/MA10 亂砍"
        )
        result["do_not_sell_at_support_reason"] = (
            "股票尚未大漲，盤整期間不能用 MA10 亂賣，"
            "未噴出前應以 MA20 / 月均線作為波段基準"
        )

    elif trend_stage == BREAKOUT:
        # Post-breakout short-term strong stock → MA5
        result["holding_mode"]           = SHORT_TERM
        result["primary_trailing_ma"]    = 5
        result["secondary_trailing_ma"]  = 20
        result["trailing_ma_rule"] = (
            "噴出後短線強勢 → 追蹤 MA5；"
            "跌破 MA5 出場；已賣一半後改追 MA20"
        )

    elif trend_stage == TRUST_BREAKOUT:
        # 投信 buy surge → MA10
        result["holding_mode"]           = TRUST_TREND
        result["primary_trailing_ma"]    = 10
        result["secondary_trailing_ma"]  = 20
        result["trailing_ma_rule"] = (
            "投信買超噴出 → 追蹤 MA10；"
            "若 MA5 / MA10 很接近，跌破 MA5 不急砍，避免砍在 MA10 支撐；"
            "若投信轉賣且跌破 MA10 → 出場"
        )
        result["institution_trailing_reason"] = (
            "投信持續買超，改追 MA10 作為主要支撐；"
            "跌破 MA10 且投信轉賣 → 轉弱警訊，應出場"
        )

    # ── half_profit_taken override (Spec B: swing mode after first sale) ──
    if half_profit_taken:
        result["holding_mode"]           = SWING
        result["primary_trailing_ma"]    = 20
        result["secondary_trailing_ma"]  = 20
        result["trailing_ma_rule"] = (
            "已賣一半獲利 → 剩餘持股改追 MA20 做波段；"
            "接受震盪，不用短線心態亂砍"
        )

    mode = result["holding_mode"]

    # ── short_term_mode exit check ────────────────────────────────────────
    if mode == SHORT_TERM:
        reasons = []
        if not np.isnan(ma5) and c < ma5:
            reasons.append(f"跌破 MA5 ({ma5:.2f}) → 出場")
        result["short_term_exit_reason"] = (
            "; ".join(reasons) if reasons else "持股中，持續追蹤 MA5"
        )

    # ── swing_mode risk check ─────────────────────────────────────────────
    if mode == SWING and entry_price and entry_price > 0 and not np.isnan(ma20):
        ma20_to_cost = (ma20 - entry_price) / entry_price
        if ma20_to_cost < -0.05:
            result["can_hold_for_swing"] = False
            result["swing_risk_reason"] = (
                f"MA20 ({ma20:.2f}) 距成本 {ma20_to_cost*100:.1f}%，"
                "跌到 MA20 整體交易從小賺變虧損，不建議硬做波段"
            )
        else:
            result["can_hold_for_swing"] = True
            result["swing_risk_reason"] = (
                f"MA20 ({ma20:.2f}) 支撐在可接受範圍 ({ma20_to_cost*100:.1f}% 距成本)，"
                "可嘗試波段操作"
            )
    elif mode == SWING:
        result["can_hold_for_swing"] = not np.isnan(ma20)

    # ── TRUST_TREND: detect MA5/MA10 convergence ─────────────────────────
    if mode == TRUST_TREND and not np.isnan(ma5) and not np.isnan(ma10) and entry_price and entry_price > 0:
        diff_pct = abs(ma5 - ma10) / entry_price
        if diff_pct < 0.02:
            result["institution_trailing_reason"] += (
                "；MA5 與 MA10 非常靠近，跌破 MA5 不急砍，避免砍在 MA10 支撐"
            )

    return result
