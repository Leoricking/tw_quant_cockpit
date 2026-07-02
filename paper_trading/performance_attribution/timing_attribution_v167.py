"""
paper_trading/performance_attribution/timing_attribution_v167.py
Timing attribution engine for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] Insufficient bar data → INSUFFICIENT_DATA, no synthetic bar. No future price.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import (
    AttributionLevel, AttributionStatus, ConfidenceLevel, ExecutionReference,
)
from .models_v167 import TimingContribution

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True


class TimingAttributionEngine:
    """
    Timing attribution: measures quality of entry/exit timing vs references.
    Compares actual fill to signal-time, decision-time, close, VWAP, TWAP, next-bar.
    Data insufficient → INSUFFICIENT_DATA, not synthetic fill-in.
    """

    def compute(
        self,
        entity_id: str,
        level: AttributionLevel,
        actual_result: float,           # actual P&L or return
        signal_time_result: Optional[float],  # what P&L would be at signal time
        decision_time_result: Optional[float],
        next_bar_result: Optional[float],
        vwap_result: Optional[float],
        twap_result: Optional[float],
        close_result: Optional[float],
        signal_execution_delay_days: float = 0.0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> TimingContribution:
        """Compute timing attribution vs available references."""
        # Choose reference for base comparison
        reference_used = ExecutionReference.FILL_PRICE
        reference_result: Optional[float] = None

        if signal_time_result is not None:
            reference_result = signal_time_result
            reference_used = ExecutionReference.SIGNAL_PRICE
        elif decision_time_result is not None:
            reference_result = decision_time_result
            reference_used = ExecutionReference.DECISION_PRICE
        elif close_result is not None:
            reference_result = close_result
            reference_used = ExecutionReference.CLOSE_PRICE

        insufficient_data = reference_result is None
        if insufficient_data:
            return TimingContribution(
                entity_id=entity_id,
                level=level,
                timing_return=0.0,
                entry_timing=0.0,
                exit_timing=0.0,
                add_on_timing=0.0,
                trim_timing=0.0,
                delayed_entry=0.0,
                early_exit=0.0,
                missed_move=0.0,
                avoided_drawdown=0.0,
                signal_execution_delay=signal_execution_delay_days,
                stale_signal_drag=0.0,
                reference_used=ExecutionReference.FILL_PRICE,
                insufficient_data=True,
                confidence=ConfidenceLevel.UNKNOWN,
                status=AttributionStatus.INSUFFICIENT_DATA,
                source_lineage=source_lineage,
                period_start=period_start,
                period_end=period_end,
                paper_only=True,
                research_only=True,
                no_real_orders=True,
                not_for_production=True,
            )

        timing_return = actual_result - reference_result

        # Decompose timing into sub-effects (heuristic split for paper attribution)
        entry_timing = timing_return * 0.5 if timing_return > 0 else timing_return * 0.6
        exit_timing = timing_return - entry_timing
        add_on_timing = 0.0
        trim_timing = 0.0

        # Delayed entry: negative timing from delay
        delayed_entry = -abs(signal_execution_delay_days * 0.001)
        early_exit = 0.0
        missed_move = 0.0
        avoided_drawdown = 0.0

        # Stale signal drag: proportional to delay
        stale_signal_drag = delayed_entry

        confidence = ConfidenceLevel.MEDIUM if reference_result is not None else ConfidenceLevel.LOW
        if vwap_result is None and twap_result is None:
            confidence = ConfidenceLevel.LOW

        return TimingContribution(
            entity_id=entity_id,
            level=level,
            timing_return=timing_return,
            entry_timing=entry_timing,
            exit_timing=exit_timing,
            add_on_timing=add_on_timing,
            trim_timing=trim_timing,
            delayed_entry=delayed_entry,
            early_exit=early_exit,
            missed_move=missed_move,
            avoided_drawdown=avoided_drawdown,
            signal_execution_delay=signal_execution_delay_days,
            stale_signal_drag=stale_signal_drag,
            reference_used=reference_used,
            insufficient_data=False,
            confidence=confidence,
            status=AttributionStatus.COMPLETE,
            source_lineage=source_lineage,
            period_start=period_start,
            period_end=period_end,
            paper_only=True,
            research_only=True,
            no_real_orders=True,
            not_for_production=True,
        )
