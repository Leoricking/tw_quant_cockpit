"""
portfolio/walk_forward/cost_model_v154.py — Cost Model Engine v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
Uses Python Decimal for precision.
"""
from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, Optional

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
COST_MODEL_VERSION = "1.5.4"

ASSUMPTIONS = [
    "FIXED_RATE_APPLIED",
    "MINIMUM_FEE_ENFORCED",
    "TAX_APPLIED_ON_SELL_ONLY",
    "RESEARCH_ONLY_SIMULATION",
]


class CostModelEngine:
    """Apply cost model to simulated transactions. Uses Decimal for precision."""

    def __init__(self):
        self.version = COST_MODEL_VERSION

    def apply_buy_cost(self, value: float, policy) -> Decimal:
        """Apply buy-side fee. Minimum fee enforced."""
        if policy is None:
            return Decimal("0")
        v = Decimal(str(value))
        rate = Decimal(str(getattr(policy, "buy_fee_rate", 0.001425)))
        min_fee = Decimal(str(getattr(policy, "minimum_fee", 20.0)))
        fee = (v * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return max(fee, min_fee)

    def apply_sell_cost(self, value: float, policy) -> Decimal:
        """Apply sell-side fee. Minimum fee enforced."""
        if policy is None:
            return Decimal("0")
        v = Decimal(str(value))
        rate = Decimal(str(getattr(policy, "sell_fee_rate", 0.001425)))
        min_fee = Decimal(str(getattr(policy, "minimum_fee", 20.0)))
        fee = (v * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return max(fee, min_fee)

    def apply_tax(self, value: float, policy) -> Decimal:
        """Apply transaction tax (Taiwan: 0.3% on sell side)."""
        if policy is None:
            return Decimal("0")
        v = Decimal(str(value))
        rate = Decimal(str(getattr(policy, "tax_rate", 0.003)))
        return (v * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_assumptions(self) -> Dict[str, Any]:
        return {
            "assumptions": ASSUMPTIONS,
            "version": COST_MODEL_VERSION,
            "research_only": True,
        }

    def total_buy_cost(self, value: float, policy) -> Dict[str, Any]:
        fee = self.apply_buy_cost(value, policy)
        return {
            "fee": float(fee),
            "tax": 0.0,
            "total": float(fee),
            "assumptions": ASSUMPTIONS,
            "research_only": True,
        }

    def total_sell_cost(self, value: float, policy) -> Dict[str, Any]:
        fee = self.apply_sell_cost(value, policy)
        tax = self.apply_tax(value, policy)
        return {
            "fee": float(fee),
            "tax": float(tax),
            "total": float(fee + tax),
            "assumptions": ASSUMPTIONS,
            "research_only": True,
        }
