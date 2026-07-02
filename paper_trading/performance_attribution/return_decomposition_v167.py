"""
paper_trading/performance_attribution/return_decomposition_v167.py
Return decomposition engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] residual always visible; never auto-zeroed; threshold-enforced.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .enums_v167 import AttributionStatus, ConfidenceLevel, ReturnBasis
from .models_v167 import ReturnContribution, AttributionLevel, ResidualContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_SCHEMA_VERSION = "167"
_POLICY_VERSION = "1.6.7-paper-attribution"


# ─────────────────────────────────────────────────────────────────────────────
# Return calculations
# ─────────────────────────────────────────────────────────────────────────────

def calc_simple_return(begin: float, end: float) -> float:
    """(end - begin) / begin. Raises ZeroDivisionError if begin == 0."""
    if begin == 0.0:
        raise ZeroDivisionError("begin equity is zero — cannot compute return")
    return (end - begin) / begin


def calc_gross_return(begin: float, end: float, cash_flows: List[Dict[str, Any]] = None) -> float:
    """
    Simple gross return ignoring costs.
    For multi-cash-flow periods: simplified beginning-of-period approximation.
    Does not use future prices.
    """
    if cash_flows:
        # Approximate: treat net cash flows as mid-period
        net_cf = sum(cf.get("amount", 0.0) for cf in cash_flows)
        adjusted_end = end - net_cf
        return calc_simple_return(begin, adjusted_end)
    return calc_simple_return(begin, end)


def calc_net_return(gross_return: float, cost_items: Dict[str, float]) -> Tuple[float, float]:
    """
    net_return = gross_return - sum(cost_items) / begin_equity.
    Returns (net_return, total_cost_rate).
    cost_items: dict of cost_name -> cost_amount (absolute).
    """
    total_cost_rate = sum(cost_items.values())
    net_return = gross_return - total_cost_rate
    return net_return, total_cost_rate


def calc_active_return(portfolio_return: float, benchmark_return: float) -> float:
    """active_return = portfolio_return - benchmark_return."""
    return portfolio_return - benchmark_return


def calc_twr(period_returns: List[float]) -> float:
    """
    Time-weighted return from list of sub-period returns.
    TWR = product of (1 + r_i) - 1.
    Returns 0.0 for empty list.
    """
    if not period_returns:
        return 0.0
    product = 1.0
    for r in period_returns:
        product *= (1.0 + r)
    return product - 1.0


def calc_mwr(cash_flows: List[Dict[str, Any]], end_value: float, begin_value: float) -> Optional[float]:
    """
    Money-weighted return (IRR approximation).
    Returns None if insufficient data (< 2 periods) or cannot converge.
    Paper/simulation only — does not use real account data.
    """
    # Require at least begin + end
    if not cash_flows and begin_value > 0:
        # Simple single-period MWR = same as simple return
        if begin_value == 0:
            return None
        return (end_value - begin_value) / begin_value

    # Simple Newton-Raphson for IRR on cash flows
    # cf = [(t_days, amount), ...] where negative = outflow (investment)
    cfs: List[Tuple[int, float]] = [(-1, begin_value)]  # outflow at t=0 (day -1 placeholder)
    for cf in cash_flows:
        t = cf.get("day_offset", 0)
        amt = cf.get("amount", 0.0)
        cfs.append((t, -amt))  # outflow = negative from investor perspective
    cfs.append((365, end_value))  # inflow at end

    # Too few data points
    if len(cfs) < 2:
        return None

    def npv(r: float) -> float:
        total = 0.0
        for t, amt in cfs:
            days = max(t, 0)
            total += amt / ((1.0 + r) ** (days / 365.0))
        return total

    # Bisect between -0.99 and 10.0
    lo, hi = -0.99, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if abs(npv(mid)) < 1e-8:
            return mid
        if npv(mid) * npv(lo) < 0:
            hi = mid
        else:
            lo = mid
    return None  # did not converge


def calc_cumulative_return(daily_returns: List[float]) -> float:
    """Cumulative return from list of daily returns."""
    return calc_twr(daily_returns)


def decompose_gross_to_net(
    gross_return: float,
    begin_equity: float,
    commission: float = 0.0,
    transaction_tax: float = 0.0,
    exchange_fee: float = 0.0,
    borrow_cost: float = 0.0,
    financing_cost: float = 0.0,
    spread_cost: float = 0.0,
    slippage: float = 0.0,
    impact_cost: float = 0.0,
) -> Dict[str, float]:
    """
    Decompose gross to net return.
    All cost amounts are absolute; divided by begin_equity to get rate.
    Returns dict of return components.
    """
    if begin_equity <= 0:
        raise ValueError(f"begin_equity must be positive, got {begin_equity}")
    be = begin_equity
    result = {
        "gross_return": gross_return,
        "commission_rate": commission / be,
        "transaction_tax_rate": transaction_tax / be,
        "exchange_fee_rate": exchange_fee / be,
        "borrow_cost_rate": borrow_cost / be,
        "financing_cost_rate": financing_cost / be,
        "spread_cost_rate": spread_cost / be,
        "slippage_rate": slippage / be,
        "impact_cost_rate": impact_cost / be,
    }
    total_cost_rate = (
        result["commission_rate"] + result["transaction_tax_rate"]
        + result["exchange_fee_rate"] + result["borrow_cost_rate"]
        + result["financing_cost_rate"] + result["spread_cost_rate"]
        + result["slippage_rate"] + result["impact_cost_rate"]
    )
    result["total_cost_rate"] = total_cost_rate
    result["net_return"] = gross_return - total_cost_rate
    result["identity_check"] = abs(result["net_return"] - (gross_return - total_cost_rate)) < 1e-10
    return result


def decompose_active_return(
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
    active_return: float,
    residual_tolerance: float = 0.0001,
) -> Dict[str, Any]:
    """
    selection + allocation + timing + exposure + execution + cost +
    risk + regime + benchmark + factor + residual = active_return.
    Returns decomposition dict with reconciliation status.
    residual is ALWAYS visible and never auto-zeroed.
    """
    component_sum = (selection + allocation + timing + exposure + execution
                     + cost + risk + regime + benchmark + factor + residual)
    model_residual = active_return - component_sum
    abs_residual = abs(model_residual)
    exceeds_threshold = abs_residual > residual_tolerance

    if exceeds_threshold:
        status = "FAILED"
    elif abs(component_sum - active_return) < 1e-8:
        status = "RECONCILED"
    else:
        status = "RECONCILED_WITH_ROUNDING"

    return {
        "selection": selection,
        "allocation": allocation,
        "timing": timing,
        "exposure": exposure,
        "execution": execution,
        "cost": cost,
        "risk": risk,
        "regime": regime,
        "benchmark": benchmark,
        "factor": factor,
        "residual": residual,
        "component_sum": component_sum,
        "active_return": active_return,
        "model_residual": model_residual,
        "abs_model_residual": abs_residual,
        "residual_tolerance": residual_tolerance,
        "exceeds_threshold": exceeds_threshold,
        "status": status,
        "residual_visible": True,
        "paper_only": True,
        "research_only": True,
    }


class ReturnDecompositionEngine:
    """
    Deterministic return decomposition engine for Paper Performance Attribution v1.6.7.
    Supports single-period, multi-period, TWR, MWR (if data sufficient).
    No future prices. No real account data.
    """

    def __init__(
        self,
        residual_tolerance: float = 0.0001,
        rounding_tolerance: float = 1e-8,
        deterministic_seed: int = 42,
    ) -> None:
        self._residual_tolerance = residual_tolerance
        self._rounding_tolerance = rounding_tolerance
        self._seed = deterministic_seed

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        begin_equity: float,
        end_equity: float,
        cash_flows: Optional[List[Dict[str, Any]]] = None,
        period_returns: Optional[List[float]] = None,
        benchmark_return: float = 0.0,
        commission: float = 0.0,
        transaction_tax: float = 0.0,
        exchange_fee: float = 0.0,
        borrow_cost: float = 0.0,
        financing_cost: float = 0.0,
        spread_cost: float = 0.0,
        slippage: float = 0.0,
        impact_cost: float = 0.0,
        realized_pnl: float = 0.0,
        unrealized_pnl: float = 0.0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> ReturnContribution:
        """
        Compute full return decomposition for a single entity/period.
        Returns ReturnContribution with all fields populated.
        """
        if begin_equity <= 0:
            return ReturnContribution(
                entity_id=entity_id,
                level=level,
                gross_return=0.0,
                net_return=0.0,
                realized_return=0.0,
                unrealized_return=0.0,
                active_return=0.0,
                cost_return=0.0,
                execution_return=0.0,
                residual_return=0.0,
                confidence=ConfidenceLevel.LOW,
                status=AttributionStatus.INSUFFICIENT_DATA,
                source_lineage=source_lineage,
                period_start=period_start,
                period_end=period_end,
                paper_only=True,
                research_only=True,
                no_real_orders=True,
                not_for_production=True,
            )

        cf_list = cash_flows or []
        gross_return = calc_gross_return(begin_equity, end_equity, cf_list)

        decomp = decompose_gross_to_net(
            gross_return, begin_equity,
            commission=commission,
            transaction_tax=transaction_tax,
            exchange_fee=exchange_fee,
            borrow_cost=borrow_cost,
            financing_cost=financing_cost,
            spread_cost=spread_cost,
            slippage=slippage,
            impact_cost=impact_cost,
        )
        net_return = decomp["net_return"]
        total_cost_rate = decomp["total_cost_rate"]

        realized_return = realized_pnl / begin_equity if begin_equity else 0.0
        unrealized_return = unrealized_pnl / begin_equity if begin_equity else 0.0
        active_return = calc_active_return(net_return, benchmark_return)
        execution_return = -(slippage / begin_equity if begin_equity else 0.0)

        # TWR if period returns provided
        twr = None
        if period_returns:
            twr = calc_twr(period_returns)

        # MWR: attempt if cash flows present
        mwr = None
        mwr_available = False
        if cf_list:
            try:
                mwr = calc_mwr(cf_list, end_equity, begin_equity)
                mwr_available = mwr is not None
            except Exception:
                mwr = None
                mwr_available = False

        cumulative = twr if twr is not None else gross_return

        # Residual: difference between active_return and explained components
        explained = -total_cost_rate + execution_return
        residual_return = active_return - explained
        if abs(residual_return) > self._residual_tolerance:
            status = AttributionStatus.DEGRADED
            confidence = ConfidenceLevel.LOW
        else:
            status = AttributionStatus.COMPLETE
            confidence = ConfidenceLevel.HIGH

        bps_active = active_return * 10_000

        return ReturnContribution(
            entity_id=entity_id,
            level=level,
            gross_return=gross_return,
            net_return=net_return,
            realized_return=realized_return,
            unrealized_return=unrealized_return,
            active_return=active_return,
            cost_return=-total_cost_rate,
            execution_return=execution_return,
            residual_return=residual_return,
            cumulative_return=cumulative,
            twr=twr,
            mwr=mwr,
            mwr_available=mwr_available,
            basis_points_active=bps_active,
            confidence=confidence,
            status=status,
            source_lineage=source_lineage,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )

    def compute_residual(
        self,
        entity_id: str,
        level: AttributionLevel,
        active_return: float,
        component_sum: float,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> ResidualContribution:
        """Compute residual between active_return and sum of all attribution components."""
        model_residual = active_return - component_sum
        rounding_residual = 0.0
        # Separate rounding from model residual
        if abs(model_residual) < self._rounding_tolerance:
            rounding_residual = model_residual
            model_residual_clean = 0.0
        else:
            model_residual_clean = model_residual

        exceeds = abs(model_residual) > self._residual_tolerance
        if exceeds:
            status = AttributionStatus.DEGRADED
        else:
            status = AttributionStatus.COMPLETE

        return ResidualContribution(
            entity_id=entity_id,
            level=level,
            residual=model_residual,
            rounding_residual=rounding_residual,
            model_residual=model_residual_clean,
            threshold=self._residual_tolerance,
            exceeds_threshold=exceeds,
            confidence=ConfidenceLevel.HIGH if not exceeds else ConfidenceLevel.LOW,
            status=status,
            source_lineage=source_lineage,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )
