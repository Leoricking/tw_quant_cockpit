"""replay_training/replay_drill_builder.py — ReplayDrillBuilder for TW Replay Training Cockpit v0.5.6.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Drill definitions
# ---------------------------------------------------------------------------
_DRILL_TEMPLATES = {
    "fake_breakout_drill": {
        "drill_name":                 "fake_breakout_drill",
        "suggested_symbol_or_pattern": "High-beta TWSE stocks (e.g., 2454, 3711)",
        "focus_points":               "Volume confirmation, wick analysis, 3-bar rule",
        "expected_skill":             "Identify fake breakouts before entry",
        "priority":                   "high",
    },
    "vwap_loss_drill": {
        "drill_name":                 "vwap_loss_drill",
        "suggested_symbol_or_pattern": "Any intraday TWSE chart with clear VWAP",
        "focus_points":               "VWAP as dynamic support, stop placement on VWAP loss",
        "expected_skill":             "Immediate action on VWAP loss",
        "priority":                   "high",
    },
    "vwap_reclaim_drill": {
        "drill_name":                 "vwap_reclaim_drill",
        "suggested_symbol_or_pattern": "Morning dip stocks",
        "focus_points":               "VWAP reclaim confirmation, volume spike on reclaim",
        "expected_skill":             "Spot VWAP reclaim as re-entry signal",
        "priority":                   "medium",
    },
    "opening_range_fail_drill": {
        "drill_name":                 "opening_range_fail_drill",
        "suggested_symbol_or_pattern": "Gap-up stocks at open",
        "focus_points":               "OR high/low levels, watch for price reclaim failure",
        "expected_skill":             "Avoid OR breakout fails, wait for OR hold",
        "priority":                   "high",
    },
    "chase_high_correction_drill": {
        "drill_name":                 "chase_high_correction_drill",
        "suggested_symbol_or_pattern": "Momentum stocks after 3+ green candles",
        "focus_points":               "Wait for pullback to VWAP or support — never chase",
        "expected_skill":             "Pullback entry discipline",
        "priority":                   "high",
    },
    "stop_loss_discipline_drill": {
        "drill_name":                 "stop_loss_discipline_drill",
        "suggested_symbol_or_pattern": "Any trending TWSE stock",
        "focus_points":               "Pre-plan stop before entry, use 3% max loss rule",
        "expected_skill":             "Always have stop level before entering",
        "priority":                   "high",
    },
    "second_wave_entry_drill": {
        "drill_name":                 "second_wave_entry_drill",
        "suggested_symbol_or_pattern": "Stocks with morning momentum",
        "focus_points":               "Identify second wave after initial breakout consolidation",
        "expected_skill":             "Higher-probability second wave entry timing",
        "priority":                   "medium",
    },
    "weak_stock_filter_drill": {
        "drill_name":                 "weak_stock_filter_drill",
        "suggested_symbol_or_pattern": "Compare sector leaders vs laggards",
        "focus_points":               "Relative strength vs index, avoid weak sector stocks",
        "expected_skill":             "Stock selection discipline — only trade leaders",
        "priority":                   "medium",
    },
}

# Mistake-type to drill mapping
_MISTAKE_TO_DRILLS = {
    "chase_high":                  ["chase_high_correction_drill", "vwap_loss_drill"],
    "ignored_stop":                ["stop_loss_discipline_drill"],
    "ignored_vwap_loss":           ["vwap_loss_drill"],
    "ignored_fake_breakout":       ["fake_breakout_drill"],
    "ignored_opening_range_fail":  ["opening_range_fail_drill"],
    "early_take_profit":           ["second_wave_entry_drill"],
    "late_stop_loss":              ["stop_loss_discipline_drill"],
    "bought_weak_stock":           ["weak_stock_filter_drill"],
    "violated_strategy":           ["chase_high_correction_drill"],
    "missed_second_wave":          ["second_wave_entry_drill"],
    "vwap_reclaim":                ["vwap_reclaim_drill"],
}


class ReplayDrillBuilder:
    """Builds targeted training drills based on detected mistakes and AI review.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self) -> None:
        pass

    def build_drills(self, mistakes: list, ai_review) -> List[dict]:
        """Build drill list from mistakes and AI review."""
        try:
            drill_names_seen = set()
            drills: List[dict] = []

            # From mistakes
            for m in mistakes:
                for drill_name in _MISTAKE_TO_DRILLS.get(m.mistake_type, []):
                    if drill_name not in drill_names_seen:
                        drill_names_seen.add(drill_name)
                        template = dict(_DRILL_TEMPLATES.get(drill_name, {}))
                        template["reason"] = f"Detected mistake: {m.mistake_type}"
                        template["no_real_orders"] = True
                        drills.append(template)

            # From AI review suggested drills
            if ai_review:
                suggested = getattr(ai_review, "suggested_drills", "") or ""
                for drill_action in suggested.split(";"):
                    drill_action = drill_action.strip()
                    # Map action to drill name
                    mapping = {
                        "TRAIN_VWAP":            ["vwap_loss_drill", "vwap_reclaim_drill"],
                        "TRAIN_FAKE_BREAKOUT":    ["fake_breakout_drill"],
                        "TRAIN_OPENING_RANGE":    ["opening_range_fail_drill"],
                        "IMPROVE_STOP_DISCIPLINE": ["stop_loss_discipline_drill"],
                        "AVOID_CHASING":          ["chase_high_correction_drill"],
                        "PRACTICE_MORE":          ["second_wave_entry_drill"],
                    }
                    for drill_name in mapping.get(drill_action, []):
                        if drill_name not in drill_names_seen:
                            drill_names_seen.add(drill_name)
                            template = dict(_DRILL_TEMPLATES.get(drill_name, {}))
                            template["reason"] = f"AI review suggested: {drill_action}"
                            template["no_real_orders"] = True
                            drills.append(template)

            # If no specific drills, add a general one
            if not drills:
                template = dict(_DRILL_TEMPLATES["fake_breakout_drill"])
                template["reason"] = "General tape reading practice"
                template["no_real_orders"] = True
                drills.append(template)

            # Sort by priority
            priority_order = {"high": 0, "medium": 1, "low": 2}
            drills.sort(key=lambda d: priority_order.get(d.get("priority", "low"), 2))

            return drills

        except Exception as exc:
            logger.error("[ReplayDrillBuilder] build_drills error: %s", exc)
            return []
