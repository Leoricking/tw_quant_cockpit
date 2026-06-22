"""
portfolio/correlation/hidden_concentration_v152.py — Hidden Concentration Detector v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

from portfolio.correlation.enums_v152 import ConcentrationRiskLevel
from portfolio.correlation.models_v152 import (
    CorrelationCluster,
    ETFOverlapResult,
    ExposureBucket,
    HiddenConcentrationResult,
    RiskContributionResult,
)

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


class HiddenConcentrationDetector:
    """
    Detects hidden concentration beyond apparent position count.
    Transparent scoring — no ML, no black box.
    Score 0-100 components documented in evidence dict.
    """

    RESEARCH_ONLY = True

    def detect(
        self,
        clusters: List[CorrelationCluster],
        risk_contributions: List[RiskContributionResult],
        industry_exposure: List[ExposureBucket],
        theme_exposure: List[ExposureBucket],
        etf_overlaps: List[ETFOverlapResult],
        weights: Dict[str, float],
    ) -> HiddenConcentrationResult:
        """
        Compute hidden concentration metrics from all exposure inputs.
        """
        apparent_count = len(weights)

        # effective_independent_bets = 1 / Σ(cluster_weight²)
        cluster_weights_sq_sum = sum(c.portfolio_weight ** 2 for c in clusters) if clusters else 0.0
        effective_bets = 1.0 / cluster_weights_sq_sum if cluster_weights_sq_sum > 0 else float(apparent_count)

        # Largest cluster weight
        all_cluster_weights = sorted([c.portfolio_weight for c in clusters], reverse=True)
        largest_cw = all_cluster_weights[0] if all_cluster_weights else 0.0
        top_cluster_weights = all_cluster_weights[:5]

        # Correlated pair count
        correlated_pair_count = sum(len(c.symbols) * (len(c.symbols) - 1) // 2 for c in clusters if len(c.symbols) > 1)

        # Industry overlap score: max single-industry weight
        industry_overlap_score = max((b.gross_weight for b in industry_exposure), default=0.0)

        # Theme overlap score: max single-theme weight (can exceed 1.0 for overlapping themes)
        theme_overlap_score = max((b.gross_weight for b in theme_exposure), default=0.0)

        # ETF overlap score: max combined_effective_exposure
        etf_overlap_score = max((e.combined_effective_exposure for e in etf_overlaps if e.status == "VALID"), default=0.0)

        # Concentration level based on largest cluster weight
        if largest_cw > 0.7:
            level = ConcentrationRiskLevel.CRITICAL
        elif largest_cw > 0.5:
            level = ConcentrationRiskLevel.HIGH
        elif largest_cw > 0.3:
            level = ConcentrationRiskLevel.MODERATE
        elif largest_cw > 0.0:
            level = ConcentrationRiskLevel.LOW
        else:
            level = ConcentrationRiskLevel.UNKNOWN

        # Transparent score 0-100
        # Components:
        #   cluster_score    (0-40): based on largest_cluster_weight
        #   industry_score   (0-30): based on industry_overlap_score
        #   etf_score        (0-20): based on etf_overlap_score
        #   diversity_score  (0-10): inversely based on effective_bets vs apparent_count
        cluster_score    = min(40.0, largest_cw * 40.0 / 0.7)
        industry_score   = min(30.0, industry_overlap_score * 30.0)
        etf_score        = min(20.0, etf_overlap_score * 20.0)
        diversity_ratio  = (apparent_count - effective_bets) / apparent_count if apparent_count > 0 else 0.0
        diversity_score  = min(10.0, max(0.0, diversity_ratio * 10.0))
        total_score      = cluster_score + industry_score + etf_score + diversity_score

        evidence: Dict[str, Any] = {
            "score_formula": "cluster_score(0-40) + industry_score(0-30) + etf_score(0-20) + diversity_score(0-10)",
            "cluster_score":    round(cluster_score, 4),
            "industry_score":   round(industry_score, 4),
            "etf_score":        round(etf_score, 4),
            "diversity_score":  round(diversity_score, 4),
            "total_score":      round(total_score, 4),
            "cluster_count":    len(clusters),
            "effective_bets":   round(effective_bets, 4),
            "research_only":    True,
            "not_a_prediction": True,
        }

        warnings: List[str] = []
        if level in (ConcentrationRiskLevel.HIGH, ConcentrationRiskLevel.CRITICAL):
            warnings.append(f"HIGH_CONCENTRATION: largest_cluster_weight={largest_cw:.3f}")
        if etf_overlap_score > 0.2:
            warnings.append(f"ETF_OVERLAP: max_combined_exposure={etf_overlap_score:.3f}")
        if theme_overlap_score > 0.5:
            warnings.append(f"THEME_OVERLAP: max_theme_weight={theme_overlap_score:.3f}")

        return HiddenConcentrationResult(
            apparent_position_count=apparent_count,
            effective_independent_bets=effective_bets,
            largest_cluster_weight=largest_cw,
            top_cluster_weights=top_cluster_weights,
            correlated_pair_count=correlated_pair_count,
            industry_overlap_score=industry_overlap_score,
            theme_overlap_score=theme_overlap_score,
            ETF_overlap_score=etf_overlap_score,
            hidden_concentration_level=level,
            warnings=warnings,
            evidence=evidence,
        )
