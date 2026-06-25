"""
portfolio/correlation/correlation_matrix_v152.py — Correlation Matrix Service v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import math
from typing import Any, Dict, List, Optional, Tuple

from portfolio.correlation.enums_v152 import (
    AlignmentMethod,
    CorrelationMethod,
    CorrelationStatus,
)
from portfolio.correlation.models_v152 import AlignedReturnSeries, CorrelationMatrixResult

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


def _mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _stddev(xs: List[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    variance = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return math.sqrt(variance)


def _pearson_pair(xs: List[float], ys: List[float]) -> Tuple[float, bool]:
    """
    Returns (correlation, is_constant).
    is_constant=True if either series is constant.
    """
    n = min(len(xs), len(ys))
    if n < 2:
        return (0.0, True)
    xs = xs[:n]
    ys = ys[:n]
    sx = _stddev(xs)
    sy = _stddev(ys)
    if sx == 0.0 or sy == 0.0:
        return (0.0, True)
    mx = _mean(xs)
    my = _mean(ys)
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / (n - 1)
    r = cov / (sx * sy)
    # clip to [-1, 1] for numerical safety
    r = max(-1.0, min(1.0, r))
    return (r, False)


def _rank_series(xs: List[float]) -> List[float]:
    """Average-rank transformation handling ties."""
    n = len(xs)
    # Sort indices by value
    indexed = sorted(range(n), key=lambda i: xs[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n and xs[indexed[j]] == xs[indexed[i]]:
            j += 1
        avg_rank = (i + j - 1) / 2.0 + 1  # 1-based average rank
        for k in range(i, j):
            ranks[indexed[k]] = avg_rank
        i = j
    return ranks


def _compute_hash(data: Any) -> str:
    payload = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def _build_result(
    aligned: AlignedReturnSeries,
    matrix: List[List[float]],
    method: CorrelationMethod,
    high_corr_threshold: float,
    min_obs: int,
    invalid_pairs: List[Dict],
) -> CorrelationMatrixResult:
    symbols = aligned.symbols
    n = len(symbols)

    # Validate symmetry & diagonal
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 1.0  # enforce
            else:
                # enforce symmetry
                avg = (matrix[i][j] + matrix[j][i]) / 2.0
                matrix[i][j] = avg
                matrix[j][i] = avg

    high_corr_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            r = matrix[i][j]
            if abs(r) >= high_corr_threshold:
                high_corr_pairs.append({
                    "symbol_a": symbols[i],
                    "symbol_b": symbols[j],
                    "correlation": r,
                })

    obs_counts: Dict[str, int] = {s: aligned.observation_count for s in symbols}

    status = aligned.status if aligned.status != CorrelationStatus.VALID else CorrelationStatus.VALID
    if invalid_pairs:
        status = CorrelationStatus.PARTIAL

    content_hash = _compute_hash({"matrix": matrix, "symbols": symbols})
    generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    import uuid
    matrix_id = f"CORR_{method.value}_{uuid.uuid4().hex[:8].upper()}"

    return CorrelationMatrixResult(
        matrix_id=matrix_id,
        symbols=symbols,
        matrix=matrix,
        observation_counts=obs_counts,
        method=method,
        alignment_method=aligned.alignment_method,
        lookback_days=aligned.observation_count,
        start_date=aligned.start_date,
        end_date=aligned.end_date,
        minimum_observations=min_obs,
        high_correlation_pairs=high_corr_pairs,
        invalid_pairs=invalid_pairs,
        status=status,
        generated_at=generated_at,
        content_hash=content_hash,
    )


class CorrelationMatrixService:
    """
    Computes Pearson and Spearman correlation matrices.
    Pure Python stdlib — no numpy/scipy required.
    """

    RESEARCH_ONLY = True

    def calculate_pearson(
        self,
        aligned: AlignedReturnSeries,
        high_corr_threshold: float = 0.75,
        min_obs: int = 60,
    ) -> CorrelationMatrixResult:
        """
        Compute Pearson correlation matrix from aligned return series.
        """
        symbols = aligned.symbols
        n = len(symbols)
        returns = aligned.returns_by_symbol

        matrix = [[0.0] * n for _ in range(n)]
        invalid_pairs: List[Dict] = []

        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] = 1.0
                elif j > i:
                    xs = returns.get(symbols[i], [])
                    ys = returns.get(symbols[j], [])
                    r, is_const = _pearson_pair(xs, ys)
                    if is_const:
                        invalid_pairs.append({
                            "symbol_a": symbols[i],
                            "symbol_b": symbols[j],
                            "reason": "CONSTANT_SERIES",
                        })
                        matrix[i][j] = 0.0
                        matrix[j][i] = 0.0
                    else:
                        matrix[i][j] = r
                        matrix[j][i] = r

        return _build_result(aligned, matrix, CorrelationMethod.PEARSON, high_corr_threshold, min_obs, invalid_pairs)

    def calculate_spearman(
        self,
        aligned: AlignedReturnSeries,
        high_corr_threshold: float = 0.75,
        min_obs: int = 60,
    ) -> CorrelationMatrixResult:
        """
        Compute Spearman correlation matrix.
        Rank-transforms returns (ties → average rank), then Pearson on ranks.
        """
        symbols = aligned.symbols
        n = len(symbols)
        returns = aligned.returns_by_symbol

        # Rank-transform each series
        ranked: Dict[str, List[float]] = {}
        for sym in symbols:
            rs = returns.get(sym, [])
            ranked[sym] = _rank_series(rs) if rs else []

        matrix = [[0.0] * n for _ in range(n)]
        invalid_pairs: List[Dict] = []

        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] = 1.0
                elif j > i:
                    xs = ranked.get(symbols[i], [])
                    ys = ranked.get(symbols[j], [])
                    r, is_const = _pearson_pair(xs, ys)
                    if is_const:
                        invalid_pairs.append({
                            "symbol_a": symbols[i],
                            "symbol_b": symbols[j],
                            "reason": "CONSTANT_SERIES",
                        })
                        matrix[i][j] = 0.0
                        matrix[j][i] = 0.0
                    else:
                        matrix[i][j] = r
                        matrix[j][i] = r

        result = _build_result(aligned, matrix, CorrelationMethod.SPEARMAN, high_corr_threshold, min_obs, invalid_pairs)
        return result
