"""
coverage_repair/repair_task_builder.py — RepairTaskBuilder for TW Quant Cockpit v1.1.2.

Builds CoverageRepairTask objects from CoverageIssue objects.
Assigns priority (P0/P1/P2/P3) and action (AUTO_SAFE/MANUAL_REVIEW/SOURCE_REQUIRED/BLOCKED).

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] INVALID OHLC → BLOCKED (never auto-modify).
[!] CONFLICT → MANUAL_REVIEW (never auto-overwrite).
[!] MISSING → SOURCE_REQUIRED (no synthetic data).
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import List

from coverage_repair.coverage_repair_schema import (
    CoverageIssue, CoverageRepairTask,
    ISSUE_MISSING, ISSUE_INSUFFICIENT, ISSUE_PARTIAL,
    ISSUE_STALE, ISSUE_DUPLICATE, ISSUE_CONFLICT, ISSUE_INVALID,
    ACTION_AUTO_SAFE, ACTION_MANUAL_REVIEW, ACTION_SOURCE_REQUIRED, ACTION_BLOCKED,
    PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
)

logger = logging.getLogger(__name__)


class RepairTaskBuilder:
    """Builds CoverageRepairTask objects from CoverageIssue objects.

    Priority rules:
        P0 — MISSING (critical: no data at all)
        P1 — CONFLICT, INVALID (data integrity problems)
        P2 — INSUFFICIENT, PARTIAL, STALE (data quality problems)
        P3 — DUPLICATE identical rows (safe cleanup)

    Action rules:
        MISSING       → SOURCE_REQUIRED (no synthetic data allowed)
        INSUFFICIENT  → SOURCE_REQUIRED (need more data)
        PARTIAL       → SOURCE_REQUIRED (need more data)
        STALE         → SOURCE_REQUIRED (need fresh data)
        DUPLICATE     → AUTO_SAFE (identical rows can be deduplicated)
        CONFLICT      → MANUAL_REVIEW (never auto-overwrite)
        INVALID       → BLOCKED (never auto-modify OHLC)

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    # Action mapping per issue type
    ACTION_MAP = {
        ISSUE_MISSING:      ACTION_SOURCE_REQUIRED,
        ISSUE_INSUFFICIENT: ACTION_SOURCE_REQUIRED,
        ISSUE_PARTIAL:      ACTION_SOURCE_REQUIRED,
        ISSUE_STALE:        ACTION_SOURCE_REQUIRED,
        ISSUE_DUPLICATE:    ACTION_AUTO_SAFE,
        ISSUE_CONFLICT:     ACTION_MANUAL_REVIEW,
        ISSUE_INVALID:      ACTION_BLOCKED,
    }

    # Priority mapping per issue type
    PRIORITY_MAP = {
        ISSUE_MISSING:      PRIORITY_P0,
        ISSUE_CONFLICT:     PRIORITY_P1,
        ISSUE_INVALID:      PRIORITY_P1,
        ISSUE_INSUFFICIENT: PRIORITY_P2,
        ISSUE_PARTIAL:      PRIORITY_P2,
        ISSUE_STALE:        PRIORITY_P2,
        ISSUE_DUPLICATE:    PRIORITY_P3,
    }

    # Blocked reasons per issue type
    BLOCKED_REASONS = {
        ISSUE_INVALID: (
            "Invalid OHLC data must not be auto-modified. "
            "Manual data correction required from authoritative source."
        ),
    }

    def build(self, issues: List[CoverageIssue], dry_run: bool = True) -> List[CoverageRepairTask]:
        """Build a list of CoverageRepairTask from detected issues."""
        tasks: List[CoverageRepairTask] = []
        for issue in issues:
            task = self._build_task(issue, dry_run=dry_run)
            tasks.append(task)
        # Sort by priority: P0 first, then P1, P2, P3
        priority_order = {PRIORITY_P0: 0, PRIORITY_P1: 1, PRIORITY_P2: 2, PRIORITY_P3: 3}
        tasks.sort(key=lambda t: priority_order.get(t.priority, 9))
        return tasks

    def _build_task(self, issue: CoverageIssue, dry_run: bool = True) -> CoverageRepairTask:
        ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
        action   = self.ACTION_MAP.get(issue.issue_type, ACTION_BLOCKED)
        priority = self.PRIORITY_MAP.get(issue.issue_type, PRIORITY_P2)
        blocked_reason = self.BLOCKED_REASONS.get(issue.issue_type)

        # INVALID always BLOCKED regardless
        if issue.issue_type == ISSUE_INVALID:
            action = ACTION_BLOCKED

        # CONFLICT always MANUAL_REVIEW
        if issue.issue_type == ISSUE_CONFLICT:
            action = ACTION_MANUAL_REVIEW

        description = self._make_description(issue, action, priority)

        return CoverageRepairTask(
            task_id=f"task_{issue.symbol}_{issue.dataset}_{issue.issue_type}_{ts}",
            issue_id=issue.issue_id,
            symbol=issue.symbol,
            dataset=issue.dataset,
            issue_type=issue.issue_type,
            action=action,
            priority=priority,
            description=description,
            dry_run=dry_run,
            destructive=False,
            blocked_reason=blocked_reason,
            affected_dates=issue.affected_dates[:],
            before_row_count=issue.row_count,
            estimated_after_row_count=self._estimate_after_count(issue),
        )

    def _make_description(self, issue: CoverageIssue, action: str, priority: str) -> str:
        type_labels = {
            ISSUE_MISSING:      "No data — source data required",
            ISSUE_INSUFFICIENT: "Insufficient rows — source data required",
            ISSUE_PARTIAL:      "Partial coverage — source data required",
            ISSUE_STALE:        "Stale data — fresh source data required",
            ISSUE_DUPLICATE:    "Identical duplicate rows — safe deduplication",
            ISSUE_CONFLICT:     "Conflicting rows — manual review required",
            ISSUE_INVALID:      "Invalid OHLCV data — BLOCKED (must not auto-modify)",
        }
        base = type_labels.get(issue.issue_type, issue.description)
        return f"[{priority}][{action}] {issue.symbol}/{issue.dataset}: {base}"

    def _estimate_after_count(self, issue: CoverageIssue) -> int:
        if issue.issue_type == ISSUE_DUPLICATE:
            dup_count = issue.details.get("duplicate_count", len(issue.affected_dates))
            return max(0, issue.row_count - dup_count)
        return issue.row_count
