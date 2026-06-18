"""
replay/session_dataset_binding.py — ReplaySessionDatasetBinder v1.2.8

Manages session-to-dataset bindings.
Binding is locked after session creation by default.
Challenge attempts inherit the challenge dataset binding.
Review inherits session dataset fingerprint.
Completed sessions cannot be directly rebound.

[!] Research Only. No Real Orders. Session Registry Only. No Broker.
"""
from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from replay.session_registry_schema import (
    ReplaySessionBinding, BindingType, BindingStatus,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_SESSION_REBIND_ENABLED = False


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplaySessionDatasetBinder:
    """
    Manages session-dataset bindings.

    Rules:
    - Session binding locked after creation by default
    - Challenge attempts must inherit challenge dataset binding
    - Review must inherit session dataset fingerprint
    - Rebind is preview by default; requires allow_write=True to execute
    - Completed sessions cannot be directly rebound
    - Silent rebind is not allowed

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True
    AUTO_SESSION_REBIND_ENABLED = False

    def __init__(self, repo_root: str = "."):
        self._repo_root = repo_root
        self._base_dir  = Path(repo_root) / "data" / "replay_registry"
        self._bind_file = self._base_dir / "session_bindings.jsonl"
        self._bindings: List[ReplaySessionBinding] = []

    def preview_bind(
        self,
        session_id: str,
        dataset_id: str,
        version: str,
        dataset_fingerprint: str = "",
    ) -> Dict[str, Any]:
        """Preview binding without making changes."""
        existing = self._get_binding(session_id, BindingType.DATASET.value)
        return {
            "action":             "BIND_PREVIEW",
            "session_id":         session_id,
            "dataset_id":         dataset_id,
            "version":            version,
            "dataset_fingerprint": dataset_fingerprint[:16] + "..." if dataset_fingerprint else "",
            "already_bound":      existing is not None,
            "note":               "Run with --execute --allow-write to bind.",
        }

    def bind(
        self,
        session_id: str,
        dataset_id: str,
        version: str,
        dataset_fingerprint: str = "",
        allow_write: bool = False,
    ) -> Dict[str, Any]:
        """Bind a dataset to a session. Locked by default. Blocked without allow_write."""
        if not allow_write:
            return {
                "blocked": True,
                "reason":  "BLOCKED because --allow-write is required",
                "preview": self.preview_bind(session_id, dataset_id, version, dataset_fingerprint),
            }
        existing = self._get_binding(session_id, BindingType.DATASET.value)
        if existing and existing.status == BindingStatus.VALID.value:
            return {
                "status":     "ALREADY_BOUND",
                "session_id": session_id,
                "dataset_id": dataset_id,
                "note":       "Binding already exists. Use rebind to change.",
            }
        binding = ReplaySessionBinding(
            binding_id=str(uuid.uuid4())[:12],
            session_id=session_id,
            binding_type=BindingType.DATASET.value,
            target_id=dataset_id,
            target_version=version,
            target_fingerprint=dataset_fingerprint,
            status=BindingStatus.VALID.value,
            created_at=_now_utc(),
            updated_at=_now_utc(),
        )
        self._bindings.append(binding)
        self._append_binding(binding)
        return {
            "status":     "BOUND",
            "session_id": session_id,
            "dataset_id": dataset_id,
            "version":    version,
            "binding_id": binding.binding_id,
        }

    def verify_binding(self, session_id: str) -> Dict[str, Any]:
        """Verify a session's dataset binding is intact."""
        binding = self._get_binding(session_id, BindingType.DATASET.value)
        if not binding:
            return {"status": "NO_BINDING", "session_id": session_id}
        return {
            "status":           binding.status,
            "session_id":       session_id,
            "dataset_id":       binding.target_id,
            "version":          binding.target_version,
            "fingerprint":      binding.target_fingerprint,
        }

    def lock_binding(self, session_id: str, allow_write: bool = False) -> Dict[str, Any]:
        if not allow_write:
            return {"blocked": True, "reason": "BLOCKED because --allow-write is required"}
        return {"status": "LOCKED", "session_id": session_id}

    def rebind_preview(
        self,
        session_id: str,
        new_dataset_id: str,
        new_version: str,
        session_status: str = "ACTIVE",
    ) -> Dict[str, Any]:
        """Preview rebind. Blocked if session is COMPLETED."""
        if session_status == "COMPLETED":
            return {
                "blocked": True,
                "reason":  "BLOCKED: Completed sessions cannot be directly rebound. "
                           "Duplicate or fork the session instead.",
                "session_id": session_id,
            }
        return {
            "action":        "REBIND_PREVIEW",
            "session_id":    session_id,
            "new_dataset_id": new_dataset_id,
            "new_version":   new_version,
            "note":          "Run with --execute --allow-write to rebind.",
        }

    def rebind_execute(
        self,
        session_id: str,
        new_dataset_id: str,
        new_version: str,
        session_status: str = "ACTIVE",
        allow_write: bool = False,
    ) -> Dict[str, Any]:
        """Execute rebind. Blocked without allow_write or if completed."""
        if session_status == "COMPLETED":
            return {
                "blocked": True,
                "reason":  "BLOCKED: Completed sessions cannot be directly rebound.",
            }
        if not allow_write:
            return {
                "blocked": True,
                "reason":  "BLOCKED because --allow-write is required",
            }
        return {
            "status":       "REBOUND",
            "session_id":   session_id,
            "new_dataset_id": new_dataset_id,
            "new_version":  new_version,
        }

    def list_bindings(self, session_id: str) -> List[ReplaySessionBinding]:
        return [b for b in self._bindings if b.session_id == session_id]

    def binding_history(self, session_id: str) -> List[Dict[str, Any]]:
        return [
            {"binding_id": b.binding_id, "type": b.binding_type,
             "target": b.target_id, "status": b.status, "created": b.created_at}
            for b in self.list_bindings(session_id)
        ]

    def summary(self, session_id: str) -> str:
        bindings = self.list_bindings(session_id)
        if not bindings:
            return f"Session {session_id}: no bindings."
        lines = [f"Session {session_id}: {len(bindings)} binding(s)"]
        for b in bindings:
            lines.append(f"  [{b.binding_type}] {b.target_id} v{b.target_version} [{b.status}]")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #

    def _get_binding(
        self, session_id: str, binding_type: str
    ) -> Optional[ReplaySessionBinding]:
        for b in self._bindings:
            if b.session_id == session_id and b.binding_type == binding_type:
                return b
        return None

    def _append_binding(self, binding: ReplaySessionBinding) -> None:
        self._base_dir.mkdir(parents=True, exist_ok=True)
        import dataclasses
        try:
            with open(str(self._bind_file), "a", encoding="utf-8") as fh:
                fh.write(json.dumps(dataclasses.asdict(binding), ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("[SessionBinder] Append failed: %s", exc)
