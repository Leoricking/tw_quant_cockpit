"""
portfolio/correlation/query_v152.py — Correlation Exposure Query Service v1.5.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] NOT PROVIDED: optimize_weights, rebalance_portfolio, submit_order, execute_order,
    sync_broker, apply_sizing_proposal, execute_hedge.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import uuid
from typing import Any, Dict, List, Optional

from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
from portfolio.correlation.models_v152 import (
    AlignedReturnSeries,
    BetaResult,
    CorrelationCluster,
    CorrelationExposureAnalysis,
    CorrelationMatrixResult,
    CovarianceMatrixResult,
    ETFOverlapResult,
    ExposureBucket,
    HiddenConcentrationResult,
    PortfolioVarianceResult,
    RiskContributionResult,
    RollingCorrelationPoint,
    SizingExposureImpact,
)

RESEARCH_ONLY = True
SERVICE_VERSION = "1.5.2"

# Blocked methods — must NOT exist on this class
_BLOCKED_METHODS = [
    "optimize_weights",
    "rebalance_portfolio",
    "submit_order",
    "execute_order",
    "sync_broker",
    "apply_sizing_proposal",
    "execute_hedge",
]


class CorrelationExposureQueryService:
    """
    Unified query service wrapping all correlation & exposure calculation modules.
    Research-only. Blocked methods are intentionally absent.
    """

    RESEARCH_ONLY = True

    def __init__(self, store=None):
        if store is None:
            from portfolio.correlation.store_v152 import CorrelationExposureStore
            store = CorrelationExposureStore(db_path=":memory:")
        self._store = store

    # ------------------------------------------------------------------
    # Eligibility
    # ------------------------------------------------------------------

    def evaluate_correlation_eligibility(
        self,
        request,
        portfolio_snapshot: Dict[str, Any],
        price_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        from portfolio.correlation.eligibility_v152 import CorrelationExposureEligibilityGate
        return CorrelationExposureEligibilityGate().evaluate(request, portfolio_snapshot, price_data)

    # ------------------------------------------------------------------
    # Return alignment
    # ------------------------------------------------------------------

    def align_return_series(
        self,
        prices_by_symbol: Dict[str, Dict[str, float]],
        as_of: str,
        method: AlignmentMethod = AlignmentMethod.INNER_JOIN,
        return_method: ReturnMethod = ReturnMethod.SIMPLE,
        min_obs: int = 60,
    ) -> AlignedReturnSeries:
        from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
        return ReturnAlignmentService().align(
            prices_by_symbol, as_of, method, return_method, min_obs
        )

    # ------------------------------------------------------------------
    # Correlation matrix
    # ------------------------------------------------------------------

    def calculate_correlation_matrix(
        self,
        aligned: AlignedReturnSeries,
        method=None,
        high_corr_threshold: float = 0.75,
        min_obs: int = 60,
    ) -> CorrelationMatrixResult:
        from portfolio.correlation.correlation_matrix_v152 import CorrelationMatrixService
        from portfolio.correlation.enums_v152 import CorrelationMethod
        svc = CorrelationMatrixService()
        if method == CorrelationMethod.SPEARMAN:
            return svc.calculate_spearman(aligned, high_corr_threshold, min_obs)
        return svc.calculate_pearson(aligned, high_corr_threshold, min_obs)

    # ------------------------------------------------------------------
    # Covariance matrix
    # ------------------------------------------------------------------

    def calculate_covariance_matrix(
        self,
        aligned: AlignedReturnSeries,
        annualization_factor: int = 252,
    ) -> CovarianceMatrixResult:
        from portfolio.correlation.covariance_matrix_v152 import CovarianceMatrixService
        return CovarianceMatrixService().calculate(aligned, annualization_factor)

    # ------------------------------------------------------------------
    # Rolling correlation
    # ------------------------------------------------------------------

    def calculate_rolling_correlation(
        self,
        prices_by_symbol: Dict[str, Dict[str, float]],
        symbol_a: str,
        symbol_b: str,
        window: int = 60,
        as_of: Optional[str] = None,
    ) -> List[RollingCorrelationPoint]:
        from portfolio.correlation.rolling_correlation_v152 import RollingCorrelationService
        return RollingCorrelationService().calculate(
            prices_by_symbol, symbol_a, symbol_b, window, as_of
        )

    # ------------------------------------------------------------------
    # Portfolio variance
    # ------------------------------------------------------------------

    def calculate_portfolio_variance(
        self,
        portfolio_id: str,
        as_of: str,
        weights: Dict[str, float],
        covariance_result: CovarianceMatrixResult,
    ) -> PortfolioVarianceResult:
        from portfolio.correlation.portfolio_variance_v152 import PortfolioVarianceCalculator
        return PortfolioVarianceCalculator().calculate(
            portfolio_id, as_of, weights, covariance_result
        )

    # ------------------------------------------------------------------
    # Risk contributions
    # ------------------------------------------------------------------

    def calculate_risk_contributions(
        self,
        weights: Dict[str, float],
        covariance_result: CovarianceMatrixResult,
        variance_result: PortfolioVarianceResult,
    ) -> List[RiskContributionResult]:
        from portfolio.correlation.risk_contribution_v152 import RiskContributionCalculator
        return RiskContributionCalculator().calculate(weights, covariance_result, variance_result)

    # ------------------------------------------------------------------
    # Beta
    # ------------------------------------------------------------------

    def calculate_asset_beta(
        self,
        symbol: str,
        benchmark_symbol: str,
        returns_by_symbol: Dict[str, List[float]],
        benchmark_returns: List[float],
        dates: List[str],
        as_of: str,
        min_obs: int = 60,
    ) -> BetaResult:
        from portfolio.correlation.beta_v152 import BetaCalculator
        return BetaCalculator().calculate_asset_beta(
            symbol, benchmark_symbol, returns_by_symbol, benchmark_returns, dates, as_of, min_obs
        )

    def calculate_portfolio_beta(
        self,
        weights: Dict[str, float],
        beta_results: List[BetaResult],
    ) -> float:
        from portfolio.correlation.beta_v152 import BetaCalculator
        return BetaCalculator().calculate_portfolio_beta(weights, beta_results)

    # ------------------------------------------------------------------
    # Clustering
    # ------------------------------------------------------------------

    def build_correlation_clusters(
        self,
        correlation_matrix: CorrelationMatrixResult,
        cluster_threshold: float = 0.75,
        weights: Optional[Dict[str, float]] = None,
    ) -> List[CorrelationCluster]:
        from portfolio.correlation.cluster_v152 import CorrelationClusterBuilder
        return CorrelationClusterBuilder().build_threshold_graph(
            correlation_matrix, cluster_threshold, weights
        )

    # ------------------------------------------------------------------
    # Exposure calculators
    # ------------------------------------------------------------------

    def calculate_industry_exposure(
        self,
        weights: Dict[str, float],
        classifications: Dict[str, Dict[str, Any]],
        as_of: Optional[str] = None,
    ) -> List[ExposureBucket]:
        from portfolio.correlation.industry_exposure_v152 import IndustryExposureCalculator
        return IndustryExposureCalculator().calculate(weights, classifications, as_of)

    def calculate_theme_exposure(
        self,
        weights: Dict[str, float],
        theme_data: Dict[str, List[Dict[str, Any]]],
    ) -> List[ExposureBucket]:
        from portfolio.correlation.theme_exposure_v152 import ThemeExposureCalculator
        return ThemeExposureCalculator().calculate(weights, theme_data)

    def calculate_market_exposure(
        self,
        weights: Dict[str, float],
        market_data: Dict[str, str],
    ) -> List[ExposureBucket]:
        from portfolio.correlation.market_exposure_v152 import MarketExposureCalculator
        return MarketExposureCalculator().calculate(weights, market_data)

    def calculate_asset_exposure(
        self,
        weights: Dict[str, float],
        asset_types: Dict[str, str],
    ) -> List[ExposureBucket]:
        from portfolio.correlation.asset_exposure_v152 import AssetExposureCalculator
        return AssetExposureCalculator().calculate(weights, asset_types)

    # ------------------------------------------------------------------
    # ETF overlap
    # ------------------------------------------------------------------

    def calculate_etf_overlap(
        self,
        portfolio_weights: Dict[str, float],
        etf_holdings: Dict[str, Dict[str, float]],
        holdings_as_of: Dict[str, str],
        holdings_available_from: Dict[str, str],
        as_of: str,
    ) -> List[ETFOverlapResult]:
        from portfolio.correlation.etf_overlap_v152 import ETFOverlapAnalyzer
        return ETFOverlapAnalyzer().analyze(
            portfolio_weights, etf_holdings, holdings_as_of, holdings_available_from, as_of
        )

    # ------------------------------------------------------------------
    # Hidden concentration
    # ------------------------------------------------------------------

    def detect_hidden_concentration(
        self,
        clusters: List[CorrelationCluster],
        risk_contributions: List[RiskContributionResult],
        industry_exposure: List[ExposureBucket],
        theme_exposure: List[ExposureBucket],
        etf_overlaps: List[ETFOverlapResult],
        weights: Dict[str, float],
    ) -> HiddenConcentrationResult:
        from portfolio.correlation.hidden_concentration_v152 import HiddenConcentrationDetector
        return HiddenConcentrationDetector().detect(
            clusters, risk_contributions, industry_exposure, theme_exposure, etf_overlaps, weights
        )

    # ------------------------------------------------------------------
    # Sizing impact
    # ------------------------------------------------------------------

    def evaluate_sizing_exposure_impact(
        self,
        portfolio_id: str,
        proposal_id: str,
        symbol: str,
        hypothetical_quantity: float,
        entry_price: float,
        portfolio_snapshot: Dict[str, Any],
        before_portfolio_volatility: float,
        after_portfolio_volatility: float,
        before_clusters: List[CorrelationCluster],
        after_clusters: List[CorrelationCluster],
        before_industry_exposure: List[ExposureBucket],
        after_industry_exposure: List[ExposureBucket],
        before_theme_exposure: List[ExposureBucket],
        after_theme_exposure: List[ExposureBucket],
    ) -> SizingExposureImpact:
        from portfolio.correlation.sizing_impact_v152 import SizingExposureImpactAnalyzer
        return SizingExposureImpactAnalyzer().analyze(
            portfolio_id, proposal_id, symbol,
            hypothetical_quantity, entry_price,
            portfolio_snapshot,
            before_portfolio_volatility, after_portfolio_volatility,
            before_clusters, after_clusters,
            before_industry_exposure, after_industry_exposure,
            before_theme_exposure, after_theme_exposure,
        )

    # ------------------------------------------------------------------
    # Stress
    # ------------------------------------------------------------------

    def run_correlation_stress(
        self,
        matrix: CorrelationMatrixResult,
        scenario_type: str = "CORRELATION_SPIKE",
        **kwargs,
    ) -> CorrelationMatrixResult:
        from portfolio.correlation.stress_v152 import CorrelationStressAnalyzer
        svc = CorrelationStressAnalyzer()
        if scenario_type == "CORRELATION_SPIKE":
            return svc.run_correlation_spike(matrix, kwargs.get("spike_amount", 0.2))
        elif scenario_type == "DIVERSIFICATION_BREAKDOWN":
            return svc.run_diversification_breakdown(matrix, kwargs.get("cluster_threshold", 0.75))
        elif scenario_type == "INDUSTRY_CO_MOVEMENT":
            return svc.run_industry_co_movement(
                matrix,
                kwargs.get("industry_exposure", []),
                kwargs.get("boost", 0.15),
            )
        elif scenario_type == "ETF_OVERLAP_SHOCK":
            return svc.run_etf_overlap_shock(
                matrix,
                kwargs.get("etf_overlaps", []),
                kwargs.get("shock", 0.3),
            )
        else:
            return svc.run_correlation_spike(matrix)

    # ------------------------------------------------------------------
    # Full analysis builder
    # ------------------------------------------------------------------

    def build_correlation_exposure_analysis(
        self,
        request,
        prices_by_symbol: Dict[str, Dict[str, float]],
        classifications: Optional[Dict[str, Dict[str, Any]]] = None,
        theme_data: Optional[Dict[str, List[Dict[str, Any]]]] = None,
        market_data: Optional[Dict[str, str]] = None,
        asset_types: Optional[Dict[str, str]] = None,
        etf_holdings: Optional[Dict[str, Dict[str, float]]] = None,
        holdings_as_of: Optional[Dict[str, str]] = None,
        holdings_available_from: Optional[Dict[str, str]] = None,
        benchmark_prices: Optional[Dict[str, float]] = None,
    ) -> CorrelationExposureAnalysis:
        """
        Build a complete CorrelationExposureAnalysis from raw inputs.
        """
        weights = request.weights
        symbols = request.symbols
        as_of   = request.as_of

        # 1. Align returns
        aligned = self.align_return_series(
            prices_by_symbol, as_of,
            method=request.alignment_method,
            return_method=request.return_method,
            min_obs=request.minimum_observations,
        )

        # 2. Correlation matrix
        corr_matrix = self.calculate_correlation_matrix(
            aligned,
            method=request.correlation_method,
            high_corr_threshold=request.high_correlation_threshold,
            min_obs=request.minimum_observations,
        )

        # 3. Covariance matrix
        cov_matrix = self.calculate_covariance_matrix(aligned)

        # 4. Portfolio variance
        port_var = self.calculate_portfolio_variance(
            request.portfolio_id, as_of, weights, cov_matrix
        )

        # 5. Risk contributions
        risk_contribs = self.calculate_risk_contributions(weights, cov_matrix, port_var)

        # 6. Beta (if benchmark provided)
        beta_results: List[BetaResult] = []
        if request.benchmark_symbol and benchmark_prices:
            bench_dates = sorted(d for d in benchmark_prices if d <= as_of)
            bench_returns: List[float] = []
            for i in range(1, len(bench_dates)):
                p0 = benchmark_prices[bench_dates[i - 1]]
                p1 = benchmark_prices[bench_dates[i]]
                if p0 != 0:
                    bench_returns.append((p1 / p0) - 1.0)
            returns_map = aligned.returns_by_symbol
            for sym in symbols:
                br = self.calculate_asset_beta(
                    sym, request.benchmark_symbol,
                    returns_map, bench_returns,
                    aligned.dates, as_of,
                    request.minimum_observations,
                )
                beta_results.append(br)

        # 7. Clusters
        clusters = self.build_correlation_clusters(
            corr_matrix, request.cluster_threshold, weights
        )

        # 8. Exposure buckets
        ind_exp  = self.calculate_industry_exposure(weights, classifications or {}, as_of)
        thm_exp  = self.calculate_theme_exposure(weights, theme_data or {})
        mkt_exp  = self.calculate_market_exposure(weights, market_data or {})
        asset_exp = self.calculate_asset_exposure(weights, asset_types or {})

        # 9. ETF overlap
        etf_ovlp = self.calculate_etf_overlap(
            weights,
            etf_holdings or {},
            holdings_as_of or {},
            holdings_available_from or {},
            as_of,
        )

        # 10. Hidden concentration
        hc = self.detect_hidden_concentration(
            clusters, risk_contribs, ind_exp, thm_exp, etf_ovlp, weights
        )

        # 11. Content hash
        analysis_id = f"CEA_{uuid.uuid4().hex[:12].upper()}"
        generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        content_hash = hashlib.sha256(
            json.dumps({
                "analysis_id": analysis_id,
                "portfolio_id": request.portfolio_id,
                "as_of": as_of,
                "corr_hash": corr_matrix.content_hash,
            }, sort_keys=True).encode()
        ).hexdigest()[:16]

        return CorrelationExposureAnalysis(
            analysis_id=analysis_id,
            request=request,
            aligned_returns=aligned,
            correlation_matrix=corr_matrix,
            covariance_matrix=cov_matrix,
            portfolio_variance=port_var,
            risk_contributions=risk_contribs,
            beta_results=beta_results,
            clusters=clusters,
            industry_exposure=ind_exp,
            theme_exposure=thm_exp,
            market_exposure=mkt_exp,
            asset_exposure=asset_exp,
            etf_overlaps=etf_ovlp,
            hidden_concentration=hc,
            generated_at=generated_at,
            content_hash=content_hash,
        )

    # ------------------------------------------------------------------
    # Explainability
    # ------------------------------------------------------------------

    def explain_correlation_exposure(
        self,
        analysis: CorrelationExposureAnalysis,
        lineage: Dict[str, Any],
    ) -> Dict[str, Any]:
        from portfolio.correlation.explain_v152 import CorrelationExposureExplainer
        return CorrelationExposureExplainer().explain(analysis, lineage)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_analysis(self, analysis: CorrelationExposureAnalysis) -> str:
        return self._store.save_analysis(analysis)

    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        return self._store.get_analysis(analysis_id)

    def list_analyses(
        self,
        portfolio_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        return self._store.list_analyses(portfolio_id=portfolio_id)

    def get_analysis_lineage(self, analysis_id: str) -> Dict[str, Any]:
        return self._store.get_lineage(analysis_id)
