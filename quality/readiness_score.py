"""
quality/readiness_score.py - Readiness Score Calculator (v0.3.20).

Shared score utilities: classification, weighting, capping.

[!] Research Only. Simulation Only. No Real Orders.
[!] PRODUCTION_BLOCKED is always True in v1.
[!] REAL_ORDER_READY is never allowed.
"""

from __future__ import annotations

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Score classification thresholds
# ---------------------------------------------------------------------------

_THRESHOLDS = [
    (90, "STRONG"),
    (75, "READY_FOR_RESEARCH"),
    (60, "PARTIAL"),
    (40, "WEAK"),
    (0,  "BLOCKED"),
]

# ---------------------------------------------------------------------------
# Score weights
# ---------------------------------------------------------------------------

_PRODUCTION_WEIGHTS: Dict[str, float] = {
    "freshness_score":          0.20,
    "coverage_score":           0.20,
    "source_confidence_score":  0.15,
    "timing_quality_score":     0.15,
    "sample_size_score":        0.10,
    "intraday_coverage_score":  0.10,
    "provider_health_score":    0.05,
    "mock_contamination_score": 0.05,
}

_BACKTEST_WEIGHTS: Dict[str, float] = {
    "coverage_score":           0.25,
    "sample_size_score":        0.20,
    "mock_contamination_score": 0.20,
    "freshness_score":          0.15,
    "timing_quality_score":     0.10,
    "source_confidence_score":  0.10,
}


class ReadinessScoreCalculator:
    """
    Shared utilities for readiness score computation and classification.

    Parameters
    ----------
    scores : dict of {score_name: float (0-100)}
    """

    VERSION = "v0.3.20"

    # Hard-coded safety invariants
    PRODUCTION_BLOCKED: bool = True
    REAL_ORDER_READY: bool = False

    def __init__(self, scores: Optional[Dict[str, float]] = None):
        self.scores = scores or {}

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    @staticmethod
    def classify(score: float) -> str:
        """Classify a 0-100 score into a named tier."""
        for threshold, label in _THRESHOLDS:
            if score >= threshold:
                return label
        return "BLOCKED"

    # ------------------------------------------------------------------
    # Composite scores
    # ------------------------------------------------------------------

    def production_readiness_score(self) -> float:
        """
        Weighted production readiness composite score.

        production_readiness_score =
          0.20 * freshness_score
          0.20 * coverage_score
          0.15 * source_confidence_score
          0.15 * timing_quality_score
          0.10 * sample_size_score
          0.10 * intraday_coverage_score
          0.05 * provider_health_score
          0.05 * mock_contamination_score
        """
        return self._weighted(self.scores, _PRODUCTION_WEIGHTS)

    def backtest_readiness_score(self) -> float:
        """
        Weighted backtest readiness composite score.

        backtest_readiness_score =
          0.25 * coverage_score
          0.20 * sample_size_score
          0.20 * mock_contamination_score
          0.15 * freshness_score
          0.10 * timing_quality_score
          0.10 * source_confidence_score

        Capping rules:
          - If mock_contamination_score < 90 → cap at 60
          - If coverage_score < 70 → cap at 70
        """
        raw = self._weighted(self.scores, _BACKTEST_WEIGHTS)

        mock_score = self.scores.get("mock_contamination_score", 100.0)
        cov_score  = self.scores.get("coverage_score", 100.0)

        cap = 100.0
        if mock_score < 90:
            cap = min(cap, 60.0)
        if cov_score < 70:
            cap = min(cap, 70.0)

        return min(raw, cap)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _weighted(scores: Dict[str, float], weights: Dict[str, float]) -> float:
        total_weight = 0.0
        total_score  = 0.0
        for key, w in weights.items():
            v = scores.get(key)
            if v is not None:
                total_score  += v * w
                total_weight += w
        if total_weight == 0:
            return 0.0
        # Renormalize to handle missing sub-scores gracefully
        return round(total_score / total_weight, 2)

    def score_summary(self) -> dict:
        """
        Return all sub-scores + composite scores + classifications.
        """
        prod  = self.production_readiness_score()
        btest = self.backtest_readiness_score()
        return {
            "sub_scores":                   dict(self.scores),
            "production_readiness_score":   prod,
            "backtest_readiness_score":     btest,
            "production_classification":    self.classify(prod),
            "backtest_classification":      self.classify(btest),
            "production_blocked":           self.PRODUCTION_BLOCKED,
            "real_order_ready":             self.REAL_ORDER_READY,
        }
