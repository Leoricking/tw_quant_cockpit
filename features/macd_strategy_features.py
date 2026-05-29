"""
features/macd_strategy_features.py - MACD strategy signal engine.

Based on:
  20220504 MACD 關鍵買進訊號這樣用
  20220518 MACD 出現這狀況要小心

Covers:
  D. MACD 多頭回檔買點 (bull trend pullback buy)
  E. MACD 空頭反彈結束警示 (bear rebound end warning)
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Trend constants
BULL    = "BULL"
BEAR    = "BEAR"
NEUTRAL = "NEUTRAL"

# Rebound status
REBOUNDING     = "REBOUNDING"
REBOUND_ENDING = "REBOUND_ENDING"
OBSERVE        = "OBSERVE"
NONE_STATUS    = "NONE"


def _macd_series(
    close: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> tuple:
    """Return (macd_line, signal_line, histogram) Series."""
    ema_fast   = close.ewm(span=fast,   adjust=False).mean()
    ema_slow   = close.ewm(span=slow,   adjust=False).mean()
    macd_line  = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram  = macd_line - signal_line
    return macd_line, signal_line, histogram


def compute_macd_strategy(df: pd.DataFrame) -> dict:
    """
    Compute MACD strategy signals for bull pullback buy and bear rebound end.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain column: close.  Sorted ascending by date.
        >= 30 rows recommended for reliable MACD.

    Returns
    -------
    dict
        macd_trend_context       : str   "BULL" | "BEAR" | "NEUTRAL"
        macd_bull_pullback_buy   : bool  Full confirmed bull pullback buy signal.
        macd_wait_confirm        : bool  Price above MA20 but histogram still green.
        macd_fake_reclaim_warning: bool  Price above MA20 but MACD not yet turned.
        macd_buy_reason          : str   Human-readable buy rationale.
        macd_bear_rebound        : bool  Bear-trend rebound above MA20 with red histogram.
        macd_rebound_end_warning : bool  Histogram flipped green while below MA20.
        macd_rebound_status      : str   "REBOUNDING" | "REBOUND_ENDING" | "OBSERVE" | "NONE"
        macd_sell_or_avoid_reason: str   Human-readable sell/avoid rationale.
    """
    result = {
        "macd_trend_context":        NEUTRAL,
        "macd_bull_pullback_buy":    False,
        "macd_wait_confirm":         False,
        "macd_fake_reclaim_warning": False,
        "macd_buy_reason":           "",
        "macd_bear_rebound":         False,
        "macd_rebound_end_warning":  False,
        "macd_rebound_status":       NONE_STATUS,
        "macd_sell_or_avoid_reason": "",
    }

    if df is None or len(df) < 30:
        result["macd_buy_reason"] = "資料不足 (<30 bars)，無法計算 MACD"
        return result

    df   = df.copy().reset_index(drop=True)
    close = df["close"]

    ma20 = close.rolling(20).mean()
    ma60 = close.rolling(60).mean() if len(df) >= 60 else pd.Series(
        [np.nan] * len(df), index=df.index)

    _, _, histogram = _macd_series(close)

    last = len(df) - 1
    c    = close.iloc[last]
    m20  = ma20.iloc[last]
    m60  = ma60.iloc[last]

    hist_last = histogram.iloc[last]
    hist_prev = histogram.iloc[last - 1] if last >= 1 else np.nan

    # ── 1. trend_context ─────────────────────────────────────────────────────
    if not np.isnan(m60):
        if c > m20 and c > m60:
            trend = BULL
        elif c < m20 and c < m60:
            trend = BEAR
        else:
            trend = NEUTRAL
    else:
        # Fallback: MA20 only
        trend = BULL if c > m20 else (BEAR if c < m20 else NEUTRAL)
    result["macd_trend_context"] = trend

    # Histogram sign flags (TW convention: positive hist = red bar)
    hist_is_red    = hist_last > 0
    hist_is_green  = hist_last < 0
    hist_prev_green = hist_prev < 0
    hist_turned_red = hist_prev_green and hist_is_red   # green → red crossover

    # ── 2. Bull pullback buy signals (Spec D) ────────────────────────────────
    if trend == BULL and not np.isnan(m20):
        # Did price touch near MA20 within last 5 bars?
        recent_low    = close.iloc[max(0, last - 5): last + 1].min()
        touched_ma20  = recent_low <= m20 * 1.02

        if touched_ma20 and hist_turned_red and c >= m20:
            # Full confirmation: pullback to MA20 + histogram flipped red + price back above MA20
            result["macd_bull_pullback_buy"] = True
            result["macd_buy_reason"] = (
                "多頭回測 MA20 + MACD 柱由綠翻紅 + 股價站回 MA20 — 確認多頭回檔買點"
            )
        elif touched_ma20 and hist_is_green and c >= m20:
            # Price reclaimed MA20 but histogram still green
            result["macd_wait_confirm"] = True
            result["macd_buy_reason"] = (
                "股價站上 MA20 但 MACD 柱仍綠 — 等待 MACD 翻紅確認 (WAIT_MACD_CONFIRM)"
            )
        elif c >= m20 and hist_is_green:
            # Price above MA20 but MACD didn't confirm — fake reclaim risk
            result["macd_fake_reclaim_warning"] = True
            result["macd_buy_reason"] = (
                "股價站上 MA20 但 MACD 未翻紅 — 假站回 / 騙線風險，不急著追買"
            )

    # ── 3. Bear rebound signals (Spec E) ─────────────────────────────────────
    if trend == BEAR and not np.isnan(m20):
        recent_high   = close.iloc[max(0, last - 5): last + 1].max()
        bounced_above = recent_high >= m20 * 0.98

        hist_turned_green = (hist_prev > 0) and hist_is_green  # red → green crossover

        # 3a. Bear rebound: price bounced above MA20, histogram turned red (short-lived recovery)
        if bounced_above and hist_is_red:
            result["macd_bear_rebound"] = True
            result["macd_rebound_status"] = REBOUNDING
            result["macd_sell_or_avoid_reason"] = (
                "空頭趨勢中反彈站上 MA20 + MACD 翻紅 — 只是反彈，非長線翻多，不可重押"
            )

        # 3b. Rebound end: histogram flipped green while price below MA20
        if hist_turned_green and c < m20:
            result["macd_rebound_end_warning"] = True
            result["macd_rebound_status"] = REBOUND_ENDING
            result["macd_sell_or_avoid_reason"] = (
                "空頭趨勢中股價跌破 MA20 + MACD 由紅翻綠 — 反彈結束風險，宜出場或回避"
            )

        # 3c. Price fell below MA20 but histogram still red → observe, don't judge too early
        elif not hist_turned_green and hist_is_red and c < m20:
            if result["macd_rebound_status"] == NONE_STATUS:
                result["macd_rebound_status"] = OBSERVE
            if not result["macd_sell_or_avoid_reason"]:
                result["macd_sell_or_avoid_reason"] = (
                    "跌破 MA20 但 MACD 仍紅 — 反彈尚未完全結束，可觀察，不提早判斷"
                )

    return result
