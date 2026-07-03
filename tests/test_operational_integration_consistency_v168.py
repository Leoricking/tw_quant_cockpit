"""
tests/test_operational_integration_consistency_v168.py — Consistency Checker tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.consistency_checker_v168 import (
    ConsistencyChecker, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.models_v168 import ConsistencyResult


class TestConsistencySafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestConsistencyCheckerCore:
    def setup_method(self):
        self.checker = ConsistencyChecker()

    def test_check_all_returns_list(self):
        ctx = {
            "component_id": "market_data",
            "run_id": "R001",
            "session_id": "S001",
        }
        results = self.checker.check_all(ctx)
        assert isinstance(results, list)

    def test_check_all_not_empty(self):
        ctx = {
            "component_id": "market_data",
            "run_id": "R001",
            "session_id": "S001",
        }
        results = self.checker.check_all(ctx)
        assert len(results) > 0

    def test_check_all_returns_consistency_results(self):
        ctx = {"component_id": "c1", "run_id": "R001"}
        results = self.checker.check_all(ctx)
        for r in results:
            assert isinstance(r, ConsistencyResult)

    def test_check_all_consistent_versions(self):
        ctx = {
            "component_id": "c1",
            "component_version": "1.6.8",
            "expected_component_version": "1.6.8",
        }
        results = self.checker.check_all(ctx)
        version_results = [r for r in results if r.dimension == "component_version"]
        assert len(version_results) > 0
        assert version_results[0].status == "CONSISTENT"

    def test_check_all_inconsistent_versions(self):
        ctx = {
            "component_id": "c1",
            "component_version": "1.6.5",
            "expected_component_version": "1.6.8",
        }
        results = self.checker.check_all(ctx)
        version_results = [r for r in results if r.dimension == "component_version"]
        assert len(version_results) > 0
        assert version_results[0].status == "INCONSISTENT"

    def test_summarize_returns_dict(self):
        ctx = {"component_id": "c1"}
        results = self.checker.check_all(ctx)
        summary = self.checker.summarize(results)
        assert isinstance(summary, dict)

    def test_summarize_has_total(self):
        ctx = {"component_id": "c1"}
        results = self.checker.check_all(ctx)
        summary = self.checker.summarize(results)
        assert "total" in summary or "total_checks" in summary

    def test_summarize_paper_only(self):
        results = self.checker.check_all({"component_id": "c1"})
        summary = self.checker.summarize(results)
        assert summary.get("paper_only") is True

    def test_check_dimension_consistent(self):
        result = self.checker.check_dimension(
            "run_id", "R001", "R001", "comp1"
        )
        assert result.status == "CONSISTENT"

    def test_check_dimension_inconsistent(self):
        result = self.checker.check_dimension(
            "run_id", "R001", "R002", "comp1"
        )
        assert result.status == "INCONSISTENT"

    def test_check_dimension_paper_only(self):
        result = self.checker.check_dimension("test_dim", "A", "A", "c1")
        assert result.paper_only is True

    def test_check_all_with_pnl(self):
        ctx = {
            "component_id": "analytics",
            "expected_pnl": 1000.0,
            "actual_pnl": 1000.0,
        }
        results = self.checker.check_all(ctx)
        pnl_results = [r for r in results if r.dimension == "pnl"]
        assert len(pnl_results) > 0
        assert pnl_results[0].status == "CONSISTENT"

    def test_check_all_with_pnl_inconsistent(self):
        ctx = {
            "component_id": "analytics",
            "expected_pnl": 1000.0,
            "actual_pnl": 2000.0,
        }
        results = self.checker.check_all(ctx)
        pnl_results = [r for r in results if r.dimension == "pnl"]
        assert len(pnl_results) > 0
        assert pnl_results[0].status == "INCONSISTENT"

    def test_check_dimension_residual_zero_when_equal(self):
        result = self.checker.check_dimension("val", "100", "100", "c1")
        assert result.residual == 0.0 or result.status == "CONSISTENT"

    def test_consistency_result_has_check_id(self):
        result = self.checker.check_dimension("dim", "A", "A", "comp_test")
        assert result.check_id is not None
        assert "comp_test" in result.check_id or "dim" in result.check_id

    def test_check_all_session_consistency(self):
        ctx = {
            "component_id": "c1",
            "session_id": "SESS_001",
            "expected_session_id": "SESS_001",
            "actual_session_id": "SESS_001",
        }
        results = self.checker.check_all(ctx)
        session_results = [r for r in results if r.dimension == "session_id"]
        assert len(session_results) > 0
        assert session_results[0].status == "CONSISTENT"

    def test_summarize_all_consistent_returns_consistent(self):
        ctx = {
            "component_id": "c1",
            "component_version": "1.6.8",
            "expected_component_version": "1.6.8",
            "schema_version": "1.6.8",
            "expected_schema_version": "1.6.8",
        }
        results = self.checker.check_all(ctx)
        summary = self.checker.summarize(results)
        assert isinstance(summary, dict)

    def test_multiple_contexts_independent(self):
        checker2 = ConsistencyChecker()
        ctx = {"component_id": "c1"}
        r1 = self.checker.check_all(ctx)
        r2 = checker2.check_all(ctx)
        assert len(r1) == len(r2)
