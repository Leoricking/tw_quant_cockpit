"""
tests/test_operational_integration_reconciler_full_v168.py — Full Reconciler tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.integration_reconciler_v168 import (
    IntegrationReconciler, _RECONCILIATION_PAIRS, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.enums_v168 import ReconciliationStatus


class TestReconcilerFullSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestReconcilerFull:
    def setup_method(self):
        self.reconciler = IntegrationReconciler()

    def test_reconciliation_pairs_count(self):
        assert len(_RECONCILIATION_PAIRS) == 10

    def test_reconcile_market_data_rows(self):
        result = self.reconciler.reconcile(
            "market_data_rows_vs_session_input_rows", 100.0, 100.0, 1e-6
        )
        assert result.status == ReconciliationStatus.RECONCILED

    def test_reconcile_session_signals(self):
        result = self.reconciler.reconcile(
            "session_signals_vs_strategy_signals", 50.0, 50.0, 1e-6
        )
        assert result.status == ReconciliationStatus.RECONCILED

    def test_reconcile_strategy_allocations(self):
        result = self.reconciler.reconcile(
            "strategy_allocations_vs_portfolio_positions", 10.0, 10.0, 1e-6
        )
        assert result.status == ReconciliationStatus.RECONCILED

    def test_reconcile_portfolio_orders(self):
        result = self.reconciler.reconcile(
            "portfolio_orders_vs_simulated_executions", 5.0, 5.0, 1e-6
        )
        assert result.status == ReconciliationStatus.RECONCILED

    def test_reconcile_analytics_pnl(self):
        result = self.reconciler.reconcile(
            "analytics_pnl_vs_attribution_pnl", 10000.0, 10000.0, 1e-6
        )
        assert result.status == ReconciliationStatus.RECONCILED

    def test_reconcile_all_passes_with_matching_context(self):
        ctx = {
            "market_data_rows": 100.0,
            "session_input_rows": 100.0,
            "session_signals": 50.0,
            "strategy_signals": 50.0,
            "strategy_allocations": 10.0,
            "portfolio_positions": 10.0,
            "portfolio_orders": 5.0,
            "simulated_executions": 5.0,
            "executions": 5.0,
            "analytics_trades": 5.0,
            "analytics_pnl": 10000.0,
            "attribution_pnl": 10000.0,
            "attribution_sessions": 3.0,
            "coordination_sessions": 3.0,
            "failure_events": 2.0,
            "recovery_records": 2.0,
            "component_health": 1.0,
            "aggregate_health": 1.0,
            "report_status": 1.0,
            "tolerance": 1e-6,
        }
        results = self.reconciler.reconcile_all(ctx)
        assert len(results) == 10
        for r in results:
            assert r.status in (
                ReconciliationStatus.RECONCILED,
                ReconciliationStatus.RECONCILED_WITH_ROUNDING,
            ), f"Reconciliation {r.dimension} status: {r.status}"

    def test_reconcile_degraded_when_near_tolerance(self):
        result = self.reconciler.reconcile(
            "near_tolerance", expected=100.0, actual=100.0 + 8e-6, tolerance=1e-6
        )
        assert result.status in (
            ReconciliationStatus.RECONCILED_WITH_ROUNDING,
            ReconciliationStatus.DEGRADED,
        )

    def test_reconcile_failed_when_far(self):
        result = self.reconciler.reconcile(
            "far_apart", expected=100.0, actual=200.0, tolerance=1e-6
        )
        assert result.status == ReconciliationStatus.FAILED

    def test_reconcile_all_empty_context(self):
        results = self.reconciler.reconcile_all({})
        assert len(results) == 10
        # All 0 vs 0 -> RECONCILED
        for r in results:
            assert r.status == ReconciliationStatus.RECONCILED

    def test_summarize_all_reconciled(self):
        results = self.reconciler.reconcile_all({})
        summary = self.reconciler.summarize(results)
        assert summary["reconciled_count"] == 10
        assert summary["failed_count"] == 0

    def test_reconcile_ids_have_dimension(self):
        results = self.reconciler.reconcile_all({})
        for r in results:
            assert "recon_" in r.reconciliation_id

    def test_reconcile_all_paper_only(self):
        results = self.reconciler.reconcile_all({})
        for r in results:
            assert r.paper_only is True

    def test_reconcile_with_list_context(self):
        ctx = {
            "market_data_rows": [1, 2, 3],
            "session_input_rows": [1, 2, 3],
        }
        results = self.reconciler.reconcile_all(ctx)
        assert len(results) == 10

    def test_reconcile_symmetric_residual(self):
        r1 = self.reconciler.reconcile("sym", 100.0, 105.0, 0.01)
        r2 = self.reconciler.reconcile("sym", 105.0, 100.0, 0.01)
        assert r1.residual == r2.residual

    def test_summarize_has_all_reconciled_flag(self):
        results = [self.reconciler.reconcile(f"d{i}", 100.0, 100.0, 0.01) for i in range(5)]
        summary = self.reconciler.summarize(results)
        assert summary["all_reconciled"] is True

    def test_reconcile_rounding_status(self):
        # Exactly at tolerance should be RECONCILED_WITH_ROUNDING
        result = self.reconciler.reconcile("rounding", 100.0, 100.0 + 5e-7, 1e-6)
        assert result.status in (
            ReconciliationStatus.RECONCILED,
            ReconciliationStatus.RECONCILED_WITH_ROUNDING,
        )

    def test_reconcile_component_id_is_reconciler(self):
        result = self.reconciler.reconcile("test", 1.0, 1.0, 0.01)
        assert result.component_id == "reconciler"

    def test_reconciliation_pair_first_entry(self):
        assert _RECONCILIATION_PAIRS[0] == ("market_data_rows", "session_input_rows")

    def test_reconciliation_pair_last_entry(self):
        assert _RECONCILIATION_PAIRS[-1] == ("aggregate_health", "report_status")
