"""
paper_trading/analytics/lesson_registry_v164.py — Lesson Registry v1.6.4

RESEARCH ONLY. PAPER SIMULATION ONLY. NO REAL ORDERS.
Versioned lessons. Human accept/reject only. No auto-apply strategy changes.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone

from paper_trading.analytics.enums_v164 import LessonStatus, ReviewScope
from paper_trading.analytics.models_v164 import LessonRecord

NO_REAL_ORDERS = True
PAPER_ONLY = True
AUTO_APPLY_LESSONS = False
AUTO_STRATEGY_CHANGE_ENABLED = False
AUTO_PARAMETER_CHANGE_ENABLED = False


class LessonRegistry:
    """
    Versioned local lesson registry.
    Human accept/reject/archive only.
    No auto-apply. No auto-strategy change.
    """

    def __init__(self) -> None:
        self._lessons: List[LessonRecord] = []

    def register(
        self,
        title: str,
        category: str,
        description: str,
        evidence_refs: Optional[List[str]] = None,
        applicable_scope: Optional[ReviewScope] = None,
        created_from_review: Optional[str] = None,
    ) -> LessonRecord:
        lesson = LessonRecord(
            lesson_id=str(uuid.uuid4()),
            title=title,
            category=category,
            description=description,
            evidence_refs=evidence_refs or [],
            applicable_scope=applicable_scope,
            created_from_review=created_from_review,
            version="1.6.4",
            status=LessonStatus.PROPOSED,
        )
        self._lessons.append(lesson)
        return lesson

    def accept(self, lesson_id: str) -> Optional[LessonRecord]:
        lesson = self._get(lesson_id)
        if lesson:
            lesson.status = LessonStatus.ACCEPTED
        return lesson

    def reject(self, lesson_id: str) -> Optional[LessonRecord]:
        lesson = self._get(lesson_id)
        if lesson:
            lesson.status = LessonStatus.REJECTED
        return lesson

    def archive(self, lesson_id: str) -> Optional[LessonRecord]:
        lesson = self._get(lesson_id)
        if lesson:
            lesson.status = LessonStatus.ARCHIVED
        return lesson

    def list_all(self) -> List[LessonRecord]:
        return list(self._lessons)

    def list_by_status(self, status: LessonStatus) -> List[LessonRecord]:
        return [l for l in self._lessons if l.status == status]

    def _get(self, lesson_id: str) -> Optional[LessonRecord]:
        for lesson in self._lessons:
            if lesson.lesson_id == lesson_id:
                return lesson
        return None


__all__ = ["LessonRegistry", "AUTO_APPLY_LESSONS"]
