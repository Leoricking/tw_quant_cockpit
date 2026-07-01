"""
paper_trading/multi_session/pause_coordinator_v166.py — Pause Coordinator v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from paper_trading.multi_session.enums_v166 import SessionLifecycleState

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True
REQUIRE_EXPLICIT_PAUSE = True


class PauseCoordinator:
    """Manages explicit pause requests. No auto-pause."""

    def __init__(self) -> None:
        self._paused: Dict[str, Dict[str, Any]] = {}

    def request_pause(self, session_id: str, reason: str, actor: str) -> Dict[str, Any]:
        record = {
            "session_id": session_id,
            "reason": reason,
            "actor": actor,
            "requested_at": datetime.now(timezone.utc).isoformat(),
            "status": "paused",
        }
        self._paused[session_id] = record
        return record

    def is_paused(self, session_id: str) -> bool:
        return session_id in self._paused

    def resume_eligible(self, session_id: str, checks: Dict[str, bool]) -> bool:
        required = ["safety_ok", "conflict_ok", "resource_ok", "risk_ok", "state_verified"]
        return all(checks.get(k, False) for k in required)

    def release_pause(self, session_id: str, checks: Dict[str, bool]) -> Dict[str, Any]:
        if not self.resume_eligible(session_id, checks):
            return {"released": False, "reason": "eligibility_checks_failed", "failed_checks": [k for k in checks if not checks[k]]}
        if session_id in self._paused:
            del self._paused[session_id]
        return {"released": True, "session_id": session_id}

    def paused_list(self) -> List[str]:
        return list(self._paused.keys())
