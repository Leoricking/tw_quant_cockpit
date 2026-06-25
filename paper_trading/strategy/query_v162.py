"""
paper_trading/strategy/query_v162.py — Query service for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from paper_trading.strategy.enums_v162 import DecisionOutcome, ProposalStatus
from paper_trading.strategy.store_v162 import PaperStrategyStore

logger = logging.getLogger(__name__)


class PaperStrategyQueryService:
    """
    Read-only query layer for the paper strategy store.

    Provides filtered queries, aggregations, and summaries.
    [!] All data is research-only paper simulation data.
    """

    def __init__(self, store: PaperStrategyStore) -> None:
        self._store = store

    # ------------------------------------------------------------------
    # Signal queries
    # ------------------------------------------------------------------

    def signals_for_strategy(self, strategy_id: str) -> List[Dict]:
        sigs = self._store.list_signals(strategy_id=strategy_id)
        return [self._signal_summary(s) for s in sigs]

    def signals_for_ticker(self, ticker: str) -> List[Dict]:
        sigs = self._store.list_signals()
        return [self._signal_summary(s) for s in sigs if s.ticker == ticker]

    def signal_count(self, strategy_id: Optional[str] = None) -> int:
        if strategy_id:
            return len(self._store.list_signals(strategy_id=strategy_id))
        return self._store.signal_count()

    # ------------------------------------------------------------------
    # Decision queries
    # ------------------------------------------------------------------

    def decisions_for_strategy(self, strategy_id: str) -> List[Dict]:
        decs = self._store.list_decisions(strategy_id=strategy_id)
        return [self._decision_summary(d) for d in decs]

    def approved_decisions(self, strategy_id: Optional[str] = None) -> List[Dict]:
        decs = self._store.list_decisions(
            strategy_id=strategy_id,
            outcome=DecisionOutcome.APPROVED.value,
        )
        return [self._decision_summary(d) for d in decs]

    def rejected_decisions(self, strategy_id: Optional[str] = None) -> List[Dict]:
        decs = self._store.list_decisions(strategy_id=strategy_id)
        non_approved = [d for d in decs if d.outcome != DecisionOutcome.APPROVED.value]
        return [self._decision_summary(d) for d in non_approved]

    def outcome_distribution(self, strategy_id: Optional[str] = None) -> Dict[str, int]:
        decs = self._store.list_decisions(strategy_id=strategy_id)
        dist: Dict[str, int] = {}
        for d in decs:
            dist[d.outcome] = dist.get(d.outcome, 0) + 1
        return dist

    # ------------------------------------------------------------------
    # Proposal queries
    # ------------------------------------------------------------------

    def proposals_for_strategy(self, strategy_id: str) -> List[Dict]:
        props = self._store.list_proposals(strategy_id=strategy_id)
        return [self._proposal_summary(p) for p in props]

    def pending_proposals(self, strategy_id: Optional[str] = None) -> List[Dict]:
        props = self._store.list_proposals(
            strategy_id=strategy_id,
            status=ProposalStatus.PENDING.value,
        )
        return [self._proposal_summary(p) for p in props]

    def accepted_proposals(self, strategy_id: Optional[str] = None) -> List[Dict]:
        props = self._store.list_proposals(
            strategy_id=strategy_id,
            status=ProposalStatus.ACCEPTED.value,
        )
        return [self._proposal_summary(p) for p in props]

    def proposal_count_by_status(self, strategy_id: Optional[str] = None) -> Dict[str, int]:
        props = self._store.list_proposals(strategy_id=strategy_id)
        dist: Dict[str, int] = {}
        for p in props:
            dist[p.status] = dist.get(p.status, 0) + 1
        return dist

    # ------------------------------------------------------------------
    # Lineage queries
    # ------------------------------------------------------------------

    def lineage_for_ticker(self, ticker: str) -> List[Dict]:
        records = self._store.list_lineage(ticker=ticker)
        return [
            {
                "lineage_id": r.lineage_id,
                "signal_type": r.signal_type,
                "outcome": r.outcome,
                "trigger_type": r.trigger_type,
                "pipeline_steps": r.pipeline_steps,
                "recorded_at": r.recorded_at,
                "reproducibility_hash": r.reproducibility_hash[:8],
            }
            for r in records
        ]

    # ------------------------------------------------------------------
    # Aggregate summary
    # ------------------------------------------------------------------

    def full_summary(self) -> Dict[str, Any]:
        return {
            "store_summary": self._store.summary(),
            "outcome_distribution": self.outcome_distribution(),
            "proposal_status_distribution": self.proposal_count_by_status(),
            "paper_only": True,
            "research_only": True,
            "not_investment_advice": True,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _signal_summary(s: Any) -> Dict:
        return {
            "signal_id": s.signal_id,
            "strategy_id": s.strategy_id,
            "ticker": s.ticker,
            "signal_type": s.signal_type,
            "confidence": s.confidence,
            "strength": s.strength,
            "generated_at": s.generated_at,
            "paper_only": s.paper_only,
        }

    @staticmethod
    def _decision_summary(d: Any) -> Dict:
        return {
            "decision_id": d.decision_id,
            "strategy_id": d.strategy_id,
            "ticker": d.ticker,
            "outcome": d.outcome,
            "reason": d.reason,
            "pipeline_steps_completed": d.pipeline_steps_completed,
            "decided_at": d.decided_at,
            "paper_only": d.paper_only,
        }

    @staticmethod
    def _proposal_summary(p: Any) -> Dict:
        return {
            "proposal_id": p.proposal_id,
            "strategy_id": p.strategy_id,
            "ticker": p.ticker,
            "signal_type": p.signal_type,
            "proposed_size": p.proposed_size,
            "status": p.status,
            "created_at": p.created_at,
            "paper_only": p.paper_only,
        }
