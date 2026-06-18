"""
replay/registry_audit.py — ReplayRegistryAudit v1.2.8

Generates and reads audit records for the registry.
Audit is append-only.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import json
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


class ReplayRegistryAudit:
    """
    Records and reads audit events for the registry.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: str = "."):
        self._repo_root = repo_root
        self._base_dir  = Path(repo_root) / "data" / "replay_registry"
        self._audit_file = self._base_dir / "registry_audit.jsonl"

    def record(
        self,
        event_type: str,
        dataset_id: Optional[str] = None,
        dataset_version: Optional[str] = None,
        session_id: Optional[str] = None,
        fingerprint: Optional[str] = None,
        package_id: Optional[str] = None,
        status: str = "OK",
        warnings: Optional[List[str]] = None,
        elapsed_seconds: float = 0.0,
    ) -> Dict[str, Any]:
        """Record an audit event."""
        event = {
            "event_id":        str(uuid.uuid4())[:12],
            "event_type":      event_type,
            "dataset_id":      dataset_id,
            "dataset_version": dataset_version,
            "session_id":      session_id,
            "fingerprint":     fingerprint,
            "package_id":      package_id,
            "status":          status,
            "warnings":        warnings or [],
            "elapsed_seconds": elapsed_seconds,
            "created_at":      _now_utc(),
            "research_only":   True,
            "no_real_orders":  True,
        }
        self._append(event)
        return event

    def list_events(
        self,
        event_type: Optional[str] = None,
        dataset_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        events = self._load_all()
        if event_type:
            events = [e for e in events if e.get("event_type") == event_type]
        if dataset_id:
            events = [e for e in events if e.get("dataset_id") == dataset_id]
        if session_id:
            events = [e for e in events if e.get("session_id") == session_id]
        return events

    def summary(self) -> str:
        events = self._load_all()
        by_type: Dict[str, int] = {}
        for e in events:
            et = e.get("event_type", "UNKNOWN")
            by_type[et] = by_type.get(et, 0) + 1
        lines = [f"Registry Audit: {len(events)} events"]
        for et, cnt in sorted(by_type.items()):
            lines.append(f"  {et}: {cnt}")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #

    def _append(self, event: Dict[str, Any]) -> None:
        self._base_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(str(self._audit_file), "a", encoding="utf-8") as fh:
                fh.write(json.dumps(event, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("[RegistryAudit] Append failed: %s", exc)

    def _load_all(self) -> List[Dict[str, Any]]:
        events = []
        if not self._audit_file.exists():
            return events
        try:
            with open(str(self._audit_file), "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        events.append(json.loads(line))
                    except Exception:
                        pass  # graceful corrupted tail
        except Exception as exc:
            logger.warning("[RegistryAudit] Load failed: %s", exc)
        return events
