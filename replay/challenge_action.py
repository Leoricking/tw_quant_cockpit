"""
replay/challenge_action.py — Challenge action log manager v1.2.7

Append-only. Records all actions with timestamps.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ChallengeActionLogManager:
    """
    Append-only action log manager for challenge attempts.

    [!] All trading action types are SIMULATION DECISION ONLY.
    [!] Append-only: actions cannot be deleted or modified.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    APPEND_ONLY = True

    def __init__(self) -> None:
        self._logs: Dict[str, List[Dict[str, Any]]] = {}

    def append(self, attempt_id: str, action: Dict[str, Any], elapsed: float = 0.0) -> Dict[str, Any]:
        """Append an action to the log."""
        from replay.challenge_schema import ReplayChallengeAction, ActionType, _now_utc
        if attempt_id not in self._logs:
            self._logs[attempt_id] = []

        prev_elapsed = (
            self._logs[attempt_id][-1].get("elapsed_since_start", 0.0)
            if self._logs[attempt_id] else 0.0
        )

        entry = {
            "action_id": action.get("action_id") or f"ACT-{len(self._logs[attempt_id]):04d}",
            "attempt_id": attempt_id,
            "replay_timestamp": action.get("replay_timestamp"),
            "action_type": action.get("action_type", "VIEW_CONTEXT"),
            "payload": action.get("payload", {}),
            "elapsed_since_start": elapsed,
            "elapsed_since_previous_action": elapsed - prev_elapsed,
            "point_in_time_verified": action.get("point_in_time_verified", False),
            "created_at": action.get("created_at") or _now_utc(),
            "simulation_decision_only": True,
            "no_paper_order": True,
            "no_broker_order": True,
        }
        self._logs[attempt_id].append(entry)
        return {"status": "APPENDED", "action_id": entry["action_id"], "count": len(self._logs[attempt_id])}

    def get_log(self, attempt_id: str) -> List[Dict[str, Any]]:
        """Return all actions for an attempt."""
        return list(self._logs.get(attempt_id, []))

    def count(self, attempt_id: str) -> int:
        return len(self._logs.get(attempt_id, []))

    def last_action(self, attempt_id: str) -> Dict[str, Any]:
        log = self._logs.get(attempt_id, [])
        return log[-1] if log else {}

    def summary(self, attempt_id: str) -> Dict[str, Any]:
        log = self._logs.get(attempt_id, [])
        by_type: Dict[str, int] = {}
        for a in log:
            t = a.get("action_type", "UNKNOWN")
            by_type[t] = by_type.get(t, 0) + 1
        return {
            "attempt_id": attempt_id,
            "total_actions": len(log),
            "by_type": by_type,
            "append_only": True,
            "research_only": True,
            "no_real_orders": True,
        }
