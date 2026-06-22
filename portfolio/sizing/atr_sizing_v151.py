"""
portfolio/sizing/atr_sizing_v151.py — ATR-Based Sizer v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Blocks if atr <= 0, atr is None, or PIT violation (available_from > as_of).
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional

RESEARCH_ONLY = True

# Default: risk 1 ATR per unit of risk budget
ATR_MULTIPLIER_DEFAULT = Decimal("1")


class ATRSizer:
    """
    ATR-based position sizing.
    stop_distance = atr_multiplier * atr
    quantity = (portfolio_value * risk_percent) / stop_distance
    """

    RESEARCH_ONLY = True

    def __init__(self, atr_multiplier: Decimal = ATR_MULTIPLIER_DEFAULT):
        self.atr_multiplier = atr_multiplier

    def calculate(self, request, policy) -> Dict[str, Any]:
        atr: Optional[Decimal] = request.atr
        entry: Optional[Decimal] = request.planned_entry_price or request.reference_price
        pv: Optional[Decimal] = request.portfolio_value
        rp: Optional[Decimal] = getattr(request, "risk_budget_percent", None) or policy.risk_per_trade_percent

        # PIT check
        atr_af = getattr(request, "atr_available_from", None)
        as_of = getattr(request, "as_of", None)
        if atr_af and as_of and atr_af > as_of:
            return self._blocked(
                f"PIT_VIOLATION_ATR: atr available_from={atr_af} > as_of={as_of}"
            )

        # Missing / invalid ATR
        if atr is None:
            return self._blocked("MISSING_ATR: atr is required for ATR_BASED sizing")
        if atr <= Decimal("0"):
            return self._blocked("INVALID_ATR: atr must be > 0")

        if entry is None:
            return self._blocked("MISSING_ENTRY_PRICE")
        if pv is None or pv <= Decimal("0"):
            return self._blocked("MISSING_PORTFOLIO_VALUE")

        stop_distance = self.atr_multiplier * atr
        risk_amount = pv * rp
        raw_quantity = (risk_amount / stop_distance).quantize(Decimal("1"), rounding="ROUND_DOWN")

        return {
            "raw_quantity": raw_quantity,
            "risk_amount": risk_amount,
            "atr": atr,
            "stop_distance": stop_distance,
            "stop_distance_percent": stop_distance / entry if entry > Decimal("0") else Decimal("0"),
            "method": "ATR_BASED",
            "blocked": False,
            "blocker_reason": "",
            "research_only": True,
        }

    @staticmethod
    def _blocked(reason: str) -> Dict[str, Any]:
        return {
            "raw_quantity": Decimal("0"),
            "risk_amount": Decimal("0"),
            "atr": None,
            "stop_distance": Decimal("0"),
            "stop_distance_percent": Decimal("0"),
            "method": "ATR_BASED",
            "blocked": True,
            "blocker_reason": reason,
            "research_only": True,
        }
