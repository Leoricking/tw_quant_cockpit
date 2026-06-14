"""
coverage_repair/repair_planner.py — CoverageRepairPlanner for TW Quant Cockpit v1.1.2.

Builds a RepairPlan from detected coverage issues.
dry_run=True by default. No data is modified during planning.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True by default. Destructive repair disabled.
[!] INVALID OHLC always BLOCKED. CONFLICT always MANUAL_REVIEW.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Optional

from coverage_repair.coverage_repair_schema import (
    RepairPlan, CoverageRepairTask,
    ACTION_AUTO_SAFE, ACTION_MANUAL_REVIEW, ACTION_SOURCE_REQUIRED, ACTION_BLOCKED,
    PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
)

logger = logging.getLogger(__name__)


class CoverageRepairPlanner:
    """Builds a RepairPlan from coverage issues.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] dry_run=True by default.
    """

    research_only  = True
    no_real_orders = True

    def build_plan(
        self,
        symbols: Optional[List[str]] = None,
        dry_run: bool = True,
    ) -> RepairPlan:
        """Detect all issues and build a full RepairPlan."""
        from coverage_repair.issue_detector import CoverageIssueDetector
        from coverage_repair.repair_task_builder import RepairTaskBuilder

        detector = CoverageIssueDetector()
        builder  = RepairTaskBuilder()

        issues = detector.detect_all(symbols=symbols)
        tasks  = builder.build(issues, dry_run=dry_run)

        return self._make_plan(issues, tasks, dry_run=dry_run)

    def build_plan_for_symbol(self, symbol: str, dry_run: bool = True) -> RepairPlan:
        """Build repair plan for a single symbol."""
        from coverage_repair.issue_detector import CoverageIssueDetector
        from coverage_repair.repair_task_builder import RepairTaskBuilder

        detector = CoverageIssueDetector()
        builder  = RepairTaskBuilder()

        issues = detector.detect_symbol(symbol)
        tasks  = builder.build(issues, dry_run=dry_run)

        return self._make_plan(issues, tasks, dry_run=dry_run)

    def _make_plan(self, issues, tasks: List[CoverageRepairTask], dry_run: bool) -> RepairPlan:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        plan_id = f"repair_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        p0 = sum(1 for t in tasks if t.priority == PRIORITY_P0)
        p1 = sum(1 for t in tasks if t.priority == PRIORITY_P1)
        p2 = sum(1 for t in tasks if t.priority == PRIORITY_P2)
        p3 = sum(1 for t in tasks if t.priority == PRIORITY_P3)

        auto_safe       = sum(1 for t in tasks if t.action == ACTION_AUTO_SAFE)
        manual_review   = sum(1 for t in tasks if t.action == ACTION_MANUAL_REVIEW)
        source_required = sum(1 for t in tasks if t.action == ACTION_SOURCE_REQUIRED)
        blocked         = sum(1 for t in tasks if t.action == ACTION_BLOCKED)

        return RepairPlan(
            plan_id=plan_id,
            created_at=ts,
            total_issues=len(issues),
            total_tasks=len(tasks),
            p0_count=p0,
            p1_count=p1,
            p2_count=p2,
            p3_count=p3,
            auto_safe_count=auto_safe,
            manual_review_count=manual_review,
            source_required_count=source_required,
            blocked_count=blocked,
            tasks=tasks,
            dry_run=dry_run,
            destructive_disabled=True,
        )
