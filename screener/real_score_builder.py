"""
screener/real_score_builder.py - Explainable bull_stock_score for real CSV mode.

Computes all 8 sub-scores + trust_cost bonus from RealDataLoader output.
Returns deduction_reasons, missing_data_reasons, formal_allowed, and per-component scores.

Score weights:
  theme_score           : 0-20  (主流題材強度)
  fundamental_score     : 0-15  (月營收 / 基本面成長)
  trend_score           : 0-15  (均線多頭或糾結突破)
  breakout_volume_score : 0-15  (帶量長紅 / 突破平台)
  institution_score     : 0-15  (法人 / 投信買超)
  holder_score          : 0-10  (大戶增加、散戶下降)
  margin_score          : 0-5   (融資未暴增)
  overheat_score        : 0-5   (KD / RSI 未過熱失控)
  trust_cost_score      : bonus (投信成本支撐)
"""

import logging

logger = logging.getLogger(__name__)


def build_real_score(symbol: str, all_data: dict) -> dict:
    """
    Compute explainable bull_stock_score from RealDataLoader.load_all() output.

    Parameters
    ----------
    symbol : str
    all_data : dict
        Output of RealDataLoader().load_all(symbol).

    Returns
    -------
    dict with:
        bull_stock_score (float 0-100),
        theme_score, fundamental_score, trend_score, breakout_volume_score,
        institution_score, holder_score, margin_score, overheat_score,
        trust_cost_score (float bonus 0-5),
        deduction_reasons (list of str),
        missing_data_reasons (list of str),
        formal_allowed (bool),
        is_bull_candidate (bool),
        is_second_wave_buy_point (bool),
        data_source (str: 'real')
    """
    sym = str(symbol)
    profile = all_data.get("profile") or {}
    dk = all_data.get("daily_k")          # dict with bars/n_bars or None
    chip = all_data.get("institutional")   # derived dict or None
    margin = all_data.get("margin")        # derived dict or None
    revenue = all_data.get("monthly_revenue")  # derived dict or None
    holder = all_data.get("holder")        # derived dict or None
    trust = all_data.get("trust_cost")    # derived dict or None

    deductions = []
    missing = []

    # ----------------------------------------------------------------
    # Gating: daily K is mandatory for formal candidacy
    # ----------------------------------------------------------------
    has_daily_k = bool(dk and dk.get("bars"))
    has_60d = dk.get("has_60d", False) if dk else False
    has_20d = dk.get("has_20d", False) if dk else False

    if not has_daily_k:
        missing.append("缺日 K 線資料，不可進入正式候選")
        return {
            "bull_stock_score": 0.0,
            "theme_score": 0.0, "fundamental_score": 0.0, "trend_score": 0.0,
            "breakout_volume_score": 0.0, "institution_score": 0.0,
            "holder_score": 0.0, "margin_score": 0.0, "overheat_score": 0.0,
            "trust_cost_score": 0.0,
            "deduction_reasons": deductions,
            "missing_data_reasons": missing,
            "formal_allowed": False,
            "is_bull_candidate": False,
            "is_second_wave_buy_point": False,
            "data_source": "real",
        }

    if not has_60d:
        missing.append(f"日 K 不足 60 日（現有 {dk.get('n_bars', 0)} 日），中線 / 長線不允許正式評分")

    bars = dk["bars"]
    closes = [b["close"] for b in bars]
    volumes = [b["volume"] for b in bars]

    # ----------------------------------------------------------------
    # 1. theme_score (0-20)
    # ----------------------------------------------------------------
    theme_score = 0.0
    tags = profile.get("theme_tags", [])
    is_mainstream = profile.get("is_mainstream_theme", False)
    if is_mainstream:
        theme_score += 12.0
    if tags:
        theme_score += min(8.0, len(tags) * 2.0)
    else:
        missing.append("無主題標籤資料")

    # ----------------------------------------------------------------
    # 2. fundamental_score (0-15)
    # ----------------------------------------------------------------
    fundamental_score = 0.0
    if revenue:
        yoy = revenue.get("latest_revenue_yoy", 0.0)
        acc_yoy = revenue.get("accumulated_revenue_yoy", 0.0)
        if yoy >= 50:
            fundamental_score += 6.0
        elif yoy >= 30:
            fundamental_score += 5.0
        elif yoy >= 20:
            fundamental_score += 3.0
        elif yoy >= 10:
            fundamental_score += 1.5
        elif yoy < 0:
            fundamental_score -= 2.0
            deductions.append(f"月營收年增 {yoy:.1f}%（負成長）")

        if acc_yoy >= 30:
            fundamental_score += 4.0
        elif acc_yoy >= 20:
            fundamental_score += 3.0
        elif acc_yoy >= 10:
            fundamental_score += 1.5

        fundamental_score = round(min(max(fundamental_score, 0.0), 15.0), 2)

        if not revenue.get("revenue_growth_pass"):
            if yoy < 30 or acc_yoy < 20:
                deductions.append(f"月營收年增 {yoy:.1f}% / 累計年增 {acc_yoy:.1f}% 未達飆股門檻（30/20）")
    else:
        missing.append("缺月營收資料，fundamental_score 不可滿分")
        fundamental_score = 4.0  # conservative partial credit

    # ----------------------------------------------------------------
    # 3. trend_score (0-15) — MA alignment
    # ----------------------------------------------------------------
    trend_score = 0.0
    if len(closes) >= 20:
        c = closes[-1]
        ma5  = sum(closes[-5:])  / 5  if len(closes) >= 5  else c
        ma10 = sum(closes[-10:]) / 10 if len(closes) >= 10 else c
        ma20 = sum(closes[-20:]) / 20

        if c > ma5 > ma10 > ma20:
            trend_score = 12.0  # 均線全部多頭排列
        elif c > ma10 > ma20:
            trend_score = 9.0
        elif c > ma20:
            trend_score = 6.0
        elif c < ma20:
            trend_score = 2.0
            deductions.append(f"股價跌破 MA20（{ma20:.1f}），趨勢偏弱")

        if has_60d:
            ma60 = sum(closes[-60:]) / 60
            if c > ma60:
                trend_score = min(15.0, trend_score + 3.0)
            else:
                trend_score = max(0.0, trend_score - 2.0)
                deductions.append(f"跌破 MA60（{ma60:.1f}），中線壓力")
    else:
        trend_score = 3.0
        missing.append("日 K 不足 20 日，均線趨勢僅能初估")

    trend_score = round(min(max(trend_score, 0.0), 15.0), 2)

    # ----------------------------------------------------------------
    # 4. breakout_volume_score (0-15) — volume expansion + breakout
    # ----------------------------------------------------------------
    breakout_volume_score = 0.0
    if len(closes) >= 20 and len(volumes) >= 20:
        avg_vol_20 = sum(volumes[-20:]) / 20
        latest_vol = volumes[-1]
        latest_close = closes[-1]
        prev_close = closes[-2] if len(closes) >= 2 else latest_close
        change_pct = (latest_close - prev_close) / max(prev_close, 1) * 100

        vol_ratio = latest_vol / max(avg_vol_20, 1)

        if change_pct > 2.0 and vol_ratio >= 1.5:
            breakout_volume_score = 12.0
        elif change_pct > 1.0 and vol_ratio >= 1.2:
            breakout_volume_score = 8.0
        elif vol_ratio >= 1.5:
            breakout_volume_score = 6.0
        elif change_pct > 0:
            breakout_volume_score = 4.0
        else:
            breakout_volume_score = 2.0

        # Check platform breakout in last 20 days
        hi20 = max(closes[-20:])
        if latest_close >= hi20 * 0.99:
            breakout_volume_score = min(15.0, breakout_volume_score + 3.0)
    else:
        breakout_volume_score = 3.0
        missing.append("量能突破資料不足")

    breakout_volume_score = round(min(max(breakout_volume_score, 0.0), 15.0), 2)

    # ----------------------------------------------------------------
    # 5. institution_score (0-15) — foreign + trust net buy
    # ----------------------------------------------------------------
    institution_score = 0.0
    if chip:
        f3d = chip.get("foreign_net_3d", 0)
        t3d = chip.get("trust_net_3d", 0)
        f5d = chip.get("foreign_net_5d", 0)
        t5d = chip.get("trust_net_5d", 0)
        sell_days = chip.get("institution_continuous_sell_days", 0)

        # Foreign score (0-8)
        if f5d >= 10000:
            institution_score += 8.0
        elif f5d >= 5000:
            institution_score += 6.0
        elif f5d >= 1000:
            institution_score += 4.0
        elif f5d > 0:
            institution_score += 2.0
        elif f5d < -5000:
            institution_score -= 3.0
            deductions.append(f"外資 5 日賣超 {f5d:.0f}（大量出脫）")

        # Trust score (0-7)
        if t5d >= 3000:
            institution_score += 7.0
        elif t5d >= 1500:
            institution_score += 5.0
        elif t5d >= 500:
            institution_score += 3.0
        elif t5d > 0:
            institution_score += 1.5
        elif t5d < -1000:
            institution_score -= 2.0
            deductions.append(f"投信 5 日賣超 {t5d:.0f}")

        if sell_days >= 3:
            institution_score -= 2.0
            deductions.append(f"法人連續 {sell_days} 日合計賣超")

        institution_score = round(min(max(institution_score, 0.0), 15.0), 2)
    else:
        missing.append("缺法人資料，institution_score 不可滿分")
        institution_score = 5.0  # conservative partial

    # ----------------------------------------------------------------
    # 6. holder_score (0-10) — major rising, retail falling
    # ----------------------------------------------------------------
    holder_score = 0.0
    if holder:
        conc_score = holder.get("chip_concentration_score", 5.0)
        major_trend = holder.get("major_holder_trend", 0)
        retail_trend = holder.get("retail_holder_trend", 0)

        holder_score = conc_score  # already 0-10

        if major_trend == -1:
            holder_score -= 2.0
            deductions.append("大戶持股下降，籌碼流出")
        if retail_trend == 1:
            holder_score -= 1.5
            deductions.append("散戶持股上升，籌碼分散風險")

        holder_score = round(min(max(holder_score, 0.0), 10.0), 2)
    else:
        missing.append("缺大戶散戶資料，holder_score 不可滿分")
        holder_score = 4.0  # conservative partial

    # ----------------------------------------------------------------
    # 7. margin_score (0-5) — low fusion risk = good
    # ----------------------------------------------------------------
    margin_score = 0.0
    if margin:
        overheat = margin.get("margin_overheat_risk", False)
        inc_pct = margin.get("margin_increase_pct", 0.0)
        if overheat:
            margin_score = 1.0
            deductions.append(f"融資 5 日暴增 {inc_pct:.1f}%，過熱風險")
        elif inc_pct > 5.0:
            margin_score = 2.5
        elif inc_pct > 2.0:
            margin_score = 3.5
        else:
            margin_score = 5.0   # stable margin = no risk
    else:
        missing.append("缺融資資料，margin_score 保守處理")
        margin_score = 3.0

    margin_score = round(min(max(margin_score, 0.0), 5.0), 2)

    # ----------------------------------------------------------------
    # 8. overheat_score (0-5) — KD/RSI not overheated
    # ----------------------------------------------------------------
    overheat_score = 0.0
    if len(closes) >= 14:
        gains = [max(closes[i] - closes[i-1], 0) for i in range(-14, 0)]
        losses = [max(closes[i-1] - closes[i], 0) for i in range(-14, 0)]
        avg_g = sum(gains) / 14
        avg_l = sum(losses) / 14
        if avg_l > 0:
            rsi = 100 - 100 / (1 + avg_g / avg_l)
        else:
            rsi = 100.0

        if rsi <= 70:
            overheat_score = 5.0
        elif rsi <= 80:
            overheat_score = 3.0
            deductions.append(f"RSI {rsi:.0f} 偏熱，注意回調風險")
        else:
            overheat_score = 1.0
            deductions.append(f"RSI {rsi:.0f} 過熱，短線追高風險高")
    else:
        overheat_score = 3.0
        missing.append("日 K 不足 14 日，RSI 無法計算")

    overheat_score = round(min(max(overheat_score, 0.0), 5.0), 2)

    # ----------------------------------------------------------------
    # Bonus: trust_cost_score (0-5)
    # ----------------------------------------------------------------
    trust_cost_score = 0.0
    trust_cost_note = None
    if trust:
        pct = trust.get("price_vs_trust_cost_pct", 0.0)
        support = trust.get("trust_cost_support", False)
        broken = trust.get("trust_cost_broken", False)
        if broken:
            trust_cost_score = 0.0
            deductions.append(f"股價跌破投信成本線 {pct:.1f}%，為警訊")
        elif support:
            trust_cost_score = 4.0
        elif pct > 5.0:
            trust_cost_score = 2.0
        trust_cost_note = f"投信成本支撐 {pct:+.1f}%"
    else:
        missing.append("缺投信成本資料")

    trust_cost_score = round(min(trust_cost_score, 5.0), 2)

    # ----------------------------------------------------------------
    # Phase 2 adjustments (KD advanced / short interest / fundamental quality)
    # ----------------------------------------------------------------
    phase2_adj = 0.0
    phase2_signals = {}
    phase2_deductions = []
    phase2_missing = []

    # Build price DataFrame from bars
    try:
        import pandas as pd
        from features.kd_advanced import compute_kd_advanced
        from features.short_interest_features import compute_short_interest
        from analysis.fundamental_quality_analyzer import analyze_fundamental_quality

        _df_p2 = pd.DataFrame(bars)
        if not _df_p2.empty and 'close' in _df_p2.columns:
            # KD advanced
            _kd_p2 = compute_kd_advanced(_df_p2)
            phase2_signals['kd_advanced'] = _kd_p2
            if _kd_p2.get('kd_low_golden_cross'):
                phase2_adj += 2.0
                deductions.append("KD 低檔黃金交叉 +2 (Phase 2)")
            if _kd_p2.get('kd_high_death_cross'):
                phase2_adj -= 2.0
                phase2_deductions.append("KD 高檔死亡交叉 -2")

            # Short interest (needs margin_df with short_balance; graceful fallback)
            _si_p2 = compute_short_interest(_df_p2)
            phase2_signals['short_interest'] = _si_p2
            _sq_fuel = _si_p2.get('short_squeeze_fuel_score', 0.0)
            if _sq_fuel >= 0.4:
                phase2_adj += min(2.0, _sq_fuel * 3.0)
            if _si_p2.get('weak_stock_short_increase'):
                phase2_adj -= 2.0
                phase2_deductions.append("弱勢股融券增加 -2")

        # Fundamental quality
        _mr_rows = None
        if revenue:
            _yr_dec = revenue.get('latest_revenue_yoy', 0) / 100.0
            _mr_rows = [{'yoy': _yr_dec}, {'yoy': _yr_dec}, {'yoy': _yr_dec}]
        _fq_p2 = analyze_fundamental_quality(
            symbol=sym,
            monthly_revenue_rows=_mr_rows,
        )
        phase2_signals['fundamental_quality'] = _fq_p2
        _fq_score_val = _fq_p2.get('fundamental_quality_score', 0.5)
        if _fq_score_val >= 0.7:
            phase2_adj += 2.0
        elif _fq_score_val < 0.3:
            phase2_adj -= 2.0
            phase2_deductions.append(f"基本面品質低 ({_fq_score_val:.2f}) -2")
        if _fq_p2.get('revenue_quality_warning'):
            phase2_adj -= 1.0
            phase2_deductions.append("營收品質警告 -1")
        if _fq_p2.get('earnings_risk_warning'):
            phase2_adj -= 2.0
            phase2_deductions.append(f"財報風險 -2: {_fq_p2['earnings_risk_warning']}")

    except Exception as _p2e:
        logger.debug("Phase 2 scoring in build_real_score: %s", _p2e)
        phase2_missing.append(f"Phase 2 signals unavailable: {_p2e}")

    deductions.extend(phase2_deductions)

    # ----------------------------------------------------------------
    # Composite score (0-100 base + bonus up to 5 + phase2 adj ±5)
    # ----------------------------------------------------------------
    base_score = (
        theme_score           # max 20
        + fundamental_score   # max 15
        + trend_score         # max 15
        + breakout_volume_score  # max 15
        + institution_score   # max 15
        + holder_score        # max 10
        + margin_score        # max 5
        + overheat_score      # max 5
    )  # max 100

    # Clamp phase2_adj to ±5 so it doesn't overwhelm existing score
    phase2_adj = max(-5.0, min(5.0, phase2_adj))

    bull_stock_score = round(min(max(base_score + trust_cost_score * 0.5 + phase2_adj, 0.0), 100.0), 1)

    # Formal allowed: must have daily K AND at least one of revenue/chip
    formal_allowed = has_daily_k and (revenue is not None or chip is not None)
    if not has_60d:
        formal_allowed = False  # mid/long require 60d

    is_bull = bull_stock_score >= 80
    is_second_wave = 65 <= bull_stock_score < 80

    return {
        "bull_stock_score":       bull_stock_score,
        "theme_score":            theme_score,
        "fundamental_score":      fundamental_score,
        "trend_score":            trend_score,
        "breakout_volume_score":  breakout_volume_score,
        "institution_score":      institution_score,
        "holder_score":           holder_score,
        "margin_score":           margin_score,
        "overheat_score":         overheat_score,
        "trust_cost_score":       trust_cost_score,
        "trust_cost_note":        trust_cost_note,
        "deduction_reasons":      deductions,
        "missing_data_reasons":   missing + phase2_missing,
        "formal_allowed":         formal_allowed,
        "is_bull_candidate":      is_bull,
        "is_second_wave_buy_point": is_second_wave,
        "data_source":            "real",
        "phase2_adj":             phase2_adj,
        "phase2_signals":         phase2_signals,
        "phase2_deduction_reasons": phase2_deductions,
    }
