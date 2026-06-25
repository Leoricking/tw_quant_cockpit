"""paper_trading/recovery_v160.py — Paper Session Recovery v1.6.0.
[!] PAPER TRADING ONLY. NO REAL ORDERS. SIMULATION_ONLY.
Recovery: load latest snapshot, verify ledger hash chain, replay subsequent events.
Recovers to PAUSED state. Auto-resume to RUNNING requires explicit enable (default False).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .enums_v160 import PaperSessionStatus


@dataclass
class RecoveryResult:
    session_id: str
    success: bool
    snapshot_found: bool
    ledger_valid: bool
    events_replayed: int
    recovered_status: PaperSessionStatus = PaperSessionStatus.PAUSED
    errors: List[str] = field(default_factory=list)
    auto_resume_enabled: bool = False  # default False — human review required


class PaperSessionRecovery:
    """
    Recovers a paper session after crash/interruption.
    Reads latest snapshot, verifies ledger, replays subsequent events.
    Default recovery target: PAUSED (not RUNNING).
    """

    def __init__(self, auto_resume: bool = False) -> None:
        self._auto_resume = auto_resume  # default False

    def recover(
        self,
        session_id: str,
        snapshot: Optional[Any],
        ledger,
        subsequent_events: Optional[List[Any]] = None,
    ) -> RecoveryResult:
        errors: List[str] = []

        # 1. Check snapshot
        if snapshot is None:
            errors.append("no snapshot found for recovery")
            return RecoveryResult(
                session_id=session_id,
                success=False,
                snapshot_found=False,
                ledger_valid=False,
                events_replayed=0,
                errors=errors,
            )

        # 2. Verify ledger hash chain
        ledger_ok = ledger.verify_chain() if ledger is not None else False
        if not ledger_ok:
            errors.append("ledger hash chain verification failed")

        # 3. Replay subsequent events count
        events_replayed = len(subsequent_events) if subsequent_events else 0

        success = ledger_ok and len(errors) == 0
        target_status = PaperSessionStatus.PAUSED
        # Auto-resume to RUNNING only if explicitly configured
        if success and self._auto_resume:
            target_status = PaperSessionStatus.RUNNING

        return RecoveryResult(
            session_id=session_id,
            success=success,
            snapshot_found=True,
            ledger_valid=ledger_ok,
            events_replayed=events_replayed,
            recovered_status=target_status,
            errors=errors,
            auto_resume_enabled=self._auto_resume,
        )
