"""
paper_trading/analytics/session_summary_v164.py — Session Summary Builder v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS. NO BROKER.
Point-in-time safe. Missing data stays missing — never defaults to 0.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional

from paper_trading.analytics.validation_v164 import require_pit, require_not_missing

NO_REAL_ORDERS = True
NO_BROKER = True
PAPER_ONLY = True


@dataclass
class SessionSummary:
    """
    Unified session summary integrating all session lifecycle data.
    point-in-time safe: all timestamps <= as_of.
    Missing fields remain None — never defaulted to 0 or healthy.
    """
    session_id: str
    session_type: Optional[str] = None
    as_of: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[Decimal] = None
    active_duration_seconds: Optional[Decimal] = None
    paused_duration_seconds: Optional[Decimal] = None
    halted_duration_seconds: Optional[Decimal] = None
    recovery_duration_seconds: Optional[Decimal] = None
    downtime_ratio: Optional[Decimal] = None
    lifecycle_transitions: List[Dict[str, Any]] = field(default_factory=list)

    # Market data
    market_data_update_count: Optional[int] = None
    market_data_stale_count: Optional[int] = None
    market_data_missing_intervals: Optional[int] = None
    market_data_quality_score: Optional[Decimal] = None

    # Strategy signals
    signals_generated: Optional[int] = None
    signals_accepted: Optional[int] = None
    signals_rejected: Optional[int] = None

    # Orders
    order_proposals: Optional[int] = None
    simulated_fills: Optional[int] = None
    rejected_orders: Optional[int] = None
    cancelled_orders: Optional[int] = None

    # PnL
    gross_pnl: Optional[Decimal] = None
    net_pnl: Optional[Decimal] = None
    realized_pnl: Optional[Decimal] = None
    unrealized_pnl: Optional[Decimal] = None
    max_drawdown: Optional[Decimal] = None

    # Costs
    transaction_cost: Optional[Decimal] = None
    slippage: Optional[Decimal] = None
    latency_p50_ms: Optional[Decimal] = None
    latency_p95_ms: Optional[Decimal] = None
    latency_p99_ms: Optional[Decimal] = None

    # Operations
    alerts_opened: Optional[int] = None
    alerts_resolved: Optional[int] = None
    incidents_opened: Optional[int] = None
    incidents_closed: Optional[int] = None
    recovery_count: Optional[int] = None
    checkpoint_restore_count: Optional[int] = None
    downtime_events: Optional[int] = None

    # Final status
    final_status: Optional[str] = None
    lineage_refs: List[str] = field(default_factory=list)

    paper_only: bool = True
    research_only: bool = True

    def validate_pit(self) -> None:
        """Validate all timestamps are <= as_of."""
        if self.as_of is None:
            return
        if self.start_time is not None:
            require_pit(self.start_time, self.as_of, "start_time")
        if self.end_time is not None:
            require_pit(self.end_time, self.as_of, "end_time")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "session_type": self.session_type,
            "as_of": self.as_of.isoformat() if self.as_of else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": str(self.duration_seconds) if self.duration_seconds is not None else None,
            "active_duration_seconds": str(self.active_duration_seconds) if self.active_duration_seconds is not None else None,
            "signals_generated": self.signals_generated,
            "signals_accepted": self.signals_accepted,
            "signals_rejected": self.signals_rejected,
            "gross_pnl": str(self.gross_pnl) if self.gross_pnl is not None else None,
            "net_pnl": str(self.net_pnl) if self.net_pnl is not None else None,
            "max_drawdown": str(self.max_drawdown) if self.max_drawdown is not None else None,
            "alerts_opened": self.alerts_opened,
            "incidents_opened": self.incidents_opened,
            "final_status": self.final_status,
            "paper_only": self.paper_only,
            "research_only": self.research_only,
        }


class SessionSummaryBuilder:
    """Builds a SessionSummary from raw session data. PIT-safe."""

    def build(
        self,
        session_id: str,
        as_of: datetime,
        raw_data: Optional[Dict[str, Any]] = None,
    ) -> SessionSummary:
        """Build summary. Missing fields remain None."""
        if raw_data is None:
            raw_data = {}

        summary = SessionSummary(
            session_id=session_id,
            as_of=as_of,
        )

        def _get(key: str):
            v = raw_data.get(key)
            return v

        summary.session_type = _get("session_type")
        summary.final_status = _get("final_status")
        summary.lineage_refs = _get("lineage_refs") or []

        # Times
        st = _get("start_time")
        et = _get("end_time")
        if isinstance(st, datetime):
            require_pit(st, as_of, "start_time")
            summary.start_time = st
        if isinstance(et, datetime):
            require_pit(et, as_of, "end_time")
            summary.end_time = et

        if summary.start_time and summary.end_time:
            delta = summary.end_time - summary.start_time
            summary.duration_seconds = Decimal(str(delta.total_seconds()))

        # Numeric fields — None if not present
        for attr, key in [
            ("gross_pnl", "gross_pnl"),
            ("net_pnl", "net_pnl"),
            ("max_drawdown", "max_drawdown"),
            ("transaction_cost", "transaction_cost"),
            ("slippage", "slippage"),
        ]:
            v = _get(key)
            if v is not None:
                setattr(summary, attr, Decimal(str(v)))

        for attr, key in [
            ("signals_generated", "signals_generated"),
            ("signals_accepted", "signals_accepted"),
            ("signals_rejected", "signals_rejected"),
            ("alerts_opened", "alerts_opened"),
            ("alerts_resolved", "alerts_resolved"),
            ("incidents_opened", "incidents_opened"),
            ("incidents_closed", "incidents_closed"),
        ]:
            v = _get(key)
            if v is not None:
                setattr(summary, attr, int(v))

        return summary


__all__ = ["SessionSummary", "SessionSummaryBuilder"]
