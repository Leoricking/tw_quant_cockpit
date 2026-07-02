"""
tests/test_paper_attribution_reconciliation_v167.py
Tests for paper attribution reconciler v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from paper_trading.performance_attribution.attribution_reconciler_v167 import (
    AttributionReconciler,
)
from paper_trading.performance_attribution.enums_v167 import ReconciliationStatus


class TestReconcilerExact:
    def setup_method(self):
        self.r = AttributionReconciler()

    def test_exact_match_is_reconciled(self):
        rec = self.r.reconcile("test", 100.0, 100.0)
        assert rec.status == ReconciliationStatus.RECONCILED

    def test_exact_match_residual_is_zero(self):
        rec = self.r.reconcile("test", 100.0, 100.0)
        assert rec.residual == 0.0

    def test_exact_match_confidence_high(self):
        from paper_trading.performance_attribution.enums_v167 import ConfidenceLevel
        rec = self.r.reconcile("test", 100.0, 100.0)
        assert rec.confidence == ConfidenceLevel.HIGH

    def test_zero_total_zero_sum_reconciled(self):
        rec = self.r.reconcile("test", 0.0, 0.0)
        assert rec.status == ReconciliationStatus.RECONCILED


class TestReconcilerRounding:
    def setup_method(self):
        self.r = AttributionReconciler()

    def test_tiny_residual_reconciled_with_rounding(self):
        rec = self.r.reconcile("test", 100.0, 100.0 + 5e-5)
        assert rec.status in (
            ReconciliationStatus.RECONCILED,
            ReconciliationStatus.RECONCILED_WITH_ROUNDING,
        )

    def test_floating_point_noise_handled(self):
        rec = self.r.reconcile("test", 0.1 + 0.2, 0.3)
        assert rec.status in (
            ReconciliationStatus.RECONCILED,
            ReconciliationStatus.RECONCILED_WITH_ROUNDING,
        )


class TestReconcilerDegraded:
    def setup_method(self):
        self.r = AttributionReconciler(tolerance=0.0001)

    def test_5x_tolerance_degraded(self):
        rec = self.r.reconcile("test", 100.0, 99.9995)
        # Within 10x but > 1x tolerance → DEGRADED
        assert rec.status == ReconciliationStatus.DEGRADED

    def test_degraded_confidence_low(self):
        from paper_trading.performance_attribution.enums_v167 import ConfidenceLevel
        rec = self.r.reconcile("test", 100.0, 99.999)
        assert rec.confidence in (ConfidenceLevel.LOW, ConfidenceLevel.UNKNOWN)


class TestReconcilerFailed:
    def setup_method(self):
        self.r = AttributionReconciler()

    def test_large_residual_fails(self):
        rec = self.r.reconcile("test", 100.0, 90.0)
        assert rec.status == ReconciliationStatus.FAILED

    def test_failed_residual_not_zero(self):
        rec = self.r.reconcile("test", 100.0, 90.0)
        assert rec.residual != 0.0

    def test_failed_residual_equals_expected_minus_actual(self):
        rec = self.r.reconcile("test", 100.0, 90.0)
        assert abs(rec.residual - 10.0) < 1e-9

    def test_failed_confidence_unknown(self):
        from paper_trading.performance_attribution.enums_v167 import ConfidenceLevel
        rec = self.r.reconcile("test", 100.0, 90.0)
        assert rec.confidence == ConfidenceLevel.UNKNOWN

    def test_failed_has_failing_dimensions(self):
        rec = self.r.reconcile("test", 100.0, 90.0)
        assert len(rec.failing_dimensions) > 0


class TestResidualNeverZeroed:
    """Core contract: residual is always computed, never auto-fixed."""

    def setup_method(self):
        self.r = AttributionReconciler()

    def test_residual_present_on_failure(self):
        rec = self.r.reconcile("test", 100.0, 95.0)
        assert rec.residual != 0.0

    def test_residual_present_on_degraded(self):
        r = AttributionReconciler(tolerance=0.0001)
        rec = r.reconcile("test", 100.0, 99.999)
        assert rec.residual != 0.0

    def test_cannot_pass_with_large_residual(self):
        rec = self.r.reconcile("test", 100.0, 50.0)
        assert rec.status == ReconciliationStatus.FAILED

    def test_residual_sign_correct(self):
        rec = self.r.reconcile("test", 100.0, 110.0)
        assert rec.residual == pytest.approx(-10.0)


class TestReconcilerPaperSafety:
    def setup_method(self):
        self.r = AttributionReconciler()

    def test_result_paper_only(self):
        rec = self.r.reconcile("test", 100.0, 100.0)
        assert rec.paper_only is True

    def test_result_research_only(self):
        rec = self.r.reconcile("test", 100.0, 100.0)
        assert rec.research_only is True

    def test_result_no_real_orders(self):
        rec = self.r.reconcile("test", 100.0, 100.0)
        assert rec.no_real_orders is True

    def test_result_not_for_production(self):
        rec = self.r.reconcile("test", 100.0, 100.0)
        assert rec.not_for_production is True


class TestReconcilerHierarchy:
    def setup_method(self):
        self.r = AttributionReconciler()

    def test_all_reconciled_when_all_match(self):
        result = self.r.reconcile_hierarchy(
            "portfolio",
            portfolio_total=100.0,
            component_sums={"symbols": 100.0, "strategies": 100.0},
        )
        assert result["all_reconciled"] is True

    def test_failing_dimensions_when_mismatch(self):
        result = self.r.reconcile_hierarchy(
            "portfolio",
            portfolio_total=100.0,
            component_sums={"symbols": 100.0, "strategies": 90.0},
        )
        assert "strategies" in result["failing_dimensions"]

    def test_paper_only_in_result(self):
        result = self.r.reconcile_hierarchy(
            "portfolio",
            portfolio_total=100.0,
            component_sums={},
        )
        assert result["paper_only"] is True


class TestReconcilerGrossNet:
    def setup_method(self):
        self.r = AttributionReconciler()

    def test_gross_minus_cost_equals_net_reconciles(self):
        rec = self.r.check_gross_net("test", gross=100.0, net=95.0, total_cost=5.0)
        assert rec.status == ReconciliationStatus.RECONCILED

    def test_gross_minus_cost_wrong_fails(self):
        rec = self.r.check_gross_net("test", gross=100.0, net=90.0, total_cost=5.0)
        assert rec.status == ReconciliationStatus.FAILED


class TestReconcilerActiveReturn:
    def setup_method(self):
        self.r = AttributionReconciler()

    def test_components_sum_to_active_return(self):
        rec = self.r.check_active_return(
            "test",
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

    def test_wrong_components_fail(self):
        rec = self.r.check_active_return(
            "test",
            active_return=0.10,
            selection=0.0, allocation=0.0, timing=0.0,
            exposure=0.0, execution=0.0, cost=0.0,
            risk=0.0, regime=0.0, benchmark=0.0,
            factor=0.0, residual=0.0,
        )
        assert rec.status == ReconciliationStatus.FAILED
