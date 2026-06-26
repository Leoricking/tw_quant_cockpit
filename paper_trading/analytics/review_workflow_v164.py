"""
paper_trading/analytics/review_workflow_v164.py — Review Workflow v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Legal transitions enforced. Evidence required to complete. No auto-complete.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from paper_trading.analytics.enums_v164 import ReviewStatus, ReviewScope, VALID_REVIEW_TRANSITIONS
from paper_trading.analytics.models_v164 import SessionReview

NO_REAL_ORDERS = True
PAPER_ONLY = True
AUTO_COMPLETE_REVIEW = False
AUTO_STRATEGY_CHANGE_ENABLED = False


class ReviewWorkflow:
    """
    Manages session reviews with legal state transitions.
    Evidence required to complete. Actor+reason required for transitions.
    COMPLETED cannot be directly deleted — only REOPENED.
    No auto-complete from analytics results.
    """

    def __init__(self) -> None:
        self._reviews: Dict[str, SessionReview] = {}

    def create(
        self,
        session_id: str,
        review_scope: ReviewScope,
        reviewer: str,
    ) -> SessionReview:
        now = datetime.now(tz=timezone.utc)
        review = SessionReview(
            review_id=str(uuid.uuid4()),
            session_id=session_id,
            status=ReviewStatus.PENDING,
            review_scope=review_scope,
            reviewer=reviewer,
            created_at=now,
            updated_at=now,
        )
        self._reviews[review.review_id] = review
        return review

    def transition(
        self,
        review_id: str,
        to_status: ReviewStatus,
        actor: str,
        reason: str,
    ) -> SessionReview:
        review = self._get(review_id)
        now = datetime.now(tz=timezone.utc)
        review.transition(to_status, actor, reason, now)
        return review

    def add_evidence(self, review_id: str, evidence_ref: str) -> None:
        review = self._get(review_id)
        if evidence_ref not in review.evidence_refs:
            review.evidence_refs.append(evidence_ref)

    def add_lesson(self, review_id: str, lesson: Any) -> None:
        review = self._get(review_id)
        review.lessons.append(lesson)

    def add_action_item(self, review_id: str, action_item: Any) -> None:
        review = self._get(review_id)
        review.action_items.append(action_item)

    def add_root_cause(self, review_id: str, rca: Any) -> None:
        review = self._get(review_id)
        review.root_causes.append(rca)

    def add_mistake(self, review_id: str, mistake: Any) -> None:
        review = self._get(review_id)
        review.mistakes.append(mistake)

    def get(self, review_id: str) -> Optional[SessionReview]:
        return self._reviews.get(review_id)

    def list_all(self) -> List[SessionReview]:
        return list(self._reviews.values())

    def list_by_status(self, status: ReviewStatus) -> List[SessionReview]:
        return [r for r in self._reviews.values() if r.status == status]

    def _get(self, review_id: str) -> SessionReview:
        review = self._reviews.get(review_id)
        if review is None:
            raise KeyError(f"Review {review_id} not found")
        return review


__all__ = ["ReviewWorkflow", "AUTO_COMPLETE_REVIEW"]
