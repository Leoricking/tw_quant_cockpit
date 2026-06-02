"""
coach/research_assistant_engine.py — ResearchAssistantEngine (v0.4.8).

Research Assistant / Coach main engine.
Reads Research Review Dashboard output and all subsystems to generate
coaching recommendations: daily/weekly checklists, replay training plans,
rule review queues, data repair priorities, journal/process coaching,
model/ML coaching.

[!] Coaching Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No broker connection. No auto-weight changes. No real-order execution.
[!] suggested_command must be research-only. No buy/sell/order suggestions.
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

from coach.coach_schema import (
    CoachRecommendation,
    REC_SAFETY_CHECK, REC_JOURNAL_REVIEW, REC_MODEL_MONITORING_REVIEW,
    PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    CAT_SAFETY, CAT_JOURNAL, CAT_MODEL, CAT_DATA, CAT_PROVIDER,
    CAT_RULE, CAT_REPLAY, CAT_WORKFLOW,
    EFFORT_QUICK, EFFORT_MEDIUM,
    DUE_TODAY, DUE_THIS_WEEK,
    STATUS_OPEN,
)
from coach.checklist_builder import ResearchChecklistBuilder
from coach.replay_training_planner import ReplayTrainingPlanner
from coach.rule_review_queue import RuleReviewQueueBuilder
from coach.data_repair_planner import DataRepairPlanner

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchAssistantEngine:
    """
    Research Assistant / Coach main engine.

    Reads persisted Research Review output + subsystem summaries,
    then builds coaching recommendations for daily/weekly use.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
      No broker connection. No auto-weight changes. No real-order execution.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(
        self,
        review_output_dir: str = "data/backtest_results/research_review",
        journal_root:        str = "journal_data",
        notification_log_dir: str = "logs/notifications",
        report_dir:          str = "reports",
    ):
        self._review_output_dir = (
            os.path.join(_BASE_DIR, review_output_dir)
            if not os.path.isabs(review_output_dir)
            else review_output_dir
        )
        self._journal_root = journal_root
        self._notification_log_dir = notification_log_dir
        self._report_dir = report_dir

        self._review_summary:      dict = {}
        self._action_plan:         list = []
        self._journal_summary:     dict = {}
        self._notification_summary: dict = {}
        self._rule_governance_summary: dict = {}
        self._model_monitoring_summary: dict = {}
        self._replay_summary:      dict = {}
        self._ml_summary:          dict = {}

        self._checklist_builder    = ResearchChecklistBuilder()
        self._replay_planner       = ReplayTrainingPlanner()
        self._rule_queue_builder   = RuleReviewQueueBuilder()
        self._data_repair_planner  = DataRepairPlanner()

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run(self, mode: str = "real", period: str = "daily") -> dict:
        """
        Run the Research Assistant Coach for the given mode/period.

        Returns a summary dict with all coaching outputs.
        Does NOT execute any commands. No buy/sell/order.
        """
        logger.info("[Coach] Running ResearchAssistantEngine mode=%s period=%s", mode, period)

        self.load_research_review()
        self.load_action_plan()
        self.load_journal_summary()
        self.load_notification_summary()
        self.load_rule_governance_summary()
        self.load_model_monitoring_summary()
        self.load_replay_summary()
        self._load_ml_summary()

        daily_checklist  = self.build_daily_checklist()
        weekly_checklist = self.build_weekly_checklist()
        replay_plan      = self.build_replay_training_plan()
        rule_queue       = self.build_rule_review_queue()
        data_repair      = self.build_data_repair_priorities()
        journal_tasks    = self.build_journal_review_tasks()
        model_tasks      = self.build_model_monitoring_tasks()
        safety_tasks     = self.build_safety_tasks()

        all_recs: List[CoachRecommendation] = (
            daily_checklist + weekly_checklist + replay_plan +
            rule_queue + data_repair + journal_tasks + model_tasks + safety_tasks
        )

        summary = self.build_summary(
            mode=mode,
            period=period,
            all_recommendations=all_recs,
            daily_checklist=daily_checklist,
            weekly_checklist=weekly_checklist,
            replay_plan=replay_plan,
            rule_queue=rule_queue,
            data_repair=data_repair,
            journal_tasks=journal_tasks,
            model_tasks=model_tasks,
            safety_tasks=safety_tasks,
        )

        logger.info(
            "[Coach] Done. total=%d P0=%d P1=%d replay=%d rules=%d data_repair=%d",
            summary["total_recommendations"],
            summary["p0_count"], summary["p1_count"],
            summary["replay_tasks_count"],
            summary["rule_review_count"],
            summary["data_repair_count"],
        )
        return summary

    # ------------------------------------------------------------------
    # Loaders — all graceful fallback
    # ------------------------------------------------------------------

    def load_research_review(self) -> dict:
        """Load latest Research Review summary from persisted CSV."""
        try:
            from review.review_store import ResearchReviewStore
            store = ResearchReviewStore(output_dir=self._review_output_dir)
            self._review_summary = store.load_latest_summary() or {}
        except Exception as exc:
            logger.warning("[Coach] load_research_review failed: %s", exc)
            self._review_summary = {}
        return self._review_summary

    def load_action_plan(self) -> list:
        """Load latest action plan from persisted CSV."""
        try:
            from review.review_store import ResearchReviewStore
            store = ResearchReviewStore(output_dir=self._review_output_dir)
            self._action_plan = store.load_latest_action_plan() or []
        except Exception as exc:
            logger.warning("[Coach] load_action_plan failed: %s", exc)
            self._action_plan = []
        return self._action_plan

    def load_journal_summary(self) -> dict:
        """Load journal coach summary."""
        try:
            from journal.journal_analytics import JournalAnalytics
            analytics = JournalAnalytics()
            self._journal_summary = analytics.coach_summary()
        except Exception as exc:
            logger.warning("[Coach] load_journal_summary failed: %s", exc)
            self._journal_summary = {}
        return self._journal_summary

    def load_notification_summary(self) -> dict:
        """Load notification coach summary."""
        try:
            from notifications.notification_center import NotificationCenter
            nc = NotificationCenter()
            self._notification_summary = nc.coach_summary()
        except Exception as exc:
            logger.warning("[Coach] load_notification_summary failed: %s", exc)
            self._notification_summary = {}
        return self._notification_summary

    def load_rule_governance_summary(self) -> dict:
        """Load rule governance coach candidates."""
        try:
            from governance.rule_confidence import RuleConfidenceScorer
            scorer = RuleConfidenceScorer()
            self._rule_governance_summary = scorer.coach_rule_review_candidates()
        except Exception as exc:
            logger.warning("[Coach] load_rule_governance_summary failed: %s", exc)
            self._rule_governance_summary = {}
        return self._rule_governance_summary

    def load_model_monitoring_summary(self) -> dict:
        """Load model monitoring coach tasks."""
        try:
            from monitoring.model_monitor import ModelMonitor
            monitor = ModelMonitor()
            self._model_monitoring_summary = monitor.coach_model_monitoring_tasks()
        except Exception as exc:
            logger.warning("[Coach] load_model_monitoring_summary failed: %s", exc)
            self._model_monitoring_summary = {}
        return self._model_monitoring_summary

    def load_replay_summary(self) -> dict:
        """Load intraday replay coach focus."""
        try:
            from replay.intraday_replay import IntradayReplayCockpit
            cockpit = IntradayReplayCockpit()
            self._replay_summary = cockpit.coach_replay_focus()
        except Exception as exc:
            logger.warning("[Coach] load_replay_summary failed: %s", exc)
            self._replay_summary = {}
        return self._replay_summary

    def _load_ml_summary(self) -> dict:
        """Load ML knowledge coach tasks."""
        try:
            from ml.knowledge_feature_readiness import KnowledgeFeatureReadiness
            kfr = KnowledgeFeatureReadiness()
            self._ml_summary = kfr.coach_ml_knowledge_tasks()
        except Exception as exc:
            logger.warning("[Coach] _load_ml_summary failed: %s", exc)
            self._ml_summary = {}
        return self._ml_summary

    # ------------------------------------------------------------------
    # Builders
    # ------------------------------------------------------------------

    def build_daily_checklist(self) -> List[CoachRecommendation]:
        """Build standard daily research checklist."""
        return self._checklist_builder.build_daily_checklist(
            context=self._review_summary
        )

    def build_weekly_checklist(self) -> List[CoachRecommendation]:
        """Build standard weekly research checklist."""
        return self._checklist_builder.build_weekly_checklist(
            context=self._review_summary
        )

    def build_replay_training_plan(self) -> List[CoachRecommendation]:
        """Build replay training plan based on journal mistakes and replay summary."""
        return self._replay_planner.build(
            journal_summary=self._journal_summary,
            replay_summary=self._replay_summary,
            review_summary=self._review_summary,
        )

    def build_rule_review_queue(self) -> List[CoachRecommendation]:
        """Build rule review queue from governance and signal quality."""
        return self._rule_queue_builder.build(
            rule_governance=self._rule_governance_summary,
            review_summary=self._review_summary,
        )

    def build_data_repair_priorities(self) -> List[CoachRecommendation]:
        """Build data repair priority list from data quality and provider reliability."""
        repair_data = {}
        try:
            from quality.data_quality_gate import DataQualityGate
            gate = DataQualityGate()
            repair_data["quality"] = gate.coach_data_repair_candidates()
        except Exception as exc:
            logger.warning("[Coach] data_quality_gate coach failed: %s", exc)
            repair_data["quality"] = {}
        try:
            from data.providers.reliability_matrix import ProviderReliabilityMatrix
            prm = ProviderReliabilityMatrix()
            repair_data["provider"] = prm.coach_provider_repair_candidates()
        except Exception as exc:
            logger.warning("[Coach] provider_reliability coach failed: %s", exc)
            repair_data["provider"] = {}
        return self._data_repair_planner.build(
            repair_data=repair_data,
            review_summary=self._review_summary,
        )

    def build_journal_review_tasks(self) -> List[CoachRecommendation]:
        """Build journal/process coaching tasks."""
        items: List[CoachRecommendation] = []
        summary = self._journal_summary

        # Review backlog
        review_backlog = summary.get("review_backlog", 0)
        if review_backlog and review_backlog > 0:
            items.append(CoachRecommendation(
                recommendation_type=REC_JOURNAL_REVIEW,
                priority=PRIORITY_P1,
                category=CAT_JOURNAL,
                title=f"Clear Journal Review Backlog ({review_backlog} pending)",
                summary=f"There are {review_backlog} journal entries pending review.",
                suggested_command="python main.py journal-summary",
                expected_benefit="Keep trade journal reviewed and process feedback current.",
                effort_level=EFFORT_MEDIUM,
                due_type=DUE_TODAY,
                tags=["journal", "review", "backlog"],
                status=STATUS_OPEN,
            ))

        # Repeated mistakes
        top_mistakes = summary.get("top_mistakes", [])
        if top_mistakes:
            top_mistake = top_mistakes[0] if isinstance(top_mistakes, list) else str(top_mistakes)
            items.append(CoachRecommendation(
                recommendation_type=REC_JOURNAL_REVIEW,
                priority=PRIORITY_P2,
                category=CAT_JOURNAL,
                title=f"Address Repeated Mistake: {top_mistake}",
                summary=f"Most repeated mistake this period: {top_mistake}. Plan replay practice.",
                suggested_command="python main.py journal-summary",
                expected_benefit="Break repeated mistake patterns through focused practice.",
                effort_level=EFFORT_MEDIUM,
                due_type=DUE_THIS_WEEK,
                tags=["journal", "mistake", "process"],
                status=STATUS_OPEN,
            ))

        # Process focus
        process_focus = summary.get("process_focus", "")
        if process_focus:
            items.append(CoachRecommendation(
                recommendation_type=REC_JOURNAL_REVIEW,
                priority=PRIORITY_P3,
                category=CAT_JOURNAL,
                title=f"Process Focus: {process_focus}",
                summary=f"This week's process focus: {process_focus}.",
                suggested_command="python main.py journal-summary",
                expected_benefit="Maintain awareness of current process improvement target.",
                effort_level=EFFORT_QUICK,
                due_type=DUE_THIS_WEEK,
                tags=["journal", "process"],
                status=STATUS_OPEN,
            ))

        return items

    def build_model_monitoring_tasks(self) -> List[CoachRecommendation]:
        """Build model/ML coaching tasks."""
        items: List[CoachRecommendation] = []
        summary = self._model_monitoring_summary

        # Drift warnings
        drift_warnings = summary.get("drift_warnings", 0)
        if drift_warnings and drift_warnings > 0:
            items.append(CoachRecommendation(
                recommendation_type=REC_MODEL_MONITORING_REVIEW,
                priority=PRIORITY_P1,
                category=CAT_MODEL,
                title=f"Model Drift Warning ({drift_warnings} models)",
                summary=f"{drift_warnings} model(s) show performance drift. Review before study.",
                suggested_command="python main.py model-monitoring --mode real",
                expected_benefit="Catch model degradation before it affects research decisions.",
                effort_level=EFFORT_MEDIUM,
                due_type=DUE_TODAY,
                tags=["model", "drift", "monitoring"],
                status=STATUS_OPEN,
            ))

        # ML knowledge leakage
        ml_summary = self._ml_summary
        leakage_count = ml_summary.get("leakage_count", 0)
        if leakage_count and leakage_count > 0:
            items.append(CoachRecommendation(
                recommendation_type=REC_MODEL_MONITORING_REVIEW,
                priority=PRIORITY_P1,
                category=CAT_MODEL,
                title=f"ML Knowledge Leakage Detected ({leakage_count} features)",
                summary=f"{leakage_count} ML feature(s) have leakage risk. Do not use in backtests.",
                suggested_command="python main.py ml-knowledge-feature-summary",
                expected_benefit="Prevent biased backtest results from leaking features.",
                effort_level=EFFORT_QUICK,
                due_type=DUE_TODAY,
                tags=["ml", "leakage", "model"],
                status=STATUS_OPEN,
            ))

        # Features needing mapping
        needs_mapping = ml_summary.get("needs_mapping", 0)
        if needs_mapping and needs_mapping > 0:
            items.append(CoachRecommendation(
                recommendation_type=REC_MODEL_MONITORING_REVIEW,
                priority=PRIORITY_P2,
                category=CAT_MODEL,
                title=f"ML Features Need Mapping ({needs_mapping})",
                summary=f"{needs_mapping} ML feature(s) lack proper backtest mapping.",
                suggested_command="python main.py ml-knowledge-feature-summary",
                expected_benefit="Ensure ML features are ready for research use.",
                effort_level=EFFORT_MEDIUM,
                due_type=DUE_THIS_WEEK,
                tags=["ml", "mapping"],
                status=STATUS_OPEN,
            ))

        return items

    def build_safety_tasks(self) -> List[CoachRecommendation]:
        """Build safety check tasks."""
        items: List[CoachRecommendation] = []

        # Critical review items from Research Review
        critical_items = int(self._review_summary.get("critical_items", 0) or 0)
        if critical_items > 0:
            items.append(CoachRecommendation(
                recommendation_type=REC_SAFETY_CHECK,
                priority=PRIORITY_P0,
                category=CAT_SAFETY,
                title=f"Resolve {critical_items} Critical Research Items",
                summary=(
                    f"Research Review found {critical_items} critical item(s). "
                    "Resolve before any backtest or research session."
                ),
                suggested_command="python main.py research-review-summary",
                expected_benefit="Remove research blockers before starting session.",
                effort_level=EFFORT_QUICK,
                due_type=DUE_TODAY,
                tags=["safety", "critical"],
                status=STATUS_OPEN,
            ))

        # Always add safety reminder
        items.append(CoachRecommendation(
            recommendation_type=REC_SAFETY_CHECK,
            priority=PRIORITY_P3,
            category=CAT_SAFETY,
            title="Confirm Stable Release Status",
            summary="Run stable release check before any research session.",
            suggested_command="python main.py stable-release-check --mode real",
            expected_benefit="Ensure system is in a known-good research state.",
            effort_level=EFFORT_QUICK,
            due_type=DUE_TODAY,
            tags=["safety", "release"],
            status=STATUS_OPEN,
        ))

        return items

    # ------------------------------------------------------------------
    # Summary builder
    # ------------------------------------------------------------------

    def build_summary(
        self,
        mode: str = "real",
        period: str = "daily",
        all_recommendations: Optional[List[CoachRecommendation]] = None,
        daily_checklist: Optional[List[CoachRecommendation]] = None,
        weekly_checklist: Optional[List[CoachRecommendation]] = None,
        replay_plan: Optional[List[CoachRecommendation]] = None,
        rule_queue: Optional[List[CoachRecommendation]] = None,
        data_repair: Optional[List[CoachRecommendation]] = None,
        journal_tasks: Optional[List[CoachRecommendation]] = None,
        model_tasks: Optional[List[CoachRecommendation]] = None,
        safety_tasks: Optional[List[CoachRecommendation]] = None,
    ) -> dict:
        """Build coach session summary dict."""
        from datetime import datetime
        all_recs = all_recommendations or []

        p0 = [r for r in all_recs if r.priority == PRIORITY_P0]
        p1 = [r for r in all_recs if r.priority == PRIORITY_P1]
        p2 = [r for r in all_recs if r.priority == PRIORITY_P2]
        p3 = [r for r in all_recs if r.priority == PRIORITY_P3]

        return {
            "generated_at":            datetime.now().isoformat(timespec="seconds"),
            "mode":                    mode,
            "period":                  period,
            "coaching_only":           True,
            "research_only":           True,
            "no_real_orders":          True,
            "production_blocked":      True,
            "total_recommendations":   len(all_recs),
            "p0_count":                len(p0),
            "p1_count":                len(p1),
            "p2_count":                len(p2),
            "p3_count":                len(p3),
            "daily_checklist_count":   len(daily_checklist or []),
            "weekly_checklist_count":  len(weekly_checklist or []),
            "replay_tasks_count":      len(replay_plan or []),
            "rule_review_count":       len(rule_queue or []),
            "data_repair_count":       len(data_repair or []),
            "journal_tasks_count":     len(journal_tasks or []),
            "model_tasks_count":       len(model_tasks or []),
            "safety_tasks_count":      len(safety_tasks or []),
            "all_recommendations":     [r.to_dict() for r in all_recs],
            "daily_checklist":         [r.to_dict() for r in (daily_checklist or [])],
            "weekly_checklist":        [r.to_dict() for r in (weekly_checklist or [])],
            "replay_training_plan":    [r.to_dict() for r in (replay_plan or [])],
            "rule_review_queue":       [r.to_dict() for r in (rule_queue or [])],
            "data_repair_plan":        [r.to_dict() for r in (data_repair or [])],
            "journal_tasks":           [r.to_dict() for r in (journal_tasks or [])],
            "model_tasks":             [r.to_dict() for r in (model_tasks or [])],
            "safety_tasks":            [r.to_dict() for r in (safety_tasks or [])],
            "read_only":               True,
        }
