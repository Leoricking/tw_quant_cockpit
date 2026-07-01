"""
paper_trading/multi_session/degraded_mode_v166.py — Degraded Mode v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List

RESEARCH_ONLY = True
PAPER_ONLY = True
NO_REAL_ORDERS = True


@dataclass
class DegradedModeRecord:
    session_id: str
    degraded_at: datetime
    reason: str
    capabilities_disabled: List[str]
    safe_capabilities: List[str]
    verification_required_before_restore: bool = True


class DegradedModeCoordinator:
    """Manages degraded mode for sessions. Verification required before restore."""

    def __init__(self) -> None:
        self._degraded: Dict[str, DegradedModeRecord] = {}

    def enter_degraded(
        self,
        session_id: str,
        reason: str,
        disable_capabilities: List[str],
        safe_capabilities: List[str],
    ) -> DegradedModeRecord:
        record = DegradedModeRecord(
            session_id=session_id,
            degraded_at=datetime.now(timezone.utc),
            reason=reason,
            capabilities_disabled=disable_capabilities,
            safe_capabilities=safe_capabilities,
        )
        self._degraded[session_id] = record
        return record

    def is_degraded(self, session_id: str) -> bool:
        return session_id in self._degraded

    def get_record(self, session_id: str) -> DegradedModeRecord:
        return self._degraded[session_id]

    def exit_degraded(self, session_id: str, verified: bool) -> bool:
        if not verified:
            return False
        if session_id in self._degraded:
            del self._degraded[session_id]
        return True

    def degraded_list(self) -> List[str]:
        return list(self._degraded.keys())
