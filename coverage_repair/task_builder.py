"""
coverage_repair/task_builder.py — Maps CoverageIssue objects to CoverageRepairTask objects.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] INVALID OHLC: never auto-modify. CONFLICT: never auto-overwrite.
[!] Synthetic price repair: DISABLED. External data download: DISABLED.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Dict, List, Optional

from coverage_repair.repair_schema import (
    CoverageIssue, CoverageRepairTask,
    ISSUE_MISSING_SYMBOL_DATA, ISSUE_INSUFFICIENT_HISTORY, ISSUE_PARTIAL_OHLC,
    ISSUE_MISSING_VOLUME, ISSUE_DUPLICATE_DATE, ISSUE_CONFLICTING_ROW,
    ISSUE_INVALID_OHLC, ISSUE_INVALID_VOLUME, ISSUE_FUTURE_DATE,
    ISSUE_STALE_DATA, ISSUE_DATE_GAP, ISSUE_MISSING_CHIPS,
    ISSUE_MISSING_REVENUE, ISSUE_MISSING_FUNDAMENTALS, ISSUE_SCHEMA_MISMATCH,
    ISSUE_SOURCE_UNKNOWN, ISSUE_IMPORT_FAILED, ISSUE_LOW_MAPPING_CONFIDENCE,
    ACTION_REVIEW, ACTION_FIX_DATA, ACTION_REIMPORT, ACTION_MERGE_SAFE,
    ACTION_DEDUPLICATE_SAFE, ACTION_NORMALIZE_SCHEMA, ACTION_NORMALIZE_DATE,
    ACTION_REFRESH_COVERAGE, ACTION_PROVIDE_SOURCE_DATA, ACTION_KEEP_OBSERVING,
    REPAIR_MODE_DRY_RUN, REPAIR_MODE_DEDUPLICATE_IDENTICAL, REPAIR_MODE_NORMALIZE_SAFE,
    REPAIR_MODE_REIMPORT_SAFE, REPAIR_MODE_MANUAL_REVIEW, REPAIR_MODE_BLOCKED,
    REPAIRABILITY_AUTO_SAFE, REPAIRABILITY_SEMI_AUTO, REPAIRABILITY_MANUAL,
    REPAIRABILITY_SOURCE_REQUIRED, REPAIRABILITY_NOT_REPAIRABLE,
    PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    STATUS_OPEN, STATUS_NEEDS_SOURCE_DATA, STATUS_NEEDS_REVIEW, STATUS_BLOCKED,
)


# ---------------------------------------------------------------------------
# Issue → action / repairability / priority mapping tables
# ---------------------------------------------------------------------------

_ACTION_MAP: Dict[str, str] = {
    ISSUE_MISSING_SYMBOL_DATA:    ACTION_PROVIDE_SOURCE_DATA,
    ISSUE_INSUFFICIENT_HISTORY:   ACTION_REIMPORT,
    ISSUE_PARTIAL_OHLC:           ACTION_REIMPORT,
    ISSUE_MISSING_VOLUME:         ACTION_REIMPORT,
    ISSUE_DUPLICATE_DATE:         ACTION_DEDUPLICATE_SAFE,
    ISSUE_CONFLICTING_ROW:        ACTION_REVIEW,
    ISSUE_INVALID_OHLC:           ACTION_REVIEW,
    ISSUE_INVALID_VOLUME:         ACTION_REVIEW,
    ISSUE_FUTURE_DATE:            ACTION_REVIEW,
    ISSUE_STALE_DATA:             ACTION_PROVIDE_SOURCE_DATA,
    ISSUE_DATE_GAP:               ACTION_REVIEW,
    ISSUE_MISSING_CHIPS:          ACTION_PROVIDE_SOURCE_DATA,
    ISSUE_MISSING_REVENUE:        ACTION_PROVIDE_SOURCE_DATA,
    ISSUE_MISSING_FUNDAMENTALS:   ACTION_PROVIDE_SOURCE_DATA,
    ISSUE_SCHEMA_MISMATCH:        ACTION_NORMALIZE_SCHEMA,
    ISSUE_SOURCE_UNKNOWN:         ACTION_REVIEW,
    ISSUE_IMPORT_FAILED:          ACTION_REIMPORT,
    ISSUE_LOW_MAPPING_CONFIDENCE: ACTION_REVIEW,
}

_REPAIRABILITY_MAP: Dict[str, str] = {
    ISSUE_MISSING_SYMBOL_DATA:    REPAIRABILITY_SOURCE_REQUIRED,
    ISSUE_INSUFFICIENT_HISTORY:   REPAIRABILITY_SOURCE_REQUIRED,
    ISSUE_PARTIAL_OHLC:           REPAIRABILITY_SOURCE_REQUIRED,
    ISSUE_MISSING_VOLUME:         REPAIRABILITY_SEMI_AUTO,
    ISSUE_DUPLICATE_DATE:         REPAIRABILITY_AUTO_SAFE,
    ISSUE_CONFLICTING_ROW:        REPAIRABILITY_MANUAL,
    ISSUE_INVALID_OHLC:           REPAIRABILITY_NOT_REPAIRABLE,
    ISSUE_INVALID_VOLUME:         REPAIRABILITY_MANUAL,
    ISSUE_FUTURE_DATE:            REPAIRABILITY_MANUAL,
    ISSUE_STALE_DATA:             REPAIRABILITY_SOURCE_REQUIRED,
    ISSUE_DATE_GAP:               REPAIRABILITY_SEMI_AUTO,
    ISSUE_MISSING_CHIPS:          REPAIRABILITY_SOURCE_REQUIRED,
    ISSUE_MISSING_REVENUE:        REPAIRABILITY_SOURCE_REQUIRED,
    ISSUE_MISSING_FUNDAMENTALS:   REPAIRABILITY_SOURCE_REQUIRED,
    ISSUE_SCHEMA_MISMATCH:        REPAIRABILITY_AUTO_SAFE,
    ISSUE_SOURCE_UNKNOWN:         REPAIRABILITY_MANUAL,
    ISSUE_IMPORT_FAILED:          REPAIRABILITY_SEMI_AUTO,
    ISSUE_LOW_MAPPING_CONFIDENCE: REPAIRABILITY_NOT_REPAIRABLE,
}

_PRIORITY_MAP: Dict[str, str] = {
    ISSUE_MISSING_SYMBOL_DATA:    PRIORITY_P1,
    ISSUE_INSUFFICIENT_HISTORY:   PRIORITY_P1,
    ISSUE_PARTIAL_OHLC:           PRIORITY_P1,
    ISSUE_MISSING_VOLUME:         PRIORITY_P2,
    ISSUE_DUPLICATE_DATE:         PRIORITY_P3,
    ISSUE_CONFLICTING_ROW:        PRIORITY_P0,
    ISSUE_INVALID_OHLC:           PRIORITY_P0,
    ISSUE_INVALID_VOLUME:         PRIORITY_P1,
    ISSUE_FUTURE_DATE:            PRIORITY_P1,
    ISSUE_STALE_DATA:             PRIORITY_P2,
    ISSUE_DATE_GAP:               PRIORITY_P2,
    ISSUE_MISSING_CHIPS:          PRIORITY_P2,
    ISSUE_MISSING_REVENUE:        PRIORITY_P2,
    ISSUE_MISSING_FUNDAMENTALS:   PRIORITY_P3,
    ISSUE_SCHEMA_MISMATCH:        PRIORITY_P1,
    ISSUE_SOURCE_UNKNOWN:         PRIORITY_P2,
    ISSUE_IMPORT_FAILED:          PRIORITY_P1,
    ISSUE_LOW_MAPPING_CONFIDENCE: PRIORITY_P1,
}

_REPAIR_MODE_MAP: Dict[str, str] = {
    ISSUE_DUPLICATE_DATE:      REPAIR_MODE_DEDUPLICATE_IDENTICAL,
    ISSUE_SCHEMA_MISMATCH:     REPAIR_MODE_NORMALIZE_SAFE,
    ISSUE_FUTURE_DATE:         REPAIR_MODE_NORMALIZE_SAFE,
    ISSUE_CONFLICTING_ROW:     REPAIR_MODE_MANUAL_REVIEW,
    ISSUE_INVALID_OHLC:        REPAIR_MODE_BLOCKED,
    ISSUE_INVALID_VOLUME:      REPAIR_MODE_BLOCKED,
    ISSUE_LOW_MAPPING_CONFIDENCE: REPAIR_MODE_BLOCKED,
}

_STATUS_MAP: Dict[str, str] = {
    REPAIRABILITY_SOURCE_REQUIRED: STATUS_NEEDS_SOURCE_DATA,
    REPAIRABILITY_MANUAL:          STATUS_NEEDS_REVIEW,
    REPAIRABILITY_NOT_REPAIRABLE:  STATUS_BLOCKED,
}

_BLOCKED_REASONS: Dict[str, str] = {
    ISSUE_INVALID_OHLC:           "Must not auto-modify OHLC prices. Manual review required.",
    ISSUE_INVALID_VOLUME:         "Must not auto-modify volume data. Manual review required.",
    ISSUE_LOW_MAPPING_CONFIDENCE: "Low mapping confidence — auto-repair prohibited.",
}

_TITLES: Dict[str, str] = {
    ISSUE_MISSING_SYMBOL_DATA:    "Provide source data for missing symbol",
    ISSUE_INSUFFICIENT_HISTORY:   "Reimport: insufficient trading history",
    ISSUE_PARTIAL_OHLC:           "Reimport: partial OHLC fields",
    ISSUE_MISSING_VOLUME:         "Reimport or review: missing volume",
    ISSUE_DUPLICATE_DATE:         "Safe deduplication of identical rows",
    ISSUE_CONFLICTING_ROW:        "Manual review: conflicting OHLCV rows",
    ISSUE_INVALID_OHLC:           "BLOCKED: invalid OHLC (must not auto-modify)",
    ISSUE_INVALID_VOLUME:         "BLOCKED: invalid volume (must not auto-modify)",
    ISSUE_FUTURE_DATE:            "Review: future date detected",
    ISSUE_STALE_DATA:             "Provide source data: stale daily data",
    ISSUE_DATE_GAP:               "Review: date gap (approximation, check holidays)",
    ISSUE_MISSING_CHIPS:          "Provide source data: missing chips dataset",
    ISSUE_MISSING_REVENUE:        "Provide source data: missing revenue dataset",
    ISSUE_MISSING_FUNDAMENTALS:   "Provide source data: missing fundamentals dataset",
    ISSUE_SCHEMA_MISMATCH:        "Normalize schema: field name or dtype mismatch",
    ISSUE_SOURCE_UNKNOWN:         "Review: unknown data source",
    ISSUE_IMPORT_FAILED:          "Reimport: previous import failed",
    ISSUE_LOW_MAPPING_CONFIDENCE: "BLOCKED: low mapping confidence",
}


class CoverageRepairTaskBuilder:
    """Converts CoverageIssue objects into prioritized CoverageRepairTask objects.

    [!] Research Only. No Real Orders.
    [!] INVALID OHLC → always BLOCKED. CONFLICT → always MANUAL_REVIEW.
    [!] Synthetic repair DISABLED. External data download DISABLED.
    """

    NO_REAL_ORDERS  = True
    RESEARCH_ONLY   = True
    DRY_RUN_DEFAULT = True

    def build_tasks(self, issues: List[CoverageIssue], dry_run: bool = True) -> List[CoverageRepairTask]:
        """Build a list of repair tasks from issues, sorted by priority."""
        tasks = [self.build_task(issue, dry_run=dry_run) for issue in issues]
        tasks = self.deduplicate_tasks(tasks)
        return self._sort_by_priority(tasks)

    def build_task(self, issue: CoverageIssue, dry_run: bool = True) -> CoverageRepairTask:
        """Build a single CoverageRepairTask from a CoverageIssue."""
        action        = self.map_issue_to_action(issue)
        repairability = self.classify_repairability(issue)
        priority      = self._map_priority(issue)
        repair_mode   = _REPAIR_MODE_MAP.get(issue.issue_type, REPAIR_MODE_DRY_RUN)
        status        = _STATUS_MAP.get(repairability, STATUS_OPEN)
        blocked_reason = _BLOCKED_REASONS.get(issue.issue_type)
        title         = _TITLES.get(issue.issue_type, f"Repair: {issue.issue_type}")
        required_input = self.build_source_requirement(issue)

        # Tier-based priority adjustment
        if issue.tier in ("CORE_10",) and priority not in (PRIORITY_P0,):
            priority = PRIORITY_P1

        return CoverageRepairTask(
            task_id=f"task_{issue.issue_id}_{uuid.uuid4().hex[:6]}",
            issue_id=issue.issue_id,
            symbol=issue.symbol,
            title=title,
            action=action,
            priority=priority,
            dataset=issue.dataset,
            repair_mode=repair_mode,
            required_input=required_input,
            dry_run=dry_run,
            destructive=False,
            status=status,
            blocked_reason=blocked_reason,
            expected_effect=self._describe_expected_effect(issue, repairability),
            research_only=True,
            no_real_orders=True,
        )

    def map_issue_to_action(self, issue: CoverageIssue) -> str:
        """Return the recommended action for a given issue type."""
        return _ACTION_MAP.get(issue.issue_type, ACTION_REVIEW)

    def classify_repairability(self, issue: CoverageIssue) -> str:
        """Return the repairability classification for a given issue."""
        return _REPAIRABILITY_MAP.get(issue.issue_type, REPAIRABILITY_MANUAL)

    def build_source_requirement(self, issue: CoverageIssue) -> Optional[str]:
        """Return a human-readable description of what source data is needed."""
        if issue.issue_type in (
            ISSUE_MISSING_SYMBOL_DATA, ISSUE_INSUFFICIENT_HISTORY,
            ISSUE_PARTIAL_OHLC, ISSUE_STALE_DATA,
        ):
            return f"Daily OHLCV CSV for {issue.symbol} ({issue.dataset})"
        if issue.issue_type == ISSUE_MISSING_CHIPS:
            return f"Chips dataset for {issue.symbol}"
        if issue.issue_type == ISSUE_MISSING_REVENUE:
            return f"Revenue dataset for {issue.symbol}"
        if issue.issue_type == ISSUE_MISSING_FUNDAMENTALS:
            return f"Fundamentals dataset for {issue.symbol}"
        return None

    def deduplicate_tasks(self, tasks: List[CoverageRepairTask]) -> List[CoverageRepairTask]:
        """Remove duplicate tasks that share the same (issue_id, action) pair."""
        seen = set()
        unique = []
        for t in tasks:
            key = (t.issue_id, t.action)
            if key not in seen:
                seen.add(key)
                unique.append(t)
        return unique

    def summarize_tasks(self, tasks: List[CoverageRepairTask]) -> dict:
        """Return a summary dict counting tasks by priority and repairability."""
        from collections import Counter
        p_counts = Counter(t.priority for t in tasks)
        r_counts = Counter(t.repair_mode for t in tasks)
        return {
            "total":         len(tasks),
            "by_priority":   dict(p_counts),
            "by_repair_mode": dict(r_counts),
            "auto_safe":     sum(1 for t in tasks if t.repair_mode == REPAIR_MODE_DEDUPLICATE_IDENTICAL),
            "manual":        sum(1 for t in tasks if t.repair_mode == REPAIR_MODE_MANUAL_REVIEW),
            "blocked":       sum(1 for t in tasks if t.repair_mode == REPAIR_MODE_BLOCKED),
            "source_required": sum(1 for t in tasks if t.status == STATUS_NEEDS_SOURCE_DATA),
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _map_priority(self, issue: CoverageIssue) -> str:
        return _PRIORITY_MAP.get(issue.issue_type, PRIORITY_P2)

    def _sort_by_priority(self, tasks: List[CoverageRepairTask]) -> List[CoverageRepairTask]:
        _ORDER = {PRIORITY_P0: 0, PRIORITY_P1: 1, PRIORITY_P2: 2, PRIORITY_P3: 3}
        return sorted(tasks, key=lambda t: _ORDER.get(t.priority, 9))

    def _describe_expected_effect(self, issue: CoverageIssue, repairability: str) -> str:
        if repairability == REPAIRABILITY_AUTO_SAFE:
            return f"Remove {issue.affected_rows} duplicate row(s) safely"
        if repairability == REPAIRABILITY_SOURCE_REQUIRED:
            return "Pending: source data required before repair"
        if repairability == REPAIRABILITY_NOT_REPAIRABLE:
            return "Cannot auto-repair — manual intervention required"
        if repairability == REPAIRABILITY_MANUAL:
            return "Manual review required"
        return "Repair mode TBD"
