"""
paper_trading/performance_attribution/slippage_attribution_v167.py
Slippage attribution for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionLevel, AttributionStatus, ConfidenceLevel
from .models_v167 import SlippageContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den != 0.0 else default


class SlippageAttributionEngine:
    """Slippage decomposition: positive, negative, vs VWAP, vs close."""

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        trades: List[Dict[str, Any]],
        begin_equity: float = 1.0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> SlippageContribution:
        """
        Compute slippage attribution from list of trade dicts.
        Each trade: {fill_price, reference_price, quantity, direction (+1/-1)}.
        """
        if not trades:
            return SlippageContribution(
                entity_id=entity_id,
                level=level,
                total_slippage=0.0,
                positive_slippage=0.0,
                negative_slippage=0.0,
                slippage_bps=0.0,
                per_trade_slippage=0.0,
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

        slippages: List[float] = []
        vwap_slippages: List[float] = []
        close_slippages: List[float] = []

        for t in trades:
            fill = t.get("fill_price", 0.0)
            ref = t.get("reference_price", fill)
            qty = t.get("quantity", 1.0)
            direction = t.get("direction", 1)
            slip = (fill - ref) * qty * direction
            slippages.append(slip)
            if t.get("vwap"):
                vwap_slippages.append((fill - t["vwap"]) * qty * direction)
            if t.get("close_price"):
                close_slippages.append((fill - t["close_price"]) * qty * direction)

        total = sum(slippages)
        positive = sum(s for s in slippages if s > 0)
        negative = sum(s for s in slippages if s < 0)
        slippage_bps = _safe_div(total, begin_equity) * 10_000
        per_trade = _safe_div(total, len(slippages))

        slippage_vs_vwap = sum(vwap_slippages) if vwap_slippages else None
        slippage_vs_close = sum(close_slippages) if close_slippages else None

        confidence = ConfidenceLevel.HIGH if len(trades) >= 5 else ConfidenceLevel.MEDIUM

        return SlippageContribution(
            entity_id=entity_id,
            level=level,
            total_slippage=total,
            positive_slippage=positive,
            negative_slippage=negative,
            slippage_bps=slippage_bps,
            per_trade_slippage=per_trade,
            slippage_vs_vwap=slippage_vs_vwap,
            slippage_vs_close=slippage_vs_close,
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
