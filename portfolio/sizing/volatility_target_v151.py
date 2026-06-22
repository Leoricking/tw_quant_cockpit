"""
portfolio/sizing/volatility_target_v151.py — Volatility Target Sizer v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Research baseline only. NO covariance. NO optimization claim.
Blocks if volatility <= 0 or None.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional

RESEARCH_ONLY = True

# Disclaimer
DISCLAIMER = (
    "RESEARCH_BASELINE: Simplified volatility targeting. "
    "NO covariance matrix. NO portfolio optimization. "
    "NOT a proper vol-target optimizer. Research use only."
)


class VolatilityTargetSizer:
    """
    Simplified volatility target sizing.
    target_weight = risk_budget_percent / volatility
    quantity = (portfolio_value * target_weight) / entry_price
    """

    RESEARCH_ONLY = True

    def calculate(self, request, policy) -> Dict[str, Any]:
        volatility: Optional[Decimal] = request.volatility
        entry: Optional[Decimal] = request.planned_entry_price or request.reference_price
        pv: Optional[Decimal] = request.portfolio_value
        rp: Optional[Decimal] = getattr(request, "risk_budget_percent", None) or policy.risk_per_trade_percent

        if volatility is None:
            return self._blocked("MISSING_VOLATILITY: volatility is required for VOLATILITY_TARGET")
        if volatility <= Decimal("0"):
            return self._blocked("INVALID_VOLATILITY: volatility must be > 0")

        if entry is None:
            return self._blocked("MISSING_ENTRY_PRICE")
        if pv is None or pv <= Decimal("0"):
            return self._blocked("MISSING_PORTFOLIO_VALUE")

        target_weight = rp / volatility
        # Cap at max single position weight from policy
        max_w = policy.max_single_position_weight
        if target_weight > max_w:
            target_weight = max_w

        target_value = pv * target_weight
        raw_quantity = (target_value / entry).quantize(Decimal("1"), rounding="ROUND_DOWN")

        return {
            "raw_quantity": raw_quantity,
            "target_weight": target_weight,
            "target_value": target_value,
            "volatility": volatility,
            "risk_budget_percent": rp,
            "method": "VOLATILITY_TARGET",
            "disclaimer": DISCLAIMER,
            "blocked": False,
            "blocker_reason": "",
            "research_only": True,
        }

    @staticmethod
    def _blocked(reason: str) -> Dict[str, Any]:
        return {
            "raw_quantity": Decimal("0"),
            "target_weight": Decimal("0"),
            "target_value": Decimal("0"),
            "volatility": None,
            "risk_budget_percent": Decimal("0"),
            "method": "VOLATILITY_TARGET",
            "disclaimer": DISCLAIMER,
            "blocked": True,
            "blocker_reason": reason,
            "research_only": True,
        }
