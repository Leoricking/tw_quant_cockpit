"""
tests/test_operational_integration_e2e_v168.py — End-to-End pipeline tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.integration_pipeline_v168 import IntegrationPipeline
from paper_trading.operational_integration.models_v168 import IntegrationContext
from paper_trading.operational_integration.integration_scorecard_v168 import IntegrationScorecard
from paper_trading.operational_integration.integration_report_v168 import IntegrationReportGenerator
from paper_trading.operational_integration.integration_reconciler_v168 import IntegrationReconciler
from paper_trading.operational_integration.determinism_checker_v168 import DeterminismChecker
from paper_trading.operational_integration.state_snapshot_v168 import StateSnapshotManager
from paper_trading.operational_integration.integration_store_v168 import IntegrationStore
from paper_trading.operational_integration.integration_query_v168 import IntegrationQueryService
from paper_trading.operational_integration.enums_v168 import (
    IntegrationStage, ReconciliationStatus, DeterminismStatus,
)
import paper_trading.operational_integration.safety_v168 as safety


def _make_context(**kwargs):
    defaults = dict(
        run_id="E2E_R001",
        session_id="E2E_S001",
        component_id="market_data_session",
        period_start="2026-01-02",
        period_end="2026-01-03",
    )
    defaults.update(kwargs)
    return IntegrationContext(**defaults)


class TestE2ESafetyFlags:
    def test_paper_only(self):
        from paper_trading.operational_integration.integration_pipeline_v168 import PAPER_ONLY
        assert PAPER_ONLY is True

    def test_research_only(self):
        from paper_trading.operational_integration.integration_pipeline_v168 import RESEARCH_ONLY
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        from paper_trading.operational_integration.integration_pipeline_v168 import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True


class TestEndToEndPipeline:
    def setup_method(self):
        self.pipeline = IntegrationPipeline()
        self.scorecard = IntegrationScorecard()
        self.report_gen = IntegrationReportGenerator()
        self.reconciler = IntegrationReconciler()
        self.det_checker = DeterminismChecker()
        self.snapshot_mgr = StateSnapshotManager()
        self.store = IntegrationStore()
        self.query_svc = IntegrationQueryService(self.store)

    def test_e2e_full_pipeline_run(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert result["status"] == "COMPLETE"
        assert result["paper_only"] is True

    def test_e2e_context_to_stages(self):
        ctx = _make_context(run_id="E2E_STAGES")
        result = self.pipeline.run(ctx)
        stages = result["stages"]
        assert len(stages) > 5

    def test_e2e_all_stages_paper_only(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        for stage in result["stages"]:
            assert stage.get("paper_only") is True

    def test_e2e_scorecard_after_pipeline(self):
        ctx = _make_context(run_id="E2E_SCORE")
        run_result = self.pipeline.run(ctx)
        run_result["contract_score"] = 100.0
        run_result["data_flow_score"] = 100.0
        score = self.scorecard.compute(run_result)
        assert score.not_for_real_trading is True
        assert score.total_score >= 0.0

    def test_e2e_report_after_pipeline(self):
        ctx = _make_context(run_id="E2E_REPORT")
        run_result = self.pipeline.run(ctx)
        sections = self.report_gen._build_sections(run_result)
        assert len(sections) == 19

    def test_e2e_reconciliation_pass(self):
        result = self.reconciler.reconcile("e2e_pnl", 1000.0, 1000.0, 0.01)
        assert result.status == ReconciliationStatus.RECONCILED

    def test_e2e_determinism_check(self):
        ctx = _make_context(run_id="E2E_DET")
        run1 = self.pipeline.run(ctx)
        run2 = self.pipeline.run(ctx)
        det_result = self.det_checker.check_run(run1, run2)
        assert det_result.status in (DeterminismStatus.DETERMINISTIC, DeterminismStatus.PARTIAL)

    def test_e2e_snapshot_after_pipeline(self):
        ctx = _make_context(run_id="E2E_SNAP")
        run_result = self.pipeline.run(ctx)
        snap = self.snapshot_mgr.take_snapshot(
            "E2E_SNAP",
            {"run_result": run_result.get("status", "COMPLETE")},
        )
        assert snap is not None
        assert snap.run_id == "E2E_SNAP"
        assert snap.paper_only is True

    def test_e2e_safety_validation(self):
        result = safety.validate_integration_safety({
            "run_id": "E2E_SAFE",
            "session_id": "SESS_001",
        })
        assert result["safe"] is True
        assert result["paper_only"] is True

    def test_e2e_safety_blocks_forbidden_field(self):
        result = safety.validate_integration_safety({
            "broker_session": "SHOULD_BE_BLOCKED",
        })
        assert result["safe"] is False
        assert result["blocked"] is True

    def test_e2e_multiple_runs_consistent(self):
        ctx1 = _make_context(run_id="E2E_CONSISTENT_1")
        ctx2 = _make_context(run_id="E2E_CONSISTENT_2")
        r1 = self.pipeline.run(ctx1)
        r2 = self.pipeline.run(ctx2)
        assert r1["status"] == r2["status"]
        assert len(r1["stages"]) == len(r2["stages"])

    def test_e2e_context_period_preserved(self):
        ctx = _make_context(
            run_id="E2E_PERIOD",
            period_start="2026-01-02",
            period_end="2026-01-05",
        )
        result = self.pipeline.run(ctx)
        assert result["period_start"] == "2026-01-02"
        assert result["period_end"] == "2026-01-05"

    def test_e2e_no_real_orders_in_all_stages(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert result["no_real_orders"] is True

    def test_e2e_not_for_production_flag(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert result["not_for_production"] is True

    def test_e2e_reconcile_all_10_pairs(self):
        results = self.reconciler.reconcile_all({})
        assert len(results) == 10
        for r in results:
            assert r.paper_only is True

    def test_e2e_pipeline_mode_research_only(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert result["mode"] == "RESEARCH_ONLY"

    def test_e2e_report_has_safety_section(self):
        ctx = _make_context(run_id="E2E_SAFETY_RPT")
        run_result = self.pipeline.run(ctx)
        sections = self.report_gen._build_sections(run_result)
        assert sections["Safety"]["paper_only"] is True
        assert sections["Safety"]["no_real_orders"] is True

    def test_e2e_snapshot_restore(self):
        snap = self.snapshot_mgr.take_snapshot("E2E_RESTORE", {"status": "COMPLETE"})
        restored = self.snapshot_mgr.restore_snapshot(snap.snapshot_id)
        assert restored.snapshot_id == snap.snapshot_id
        assert restored.components["status"] == "COMPLETE"

    def test_e2e_scorecard_grade_with_all_100(self):
        run_result = {
            "run_id": "E2E_GRADE",
            "contract_score": 100.0,
            "data_flow_score": 100.0,
            "lineage_score": 100.0,
            "identity_score": 100.0,
            "timestamp_score": 100.0,
            "reconciliation_score": 100.0,
            "determinism_score": 100.0,
            "failure_isolation_score": 100.0,
            "safety_score": 100.0,
        }
        score = self.scorecard.compute(run_result)
        assert score.grade == "A"
        assert abs(score.total_score - 100.0) < 1e-6

    def test_e2e_report_not_for_real_trading_section(self):
        ctx = _make_context(run_id="E2E_NFP")
        run_result = self.pipeline.run(ctx)
        sections = self.report_gen._build_sections(run_result)
        assert sections["Not for Real Trading"]["not_for_production"] is True
