"""
paper_trading/performance_attribution/position_attribution_v167.py
Position attribution for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionLevel, AttributionStatus, ConfidenceLevel, PositionState

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class PositionAttributionEngine:
    """Per-position attribution: open/close dates, realized/unrealized PnL, add-on/trim effects."""

    def compute(
        self,
        position_id: str,
        symbol: str,
        open_date: str,
        close_date: Optional[str],
        average_cost: float,
        current_price: float,
        quantity: float,
        state: PositionState,
        realized_pnl: float,
        unrealized_pnl: float,
        cost: float,
        risk_contribution: float,
        drawdown: float,
        add_on_trades: Optional[List[Dict[str, Any]]] = None,
        trim_trades: Optional[List[Dict[str, Any]]] = None,
        holding_days: int = 0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> Dict[str, Any]:
        """Compute position attribution."""
        total_pnl = realized_pnl + unrealized_pnl
        net_pnl = total_pnl - cost

        # Add-on effect: PnL from size-increasing trades
        add_on_effect = 0.0
        if add_on_trades:
            for t in add_on_trades:
                fill = t.get("fill_price", average_cost)
                qty = t.get("quantity", 0.0)
                add_on_effect += (current_price - fill) * qty

        # Trim effect: PnL from size-reducing trades
        trim_effect = 0.0
        if trim_trades:
            for t in trim_trades:
                fill = t.get("fill_price", current_price)
                cost_basis = t.get("cost_basis", average_cost)
                qty = t.get("quantity", 0.0)
                trim_effect += (fill - cost_basis) * qty

        confidence = ConfidenceLevel.HIGH if state == PositionState.CLOSED else ConfidenceLevel.MEDIUM
        status = AttributionStatus.COMPLETE

        return {
            "position_id": position_id,
            "symbol": symbol,
            "open_date": open_date,
            "close_date": close_date,
            "average_cost": average_cost,
            "current_price": current_price,
            "quantity": quantity,
            "state": state.value,
            "holding_days": holding_days,
            "realized_pnl": realized_pnl,
            "unrealized_pnl": unrealized_pnl,
            "total_pnl": total_pnl,
            "net_pnl": net_pnl,
            "cost": cost,
            "risk_contribution": risk_contribution,
            "drawdown": drawdown,
            "add_on_effect": add_on_effect,
            "trim_effect": trim_effect,
            "confidence": confidence.value,
            "status": status.value,
            "period_start": period_start,
            "period_end": period_end,
            "source_lineage": source_lineage,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        }
