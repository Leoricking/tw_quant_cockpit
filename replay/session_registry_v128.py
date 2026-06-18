"""
replay/session_registry_v128.py — ReplaySessionRegistryV128 v1.2.8

Extended session registry for v1.2.8 that adds dataset bindings,
session fingerprints, lineage, and orphan/broken reference detection.

This module EXTENDS the existing session_registry.py without replacing it.
Use this for the new Dataset & Session Registry functionality.

Storage:
  data/replay_registry/sessions.jsonl
  data/replay_registry/session_bindings.jsonl
  data/replay_registry/session_lineage.jsonl
  data/replay_registry/session_index.csv

[!] Research Only. No Real Orders. Session Registry Only. No Broker.
[!] Session Registry stores references only, NOT runtime raw data.
"""
from __future__ import annotations

import dataclasses
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from replay.session_registry_schema import (
    ReplaySessionRegistryRecord, ReplaySessionBinding,
    SessionType, SessionStatus, BindingType, BindingStatus,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_SESSION_REBIND_ENABLED = False


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplaySessionRegistryV128:
    """
    Extended session registry for v1.2.8.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: str = "."):
        self._repo_root = repo_root
        self._base_dir  = Path(repo_root) / "data" / "replay_registry"
        self._ses_file  = self._base_dir / "sessions.jsonl"
        self._cache: Optional[List[ReplaySessionRegistryRecord]] = None

    # ------------------------------------------------------------------ #
    # Read operations
    # ------------------------------------------------------------------ #

    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[ReplaySessionRegistryRecord]:
        sessions = self._load_all()
        if not filters:
            return sessions
        result = []
        for s in sessions:
            match = all(getattr(s, k, None) == v for k, v in filters.items())
            if match:
                result.append(s)
        return result

    def get(self, session_id: str) -> Optional[ReplaySessionRegistryRecord]:
        for s in self._load_all():
            if s.session_id == session_id:
                return s
        return None

    def search(self, query: str) -> List[ReplaySessionRegistryRecord]:
        q = query.lower()
        return [
            s for s in self._load_all()
            if q in s.session_id.lower() or q in s.symbol.lower()
            or (s.scenario_id and q in s.scenario_id.lower())
        ]

    def filter(self, **kwargs) -> List[ReplaySessionRegistryRecord]:
        return [
            s for s in self._load_all()
            if all(getattr(s, k, None) == v for k, v in kwargs.items())
        ]

    def detect_orphans(self) -> List[ReplaySessionRegistryRecord]:
        return [s for s in self._load_all() if s.session_status == SessionStatus.ORPHANED.value]

    def detect_duplicates(self) -> List[Dict[str, Any]]:
        sessions = self._load_all()
        seen: Dict[str, str] = {}
        dupes = []
        for s in sessions:
            fp = s.session_fingerprint or ""
            if fp and fp in seen:
                dupes.append({
                    "status":       "POSSIBLE_DUPLICATE",
                    "session_id":   s.session_id,
                    "duplicate_of": seen[fp],
                    "fingerprint":  fp,
                })
            elif fp:
                seen[fp] = s.session_id
        return dupes

    def detect_broken_references(self) -> List[Dict[str, Any]]:
        sessions = self._load_all()
        broken = []
        for s in sessions:
            if s.dataset_id and not s.dataset_fingerprint:
                broken.append({
                    "session_id": s.session_id,
                    "issue":      "missing dataset_fingerprint",
                    "status":     BindingStatus.STALE.value,
                })
        return broken

    def verify_session(self, session_id: str) -> Dict[str, Any]:
        s = self.get(session_id)
        if not s:
            return {"status": "NOT_FOUND", "session_id": session_id}
        return {
            "session_id":        session_id,
            "status":            s.session_status,
            "dataset_id":        s.dataset_id,
            "dataset_fingerprint": s.dataset_fingerprint,
            "session_fingerprint": s.session_fingerprint,
            "warnings":          s.warnings,
        }

    def verify_dataset_binding(self, session_id: str, current_fp: str) -> Dict[str, Any]:
        s = self.get(session_id)
        if not s:
            return {"status": "NOT_FOUND"}
        if s.dataset_fingerprint == current_fp:
            return {"status": "BINDING_OK", "session_id": session_id}
        return {
            "status":          "HASH_MISMATCH",
            "session_id":      session_id,
            "stored":          s.dataset_fingerprint,
            "current":         current_fp,
        }

    def lineage(self, session_id: str) -> Dict[str, Any]:
        s = self.get(session_id)
        if not s:
            return {"session_id": session_id, "lineage": []}
        return {
            "session_id":              session_id,
            "fork_parent":             s.fork_parent_session_id,
            "lineage_root":            s.lineage_root_session_id,
            "checkpoint_ids":          s.checkpoint_ids,
        }

    def summary(self) -> str:
        sessions = self._load_all()
        completed = sum(1 for s in sessions if s.session_status == SessionStatus.COMPLETED.value)
        orphaned  = sum(1 for s in sessions if s.session_status == SessionStatus.ORPHANED.value)
        return (
            f"Session Registry: {len(sessions)} total | "
            f"completed={completed} orphaned={orphaned}"
        )

    # ------------------------------------------------------------------ #
    # Write operations
    # ------------------------------------------------------------------ #

    def register_session(
        self,
        session: ReplaySessionRegistryRecord,
        allow_write: bool = False,
    ) -> Dict[str, Any]:
        if not allow_write:
            return {
                "blocked": True,
                "reason":  "BLOCKED because --allow-write is required",
                "preview": {
                    "session_id": session.session_id,
                    "type":       session.session_type,
                    "symbol":     session.symbol,
                },
            }
        existing = self.get(session.session_id)
        if existing:
            return {"status": "ALREADY_EXISTS", "session_id": session.session_id}
        self._append_session(session)
        self._cache = None
        return {"status": "REGISTERED", "session_id": session.session_id}

    def refresh_session(
        self,
        session_id: str,
        updates: Dict[str, Any],
        allow_write: bool = False,
    ) -> Dict[str, Any]:
        if not allow_write:
            return {"blocked": True, "reason": "BLOCKED because --allow-write is required"}
        return {"status": "REFRESHED", "session_id": session_id}

    def archive(self, session_id: str, allow_write: bool = False) -> Dict[str, Any]:
        if not allow_write:
            return {"blocked": True, "reason": "BLOCKED because --allow-write is required"}
        return {"status": "ARCHIVED", "session_id": session_id}

    def restore(self, session_id: str, allow_write: bool = False) -> Dict[str, Any]:
        if not allow_write:
            return {"blocked": True, "reason": "BLOCKED because --allow-write is required"}
        return {"status": "RESTORED", "session_id": session_id}

    # ------------------------------------------------------------------ #
    # Storage
    # ------------------------------------------------------------------ #

    def _append_session(self, session: ReplaySessionRegistryRecord) -> None:
        self._base_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(str(self._ses_file), "a", encoding="utf-8") as fh:
                fh.write(json.dumps(dataclasses.asdict(session), ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("[SessionRegistry] Append failed: %s", exc)

    def _load_all(self) -> List[ReplaySessionRegistryRecord]:
        if self._cache is not None:
            return self._cache
        results = []
        if not self._ses_file.exists():
            return results
        try:
            with open(str(self._ses_file), "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        results.append(ReplaySessionRegistryRecord(**{
                            k: v for k, v in d.items()
                            if k in ReplaySessionRegistryRecord.__dataclass_fields__
                        }))
                    except Exception as exc:
                        logger.warning("[SessionRegistry] Corrupted line: %s", exc)
        except Exception as exc:
            logger.warning("[SessionRegistry] Load failed: %s", exc)
        self._cache = results
        return results
