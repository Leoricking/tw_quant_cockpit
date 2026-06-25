"""
paper_trading/strategy/store_v162.py — In-memory + optional file store for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import json
import logging
import os
import threading
from typing import Any, Dict, List, Optional

from paper_trading.strategy.models_v162 import (
    DecisionResult,
    JournalEntry,
    LineageRecord,
    PaperOrderProposal,
    PaperSignal,
    StrategyCheckpoint,
    _now_iso,
)

logger = logging.getLogger(__name__)

_DEFAULT_STORE_DIR = "data/paper_strategy/store"


class PaperStrategyStore:
    """
    In-memory store for all paper strategy artifacts with optional JSON persistence.

    Stores:
      - Signals
      - Decisions
      - Proposals
      - Journal entries
      - Lineage records
      - Checkpoints

    Thread-safe. All data is research-only and paper-simulation data.
    [!] NOT a real trade ledger. NOT connected to any broker or account.
    """

    def __init__(
        self,
        store_dir: Optional[str] = None,
        persist: bool = False,
    ) -> None:
        self.store_dir = store_dir or _DEFAULT_STORE_DIR
        self.persist = persist
        self._lock = threading.Lock()

        self._signals: Dict[str, PaperSignal] = {}
        self._decisions: Dict[str, DecisionResult] = {}
        self._proposals: Dict[str, PaperOrderProposal] = {}
        self._journal_entries: List[JournalEntry] = []
        self._lineage_records: List[LineageRecord] = []
        self._checkpoints: Dict[str, StrategyCheckpoint] = {}

        if persist:
            os.makedirs(self.store_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    def save_signal(self, signal: PaperSignal) -> None:
        with self._lock:
            self._signals[signal.signal_id] = signal
        if self.persist:
            self._write_json("signals", signal.signal_id, self._signal_to_dict(signal))

    def get_signal(self, signal_id: str) -> Optional[PaperSignal]:
        with self._lock:
            return self._signals.get(signal_id)

    def list_signals(self, strategy_id: Optional[str] = None) -> List[PaperSignal]:
        with self._lock:
            sigs = list(self._signals.values())
        if strategy_id:
            sigs = [s for s in sigs if s.strategy_id == strategy_id]
        return sigs

    def signal_count(self) -> int:
        with self._lock:
            return len(self._signals)

    # ------------------------------------------------------------------
    # Decisions
    # ------------------------------------------------------------------

    def save_decision(self, decision: DecisionResult) -> None:
        with self._lock:
            self._decisions[decision.decision_id] = decision

    def get_decision(self, decision_id: str) -> Optional[DecisionResult]:
        with self._lock:
            return self._decisions.get(decision_id)

    def list_decisions(
        self,
        strategy_id: Optional[str] = None,
        outcome: Optional[str] = None,
    ) -> List[DecisionResult]:
        with self._lock:
            decs = list(self._decisions.values())
        if strategy_id:
            decs = [d for d in decs if d.strategy_id == strategy_id]
        if outcome:
            decs = [d for d in decs if d.outcome == outcome]
        return decs

    def decision_count(self) -> int:
        with self._lock:
            return len(self._decisions)

    # ------------------------------------------------------------------
    # Proposals
    # ------------------------------------------------------------------

    def save_proposal(self, proposal: PaperOrderProposal) -> None:
        with self._lock:
            self._proposals[proposal.proposal_id] = proposal

    def get_proposal(self, proposal_id: str) -> Optional[PaperOrderProposal]:
        with self._lock:
            return self._proposals.get(proposal_id)

    def list_proposals(
        self,
        strategy_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[PaperOrderProposal]:
        with self._lock:
            props = list(self._proposals.values())
        if strategy_id:
            props = [p for p in props if p.strategy_id == strategy_id]
        if status:
            props = [p for p in props if p.status == status]
        return props

    def proposal_count(self) -> int:
        with self._lock:
            return len(self._proposals)

    # ------------------------------------------------------------------
    # Journal
    # ------------------------------------------------------------------

    def save_journal_entry(self, entry: JournalEntry) -> None:
        with self._lock:
            self._journal_entries.append(entry)

    def list_journal_entries(
        self, strategy_id: Optional[str] = None, limit: int = 0
    ) -> List[JournalEntry]:
        with self._lock:
            entries = list(self._journal_entries)
        if strategy_id:
            entries = [e for e in entries if e.strategy_id == strategy_id]
        if limit > 0:
            entries = entries[-limit:]
        return entries

    # ------------------------------------------------------------------
    # Lineage
    # ------------------------------------------------------------------

    def save_lineage(self, record: LineageRecord) -> None:
        with self._lock:
            self._lineage_records.append(record)

    def list_lineage(
        self, strategy_id: Optional[str] = None, ticker: Optional[str] = None
    ) -> List[LineageRecord]:
        with self._lock:
            records = list(self._lineage_records)
        if strategy_id:
            records = [r for r in records if r.strategy_id == strategy_id]
        if ticker:
            records = [r for r in records if r.ticker == ticker]
        return records

    # ------------------------------------------------------------------
    # Checkpoints
    # ------------------------------------------------------------------

    def save_checkpoint(self, checkpoint: StrategyCheckpoint) -> None:
        with self._lock:
            self._checkpoints[checkpoint.checkpoint_id] = checkpoint

    def get_checkpoint(self, checkpoint_id: str) -> Optional[StrategyCheckpoint]:
        with self._lock:
            return self._checkpoints.get(checkpoint_id)

    def latest_checkpoint(self, strategy_id: str) -> Optional[StrategyCheckpoint]:
        with self._lock:
            cps = [c for c in self._checkpoints.values()
                   if c.strategy_id == strategy_id]
        if not cps:
            return None
        return sorted(cps, key=lambda c: c.saved_at)[-1]

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def _write_json(self, category: str, item_id: str, data: Dict[str, Any]) -> None:
        try:
            dir_path = os.path.join(self.store_dir, category)
            os.makedirs(dir_path, exist_ok=True)
            path = os.path.join(dir_path, f"{item_id[:16]}.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
        except OSError as exc:
            logger.warning("[v1.6.2][store] Write error: %s", exc)

    @staticmethod
    def _signal_to_dict(signal: PaperSignal) -> Dict[str, Any]:
        return {
            "signal_id": signal.signal_id,
            "strategy_id": signal.strategy_id,
            "ticker": signal.ticker,
            "signal_type": signal.signal_type,
            "confidence": signal.confidence,
            "paper_only": signal.paper_only,
            "research_only": signal.research_only,
            "not_a_real_order": signal.not_a_real_order,
            "generated_at": signal.generated_at,
        }

    def summary(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "signals": len(self._signals),
                "decisions": len(self._decisions),
                "proposals": len(self._proposals),
                "journal_entries": len(self._journal_entries),
                "lineage_records": len(self._lineage_records),
                "checkpoints": len(self._checkpoints),
                "persist": self.persist,
                "store_dir": self.store_dir,
                "paper_only": True,
                "research_only": True,
            }
