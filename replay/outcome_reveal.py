"""
replay/outcome_reveal.py — ReplayOutcomeRevealManager for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Default: BLOCKED (not revealed).
[!] Must have --reveal AND --confirm-review flags.
[!] Session must be completed (or PARTIAL_REVIEW if explicitly allowed).
[!] Does NOT modify original session snapshot or journal entry.
[!] Writes only to review store (data/replay_scoring/).
[!] AUTO_OUTCOME_REVEAL_ENABLED = False (invariant).
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_OUTCOME_REVEAL_ENABLED = False


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_reveal_id() -> str:
    return f"REV-{uuid.uuid4().hex[:12].upper()}"


class ReplayOutcomeRevealManager:
    """
    Manages outcome reveal for replay sessions.

    [!] Default: BLOCKED.
    [!] Must have reveal=True AND confirm_review=True.
    [!] Session must be completed.
    [!] Does NOT modify original session snapshot or journal entry.
    [!] Writes only to data/replay_scoring/.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    AUTO_OUTCOME_REVEAL_ENABLED = False

    def __init__(self, store=None):
        self._store = store

    def preview(
        self,
        session_id: str,
        session_state: Optional[Dict[str, Any]] = None,
        window_bars: int = 20,
    ) -> Dict[str, Any]:
        """
        Preview what would be revealed without actually revealing.
        Returns status and eligibility info — NO actual reveal happens.
        """
        state = session_state or {}
        eligible, reason = self._check_eligibility(state)

        return {
            "session_id": session_id,
            "action": "PREVIEW_ONLY",
            "eligible_for_reveal": eligible,
            "ineligible_reason": "" if eligible else reason,
            "window_bars": window_bars,
            "status": "BLOCKED" if not eligible else "ELIGIBLE",
            "note": (
                "This is a PREVIEW only. No reveal has occurred. "
                "Use --reveal --confirm-review to actually reveal."
            ),
            "simulation_only": True,
            "research_only": True,
            "auto_outcome_reveal_enabled": False,
        }

    def reveal(
        self,
        session_id: str,
        session_state: Optional[Dict[str, Any]] = None,
        session_config: Optional[Dict[str, Any]] = None,
        journal_entry: Optional[Dict[str, Any]] = None,
        reveal_flag: bool = False,
        confirm_review_flag: bool = False,
        window_bars: int = 20,
        notes: str = "",
    ) -> "OutcomeRevealRecord":
        """
        Reveal outcome for a session.
        Returns BLOCKED if flags are not set or session is not completed.
        Does NOT modify original session snapshot or journal entry.
        """
        from replay.scoring_schema import (
            OutcomeRevealRecord, OutcomeRevealStatus,
        )

        entry = journal_entry or {}
        state = session_state or {}
        config = session_config or {}

        # Guard: Must have both flags
        if not reveal_flag or not confirm_review_flag:
            logger.info(
                "Outcome reveal BLOCKED: reveal_flag=%s, confirm_review_flag=%s",
                reveal_flag, confirm_review_flag,
            )
            return OutcomeRevealRecord(
                reveal_id=_new_reveal_id(),
                session_id=session_id,
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=entry.get("symbol", config.get("symbol", "")),
                reveal_window_bars=window_bars,
                reveal_confirmed=False,
                confirm_review_flag=confirm_review_flag,
                status=OutcomeRevealStatus.BLOCKED.value,
                notes=(
                    "BLOCKED: --reveal and --confirm-review flags both required. "
                    f"reveal_flag={reveal_flag}, confirm_review_flag={confirm_review_flag}"
                ),
                revealed_by="USER",
            )

        # Guard: Session must be completed
        eligible, reason = self._check_eligibility(state)
        if not eligible:
            return OutcomeRevealRecord(
                reveal_id=_new_reveal_id(),
                session_id=session_id,
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=entry.get("symbol", config.get("symbol", "")),
                reveal_window_bars=window_bars,
                reveal_confirmed=False,
                confirm_review_flag=confirm_review_flag,
                status=OutcomeRevealStatus.BLOCKED.value,
                notes=f"BLOCKED: Session not eligible for reveal. {reason}",
                revealed_by="USER",
            )

        session_end_date = config.get("end_date", state.get("current_date", ""))
        outcome_summary = self._build_outcome_summary(state, config, window_bars)

        record = OutcomeRevealRecord(
            reveal_id=_new_reveal_id(),
            session_id=session_id,
            journal_entry_id=entry.get("journal_entry_id"),
            decision_id=entry.get("decision_id"),
            symbol=entry.get("symbol", config.get("symbol", "")),
            session_end_date=session_end_date,
            reveal_window_bars=window_bars,
            reveal_confirmed=True,
            confirm_review_flag=True,
            status=OutcomeRevealStatus.REVEALED.value,
            outcome_data_summary=outcome_summary,
            original_snapshot_unchanged=True,
            original_journal_unchanged=True,
            notes=notes,
            revealed_by="USER",
        )

        # Persist to store if available
        if self._store:
            try:
                self._store.append("reveal", record.to_dict())
            except Exception as exc:
                logger.warning("Failed to persist reveal record: %s", exc)

        return record

    def _check_eligibility(self, state: Dict[str, Any]) -> Tuple[bool, str]:
        status = state.get("status", "")
        completed = bool(state.get("completed", False))

        if completed or status == "COMPLETED":
            return True, ""
        elif status == "PARTIAL_REVIEW":
            return True, ""
        else:
            return False, (
                f"Session status={status!r}, completed={completed}. "
                "Session must be COMPLETED before outcome reveal."
            )

    def _build_outcome_summary(
        self,
        state: Dict[str, Any],
        config: Dict[str, Any],
        window_bars: int,
    ) -> str:
        symbol = config.get("symbol", "")
        end_date = config.get("end_date", "")
        current_date = state.get("current_date", "")
        return (
            f"Outcome window: {window_bars} bars after session end. "
            f"Symbol: {symbol}. Session end: {end_date or current_date}. "
            "Post-session market data available for review."
        )
