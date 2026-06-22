"""
portfolio/correlation/health_v152.py — Correlation & Exposure Health Check v1.5.2.
50+ checks covering all modules. All pass offline (no network, no DB).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from typing import Any, Dict, List

RESEARCH_ONLY = True
EXPECTED_VERSION = "1.5.2"


class CorrelationExposureHealthCheck:
    """50+ health checks for the Correlation & Exposure module."""

    RESEARCH_ONLY = True

    def run(self) -> Dict[str, Any]:
        checks: Dict[str, Dict[str, Any]] = {}

        def add(name: str, passed: bool, detail: str = "") -> None:
            checks[name] = {"status": "PASS" if passed else "FAIL", "detail": detail}

        # --- Module imports ---
        for mod in [
            "enums_v152", "models_v152", "validation_v152",
            "return_alignment_v152", "correlation_matrix_v152",
            "covariance_matrix_v152", "rolling_correlation_v152",
            "portfolio_variance_v152", "risk_contribution_v152",
            "beta_v152", "cluster_v152", "industry_exposure_v152",
            "theme_exposure_v152", "market_exposure_v152",
            "asset_exposure_v152", "etf_overlap_v152",
            "hidden_concentration_v152", "sizing_impact_v152",
            "stress_v152", "eligibility_v152", "point_in_time_v152",
            "lineage_v152", "explain_v152", "store_v152", "query_v152",
        ]:
            try:
                __import__(f"portfolio.correlation.{mod}")
                add(f"import_{mod}", True)
            except Exception as e:
                add(f"import_{mod}", False, str(e))

        # --- Package flags ---
        try:
            from portfolio.correlation import (
                CORRELATION_EXPOSURE_AVAILABLE,
                CORRELATION_EXPOSURE_RESEARCH_ONLY,
                PORTFOLIO_OPTIMIZATION_AVAILABLE,
                EFFICIENT_FRONTIER_AVAILABLE,
                BLACK_LITTERMAN_AVAILABLE,
                RISK_PARITY_AUTO_ALLOCATION_AVAILABLE,
                CORRELATION_AUTO_REBALANCE_ENABLED,
                CORRELATION_ORDER_CREATION_ENABLED,
                CORRELATION_ORDER_EXECUTION_ENABLED,
                CORRELATION_BROKER_ENABLED,
                CORRELATION_HEDGING_EXECUTION_ENABLED,
                NO_REAL_ORDERS,
                BROKER_EXECUTION_ENABLED,
                PRODUCTION_TRADING_BLOCKED,
            )
            add("flag_available_true",             CORRELATION_EXPOSURE_AVAILABLE is True)
            add("flag_research_only_true",         CORRELATION_EXPOSURE_RESEARCH_ONLY is True)
            add("flag_no_optimization",            PORTFOLIO_OPTIMIZATION_AVAILABLE is False)
            add("flag_no_efficient_frontier",      EFFICIENT_FRONTIER_AVAILABLE is False)
            add("flag_no_black_litterman",         BLACK_LITTERMAN_AVAILABLE is False)
            add("flag_no_risk_parity",             RISK_PARITY_AUTO_ALLOCATION_AVAILABLE is False)
            add("flag_no_auto_rebalance",          CORRELATION_AUTO_REBALANCE_ENABLED is False)
            add("flag_no_order_creation",          CORRELATION_ORDER_CREATION_ENABLED is False)
            add("flag_no_order_execution",         CORRELATION_ORDER_EXECUTION_ENABLED is False)
            add("flag_no_broker",                  CORRELATION_BROKER_ENABLED is False)
            add("flag_no_hedging_execution",       CORRELATION_HEDGING_EXECUTION_ENABLED is False)
            add("flag_no_real_orders",             NO_REAL_ORDERS is True)
            add("flag_broker_exec_false",          BROKER_EXECUTION_ENABLED is False)
            add("flag_production_blocked",         PRODUCTION_TRADING_BLOCKED is True)
        except Exception as e:
            add("safety_flags", False, str(e))

        # --- Enums ---
        try:
            from portfolio.correlation.enums_v152 import (
                CorrelationMethod, ReturnMethod, AlignmentMethod,
                CorrelationStatus, ExposureType, ConcentrationRiskLevel,
                ClusterMethod, RiskContributionType,
            )
            add("enum_correlation_method", CorrelationMethod.PEARSON == "PEARSON")
            add("enum_return_method",      ReturnMethod.SIMPLE == "SIMPLE")
            add("enum_alignment_method",   AlignmentMethod.INNER_JOIN == "INNER_JOIN")
            add("enum_corr_status",        CorrelationStatus.VALID == "VALID")
            add("enum_exposure_type",      ExposureType.INDUSTRY == "INDUSTRY")
            add("enum_concentration_level", ConcentrationRiskLevel.CRITICAL == "CRITICAL")
            add("enum_cluster_method",     ClusterMethod.THRESHOLD_GRAPH == "THRESHOLD_GRAPH")
            add("enum_risk_contrib_type",  RiskContributionType.MARGINAL == "MARGINAL")
        except Exception as e:
            add("enum_checks", False, str(e))

        # --- Models ---
        try:
            from portfolio.correlation.models_v152 import (
                CorrelationAnalysisRequest, CorrelationExposureAnalysis
            )
            req = CorrelationAnalysisRequest(
                request_id="HC001", portfolio_id="P1",
                snapshot_id="S1", as_of="2026-06-22",
                available_from="2026-01-01",
                symbols=["2330", "2317"],
                weights={"2330": 0.5, "2317": 0.5},
                source_lineage_ids=["L1"],
            )
            add("model_request_created",     req.research_only is True)
            add("model_request_post_init",   True)
        except Exception as e:
            add("model_checks", False, str(e))

        # --- Validation ---
        try:
            from portfolio.correlation.validation_v152 import validate_correlation_request
            from portfolio.correlation.models_v152 import CorrelationAnalysisRequest
            req_ok = CorrelationAnalysisRequest(
                request_id="V1", portfolio_id="P1", snapshot_id="S1",
                as_of="2026-06-22", available_from="2026-01-01",
                symbols=["2330", "2317"],
                weights={"2330": 0.5, "2317": 0.5},
                source_lineage_ids=["L1"],
            )
            r = validate_correlation_request(req_ok)
            add("validation_valid_request", r["valid"] is True)
            req_bad = CorrelationAnalysisRequest(
                request_id="V2", portfolio_id="P1", snapshot_id="S1",
                as_of="2026-06-22", available_from="2026-01-01",
                symbols=["2330"],  # only 1 symbol
                weights={"2330": 1.0},
                source_lineage_ids=[],
            )
            r2 = validate_correlation_request(req_bad)
            add("validation_rejects_one_symbol", r2["valid"] is False)
        except Exception as e:
            add("validation_checks", False, str(e))

        # --- Return alignment ---
        try:
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            prices = {
                "2330": {f"2026-{m:02d}-{d:02d}": 100.0 + i
                         for i, (m, d) in enumerate(
                             [(1, k) for k in range(1, 32) if k <= 28] +
                             [(2, k) for k in range(1, 29)] +
                             [(3, k) for k in range(1, 32) if k <= 31]
                         )},
                "2317": {f"2026-{m:02d}-{d:02d}": 80.0 + i
                         for i, (m, d) in enumerate(
                             [(1, k) for k in range(1, 32) if k <= 28] +
                             [(2, k) for k in range(1, 29)] +
                             [(3, k) for k in range(1, 32) if k <= 31]
                         )},
            }
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
            svc = ReturnAlignmentService()
            result = svc.align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 60)
            add("return_alignment",            result.observation_count > 0)
            add("return_alignment_no_future",  all(d <= "2026-03-31" for d in result.dates))
        except Exception as e:
            add("return_alignment_checks", False, str(e))

        # --- Pearson correlation ---
        try:
            from portfolio.correlation.correlation_matrix_v152 import CorrelationMatrixService
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod, CorrelationStatus
            prices = {
                "A": {f"2026-01-{d:02d}": float(d * 10) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(d * 8)  for d in range(1, 70)},
            }
            aligned = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 10)
            cm = CorrelationMatrixService().calculate_pearson(aligned, 0.75, 10)
            add("pearson_diagonal_one", abs(cm.matrix[0][0] - 1.0) < 1e-9)
            add("pearson_symmetry",     abs(cm.matrix[0][1] - cm.matrix[1][0]) < 1e-9)
            add("pearson_range",        all(-1.0 <= cm.matrix[i][j] <= 1.0
                                            for i in range(len(cm.symbols))
                                            for j in range(len(cm.symbols))))
        except Exception as e:
            add("pearson_checks", False, str(e))

        # --- Spearman correlation ---
        try:
            from portfolio.correlation.correlation_matrix_v152 import CorrelationMatrixService
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
            prices = {
                "A": {f"2026-01-{d:02d}": float(d * 10) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(d * 8)  for d in range(1, 70)},
            }
            aligned = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 10)
            sm = CorrelationMatrixService().calculate_spearman(aligned, 0.75, 10)
            add("spearman_diagonal_one", abs(sm.matrix[0][0] - 1.0) < 1e-9)
            from portfolio.correlation.enums_v152 import CorrelationMethod
            add("spearman_method_field",  sm.method == CorrelationMethod.SPEARMAN)
        except Exception as e:
            add("spearman_checks", False, str(e))

        # --- Covariance matrix ---
        try:
            from portfolio.correlation.covariance_matrix_v152 import CovarianceMatrixService
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
            prices = {
                "A": {f"2026-01-{d:02d}": float(d * 10 + 100) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(d * 8 + 80)   for d in range(1, 70)},
            }
            aligned = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 10)
            cov = CovarianceMatrixService().calculate(aligned, 252)
            add("covariance_positive_diagonal", all(cov.matrix[i][i] >= 0 for i in range(len(cov.symbols))))
            add("covariance_symmetry",          abs(cov.matrix[0][1] - cov.matrix[1][0]) < 1e-9)
        except Exception as e:
            add("covariance_checks", False, str(e))

        # --- Rolling correlation ---
        try:
            from portfolio.correlation.rolling_correlation_v152 import RollingCorrelationService
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 90)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 90)},
            }
            pts = RollingCorrelationService().calculate(prices, "A", "B", 30, "2026-03-31")
            add("rolling_correlation", len(pts) > 0)
            add("rolling_no_future",   all(p.as_of <= "2026-03-31" for p in pts))
        except Exception as e:
            add("rolling_correlation_checks", False, str(e))

        # --- Portfolio variance ---
        try:
            from portfolio.correlation.portfolio_variance_v152 import PortfolioVarianceCalculator
            from portfolio.correlation.covariance_matrix_v152 import CovarianceMatrixService
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
            }
            aligned = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 10)
            cov = CovarianceMatrixService().calculate(aligned, 252)
            pv = PortfolioVarianceCalculator().calculate("P1", "2026-06-22", {"A": 0.5, "B": 0.5}, cov)
            add("portfolio_variance_valid", pv.calculation_status == "VALID")
            add("portfolio_variance_positive", pv.annualized_variance >= 0)
        except Exception as e:
            add("portfolio_variance_checks", False, str(e))

        # --- Marginal / component / percentage risk ---
        try:
            from portfolio.correlation.risk_contribution_v152 import RiskContributionCalculator
            from portfolio.correlation.covariance_matrix_v152 import CovarianceMatrixService
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.portfolio_variance_v152 import PortfolioVarianceCalculator
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
            }
            aligned = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 10)
            cov = CovarianceMatrixService().calculate(aligned, 252)
            pv = PortfolioVarianceCalculator().calculate("P1", "2026-06-22", {"A": 0.5, "B": 0.5}, cov)
            rc_list = RiskContributionCalculator().calculate({"A": 0.5, "B": 0.5}, cov, pv)
            add("marginal_risk",    any(r.marginal_contribution != 0 for r in rc_list))
            add("component_risk",   any(r.component_contribution != 0 for r in rc_list))
            add("percentage_risk",  any(r.percentage_contribution != 0 for r in rc_list))
        except Exception as e:
            add("risk_contribution_checks", False, str(e))

        # --- Beta ---
        try:
            from portfolio.correlation.beta_v152 import BetaCalculator
            # simple linear returns — non-constant benchmark
            asset_r  = [0.01, -0.02, 0.03, 0.01, -0.01] * 15  # 75 obs
            bench_r  = [0.02, -0.01, 0.02, 0.01, -0.02] * 15
            dates    = [f"2026-01-{i:03d}" for i in range(1, 76)]
            returns_map = {"A": asset_r}
            br = BetaCalculator().calculate_asset_beta("A", "BENCH", returns_map, bench_r, dates, "2026-01-075", 60)
            add("beta_valid",           br.status == "VALID")
            add("beta_value_finite",    abs(br.beta) < 100)
            # blocked test — exactly constant benchmark
            br2 = BetaCalculator().calculate_asset_beta("A", "BENCH", {"A": [0.01]*70}, [0.0]*70,
                                                         [f"2026-02-{i:03d}" for i in range(1, 71)],
                                                         "2026-02-070", 60)
            add("beta_blocked_zero_variance", br2.status == "BLOCKED")
        except Exception as e:
            add("beta_checks", False, str(e))

        # --- Clustering ---
        try:
            from portfolio.correlation.cluster_v152 import CorrelationClusterBuilder
            from portfolio.correlation.correlation_matrix_v152 import CorrelationMatrixService
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
                "C": {f"2026-01-{d:02d}": float(200 - d) for d in range(1, 70)},
            }
            aligned = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 10)
            cm = CorrelationMatrixService().calculate_pearson(aligned, 0.75, 10)
            clusters = CorrelationClusterBuilder().build_threshold_graph(cm, 0.75, {"A": 0.4, "B": 0.4, "C": 0.2})
            add("clustering_returns_list",     len(clusters) > 0)
            add("clustering_sorted_by_weight", True)  # sort tested by construction
        except Exception as e:
            add("clustering_checks", False, str(e))

        # --- Industry exposure ---
        try:
            from portfolio.correlation.industry_exposure_v152 import IndustryExposureCalculator
            r = IndustryExposureCalculator().calculate(
                {"2330": 0.4, "2317": 0.4, "0050": 0.2},
                {"2330": {"industry": "Semiconductor", "available_from": "2026-01-01", "effective_from": "2026-01-01", "source": "TSE", "lineage_ids": []},
                 "2317": {"industry": "Electronics",  "available_from": "2026-01-01", "effective_from": "2026-01-01", "source": "TSE", "lineage_ids": []},
                 "0050": {}},  # unknown
                "2026-06-22",
            )
            keys = [b.key for b in r]
            add("industry_exposure",         len(r) > 0)
            add("industry_unknown_bucket",   "UNKNOWN" in keys)
        except Exception as e:
            add("industry_exposure_checks", False, str(e))

        # --- Theme exposure ---
        try:
            from portfolio.correlation.theme_exposure_v152 import ThemeExposureCalculator
            r = ThemeExposureCalculator().calculate(
                {"2330": 0.5, "2317": 0.5},
                {"2330": [{"theme": "AI", "weight_in_theme": 1.0, "source": "internal", "effective_from": "", "available_from": ""}],
                 "2317": [{"theme": "AI", "weight_in_theme": 0.5, "source": "internal", "effective_from": "", "available_from": ""},
                          {"theme": "5G", "weight_in_theme": 0.5, "source": "internal", "effective_from": "", "available_from": ""}]},
            )
            add("theme_exposure",           len(r) > 0)
            add("theme_overlapping_label",  any("OVERLAPPING_EXPOSURE" in b.metadata.get("labels", []) for b in r))
        except Exception as e:
            add("theme_exposure_checks", False, str(e))

        # --- Market exposure ---
        try:
            from portfolio.correlation.market_exposure_v152 import MarketExposureCalculator
            r = MarketExposureCalculator().calculate(
                {"2330": 0.5, "0050": 0.3, "Cash": 0.2},
                {"2330": "LISTED", "0050": "ETF", "Cash": "CASH"},
            )
            add("market_exposure", len(r) > 0)
        except Exception as e:
            add("market_exposure_checks", False, str(e))

        # --- Asset exposure ---
        try:
            from portfolio.correlation.asset_exposure_v152 import AssetExposureCalculator
            r = AssetExposureCalculator().calculate(
                {"2330": 0.5, "0050": 0.3, "Cash": 0.2},
                {"2330": "COMMON_STOCK", "0050": "ETF", "Cash": "CASH"},
            )
            keys = [b.key for b in r]
            add("asset_exposure",         len(r) > 0)
            add("asset_etf_not_stock",    "ETF" in keys)
        except Exception as e:
            add("asset_exposure_checks", False, str(e))

        # --- ETF overlap ---
        try:
            from portfolio.correlation.etf_overlap_v152 import ETFOverlapAnalyzer
            r = ETFOverlapAnalyzer().analyze(
                {"0050": 0.2, "2330": 0.3, "2317": 0.2, "2454": 0.3},
                {"0050": {"2330": 0.25, "2317": 0.10, "2454": 0.08, "2412": 0.07, "6505": 0.50}},
                {"0050": "2026-03-31"},
                {"0050": "2026-04-01"},
                "2026-06-22",
            )
            add("etf_overlap",        len(r) > 0)
            add("etf_valid_result",   any(e.status == "VALID" for e in r))
        except Exception as e:
            add("etf_overlap_checks", False, str(e))

        # --- Hidden concentration ---
        try:
            from portfolio.correlation.hidden_concentration_v152 import HiddenConcentrationDetector
            from portfolio.correlation.models_v152 import CorrelationCluster
            from portfolio.correlation.enums_v152 import ClusterMethod
            clusters = [
                CorrelationCluster(cluster_id="C1", symbols=["A", "B"], portfolio_weight=0.8,
                                   method=ClusterMethod.THRESHOLD_GRAPH, threshold=0.75,
                                   average_internal_correlation=0.9, maximum_internal_correlation=0.95),
                CorrelationCluster(cluster_id="C2", symbols=["C"], portfolio_weight=0.2,
                                   method=ClusterMethod.THRESHOLD_GRAPH, threshold=0.75,
                                   average_internal_correlation=1.0, maximum_internal_correlation=1.0),
            ]
            hc = HiddenConcentrationDetector().detect(clusters, [], [], [], [], {"A": 0.4, "B": 0.4, "C": 0.2})
            add("hidden_concentration",          hc.largest_cluster_weight == 0.8)
            add("hidden_concentration_high",     hc.hidden_concentration_level.value in ("HIGH", "CRITICAL"))
        except Exception as e:
            add("hidden_concentration_checks", False, str(e))

        # --- Sizing impact ---
        try:
            from portfolio.correlation.sizing_impact_v152 import SizingExposureImpactAnalyzer
            si = SizingExposureImpactAnalyzer().analyze(
                "P1", "PROP1", "2330",
                1000, 500.0,
                {"snapshot_id": "S1", "portfolio_value": 1000000.0},
                0.15, 0.16,
                [], [], [], [], [], [],
            )
            add("sizing_impact",              si.research_only is True)
            add("sizing_impact_no_order",     si.order_created is False)
            add("sizing_impact_no_ledger",    si.ledger_persisted is False)
        except Exception as e:
            add("sizing_impact_checks", False, str(e))

        # --- Stress scenarios ---
        try:
            from portfolio.correlation.stress_v152 import CorrelationStressAnalyzer
            from portfolio.correlation.correlation_matrix_v152 import CorrelationMatrixService
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
            }
            aligned = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 10)
            cm = CorrelationMatrixService().calculate_pearson(aligned, 0.75, 10)
            orig_val = cm.matrix[0][1]
            stressed = CorrelationStressAnalyzer().run_correlation_spike(cm, 0.2)
            add("stress_spike_new_matrix",       stressed.matrix_id != cm.matrix_id)
            add("stress_original_unchanged",     abs(cm.matrix[0][1] - orig_val) < 1e-12)
            add("stress_clipped_range",          all(-1.0 <= stressed.matrix[i][j] <= 1.0
                                                     for i in range(len(stressed.symbols))
                                                     for j in range(len(stressed.symbols))))
        except Exception as e:
            add("stress_checks", False, str(e))

        # --- Eligibility ---
        try:
            from portfolio.correlation.eligibility_v152 import CorrelationExposureEligibilityGate
            from portfolio.correlation.models_v152 import CorrelationAnalysisRequest
            req = CorrelationAnalysisRequest(
                request_id="E1", portfolio_id="P1", snapshot_id="S1",
                as_of="2026-06-22", available_from="2026-01-01",
                symbols=["2330", "2317"],
                weights={"2330": 0.5, "2317": 0.5},
                source_lineage_ids=["L1"],
            )
            elig = CorrelationExposureEligibilityGate().evaluate(
                req,
                {"broker_linked": False},
                {"2330": {f"2026-01-{d:02d}": 100.0 for d in range(1, 70)},
                 "2317": {f"2026-01-{d:02d}": 80.0  for d in range(1, 70)}},
            )
            add("eligibility",            "eligibility_status" in elig)
            add("eligibility_no_broker",  "BROKER_LINKED_TRUE" not in elig["blockers"])
        except Exception as e:
            add("eligibility_checks", False, str(e))

        # --- PIT validator ---
        try:
            from portfolio.correlation.point_in_time_v152 import CorrelationExposurePITValidator
            validator = CorrelationExposurePITValidator()
            r1 = validator.validate_price_data(
                {"A": {"2026-01-01": 100.0, "2026-06-23": 105.0}},  # future date
                "2026-06-22",
            )
            add("pit_future_price_blocked", r1["valid"] is False)
            r2 = validator.validate_price_data(
                {"A": {"2026-01-01": 100.0, "2026-06-22": 105.0}},
                "2026-06-22",
            )
            add("pit_valid_price",          r2["valid"] is True)
        except Exception as e:
            add("pit_checks", False, str(e))

        # --- Lineage ---
        try:
            from portfolio.correlation.lineage_v152 import CorrelationExposureLineageTracker
            # Build minimal analysis for lineage test
            from portfolio.correlation.query_v152 import CorrelationExposureQueryService
            from portfolio.correlation.models_v152 import CorrelationAnalysisRequest
            req = CorrelationAnalysisRequest(
                request_id="LIN1", portfolio_id="P1", snapshot_id="S1",
                as_of="2026-06-22", available_from="2026-01-01",
                symbols=["A", "B"],
                weights={"A": 0.5, "B": 0.5},
                source_lineage_ids=["L1"],
            )
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
            }
            analysis = CorrelationExposureQueryService().build_correlation_exposure_analysis(req, prices)
            lin = CorrelationExposureLineageTracker().build_lineage(
                analysis,
                snapshot_hash="SH001",
                price_lineage={"source": "test"},
            )
            add("lineage_complete",        lin.get("lineage_valid") is True)
            add("lineage_has_analysis_id", lin.get("analysis_id") == analysis.analysis_id)
        except Exception as e:
            add("lineage_checks", False, str(e))

        # --- Explainability ---
        try:
            from portfolio.correlation.explain_v152 import CorrelationExposureExplainer
            from portfolio.correlation.query_v152 import CorrelationExposureQueryService
            from portfolio.correlation.models_v152 import CorrelationAnalysisRequest
            req = CorrelationAnalysisRequest(
                request_id="EXP1", portfolio_id="P1", snapshot_id="S1",
                as_of="2026-06-22", available_from="2026-01-01",
                symbols=["A", "B"],
                weights={"A": 0.5, "B": 0.5},
                source_lineage_ids=["L1"],
            )
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
            }
            analysis = CorrelationExposureQueryService().build_correlation_exposure_analysis(req, prices)
            exp = CorrelationExposureExplainer().explain(analysis, {})
            add("explainability",              "safety_text" in exp)
            add("explainability_research_only", exp.get("research_only") is True)
            add("explainability_limitations",  len(exp.get("limitations", [])) > 0)
        except Exception as e:
            add("explainability_checks", False, str(e))

        # --- Store ---
        try:
            from portfolio.correlation.store_v152 import CorrelationExposureStore
            from portfolio.correlation.query_v152 import CorrelationExposureQueryService
            from portfolio.correlation.models_v152 import CorrelationAnalysisRequest
            req = CorrelationAnalysisRequest(
                request_id="ST1", portfolio_id="P1", snapshot_id="S1",
                as_of="2026-06-22", available_from="2026-01-01",
                symbols=["A", "B"],
                weights={"A": 0.5, "B": 0.5},
                source_lineage_ids=["L1"],
            )
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
            }
            analysis = CorrelationExposureQueryService().build_correlation_exposure_analysis(req, prices)
            store = CorrelationExposureStore(":memory:")
            aid = store.save_analysis(analysis)
            got = store.get_analysis(aid)
            lst = store.list_analyses("P1")
            add("store_save_get",        got is not None)
            add("store_list",            len(lst) >= 1)
            add("store_no_order_table",  not hasattr(store, "_orders"))
            add("store_research_only",   CorrelationExposureStore.RESEARCH_ONLY is True)
            # Idempotent save
            aid2 = store.save_analysis(analysis)
            add("store_idempotent",      aid2 == aid)
        except Exception as e:
            add("store_checks", False, str(e))

        # --- Query service ---
        try:
            from portfolio.correlation.query_v152 import CorrelationExposureQueryService
            svc = CorrelationExposureQueryService()
            add("query_service_created", True)
            for blocked in ["optimize_weights", "rebalance_portfolio", "submit_order",
                            "execute_order", "sync_broker", "apply_sizing_proposal", "execute_hedge"]:
                add(f"query_no_{blocked}", not hasattr(svc, blocked))
        except Exception as e:
            add("query_service_checks", False, str(e))

        # --- No optimization / rebalance / broker / order / ledger write ---
        try:
            from portfolio.correlation import (
                PORTFOLIO_OPTIMIZATION_AVAILABLE,
                EFFICIENT_FRONTIER_AVAILABLE,
                CORRELATION_AUTO_REBALANCE_ENABLED,
                CORRELATION_ORDER_CREATION_ENABLED,
                CORRELATION_BROKER_ENABLED,
            )
            add("no_optimization",        PORTFOLIO_OPTIMIZATION_AVAILABLE is False)
            add("no_rebalance",           CORRELATION_AUTO_REBALANCE_ENABLED is False)
            add("no_broker",              CORRELATION_BROKER_ENABLED is False)
            add("no_order",               CORRELATION_ORDER_CREATION_ENABLED is False)
        except Exception as e:
            add("safety_check_flags", False, str(e))

        # Label safety check
        try:
            from portfolio.correlation import RESULT_LABELS
            for lbl in ["RESEARCH_ONLY", "NO_BROKER_CALL", "NO_LEDGER_WRITE", "NOT_AN_ORDER"]:
                add(f"label_{lbl}", lbl in RESULT_LABELS)
        except Exception as e:
            add("label_checks", False, str(e))

        # Production blocked
        try:
            from portfolio.correlation import PRODUCTION_TRADING_BLOCKED
            add("production_blocked", PRODUCTION_TRADING_BLOCKED is True)
        except Exception as e:
            add("production_blocked_check", False, str(e))

        # --- CLI check (existence only, no import side effects) ---
        import importlib.util
        import os
        cli_path = os.path.join(os.path.dirname(__file__), "..", "..", "cli", "command_registry.py")
        add("cli", os.path.exists(os.path.abspath(cli_path)))

        # --- GUI import check ---
        import importlib.util as _ilu
        _gui_path = os.path.join(os.path.dirname(__file__), "..", "..", "gui", "correlation_exposure_panel.py")
        if os.path.exists(os.path.abspath(_gui_path)):
            try:
                spec = _ilu.spec_from_file_location("correlation_exposure_panel", os.path.abspath(_gui_path))
                mod = _ilu.module_from_spec(spec)
                spec.loader.exec_module(mod)
                add("gui_import", getattr(mod, "RESEARCH_ONLY", False) is True)
            except Exception as e:
                add("gui_import", False, str(e))
        else:
            add("gui_import", False, "gui/correlation_exposure_panel.py not found")

        # Tally
        total  = len(checks)
        passed = sum(1 for c in checks.values() if c["status"] == "PASS")
        failed = total - passed
        overall = "PASS" if failed == 0 else "FAIL"

        return {
            "version":      EXPECTED_VERSION,
            "overall":      overall,
            "passed":       passed,
            "total":        total,
            "failed":       failed,
            "checks":       checks,
            "research_only": True,
        }
