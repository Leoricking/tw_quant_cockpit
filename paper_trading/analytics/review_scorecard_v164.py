"""
paper_trading/analytics/review_scorecard_v164.py — Review Scorecard v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Scores 0-100. Weights versioned. Insufficient data -> no high scores.
Blocking failures cap score. Score does NOT auto-change strategy.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, List, Optional

from paper_trading.analytics.enums_v164 import (
    MetricQuality, ScorecardDimension, SCORECARD_WEIGHTS, SCORECARD_WEIGHT_VERSION,
)
from paper_trading.analytics.models_v164 import ReviewScorecard
from paper_trading.analytics.validation_v164 import validate_score

NO_REAL_ORDERS = True
PAPER_ONLY = True
AUTO_STRATEGY_CHANGE_ENABLED = False

INSUFFICIENT_DATA_MAX_SCORE = Decimal("50")
BLOCKING_FAILURE_MAX_SCORE = Decimal("40")


class ReviewScorecardBuilder:
    """
    Builds a ReviewScorecard with versioned weights.
    Insufficient data → score cannot be high.
    Blocking failure → score ceiling applied.
    Score does not trigger any automatic changes.
    """

    def build(
        self,
        session_id: str,
        dimension_scores: Dict[ScorecardDimension, Decimal],
        dimension_qualities: Dict[ScorecardDimension, MetricQuality],
        blocking_failures: Optional[List[str]] = None,
        warnings: Optional[List[str]] = None,
    ) -> ReviewScorecard:
        scorecard = ReviewScorecard(
            session_id=session_id,
            blocking_failures=blocking_failures or [],
            warnings=warnings or [],
            weight_version=SCORECARD_WEIGHT_VERSION,
        )

        # Apply scores with quality ceiling
        def _apply(dim: ScorecardDimension, attr: str) -> None:
            score = dimension_scores.get(dim, Decimal("0"))
            quality = dimension_qualities.get(dim, MetricQuality.UNKNOWN)
            score = validate_score(score, dim.value)
            if quality in (MetricQuality.INSUFFICIENT_DATA, MetricQuality.UNKNOWN):
                score = min(score, INSUFFICIENT_DATA_MAX_SCORE)
            setattr(scorecard, attr, score)

        _apply(ScorecardDimension.DATA_QUALITY, "data_quality_score")
        _apply(ScorecardDimension.SIGNAL_QUALITY, "signal_quality_score")
        _apply(ScorecardDimension.STRATEGY_QUALITY, "strategy_quality_score")
        _apply(ScorecardDimension.EXECUTION_QUALITY, "execution_quality_score")
        _apply(ScorecardDimension.OPERATIONAL_QUALITY, "operational_quality_score")
        _apply(ScorecardDimension.RISK_DISCIPLINE, "risk_discipline_score")
        _apply(ScorecardDimension.RECOVERY_QUALITY, "recovery_quality_score")

        # Apply blocking failure ceiling
        if blocking_failures:
            scorecard.score_ceiling = BLOCKING_FAILURE_MAX_SCORE

        scorecard.compute_overall()

        # Determine quality
        all_qualities = list(dimension_qualities.values())
        if all(q == MetricQuality.VALID for q in all_qualities):
            scorecard.quality = MetricQuality.VALID
        elif any(q in (MetricQuality.INSUFFICIENT_DATA, MetricQuality.UNKNOWN) for q in all_qualities):
            scorecard.quality = MetricQuality.PARTIAL
        else:
            scorecard.quality = MetricQuality.PARTIAL

        return scorecard


__all__ = ["ReviewScorecardBuilder", "INSUFFICIENT_DATA_MAX_SCORE", "BLOCKING_FAILURE_MAX_SCORE"]
