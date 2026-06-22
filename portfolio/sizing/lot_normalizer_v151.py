"""
portfolio/sizing/lot_normalizer_v151.py — Lot Size Normalizer v1.5.1.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
Default: ROUND_DOWN (never up). Odd-lot rules respected.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, Optional

RESEARCH_ONLY = True


class LotNormalizer:
    """
    Normalizes raw_quantity to lot boundaries.
    - Default: ROUND_DOWN (floor to lot)
    - allow_odd_lot=False: floor to lot boundary
    - If result * reference_price < minimum_order_value: return 0
    """

    RESEARCH_ONLY = True

    def normalize(
        self,
        raw_quantity: Decimal,
        lot_size: int,
        allow_odd_lot: bool,
        minimum_order_value: Optional[Decimal],
        reference_price: Optional[Decimal],
    ) -> Dict[str, Any]:
        if lot_size <= 0:
            return {
                "normalized_quantity": Decimal("0"),
                "removed_by_rounding": raw_quantity,
                "odd_lot": False,
                "lot_size": lot_size,
                "reason": "INVALID_LOT_SIZE",
                "research_only": True,
            }

        lot_d = Decimal(str(lot_size))

        if allow_odd_lot:
            # Just floor to integer shares
            normalized = raw_quantity.quantize(Decimal("1"), rounding="ROUND_DOWN")
            odd_lot = (normalized % lot_d) != Decimal("0")
        else:
            # Floor to lot boundary
            normalized = (raw_quantity // lot_d) * lot_d
            odd_lot = False

        removed = raw_quantity - normalized

        # Minimum order value check
        if minimum_order_value is not None and reference_price is not None and reference_price > Decimal("0"):
            order_value = normalized * reference_price
            if order_value < minimum_order_value and normalized > Decimal("0"):
                return {
                    "normalized_quantity": Decimal("0"),
                    "removed_by_rounding": raw_quantity,
                    "odd_lot": False,
                    "lot_size": lot_size,
                    "reason": (
                        f"BELOW_MINIMUM_ORDER_VALUE: {order_value} < {minimum_order_value}"
                    ),
                    "research_only": True,
                }

        return {
            "normalized_quantity": normalized,
            "removed_by_rounding": removed,
            "odd_lot": odd_lot,
            "lot_size": lot_size,
            "reason": "OK",
            "research_only": True,
        }
