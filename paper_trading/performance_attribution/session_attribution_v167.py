"""
paper_trading/performance_attribution/session_attribution_v167.py
Session attribution for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] READ-ONLY attribution only. Must NOT start/stop/restart/modify session state or funds.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .enums_v167 import AttributionLevel, AttributionStatus, ConfidenceLevel, SessionState

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

# Safety: session attribution is strictly READ-ONLY
SESSION_ATTRIBUTION_READ_ONLY          = True
SESSION_ATTRIBUTION_NO_START           = True
SESSION_ATTRIBUTION_NO_STOP            = True
SESSION_ATTRIBUTION_NO_RESTART         = True
SESSION_ATTRIBUTION_NO_FAILOVER        = True
SESSION_ATTRIBUTION_NO_CAPITAL_CHANGE  = True
SESSION_ATTRIBUTION_NO_RISK_OVERRIDE   = True


class SessionAttributionEngine:
    """
    Session-level attribution: return, PnL, risk, cost, slippage, turnover per session.
    Integrates with v1.6.6 multi-session coordination (read-only).
    Must NOT modify session state, capital, risk limits, or coordination outcomes.
    """

    def compute(
        self,
        session_id: str,
        session_return: float,
        session_pnl: float,
        session_risk: float,
        session_cost: float,
        session_slippage: float,
        session_turnover: float,
        capital_usage: float,
        symbol_overlap: List[str],
        strategy_overlap: List[str],
        stale_session: bool = False,
        failed_session: bool = False,
        recovery_contribution: float = 0.0,
        leader_contribution: float = 0.0,
        follower_contribution: float = 0.0,
        conflict_contribution: float = 0.0,
        resource_contention_effect: float = 0.0,
        period_start: str = "",
        period_end: str = "",
        source_lineage: str = "",
    ) -> Dict[str, Any]:
        """Compute session attribution. Read-only. No state modification."""
        residual = session_return - (leader_contribution + follower_contribution
                                     + recovery_contribution + conflict_contribution)
        if stale_session:
            confidence = ConfidenceLevel.LOW
            status = AttributionStatus.DEGRADED
        elif failed_session:
            confidence = ConfidenceLevel.LOW
            status = AttributionStatus.DEGRADED
        else:
            confidence = ConfidenceLevel.HIGH
            status = AttributionStatus.COMPLETE

        return {
            "session_id": session_id,
            "session_return": session_return,
            "session_pnl": session_pnl,
            "session_risk": session_risk,
            "session_cost": session_cost,
            "session_slippage": session_slippage,
            "session_turnover": session_turnover,
            "capital_usage": capital_usage,
            "symbol_overlap": symbol_overlap,
            "strategy_overlap": strategy_overlap,
            "stale_session": stale_session,
            "failed_session": failed_session,
            "recovery_contribution": recovery_contribution,
            "leader_contribution": leader_contribution,
            "follower_contribution": follower_contribution,
            "conflict_contribution": conflict_contribution,
            "resource_contention_effect": resource_contention_effect,
            "session_residual": residual,
            "confidence": confidence.value,
            "status": status.value,
            "period_start": period_start,
            "period_end": period_end,
            "source_lineage": source_lineage,
            # Safety flags
            "read_only": True,
            "no_session_start": True,
            "no_session_stop": True,
            "no_capital_change": True,
            "no_risk_override": True,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_for_production": True,
        }

    def compare_sessions(
        self, session_results: List[Dict[str, Any]], dimension: str = "session_return"
    ) -> List[Dict[str, Any]]:
        """Rank sessions by dimension. Read-only."""
        return sorted(session_results, key=lambda r: r.get(dimension, 0.0), reverse=True)
