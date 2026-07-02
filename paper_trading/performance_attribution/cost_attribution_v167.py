"""
paper_trading/performance_attribution/cost_attribution_v167.py
Cost attribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Unknown cost must not be defaulted to 0. known/estimated/unknown separated.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import (
    AttributionLevel, AttributionStatus, ConfidenceLevel, CostQuality,
)
from .models_v167 import CostContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den != 0.0 else default


class CostAttributionEngine:
    """
    Cost attribution: decomposes all cost components.
    known_cost, estimated_cost, unknown_cost must be separately tracked.
    unknown cost is NEVER defaulted to 0 without disclosure.
    """

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        commission: float = 0.0,
        transaction_tax: float = 0.0,
        exchange_fee: float = 0.0,
        borrow_fee: float = 0.0,
        financing_cost: float = 0.0,
        slippage: float = 0.0,
        spread: float = 0.0,
        impact_proxy: float = 0.0,
        turnover_cost: float = 0.0,
        other_modeled: float = 0.0,
        unknown_cost: float = 0.0,
        estimated_cost: float = 0.0,
        begin_equity: float = 1.0,
        gross_pnl: float = 0.0,
        net_pnl: float = 0.0,
        turnover: float = 0.0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> CostContribution:
        """
        Compute cost attribution with known/estimated/unknown separation.
        unknown_cost is explicitly tracked and shown — never silently zeroed.
        """
        known_cost = (commission + transaction_tax + exchange_fee + borrow_fee
                      + financing_cost + slippage + spread + impact_proxy
                      + turnover_cost + other_modeled)
        total_cost = known_cost + estimated_cost + unknown_cost

        # Determine quality
        if unknown_cost > 0:
            quality = CostQuality.UNKNOWN
            confidence = ConfidenceLevel.LOW
        elif estimated_cost > 0:
            quality = CostQuality.ESTIMATED
            confidence = ConfidenceLevel.MEDIUM
        else:
            quality = CostQuality.KNOWN
            confidence = ConfidenceLevel.HIGH

        # Derived metrics
        cost_bps = _safe_div(total_cost, begin_equity) * 10_000
        cost_pct_gross = _safe_div(total_cost, abs(gross_pnl)) * 100 if gross_pnl != 0 else 0.0
        cost_pct_net = _safe_div(total_cost, abs(net_pnl)) * 100 if net_pnl != 0 else 0.0
        cost_pct_equity = _safe_div(total_cost, begin_equity) * 100

        return CostContribution(
            entity_id=entity_id,
            level=level,
            commission=commission,
            transaction_tax=transaction_tax,
            exchange_fee=exchange_fee,
            borrow_fee=borrow_fee,
            financing_cost=financing_cost,
            slippage=slippage,
            spread=spread,
            impact_proxy=impact_proxy,
            turnover_cost=turnover_cost,
            other_modeled=other_modeled,
            unknown_cost=unknown_cost,
            estimated_cost=estimated_cost,
            known_cost=known_cost,
            total_cost=total_cost,
            cost_bps=cost_bps,
            cost_pct_gross_pnl=cost_pct_gross,
            cost_pct_net_pnl=cost_pct_net,
            cost_pct_equity=cost_pct_equity,
            cost_quality=quality,
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
