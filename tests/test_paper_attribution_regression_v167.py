"""
tests/test_paper_attribution_regression_v167.py
Regression tests for paper attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest


class TestVersionCompatibility:
    def test_v167_is_known_release(self):
        from paper_trading.performance_attribution.version_v167 import is_known_release
        assert is_known_release("Paper Performance Attribution") is True

    def test_v166_is_known_release(self):
        from paper_trading.performance_attribution.version_v167 import is_known_release
        assert is_known_release("Multi-session Coordination") is True

    def test_v165_is_known_release(self):
        from paper_trading.performance_attribution.version_v167 import is_known_release
        assert is_known_release("Failure Injection and Recovery Validation") is True

    def test_current_version_is_1_6_7(self):
        from paper_trading.performance_attribution.version_v167 import VERSION
        assert VERSION == "1.6.7"


class TestSafetyRegressions:
    def test_module_safety_flags_always_correct(self):
        import paper_trading.performance_attribution as pkg
        assert pkg.PAPER_ATTRIBUTION_AVAILABLE is True
        assert pkg.REAL_PERFORMANCE_ATTRIBUTION_ENABLED is False
        assert pkg.NO_REAL_ORDERS is True

    def test_safety_module_all_safe(self):
        from paper_trading.performance_attribution.safety_v167 import audit_safety
        assert audit_safety()["all_safe"] is True

    def test_forbidden_fields_never_empty(self):
        from paper_trading.performance_attribution.enums_v167 import FORBIDDEN_FIELDS
        assert len(FORBIDDEN_FIELDS) >= 10

    def test_fixture_schema_still_requires_10_markers(self):
        from paper_trading.performance_attribution.fixture_schema_v167 import REQUIRED_FIXTURE_MARKERS
        assert len(REQUIRED_FIXTURE_MARKERS) == 10


class TestReconcilerRegressions:
    def test_exact_match_always_reconciled(self):
        from paper_trading.performance_attribution.attribution_reconciler_v167 import AttributionReconciler
        from paper_trading.performance_attribution.enums_v167 import ReconciliationStatus
        r = AttributionReconciler()
        for val in [0.0, 100.0, -50.0, 0.001, 1000000.0]:
            rec = r.reconcile("test", val, val)
            assert rec.status == ReconciliationStatus.RECONCILED, f"Failed at {val}"

    def test_large_residual_always_fails(self):
        from paper_trading.performance_attribution.attribution_reconciler_v167 import AttributionReconciler
        from paper_trading.performance_attribution.enums_v167 import ReconciliationStatus
        r = AttributionReconciler()
        for residual in [10.0, 50.0, 1000.0]:
            rec = r.reconcile("test", 100.0, 100.0 - residual)
            assert rec.status == ReconciliationStatus.FAILED, f"Should fail for residual={residual}"

    def test_residual_never_auto_zeroed(self):
        from paper_trading.performance_attribution.attribution_reconciler_v167 import AttributionReconciler
        r = AttributionReconciler()
        for diff in [1.0, 5.0, 50.0]:
            rec = r.reconcile("test", 100.0, 100.0 - diff)
            assert rec.residual != 0.0


class TestScorecardRegressions:
    def test_real_markers_always_score_zero(self):
        from paper_trading.performance_attribution.attribution_scorecard_v167 import AttributionScorecardEngine
        from paper_trading.performance_attribution.enums_v167 import ReconciliationStatus, DataQualityStatus
        engine = AttributionScorecardEngine()
        for _ in range(3):
            sc = engine.compute(
                entity_id="reg", reconciliation_status=ReconciliationStatus.RECONCILED,
                residual_pct=0.0, data_quality=DataQualityStatus.COMPLETE,
                has_execution_data=True, execution_simulated=True,
                cost_quality="KNOWN", has_benchmark=True, benchmark_stale=False,
                has_risk_data=True, risk_data_complete=True,
                has_source_lineage=True, deterministic=True,
                has_real_markers=True, has_credentials=False, fixture_only=False,
            )
            assert sc.total_score == 0.0

    def test_score_weights_sum_always_100(self):
        from paper_trading.performance_attribution.attribution_scorecard_v167 import SCORE_WEIGHTS
        assert sum(SCORE_WEIGHTS.values()) == 100

    def test_fixture_always_below_100(self):
        from paper_trading.performance_attribution.attribution_scorecard_v167 import AttributionScorecardEngine
        from paper_trading.performance_attribution.enums_v167 import ReconciliationStatus, DataQualityStatus
        engine = AttributionScorecardEngine()
        sc = engine.compute(
            entity_id="fix", reconciliation_status=ReconciliationStatus.RECONCILED,
            residual_pct=0.0, data_quality=DataQualityStatus.COMPLETE,
            has_execution_data=True, execution_simulated=True,
            cost_quality="KNOWN", has_benchmark=True, benchmark_stale=False,
            has_risk_data=True, risk_data_complete=True,
            has_source_lineage=True, deterministic=True,
            has_real_markers=False, has_credentials=False, fixture_only=True,
        )
        assert sc.total_score < 100.0


class TestValidatorRegressions:
    def test_missing_paper_only_always_fails(self):
        from paper_trading.performance_attribution.attribution_validator_v167 import AttributionValidator
        v = AttributionValidator()
        r = v.validate_input({
            "research_only": True, "no_real_orders": True, "not_for_production": True,
        })
        assert r["valid"] is False

    def test_broker_session_always_blocked(self):
        from paper_trading.performance_attribution.attribution_validator_v167 import AttributionValidator
        v = AttributionValidator()
        r = v.validate_input({
            "paper_only": True, "research_only": True,
            "no_real_orders": True, "not_for_production": True,
            "broker_session": "live",
        })
        assert r["blocked"] is True

    def test_reversed_period_always_fails(self):
        from paper_trading.performance_attribution.attribution_validator_v167 import AttributionValidator
        v = AttributionValidator()
        r = v.validate_input({
            "paper_only": True, "research_only": True,
            "no_real_orders": True, "not_for_production": True,
            "attribution_period_start": "2024-12-31",
            "attribution_period_end": "2024-01-01",
        })
        assert r["valid"] is False


class TestStoreRegressions:
    def test_empty_store_always_zero_runs(self):
        from paper_trading.performance_attribution.attribution_store_v167 import AttributionStore
        store = AttributionStore()
        assert store.summarize()["total_runs"] == 0
        assert store.list_runs() == []

    def test_forbidden_field_always_blocked(self):
        from paper_trading.performance_attribution.attribution_store_v167 import AttributionStore
        store = AttributionStore()
        for field in ("broker_session", "real_account_token", "api_secret"):
            r = store.save_run("bad", {
                "paper_only": True, "research_only": True,
                field: "bad_value",
            })
            assert r["saved"] is False, f"Should be blocked for {field}"


class TestReport31Sections:
    def test_report_always_has_31_sections(self):
        from paper_trading.performance_attribution.attribution_report_v167 import (
            AttributionReportEngine, REPORT_SECTIONS,
        )
        assert len(REPORT_SECTIONS) == 31
        engine = AttributionReportEngine({"paper_only": True})
        report = engine.build_all_sections()
        assert len(report["sections"]) == 31

    def test_gui_model_always_31_tabs(self):
        from paper_trading.performance_attribution.attribution_report_v167 import AttributionReportEngine
        engine = AttributionReportEngine({})
        gui = engine.to_gui_model()
        assert gui["tab_count"] == 31


class TestScenarioRegistryRegressions:
    def test_always_80_plus_scenarios(self):
        from paper_trading.performance_attribution.scenario_registry_v167 import _SCENARIOS
        assert len(_SCENARIOS) >= 80

    def test_all_scenario_ids_unique(self):
        from paper_trading.performance_attribution.scenario_registry_v167 import _SCENARIOS
        ids = [s["id"] for s in _SCENARIOS]
        assert len(ids) == len(set(ids))

    def test_all_scenarios_paper_only(self):
        from paper_trading.performance_attribution.scenario_registry_v167 import _SCENARIOS
        for s in _SCENARIOS:
            assert s.get("paper_only") is True


class TestFixtureRegressions:
    def test_10_required_markers_stable(self):
        from paper_trading.performance_attribution.fixture_schema_v167 import REQUIRED_FIXTURE_MARKERS
        assert len(REQUIRED_FIXTURE_MARKERS) == 10

    def test_template_always_valid(self):
        from paper_trading.performance_attribution.fixture_schema_v167 import (
            build_fixture_template, validate_fixture_full,
        )
        for i in range(5):
            tmpl = build_fixture_template(f"reg_tmpl_{i}", "regression", "test")
            r = validate_fixture_full(tmpl)
            assert r["valid"] is True
