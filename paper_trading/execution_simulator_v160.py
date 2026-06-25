"""paper_trading/execution_simulator_v160.py — Paper Execution Simulator v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY. NOT_A_REAL_ORDER.
Fill model: bid/ask + last price + volume + latency + slippage + liquidity.
No guaranteed fill on price touch. No future tick use. No intraday H/L backdating.
No fill when price data missing.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional, Tuple

from .enums_v160 import (
    PaperOrderSide, PaperOrderStatus, PaperOrderType,
    PaperFillStatus, SlippageModel, LatencyModel,
)
from .models_v160 import PaperMarketEvent, PaperOrder, PaperFill
from .slippage_model_v160 import compute_slippage
from .liquidity_model_v160 import LiquidityChecker
from .latency_model_v160 import LatencyAssumption, build_latency_assumption
from .partial_fill_v160 import compute_fill_quantities
from .paper_fill_v160 import create_paper_fill


@dataclass
class SimulationResult:
    filled: bool
    fill: Optional[PaperFill] = None
    new_order_status: Optional[PaperOrderStatus] = None
    block_reason: str = ""
    warning: str = ""
    assumption: str = ""


class PaperExecutionSimulator:
    """
    Simulates paper order fills from market events.
    Model disclosed: bid/ask spread + participation-based slippage + latency assumption.
    Does not guarantee fill on price touch alone.
    Does not use future ticks.
    """

    def __init__(
        self,
        slippage_model: SlippageModel = SlippageModel.FIXED_BPS,
        latency_model_id: str = "ZERO_DISCLOSED",
        fixed_bps: Decimal = Decimal("10"),
        max_participation: Decimal = Decimal("0.10"),
    ) -> None:
        self._slippage_model = slippage_model
        self._latency = build_latency_assumption(latency_model_id)
        self._fixed_bps = fixed_bps
        self._liquidity = LiquidityChecker()
        self._max_participation = max_participation

    def simulate(
        self,
        order: PaperOrder,
        event: PaperMarketEvent,
    ) -> SimulationResult:
        # Safety: no future event use
        if event.available_from > event.received_timestamp:
            return SimulationResult(
                filled=False,
                block_reason="FUTURE_EVENT_USE_BLOCKED",
            )

        # Require price
        last_price = event.price
        if last_price is None or last_price <= Decimal("0"):
            return SimulationResult(
                filled=False,
                block_reason="MISSING_PRICE — no fill without price data",
            )

        # Check order can be filled
        if order.status not in {PaperOrderStatus.QUEUED, PaperOrderStatus.PARTIALLY_FILLED}:
            return SimulationResult(
                filled=False,
                block_reason=f"order status {order.status.value} cannot be filled",
            )

        # Price condition check
        fill_eligible, price_reason = self._check_price_condition(order, last_price, event)
        if not fill_eligible:
            return SimulationResult(
                filled=False,
                block_reason=price_reason,
                assumption="PRICE_CONDITION_NOT_MET",
            )

        # Liquidity check
        liq = self._liquidity.check(
            order_quantity=order.remaining_quantity,
            available_volume=event.volume,
            max_participation=self._max_participation,
        )
        if liq.blocked:
            return SimulationResult(
                filled=False,
                block_reason=liq.block_reason,
                warning=liq.block_reason,
            )

        fill_qty = liq.fillable_quantity
        if fill_qty <= Decimal("0"):
            return SimulationResult(
                filled=False,
                block_reason="no fillable quantity",
                warning="ZERO_VOLUME_NO_FILL",
            )

        # Slippage
        slip_result = compute_slippage(
            model=self._slippage_model,
            side=order.side,
            price=last_price,
            quantity=fill_qty,
            bid=event.bid,
            ask=event.ask,
            volume=event.volume,
            fixed_bps=self._fixed_bps,
            max_participation=self._max_participation,
        )
        if slip_result.blocked:
            return SimulationResult(
                filled=False,
                block_reason=slip_result.block_reason,
            )

        fill_price = slip_result.adjusted_price

        # Compute fill quantities
        try:
            actual_fill, remaining_after, new_status, fill_status = compute_fill_quantities(
                order.quantity, order.filled_quantity, fill_qty
            )
        except ValueError as exc:
            return SimulationResult(
                filled=False,
                block_reason=str(exc),
            )

        fill = create_paper_fill(
            paper_order_id=order.paper_order_id,
            session_id=order.session_id,
            symbol=order.symbol,
            side=order.side,
            quantity=actual_fill,
            fill_price=fill_price,
            slippage=slip_result.slippage_amount,
            market_event_id=event.event_id,
            latency_assumption=self._latency.describe(),
            liquidity_assumption=liq.assumption,
        )

        return SimulationResult(
            filled=True,
            fill=fill,
            new_order_status=new_status,
            assumption=f"{slip_result.assumption} | {liq.assumption} | {self._latency.describe()}",
            warning=slip_result.warning,
        )

    def _check_price_condition(
        self,
        order: PaperOrder,
        last_price: Decimal,
        event: PaperMarketEvent,
    ) -> Tuple[bool, str]:
        if order.order_type == PaperOrderType.MARKET:
            return True, ""
        if order.order_type == PaperOrderType.LIMIT:
            if order.limit_price is None:
                return False, "LIMIT order missing limit_price"
            if order.side == PaperOrderSide.BUY and last_price <= order.limit_price:
                return True, ""
            if order.side == PaperOrderSide.SELL and last_price >= order.limit_price:
                return True, ""
            return False, f"LIMIT price condition not met: last={last_price} limit={order.limit_price}"
        if order.order_type == PaperOrderType.STOP:
            if order.stop_price is None:
                return False, "STOP order missing stop_price"
            if order.side == PaperOrderSide.BUY and last_price >= order.stop_price:
                return True, ""
            if order.side == PaperOrderSide.SELL and last_price <= order.stop_price:
                return True, ""
            return False, f"STOP trigger not reached: last={last_price} stop={order.stop_price}"
        if order.order_type == PaperOrderType.STOP_LIMIT:
            if order.stop_price is None or order.limit_price is None:
                return False, "STOP_LIMIT order missing stop_price or limit_price"
            triggered = (
                (order.side == PaperOrderSide.BUY and last_price >= order.stop_price) or
                (order.side == PaperOrderSide.SELL and last_price <= order.stop_price)
            )
            if not triggered:
                return False, "STOP_LIMIT stop not triggered"
            if order.side == PaperOrderSide.BUY and last_price <= order.limit_price:
                return True, ""
            if order.side == PaperOrderSide.SELL and last_price >= order.limit_price:
                return True, ""
            return False, "STOP_LIMIT limit condition not met after stop trigger"
        return False, f"unknown order type: {order.order_type}"
