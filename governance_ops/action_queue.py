"""
governance_ops.action_queue — GovernanceActionQueue v1.1.6

Builds, deduplicates, prioritizes, and manages governance action item metadata.
Dashboard CANNOT: modify K-lines, fix conflicts, import data, execute overrides, execute broker/trades.
Dashboard CAN: acknowledge/defer/resolve action metadata, copy safe CLI commands.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Action queue is metadata-only. No auto-execution of destructive actions.
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from governance_ops.governance_schema import GovernanceActionItem, _now_utc, _new_uuid
from governance_ops.priority_engine import GovernancePriorityEngine

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_QUEUE_PATH = os.path.join(BASE_DIR, "data", "governance_ops", "action_queue.csv")
DEFAULT_AUDIT_PATH = os.path.join(BASE_DIR, "data", "governance_ops", "action_audit.jsonl")


class GovernanceActionQueue:
    """
    Manages governance action queue metadata.

    - build() aggregates actions from all adapters
    - deduplicate() removes duplicate actions for the same issue
    - prioritize() assigns P0/P1/P2/P3 to all actions
    - acknowledge/defer/resolve update metadata only (no data modification)

    [!] Research Only. No Real Orders.
    """

    def __init__(self, queue_path: str = DEFAULT_QUEUE_PATH,
                 audit_path: str = DEFAULT_AUDIT_PATH):
        self._queue_path = queue_path
        self._audit_path = audit_path
        self._engine = GovernancePriorityEngine()
        self._actions: List[GovernanceActionItem] = []

    def build(self, summary_sources: list) -> List[GovernanceActionItem]:
        """Build action queue from summary sources (list of adapters)."""
        all_actions: List[GovernanceActionItem] = []
        for source in (summary_sources or []):
            try:
                actions = source.list_actions() if hasattr(source, "list_actions") else []
                all_actions.extend(actions)
            except Exception as exc:
                logger.warning("GovernanceActionQueue.build: source error: %s", exc)
        all_actions = self.deduplicate(all_actions)
        all_actions = self.prioritize(all_actions)
        self._actions = all_actions
        return all_actions

    def build_from_onboarding(self, adapter) -> List[GovernanceActionItem]:
        """Build action items from onboarding adapter issues."""
        items = []
        try:
            issues = adapter.list_issues() if hasattr(adapter, "list_issues") else []
            for issue in (issues or []):
                if not isinstance(issue, dict):
                    continue
                item = GovernanceActionItem(
                    action_id=_new_uuid(),
                    priority="P1",
                    action_type="IMPORT_RETRY",
                    symbol=issue.get("symbol"),
                    dataset=issue.get("dataset", ""),
                    source=issue.get("source", ""),
                    title=f"Import issue: {issue.get('issue', 'unknown')}",
                    description=str(issue),
                    reason_codes=[issue.get("issue", "IMPORT_ISSUE")],
                    source_module="ONBOARDING",
                    safe_action="RETRY_IMPORT",
                    suggested_command="python main.py import-batch --dry-run",
                    requires_manual_review=True,
                )
                item.priority = self._engine.assign_priority(item)
                items.append(item)
        except Exception as exc:
            logger.warning("build_from_onboarding error: %s", exc)
        return items

    def build_from_repairs(self, adapter) -> List[GovernanceActionItem]:
        """Build action items from repair adapter issues."""
        items = []
        try:
            issues = adapter.list_issues() if hasattr(adapter, "list_issues") else []
            for issue in (issues or []):
                if not isinstance(issue, dict):
                    continue
                item = GovernanceActionItem(
                    action_id=_new_uuid(),
                    priority="P1",
                    action_type="REVIEW_CONFLICT" if issue.get("issue") == "CONFLICT" else "REVIEW_INVALID_DATA",
                    symbol=issue.get("symbol"),
                    dataset=issue.get("dataset", ""),
                    title=f"Repair task: {issue.get('issue', 'unknown')}",
                    description=str(issue),
                    reason_codes=[issue.get("issue", "REPAIR_ISSUE")],
                    source_module="COVERAGE_REPAIR",
                    safe_action="REVIEW",
                    suggested_command="python main.py coverage-repair-tasks",
                    requires_manual_review=True,
                )
                item.priority = self._engine.assign_priority(item)
                items.append(item)
        except Exception as exc:
            logger.warning("build_from_repairs error: %s", exc)
        return items

    def build_from_freshness(self, adapter) -> List[GovernanceActionItem]:
        """Build action items from freshness adapter issues."""
        items = []
        try:
            issues = adapter.list_issues() if hasattr(adapter, "list_issues") else []
            for issue in (issues or []):
                if not isinstance(issue, dict):
                    continue
                item = GovernanceActionItem(
                    action_id=_new_uuid(),
                    priority="P2",
                    action_type="REVIEW_STALE_DATA",
                    symbol=issue.get("symbol"),
                    dataset=issue.get("dataset", ""),
                    title=f"Stale data: {issue.get('symbol', 'unknown')}",
                    description=str(issue),
                    reason_codes=[issue.get("issue", "STALE")],
                    source_module="FRESHNESS",
                    safe_action="REFRESH_COVERAGE",
                    suggested_command="python main.py freshness-repair-handoff",
                    requires_manual_review=True,
                )
                item.priority = self._engine.assign_priority(item)
                items.append(item)
        except Exception as exc:
            logger.warning("build_from_freshness error: %s", exc)
        return items

    def build_from_quality_gates(self, adapter) -> List[GovernanceActionItem]:
        """Build action items from quality gate adapter issues."""
        items = []
        try:
            issues = adapter.list_issues() if hasattr(adapter, "list_issues") else []
            for issue in (issues or []):
                if not isinstance(issue, dict):
                    continue
                item = GovernanceActionItem(
                    action_id=_new_uuid(),
                    priority="P1",
                    action_type="REVIEW_GATE_BLOCK",
                    symbol=issue.get("symbol"),
                    dataset=issue.get("dataset", ""),
                    title=f"Gate block: {issue.get('symbol', 'unknown')}",
                    description=str(issue),
                    reason_codes=[issue.get("issue", "GATE_BLOCK")],
                    source_module="QUALITY_GATES",
                    safe_action="REVIEW",
                    suggested_command="python main.py quality-gate-explain --stock " + str(issue.get("symbol", "")),
                    requires_manual_review=True,
                )
                item.priority = self._engine.assign_priority(item)
                items.append(item)
        except Exception as exc:
            logger.warning("build_from_quality_gates error: %s", exc)
        return items

    def build_from_enforcement(self, adapter) -> List[GovernanceActionItem]:
        """Build action items from enforcement adapter issues."""
        items = []
        try:
            issues = adapter.list_issues() if hasattr(adapter, "list_issues") else []
            for issue in (issues or []):
                if not isinstance(issue, dict):
                    continue
                item = GovernanceActionItem(
                    action_id=_new_uuid(),
                    priority="P0",
                    action_type="VERIFY_REPRODUCIBILITY",
                    symbol=None,
                    dataset="",
                    title=f"Non-qualified run: {issue.get('run_id', 'unknown')}",
                    description=str(issue),
                    reason_codes=["NON_QUALIFIED_RUN"],
                    source_module="GATE_ENFORCEMENT",
                    source_record_id=issue.get("run_id", ""),
                    safe_action="VERIFY_AUDIT",
                    suggested_command="python main.py gate-enforcement-verify --run-id " + str(issue.get("run_id", "")),
                    requires_manual_review=True,
                )
                item.priority = self._engine.assign_priority(item)
                items.append(item)
        except Exception as exc:
            logger.warning("build_from_enforcement error: %s", exc)
        return items

    def deduplicate(self, actions: List[GovernanceActionItem]) -> List[GovernanceActionItem]:
        """Remove duplicate actions for the same issue (same symbol+dataset+reason)."""
        seen = set()
        result = []
        for action in actions:
            key = (
                action.action_type,
                action.symbol or "",
                action.dataset,
                tuple(sorted(action.reason_codes or [])),
            )
            if key not in seen:
                seen.add(key)
                result.append(action)
        return result

    def prioritize(self, actions: List[GovernanceActionItem]) -> List[GovernanceActionItem]:
        """Assign priority to all actions and sort by priority."""
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        for action in actions:
            action.priority = self._engine.assign_priority(action)
        return sorted(actions, key=lambda a: (priority_order.get(a.priority, 4),))

    def list_open(self) -> List[GovernanceActionItem]:
        """Return open actions."""
        return [a for a in self._actions if a.status in ("OPEN", "IN_PROGRESS")]

    def list_by_priority(self, priority: str) -> List[GovernanceActionItem]:
        """Return actions matching priority."""
        return [a for a in self._actions if a.priority == priority]

    def list_by_symbol(self, symbol: str) -> List[GovernanceActionItem]:
        """Return actions for a specific symbol."""
        return [a for a in self._actions if a.symbol == symbol]

    def acknowledge(self, action_id: str) -> bool:
        """Acknowledge an action (metadata only — does not modify data)."""
        for action in self._actions:
            if action.action_id == action_id:
                action.status = "ACKNOWLEDGED"
                action.updated_at = _now_utc()
                self._append_audit_event(action_id, "ACTION_ACKNOWLEDGED", "")
                return True
        logger.warning("acknowledge: action_id not found: %s", action_id)
        return False

    def defer(self, action_id: str, reason: str) -> bool:
        """Defer an action (metadata only)."""
        for action in self._actions:
            if action.action_id == action_id:
                action.status = "DEFERRED"
                action.updated_at = _now_utc()
                self._append_audit_event(action_id, "ACTION_DEFERRED", reason)
                return True
        logger.warning("defer: action_id not found: %s", action_id)
        return False

    def resolve(self, action_id: str, note: str) -> bool:
        """Resolve an action (metadata only)."""
        for action in self._actions:
            if action.action_id == action_id:
                action.status = "RESOLVED"
                action.updated_at = _now_utc()
                self._append_audit_event(action_id, "ACTION_RESOLVED", note)
                return True
        logger.warning("resolve: action_id not found: %s", action_id)
        return False

    def export_queue(self, output_path: str) -> str:
        """Export action queue to CSV."""
        try:
            import csv
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            if not self._actions:
                # write header only
                with open(output_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=list(GovernanceActionItem.__dataclass_fields__.keys()) if hasattr(GovernanceActionItem, "__dataclass_fields__") else ["action_id", "priority", "action_type", "symbol", "title", "status"])
                    writer.writeheader()
                return output_path
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                rows = [a.to_dict() for a in self._actions]
                if rows:
                    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                    writer.writeheader()
                    writer.writerows(rows)
            return output_path
        except Exception as exc:
            logger.warning("export_queue error: %s", exc)
            return output_path

    def _append_audit_event(self, action_id: str, event_type: str, note: str) -> None:
        """Append action audit event (metadata audit only, no secrets)."""
        try:
            os.makedirs(os.path.dirname(self._audit_path), exist_ok=True)
            event = {
                "event_type": event_type,
                "action_id": action_id,
                "timestamp": _now_utc(),
                "note": note,
                "research_only": True,
                "no_real_orders": True,
            }
            with open(self._audit_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("_append_audit_event error: %s", exc)
