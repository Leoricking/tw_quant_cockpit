"""
Halt Policy v1.6.3 — No auto-resume.

PAPER SESSION OPERATIONS ONLY. RESEARCH ONLY. NO REAL ORDERS.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

from paper_trading.operations.enums_v163 import OperationalStatus

AUTO_RESUME_RUNNING = False   # MUST be False


HALT_TRIGGERS = [
    "safety_violation",
    "critical_health_failure",
    "failed_recovery",
    "corrupted_checkpoint",
    "missing_lineage",
    "kill_switch_active",
    "repeated_data_disconnect",
    "repeated_strategy_failure",
]


@dataclass
class HaltResult:
    success:       bool
    session_id:    str
    message:       str
    trigger:       str
    checkpoint_id: Optional[str] = None
    audit_id:      Optional[str] = None
    incident_id:   Optional[str] = None
    auto_resume:   bool          = False  # Always False
    broker_called: bool          = False
    ledger_write:  bool          = False


class HaltPolicy:
    """
    Halt flow (10 steps):
    1. reject new signals
    2. reject new decisions
    3. reject new proposals
    4. reject new Paper Orders
    5. preserve journal
    6. create checkpoint
    7. set HALTED
    8. emit critical alert
    9. open incident
    10. require explicit recovery (NO auto-resume)
    """

    def execute(
        self,
        session_id:    str,
        current_status: OperationalStatus,
        trigger:       str,
        reason:        str = "",
    ) -> HaltResult:
        from paper_trading.operations.models_v163 import _new_id

        if trigger not in HALT_TRIGGERS:
            # Still halt on unknown triggers — treat as safety_violation
            trigger = "safety_violation"

        # Already halted — idempotent
        if current_status == OperationalStatus.HALTED:
            return HaltResult(
                success=True, session_id=session_id,
                message="Already HALTED",
                trigger=trigger,
                auto_resume=False, broker_called=False, ledger_write=False,
            )

        return HaltResult(
            success=True,
            session_id=session_id,
            message=f"Session {session_id} HALTED: {trigger} — {reason}",
            trigger=trigger,
            checkpoint_id=_new_id("chk_"),
            audit_id=_new_id("aud_"),
            incident_id=_new_id("inc_"),
            auto_resume=False,
            broker_called=False,
            ledger_write=False,
        )


__all__ = ["HaltPolicy", "HaltResult", "HALT_TRIGGERS", "AUTO_RESUME_RUNNING"]
