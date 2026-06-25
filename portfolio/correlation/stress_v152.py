"""
portfolio/correlation/stress_v152.py — Correlation Stress Analyzer v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No prediction claims. Assumptions listed. Original matrix never modified.
"""
from __future__ import annotations

import copy
import hashlib
import json
import datetime
import uuid
from typing import Any, Dict, List

from portfolio.correlation.enums_v152 import CorrelationMethod, CorrelationStatus
from portfolio.correlation.models_v152 import (
    CorrelationMatrixResult,
    ETFOverlapResult,
    ExposureBucket,
)

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


def _compute_hash(data: Any) -> str:
    payload = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def _clone_matrix(result: CorrelationMatrixResult) -> CorrelationMatrixResult:
    """Deep copy a CorrelationMatrixResult."""
    return CorrelationMatrixResult(
        matrix_id=f"STRESS_{uuid.uuid4().hex[:8].upper()}",
        symbols=list(result.symbols),
        matrix=[list(row) for row in result.matrix],
        observation_counts=dict(result.observation_counts),
        method=result.method,
        alignment_method=result.alignment_method,
        lookback_days=result.lookback_days,
        start_date=result.start_date,
        end_date=result.end_date,
        minimum_observations=result.minimum_observations,
        high_correlation_pairs=list(result.high_correlation_pairs),
        invalid_pairs=list(result.invalid_pairs),
        status=result.status,
        generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source_lineage_ids=list(result.source_lineage_ids),
        metadata=dict(result.metadata),
    )


