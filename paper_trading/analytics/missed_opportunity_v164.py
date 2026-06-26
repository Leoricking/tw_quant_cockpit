"""
paper_trading/analytics/missed_opportunity_v164.py — Missed Opportunity Analysis v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Post-event analysis only. Not used in real-time decisions.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True
POST_EVENT_ANALYSIS_ONLY = True


@dataclass
class MissedOpportunityRecord:
    """A missed opportunity detected in post-event review."""
    opportunity_id: str
    signal_id: Optional[str] = None
    reason: str = ""
    estimated_impact: Optional[Decimal] = None
    confidence: str = "LOW"
    evidence_refs: List[str] = field(default_factory=list)
    post_event_label: str = "POST_EVENT_ONLY"


@dataclass
class MissedOpportunityAnalysis:
    session_id: str
    missed_signal_count: Optional[int] = None
    estimated_total_impact: Optional[Decimal] = None
    opportunities: List[MissedOpportunityRecord] = field(default_factory=list)
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    paper_only: bool = True
    post_event_label: str = "POST_EVENT_ONLY"


class MissedOpportunityAnalyzer:
    """Identifies missed opportunities from post-session data."""

    def analyze(
        self,
        session_id: str,
        missed_signal_count: int,
        estimated_impact: Optional[Decimal] = None,
    ) -> MissedOpportunityAnalysis:
        quality = MetricQuality.VALID if missed_signal_count >= 0 else MetricQuality.UNKNOWN
        return MissedOpportunityAnalysis(
            session_id=session_id,
            missed_signal_count=missed_signal_count,
            estimated_total_impact=estimated_impact,
            quality=quality,
        )


__all__ = ["MissedOpportunityRecord", "MissedOpportunityAnalysis", "MissedOpportunityAnalyzer"]
