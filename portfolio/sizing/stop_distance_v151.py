"""
portfolio/sizing/stop_distance_v151.py — Stop Distance Sizer v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Supports absolute stop and percentage stop.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional

RESEARCH_ONLY = True


class StopDistanceSizer:
    """
    Stop-distance-based position sizing.
    Absolute stop: stop_price provided directly.
    Percentage stop: stop_percent = (entry - stop) / entry
    """

    RESEARCH_ONLY = True

    def calculate(self, request, policy) -> Dict[str, Any]:
        entry: Optional[Decimal] = request.planned_entry_price or request.reference_price
        stop: Optional[Decimal] = request.stop_price
        pv: Optional[Decimal] = request.portfolio_value
        rp: Optional[Decimal] = getattr(request, "risk_budget_percent", None) or policy.risk_per_trade_percent

        if entry is None:
            return self._blocked("MISSING_ENTRY_PRICE")
        if pv is None or pv <= Decimal("0"):
            return self._blocked("MISSING_PORTFOLIO_VALUE")

        # Derive stop distance
        if stop is not None:
            if stop >= entry:
                return self._blocked(
                    "BLOCKED_INVALID_STOP_DIRECTION: stop_price must be < entry for long-only"
                )
            stop_distance = entry - stop
        else:
            # Fallback: use 2% stop if nothing provided
            stop_distance = entry * Decimal("0.02")
            stop = entry - stop_distance

        if stop_distance <= Decimal("0"):
            return self._blocked("BLOCKED_ZERO_STOP_DISTANCE")

        risk_amount = pv * rp
        raw_quantity = (risk_amount / stop_distance).quantize(Decimal("1"), rounding="ROUND_DOWN")

        return {
            "raw_quantity": raw_quantity,
            "risk_amount": risk_amount,
            "stop_price": stop,
            "stop_distance": stop_distance,
            "stop_distance_percent": stop_distance / entry,
            "method": "STOP_DISTANCE",
            "blocked": False,
            "blocker_reason": "",
            "research_only": True,
        }

    @staticmethod
    def _blocked(reason: str) -> Dict[str, Any]:
        return {
            "raw_quantity": Decimal("0"),
            "risk_amount": Decimal("0"),
            "stop_price": None,
            "stop_distance": Decimal("0"),
            "stop_distance_percent": Decimal("0"),
            "method": "STOP_DISTANCE",
            "blocked": True,
            "blocker_reason": reason,
            "research_only": True,
        }
