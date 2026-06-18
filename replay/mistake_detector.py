"""
replay/mistake_detector.py — ReplayMistakeDetector for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] System-detected mistakes: status=SUGGESTED (never auto-CONFIRMED).
[!] Must have evidence field. Must have confidence field.
[!] WAIT/SKIP not misclassified as mistakes.
[!] Planned stop not misclassified as PANIC_SELL.
[!] Planned reduce not misclassified as EXITED_TOO_EARLY.
[!] Single loss != mistake. Single profit != good decision.
[!] Emotional/bias: SELF_REPORTED or RULE_SUGGESTED only. NOT diagnosis.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_MISTAKE_CONFIRMATION_ENABLED = False


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_mistake_id() -> str:
    return f"MIS-{uuid.uuid4().hex[:12].upper()}"


class ReplayMistakeDetector:
    """
    Detects potential mistakes in replay decisions.

    Rules:
    - All detected mistakes start as SUGGESTED — never auto-CONFIRMED.
    - WAIT/SKIP with documented rationale → NOT a mistake.
    - Planned stop triggered → NOT PANIC_SELL.
    - Planned reduce per original plan → NOT EXITED_TOO_EARLY.
    - Single loss → NOT automatically a mistake.
    - Single profit → NOT automatically a good decision.
    - Emotional patterns: SELF_REPORTED or RULE_SUGGESTED only. NOT diagnosis.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    AUTO_MISTAKE_CONFIRMATION_ENABLED = False

    def detect(
        self,
        session_id: str,
        journal_entry: Optional[Dict[str, Any]] = None,
        session_state: Optional[Dict[str, Any]] = None,
        decisions: Optional[List[Dict[str, Any]]] = None,
    ) -> List["MistakeRecord"]:
        """
        Detect potential mistakes in a session.
        Returns list of MistakeRecord (all SUGGESTED status).
        """
        from replay.scoring_schema import MistakeRecord, MistakeStatus, MistakeSource, MistakeSeverity

        entry = journal_entry or {}
        state = session_state or {}
        decision_list = decisions or []

        mistakes: List[MistakeRecord] = []
        action = entry.get("action", "")
        symbol = entry.get("symbol", "")
        replay_date = entry.get("replay_date", state.get("current_date", ""))

        # ---- Safety: WAIT/SKIP guard ----
        is_wait_or_skip = action in ("WAIT", "SKIP")
        decision_reason = entry.get("decision_reason", "")
        if is_wait_or_skip and (decision_reason or entry.get("no_trade_conditions")):
            # Well-reasoned WAIT/SKIP — do NOT flag as mistake
            return mistakes

        # ---- Check: No thesis documented ----
        if action in ("ENTER", "ADD") and not entry.get("thesis_id"):
            mistakes.append(MistakeRecord(
                mistake_id=_new_mistake_id(),
                session_id=session_id,
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=symbol,
                replay_date=replay_date,
                mistake_type="NO_THESIS_DOCUMENTED",
                category="PROCESS",
                description="Entry decision made without a documented trade thesis.",
                evidence=["action=ENTER/ADD", "thesis_id=None"],
                confidence=70,
                severity=MistakeSeverity.MEDIUM.value,
                status=MistakeStatus.SUGGESTED.value,
                source=MistakeSource.RULE_SUGGESTED.value,
                action=action,
                is_wait_or_skip=False,
                auto_confirmed=False,
            ))

        # ---- Check: No stop defined ----
        if action in ("ENTER", "ADD") and not entry.get("risk_plan_id"):
            stop_note = entry.get("stop_price_note", "")
            if not stop_note:
                mistakes.append(MistakeRecord(
                    mistake_id=_new_mistake_id(),
                    session_id=session_id,
                    journal_entry_id=entry.get("journal_entry_id"),
                    decision_id=entry.get("decision_id"),
                    symbol=symbol,
                    replay_date=replay_date,
                    mistake_type="NO_STOP_DEFINED",
                    category="RISK",
                    description="Entry made without a defined stop price or risk plan.",
                    evidence=["risk_plan_id=None", "stop_price_note=empty"],
                    confidence=75,
                    severity=MistakeSeverity.HIGH.value,
                    status=MistakeStatus.SUGGESTED.value,
                    source=MistakeSource.RULE_SUGGESTED.value,
                    action=action,
                    is_wait_or_skip=False,
                    auto_confirmed=False,
                ))

        # ---- Check: No checklist ----
        checklist_ids = entry.get("checklist_ids", [])
        if action in ("ENTER", "ADD") and not checklist_ids:
            mistakes.append(MistakeRecord(
                mistake_id=_new_mistake_id(),
                session_id=session_id,
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=symbol,
                replay_date=replay_date,
                mistake_type="SKIPPED_CHECKLIST",
                category="PROCESS",
                description="Entry decision made without completing any checklist.",
                evidence=["checklist_ids=[]"],
                confidence=65,
                severity=MistakeSeverity.MEDIUM.value,
                status=MistakeStatus.SUGGESTED.value,
                source=MistakeSource.RULE_SUGGESTED.value,
                action=action,
                is_wait_or_skip=False,
                auto_confirmed=False,
            ))

        # ---- Check: Point-in-time violation ----
        pit = bool(entry.get("point_in_time_verified", False))
        state_pit = bool(state.get("point_in_time_verified", False))
        if not pit and not state_pit and action in ("ENTER", "ADD", "EXIT", "STOP"):
            mistakes.append(MistakeRecord(
                mistake_id=_new_mistake_id(),
                session_id=session_id,
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=symbol,
                replay_date=replay_date,
                mistake_type="POINT_IN_TIME_VIOLATION",
                category="DATA",
                description="point_in_time_verified=False on session snapshot.",
                evidence=["point_in_time_verified=False"],
                confidence=80,
                severity=MistakeSeverity.HIGH.value,
                status=MistakeStatus.SUGGESTED.value,
                source=MistakeSource.RULE_SUGGESTED.value,
                action=action,
                is_wait_or_skip=False,
                auto_confirmed=False,
            ))

        # ---- Check: EXIT with no stop/plan signal (potential PANIC_SELL) ----
        # ONLY if NOT a planned stop
        if action in ("EXIT", "STOP", "REDUCE"):
            is_planned_stop = bool(entry.get("risk_plan_id")) and action == "STOP"
            is_planned_reduce = bool(entry.get("risk_plan_id")) and action == "REDUCE"
            fallback = entry.get("fallback_action", "")

            if action == "STOP" and not is_planned_stop and not fallback:
                mistakes.append(MistakeRecord(
                    mistake_id=_new_mistake_id(),
                    session_id=session_id,
                    journal_entry_id=entry.get("journal_entry_id"),
                    decision_id=entry.get("decision_id"),
                    symbol=symbol,
                    replay_date=replay_date,
                    mistake_type="PANIC_SELL",
                    category="EXIT",
                    description=(
                        "STOP action without documented risk plan. "
                        "Possible PANIC_SELL — requires review. "
                        "[!] Planned stop is NOT PANIC_SELL."
                    ),
                    evidence=["action=STOP", "risk_plan_id=None", "fallback_action=empty"],
                    confidence=50,
                    severity=MistakeSeverity.MEDIUM.value,
                    status=MistakeStatus.SUGGESTED.value,
                    source=MistakeSource.RULE_SUGGESTED.value,
                    action=action,
                    is_wait_or_skip=False,
                    is_planned_stop=False,
                    auto_confirmed=False,
                ))

        # ---- Check: Emotional state flags (self-reported only) ----
        emotional_state_id = entry.get("emotional_state_id")
        if emotional_state_id:
            # Only check if user explicitly flagged FOMO or revenge
            fomo = bool(entry.get("fomo", False))
            revenge = bool(entry.get("revenge_trading_risk", False))
            if fomo and action in ("ENTER", "ADD"):
                mistakes.append(MistakeRecord(
                    mistake_id=_new_mistake_id(),
                    session_id=session_id,
                    journal_entry_id=entry.get("journal_entry_id"),
                    decision_id=entry.get("decision_id"),
                    symbol=symbol,
                    replay_date=replay_date,
                    mistake_type="FOMO_ENTRY",
                    category="EMOTIONAL",
                    description=(
                        "Self-reported FOMO flag present at entry. "
                        "[!] Self-reported only. NOT psychological diagnosis."
                    ),
                    evidence=["emotional_state_id present", "fomo=True (self-reported)"],
                    confidence=40,
                    severity=MistakeSeverity.LOW.value,
                    status=MistakeStatus.SUGGESTED.value,
                    source=MistakeSource.SELF_REPORTED.value,
                    action=action,
                    is_wait_or_skip=False,
                    auto_confirmed=False,
                ))
            if revenge:
                mistakes.append(MistakeRecord(
                    mistake_id=_new_mistake_id(),
                    session_id=session_id,
                    journal_entry_id=entry.get("journal_entry_id"),
                    decision_id=entry.get("decision_id"),
                    symbol=symbol,
                    replay_date=replay_date,
                    mistake_type="REVENGE_TRADE",
                    category="EMOTIONAL",
                    description=(
                        "Self-reported revenge trading risk flag present. "
                        "[!] Self-reported only. NOT psychological diagnosis."
                    ),
                    evidence=["emotional_state_id present", "revenge_trading_risk=True (self-reported)"],
                    confidence=40,
                    severity=MistakeSeverity.LOW.value,
                    status=MistakeStatus.SUGGESTED.value,
                    source=MistakeSource.SELF_REPORTED.value,
                    action=action,
                    is_wait_or_skip=False,
                    auto_confirmed=False,
                ))

        # ---- v1.2.4 Strategy Knowledge Replay: strategy-related mistake suggestions ----
        # Rules:
        # - All need evidence + confidence; valid thesis/stop/invalidation → not auto-flagged
        # - NEVER auto-CONFIRM — all remain SUGGESTED
        strategy_signals = entry.get("strategy_signals_at_decision", {})
        strategy_warnings = entry.get("strategy_warnings_at_decision", []) or []
        strategy_conflicts = entry.get("strategy_conflicts_at_decision", []) or []

        has_stop_plan = bool(entry.get("stop_price") or entry.get("risk_plan_id"))
        has_thesis = bool(entry.get("thesis_id") or entry.get("decision_reason"))
        has_invalidation = bool(entry.get("invalidation_conditions"))

        # NO_CHASE_WARNING_IGNORED
        if (action in ("ENTER", "ADD") and not is_wait_or_skip
                and strategy_signals
                and not has_thesis):
            modules = strategy_signals.get("modules", []) if isinstance(strategy_signals, dict) else []
            for mod in modules:
                if (mod.get("module_name") == "NO_CHASE"
                        and "chase_warning" in str(mod.get("signal", "")).lower()):
                    mistakes.append(MistakeRecord(
                        mistake_id=_new_mistake_id(),
                        session_id=session_id,
                        journal_entry_id=entry.get("journal_entry_id"),
                        decision_id=entry.get("decision_id"),
                        symbol=symbol,
                        replay_date=replay_date,
                        mistake_type="NO_CHASE_WARNING_IGNORED",
                        category="STRATEGY",
                        description="Entry made while No-Chase warning was active and no thesis documented.",
                        evidence=["NO_CHASE signal: " + str(mod.get("signal", "")), "action=ENTER/ADD", "thesis=missing"],
                        confidence=55,
                        severity=MistakeSeverity.MEDIUM.value,
                        status=MistakeStatus.SUGGESTED.value,
                        source=MistakeSource.RULE_SUGGESTED.value,
                        action=action,
                        is_wait_or_skip=False,
                        auto_confirmed=False,
                    ))
                    break

        # NO_PANIC_SELL_WARNING_IGNORED — only if no planned stop
        if (action in ("STOP", "EXIT") and not is_wait_or_skip
                and not has_stop_plan and strategy_signals):
            modules = strategy_signals.get("modules", []) if isinstance(strategy_signals, dict) else []
            for mod in modules:
                if (mod.get("module_name") == "NO_PANIC_SELL"
                        and "panic_sell_warning" in str(mod.get("signal", "")).lower()):
                    mistakes.append(MistakeRecord(
                        mistake_id=_new_mistake_id(),
                        session_id=session_id,
                        journal_entry_id=entry.get("journal_entry_id"),
                        decision_id=entry.get("decision_id"),
                        symbol=symbol,
                        replay_date=replay_date,
                        mistake_type="NO_PANIC_SELL_WARNING_IGNORED",
                        category="STRATEGY",
                        description="Exit/stop made without a documented stop plan while panic-sell warning active.",
                        evidence=["NO_PANIC_SELL signal active", "no stop plan documented"],
                        confidence=55,
                        severity=MistakeSeverity.MEDIUM.value,
                        status=MistakeStatus.SUGGESTED.value,
                        source=MistakeSource.RULE_SUGGESTED.value,
                        action=action,
                        is_planned_stop=False,
                        is_wait_or_skip=False,
                        auto_confirmed=False,
                    ))
                    break

        # STRATEGY_CONFLICT_NOT_REVIEWED
        if strategy_conflicts and action in ("ENTER", "ADD", "HOLD"):
            high_conflicts = [c for c in strategy_conflicts if c.get("severity") == "HIGH"]
            if high_conflicts and not entry.get("strategy_rule_review_ids"):
                mistakes.append(MistakeRecord(
                    mistake_id=_new_mistake_id(),
                    session_id=session_id,
                    journal_entry_id=entry.get("journal_entry_id"),
                    decision_id=entry.get("decision_id"),
                    symbol=symbol,
                    replay_date=replay_date,
                    mistake_type="STRATEGY_CONFLICT_NOT_REVIEWED",
                    category="STRATEGY",
                    description="Decision made with HIGH-severity strategy conflicts not reviewed.",
                    evidence=[f"conflicts: {[c.get('conflict_type') for c in high_conflicts]}"],
                    confidence=50,
                    severity=MistakeSeverity.MEDIUM.value,
                    status=MistakeStatus.SUGGESTED.value,
                    source=MistakeSource.RULE_SUGGESTED.value,
                    action=action,
                    is_wait_or_skip=False,
                    auto_confirmed=False,
                ))

        # v1.2.5 MTF mistake types (SUGGESTED only — never auto-confirmed)
        mtf_agreement = entry.get("mtf_agreement_status")
        mtf_conflicts = entry.get("mtf_conflicts_at_decision") or []
        mtf_partial = entry.get("mtf_partial_bar_warning", False)

        if mtf_partial and action not in ("WAIT", "SKIP", "REDUCE", "PASS"):
            mistakes.append(MistakeRecord(
                mistake_id=_new_mistake_id(),
                session_id=session_id,
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=symbol,
                replay_date=replay_date,
                mistake_type="MTF_PARTIAL_BAR_NOT_ACKNOWLEDGED",
                category="MTF",
                description="Decision made without acknowledging active partial bar warning.",
                evidence=["mtf_partial_bar_warning=True was present at decision time"],
                confidence=40,
                severity=MistakeSeverity.LOW.value,
                status=MistakeStatus.SUGGESTED.value,
                source=MistakeSource.RULE_SUGGESTED.value,
                action=action,
                is_wait_or_skip=False,
                auto_confirmed=False,
            ))

        if mtf_conflicts and len(mtf_conflicts) >= 3 and action not in ("WAIT", "SKIP"):
            mistakes.append(MistakeRecord(
                mistake_id=_new_mistake_id(),
                session_id=session_id,
                journal_entry_id=entry.get("journal_entry_id"),
                decision_id=entry.get("decision_id"),
                symbol=symbol,
                replay_date=replay_date,
                mistake_type="MTF_HIGH_CONFLICT_NOT_REVIEWED",
                category="MTF",
                description="Multiple MTF conflicts present but decision taken without WAIT/SKIP.",
                evidence=[f"mtf_conflict_count={len(mtf_conflicts)}"],
                confidence=40,
                severity=MistakeSeverity.LOW.value,
                status=MistakeStatus.SUGGESTED.value,
                source=MistakeSource.RULE_SUGGESTED.value,
                action=action,
                is_wait_or_skip=False,
                auto_confirmed=False,
            ))

        # Ensure none are auto-confirmed
        for m in mistakes:
            m.auto_confirmed = False

        return mistakes
