"""
paper_trading/strategy/checkpoint_v162.py — Checkpoint manager for Paper Strategy Orchestration v1.6.2.
[!] PAPER STRATEGY ONLY. NO REAL ORDERS. NO BROKER. RESEARCH ONLY. NOT INVESTMENT ADVICE.
"""
from __future__ import annotations

import json
import logging
import os
import threading
from typing import Any, Dict, List, Optional

from paper_trading.strategy.enums_v162 import CheckpointReason
from paper_trading.strategy.models_v162 import StrategyCheckpoint, _new_id, _now_iso
from paper_trading.strategy.strategy_state_v162 import StrategyState

logger = logging.getLogger(__name__)

_DEFAULT_CHECKPOINT_DIR = "data/paper_strategy/checkpoints"


class CheckpointManager:
    """
    Saves and loads paper strategy state checkpoints.

    Checkpoints allow strategy state recovery after crashes or restarts.
    Stored as JSON files in a configurable directory.

    [!] Research-only. Checkpoints do not represent real account state.
    """

    def __init__(
        self,
        strategy_id: str,
        checkpoint_dir: str = _DEFAULT_CHECKPOINT_DIR,
        max_checkpoints: int = 5,
    ) -> None:
        self.strategy_id = strategy_id
        self.checkpoint_dir = checkpoint_dir
        self.max_checkpoints = max_checkpoints
        self._lock = threading.Lock()
        self._checkpoints: List[StrategyCheckpoint] = []
        os.makedirs(checkpoint_dir, exist_ok=True)

    def save(
        self,
        state: StrategyState,
        reason: CheckpointReason = CheckpointReason.PERIODIC,
    ) -> StrategyCheckpoint:
        """Save a checkpoint of the current strategy state."""
        cp = StrategyCheckpoint(
            checkpoint_id=_new_id(),
            strategy_id=self.strategy_id,
            reason=reason.value,
            saved_at=_now_iso(),
            signal_count=state.signal_count,
            decision_count=state.decision_count,
            proposal_count=state.proposal_count,
            cooldown_map=state.cooldown_snapshot(),
            rate_window=state.rate_window_snapshot(),
            open_proposals=state.open_proposals_snapshot(),
            extra_state={},
        )

        with self._lock:
            self._checkpoints.append(cp)
            # Prune old checkpoints
            if len(self._checkpoints) > self.max_checkpoints:
                oldest = self._checkpoints.pop(0)
                self._delete_file(oldest.checkpoint_id)

        self._write_file(cp)
        logger.info(
            "[v1.6.2][checkpoint] Saved checkpoint %s for strategy %s (reason=%s)",
            cp.checkpoint_id[:8], self.strategy_id[:8], reason.value
        )
        return cp

    def latest(self) -> Optional[StrategyCheckpoint]:
        """Return the most recent checkpoint, or None if none exist."""
        with self._lock:
            if not self._checkpoints:
                return self._load_latest_from_disk()
            return self._checkpoints[-1]

    def restore_to_state(self, state: StrategyState, checkpoint: StrategyCheckpoint) -> None:
        """Apply a checkpoint to a StrategyState instance."""
        state.signal_count = checkpoint.signal_count
        state.decision_count = checkpoint.decision_count
        state.proposal_count = checkpoint.proposal_count
        state.restore_cooldown(checkpoint.cooldown_map)
        state.restore_rate_window(checkpoint.rate_window)
        logger.info(
            "[v1.6.2][checkpoint] Restored state from checkpoint %s",
            checkpoint.checkpoint_id[:8]
        )

    def list_checkpoints(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                {
                    "checkpoint_id": cp.checkpoint_id,
                    "reason": cp.reason,
                    "saved_at": cp.saved_at,
                    "signal_count": cp.signal_count,
                    "decision_count": cp.decision_count,
                }
                for cp in self._checkpoints
            ]

    def _checkpoint_path(self, checkpoint_id: str) -> str:
        return os.path.join(
            self.checkpoint_dir,
            f"{self.strategy_id[:8]}_{checkpoint_id[:8]}.json"
        )

    def _write_file(self, cp: StrategyCheckpoint) -> None:
        path = self._checkpoint_path(cp.checkpoint_id)
        data = {
            "checkpoint_id": cp.checkpoint_id,
            "strategy_id": cp.strategy_id,
            "reason": cp.reason,
            "saved_at": cp.saved_at,
            "signal_count": cp.signal_count,
            "decision_count": cp.decision_count,
            "proposal_count": cp.proposal_count,
            "cooldown_map": cp.cooldown_map,
            "rate_window": cp.rate_window,
            "open_proposals": cp.open_proposals,
            "extra_state": cp.extra_state,
        }
        try:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
        except OSError as exc:
            logger.warning("[v1.6.2][checkpoint] Write error: %s", exc)

    def _delete_file(self, checkpoint_id: str) -> None:
        path = self._checkpoint_path(checkpoint_id)
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError as exc:
            logger.warning("[v1.6.2][checkpoint] Delete error: %s", exc)

    def _load_latest_from_disk(self) -> Optional[StrategyCheckpoint]:
        """Find and load the most recent checkpoint file from disk."""
        try:
            files = [
                f for f in os.listdir(self.checkpoint_dir)
                if f.startswith(self.strategy_id[:8]) and f.endswith(".json")
            ]
            if not files:
                return None
            files.sort(reverse=True)
            path = os.path.join(self.checkpoint_dir, files[0])
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            return StrategyCheckpoint(
                checkpoint_id=data.get("checkpoint_id", _new_id()),
                strategy_id=data.get("strategy_id", self.strategy_id),
                reason=data.get("reason", CheckpointReason.PERIODIC.value),
                saved_at=data.get("saved_at", _now_iso()),
                signal_count=data.get("signal_count", 0),
                decision_count=data.get("decision_count", 0),
                proposal_count=data.get("proposal_count", 0),
                cooldown_map=data.get("cooldown_map", {}),
                rate_window=data.get("rate_window", []),
                open_proposals=data.get("open_proposals", []),
                extra_state=data.get("extra_state", {}),
            )
        except Exception as exc:
            logger.warning("[v1.6.2][checkpoint] Load from disk error: %s", exc)
            return None
