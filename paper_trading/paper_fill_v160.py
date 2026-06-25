"""paper_trading/paper_fill_v160.py — Paper Fill Service v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY. NOT_A_REAL_ORDER.
"""
from __future__ import annotations
import hashlib
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from .enums_v160 import PaperFillStatus, PaperOrderSide
from .models_v160 import PaperFill


# Taiwan securities transaction tax: 0.3% on sell
_TW_TRANSACTION_TAX_SELL = Decimal("0.003")
# Brokerage fee (both sides): 0.1425%, capped by broker minimum
_TW_BROKERAGE_FEE_RATE = Decimal("0.001425")
_MIN_FEE = Decimal("20")  # TWD minimum commission


def compute_tw_costs(
    side: PaperOrderSide,
    quantity: Decimal,
    price: Decimal,
) -> tuple:
    """Returns (gross_amount, fee, tax, net_amount) — paper only, simplified."""
    gross = quantity * price
    fee = max(gross * _TW_BROKERAGE_FEE_RATE, _MIN_FEE)
    tax = gross * _TW_TRANSACTION_TAX_SELL if side == PaperOrderSide.SELL else Decimal("0")
    if side == PaperOrderSide.BUY:
        net = gross + fee
    else:
        net = gross - fee - tax
    return gross, fee, tax, net


def create_paper_fill(
    paper_order_id: str,
    session_id: str,
    symbol: str,
    side: PaperOrderSide,
    quantity: Decimal,
    fill_price: Decimal,
    slippage: Decimal = Decimal("0"),
    market_event_id: str = "",
    latency_assumption: str = "ZERO_DISCLOSED",
    liquidity_assumption: str = "PARTICIPATION",
    simulated_at: Optional[str] = None,
) -> PaperFill:
    gross, fee, tax, net = compute_tw_costs(side, quantity, fill_price)
    if simulated_at is None:
        simulated_at = datetime.now(timezone.utc).isoformat()
    fill_id = f"fill_{uuid.uuid4().hex[:12]}"
    return PaperFill(
        fill_id=fill_id,
        paper_order_id=paper_order_id,
        session_id=session_id,
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=fill_price,
        gross_amount=gross,
        fee=fee,
        tax=tax,
        slippage=slippage,
        net_amount=net,
        simulated_at=simulated_at,
        market_event_id=market_event_id,
        fill_status=PaperFillStatus.SIMULATED,
        liquidity_assumption=liquidity_assumption,
        latency_assumption=latency_assumption,
    )
