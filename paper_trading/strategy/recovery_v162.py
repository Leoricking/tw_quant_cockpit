"""
paper_trading/strategy/recovery_v162.py — Recovery manager for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Tuple

from paper_trading.strategy.enums_v162 import (
    CheckpointReason,
    JournalEventType,
    RecoveryMode,
    StrategyStatus,
)
from paper_trading.strategy.models_v162 import StrategyCheckpoint, _now_iso
from paper_trading.strategy.strategy_state_v162 import StrategyState

logger = logging.getLogger(__name__)


class RecoveryManager:
    """
    Restores paper strategy state from a checkpoint after failure or restart.

    Modes:
      STATE_RESTORE — Restore counters/cooldown/rate window from checkpoint.
                      Most common mode for graceful recovery.
      FULL_REPLAY   — Restore from checkpoint then replay journal signals.
                      Used for strict reproducibility verification.
      COLD_START    — Ignore checkpoint; start fresh.
                      Used when checkpoint is corrupt or missing.

    [!] Research-only. No real portfolio state is touched.
    """

    def __init__(self, strategy_id: str) -> None:
        self.strategy_id = strategy_id
        self._recovery_count: int = 0
        self._last_recovery_at: Optional[str] = None
        self._last_mode: Optional[str] = None

    def recover(
        self,
        state: StrategyState,
        checkpoint: Optional[StrategyCheckpoint],
        mode: RecoveryMode = RecoveryMode.STATE_RESTORE,
    ) -> Tuple[bool, str]:
        """
        Attempt to recover the strategy state.
        Returns (ok, detail).
        """
        if mode == RecoveryMode.COLD_START:
            logger.info("[v1.6.2][recovery] COLD_START: no checkpoint used for %s", self.strategy_id[:8])
            self._record(RecoveryMode.COLD_START, True)
            return True, "cold_start: fresh state"

        if checkpoint is None:
            logger.warning(
                "[v1.6.2][recovery] No checkpoint available for %s — falling back to COLD_START",
                self.strategy_id[:8]
            )
            self._record(RecoveryMode.COLD_START, False)
            return False, "no_checkpoint_available"

        if mode == RecoveryMode.STATE_RESTORE:
            return self._state_restore(state, checkpoint)

        if mode == RecoveryMode.FULL_REPLAY:
            return self._full_replay(state, checkpoint)

        return False, f"Unknown recovery mode: {mode}"

    def _state_restore(
        self, state: StrategyState, checkpoint: StrategyCheckpoint
    ) -> Tuple[bool, str]:
        """Restore counters and cooldown/rate windows from checkpoint."""
        try:
            state.signal_count = checkpoint.signal_count
            state.decision_count = checkpoint.decision_count
            state.proposal_count = checkpoint.proposal_count
            state.restore_cooldown(checkpoint.cooldown_map)
            state.restore_rate_window(checkpoint.rate_window)
            state.set_status(StrategyStatus.READY)
            self._record(RecoveryMode.STATE_RESTORE, True)
            logger.info(
                "[v1.6.2][recovery] STATE_RESTORE success for %s from checkpoint %s",
                self.strategy_id[:8], checkpoint.checkpoint_id[:8]
            )
            return True, f"state_restored_from_{checkpoint.checkpoint_id[:8]}"
        except Exception as exc:
            self._record(RecoveryMode.STATE_RESTORE, False)
            logger.error("[v1.6.2][recovery] STATE_RESTORE error: %s", exc)
            return False, str(exc)

    def _full_replay(
        self, state: StrategyState, checkpoint: StrategyCheckpoint
    ) -> Tuple[bool, str]:
        """State restore + indicate that a replay is needed."""
        ok, detail = self._state_restore(state, checkpoint)
        if ok:
            self._record(RecoveryMode.FULL_REPLAY, True)
            return True, f"state_restored+replay_required:{detail}"
        return False, detail

    def _record(self, mode: RecoveryMode, ok: bool) -> None:
        self._recovery_count += 1
        self._last_recovery_at = _now_iso()
        self._last_mode = mode.value

    def stats(self) -> Dict[str, Any]:
        return {
            "strategy_id": self.strategy_id,
            "recovery_count": self._recovery_count,
            "last_recovery_at": self._last_recovery_at,
            "last_mode": self._last_mode,
            "paper_only": True,
            "research_only": True,
        }
