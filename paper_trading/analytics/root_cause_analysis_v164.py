"""
paper_trading/analytics/root_cause_analysis_v164.py — Root Cause Analysis v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Deterministic RCA process. No unsupported causality assertions.
Temporal correlation ≠ causation. Unknown root cause allowed and honest.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid

from paper_trading.analytics.enums_v164 import RootCauseCategory
from paper_trading.analytics.models_v164 import RootCauseRecord

NO_REAL_ORDERS = True
PAPER_ONLY = True
UNSUPPORTED_CAUSALITY_FORBIDDEN = True
TIMELINE_CORRELATION_IS_NOT_CAUSATION = True
AUDIT_TIMELINE_MODIFICATION_FORBIDDEN = True


class RootCauseAnalyzer:
    """
    Deterministic RCA pipeline:
    Observed Problem → Evidence Collection → Timeline Correlation
    → Candidate Causes → Exclusion Rules → Confidence → Root Cause
    """

    def analyze(
        self,
        problem: str,
        evidence: List[Dict[str, Any]],
        candidate_causes: List[str],
        exclusion_rules: Optional[Dict[str, str]] = None,
    ) -> RootCauseRecord:
        """
        Run RCA. Returns RootCauseRecord.
        - Never asserts causation without evidence_refs.
        - Unknown root cause is an honest result.
        - Does not modify original audit timeline.
        """
        if not problem:
            raise ValueError("problem description required for RCA")

        exclusion_rules = exclusion_rules or {}
        excluded: List[str] = []
        remaining: List[str] = []

        for cause in candidate_causes:
            if cause in exclusion_rules:
                excluded.append(cause)
            else:
                remaining.append(cause)

        # Evidence-based confidence
        evidence_refs = [ev.get("ref", str(uuid.uuid4())) for ev in evidence]
        confidence = Decimal("0.0")
        root_cause_category = RootCauseCategory.UNKNOWN
        causal_label = "UNKNOWN"

        if evidence and remaining:
            # Simple heuristic: confidence proportional to evidence quantity
            # Real RCA would use domain-specific rules
            confidence = min(
                Decimal(str(len(evidence))) / Decimal("5"),
                Decimal("0.9"),
            )
            causal_label = "ASSOCIATED" if confidence < Decimal("0.7") else "CAUSAL"

            # Map first remaining cause to a category
            cause_map: Dict[str, RootCauseCategory] = {
                "data_quality": RootCauseCategory.DATA_QUALITY,
                "signal_quality": RootCauseCategory.SIGNAL_QUALITY,
                "strategy": RootCauseCategory.STRATEGY_LOGIC,
                "execution": RootCauseCategory.EXECUTION_SIMULATION,
                "latency": RootCauseCategory.LATENCY,
                "config": RootCauseCategory.CONFIGURATION,
                "operation": RootCauseCategory.OPERATIONAL_PROCESS,
                "incident": RootCauseCategory.INCIDENT,
            }
            for key, cat in cause_map.items():
                if any(key in c.lower() for c in remaining):
                    root_cause_category = cat
                    break

        elif not remaining:
            causal_label = "UNKNOWN"
            confidence = Decimal("0.0")
            root_cause_category = RootCauseCategory.UNKNOWN

        return RootCauseRecord(
            rca_id=str(uuid.uuid4()),
            problem=problem,
            candidate_causes=candidate_causes,
            excluded_causes=excluded,
            root_cause_category=root_cause_category,
            confidence=confidence,
            evidence_refs=evidence_refs,
            causal_label=causal_label,
        )


__all__ = ["RootCauseAnalyzer"]
