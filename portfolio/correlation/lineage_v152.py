"""
portfolio/correlation/lineage_v152.py — Correlation Exposure Lineage Tracker v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List

from portfolio.correlation.models_v152 import CorrelationExposureAnalysis

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"


class CorrelationExposureLineageTracker:
    """
    Builds and validates complete lineage dictionaries for a correlation analysis.
    Validates: no orphan results — analysis must have snapshot_hash, matrix must have price_lineage.
    """

    RESEARCH_ONLY = True

    def build_lineage(
        self,
        analysis: CorrelationExposureAnalysis,
        snapshot_hash: str = "",
        price_lineage: Dict[str, Any] = None,
        benchmark_lineage: Dict[str, Any] = None,
        classification_lineage: Dict[str, Any] = None,
        etf_holdings_lineage: Dict[str, Any] = None,
        sizing_proposal_hash: str = "",
        policy_version: str = "",
        calculation_version: str = "1.5.2",
        thresholds: Dict[str, Any] = None,
        assumptions: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Build a complete lineage dict for the analysis.
        Validates: snapshot_hash required, price_lineage required for matrix.
        """
        price_lineage         = price_lineage or {}
        benchmark_lineage     = benchmark_lineage or {}
        classification_lineage = classification_lineage or {}
        etf_holdings_lineage  = etf_holdings_lineage or {}
        thresholds            = thresholds or {}
        assumptions           = assumptions or []

        errors: List[str] = []

        # Validate: no orphan results
        if not snapshot_hash:
            errors.append("LINEAGE_ERROR: snapshot_hash is missing")
        if not price_lineage:
            errors.append("LINEAGE_ERROR: price_lineage is empty — matrix has no price lineage")

        lineage = {
            "analysis_id":            analysis.analysis_id,
            "portfolio_id":           analysis.request.portfolio_id,
            "snapshot_id":            analysis.request.snapshot_id,
            "snapshot_hash":          snapshot_hash,
            "as_of":                  analysis.request.as_of,
            "available_from":         analysis.request.available_from,
            "calculation_version":    calculation_version,
            "policy_version":         policy_version,
            "price_lineage":          price_lineage,
            "benchmark_lineage":      benchmark_lineage,
            "classification_lineage": classification_lineage,
            "etf_holdings_lineage":   etf_holdings_lineage,
            "sizing_proposal_hash":   sizing_proposal_hash,
            "symbols":                list(analysis.request.symbols),
            "return_method":          analysis.request.return_method.value,
            "correlation_method":     analysis.request.correlation_method.value,
            "alignment_method":       analysis.request.alignment_method.value,
            "lookback_days":          analysis.request.lookback_days,
            "minimum_observations":   analysis.request.minimum_observations,
            "high_corr_threshold":    analysis.request.high_correlation_threshold,
            "cluster_threshold":      analysis.request.cluster_threshold,
            "source_lineage_ids":     list(analysis.request.source_lineage_ids),
            "correlation_matrix_id":  analysis.correlation_matrix.matrix_id,
            "correlation_content_hash": analysis.correlation_matrix.content_hash,
            "aligned_returns_hash":   analysis.aligned_returns.content_hash,
            "thresholds":             thresholds,
            "assumptions":            assumptions,
            "lineage_errors":         errors,
            "lineage_valid":          len(errors) == 0,
            "generated_at":           datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "research_only":          True,
            "labels":                 analysis.labels,
        }

        return lineage
