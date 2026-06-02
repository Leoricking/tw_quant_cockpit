"""
coach/checklist_builder.py — ResearchChecklistBuilder (v0.4.8).

Builds daily and weekly research checklists.
All tasks are research-only — no buy/sell/order suggestions.

[!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List

from coach.coach_schema import (
    CoachRecommendation,
    REC_DAILY_CHECKLIST, REC_WEEKLY_CHECKLIST,
    PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    CAT_DATA, CAT_PROVIDER, CAT_WORKFLOW, CAT_RULE,
    CAT_REPLAY, CAT_JOURNAL, CAT_MODEL, CAT_LEARNING,
    EFFORT_QUICK, EFFORT_MEDIUM,
    DUE_TODAY, DUE_THIS_WEEK,
    STATUS_OPEN,
)

logger = logging.getLogger(__name__)


class ResearchChecklistBuilder:
    """
    Builds daily and weekly research checklists.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
      All suggested_commands are research-only.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def build_daily_checklist(self, context: dict = None) -> List[CoachRecommendation]:
        """Build the standard daily research checklist."""
        context = context or {}
        items = [
            self._item(
                rec_type=REC_DAILY_CHECKLIST,
                priority=PRIORITY_P1,
                category=CAT_DATA,
                title="Check Data Quality Gate",
                summary="Verify data freshness, coverage, and quality gates.",
                suggested_command="python main.py data-quality-gate --mode real",
                expected_benefit="Detect stale or missing data before research.",
                effort=EFFORT_QUICK,
                due=DUE_TODAY,
                tags=["data", "daily"],
            ),
            self._item(
                rec_type=REC_DAILY_CHECKLIST,
                priority=PRIORITY_P1,
                category=CAT_PROVIDER,
                title="Check Provider Reliability",
                summary="Check data provider health and fallback status.",
                suggested_command="python main.py provider-reliability --mode real",
                expected_benefit="Ensure data sources are healthy.",
                effort=EFFORT_QUICK,
                due=DUE_TODAY,
                tags=["provider", "daily"],
            ),
            self._item(
                rec_type=REC_DAILY_CHECKLIST,
                priority=PRIORITY_P1,
                category=CAT_WORKFLOW,
                title="Check Notification Center",
                summary="Review any new warnings, critical alerts, or data events.",
                suggested_command="python main.py notification-list",
                expected_benefit="Stay aware of system alerts and data issues.",
                effort=EFFORT_QUICK,
                due=DUE_TODAY,
                tags=["notification", "daily"],
            ),
            self._item(
                rec_type=REC_DAILY_CHECKLIST,
                priority=PRIORITY_P1,
                category=CAT_WORKFLOW,
                title="Check Research Review Dashboard",
                summary="Review today's overall research score and open items.",
                suggested_command="python main.py research-review-summary",
                expected_benefit="Get today's research health at a glance.",
                effort=EFFORT_QUICK,
                due=DUE_TODAY,
                tags=["review", "daily"],
            ),
            self._item(
                rec_type=REC_DAILY_CHECKLIST,
                priority=PRIORITY_P2,
                category=CAT_JOURNAL,
                title="Check Journal Review Queue",
                summary="Check if any journal entries are pending review.",
                suggested_command="python main.py journal-summary",
                expected_benefit="Keep trade journal reviewed and up to date.",
                effort=EFFORT_QUICK,
                due=DUE_TODAY,
                tags=["journal", "daily"],
            ),
            self._item(
                rec_type=REC_DAILY_CHECKLIST,
                priority=PRIORITY_P2,
                category=CAT_RULE,
                title="Check Rule Governance Needs Review",
                summary="Check if any rules have low/weak confidence needing review.",
                suggested_command="python main.py rule-governance --mode real",
                expected_benefit="Identify rules needing more data or manual review.",
                effort=EFFORT_QUICK,
                due=DUE_TODAY,
                tags=["rule", "daily"],
            ),
            self._item(
                rec_type=REC_DAILY_CHECKLIST,
                priority=PRIORITY_P2,
                category=CAT_REPLAY,
                title="Check Replay Training Focus",
                summary="Review intraday replay training status and today's practice focus.",
                suggested_command="python main.py intraday-replay --mode real",
                expected_benefit="Identify scenario practice for today.",
                effort=EFFORT_QUICK,
                due=DUE_TODAY,
                tags=["replay", "daily"],
            ),
            self._item(
                rec_type=REC_DAILY_CHECKLIST,
                priority=PRIORITY_P2,
                category=CAT_MODEL,
                title="Check ML Knowledge Leakage",
                summary="Verify ML feature leakage status before any model review.",
                suggested_command="python main.py ml-knowledge-feature-summary",
                expected_benefit="Ensure ML features are safe before study.",
                effort=EFFORT_QUICK,
                due=DUE_TODAY,
                tags=["ml", "daily"],
            ),
            self._item(
                rec_type=REC_DAILY_CHECKLIST,
                priority=PRIORITY_P3,
                category=CAT_WORKFLOW,
                title="Read Auto Report Daily Summary",
                summary="Read today's auto-generated research report.",
                suggested_command="python main.py auto-report --mode real --profile daily",
                expected_benefit="Get comprehensive daily research output.",
                effort=EFFORT_MEDIUM,
                due=DUE_TODAY,
                tags=["report", "daily"],
            ),
        ]
        return items

    def build_weekly_checklist(self, context: dict = None) -> List[CoachRecommendation]:
        """Build the standard weekly research checklist."""
        context = context or {}
        items = [
            self._item(
                rec_type=REC_WEEKLY_CHECKLIST,
                priority=PRIORITY_P1,
                category=CAT_JOURNAL,
                title="Review top mistakes this week",
                summary="Identify the most repeated mistake tags and plan replay practice.",
                suggested_command="python main.py journal-summary",
                expected_benefit="Understand persistent process errors.",
                effort=EFFORT_MEDIUM,
                due=DUE_THIS_WEEK,
                tags=["mistake", "weekly"],
            ),
            self._item(
                rec_type=REC_WEEKLY_CHECKLIST,
                priority=PRIORITY_P1,
                category=CAT_RULE,
                title="Review weak rules this week",
                summary="Identify rules with insufficient sample or low confidence.",
                suggested_command="python main.py rule-governance --mode real",
                expected_benefit="Focus backtest effort on rules that need validation.",
                effort=EFFORT_MEDIUM,
                due=DUE_THIS_WEEK,
                tags=["rule", "weekly"],
            ),
            self._item(
                rec_type=REC_WEEKLY_CHECKLIST,
                priority=PRIORITY_P2,
                category=CAT_REPLAY,
                title="Review replay training progress",
                summary="Assess which replay scenarios were practiced this week.",
                suggested_command="python main.py replay-training-summary",
                expected_benefit="Track skill development in scenario practice.",
                effort=EFFORT_MEDIUM,
                due=DUE_THIS_WEEK,
                tags=["replay", "weekly"],
            ),
            self._item(
                rec_type=REC_WEEKLY_CHECKLIST,
                priority=PRIORITY_P2,
                category=CAT_MODEL,
                title="Review model monitoring warnings",
                summary="Check for drift or degradation in prediction models.",
                suggested_command="python main.py model-monitoring --mode real",
                expected_benefit="Catch model drift before it affects decisions.",
                effort=EFFORT_MEDIUM,
                due=DUE_THIS_WEEK,
                tags=["model", "weekly"],
            ),
            self._item(
                rec_type=REC_WEEKLY_CHECKLIST,
                priority=PRIORITY_P2,
                category=CAT_JOURNAL,
                title="Review portfolio journal outcomes",
                summary="Summarize this week's simulated trade outcomes and process quality.",
                suggested_command="python main.py journal-summary",
                expected_benefit="Track trading process quality trend.",
                effort=EFFORT_MEDIUM,
                due=DUE_THIS_WEEK,
                tags=["journal", "weekly"],
            ),
            self._item(
                rec_type=REC_WEEKLY_CHECKLIST,
                priority=PRIORITY_P2,
                category=CAT_DATA,
                title="Review data blockers",
                summary="Review any persistent data quality issues blocking backtest.",
                suggested_command="python main.py data-quality-gate --mode real",
                expected_benefit="Clear data blockers before next week.",
                effort=EFFORT_MEDIUM,
                due=DUE_THIS_WEEK,
                tags=["data", "weekly"],
            ),
            self._item(
                rec_type=REC_WEEKLY_CHECKLIST,
                priority=PRIORITY_P3,
                category=CAT_LEARNING,
                title="Update research notes",
                summary="Write this week's observations and learnings to journal.",
                suggested_command="python main.py journal-summary",
                expected_benefit="Build institutional knowledge over time.",
                effort=EFFORT_MEDIUM,
                due=DUE_THIS_WEEK,
                tags=["notes", "weekly"],
            ),
        ]
        return items

    @staticmethod
    def _item(
        rec_type: str,
        priority: str,
        category: str,
        title: str,
        summary: str,
        suggested_command: str,
        expected_benefit: str = "",
        effort: str = EFFORT_QUICK,
        due: str = DUE_TODAY,
        tags: List[str] = None,
    ) -> CoachRecommendation:
        return CoachRecommendation(
            recommendation_type=rec_type,
            priority=priority,
            category=category,
            title=title,
            summary=summary,
            suggested_command=suggested_command,
            expected_benefit=expected_benefit,
            effort_level=effort,
            due_type=due,
            tags=tags or [],
            status=STATUS_OPEN,
        )
