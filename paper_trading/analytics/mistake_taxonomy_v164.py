"""
paper_trading/analytics/mistake_taxonomy_v164.py — Mistake Taxonomy v1.6.4
RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Mistakes are SUGGESTED status — system cannot auto-confirm.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid

from paper_trading.analytics.enums_v164 import AnomalySeverity, MistakeCategory
from paper_trading.analytics.models_v164 import MistakeRecord

NO_REAL_ORDERS = True
PAPER_ONLY = True
AUTO_CONFIRM_MISTAKES = False  # System suggests only
AUTO_STRATEGY_CHANGE_ENABLED = False


MISTAKE_DEFINITIONS: Dict[MistakeCategory, str] = {
    MistakeCategory.STALE_DATA_DECISION:      "Decision made on stale market data",
    MistakeCategory.MISSING_DATA_ASSUMPTION:  "Assumed missing data was normal/zero",
    MistakeCategory.DUPLICATE_SIGNAL:         "Same signal processed multiple times",
    MistakeCategory.CONFLICTING_SIGNAL:       "Conflicting signals not reconciled",
    MistakeCategory.LATE_SIGNAL:              "Signal arrived after validity window",
    MistakeCategory.OVERTRADING:              "Excessive turnover or signal frequency",
    MistakeCategory.UNDERTRADING:             "Insufficient signal utilization",
    MistakeCategory.EXCESSIVE_REJECTION:      "High proposal rejection rate",
    MistakeCategory.POOR_SIMULATED_EXECUTION: "Paper execution simulator inconsistency",
    MistakeCategory.HIGH_SLIPPAGE:            "Simulated slippage above threshold",
    MistakeCategory.LATENCY_SENSITIVITY:      "Decision quality degraded by latency",
    MistakeCategory.IGNORED_ALERT:            "Alert not acknowledged in time",
    MistakeCategory.DELAYED_ACKNOWLEDGEMENT:  "Alert acknowledgement delayed",
    MistakeCategory.PREMATURE_RESUME_ATTEMPT: "Resume attempted before safe conditions",
    MistakeCategory.FAILED_RECOVERY:          "Recovery attempt unsuccessful",
    MistakeCategory.INCOMPLETE_LINEAGE:       "Lineage gaps in analytical chain",
    MistakeCategory.IRREPRODUCIBLE_RESULT:    "Result cannot be reproduced",
    MistakeCategory.UNSUPPORTED_CONCLUSION:   "Conclusion without sufficient evidence",
}


class MistakeTaxonomyClassifier:
    """
    Classifies mistakes from session data.
    All classifications are SUGGESTED — cannot be auto-confirmed.
    Does not auto-change strategy.
    """

    def classify(
        self,
        evidence: Dict[str, Any],
    ) -> List[MistakeRecord]:
        mistakes: List[MistakeRecord] = []

        def _add(cat: MistakeCategory, sev: AnomalySeverity, metric: Optional[str] = None, ev: Optional[List[str]] = None) -> None:
            mistakes.append(MistakeRecord(
                mistake_id=str(uuid.uuid4()),
                category=cat,
                severity=sev,
                evidence=ev or [],
                affected_metric=metric,
                root_cause=None,
                lesson=MISTAKE_DEFINITIONS.get(cat, ""),
                recommended_action="Review and confirm manually. No auto-change applied.",
            ))

        # Check for stale data
        stale_ratio = evidence.get("stale_ratio")
        if stale_ratio is not None and Decimal(str(stale_ratio)) > Decimal("0.1"):
            _add(MistakeCategory.STALE_DATA_DECISION, AnomalySeverity.HIGH,
                 "stale_ratio", [f"stale_ratio={stale_ratio}"])

        # Check for excessive rejection
        rejection_ratio = evidence.get("rejection_ratio")
        if rejection_ratio is not None and Decimal(str(rejection_ratio)) > Decimal("0.3"):
            _add(MistakeCategory.EXCESSIVE_REJECTION, AnomalySeverity.MEDIUM,
                 "rejection_ratio", [f"rejection_ratio={rejection_ratio}"])

        # Check for ignored alerts
        mean_tta = evidence.get("mean_time_to_acknowledge_seconds")
        if mean_tta is not None and Decimal(str(mean_tta)) > Decimal("300"):
            _add(MistakeCategory.DELAYED_ACKNOWLEDGEMENT, AnomalySeverity.MEDIUM,
                 "mean_time_to_acknowledge_seconds", [f"mtta={mean_tta}s"])

        # Check for failed recovery
        failed_recoveries = evidence.get("failed_recoveries")
        if failed_recoveries is not None and int(failed_recoveries) > 0:
            _add(MistakeCategory.FAILED_RECOVERY, AnomalySeverity.HIGH,
                 "failed_recoveries", [f"failed={failed_recoveries}"])

        # Duplicate signals
        duplicate_count = evidence.get("duplicate_count")
        if duplicate_count is not None and int(duplicate_count) > 0:
            _add(MistakeCategory.DUPLICATE_SIGNAL, AnomalySeverity.LOW,
                 "duplicate_count", [f"duplicates={duplicate_count}"])

        return mistakes


__all__ = ["MistakeTaxonomyClassifier", "MISTAKE_DEFINITIONS", "AUTO_CONFIRM_MISTAKES"]
