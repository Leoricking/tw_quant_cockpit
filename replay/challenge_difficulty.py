"""
replay/challenge_difficulty.py — Challenge difficulty settings v1.2.7

[!] All difficulty levels keep Future Firewall active.
[!] EXPERT still keeps Future Firewall. Still no future data.
[!] CUSTOM cannot disable No Real Orders or Future Firewall.
[!] CUSTOM cannot enable auto-execution.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# ---------------------------------------------------------------------------
# Difficulty presets
# ---------------------------------------------------------------------------

DIFFICULTY_SETTINGS: Dict[str, Dict[str, Any]] = {
    "BEGINNER": {
        "difficulty": "BEGINNER",
        "symbol_visible": True,
        "date_visible": True,
        "time_multiplier": 2.0,
        "max_hints": 5,
        "show_main_indicators": True,
        "show_strategy_warnings": True,
        "show_review_conclusion": True,
        "require_higher_tf_context": False,
        "require_strategy_conflict_review": False,
        "signal_labels_visible": True,
        "timeframe_labels_visible": True,
        "info_lookup_active": False,
        "future_firewall": True,           # ALWAYS active
        "no_real_orders": True,            # ALWAYS True
        "no_auto_execution": True,         # ALWAYS True
        "outcome_hidden": True,            # default hidden
    },
    "INTERMEDIATE": {
        "difficulty": "INTERMEDIATE",
        "symbol_visible": True,
        "date_visible": True,
        "time_multiplier": 1.0,
        "max_hints": 2,
        "show_main_indicators": True,
        "show_strategy_warnings": True,
        "show_review_conclusion": False,
        "require_higher_tf_context": True,
        "require_strategy_conflict_review": False,
        "signal_labels_visible": True,
        "timeframe_labels_visible": True,
        "info_lookup_active": False,
        "future_firewall": True,
        "no_real_orders": True,
        "no_auto_execution": True,
        "outcome_hidden": True,
    },
    "ADVANCED": {
        "difficulty": "ADVANCED",
        "symbol_visible": True,            # optional: can hide
        "date_visible": True,              # optional: can hide
        "time_multiplier": 1.0,
        "max_hints": 1,
        "show_main_indicators": True,
        "show_strategy_warnings": True,
        "show_review_conclusion": False,
        "require_higher_tf_context": True,
        "require_strategy_conflict_review": True,
        "signal_labels_visible": True,
        "timeframe_labels_visible": True,
        "info_lookup_active": True,
        "mtf_strategy_conflict_required": True,
        "future_firewall": True,
        "no_real_orders": True,
        "no_auto_execution": True,
        "outcome_hidden": True,
    },
    "EXPERT": {
        "difficulty": "EXPERT",
        "symbol_visible": False,           # can hide symbol + date
        "date_visible": False,
        "time_multiplier": 0.8,
        "max_hints": 0,
        "show_main_indicators": False,
        "show_strategy_warnings": False,
        "show_review_conclusion": False,
        "require_higher_tf_context": True,
        "require_strategy_conflict_review": True,
        "signal_labels_visible": False,
        "timeframe_labels_visible": False,
        "info_lookup_active": True,
        "mtf_strategy_conflict_required": True,
        "point_in_time_raw_context_only": True,
        "future_firewall": True,           # STILL ACTIVE for EXPERT
        "no_real_orders": True,            # STILL True for EXPERT
        "no_auto_execution": True,         # STILL True for EXPERT
        "outcome_hidden": True,
    },
    "CUSTOM": {
        "difficulty": "CUSTOM",
        "symbol_visible": True,
        "date_visible": True,
        "time_multiplier": 1.0,
        "max_hints": 3,
        "show_main_indicators": True,
        "show_strategy_warnings": True,
        "show_review_conclusion": False,
        "future_firewall": True,           # CANNOT disable
        "no_real_orders": True,            # CANNOT disable
        "no_auto_execution": True,         # CANNOT disable
        "outcome_hidden": True,
        # All fields configurable within safety bounds:
        "_safety_note": "Cannot disable future_firewall, no_real_orders, or no_auto_execution",
    },
}

_IMMUTABLE_SAFETY_FLAGS = {
    "future_firewall": True,
    "no_real_orders": True,
    "no_auto_execution": True,
}


def get_difficulty_settings(difficulty: str) -> Dict[str, Any]:
    """Return difficulty settings, always enforcing safety invariants."""
    settings = dict(DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["INTERMEDIATE"]))
    # Always enforce safety flags — cannot be overridden
    settings.update(_IMMUTABLE_SAFETY_FLAGS)
    return settings


def apply_custom_settings(
    base_settings: Dict[str, Any],
    overrides: Dict[str, Any],
) -> Dict[str, Any]:
    """Apply custom overrides to base settings, enforcing safety invariants."""
    merged = dict(base_settings)
    for k, v in overrides.items():
        if k in _IMMUTABLE_SAFETY_FLAGS:
            logger.warning("Cannot override safety flag '%s'; enforcing %s", k, _IMMUTABLE_SAFETY_FLAGS[k])
            continue
        merged[k] = v
    # Always enforce
    merged.update(_IMMUTABLE_SAFETY_FLAGS)
    return merged


def validate_custom_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Validate custom settings — check safety invariants."""
    errors = []
    for flag, required_value in _IMMUTABLE_SAFETY_FLAGS.items():
        if settings.get(flag) != required_value:
            errors.append(f"{flag} must be {required_value}")
    if settings.get("max_hints", 0) < 0:
        errors.append("max_hints cannot be negative")
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "safety_note": "future_firewall, no_real_orders, no_auto_execution cannot be disabled",
    }
