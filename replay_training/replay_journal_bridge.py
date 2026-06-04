"""replay_training/replay_journal_bridge.py — ReplayJournalBridge for TW Replay Training Cockpit v0.5.6.

Creates research/replay training journal entries only.
No real trade entries. No broker connection.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class ReplayJournalBridge:
    """Bridge between replay training sessions and the portfolio journal.

    Creates research/replay training journal entries only. No real trade entries.
    Graceful fallback if journal module not available.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self) -> None:
        self._journal_available: Optional[bool] = None

    def _check_journal(self) -> bool:
        if self._journal_available is None:
            try:
                import journal  # noqa: F401
                self._journal_available = True
            except ImportError:
                self._journal_available = False
        return self._journal_available

    def export_to_journal(self, session, ai_review, mistakes: list) -> dict:
        """Export a replay training session as a research journal entry.

        Returns dict with journal_entry_id (or None) and status.
        No real trade entries. No broker connection.
        """
        try:
            payload = self.build_journal_entry_payload(session, ai_review, mistakes)

            if not self._check_journal():
                return {
                    "ok":     True,
                    "status": "journal_module_unavailable",
                    "payload": payload,
                    "note":   "Journal module not available — payload built but not saved.",
                    "no_real_orders": True,
                }

            # Try to write via journal module (research entry only)
            try:
                from journal.journal_store import JournalStore
                store = JournalStore()
                entry_id = store.add_entry(
                    entry_type="replay_training",
                    symbol=session.symbol,
                    trade_date=session.trade_date,
                    note=payload.get("summary", ""),
                    tags="replay_training,research_only,no_real_orders",
                    extra=payload,
                )
                return {
                    "ok":               True,
                    "status":           "saved",
                    "journal_entry_id": entry_id,
                    "no_real_orders":   True,
                }
            except Exception as exc:
                logger.warning("[ReplayJournalBridge] journal save fallback: %s", exc)
                return {
                    "ok":     True,
                    "status": "save_failed_graceful",
                    "error":  str(exc),
                    "payload": payload,
                    "no_real_orders": True,
                }

        except Exception as exc:
            logger.error("[ReplayJournalBridge] export_to_journal error: %s", exc)
            return {
                "ok":     False,
                "error":  str(exc),
                "no_real_orders": True,
            }

    def build_journal_entry_payload(self, session, ai_review, mistakes: list) -> dict:
        """Build a research journal entry payload dict.

        No real trade fields. No BUY/SELL/ORDER data.
        """
        mistakes_list = [
            {"type": m.mistake_type, "severity": m.severity, "description": m.description}
            for m in (mistakes or [])
        ]

        summary = ""
        score   = 0.0
        drills  = ""
        if ai_review:
            summary = getattr(ai_review, "summary", "")
            score   = getattr(ai_review, "score",   0.0)
            drills  = getattr(ai_review, "suggested_drills", "")

        return {
            "entry_type":         "replay_training",
            "session_id":         session.session_id if session else "",
            "symbol":             session.symbol     if session else "",
            "trade_date":         session.trade_date if session else "",
            "timeframe":          session.timeframe  if session else "",
            "score":              score,
            "summary":            summary,
            "mistakes_count":     len(mistakes or []),
            "mistakes":           mistakes_list,
            "suggested_drills":   drills,
            "created_at":         datetime.now().isoformat(),
            "read_only":          True,
            "no_real_orders":     True,
            "production_blocked": True,
            "research_only":      True,
            "label": "Replay Training Only / Research Only / No Real Orders / No Broker Execution",
        }
