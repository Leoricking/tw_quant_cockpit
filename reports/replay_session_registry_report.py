"""
reports/replay_session_registry_report.py — Session Registry report v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def build_session_registry_report(
    session_registry=None,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a session registry markdown report."""
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    markdown_lines = [
        f"# Session Registry Report — {date}",
        "",
        "[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.",
        "",
    ]

    try:
        if session_registry is None:
            from replay.session_registry_v128 import ReplaySessionRegistryV128
            session_registry = ReplaySessionRegistryV128()
        from replay.session_registry_summary import ReplaySessionRegistrySummary
        summary = ReplaySessionRegistrySummary().full_summary(session_registry)
        sessions = session_registry.list()

        total     = len(sessions)
        orphaned  = len(session_registry.detect_orphans())
        broken    = len(session_registry.detect_broken_references())
        completed = sum(1 for s in sessions
                        if (getattr(s, "status", None) or {}) == "COMPLETED"
                        or (isinstance(s, dict) and s.get("status") == "COMPLETED"))

        markdown_lines += [
            "## Summary",
            "",
            f"- Total sessions: {total}",
            f"- Completed: {completed}",
            f"- Orphaned: {orphaned}",
            f"- Broken references: {broken}",
            "",
            "## Session List",
            "",
        ]
        for s in sessions:
            sid = getattr(s, "session_id", None) or (s.get("session_id") if isinstance(s, dict) else "?")
            markdown_lines.append(f"- {sid}")
    except Exception as exc:
        logger.warning("build_session_registry_report failed: %s", exc)
        markdown_lines.append(f"Report generation failed: {exc}")

    return {
        "report_type":   "SESSION_REGISTRY_REPORT",
        "report_date":   date,
        "markdown":      "\n".join(markdown_lines),
        "research_only": True,
        "no_real_orders": True,
        "version":       "1.2.8",
    }


def build_session_summary(session_registry=None) -> Dict[str, Any]:
    """Return concise session summary dict."""
    try:
        if session_registry is None:
            from replay.session_registry_v128 import ReplaySessionRegistryV128
            session_registry = ReplaySessionRegistryV128()
        from replay.session_registry_summary import ReplaySessionRegistrySummary
        return ReplaySessionRegistrySummary().full_summary(session_registry)
    except Exception as exc:
        logger.warning("build_session_summary failed: %s", exc)
        return {"error": str(exc), "research_only": True}


def get_session_rows(session_registry=None) -> List[Dict[str, Any]]:
    """Return list of session dicts for table display."""
    try:
        if session_registry is None:
            from replay.session_registry_v128 import ReplaySessionRegistryV128
            session_registry = ReplaySessionRegistryV128()
        sessions = session_registry.list()
        return [vars(s) if hasattr(s, "__dict__") else s for s in sessions]
    except Exception as exc:
        logger.warning("get_session_rows failed: %s", exc)
        return []
