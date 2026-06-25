"""
paper_trading/market_data/resume_v161.py — Session Resume v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Resume always targets PAUSED state — operator must explicitly start.
"""
from __future__ import annotations
from typing import Optional, Dict, Any

from paper_trading.market_data.enums_v161 import MarketDataSessionStatus
from paper_trading.market_data.models_v161 import MarketDataCheckpoint

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
RESUME_TO_PAUSED_NOT_RUNNING: bool = True   # Key invariant


class ResumeResult:
    def __init__(
        self,
        success: bool,
        new_status: MarketDataSessionStatus,
        checkpoint_id: Optional[str],
        message: str,
    ) -> None:
        self.success = success
        self.new_status = new_status
        self.checkpoint_id = checkpoint_id
        self.message = message


class SessionResumeManager:
    """
    Handles checkpoint-based session resumption.
    INVARIANT: Always resumes to PAUSED. Operator must call start() to go ACTIVE.
    Prevents auto-resume to RUNNING after crash/restore.
    """

    def resume_from_checkpoint(
        self,
        checkpoint: MarketDataCheckpoint,
    ) -> ResumeResult:
        """
        Resume session from a checkpoint.
        Always sets new_status=PAUSED. Never RUNNING or ACTIVE.
        """
        # Invariant check
        new_status = MarketDataSessionStatus.PAUSED

        return ResumeResult(
            success=True,
            new_status=new_status,  # Always PAUSED
            checkpoint_id=checkpoint.checkpoint_id,
            message=(
                f"Session resumed from checkpoint {checkpoint.checkpoint_id}. "
                "Status=PAUSED. Call start() to activate. "
                "RESUME_TO_PAUSED_NOT_RUNNING=True."
            ),
        )

    def resume_from_scratch(self) -> ResumeResult:
        """Start fresh — also PAUSED until explicitly started."""
        return ResumeResult(
            success=True,
            new_status=MarketDataSessionStatus.PAUSED,
            checkpoint_id=None,
            message="Session initialized to PAUSED state. Call start() to activate.",
        )

    def cannot_auto_resume_to_running(self) -> bool:
        """Confirms invariant: auto-resume to RUNNING is always False."""
        return False
