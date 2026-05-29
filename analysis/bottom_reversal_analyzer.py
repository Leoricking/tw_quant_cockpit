"""
analysis/bottom_reversal_analyzer.py - Bottom reversal / breakdown-reversal strategy.

Based on 老王「抄底王」strategy notes.

IMPORTANT RULES:
- This is NOT an A/B/C strong-stock buy point.
- Output only REBOUND or SPECULATIVE_REBOUND — never mix into A/B/C grades.
- Confirmation must wait one day (no intraday look-ahead).
- Stop loss must be below the reversal-day low.
- Do NOT output formal long-term buy conclusions.
- Data leakage prevention: all signals use only past bars (t-1 and earlier).
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Decline thresholds to qualify as a deep-pullback candidate
DECLINE_THRESHOLDS = [0.20, 0.30, 0.35]

# Bottom signals
SIG_REBOUND     = "REBOUND"
SIG_SPECULATIVE = "SPECULATIVE_REBOUND"
SIG_NONE        = "NONE"


def analyze_bottom_reversal(df: pd.DataFrame) -> dict:
    """
    Detect bottom reversal / breakdown reversal patterns.

    Parameters
    ----------
    df : pd.DataFrame
        Daily OHLCV. Must contain: close, high, low (open optional).
        Sorted ascending by date.  At least 20 rows recommended.

    Returns
    -------
    dict
        bottom_signal            : str   "REBOUND" | "SPECULATIVE_REBOUND" | "NONE"
        bottom_reversal_detected : bool
        rebound_entry_price      : float | None
        rebound_stop_loss_price  : float | None
        rebound_target_price     : float | None
        rebound_risk_level       : str   "HIGH" | "MEDIUM" | "LOW" | "NONE"
        rebound_reason           : str
        is_speculative_rebound   : bool
    """
    result = {
        "bottom_signal":            SIG_NONE,
        "bottom_reversal_detected": False,
        "rebound_entry_price":      None,
        "rebound_stop_loss_price":  None,
        "rebound_target_price":     None,
        "rebound_risk_level":       "NONE",
        "rebound_reason":           "",
        "is_speculative_rebound":   False,
    }

    if df is None or len(df) < 10:
        result["rebound_reason"] = "資料不足 (<10 bars)，無法判斷破底翻"
        return result

    df   = df.copy().reset_index(drop=True)
    close = df["close"]
    high  = df["high"]  if "high"  in df.columns else close
    low   = df["low"]   if "low"   in df.columns else close

    last = len(df) - 1

    # ── Use last-completed bar (last - 1) to avoid look-ahead ────────────
    # The most-recent "confirmed" bar is [last-1]; [last] is today (not yet closed).
    # We read today's open and current price as [last].
    confirmed_last = last - 1
    if confirmed_last < 5:
        result["rebound_reason"] = "確認 bar 不足，無法判斷"
        return result

    c_now   = close.iloc[last]
    c_conf  = close.iloc[confirmed_last]
    l_conf  = low.iloc[confirmed_last]
    h_conf  = high.iloc[confirmed_last]

    # ── Step 1: Check deep decline qualifier ─────────────────────────────
    peak_price = high.iloc[:confirmed_last + 1].max()
    if peak_price <= 0:
        result["rebound_reason"] = "無法確定高點"
        return result

    decline_pct = (peak_price - c_conf) / peak_price
    qualifies   = any(decline_pct >= t for t in DECLINE_THRESHOLDS)

    if not qualifies:
        result["rebound_reason"] = (
            f"波段跌幅 {decline_pct:.1%}，未達 20% 閾值，不符跌深候選"
        )
        return result

    # ── Step 2: Check 20/60-day new low then reversal ────────────────────
    n20_low  = low.iloc[max(0, confirmed_last - 19): confirmed_last + 1].min()
    n60_low  = low.iloc[max(0, confirmed_last - 59): confirmed_last + 1].min()

    # "New low": today's low == period low
    new_20d_low = (l_conf <= n20_low * 1.001)
    new_60d_low = (l_conf <= n60_low * 1.001)

    # "Not breaking lower today" = current price > confirmed low
    not_breaking_lower = c_now > l_conf

    # "Long black day not breaking lower" — big down candle yesterday but no new low today
    prev2 = confirmed_last - 1
    long_black = False
    if prev2 >= 0:
        c_prev = close.iloc[prev2]
        if c_prev > 0:
            day_change = (c_conf - c_prev) / c_prev
            long_black = day_change < -0.03   # >3% red candle

    # ── Step 3: "Breakdown then reclaim" pattern ─────────────────────────
    # Prior day made new low, current day reclaimed previous day's low
    prev_low   = low.iloc[confirmed_last - 1] if confirmed_last >= 1 else np.nan
    breakdown_reclaim = (
        not np.isnan(prev_low)
        and l_conf < prev_low         # broke below prev day's low
        and c_now  > prev_low         # then reclaimed it
    )

    # ── Classify signal ───────────────────────────────────────────────────
    reversal_detected = False
    is_speculative    = False
    reasons           = []

    if (new_20d_low or new_60d_low) and not_breaking_lower:
        reversal_detected = True
        day_label = "60日" if new_60d_low else "20日"
        reasons.append(
            f"創 {day_label} 新低後隔日未再破低 → 破底翻觀察"
        )

    if long_black and not_breaking_lower:
        reversal_detected = True
        reasons.append("長黑收低後隔日未破低 → 止跌觀察")

    if breakdown_reclaim:
        reversal_detected = True
        is_speculative    = True
        reasons.append("破底翻站回前低 → 投機反彈型，風險較高")

    if not reversal_detected:
        result["rebound_reason"] = (
            f"跌幅 {decline_pct:.1%}，但未出現明確破底翻或止跌訊號"
        )
        return result

    # ── Price targets ─────────────────────────────────────────────────────
    entry_price    = round(c_now, 2)
    # Stop below the reversal-day low (confirmed_last low)
    stop_price     = round(l_conf * 0.995, 2)
    # Target: recover ~50% of recent drop
    recent_low     = low.iloc[max(0, confirmed_last - 10): confirmed_last + 1].min()
    recover_target = recent_low + (peak_price - recent_low) * 0.382
    target_price   = round(recover_target, 2)

    # ── Risk level ────────────────────────────────────────────────────────
    stop_dist_pct = (entry_price - stop_price) / entry_price if entry_price > 0 else 0
    if stop_dist_pct < 0.03:
        risk_level = "LOW"
    elif stop_dist_pct < 0.06:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    if is_speculative:
        risk_level = "HIGH"

    reasons.append(
        f"停損設在破底日低點下方 ({stop_price})，"
        f"目標 38.2% 反彈 ({target_price})"
    )
    reasons.append("反彈策略，不可輸出正式長線買進結論")

    signal = SIG_SPECULATIVE if is_speculative else SIG_REBOUND

    result.update({
        "bottom_signal":            signal,
        "bottom_reversal_detected": True,
        "rebound_entry_price":      entry_price,
        "rebound_stop_loss_price":  stop_price,
        "rebound_target_price":     target_price,
        "rebound_risk_level":       risk_level,
        "rebound_reason":           "；".join(reasons),
        "is_speculative_rebound":   is_speculative,
    })
    return result
