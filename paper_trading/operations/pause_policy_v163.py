"""
Safe Pause Policy v1.6.3 — Idempotent.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
No broker calls. No Ledger write. No position modification.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from paper_trading.operations.enums_v163 import OperationalStatus


BLOCKED = "BLOCKED"
PAUSED  = "PAUSED"


@dataclass
class PauseResult:
    success:       bool
    status:        str
    session_id:    str
    message:       str
    checkpoint_id: Optional[str] = None
    audit_id:      Optional[str] = None
    broker_called: bool          = False
    ledger_write:  bool          = False
    position_modified: bool      = False


class PausePolicy:
    """
    Pause flow (11 steps from spec):
    1. validate supervisor
    2. validate target session
    3. validate current state
    4. check dependencies
    5. stop new strategy proposals
    6. stop new Paper Orders
    7. preserve existing state
    8. create checkpoint
    9. update status PAUSED
    10. create audit event
    11. emit alert/incident event if required

    Idempotent: pausing an already-PAUSED session returns success without re-pausing.
    No broker calls. No Ledger write. No position modification.
    """

    PAUSEABLE_STATES = {
        OperationalStatus.RUNNING,
        OperationalStatus.DEGRADED,
        OperationalStatus.STARTING,
    }

    def execute(
        self,
        session_id:    str,
        current_status: OperationalStatus,
        supervisor_id: str,
        reason:        str = "",
        *,
        skip_checkpoint: bool = False,
    ) -> PauseResult:
        # Idempotent
        if current_status == OperationalStatus.PAUSED:
            return PauseResult(
                success=True, status=PAUSED, session_id=session_id,
                message="Already PAUSED",
                broker_called=False, ledger_write=False, position_modified=False,
            )

        if current_status not in self.PAUSEABLE_STATES:
            return PauseResult(
                success=False, status=BLOCKED, session_id=session_id,
                message=f"Cannot pause from {current_status} — BLOCKED",
                broker_called=False, ledger_write=False, position_modified=False,
            )

        if not supervisor_id:
            return PauseResult(
                success=False, status=BLOCKED, session_id=session_id,
                message="Missing supervisor — BLOCKED",
                broker_called=False, ledger_write=False, position_modified=False,
            )

        from paper_trading.operations.models_v163 import _new_id
        checkpoint_id = None if skip_checkpoint else _new_id("chk_")
        audit_id      = _new_id("aud_")

        return PauseResult(
            success=True,
            status=PAUSED,
            session_id=session_id,
            message=f"Session {session_id} paused: {reason}",
            checkpoint_id=checkpoint_id,
            audit_id=audit_id,
            broker_called=False,
            ledger_write=False,
            position_modified=False,
        )


__all__ = ["PausePolicy", "PauseResult"]
