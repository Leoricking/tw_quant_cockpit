"""coverage_repair/planner.py — CoverageRepairPlanner for v1.3.3.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True default. destructive=False always. executable=False until safety checks pass.
[!] Never: create fake data, use Mock to fill gaps, auto-overwrite source conflict,
[!]        auto-change symbol/market, auto-delete history, auto-rebuild entire DB,
[!]        auto-ordering.
"""
from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, List, Tuple

from coverage_repair.models_v133 import (
    CoverageRepairTask,
    RepairActionType,
    RepairIssueType,
    RepairPlan,
    RepairTaskStatus,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Actions that require human review before execution
_MANUAL_REQUIRED_ISSUES = {
    RepairIssueType.SOURCE_CONFLICT,
    RepairIssueType.MARKET_CONFLICT,
    RepairIssueType.PROVIDER_AUTH_REQUIRED,
    RepairIssueType.INVALID_SCHEMA,
    RepairIssueType.MISSING_CAPABILITY,
    RepairIssueType.CORPORATE_ACTION_UNKNOWN,
    RepairIssueType.DEMO_ONLY_DATA,
}

_MANUAL_REQUIRED_ACTIONS = {
    RepairActionType.REVIEW_SOURCE_CONFLICT,
    RepairActionType.REVIEW_MARKET_CONFLICT,
    RepairActionType.REQUEST_AUTH_CONFIGURATION,
    RepairActionType.FIX_SCHEMA,
    RepairActionType.MARK_UNSUPPORTED,
    RepairActionType.MARK_EXCLUDED,
    RepairActionType.MANUAL_REVIEW,
    RepairActionType.NO_SAFE_ACTION,
}

# Forbidden actions — must never appear in a plan
_FORBIDDEN_ACTIONS = {
    "BUY", "SELL", "ORDER", "SUBMIT_ORDER", "AUTO_TRADE",
    "BROKER_LOGIN", "EXECUTE_TRADE", "FILL_MOCK", "FAKE_DATA",
    "AUTO_OVERWRITE", "DELETE_HISTORY", "REBUILD_ENTIRE_DB",
}


class CoverageRepairPlanner:
    """Builds repair plans from tasks.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] dry_run=True default. destructive=False always.
    """

    no_real_orders = True
    production_trading_blocked = True

    def build_plan(self, task: CoverageRepairTask) -> RepairPlan:
        """Build a RepairPlan for a single task."""
        action = self.choose_safe_action(task)
        preconditions = self.list_preconditions(task)
        expected = self.estimate_effect(task)
        blocking: List[str] = []
        warnings: List[str] = []

        # Determine if manually required
        manual = (action in _MANUAL_REQUIRED_ACTIONS or
                  task.issue_type in _MANUAL_REQUIRED_ISSUES)

        # Destructive check (always False)
        destructive = False

        # Executable only if: safe_auto action, not manual, task is open/planned/ready
        executable = (
            not manual and
            RepairActionType.is_safe_auto(action) and
            task.status in (RepairTaskStatus.OPEN, RepairTaskStatus.PLANNED,
                            RepairTaskStatus.READY_TO_RETRY)
        )

        if manual:
            blocking.append(f"Manual review required for action: {action}")
        if task.status == RepairTaskStatus.BLOCKED:
            blocking.append(f"Task is BLOCKED: {task.blocking_reason}")
        if task.status in (RepairTaskStatus.RESOLVED, RepairTaskStatus.CANCELLED):
            blocking.append(f"Task is in terminal status: {task.status}")
        if task.attempt_count >= task.max_attempts:
            blocking.append(f"Max attempts reached: {task.attempt_count}/{task.max_attempts}")
            executable = False

        if not executable and not blocking:
            blocking.append("Plan not yet approved for execution (dry_run=True required first)")

        plan = RepairPlan(
            plan_id=str(uuid.uuid4()),
            task_id=task.task_id,
            symbol=task.symbol,
            profile=task.profile,
            selected_action=action,
            preconditions=preconditions,
            expected_result=expected,
            provider_id=task.provider_id,
            capability=task.provider_capability,
            dry_run=True,  # default always True
            destructive=destructive,
            executable=executable,
            blocking_reasons=blocking,
            warnings=warnings,
            metadata={
                "issue_type": task.issue_type,
                "priority": task.priority,
                "no_real_orders": True,
                "production_trading_blocked": True,
            },
        )
        return plan

    def build_batch_plan(self, tasks: List[CoverageRepairTask]) -> List[RepairPlan]:
        """Build plans for multiple tasks."""
        return [self.build_plan(t) for t in tasks]

    def validate_plan(self, plan: RepairPlan) -> Tuple[bool, List[str]]:
        """Validate a plan. Returns (is_valid, error_list)."""
        errors: List[str] = []

        # Check for forbidden actions
        if self.detect_destructive_action(plan):
            errors.append(f"Plan contains forbidden/destructive action: {plan.selected_action}")

        # Destructive must always be False
        if plan.destructive:
            errors.append("Plan destructive=True is NEVER allowed")

        # No forbidden action strings
        action_upper = plan.selected_action.upper()
        for forbidden in _FORBIDDEN_ACTIONS:
            if forbidden in action_upper:
                errors.append(f"Forbidden keyword in action: {forbidden}")

        # If executable=True, must have passed safety checks
        if plan.executable and plan.blocking_reasons:
            errors.append("Plan marked executable but has blocking reasons")

        return len(errors) == 0, errors

    def choose_safe_action(self, task: CoverageRepairTask) -> str:
        """Choose the safest available action for a task."""
        candidates = list(task.suggested_actions) if task.suggested_actions else []

        # Filter out forbidden
        safe_candidates = [a for a in candidates if not RepairActionType.is_forbidden(a)]

        # Prefer safe auto actions
        auto_safe = [a for a in safe_candidates if RepairActionType.is_safe_auto(a)]
        if auto_safe:
            return auto_safe[0]

        # Then non-forbidden manual actions
        if safe_candidates:
            return safe_candidates[0]

        return RepairActionType.NO_SAFE_ACTION

    def list_preconditions(self, task: CoverageRepairTask) -> List[str]:
        """List preconditions for the task's selected action."""
        preconditions: List[str] = [
            "dry_run=True (execution requires explicit approval)",
            "destructive=False (always)",
            "no_real_orders=True",
            "production_trading_blocked=True",
        ]
        issue = task.issue_type
        action = task.selected_action

        if action == RepairActionType.REFRESH_PROVIDER:
            preconditions.append("Provider must be configured and enabled")
            preconditions.append("Provider must not be rate-limited")
        elif action == RepairActionType.REBUILD_CACHE:
            preconditions.append("Original data source must be available")
        elif action == RepairActionType.RECALCULATE_INDICATORS:
            preconditions.append("Base OHLCV data must be present and valid")
        elif action == RepairActionType.EXTEND_HISTORY:
            preconditions.append("Historical data source must be available")
            preconditions.append("History extension does not overwrite existing validated data")
        elif action == RepairActionType.REVIEW_SOURCE_CONFLICT:
            preconditions.append("Human review required before any resolution")
            preconditions.append("No auto-overwrite of conflicting sources")
        elif action == RepairActionType.REQUEST_AUTH_CONFIGURATION:
            preconditions.append("Auth credentials must be configured by operator")
            preconditions.append("No auto-credential injection")

        if issue == RepairIssueType.DEMO_ONLY_DATA:
            preconditions.append("DEMO_ONLY: cannot be auto-resolved — requires real data source")

        return preconditions

    def estimate_effect(self, task: CoverageRepairTask) -> str:
        """Estimate the expected effect of the repair action."""
        action = task.selected_action
        effects = {
            RepairActionType.REFRESH_PROVIDER: "Provider data refreshed; quality re-evaluated",
            RepairActionType.RETRY_PROVIDER: "Provider request retried; transient errors may clear",
            RepairActionType.REBUILD_CACHE: "Cache rebuilt from source; stale entries cleared",
            RepairActionType.INVALIDATE_CACHE: "Cache cleared; next fetch pulls fresh data",
            RepairActionType.RECALCULATE_INDICATORS: "Technical indicators recalculated from base data",
            RepairActionType.REVALIDATE_QUALITY: "Quality score recalculated; status may improve",
            RepairActionType.RECALCULATE_COVERAGE: "Coverage status recalculated for symbol/profile",
            RepairActionType.EXTEND_HISTORY: "Historical range extended; MA/indicator history improved",
            RepairActionType.ENABLE_CONFIGURED_PROVIDER: "Provider enabled; retry becomes available",
            RepairActionType.WAIT_FOR_SOURCE: "Task waits for source availability; no data change",
            RepairActionType.WAIT_FOR_RATE_LIMIT: "Task waits for rate limit to clear",
            RepairActionType.REVIEW_SOURCE_CONFLICT: "Human resolves source conflict; no auto-change",
            RepairActionType.REVIEW_MARKET_CONFLICT: "Human resolves market conflict; no auto-change",
            RepairActionType.REQUEST_AUTH_CONFIGURATION: "Auth configured by operator; provider becomes available",
            RepairActionType.FIX_SCHEMA: "Schema corrected by operator; data re-ingested",
            RepairActionType.MANUAL_REVIEW: "Operator reviews situation; outcome depends on finding",
            RepairActionType.NO_SAFE_ACTION: "No safe automated action available; manual review required",
        }
        return effects.get(action, f"Action: {action} — effect unknown")

    def detect_destructive_action(self, plan: RepairPlan) -> bool:
        """Returns True if the plan contains a forbidden or destructive action."""
        action_upper = (plan.selected_action or "").upper()
        for forbidden in _FORBIDDEN_ACTIONS:
            if forbidden in action_upper:
                return True
        if RepairActionType.is_forbidden(plan.selected_action):
            return True
        return plan.destructive  # always False by construction

    def summarize_plan(self, plan: RepairPlan) -> str:
        """Return a human-readable plan summary."""
        lines = [
            f"Plan ID      : {plan.plan_id}",
            f"Task ID      : {plan.task_id}",
            f"Symbol       : {plan.symbol}",
            f"Profile      : {plan.profile}",
            f"Action       : {plan.selected_action}",
            f"Dry Run      : {plan.dry_run}",
            f"Destructive  : {plan.destructive}",
            f"Executable   : {plan.executable}",
            f"Expected     : {plan.expected_result}",
        ]
        if plan.blocking_reasons:
            lines.append(f"Blocking     : {'; '.join(plan.blocking_reasons)}")
        if plan.warnings:
            lines.append(f"Warnings     : {'; '.join(plan.warnings)}")
        lines.extend([
            f"No Real Orders          : True",
            f"Production Trading BLOCKED: True",
        ])
        return "\n".join(lines)
