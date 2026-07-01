"""
paper_trading/multi_session/scorecard_v166.py — Multi-session Coordination Scorecard v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] 0-100 score. Blocking failure caps max score. Unknown != full score.
[!] No automatic production action.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
NO_AUTO_PRODUCTION_ACTION = True

SCORECARD_WEIGHTS: Dict[str, int] = {
    "registration_integrity": 8,
    "resource_coordination": 12,
    "conflict_detection": 12,
    "conflict_resolution": 10,
    "fairness": 8,
    "event_ordering": 10,
    "data_isolation": 10,
    "risk_coordination": 10,
    "capital_coordination": 5,
    "lifecycle_safety": 5,
    "failure_isolation": 5,
    "replay_reproducibility": 5,
}
assert sum(SCORECARD_WEIGHTS.values()) == 100


@dataclass
class ScorecardResult:
    total_score: int
    dimension_scores: Dict[str, float]
    blocking_failures: List[str]
    unknown_dimensions: List[str]
    capped: bool
    explanation: Dict[str, str]

    def is_blocking(self) -> bool:
        return len(self.blocking_failures) > 0


class MultiSessionScorecard:
    """
    Computes 0-100 coordination scorecard.
    Blocking failure caps maximum score. Unknown != full score.
    """

    def compute(
        self,
        dimension_results: Dict[str, Any],
    ) -> ScorecardResult:
        dimension_scores: Dict[str, float] = {}
        blocking_failures: List[str] = []
        unknown_dimensions: List[str] = []
        explanation: Dict[str, str] = {}

        for dim, weight in SCORECARD_WEIGHTS.items():
            result = dimension_results.get(dim)
            if result is None:
                unknown_dimensions.append(dim)
                dimension_scores[dim] = 0.0
                explanation[dim] = "unknown — scored 0"
            elif result is True or result == "PASS":
                dimension_scores[dim] = float(weight)
                explanation[dim] = "pass"
            elif result is False or result == "FAIL":
                dimension_scores[dim] = 0.0
                blocking_failures.append(dim)
                explanation[dim] = "fail — blocking"
            elif result == "WARN":
                dimension_scores[dim] = weight * 0.7
                explanation[dim] = "warn — partial credit"
            elif isinstance(result, (int, float)):
                dimension_scores[dim] = min(float(weight), float(result))
                explanation[dim] = f"partial: {result}"
            else:
                unknown_dimensions.append(dim)
                dimension_scores[dim] = 0.0
                explanation[dim] = f"unrecognized result type: {type(result).__name__}"

        total = sum(dimension_scores.values())
        capped = False

        if blocking_failures:
            total = min(total, 60.0)
            capped = True

        return ScorecardResult(
            total_score=int(total),
            dimension_scores=dimension_scores,
            blocking_failures=blocking_failures,
            unknown_dimensions=unknown_dimensions,
            capped=capped,
            explanation=explanation,
        )
