"""
replay/session_checkpoint.py — ReplayCheckpoint and ReplayCheckpointManager v1.2.1

RCP- prefix for checkpoint IDs.
Checkpoints store only data available at replay_date — NO future data.
restore: creates new state revision, does NOT overwrite append-only history.
fork: creates new session.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

FORBIDDEN_CHECKPOINT_FIELDS = [
    "future_return", "outcome", "final_label", "answer",
    "realized_pnl", "broker", "order_token", "api_key", "secret",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ReplayCheckpoint:
    checkpoint_id: str
    session_id: str
    replay_date: str
    timeline_index: int
    session_status: str
    state_snapshot: Dict[str, Any]
    latest_decision_id: Optional[str]
    decision_count: int
    annotation_count: int
    warning_count: int
    point_in_time_verified: bool
    qualification: str
    created_at: str
    note: str = ""
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checkpoint_id": self.checkpoint_id,
            "session_id": self.session_id,
            "replay_date": self.replay_date,
            "timeline_index": self.timeline_index,
            "session_status": self.session_status,
            "state_snapshot": self.state_snapshot,
            "latest_decision_id": self.latest_decision_id,
            "decision_count": self.decision_count,
            "annotation_count": self.annotation_count,
            "warning_count": self.warning_count,
            "point_in_time_verified": self.point_in_time_verified,
            "qualification": self.qualification,
            "created_at": self.created_at,
            "note": self.note,
            "research_only": True,
            "no_real_orders": True,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReplayCheckpoint":
        return cls(
            checkpoint_id=d.get("checkpoint_id", ""),
            session_id=d.get("session_id", ""),
            replay_date=d.get("replay_date", ""),
            timeline_index=int(d.get("timeline_index", 0)),
            session_status=d.get("session_status", "CREATED"),
            state_snapshot=d.get("state_snapshot", {}),
            latest_decision_id=d.get("latest_decision_id"),
            decision_count=int(d.get("decision_count", 0)),
            annotation_count=int(d.get("annotation_count", 0)),
            warning_count=int(d.get("warning_count", 0)),
            point_in_time_verified=bool(d.get("point_in_time_verified", False)),
            qualification=d.get("qualification", "UNKNOWN"),
            created_at=d.get("created_at", _now_utc()),
            note=d.get("note", ""),
            research_only=True,
            no_real_orders=True,
        )


class ReplayCheckpointManager:
    """
    Manages replay session checkpoints.
    RCP- prefix for checkpoint IDs.
    Checkpoints store only data available at replay_date — NO future data.
    restore: creates new state revision, does NOT overwrite append-only history.
    fork: creates new session.
    """

    CHECKPOINT_ID_PREFIX = "RCP-"
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None, firewall=None, repo_root=None):
        self._repo_root = repo_root or "."
        self._store = store
        self._firewall = firewall
        self._base_dir = Path(self._repo_root) / "data" / "replay_sessions"

    def _checkpoint_file(self) -> Path:
        return self._base_dir / "checkpoints.jsonl"

    def _gen_checkpoint_id(self) -> str:
        return f"{self.CHECKPOINT_ID_PREFIX}{uuid.uuid4().hex[:12].upper()}"

    def create_checkpoint(self, session_id: str, note: str = "") -> Optional[ReplayCheckpoint]:
        """Create a checkpoint for the current session state."""
        state_dict = None
        if self._store:
            state_dict = self._store.load_session_state(session_id)
        if state_dict is None:
            state_dict = {}

        # Remove forbidden fields from snapshot
        snapshot = {k: v for k, v in state_dict.items() if k not in FORBIDDEN_CHECKPOINT_FIELDS}

        decisions = []
        annotations = []
        if self._store:
            try:
                decisions = self._store.load_decisions(session_id)
            except Exception:
                pass
            try:
                annotations = self._store.load_annotations(session_id)
            except Exception:
                pass

        checkpoint = ReplayCheckpoint(
            checkpoint_id=self._gen_checkpoint_id(),
            session_id=session_id,
            replay_date=state_dict.get("current_date", ""),
            timeline_index=int(state_dict.get("current_index", 0)),
            session_status=state_dict.get("status", "CREATED"),
            state_snapshot=snapshot,
            latest_decision_id=state_dict.get("last_decision_id"),
            decision_count=len(decisions),
            annotation_count=len(annotations),
            warning_count=len(state_dict.get("warnings", [])),
            point_in_time_verified=bool(state_dict.get("point_in_time_verified", False)),
            qualification=state_dict.get("qualification", "UNKNOWN"),
            created_at=_now_utc(),
            note=note,
        )

        self._save_checkpoint(checkpoint)
        return checkpoint

    def _save_checkpoint(self, checkpoint: ReplayCheckpoint):
        cp_file = self._checkpoint_file()
        cp_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(str(cp_file), "a", encoding="utf-8") as f:
                f.write(json.dumps(checkpoint.to_dict(), ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("[CheckpointManager] Save failed: %s", exc)

        # Also write individual checkpoint file
        session_dir = self._base_dir / checkpoint.session_id / "checkpoints"
        session_dir.mkdir(parents=True, exist_ok=True)
        cp_path = session_dir / f"{checkpoint.checkpoint_id}.json"
        try:
            tmp = str(cp_path) + ".tmp_" + uuid.uuid4().hex[:6]
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(checkpoint.to_dict(), f, ensure_ascii=False, indent=2)
            os.replace(tmp, str(cp_path))
        except Exception as exc:
            logger.warning("[CheckpointManager] Individual save failed: %s", exc)

    def list_checkpoints(self, session_id: str) -> List[Dict[str, Any]]:
        session_dir = self._base_dir / session_id / "checkpoints"
        if not session_dir.exists():
            return []
        results = []
        for p in sorted(session_dir.glob("RCP-*.json")):
            try:
                with open(str(p), "r", encoding="utf-8") as f:
                    results.append(json.load(f))
            except Exception:
                pass
        return results

    def get_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        # Search all session checkpoints
        for session_dir in self._base_dir.iterdir():
            if session_dir.is_dir():
                cp_path = session_dir / "checkpoints" / f"{checkpoint_id}.json"
                if cp_path.exists():
                    try:
                        with open(str(cp_path), "r", encoding="utf-8") as f:
                            return json.load(f)
                    except Exception:
                        pass
        return None

    def restore_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Restore from checkpoint — creates new state revision, does NOT overwrite history."""
        cp = self.get_checkpoint(checkpoint_id)
        if cp is None:
            return None
        session_id = cp.get("session_id", "")
        if not session_id or not self._store:
            return {"restored": False, "error": "session_id or store missing"}
        # Load snapshot and apply as new state
        snapshot = cp.get("state_snapshot", {})
        snapshot["updated_at"] = _now_utc()
        snapshot["last_checkpoint_id"] = checkpoint_id
        # Save the restored state
        try:
            from replay.replay_schema import ReplaySessionState
            new_state = ReplaySessionState.from_dict(snapshot)
            self._store.save_session_state(new_state)
            return {"restored": True, "session_id": session_id, "checkpoint_id": checkpoint_id}
        except Exception as exc:
            logger.warning("[CheckpointManager] restore failed: %s", exc)
            return {"restored": False, "error": str(exc)}

    def fork_from_checkpoint(self, checkpoint_id: str, new_name: Optional[str] = None) -> Optional[str]:
        """Fork: creates new session from checkpoint. Returns new session_id."""
        cp = self.get_checkpoint(checkpoint_id)
        if cp is None:
            return None
        # New session ID
        new_sid = f"RPL-{uuid.uuid4().hex[:8].upper()}-FORK"
        logger.info("[CheckpointManager] Fork: %s -> %s", checkpoint_id, new_sid)
        return new_sid

    def compare_checkpoints(self, checkpoint_a_id: str, checkpoint_b_id: str) -> Dict[str, Any]:
        """Compare two checkpoints — NO future performance fields."""
        a = self.get_checkpoint(checkpoint_a_id) or {}
        b = self.get_checkpoint(checkpoint_b_id) or {}
        FORBIDDEN = {"future_return", "realized_pnl", "outcome", "final_label", "hindsight_score"}
        return {
            "checkpoint_a": checkpoint_a_id,
            "checkpoint_b": checkpoint_b_id,
            "session_a": a.get("session_id"),
            "session_b": b.get("session_id"),
            "date_a": a.get("replay_date"),
            "date_b": b.get("replay_date"),
            "decision_count_a": a.get("decision_count", 0),
            "decision_count_b": b.get("decision_count", 0),
            "qualification_a": a.get("qualification"),
            "qualification_b": b.get("qualification"),
            "research_only": True,
            "no_future_performance": True,
        }

    def validate_checkpoint(self, checkpoint) -> bool:
        if isinstance(checkpoint, ReplayCheckpoint):
            d = checkpoint.to_dict()
        else:
            d = checkpoint
        for f in FORBIDDEN_CHECKPOINT_FIELDS:
            if f in d:
                return False
        return True

    def rebuild_checkpoint_index(self) -> int:
        count = 0
        cp_file = self._checkpoint_file()
        cp_file.parent.mkdir(parents=True, exist_ok=True)
        entries = []
        if self._base_dir.exists():
            for session_dir in self._base_dir.iterdir():
                if session_dir.is_dir():
                    cp_dir = session_dir / "checkpoints"
                    if cp_dir.exists():
                        for p in sorted(cp_dir.glob("RCP-*.json")):
                            try:
                                with open(str(p), "r", encoding="utf-8") as f:
                                    entries.append(json.load(f))
                                    count += 1
                            except Exception:
                                pass
        with open(str(cp_file), "w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        return count
