"""
paper_trading/performance_attribution/pnl_attribution_v167.py
PnL attribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] child sum = parent sum enforced; residual always visible.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .enums_v167 import (
    AttributionLevel, AttributionStatus, ConfidenceLevel, TradeDirection
)
from .models_v167 import PnLContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_SCHEMA_VERSION = "167"


def _sum_pnl_list(items: List[Dict[str, Any]], key: str) -> float:
    return sum(item.get(key, 0.0) for item in items)


class PnLAttributionEngine:
    """
    PnL attribution engine. Decomposes PnL across dimensions.
    Enforces hierarchy: trade → position → symbol → strategy → portfolio.
    session sum must also equal portfolio sum.
    """

    def __init__(self, residual_tolerance: float = 0.0001) -> None:
        self._tolerance = residual_tolerance

    def compute_trade_pnl(self, trade: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute PnL for a single trade.
        gross_pnl = (fill_price - cost_basis) * quantity * direction_sign
        net_pnl = gross_pnl - costs
        """
        fill = trade.get("fill_price", 0.0)
        cost_basis = trade.get("cost_basis", fill)
        qty = trade.get("quantity", 0.0)
        direction = trade.get("direction", TradeDirection.LONG)
        sign = -1.0 if direction == TradeDirection.SHORT or direction == "SHORT" else 1.0

        gross_pnl = (fill - cost_basis) * qty * sign
        commission = trade.get("commission", 0.0)
        tax = trade.get("transaction_tax", 0.0)
        exchange_fee = trade.get("exchange_fee", 0.0)
        slippage = trade.get("slippage", 0.0)
        total_cost = commission + tax + exchange_fee + slippage
        net_pnl = gross_pnl - total_cost

        return {
            "trade_id": trade.get("trade_id", ""),
            "gross_pnl": gross_pnl,
            "net_pnl": net_pnl,
            "commission": commission,
            "transaction_tax": tax,
            "exchange_fee": exchange_fee,
            "slippage": slippage,
            "total_cost": total_cost,
            "residual": 0.0,
            "paper_only": True,
            "research_only": True,
        }

    def aggregate_trades_to_position(
        self, trades: List[Dict[str, Any]], position_id: str
    ) -> Dict[str, Any]:
        """Aggregate trade PnLs to position level. trade sum = position sum."""
        trade_pnls = [self.compute_trade_pnl(t) for t in trades]
        gross = sum(p["gross_pnl"] for p in trade_pnls)
        net = sum(p["net_pnl"] for p in trade_pnls)
        commission = sum(p["commission"] for p in trade_pnls)
        tax = sum(p["transaction_tax"] for p in trade_pnls)
        exchange_fee = sum(p["exchange_fee"] for p in trade_pnls)
        slippage = sum(p["slippage"] for p in trade_pnls)
        total_cost = sum(p["total_cost"] for p in trade_pnls)

        # Verify: gross - total_cost == net (within tolerance)
        expected_net = gross - total_cost
        residual = net - expected_net
        if abs(residual) > self._tolerance:
            status = AttributionStatus.DEGRADED
        else:
            status = AttributionStatus.COMPLETE

        return {
            "position_id": position_id,
            "gross_pnl": gross,
            "net_pnl": net,
            "commission": commission,
            "transaction_tax": tax,
            "exchange_fee": exchange_fee,
            "slippage": slippage,
            "total_cost": total_cost,
            "residual": residual,
            "status": status.value,
            "trade_count": len(trades),
            "paper_only": True,
            "research_only": True,
        }

    def aggregate_to_symbol(
        self, position_pnls: List[Dict[str, Any]], symbol: str
    ) -> Dict[str, Any]:
        """Aggregate position PnLs to symbol level. position sum = symbol sum."""
        gross = sum(p.get("gross_pnl", 0.0) for p in position_pnls)
        net = sum(p.get("net_pnl", 0.0) for p in position_pnls)
        total_cost = sum(p.get("total_cost", 0.0) for p in position_pnls)
        residual = sum(p.get("residual", 0.0) for p in position_pnls)
        return {
            "symbol": symbol,
            "gross_pnl": gross,
            "net_pnl": net,
            "total_cost": total_cost,
            "residual": residual,
            "position_count": len(position_pnls),
            "paper_only": True,
            "research_only": True,
        }

    def aggregate_to_strategy(
        self, symbol_pnls: List[Dict[str, Any]], strategy_id: str
    ) -> Dict[str, Any]:
        """Aggregate symbol PnLs to strategy level."""
        gross = sum(p.get("gross_pnl", 0.0) for p in symbol_pnls)
        net = sum(p.get("net_pnl", 0.0) for p in symbol_pnls)
        total_cost = sum(p.get("total_cost", 0.0) for p in symbol_pnls)
        residual = sum(p.get("residual", 0.0) for p in symbol_pnls)
        return {
            "strategy_id": strategy_id,
            "gross_pnl": gross,
            "net_pnl": net,
            "total_cost": total_cost,
            "residual": residual,
            "symbol_count": len(symbol_pnls),
            "paper_only": True,
            "research_only": True,
        }

    def aggregate_to_portfolio(
        self, strategy_pnls: List[Dict[str, Any]], portfolio_id: str
    ) -> Dict[str, Any]:
        """Aggregate strategy PnLs to portfolio level. strategy sum = portfolio sum."""
        gross = sum(p.get("gross_pnl", 0.0) for p in strategy_pnls)
        net = sum(p.get("net_pnl", 0.0) for p in strategy_pnls)
        total_cost = sum(p.get("total_cost", 0.0) for p in strategy_pnls)
        residual = sum(p.get("residual", 0.0) for p in strategy_pnls)
        return {
            "portfolio_id": portfolio_id,
            "gross_pnl": gross,
            "net_pnl": net,
            "total_cost": total_cost,
            "residual": residual,
            "strategy_count": len(strategy_pnls),
            "paper_only": True,
            "research_only": True,
        }

    def verify_hierarchy(
        self,
        portfolio_gross: float,
        strategy_sum_gross: float,
        symbol_sum_gross: float,
        position_sum_gross: float,
        trade_sum_gross: float,
    ) -> Dict[str, Any]:
        """
        Verify: trade sum ≈ position sum ≈ symbol sum ≈ strategy sum ≈ portfolio.
        Returns verification dict with all checks.
        """
        checks = {}
        tol = self._tolerance

        checks["trade_eq_position"] = abs(trade_sum_gross - position_sum_gross) < tol
        checks["position_eq_symbol"] = abs(position_sum_gross - symbol_sum_gross) < tol
        checks["symbol_eq_strategy"] = abs(symbol_sum_gross - strategy_sum_gross) < tol
        checks["strategy_eq_portfolio"] = abs(strategy_sum_gross - portfolio_gross) < tol

        all_pass = all(checks.values())
        return {
            "all_pass": all_pass,
            "checks": checks,
            "tolerance": tol,
            "trade_sum": trade_sum_gross,
            "position_sum": position_sum_gross,
            "symbol_sum": symbol_sum_gross,
            "strategy_sum": strategy_sum_gross,
            "portfolio": portfolio_gross,
            "paper_only": True,
            "research_only": True,
        }

    def build_contribution(
        self,
        entity_id: str,
        level: AttributionLevel,
        agg: Dict[str, Any],
        begin_equity: float,
        realized_pnl: float = 0.0,
        unrealized_pnl: float = 0.0,
        dividend: float = 0.0,
        distribution: float = 0.0,
        cash_carry: float = 0.0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> PnLContribution:
        """Build a PnLContribution model from an aggregation result."""
        gross_pnl = agg.get("gross_pnl", 0.0)
        net_pnl = agg.get("net_pnl", 0.0)
        total_cost = agg.get("total_cost", 0.0)
        residual = agg.get("residual", 0.0)

        expected_net = gross_pnl - total_cost
        check_residual = net_pnl - expected_net
        if abs(check_residual) > self._tolerance:
            status = AttributionStatus.DEGRADED
            confidence = ConfidenceLevel.LOW
        else:
            status = AttributionStatus.COMPLETE
            confidence = ConfidenceLevel.HIGH

        return PnLContribution(
            entity_id=entity_id,
            level=level,
            realized_pnl=realized_pnl,
            unrealized_pnl=unrealized_pnl,
            gross_pnl=gross_pnl,
            net_pnl=net_pnl,
            commission=agg.get("commission", 0.0),
            transaction_tax=agg.get("transaction_tax", 0.0),
            exchange_fee=agg.get("exchange_fee", 0.0),
            slippage=agg.get("slippage", 0.0),
            dividend=dividend,
            distribution=distribution,
            cash_carry=cash_carry,
            residual=residual + check_residual,
            confidence=confidence,
            status=status,
            source_lineage=source_lineage,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )
