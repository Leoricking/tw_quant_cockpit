"""
paper_trading/performance_attribution/trade_attribution_v167.py
Trade attribution for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import (
    AttributionLevel, AttributionStatus, ConfidenceLevel,
    TradeDirection, ExecutionQuality,
)

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den != 0.0 else default


class TradeAttributionEngine:
    """Per-trade attribution: side, fill, gross/net PnL, cost, slippage, timing, execution quality."""

    def compute(
        self,
        trade_id: str,
        symbol: str,
        direction: TradeDirection,
        quantity: float,
        signal_price: Optional[float],
        decision_price: Optional[float],
        fill_price: float,
        exit_price: Optional[float],
        cost_basis: float,
        commission: float = 0.0,
        transaction_tax: float = 0.0,
        slippage: float = 0.0,
        simulated: bool = True,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> Dict[str, Any]:
        """Compute per-trade attribution."""
        direction_sign = 1 if direction == TradeDirection.LONG else -1

        gross_pnl = (fill_price - cost_basis) * quantity * direction_sign
        if exit_price is not None:
            gross_pnl = (exit_price - fill_price) * quantity * direction_sign

        cost_total = commission + transaction_tax + slippage
        net_pnl = gross_pnl - cost_total

        # Timing: fill vs signal
        timing = 0.0
        if signal_price:
            timing = (fill_price - signal_price) * quantity * direction_sign

        # Implementation shortfall
        impl_shortfall = 0.0
        if decision_price:
            impl_shortfall = (fill_price - decision_price) * quantity * direction_sign

        # Execution quality
        if abs(slippage) < 0.0001 and abs(impl_shortfall) < abs(fill_price * quantity * 0.001):
            exec_quality = ExecutionQuality.EXCELLENT
        elif abs(slippage) < abs(fill_price * quantity * 0.002):
            exec_quality = ExecutionQuality.GOOD
        else:
            exec_quality = ExecutionQuality.NEUTRAL

        contribution = net_pnl

        return {
            "trade_id": trade_id,
            "symbol": symbol,
            "direction": direction.value,
            "quantity": quantity,
            "signal_price": signal_price,
            "decision_price": decision_price,
            "fill_price": fill_price,
            "exit_price": exit_price,
            "gross_pnl": gross_pnl,
            "net_pnl": net_pnl,
            "cost": cost_total,
            "commission": commission,
            "transaction_tax": transaction_tax,
            "slippage": slippage,
            "timing": timing,
            "implementation_shortfall": impl_shortfall,
            "execution_quality": exec_quality.value,
            "contribution": contribution,
            "simulated": simulated,
            "confidence": ConfidenceLevel.HIGH.value,
            "status": AttributionStatus.COMPLETE.value,
            "period_start": period_start,
            "period_end": period_end,
            "source_lineage": source_lineage,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        }
