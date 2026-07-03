"""
paper_trading/operational_integration/integration_scorecard_v168.py
Integration Scorecard for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict

from .models_v168 import IntegrationScore

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_WEIGHTS = {
    "contract": 15,
    "data_flow": 15,
    "lineage": 15,
    "identity": 10,
    "timestamp": 10,
    "reconciliation": 15,
    "determinism": 10,
    "failure_isolation": 5,
    "safety": 5,
}
assert sum(_WEIGHTS.values()) == 100, "Weights must sum to 100"


class IntegrationScorecard:
    """Computes integration quality scorecard. Research only."""

    def compute(self, run_result: Dict[str, Any]) -> IntegrationScore:
        """
        Compute integration score from run result.
        Each dimension is 0..100. Weighted sum produces total_score 0..100.
        """
        run_id = run_result.get("run_id", "unknown")

        # Extract individual dimension scores from run_result
        def _score(key: str, default: float = 100.0) -> float:
            v = run_result.get(f"{key}_score", default)
            try:
                return max(0.0, min(100.0, float(v)))
            except (TypeError, ValueError):
                return default

        contract_score = _score("contract")
        data_flow_score = _score("data_flow")
        lineage_score = _score("lineage")
        identity_score = _score("identity")
        timestamp_score = _score("timestamp")
        reconciliation_score = _score("reconciliation")
        determinism_score = _score("determinism")
        failure_isolation_score = _score("failure_isolation")
        safety_score = _score("safety")

        # Safety block: if safety score is 0, cap total at 0
        if self.check_safety_blocking(run_result):
            total_score = 0.0
            grade = "F"
        else:
            total_score = (
                contract_score * _WEIGHTS["contract"]
                + data_flow_score * _WEIGHTS["data_flow"]
                + lineage_score * _WEIGHTS["lineage"]
                + identity_score * _WEIGHTS["identity"]
                + timestamp_score * _WEIGHTS["timestamp"]
                + reconciliation_score * _WEIGHTS["reconciliation"]
                + determinism_score * _WEIGHTS["determinism"]
                + failure_isolation_score * _WEIGHTS["failure_isolation"]
                + safety_score * _WEIGHTS["safety"]
            ) / 100.0
            grade = self.get_grade(total_score)

        usable_for_research = total_score >= 60.0 and not self.check_safety_blocking(run_result)
        usable_for_paper_review = total_score >= 70.0 and not self.check_safety_blocking(run_result)

        return IntegrationScore(
            run_id=run_id,
            total_score=total_score,
            grade=grade,
            contract_score=contract_score,
            data_flow_score=data_flow_score,
            lineage_score=lineage_score,
            identity_score=identity_score,
            timestamp_score=timestamp_score,
            reconciliation_score=reconciliation_score,
            determinism_score=determinism_score,
            failure_isolation_score=failure_isolation_score,
            safety_score=safety_score,
            usable_for_research=usable_for_research,
            usable_for_paper_review=usable_for_paper_review,
            not_for_real_trading=True,
        )

    def get_grade(self, score: float) -> str:
        """Return letter grade for score."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def check_safety_blocking(self, run_result: Dict[str, Any]) -> bool:
        """Return True if safety violations would block this run."""
        safety_violations = run_result.get("safety_violations", [])
        broker_enabled = run_result.get("broker_enabled", False)
        real_orders = run_result.get("real_orders_enabled", False)
        return bool(safety_violations) or broker_enabled or real_orders

    def summarize(self, score: IntegrationScore) -> Dict[str, Any]:
        """Return summary of integration score."""
        return {
            "run_id": score.run_id,
            "total_score": score.total_score,
            "grade": score.grade,
            "usable_for_research": score.usable_for_research,
            "usable_for_paper_review": score.usable_for_paper_review,
            "not_for_real_trading": True,
            "dimension_scores": {
                "contract": score.contract_score,
                "data_flow": score.data_flow_score,
                "lineage": score.lineage_score,
                "identity": score.identity_score,
                "timestamp": score.timestamp_score,
                "reconciliation": score.reconciliation_score,
                "determinism": score.determinism_score,
                "failure_isolation": score.failure_isolation_score,
                "safety": score.safety_score,
            },
            "paper_only": True,
        }
