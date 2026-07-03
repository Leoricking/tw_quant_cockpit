"""
tests/test_operational_integration_determinism_v168.py — Determinism Checker tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.determinism_checker_v168 import (
    DeterminismChecker, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS, _stable_hash,
)
from paper_trading.operational_integration.models_v168 import DeterminismResult
from paper_trading.operational_integration.enums_v168 import DeterminismStatus


class TestDeterminismSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestDeterminismCheckerCore:
    def setup_method(self):
        self.checker = DeterminismChecker()

    def test_check_hash_stability_equal(self):
        result = self.checker.check_hash_stability("abc123", "abc123")
        assert result is True

    def test_check_hash_stability_different(self):
        result = self.checker.check_hash_stability("abc123", "xyz789")
        assert result is False

    def test_check_order_stability_equal(self):
        result = self.checker.check_order_stability(["a", "b", "c"], ["a", "b", "c"])
        assert result is True

    def test_check_order_stability_different(self):
        result = self.checker.check_order_stability(["a", "b"], ["b", "a"])
        assert result is False

    def test_check_score_stability_equal(self):
        result = self.checker.check_score_stability(95.0, 95.0)
        assert result is True

    def test_check_score_stability_different(self):
        result = self.checker.check_score_stability(95.0, 94.9)
        assert result is False

    def test_check_run_returns_result(self):
        run1 = {"run_id": "R001", "component_id": "c1", "scorecard_total": 95.0}
        run2 = {"run_id": "R001", "component_id": "c1", "scorecard_total": 95.0}
        result = self.checker.check_run(run1, run2)
        assert isinstance(result, DeterminismResult)

    def test_check_run_deterministic(self):
        run1 = {"run_id": "R001", "component_id": "c1", "scorecard_total": 95.0, "value": 42}
        run2 = {"run_id": "R001", "component_id": "c1", "scorecard_total": 95.0, "value": 42}
        result = self.checker.check_run(run1, run2)
        assert result.status == DeterminismStatus.DETERMINISTIC

    def test_check_run_non_deterministic(self):
        run1 = {"run_id": "R001", "component_id": "c1", "scorecard_total": 95.0, "value": 42}
        run2 = {"run_id": "R001", "component_id": "c1", "scorecard_total": 90.0, "value": 99}
        result = self.checker.check_run(run1, run2)
        assert result.status != DeterminismStatus.DETERMINISTIC

    def test_check_run_paper_only(self):
        run1 = {"run_id": "R001", "component_id": "c1"}
        run2 = {"run_id": "R001", "component_id": "c1"}
        result = self.checker.check_run(run1, run2)
        assert result.paper_only is True

    def test_check_run_hash_stable(self):
        data = {"run_id": "R001", "component_id": "c1", "x": 5}
        result = self.checker.check_run(data, data.copy())
        assert result.hash_stable is True

    def test_check_snapshot_stability_same(self):
        snap1 = {"component": "value1"}
        snap2 = {"component": "value1"}
        result = self.checker.check_snapshot_stability(snap1, snap2)
        assert result is True

    def test_check_snapshot_stability_different(self):
        snap1 = {"component": "value1"}
        snap2 = {"component": "value2"}
        result = self.checker.check_snapshot_stability(snap1, snap2)
        assert result is False

    def test_check_report_stability_same(self):
        r1 = {"run_id": "R001", "status": "COMPLETE"}
        r2 = {"run_id": "R001", "status": "COMPLETE"}
        result = self.checker.check_report_stability(r1, r2)
        assert result is True

    def test_check_report_stability_different(self):
        r1 = {"run_id": "R001", "status": "COMPLETE"}
        r2 = {"run_id": "R001", "status": "FAILED"}
        result = self.checker.check_report_stability(r1, r2)
        assert result is False

    def test_summarize_returns_dict(self):
        run = {"run_id": "R001", "component_id": "c1"}
        result = self.checker.check_run(run, run.copy())
        summary = self.checker.summarize([result])
        assert isinstance(summary, dict)

    def test_summarize_paper_only(self):
        summary = self.checker.summarize([])
        assert summary.get("paper_only") is True

    def test_stable_hash_deterministic(self):
        obj = {"a": 1, "b": 2}
        h1 = _stable_hash(obj)
        h2 = _stable_hash(obj)
        assert h1 == h2

    def test_stable_hash_different_objects(self):
        h1 = _stable_hash({"a": 1})
        h2 = _stable_hash({"a": 2})
        assert h1 != h2

    def test_check_run_timestamps_excluded(self):
        run1 = {"run_id": "R001", "component_id": "c1", "created_at": "2026-01-01T00:00:00Z"}
        run2 = {"run_id": "R001", "component_id": "c1", "created_at": "2026-01-02T00:00:00Z"}
        result = self.checker.check_run(run1, run2)
        assert result.hash_stable is True
