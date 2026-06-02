"""
coach/replay_training_planner.py — ReplayTrainingPlanner (v0.4.8).

Builds Replay training plan based on journal mistakes and replay status.

[!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] suggested_command must be research-only. No buy/sell/order suggestions.
"""
from __future__ import annotations

import logging
from typing import Dict, List

from coach.coach_schema import (
    CoachRecommendation,
    REC_REPLAY_TRAINING,
    PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    CAT_REPLAY,
    EFFORT_MEDIUM,
    DUE_TODAY, DUE_THIS_WEEK,
    STATUS_OPEN,
)

logger = logging.getLogger(__name__)

# Training focus scenarios
SCENARIO_FAKE_BREAKOUT       = "fake_breakout"
SCENARIO_VWAP_LOSS           = "vwap_loss"
SCENARIO_VWAP_RECLAIM        = "vwap_reclaim"
SCENARIO_OPENING_RANGE_BREAK = "opening_range_break"
SCENARIO_OPENING_RANGE_FAIL  = "opening_range_fail"
SCENARIO_VOLUME_PROFILE_POC  = "volume_profile_poc"
SCENARIO_CHASE_HIGH          = "chase_high_correction"
SCENARIO_STOP_LOSS           = "stop_loss_discipline"
SCENARIO_WEAK_STOCK_FILTER   = "weak_stock_filter"

ALL_SCENARIOS = [
    SCENARIO_FAKE_BREAKOUT, SCENARIO_VWAP_LOSS, SCENARIO_VWAP_RECLAIM,
    SCENARIO_OPENING_RANGE_BREAK, SCENARIO_OPENING_RANGE_FAIL,
    SCENARIO_VOLUME_PROFILE_POC, SCENARIO_CHASE_HIGH,
    SCENARIO_STOP_LOSS, SCENARIO_WEAK_STOCK_FILTER,
]

_SCENARIO_META = {
    SCENARIO_FAKE_BREAKOUT: {
        "label":          "Fake Breakout Recognition",
        "expected_skill": "Recognize false breakouts before chasing",
        "due_type":       DUE_TODAY,
    },
    SCENARIO_VWAP_LOSS: {
        "label":          "VWAP Loss Recovery",
        "expected_skill": "Manage VWAP loss scenarios without panic",
        "due_type":       DUE_TODAY,
    },
    SCENARIO_VWAP_RECLAIM: {
        "label":          "VWAP Reclaim Pattern",
        "expected_skill": "Identify VWAP reclaim for continuation",
        "due_type":       DUE_THIS_WEEK,
    },
    SCENARIO_OPENING_RANGE_BREAK: {
        "label":          "Opening Range Break",
        "expected_skill": "Execute planned opening range breakout with stop",
        "due_type":       DUE_TODAY,
    },
    SCENARIO_OPENING_RANGE_FAIL: {
        "label":          "Opening Range Failure",
        "expected_skill": "Recognize failed opening range, fade or avoid",
        "due_type":       DUE_THIS_WEEK,
    },
    SCENARIO_VOLUME_PROFILE_POC: {
        "label":          "Volume Profile POC",
        "expected_skill": "Use POC as support/resistance reference",
        "due_type":       DUE_THIS_WEEK,
    },
    SCENARIO_CHASE_HIGH: {
        "label":          "Chase High Correction",
        "expected_skill": "Avoid entering after parabolic extension",
        "due_type":       DUE_TODAY,
    },
    SCENARIO_STOP_LOSS: {
        "label":          "Stop Loss Discipline",
        "expected_skill": "Execute stops without hesitation",
        "due_type":       DUE_TODAY,
    },
    SCENARIO_WEAK_STOCK_FILTER: {
        "label":          "Weak Stock Filter",
        "expected_skill": "Filter out relative weakness before entry",
        "due_type":       DUE_THIS_WEEK,
    },
}

