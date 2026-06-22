"""
release/correlation_exposure_release_gate_v152.py — Correlation & Exposure Release Gate v1.5.2.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
30 gate checks.
"""
from __future__ import annotations

from typing import Any, Dict, List

RESEARCH_ONLY = True
GATE_VERSION  = "1.5.2"


class CorrelationExposureReleaseGate:
    """
    30-check release gate for Correlation & Exposure v1.5.2.
    """

    RESEARCH_ONLY = True

    def run(self) -> Dict[str, Any]:
        results: List[Dict] = []
        passed_count = 0
        failed_count = 0

        def check(name: str, fn) -> bool:
            nonlocal passed_count, failed_count
            try:
                ok, detail = fn()
            except Exception as e:
                ok, detail = False, str(e)
            results.append({"check": name, "passed": ok, "detail": detail})
            if ok:
                passed_count += 1
            else:
                failed_count += 1
            return ok

        # 1. PACKAGE_FLAGS_VALID
        def _flags():
            from portfolio.correlation import (
                CORRELATION_EXPOSURE_AVAILABLE, CORRELATION_EXPOSURE_RESEARCH_ONLY,
                PORTFOLIO_OPTIMIZATION_AVAILABLE, EFFICIENT_FRONTIER_AVAILABLE,
                BLACK_LITTERMAN_AVAILABLE, RISK_PARITY_AUTO_ALLOCATION_AVAILABLE,
                CORRELATION_AUTO_REBALANCE_ENABLED, CORRELATION_ORDER_CREATION_ENABLED,
                CORRELATION_ORDER_EXECUTION_ENABLED, CORRELATION_BROKER_ENABLED,
                CORRELATION_HEDGING_EXECUTION_ENABLED,
                NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
            )
            assert CORRELATION_EXPOSURE_AVAILABLE is True
            assert CORRELATION_EXPOSURE_RESEARCH_ONLY is True
            assert PORTFOLIO_OPTIMIZATION_AVAILABLE is False
            assert EFFICIENT_FRONTIER_AVAILABLE is False
            assert BLACK_LITTERMAN_AVAILABLE is False
            assert RISK_PARITY_AUTO_ALLOCATION_AVAILABLE is False
            assert CORRELATION_AUTO_REBALANCE_ENABLED is False
            assert CORRELATION_ORDER_CREATION_ENABLED is False
            assert CORRELATION_ORDER_EXECUTION_ENABLED is False
            assert CORRELATION_BROKER_ENABLED is False
            assert CORRELATION_HEDGING_EXECUTION_ENABLED is False
            assert NO_REAL_ORDERS is True
            assert BROKER_EXECUTION_ENABLED is False
            assert PRODUCTION_TRADING_BLOCKED is True
            return True, "all package flags valid"
        check("PACKAGE_FLAGS_VALID", _flags)

        # 2. ENUMS_VALID
        def _enums():
            from portfolio.correlation.enums_v152 import (
                CorrelationMethod, ReturnMethod, AlignmentMethod,
                CorrelationStatus, ExposureType, ConcentrationRiskLevel,
                ClusterMethod, RiskContributionType,
            )
            assert CorrelationMethod.PEARSON == "PEARSON"
            assert ReturnMethod.LOG == "LOG"
            assert AlignmentMethod.INNER_JOIN == "INNER_JOIN"
            assert CorrelationStatus.INSUFFICIENT_SAMPLE == "INSUFFICIENT_SAMPLE"
            assert ExposureType.INDUSTRY == "INDUSTRY"
            assert ConcentrationRiskLevel.CRITICAL == "CRITICAL"
            assert ClusterMethod.THRESHOLD_GRAPH == "THRESHOLD_GRAPH"
            assert RiskContributionType.MARGINAL == "MARGINAL"
            return True, "all enums valid"
        check("ENUMS_VALID", _enums)

        # 3. MODELS_VALID
        def _models():
            from portfolio.correlation.models_v152 import CorrelationAnalysisRequest
            req = CorrelationAnalysisRequest(
                request_id="G3", portfolio_id="P", snapshot_id="S",
                as_of="2026-06-22", available_from="2026-01-01",
                symbols=["2330", "2317"],
                weights={"2330": 0.5, "2317": 0.5},
                source_lineage_ids=["L1"],
            )
            assert req.research_only is True
            return True, "models valid"
        check("MODELS_VALID", _models)

        # 4. RESEARCH_ONLY_ENFORCED
        def _ro():
            from portfolio.correlation.models_v152 import CorrelationAnalysisRequest
            try:
                req = CorrelationAnalysisRequest(
                    request_id="G4", portfolio_id="P", snapshot_id="S",
                    as_of="2026-06-22", available_from="2026-01-01",
                    symbols=["A", "B"], weights={"A": 0.5, "B": 0.5},
                    research_only=False,
                )
                req.research_only  # should have raised
                return False, "AssertionError not raised"
            except AssertionError:
                return True, "research_only=False correctly rejected"
        check("RESEARCH_ONLY_ENFORCED", _ro)

        # 5. VALIDATION_VALID
        def _val():
            from portfolio.correlation.validation_v152 import validate_correlation_request
            from portfolio.correlation.models_v152 import CorrelationAnalysisRequest
            req = CorrelationAnalysisRequest(
                request_id="G5", portfolio_id="P", snapshot_id="S",
                as_of="2026-06-22", available_from="2026-01-01",
                symbols=["2330", "2317"],
                weights={"2330": 0.5, "2317": 0.5},
                source_lineage_ids=["L1"],
            )
            r = validate_correlation_request(req)
            assert r["valid"] is True
            return True, "validation valid"
        check("VALIDATION_VALID", _val)

        # 6. RETURN_ALIGNMENT_VALID
        def _ra():
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
            }
            r = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 60)
            assert r.observation_count > 0
            return True, f"aligned obs={r.observation_count}"
        check("RETURN_ALIGNMENT_VALID", _ra)

        # 7. NO_FUTURE_DATA
        def _pit_price():
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod, CorrelationStatus
            prices = {
                "A": {"2026-06-20": 100.0, "2026-06-25": 105.0},  # 25th is future vs 22nd
                "B": {"2026-06-20": 80.0,  "2026-06-25": 82.0},
            }
            r = ReturnAlignmentService().align(prices, "2026-06-22", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 1)
            # Future dates should be excluded
            assert all(d <= "2026-06-22" for d in r.dates)
            return True, "future data excluded"
        check("NO_FUTURE_DATA", _pit_price)

        # 8. PEARSON_MATRIX_VALID
        def _pearson():
            from portfolio.correlation.correlation_matrix_v152 import CorrelationMatrixService
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
            }
            aligned = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 10)
            cm = CorrelationMatrixService().calculate_pearson(aligned, 0.75, 10)
            assert abs(cm.matrix[0][0] - 1.0) < 1e-9
            assert abs(cm.matrix[0][1] - cm.matrix[1][0]) < 1e-9
            return True, "Pearson matrix valid"
        check("PEARSON_MATRIX_VALID", _pearson)

        # 9. SPEARMAN_MATRIX_VALID
        def _spearman():
            from portfolio.correlation.correlation_matrix_v152 import CorrelationMatrixService
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod, CorrelationMethod
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
            }
            aligned = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 10)
            sm = CorrelationMatrixService().calculate_spearman(aligned, 0.75, 10)
            assert sm.method == CorrelationMethod.SPEARMAN
            assert abs(sm.matrix[0][0] - 1.0) < 1e-9
            return True, "Spearman matrix valid"
        check("SPEARMAN_MATRIX_VALID", _spearman)

        # 10. COVARIANCE_MATRIX_VALID
        def _cov():
            from portfolio.correlation.covariance_matrix_v152 import CovarianceMatrixService
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
            }
            aligned = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 10)
            cov = CovarianceMatrixService().calculate(aligned, 252)
            assert all(cov.matrix[i][i] >= 0 for i in range(len(cov.symbols)))
            return True, "covariance matrix valid"
        check("COVARIANCE_MATRIX_VALID", _cov)

        # 11. ROLLING_CORRELATION_VALID
        def _rolling():
            from portfolio.correlation.rolling_correlation_v152 import RollingCorrelationService
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 90)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 90)},
            }
            pts = RollingCorrelationService().calculate(prices, "A", "B", 30, "2026-03-31")
            assert len(pts) > 0
            return True, f"rolling points={len(pts)}"
        check("ROLLING_CORRELATION_VALID", _rolling)

        # 12. PORTFOLIO_VARIANCE_VALID
        def _pv():
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
            assert pv.calculation_status == "VALID"
            assert pv.annualized_variance >= 0
            return True, f"annualized_vol={pv.annualized_volatility:.6f}"
        check("PORTFOLIO_VARIANCE_VALID", _pv)

        # 13. MARGINAL_RISK_VALID
        def _mrc():
            from portfolio.correlation.risk_contribution_v152 import RiskContributionCalculator
            from portfolio.correlation.covariance_matrix_v152 import CovarianceMatrixService
            from portfolio.correlation.portfolio_variance_v152 import PortfolioVarianceCalculator
            from portfolio.correlation.return_alignment_v152 import ReturnAlignmentService
            from portfolio.correlation.enums_v152 import AlignmentMethod, ReturnMethod
            prices = {
                "A": {f"2026-01-{d:02d}": float(100 + d) for d in range(1, 70)},
                "B": {f"2026-01-{d:02d}": float(80 + d)  for d in range(1, 70)},
            }
            aligned = ReturnAlignmentService().align(prices, "2026-03-31", AlignmentMethod.INNER_JOIN, ReturnMethod.SIMPLE, 10)
            cov = CovarianceMatrixService().calculate(aligned, 252)
            pv  = PortfolioVarianceCalculator().calculate("P1", "2026-06-22", {"A": 0.5, "B": 0.5}, cov)
            rc  = RiskContributionCalculator().calculate({"A": 0.5, "B": 0.5}, cov, pv)
            assert any(r.marginal_contribution != 0 for r in rc)
            return True, "marginal risk contributions valid"
        check("MARGINAL_RISK_VALID", _mrc)

        # 14. BETA_VALID
        def _beta():
            from portfolio.correlation.beta_v152 import BetaCalculator
            asset_r = [0.01, -0.02, 0.03, 0.01, -0.01] * 15
            bench_r = [0.02, -0.01, 0.02, 0.01, -0.02] * 15
            dates   = [f"2026-01-{i:03d}" for i in range(1, 76)]
            br = BetaCalculator().calculate_asset_beta(
                "A", "BENCH", {"A": asset_r}, bench_r, dates, "2026-01-075", 60
            )
            assert br.status == "VALID"
            return True, f"beta={br.beta:.4f}"
        check("BETA_VALID", _beta)

        # 15. BETA_BLOCKED_ZERO_VARIANCE
        def _beta_blocked():
            from portfolio.correlation.beta_v152 import BetaCalculator
            asset_r = [0.01] * 70
            bench_r = [0.0] * 70  # exactly constant → zero variance
            dates   = [f"2026-01-{i:03d}" for i in range(1, 71)]
            br = BetaCalculator().calculate_asset_beta(
                "A", "BENCH", {"A": asset_r}, bench_r, dates, "2026-01-070", 60
            )
            assert br.status == "BLOCKED"
            return True, "zero benchmark variance correctly blocked"
        check("BETA_BLOCKED_ZERO_VARIANCE", _beta_blocked)

        # 16. CLUSTERING_VALID
        def _cluster():
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
            clusters = CorrelationClusterBuilder().build_threshold_graph(cm, 0.75)
            assert len(clusters) > 0
            return True, f"clusters={len(clusters)}"
        check("CLUSTERING_VALID", _cluster)

        # 17. INDUSTRY_EXPOSURE_VALID
        def _ind():
            from portfolio.correlation.industry_exposure_v152 import IndustryExposureCalculator
            r = IndustryExposureCalculator().calculate(
                {"2330": 0.4, "2317": 0.4, "2454": 0.2},
                {"2330": {"industry": "Semiconductor", "available_from": "2026-01-01", "effective_from": "2026-01-01", "source": "TSE", "lineage_ids": []},
                 "2317": {"industry": "Electronics",   "available_from": "2026-01-01", "effective_from": "2026-01-01", "source": "TSE", "lineage_ids": []},
                 "2454": {"industry": "Semiconductor",  "available_from": "2026-01-01", "effective_from": "2026-01-01", "source": "TSE", "lineage_ids": []}},
                "2026-06-22",
            )
            assert any(b.key == "Semiconductor" for b in r)
            return True, "industry exposure valid"
        check("INDUSTRY_EXPOSURE_VALID", _ind)

        # 18. INDUSTRY_UNKNOWN_BUCKET
        def _ind_unk():
            from portfolio.correlation.industry_exposure_v152 import IndustryExposureCalculator
            r = IndustryExposureCalculator().calculate(
                {"2330": 0.5, "UNK": 0.5},
                {"2330": {"industry": "Semiconductor", "available_from": "2026-01-01", "effective_from": "2026-01-01", "source": "TSE", "lineage_ids": []}},
                "2026-06-22",
            )
            assert any(b.key == "UNKNOWN" for b in r)
            return True, "UNKNOWN industry bucket created"
        check("INDUSTRY_UNKNOWN_BUCKET", _ind_unk)

        # 19. THEME_EXPOSURE_VALID
        def _theme():
            from portfolio.correlation.theme_exposure_v152 import ThemeExposureCalculator
            r = ThemeExposureCalculator().calculate(
                {"2330": 0.5, "2317": 0.5},
                {"2330": [{"theme": "AI", "weight_in_theme": 1.0, "source": "internal", "effective_from": "", "available_from": ""}],
                 "2317": [{"theme": "AI", "weight_in_theme": 0.5, "source": "internal", "effective_from": "", "available_from": ""},
                          {"theme": "5G", "weight_in_theme": 0.5, "source": "internal", "effective_from": "", "available_from": ""}]},
            )
            assert len(r) >= 2
            assert any("OVERLAPPING_EXPOSURE" in b.metadata.get("labels", []) for b in r)
            return True, "theme exposure valid"
        check("THEME_EXPOSURE_VALID", _theme)

        # 20. MARKET_EXPOSURE_VALID
        def _mkt():
            from portfolio.correlation.market_exposure_v152 import MarketExposureCalculator
            r = MarketExposureCalculator().calculate(
                {"2330": 0.5, "0050": 0.3, "Cash": 0.2},
                {"2330": "LISTED", "0050": "ETF", "Cash": "CASH"},
            )
            assert len(r) == 3
            return True, "market exposure valid"
        check("MARKET_EXPOSURE_VALID", _mkt)

        # 21. ASSET_EXPOSURE_VALID
        def _asset():
            from portfolio.correlation.asset_exposure_v152 import AssetExposureCalculator
            r = AssetExposureCalculator().calculate(
                {"2330": 0.5, "0050": 0.3, "Cash": 0.2},
                {"2330": "COMMON_STOCK", "0050": "ETF", "Cash": "CASH"},
            )
            keys = [b.key for b in r]
            assert "ETF" in keys
            assert "COMMON_STOCK" in keys
            return True, "asset exposure valid"
        check("ASSET_EXPOSURE_VALID", _asset)

        # 22. ETF_OVERLAP_VALID
        def _etf():
            from portfolio.correlation.etf_overlap_v152 import ETFOverlapAnalyzer
            r = ETFOverlapAnalyzer().analyze(
                {"0050": 0.2, "2330": 0.3, "2317": 0.2, "2454": 0.3},
                {"0050": {"2330": 0.25, "2317": 0.10, "2454": 0.08, "X": 0.57}},
                {"0050": "2026-03-31"},
                {"0050": "2026-04-01"},
                "2026-06-22",
            )
            assert any(e.status == "VALID" for e in r)
            return True, "ETF overlap valid"
        check("ETF_OVERLAP_VALID", _etf)

        # 23. HIDDEN_CONCENTRATION_VALID
        def _hc():
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
            assert hc.largest_cluster_weight == 0.8
            return True, f"concentration_level={hc.hidden_concentration_level.value}"
        check("HIDDEN_CONCENTRATION_VALID", _hc)

        # 24. SIZING_IMPACT_RESEARCH_ONLY
        def _si():
            from portfolio.correlation.sizing_impact_v152 import SizingExposureImpactAnalyzer
            si = SizingExposureImpactAnalyzer().analyze(
                "P1", "PROP1", "2330",
                1000, 500.0,
                {"snapshot_id": "S1", "portfolio_value": 1000000.0},
                0.15, 0.16,
                [], [], [], [], [], [],
            )
            assert si.research_only is True
            assert si.order_created is False
            assert si.ledger_persisted is False
            return True, "sizing impact research-only enforced"
        check("SIZING_IMPACT_RESEARCH_ONLY", _si)

        # 25. STRESS_SCENARIOS_VALID
        def _stress():
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
            orig = cm.matrix[0][1]
            stressed = CorrelationStressAnalyzer().run_correlation_spike(cm, 0.2)
            assert stressed.matrix_id != cm.matrix_id
            assert abs(cm.matrix[0][1] - orig) < 1e-12  # original unchanged
            return True, "stress scenarios valid, original unchanged"
        check("STRESS_SCENARIOS_VALID", _stress)

        # 26. ELIGIBILITY_GATE_VALID
        def _elig():
            from portfolio.correlation.eligibility_v152 import CorrelationExposureEligibilityGate
            from portfolio.correlation.models_v152 import CorrelationAnalysisRequest
            req = CorrelationAnalysisRequest(
                request_id="G26", portfolio_id="P", snapshot_id="S",
                as_of="2026-06-22", available_from="2026-01-01",
                symbols=["2330", "2317"],
                weights={"2330": 0.5, "2317": 0.5},
                source_lineage_ids=["L1"],
            )
            elig = CorrelationExposureEligibilityGate().evaluate(
                req, {"broker_linked": False},
                {"2330": {f"2026-01-{d:02d}": 100.0 for d in range(1, 70)},
                 "2317": {f"2026-01-{d:02d}": 80.0  for d in range(1, 70)}},
            )
            assert "eligibility_status" in elig
            assert "BROKER_LINKED_TRUE" not in elig["blockers"]
            return True, f"eligibility_status={elig['eligibility_status']}"
        check("ELIGIBILITY_GATE_VALID", _elig)

        # 27. PIT_VALIDATION_VALID
        def _pit():
            from portfolio.correlation.point_in_time_v152 import CorrelationExposurePITValidator
            v = CorrelationExposurePITValidator()
            r = v.validate_price_data({"A": {"2026-06-23": 100.0}}, "2026-06-22")
            assert r["valid"] is False
            r2 = v.validate_price_data({"A": {"2026-06-22": 100.0}}, "2026-06-22")
            assert r2["valid"] is True
            return True, "PIT validation correct"
        check("PIT_VALIDATION_VALID", _pit)

        # 28. LINEAGE_VALID
        def _lin():
            from portfolio.correlation.lineage_v152 import CorrelationExposureLineageTracker
            from portfolio.correlation.query_v152 import CorrelationExposureQueryService
            from portfolio.correlation.models_v152 import CorrelationAnalysisRequest
            req = CorrelationAnalysisRequest(
                request_id="G28", portfolio_id="P", snapshot_id="S",
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
                analysis, snapshot_hash="SH001", price_lineage={"src": "test"}
            )
            assert lin["lineage_valid"] is True
            return True, "lineage valid"
        check("LINEAGE_VALID", _lin)

        # 29. QUERY_SERVICE_VALID
        def _qs():
            from portfolio.correlation.query_v152 import CorrelationExposureQueryService
            svc = CorrelationExposureQueryService()
            for blocked in ["optimize_weights", "rebalance_portfolio", "submit_order",
                            "execute_order", "sync_broker", "apply_sizing_proposal", "execute_hedge"]:
                assert not hasattr(svc, blocked), f"blocked method {blocked} found"
            return True, "query service valid, blocked methods absent"
        check("QUERY_SERVICE_VALID", _qs)

        # 30. STORE_NO_LEDGER
        def _store():
            from portfolio.correlation.store_v152 import CorrelationExposureStore
            store = CorrelationExposureStore(":memory:")
            assert CorrelationExposureStore.RESEARCH_ONLY is True
            assert not hasattr(store, "_orders"), "order table must not exist"
            assert not hasattr(store, "sync_broker"), "broker sync must not exist"
            return True, "store: no order table, no broker, RESEARCH_ONLY=True"
        check("STORE_NO_LEDGER", _store)

        gate_passed = failed_count == 0
        return {
            "gate_passed":   gate_passed,
            "status":        "PASS" if gate_passed else "FAIL",
            "version":       GATE_VERSION,
            "passed":        passed_count,
            "failed":        failed_count,
            "total":         len(results),
            "checks":        results,
            "research_only": True,
        }
