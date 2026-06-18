"""
replay/challenge_attempt.py — Attempt manager v1.2.7

Append-only action log. Create/save/load attempt state.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ChallengeAttemptManager:
    """
    Manages challenge attempt lifecycle: create, save, load, append actions.

    Action log is append-only.
    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    APPEND_ONLY_ACTIONS = True

    def __init__(self) -> None:
        self._attempts: Dict[str, Dict[str, Any]] = {}
        self._action_logs: Dict[str, List[Dict[str, Any]]] = {}

    def create(self, challenge_id: str, user_label: str = "") -> Dict[str, Any]:
        """Create a new attempt."""
        from replay.challenge_schema import ReplayChallengeAttempt, AttemptStatus, _now_utc
        attempt = ReplayChallengeAttempt(
            challenge_id=challenge_id,
            user_label=user_label,
            status=AttemptStatus.NOT_STARTED,
        )
        d = attempt.to_dict()
        self._attempts[attempt.attempt_id] = d
        self._action_logs[attempt.attempt_id] = []
        return {"status": "CREATED", "attempt_id": attempt.attempt_id, "attempt": d}

    def save(self, attempt: Dict[str, Any]) -> Dict[str, Any]:
        """Save (overwrite) attempt state."""
        aid = attempt.get("attempt_id", "")
        if not aid:
            return {"status": "ERROR", "message": "attempt_id required"}
        attempt["research_only"] = True
        attempt["no_real_orders"] = True
        self._attempts[aid] = attempt
        return {"status": "SAVED", "attempt_id": aid}

    def load(self, attempt_id: str) -> Optional[Dict[str, Any]]:
        """Load attempt state."""
        return self._attempts.get(attempt_id)

    def append_action(self, attempt_id: str, action: Dict[str, Any]) -> Dict[str, Any]:
        """Append action to the log (append-only)."""
        if attempt_id not in self._action_logs:
            self._action_logs[attempt_id] = []
        action["simulation_decision_only"] = True
        action["no_paper_order"] = True
        action["no_broker_order"] = True
        self._action_logs[attempt_id].append(action)
        # Update action count in attempt
        if attempt_id in self._attempts:
            self._attempts[attempt_id]["actions"] = self._action_logs[attempt_id]
        return {"status": "APPENDED", "attempt_id": attempt_id, "action_id": action.get("action_id")}

    def get_actions(self, attempt_id: str) -> List[Dict[str, Any]]:
        """Get all actions for an attempt."""
        return list(self._action_logs.get(attempt_id, []))

    def list_attempts(self) -> List[Dict[str, Any]]:
        """List all attempts."""
        return list(self._attempts.values())

    def count_attempts_for_challenge(self, challenge_id: str) -> int:
        """Count attempts for a challenge."""
        return sum(
            1 for a in self._attempts.values()
            if a.get("challenge_id") == challenge_id
        )

    def summary(self) -> Dict[str, Any]:
        total = len(self._attempts)
        statuses: Dict[str, int] = {}
        for a in self._attempts.values():
            s = a.get("status", "UNKNOWN")
            statuses[s] = statuses.get(s, 0) + 1
        return {
            "total_attempts": total,
            "by_status": statuses,
            "append_only_actions": True,
            "research_only": True,
            "no_real_orders": True,
        }
