"""
replay/replay_training_session.py — ReplayTrainingSession v1.2.0

Manages replay training session lifecycle.
Session IDs: RPL-{symbol}-{YYYYMMDD}-{random4}
Archived sessions: immutable (duplicate to continue)
Decisions: SIMULATION only, no paper orders, no broker calls

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
import random
import string
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

SESSION_ID_PREFIX = "RPL-"


def _make_session_id(symbol: str) -> str:
    date_part = datetime.now().strftime("%Y%m%d")
    rand_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{SESSION_ID_PREFIX}{symbol}-{date_part}-{rand_part}"


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplayTrainingSession:
    """
    Manages replay training session lifecycle.
    Session IDs: RPL-{symbol}-{YYYYMMDD}-{random4}
    Archived sessions: immutable (duplicate to continue)
    Decisions: SIMULATION only, no paper orders, no broker calls
    """

    SESSION_ID_PREFIX = SESSION_ID_PREFIX

    def __init__(self, engine=None, store=None, calendar=None):
        self._engine = engine
        self._store = store
        self._calendar = calendar
        self._current_session_id: Optional[str] = None

    def create(self, config) -> Any:
        """Create a new session. Returns ReplaySessionState."""
        from replay.replay_schema import ReplaySessionState

        if self._store:
            self._store.save_session_config(config)

        state = ReplaySessionState(
            session_id=config.session_id,
            current_date=config.initial_date or config.start_date,
            current_index=0,
            total_steps=0,
            status="CREATED",
            playback_speed=config.playback_speed,
            qualification="UNKNOWN",
        )

        if self._store:
            self._store.save_session_state(state)
            from replay.replay_schema import ReplayEvent
            event = ReplayEvent(
                event_id=f"EVT-{uuid.uuid4().hex[:12].upper()}",
                session_id=config.session_id,
                replay_date=state.current_date,
                event_type="SESSION_CREATED",
                payload={"config": config.to_dict()},
            )
            self._store.append_event(event)

        self._current_session_id = config.session_id
        return state

    def load(self, session_id: str) -> Optional[Any]:
        """Load session state. Returns ReplaySessionState or None."""
        from replay.replay_schema import ReplaySessionState

        if not self._store:
            return None
        state_dict = self._store.load_session_state(session_id)
        if not state_dict:
            return None
        state = ReplaySessionState.from_dict(state_dict)
        self._current_session_id = session_id

        event = self._make_event(session_id, state.current_date, "SESSION_LOADED")
        if self._store:
            self._store.append_event(event)

        return state

    def resume(self, session_id: str) -> Optional[Any]:
        """Resume a paused session. Returns updated state."""
        from replay.replay_schema import ReplaySessionState

        if not self._store:
            return None
        state_dict = self._store.load_session_state(session_id)
        if not state_dict:
            return None
        state = ReplaySessionState.from_dict(state_dict)
        if state.status == "ARCHIVED":
            logger.warning("[ReplayTrainingSession] Cannot resume ARCHIVED session %s", session_id)
            return state
        state.status = "READY"
        state.paused = False
        state.updated_at = _now_utc()
        self._store.save_session_state(state)

        event = self._make_event(session_id, state.current_date, "SESSION_RESUMED")
        self._store.append_event(event)

        self._current_session_id = session_id
        return state

    def pause(self, session_id: Optional[str] = None) -> Optional[Any]:
        """Pause active session. Returns updated state."""
        from replay.replay_schema import ReplaySessionState

        sid = session_id or self._current_session_id
        if not sid or not self._store:
            return None
        state_dict = self._store.load_session_state(sid)
        if not state_dict:
            return None
        state = ReplaySessionState.from_dict(state_dict)
        state.status = "PAUSED"
        state.paused = True
        state.updated_at = _now_utc()
        self._store.save_session_state(state)

        event = self._make_event(sid, state.current_date, "PLAY_PAUSED")
        self._store.append_event(event)
        return state

    def play(self, session_id: Optional[str] = None, speed: Optional[int] = None) -> Optional[Any]:
        """Set session to PLAYING. Returns updated state."""
        from replay.replay_schema import ReplaySessionState

        sid = session_id or self._current_session_id
        if not sid or not self._store:
            return None
        state_dict = self._store.load_session_state(sid)
        if not state_dict:
            return None
        state = ReplaySessionState.from_dict(state_dict)
        state.status = "PLAYING"
        state.paused = False
        if speed is not None:
            state.playback_speed = speed
        state.updated_at = _now_utc()
        self._store.save_session_state(state)

        event = self._make_event(sid, state.current_date, "PLAY_STARTED")
        self._store.append_event(event)
        return state

    def archive(self, session_id: Optional[str] = None) -> Optional[Any]:
        """Archive a session. Archived sessions are immutable. Returns updated state."""
        from replay.replay_schema import ReplaySessionState

        sid = session_id or self._current_session_id
        if not sid or not self._store:
            return None
        state_dict = self._store.load_session_state(sid)
        if not state_dict:
            return None
        state = ReplaySessionState.from_dict(state_dict)
        state.status = "ARCHIVED"
        state.updated_at = _now_utc()
        self._store.save_session_state(state)

        event = self._make_event(sid, state.current_date, "SESSION_ARCHIVED")
        self._store.append_event(event)
        return state

    def duplicate(self, session_id: Optional[str] = None, new_name: Optional[str] = None) -> Optional[Any]:
        """
        Duplicate a session. Returns new ReplaySessionState with new session_id.
        """
        from replay.replay_schema import ReplaySessionConfig, ReplaySessionState

        sid = session_id or self._current_session_id
        if not sid or not self._store:
            return None
        config_dict = self._store.load_session_config(sid)
        state_dict = self._store.load_session_state(sid)
        if not config_dict:
            return None

        # Create new config with new ID
        new_config = ReplaySessionConfig.from_dict(config_dict)
        new_config.session_id = _make_session_id(new_config.symbol)
        if new_name:
            new_config.session_name = new_name
        else:
            new_config.session_name = f"Copy of {new_config.session_name}"
        new_config.created_at = _now_utc()

        # Create fresh state
        old_state = ReplaySessionState.from_dict(state_dict) if state_dict else None
        new_state = ReplaySessionState(
            session_id=new_config.session_id,
            current_date=new_config.start_date,
            current_index=0,
            total_steps=old_state.total_steps if old_state else 0,
            status="CREATED",
            playback_speed=new_config.playback_speed,
            qualification="UNKNOWN",
        )

        self._store.save_session_config(new_config)
        self._store.save_session_state(new_state)

        event = self._make_event(new_config.session_id, new_state.current_date, "SESSION_CREATED",
                                  payload={"duplicated_from": sid})
        self._store.append_event(event)

        return new_state

    def validate(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Validate session integrity. Returns dict of checks."""
        sid = session_id or self._current_session_id
        results = {"session_id": sid, "research_only": True, "no_real_orders": True}
        if not sid or not self._store:
            results["valid"] = False
            results["reason"] = "No session_id or store"
            return results
        config = self._store.load_session_config(sid)
        state = self._store.load_session_state(sid)
        results["config_found"] = config is not None
        results["state_found"] = state is not None
        results["valid"] = config is not None and state is not None
        if config:
            results["research_only_config"] = config.get("research_only", True)
            results["no_real_orders_config"] = config.get("no_real_orders", True)
        return results

    def summary(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Return summary for session."""
        sid = session_id or self._current_session_id
        if not sid or not self._store:
            return {"session_id": sid, "error": "No store"}
        config = self._store.load_session_config(sid) or {}
        state = self._store.load_session_state(sid) or {}
        decisions = self._store.load_decisions(sid)
        return {
            "session_id": sid,
            "name": config.get("session_name", ""),
            "symbol": config.get("symbol", ""),
            "status": state.get("status", ""),
            "current_date": state.get("current_date", ""),
            "decisions": len(decisions),
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _make_event(self, session_id: str, replay_date: str, event_type: str, payload: Optional[Dict] = None):
        from replay.replay_schema import ReplayEvent
        return ReplayEvent(
            event_id=f"EVT-{uuid.uuid4().hex[:12].upper()}",
            session_id=session_id,
            replay_date=replay_date,
            event_type=event_type,
            payload=payload or {},
        )
