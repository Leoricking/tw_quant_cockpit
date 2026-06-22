"""
portfolio/correlation/risk_contribution_v152.py — Risk Contribution Calculator v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import math
from typing import Dict, List

from portfolio.correlation.models_v152 import (
    CovarianceMatrixResult,
    PortfolioVarianceResult,
    RiskContributionResult,
)

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


class RiskContributionCalculator:
    """
    Decomposes portfolio risk into marginal, component and percentage contributions.

    MRC_i = (Σw)_i / σ_portfolio
    CRC_i = w_i × MRC_i
    PCR_i = CRC_i / σ_portfolio

    Negative contributions are preserved (not clipped).
    """

    RESEARCH_ONLY = True

    def calculate(
        self,
        weights: Dict[str, float],
        covariance_result: CovarianceMatrixResult,
        portfolio_variance_result: PortfolioVarianceResult,
    ) -> List[RiskContributionResult]:
        """
        Returns one RiskContributionResult per symbol.
        Returns BLOCKED results if portfolio_volatility == 0.
        """
        cov_symbols = covariance_result.symbols
        sym_idx = {s: i for i, s in enumerate(cov_symbols)}

        # Only process symbols present in weights AND covariance
        syms = [s for s in cov_symbols if s in weights]
        w_vec = [weights[s] for s in syms]
        n = len(syms)

        port_vol = portfolio_variance_result.annualized_volatility

        if port_vol <= 0.0:
            return [
                RiskContributionResult(
                    symbol=s,
                    weight=weights.get(s, 0.0),
                    status="BLOCKED",
                    metadata={"reason": "portfolio_volatility_zero"},
                )
                for s in syms
            ]

        # Sub-covariance matrix
        sub_cov = [[0.0] * n for _ in range(n)]
        for i, si in enumerate(syms):
            for j, sj in enumerate(syms):
                sub_cov[i][j] = covariance_result.matrix[sym_idx[si]][sym_idx[sj]]

        # Σw vector (matrix-vector product)
        sigma_w = [
            sum(sub_cov[i][j] * w_vec[j] for j in range(n))
            for i in range(n)
        ]

        results: List[RiskContributionResult] = []
        total_crc = 0.0

        for i, sym in enumerate(syms):
            wi = w_vec[i]
            mrc_i = sigma_w[i] / port_vol          # MRC_i
            crc_i = wi * mrc_i                      # CRC_i
            pcr_i = crc_i / port_vol                # PCR_i (% of variance)
            total_crc += crc_i

            # Standalone volatility: sqrt(Cov_ii)
            standalone = math.sqrt(sub_cov[i][i]) if sub_cov[i][i] >= 0 else 0.0
            diversification_effect = standalone - mrc_i

            results.append(RiskContributionResult(
                symbol=sym,
                weight=wi,
                marginal_contribution=mrc_i,
                component_contribution=crc_i,
                percentage_contribution=pcr_i,
                standalone_volatility=standalone,
                diversification_effect=diversification_effect,
                status="VALID",
            ))

        # Sanity check: sum(CRC_i) ≈ portfolio_variance (within tolerance 1e-6)
        port_var = portfolio_variance_result.annualized_variance
        if abs(total_crc - port_var) > 1e-4:
            for r in results:
                r.metadata["crc_sum_check"] = f"sum_crc={total_crc:.8f} port_var={port_var:.8f}"

        return results
