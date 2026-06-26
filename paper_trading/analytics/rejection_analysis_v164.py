"""
paper_trading/analytics/rejection_analysis_v164.py — Rejection Analysis v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True


@dataclass
class RejectionAnalysisResult:
    session_id: str
    total_proposals: int = 0
    rejected_count: int = 0
    rejection_ratio: Optional[Decimal] = None
    rejection_reasons: Dict[str, int] = field(default_factory=dict)
    high_rejection_detected: bool = False
    threshold: Decimal = Decimal("0.3")
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    paper_only: bool = True


class RejectionAnalyzer:
    HIGH_REJECTION_THRESHOLD = Decimal("0.3")

    def analyze(
        self,
        session_id: str,
        total_proposals: int,
        rejected_count: int,
        rejection_reasons: Optional[Dict[str, int]] = None,
    ) -> RejectionAnalysisResult:
        rejection_ratio: Optional[Decimal] = None
        if total_proposals > 0:
            rejection_ratio = Decimal(str(rejected_count)) / Decimal(str(total_proposals))

        high = rejection_ratio is not None and rejection_ratio > self.HIGH_REJECTION_THRESHOLD

        return RejectionAnalysisResult(
            session_id=session_id,
            total_proposals=total_proposals,
            rejected_count=rejected_count,
            rejection_ratio=rejection_ratio,
            rejection_reasons=rejection_reasons or {},
            high_rejection_detected=high,
            threshold=self.HIGH_REJECTION_THRESHOLD,
            quality=MetricQuality.VALID if total_proposals > 0 else MetricQuality.INSUFFICIENT_DATA,
        )


__all__ = ["RejectionAnalysisResult", "RejectionAnalyzer"]
