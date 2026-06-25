"""paper_trading/session_replay_v160.py — Paper Session Replay v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
Same input → same result. Deterministic. No future events. Sequence and hash validated.
Replay cannot be labeled as live.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .enums_v160 import DataMode
from .event_v160 import PaperEvent
from .event_journal_v160 import PaperEventJournal


@dataclass
class ReplayResult:
    session_id: str
    events_replayed: int
    sequence_valid: bool
    hash_chain_valid: bool
    reproducible: bool
    ledger_hash: str = ""
    snapshot_hash: str = ""
    errors: List[str] = field(default_factory=list)
    replay_mode: str = "REPLAY"
    paper_only: bool = True
    not_live: bool = True


class PaperSessionReplay:
    """
    Replays a paper session from stored events.
    Deterministic: same events → same result.
    Does not use future events. Cannot be labeled as live.
    """

    def replay(
        self,
        session_id: str,
        events: List[PaperEvent],
        expected_ledger_hash: Optional[str] = None,
        expected_snapshot_hash: Optional[str] = None,
    ) -> ReplayResult:
        errors: List[str] = []

        # Validate sequences
        for i, event in enumerate(events):
            if event.sequence != i:
                errors.append(f"sequence mismatch at index {i}: expected {i}, got {event.sequence}")

        # Rebuild journal and verify hash chain
        journal = PaperEventJournal()
        for event in events:
            try:
                journal.append(event)
            except ValueError as exc:
                errors.append(str(exc))
                break

        hash_ok = journal.verify_chain()
        seq_ok = len(errors) == 0
        final_hash = journal.last_hash()

        ledger_ok = True
        if expected_ledger_hash and expected_ledger_hash != final_hash:
            ledger_ok = False
            errors.append(f"ledger hash mismatch: expected {expected_ledger_hash}, got {final_hash}")

        return ReplayResult(
            session_id=session_id,
            events_replayed=journal.count(),
            sequence_valid=seq_ok,
            hash_chain_valid=hash_ok,
            reproducible=seq_ok and hash_ok and ledger_ok,
            ledger_hash=final_hash,
            errors=errors,
            replay_mode="REPLAY",
            paper_only=True,
            not_live=True,
        )
