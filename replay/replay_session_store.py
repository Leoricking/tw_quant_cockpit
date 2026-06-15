"""
replay/replay_session_store.py — ReplaySessionStore v1.2.0

Persists replay session data.
Output: data/replay_sessions/
All append-only (sessions.jsonl, decisions.jsonl, events.jsonl, annotations.jsonl)
Current state: atomic write to session_state.json
Does NOT store: future labels, broker credentials, secrets, order tokens

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import json
import logging
import os
import tempfile
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplaySessionStore:
    """
    Persists replay session data.
    Output: data/replay_sessions/
    All append-only (sessions.jsonl, decisions.jsonl, events.jsonl, annotations.jsonl)
    Current state: atomic write to session_state.json
    Does NOT store: future labels, broker credentials, secrets, order tokens
    """

    OUTPUT_DIR = "data/replay_sessions"

    def __init__(self, repo_root=None):
        self.base_dir = Path(repo_root or ".") / self.OUTPUT_DIR
        self._ensure_dirs()

    # ------------------------------------------------------------------
    # Session config
    # ------------------------------------------------------------------

    def save_session_config(self, config) -> None:
        """Save session config as JSON file."""
        self._ensure_dirs()
        session_dir = self.base_dir / config.session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        config_path = session_dir / "session_config.json"
        data = config.to_dict() if hasattr(config, "to_dict") else config
        self._atomic_write_json(config_path, data)
        # Also append to global sessions index
        sessions_file = self.base_dir / "sessions.jsonl"
        self._append_jsonl(sessions_file, data)

    def save_session_state(self, state) -> None:
        """Atomic write to session_state.json."""
        self._ensure_dirs()
        session_dir = self.base_dir / state.session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        state_path = session_dir / "session_state.json"
        data = state.to_dict() if hasattr(state, "to_dict") else state
        self._atomic_write_json(state_path, data)

    # ------------------------------------------------------------------
    # Append-only stores
    # ------------------------------------------------------------------

    def append_decision(self, decision) -> None:
        """Append decision to decisions.jsonl."""
        self._ensure_dirs()
        session_dir = self.base_dir / decision.session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        decisions_file = session_dir / "decisions.jsonl"
        data = decision.to_dict() if hasattr(decision, "to_dict") else decision
        self._append_jsonl(decisions_file, data)

    def append_event(self, event) -> None:
        """Append event to events.jsonl."""
        self._ensure_dirs()
        session_dir = self.base_dir / event.session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        events_file = session_dir / "events.jsonl"
        data = event.to_dict() if hasattr(event, "to_dict") else event
        self._append_jsonl(events_file, data)

    def append_annotation(self, annotation) -> None:
        """Append annotation to annotations.jsonl."""
        self._ensure_dirs()
        session_dir = self.base_dir / annotation.session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        annotations_file = session_dir / "annotations.jsonl"
        data = annotation.to_dict() if hasattr(annotation, "to_dict") else annotation
        self._append_jsonl(annotations_file, data)

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_session_config(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session config from JSON."""
        config_path = self.base_dir / session_id / "session_config.json"
        if not config_path.exists():
            return None
        try:
            with open(str(config_path), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("[ReplaySessionStore] Failed loading config %s: %s", config_path, exc)
            return None

    def load_session_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load current session state from JSON."""
        state_path = self.base_dir / session_id / "session_state.json"
        if not state_path.exists():
            return None
        try:
            with open(str(state_path), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("[ReplaySessionStore] Failed loading state %s: %s", state_path, exc)
            return None

    def load_decisions(self, session_id: str) -> List[Dict[str, Any]]:
        """Load all decisions for session."""
        decisions_file = self.base_dir / session_id / "decisions.jsonl"
        return self._load_jsonl(decisions_file)

    def load_events(self, session_id: str) -> List[Dict[str, Any]]:
        """Load all events for session."""
        events_file = self.base_dir / session_id / "events.jsonl"
        return self._load_jsonl(events_file)

    def load_annotations(self, session_id: str) -> List[Dict[str, Any]]:
        """Load all annotations for session."""
        annotations_file = self.base_dir / session_id / "annotations.jsonl"
        return self._load_jsonl(annotations_file)

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------

    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions from sessions.jsonl index."""
        sessions_file = self.base_dir / "sessions.jsonl"
        if not sessions_file.exists():
            return []
        raw = self._load_jsonl(sessions_file)
        # Deduplicate by session_id, keep last
        seen = {}
        for item in raw:
            sid = item.get("session_id", "")
            if sid:
                seen[sid] = item
        return list(seen.values())

    def rebuild_index(self) -> int:
        """Rebuild sessions.jsonl from all session_config.json files."""
        self._ensure_dirs()
        configs = []
        for session_dir in self.base_dir.iterdir():
            if session_dir.is_dir():
                config_path = session_dir / "session_config.json"
                if config_path.exists():
                    try:
                        with open(str(config_path), "r", encoding="utf-8") as f:
                            configs.append(json.load(f))
                    except Exception:
                        pass
        sessions_file = self.base_dir / "sessions.jsonl"
        with open(str(sessions_file), "w", encoding="utf-8") as f:
            for item in configs:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        return len(configs)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _ensure_dirs(self) -> None:
        """Ensure output directory exists."""
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _atomic_write_json(self, path: Path, data: Any) -> None:
        """Write JSON atomically using temp file + rename."""
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = str(path) + ".tmp_" + uuid.uuid4().hex[:8]
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, str(path))
        except Exception as exc:
            logger.warning("[ReplaySessionStore] Atomic write failed %s: %s", path, exc)
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            raise

    def _append_jsonl(self, path: Path, data: Any) -> None:
        """Append one JSON line to a .jsonl file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(str(path), "a", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("[ReplaySessionStore] Append failed %s: %s", path, exc)

    def _load_jsonl(self, path: Path) -> List[Dict[str, Any]]:
        """Load all valid JSON lines from a .jsonl file. Tolerates corrupted tail."""
        if not path.exists():
            return []
        results = []
        try:
            with open(str(path), "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        results.append(json.loads(line))
                    except json.JSONDecodeError:
                        logger.warning("[ReplaySessionStore] Skipping corrupted line %d in %s", line_no, path)
        except Exception as exc:
            logger.warning("[ReplaySessionStore] Failed reading %s: %s", path, exc)
        return results
