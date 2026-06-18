"""
replay/session_registry_summary.py — ReplaySessionRegistrySummary v1.2.8

Generates text summaries of session registry state.

[!] Research Only. No Real Orders. Session Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplaySessionRegistrySummary:
    """
    Text summaries of the session registry.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, registry=None):
        self._registry = registry

    def full_summary(self) -> str:
        if self._registry is None:
            return "Session Registry: not initialized."
        sessions = self._registry.list()
        total     = len(sessions)
        completed = sum(1 for s in sessions if s.session_status == "COMPLETED")
        orphaned  = sum(1 for s in sessions if s.session_status == "ORPHANED")
        bound     = sum(1 for s in sessions if s.dataset_id)
        unbound   = total - bound
        dupes     = len(self._registry.detect_duplicates())
        broken    = len(self._registry.detect_broken_references())
        lines = [
            "=" * 60,
            "  Replay Session Registry Summary v1.2.8",
            "  [!] Session Registry Only | No Real Orders",
            "=" * 60,
            f"  Total sessions:    {total}",
            f"  Completed:         {completed}",
            f"  Orphaned:          {orphaned}",
            f"  Dataset-bound:     {bound}",
            f"  Unbound:           {unbound}",
            f"  Possible dupes:    {dupes}",
            f"  Broken refs:       {broken}",
            "=" * 60,
        ]
        return "\n".join(lines)

    def per_session(self, session_id: str) -> str:
        if self._registry is None:
            return f"Session {session_id}: registry not initialized."
        s = self._registry.get(session_id)
        if s is None:
            return f"Session {session_id}: NOT FOUND."
        return (
            f"Session: {s.session_id}\n"
            f"  Type:             {s.session_type}\n"
            f"  Status:           {s.session_status}\n"
            f"  Symbol:           {s.symbol}\n"
            f"  Dataset:          {s.dataset_id or 'UNBOUND'}\n"
            f"  Dataset Version:  {s.dataset_version or '-'}\n"
            f"  Session FP:       {(s.session_fingerprint or '')[:16]}...\n"
            f"  Dataset FP:       {(s.dataset_fingerprint or '')[:16]}...\n"
            f"  Warnings:         {s.warnings}"
        )
