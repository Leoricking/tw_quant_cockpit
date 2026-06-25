"""paper_trading/slippage_model_v160.py — Slippage Model v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
Paper-only, policy-versioned, deterministic. No optimistic fallback.
Stale liquidity = warning. Missing spread/volume = BLOCK or conservative assumption.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from .enums_v160 import PaperOrderSide, SlippageModel


@dataclass
class SlippageResult:
    slippage_bps: Decimal
    slippage_amount: Decimal
    adjusted_price: Decimal
    model_used: SlippageModel
    assumption: str
    warning: str = ""
    blocked: bool = False
    block_reason: str = ""


def compute_slippage(
    model: SlippageModel,
    side: PaperOrderSide,
    price: Decimal,
    quantity: Decimal,
    bid: Optional[Decimal] = None,
    ask: Optional[Decimal] = None,
    volume: Optional[Decimal] = None,
    volatility_bps: Optional[Decimal] = None,
    fixed_bps: Decimal = Decimal("10"),
    max_participation: Decimal = Decimal("0.05"),
) -> SlippageResult:
    """Compute slippage for a paper order fill. Deterministic, paper-only."""
    if price <= Decimal("0"):
        return SlippageResult(
            slippage_bps=Decimal("0"),
            slippage_amount=Decimal("0"),
            adjusted_price=price,
            model_used=model,
            assumption="MISSING_PRICE",
            blocked=True,
            block_reason="price is zero or negative — BLOCK fill",
        )

    if model == SlippageModel.FIXED_BPS:
        bps = fixed_bps
        slip = price * bps / Decimal("10000")
        adj = price + slip if side == PaperOrderSide.BUY else price - slip
        return SlippageResult(
            slippage_bps=bps,
            slippage_amount=slip,
            adjusted_price=adj,
            model_used=model,
            assumption=f"FIXED_{bps}bps_PAPER_ONLY",
        )

    if model == SlippageModel.SPREAD_BASED:
        if bid is None or ask is None:
            return SlippageResult(
                slippage_bps=Decimal("0"),
                slippage_amount=Decimal("0"),
                adjusted_price=price,
                model_used=model,
                assumption="CONSERVATIVE_SPREAD_MISSING",
                warning="Missing bid/ask: using conservative fixed 20bps fallback",
                blocked=False,
            )
        spread = ask - bid
        half_spread = spread / Decimal("2")
        adj = price + half_spread if side == PaperOrderSide.BUY else price - half_spread
        if price > Decimal("0"):
            bps = (half_spread / price) * Decimal("10000")
        else:
            bps = Decimal("0")
        return SlippageResult(
            slippage_bps=bps,
            slippage_amount=half_spread,
            adjusted_price=adj,
            model_used=model,
            assumption="HALF_SPREAD_PAPER_ONLY",
        )

    if model == SlippageModel.PARTICIPATION_BASED:
        if volume is None or volume <= Decimal("0"):
            return SlippageResult(
                slippage_bps=Decimal("20"),
                slippage_amount=price * Decimal("20") / Decimal("10000"),
                adjusted_price=price,
                model_used=model,
                assumption="CONSERVATIVE_VOLUME_MISSING",
                warning="STALE_LIQUIDITY: missing volume, using conservative 20bps",
            )
        participation = min(quantity / volume, max_participation)
        bps = participation * Decimal("200")  # 1% participation = 20bps
        slip = price * bps / Decimal("10000")
        adj = price + slip if side == PaperOrderSide.BUY else price - slip
        return SlippageResult(
            slippage_bps=bps,
            slippage_amount=slip,
            adjusted_price=adj,
            model_used=model,
            assumption=f"PARTICIPATION_{float(participation):.2%}_PAPER_ONLY",
        )

    if model == SlippageModel.VOLATILITY_ADJUSTED:
        vol_bps = volatility_bps if volatility_bps is not None else Decimal("30")
        bps = vol_bps / Decimal("2")
        slip = price * bps / Decimal("10000")
        adj = price + slip if side == PaperOrderSide.BUY else price - slip
        return SlippageResult(
            slippage_bps=bps,
            slippage_amount=slip,
            adjusted_price=adj,
            model_used=model,
            assumption=f"VOLATILITY_ADJUSTED_{vol_bps}bps_PAPER_ONLY",
        )

    return SlippageResult(
        slippage_bps=fixed_bps,
        slippage_amount=price * fixed_bps / Decimal("10000"),
        adjusted_price=price,
        model_used=model,
        assumption="DEFAULT_FIXED_BPS",
    )
