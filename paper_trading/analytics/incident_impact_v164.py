"""
paper_trading/analytics/incident_impact_v164.py — Incident Impact Analysis v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Correlation is not causation — labels ASSOCIATED, not causal.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional
from paper_trading.analytics.enums_v164 import MetricQuality

NO_REAL_ORDERS = True
PAPER_ONLY = True
CAUSAL_ASSERTION_WITHOUT_EVIDENCE_FORBIDDEN = True


@dataclass
class IncidentImpactRecord:
    """Impact analysis for a single incident. Correlation ≠ causation."""
    incident_id: str
    duration_seconds: Optional[Decimal] = None
    affected_session_count: int = 0
    rejected_signals_during: int = 0
    missed_proposals: int = 0
    estimated_pnl_impact: Optional[Decimal] = None
    downtime_impact_seconds: Optional[Decimal] = None
    causal_label: str = "ASSOCIATED"  # never asserted as CAUSAL without evidence
    evidence_refs: List[str] = field(default_factory=list)
    quality: MetricQuality = MetricQuality.UNKNOWN


@dataclass
class IncidentImpactAnalysis:
    session_id: str
    total_incidents: int = 0
    total_duration_seconds: Optional[Decimal] = None
    total_estimated_pnl_impact: Optional[Decimal] = None
    records: List[IncidentImpactRecord] = field(default_factory=list)
    quality: MetricQuality = MetricQuality.UNKNOWN
    policy_version: str = "1.6.4"
    paper_only: bool = True


class IncidentImpactAnalyzer:

    def analyze(
        self,
        session_id: str,
        incident_records: List[Dict[str, Any]],
    ) -> IncidentImpactAnalysis:
        records: List[IncidentImpactRecord] = []
        total_pnl = Decimal("0")
        total_duration = Decimal("0")

        for inc in incident_records:
            impact = Decimal(str(inc.get("estimated_pnl_impact", "0")))
            dur = Decimal(str(inc.get("duration_seconds", "0")))
            rec = IncidentImpactRecord(
                incident_id=inc.get("incident_id", ""),
                duration_seconds=dur,
                affected_session_count=inc.get("affected_session_count", 0),
                rejected_signals_during=inc.get("rejected_signals", 0),
                missed_proposals=inc.get("missed_proposals", 0),
                estimated_pnl_impact=impact,
                causal_label="ASSOCIATED",
                evidence_refs=inc.get("evidence_refs", []),
                quality=MetricQuality.PARTIAL,
            )
            records.append(rec)
            total_pnl += impact
            total_duration += dur

        return IncidentImpactAnalysis(
            session_id=session_id,
            total_incidents=len(records),
            total_duration_seconds=total_duration,
            total_estimated_pnl_impact=total_pnl,
            records=records,
            quality=MetricQuality.VALID if records else MetricQuality.INSUFFICIENT_DATA,
        )


__all__ = ["IncidentImpactRecord", "IncidentImpactAnalysis", "IncidentImpactAnalyzer"]
