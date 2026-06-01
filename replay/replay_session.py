"""replay/replay_session.py — Replay Session management (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice."""
from __future__ import annotations

import json
import logging
import os
import random
import string
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
CREATED = "CREATED"
RUNNING = "RUNNING"
PAUSED = "PAUSED"
COMPLETED = "COMPLETED"
FAILED = "FAILED"
ARCHIVED = "ARCHIVED"


# ---------------------------------------------------------------------------
# ReplaySession dataclass
# ---------------------------------------------------------------------------
@dataclass
class ReplaySession:
    """Represents a single intraday replay training session.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    """

    session_id: str
    session_name: str = ""
    symbol: str = ""
    date: str = ""
    freq: str = "1min"
    mode: str = "real"
    created_at: str = ""
    started_at: str = ""
    finished_at: str = ""
    current_index: int = 0
    total_bars: int = 0
    playback_speed: float = 1.0
    training_mode: bool = True
    reveal_future: bool = False
    status: str = CREATED
    notes: str = ""
    research_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "session_name": self.session_name,
            "symbol": self.symbol,
            "date": self.date,
            "freq": self.freq,
            "mode": self.mode,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "current_index": self.current_index,
            "total_bars": self.total_bars,
            "playback_speed": self.playback_speed,
            "training_mode": self.training_mode,
            "reveal_future": self.reveal_future,
            "status": self.status,
            "notes": self.notes,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ReplaySession":
        return cls(
            session_id=d.get("session_id", ""),
            session_name=d.get("session_name", ""),
            symbol=d.get("symbol", ""),
            date=d.get("date", ""),
            freq=d.get("freq", "1min"),
            mode=d.get("mode", "real"),
            created_at=d.get("created_at", ""),
            started_at=d.get("started_at", ""),
            finished_at=d.get("finished_at", ""),
            current_index=d.get("current_index", 0),
            total_bars=d.get("total_bars", 0),
            playback_speed=d.get("playback_speed", 1.0),
            training_mode=d.get("training_mode", True),
            reveal_future=d.get("reveal_future", False),
            status=d.get("status", CREATED),
            notes=d.get("notes", ""),
            research_only=d.get("research_only", True),
            no_real_orders=d.get("no_real_orders", True),
            production_blocked=d.get("production_blocked", True),
        )


# ---------------------------------------------------------------------------
# ReplaySessionManager
# ---------------------------------------------------------------------------
class ReplaySessionManager:
    """Manages replay session lifecycle.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    """

    read_only = True
    no_real_orders = True

    def __init__(self, replay_root: str = "replay_sessions"):
        self._replay_root = os.path.join(BASE_DIR, replay_root)
        self._sessions_dir = os.path.join(self._replay_root, "sessions")
        self._index_path = os.path.join(self._replay_root, "sessions_index.json")
        os.makedirs(self._sessions_dir, exist_ok=True)
        logger.info("[ReplaySessionManager] sessions dir: %s", self._sessions_dir)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load_index(self) -> list:
        if not os.path.exists(self._index_path):
            return []
        try:
            with open(self._index_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception as exc:
            logger.warning("[ReplaySessionManager] failed to load index: %s", exc)
            return []

    def _save_index(self, index: list) -> bool:
        try:
            with open(self._index_path, "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
            return True
        except Exception as exc:
            logger.error("[ReplaySessionManager] failed to save index: %s", exc)
            return False

    def _session_path(self, session_id: str) -> str:
        return os.path.join(self._sessions_dir, f"{session_id}.json")

    @staticmethod
    def _generate_session_id() -> str:
        now = datetime.now()
        suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"REPLAY-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}-{suffix}"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def create_session(
        self,
        symbol: str,
        date: Optional[str] = None,
        freq: str = "1min",
        name: Optional[str] = None,
        training_mode: bool = True,
    ) -> ReplaySession:
        """Create and persist a new replay session."""
        now_str = datetime.now().isoformat()
        session_id = self._generate_session_id()
        session_name = name or f"Replay {symbol} {date or 'latest'} {freq}"
        session = ReplaySession(
            session_id=session_id,
            session_name=session_name,
            symbol=symbol,
            date=date or "",
            freq=freq,
            created_at=now_str,
            training_mode=training_mode,
        )
        self.save_session(session)

        # update index
        index = self._load_index()
        index.insert(
            0,
            {
                "session_id": session_id,
                "session_name": session_name,
                "symbol": symbol,
                "date": date or "",
                "freq": freq,
                "created_at": now_str,
                "status": CREATED,
            },
        )
        self._save_index(index)
        logger.info("[ReplaySessionManager] created session %s", session_id)
        return session

    def load_session(self, session_id: str) -> Optional[ReplaySession]:
        path = self._session_path(session_id)
        if not os.path.exists(path):
            logger.warning("[ReplaySessionManager] session not found: %s", session_id)
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
            return ReplaySession.from_dict(d)
        except Exception as exc:
            logger.error("[ReplaySessionManager] load_session error: %s", exc)
            return None

    def save_session(self, session: ReplaySession) -> bool:
        try:
            path = self._session_path(session.session_id)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(session.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as exc:
            logger.error("[ReplaySessionManager] save_session error: %s", exc)
            return False

    def list_sessions(self, limit: int = 50) -> list:
        """Return list of session summary dicts sorted by created_at desc."""
        index = self._load_index()
        sorted_index = sorted(index, key=lambda x: x.get("created_at", ""), reverse=True)
        return sorted_index[:limit]

    def update_progress(self, session_id: str, current_index: int) -> bool:
        session = self.load_session(session_id)
        if session is None:
            return False
        session.current_index = current_index
        if session.status == CREATED:
            session.status = RUNNING
            session.started_at = datetime.now().isoformat()
        return self.save_session(session)

    def complete_session(self, session_id: str) -> bool:
        session = self.load_session(session_id)
        if session is None:
            return False
        session.status = COMPLETED
        session.finished_at = datetime.now().isoformat()
        return self.save_session(session)

    def summary(self) -> dict:
        """Return aggregate summary across all sessions."""
        index = self._load_index()
        by_status: dict = {}
        for entry in index:
            s = entry.get("status", CREATED)
            by_status[s] = by_status.get(s, 0) + 1
        return {
            "total": len(index),
            "by_status": by_status,
            "avg_training_score": None,  # placeholder — not yet computed
            "research_only": True,
            "no_real_orders": True,
        }