# Mapping from journal mistake tag patterns to scenario priorities
_MISTAKE_TO_SCENARIO: Dict[str, List[str]] = {
    "chase_high":              [SCENARIO_CHASE_HIGH, SCENARIO_FAKE_BREAKOUT],
    "chased":                  [SCENARIO_CHASE_HIGH, SCENARIO_FAKE_BREAKOUT],
    "fake_breakout":           [SCENARIO_FAKE_BREAKOUT],
    "ignored_fake_breakout":   [SCENARIO_FAKE_BREAKOUT],
    "vwap_loss":               [SCENARIO_VWAP_LOSS, SCENARIO_VWAP_RECLAIM],
    "ignored_vwap_loss":       [SCENARIO_VWAP_LOSS],
    "no_plan":                 [SCENARIO_OPENING_RANGE_BREAK, SCENARIO_STOP_LOSS],
    "no_stop":                 [SCENARIO_STOP_LOSS],
    "weak_stock":              [SCENARIO_WEAK_STOCK_FILTER],
    "weak_stock_filter":       [SCENARIO_WEAK_STOCK_FILTER],
    "opening_range":           [SCENARIO_OPENING_RANGE_BREAK, SCENARIO_OPENING_RANGE_FAIL],
    "poc":                     [SCENARIO_VOLUME_PROFILE_POC],
}


class ReplayTrainingPlanner:
    """
    Builds Replay training plan based on journal mistakes and replay status.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def build(
        self,
        journal_summary: dict = None,
        replay_summary:  dict = None,
        review_summary:  dict = None,
    ) -> List[CoachRecommendation]:
        """
        Build replay training recommendations.

        Analyzes journal mistake tags to select relevant scenarios.
        Falls back to basic plan if no data available.
        """
        journal_summary = journal_summary or {}
        replay_summary  = replay_summary  or {}
        review_summary  = review_summary  or {}

        selected: Dict[str, str] = {}  # scenario -> reason

        # Derive scenarios from top mistakes
        top_mistakes = journal_summary.get("top_mistakes", [])
        if isinstance(top_mistakes, list):
            for mistake in top_mistakes:
                m_lower = str(mistake).lower()
                for key, scenarios in _MISTAKE_TO_SCENARIO.items():
                    if key in m_lower:
                        for s in scenarios:
                            if s not in selected:
                                selected[s] = f"Journal mistake: {mistake}"

        # Derive from most_common_mistake field
        mcm = journal_summary.get("most_common_mistake", "")
        if mcm:
            mcm_lower = str(mcm).lower()
            for key, scenarios in _MISTAKE_TO_SCENARIO.items():
                if key in mcm_lower:
                    for s in scenarios:
                        if s not in selected:
                            selected[s] = f"Most common mistake: {mcm}"

        # Add overdue scenarios from replay_summary
        overdue = replay_summary.get("overdue_scenarios", [])
        if isinstance(overdue, list):
            for s in overdue:
                if s in ALL_SCENARIOS and s not in selected:
                    selected[s] = "Overdue replay scenario"

        # Fallback: if no scenarios selected, use defaults
        if not selected:
            selected = {
                SCENARIO_FAKE_BREAKOUT:       "Default daily practice",
                SCENARIO_OPENING_RANGE_BREAK: "Default daily practice",
                SCENARIO_STOP_LOSS:           "Default daily practice",
            }

        items: List[CoachRecommendation] = []
        for i, (scenario, reason) in enumerate(selected.items()):
            meta = _SCENARIO_META.get(scenario, {})
            label         = meta.get("label", scenario)
            expected_skill = meta.get("expected_skill", "")
            due_type      = meta.get("due_type", DUE_THIS_WEEK)
            priority      = PRIORITY_P1 if i < 2 else (PRIORITY_P2 if i < 4 else PRIORITY_P3)

            items.append(CoachRecommendation(
                recommendation_type=REC_REPLAY_TRAINING,
                priority=priority,
                category=CAT_REPLAY,
                title=f"Replay: {label}",
                summary=f"Practice scenario: {label}. Reason: {reason}",
                rationale=reason,
                suggested_command=f"python main.py intraday-replay --mode real",
                expected_benefit=expected_skill,
                effort_level=EFFORT_MEDIUM,
                due_type=due_type,
                tags=["replay", scenario],
                status=STATUS_OPEN,
            ))

        return items
