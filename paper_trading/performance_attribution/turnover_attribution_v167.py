"""
paper_trading/performance_attribution/turnover_attribution_v167.py
Turnover attribution for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionLevel, AttributionStatus, ConfidenceLevel
from .models_v167 import TurnoverContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den != 0.0 else default


class TurnoverAttributionEngine:
    """Turnover attribution: rate, cost, drag."""

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        trades: List[Dict[str, Any]],
        begin_equity: float,
        cost_per_turn: float = 0.002,  # 20 bps round-trip default
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> TurnoverContribution:
        """
        Compute turnover attribution.
        turnover_rate = sum(abs(trade_value)) / avg_equity
        turnover_cost = turnover_rate * cost_per_turn
        """
        if begin_equity <= 0 or not trades:
            return TurnoverContribution(
                entity_id=entity_id,
                level=level,
                turnover_rate=0.0,
                turnover_cost=0.0,
                turnover_drag_bps=0.0,
                trade_count=0,
                avg_trade_size=0.0,
                confidence=ConfidenceLevel.UNKNOWN,
                status=AttributionStatus.INSUFFICIENT_DATA,
                source_lineage=source_lineage,
                period_start=period_start,
                period_end=period_end,
                paper_only=True,
                research_only=True,
                no_real_orders=True,
                not_for_production=True,
            )

        trade_values = [
            abs(t.get("fill_price", 0.0) * t.get("quantity", 0.0))
            for t in trades
        ]
        total_traded = sum(trade_values)
        turnover_rate = _safe_div(total_traded, begin_equity)
        turnover_cost = turnover_rate * cost_per_turn
        turnover_drag_bps = turnover_cost * 10_000
        avg_trade_size = _safe_div(total_traded, len(trades))

        return TurnoverContribution(
            entity_id=entity_id,
            level=level,
            turnover_rate=turnover_rate,
            turnover_cost=turnover_cost,
            turnover_drag_bps=turnover_drag_bps,
            trade_count=len(trades),
            avg_trade_size=avg_trade_size,
            confidence=ConfidenceLevel.HIGH,
            status=AttributionStatus.COMPLETE,
            source_lineage=source_lineage,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )
