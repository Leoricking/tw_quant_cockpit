"""
paper_trading/strategy/explain_v162.py — Decision explainer for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from paper_trading.strategy.models_v162 import (
    DecisionContext,
    DecisionResult,
    LineageRecord,
    PaperSignal,
)

logger = logging.getLogger(__name__)


class DecisionExplainer:
    """
    Generates human-readable explanations of paper strategy decisions.

    Explains:
      - Why a signal was rejected or approved
      - Which pipeline step caused a REJECT
      - What conditions must change for approval
      - Lineage tracing from trigger to proposal

    [!] Research-only explanations. Not financial advice.
    """

    def explain_decision(
        self,
        decision: DecisionResult,
        context: Optional[DecisionContext] = None,
        signal: Optional[PaperSignal] = None,
    ) -> Dict[str, Any]:
        """
        Generate an explanation for a decision.
        Returns a structured dict with narrative and step breakdown.
        """
        pipeline_log = []
        if context is not None:
            pipeline_log = context.pipeline_log

        narrative = self._build_narrative(decision, context, signal)
        conditions = self._build_conditions(decision, context)

        return {
            "decision_id": decision.decision_id,
            "ticker": decision.ticker,
            "strategy_id": decision.strategy_id,
            "outcome": decision.outcome,
            "reason": decision.reason,
            "pipeline_steps_completed": decision.pipeline_steps_completed,
            "pipeline_log": pipeline_log,
            "narrative": narrative,
            "conditions_for_approval": conditions,
            "decided_at": decision.decided_at,
            "paper_only": True,
            "research_only": True,
            "not_investment_advice": True,
        }

    def _build_narrative(
        self,
        decision: DecisionResult,
        context: Optional[DecisionContext],
        signal: Optional[PaperSignal],
    ) -> str:
        lines: List[str] = [
            f"[PAPER SIMULATION] Decision for {decision.ticker}: {decision.outcome}",
            f"Reason: {decision.reason}",
            f"Pipeline completed {decision.pipeline_steps_completed} of 16 steps.",
        ]
        if signal:
            lines.append(
                f"Signal: {signal.signal_type} (confidence={signal.confidence:.2f}, "
                f"strength={signal.strength})"
            )
        if context:
            lines.append(
                f"Context: market_open={context.market_open}, "
                f"data_quality_ok={context.data_quality_ok}, "
                f"pit_valid={context.pit_valid}"
            )
        lines.append("[!] NOT INVESTMENT ADVICE. RESEARCH ONLY.")
        return "\n".join(lines)

    def _build_conditions(
        self,
        decision: DecisionResult,
        context: Optional[DecisionContext],
    ) -> List[str]:
        """List what would need to change for this decision to result in APPROVED."""
        from paper_trading.strategy.enums_v162 import DecisionOutcome
        outcome = decision.outcome
        conditions: List[str] = []

        if outcome == DecisionOutcome.APPROVED.value:
            conditions.append("Decision already APPROVED (paper simulation)")
            return conditions

        if outcome == DecisionOutcome.DUPLICATE.value:
            conditions.append("Wait for deduplication window to expire")
        elif outcome == DecisionOutcome.COOLDOWN.value:
            conditions.append("Wait for cooldown period to expire")
        elif outcome == DecisionOutcome.RATE_LIMITED.value:
            conditions.append("Wait for rate-limit window to reset (60s rolling)")
        elif outcome == DecisionOutcome.DATA_STALE.value:
            conditions.append("Ensure data quality check passes")
            conditions.append("Ensure point-in-time data is valid")
        elif outcome == DecisionOutcome.INELIGIBLE.value:
            conditions.append(f"Ticker {decision.ticker} must be eligible")
        elif outcome == DecisionOutcome.SIZING_ZERO.value:
            conditions.append("Position sizing must return a positive size")
        elif outcome == DecisionOutcome.RISK_BLOCKED.value:
            conditions.append("Risk controls must not block (drawdown/position limits)")
        elif outcome == DecisionOutcome.CONFLICT.value:
            conditions.append("Conflicting signals must be resolved first")
        elif outcome == DecisionOutcome.DEFERRED.value:
            conditions.append("Explicit manual approval required (MANUAL_REQUIRED mode)")
            conditions.append("Or switch to AUTO_PAPER_ONLY approval mode")
        elif outcome == DecisionOutcome.BLOCKED.value:
            conditions.append("Strategy must be in RUNNING status")
            conditions.append("No permanently-forbidden signal types")

        if context and not context.market_open:
            conditions.append("Market is currently closed — signals may proceed in paper simulation")

        return conditions

    def explain_lineage(self, lineage: LineageRecord) -> Dict[str, Any]:
        """Explain a lineage record in human-readable form."""
        return {
            "lineage_id": lineage.lineage_id,
            "ticker": lineage.ticker,
            "signal_type": lineage.signal_type,
            "trigger_type": lineage.trigger_type,
            "outcome": lineage.outcome,
            "pipeline_steps": lineage.pipeline_steps,
            "reproducibility_hash": lineage.reproducibility_hash,
            "has_proposal": bool(lineage.proposal_id),
            "recorded_at": lineage.recorded_at,
            "narrative": (
                f"Signal ({lineage.signal_type}) for {lineage.ticker} "
                f"triggered by {lineage.trigger_type} → {lineage.outcome} "
                f"after {lineage.pipeline_steps} pipeline steps. "
                f"[PAPER ONLY. NOT INVESTMENT ADVICE.]"
            ),
            "paper_only": True,
            "research_only": True,
        }
