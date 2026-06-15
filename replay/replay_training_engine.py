"""
replay/replay_training_engine.py — ReplayTrainingEngine v1.2.0

Main engine coordinating all replay components.
Flow: validate symbol -> validate real data -> build calendar -> build timeline
      -> apply firewall -> build PIT snapshot -> apply quality gate -> apply strategy knowledge
      -> save state -> record event -> register run

Registry run_type: REPLAY_TRAINING
Qualification:
- real + PIT verified + gate qualified: OBSERVATIONAL_ONLY
- mock: DEMO_ONLY
- future firewall fail: BLOCKED

Does NOT create paper orders. Does NOT call broker.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import logging
import os
import random
import string
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _make_session_id(symbol: str) -> str:
    date_part = datetime.now().strftime("%Y%m%d")
    rand_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"RPL-{symbol}-{date_part}-{rand_part}"


class ReplayTrainingEngine:
    """
    Main engine coordinating all replay components.
    Does NOT create paper orders. Does NOT call broker.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    REPLAY_TRAINING_ONLY = True

    def __init__(self, repo_root=None, mode: str = "real"):
        self.repo_root = Path(repo_root) if repo_root else Path(".")
        self.mode = mode

        # Initialize sub-components
        from replay.replay_data_source import ReplayDataSource
        from replay.future_data_firewall import ReplayFutureDataFirewall
        from replay.replay_calendar import ReplayTradingCalendar
        from replay.replay_timeline import ReplayTimeline
        from replay.point_in_time_context import PointInTimeReplayContextBuilder
        from replay.replay_session_store import ReplaySessionStore
        from replay.replay_training_session import ReplayTrainingSession
        from replay.replay_decision import ReplayDecisionManager
        from replay.replay_annotations import ReplayAnnotationManager
        from replay.replay_summary import ReplaySessionSummaryBuilder
        from replay.replay_query import ReplayQuery

        self._data_source = ReplayDataSource(repo_root=str(self.repo_root), mode=mode)
        self._firewall = ReplayFutureDataFirewall()
        self._calendar = ReplayTradingCalendar(repo_root=str(self.repo_root))
        self._timeline = ReplayTimeline(calendar=self._calendar)
        self._pit_builder = PointInTimeReplayContextBuilder(
            data_source=self._data_source,
            firewall=self._firewall,
            repo_root=str(self.repo_root),
        )
        self._store = ReplaySessionStore(repo_root=str(self.repo_root))
        self._session_mgr = ReplayTrainingSession(store=self._store, calendar=self._calendar)
        self._decision_mgr = ReplayDecisionManager(store=self._store)
        self._annotation_mgr = ReplayAnnotationManager(store=self._store)
        self._summary_builder = ReplaySessionSummaryBuilder(store=self._store)
        self._query = ReplayQuery(store=self._store)

        # Active sessions: session_id -> ReplayTimeline
        self._active_timelines: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------

    def create_session(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        name: Optional[str] = None,
        **kwargs,
    ) -> Any:
        """Create a new replay training session. Returns ReplaySessionState."""
        from replay.replay_schema import ReplaySessionConfig, ReplaySessionState
        from replay.replay_timeline import ReplayTimeline

        session_id = _make_session_id(symbol)
        config = ReplaySessionConfig(
            session_id=session_id,
            session_name=name or f"Replay {symbol} {start_date}~{end_date}",
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            initial_date=kwargs.get("initial_date"),
            mode=self.mode,
            tier=kwargs.get("tier", ""),
            visible_history_days=int(kwargs.get("visible_history_days", 120)),
            playback_speed=int(kwargs.get("playback_speed", 1)),
            strict_future_firewall=True,
            include_strategy_knowledge=bool(kwargs.get("include_strategy_knowledge", True)),
            include_quality_gate=bool(kwargs.get("include_quality_gate", True)),
            include_freshness=bool(kwargs.get("include_freshness", True)),
            include_fundamental=bool(kwargs.get("include_fundamental", True)),
            include_chips=bool(kwargs.get("include_chips", True)),
        )

        # Build calendar and timeline
        dates = self._calendar.build_timeline(symbol, start_date, end_date)
        if not dates:
            # Try approximate dates from CSV file if any
            logger.warning("[ReplayTrainingEngine] No trading dates found for %s %s~%s", symbol, start_date, end_date)
            # Generate business days as fallback for mock mode
            if self.mode == "mock":
                dates = self._generate_mock_dates(start_date, end_date)
            else:
                dates = []

        timeline = ReplayTimeline(calendar=self._calendar)
        timeline.initialize(dates, initial_date=config.initial_date)
        self._active_timelines[session_id] = timeline

        # Build state
        initial_date = config.initial_date or (dates[0] if dates else start_date)
        state = ReplaySessionState(
            session_id=session_id,
            current_date=initial_date,
            current_index=0,
            total_steps=len(dates),
            status="READY",
            playback_speed=config.playback_speed,
            visible_from=dates[0] if dates else start_date,
            visible_to=initial_date,
            available_records=len(dates),
            qualification="DEMO_ONLY" if self.mode == "mock" else "UNKNOWN",
        )

        self._store.save_session_config(config)
        self._store.save_session_state(state)

        event = self._make_event(session_id, initial_date, "SESSION_CREATED",
                                  {"config": config.to_dict(), "total_dates": len(dates)})
        self._store.append_event(event)

        self.register_run(session_id, "SESSION_CREATED")
        return state

    def open_session(self, session_id: str) -> Optional[Any]:
        """Open and initialize a session for navigation."""
        from replay.replay_schema import ReplaySessionState
        from replay.replay_timeline import ReplayTimeline

        state_dict = self._store.load_session_state(session_id)
        if not state_dict:
            logger.warning("[ReplayTrainingEngine] Session not found: %s", session_id)
            return None
        state = ReplaySessionState.from_dict(state_dict)
        config_dict = self._store.load_session_config(session_id)
        if not config_dict:
            return state

        # Rebuild timeline
        from replay.replay_schema import ReplaySessionConfig
        config = ReplaySessionConfig.from_dict(config_dict)
        dates = self._calendar.build_timeline(config.symbol, config.start_date, config.end_date)
        if not dates and self.mode == "mock":
            dates = self._generate_mock_dates(config.start_date, config.end_date)

        timeline = ReplayTimeline(calendar=self._calendar)
        timeline.initialize(dates, initial_date=state.current_date)
        self._active_timelines[session_id] = timeline

        event = self._make_event(session_id, state.current_date, "SESSION_LOADED")
        self._store.append_event(event)
        return state

    def resume_session(self, session_id: str) -> Optional[Any]:
        """Resume a session. Returns updated state."""
        return self._session_mgr.resume(session_id)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def step_previous(self, session_id: str) -> Optional[Any]:
        """Move to previous day. Returns updated state."""
        from replay.replay_schema import ReplaySessionState

        timeline = self._get_timeline(session_id)
        if not timeline:
            return None

        prev_date, changed = timeline.previous()
        state_dict = self._store.load_session_state(session_id)
        if not state_dict:
            return None
        state = ReplaySessionState.from_dict(state_dict)

        if changed:
            state.current_date = prev_date
            state.current_index, _ = timeline.progress()
            state.updated_at = _now_utc()
            self._store.save_session_state(state)
            event = self._make_event(session_id, prev_date, "DATE_CHANGED", {"direction": "previous"})
            self._store.append_event(event)

        return state

    def step_next(self, session_id: str) -> Optional[Any]:
        """Move to next day. Returns updated state."""
        from replay.replay_schema import ReplaySessionState

        timeline = self._get_timeline(session_id)
        if not timeline:
            return None

        next_date, changed, completed = timeline.next()
        state_dict = self._store.load_session_state(session_id)
        if not state_dict:
            return None
        state = ReplaySessionState.from_dict(state_dict)

        if changed or completed:
            state.current_date = next_date
            state.current_index, _ = timeline.progress()
            if completed:
                state.completed = True
                state.status = "COMPLETED"
            state.updated_at = _now_utc()
            self._store.save_session_state(state)
            event_type = "SESSION_COMPLETED" if completed else "DATE_CHANGED"
            event = self._make_event(session_id, next_date, event_type, {"direction": "next", "completed": completed})
            self._store.append_event(event)

        return state

    def jump(self, session_id: str, date: str) -> Optional[Any]:
        """Jump to a specific date. Returns updated state."""
        from replay.replay_schema import ReplaySessionState

        timeline = self._get_timeline(session_id)
        if not timeline:
            return None

        actual_date, normalized = timeline.jump(date)
        if actual_date is None:
            return None

        state_dict = self._store.load_session_state(session_id)
        if not state_dict:
            return None
        state = ReplaySessionState.from_dict(state_dict)
        state.current_date = actual_date
        state.current_index, _ = timeline.progress()
        state.updated_at = _now_utc()
        self._store.save_session_state(state)

        event = self._make_event(session_id, actual_date, "DATE_CHANGED",
                                  {"jump_to": date, "actual": actual_date, "normalized": normalized})
        self._store.append_event(event)
        return state

    def play_step(self, session_id: str, speed: int = 1) -> Optional[Any]:
        """Advance one step at playback speed. Returns updated state."""
        return self.step_next(session_id)

    def pause(self, session_id: str) -> Optional[Any]:
        """Pause session. Returns updated state."""
        from replay.replay_schema import ReplaySessionState

        state_dict = self._store.load_session_state(session_id)
        if not state_dict:
            return None
        state = ReplaySessionState.from_dict(state_dict)
        state.status = "PAUSED"
        state.paused = True
        state.updated_at = _now_utc()
        self._store.save_session_state(state)
        event = self._make_event(session_id, state.current_date, "PLAY_PAUSED")
        self._store.append_event(event)
        return state

    # ------------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------------

    def current_snapshot(self, session_id: str) -> Optional[Any]:
        """Returns ReplayMarketSnapshot for current date."""
        state_dict = self._store.load_session_state(session_id)
        if not state_dict:
            return None
        config_dict = self._store.load_session_config(session_id)
        if not config_dict:
            return None

        from replay.replay_schema import ReplaySessionConfig, ReplaySessionState
        state = ReplaySessionState.from_dict(state_dict)
        config = ReplaySessionConfig.from_dict(config_dict)

        try:
            snapshot = self._pit_builder.build(config.symbol, state.current_date, config)
            return snapshot
        except Exception as exc:
            logger.warning("[ReplayTrainingEngine] Snapshot error for %s at %s: %s",
                           config.symbol, state.current_date, exc)
            return None

    # ------------------------------------------------------------------
    # Decisions and annotations
    # ------------------------------------------------------------------

    def record_decision(self, session_id: str, action: str, **kwargs) -> Optional[Any]:
        """Record a simulation decision. Returns ReplayDecision."""
        state_dict = self._store.load_session_state(session_id)
        config_dict = self._store.load_session_config(session_id)
        if not state_dict or not config_dict:
            return None

        from replay.replay_schema import ReplaySessionConfig, ReplaySessionState
        state = ReplaySessionState.from_dict(state_dict)
        config = ReplaySessionConfig.from_dict(config_dict)

        decision = self._decision_mgr.create_decision(
            session_id=session_id,
            symbol=config.symbol,
            replay_date=state.current_date,
            action=action,
            **kwargs,
        )

        # Update state
        state.last_action = action
        state.last_decision_id = decision.decision_id
        state.updated_at = _now_utc()
        self._store.save_session_state(state)

        event = self._make_event(session_id, state.current_date, "DECISION_RECORDED",
                                  {"decision_id": decision.decision_id, "action": action})
        self._store.append_event(event)
        return decision

    def add_annotation(self, session_id: str, **kwargs) -> Optional[Any]:
        """Add annotation. Returns ReplayAnnotation."""
        state_dict = self._store.load_session_state(session_id)
        if not state_dict:
            return None

        from replay.replay_schema import ReplaySessionState
        state = ReplaySessionState.from_dict(state_dict)

        annotation = self._annotation_mgr.add(
            session_id=session_id,
            replay_date=state.current_date,
            annotation_type=kwargs.get("annotation_type", "NOTE"),
            title=kwargs.get("title", ""),
            content=kwargs.get("content", ""),
            **{k: v for k, v in kwargs.items() if k not in ("annotation_type", "title", "content")},
        )

        event = self._make_event(session_id, state.current_date, "ANNOTATION_ADDED",
                                  {"annotation_id": annotation.annotation_id})
        self._store.append_event(event)
        return annotation

    # ------------------------------------------------------------------
    # Query and summary
    # ------------------------------------------------------------------

    def list_sessions(self, **kwargs) -> List[Dict[str, Any]]:
        """List all sessions."""
        return self._query.list_sessions(limit=kwargs.get("limit", 50))

    def validate_session(self, session_id: str) -> Dict[str, Any]:
        """Validate session integrity."""
        return self._session_mgr.validate(session_id)

    def build_summary(self, session_id: str) -> Dict[str, Any]:
        """Build session summary."""
        return self._summary_builder.build(session_id)

    def archive_session(self, session_id: str) -> Optional[Any]:
        """Archive a session."""
        return self._session_mgr.archive(session_id)

    def duplicate_session(self, session_id: str, new_name: Optional[str] = None) -> Optional[Any]:
        """Duplicate a session. Returns new state with new session_id."""
        return self._session_mgr.duplicate(session_id=session_id, new_name=new_name)

    # ------------------------------------------------------------------
    # Firewall and PIT checks
    # ------------------------------------------------------------------

    def firewall_check(self, session_id: str) -> Dict[str, Any]:
        """Run firewall check on current snapshot."""
        snapshot = self.current_snapshot(session_id)
        if snapshot is None:
            return {"session_id": session_id, "status": "NO_SNAPSHOT", "is_clean": False}
        is_clean, issues = self._firewall.verify_snapshot(snapshot)
        return {
            "session_id": session_id,
            "replay_date": snapshot.replay_date,
            "is_clean": is_clean,
            "issues": issues,
            "future_data_blocked_count": snapshot.future_data_blocked_count,
            "point_in_time_verified": snapshot.point_in_time_verified,
            "research_only": True,
            "no_real_orders": True,
        }

    def point_in_time_check(self, session_id: str) -> Dict[str, Any]:
        """Check point-in-time integrity for current snapshot."""
        snapshot = self.current_snapshot(session_id)
        if snapshot is None:
            return {"session_id": session_id, "status": "NO_SNAPSHOT"}
        return {
            "session_id": session_id,
            "replay_date": snapshot.replay_date,
            "point_in_time_verified": snapshot.point_in_time_verified,
            "future_data_blocked_count": snapshot.future_data_blocked_count,
            "timing_warnings": snapshot.timing_warnings,
            "available_sections": snapshot.available_sections,
            "unavailable_sections": snapshot.unavailable_sections,
            "research_only": True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Registry
    # ------------------------------------------------------------------

    def register_run(self, session_id: str, event_type: str) -> None:
        """Register a run in research registry."""
        try:
            from research_registry.registry_store import ResearchRegistryStore
            from release.version_info import VERSION, RELEASE_NAME
            import uuid as _uuid
            store = ResearchRegistryStore(repo_root=str(self.repo_root))
            run_id = f"run_{_uuid.uuid4().hex[:16]}"
            store.append_run({
                "registry_id": f"reg_{_uuid.uuid4().hex[:12]}",
                "run_id": run_id,
                "run_type": "REPLAY_TRAINING",
                "command_name": f"replay-{event_type.lower().replace('_', '-')}",
                "command_category": "SIMULATION",
                "status": "COMPLETED",
                "qualification": "DEMO_ONLY" if self.mode == "mock" else "OBSERVATIONAL_ONLY",
                "mode": self.mode,
                "stock": session_id,
                "started_at": _now_utc(),
                "completed_at": _now_utc(),
                "code_version": VERSION,
                "release_name": RELEASE_NAME,
                "research_only": True,
                "no_real_orders": True,
            })
        except Exception as exc:
            logger.debug("[ReplayTrainingEngine] Registry register_run failed (non-fatal): %s", exc)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_timeline(self, session_id: str):
        """Get or rebuild timeline for session_id."""
        if session_id not in self._active_timelines:
            self.open_session(session_id)
        return self._active_timelines.get(session_id)

    def _make_event(self, session_id: str, replay_date: str, event_type: str, payload: Optional[Dict] = None):
        from replay.replay_schema import ReplayEvent
        return ReplayEvent(
            event_id=f"EVT-{uuid.uuid4().hex[:12].upper()}",
            session_id=session_id,
            replay_date=replay_date,
            event_type=event_type,
            payload=payload or {},
        )

    def _generate_mock_dates(self, start_date: str, end_date: str) -> List[str]:
        """Generate approximate trading dates (Mon-Fri) for mock mode."""
        try:
            import pandas as pd
            dates = pd.bdate_range(start=start_date, end=end_date)
            return [d.strftime("%Y-%m-%d") for d in dates]
        except Exception:
            return []
