"""
portfolio/sizing/weight_cap_v151.py — Weight Cap Constraint v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Single-name cap: (current_value + incremental_value) / portfolio_value <= max_weight
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional

RESEARCH_ONLY = True


class WeightCapConstraint:
    """
    Caps incremental quantity so total position weight stays <= max_weight.
    Blocks if portfolio_value is None or 0.
    """

    RESEARCH_ONLY = True

    def apply(
        self,
        request,
        raw_quantity: Decimal,
        policy,
        max_weight: Optional[Decimal] = None,
        constraint_label: str = "SINGLE_NAME_LIMIT",
    ) -> Dict[str, Any]:
        pv: Optional[Decimal] = request.portfolio_value
        entry: Optional[Decimal] = request.planned_entry_price or request.reference_price
        current_value: Decimal = request.current_market_value or Decimal("0")

        if pv is None or pv <= Decimal("0"):
            return {
                "capped_quantity": Decimal("0"),
                "applied": True,
                "reason": "BLOCKED_NO_PORTFOLIO_VALUE: portfolio_value required for weight cap",
                "severity": "BLOCKING",
                "research_only": True,
            }

        if entry is None or entry <= Decimal("0"):
            return {
                "capped_quantity": raw_quantity,
                "applied": False,
                "reason": "MISSING_ENTRY_PRICE: cannot compute weight cap without price",
                "severity": "WARNING",
                "research_only": True,
            }

        cap = max_weight if max_weight is not None else policy.max_single_position_weight
        max_total_value = pv * cap
        room = max_total_value - current_value
        if room <= Decimal("0"):
            return {
                "capped_quantity": Decimal("0"),
                "applied": True,
                "reason": f"{constraint_label}_BLOCKED: current_value={current_value} already at cap={cap}",
                "severity": "BLOCKING",
                "research_only": True,
            }

        max_qty = (room / entry).quantize(Decimal("1"), rounding="ROUND_DOWN")
        if raw_quantity > max_qty:
            return {
                "capped_quantity": max_qty,
                "applied": True,
                "reason": (
                    f"{constraint_label}: raw={raw_quantity} > weight_max={max_qty} "
                    f"(cap={cap}, pv={pv}, current={current_value})"
                ),
                "severity": "HARD_CAP",
                "research_only": True,
            }

        return {
            "capped_quantity": raw_quantity,
            "applied": False,
            "reason": f"{constraint_label}_OK",
            "severity": "INFO",
            "research_only": True,
        }
