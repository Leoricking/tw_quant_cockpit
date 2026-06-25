"""paper_trading/liquidity_model_v160.py — Liquidity Model v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
Large paper orders check available volume. No guaranteed fill without liquidity check.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple


@dataclass
class LiquidityResult:
    available_volume: Decimal
    max_participation: Decimal
    fillable_quantity: Decimal
    remaining_quantity: Decimal
    partial_fill: bool
    stale_quote: bool = False
    zero_volume: bool = False
    suspended: bool = False
    price_limit_breached: bool = False
    blocked: bool = False
    block_reason: str = ""
    assumption: str = ""


class LiquidityChecker:
    """Check available liquidity for paper order fill simulation."""

    DEFAULT_MAX_PARTICIPATION = Decimal("0.10")  # 10% of volume

    def check(
        self,
        order_quantity: Decimal,
        available_volume: Optional[Decimal],
        is_suspended: bool = False,
        price: Optional[Decimal] = None,
        price_limit: Optional[Decimal] = None,
        stale: bool = False,
        max_participation: Optional[Decimal] = None,
    ) -> LiquidityResult:
        part = max_participation or self.DEFAULT_MAX_PARTICIPATION

        if is_suspended:
            return LiquidityResult(
                available_volume=Decimal("0"),
                max_participation=part,
                fillable_quantity=Decimal("0"),
                remaining_quantity=order_quantity,
                partial_fill=False,
                suspended=True,
                blocked=True,
                block_reason="symbol suspended — no fill",
            )

        if stale:
            return LiquidityResult(
                available_volume=Decimal("0"),
                max_participation=part,
                fillable_quantity=Decimal("0"),
                remaining_quantity=order_quantity,
                partial_fill=False,
                stale_quote=True,
                blocked=True,
                block_reason="stale quote — fill blocked",
            )

        if price_limit is not None and price is not None:
            if price > price_limit:
                return LiquidityResult(
                    available_volume=available_volume or Decimal("0"),
                    max_participation=part,
                    fillable_quantity=Decimal("0"),
                    remaining_quantity=order_quantity,
                    partial_fill=False,
                    price_limit_breached=True,
                    blocked=True,
                    block_reason=f"price {price} exceeds limit {price_limit}",
                )

        if available_volume is None or available_volume <= Decimal("0"):
            return LiquidityResult(
                available_volume=Decimal("0"),
                max_participation=part,
                fillable_quantity=Decimal("0"),
                remaining_quantity=order_quantity,
                partial_fill=False,
                zero_volume=True,
                assumption="ZERO_VOLUME_NO_FILL",
            )

        max_fill = available_volume * part
        if order_quantity <= max_fill:
            return LiquidityResult(
                available_volume=available_volume,
                max_participation=part,
                fillable_quantity=order_quantity,
                remaining_quantity=Decimal("0"),
                partial_fill=False,
                assumption=f"FULL_FILL_WITHIN_{float(part):.0%}_PARTICIPATION",
            )
        else:
            return LiquidityResult(
                available_volume=available_volume,
                max_participation=part,
                fillable_quantity=max_fill,
                remaining_quantity=order_quantity - max_fill,
                partial_fill=True,
                assumption=f"PARTIAL_FILL_{float(part):.0%}_PARTICIPATION_LIMIT",
            )
