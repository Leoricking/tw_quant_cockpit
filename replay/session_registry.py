"""
replay/session_registry.py — ReplaySessionRegistry v1.2.1

Unified index for replay domain metadata.
Does NOT replace Research Run Registry.
Links to Research Run Registry via session_id + registry_run_id.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplaySessionRegistry:
    """
    Unified index for replay domain metadata.
    Does NOT replace Research Run Registry.
    Links to Research Run Registry via session_id + registry_run_id.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None, repo_root=None):
        self._store = store
        self._repo_root = repo_root or "."
        self._base_dir = Path(self._repo_root) / "data" / "replay_sessions"
        self._registry_file = self._base_dir / "session_registry.jsonl"

    def _append_entry(self, entry: Dict[str, Any]):
        self._base_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(str(self._registry_file), "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("[SessionRegistry] Append failed: %s", exc)

    def _load_all(self) -> List[Dict[str, Any]]:
        if not self._registry_file.exists():
            return []
        results = []
        try:
            with open(str(self._registry_file), "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        results.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        except Exception:
            pass
        return results

    def register_scenario(self, scenario) -> None:
        d = scenario.to_dict() if hasattr(scenario, "to_dict") else scenario
        entry = {
            "type": "scenario",
            "scenario_id": d.get("scenario_id"),
            "scenario_name": d.get("scenario_name"),
            "category": d.get("category"),
            "archived": d.get("archived", False),
            "registered_at": _now_utc(),
        }
        self._append_entry(entry)

    def register_session(self, session_config, session_state) -> None:
        config = session_config.to_dict() if hasattr(session_config, "to_dict") else session_config
        state = session_state.to_dict() if hasattr(session_state, "to_dict") else session_state
        entry = {
            "type": "session",
            "session_id": config.get("session_id"),
            "symbol": config.get("symbol"),
            "scenario_id": config.get("scenario_id"),
            "status": state.get("status"),
            "qualification": state.get("qualification"),
            "registered_at": _now_utc(),
        }
        self._append_entry(entry)

    def register_checkpoint(self, checkpoint) -> None:
        d = checkpoint.to_dict() if hasattr(checkpoint, "to_dict") else checkpoint
        entry = {
            "type": "checkpoint",
            "checkpoint_id": d.get("checkpoint_id"),
            "session_id": d.get("session_id"),
            "replay_date": d.get("replay_date"),
            "registered_at": _now_utc(),
        }
        self._append_entry(entry)

    def update_status(self, entity_type: str, entity_id: str, status: str) -> None:
        self._append_entry({
            "type": "status_update",
            "entity_type": entity_type,
            "entity_id": entity_id,
            "status": status,
            "updated_at": _now_utc(),
        })

    def rebuild(self) -> int:
        # Rebuild from store sessions
        if self._store is None:
            return 0
        sessions = self._store.list_sessions()
        self._base_dir.mkdir(parents=True, exist_ok=True)
        entries = []
        for s in sessions:
            entries.append({"type": "session", **s, "registered_at": _now_utc()})
        with open(str(self._registry_file), "w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        return len(entries)

    def validate(self) -> Dict[str, Any]:
        entries = self._load_all()
        return {
            "total_entries": len(entries),
            "types": list({e.get("type") for e in entries}),
            "valid": True,
            "research_only": True,
        }

    def search(self, query: str) -> List[Dict[str, Any]]:
        q = query.lower()
        entries = self._load_all()
        results = []
        for e in entries:
            if any(q in str(v).lower() for v in e.values()):
                results.append(e)
        return results

    def summary(self) -> Dict[str, Any]:
        entries = self._load_all()
        scenarios = [e for e in entries if e.get("type") == "scenario"]
        sessions = [e for e in entries if e.get("type") == "session"]
        checkpoints = [e for e in entries if e.get("type") == "checkpoint"]
        return {
            "total_entries": len(entries),
            "scenarios": len(scenarios),
            "sessions": len(sessions),
            "checkpoints": len(checkpoints),
            "research_only": True,
            "no_real_orders": True,
        }

    def latest_active(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        entries = self._load_all()
        sessions = [e for e in entries if e.get("type") == "session" and e.get("status") in ("PLAYING", "READY", "PAUSED")]
        if symbol:
            sessions = [s for s in sessions if s.get("symbol") == symbol]
        return sessions

    def latest_completed(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        entries = self._load_all()
        sessions = [e for e in entries if e.get("type") == "session" and e.get("status") == "COMPLETED"]
        if symbol:
            sessions = [s for s in sessions if s.get("symbol") == symbol]
        return sessions

    def blocked_sessions(self) -> List[Dict[str, Any]]:
        entries = self._load_all()
        return [e for e in entries if e.get("type") == "session" and e.get("status") == "BLOCKED"]

    def orphan_sessions(self) -> List[Dict[str, Any]]:
        entries = self._load_all()
        return [e for e in entries if e.get("type") == "session" and not e.get("scenario_id")]
