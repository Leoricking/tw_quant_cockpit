"""
paper_trading/strategy/lineage_v162.py — Lineage tracking for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import hashlib
import json
import logging
import threading
from typing import Any, Dict, List, Optional

from paper_trading.strategy.models_v162 import (
    DecisionResult,
    LineageRecord,
    PaperOrderProposal,
    PaperSignal,
    _new_id,
    _now_iso,
)

logger = logging.getLogger(__name__)


def _compute_reproducibility_hash(
    signal: PaperSignal,
    decision: DecisionResult,
) -> str:
    """
    Compute a deterministic hash for a signal→decision chain.
    Used for reproducibility verification.
    """
    payload = json.dumps(
        {
            "signal_id": signal.signal_id,
            "strategy_id": signal.strategy_id,
            "ticker": signal.ticker,
            "signal_type": signal.signal_type,
            "confidence": signal.confidence,
            "strength": signal.strength,
            "normalized_value": signal.normalized_value,
            "outcome": decision.outcome,
            "pipeline_steps": decision.pipeline_steps_completed,
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:32]


class LineageTracker:
    """
    Records complete lineage for every paper proposal:
    trigger → signal → decision → proposal chain.

    Used for audit, reproducibility, and replay verification.
    Thread-safe.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: List[LineageRecord] = []

    def record(
        self,
        signal: PaperSignal,
        decision: DecisionResult,
        proposal: Optional[PaperOrderProposal] = None,
    ) -> LineageRecord:
        """Record a lineage entry. Returns the LineageRecord."""
        hash_val = _compute_reproducibility_hash(signal, decision)
        rec = LineageRecord(
            lineage_id=_new_id(),
            proposal_id=proposal.proposal_id if proposal else "",
            decision_id=decision.decision_id,
            signal_id=signal.signal_id,
            strategy_id=signal.strategy_id,
            trigger_type=signal.trigger_type,
            ticker=signal.ticker,
            signal_type=signal.signal_type,
            recorded_at=_now_iso(),
            reproducibility_hash=hash_val,
            pipeline_steps=decision.pipeline_steps_completed,
            outcome=decision.outcome,
            extra={
                "confidence": signal.confidence,
                "strength": signal.strength,
                "normalized_value": signal.normalized_value,
                "dedup_key": signal.dedup_key,
            },
        )
        with self._lock:
            self._records.append(rec)

        logger.debug(
            "[v1.6.2][lineage] Recorded %s → %s → %s (outcome=%s hash=%s)",
            signal.signal_id[:8],
            decision.decision_id[:8],
            rec.proposal_id[:8] if rec.proposal_id else "none",
            decision.outcome,
            hash_val[:8],
        )
        return rec

    def find_by_proposal(self, proposal_id: str) -> Optional[LineageRecord]:
        with self._lock:
            for rec in self._records:
                if rec.proposal_id == proposal_id:
                    return rec
        return None

    def find_by_signal(self, signal_id: str) -> List[LineageRecord]:
        with self._lock:
            return [r for r in self._records if r.signal_id == signal_id]

    def find_by_ticker(self, ticker: str) -> List[LineageRecord]:
        with self._lock:
            return [r for r in self._records if r.ticker == ticker]

    def all_records(self) -> List[LineageRecord]:
        with self._lock:
            return list(self._records)

    def count(self) -> int:
        with self._lock:
            return len(self._records)

    def summary(self) -> Dict[str, Any]:
        with self._lock:
            outcomes: Dict[str, int] = {}
            for r in self._records:
                outcomes[r.outcome] = outcomes.get(r.outcome, 0) + 1
            return {
                "total_records": len(self._records),
                "outcome_distribution": outcomes,
                "paper_only": True,
                "research_only": True,
            }

    def verify_reproducibility(self, signal: PaperSignal, decision: DecisionResult) -> bool:
        """
        Verify that a signal+decision pair produces the same hash as a previously
        recorded lineage entry with the same signal_id.
        """
        expected_hash = _compute_reproducibility_hash(signal, decision)
        with self._lock:
            for rec in self._records:
                if rec.signal_id == signal.signal_id:
                    return rec.reproducibility_hash == expected_hash
        # No prior record — cannot verify
        return False
