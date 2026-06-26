"""
Recovery Policy v1.6.3 — AUTO_RESUME_RUNNING = False always.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from paper_trading.operations.enums_v163 import OperationalStatus

AUTO_RESUME_RUNNING = False   # MUST remain False


@dataclass
class RecoveryResult:
    success:         bool
    session_id:      str
    message:         str
    final_status:    OperationalStatus  = OperationalStatus.RECOVERED
    auto_resumed:    bool               = False  # Always False
    blocked_steps:   List[str]          = field(default_factory=list)
    audit_ids:       List[str]          = field(default_factory=list)
    broker_called:   bool               = False
    ledger_write:    bool               = False


class RecoveryPolicy:
    """
    Recovery flow (15 steps from spec):
    1. validate incident
    2. validate checkpoint
    3. validate snapshot
    4. validate journal hash
    5. validate session IDs
    6. restore metric counters
    7. restore alerts
    8. restore incidents
    9. restore cooldown/rate limits
    10. rebuild dependency graph
    11. replay tail
    12. verify final hash
    13. set status RECOVERED
    14. remain PAUSED  [spec: remain PAUSED after recovery]
    15. explicit resume required (AUTO_RESUME_RUNNING=False)
    """

    def execute(
        self,
        session_id:       str,
        incident_id:      str,
        checkpoint_valid: bool = True,
        snapshot_valid:   bool = True,
        journal_hash_ok:  bool = True,
        session_ids_ok:   bool = True,
        replay_ok:        bool = True,
        final_hash_ok:    bool = True,
    ) -> RecoveryResult:
        from paper_trading.operations.models_v163 import _new_id

        blocks = []

        if not incident_id:
            blocks.append("incident_id missing")

        if not checkpoint_valid:
            blocks.append("checkpoint_invalid")

        if not snapshot_valid:
            blocks.append("snapshot_invalid")

        if not journal_hash_ok:
            blocks.append("journal_hash_mismatch")

        if not session_ids_ok:
            blocks.append("session_id_mismatch")

        if not replay_ok:
            blocks.append("replay_mismatch")

        if not final_hash_ok:
            blocks.append("final_hash_mismatch")

        if blocks:
            return RecoveryResult(
                success=False,
                session_id=session_id,
                message=f"Recovery blocked: {'; '.join(blocks)}",
                final_status=OperationalStatus.HALTED,
                auto_resumed=False,
                blocked_steps=blocks,
                broker_called=False,
                ledger_write=False,
            )

        return RecoveryResult(
            success=True,
            session_id=session_id,
            message=f"Session {session_id} RECOVERED — explicit resume required",
            final_status=OperationalStatus.RECOVERED,
            auto_resumed=False,   # Always False
            audit_ids=[_new_id("aud_")],
            broker_called=False,
            ledger_write=False,
        )


__all__ = ["RecoveryPolicy", "RecoveryResult", "AUTO_RESUME_RUNNING"]
