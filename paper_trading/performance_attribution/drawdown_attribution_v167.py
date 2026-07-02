"""
paper_trading/performance_attribution/drawdown_attribution_v167.py
Drawdown attribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] peak/trough/recovery traceable. residual visible. no_recovery clearly marked.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionLevel, AttributionStatus, ConfidenceLevel
from .models_v167 import DrawdownContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


def find_max_drawdown_period(equity_curve: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Find max drawdown peak, trough, and recovery from equity curve.
    equity_curve: [{date: str, value: float}, ...]
    Returns dict with peak/trough/recovery info.
    """
    if not equity_curve:
        return {
            "max_drawdown": 0.0, "peak_date": "", "trough_date": "",
            "recovery_date": None, "peak_to_trough_days": 0,
            "recovery_days": None, "no_recovery": True,
        }

    peak_val = equity_curve[0]["value"]
    peak_date = equity_curve[0]["date"]
    trough_val = peak_val
    trough_date = peak_date
    max_dd = 0.0
    best_peak_val = peak_val
    best_peak_date = peak_date
    best_trough_val = peak_val
    best_trough_date = peak_date
    recovery_date: Optional[str] = None

    for i, point in enumerate(equity_curve):
        val = point["value"]
        dt = point["date"]
        if val > peak_val:
            peak_val = val
            peak_date = dt
            trough_val = val
            trough_date = dt
        else:
            dd = (val - peak_val) / peak_val if peak_val != 0 else 0.0
            if dd < max_dd:
                max_dd = dd
                best_peak_val = peak_val
                best_peak_date = peak_date
                best_trough_val = val
                best_trough_date = dt
                recovery_date = None  # reset recovery

        # Check recovery (value exceeds peak after trough)
        if best_trough_date and val >= best_peak_val and dt > best_trough_date and recovery_date is None:
            recovery_date = dt

    # Days between peak and trough (approximation from index difference)
    dates = [p["date"] for p in equity_curve]
    peak_idx = dates.index(best_peak_date) if best_peak_date in dates else 0
    trough_idx = dates.index(best_trough_date) if best_trough_date in dates else 0
    p2t_days = max(0, trough_idx - peak_idx)

    recovery_days: Optional[int] = None
    if recovery_date and recovery_date in dates:
        rec_idx = dates.index(recovery_date)
        recovery_days = max(0, rec_idx - trough_idx)

    no_recovery = recovery_date is None

    return {
        "max_drawdown": abs(max_dd),
        "peak_date": best_peak_date,
        "trough_date": best_trough_date,
        "recovery_date": recovery_date,
        "peak_to_trough_days": p2t_days,
        "recovery_days": recovery_days,
        "no_recovery": no_recovery,
    }


class DrawdownAttributionEngine:
    """Drawdown attribution: decomposes sources of drawdown."""

    def __init__(self, residual_tolerance: float = 0.0001) -> None:
        self._tolerance = residual_tolerance

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        equity_curve: List[Dict[str, Any]],
        symbol_contributions: Optional[Dict[str, float]] = None,
        strategy_contributions: Optional[Dict[str, float]] = None,
        session_contributions: Optional[Dict[str, float]] = None,
        allocation_contrib: float = 0.0,
        concentration_contrib: float = 0.0,
        leverage_contrib: float = 0.0,
        execution_contrib: float = 0.0,
        cost_contrib: float = 0.0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> DrawdownContribution:
        """Compute drawdown attribution."""
        dd_info = find_max_drawdown_period(equity_curve)
        max_dd = dd_info["max_drawdown"]

        sym_contrib = sum(symbol_contributions.values()) if symbol_contributions else 0.0
        strat_contrib = sum(strategy_contributions.values()) if strategy_contributions else 0.0
        sess_contrib = sum(session_contributions.values()) if session_contributions else 0.0

        explained = (sym_contrib + strat_contrib + sess_contrib + allocation_contrib
                     + concentration_contrib + leverage_contrib + execution_contrib
                     + cost_contrib)
        residual = max_dd - explained

        if abs(residual) > self._tolerance:
            reconciled = False
            confidence = ConfidenceLevel.LOW
            status = AttributionStatus.DEGRADED
        else:
            reconciled = True
            confidence = ConfidenceLevel.HIGH
            status = AttributionStatus.COMPLETE

        incomplete_period = dd_info["no_recovery"] and bool(equity_curve)

        return DrawdownContribution(
            entity_id=entity_id,
            level=level,
            max_drawdown=max_dd,
            peak_timestamp=dd_info["peak_date"],
            trough_timestamp=dd_info["trough_date"],
            recovery_timestamp=dd_info["recovery_date"],
            peak_to_trough_duration=dd_info["peak_to_trough_days"],
            recovery_duration=dd_info["recovery_days"],
            no_recovery=dd_info["no_recovery"],
            symbol_contribution=sym_contrib,
            strategy_contribution=strat_contrib,
            session_contribution=sess_contrib,
            allocation_contribution=allocation_contrib,
            concentration_contribution=concentration_contrib,
            leverage_contribution=leverage_contrib,
            execution_contribution=execution_contrib,
            cost_contribution=cost_contrib,
            residual_contribution=residual,
            reconciled=reconciled,
            incomplete_period=incomplete_period,
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
