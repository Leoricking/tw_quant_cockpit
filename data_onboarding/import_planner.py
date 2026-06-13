"""
data_onboarding/import_planner.py — ImportPlanner for TW Quant Cockpit v1.1.1.

Builds an ImportPlan from discovered + validated files.
Default: dry_run=True, destructive_disabled=True.
REPLACE_EXPLICIT requires explicit opt-in.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] REPLACE_EXPLICIT is BLOCKED by default.
[!] Conflicts always go to REVIEW — not auto-overwrite.
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

from data_onboarding.onboarding_schema import (
    ImportPlan, ImportPlanItem,
    IMPORT_MODE_MERGE_SAFE, IMPORT_MODE_APPEND_SAFE,
    IMPORT_MODE_REPLACE_EXPLICIT, IMPORT_MODE_DRY_RUN,
    PLAN_ACTION_MERGE_SAFE, PLAN_ACTION_APPEND_SAFE,
    PLAN_ACTION_REPLACE_EXPLICIT, PLAN_ACTION_SKIP,
    PLAN_ACTION_REVIEW, PLAN_ACTION_BLOCKED,
    VALIDATION_OK, VALIDATION_WARNING, VALIDATION_FAIL, VALIDATION_BLOCKED,
)


class ImportPlanner:
    """
    Builds an ImportPlan from discovered + validated files.
    Default: dry_run=True, destructive_disabled=True.
    REPLACE_EXPLICIT requires explicit opt-in.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def build_plan(
        self,
        path: str,
        mode: str = IMPORT_MODE_MERGE_SAFE,
        dry_run: bool = True,
        allow_replace: bool = False,
    ) -> ImportPlan:
        """
        Discover files, validate them, build plan items.
        REPLACE_EXPLICIT is BLOCKED unless allow_replace=True.
        Conflict files get action=REVIEW, not auto-overwrite.
        """
        from data_onboarding.file_discovery import ImportFileDiscovery
        from data_onboarding.file_validator import ImportFileValidator
        from data_onboarding.duplicate_detector import DuplicateDetector

        discovery = ImportFileDiscovery()
        validator = ImportFileValidator()
        dup_det   = DuplicateDetector()

        discovered = discovery.discover(path)
        items: List[ImportPlanItem] = []

        for disc in discovered:
            val_result = validator.validate(
                disc.file_path,
                disc.detected_symbol,
                disc.detected_dataset or 'daily',
            )
            item = self.plan_file(disc, mode, allow_replace, val_result, dup_det)
            items.append(item)

        # Build counts
        merge_count   = sum(1 for i in items if i.action == PLAN_ACTION_MERGE_SAFE)
        append_count  = sum(1 for i in items if i.action == PLAN_ACTION_APPEND_SAFE)
        replace_count = sum(1 for i in items if i.action == PLAN_ACTION_REPLACE_EXPLICIT)
        blocked_count = sum(1 for i in items if i.action == PLAN_ACTION_BLOCKED)
        review_count  = sum(1 for i in items if i.action == PLAN_ACTION_REVIEW)
        skip_count    = sum(1 for i in items if i.action == PLAN_ACTION_SKIP)

        plan = ImportPlan(
            plan_id=str(uuid.uuid4())[:8],
            created_at=datetime.now().isoformat(),
            source_path=path,
            total_files=len(items),
            merge_safe_count=merge_count,
            append_safe_count=append_count,
            replace_explicit_count=replace_count,
            blocked_count=blocked_count,
            review_count=review_count,
            skip_count=skip_count,
            items=items,
            dry_run=dry_run,
            destructive_disabled=True,
        )
        return plan

    def plan_file(self, discovered, mode: str, allow_replace: bool,
                  val_result=None, dup_det=None) -> ImportPlanItem:
        """Plan a single file."""
        file_path  = discovered.file_path
        symbol     = discovered.detected_symbol
        dataset    = discovered.detected_dataset or 'daily'
        file_type  = discovered.file_type
        val_status = VALIDATION_OK
        blocked_reason: Optional[str] = None

        if val_result is not None:
            val_status = val_result.status

        # Determine action
        if val_status == VALIDATION_BLOCKED:
            action = PLAN_ACTION_BLOCKED
            blocked_reason = "Validation BLOCKED"
        elif val_status == VALIDATION_FAIL:
            action = PLAN_ACTION_BLOCKED
            blocked_reason = "Validation FAILED — required columns missing or critical errors"
        elif mode == IMPORT_MODE_REPLACE_EXPLICIT:
            if not allow_replace:
                action = PLAN_ACTION_BLOCKED
                blocked_reason = "REPLACE_EXPLICIT requires allow_replace=True (destructive import disabled)"
            else:
                action = PLAN_ACTION_REPLACE_EXPLICIT
        elif val_status == VALIDATION_WARNING:
            # Check for conflicts
            if val_result is not None and val_result.conflict_count > 0:
                action = PLAN_ACTION_REVIEW
            else:
                action = PLAN_ACTION_MERGE_SAFE if mode == IMPORT_MODE_MERGE_SAFE else PLAN_ACTION_APPEND_SAFE
        else:
            # OK — check for conflicts via duplicate detector
            requires_review = False
            if dup_det is not None and symbol:
                try:
                    import pandas as pd
                    df = None
                    ext = os.path.splitext(file_path)[1].lower()
                    if ext == '.csv':
                        for enc in ['utf-8-sig', 'utf-8', 'big5', 'cp950']:
                            try:
                                df = pd.read_csv(file_path, encoding=enc)
                                break
                            except Exception:
                                continue
                    elif ext in ('.xlsx', '.xls'):
                        try:
                            df = pd.read_excel(file_path)
                        except Exception:
                            pass
                    if df is not None:
                        det = dup_det.detect_against_existing(df, symbol, dataset)
                        if det.get("conflicts", 0) > 0:
                            requires_review = True
                except Exception:
                    pass

            if requires_review:
                action = PLAN_ACTION_REVIEW
            elif mode == IMPORT_MODE_APPEND_SAFE:
                action = PLAN_ACTION_APPEND_SAFE
            else:
                action = PLAN_ACTION_MERGE_SAFE

        return ImportPlanItem(
            file_path=file_path,
            symbol=symbol,
            dataset=dataset,
            file_type=file_type,
            action=action,
            import_mode=mode,
            dry_run=True,
            destructive=(action == PLAN_ACTION_REPLACE_EXPLICIT),
            blocked_reason=blocked_reason,
            expected_new_rows=val_result.valid_rows if val_result else 0,
            expected_skip_rows=val_result.duplicate_count if val_result else 0,
            expected_conflict_rows=val_result.conflict_count if val_result else 0,
            requires_review=(action == PLAN_ACTION_REVIEW),
            validation_status=val_status,
        )

    def summarize_plan(self, plan: ImportPlan) -> dict:
        return {
            "plan_id":        plan.plan_id,
            "source_path":    plan.source_path,
            "total_files":    plan.total_files,
            "merge_safe":     plan.merge_safe_count,
            "append_safe":    plan.append_safe_count,
            "replace_explicit": plan.replace_explicit_count,
            "blocked":        plan.blocked_count,
            "review":         plan.review_count,
            "skip":           plan.skip_count,
            "dry_run":        plan.dry_run,
            "research_only":  True,
            "no_real_orders": True,
        }

    def list_blocked(self, plan: ImportPlan) -> List[ImportPlanItem]:
        return [i for i in plan.items if i.action == PLAN_ACTION_BLOCKED]

    def list_review(self, plan: ImportPlan) -> List[ImportPlanItem]:
        return [i for i in plan.items if i.action == PLAN_ACTION_REVIEW]
