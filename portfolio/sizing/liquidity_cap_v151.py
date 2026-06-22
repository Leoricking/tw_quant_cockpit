"""
portfolio/sizing/liquidity_cap_v151.py — Liquidity Cap Constraint v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
estimated_order_value <= average_daily_value × participation_limit
Missing/stale liquidity: BLOCKED or WARNING.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional

RESEARCH_ONLY = True


class LiquidityCapConstraint:
    """
    Caps order quantity based on average daily value (ADV) participation limit.
    Stale or missing liquidity data → BLOCKED or WARNING depending on severity.
    """

    RESEARCH_ONLY = True

    def apply(self, request, raw_quantity: Decimal, policy) -> Dict[str, Any]:
        adv: Optional[Decimal] = request.average_daily_value
        entry: Optional[Decimal] = request.planned_entry_price or request.reference_price
        participation = (
            getattr(request, "liquidity_participation_limit", None)
            or policy.max_liquidity_participation
        )

        # PIT check for liquidity data
        adv_af = getattr(request, "average_daily_value_available_from", None)
        as_of = getattr(request, "as_of", None)
        if adv_af and as_of and adv_af > as_of:
            return {
                "capped_quantity": Decimal("0"),
                "applied": True,
                "reason": (
                    f"PIT_VIOLATION_LIQUIDITY: adv available_from={adv_af} > as_of={as_of}. "
                    "Future liquidity data not allowed."
                ),
                "severity": "BLOCKING",
                "research_only": True,
            }

        if adv is None:
            return {
                "capped_quantity": raw_quantity,
                "applied": False,
                "reason": "LIQUIDITY_UNKNOWN: average_daily_value not provided — WARNING",
                "severity": "WARNING",
                "research_only": True,
            }

        if adv <= Decimal("0"):
            return {
                "capped_quantity": Decimal("0"),
                "applied": True,
                "reason": "LIQUIDITY_BLOCKED: average_daily_value <= 0",
                "severity": "BLOCKING",
                "research_only": True,
            }

        if entry is None or entry <= Decimal("0"):
            return {
                "capped_quantity": raw_quantity,
                "applied": False,
                "reason": "LIQUIDITY_CAP_SKIP: entry_price unknown",
                "severity": "WARNING",
                "research_only": True,
            }

        max_order_value = adv * participation
        max_qty = (max_order_value / entry).quantize(Decimal("1"), rounding="ROUND_DOWN")

        if raw_quantity > max_qty:
            return {
                "capped_quantity": max_qty,
                "applied": True,
                "reason": (
                    f"LIQUIDITY_CAP: raw={raw_quantity} > liquidity_max={max_qty} "
                    f"(adv={adv}, participation={participation})"
                ),
                "severity": "HARD_CAP",
                "research_only": True,
            }

        return {
            "capped_quantity": raw_quantity,
            "applied": False,
            "reason": "LIQUIDITY_OK",
            "severity": "INFO",
            "research_only": True,
        }
