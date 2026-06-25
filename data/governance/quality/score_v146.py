"""
data/governance/quality/score_v146.py — Quality Score Engine v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Score 0-100 weighted. Score CANNOT override blocking failures.
[!] Weights versioned and configurable.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from data.governance.quality.models_v146 import GateStatus, QualityGateResult, QualityScore

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False

# Default weights (sum = 100)
_DEFAULT_WEIGHTS: Dict[str, float] = {
    "data_quality": 20.0,
    "freshness": 15.0,
    "coverage": 15.0,
    "provenance": 15.0,
    "pit": 10.0,
    "schema": 10.0,
    "authority_conflict": 10.0,
    "operational": 5.0,
}

# Gate ID → weight category mapping
_GATE_TO_CATEGORY: Dict[str, str] = {
    "data_quality": "data_quality",
    "freshness": "freshness",
    "coverage": "coverage",
    "provenance_completeness": "provenance",
    "point_in_time": "pit",
    "schema_drift": "schema",
    "authority_hierarchy": "authority_conflict",
    "conflict_resolution": "authority_conflict",
    "provider_registration": "operational",
    "provider_health": "operational",
    "endpoint_readiness": "operational",
    "safety_invariants": "operational",
}


class QualityScoreEngine:
    """
    Computes 0-100 weighted quality score.
    Score CANNOT override blocking failures (safety invariant).
    """

    POLICY_VERSION = "1.4.6"

    def __init__(self, weights: Optional[Dict[str, float]] = None) -> None:
        self._weights = weights or dict(_DEFAULT_WEIGHTS)
        # Normalize weights to sum to 100
        total = sum(self._weights.values())
        if total > 0:
            self._weights = {k: v * 100.0 / total for k, v in self._weights.items()}

    def compute(
        self, provider_id: str, subject_id: str,
        gate_results: List[QualityGateResult],
        blocking_failures: Optional[List[str]] = None,
    ) -> QualityScore:
        """Compute quality score. Score does NOT override blocking failures."""
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
        blocking_failures = blocking_failures or []
        has_blocking = len(blocking_failures) > 0

        component_scores: Dict[str, float] = {}

        for result in gate_results:
            category = _GATE_TO_CATEGORY.get(result.gate_id)
            if category is None:
                continue
            # Convert gate status to component score
            if result.status == GateStatus.PASS.value:
                raw_score = 100.0
            elif result.status == GateStatus.WARN.value:
                raw_score = 70.0
            elif result.status == GateStatus.NOT_APPLICABLE.value:
                raw_score = 100.0  # not applicable = no penalty
            else:
                raw_score = 0.0  # FAIL/BLOCKED/UNKNOWN

            # Average if multiple gates in same category
            if category in component_scores:
                component_scores[category] = (component_scores[category] + raw_score) / 2.0
            else:
                component_scores[category] = raw_score

        # Weighted total
        total_score = 0.0
        for category, weight in self._weights.items():
            cat_score = component_scores.get(category, 50.0)  # default 50 if no gate
            total_score += cat_score * (weight / 100.0)

        total_score = max(0.0, min(100.0, total_score))

        return QualityScore(
            score=total_score,
            provider_id=provider_id,
            subject_id=subject_id,
            component_scores=component_scores,
            weights=self._weights,
            blocking_failures_present=has_blocking,
            can_override_blocking=False,  # always False
            computed_at=now,
            policy_version=self.POLICY_VERSION,
        )
