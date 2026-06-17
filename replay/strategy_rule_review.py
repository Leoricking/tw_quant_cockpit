"""
replay/strategy_rule_review.py — Rule review manager for v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
[!] All reviews start as SUGGESTED. System cannot auto-CONFIRM.
[!] Planned stop not auto-CONTRADICTED for No Panic Sell.
[!] Planned breakout not auto-chasing for No Chase.
[!] All operations are append-only.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_CONFIRM_ENABLED = False


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_review_id() -> str:
    return f"SRR-{uuid.uuid4().hex[:12].upper()}"


class StrategyRuleReviewManager:
    """
    Manages review records comparing strategy signals to decision actions.

    Rules:
    - All reviews start as SUGGESTED. System cannot auto-CONFIRM.
    - Has valid stop/invalidation plan → planned stop not CONTRADICTED.
    - Planned breakout entry → not auto-chasing.
    - WAIT/SKIP decisions → most NOT_APPLICABLE.
    - All operations are append-only.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    AUTO_CONFIRM_ENABLED = False

    def review_entry(
        self, journal_entry_id: str, journal_entry: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Create rule review records for a journal entry.
        Returns SUGGESTED records only.
        """
        from replay.strategy_replay_schema import StrategyRuleReviewRecord
        entry = journal_entry or {}
        session_id = entry.get("session_id", "")
        decision_id = entry.get("decision_id", "")
        replay_date = entry.get("replay_date", "")
        action = entry.get("action", "")
        snapshot = entry.get("strategy_signals_at_decision", {})
        modules = snapshot.get("modules", []) if isinstance(snapshot, dict) else []

        records = []
        for mod in modules:
            module_name = mod.get("module_name", "")
            rule_signal = mod.get("signal", "")
            if not rule_signal or rule_signal in ("UNAVAILABLE", "UNKNOWN"):
                continue
            relationship = self.build_relationship(module_name, rule_signal, action, entry)
            record = StrategyRuleReviewRecord(
                review_id=_new_review_id(),
                session_id=session_id,
                journal_entry_id=journal_entry_id,
                decision_id=decision_id,
                replay_date=replay_date,
                module_name=module_name,
                rule_signal=rule_signal,
                decision_action=action,
                relationship=relationship,
                system_suggested=True,
                user_confirmed=False,
                evidence=[f"Signal: {rule_signal}", f"Action: {action}"],
                counter_evidence=[],
                confidence="OBSERVATIONAL",
                status="SUGGESTED",
                note="",
                created_at=_now_utc(),
                updated_at=_now_utc(),
            )
            records.append(record.to_dict())
        return records

    def review_session(self, session_id: str) -> Dict[str, Any]:
        """Return a stub review for a session (store queries needed for full implementation)."""
        return {
            "session_id": session_id,
            "status": "SUGGESTED",
            "note": "Use store queries to retrieve full session reviews.",
            "research_only": True,
        }

    def build_relationship(
        self,
        module_name: str,
        rule_signal: str,
        decision_action: str,
        journal_entry: Dict[str, Any],
    ) -> str:
        """
        Determine FOLLOWED/IGNORED/CONTRADICTED/NOT_APPLICABLE.

        Rules:
        - Has valid stop/invalidation plan → planned stop not CONTRADICTED
        - Planned breakout entry → not auto-chasing
        - WAIT/SKIP decisions → most NOT_APPLICABLE
        """
        action_upper = decision_action.upper() if decision_action else ""
        signal_lower = rule_signal.lower() if rule_signal else ""

        # WAIT/SKIP → most NOT_APPLICABLE
        if action_upper in ("WAIT", "SKIP", "WATCH"):
            return "NOT_APPLICABLE"

        # Planned stop check for NO_PANIC_SELL
        if module_name == "NO_PANIC_SELL":
            has_stop_plan = bool(journal_entry.get("stop_price") or journal_entry.get("stop_type"))
            if has_stop_plan and action_upper in ("STOP", "EXIT"):
                return "FOLLOWED"  # Planned stop — not contradicted
            if "panic_sell_warning" in signal_lower and action_upper in ("STOP", "EXIT"):
                return "NEEDS_REVIEW"

        # Planned breakout check for NO_CHASE
        if module_name == "NO_CHASE":
            has_entry_plan = bool(journal_entry.get("entry_trigger") or journal_entry.get("thesis_text"))
            if has_entry_plan and action_upper == "ENTER":
                return "NEEDS_REVIEW"  # May be planned, not chasing
            if "chase_warning" in signal_lower and action_upper == "ENTER":
                return "NEEDS_REVIEW"

        # DO_NOT_REBUY_YET
        if module_name == "DO_NOT_REBUY_YET":
            if "do_not_rebuy" in signal_lower and action_upper in ("ENTER", "ADD"):
                return "NEEDS_REVIEW"

        # General: bullish signal + ENTER/ADD → FOLLOWED
        bullish_signals = ["golden_cross", "low_kd_cross", "confirmed", "valid", "support", "strong"]
        if any(bs in signal_lower for bs in bullish_signals) and action_upper in ("ENTER", "ADD", "HOLD"):
            return "FOLLOWED"

        # Warning signal + action anyway → NEEDS_REVIEW
        warning_signals = ["warning", "cross_down", "overbought", "weak", "negative"]
        if any(ws in signal_lower for ws in warning_signals) and action_upper in ("ENTER", "ADD"):
            return "NEEDS_REVIEW"

        return "INSUFFICIENT"

    def confirm(self, review_id: str, reason: str = "") -> Dict[str, Any]:
        """Append-only confirm. Returns history entry."""
        return {
            "review_id": review_id,
            "action": "confirm",
            "new_status": "CONFIRMED",
            "reason": reason,
            "created_at": _now_utc(),
            "preserve_original": True,
            "auto_confirmed": False,
        }

    def dismiss(self, review_id: str, reason: str = "") -> Dict[str, Any]:
        """Append-only dismiss. Does not delete original suggestion."""
        return {
            "review_id": review_id,
            "action": "dismiss",
            "new_status": "DISMISSED",
            "reason": reason,
            "created_at": _now_utc(),
            "preserve_original": True,
        }

    def override(
        self, review_id: str, relationship: str, reason: str = ""
    ) -> Dict[str, Any]:
        """Append-only override. Preserves original."""
        return {
            "review_id": review_id,
            "action": "override",
            "new_status": "OVERRIDDEN",
            "new_relationship": relationship,
            "reason": reason,
            "created_at": _now_utc(),
            "preserve_original": True,
        }

    def reopen(self, review_id: str, reason: str = "") -> Dict[str, Any]:
        """Append-only reopen. Preserves history."""
        return {
            "review_id": review_id,
            "action": "reopen",
            "new_status": "NEEDS_REVIEW",
            "reason": reason,
            "created_at": _now_utc(),
            "preserve_original": True,
        }

    def history(self, review_id: str) -> List[Dict[str, Any]]:
        """Return history entries for a review (requires store queries)."""
        return []

    def summary(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Return summary (requires store queries for full implementation)."""
        return {
            "session_id": session_id,
            "suggested": 0,
            "confirmed": 0,
            "dismissed": 0,
            "overridden": 0,
            "note": "Use store queries for full summary.",
            "research_only": True,
        }
