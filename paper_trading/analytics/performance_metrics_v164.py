"""
paper_trading/analytics/performance_metrics_v164.py — Paper Performance Metrics v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
Gross/net PnL, drawdown, turnover — all paper simulation metrics.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional

from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True


@dataclass
class PaperPerformanceMetrics:
    """Paper simulation performance metrics. No real orders. No broker."""
    session_id: str
    gross_pnl: Optional[Decimal] = None
    net_pnl: Optional[Decimal] = None
    realized_pnl: Optional[Decimal] = None
    unrealized_pnl: Optional[Decimal] = None
    max_drawdown: Optional[Decimal] = None
    turnover: Optional[Decimal] = None
    transaction_cost: Optional[Decimal] = None
    slippage: Optional[Decimal] = None
    fill_ratio: Optional[Decimal] = None
    rejection_ratio: Optional[Decimal] = None
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    paper_only: bool = True
    research_only: bool = True

    def validate(self) -> List[str]:
        """Return list of validation issues."""
        issues: List[str] = []
        if self.gross_pnl is not None and self.net_pnl is not None:
            if self.net_pnl > self.gross_pnl:
                issues.append(
                    f"net_pnl ({self.net_pnl}) > gross_pnl ({self.gross_pnl}) — check costs"
                )
        if self.max_drawdown is not None and self.max_drawdown > Decimal("0"):
            issues.append(
                f"max_drawdown should be <= 0 (got {self.max_drawdown})"
            )
        return issues


class PaperPerformanceMetricsComputer:
    """Computes paper performance metrics from session data."""

    def compute(
        self,
        session_id: str,
        raw: Dict[str, Any],
    ) -> PaperPerformanceMetrics:
        def _dec(key: str) -> Optional[Decimal]:
            v = raw.get(key)
            return Decimal(str(v)) if v is not None else None

        metrics = PaperPerformanceMetrics(
            session_id=session_id,
            gross_pnl=_dec("gross_pnl"),
            net_pnl=_dec("net_pnl"),
            realized_pnl=_dec("realized_pnl"),
            unrealized_pnl=_dec("unrealized_pnl"),
            max_drawdown=_dec("max_drawdown"),
            turnover=_dec("turnover"),
            transaction_cost=_dec("transaction_cost"),
            slippage=_dec("slippage"),
            fill_ratio=_dec("fill_ratio"),
            rejection_ratio=_dec("rejection_ratio"),
        )

        # Quality assessment
        required_fields = [metrics.gross_pnl, metrics.net_pnl, metrics.max_drawdown]
        available = sum(1 for f in required_fields if f is not None)
        if available == len(required_fields):
            metrics.quality = MetricQuality.VALID
        elif available > 0:
            metrics.quality = MetricQuality.PARTIAL
        else:
            metrics.quality = MetricQuality.INSUFFICIENT_DATA

        return metrics


__all__ = ["PaperPerformanceMetrics", "PaperPerformanceMetricsComputer"]
