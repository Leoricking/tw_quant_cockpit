"""
paper_trading/performance_attribution/attribution_scorecard_v167.py
Attribution Quality Scorecard (0–100) for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Fixture cannot auto-score HIGH. Missing benchmark penalizes. Large residual penalizes.
[!] real marker → BLOCKING. non-determinism → FAIL or heavy penalty.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import ConfidenceLevel, ReconciliationStatus, DataQualityStatus
from .models_v167 import AttributionScore

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

# Scoring weights (sum = 100)
SCORE_WEIGHTS = {
    "reconciliation_quality":  25,
    "data_completeness":       20,
    "execution_data_quality":  15,
    "cost_completeness":       10,
    "benchmark_quality":       10,
    "risk_model_quality":      10,
    "lineage_quality":          5,
    "determinism":              5,
}
assert sum(SCORE_WEIGHTS.values()) == 100


def _grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


class AttributionScorecardEngine:
    """
    Computes 0–100 attribution quality score from validation results.
    Cannot be fixed to return PASS/100. Real markers → blocking issue.
    """

    def compute(
        self,
        entity_id: str,
        reconciliation_status: ReconciliationStatus,
        residual_pct: float,               # abs(residual) / total
        data_quality: DataQualityStatus,
        has_execution_data: bool,
        execution_simulated: bool,
        cost_quality: str,                  # "KNOWN", "ESTIMATED", "UNKNOWN"
        has_benchmark: bool,
        benchmark_stale: bool,
        has_risk_data: bool,
        risk_data_complete: bool,
        has_source_lineage: bool,
        deterministic: bool,
        has_real_markers: bool,
        has_credentials: bool,
        fixture_only: bool,
        period_start: str = "",
        period_end: str = "",
    ) -> AttributionScore:
        """Compute attribution quality score."""
        scores: Dict[str, float] = {}
        warnings: List[str] = []
        blocking_issues: List[str] = []

        # BLOCKING checks
        if has_real_markers:
            blocking_issues.append("BLOCKED: real order/account/broker markers present")
        if has_credentials:
            blocking_issues.append("BLOCKED: credentials/secrets present")
        if blocking_issues:
            return AttributionScore(
                entity_id=entity_id,
                total_score=0.0,
                grade="F",
                reconciliation_score=0.0,
                data_completeness_score=0.0,
                execution_quality_score=0.0,
                cost_completeness_score=0.0,
                benchmark_quality_score=0.0,
                risk_model_quality_score=0.0,
                lineage_quality_score=0.0,
                determinism_score=0.0,
                component_scores=scores,
                failed_dimensions=list(scores.keys()),
                warnings=warnings,
                blocking_issues=blocking_issues,
                confidence=ConfidenceLevel.UNKNOWN,
                usable_for_research=False,
                usable_for_paper_review=False,
                not_for_real_trading=True,
                period_start=period_start,
                period_end=period_end,
                paper_only=True,
                research_only=True,
                no_real_orders=True,
                not_for_production=True,
            )

        # 1. Reconciliation quality (25 pts)
        rec_score = {
            ReconciliationStatus.RECONCILED: 25.0,
            ReconciliationStatus.RECONCILED_WITH_ROUNDING: 20.0,
            ReconciliationStatus.DEGRADED: 10.0,
            ReconciliationStatus.FAILED: 0.0,
            ReconciliationStatus.INSUFFICIENT_DATA: 5.0,
        }.get(reconciliation_status, 0.0)
        if residual_pct > 0.01:  # >1% residual → penalize further
            rec_score = max(0.0, rec_score - 10.0)
            warnings.append(f"large_residual: {residual_pct:.2%}")
        scores["reconciliation_quality"] = rec_score

        # 2. Data completeness (20 pts)
        data_score = {
            DataQualityStatus.COMPLETE: 20.0,
            DataQualityStatus.PARTIAL: 12.0,
            DataQualityStatus.DEGRADED: 6.0,
            DataQualityStatus.INSUFFICIENT: 0.0,
            DataQualityStatus.UNKNOWN: 3.0,
        }.get(data_quality, 0.0)
        scores["data_completeness"] = data_score

        # 3. Execution data quality (15 pts)
        if not has_execution_data:
            exec_score = 5.0
            warnings.append("no_execution_data")
        elif not execution_simulated:
            exec_score = 0.0
            blocking_issues.append("BLOCKED: execution not marked simulated")
        else:
            exec_score = 15.0
        scores["execution_data_quality"] = exec_score

        # 4. Cost completeness (10 pts)
        cost_score = {"KNOWN": 10.0, "ESTIMATED": 6.0, "UNKNOWN": 0.0}.get(cost_quality, 0.0)
        if cost_quality == "UNKNOWN":
            warnings.append("unknown_cost: score penalized")
        scores["cost_completeness"] = cost_score

        # 5. Benchmark quality (10 pts)
        if not has_benchmark:
            bm_score = 0.0
            warnings.append("missing_benchmark: score penalized")
        elif benchmark_stale:
            bm_score = 4.0
            warnings.append("stale_benchmark")
        else:
            bm_score = 10.0
        scores["benchmark_quality"] = bm_score

        # 6. Risk model quality (10 pts)
        if not has_risk_data:
            risk_score = 0.0
            warnings.append("no_risk_data")
        elif not risk_data_complete:
            risk_score = 5.0
            warnings.append("incomplete_risk_data")
        else:
            risk_score = 10.0
        scores["risk_model_quality"] = risk_score

        # 7. Lineage quality (5 pts)
        lineage_score = 5.0 if has_source_lineage else 0.0
        if not has_source_lineage:
            warnings.append("missing_source_lineage")
        scores["lineage_quality"] = lineage_score

        # 8. Determinism (5 pts)
        if not deterministic:
            det_score = 0.0
            blocking_issues.append("FAIL: non-deterministic attribution")
        else:
            det_score = 5.0
        scores["determinism"] = det_score

        # Fixture penalty: fixtures cannot auto-score high
        if fixture_only:
            for key in scores:
                scores[key] = min(scores[key], scores[key] * 0.8)
            warnings.append("fixture_only: scores capped at 80%")

        total_score = round(sum(scores.values()), 2)
        grade = _grade(total_score)
        failed_dims = [k for k, v in scores.items() if v < SCORE_WEIGHTS[k] * 0.5]

        confidence = (
            ConfidenceLevel.HIGH if total_score >= 80 else
            ConfidenceLevel.MEDIUM if total_score >= 60 else
            ConfidenceLevel.LOW
        )

        usable_for_research = total_score >= 60 and not blocking_issues
        usable_for_paper_review = total_score >= 70 and not blocking_issues

        return AttributionScore(
            entity_id=entity_id,
            total_score=total_score,
            grade=grade,
            reconciliation_score=scores["reconciliation_quality"],
            data_completeness_score=scores["data_completeness"],
            execution_quality_score=scores["execution_data_quality"],
            cost_completeness_score=scores["cost_completeness"],
            benchmark_quality_score=scores["benchmark_quality"],
            risk_model_quality_score=scores["risk_model_quality"],
            lineage_quality_score=scores["lineage_quality"],
            determinism_score=scores["determinism"],
            component_scores=scores,
            failed_dimensions=failed_dims,
            warnings=warnings,
            blocking_issues=blocking_issues,
            confidence=confidence,
            usable_for_research=usable_for_research,
            usable_for_paper_review=usable_for_paper_review,
            not_for_real_trading=True,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )
