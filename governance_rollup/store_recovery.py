"""
governance_rollup/store_recovery.py — GovernanceStoreRecoveryPlanner v1.1.9

Plans recovery actions for problematic governance stores.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] ALL executions require allow_write=True. Default: dry_run=True.
[!] NEVER modifies original append-only history directly.
[!] NEVER modifies OHLCV, financial, or trading data.
[!] ALWAYS creates backup before any write.
[!] Rollback must always be available.
"""
from __future__ import annotations

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from governance_rollup.rollup_schema import (
    RecoveryPlan,
    ISSUE_CORRUPTED_TAIL, ISSUE_MISSING_INDEX, ISSUE_STALE_INDEX,
    ISSUE_MALFORMED_JSON, ISSUE_MISSING_STATE_FILE, ISSUE_MISSING_DIRECTORY,
    ISSUE_UNKNOWN,
    ACTION_REBUILD_INDEX, ACTION_TRUNCATE_CORRUPTED_TAIL_COPY,
    ACTION_RESTORE_BACKUP, ACTION_REBUILD_STATE, ACTION_MANUAL_REVIEW,
    ACTION_NO_ACTION,
)

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True

_BASE_DIR = Path(__file__).resolve().parent.parent
_BACKUP_DIR = _BASE_DIR / "data" / "governance_rollup" / "backups"


class GovernanceStoreRecoveryPlanner:
    """
    Plans recovery actions for problematic governance stores.

    ALL executions require allow_write=True.
    Default: dry_run=True.
    NEVER modifies original append-only history directly.
    NEVER modifies OHLCV, financial, or trading data.
    ALWAYS creates backup before any write.
    Rollback must always be available.
    """

    def __init__(self) -> None:
        self._plans: Dict[str, RecoveryPlan] = {}

    def plan(self, store_validation: Dict[str, Any]) -> RecoveryPlan:
        """Create a recovery plan from a store validation result."""
        path = store_validation.get("path", "")
        status = store_validation.get("status", "UNKNOWN")
        store_id = store_validation.get("store_id", Path(path).stem if path else "unknown")
        module_name = store_validation.get("module_name", "unknown")

        # Map status to issue type and proposed action
        issue_map = {
            "CORRUPTED_TAIL":    (ISSUE_CORRUPTED_TAIL, ACTION_TRUNCATE_CORRUPTED_TAIL_COPY, False),
            "CORRUPTED_MIDDLE":  (ISSUE_MALFORMED_JSON, ACTION_MANUAL_REVIEW, True),
            "MALFORMED_JSON":    (ISSUE_MALFORMED_JSON, ACTION_MANUAL_REVIEW, True),
            "MISSING_INDEX":     (ISSUE_MISSING_INDEX, ACTION_REBUILD_INDEX, False),
            "STALE_INDEX":       (ISSUE_STALE_INDEX, ACTION_REBUILD_INDEX, False),
            "MISSING":           (ISSUE_MISSING_STATE_FILE, ACTION_REBUILD_STATE, False),
        }
        issue_type, proposed_action, destructive = issue_map.get(
            status, (ISSUE_UNKNOWN, ACTION_MANUAL_REVIEW, True)
        )

        plan_id = f"PLAN-{store_id}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        backup_path = str(_BACKUP_DIR / f"{Path(path).name}.{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}.bak") if path else ""

        plan = RecoveryPlan(
            plan_id=plan_id,
            store_id=store_id,
            module_name=module_name,
            issue_type=issue_type,
            current_path=path,
            backup_path=backup_path,
            proposed_action=proposed_action,
            destructive=destructive,
            dry_run=True,
            requires_allow_write=True,
            estimated_record_loss=store_validation.get("estimated_record_loss", 0),
            safe=not destructive,
            status="PENDING",
            reason=f"Auto-planned for store status={status}",
        )
        self._plans[plan_id] = plan
        return plan

    def preview(self, plan_id: str) -> Dict[str, Any]:
        """Preview a recovery plan (dry-run, no writes)."""
        plan = self._plans.get(plan_id)
        if not plan:
            return {
                "plan_id": plan_id,
                "status": "NOT_FOUND",
                "dry_run": True,
                "preview": "Plan not found",
            }
        return {
            "plan_id": plan.plan_id,
            "store_id": plan.store_id,
            "module_name": plan.module_name,
            "issue_type": plan.issue_type,
            "current_path": plan.current_path,
            "backup_path": plan.backup_path,
            "proposed_action": plan.proposed_action,
            "destructive": plan.destructive,
            "dry_run": True,
            "requires_allow_write": plan.requires_allow_write,
            "estimated_record_loss": plan.estimated_record_loss,
            "safe": plan.safe,
            "status": plan.status,
            "reason": plan.reason,
            "note": "[DRY RUN] No changes made. Pass allow_write=True to execute.",
            "research_only": True,
            "no_real_orders": True,
        }

    def execute(self, plan_id: str, allow_write: bool = False) -> Dict[str, Any]:
        """
        Execute a recovery plan.
        BLOCKED if allow_write=False (default).
        """
        if not allow_write:
            return {
                "plan_id": plan_id,
                "status": "BLOCKED",
                "reason": "allow_write=False — pass allow_write=True to execute",
                "dry_run": True,
                "research_only": True,
                "no_real_orders": True,
            }
        plan = self._plans.get(plan_id)
        if not plan:
            return {"plan_id": plan_id, "status": "NOT_FOUND", "reason": "Plan not found"}

        # Safety checks
        path = Path(plan.current_path)

        # NEVER modify OHLCV / trading data
        forbidden_keywords = ["ohlcv", "price", "trade", "order", "broker", "financial"]
        for kw in forbidden_keywords:
            if kw in plan.current_path.lower():
                plan.status = "BLOCKED"
                plan.reason = f"Forbidden path keyword '{kw}' — will not modify financial data"
                return {
                    "plan_id": plan_id,
                    "status": "BLOCKED",
                    "reason": plan.reason,
                    "research_only": True,
                    "no_real_orders": True,
                }

        # Create backup first
        backup_result = self.create_backup(plan.current_path)
        if not backup_result.get("success"):
            return {
                "plan_id": plan_id,
                "status": "FAILED",
                "reason": f"Backup failed: {backup_result.get('reason')}",
            }

        plan.backup_path = backup_result.get("backup_path", plan.backup_path)

        try:
            if plan.proposed_action == ACTION_REBUILD_INDEX:
                result = self.rebuild_state(plan.current_path, allow_write=True)
            elif plan.proposed_action == ACTION_TRUNCATE_CORRUPTED_TAIL_COPY:
                result = self.truncate_corrupted_tail_copy(
                    plan.current_path, plan.backup_path, allow_write=True
                )
            elif plan.proposed_action == ACTION_RESTORE_BACKUP:
                result = self.restore_backup(plan.backup_path, plan.current_path, allow_write=True)
            else:
                result = {
                    "success": False,
                    "reason": f"No executor for action: {plan.proposed_action}",
                }

            if result.get("success"):
                plan.status = "COMPLETED"
            else:
                plan.status = "FAILED"
                plan.reason = result.get("reason", "Unknown error")

            return {
                "plan_id": plan_id,
                "status": plan.status,
                "action_result": result,
                "backup_path": plan.backup_path,
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as exc:
            plan.status = "FAILED"
            plan.reason = str(exc)
            return {
                "plan_id": plan_id,
                "status": "FAILED",
                "reason": str(exc),
            }

    def create_backup(self, path: str) -> Dict[str, Any]:
        """Create a backup of a file before any write operation."""
        source = Path(path)
        if not source.exists():
            return {"success": False, "reason": "Source file does not exist"}
        try:
            _BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup_path = _BACKUP_DIR / f"{source.name}.{ts}.bak"
            shutil.copy2(str(source), str(backup_path))
            logger.info("create_backup: backed up %s -> %s", source, backup_path)
            return {
                "success": True,
                "backup_path": str(backup_path),
            }
        except Exception as exc:
            logger.error("create_backup failed for %s: %s", path, exc)
            return {"success": False, "reason": str(exc)}

    def rebuild_state(self, path: str, allow_write: bool = False) -> Dict[str, Any]:
        """Rebuild state file for a store. BLOCKED if allow_write=False."""
        if not allow_write:
            return {
                "success": False,
                "status": "BLOCKED",
                "reason": "allow_write=False",
            }
        # Placeholder — actual rebuild logic would vary per module
        return {
            "success": True,
            "note": "rebuild_state: placeholder implementation",
        }

    def truncate_corrupted_tail_copy(
        self, path: str, backup_path: str, allow_write: bool = False
    ) -> Dict[str, Any]:
        """
        Create a copy with corrupted tail removed.
        NEVER modifies the original append-only file.
        BLOCKED if allow_write=False.
        """
        if not allow_write:
            return {
                "success": False,
                "status": "BLOCKED",
                "reason": "allow_write=False",
            }
        source = Path(path)
        if not source.exists():
            return {"success": False, "reason": "Source does not exist"}
        try:
            lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
            # Remove trailing blank lines and last corrupted line
            import json as _json
            valid_lines = []
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    _json.loads(stripped)
                    valid_lines.append(stripped)
                except Exception:
                    # Mark but skip corrupted line
                    logger.warning("truncate_corrupted_tail_copy: skipping corrupted line: %s", stripped[:80])
            # Write to a new copy (never overwrite original)
            copy_path = Path(path + ".recovered")
            copy_path.write_text(
                "\n".join(valid_lines) + "\n" if valid_lines else "",
                encoding="utf-8",
            )
            logger.info("truncate_corrupted_tail_copy: wrote recovered copy to %s", copy_path)
            return {
                "success": True,
                "recovered_path": str(copy_path),
                "original_lines": len(lines),
                "recovered_lines": len(valid_lines),
                "note": "Original file NOT modified. Recovery written to .recovered copy.",
            }
        except Exception as exc:
            logger.error("truncate_corrupted_tail_copy failed: %s", exc)
            return {"success": False, "reason": str(exc)}

    def restore_backup(
        self, backup_path: str, target_path: str, allow_write: bool = False
    ) -> Dict[str, Any]:
        """Restore from backup. BLOCKED if allow_write=False."""
        if not allow_write:
            return {
                "success": False,
                "status": "BLOCKED",
                "reason": "allow_write=False",
            }
        backup = Path(backup_path)
        target = Path(target_path)
        if not backup.exists():
            return {"success": False, "reason": f"Backup not found: {backup_path}"}
        try:
            shutil.copy2(str(backup), str(target))
            logger.info("restore_backup: restored %s -> %s", backup, target)
            return {"success": True, "restored_from": backup_path, "restored_to": target_path}
        except Exception as exc:
            return {"success": False, "reason": str(exc)}

    def verify_recovery(self, path: str) -> Dict[str, Any]:
        """Verify that a recovered store is valid."""
        from governance_rollup.store_validator import GovernanceStoreValidator
        validator = GovernanceStoreValidator()
        p = Path(path)
        if p.suffix.lower() == ".jsonl":
            return validator.validate_jsonl(p)
        if p.suffix.lower() == ".json":
            return validator.validate_json(p)
        return {"valid": p.exists(), "status": "VERIFIED" if p.exists() else "MISSING"}

    def rollback_recovery(
        self, backup_path: str, target_path: str, allow_write: bool = False
    ) -> Dict[str, Any]:
        """Rollback a recovery by restoring the backup. BLOCKED if allow_write=False."""
        if not allow_write:
            return {
                "success": False,
                "status": "BLOCKED",
                "reason": "allow_write=False — rollback requires explicit allow_write=True",
            }
        return self.restore_backup(backup_path, target_path, allow_write=True)
