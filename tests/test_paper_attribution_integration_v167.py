"""
tests/test_paper_attribution_integration_v167.py
Integration tests for paper attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest


class TestPackageImport:
    def test_package_importable(self):
        import paper_trading.performance_attribution
        assert True

    def test_paper_attribution_available(self):
        import paper_trading.performance_attribution as pkg
        assert pkg.PAPER_ATTRIBUTION_AVAILABLE is True

    def test_real_disabled(self):
        import paper_trading.performance_attribution as pkg
        assert pkg.REAL_PERFORMANCE_ATTRIBUTION_ENABLED is False


class TestEngineImports:
    def test_return_decomp_engine(self):
        from paper_trading.performance_attribution.return_decomposition_v167 import ReturnDecompositionEngine
        e = ReturnDecompositionEngine()
        assert e is not None

    def test_pnl_attribution_engine(self):
        from paper_trading.performance_attribution.pnl_attribution_v167 import PnLAttributionEngine
        e = PnLAttributionEngine()
        assert e is not None

    def test_reconciler(self):
        from paper_trading.performance_attribution.attribution_reconciler_v167 import AttributionReconciler
        e = AttributionReconciler()
        assert e is not None

    def test_scorecard_engine(self):
        from paper_trading.performance_attribution.attribution_scorecard_v167 import AttributionScorecardEngine
        e = AttributionScorecardEngine()
        assert e is not None

    def test_validator(self):
        from paper_trading.performance_attribution.attribution_validator_v167 import AttributionValidator
        e = AttributionValidator()
        assert e is not None

    def test_store(self):
        from paper_trading.performance_attribution.attribution_store_v167 import AttributionStore
        s = AttributionStore()
        assert s is not None

    def test_query_api(self):
        from paper_trading.performance_attribution.attribution_store_v167 import AttributionStore
        from paper_trading.performance_attribution.attribution_query_v167 import AttributionQueryAPI
        s = AttributionStore()
        q = AttributionQueryAPI(s)
        assert q is not None

    def test_report_engine(self):
        from paper_trading.performance_attribution.attribution_report_v167 import AttributionReportEngine
        e = AttributionReportEngine()
        assert e is not None

    def test_health_check(self):
        from paper_trading.performance_attribution.health_v167 import PaperAttributionHealthCheck
        h = PaperAttributionHealthCheck()
        assert h is not None


class TestStoreRoundTrip:
    """End-to-end store save/load/query cycle."""

    def setup_method(self):
        from paper_trading.performance_attribution.attribution_store_v167 import AttributionStore
        from paper_trading.performance_attribution.attribution_query_v167 import AttributionQueryAPI
        self.store = AttributionStore()
        self.q = AttributionQueryAPI(self.store)

    def _save_run(self, run_id, **overrides):
        data = {
            "paper_only": True,
            "research_only": True,
            "portfolio_id": "INT_P1",
            "status": "COMPLETE",
            "period_start": "2024-01-01",
            "period_end": "2024-01-31",
            "portfolio_attribution": {
                "active_return": 0.04,
                "gross_return": 0.05,
                "net_return": 0.045,
                "reconciled": True,
                "confidence": "HIGH",
            },
            "strategy_attribution": {
                "s1": {"return": 0.03},
                "s2": {"return": 0.01},
            },
            "symbol_attribution": {
                "AAPL": {"return": 0.08, "weight": 0.3},
                "MSFT": {"return": 0.04, "weight": 0.25},
                "TSLA": {"return": -0.02, "weight": 0.15},
            },
        }
        data.update(overrides)
        return self.store.save_run(run_id, data)

    def test_save_then_load(self):
        self._save_run("int_run_1")
        loaded = self.store.load_run("int_run_1")
        assert loaded is not None
        assert loaded["portfolio_id"] == "INT_P1"

    def test_query_portfolio_after_save(self):
        self._save_run("int_run_2")
        r = self.q.get_portfolio_attribution("int_run_2")
        assert r["active_return"] == 0.04

    def test_query_strategy_after_save(self):
        self._save_run("int_run_3")
        r = self.q.get_strategy_attribution("int_run_3")
        assert "s1" in r
        assert "s2" in r

    def test_query_top_contributors(self):
        self._save_run("int_run_4")
        r = self.q.get_top_contributors("int_run_4", level="symbol", n=2)
        assert len(r["top_contributors"]) == 2

    def test_summarize_attribution(self):
        self._save_run("int_run_5")
        r = self.q.summarize_attribution("int_run_5")
        assert r["portfolio_id"] == "INT_P1"
        assert r["paper_only"] is True

    def test_not_found_handled(self):
        r = self.q.get_portfolio_attribution("no_such_run_xyz")
        assert "error" in r

    def test_compare_two_periods(self):
        self._save_run("int_period_0", portfolio_attribution={"active_return": 0.03, "reconciled": True, "confidence": "HIGH"})
        self._save_run("int_period_1", portfolio_attribution={"active_return": 0.05, "reconciled": True, "confidence": "HIGH"})
        r = self.q.compare_periods(["int_period_0", "int_period_1"])
        assert r["comparison"]["int_period_0"] == 0.03
        assert r["comparison"]["int_period_1"] == 0.05

    def test_export_json(self):
        self._save_run("int_export_run")
        j = self.store.export_json("int_export_run")
        assert "portfolio_id" in j
        assert "INT_P1" in j

    def test_store_summary_after_saves(self):
        for i in range(3):
            self._save_run(f"int_summ_{i}")
        s = self.store.summarize()
        assert s["total_runs"] >= 3


class TestReconcilerIntegration:
    def test_portfolio_reconciliation_pass(self):
        from paper_trading.performance_attribution.attribution_reconciler_v167 import AttributionReconciler
        from paper_trading.performance_attribution.enums_v167 import ReconciliationStatus
        r = AttributionReconciler()
        # Portfolio = strategies sum
        rec = r.reconcile("portfolio", 100.0, 100.0)
        assert rec.status == ReconciliationStatus.RECONCILED
        assert rec.paper_only is True

    def test_active_return_reconciliation(self):
        from paper_trading.performance_attribution.attribution_reconciler_v167 import AttributionReconciler
        from paper_trading.performance_attribution.enums_v167 import ReconciliationStatus
        r = AttributionReconciler()
        rec = r.check_active_return(
            "portfolio",
            active_return=0.10,
            selection=0.05, allocation=0.03, timing=0.01,
            exposure=0.0, execution=-0.01, cost=-0.01,
            risk=0.0, regime=0.01, benchmark=0.0,
            factor=0.005, residual=0.015,
        )
        assert rec.status in (
            ReconciliationStatus.RECONCILED,
            ReconciliationStatus.RECONCILED_WITH_ROUNDING,
        )


class TestScorecardIntegration:
    def test_full_score_no_blocking(self):
        from paper_trading.performance_attribution.attribution_scorecard_v167 import AttributionScorecardEngine
        from paper_trading.performance_attribution.enums_v167 import ReconciliationStatus, DataQualityStatus
        engine = AttributionScorecardEngine()
        sc = engine.compute(
            entity_id="int_test",
            reconciliation_status=ReconciliationStatus.RECONCILED,
            residual_pct=0.0,
            data_quality=DataQualityStatus.COMPLETE,
            has_execution_data=True, execution_simulated=True,
            cost_quality="KNOWN", has_benchmark=True, benchmark_stale=False,
            has_risk_data=True, risk_data_complete=True,
            has_source_lineage=True, deterministic=True,
            has_real_markers=False, has_credentials=False, fixture_only=False,
        )
        assert sc.total_score > 80.0
        assert sc.blocking_issues == []
        assert sc.paper_only is True

    def test_blocked_never_usable(self):
        from paper_trading.performance_attribution.attribution_scorecard_v167 import AttributionScorecardEngine
        from paper_trading.performance_attribution.enums_v167 import ReconciliationStatus, DataQualityStatus
        engine = AttributionScorecardEngine()
        sc = engine.compute(
            entity_id="blocked_test",
            reconciliation_status=ReconciliationStatus.RECONCILED,
            residual_pct=0.0,
            data_quality=DataQualityStatus.COMPLETE,
            has_execution_data=True, execution_simulated=True,
            cost_quality="KNOWN", has_benchmark=True, benchmark_stale=False,
            has_risk_data=True, risk_data_complete=True,
            has_source_lineage=True, deterministic=True,
            has_real_markers=True,  # BLOCKED
            has_credentials=False, fixture_only=False,
        )
        assert sc.usable_for_research is False
        assert sc.usable_for_paper_review is False


class TestReportIntegration:
    def test_full_report_31_sections(self):
        from paper_trading.performance_attribution.attribution_report_v167 import AttributionReportEngine
        run_data = {
            "run_id": "full_rpt",
            "portfolio_id": "FULL_P",
            "period_start": "2024-01-01",
            "period_end": "2024-01-31",
            "status": "COMPLETE",
            "paper_only": True,
            "research_only": True,
            "portfolio_attribution": {
                "active_return": 0.03,
                "gross_return": 0.04,
                "net_return": 0.035,
                "reconciled": True,
                "confidence": "HIGH",
            },
        }
        engine = AttributionReportEngine(run_data)
        report = engine.build_all_sections()
        assert len(report["sections"]) == 31
        assert report["paper_only"] is True

    def test_gui_model_31_tabs(self):
        from paper_trading.performance_attribution.attribution_report_v167 import AttributionReportEngine
        engine = AttributionReportEngine({"run_id": "gui_rpt", "paper_only": True})
        gui = engine.to_gui_model()
        assert gui["tab_count"] == 31
        assert gui["not_for_real_trading"] is True


class TestDeterminism:
    def test_reconciler_deterministic(self):
        from paper_trading.performance_attribution.attribution_reconciler_v167 import AttributionReconciler
        r = AttributionReconciler()
        rec1 = r.reconcile("test", 100.0, 95.0)
        rec2 = r.reconcile("test", 100.0, 95.0)
        assert rec1.residual == rec2.residual
        assert rec1.status == rec2.status

    def test_scorecard_deterministic(self):
        from paper_trading.performance_attribution.attribution_scorecard_v167 import AttributionScorecardEngine
        from paper_trading.performance_attribution.enums_v167 import ReconciliationStatus, DataQualityStatus
        engine = AttributionScorecardEngine()
        kwargs = dict(
            entity_id="det",
            reconciliation_status=ReconciliationStatus.RECONCILED,
            residual_pct=0.0,
            data_quality=DataQualityStatus.COMPLETE,
            has_execution_data=True, execution_simulated=True,
            cost_quality="KNOWN", has_benchmark=True, benchmark_stale=False,
            has_risk_data=True, risk_data_complete=True,
            has_source_lineage=True, deterministic=True,
            has_real_markers=False, has_credentials=False, fixture_only=False,
        )
        sc1 = engine.compute(**kwargs)
        sc2 = engine.compute(**kwargs)
        assert sc1.total_score == sc2.total_score
