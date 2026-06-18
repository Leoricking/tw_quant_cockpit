"""
gui/replay_challenge_journal_panel.py — Challenge journal panel v1.2.7

Challenge-local journal draft only. Separated from official Journal.
Export only with explicit --execute --allow-write. Does NOT export outcome or answer key.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, Optional
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True

class ReplayChallengeJournalPanel:
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    SEPARATED_FROM_OFFICIAL_JOURNAL = True
    EXPORTS_OUTCOME = False
    EXPORTS_ANSWER_KEY = False
    def __init__(self) -> None:
        self._draft: Dict[str, Any] = {}
    def update_draft(self, field: str, value: Any) -> None:
        forbidden = {"outcome", "answer_key", "forward_return", "realized_pnl"}
        if field in forbidden:
            logger.warning("Attempted to write forbidden field '%s' to challenge journal draft", field)
            return
        self._draft[field] = value
    def get_draft(self) -> Dict[str, Any]:
        return dict(self._draft)
    def export_to_official(self, allow_write: bool = False) -> Dict[str, Any]:
        if not allow_write:
            return {"status": "BLOCKED", "message": "Export requires allow_write=True and --execute --allow-write"}
        export = {k: v for k, v in self._draft.items() if k not in {"outcome", "answer_key", "forward_return", "realized_pnl"}}
        export["challenge_mode"] = True
        export["simulation_only"] = True
        return {"status": "EXPORTED", "data": export, "outcome_exported": False, "answer_key_exported": False}
    def summary(self) -> dict:
        return {"draft_fields": list(self._draft.keys()), "separated_from_official": True, "exports_outcome": False, "exports_answer_key": False, "research_only": True}
