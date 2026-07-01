"""
paper_trading/multi_session/explain_v166.py — Coordination Explainer v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List
from paper_trading.multi_session.models_v166 import CoordinationDecision, SessionConflict, CoordinationResult

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True


class CoordinationExplainer:
    """Explains coordination decisions and outcomes in human-readable form."""

    def explain_decision(self, decision: CoordinationDecision) -> str:
        return (
            f"Decision [{decision.decision_id[:8]}]: {decision.decision_type.value} "
            f"for sessions {decision.session_ids} — {decision.reason}. "
            f"Action: {decision.selected_action}. "
            f"Safety blocks: {decision.safety_blocks or 'none'}."
        )

    def explain_conflict(self, conflict: SessionConflict) -> str:
        return (
            f"Conflict [{conflict.conflict_id[:8]}]: {conflict.conflict_type.value} "
            f"({conflict.severity.value}) affecting sessions {conflict.session_ids}. "
            f"Blocking: {conflict.blocking}. "
            f"Resolution options: {conflict.resolution_options}."
        )

    def explain_result(self, result: CoordinationResult) -> str:
        return (
            f"Coordination [{result.coordination_id[:8]}]: "
            f"admitted={len(result.sessions_admitted)}, "
            f"blocked={len(result.sessions_blocked)}, "
            f"conflicts={result.conflicts_detected} ({result.conflicts_unresolved} unresolved). "
            f"Risk={result.risk_result.value}, Capital={result.capital_result.value}. "
            f"Warnings: {len(result.warnings)}."
        )

    def explain_all(self, results: List[CoordinationResult]) -> List[str]:
        return [self.explain_result(r) for r in results]
