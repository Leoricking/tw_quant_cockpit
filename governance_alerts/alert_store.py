"""
governance_alerts.alert_store — GovernanceAlertStore v1.1.7

Append-only storage for alerts, transitions, digests, and checklists.
Atomic writes for state/index. Corrupt tail handled gracefully.

Runtime outputs (NOT committed):
  data/governance_alerts/alerts.jsonl
  data/governance_alerts/alert_transitions.jsonl
  data/governance_alerts/alert_index.csv
  data/governance_alerts/open_alerts.csv
  data/governance_alerts/escalations.csv
  data/governance_alerts/digests.jsonl
  data/governance_alerts/daily_checklists.jsonl
  data/governance_alerts/daily_metrics.csv
  data/governance_alerts/notification_previews/
  data/governance_alerts/alert_state.json

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Append-only. History cannot be overwritten.
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_STORE_DIR = os.path.join(BASE_DIR, "data", "governance_alerts")


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _transition_hash(t_dict: dict, prev_hash: str = "") -> str:
    payload = {
        "transition_id": t_dict.get("transition_id", ""),
        "alert_id": t_dict.get("alert_id", ""),
        "from_status": t_dict.get("from_status", ""),
        "to_status": t_dict.get("to_status", ""),
        "timestamp": t_dict.get("timestamp", ""),
        "prev_hash": prev_hash,
    }
    return _sha256(json.dumps(payload, sort_keys=True))


class GovernanceAlertStore:
    """Append-only storage for governance alerts and state transitions.

    [!] Research Only. No Real Orders.
    [!] Alert and transition history cannot be overwritten.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, store_dir: Optional[str] = None):
        self._dir = store_dir or DEFAULT_STORE_DIR
        self._alerts_file = os.path.join(self._dir, "alerts.jsonl")
        self._transitions_file = os.path.join(self._dir, "alert_transitions.jsonl")
        self._state_file = os.path.join(self._dir, "alert_state.json")
        self._digests_file = os.path.join(self._dir, "digests.jsonl")
        self._checklists_file = os.path.join(self._dir, "daily_checklists.jsonl")
        self._index_file = os.path.join(self._dir, "alert_index.csv")
        self._open_file = os.path.join(self._dir, "open_alerts.csv")
        self._escalations_file = os.path.join(self._dir, "escalations.csv")
        self._previews_dir = os.path.join(self._dir, "notification_previews")
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        try:
            os.makedirs(self._dir, exist_ok=True)
            os.makedirs(self._previews_dir, exist_ok=True)
        except Exception as exc:
            logger.warning("GovernanceAlertStore: cannot create dir: %s", exc)

    # -----------------------------------------------------------------------
    # Alert operations
    # -----------------------------------------------------------------------

    def upsert_alert(self, alert) -> None:
        """Append alert to JSONL (new write or update record)."""
        try:
            with open(self._alerts_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(alert.to_dict(), ensure_ascii=False) + "\n")
            self._update_state(alert)
        except Exception as exc:
            logger.warning("upsert_alert: %s", exc)

    def get_alert(self, alert_id: str):
        """Load the latest state of an alert by ID from state file."""
        state = self._load_state()
        d = state.get(alert_id)
        if d is None:
            return None
        try:
            from governance_alerts.alert_schema import GovernanceAlert
            return GovernanceAlert.from_dict(d)
        except Exception as exc:
            logger.warning("get_alert %s: %s", alert_id, exc)
            return None

    def list_open_alerts(self) -> List:
        """Return all currently open/active alerts from state."""
        state = self._load_state()
        alerts = []
        for alert_id, d in state.items():
            if d.get("status") not in ("RESOLVED", "SUPPRESSED"):
                try:
                    from governance_alerts.alert_schema import GovernanceAlert
                    alerts.append(GovernanceAlert.from_dict(d))
                except Exception:
                    pass
        return alerts

    def list_all_alerts(self) -> List:
        """Return all alerts from state file (all statuses)."""
        state = self._load_state()
        alerts = []
        for alert_id, d in state.items():
            try:
                from governance_alerts.alert_schema import GovernanceAlert
                alerts.append(GovernanceAlert.from_dict(d))
            except Exception:
                pass
        return alerts

    def query_alerts(self, priority: Optional[str] = None, status: Optional[str] = None,
                     alert_type: Optional[str] = None, symbol: Optional[str] = None,
                     source: Optional[str] = None) -> List:
        """Query alerts with optional filters."""
        alerts = self.list_all_alerts()
        if priority:
            alerts = [a for a in alerts if a.priority == priority.upper()]
        if status:
            alerts = [a for a in alerts if a.status == status.upper()]
        if alert_type:
            alerts = [a for a in alerts if a.alert_type == alert_type.upper()]
        if symbol:
            alerts = [a for a in alerts if a.symbol == str(symbol)]
        if source:
            alerts = [a for a in alerts if a.source == str(source)]
        return alerts

    # -----------------------------------------------------------------------
    # Transition operations (append-only, hash chain)
    # -----------------------------------------------------------------------

    def append_transition(self, transition) -> None:
        """Append a state transition to the JSONL (append-only)."""
        try:
            prev_hash = self._last_transition_hash()
            t_dict = transition.to_dict()
            t_dict["immutable_hash"] = _transition_hash(t_dict, prev_hash)
            transition.immutable_hash = t_dict["immutable_hash"]
            with open(self._transitions_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(t_dict, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("append_transition: %s", exc)

    def list_transitions(self, alert_id: Optional[str] = None) -> List:
        """Load all transitions (optionally filtered by alert_id)."""
        from governance_alerts.alert_schema import AlertStateTransition
        transitions = []
        if not os.path.isfile(self._transitions_file):
            return transitions
        try:
            with open(self._transitions_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        t = AlertStateTransition.from_dict(d)
                        if alert_id is None or t.alert_id == alert_id:
                            transitions.append(t)
                    except Exception:
                        continue
        except Exception as exc:
            logger.warning("list_transitions: %s", exc)
        return transitions

    def verify_transition_chain(self) -> dict:
        """Verify the hash chain integrity of all transitions."""
        transitions = self.list_transitions()
        if not transitions:
            return {"valid": True, "transitions": 0, "broken_at": None}

        prev_hash = ""
        for i, t in enumerate(transitions):
            expected = _transition_hash(t.to_dict(), prev_hash)
            actual = t.immutable_hash
            if actual and actual != expected:
                return {
                    "valid": False,
                    "transitions": len(transitions),
                    "broken_at": i,
                    "transition_id": t.transition_id,
                    "expected": expected[:8] + "...",
                    "actual": actual[:8] + "...",
                }
            prev_hash = actual or expected

        return {"valid": True, "transitions": len(transitions), "broken_at": None}

    def _last_transition_hash(self) -> str:
        """Return the hash of the last transition for chain linking."""
        if not os.path.isfile(self._transitions_file):
            return ""
        try:
            last_line = ""
            with open(self._transitions_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        last_line = line.strip()
            if last_line:
                d = json.loads(last_line)
                return d.get("immutable_hash", "")
        except Exception:
            pass
        return ""

    # -----------------------------------------------------------------------
    # Digest operations
    # -----------------------------------------------------------------------

    def append_digest(self, digest) -> None:
        """Append a digest to JSONL."""
        try:
            with open(self._digests_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(digest.to_dict(), ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("append_digest: %s", exc)

    def latest_digest(self, digest_type: Optional[str] = None):
        """Return the most recent digest (optionally filtered by type)."""
        from governance_alerts.alert_schema import GovernanceDigest
        if not os.path.isfile(self._digests_file):
            return None
        last = None
        try:
            with open(self._digests_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        if digest_type is None or d.get("digest_type") == digest_type.upper():
                            last = GovernanceDigest.from_dict(d)
                    except Exception:
                        continue
        except Exception as exc:
            logger.warning("latest_digest: %s", exc)
        return last

    # -----------------------------------------------------------------------
    # Checklist operations
    # -----------------------------------------------------------------------

    def append_checklist(self, checklist) -> None:
        """Append a checklist to JSONL."""
        try:
            with open(self._checklists_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(checklist.to_dict(), ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("append_checklist: %s", exc)

    def latest_checklist(self):
        """Return the most recent daily checklist."""
        from governance_alerts.alert_schema import DailyOperationsChecklist
        if not os.path.isfile(self._checklists_file):
            return None
        last = None
        try:
            with open(self._checklists_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        last = DailyOperationsChecklist.from_dict(d)
                    except Exception:
                        continue
        except Exception as exc:
            logger.warning("latest_checklist: %s", exc)
        return last

    def mark_checklist_item(self, checklist_id: str, item_id: str, status: str, note: str = "") -> bool:
        """Update a checklist item status. Metadata only."""
        cl = self.latest_checklist()
        if cl is None or cl.checklist_id != checklist_id:
            return False
        for item in cl.items:
            if item.item_id == item_id:
                item.status = status
                item.note = note
                if status == "COMPLETE":
                    item.completed_at = _now_utc()
                self.append_checklist(cl)
                return True
        return False

    # -----------------------------------------------------------------------
    # State management
    # -----------------------------------------------------------------------

    def _update_state(self, alert) -> None:
        """Update the alert state JSON (current state of each alert by ID)."""
        state = self._load_state()
        state[alert.alert_id] = alert.to_dict()
        self._save_state(state)

    def _load_state(self) -> Dict:
        if not os.path.isfile(self._state_file):
            return {}
        try:
            with open(self._state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("_load_state: corrupt or missing: %s", exc)
            return {}

    def _save_state(self, state: Dict) -> None:
        tmp = self._state_file + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self._state_file)
        except Exception as exc:
            logger.warning("_save_state: %s", exc)
            try:
                os.remove(tmp)
            except Exception:
                pass

    def save_notification_preview(self, preview_text: str, preview_type: str = "digest") -> str:
        """Save a notification preview to local file. No external send."""
        from datetime import datetime, timezone
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        fname = f"preview_{preview_type}_{ts}.md"
        fpath = os.path.join(self._previews_dir, fname)
        try:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(preview_text)
            return fpath
        except Exception as exc:
            logger.warning("save_notification_preview: %s", exc)
            return ""
