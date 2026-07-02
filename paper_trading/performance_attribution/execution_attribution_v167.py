"""
paper_trading/performance_attribution/execution_attribution_v167.py
Execution attribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] All executions are SIMULATED. Must be marked simulated. No real order. No broker.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import (
    AttributionLevel, AttributionStatus, ConfidenceLevel, ExecutionQuality,
)
from .models_v167 import ExecutionContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den != 0.0 else default


class ExecutionAttributionEngine:
    """
    Execution attribution: implementation shortfall, slippage, spread, fill quality.
    All paper executions must be marked simulated with model_version + slippage_policy.
    """

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        fill_price: float,
        signal_price: Optional[float],
        decision_price: Optional[float],
        order_price: Optional[float],
        close_price: Optional[float],
        vwap: Optional[float],
        twap: Optional[float],
        quantity: float,
        direction: int,                  # +1 long, -1 short
        filled_quantity: float,
        ordered_quantity: float,
        model_version: str = "",
        slippage_policy: str = "",
        liquidity_assumption: str = "",
        price_reference: str = "",
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> ExecutionContribution:
        """
        Compute execution attribution.
        implementation_shortfall = (fill - decision) * qty * direction
        """
        # IS = fill price vs decision price (primary)
        ref_price = decision_price or signal_price or order_price or close_price or fill_price
        impl_shortfall = (fill_price - ref_price) * quantity * direction

        # Delay cost: signal to decision
        delay_cost = 0.0
        if signal_price and decision_price:
            delay_cost = (decision_price - signal_price) * quantity * direction

        # Spread cost estimate
        spread_cost = 0.0
        if close_price and close_price > 0:
            bid_ask_estimate = close_price * 0.001  # 10 bps spread estimate
            spread_cost = bid_ask_estimate * quantity * 0.5

        # Slippage vs reference
        slippage = 0.0
        if vwap and vwap > 0:
            slippage = (fill_price - vwap) * quantity * direction
        elif close_price and close_price > 0:
            slippage = (fill_price - close_price) * quantity * direction

        # Adverse selection proxy
        adverse_selection = max(0.0, slippage * 0.3)

        # Fill ratio
        fill_ratio = _safe_div(filled_quantity, ordered_quantity, default=0.0)
        unfilled_qty = max(0.0, ordered_quantity - filled_quantity)

        # Partial fill impact
        partial_fill_impact = 0.0
        if unfilled_qty > 0 and close_price:
            partial_fill_impact = -(unfilled_qty * abs(close_price - fill_price))

        # Unfilled opportunity cost
        unfilled_opportunity = 0.0
        if unfilled_qty > 0 and close_price and fill_price:
            unfilled_opportunity = -(unfilled_qty * abs(close_price - fill_price))

        # Execution quality
        if fill_ratio >= 0.99 and abs(impl_shortfall) < abs(ref_price * quantity * 0.001):
            qual = ExecutionQuality.EXCELLENT
        elif fill_ratio >= 0.95:
            qual = ExecutionQuality.GOOD
        elif fill_ratio >= 0.80:
            qual = ExecutionQuality.NEUTRAL
        elif fill_ratio >= 0.50:
            qual = ExecutionQuality.POOR
        else:
            qual = ExecutionQuality.VERY_POOR

        confidence = ConfidenceLevel.HIGH if decision_price else ConfidenceLevel.MEDIUM
        if not vwap and not close_price:
            confidence = ConfidenceLevel.LOW

        return ExecutionContribution(
            entity_id=entity_id,
            level=level,
            implementation_shortfall=impl_shortfall,
            delay_cost=delay_cost,
            spread_cost=spread_cost,
            slippage=slippage,
            adverse_selection_proxy=adverse_selection,
            partial_fill_impact=partial_fill_impact,
            unfilled_opportunity_cost=unfilled_opportunity,
            fill_ratio=fill_ratio,
            simulated=True,
            model_version=model_version,
            slippage_policy=slippage_policy,
            liquidity_assumption=liquidity_assumption,
            confidence=confidence,
            status=AttributionStatus.COMPLETE,
            source_lineage=source_lineage,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )
