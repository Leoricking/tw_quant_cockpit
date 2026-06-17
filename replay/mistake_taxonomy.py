"""
replay/mistake_taxonomy.py — MistakeTaxonomy for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Mistake types are patterns to learn from, not psychological diagnoses.
[!] WAIT/SKIP decisions that are well-reasoned are NOT mistakes.
[!] Planned stops are NOT PANIC_SELL. Planned reduces are NOT EXITED_TOO_EARLY.
[!] Single loss != mistake. Single profit != good decision.
[!] Emotional/bias: SELF_REPORTED or RULE_SUGGESTED only. NOT psychological diagnosis.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Re-export MistakeRecord for convenience import
from replay.scoring_schema import MistakeRecord  # noqa: F401


class MistakeType:
    # --- Entry mistakes ---
    CHASING_BREAKOUT = "CHASING_BREAKOUT"
    ENTERING_WITHOUT_CONFIRMATION = "ENTERING_WITHOUT_CONFIRMATION"
    IGNORING_INVALIDATION_CONDITIONS = "IGNORING_INVALIDATION_CONDITIONS"
    OVERSIZING_ENTRY = "OVERSIZING_ENTRY"
    ENTERING_AGAINST_TREND = "ENTERING_AGAINST_TREND"
    SKIPPING_VALID_SETUP = "SKIPPING_VALID_SETUP"

    # --- Exit mistakes ---
    PANIC_SELL = "PANIC_SELL"               # ONLY if NOT a planned stop
    EXITED_TOO_EARLY = "EXITED_TOO_EARLY"  # ONLY if NOT a planned reduce
    HOLDING_TOO_LONG = "HOLDING_TOO_LONG"
    IGNORING_STOP_LOSS = "IGNORING_STOP_LOSS"
    MISSING_TARGET_EXIT = "MISSING_TARGET_EXIT"

    # --- Risk mistakes ---
    NO_STOP_DEFINED = "NO_STOP_DEFINED"
    RISK_REWARD_IGNORED = "RISK_REWARD_IGNORED"
    OVERSIZING_POSITION = "OVERSIZING_POSITION"
    ADDING_TO_LOSER = "ADDING_TO_LOSER"
    CONCENTRATION_RISK_IGNORED = "CONCENTRATION_RISK_IGNORED"

    # --- Process/discipline mistakes ---
    SKIPPED_CHECKLIST = "SKIPPED_CHECKLIST"
    NO_THESIS_DOCUMENTED = "NO_THESIS_DOCUMENTED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    REVISED_PLAN_MID_TRADE = "REVISED_PLAN_MID_TRADE"
    IGNORED_INVALIDATION_SIGNAL = "IGNORED_INVALIDATION_SIGNAL"

    # --- Emotional/behavioral patterns (self-reported or rule-triggered only) ---
    FOMO_ENTRY = "FOMO_ENTRY"
    REVENGE_TRADE = "REVENGE_TRADE"
    OVERCONFIDENCE = "OVERCONFIDENCE"
    LOSS_AVERSION_HOLD = "LOSS_AVERSION_HOLD"
    ANCHORING_BIAS = "ANCHORING_BIAS"

    # --- Data/timing mistakes ---
    FUTURE_DATA_RISK = "FUTURE_DATA_RISK"
    STALE_DATA_USED = "STALE_DATA_USED"
    POINT_IN_TIME_VIOLATION = "POINT_IN_TIME_VIOLATION"

    # --- Other ---
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"


class MistakeCategory:
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    RISK = "RISK"
    PROCESS = "PROCESS"
    EMOTIONAL = "EMOTIONAL"
    DATA = "DATA"
    OTHER = "OTHER"


# Map mistake types to categories
MISTAKE_CATEGORY_MAP: Dict[str, str] = {
    MistakeType.CHASING_BREAKOUT: MistakeCategory.ENTRY,
    MistakeType.ENTERING_WITHOUT_CONFIRMATION: MistakeCategory.ENTRY,
    MistakeType.IGNORING_INVALIDATION_CONDITIONS: MistakeCategory.ENTRY,
    MistakeType.OVERSIZING_ENTRY: MistakeCategory.ENTRY,
    MistakeType.ENTERING_AGAINST_TREND: MistakeCategory.ENTRY,
    MistakeType.SKIPPING_VALID_SETUP: MistakeCategory.ENTRY,
    MistakeType.PANIC_SELL: MistakeCategory.EXIT,
    MistakeType.EXITED_TOO_EARLY: MistakeCategory.EXIT,
    MistakeType.HOLDING_TOO_LONG: MistakeCategory.EXIT,
    MistakeType.IGNORING_STOP_LOSS: MistakeCategory.EXIT,
    MistakeType.MISSING_TARGET_EXIT: MistakeCategory.EXIT,
    MistakeType.NO_STOP_DEFINED: MistakeCategory.RISK,
    MistakeType.RISK_REWARD_IGNORED: MistakeCategory.RISK,
    MistakeType.OVERSIZING_POSITION: MistakeCategory.RISK,
    MistakeType.ADDING_TO_LOSER: MistakeCategory.RISK,
    MistakeType.CONCENTRATION_RISK_IGNORED: MistakeCategory.RISK,
    MistakeType.SKIPPED_CHECKLIST: MistakeCategory.PROCESS,
    MistakeType.NO_THESIS_DOCUMENTED: MistakeCategory.PROCESS,
    MistakeType.INSUFFICIENT_EVIDENCE: MistakeCategory.PROCESS,
    MistakeType.REVISED_PLAN_MID_TRADE: MistakeCategory.PROCESS,
    MistakeType.IGNORED_INVALIDATION_SIGNAL: MistakeCategory.PROCESS,
    MistakeType.FOMO_ENTRY: MistakeCategory.EMOTIONAL,
    MistakeType.REVENGE_TRADE: MistakeCategory.EMOTIONAL,
    MistakeType.OVERCONFIDENCE: MistakeCategory.EMOTIONAL,
    MistakeType.LOSS_AVERSION_HOLD: MistakeCategory.EMOTIONAL,
    MistakeType.ANCHORING_BIAS: MistakeCategory.EMOTIONAL,
    MistakeType.FUTURE_DATA_RISK: MistakeCategory.DATA,
    MistakeType.STALE_DATA_USED: MistakeCategory.DATA,
    MistakeType.POINT_IN_TIME_VIOLATION: MistakeCategory.DATA,
    MistakeType.OTHER: MistakeCategory.OTHER,
    MistakeType.UNKNOWN: MistakeCategory.OTHER,
}

# Descriptions for each mistake type
MISTAKE_DESCRIPTIONS: Dict[str, str] = {
    MistakeType.CHASING_BREAKOUT: (
        "Entered after a breakout was already extended. "
        "Risk/reward may be unfavorable at extended prices."
    ),
    MistakeType.ENTERING_WITHOUT_CONFIRMATION: (
        "Entry made before confirmation conditions were met per original thesis."
    ),
    MistakeType.IGNORING_INVALIDATION_CONDITIONS: (
        "Entered or held despite one or more invalidation conditions being triggered."
    ),
    MistakeType.OVERSIZING_ENTRY: (
        "Initial position size exceeded the defined maximum or risk tolerance."
    ),
    MistakeType.ENTERING_AGAINST_TREND: (
        "Entered against the dominant trend without documented counter-trend rationale."
    ),
    MistakeType.SKIPPING_VALID_SETUP: (
        "A valid, well-reasoned setup meeting all criteria was skipped without documented reason. "
        "[!] A deliberate WAIT/SKIP with good rationale is NOT this mistake."
    ),
    MistakeType.PANIC_SELL: (
        "Exit was driven by fear or short-term price movement rather than a planned stop. "
        "[!] A planned stop triggered at the predefined level is NOT PANIC_SELL."
    ),
    MistakeType.EXITED_TOO_EARLY: (
        "Position was exited before the planned target or thesis invalidation. "
        "[!] A planned partial reduce per original plan is NOT EXITED_TOO_EARLY."
    ),
    MistakeType.HOLDING_TOO_LONG: (
        "Held position past the invalidation signal or after thesis was invalidated."
    ),
    MistakeType.IGNORING_STOP_LOSS: (
        "Predefined stop price was breached but position was not reduced or exited."
    ),
    MistakeType.MISSING_TARGET_EXIT: (
        "Failed to reduce or exit when the planned target was reached."
    ),
    MistakeType.NO_STOP_DEFINED: (
        "No stop price or stop condition was defined before entry."
    ),
    MistakeType.RISK_REWARD_IGNORED: (
        "Risk/reward ratio was not estimated or was unfavorable but ignored."
    ),
    MistakeType.OVERSIZING_POSITION: (
        "Total position size exceeded defined concentration or max-risk limits."
    ),
    MistakeType.ADDING_TO_LOSER: (
        "Added to a losing position without a documented plan to do so."
    ),
    MistakeType.CONCENTRATION_RISK_IGNORED: (
        "Position creates excessive concentration in one name, sector, or theme."
    ),
    MistakeType.SKIPPED_CHECKLIST: (
        "Discipline checklist was not completed before the decision."
    ),
    MistakeType.NO_THESIS_DOCUMENTED: (
        "No trade thesis was documented before or with the entry decision."
    ),
    MistakeType.INSUFFICIENT_EVIDENCE: (
        "Decision was made with insufficient supporting evidence documented."
    ),
    MistakeType.REVISED_PLAN_MID_TRADE: (
        "Plan was revised during the trade without documented justification."
    ),
    MistakeType.IGNORED_INVALIDATION_SIGNAL: (
        "A predefined invalidation signal was observed but not acted upon."
    ),
    MistakeType.FOMO_ENTRY: (
        "Self-reported or rule-triggered: entry appears driven by fear of missing out. "
        "[!] Self-reported or rule-triggered only. NOT psychological diagnosis."
    ),
    MistakeType.REVENGE_TRADE: (
        "Self-reported or rule-triggered: trade appears made to recover from a prior loss. "
        "[!] Self-reported or rule-triggered only. NOT psychological diagnosis."
    ),
    MistakeType.OVERCONFIDENCE: (
        "Self-reported or rule-triggered: position sizing or certainty level appears inflated. "
        "[!] Self-reported or rule-triggered only. NOT psychological diagnosis."
    ),
    MistakeType.LOSS_AVERSION_HOLD: (
        "Self-reported or rule-triggered: held past stop to avoid realizing a loss. "
        "[!] Self-reported or rule-triggered only. NOT psychological diagnosis."
    ),
    MistakeType.ANCHORING_BIAS: (
        "Self-reported or rule-triggered: plan appears anchored to an arbitrary reference price. "
        "[!] Self-reported or rule-triggered only. NOT psychological diagnosis."
    ),
    MistakeType.FUTURE_DATA_RISK: (
        "Session data may include fields that should not have been available at replay date."
    ),
    MistakeType.STALE_DATA_USED: (
        "Data used in the decision appears stale or from before a relevant update."
    ),
    MistakeType.POINT_IN_TIME_VIOLATION: (
        "point_in_time_verified=False on the session snapshot."
    ),
    MistakeType.OTHER: "Other mistake — see notes.",
    MistakeType.UNKNOWN: "Unknown mistake type.",
}


class MistakeTaxonomy:
    """
    Taxonomy of mistake types for replay training.
    [!] Research Only. No Real Orders.
    [!] WAIT/SKIP decisions that are well-reasoned are NOT mistakes.
    [!] Planned stop != PANIC_SELL. Planned reduce != EXITED_TOO_EARLY.
    [!] Emotional patterns: self-reported or rule-triggered only. NOT diagnosis.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    ALL_TYPES: List[str] = [
        MistakeType.CHASING_BREAKOUT,
        MistakeType.ENTERING_WITHOUT_CONFIRMATION,
        MistakeType.IGNORING_INVALIDATION_CONDITIONS,
        MistakeType.OVERSIZING_ENTRY,
        MistakeType.ENTERING_AGAINST_TREND,
        MistakeType.SKIPPING_VALID_SETUP,
        MistakeType.PANIC_SELL,
        MistakeType.EXITED_TOO_EARLY,
        MistakeType.HOLDING_TOO_LONG,
        MistakeType.IGNORING_STOP_LOSS,
        MistakeType.MISSING_TARGET_EXIT,
        MistakeType.NO_STOP_DEFINED,
        MistakeType.RISK_REWARD_IGNORED,
        MistakeType.OVERSIZING_POSITION,
        MistakeType.ADDING_TO_LOSER,
        MistakeType.CONCENTRATION_RISK_IGNORED,
        MistakeType.SKIPPED_CHECKLIST,
        MistakeType.NO_THESIS_DOCUMENTED,
        MistakeType.INSUFFICIENT_EVIDENCE,
        MistakeType.REVISED_PLAN_MID_TRADE,
        MistakeType.IGNORED_INVALIDATION_SIGNAL,
        MistakeType.FOMO_ENTRY,
        MistakeType.REVENGE_TRADE,
        MistakeType.OVERCONFIDENCE,
        MistakeType.LOSS_AVERSION_HOLD,
        MistakeType.ANCHORING_BIAS,
        MistakeType.FUTURE_DATA_RISK,
        MistakeType.STALE_DATA_USED,
        MistakeType.POINT_IN_TIME_VIOLATION,
        MistakeType.OTHER,
        MistakeType.UNKNOWN,
    ]

    EMOTIONAL_TYPES: List[str] = [
        MistakeType.FOMO_ENTRY,
        MistakeType.REVENGE_TRADE,
        MistakeType.OVERCONFIDENCE,
        MistakeType.LOSS_AVERSION_HOLD,
        MistakeType.ANCHORING_BIAS,
    ]

    EXIT_TYPES_WITH_PLANNED_EXCEPTIONS: List[str] = [
        MistakeType.PANIC_SELL,
        MistakeType.EXITED_TOO_EARLY,
    ]

    @classmethod
    def get_category(cls, mistake_type: str) -> str:
        return MISTAKE_CATEGORY_MAP.get(mistake_type, MistakeCategory.OTHER)

    @classmethod
    def get_description(cls, mistake_type: str) -> str:
        return MISTAKE_DESCRIPTIONS.get(mistake_type, "No description available.")

    @classmethod
    def is_emotional(cls, mistake_type: str) -> bool:
        return mistake_type in cls.EMOTIONAL_TYPES

    @classmethod
    def requires_planned_exception_check(cls, mistake_type: str) -> bool:
        """PANIC_SELL and EXITED_TOO_EARLY require checking for planned stops/reduces."""
        return mistake_type in cls.EXIT_TYPES_WITH_PLANNED_EXCEPTIONS

    @classmethod
    def is_valid_type(cls, mistake_type: str) -> bool:
        return mistake_type in cls.ALL_TYPES

    @classmethod
    def list_by_category(cls, category: str) -> List[str]:
        return [t for t, c in MISTAKE_CATEGORY_MAP.items() if c == category]

    @classmethod
    def taxonomy_dict(cls) -> List[Dict[str, Any]]:
        result = []
        for mtype in cls.ALL_TYPES:
            result.append({
                "type": mtype,
                "category": cls.get_category(mtype),
                "description": cls.get_description(mtype),
                "is_emotional": cls.is_emotional(mtype),
                "requires_planned_exception_check": cls.requires_planned_exception_check(mtype),
            })
        return result

    @classmethod
    def safety_note(cls) -> str:
        return (
            "[!] Mistake taxonomy is for research training only. "
            "WAIT/SKIP with good rationale is NOT a mistake. "
            "Planned stop is NOT PANIC_SELL. "
            "Planned reduce is NOT EXITED_TOO_EARLY. "
            "Single loss != mistake. Single profit != good decision. "
            "Emotional types are self-reported or rule-triggered only — NOT psychological diagnosis."
        )
