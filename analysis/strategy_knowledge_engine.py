"""
analysis/strategy_knowledge_engine.py - Strategy Knowledge Engine.

v0.3.6: Aggregates capital allocation, holding period, volume behavior,
        MACD strategy, valuation river, and exit point signals into a
        unified strategy_signals dict.

Based on 8 teaching modules from 老王:
  20201028, 20201105, 20201112, 20201119,
  20220406, 20220504, 20220518, 20220601
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def build_strategy_signals(
    df: pd.DataFrame,
    symbol: str = "",
    # Position sizing parameters
    entry_price: float = None,
    portfolio_value: float = 1_000_000,
    strategy_capital_ratio: float = 0.30,
    n_positions: int = 4,
    atr: float = None,
    # Fundamental / valuation parameters
    estimated_eps: float = None,
    trailing_eps: float = None,
    pe_low: float = None,
    pe_mid: float = None,
    pe_high: float = None,
    pe_extreme_low: float = None,
    pe_extreme_high: float = None,
    revenue_growth: float = None,
    gross_margin: float = None,
    eps_declining: bool = False,
    # Institutional chip parameters
    institution_type: str = "none",
    institution_net: float = 0.0,
    institution_buying: bool = False,
    # Trade state parameters
    half_profit_taken: bool = False,
    trend_stage: str = None,
    previous_high: float = None,
    take_profit_price: float = None,
) -> dict:
    """
    Build a unified strategy_signals dict by aggregating all sub-engines.

    Parameters
    ----------
    df : pd.DataFrame
        Daily OHLCV data for the stock.  Must contain: close, volume.
        Sorted ascending by date.
    symbol : str
    entry_price : float, optional
        Average cost basis.  Used for swing risk, position sizing, and exits.
    portfolio_value : float
        Total portfolio value in NTD.
    strategy_capital_ratio : float
        Fraction of portfolio dedicated to strategy (default 0.30 = 30 %).
    n_positions : int
        How many stocks in the strategy basket (default 4).
    atr : float, optional
        Average True Range for stop / target computation.
    estimated_eps, trailing_eps : float, optional
    pe_* : float, optional
    revenue_growth, gross_margin : float, optional
    eps_declining : bool
    institution_type : str   "foreign" | "trust" | "none"
    institution_net  : float
    institution_buying : bool
    half_profit_taken : bool
    trend_stage : str, optional
    previous_high : float, optional
    take_profit_price : float, optional

    Returns
    -------
    dict with keys matching Spec I:
        entry_signals
        exit_signals
        risk_signals
        volume_signals
        kd_signals
        macd_signals
        valuation_signals
        sector_signals
        position_plan
        holding_period_plan
        no_chase_reasons
        no_sell_low_reasons
        do_not_rebuy_yet_reasons
        final_strategy_decision
    """
    # ── Lazy imports (all sub-engines) ────────────────────────────────────
    from features.volume_behavior       import compute_volume_behavior
    from features.macd_strategy_features import compute_macd_strategy
    from analysis.holding_period_analyzer import analyze_holding_period
    from analysis.valuation_river_analyzer import analyze_valuation_river
    from analysis.exit_point_analyzer    import analyze_exit_point
    from risk.position_sizing            import portfolio_capital_allocation

    current_price = (
        df["close"].iloc[-1]
        if df is not None and len(df) > 0
        else (entry_price or 0)
    )

    # ── Sub-engine calls ──────────────────────────────────────────────────
    vol_signals     = {}
    macd_signals    = {}
    holding_plan    = {}
    val_signals     = {}
    exit_sigs       = {}
    pos_plan        = {}

    try:
        vol_signals = compute_volume_behavior(df)
    except Exception as exc:
        logger.warning("volume_behavior failed for %s: %s", symbol, exc)

    try:
        macd_signals = compute_macd_strategy(df)
    except Exception as exc:
        logger.warning("macd_strategy_features failed for %s: %s", symbol, exc)

    try:
        holding_plan = analyze_holding_period(
            df,
            entry_price=entry_price,
            half_profit_taken=half_profit_taken,
            institution_buying=institution_buying,
            trend_stage=trend_stage,
        )
    except Exception as exc:
        logger.warning("holding_period_analyzer failed for %s: %s", symbol, exc)

    try:
        val_signals = analyze_valuation_river(
            current_price=current_price,
            estimated_eps=estimated_eps,
            trailing_eps=trailing_eps,
            pe_low=pe_low, pe_mid=pe_mid, pe_high=pe_high,
            pe_extreme_low=pe_extreme_low, pe_extreme_high=pe_extreme_high,
            revenue_growth=revenue_growth,
            gross_margin=gross_margin,
            eps_declining=eps_declining,
        )
    except Exception as exc:
        logger.warning("valuation_river_analyzer failed for %s: %s", symbol, exc)

    try:
        exit_sigs = analyze_exit_point(
            df,
            entry_price=entry_price,
            take_profit_price=take_profit_price,
            previous_high=previous_high,
            institution_type=institution_type,
            institution_net=institution_net,
            half_sold=half_profit_taken,
        )
    except Exception as exc:
        logger.warning("exit_point_analyzer failed for %s: %s", symbol, exc)

    try:
        pos_plan = portfolio_capital_allocation(
            portfolio_value=portfolio_value,
            strategy_capital_ratio=strategy_capital_ratio,
            n_positions=n_positions,
            entry_price=entry_price or current_price,
            atr=atr,
        )
    except Exception as exc:
        logger.warning("portfolio_capital_allocation failed for %s: %s", symbol, exc)

    # ── Entry signals ─────────────────────────────────────────────────────
    entry_signals = {
        "macd_bull_pullback_buy":    macd_signals.get("macd_bull_pullback_buy",    False),
        "macd_wait_confirm":         macd_signals.get("macd_wait_confirm",         False),
        "macd_fake_reclaim_warning": macd_signals.get("macd_fake_reclaim_warning", False),
        "volume_breakout_confirmed": vol_signals.get("breakout_volume_confirmed",  False),
        "strong_volume_breakout":    vol_signals.get("strong_volume_breakout",     False),
    }

    # ── No-chase reasons ──────────────────────────────────────────────────
    no_chase = []
    if pos_plan.get("no_chase_reason"):
        no_chase.append(pos_plan["no_chase_reason"])
    if macd_signals.get("macd_fake_reclaim_warning"):
        no_chase.append("MACD 假站回風險，不追高")
    if vol_signals.get("one_day_volume_spike_risk"):
        no_chase.append("一日量能風險，不追高")
    if val_signals.get("valuation_sell_zone"):
        no_chase.append("本益比高估區，不建議追高")

    # ── No-panic-sell reasons ─────────────────────────────────────────────
    no_sell_low = []
    if holding_plan.get("do_not_sell_at_support_reason"):
        no_sell_low.append(holding_plan["do_not_sell_at_support_reason"])
    if holding_plan.get("institution_trailing_reason"):
        no_sell_low.append(holding_plan["institution_trailing_reason"])
    if vol_signals.get("volume_shrink_above_ma"):
        no_sell_low.append("量縮守均線，屬正常整理，不需亂砍")

    # ── Risk signals ──────────────────────────────────────────────────────
    risk_signals = {
        "one_day_volume_spike_risk": vol_signals.get("one_day_volume_spike_risk", False),
        "volume_failure_warning":    vol_signals.get("volume_failure_warning",    False),
        "macd_rebound_end_warning":  macd_signals.get("macd_rebound_end_warning", False),
        "valuation_overvalued":      val_signals.get("valuation_sell_zone",       False),
    }

    # ── Final decision ────────────────────────────────────────────────────
    decision_parts = []
    warning_parts  = []

    trend_ctx = macd_signals.get("macd_trend_context", "NEUTRAL")
    if entry_signals["macd_bull_pullback_buy"] and entry_signals["volume_breakout_confirmed"]:
        decision_parts.append("多頭回檔買點確認 + 放量突破 → 積極買進")
    elif entry_signals["macd_bull_pullback_buy"]:
        decision_parts.append("MACD 多頭回檔買點確認 → 可買進")
    elif entry_signals["macd_wait_confirm"]:
        decision_parts.append("等待 MACD 翻紅確認 → 暫觀察")
    elif entry_signals["macd_fake_reclaim_warning"]:
        decision_parts.append("MACD 假站回風險 → 不追買")
    elif trend_ctx == "BEAR":
        decision_parts.append("空頭趨勢 → 避免買進")

    if exit_sigs.get("relative_high_exit_signal"):
        decision_parts.append("觸及前高壓力 → 先賣一半")
    if exit_sigs.get("failed_breakout_exit_signal"):
        warning_parts.append("突破失敗風險，考慮出清或降低持股")
    if risk_signals["macd_rebound_end_warning"]:
        warning_parts.append("MACD 反彈結束警示，宜出場或回避")
    if val_signals.get("valuation_buy_zone"):
        decision_parts.append("估值低估區，長線可關注")

    final_decision = "；".join(decision_parts) if decision_parts else "無明確訊號，持續觀察"
    final_warning  = "；".join(warning_parts)   if warning_parts  else ""

    return {
        "entry_signals":         entry_signals,
        "exit_signals":          exit_sigs,
        "risk_signals":          risk_signals,
        "volume_signals":        vol_signals,
        "kd_signals":            {},   # placeholder — KD engine integrates separately
        "macd_signals":          macd_signals,
        "valuation_signals":     val_signals,
        "sector_signals":        {},   # placeholder — sector rotation engine
        "position_plan":         pos_plan,
        "holding_period_plan":   holding_plan,
        "no_chase_reasons":      no_chase,
        "no_sell_low_reasons":   no_sell_low,
        "do_not_rebuy_yet_reasons": (
            [exit_sigs["do_not_rebuy_yet_reason"]]
            if exit_sigs.get("do_not_rebuy_yet_reason") else []
        ),
        "final_strategy_decision": {
            "decision": final_decision,
            "warning":  final_warning,
        },
    }
