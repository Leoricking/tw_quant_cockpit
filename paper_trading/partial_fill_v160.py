"""paper_trading/partial_fill_v160.py — Partial Fill Handler v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
"""
from __future__ import annotations
from decimal import Decimal
from typing import List, Tuple

from .enums_v160 import PaperOrderStatus, PaperFillStatus


def compute_fill_quantities(
    order_quantity: Decimal,
    already_filled: Decimal,
    new_fill: Decimal,
) -> Tuple[Decimal, Decimal, PaperOrderStatus, PaperFillStatus]:
    """
    Returns (fill_quantity, remaining_after, new_order_status, fill_status).
    Overfill is blocked.
    """
    remaining = order_quantity - already_filled
    if remaining <= Decimal("0"):
        raise ValueError("Order already fully filled — overfill blocked")
    if new_fill <= Decimal("0"):
        raise ValueError("Fill quantity must be positive")
    if new_fill > remaining:
        raise ValueError(f"Overfill blocked: trying to fill {new_fill}, only {remaining} remaining")

    actual_fill = new_fill
    remaining_after = remaining - actual_fill

    if remaining_after <= Decimal("0"):
        order_status = PaperOrderStatus.FILLED
        fill_status = PaperFillStatus.COMPLETE
    else:
        order_status = PaperOrderStatus.PARTIALLY_FILLED
        fill_status = PaperFillStatus.PARTIAL

    return actual_fill, remaining_after, order_status, fill_status


def is_overfill(order_quantity: Decimal, total_filled: Decimal) -> bool:
    return total_filled > order_quantity