class CorrelationStressAnalyzer:
    """
    Stress-test scenarios for correlation matrices.
    Each scenario creates a NEW matrix — the original is NEVER modified.
    No prediction claims. Pure research analytics.
    """

    RESEARCH_ONLY = True

    def run_correlation_spike(
        self,
        correlation_matrix: CorrelationMatrixResult,
        spike_amount: float = 0.2,
    ) -> CorrelationMatrixResult:
        """
        Add spike_amount to all off-diagonal entries, clip to [-1, 1].
        Original matrix not modified.
        """
        stressed = _clone_matrix(correlation_matrix)
        n = len(stressed.symbols)
        for i in range(n):
            for j in range(n):
                if i != j:
                    stressed.matrix[i][j] = max(-1.0, min(1.0, stressed.matrix[i][j] + spike_amount))
        stressed.content_hash = _compute_hash(stressed.matrix)
        stressed.metadata["scenario"] = "CORRELATION_SPIKE"
        stressed.metadata["spike_amount"] = spike_amount
        stressed.metadata["assumptions"] = [
            "RESEARCH_ONLY",
            "HYPOTHETICAL_STRESS_SCENARIO",
            "NOT_A_PREDICTION",
            f"All off-diagonal entries increased by {spike_amount}, clipped to [-1,1]",
        ]
        return stressed

    def run_diversification_breakdown(
        self,
        matrix: CorrelationMatrixResult,
        cluster_threshold: float = 0.75,
    ) -> CorrelationMatrixResult:
        """
        Set within-cluster off-diagonal correlations to 0.95 (breakdown scenario).
        Clusters identified by current threshold.
        """
        from portfolio.correlation.cluster_v152 import CorrelationClusterBuilder
        stressed = _clone_matrix(matrix)
        clusters = CorrelationClusterBuilder().build_threshold_graph(stressed, cluster_threshold)

        sym_idx = {s: i for i, s in enumerate(stressed.symbols)}
        for cluster in clusters:
            if len(cluster.symbols) < 2:
                continue
            for si in cluster.symbols:
                for sj in cluster.symbols:
                    if si != sj:
                        ii = sym_idx[si]
                        jj = sym_idx[sj]
                        stressed.matrix[ii][jj] = 0.95

        stressed.content_hash = _compute_hash(stressed.matrix)
        stressed.metadata["scenario"] = "DIVERSIFICATION_BREAKDOWN"
        stressed.metadata["cluster_threshold"] = cluster_threshold
        stressed.metadata["assumptions"] = [
            "RESEARCH_ONLY",
            "HYPOTHETICAL_STRESS_SCENARIO",
            "NOT_A_PREDICTION",
            "Within-cluster correlations set to 0.95",
        ]
        return stressed

    def run_benchmark_sensitivity(
        self,
        beta_results: List,
        shock_percent: float = 0.1,
    ) -> Dict[str, Any]:
        """
        Estimate portfolio sensitivity to a benchmark shock of shock_percent.
        Returns descriptive dict — no orders, no execution.
        """
        symbol_impacts = {}
        for br in beta_results:
            if getattr(br, "status", "") == "VALID":
                estimated_return = br.beta * shock_percent
                symbol_impacts[br.symbol] = {
                    "beta": br.beta,
                    "benchmark_shock": shock_percent,
                    "estimated_return": estimated_return,
                }

        return {
            "scenario": "BENCHMARK_SENSITIVITY",
            "shock_percent": shock_percent,
            "symbol_impacts": symbol_impacts,
            "assumptions": [
                "RESEARCH_ONLY",
                "HYPOTHETICAL_STRESS_SCENARIO",
                "NOT_A_PREDICTION",
                "Linear beta approximation only",
                "Does not account for non-linearity or tail events",
            ],
            "research_only": True,
        }

    def run_industry_co_movement(
        self,
        matrix: CorrelationMatrixResult,
        industry_exposure: List[ExposureBucket],
        boost: float = 0.15,
    ) -> CorrelationMatrixResult:
        """
        Boost same-industry correlations by boost amount, clipped to [-1, 1].
        """
        stressed = _clone_matrix(matrix)

        # Build symbol→industry map from exposure buckets
        # (industry_exposure gives bucket-level data, not symbol-level)
        # We rely on metadata if available; otherwise skip per-symbol lookup
        n = len(stressed.symbols)

        # Collect industry info from bucket metadata if present
        sym_industry: Dict[str, str] = {}
        for bucket in industry_exposure:
            for sym_info in bucket.metadata.get("symbols", []):
                sym = sym_info if isinstance(sym_info, str) else sym_info.get("symbol", "")
                if sym:
                    sym_industry[sym] = bucket.key

        sym_idx = {s: i for i, s in enumerate(stressed.symbols)}
        for i, si in enumerate(stressed.symbols):
            for j, sj in enumerate(stressed.symbols):
                if i < j:
                    ind_i = sym_industry.get(si, "")
                    ind_j = sym_industry.get(sj, "")
                    if ind_i and ind_j and ind_i == ind_j:
                        new_val = max(-1.0, min(1.0, stressed.matrix[i][j] + boost))
                        stressed.matrix[i][j] = new_val
                        stressed.matrix[j][i] = new_val

        stressed.content_hash = _compute_hash(stressed.matrix)
        stressed.metadata["scenario"] = "INDUSTRY_CO_MOVEMENT"
        stressed.metadata["boost"] = boost
        stressed.metadata["assumptions"] = [
            "RESEARCH_ONLY",
            "HYPOTHETICAL_STRESS_SCENARIO",
            "NOT_A_PREDICTION",
            f"Same-industry correlations boosted by {boost}",
        ]
        return stressed

    def run_etf_overlap_shock(
        self,
        matrix: CorrelationMatrixResult,
        etf_overlaps: List[ETFOverlapResult],
        shock: float = 0.3,
    ) -> CorrelationMatrixResult:
        """
        Boost correlations between ETF-overlapping symbols by shock amount.
        """
        stressed = _clone_matrix(matrix)
        sym_idx = {s: i for i, s in enumerate(stressed.symbols)}

        for overlap in etf_overlaps:
            if overlap.status != "VALID":
                continue
            affected = overlap.overlapping_constituents
            for i, si in enumerate(affected):
                for j, sj in enumerate(affected):
                    if i < j and si in sym_idx and sj in sym_idx:
                        ii = sym_idx[si]
                        jj = sym_idx[sj]
                        new_val = max(-1.0, min(1.0, stressed.matrix[ii][jj] + shock))
                        stressed.matrix[ii][jj] = new_val
                        stressed.matrix[jj][ii] = new_val

        stressed.content_hash = _compute_hash(stressed.matrix)
        stressed.metadata["scenario"] = "ETF_OVERLAP_SHOCK"
        stressed.metadata["shock"] = shock
        stressed.metadata["assumptions"] = [
            "RESEARCH_ONLY",
            "HYPOTHETICAL_STRESS_SCENARIO",
            "NOT_A_PREDICTION",
            f"ETF-overlapping symbol correlations boosted by {shock}",
        ]
        return stressed
