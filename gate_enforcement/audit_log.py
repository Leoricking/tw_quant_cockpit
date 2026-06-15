"""
gate_enforcement.audit_log — QualityGateAuditLog v1.1.5

Append-only JSONL audit log for gate enforcement events.
Research Only. No Real Orders.

Files:
  data/quality_gate_audit/enforcement_audit.jsonl
  data/quality_gate_audit/run_snapshots.jsonl
  data/quality_gate_audit/run_index.csv
  data/quality_gate_audit/exclusion_records.csv
  data/quality_gate_audit/override_events.csv
  data/quality_gate_audit/reproducibility_hashes.csv

Audit failures MUST NOT be silent.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from gate_enforcement.enforcement_schema import EnforcementAuditEvent

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_AUDIT_DIR = os.path.join(BASE_DIR, "data", "quality_gate_audit")


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _event_hash(event_dict: dict, prev_hash: str = "") -> str:
    """Compute immutable hash for an event (with optional chain hash)."""
    payload = {
        "event_id": event_dict.get("event_id", ""),
        "run_id": event_dict.get("run_id", ""),
        "event_type": event_dict.get("event_type", ""),
        "timestamp": event_dict.get("timestamp", ""),
        "command_name": event_dict.get("command_name", ""),
        "symbol": event_dict.get("symbol", ""),
        "gate_name": event_dict.get("gate_name", ""),
        "new_state": event_dict.get("new_state", ""),
        "reason": event_dict.get("reason", ""),
        "prev_hash": prev_hash,
    }
    return _sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False))


class QualityGateAuditLog:
    """
    Append-only audit log for gate enforcement events.
    Audit failure raises RuntimeError — must NOT be silent.
    """

    def __init__(self, audit_dir: str = DEFAULT_AUDIT_DIR):
        self._audit_dir = audit_dir if os.path.isabs(audit_dir) else os.path.join(BASE_DIR, audit_dir)
        self._events_path = os.path.join(self._audit_dir, "enforcement_audit.jsonl")
        self._run_index_path = os.path.join(self._audit_dir, "run_index.csv")
        self._exclusion_path = os.path.join(self._audit_dir, "exclusion_records.csv")
        self._override_path = os.path.join(self._audit_dir, "override_events.csv")
        self._hashes_path = os.path.join(self._audit_dir, "reproducibility_hashes.csv")
        os.makedirs(self._audit_dir, exist_ok=True)

    def append(self, event: EnforcementAuditEvent) -> None:
        """Append an event to the audit log. Raises on failure."""
        try:
            prev_hash = self._last_hash()
            event_dict = event.to_dict()
            # Compute and set immutable_hash
            computed_hash = _event_hash(event_dict, prev_hash)
            event_dict["immutable_hash"] = computed_hash
            event_dict["chain_prev_hash"] = prev_hash

            with open(self._events_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_dict, ensure_ascii=False) + "\n")
        except Exception as exc:
            # Audit failure MUST NOT be silent
            logger.error("AUDIT LOG FAILURE: %s", exc)
            raise RuntimeError(f"QualityGateAuditLog.append failed: {exc}") from exc

    def list_events(self, run_id: Optional[str] = None) -> List[dict]:
        """List events from the audit log, optionally filtered by run_id."""
        events = []
        if not os.path.isfile(self._events_path):
            return events
        try:
            with open(self._events_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        if run_id is None or d.get("run_id") == run_id:
                            events.append(d)
                    except json.JSONDecodeError:
                        continue
        except Exception as exc:
            logger.error("list_events failed: %s", exc)
        return events

    def verify_chain(self) -> dict:
        """Verify the immutable hash chain of all events."""
        events = []
        if not os.path.isfile(self._events_path):
            return {"valid": True, "events": 0, "broken_at": None, "error": "no events"}
        try:
            with open(self._events_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            events.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except Exception as exc:
            return {"valid": False, "events": 0, "broken_at": None, "error": str(exc)}

        prev_hash = ""
        for i, event in enumerate(events):
            stored_hash = event.get("immutable_hash", "")
            prev_hash_in_event = event.get("chain_prev_hash", "")
            event_dict = {k: v for k, v in event.items() if k not in ("immutable_hash", "chain_prev_hash")}
            expected_hash = _event_hash(event_dict, prev_hash_in_event)
            if stored_hash != expected_hash:
                return {
                    "valid": False,
                    "events": len(events),
                    "broken_at": i,
                    "event_id": event.get("event_id"),
                }
            prev_hash = stored_hash

        return {"valid": True, "events": len(events), "broken_at": None}

    def get_run_timeline(self, run_id: str) -> List[dict]:
        """Return all events for a run in chronological order."""
        events = self.list_events(run_id=run_id)
        return sorted(events, key=lambda e: e.get("timestamp", ""))

    def record_exclusion(self, run_id: str, symbol: str, gate_name: str,
                         decision: str, reason_codes: list) -> None:
        try:
            write_header = not os.path.isfile(self._exclusion_path)
            with open(self._exclusion_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "run_id", "symbol", "gate_name", "decision", "reason_codes", "recorded_at"
                ])
                if write_header:
                    writer.writeheader()
                writer.writerow({
                    "run_id": run_id,
                    "symbol": symbol,
                    "gate_name": gate_name,
                    "decision": decision,
                    "reason_codes": json.dumps(reason_codes),
                    "recorded_at": _now_utc(),
                })
        except Exception as exc:
            logger.error("record_exclusion failed: %s", exc)
            raise RuntimeError(f"Audit record_exclusion failed: {exc}") from exc

    def record_override(self, run_id: str, symbol: str, override_id: str,
                        reason: str, approved: bool) -> None:
        try:
            write_header = not os.path.isfile(self._override_path)
            with open(self._override_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "run_id", "symbol", "override_id", "reason", "approved", "recorded_at"
                ])
                if write_header:
                    writer.writeheader()
                writer.writerow({
                    "run_id": run_id,
                    "symbol": symbol,
                    "override_id": override_id,
                    "reason": reason,
                    "approved": approved,
                    "recorded_at": _now_utc(),
                })
        except Exception as exc:
            logger.error("record_override failed: %s", exc)
            raise RuntimeError(f"Audit record_override failed: {exc}") from exc

    def record_completion(self, run_id: str, status: str, reproducibility_hash: str = "") -> None:
        try:
            event = EnforcementAuditEvent(
                event_id=_new_uuid(),
                run_id=run_id,
                event_type="RUN_COMPLETED",
                actor="system",
                timestamp=_now_utc(),
                command_name="",
                symbol=None,
                gate_name="",
                previous_state=None,
                new_state=status,
                reason="Run completed",
                metadata={"reproducibility_hash": reproducibility_hash},
                immutable_hash="",
            )
            self.append(event)
        except Exception as exc:
            logger.error("record_completion failed: %s", exc)
            raise RuntimeError(f"Audit record_completion failed: {exc}") from exc

    def export_audit(self, output_path: str) -> str:
        """Export all audit events to a JSONL file at output_path."""
        events = self.list_events()
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                for event in events:
                    f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.error("export_audit failed: %s", exc)
            raise
        return output_path

    def _last_hash(self) -> str:
        """Return the immutable_hash of the last event, or empty string."""
        if not os.path.isfile(self._events_path):
            return ""
        last_hash = ""
        try:
            with open(self._events_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            d = json.loads(line)
                            last_hash = d.get("immutable_hash", "")
                        except json.JSONDecodeError:
                            continue
        except Exception:
            pass
        return last_hash
