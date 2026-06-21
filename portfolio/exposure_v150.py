"""
portfolio/exposure_v150.py — Portfolio Exposure Summary v1.5.0.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Descriptive exposure only. No optimal allocation.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional

_EXPOSURE_VERSION = "1.5.0"


class PortfolioExposureCalculator:
    """
    Calculates descriptive portfolio exposure.
    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] Unknown exposure not filled as zero.
    [!] Overlapping themes explicitly disclosed.
    """
    VERSION = _EXPOSURE_VERSION

    def calculate(
        self,
        position_valuations: List[Dict[str, Any]],
        cash_twd: Decimal,
        total_value: Decimal,
        classification_map: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Calculate exposure summary.
        classification_map: symbol -> {market, asset_type, industry, themes: [str]}
        """
        if total_value == Decimal("0"):
            return self._empty_exposure()

        classification_map = classification_map or {}
        securities_value = Decimal("0")
        listed_val = Decimal("0")
        otc_val = Decimal("0")
        etf_val = Decimal("0")
        equity_val = Decimal("0")
        unknown_val = Decimal("0")
        industry_exposure: Dict[str, Decimal] = {}
        theme_exposure: Dict[str, Decimal] = {}
        top_positions = []

        for pv in position_valuations:
            if pv.get("valuation_status") not in ("VALID",):
                continue
            symbol = pv.get("symbol", "")
            mkt_val = pv.get("market_value", Decimal("0")) or Decimal("0")
            weight = mkt_val / total_value
            securities_value += mkt_val

            clf = classification_map.get(symbol, {})
            market = clf.get("market", "UNKNOWN")
            asset_type = clf.get("asset_type", "UNKNOWN")
            industry = clf.get("industry", "UNKNOWN")
            themes = clf.get("themes", [])

            if market == "TWSE":
                listed_val += mkt_val
            elif market == "TPEX":
                otc_val += mkt_val
            else:
                unknown_val += mkt_val

            if asset_type == "ETF":
                etf_val += mkt_val
            elif asset_type == "COMMON_STOCK":
                equity_val += mkt_val
            elif asset_type == "UNKNOWN":
                unknown_val += mkt_val

            if industry and industry != "UNKNOWN":
                industry_exposure[industry] = industry_exposure.get(industry, Decimal("0")) + mkt_val
            # Themes: overlapping — not mutually exclusive
            for theme in themes:
                theme_exposure[theme] = theme_exposure.get(theme, Decimal("0")) + mkt_val

            top_positions.append({"symbol": symbol, "weight": weight, "market_value": mkt_val})

        top_positions.sort(key=lambda x: x["weight"], reverse=True)
        cash_weight = cash_twd / total_value
        equity_weight = equity_val / total_value
        etf_weight = etf_val / total_value
        listed_weight = listed_val / total_value
        otc_weight = otc_val / total_value
        unk_weight = unknown_val / total_value

        # Industry weights
        ind_weights = {k: v / total_value for k, v in industry_exposure.items()}
        theme_weights = {k: v / total_value for k, v in theme_exposure.items()}

        # Overlapping themes if sum > 1.0
        overlapping_themes = []
        theme_sum = sum(theme_weights.values())
        if theme_sum > Decimal("1.0"):
            overlapping_themes = list(theme_weights.keys())

        return {
            "gross_exposure": securities_value / total_value,
            "net_exposure": securities_value / total_value,
            "cash_weight": cash_weight,
            "equity_weight": equity_weight,
            "etf_weight": etf_weight,
            "listed_weight": listed_weight,
            "otc_weight": otc_weight,
            "unknown_weight": unk_weight,
            "top_positions": top_positions[:10],
            "industry_exposure": ind_weights,
            "theme_exposure": theme_weights,
            "overlapping_themes": overlapping_themes,
            "total_value": total_value,
        }

    def _empty_exposure(self) -> Dict[str, Any]:
        return {
            "gross_exposure": Decimal("0"), "net_exposure": Decimal("0"),
            "cash_weight": Decimal("0"), "equity_weight": Decimal("0"),
            "etf_weight": Decimal("0"), "listed_weight": Decimal("0"),
            "otc_weight": Decimal("0"), "unknown_weight": Decimal("0"),
            "top_positions": [], "industry_exposure": {},
            "theme_exposure": {}, "overlapping_themes": [],
            "total_value": Decimal("0"),
        }
