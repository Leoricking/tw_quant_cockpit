"""
portfolio/correlation/explain_v152.py — Correlation Exposure Explainer v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

from typing import Any, Dict, List

from portfolio.correlation.models_v152 import CorrelationExposureAnalysis

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"

SAFETY_TEXT = (
    "This is a research-only analysis. "
    "Correlation is historical and NOT predictive. "
    "No weight optimization. No auto rebalance. No broker connection. "
    "No real orders. Not investment advice."
)

LIMITATIONS = [
    "Historical correlation is not predictive of future correlation.",
    "Correlation can change rapidly in stress periods.",
    "Sample size affects reliability — use at least 60 observations.",
    "Pearson correlation assumes linearity; use Spearman for fat-tailed returns.",
    "ETF overlap analysis depends on ETF holdings data freshness.",
    "Industry/theme classifications may lag sector rotation.",
]


class CorrelationExposureExplainer:
    """
    Generates structured natural-language explanation of a correlation analysis result.
    """

    RESEARCH_ONLY = True

    def explain(
        self,
        analysis: CorrelationExposureAnalysis,
        lineage: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Returns structured explanation dict.
        """
        req = analysis.request
        corr = analysis.correlation_matrix
        cov  = analysis.covariance_matrix
        pv   = analysis.portfolio_variance

        # High-correlation pairs summary
        high_corr = [
            f"{p['symbol_a']}-{p['symbol_b']} ({p['correlation']:.3f})"
            for p in (corr.high_correlation_pairs or [])
        ]

        # Clusters summary
        cluster_summary = [
            {
                "cluster_id": c.cluster_id,
                "symbols": c.symbols,
                "weight": round(c.portfolio_weight, 4),
                "avg_corr": round(c.average_internal_correlation, 4),
            }
            for c in analysis.clusters
        ]

        # Risk contributors
        top_risk = sorted(
            analysis.risk_contributions,
            key=lambda r: abs(r.percentage_contribution),
            reverse=True
        )[:5]
        top_contributors = [
            {
                "symbol": r.symbol,
                "weight": round(r.weight, 4),
                "pct_contribution": round(r.percentage_contribution, 4),
            }
            for r in top_risk
        ]

        # Portfolio beta
        port_beta = None
        from portfolio.correlation.beta_v152 import BetaCalculator
        if analysis.beta_results:
            port_beta = BetaCalculator().calculate_portfolio_beta(
                req.weights, analysis.beta_results
            )

        # Top industries / themes
        top_industries = [
            {"industry": b.key, "weight": round(b.gross_weight, 4)}
            for b in sorted(analysis.industry_exposure, key=lambda x: -x.gross_weight)[:5]
        ]
        top_themes = [
            {"theme": b.key, "weight": round(b.gross_weight, 4)}
            for b in sorted(analysis.theme_exposure, key=lambda x: -x.gross_weight)[:5]
        ]

        # ETF overlaps summary
        etf_overlap_summary = [
            {
                "etf": e.etf_symbol,
                "overlapping": e.overlapping_constituents,
                "combined_exposure": round(e.combined_effective_exposure, 4),
            }
            for e in analysis.etf_overlaps if e.status == "VALID"
        ]

        # Hidden concentration
        hc = analysis.hidden_concentration
        hc_summary = None
        if hc is not None:
            hc_summary = {
                "level": hc.hidden_concentration_level.value,
                "effective_bets": round(hc.effective_independent_bets, 4),
                "largest_cluster_weight": round(hc.largest_cluster_weight, 4),
            }

        # Sizing impact
        si = analysis.sizing_impact
        sizing_summary = None
        if si is not None:
            sizing_summary = {
                "symbol": si.symbol,
                "hypothetical_weight": round(si.hypothetical_weight, 4),
                "volatility_delta": round(si.volatility_delta, 6),
                "research_only": True,
                "order_created": False,
            }

        # Warnings / blockers
        warnings: List[str] = []
        blockers: List[str] = []
        for rc in analysis.risk_contributions:
            if rc.status != "VALID":
                blockers.append(f"risk_contribution:{rc.symbol}:{rc.status}")
        for br in analysis.beta_results:
            if br.status != "VALID":
                blockers.append(f"beta:{br.symbol}:{br.status}")

        return {
            "analysis_id":         analysis.analysis_id,
            "portfolio_id":        req.portfolio_id,
            "as_of":               req.as_of,
            "symbols":             list(req.symbols),
            "weights":             dict(req.weights),
            "return_method":       req.return_method.value,
            "alignment_method":    req.alignment_method.value,
            "lookback":            req.lookback_days,
            "sample_count":        analysis.aligned_returns.observation_count,
            "correlation_method":  req.correlation_method.value,
            "threshold":           req.high_correlation_threshold,
            "high_correlation_pairs": high_corr,
            "clusters":            cluster_summary,
            "portfolio_volatility": round(pv.annualized_volatility, 6),
            "top_risk_contributors": top_contributors,
            "portfolio_beta":      round(port_beta, 6) if port_beta is not None else None,
            "top_industries":      top_industries,
            "top_themes":          top_themes,
            "etf_overlaps":        etf_overlap_summary,
            "hidden_concentration": hc_summary,
            "sizing_impact":       sizing_summary,
            "warnings":            warnings,
            "blockers":            blockers,
            "assumptions":         [
                "RESEARCH_ONLY",
                "DESCRIPTIVE_ANALYTICS_ONLY",
                "NOT_AN_OPTIMIZATION",
                "NOT_A_REBALANCE_INSTRUCTION",
                "NOT_AN_ORDER",
                "NO_BROKER_CALL",
                "NO_LEDGER_WRITE",
            ],
            "limitations":         LIMITATIONS,
            "safety_text":         SAFETY_TEXT,
            "lineage_valid":       lineage.get("lineage_valid", False),
            "research_only":       True,
        }
