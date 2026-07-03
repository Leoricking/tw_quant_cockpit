"""
paper_trading/operational_integration/session_bridge_v168.py
Session Bridge for Operational Integration Hardening v1.6.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

_PAPER_SESSION_PREFIXES = ("paper_", "sim_", "research_", "test_", "demo_")


class SessionBridge:
    """Session validation and lineage bridge. Research only."""

    def __init__(self) -> None:
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def validate_session_identity(
        self, session_id: str, expected_components: List[str]
    ) -> Dict[str, Any]:
        """Validate that a session has all expected components registered."""
        if not session_id:
            return {"valid": False, "errors": ["missing session_id"], "paper_only": True}
        session = self._sessions.get(session_id, {})
        registered = session.get("components", [])
        missing = [c for c in expected_components if c not in registered]
        return {
            "valid": len(missing) == 0,
            "session_id": session_id,
            "missing_components": missing,
            "registered_count": len(registered),
            "paper_only": True,
        }

    def check_session_overlap(self, session_ids: List[str]) -> List[Dict[str, Any]]:
        """Check for overlapping time periods between sessions."""
        overlaps = []
        periods = []
        for sid in session_ids:
            session = self._sessions.get(sid, {})
            start = session.get("period_start", "")
            end = session.get("period_end", "")
            if start and end:
                periods.append((sid, start, end))
        for i in range(len(periods)):
            for j in range(i + 1, len(periods)):
                s1, start1, end1 = periods[i]
                s2, start2, end2 = periods[j]
                if start1 <= end2 and start2 <= end1:
                    overlaps.append({
                        "session_1": s1,
                        "session_2": s2,
                        "overlap_start": max(start1, start2),
                        "overlap_end": min(end1, end2),
                    })
        return overlaps

    def check_session_lineage(self, session_id: str) -> Dict[str, Any]:
        """Check lineage integrity for a session."""
        session = self._sessions.get(session_id, {})
        parent = session.get("parent_session_id", "")
        lineage_id = session.get("lineage_id", "")
        return {
            "session_id": session_id,
            "has_lineage": bool(lineage_id),
            "has_parent": bool(parent),
            "lineage_id": lineage_id,
            "parent_session_id": parent,
            "is_root": not bool(parent),
            "paper_only": True,
        }

    def is_paper_session(self, session_id: str) -> bool:
        """Return True if session_id is a paper/simulation session."""
        lower = session_id.lower()
        if any(lower.startswith(p) for p in _PAPER_SESSION_PREFIXES):
            return True
        session = self._sessions.get(session_id, {})
        return session.get("paper_only", False) or session.get("is_paper", False)

    def register_session(self, session_id: str, session_data: Dict[str, Any]) -> None:
        """Register session metadata. Always enforces paper_only=True."""
        enriched = dict(session_data)
        enriched["paper_only"] = True  # enforce — all sessions are paper-only
        self._sessions[session_id] = enriched

    def summarize(self, session_id: str) -> Dict[str, Any]:
        """Return summary for a specific session."""
        session = self._sessions.get(session_id, {})
        return {
            "session_id": session_id,
            "registered": session_id in self._sessions,
            "paper_only": session.get("paper_only", False),
            "period_start": session.get("period_start", ""),
            "period_end": session.get("period_end", ""),
            "components": session.get("components", []),
        }
