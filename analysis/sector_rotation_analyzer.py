"""
analysis/sector_rotation_analyzer.py - Sector rotation / leader-laggard analysis.

Rules (老王教學: 族群聯動 / 指標股擴散 / 落後補漲 / 母以子貴):
- Leader stock breakout → watch same-sector laggards above MA20/MA60
- 60-day rolling correlation (no look-ahead)
- If leader turns weak → do NOT chase laggards
- Parent/child/cross-holding theme bonus only — cannot replace fundamentals
- No sector map → output "UNAVAILABLE", do not crash
"""

import logging
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def analyze_sector_rotation(
    symbol: str,
    df: pd.DataFrame,
    sector_peers: Optional[Dict[str, pd.DataFrame]] = None,
    theme_tags: Optional[List[str]] = None,
    leader_symbol: Optional[str] = None,
    leader_df: Optional[pd.DataFrame] = None,
) -> dict:
    """
    Analyze sector linkage and leader-laggard dynamics.

    Parameters
    ----------
    symbol : str
        Target stock symbol.
    df : pd.DataFrame
        Daily OHLCV for the target stock. Must contain: close. Sorted ascending.
    sector_peers : dict, optional
        {symbol: DataFrame} for sector peers. Each DF must contain close.
        If None → fallback to UNAVAILABLE.
    theme_tags : list of str, optional
        Sector / theme tags for this stock.
    leader_symbol : str, optional
        Designated sector leader symbol.
    leader_df : pd.DataFrame, optional
        Daily OHLCV for the sector leader.

    Returns
    -------
    dict
        sector_signal           : str  "LAGGARD_FOLLOW" | "WATCH" | "UNAVAILABLE" | "LEADER_WEAK"
        leader_symbol           : str | None
        leader_strength_score   : float  0.0–1.0
        linked_candidates       : list of str
        linkage_score           : float  0.0–1.0
        sector_rotation_reason  : str
        laggard_follow_signal   : bool
        parent_child_theme_signal: bool
    """
    result = {
        "sector_signal":             "UNAVAILABLE",
        "leader_symbol":             leader_symbol,
        "leader_strength_score":     0.0,
        "linked_candidates":         [],
        "linkage_score":             0.0,
        "sector_rotation_reason":    "",
        "laggard_follow_signal":     False,
        "parent_child_theme_signal": False,
    }

    if df is None or len(df) < 20:
        result["sector_rotation_reason"] = "目標股資料不足，無法分析族群聯動"
        return result

    # ── If no peer data, output UNAVAILABLE gracefully ───────────────────
    if not sector_peers and not leader_df:
        result["sector_rotation_reason"] = "缺族群 / 指標股資料，無法判斷落後補漲"
        return result

    df = df.copy().reset_index(drop=True)
    close = df["close"]

    ma20 = close.rolling(20).mean().iloc[-1]
    ma60 = close.rolling(60).mean().iloc[-1] if len(df) >= 60 else np.nan
    c    = close.iloc[-1]

    above_ma20 = (not np.isnan(ma20)) and c > ma20
    above_ma60 = (not np.isnan(ma60)) and c > ma60

    # ── Leader analysis ───────────────────────────────────────────────────
    leader_strong   = False
    leader_score    = 0.0
    leader_reasons  = []

    if leader_df is not None and len(leader_df) >= 20:
        ld = leader_df.copy().reset_index(drop=True)
        lc = ld["close"]
        lma20 = lc.rolling(20).mean().iloc[-1]
        lma60 = lc.rolling(60).mean().iloc[-1] if len(ld) >= 60 else np.nan
        lc_last = lc.iloc[-1]

        if (not np.isnan(lma20)) and lc_last > lma20:
            leader_strong  = True
            leader_score  += 0.5
            leader_reasons.append("指標股站上 MA20")
        if (not np.isnan(lma60)) and lc_last > lma60:
            leader_score  += 0.3
            leader_reasons.append("指標股站上 MA60")

        # Check if leader had a recent breakout (close > max of prior 10 bars)
        if len(lc) >= 11:
            prior_max = lc.iloc[-11:-1].max()
            if lc_last > prior_max:
                leader_score  += 0.2
                leader_reasons.append("指標股近期突破")

    result["leader_strength_score"] = round(min(1.0, leader_score), 3)

    # ── 60-day rolling correlation with peers ────────────────────────────
    linked = []
    total_corr_score = 0.0
    peer_count = 0

    if sector_peers:
        for peer_sym, peer_df in sector_peers.items():
            if peer_sym == symbol:
                continue
            if peer_df is None or len(peer_df) < 20:
                continue
            try:
                pclose = peer_df.sort_values("date")["close"] if "date" in peer_df.columns else peer_df["close"]
                # Align on index (use last 60 bars)
                n = min(60, len(close), len(pclose))
                c_tail = close.iloc[-n:].values
                p_tail = pclose.iloc[-n:].values
                if len(c_tail) >= 10 and np.std(c_tail) > 0 and np.std(p_tail) > 0:
                    corr = float(np.corrcoef(c_tail, p_tail)[0, 1])
                    if corr >= 0.6:
                        linked.append(peer_sym)
                        total_corr_score += corr
                        peer_count += 1
            except Exception:
                pass

    linkage_score = (total_corr_score / peer_count) if peer_count > 0 else 0.0
    result["linked_candidates"] = linked
    result["linkage_score"]     = round(min(1.0, linkage_score), 3)

    # ── Signal logic ─────────────────────────────────────────────────────
    reasons = leader_reasons[:]

    if leader_df is not None and not leader_strong:
        result["sector_signal"]          = "LEADER_WEAK"
        result["laggard_follow_signal"]  = False
        reasons.append("指標股轉弱，落後股不可追")
        result["sector_rotation_reason"] = "；".join(reasons)
        return result

    if leader_strong and above_ma20 and not above_ma60:
        # Target above MA20 but not MA60 → candidate laggard
        result["sector_signal"]         = "LAGGARD_FOLLOW"
        result["laggard_follow_signal"] = True
        reasons.append(
            "指標股已突破，本股站上 MA20 但尚未拉開，可列為落後補漲觀察"
        )
    elif leader_strong and above_ma20 and above_ma60:
        result["sector_signal"] = "WATCH"
        reasons.append("本股已站 MA20/MA60，族群強勢，繼續追蹤")
    elif not leader_df:
        result["sector_signal"] = "WATCH"
        reasons.append(f"族群聯動評分 {linkage_score:.2f}，無指標股資料")
    else:
        result["sector_signal"] = "WATCH"
        reasons.append("族群條件未完整，持續觀察")

    # ── Parent/child theme signal ─────────────────────────────────────────
    if theme_tags and any(t in ["母子概念", "轉投資", "子公司概念"] for t in theme_tags):
        result["parent_child_theme_signal"] = True
        reasons.append("母公司 / 子公司 / 轉投資概念加分，但不可取代基本面技術面")

    result["sector_rotation_reason"] = "；".join(reasons) if reasons else "無族群資料"
    return result
