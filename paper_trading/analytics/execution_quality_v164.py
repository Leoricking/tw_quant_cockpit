"""
paper_trading/analytics/execution_quality_v164.py — Execution Quality Analysis v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
All execution analysis is paper simulation. No real broker capabilities.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional

from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
NO_BROKER = True
PAPER_ONLY = True

# Safety: All execution analysis is paper simulation
EXECUTION_IS_PAPER_SIMULATION = True
BROKER_EXECUTION_CAPABILITY_INCLUDED = False


@dataclass
class ExecutionQualityMetrics:
    """Paper execution quality analysis. No real broker."""
    session_id: str
    simulated_orders: Optional[int] = None
    simulated_fills: Optional[int] = None
    rejected_orders: Optional[int] = None
    cancelled_orders: Optional[int] = None
    partial_fills: Optional[int] = None
    fill_ratio: Optional[Decimal] = None
    rejection_ratio: Optional[Decimal] = None
    cancellation_ratio: Optional[Decimal] = None
    partial_fill_ratio: Optional[Decimal] = None
    proposal_to_submit_latency_p50_ms: Optional[Decimal] = None
    proposal_to_submit_latency_p95_ms: Optional[Decimal] = None
    submit_to_fill_latency_p50_ms: Optional[Decimal] = None
    submit_to_fill_latency_p95_ms: Optional[Decimal] = None
    simulated_slippage: Optional[Decimal] = None
    price_improvement: Optional[Decimal] = None
    stale_proposal_ratio: Optional[Decimal] = None
    execution_simulator_consistent: Optional[bool] = None
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    paper_only: bool = True
    broker_execution: bool = False

    def validate_no_broker(self) -> None:
        if self.broker_execution:
            raise ValueError(
                "broker_execution=True is forbidden. All execution is paper simulation."
            )


class ExecutionQualityAnalyzer:
    """Analyzes paper execution quality from session data."""

    def analyze(self, session_id: str, raw: Dict[str, Any]) -> ExecutionQualityMetrics:
        def _dec(key: str) -> Optional[Decimal]:
            v = raw.get(key)
            return Decimal(str(v)) if v is not None else None

        def _int(key: str) -> Optional[int]:
            v = raw.get(key)
            return int(v) if v is not None else None

        fills = _int("simulated_fills")
        orders = _int("simulated_orders")
        rejected = _int("rejected_orders")

        fill_ratio: Optional[Decimal] = None
        rejection_ratio: Optional[Decimal] = None
        if orders and orders > 0:
            if fills is not None:
                fill_ratio = Decimal(str(fills)) / Decimal(str(orders))
            if rejected is not None:
                rejection_ratio = Decimal(str(rejected)) / Decimal(str(orders))

        metrics = ExecutionQualityMetrics(
            session_id=session_id,
            simulated_orders=orders,
            simulated_fills=fills,
            rejected_orders=rejected,
            cancelled_orders=_int("cancelled_orders"),
            partial_fills=_int("partial_fills"),
            fill_ratio=_dec("fill_ratio") or fill_ratio,
            rejection_ratio=_dec("rejection_ratio") or rejection_ratio,
            cancellation_ratio=_dec("cancellation_ratio"),
            partial_fill_ratio=_dec("partial_fill_ratio"),
            proposal_to_submit_latency_p50_ms=_dec("proposal_to_submit_p50_ms"),
            proposal_to_submit_latency_p95_ms=_dec("proposal_to_submit_p95_ms"),
            submit_to_fill_latency_p50_ms=_dec("submit_to_fill_p50_ms"),
            submit_to_fill_latency_p95_ms=_dec("submit_to_fill_p95_ms"),
            simulated_slippage=_dec("simulated_slippage"),
            price_improvement=_dec("price_improvement"),
            stale_proposal_ratio=_dec("stale_proposal_ratio"),
            execution_simulator_consistent=raw.get("execution_simulator_consistent"),
            broker_execution=False,
        )

        available = sum(1 for v in [
            metrics.simulated_orders, metrics.fill_ratio, metrics.simulated_slippage
        ] if v is not None)
        if available == 3:
            metrics.quality = MetricQuality.VALID
        elif available > 0:
            metrics.quality = MetricQuality.PARTIAL
        else:
            metrics.quality = MetricQuality.INSUFFICIENT_DATA

        metrics.validate_no_broker()
        return metrics


__all__ = ["ExecutionQualityMetrics", "ExecutionQualityAnalyzer"]
