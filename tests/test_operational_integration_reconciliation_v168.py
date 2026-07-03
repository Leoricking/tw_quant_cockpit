"""
tests/test_operational_integration_reconciliation_v168.py — Integration Reconciler tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.integration_reconciler_v168 import (
    IntegrationReconciler, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.models_v168 import ReconciliationResult
from paper_trading.operational_integration.enums_v168 import ReconciliationStatus


class TestReconciliationSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestIntegrationReconcilerCore:
    def setup_method(self):
        self.reconciler = IntegrationReconciler()

    def test_reconcile_returns_result(self):
        result = self.reconciler.reconcile(
            dimension="pnl", expected=100.0, actual=100.0, tolerance=0.01
        )
        assert isinstance(result, ReconciliationResult)

    def test_reconcile_exact_match_reconciled(self):
        result = self.reconciler.reconcile(
            dimension="pnl", expected=100.0, actual=100.0, tolerance=0.01
        )
        assert result.status == ReconciliationStatus.RECONCILED

    def test_reconcile_within_tolerance(self):
        result = self.reconciler.reconcile(
            dimension="pnl", expected=100.0, actual=100.0000001, tolerance=1e-4
        )
        assert result.status in (ReconciliationStatus.RECONCILED, ReconciliationStatus.RECONCILED_WITH_ROUNDING)

    def test_reconcile_outside_tolerance_failed(self):
        result = self.reconciler.reconcile(
            dimension="pnl", expected=100.0, actual=200.0, tolerance=0.01
        )
        assert result.status == ReconciliationStatus.FAILED

    def test_reconcile_paper_only(self):
        result = self.reconciler.reconcile(
            dimension="pnl", expected=100.0, actual=100.0, tolerance=0.01
        )
        assert result.paper_only is True

    def test_reconcile_residual_computed(self):
        result = self.reconciler.reconcile(
            dimension="pnl", expected=100.0, actual=105.0, tolerance=0.01
        )
        assert abs(result.residual - 5.0) < 1e-9

    def test_reconcile_dimension_stored(self):
        result = self.reconciler.reconcile(
            dimension="my_dimension", expected=1.0, actual=1.0, tolerance=0.01
        )
        assert result.dimension == "my_dimension"

    def test_reconcile_expected_stored(self):
        result = self.reconciler.reconcile(
            dimension="test", expected=42.0, actual=42.0, tolerance=0.01
        )
        assert result.expected == 42.0

    def test_reconcile_actual_stored(self):
        result = self.reconciler.reconcile(
            dimension="test", expected=42.0, actual=43.0, tolerance=0.01
        )
        assert result.actual == 43.0

    def test_reconcile_all_returns_list(self):
        ctx = {
            "market_data_rows": 100.0,
            "session_input_rows": 100.0,
        }
        results = self.reconciler.reconcile_all(ctx)
        assert isinstance(results, list)
        assert len(results) > 0

    def test_reconcile_all_10_pairs(self):
        results = self.reconciler.reconcile_all({})
        assert len(results) == 10

    def test_reconcile_all_paper_only(self):
        results = self.reconciler.reconcile_all({})
        for r in results:
            assert r.paper_only is True

    def test_summarize_returns_dict(self):
        result = self.reconciler.reconcile(
            dimension="pnl", expected=100.0, actual=100.0, tolerance=0.01
        )
        summary = self.reconciler.summarize([result])
        assert isinstance(summary, dict)

    def test_summarize_paper_only(self):
        summary = self.reconciler.summarize([])
        assert summary.get("paper_only") is True

    def test_summarize_has_total(self):
        results = [
            self.reconciler.reconcile("d1", 100.0, 100.0, 0.01),
            self.reconciler.reconcile("d2", 200.0, 200.0, 0.01),
        ]
        summary = self.reconciler.summarize(results)
        assert "total_reconciliations" in summary
        assert summary["total_reconciliations"] == 2

    def test_reconcile_id_has_dimension(self):
        result = self.reconciler.reconcile("test_dim", 1.0, 1.0, 0.01)
        assert "test_dim" in result.reconciliation_id

    def test_reconcile_zero_values(self):
        result = self.reconciler.reconcile("zeros", 0.0, 0.0, 0.01)
        assert result.status == ReconciliationStatus.RECONCILED

    def test_reconcile_with_rounding(self):
        result = self.reconciler.reconcile(
            dimension="rounding", expected=100.0, actual=100.0 + 1e-8, tolerance=1e-6
        )
        assert result.status in (
            ReconciliationStatus.RECONCILED,
            ReconciliationStatus.RECONCILED_WITH_ROUNDING,
        )

    def test_reconcile_all_with_matching_context(self):
        ctx = {
            "market_data_rows": 100.0,
            "session_input_rows": 100.0,
            "session_signals": 50.0,
            "strategy_signals": 50.0,
            "tolerance": 1e-6,
        }
        results = self.reconciler.reconcile_all(ctx)
        assert len(results) == 10

    def test_reconcile_degraded_status(self):
        # Within 10x tolerance but not within tolerance
        result = self.reconciler.reconcile(
            dimension="near", expected=100.0, actual=100.0 + 5e-6, tolerance=1e-6
        )
        assert result.status in (
            ReconciliationStatus.RECONCILED_WITH_ROUNDING,
            ReconciliationStatus.DEGRADED,
            ReconciliationStatus.FAILED,
        )
