"""
replay/emotional_state.py — EmotionalStateCapture for v1.2.2

[!] Research Only. No Real Orders. Replay Training Only.
[!] Self-reported emotional state ONLY. NOT a psychological diagnosis.
[!] Values must be 0-100. No automated scoring.
[!] Flags are self-reported: SELF_REPORTED_FOMO, SELF_REPORTED_REVENGE_RISK, etc.
[!] Cannot stop Session automatically — only provides WARN unless user hard-blocks.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Self-reported risk flags
SELF_REPORTED_FLAGS = [
    "SELF_REPORTED_FOMO",
    "SELF_REPORTED_REVENGE_RISK",
    "SELF_REPORTED_LOSS_AVERSION",
    "SELF_REPORTED_HIGH_STRESS",
    "SELF_REPORTED_LOW_FOCUS",
    "SELF_REPORTED_FATIGUE",
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class EmotionalStateCapture:
    """
    Captures self-reported emotional state for journal entries.

    [!] Self-reported only. NOT psychological diagnosis.
    [!] All values 0-100. Missing values allowed (None).
    [!] NO_PSYCHOLOGICAL_DIAGNOSIS invariant.
    """

    no_real_orders = True
    research_only = True

    # NO_PSYCHOLOGICAL_DIAGNOSIS — this is self-reported training journal data only

    def record_state(
        self,
        session_id: str,
        decision_id: str,
        emotion: str = "NEUTRAL",
        confidence: Optional[int] = None,
        anxiety: Optional[int] = None,
        focus: Optional[int] = None,
        notes: str = "",
        bias_flags: Optional[List[str]] = None,
        **kwargs,
    ) -> "EmotionalStateRecord":
        """
        Record self-reported emotional state.
        [!] self_reported=True always enforced.
        """
        from replay.decision_journal_schema import EmotionalStateRecord

        self.validate_levels(confidence=confidence, anxiety=anxiety, focus=focus)

        stress = kwargs.get("stress")
        urgency = kwargs.get("urgency")
        fear = kwargs.get("fear")
        greed = kwargs.get("greed")
        fatigue = kwargs.get("fatigue")
        intensity = kwargs.get("intensity")

        for name, val in [("stress", stress), ("urgency", urgency), ("fear", fear),
                          ("greed", greed), ("fatigue", fatigue), ("intensity", intensity)]:
            if val is not None:
                self._validate_level(name, val)

        fomo = bool(kwargs.get("fomo", False))
        revenge_trading_risk = bool(kwargs.get("revenge_trading_risk", False))
        loss_aversion_risk = bool(kwargs.get("loss_aversion_risk", False))

        flags = list(bias_flags or [])
        risks = self.detect_self_reported_risks(
            confidence=confidence, anxiety=anxiety, focus=focus,
            fomo=fomo, revenge_trading_risk=revenge_trading_risk,
            loss_aversion_risk=loss_aversion_risk,
            fatigue=fatigue,
        )
        for r in risks:
            if r not in flags:
                flags.append(r)

        return EmotionalStateRecord(
            emotional_state_id=f"EMO-{uuid.uuid4().hex[:12].upper()}",
            session_id=session_id,
            decision_id=decision_id,
            primary_emotion=emotion.upper(),
            confidence_level=confidence,
            anxiety_level=anxiety,
            focus_level=focus,
            intensity=intensity,
            stress_level=stress,
            urgency_level=urgency,
            fear_level=fear,
            greed_level=greed,
            fatigue_level=fatigue,
            fomo=fomo,
            revenge_trading_risk=revenge_trading_risk,
            loss_aversion_risk=loss_aversion_risk,
            cognitive_bias_flags=flags,
            notes=notes,
            self_reported=True,
            simulation_only=True,
            research_only=True,
            no_real_orders=True,
        )

    def validate_levels(
        self,
        confidence: Optional[int] = None,
        anxiety: Optional[int] = None,
        focus: Optional[int] = None,
        **kwargs,
    ) -> None:
        """All levels must be 0-100 if provided."""
        for name, val in [("confidence", confidence), ("anxiety", anxiety), ("focus", focus)]:
            if val is not None:
                self._validate_level(name, val)

    def _validate_level(self, name: str, val: int) -> None:
        """Raise ValueError if level is outside 0-100."""
        try:
            v = int(val)
        except (TypeError, ValueError):
            raise ValueError(f"Emotional state level '{name}' must be integer 0-100, got: {val}")
        if not (0 <= v <= 100):
            raise ValueError(
                f"Emotional state level '{name}' must be 0-100, got: {val}. "
                "Self-reported emotional data only."
            )

    def detect_self_reported_risks(
        self,
        confidence: Optional[int] = None,
        anxiety: Optional[int] = None,
        focus: Optional[int] = None,
        fomo: bool = False,
        revenge_trading_risk: bool = False,
        loss_aversion_risk: bool = False,
        fatigue: Optional[int] = None,
        **kwargs,
    ) -> List[str]:
        """
        Detect self-reported risk flags based on reported values.
        [!] Not diagnosis. Only flags from user-provided data.
        """
        flags = []
        if fomo:
            flags.append("SELF_REPORTED_FOMO")
        if revenge_trading_risk:
            flags.append("SELF_REPORTED_REVENGE_RISK")
        if loss_aversion_risk:
            flags.append("SELF_REPORTED_LOSS_AVERSION")
        if anxiety is not None and anxiety >= 70:
            flags.append("SELF_REPORTED_HIGH_STRESS")
        if focus is not None and focus <= 30:
            flags.append("SELF_REPORTED_LOW_FOCUS")
        if fatigue is not None and fatigue >= 70:
            flags.append("SELF_REPORTED_FATIGUE")
        return flags

    def create_record(self, session_id: str, decision_id: str, **kwargs) -> "EmotionalStateRecord":
        """Alias for record_state."""
        return self.record_state(session_id=session_id, decision_id=decision_id, **kwargs)

    def update_record(
        self, state_dict: Dict[str, Any], **kwargs
    ) -> Dict[str, Any]:
        """Update fields in an emotional state record (returns new dict)."""
        updated = dict(state_dict)
        for k, v in kwargs.items():
            if k in ("self_reported", "simulation_only", "research_only", "no_real_orders"):
                continue  # These are invariants
            if k in ("confidence_level", "anxiety_level", "focus_level",
                     "stress_level", "urgency_level", "fear_level",
                     "greed_level", "fatigue_level", "intensity"):
                if v is not None:
                    self._validate_level(k, v)
            updated[k] = v
        updated["self_reported"] = True
        updated["simulation_only"] = True
        return updated

    def validate_scores(self, state_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Validate all score fields in a state dict."""
        errors = []
        level_fields = [
            "confidence_level", "anxiety_level", "focus_level",
            "stress_level", "urgency_level", "fear_level",
            "greed_level", "fatigue_level", "intensity",
        ]
        for fld in level_fields:
            val = state_dict.get(fld)
            if val is not None:
                try:
                    self._validate_level(fld, val)
                except ValueError as exc:
                    errors.append(str(exc))
        return {"valid": len(errors) == 0, "errors": errors}

    def session_history(self, session_id: str, store=None) -> List[Dict[str, Any]]:
        """Get emotional state history for a session."""
        if store is None:
            return []
        states = store.load_emotional_states()
        return [s for s in states if s.get("session_id") == session_id]

    def journal_history(self, journal_entry_id: str, store=None) -> List[Dict[str, Any]]:
        """Get emotional state history for a journal entry."""
        if store is None:
            return []
        states = store.load_emotional_states()
        return [s for s in states if s.get("decision_id") == journal_entry_id
                or s.get("emotional_state_id") == journal_entry_id]

    def summary(self, states: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize emotional states (no performance metrics)."""
        if not states:
            return {"total": 0}
        emotion_counts: Dict[str, int] = {}
        for s in states:
            e = s.get("primary_emotion", "UNKNOWN")
            emotion_counts[e] = emotion_counts.get(e, 0) + 1
        return {
            "total": len(states),
            "emotion_distribution": emotion_counts,
        }


# Backward-compat alias
ReplayEmotionalStateManager = EmotionalStateCapture
