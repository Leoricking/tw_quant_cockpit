"""
replay/session_manager.py — ReplaySessionManager v1.2.1

Manages session lifecycle: create, search, filter, fork, clone, archive, restore.
delete_from_view: marks hidden=True, does NOT delete audit.
archive: does NOT delete data.
restore: only restores metadata state.
fork: always creates new session_id.
fork/duplicate: never copies future data.
archived sessions: immutable; must restore to resume.
session_folder: uses repo-relative runtime path.

[!] Research Only. No Real Orders. Replay Training Only.
[!] No auto-play, no auto-decision, no auto-scoring, no trade execution.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplaySessionManager:
    """
    Manages session lifecycle: create, search, filter, fork, clone, archive, restore.
    delete_from_view: marks hidden=True, does NOT delete audit.
    archive: does NOT delete data. archived sessions are immutable until restored.
    fork: always creates new session_id. Never copies future data.
    session_folder: uses repo-relative runtime path.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(
        self, engine=None, store=None, lineage=None,
        checkpoint_mgr=None, scenario_lib=None, repo_root=None,
    ):
        self._engine = engine
        self._repo_root = repo_root or "."
        if store is None:
            from replay.replay_session_store import ReplaySessionStore
            store = ReplaySessionStore(repo_root=repo_root)
        self._store = store
        if lineage is None:
            try:
                from replay.session_lineage import ReplaySessionLineageManager
                lineage = ReplaySessionLineageManager(store=store, repo_root=repo_root)
            except Exception as exc:
                logger.warning("[SessionManager] Could not init lineage: %s", exc)
        self._lineage = lineage
        if checkpoint_mgr is None:
            try:
                from replay.session_checkpoint import ReplayCheckpointManager
                checkpoint_mgr = ReplayCheckpointManager(store=store, repo_root=repo_root)
            except Exception as exc:
                logger.warning("[SessionManager] Could not init checkpoint_mgr: %s", exc)
        self._checkpoint_mgr = checkpoint_mgr
        if scenario_lib is None:
            try:
                from replay.scenario_library import ReplayScenarioLibrary
                scenario_lib = ReplayScenarioLibrary(repo_root=repo_root)
            except Exception as exc:
                logger.warning("[SessionManager] Could not init scenario_lib: %s", exc)
        self._scenario_lib = scenario_lib

    def _gen_session_id(self, symbol: str = "") -> str:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        short = uuid.uuid4().hex[:6].upper()
        sym = symbol.upper()[:6] if symbol else "UNK"
        return f"RPL-{sym}-{ts}-{short}"

    def create_from_scenario(
        self, scenario_id: str, symbol: str,
        start_date: Optional[str] = None, end_date: Optional[str] = None,
        overrides: Optional[Dict] = None,
    ) -> Optional[Any]:
        """Create a session from a scenario template."""
        if self._scenario_lib:
            instance = self._scenario_lib.instantiate(scenario_id, symbol, start_date, end_date, overrides)
        else:
            instance = None

        # Get template for defaults
        template = None
        if self._scenario_lib:
            tpl = self._scenario_lib.get_template(scenario_id)
            if tpl:
                from replay.scenario_schema import ReplayScenarioTemplate
                template = ReplayScenarioTemplate.from_dict(tpl)

        session_id = self._gen_session_id(symbol)
        name = f"{scenario_id} | {symbol}"
        if template:
            name = f"{template.scenario_name} | {symbol}"

        from replay.replay_schema import ReplaySessionConfig, ReplaySessionState
        config = ReplaySessionConfig(
            session_id=session_id,
            session_name=name,
            symbol=symbol,
            start_date=start_date or (template.start_date if template else "") or "",
            end_date=end_date or (template.end_date if template else "") or "",
            mode="real",
            strict_future_firewall=True,
            include_quality_gate=True,
            include_strategy_knowledge=True,
        )
        # Add v1.2.1 fields via dict update
        config_dict = config.to_dict()
        config_dict["scenario_id"] = scenario_id
        config_dict["scenario_instance_id"] = instance.instance_id if instance else None
        config_dict["root_session_id"] = session_id
        config_dict["parent_session_id"] = None
        config_dict["tags"] = []
        config_dict["portable_metadata_version"] = 1

        state = ReplaySessionState(
            session_id=session_id,
            current_date=config.start_date or "",
            current_index=0,
            total_steps=0,
            status="CREATED",
            qualification="OBSERVATIONAL_ONLY",
        )
        state_dict = state.to_dict()
        state_dict["checkpoint_count"] = 0
        state_dict["fork_count"] = 0
        state_dict["child_session_count"] = 0
        state_dict["hidden"] = False

        # Store
        from replay.replay_schema import ReplaySessionConfig as RSC
        config_obj = RSC.from_dict(config_dict)
        self._store.save_session_config(config_obj)
        from replay.replay_schema import ReplaySessionState as RSS
        state_obj = RSS.from_dict(state_dict)
        self._store.save_session_state(state_obj)

        # Lineage
        if self._lineage:
            self._lineage.create_root(session_id, scenario_id)

        return state_obj

    def create_free_practice(
        self, symbol: str, start_date: str, end_date: str,
        name: Optional[str] = None, **kwargs,
    ) -> Optional[Any]:
        """Create a free practice session (no scenario template)."""
        session_id = self._gen_session_id(symbol)
        session_name = name or f"Free Practice | {symbol} | {start_date}"

        from replay.replay_schema import ReplaySessionConfig, ReplaySessionState
        config = ReplaySessionConfig(
            session_id=session_id,
            session_name=session_name,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            mode="real",
        )
        state = ReplaySessionState(
            session_id=session_id,
            current_date=start_date,
            current_index=0,
            total_steps=0,
            status="CREATED",
        )
        self._store.save_session_config(config)
        self._store.save_session_state(state)
        if self._lineage:
            self._lineage.create_root(session_id, None)
        return state

    def list_sessions(
        self, include_hidden: bool = False, include_archived: bool = False,
    ) -> List[Dict[str, Any]]:
        sessions = self._store.list_sessions()
        result = []
        for s in sessions:
            sid = s.get("session_id", "")
            state = self._store.load_session_state(sid) or {}
            if not include_hidden and state.get("hidden", False):
                continue
            if not include_archived and state.get("status") == "ARCHIVED":
                continue
            result.append({**s, "_state": state})
        return result

    def search_sessions(self, query: str) -> List[Dict[str, Any]]:
        q = query.lower()
        all_sessions = self._store.list_sessions()
        results = []
        for s in all_sessions:
            sid = s.get("session_id", "")
            name = s.get("session_name", "")
            symbol = s.get("symbol", "")
            state = self._store.load_session_state(sid) or {}
            if (q in sid.lower() or q in name.lower() or q in symbol.lower()):
                results.append({**s, "_state": state})
        return results

    def filter_sessions(
        self, symbol=None, scenario=None, status=None, qualification=None,
        date_from=None, date_to=None, tag=None, archived=None,
        active=None, completed=None, blocked=None,
    ) -> List[Dict[str, Any]]:
        all_sessions = self._store.list_sessions()
        results = []
        for s in all_sessions:
            sid = s.get("session_id", "")
            state = self._store.load_session_state(sid) or {}
            if symbol and s.get("symbol") != symbol:
                continue
            if scenario and s.get("scenario_id") != scenario:
                continue
            if status and state.get("status") != status:
                continue
            if qualification and state.get("qualification") != qualification:
                continue
            if archived is not None:
                is_arch = state.get("status") == "ARCHIVED"
                if archived != is_arch:
                    continue
            if active is not None:
                is_active = state.get("status") in ("PLAYING", "READY", "PAUSED")
                if active != is_active:
                    continue
            if completed is not None:
                is_comp = state.get("status") == "COMPLETED"
                if completed != is_comp:
                    continue
            if blocked is not None:
                is_blocked = state.get("status") == "BLOCKED"
                if blocked != is_blocked:
                    continue
            results.append({**s, "_state": state})
        return results

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        config = self._store.load_session_config(session_id)
        if config is None:
            return None
        state = self._store.load_session_state(session_id) or {}
        return {**config, "_state": state}

    def resume_session(self, session_id: str) -> Optional[Any]:
        from replay.replay_schema import ReplaySessionState
        state_dict = self._store.load_session_state(session_id)
        if state_dict is None:
            return None
        if state_dict.get("status") == "ARCHIVED":
            logger.warning("[SessionManager] Cannot resume archived session %s. Restore first.", session_id)
            return None
        state_dict["status"] = "PLAYING"
        state_dict["updated_at"] = _now_utc()
        state = ReplaySessionState.from_dict(state_dict)
        self._store.save_session_state(state)
        return state

    def duplicate_session(self, session_id: str, new_name: Optional[str] = None) -> Optional[Any]:
        config_dict = self._store.load_session_config(session_id)
        if config_dict is None:
            return None
        from replay.replay_schema import ReplaySessionConfig, ReplaySessionState
        new_id = self._gen_session_id(config_dict.get("symbol", ""))
        now = _now_utc()
        new_config = dict(config_dict)
        new_config["session_id"] = new_id
        new_config["session_name"] = new_name or f"{config_dict.get('session_name', '')} (copy)"
        new_config["created_at"] = now
        new_config["root_session_id"] = new_id
        new_config["parent_session_id"] = session_id
        config_obj = ReplaySessionConfig.from_dict(new_config)
        self._store.save_session_config(config_obj)

        state = ReplaySessionState(
            session_id=new_id,
            current_date=config_dict.get("start_date", ""),
            current_index=0,
            total_steps=0,
            status="CREATED",
        )
        self._store.save_session_state(state)
        if self._lineage:
            self._lineage.mark_duplicate(session_id, new_id)
        return state

    def fork_session(
        self, session_id: str, checkpoint_id: Optional[str] = None,
        new_name: Optional[str] = None,
    ) -> Optional[Any]:
        """Fork always creates new session_id. Never copies future data."""
        config_dict = self._store.load_session_config(session_id)
        if config_dict is None:
            return None

        from replay.replay_schema import ReplaySessionConfig, ReplaySessionState

        # Start from checkpoint if specified
        if checkpoint_id and self._checkpoint_mgr:
            cp = self._checkpoint_mgr.get_checkpoint(checkpoint_id)
            start_state = cp.get("state_snapshot", {}) if cp else {}
        else:
            start_state = self._store.load_session_state(session_id) or {}

        new_id = self._gen_session_id(config_dict.get("symbol", ""))
        now = _now_utc()
        new_config = dict(config_dict)
        new_config["session_id"] = new_id
        new_config["session_name"] = new_name or f"{config_dict.get('session_name', '')} (fork)"
        new_config["created_at"] = now
        new_config["root_session_id"] = config_dict.get("root_session_id", session_id)
        new_config["parent_session_id"] = session_id
        new_config["source_checkpoint_id"] = checkpoint_id
        config_obj = ReplaySessionConfig.from_dict(new_config)
        self._store.save_session_config(config_obj)

        fork_state = dict(start_state)
        fork_state["session_id"] = new_id
        fork_state["status"] = "CREATED"
        fork_state["updated_at"] = now
        # Remove any future fields
        for ff in ["future_return", "realized_pnl", "outcome", "final_label"]:
            fork_state.pop(ff, None)
        state_obj = ReplaySessionState.from_dict(fork_state)
        self._store.save_session_state(state_obj)

        if self._lineage:
            self._lineage.mark_fork(session_id, new_id, checkpoint_id)

        return state_obj

    def archive_session(self, session_id: str) -> Optional[Any]:
        from replay.replay_schema import ReplaySessionState
        state_dict = self._store.load_session_state(session_id)
        if state_dict is None:
            return None
        state_dict["status"] = "ARCHIVED"
        state_dict["archived_at"] = _now_utc()
        state_dict["updated_at"] = _now_utc()
        state = ReplaySessionState.from_dict(state_dict)
        self._store.save_session_state(state)
        return state

    def restore_session(self, session_id: str) -> Optional[Any]:
        """Restore only restores metadata state."""
        from replay.replay_schema import ReplaySessionState
        state_dict = self._store.load_session_state(session_id)
        if state_dict is None:
            return None
        state_dict["status"] = "PAUSED"
        state_dict["restored_at"] = _now_utc()
        state_dict["updated_at"] = _now_utc()
        state = ReplaySessionState.from_dict(state_dict)
        self._store.save_session_state(state)
        return state

    def delete_from_view(self, session_id: str) -> bool:
        """Sets hidden=True only — does NOT delete audit."""
        from replay.replay_schema import ReplaySessionState
        state_dict = self._store.load_session_state(session_id)
        if state_dict is None:
            return False
        state_dict["hidden"] = True
        state_dict["updated_at"] = _now_utc()
        state = ReplaySessionState.from_dict(state_dict)
        self._store.save_session_state(state)
        return True

    def session_folder(self, session_id: str) -> str:
        return str(Path(self._repo_root) / "data" / "replay_sessions" / session_id)

    def session_summary(self, session_id: str) -> Dict[str, Any]:
        config = self._store.load_session_config(session_id) or {}
        state = self._store.load_session_state(session_id) or {}
        decisions = self._store.load_decisions(session_id)
        annotations = self._store.load_annotations(session_id)
        checkpoints = []
        if self._checkpoint_mgr:
            checkpoints = self._checkpoint_mgr.list_checkpoints(session_id)
        lineage = None
        if self._lineage:
            lin = self._lineage.get_lineage(session_id)
            if lin:
                lineage = lin.to_dict()
        return {
            "session_id": session_id,
            "config": config,
            "state": state,
            "decision_count": len(decisions),
            "annotation_count": len(annotations),
            "checkpoint_count": len(checkpoints),
            "lineage": lineage,
            "research_only": True,
            "no_real_orders": True,
        }

    def session_health(self, session_id: str) -> Dict[str, Any]:
        config = self._store.load_session_config(session_id)
        state = self._store.load_session_state(session_id)
        return {
            "session_id": session_id,
            "config_present": config is not None,
            "state_present": state is not None,
            "status": state.get("status") if state else "UNKNOWN",
            "qualification": state.get("qualification") if state else "UNKNOWN",
            "research_only": True,
        }

    def batch_create(
        self, scenario_id: str, symbols: List[str],
        date_ranges=None, allow_write: bool = False, max_sessions: int = 50,
    ) -> Dict[str, Any]:
        from replay.batch_session_builder import ReplayBatchSessionBuilder
        builder = ReplayBatchSessionBuilder(
            session_manager=self,
            scenario_lib=self._scenario_lib,
            repo_root=self._repo_root,
        )
        return builder.build_from_scenario(
            scenario_id, symbols, date_ranges,
            allow_write=allow_write, max_sessions=max_sessions,
        )
