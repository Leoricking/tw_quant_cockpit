"""
coverage_repair/repair_prioritizer.py — Priority scoring and grouping for coverage repair tasks.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Priority is NOT based on stock popularity or expected returns.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from coverage_repair.repair_schema import (
    CoverageRepairTask,
    PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    REPAIR_MODE_BLOCKED, REPAIR_MODE_MANUAL_REVIEW, REPAIR_MODE_DEDUPLICATE_IDENTICAL,
    STATUS_BLOCKED, STATUS_NEEDS_SOURCE_DATA, STATUS_NEEDS_REVIEW,
    ISSUE_INVALID_OHLC, ISSUE_INVALID_VOLUME, ISSUE_CONFLICTING_ROW,
    ISSUE_SCHEMA_MISMATCH, ISSUE_MISSING_SYMBOL_DATA, ISSUE_INSUFFICIENT_HISTORY,
    ISSUE_STALE_DATA, ISSUE_DUPLICATE_DATE, ISSUE_PARTIAL_OHLC,
    ISSUE_MISSING_CHIPS, ISSUE_MISSING_REVENUE, ISSUE_MISSING_VOLUME,
    ISSUE_MISSING_FUNDAMENTALS, ISSUE_LOW_MAPPING_CONFIDENCE,
)

# ---------------------------------------------------------------------------
# Scoring weights (higher = more urgent)
# ---------------------------------------------------------------------------

_TIER_WEIGHT: Dict[str, int] = {
    "CORE_10":      40,
    "RESEARCH_30":  20,
    "EXPANDED_50":  10,
    "BROAD_100":     5,
}

_PRIORITY_SCORE: Dict[str, int] = {
    PRIORITY_P0: 100,
    PRIORITY_P1:  60,
    PRIORITY_P2:  30,
    PRIORITY_P3:  10,
}

# Issue types that are critical regardless of tier
_CRITICAL_ISSUE_TYPES = {
    ISSUE_INVALID_OHLC, ISSUE_INVALID_VOLUME,
    ISSUE_CONFLICTING_ROW, ISSUE_SCHEMA_MISMATCH,
}

# Issue types that block formal backtest
_BACKTEST_BLOCKERS = {
    ISSUE_INVALID_OHLC, ISSUE_CONFLICTING_ROW, ISSUE_SCHEMA_MISMATCH,
    ISSUE_MISSING_SYMBOL_DATA, ISSUE_INSUFFICIENT_HISTORY,
}


class CoverageRepairPrioritizer:
    """Scores and sorts CoverageRepairTask objects by urgency.

    Priority criteria:
    - Tier importance (CORE_10 > RESEARCH_30 > EXPANDED_50 > BROAD_100)
    - Severity of issue
    - Whether issue blocks formal backtest
    - Auto-safe possibility
    - Source availability
    - Affected data ratio

    [!] Research Only. No Real Orders.
    [!] Priority is NOT based on stock popularity or expected returns.
    """

    NO_REAL_ORDERS = True
    RESEARCH_ONLY  = True

    def score_task(self, task: CoverageRepairTask, context: Optional[dict] = None) -> int:
        """Return an integer urgency score for a task. Higher = more urgent."""
        context = context or {}
        score = _PRIORITY_SCORE.get(task.priority, 10)

        # Tier bonus
        tier = getattr(task, "tier", None) or context.get("tier")
        if tier:
            score += _TIER_WEIGHT.get(tier, 0)

        # Backtest blocker bonus
        issue_type = context.get("issue_type", "")
        if issue_type in _BACKTEST_BLOCKERS:
            score += 30

        # Auto-safe bonus (quick win)
        if task.repair_mode == REPAIR_MODE_DEDUPLICATE_IDENTICAL:
            score += 5

        # Blocked / manual penalty (can't do quickly)
        if task.repair_mode in (REPAIR_MODE_BLOCKED, REPAIR_MODE_MANUAL_REVIEW):
            score -= 10

        # Source-required penalty
        if task.status == STATUS_NEEDS_SOURCE_DATA:
            score -= 15

        return max(score, 0)

    def prioritize(self, tasks: List[CoverageRepairTask]) -> List[CoverageRepairTask]:
        """Return tasks sorted from highest to lowest urgency."""
        _ORDER = {PRIORITY_P0: 0, PRIORITY_P1: 1, PRIORITY_P2: 2, PRIORITY_P3: 3}
        return sorted(
            tasks,
            key=lambda t: (_ORDER.get(t.priority, 9), t.symbol, t.task_id),
        )

    def explain_priority(self, task: CoverageRepairTask) -> str:
        """Return a short human-readable explanation of why a task has its priority."""
        reasons = []
        if task.priority == PRIORITY_P0:
            reasons.append("P0: critical data integrity issue (invalid/conflict/schema)")
        elif task.priority == PRIORITY_P1:
            reasons.append("P1: missing or insufficient core data")
        elif task.priority == PRIORITY_P2:
            reasons.append("P2: partial coverage or optional dataset issue")
        else:
            reasons.append("P3: low-impact metadata or optional improvement")

        if task.repair_mode == REPAIR_MODE_BLOCKED:
            reasons.append("blocked: requires manual intervention")
        elif task.repair_mode == REPAIR_MODE_DEDUPLICATE_IDENTICAL:
            reasons.append("auto-safe: identical duplicate removal")

        if task.status == STATUS_NEEDS_SOURCE_DATA:
            reasons.append("source data required before repair")

        return "; ".join(reasons) if reasons else "no additional context"

    def group_by_priority(self, tasks: List[CoverageRepairTask]) -> Dict[str, List[CoverageRepairTask]]:
        """Group tasks by priority level. Returns dict with keys P0-P3."""
        groups: Dict[str, List[CoverageRepairTask]] = {
            PRIORITY_P0: [],
            PRIORITY_P1: [],
            PRIORITY_P2: [],
            PRIORITY_P3: [],
        }
        for task in tasks:
            groups.setdefault(task.priority, []).append(task)
        return groups

    def group_by_symbol(self, tasks: List[CoverageRepairTask]) -> Dict[str, List[CoverageRepairTask]]:
        """Group tasks by symbol. Returns dict keyed by symbol."""
        groups: Dict[str, List[CoverageRepairTask]] = {}
        for task in tasks:
            groups.setdefault(task.symbol, []).append(task)
        return groups
