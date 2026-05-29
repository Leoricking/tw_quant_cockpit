"""
analysis/valuation_river_analyzer.py - PE river chart / valuation zone engine.

Based on: 20220601 本益比河流圖

Computes PE-based valuation zones and price targets.
Gracefully handles missing EPS or PE band data without crashing.
"""

import logging

import numpy as np

logger = logging.getLogger(__name__)

# Valuation zone constants
BELOW_HISTORICAL_LOW = "BELOW_HISTORICAL_LOW"
LOW_VALUE_ZONE       = "LOW_VALUE_ZONE"
FAIR_VALUE_ZONE      = "FAIR_VALUE_ZONE"
HIGH_VALUE_ZONE      = "HIGH_VALUE_ZONE"
OVERVALUED_ZONE      = "OVERVALUED_ZONE"
UNAVAILABLE          = "UNAVAILABLE"


def analyze_valuation_river(
    current_price: float,
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
) -> dict:
    """
    Compute PE river chart valuation zone and price targets.

    Parameters
    ----------
    current_price : float
        Latest close price.
    estimated_eps : float, optional
        Forward / estimated EPS (current fiscal year).  Preferred.
    trailing_eps : float, optional
        Last year actual EPS — used as fallback when estimated_eps is absent.
    pe_low, pe_mid, pe_high : float, optional
        Historical PE band: low / mid / high.
        Defaults to (12, 18, 25) if not provided.
    pe_extreme_low, pe_extreme_high : float, optional
        Historical PE extremes (absolute floor / ceiling).
        Defaults to (8, 35).
    revenue_growth : float, optional
        YoY revenue growth as decimal (0.15 = +15%).
    gross_margin : float, optional
        Gross margin as decimal (0.40 = 40%).
    eps_declining : bool
        True if current year EPS is lower than prior year.

    Returns
    -------
    dict
        valuation_zone     : str   one of the zone constants or "UNAVAILABLE"
        current_pe         : float | None
        estimated_eps      : float | None   (the EPS actually used)
        fair_value_price   : float | None   (eps × pe_mid)
        low_value_price    : float | None   (eps × pe_low)
        high_value_price   : float | None   (eps × pe_high)
        valuation_buy_zone : bool
        valuation_sell_zone: bool
        valuation_warning  : str
    """
    result = {
        "valuation_zone":     UNAVAILABLE,
        "current_pe":         None,
        "estimated_eps":      None,
        "fair_value_price":   None,
        "low_value_price":    None,
        "high_value_price":   None,
        "valuation_buy_zone":  False,
        "valuation_sell_zone": False,
        "valuation_warning":   "",
    }

    warnings = []

    # ── Choose EPS ─────────────────────────────────────────────────────────
    eps = estimated_eps
    if eps is None:
        eps = trailing_eps
        if eps is not None:
            warnings.append("僅使用過去 EPS，非正式估值，不得當作長線結論依據")

    if eps is None:
        warnings.append("缺 EPS 資料，無法計算 PE 估值")
        result["valuation_warning"] = "；".join(warnings)
        return result

    if eps <= 0:
        warnings.append("EPS <= 0 或公司虧損，不可使用 PE 河流圖估值")
        result["valuation_warning"] = "；".join(warnings)
        return result

    if eps_declining and trailing_eps and trailing_eps > eps:
        warnings.append(
            "今年 EPS 預估下降，已用較低 EPS 重估；"
            "不可引用去年高 EPS 推算目標價"
        )

    result["estimated_eps"] = round(eps, 2)

    # ── PE bands (with defaults) ─────────────────────────────────────────
    _pe_xl = pe_extreme_low  or  8.0
    _pe_lo = pe_low          or 12.0
    _pe_mi = pe_mid          or 18.0
    _pe_hi = pe_high         or 25.0
    _pe_xh = pe_extreme_high or 35.0

    # ── Price targets ────────────────────────────────────────────────────
    result["fair_value_price"] = round(eps * _pe_mi, 2)
    result["low_value_price"]  = round(eps * _pe_lo, 2)
    result["high_value_price"] = round(eps * _pe_hi, 2)

    # Bonus: expose the full band for callers that want them
    result["_pe_targets"] = {
        "extreme_low_price":  round(eps * _pe_xl, 2),
        "low_price":          round(eps * _pe_lo, 2),
        "mid_price":          round(eps * _pe_mi, 2),
        "high_price":         round(eps * _pe_hi, 2),
        "extreme_high_price": round(eps * _pe_xh, 2),
    }

    # ── Current PE ──────────────────────────────────────────────────────
    if current_price and current_price > 0:
        current_pe = current_price / eps
        result["current_pe"] = round(current_pe, 2)

        # Zone classification
        if current_pe < _pe_xl:
            zone = BELOW_HISTORICAL_LOW
        elif current_pe < _pe_lo:
            zone = LOW_VALUE_ZONE
        elif current_pe <= _pe_hi:
            zone = FAIR_VALUE_ZONE
        elif current_pe <= _pe_xh:
            zone = HIGH_VALUE_ZONE
        else:
            zone = OVERVALUED_ZONE

        result["valuation_zone"]      = zone
        result["valuation_buy_zone"]  = zone in (BELOW_HISTORICAL_LOW, LOW_VALUE_ZONE)
        result["valuation_sell_zone"] = zone in (HIGH_VALUE_ZONE, OVERVALUED_ZONE)

        if zone in (HIGH_VALUE_ZONE, OVERVALUED_ZONE):
            warnings.append("本益比位於高估區，不建議追高")
        if zone in (BELOW_HISTORICAL_LOW, LOW_VALUE_ZONE):
            warnings.append("本益比位於低估區，若基本面未惡化可列為長線觀察")

    # ── Fundamental context ──────────────────────────────────────────────
    if revenue_growth is not None and gross_margin is None:
        warnings.append("營收成長但毛利率 / EPS 未確認，估值分數保守")

    result["valuation_warning"] = "；".join(warnings) if warnings else ""
    return result
