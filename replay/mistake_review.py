"""
replay/mistake_review.py — ReplayMistakeReviewManager for v1.2.3

[!] Research Only. No Real Orders. Replay Training Only.
[!] Append-only review records.
[!] dismiss preserves original suggestion.
[!] override preserves original type/severity.
[!] reopen preserves history.
[!] SYSTEM cannot auto-CONFIRM.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_MISTAKE_CONFIRMATION_ENABLED = False


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_review_id() -> str:
    return f"MRV-{uuid.uuid4().hex[:12].upper()}"


class ReplayMistakeReviewManager:
    """
    Manages the lifecycle of mistake review records.

    Rules:
    - All reviews are append-only — never overwrites original mistake.
    - dismiss: preserves original suggestion, marks DISMISSED.
    - confirm: USER only — SYSTEM cannot auto-confirm.
    - override: preserves original type/severity in history.
    - reopen: preserves history, marks REOPENED.
    - reviewer: USER or SYSTEM_REVIEW. SYSTEM cannot CONFIRM.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True
    AUTO_MISTAKE_CONFIRMATION_ENABLED = False

    def __init__(self, store=None):
        self._store = store

    def confirm(
        self,
        mistake: Dict[str, Any],
        rationale: str = "",
        reviewer: str = "USER",
        notes: str = "",
    ) -> "MistakeReviewRecord":
        """
        Confirm a mistake. USER only — SYSTEM cannot auto-confirm.
        """
        from replay.scoring_schema import MistakeReviewRecord, MistakeStatus, ReviewerRole

        # Guard: System cannot auto-confirm
        if reviewer == ReviewerRole.SYSTEM_REVIEW.value:
            logger.warning("SYSTEM_REVIEW cannot auto-confirm mistakes. Downgrading to NEEDS_REVIEW.")
            return self._build_review(
                mistake=mistake,
                action="confirm_blocked",
                new_status=MistakeStatus.NEEDS_REVIEW.value,
                reviewer=reviewer,
                rationale=f"BLOCKED: System cannot auto-confirm. {rationale}",
                notes=notes,
            )

        return self._build_review(
            mistake=mistake,
            action="confirm",
            new_status=MistakeStatus.CONFIRMED.value,
            reviewer=reviewer,
            rationale=rationale,
            notes=notes,
        )

    def dismiss(
        self,
        mistake: Dict[str, Any],
        rationale: str = "",
        reviewer: str = "USER",
        notes: str = "",
    ) -> "MistakeReviewRecord":
        """
        Dismiss a mistake. Original suggestion preserved in history.
        """
        from replay.scoring_schema import MistakeReviewRecord, MistakeStatus

        return self._build_review(
            mistake=mistake,
            action="dismiss",
            new_status=MistakeStatus.DISMISSED.value,
            reviewer=reviewer,
            rationale=rationale,
            notes=notes,
        )

    def override(
        self,
        mistake: Dict[str, Any],
        override_type: Optional[str] = None,
        override_severity: Optional[str] = None,
        rationale: str = "",
        reviewer: str = "USER",
        notes: str = "",
    ) -> "MistakeReviewRecord":
        """
        Override mistake type or severity.
        Preserves original type/severity in review record.
        """
        from replay.scoring_schema import MistakeReviewRecord, MistakeStatus

        return self._build_review(
            mistake=mistake,
            action="override",
            new_status=MistakeStatus.OVERRIDDEN.value,
            reviewer=reviewer,
            rationale=rationale,
            override_type=override_type,
            override_severity=override_severity,
            notes=notes,
        )

    def reopen(
        self,
        mistake: Dict[str, Any],
        rationale: str = "",
        reviewer: str = "USER",
        notes: str = "",
    ) -> "MistakeReviewRecord":
        """
        Reopen a dismissed or overridden mistake.
        Preserves full review history.
        """
        from replay.scoring_schema import MistakeReviewRecord, MistakeStatus

        return self._build_review(
            mistake=mistake,
            action="reopen",
            new_status=MistakeStatus.REOPENED.value,
            reviewer=reviewer,
            rationale=rationale,
            notes=notes,
        )

    def _build_review(
        self,
        mistake: Dict[str, Any],
        action: str,
        new_status: str,
        reviewer: str,
        rationale: str = "",
        override_type: Optional[str] = None,
        override_severity: Optional[str] = None,
        notes: str = "",
    ) -> "MistakeReviewRecord":
        from replay.scoring_schema import MistakeReviewRecord

        record = MistakeReviewRecord(
            review_id=_new_review_id(),
            mistake_id=mistake.get("mistake_id", ""),
            session_id=mistake.get("session_id", ""),
            action=action,
            new_status=new_status,
            reviewer=reviewer,
            rationale=rationale,
            override_type=override_type,
            override_severity=override_severity,
            preserve_original=True,
            auto_confirmed=False,
            notes=notes,
        )

        # Persist if store available
        if self._store:
            try:
                self._store.append("mistake_review", record.to_dict())
            except Exception as exc:
                logger.warning("Failed to persist review record: %s", exc)

        return record
