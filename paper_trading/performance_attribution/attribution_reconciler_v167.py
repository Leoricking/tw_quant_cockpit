"""
paper_trading/performance_attribution/attribution_reconciler_v167.py
Reconciliation engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Cannot fix PASS. Cannot zero residual. Cannot RECONCILE when tolerance exceeded.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

from .enums_v167 import ReconciliationStatus, ConfidenceLevel
from .models_v167 import AttributionReconciliation

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class AttributionReconciler:
    """
    Reconciliation engine.
    Checks hierarchy, gross/net, costs, strategy/session sums, benchmark, etc.
    Never returns RECONCILED when residual exceeds tolerance.
    Never sets residual to 0.
    """

    def __init__(
        self,
        tolerance: float = 0.0001,
        rounding_tolerance: float = 1e-8,
    ) -> None:
        self._tol = tolerance
        self._rounding_tol = rounding_tolerance

    def reconcile(
        self,
        entity_id: str,
        expected_total: float,
        component_sum: float,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> AttributionReconciliation:
        """
        Core reconciliation: expected_total vs component_sum.
        Returns RECONCILED, RECONCILED_WITH_ROUNDING, DEGRADED, or FAILED.
        """
        residual = expected_total - component_sum
        abs_res = abs(residual)

        # Separate rounding vs model residual
        if abs_res <= self._rounding_tol:
            rounding_residual = residual
            model_residual = 0.0
            status = ReconciliationStatus.RECONCILED
            confidence = ConfidenceLevel.HIGH
        elif abs_res <= self._tol:
            rounding_residual = residual
            model_residual = 0.0
            status = ReconciliationStatus.RECONCILED_WITH_ROUNDING
            confidence = ConfidenceLevel.MEDIUM
        elif abs_res <= self._tol * 10:
            rounding_residual = 0.0
            model_residual = residual
            status = ReconciliationStatus.DEGRADED
            confidence = ConfidenceLevel.LOW
        else:
            rounding_residual = 0.0
            model_residual = residual
            status = ReconciliationStatus.FAILED
            confidence = ConfidenceLevel.UNKNOWN

        return AttributionReconciliation(
            entity_id=entity_id,
            expected_total=expected_total,
            actual_component_sum=component_sum,
            residual=residual,
            rounding_residual=rounding_residual,
            model_residual=model_residual,
            tolerance=self._tol,
            status=status,
            failing_dimensions=[] if status in (
                ReconciliationStatus.RECONCILED,
                ReconciliationStatus.RECONCILED_WITH_ROUNDING,
            ) else ["component_sum"],
            source_lineage=source_lineage,
            precision=8,
            confidence=confidence,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )

    def reconcile_hierarchy(
        self,
        entity_id: str,
        portfolio_total: float,
        component_sums: Dict[str, float],   # name -> sum
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> Dict[str, Any]:
        """
        Full hierarchy reconciliation check.
        Checks: portfolio vs sum of each aggregation level.
        """
        checks: Dict[str, Any] = {}
        failing_dimensions: List[str] = []

        for dim_name, dim_sum in component_sums.items():
            rec = self.reconcile(entity_id, portfolio_total, dim_sum, period_start, period_end, source_lineage)
            checks[dim_name] = {
                "residual": rec.residual,
                "status": rec.status.value,
                "tolerance": self._tol,
            }
            if rec.status not in (ReconciliationStatus.RECONCILED, ReconciliationStatus.RECONCILED_WITH_ROUNDING):
                failing_dimensions.append(dim_name)

        all_reconciled = len(failing_dimensions) == 0
        return {
            "entity_id": entity_id,
            "all_reconciled": all_reconciled,
            "checks": checks,
            "failing_dimensions": failing_dimensions,
            "tolerance": self._tol,
            "period_start": period_start,
            "period_end": period_end,
            "source_lineage": source_lineage,
            "paper_only": True,
            "research_only": True,
        }

    def check_gross_net(
        self,
        entity_id: str,
        gross: float,
        net: float,
        total_cost: float,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> AttributionReconciliation:
        """Reconcile: gross - total_cost == net."""
        expected_net = gross - total_cost
        return self.reconcile(entity_id, expected_net, net, period_start, period_end, source_lineage)

    def check_realized_unrealized(
        self,
        entity_id: str,
        total_pnl: float,
        realized: float,
        unrealized: float,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> AttributionReconciliation:
        """Reconcile: realized + unrealized == total."""
        return self.reconcile(entity_id, total_pnl, realized + unrealized, period_start, period_end, source_lineage)

    def check_active_return(
        self,
        entity_id: str,
        active_return: float,
        selection: float,
        allocation: float,
        timing: float,
        exposure: float,
        execution: float,
        cost: float,
        risk: float,
        regime: float,
        benchmark: float,
        factor: float,
        residual: float,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> AttributionReconciliation:
        """Reconcile active return vs sum of all attribution dimensions."""
        component_sum = (selection + allocation + timing + exposure + execution
                         + cost + risk + regime + benchmark + factor + residual)
        return self.reconcile(entity_id, active_return, component_sum, period_start, period_end, source_lineage)
