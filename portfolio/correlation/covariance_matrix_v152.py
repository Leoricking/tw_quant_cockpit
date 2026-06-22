"""
portfolio/correlation/covariance_matrix_v152.py — Covariance Matrix Service v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Dict, List

from portfolio.correlation.enums_v152 import CorrelationStatus
from portfolio.correlation.models_v152 import AlignedReturnSeries, CovarianceMatrixResult

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


def _mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _compute_hash(data: Any) -> str:
    payload = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


class CovarianceMatrixService:
    """
    Computes annualised covariance matrix from aligned returns.
    Pure Python stdlib — no numpy required.
    """

    RESEARCH_ONLY = True

    def calculate(
        self,
        aligned: AlignedReturnSeries,
        annualization_factor: int = 252,
    ) -> CovarianceMatrixResult:
        """
        Compute covariance matrix.

        Returns an annualised CovarianceMatrixResult.
        """
        symbols = aligned.symbols
        n = len(symbols)
        returns = aligned.returns_by_symbol

        obs_count = aligned.observation_count

        if obs_count < 2:
            empty = [[0.0] * n for _ in range(n)]
            return CovarianceMatrixResult(
                symbols=symbols,
                matrix=empty,
                annualization_factor=annualization_factor,
                observation_count=obs_count,
                status=CorrelationStatus.INSUFFICIENT_SAMPLE,
            )

        # Build daily covariance matrix
        matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                xs = returns.get(symbols[i], [])
                ys = returns.get(symbols[j], [])
                pair_len = min(len(xs), len(ys))
                if pair_len < 2:
                    cov = 0.0
                else:
                    xs_t = xs[:pair_len]
                    ys_t = ys[:pair_len]
                    mx = _mean(xs_t)
                    my = _mean(ys_t)
                    cov = sum((xs_t[k] - mx) * (ys_t[k] - my) for k in range(pair_len)) / (pair_len - 1)
                # Annualise
                cov_ann = cov * annualization_factor
                matrix[i][j] = cov_ann
                matrix[j][i] = cov_ann

        # Validate: positive diagonal
        for i in range(n):
            if matrix[i][i] < 0:
                matrix[i][i] = abs(matrix[i][i])  # fix numerical artifact

        content_hash = _compute_hash({"matrix": matrix, "symbols": symbols})

        return CovarianceMatrixResult(
            symbols=symbols,
            matrix=matrix,
            annualization_factor=annualization_factor,
            observation_count=obs_count,
            status=aligned.status if aligned.status != CorrelationStatus.VALID else CorrelationStatus.VALID,
            content_hash=content_hash,
        )
