"""
analysis/fundamental_quality_analyzer.py - Fundamental quality / earnings guard.

Rules (老王教學: 財報 / 營收防呆):
- High revenue growth + unconfirmed gross margin/EPS → conservative score
- Price breaking MA20/MA60 before earnings → flag as pre-earnings weakness
- EPS <= 0 → disable PE river chart
- Gross margin declining + operating margin declining → deduct even if revenue grows
- Insufficient data → mark PARTIAL, do not produce formal long-term conclusion
- TODO: future API must use announcement_date to prevent data leakage

DATA LEAKAGE PREVENTION:
- All fundamental data must be pre-announcement data only.
- announcement_date enforcement is TODO pending API support.
- Until then, any fundamental score is PARTIAL / indicative only.
"""

import logging

import numpy as np

logger = logging.getLogger(__name__)


def analyze_fundamental_quality(
    symbol: str = "",
    monthly_revenue_rows: list = None,
    eps_ttm: float = None,
    eps_qoq_change: float = None,
    gross_margin: float = None,
    gross_margin_prev: float = None,
    operating_margin: float = None,
    operating_margin_prev: float = None,
    price_vs_ma20: float = None,
    price_vs_ma60: float = None,
) -> dict:
    """
    Evaluate fundamental data quality and flag risks.

    Parameters
    ----------
    symbol : str
    monthly_revenue_rows : list of dict, optional
        Each row: {'revenue': float, 'yoy': float, 'mom': float}.
        Recent months first or last — function uses last 3 entries.
    eps_ttm : float, optional
        Trailing-12-month EPS. Positive = profitable.
    eps_qoq_change : float, optional
        EPS change vs prior quarter (decimal). Negative = deteriorating.
    gross_margin : float, optional
        Current gross margin (decimal). 0.40 = 40%.
    gross_margin_prev : float, optional
        Prior period gross margin for comparison.
    operating_margin : float, optional
        Current operating margin.
    operating_margin_prev : float, optional
        Prior period operating margin.
    price_vs_ma20 : float, optional
        (close - MA20) / MA20.  Negative = price below MA20.
    price_vs_ma60 : float, optional
        (close - MA60) / MA60.  Negative = price below MA60.

    Returns
    -------
    dict
        fundamental_quality_score    : float  0.0–1.0 (0=poor, 1=excellent)
        revenue_growth_signal        : str
        margin_quality_signal        : str
        eps_quality_signal           : str
        revenue_quality_warning      : str
        earnings_risk_warning        : str
        pre_earnings_price_warning   : str
        fundamental_quality_reason   : str
    """
    result = {
        "fundamental_quality_score":  0.5,   # neutral default
        "revenue_growth_signal":      "PARTIAL",
        "margin_quality_signal":      "PARTIAL",
        "eps_quality_signal":         "PARTIAL",
        "revenue_quality_warning":    "",
        "earnings_risk_warning":      "",
        "pre_earnings_price_warning": "",
        "fundamental_quality_reason": "",
    }

    warnings  = []
    reasons   = []
    score     = 0.5
    has_data  = False

    # ── Revenue analysis ─────────────────────────────────────────────────
    if monthly_revenue_rows and len(monthly_revenue_rows) >= 3:
        has_data = True
        recent = monthly_revenue_rows[-3:]
        yoy_values = [r.get("yoy") for r in recent if r.get("yoy") is not None]
        if yoy_values:
            avg_yoy = sum(yoy_values) / len(yoy_values)
            if avg_yoy > 0.15:
                score += 0.15
                reasons.append(f"近3月均YoY {avg_yoy:.1%}，營收成長強")
                result["revenue_growth_signal"] = "STRONG"
            elif avg_yoy > 0.05:
                score += 0.05
                result["revenue_growth_signal"] = "MODERATE"
            elif avg_yoy < -0.10:
                score -= 0.15
                warnings.append("營收年增率連續負值，基本面惡化")
                result["revenue_growth_signal"] = "DECLINING"
            else:
                result["revenue_growth_signal"] = "FLAT"

            # Revenue quality warning: high revenue but margin not confirmed
            if avg_yoy > 0.15 and gross_margin is None:
                warnings.append("月營收高成長但毛利率未確認，不可給高分")
                result["revenue_quality_warning"] = (
                    "月營收年增高，但毛利率 / EPS 未確認，估值分數保守"
                )
        else:
            result["revenue_growth_signal"] = "PARTIAL"
    else:
        result["revenue_growth_signal"] = "UNAVAILABLE"

    # ── EPS / profitability ───────────────────────────────────────────────
    if eps_ttm is not None:
        has_data = True
        if eps_ttm > 0:
            score += 0.1
            result["eps_quality_signal"] = "POSITIVE"
            reasons.append(f"EPS TTM = {eps_ttm:.2f} > 0")
        else:
            score -= 0.2
            warnings.append("EPS <= 0，不可使用本益比河流圖，嚴禁正式長線估值")
            result["eps_quality_signal"]  = "NEGATIVE"
            result["earnings_risk_warning"] = "EPS <= 0 或公司虧損，禁止 PE 估值"

        if eps_qoq_change is not None and eps_qoq_change < -0.1:
            score -= 0.1
            warnings.append(f"EPS 季減 {eps_qoq_change:.1%}，獲利惡化中")
            result["earnings_risk_warning"] = (
                result.get("earnings_risk_warning", "")
                + f"；EPS 季減 {eps_qoq_change:.1%}"
            ).lstrip("；")
    else:
        result["eps_quality_signal"] = "UNAVAILABLE"

    # ── Margin quality ────────────────────────────────────────────────────
    margin_ok = True
    if gross_margin is not None:
        has_data = True
        if gross_margin_prev is not None:
            if gross_margin < gross_margin_prev - 0.02:
                score -= 0.1
                warnings.append(
                    f"毛利率下滑 {(gross_margin - gross_margin_prev):.1%}，"
                    "即使營收成長也需扣分"
                )
                margin_ok = False
                result["margin_quality_signal"] = "DECLINING"
            elif gross_margin > gross_margin_prev + 0.02:
                score += 0.1
                result["margin_quality_signal"] = "IMPROVING"
            else:
                result["margin_quality_signal"] = "STABLE"
        else:
            result["margin_quality_signal"] = "PARTIAL"
    else:
        result["margin_quality_signal"] = "UNAVAILABLE"

    if operating_margin is not None and operating_margin_prev is not None:
        if operating_margin < operating_margin_prev - 0.02:
            score -= 0.05
            warnings.append("營業利益率下滑，獲利品質需留意")

    # ── Pre-earnings price weakness ───────────────────────────────────────
    pre_warn_parts = []
    if price_vs_ma20 is not None and price_vs_ma20 < -0.03:
        pre_warn_parts.append("股價跌破 MA20")
    if price_vs_ma60 is not None and price_vs_ma60 < -0.03:
        pre_warn_parts.append("股價跌破 MA60")
    if pre_warn_parts:
        result["pre_earnings_price_warning"] = (
            "財報前 " + " / ".join(pre_warn_parts) + "，標示「財報前價格先轉弱」風險；"
            "TODO: 須使用 announcement_date 防止資料穿越"
        )
        score -= 0.05
        warnings.append(result["pre_earnings_price_warning"])

    # ── Data leakage TODO note ────────────────────────────────────────────
    reasons.append(
        "TODO: 未來 API 須用 announcement_date 確認財報資料時間，本階段為 PARTIAL 指示性判斷"
    )

    # ── Final score clamp ─────────────────────────────────────────────────
    if not has_data:
        score = 0.5
        result["fundamental_quality_reason"] = "缺基本面資料，顯示 PARTIAL，不硬算正式長線結論"
    else:
        result["fundamental_quality_reason"] = (
            "；".join(reasons + warnings) if (reasons or warnings) else "基本面無異常"
        )

    result["fundamental_quality_score"] = round(max(0.0, min(1.0, score)), 3)
    return result
