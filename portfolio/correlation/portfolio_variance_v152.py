"""
portfolio/correlation/portfolio_variance_v152.py — Portfolio Variance Calculator v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List

from portfolio.correlation.enums_v152 import CorrelationStatus
from portfolio.correlation.models_v152 import CovarianceMatrixResult, PortfolioVarianceResult

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


class PortfolioVarianceCalculator:
    """
    Computes portfolio variance wᵀΣw using pure Python matrix math.
    Descriptive only — no optimization, no rebalance.
    """

    RESEARCH_ONLY = True

    def calculate(
        self,
        portfolio_id: str,
        as_of: str,
        weights: Dict[str, float],
        covariance_result: CovarianceMatrixResult,
    ) -> PortfolioVarianceResult:
        """
        Compute portfolio variance from weights and covariance matrix.

        Validates:
        - weights ordering matches covariance symbols
        - weights sum ≈ 1.0 (within 0.01)
        - no negative weights
        - all symbols in covariance matrix
        - covariance status == VALID
        """
        base = PortfolioVarianceResult(
            portfolio_id=portfolio_id,
            as_of=as_of,
            weights=weights,
        )

        # Blocked if covariance not valid
        if covariance_result.status != CorrelationStatus.VALID:
            base.calculation_status = "BLOCKED"
            base.assumptions = [f"BLOCKED: covariance status={covariance_result.status.value}"]
            return base

        cov_symbols = covariance_result.symbols
        cov_set = set(cov_symbols)

        # All weight symbols must be in covariance matrix
        missing = [s for s in weights if s not in cov_set]
        if missing:
            base.calculation_status = "BLOCKED"
            base.assumptions = [f"BLOCKED: symbols not in covariance matrix: {missing}"]
            return base

        # Check weights sum
        w_sum = sum(weights.values())
        if abs(w_sum - 1.0) > 0.01:
            base.calculation_status = "BLOCKED"
            base.assumptions = [f"BLOCKED: weights sum={w_sum:.6f}, expected ~1.0"]
            return base

        # No negative weights
        neg = [s for s, w in weights.items() if w < 0]
        if neg:
            base.calculation_status = "BLOCKED"
            base.assumptions = [f"BLOCKED: negative weights for {neg}"]
            return base

        # Order weights to match covariance symbols
        # (only use symbols that appear in weights)
        w_syms = [s for s in cov_symbols if s in weights]
        w_vec = [weights[s] for s in w_syms]

        # Build sub-matrix for w_syms
        sym_idx = {s: i for i, s in enumerate(cov_symbols)}
        n = len(w_syms)
        sub_cov = [[0.0] * n for _ in range(n)]
        for i, si in enumerate(w_syms):
            for j, sj in enumerate(w_syms):
                sub_cov[i][j] = covariance_result.matrix[sym_idx[si]][sym_idx[sj]]

        # wᵀΣw — annualized covariance matrix already annualized
        # σ_p² = Σ_i Σ_j w_i * w_j * Cov_ij
        annualized_variance = sum(
            w_vec[i] * w_vec[j] * sub_cov[i][j]
            for i in range(n)
            for j in range(n)
        )
        annualized_variance = max(0.0, annualized_variance)
        annualized_volatility = math.sqrt(annualized_variance)

        ann_factor = covariance_result.annualization_factor or 252
        daily_variance = annualized_variance / ann_factor
        daily_volatility = math.sqrt(daily_variance) if daily_variance > 0 else 0.0

        assumptions = [
            "RESEARCH_ONLY",
            "DESCRIPTIVE_ANALYTICS_ONLY",
            f"annualization_factor={ann_factor}",
            "no_optimization",
            "no_rebalance",
        ]

        return PortfolioVarianceResult(
            portfolio_id=portfolio_id,
            as_of=as_of,
            weights=weights,
            daily_variance=daily_variance,
            daily_volatility=daily_volatility,
            annualized_variance=annualized_variance,
            annualized_volatility=annualized_volatility,
            calculation_status="VALID",
            assumptions=assumptions,
        )
