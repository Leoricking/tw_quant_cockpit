"""
strategy_filters/financial_turnaround_filter.py — Financial Turnaround & Trend Discipline Filter (v0.5.1.1).

策略名稱: 財報翻多 + 趨勢紀律策略篩選
English:  Financial Turnaround & Trend Discipline

Scoring (0–100):
  財報 / EPS 成長              : 25
  月營收 / 毛利率 / 營益率續強   : 15
  低位階 / 底部翻多              : 15
  技術轉強 / 站回均線            : 15
  法人 / 籌碼支持                : 15
  風控健康度 / 融資未失控         : 10
  (避雷扣分: 最多 -30)

Scenarios:
  A. 財報好 + 低位階 + 技術翻多   → SECOND_WAVE_CANDIDATE
  B. 財報好，但已大漲             → DO_NOT_CHASE
  C. 財報差 + 大盤創高個股不過高   → AVOID_OR_ROTATE

Suggested actions (no BUY / SELL / ORDER):
  WATCH | WAIT_PULLBACK | SECOND_WAVE_CANDIDATE | REDUCE_RISK | AVOID | ROTATE_TO_STRONGER

[!] Research Only. Strategy Filter Only. No Real Orders. Production Trading: BLOCKED.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety invariants
# ---------------------------------------------------------------------------
_RESEARCH_ONLY = True
_NO_REAL_ORDERS = True
_PRODUCTION_BLOCKED = True

# ---------------------------------------------------------------------------
# Score weight ceilings
# ---------------------------------------------------------------------------
_W_FUNDAMENTAL    = 25  # EPS / 財報
_W_REVENUE        = 15  # 月營收 / 毛利率 / 營益率
_W_BASE           = 15  # 低位階 / 底部翻多
_W_TECHNICAL      = 15  # 技術轉強 / 站回均線
_W_CHIP           = 15  # 法人 / 籌碼
_W_RISK           = 10  # 風控健康度 / 融資
_MAX_DEDUCT       = 30  # 避雷扣分上限

# ---------------------------------------------------------------------------
# Scenario labels
# ---------------------------------------------------------------------------
SCENARIO_A = "SCENARIO_A_LOW_BASE_BREAKOUT"
SCENARIO_B = "SCENARIO_B_EXTENDED_GOOD_FUNDAMENTAL"
SCENARIO_C = "SCENARIO_C_RELATIVE_WEAKNESS_POOR_FUNDAMENTAL"
SCENARIO_UNKNOWN = "SCENARIO_UNKNOWN"

# ---------------------------------------------------------------------------
# Suggested action constants (no BUY / SELL / ORDER)
# ---------------------------------------------------------------------------
ACTION_WATCH             = "WATCH"
ACTION_WAIT_PULLBACK     = "WAIT_PULLBACK"
ACTION_SECOND_WAVE       = "SECOND_WAVE_CANDIDATE"
ACTION_REDUCE_RISK       = "REDUCE_RISK"
ACTION_AVOID             = "AVOID"
ACTION_ROTATE            = "ROTATE_TO_STRONGER"

_VALID_ACTIONS = {
    ACTION_WATCH, ACTION_WAIT_PULLBACK, ACTION_SECOND_WAVE,
    ACTION_REDUCE_RISK, ACTION_AVOID, ACTION_ROTATE,
}

# Score interpretation bands
_BAND_STRONG  = 80   # 80–100: 財報翻多強勢候選
_BAND_WATCH   = 65   # 65–79 : 觀察股
_BAND_NEUTRAL = 50   # 50–64 : 僅觀察不追
                     # < 50  : 避開


class FinancialTurnaroundFilter:
    """
    財報翻多 + 趨勢紀律策略篩選器.

    Evaluates a stock on 6 dimensions and classifies it into one of three
    scenario archetypes.

    Parameters
    ----------
    mode : 'real' | 'mock'
        Data mode. Does NOT affect safety logic.

    Safety invariants
    -----------------
    read_only          = True
    no_real_orders     = True
    production_blocked = True
    All suggested_action values are restricted to WATCH / WAIT_PULLBACK /
    SECOND_WAVE_CANDIDATE / REDUCE_RISK / AVOID / ROTATE_TO_STRONGER.
    No BUY / SELL / ORDER output is ever generated.
    """

    VERSION = "v0.5.1.1"

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(self, mode: str = "real") -> None:
        self.mode = mode

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def evaluate(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a stock and return the full filter decision.

        Parameters
        ----------
        stock_data : dict
            Must contain at minimum 'symbol'. All other keys are optional
            and default to None / safe fallback values.

        Returns
        -------
        dict with keys:
            symbol, score, scenario, labels,
            bullish_reasons, risk_reasons,
            entry_conditions, exit_conditions, avoid_conditions,
            suggested_action,
            research_only, no_real_orders, production_blocked

        [!] suggested_action is NEVER 'BUY', 'SELL', or 'ORDER'.
        """
        symbol = str(stock_data.get("symbol", "UNKNOWN"))
        logger.debug("FinancialTurnaroundFilter.evaluate: symbol=%s mode=%s", symbol, self.mode)

        # --- Score components ---
        fund_score   = self.score_fundamentals(stock_data)
        tech_score   = self.score_technical(stock_data)
        chip_score   = self.score_chip(stock_data)
        risk_score   = self.score_risk(stock_data)
        deduction    = self._score_deductions(stock_data)

        raw_score = (
            fund_score["fundamental_score"]
            + fund_score["revenue_score"]
            + tech_score["base_score"]
            + tech_score["technical_score"]
            + chip_score["chip_score"]
            + risk_score["risk_score"]
            - deduction["total_deduction"]
        )
        score = max(0, min(100, raw_score))

        # --- Classify scenario ---
        scenario = self.classify_scenario(stock_data)

        # --- Labels ---
        labels = self._build_labels(scenario, stock_data)

        # --- Build reasons ---
        bullish_reasons = (
            fund_score["bullish_reasons"]
            + tech_score["bullish_reasons"]
            + chip_score["bullish_reasons"]
        )
        risk_reasons = (
            risk_score["risk_reasons"]
            + deduction["risk_reasons"]
        )

        # --- Entry / exit / avoid conditions ---
        entry_conditions  = self._build_entry_conditions(stock_data)
        exit_conditions   = self._build_exit_conditions(stock_data)
        avoid_conditions  = self._build_avoid_conditions(stock_data)

        # --- Decision ---
        decision = self.build_decision(score, scenario, stock_data)

        return {
            "symbol":            symbol,
            "score":             score,
            "scenario":          scenario,
            "labels":            labels,
            "bullish_reasons":   bullish_reasons,
            "risk_reasons":      risk_reasons,
            "entry_conditions":  entry_conditions,
            "exit_conditions":   exit_conditions,
            "avoid_conditions":  avoid_conditions,
            "suggested_action":  decision["suggested_action"],
            "score_breakdown":   {
                "fundamental":  fund_score["fundamental_score"],
                "revenue":      fund_score["revenue_score"],
                "base":         tech_score["base_score"],
                "technical":    tech_score["technical_score"],
                "chip":         chip_score["chip_score"],
                "risk":         risk_score["risk_score"],
                "deduction":    -deduction["total_deduction"],
            },
            # Safety metadata
            "research_only":       True,
            "no_real_orders":      True,
            "production_blocked":  True,
            "mode":                self.mode,
            "filter_version":      self.VERSION,
        }

    # ------------------------------------------------------------------
    # Score: Fundamentals (EPS / 財報)
    # ------------------------------------------------------------------

    def score_fundamentals(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score fundamental quality up to _W_FUNDAMENTAL (25) + _W_REVENUE (15).

        Keys read from stock_data:
            eps_yoy_growth     : float (%)   — EPS 年增率
            q1_eps             : float       — Q1 EPS
            estimated_annual_eps: float      — 全年 EPS 估算 (or None → q1_eps * 4)
            current_price      : float       — 收盤價
            eps_declining      : bool        — EPS 衰退
            revenue_growth     : bool        — 月營收續強
            gross_margin_ok    : bool        — 毛利率未惡化
            operating_margin_ok: bool        — 營益率未惡化
            revenue_declining  : bool        — 營收衰退
        """
        score     = 0
        rev_score = 0
        bullish   = []

        eps_growth  = _safe_float(stock_data.get("eps_yoy_growth"))
        q1_eps      = _safe_float(stock_data.get("q1_eps"))
        ann_eps     = _safe_float(stock_data.get("estimated_annual_eps"))
        price       = _safe_float(stock_data.get("current_price"))
        eps_decline = _safe_bool(stock_data.get("eps_declining"))
        rev_growth  = _safe_bool(stock_data.get("revenue_growth"))
        gm_ok       = _safe_bool(stock_data.get("gross_margin_ok"), default=True)
        om_ok       = _safe_bool(stock_data.get("operating_margin_ok"), default=True)
        rev_decline = _safe_bool(stock_data.get("revenue_declining"))

        # EPS 年增明顯: +10
        if eps_growth is not None and eps_growth > 0 and not eps_decline:
            score += 10
            bullish.append(f"EPS年增 {eps_growth:.1f}%")

        # Q1 EPS × 4 後本益比仍合理: +8
        if q1_eps is not None and q1_eps > 0:
            estimated = ann_eps if ann_eps else q1_eps * 4
            if price is not None and price > 0 and estimated > 0:
                pe_est = price / estimated
                if pe_est < 25:
                    score += 8
                    bullish.append(f"Q1×4估算PE {pe_est:.1f}倍，尚合理")
            elif estimated > 0:
                score += 5
                bullish.append("Q1 EPS正成長")

        # 月營收續強: +8
        if rev_growth:
            rev_score += 8
            bullish.append("月營收續強")

        # 毛利率未惡化: partial
        if gm_ok:
            rev_score += 4
            bullish.append("毛利率未惡化")

        # 營益率未惡化: partial
        if om_ok:
            rev_score += 3
            bullish.append("營益率未惡化")

        # Cap at ceiling
        score     = min(score,     _W_FUNDAMENTAL)
        rev_score = min(rev_score, _W_REVENUE)

        return {
            "fundamental_score": score,
            "revenue_score":     rev_score,
            "bullish_reasons":   bullish,
        }

    # ------------------------------------------------------------------
    # Score: Technical (低位階 / 站回均線)
    # ------------------------------------------------------------------

    def score_technical(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score technical position up to _W_BASE (15) + _W_TECHNICAL (15).

        Keys read from stock_data:
            low_base           : bool  — 低位階
            bottom_reversal    : bool  — 底部翻多
            above_ma5          : bool  — 站上5日線
            above_ma10         : bool  — 站上10日線
            above_ma20         : bool  — 站上20日線
            above_ma60         : bool  — 站上60日線
            breakout_resistance: bool  — 突破下降壓力
            pullback_held_ma10 : bool  — 回測10日線不破
            pullback_held_ma5  : bool  — 回測5日線不破
            ma20_broken_3d     : bool  — 跌破20日線且3天站不回
            ma60_broken        : bool  — 跌破60日線
        """
        base_score = 0
        tech_score = 0
        bullish    = []

        low_base    = _safe_bool(stock_data.get("low_base"))
        bottom_rev  = _safe_bool(stock_data.get("bottom_reversal"))
        above_ma5   = _safe_bool(stock_data.get("above_ma5"))
        above_ma10  = _safe_bool(stock_data.get("above_ma10"))
        above_ma20  = _safe_bool(stock_data.get("above_ma20"))
        above_ma60  = _safe_bool(stock_data.get("above_ma60"))
        breakout    = _safe_bool(stock_data.get("breakout_resistance"))
        pb_ma10     = _safe_bool(stock_data.get("pullback_held_ma10"))
        pb_ma5      = _safe_bool(stock_data.get("pullback_held_ma5"))
        ma20_broken = _safe_bool(stock_data.get("ma20_broken_3d"))
        ma60_broken = _safe_bool(stock_data.get("ma60_broken"))

        # 低位階: +8
        if low_base:
            base_score += 8
            bullish.append("低位階")
        # 底部翻多: +7
        if bottom_rev:
            base_score += 7
            bullish.append("底部翻多")

        # 站上5/10/20日線: +8
        ma_count = sum([above_ma5, above_ma10, above_ma20])
        if ma_count >= 3:
            tech_score += 8
            bullish.append("站上5/10/20日線")
        elif ma_count >= 2:
            tech_score += 5
            bullish.append("站上多條均線")
        elif ma_count >= 1:
            tech_score += 2

        # 回測10日線不破: +8
        if pb_ma10:
            tech_score += 8
            bullish.append("回測10日線不破")
        elif pb_ma5:
            tech_score += 4
            bullish.append("回測5日線不破")

        # 突破下降壓力: +8
        if breakout:
            tech_score += 8
            bullish.append("突破下降壓力線")

        # 站上60日線 bonus
        if above_ma60:
            tech_score += 3
            bullish.append("站上60日線")

        # Deduct for broken MAs (handled in deductions, but cap accordingly)
        if ma20_broken or ma60_broken:
            tech_score = max(0, tech_score - 5)

        base_score = min(base_score, _W_BASE)
        tech_score = min(tech_score, _W_TECHNICAL)

        return {
            "base_score":      base_score,
            "technical_score": tech_score,
            "bullish_reasons": bullish,
        }

    # ------------------------------------------------------------------
    # Score: Chip / Institutional (籌碼)
    # ------------------------------------------------------------------

    def score_chip(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score chip / institutional support up to _W_CHIP (15).

        Keys read from stock_data:
            institutional_selling  : bool  — 法人連續大賣
            institutional_buying   : bool  — 投信續買
            major_holder_up        : bool  — 大戶增加
            retail_holder_down     : bool  — 散戶減少
            margin_surge           : bool  — 融資暴增
            retail_chasing_high    : bool  — 散戶大量追高
            institutional_unloading: bool  — 法人開始調節
        """
        score   = 0
        bullish = []

        inst_sell   = _safe_bool(stock_data.get("institutional_selling"))
        inst_buy    = _safe_bool(stock_data.get("institutional_buying"))
        major_up    = _safe_bool(stock_data.get("major_holder_up"))
        retail_down = _safe_bool(stock_data.get("retail_holder_down"))
        margin_surge= _safe_bool(stock_data.get("margin_surge"))
        retail_chase= _safe_bool(stock_data.get("retail_chasing_high"))
        inst_unload = _safe_bool(stock_data.get("institutional_unloading"))

        # 法人未連續大賣: +8
        if not inst_sell:
            score += 8
            bullish.append("法人未連續大賣")

        # 投信續買: +4
        if inst_buy:
            score += 4
            bullish.append("投信續買")

        # 大戶增加、散戶下降: +6
        if major_up and retail_down:
            score += 6
            bullish.append("大戶增加、散戶下降")
        elif major_up:
            score += 3
            bullish.append("大戶持股增加")

        # 融資未暴增: +5 (deducted in deductions if surged)
        if not margin_surge:
            score += 5
            bullish.append("融資未暴增")

        # Penalty adjustments (partial, main in deductions)
        if retail_chase or inst_unload:
            score = max(0, score - 3)

        score = min(score, _W_CHIP)

        return {
            "chip_score":      score,
            "bullish_reasons": bullish,
        }

    # ------------------------------------------------------------------
    # Score: Risk health
    # ------------------------------------------------------------------

    def score_risk(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score risk health up to _W_RISK (10).

        Keys read from stock_data:
            no_margin          : bool  — 不融資
            position_diversified: bool — 持股分散
            not_chasing_news   : bool  — 未追新聞熱點
        """
        score      = 0
        risk_reasons = []

        no_margin   = _safe_bool(stock_data.get("no_margin"), default=True)
        diversified = _safe_bool(stock_data.get("position_diversified"), default=True)
        no_news     = _safe_bool(stock_data.get("not_chasing_news"), default=True)

        if no_margin:
            score += 5
        else:
            risk_reasons.append("使用融資，風險上升")

        if diversified:
            score += 3
        else:
            risk_reasons.append("持股過度集中")

        if no_news:
            score += 2
        else:
            risk_reasons.append("追新聞熱點，風險上升")

        score = min(score, _W_RISK)

        return {
            "risk_score":    score,
            "risk_reasons":  risk_reasons,
        }

    # ------------------------------------------------------------------
    # Deductions (避雷扣分, capped at _MAX_DEDUCT)
    # ------------------------------------------------------------------

    def _score_deductions(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply deduction conditions. Total capped at _MAX_DEDUCT (30).

        Deduction items per spec:
            高檔爆量長上影          : -10
            KD/RSI過熱且放量轉弱    : -8
            法人轉賣                : -8
            融資暴增                : -8
            大盤創高但個股不過前高   : -10
            EPS衰退                 : -12
            營收衰退                : -10
            跌破20日線且3天站不回   : -12
            跌破60日線              : -15
            M頭/多重頂/頭肩頂/弧形頂: -15
        """
        deduction   = 0
        risk_reasons = []

        high_volume_upper_shadow = _safe_bool(stock_data.get("high_volume_upper_shadow"))
        kd_rsi_hot               = _safe_bool(stock_data.get("kd_rsi_overbought_with_reversal"))
        inst_turning_sell        = _safe_bool(stock_data.get("institutional_unloading"))
        margin_surge             = _safe_bool(stock_data.get("margin_surge"))
        market_high_stock_lag    = _safe_bool(stock_data.get("market_new_high_stock_lags"))
        eps_declining            = _safe_bool(stock_data.get("eps_declining"))
        rev_declining            = _safe_bool(stock_data.get("revenue_declining"))
        ma20_broken_3d           = _safe_bool(stock_data.get("ma20_broken_3d"))
        ma60_broken              = _safe_bool(stock_data.get("ma60_broken"))
        top_pattern              = _safe_bool(stock_data.get("top_pattern"))

        if high_volume_upper_shadow:
            deduction += 10
            risk_reasons.append("高檔爆量長上影 (-10)")
        if kd_rsi_hot:
            deduction += 8
            risk_reasons.append("KD/RSI過熱且放量轉弱 (-8)")
        if inst_turning_sell:
            deduction += 8
            risk_reasons.append("法人轉賣 (-8)")
        if margin_surge:
            deduction += 8
            risk_reasons.append("融資暴增 (-8)")
        if market_high_stock_lag:
            deduction += 10
            risk_reasons.append("大盤創高但個股不過前高 (-10)")
        if eps_declining:
            deduction += 12
            risk_reasons.append("EPS衰退 (-12)")
        if rev_declining:
            deduction += 10
            risk_reasons.append("營收衰退 (-10)")
        if ma20_broken_3d:
            deduction += 12
            risk_reasons.append("跌破20日線且3天站不回 (-12)")
        if ma60_broken:
            deduction += 15
            risk_reasons.append("跌破60日線 (-15)")
        if top_pattern:
            deduction += 15
            risk_reasons.append("M頭/多重頂/頭肩頂/弧形頂 (-15)")

        return {
            "total_deduction": min(deduction, _MAX_DEDUCT),
            "risk_reasons":    risk_reasons,
        }

    # ------------------------------------------------------------------
    # Scenario classification
    # ------------------------------------------------------------------

    def classify_scenario(self, stock_data: Dict[str, Any]) -> str:
        """
        Classify into one of three scenario archetypes.

        Scenario A: 財報好 + 低位階 + 技術翻多
        Scenario B: 財報好，但已大漲
        Scenario C: 財報差 + 大盤創高但個股不過高
        """
        eps_growth  = _safe_float(stock_data.get("eps_yoy_growth"))
        rev_growth  = _safe_bool(stock_data.get("revenue_growth"))
        eps_decline = _safe_bool(stock_data.get("eps_declining"))
        low_base    = _safe_bool(stock_data.get("low_base"))
        bottom_rev  = _safe_bool(stock_data.get("bottom_reversal"))
        breakout    = _safe_bool(stock_data.get("breakout_resistance"))
        above_ma5   = _safe_bool(stock_data.get("above_ma5"))
        above_ma20  = _safe_bool(stock_data.get("above_ma20"))
        no_inst_sell= not _safe_bool(stock_data.get("institutional_selling"))
        no_margin   = not _safe_bool(stock_data.get("margin_surge"))

        # Extended / chased signals
        extended        = _safe_bool(stock_data.get("price_extended"))
        high_vol_shadow = _safe_bool(stock_data.get("high_volume_upper_shadow"))
        kd_hot          = _safe_bool(stock_data.get("kd_rsi_overbought_with_reversal"))
        retail_chase    = _safe_bool(stock_data.get("retail_chasing_high"))
        inst_unload     = _safe_bool(stock_data.get("institutional_unloading"))
        ma5_broken_vol  = _safe_bool(stock_data.get("ma5_broken_with_volume"))

        # Weakness signals
        market_lag   = _safe_bool(stock_data.get("market_new_high_stock_lags"))
        rev_decline  = _safe_bool(stock_data.get("revenue_declining"))
        ma20_broken  = _safe_bool(stock_data.get("ma20_broken_3d"))
        ma60_broken  = _safe_bool(stock_data.get("ma60_broken"))
        top_pattern  = _safe_bool(stock_data.get("top_pattern"))

        fundamental_good = (
            (eps_growth is not None and eps_growth > 0 and not eps_decline)
            or rev_growth
        )
        technical_bullish = (
            (low_base or bottom_rev)
            and (breakout or above_ma5 or above_ma20)
        )
        scenario_a_cond = (
            fundamental_good
            and technical_bullish
            and no_inst_sell
            and no_margin
            and not extended
        )

        scenario_b_cond = (
            fundamental_good
            and extended
            and (high_vol_shadow or kd_hot or retail_chase or inst_unload or ma5_broken_vol)
        )

        scenario_c_cond = (
            (eps_decline or rev_decline)
            and (market_lag or ma20_broken or ma60_broken or top_pattern)
        )

        if scenario_a_cond:
            return SCENARIO_A
        if scenario_b_cond:
            return SCENARIO_B
        if scenario_c_cond:
            return SCENARIO_C
        return SCENARIO_UNKNOWN

    # ------------------------------------------------------------------
    # Labels
    # ------------------------------------------------------------------

    def _build_labels(self, scenario: str, stock_data: Dict[str, Any]) -> List[str]:
        """Build scenario-specific system labels."""
        labels: List[str] = []

        if scenario == SCENARIO_A:
            labels += [
                "FINANCIAL_TURNAROUND",
                "LOW_BASE_BREAKOUT",
                "SECOND_WAVE_CANDIDATE",
                "PULLBACK_ENTRY_ONLY",
            ]
        elif scenario == SCENARIO_B:
            labels += [
                "GOOD_FUNDAMENTAL_BUT_EXTENDED",
                "DO_NOT_CHASE",
                "TAKE_PROFIT_OR_REDUCE",
                "WAIT_PULLBACK",
            ]
        elif scenario == SCENARIO_C:
            labels += [
                "RELATIVE_WEAKNESS",
                "FUNDAMENTAL_DETERIORATION",
                "TOP_PATTERN_RISK",
                "AVOID_OR_ROTATE",
            ]

        return labels

    # ------------------------------------------------------------------
    # Entry / exit / avoid conditions (human-readable)
    # ------------------------------------------------------------------

    def _build_entry_conditions(self, stock_data: Dict[str, Any]) -> List[str]:
        conditions = []
        if _safe_bool(stock_data.get("revenue_growth")):
            conditions.append("月營收續強")
        eps_growth = _safe_float(stock_data.get("eps_yoy_growth"))
        if eps_growth is not None and eps_growth > 0:
            conditions.append(f"EPS年增 {eps_growth:.1f}%")
        if _safe_bool(stock_data.get("low_base")):
            conditions.append("低位階")
        if _safe_bool(stock_data.get("bottom_reversal")):
            conditions.append("底部翻多")
        if _safe_bool(stock_data.get("breakout_resistance")):
            conditions.append("突破下降壓力")
        if _safe_bool(stock_data.get("pullback_held_ma10")):
            conditions.append("回測10日線不破")
        if _safe_bool(stock_data.get("pullback_held_ma5")):
            conditions.append("回測5日線不破")
        if not _safe_bool(stock_data.get("institutional_selling")):
            conditions.append("法人未連續大賣")
        if not _safe_bool(stock_data.get("margin_surge")):
            conditions.append("融資未暴增")
        return conditions

    def _build_exit_conditions(self, stock_data: Dict[str, Any]) -> List[str]:
        conditions = []
        if _safe_bool(stock_data.get("ma20_broken_3d")):
            conditions.append("跌破20日線且3天站不回 → 減碼1/3～1/2")
        if _safe_bool(stock_data.get("ma60_broken")):
            conditions.append("跌破60日線 → 趨勢轉弱")
        if _safe_bool(stock_data.get("high_volume_upper_shadow")):
            conditions.append("高檔爆量長上影 → 考慮減碼")
        if _safe_bool(stock_data.get("institutional_unloading")):
            conditions.append("法人轉賣 → 降低持倉")
        if _safe_bool(stock_data.get("ma5_broken_with_volume")):
            conditions.append("跌破5日線且放量 → 先減碼")
        return conditions

    def _build_avoid_conditions(self, stock_data: Dict[str, Any]) -> List[str]:
        conditions = []
        if _safe_bool(stock_data.get("eps_declining")):
            conditions.append("EPS衰退")
        if _safe_bool(stock_data.get("revenue_declining")):
            conditions.append("營收衰退")
        if _safe_bool(stock_data.get("market_new_high_stock_lags")):
            conditions.append("大盤創高但個股不過前高")
        if _safe_bool(stock_data.get("top_pattern")):
            conditions.append("M頭/多重頂/頭肩頂/弧形頂")
        if _safe_bool(stock_data.get("retail_chasing_high")):
            conditions.append("散戶大量追高")
        if _safe_bool(stock_data.get("margin_surge")):
            conditions.append("融資暴增")
        return conditions

    # ------------------------------------------------------------------
    # Final decision
    # ------------------------------------------------------------------

    def build_decision(
        self,
        score: float,
        scenario: str,
        stock_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Map score + scenario to a suggested_action.

        [!] Output is NEVER 'BUY', 'SELL', or 'ORDER'.
        All valid actions: WATCH | WAIT_PULLBACK | SECOND_WAVE_CANDIDATE |
                           REDUCE_RISK | AVOID | ROTATE_TO_STRONGER
        """
        action: str

        if scenario == SCENARIO_A:
            if score >= _BAND_STRONG:
                action = ACTION_SECOND_WAVE
            elif score >= _BAND_WATCH:
                action = ACTION_WAIT_PULLBACK
            else:
                action = ACTION_WATCH
        elif scenario == SCENARIO_B:
            if _safe_bool(stock_data.get("ma5_broken_with_volume")):
                action = ACTION_REDUCE_RISK
            else:
                action = ACTION_WAIT_PULLBACK
        elif scenario == SCENARIO_C:
            action = ACTION_ROTATE
        else:
            # SCENARIO_UNKNOWN: use score band
            if score >= _BAND_STRONG:
                action = ACTION_WATCH
            elif score >= _BAND_WATCH:
                action = ACTION_WATCH
            elif score >= _BAND_NEUTRAL:
                action = ACTION_WATCH
            else:
                action = ACTION_AVOID

        assert action in _VALID_ACTIONS, f"Invalid action: {action}"

        return {
            "suggested_action": action,
            "score_band":       _score_band(score),
        }


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _safe_float(v: Any) -> Optional[float]:
    if v is None:
        return None
    try:
        import math
        f = float(v)
        return None if math.isnan(f) else f
    except (TypeError, ValueError):
        return None


def _safe_bool(v: Any, default: bool = False) -> bool:
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        return v.strip().lower() in ("true", "1", "yes")
    return default


def _score_band(score: float) -> str:
    if score >= _BAND_STRONG:
        return "STRONG_CANDIDATE"
    if score >= _BAND_WATCH:
        return "WATCH"
    if score >= _BAND_NEUTRAL:
        return "NEUTRAL"
    return "AVOID"
