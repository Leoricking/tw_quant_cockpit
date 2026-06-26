"""
paper_trading/analytics/market_data_attribution_v164.py — Market Data Attribution v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True


class MarketDataAttributionComputer:
    """Attributes PnL/quality impact to market data quality issues."""

    def compute(
        self,
        stale_count: int,
        missing_intervals: int,
        total_intervals: int,
        pnl_impact_estimate: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        quality = MetricQuality.VALID
        issues = []
        if total_intervals > 0:
            stale_ratio = Decimal(str(stale_count)) / Decimal(str(total_intervals))
            missing_ratio = Decimal(str(missing_intervals)) / Decimal(str(total_intervals))
        else:
            stale_ratio = Decimal("0")
            missing_ratio = Decimal("0")
            quality = MetricQuality.INSUFFICIENT_DATA

        if stale_ratio > Decimal("0.1"):
            issues.append(f"High stale ratio: {stale_ratio:.2%}")
            quality = MetricQuality.PARTIAL
        if missing_ratio > Decimal("0.05"):
            issues.append(f"High missing ratio: {missing_ratio:.2%}")
            quality = MetricQuality.PARTIAL

        return {
            "stale_count": stale_count,
            "missing_intervals": missing_intervals,
            "total_intervals": total_intervals,
            "stale_ratio": stale_ratio,
            "missing_ratio": missing_ratio,
            "pnl_impact_estimate": pnl_impact_estimate,
            "quality": quality,
            "issues": issues,
            "paper_only": True,
            "policy_version": "1.6.4",
        }


__all__ = ["MarketDataAttributionComputer"]
