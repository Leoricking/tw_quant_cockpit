"""
portfolio/sizing/fixed_fractional_v151.py — Fixed Fractional Sizer v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Formula: risk_amount = portfolio_value × risk_per_trade_percent
         quantity = risk_amount / (entry - stop)
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional

RESEARCH_ONLY = True


class FixedFractionalSizer:
    """
    Fixed fractional position sizing.
    Blocks if stop_distance <= 0 or stop >= entry.
    """

    RESEARCH_ONLY = True

    def calculate(self, request, policy) -> Dict[str, Any]:
        """
        Returns dict with keys:
            raw_quantity, risk_amount, risk_per_share, stop_distance,
            method, blocked, blocker_reason
        """
        entry: Optional[Decimal] = request.planned_entry_price or request.reference_price
        stop: Optional[Decimal] = request.stop_price
        pv: Optional[Decimal] = request.portfolio_value
        rp: Optional[Decimal] = getattr(request, "risk_budget_percent", None) or policy.risk_per_trade_percent

        # Guard: missing required fields
        if entry is None:
            return self._blocked("MISSING_ENTRY_PRICE: planned_entry_price is required", Decimal("0"))
        if stop is None:
            return self._blocked("MISSING_STOP_PRICE: stop_price is required", Decimal("0"))
        if pv is None or pv <= Decimal("0"):
            return self._blocked("MISSING_PORTFOLIO_VALUE: portfolio_value is required and > 0", Decimal("0"))

        # Guard: invalid stop direction (long-only)
        if stop >= entry:
            return self._blocked(
                "BLOCKED_INVALID_STOP_DIRECTION: stop_price must be < entry_price for long-only",
                Decimal("0"),
            )

        stop_distance = entry - stop
        if stop_distance <= Decimal("0"):
            return self._blocked(
                "BLOCKED_ZERO_STOP_DISTANCE: stop_distance must be > 0",
                Decimal("0"),
            )

        risk_amount = pv * rp
        raw_quantity = risk_amount / stop_distance
        # Floor to integer shares
        raw_quantity = raw_quantity.quantize(Decimal("1"), rounding="ROUND_DOWN")

        return {
            "raw_quantity": raw_quantity,
            "risk_amount": risk_amount,
            "risk_per_share": stop_distance,
            "stop_distance": stop_distance,
            "stop_distance_percent": stop_distance / entry,
            "method": "FIXED_FRACTIONAL",
            "blocked": False,
            "blocker_reason": "",
            "research_only": True,
        }

    @staticmethod
    def _blocked(reason: str, qty: Decimal) -> Dict[str, Any]:
        return {
            "raw_quantity": qty,
            "risk_amount": Decimal("0"),
            "risk_per_share": Decimal("0"),
            "stop_distance": Decimal("0"),
            "stop_distance_percent": Decimal("0"),
            "method": "FIXED_FRACTIONAL",
            "blocked": True,
            "blocker_reason": reason,
            "research_only": True,
        }
