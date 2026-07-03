"""
tests/test_operational_integration_determinism_full_v168.py — Full Determinism tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.determinism_checker_v168 import (
    DeterminismChecker, _stable_hash, _EXCLUDE_FIELDS, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.integration_pipeline_v168 import IntegrationPipeline
from paper_trading.operational_integration.models_v168 import IntegrationContext
from paper_trading.operational_integration.enums_v168 import DeterminismStatus


def _make_context(run_id="DET_R001"):
    return IntegrationContext(
        run_id=run_id,
        session_id="DET_S001",
        component_id="market_data_session",
        period_start="2026-01-02",
        period_end="2026-01-03",
    )


class TestDeterminismFullSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestDeterminismFull:
    def setup_method(self):
        self.checker = DeterminismChecker()
        self.pipeline = IntegrationPipeline()

    def test_stable_hash_same_input_same_output(self):
        h = _stable_hash({"key": "value", "number": 42})
        h2 = _stable_hash({"key": "value", "number": 42})
        assert h == h2

    def test_stable_hash_different_inputs(self):
        h1 = _stable_hash({"key": "value1"})
        h2 = _stable_hash({"key": "value2"})
        assert h1 != h2

    def test_stable_hash_dict_order_independent(self):
        h1 = _stable_hash({"a": 1, "b": 2})
        h2 = _stable_hash({"b": 2, "a": 1})
        assert h1 == h2

    def test_exclude_fields_contains_created_at(self):
        assert "created_at" in _EXCLUDE_FIELDS

    def test_exclude_fields_contains_updated_at(self):
        assert "updated_at" in _EXCLUDE_FIELDS

    def test_exclude_fields_contains_timestamp(self):
        assert "timestamp" in _EXCLUDE_FIELDS

    def test_pipeline_runs_deterministic(self):
        ctx = _make_context("DET_PIPELINE_1")
        r1 = self.pipeline.run(ctx)
        r2 = self.pipeline.run(ctx)
        result = self.checker.check_run(r1, r2)
        assert result.status == DeterminismStatus.DETERMINISTIC

    def test_check_run_hash_stable_pipeline(self):
        ctx = _make_context("DET_HASH_1")
        r1 = self.pipeline.run(ctx)
        r2 = self.pipeline.run(ctx)
        result = self.checker.check_run(r1, r2)
        assert result.hash_stable is True

    def test_check_run_order_stable_pipeline(self):
        ctx = _make_context("DET_ORDER_1")
        r1 = self.pipeline.run(ctx)
        r2 = self.pipeline.run(ctx)
        result = self.checker.check_run(r1, r2)
        assert result.order_stable is True

    def test_check_run_score_stable(self):
        r1 = {"run_id": "R1", "component_id": "c1", "scorecard_total": 95.0}
        r2 = {"run_id": "R1", "component_id": "c1", "scorecard_total": 95.0}
        result = self.checker.check_run(r1, r2)
        assert result.score_stable is True

    def test_check_run_score_unstable(self):
        r1 = {"run_id": "R1", "component_id": "c1", "scorecard_total": 95.0}
        r2 = {"run_id": "R1", "component_id": "c1", "scorecard_total": 85.0}
        result = self.checker.check_run(r1, r2)
        assert result.score_stable is False

    def test_summarize_all_deterministic(self):
        ctx = _make_context("DET_SUM_1")
        r1 = self.pipeline.run(ctx)
        r2 = self.pipeline.run(ctx)
        result = self.checker.check_run(r1, r2)
        summary = self.checker.summarize([result])
        assert isinstance(summary, dict)
        assert summary.get("paper_only") is True

    def test_summarize_deterministic_count(self):
        runs = []
        for i in range(3):
            ctx = _make_context(f"DET_COUNT_{i}")
            r1 = self.pipeline.run(ctx)
            r2 = self.pipeline.run(ctx)
            runs.append(self.checker.check_run(r1, r2))
        summary = self.checker.summarize(runs)
        assert "total" in summary or "deterministic_count" in summary or "total_checks" in summary

    def test_multiple_pipeline_runs_all_deterministic(self):
        ctx = _make_context("DET_MULTI")
        results = []
        for _ in range(3):
            r = self.pipeline.run(ctx)
            results.append(r)
        for i in range(1, len(results)):
            det_result = self.checker.check_run(results[0], results[i])
            assert det_result.status == DeterminismStatus.DETERMINISTIC

    def test_check_snapshot_stability_identical(self):
        snap = {"component_a": "value1", "component_b": "value2"}
        assert self.checker.check_snapshot_stability(snap, snap.copy()) is True

    def test_check_snapshot_stability_different(self):
        snap1 = {"component_a": "value1"}
        snap2 = {"component_a": "value2"}
        assert self.checker.check_snapshot_stability(snap1, snap2) is False

    def test_check_snapshot_stability_none_both(self):
        assert self.checker.check_snapshot_stability(None, None) is True

    def test_check_hash_stability_same_sha256(self):
        import hashlib
        import json
        data = {"x": 1, "y": 2}
        h = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        assert self.checker.check_hash_stability(h, h) is True

    def test_check_report_stability_timestamps_excluded(self):
        r1 = {"run_id": "R001", "status": "COMPLETE", "created_at": "2026-01-01"}
        r2 = {"run_id": "R001", "status": "COMPLETE", "created_at": "2026-01-02"}
        assert self.checker.check_report_stability(r1, r2) is True

    def test_result_paper_only(self):
        r1 = {"run_id": "R1", "component_id": "c1"}
        r2 = {"run_id": "R1", "component_id": "c1"}
        result = self.checker.check_run(r1, r2)
        assert result.paper_only is True

    def test_result_no_real_orders(self):
        r1 = {"run_id": "R1", "component_id": "c1"}
        r2 = {"run_id": "R1", "component_id": "c1"}
        result = self.checker.check_run(r1, r2)
        assert result.no_real_orders is True
