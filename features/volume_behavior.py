"""
features/volume_behavior.py - Volume behavior analysis engine.

Based on: 20220406 成交量(上)

Classifies volume patterns: breakout confirmation, roll-up, one-day spike risk,
shrink-above-MA (healthy consolidation), and failure breakout.
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def compute_volume_behavior(df: pd.DataFrame) -> dict:
    """
    Analyze volume behavior patterns from OHLCV daily data.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: close, volume. Sorted ascending by date.
        At least 10 rows recommended.

    Returns
    -------
    dict
        breakout_volume_confirmed : bool
            Current bar volume >= 2× vol_ma5 or vol_ma10.
        strong_volume_breakout    : bool
            Current bar volume >= 3× average — extra strong signal.
        volume_roll_up_score      : float  0.0–1.0
            Proportion of last 5 bars sustaining >= 60% of peak volume.
        one_day_volume_spike_risk : bool
            Prior bar spiked, current bar already shrunk — one-day wonder.
        volume_shrink_above_ma    : bool
            Volume declining but price still above MA5 & MA10 — healthy rest.
        volume_failure_warning    : bool
            High-vol bar followed by price slipping below MA5/MA10.
        demand_persistence_score  : float  0.0–1.0
            Composite demand score (roll-up + breakout − spike risk − failure).
    """
    result = {
        "breakout_volume_confirmed": False,
        "strong_volume_breakout":    False,
        "volume_roll_up_score":      0.0,
        "one_day_volume_spike_risk": False,
        "volume_shrink_above_ma":    False,
        "volume_failure_warning":    False,
        "demand_persistence_score":  0.0,
    }

    if df is None or len(df) < 5:
        return result

    df = df.copy().reset_index(drop=True)
    close  = df["close"]
    volume = df["volume"]

    vol_ma5  = volume.rolling(5).mean()
    vol_ma10 = volume.rolling(10).mean()
    ma5  = close.rolling(5).mean()
    ma10 = close.rolling(10).mean()

    last = len(df) - 1
    last_vol   = volume.iloc[last]
    last_close = close.iloc[last]

    v5  = vol_ma5.iloc[last]
    v10 = vol_ma10.iloc[last] if len(df) >= 10 else np.nan
    m5  = ma5.iloc[last]
    m10 = ma10.iloc[last] if len(df) >= 10 else np.nan

    def _valid(x):
        return x is not None and not np.isnan(x) and x > 0

    # ── 1. breakout_volume_confirmed & strong_volume_breakout ───────────────
    bv = sv = False
    if _valid(v5):
        ratio5 = last_vol / v5
        if ratio5 >= 2.0:
            bv = True
        if ratio5 >= 3.0:
            sv = True
    if not bv and _valid(v10):
        ratio10 = last_vol / v10
        if ratio10 >= 2.0:
            bv = True
        if ratio10 >= 3.0:
            sv = True
    result["breakout_volume_confirmed"] = bv
    result["strong_volume_breakout"]    = sv

    # ── 2. volume_roll_up ───────────────────────────────────────────────────
    roll_up_score = 0.0
    if last >= 4:
        window = volume.iloc[last - 4: last + 1]
        peak   = window.max()
        if peak > 0:
            sustained = (window >= peak * 0.6).sum()
            roll_up_score = min(1.0, sustained / len(window))
    result["volume_roll_up_score"] = round(roll_up_score, 3)

    # ── 3. one_day_volume_spike_risk ────────────────────────────────────────
    spike_risk = False
    if last >= 2:
        vol_prev = volume.iloc[last - 1]
        ref      = v10 if _valid(v10) else (v5 if _valid(v5) else None)
        if ref and ref > 0:
            if vol_prev >= ref * 2.0 and last_vol < ref * 1.2:
                spike_risk = True
    result["one_day_volume_spike_risk"] = spike_risk

    # ── 4. volume_shrink_above_ma ───────────────────────────────────────────
    shrink_above = False
    if last >= 2 and _valid(m5) and _valid(m10):
        vol_window   = volume.iloc[max(0, last - 2): last + 1]
        vol_declining = vol_window.iloc[-1] < vol_window.iloc[0]
        above_ma      = last_close > m5 and last_close > m10
        if vol_declining and above_ma:
            shrink_above = True
    result["volume_shrink_above_ma"] = shrink_above

    # ── 5. volume_failure_warning ───────────────────────────────────────────
    vol_failure = False
    if last >= 1 and (_valid(m5) or _valid(m10)):
        prev_vol = volume.iloc[last - 1]
        ref      = v5 if _valid(v5) else v10
        if ref and ref > 0:
            prev_high_vol   = prev_vol >= ref * 1.5
            price_fell_back = ((_valid(m5) and last_close < m5) or
                               (_valid(m10) and last_close < m10))
            no_recovery_vol = last_vol < ref * 1.2
            if prev_high_vol and price_fell_back and no_recovery_vol:
                vol_failure = True
    result["volume_failure_warning"] = vol_failure

    # ── demand_persistence_score ────────────────────────────────────────────
    dps = roll_up_score * 0.5
    if bv:
        dps += 0.3
    if sv:
        dps += 0.1
    if shrink_above:
        dps += 0.1
    if spike_risk:
        dps -= 0.3
    if vol_failure:
        dps -= 0.4
    result["demand_persistence_score"] = round(max(0.0, min(1.0, dps)), 3)

    return result
