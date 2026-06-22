"""
reports/correlation_exposure_report.py — Correlation & Exposure Report v1.5.2.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Never executable. No broker. No order. No ledger write.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

RESEARCH_ONLY  = True
REPORT_VERSION = "1.5.2"


class CorrelationExposureReport:
    """
    Generates comprehensive correlation & exposure research reports.
    Sections: context, correlation, covariance, risk, clusters, exposure,
              etf_overlap, hidden_concentration, sizing_impact, stress,
              lineage, safety.
    """

    RESEARCH_ONLY  = True
    REPORT_VERSION = REPORT_VERSION

    def generate(
        self,
        portfolio_id: str,
        as_of: str,
        analysis=None,
        lineage: Optional[Dict[str, Any]] = None,
        request=None,
    ) -> Dict[str, Any]:
        """
        Generate a full correlation & exposure report.
        Returns dict with all sections.
        Never executable. No broker. No order. No ledger write.
        """
        generated_at = datetime.datetime.utcnow().isoformat()
        lineage = lineage or {}

        return {
            "report_version":   REPORT_VERSION,
            "generated_at":     generated_at,
            "portfolio_id":     portfolio_id,
            "as_of":            as_of,
            "research_only":    True,
            "executable":       False,
            "order_created":    False,
            "broker_called":    False,
            "ledger_write":     False,
            "sections":         [
                self._section_context(portfolio_id, as_of, analysis),
                self._section_correlation(analysis),
                self._section_covariance(analysis),
                self._section_risk(analysis),
                self._section_clusters(analysis),
                self._section_exposure(analysis),
                self._section_etf_overlap(analysis),
                self._section_hidden_concentration(analysis),
                self._section_sizing_impact(analysis),
                self._section_stress(analysis),
                self._section_lineage(lineage),
                self._section_safety(),
            ],
        }

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_context(self, portfolio_id: str, as_of: str, analysis) -> Dict:
        return {
            "section":         "context",
            "portfolio_id":    portfolio_id,
            "as_of":           as_of,
            "analysis_id":     getattr(analysis, "analysis_id", "") if analysis else "",
            "report_type":     "CORRELATION_EXPOSURE_RESEARCH",
            "research_only":   True,
        }

    def _section_correlation(self, analysis) -> Dict:
        if analysis is None:
            return {"section": "correlation", "status": "NO_ANALYSIS_PROVIDED"}
        cm = getattr(analysis, "correlation_matrix", None)
        if cm is None:
            return {"section": "correlation", "status": "NO_MATRIX"}
        return {
            "section":              "correlation",
            "matrix_id":            cm.matrix_id,
            "method":               cm.method.value,
            "symbols":              cm.symbols,
            "observation_count":    next(iter(cm.observation_counts.values()), 0) if cm.observation_counts else 0,
            "start_date":           cm.start_date,
            "end_date":             cm.end_date,
            "high_correlation_pairs": cm.high_correlation_pairs,
            "status":               cm.status.value,
            "content_hash":         cm.content_hash,
        }

    def _section_covariance(self, analysis) -> Dict:
        if analysis is None:
            return {"section": "covariance", "status": "NO_ANALYSIS_PROVIDED"}
        cov = getattr(analysis, "covariance_matrix", None)
        if cov is None:
            return {"section": "covariance", "status": "NO_MATRIX"}
        return {
            "section":              "covariance",
            "symbols":              cov.symbols,
            "observation_count":    cov.observation_count,
            "annualization_factor": cov.annualization_factor,
            "status":               cov.status.value,
            "content_hash":         cov.content_hash,
        }

    def _section_risk(self, analysis) -> Dict:
        if analysis is None:
            return {"section": "risk", "status": "NO_ANALYSIS_PROVIDED"}
        pv = getattr(analysis, "portfolio_variance", None)
        rc_list = getattr(analysis, "risk_contributions", [])
        return {
            "section":               "risk",
            "portfolio_id":          getattr(pv, "portfolio_id", "") if pv else "",
            "annualized_volatility": getattr(pv, "annualized_volatility", 0.0) if pv else 0.0,
            "annualized_variance":   getattr(pv, "annualized_variance", 0.0) if pv else 0.0,
            "calculation_status":    getattr(pv, "calculation_status", "") if pv else "",
            "risk_contributions":    [
                {
                    "symbol":                r.symbol,
                    "weight":                round(r.weight, 4),
                    "marginal_contribution": round(r.marginal_contribution, 6),
                    "component_contribution": round(r.component_contribution, 6),
                    "percentage_contribution": round(r.percentage_contribution, 6),
                }
                for r in rc_list
            ],
        }

    def _section_clusters(self, analysis) -> Dict:
        if analysis is None:
            return {"section": "clusters", "status": "NO_ANALYSIS_PROVIDED"}
        clusters = getattr(analysis, "clusters", [])
        return {
            "section":  "clusters",
            "count":    len(clusters),
            "clusters": [
                {
                    "cluster_id":     c.cluster_id,
                    "symbols":        c.symbols,
                    "portfolio_weight": round(c.portfolio_weight, 4),
                    "avg_correlation": round(c.average_internal_correlation, 4),
                    "max_correlation": round(c.maximum_internal_correlation, 4),
                }
                for c in clusters
            ],
        }

    def _section_exposure(self, analysis) -> Dict:
        if analysis is None:
            return {"section": "exposure", "status": "NO_ANALYSIS_PROVIDED"}

        def _summarise(buckets: List) -> List[Dict]:
            return [
                {
                    "key":          b.key,
                    "gross_weight": round(b.gross_weight, 4),
                    "status":       b.status,
                }
                for b in buckets
            ]

        return {
            "section":          "exposure",
            "industry_buckets": _summarise(getattr(analysis, "industry_exposure", [])),
            "theme_buckets":    _summarise(getattr(analysis, "theme_exposure", [])),
            "market_buckets":   _summarise(getattr(analysis, "market_exposure", [])),
            "asset_buckets":    _summarise(getattr(analysis, "asset_exposure", [])),
        }

    def _section_etf_overlap(self, analysis) -> Dict:
        if analysis is None:
            return {"section": "etf_overlap", "status": "NO_ANALYSIS_PROVIDED"}
        overlaps = getattr(analysis, "etf_overlaps", [])
        return {
            "section": "etf_overlap",
            "count":   len(overlaps),
            "overlaps": [
                {
                    "etf_symbol":               e.etf_symbol,
                    "overlapping_constituents": e.overlapping_constituents,
                    "direct_weight":            round(e.direct_weight, 4),
                    "indirect_weight":          round(e.indirect_weight, 4),
                    "combined_exposure":        round(e.combined_effective_exposure, 4),
                    "status":                   e.status,
                }
                for e in overlaps
            ],
        }

    def _section_hidden_concentration(self, analysis) -> Dict:
        if analysis is None:
            return {"section": "hidden_concentration", "status": "NO_ANALYSIS_PROVIDED"}
        hc = getattr(analysis, "hidden_concentration", None)
        if hc is None:
            return {"section": "hidden_concentration", "status": "NOT_COMPUTED"}
        return {
            "section":                  "hidden_concentration",
            "level":                    hc.hidden_concentration_level.value,
            "apparent_position_count":  hc.apparent_position_count,
            "effective_independent_bets": round(hc.effective_independent_bets, 4),
            "largest_cluster_weight":   round(hc.largest_cluster_weight, 4),
            "warnings":                 hc.warnings,
        }

    def _section_sizing_impact(self, analysis) -> Dict:
        if analysis is None:
            return {"section": "sizing_impact", "status": "NO_ANALYSIS_PROVIDED"}
        si = getattr(analysis, "sizing_impact", None)
        if si is None:
            return {"section": "sizing_impact", "status": "NOT_COMPUTED"}
        return {
            "section":                    "sizing_impact",
            "proposal_id":                si.proposal_id,
            "symbol":                     si.symbol,
            "hypothetical_weight":        round(si.hypothetical_weight, 4),
            "before_portfolio_volatility": round(si.before_portfolio_volatility, 6),
            "after_portfolio_volatility":  round(si.after_portfolio_volatility, 6),
            "volatility_delta":           round(si.volatility_delta, 6),
            "research_only":              True,
            "order_created":              False,
            "ledger_persisted":           False,
        }

    def _section_stress(self, analysis) -> Dict:
        if analysis is None:
            return {"section": "stress", "status": "NO_ANALYSIS_PROVIDED"}
        stress = getattr(analysis, "stress_results", [])
        return {
            "section":   "stress",
            "count":     len(stress),
            "scenarios": [
                {
                    "matrix_id":  s.matrix_id,
                    "scenario":   s.metadata.get("scenario", ""),
                    "status":     s.status.value,
                }
                for s in stress
            ],
        }

    def _section_lineage(self, lineage: Dict[str, Any]) -> Dict:
        return {
            "section":         "lineage",
            "analysis_id":     lineage.get("analysis_id", ""),
            "snapshot_hash":   lineage.get("snapshot_hash", ""),
            "lineage_valid":   lineage.get("lineage_valid", False),
            "lineage_errors":  lineage.get("lineage_errors", []),
            "calculation_version": lineage.get("calculation_version", ""),
        }

    def _section_safety(self) -> Dict:
        from portfolio.correlation import (
            CORRELATION_EXPOSURE_RESEARCH_ONLY,
            PORTFOLIO_OPTIMIZATION_AVAILABLE,
            CORRELATION_AUTO_REBALANCE_ENABLED,
            CORRELATION_ORDER_CREATION_ENABLED,
            CORRELATION_BROKER_ENABLED,
            NO_REAL_ORDERS,
            BROKER_EXECUTION_ENABLED,
            PRODUCTION_TRADING_BLOCKED,
            RESULT_LABELS,
        )
        return {
            "section":                       "safety",
            "research_only":                 CORRELATION_EXPOSURE_RESEARCH_ONLY,
            "portfolio_optimization_enabled": PORTFOLIO_OPTIMIZATION_AVAILABLE,
            "auto_rebalance_enabled":        CORRELATION_AUTO_REBALANCE_ENABLED,
            "order_creation_enabled":        CORRELATION_ORDER_CREATION_ENABLED,
            "broker_enabled":                CORRELATION_BROKER_ENABLED,
            "no_real_orders":                NO_REAL_ORDERS,
            "broker_execution_enabled":      BROKER_EXECUTION_ENABLED,
            "production_trading_blocked":    PRODUCTION_TRADING_BLOCKED,
            "labels":                        RESULT_LABELS,
        }
