"""
replay/session_portability.py — ReplaySessionPortability v1.2.1

Handles cross-computer metadata export/import.
Supports: D:/code/Claude/tw_quant_cockpit, C:/Users/Rossi/Documents/Claude/trading_master
Prefers repo-relative paths. Keeps original_local_path as metadata.
Import: metadata only (no market data, no DB, no full OHLCV history).
Export: excludes secrets, broker config, future data.
Missing local price data: marks session DATA_UNAVAILABLE.
Import does NOT auto-execute session.

[!] Research Only. No Real Orders. Replay Training Only.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

SENSITIVE_FIELDS = [
    "api_key", "secret", "broker", "order_token", "password",
    "future_return", "realized_pnl", "outcome", "final_label",
]

KNOWN_REPO_ROOTS = [
    "D:/code/Claude/tw_quant_cockpit",
    "C:/Users/Rossi/Documents/Claude/trading_master",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplaySessionPortability:
    """
    Handles cross-computer metadata export/import.
    Prefers repo-relative paths. Keeps original_local_path as metadata.
    Import: metadata only. Does NOT auto-execute.
    Missing local price data: marks DATA_UNAVAILABLE.
    """

    KNOWN_REPO_ROOTS = KNOWN_REPO_ROOTS
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, store=None, repo_root: Optional[str] = None):
        self._store = store
        self._repo_root = repo_root or "."

    def export_metadata(self, session_id: str, output_path: Optional[str] = None) -> Optional[str]:
        if self._store is None:
            return None
        config = self._store.load_session_config(session_id)
        state = self._store.load_session_state(session_id)
        if config is None:
            return None

        payload = {
            "session_id": session_id,
            "config": self.redact_sensitive_fields(config),
            "state": self.redact_sensitive_fields(state or {}),
            "export_version": "1.2.1",
            "exported_at": _now_utc(),
            "original_local_path": str(Path(self._repo_root).resolve()),
            "portable_metadata_version": 1,
            "research_only": True,
            "no_real_orders": True,
            "import_does_not_auto_execute": True,
        }

        if output_path is None:
            exports_dir = Path(self._repo_root) / "data" / "replay_sessions" / "session_exports"
            exports_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(exports_dir / f"{session_id}_export.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return output_path

    def import_metadata(self, path: str, dry_run: bool = True) -> Dict[str, Any]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except Exception as exc:
            return {"ok": False, "error": str(exc), "dry_run": dry_run}

        errors = self.validate_payload(payload)
        if errors:
            return {"ok": False, "errors": errors, "dry_run": dry_run}

        payload = self.normalize_paths(payload)
        session_id = payload.get("session_id", "")

        if not dry_run and self._store and session_id:
            config = payload.get("config", {})
            state = payload.get("state", {})
            # Mark as DATA_UNAVAILABLE if local data may be missing
            if state:
                state["qualification"] = "DATA_UNAVAILABLE"
            # Save to store
            try:
                from replay.replay_schema import ReplaySessionConfig, ReplaySessionState
                cfg_obj = ReplaySessionConfig.from_dict(config)
                self._store.save_session_config(cfg_obj)
                if state:
                    state_obj = ReplaySessionState.from_dict(state)
                    self._store.save_session_state(state_obj)
            except Exception as exc:
                logger.warning("[Portability] import failed: %s", exc)
                return {"ok": False, "error": str(exc), "dry_run": dry_run}

        return {
            "ok": True,
            "session_id": session_id,
            "dry_run": dry_run,
            "import_does_not_auto_execute": True,
            "qualification": "DATA_UNAVAILABLE",
        }

    def normalize_paths(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize paths from known repo roots to repo-relative."""
        original = payload.get("original_local_path", "")
        current_root = str(Path(self._repo_root).resolve())

        def _normalize(v):
            if isinstance(v, str):
                for root in KNOWN_REPO_ROOTS:
                    if v.startswith(root):
                        rel = v[len(root):].lstrip("/\\")
                        return os.path.join(current_root, rel)
            return v

        def _walk(obj):
            if isinstance(obj, dict):
                return {k: _walk(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_walk(i) for i in obj]
            return _normalize(obj)

        return _walk(payload)

    def to_repo_relative(self, path: str) -> str:
        for root in KNOWN_REPO_ROOTS:
            if path.startswith(root):
                return path[len(root):].lstrip("/\\")
        return path

    def resolve_repo_relative(self, path: str) -> str:
        if os.path.isabs(path):
            return path
        return str(Path(self._repo_root) / path)

    def validate_payload(self, payload: Dict[str, Any]) -> List[str]:
        errors = []
        if not payload.get("session_id"):
            errors.append("session_id missing")
        # Check for sensitive fields
        sensitive = self.redact_sensitive_fields(payload)
        for f in SENSITIVE_FIELDS:
            if f in payload:
                errors.append(f"Sensitive field found: {f}")
        return errors

    def redact_sensitive_fields(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        def _redact(obj):
            if isinstance(obj, dict):
                return {k: ("[REDACTED]" if k in SENSITIVE_FIELDS else _redact(v)) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_redact(i) for i in obj]
            return obj
        return _redact(payload)

    def portability_report(self, session_id: str) -> Dict[str, Any]:
        return {
            "session_id": session_id,
            "current_repo_root": self._repo_root,
            "known_repo_roots": KNOWN_REPO_ROOTS,
            "export_available": self._store is not None,
            "research_only": True,
            "no_real_orders": True,
        }
