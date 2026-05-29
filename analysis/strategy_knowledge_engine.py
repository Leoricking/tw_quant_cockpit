"""
analysis/strategy_knowledge_engine.py - Strategy Knowledge Engine.

v0.3.6 core + Phase 2: Aggregates all sub-engines into a unified
strategy_signals dict.

v0.3.6 core modules (老王 8 teaching notes):
  capital_allocation, holding_period, volume_behavior, macd_strategy,
  valuation_river, exit_point

v0.3.6 Phase 2 additions:
  kd_advanced, short_interest, bottom_reversal, sector_rotation,
  fundamental_quality
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def build_strategy_signals(
    df: pd.DataFrame,
    symbol: str = "",
    # Position sizing
    entry_price: float = None,
    portfolio_value: float = 1_000_000,
    strategy_capital_ratio: float = 0.30,
    n_positions: int = 4,
    atr: float = None,
    # Valuation / fundamentals
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
    # Institutional chip
    institution_type: str = "none",
    institution_net: float = 0.0,
    institution_buying: bool = False,
    # Trade state
    half_profit_taken: bool = False,
    trend_stage: str = None,
    previous_high: float = None,
    take_profit_price: float = None,
    # Phase 2: short interest
    margin_df: pd.DataFrame = None,
    # Phase 2: sector rotation
    sector_peers: dict = None,
    theme_tags: list = None,
    leader_symbol: str = None,
    leader_df: pd.DataFrame = None,
    # Phase 2: fundamental quality
    monthly_revenue_rows: list = None,
    eps_ttm: float = None,
    eps_qoq_change: float = None,
    gross_margin_prev: float = None,
    operating_margin: float = None,
    operating_margin_prev: float = None,
    price_vs_ma20: float = None,
    price_vs_ma60: float = None,
) -> dict:
    """
    Build a unified strategy_signals dict by aggregating all sub-engines.

    Parameters
    ----------
    df : pd.DataFrame
        Daily OHLCV for the stock. Must contain: close, volume. Sorted ascending.
    symbol : str
    (all other params documented inline — see individual sub-engine docstrings)

    Returns
    -------
    dict
        entry_signals, exit_signals, risk_signals, volume_signals,
        kd_signals, macd_signals, valuation_signals, sector_signals,
        position_plan, holding_period_plan,
        kd_advanced_signals, short_interest_signals, bottom_reversal_signals,
        sector_rotation_signals, fundamental_quality_signals,
        no_chase_reasons, no_sell_low_reasons, do_not_rebuy_yet_reasons,
        final_strategy_decision, phase2_completed
    """
    # ── Lazy imports ──────────────────────────────────────────────────────
    from features.volume_behavior        import compute_volume_behavior
    from features.macd_strategy_features  import compute_macd_strategy
    from features.kd_advanced            import compute_kd_advanced
    from features.short_interest_features import compute_short_interest
    from analysis.holding_period_analyzer  import analyze_holding_period
    from analysis.valuation_river_analyzer import analyze_valuation_river
    from analysis.exit_point_analyzer     import analyze_exit_point
    from analysis.bottom_reversal_analyzer import analyze_bottom_reversal
    from analysis.sector_rotation_analyzer import analyze_sector_rotation
    from analysis.fundamental_quality_analyzer import analyze_fundamental_quality
    from risk.position_sizing             import portfolio_capital_allocation

    current_price = (
        float(df["close"].iloc[-1])
        if df is not None and len(df) > 0
        else (entry_price or 0.0)
    )

    # ── v0.3.6 core sub-engines ───────────────────────────────────────────
    vol_signals  = {}
    macd_signals = {}
    holding_plan = {}
    val_signals  = {}
    exit_sigs    = {}
    pos_plan     = {}

    try:
        vol_signals = compute_volume_behavior(df)
    except Exception as exc:
        logger.warning("volume_behavior failed for %s: %s", symbol, exc)

    try:
        macd_signals = compute_macd_strategy(df)
    except Exception as exc:
        logger.warning("macd_strategy failed for %s: %s", symbol, exc)

    try:
        holding_plan = analyze_holding_period(
            df,
            entry_price=entry_price,
            half_profit_taken=half_profit_taken,
            institution_buying=institution_buying,
            trend_stage=trend_stage,
        )
    except Exception as exc:
        logger.warning("holding_period failed for %s: %s", symbol, exc)

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
        logger.warning("valuation_river failed for %s: %s", symbol, exc)

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
        logger.warning("exit_point failed for %s: %s", symbol, exc)

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

    # ── Phase 2 sub-engines ───────────────────────────────────────────────
    kd_signals      = {}
    si_signals      = {}
    br_signals      = {}
    sr_signals      = {}
    fq_signals      = {}

    try:
        kd_signals = compute_kd_advanced(df)
    except Exception as exc:
        logger.warning("kd_advanced failed for %s: %s", symbol, exc)

    try:
        si_signals = compute_short_interest(df, margin_df=margin_df)
    except Exception as exc:
        logger.warning("short_interest failed for %s: %s", symbol, exc)

    try:
        br_signals = analyze_bottom_reversal(df)
    except Exception as exc:
        logger.warning("bottom_reversal failed for %s: %s", symbol, exc)

    try:
        sr_signals = analyze_sector_rotation(
            symbol=symbol,
            df=df,
            sector_peers=sector_peers,
            theme_tags=theme_tags,
            leader_symbol=leader_symbol,
            leader_df=leader_df,
        )
    except Exception as exc:
        logger.warning("sector_rotation failed for %s: %s", symbol, exc)

    try:
        fq_signals = analyze_fundamental_quality(
            symbol=symbol,
            monthly_revenue_rows=monthly_revenue_rows,
            eps_ttm=eps_ttm,
            eps_qoq_change=eps_qoq_change,
            gross_margin=gross_margin,
            gross_margin_prev=gross_margin_prev,
            operating_margin=operating_margin,
            operating_margin_prev=operating_margin_prev,
            price_vs_ma20=price_vs_ma20,
            price_vs_ma60=price_vs_ma60,
        )
    except Exception as exc:
        logger.warning("fundamental_quality failed for %s: %s", symbol, exc)

    # ── Entry signals ─────────────────────────────────────────────────────
    entry_signals = {
        "macd_bull_pullback_buy":    macd_signals.get("macd_bull_pullback_buy",    False),
        "macd_wait_confirm":         macd_signals.get("macd_wait_confirm",         False),
        "macd_fake_reclaim_warning": macd_signals.get("macd_fake_reclaim_warning", False),
        "volume_breakout_confirmed": vol_signals.get("breakout_volume_confirmed",  False),
        "strong_volume_breakout":    vol_signals.get("strong_volume_breakout",     False),
        "kd_low_golden_cross":       kd_signals.get("kd_low_golden_cross",         False),
        "kd_high_death_cross":       kd_signals.get("kd_high_death_cross",         False),
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
    if kd_signals.get("kd_high_death_cross"):
        no_chase.append("KD 高檔死亡交叉，降低追價")
    if si_signals.get("weak_stock_short_increase"):
        no_chase.append("弱勢股融券增加，不視為多方訊號")
    if fq_signals.get("earnings_risk_warning"):
        no_chase.append(f"財報風險：{fq_signals['earnings_risk_warning']}")

    # ── No-panic-sell reasons ─────────────────────────────────────────────
    no_sell_low = []
    if holding_plan.get("do_not_sell_at_support_reason"):
        no_sell_low.append(holding_plan["do_not_sell_at_support_reason"])
    if holding_plan.get("institution_trailing_reason"):
        no_sell_low.append(holding_plan["institution_trailing_reason"])
    if vol_signals.get("volume_shrink_above_ma"):
        no_sell_low.append("量縮守均線，屬正常整理，不需亂砍")
    if kd_signals.get("kd_high_sticky_trend"):
        no_sell_low.append(
            f"KD 高檔鈍化 {kd_signals.get('kd_high_sticky_days', 0)} 日，"
            "強勢股不因一次高檔交叉就立刻賣"
        )

    # ── Risk signals ──────────────────────────────────────────────────────
    risk_signals = {
        "one_day_volume_spike_risk": vol_signals.get("one_day_volume_spike_risk", False),
        "volume_failure_warning":    vol_signals.get("volume_failure_warning",    False),
        "macd_rebound_end_warning":  macd_signals.get("macd_rebound_end_warning", False),
        "valuation_overvalued":      val_signals.get("valuation_sell_zone",       False),
        "kd_high_death_cross":       kd_signals.get("kd_high_death_cross",        False),
        "short_covering_warning":    si_signals.get("short_covering_warning",     False),
        "fundamental_quality_low":   (fq_signals.get("fundamental_quality_score", 0.5) < 0.3),
    }

    # ── Final decision ────────────────────────────────────────────────────
    decision_parts = []
    warning_parts  = []
    trend_ctx = macd_signals.get("macd_trend_context", "NEUTRAL")

    # A/B/C strong-stock buy
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

    # KD contribution
    if entry_signals["kd_low_golden_cross"]:
        decision_parts.append("KD 低檔黃金交叉 → 加分")
    if entry_signals["kd_high_death_cross"]:
        warning_parts.append("KD 高檔死亡交叉 → 降低追高意願")

    # Rebound (separate track — NOT A/B/C)
    if br_signals.get("bottom_reversal_detected"):
        br_sig = br_signals.get("bottom_signal", "REBOUND")
        br_risk = br_signals.get("rebound_risk_level", "HIGH")
        decision_parts.append(
            f"反彈策略 [{br_sig}] 風險 {br_risk} — 非強勢 A/B/C 買點"
        )

    # Exits
    if exit_sigs.get("relative_high_exit_signal"):
        decision_parts.append("觸及前高壓力 → 先賣一半")
    if exit_sigs.get("failed_breakout_exit_signal"):
        warning_parts.append("突破失敗風險，考慮出清或降低持股")
    if risk_signals["macd_rebound_end_warning"]:
        warning_parts.append("MACD 反彈結束警示，宜出場或回避")

    # Squeeze
    if si_signals.get("short_interest_signal") == "SQUEEZE_FUEL":
        decision_parts.append("融券軋空燃料充足，強勢股續強機率提升")

    # Sector
    if sr_signals.get("laggard_follow_signal"):
        decision_parts.append("族群落後補漲候選")
    if sr_signals.get("sector_signal") == "LEADER_WEAK":
        warning_parts.append("指標股轉弱，落後股不可追")

    # Valuation
    if val_signals.get("valuation_buy_zone"):
        decision_parts.append("估值低估區，長線可關注")

    # Fundamental
    if fq_signals.get("earnings_risk_warning"):
        warning_parts.append(f"財報風險：{fq_signals['earnings_risk_warning']}")
    if fq_signals.get("pre_earnings_price_warning"):
        warning_parts.append(fq_signals["pre_earnings_price_warning"])

    # Data guard
    fq_score = fq_signals.get("fundamental_quality_score", 0.5)
    if fq_score < 0.3:
        warning_parts.append("基本面品質分數低，不建議中長線正式買點")

    final_decision = "；".join(decision_parts) if decision_parts else "無明確訊號，持續觀察"
    final_warning  = "；".join(warning_parts)  if warning_parts  else ""

    return {
        # v0.3.6 core
        "entry_signals":         entry_signals,
        "exit_signals":          exit_sigs,
        "risk_signals":          risk_signals,
        "volume_signals":        vol_signals,
        "kd_signals":            kd_signals,        # now populated by kd_advanced
        "macd_signals":          macd_signals,
        "valuation_signals":     val_signals,
        "sector_signals":        sr_signals,        # now populated by sector_rotation
        "position_plan":         pos_plan,
        "holding_period_plan":   holding_plan,
        "no_chase_reasons":      no_chase,
        "no_sell_low_reasons":   no_sell_low,
        "do_not_rebuy_yet_reasons": (
            [exit_sigs["do_not_rebuy_yet_reason"]]
            if exit_sigs.get("do_not_rebuy_yet_reason") else []
        ),
        # Phase 2 additions
        "kd_advanced_signals":           kd_signals,
        "short_interest_signals":        si_signals,
        "bottom_reversal_signals":       br_signals,
        "sector_rotation_signals":       sr_signals,
        "fundamental_quality_signals":   fq_signals,
        "phase2_completed":              True,
        # Final
        "final_strategy_decision": {
            "decision": final_decision,
            "warning":  final_warning,
        },
    }
