"""
notifications/notification_rules.py — NotificationRuleEngine (v0.4.5).

Evaluates various system summaries and produces notification events.

[!] Notification Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No real-order execution. Signal/ML alerts are NOT trading instructions.
"""
from __future__ import annotations

import logging
from typing import List

from notifications.notification_schema import (
    NotificationEvent,
    EVENT_DATA_QUALITY_ALERT, EVENT_PROVIDER_FAILURE, EVENT_PROVIDER_RECOVERY,
    EVENT_SIGNAL_QUALITY_ALERT, EVENT_ML_KNOWLEDGE_LEAKAGE, EVENT_MODEL_MONITORING_ALERT,
    EVENT_INTRADAY_REPLAY_REMINDER, EVENT_EXPERIMENT_CREATED, EVENT_SYSTEM_HEALTH,
    EVENT_SAFETY_WARNING, EVENT_DAILY_REPORT_READY, EVENT_RULE_GOVERNANCE_REVIEW,
    SEV_INFO, SEV_NOTICE, SEV_WARNING, SEV_ERROR, SEV_CRITICAL,
    CAT_DATA, CAT_PROVIDER, CAT_SIGNAL, CAT_ML, CAT_REPLAY,
    CAT_EXPERIMENT, CAT_SAFETY, CAT_SYSTEM, CAT_REPORT, CAT_GOVERNANCE,
)

logger = logging.getLogger(__name__)


class NotificationRuleEngine:
    """
    Evaluates system summaries and produces notification events.

    Each evaluate_* method returns a list of NotificationEvent (may be empty).
    Methods never raise — failures return empty list.

    [!] Notification Only. No Real Orders. Research Only.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Safety check — always run first
    # ------------------------------------------------------------------

    def evaluate_safety(self, context: dict) -> List[NotificationEvent]:
        """
        Safety invariant checks. CRITICAL if any safety invariant violated.
        production_blocked=True is the EXPECTED safe state — not an error.
        """
        events = []
        try:
            if context.get("real_order_ready", False):
                events.append(NotificationEvent(
                    event_type=EVENT_SAFETY_WARNING, severity=SEV_CRITICAL,
                    title="SAFETY: REAL_ORDER_READY=True detected",
                    message="REAL_ORDER_READY must always be False. This is a critical safety violation.",
                    category=CAT_SAFETY, action_required=True, can_ignore=False,
                    next_steps=["Immediately investigate and disable real order capability"],
                ))
            if context.get("supports_real_orders", False):
                events.append(NotificationEvent(
                    event_type=EVENT_SAFETY_WARNING, severity=SEV_CRITICAL,
                    title="SAFETY: supports_real_orders=True detected",
                    message="Real order support must be disabled. Research only platform.",
                    category=CAT_SAFETY, action_required=True, can_ignore=False,
                ))
            if context.get("production_blocked") is False:
                events.append(NotificationEvent(
                    event_type=EVENT_SAFETY_WARNING, severity=SEV_CRITICAL,
                    title="SAFETY: production_blocked=False detected",
                    message="Production trading block has been removed. This is a critical safety violation.",
                    category=CAT_SAFETY, action_required=True, can_ignore=False,
                ))
        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_safety: %s", exc)
        return events

    # ------------------------------------------------------------------
    # Data Quality
    # ------------------------------------------------------------------

    def evaluate_data_quality(self, dq_summary: dict) -> List[NotificationEvent]:
        """
        Evaluate data quality gate summary.
        production_blocked=True is expected safe state — INFO, not ERROR.
        """
        events = []
        try:
            # production_blocked=True is expected
            if dq_summary.get("production_blocked", True):
                events.append(NotificationEvent(
                    event_type=EVENT_DATA_QUALITY_ALERT, severity=SEV_INFO,
                    title="Data Quality: Production Trading Blocked (expected)",
                    message="production_blocked=True is the expected safe state for this research platform.",
                    category=CAT_DATA, can_ignore=True,
                    source="data_quality_gate",
                ))

            score = dq_summary.get("backtest_readiness_score", 100)
            if isinstance(score, (int, float)) and score < 60:
                events.append(NotificationEvent(
                    event_type=EVENT_DATA_QUALITY_ALERT, severity=SEV_WARNING,
                    title=f"Data Quality: Low Backtest Readiness Score ({score:.0f})",
                    message=f"Backtest readiness score {score:.0f} is below threshold 60.",
                    category=CAT_DATA, action_required=True, can_ignore=True,
                    next_steps=["Check data imports", "Run data-freshness check", "Review blockers"],
                    source="data_quality_gate",
                ))

            # Stale data
            stale = dq_summary.get("stale_datasets", []) or dq_summary.get("staleness", {})
            if stale:
                events.append(NotificationEvent(
                    event_type=EVENT_DATA_QUALITY_ALERT, severity=SEV_WARNING,
                    title="Data Quality: Stale Data Detected",
                    message=f"Stale datasets found: {stale}",
                    category=CAT_DATA, action_required=True, can_ignore=True,
                    next_steps=["Run update-data", "Check provider health"],
                    source="data_quality_gate",
                ))

            # Mock contamination
            mock_score = dq_summary.get("mock_contamination_score", 0)
            if isinstance(mock_score, (int, float)) and mock_score > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_DATA_QUALITY_ALERT, severity=SEV_ERROR,
                    title=f"Data Quality: Mock Contamination Detected ({mock_score:.2f})",
                    message="Real-mode dataset contains mock data contamination.",
                    category=CAT_DATA, action_required=True, can_ignore=False,
                    next_steps=["Investigate mock data sources", "Re-import clean data"],
                    source="data_quality_gate",
                ))

            # Blockers
            blockers = dq_summary.get("blockers", [])
            for blocker in (blockers[:3] if isinstance(blockers, list) else []):
                events.append(NotificationEvent(
                    event_type=EVENT_DATA_QUALITY_ALERT, severity=SEV_WARNING,
                    title=f"Data Quality: Blocker — {blocker}",
                    message=str(blocker),
                    category=CAT_DATA, action_required=True, can_ignore=True,
                    source="data_quality_gate",
                ))

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_data_quality: %s", exc)
        return events

    # ------------------------------------------------------------------
    # Provider Health
    # ------------------------------------------------------------------

    def evaluate_provider_health(self, provider_summary: dict) -> List[NotificationEvent]:
        """Evaluate provider health summary."""
        events = []
        try:
            failures = provider_summary.get("failed", []) or provider_summary.get("failed_providers", [])
            for p in (failures[:3] if isinstance(failures, list) else []):
                events.append(NotificationEvent(
                    event_type=EVENT_PROVIDER_FAILURE, severity=SEV_WARNING,
                    title=f"Provider Failure: {p}",
                    message=f"Provider '{p}' failed health check.",
                    category=CAT_PROVIDER, action_required=True, can_ignore=True,
                    next_steps=["Check API token", "Run provider-health", "Verify network"],
                    source="provider_health",
                ))

            token_missing_no_fallback = provider_summary.get("token_missing_no_fallback", [])
            for p in (token_missing_no_fallback[:3] if isinstance(token_missing_no_fallback, list) else []):
                events.append(NotificationEvent(
                    event_type=EVENT_PROVIDER_FAILURE, severity=SEV_WARNING,
                    title=f"Provider: Token Missing (no fallback) — {p}",
                    message=f"Provider '{p}' has no token and no fallback available.",
                    category=CAT_PROVIDER, action_required=True, can_ignore=True,
                    next_steps=["Configure API token in .env", "Or use manual import fallback"],
                    source="provider_health",
                ))

            token_missing_with_fallback = provider_summary.get("token_missing_with_fallback", [])
            for p in (token_missing_with_fallback[:3] if isinstance(token_missing_with_fallback, list) else []):
                events.append(NotificationEvent(
                    event_type=EVENT_PROVIDER_FAILURE, severity=SEV_NOTICE,
                    title=f"Provider: Token Missing (fallback available) — {p}",
                    message=f"Provider '{p}' has no token but fallback is available.",
                    category=CAT_PROVIDER, can_ignore=True,
                    source="provider_health",
                ))

            retry_failed = provider_summary.get("retry_failed", [])
            for p in (retry_failed[:3] if isinstance(retry_failed, list) else []):
                events.append(NotificationEvent(
                    event_type=EVENT_PROVIDER_FAILURE, severity=SEV_ERROR,
                    title=f"Provider: Retry Failed — {p}",
                    message=f"Provider '{p}' failed after all retry attempts.",
                    category=CAT_PROVIDER, action_required=True, can_ignore=True,
                    source="provider_health",
                ))

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_provider_health: %s", exc)
        return events

    # ------------------------------------------------------------------
    # Signal Quality
    # ------------------------------------------------------------------

    def evaluate_signal_quality(self, signal_summary: dict) -> List[NotificationEvent]:
        """
        Evaluate signal quality summary.
        Signal alerts are NOT trading instructions — research only.
        """
        events = []
        try:
            disable_count = signal_summary.get("disable_count", 0) or signal_summary.get("disabled_signals", 0)
            if disable_count and int(disable_count) > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_SIGNAL_QUALITY_ALERT, severity=SEV_WARNING,
                    title=f"Signal Quality: {disable_count} Disabled Signals",
                    message=(
                        f"{disable_count} signals have been disabled due to quality issues. "
                        "NOT a trading instruction — research only."
                    ),
                    category=CAT_SIGNAL, action_required=True, can_ignore=True,
                    next_steps=["Review signal quality report", "Check data freshness"],
                    source="signal_quality_engine",
                ))

            reduce_count = signal_summary.get("reduce_count", 0) or signal_summary.get("reduced_signals", 0)
            if reduce_count and int(reduce_count) > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_SIGNAL_QUALITY_ALERT, severity=SEV_NOTICE,
                    title=f"Signal Quality: {reduce_count} Reduced Signals",
                    message=f"{reduce_count} signals have been reduced. NOT a trading instruction.",
                    category=CAT_SIGNAL, can_ignore=True,
                    source="signal_quality_engine",
                ))

            boost_count = signal_summary.get("boost_count", 0) or signal_summary.get("boosted_signals", 0)
            if boost_count and int(boost_count) > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_SIGNAL_QUALITY_ALERT, severity=SEV_INFO,
                    title=f"Signal Quality: {boost_count} Boosted Signals",
                    message=f"{boost_count} boosted signals available. NOT a trading instruction.",
                    category=CAT_SIGNAL, can_ignore=True,
                    source="signal_quality_engine",
                ))

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_signal_quality: %s", exc)
        return events

    # ------------------------------------------------------------------
    # ML Knowledge
    # ------------------------------------------------------------------

    def evaluate_ml_knowledge(self, ml_summary: dict) -> List[NotificationEvent]:
        """Evaluate ML knowledge integration summary."""
        events = []
        try:
            auto_enabled = ml_summary.get("auto_enabled_count", 0)
            if auto_enabled and int(auto_enabled) > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_ML_KNOWLEDGE_LEAKAGE, severity=SEV_CRITICAL,
                    title=f"ML Knowledge: auto_enabled_count = {auto_enabled} (CRITICAL — should be 0)",
                    message="ML knowledge features have auto_enabled=True. This violates the research platform safety invariant.",
                    category=CAT_ML, action_required=True, can_ignore=False,
                    next_steps=["Investigate and disable auto_enabled features immediately"],
                    source="ml_knowledge_integration",
                ))

            leakage_risk = ml_summary.get("leakage_risk_count", 0)
            if leakage_risk and int(leakage_risk) > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_ML_KNOWLEDGE_LEAKAGE, severity=SEV_WARNING,
                    title=f"ML Knowledge: {leakage_risk} Leakage Risk Feature(s)",
                    message=f"{leakage_risk} transcript-derived features have leakage risk.",
                    category=CAT_ML, action_required=True, can_ignore=True,
                    next_steps=["Run ml-knowledge-leakage-check", "Review leakage findings"],
                    source="ml_knowledge_integration",
                ))

            long_cycle = ml_summary.get("metadata_only_count", 0) or ml_summary.get("long_cycle_count", 0)
            if long_cycle and int(long_cycle) > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_ML_KNOWLEDGE_LEAKAGE, severity=SEV_NOTICE,
                    title=f"ML Knowledge: {long_cycle} Long-Cycle / Regime Feature(s) (Metadata Only)",
                    message=(
                        f"{long_cycle} features are regime/cycle metadata only. "
                        "not_for_short_term_label=True."
                    ),
                    category=CAT_ML, can_ignore=True,
                    source="ml_knowledge_integration",
                ))

            needs_backtest = ml_summary.get("needs_backtest_count", 0)
            if needs_backtest and int(needs_backtest) > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_ML_KNOWLEDGE_LEAKAGE, severity=SEV_NOTICE,
                    title=f"ML Knowledge: {needs_backtest} Feature(s) Need Backtest Validation",
                    message=f"{needs_backtest} rule candidate features require empirical backtest before use.",
                    category=CAT_ML, can_ignore=True,
                    source="ml_knowledge_integration",
                ))

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_ml_knowledge: %s", exc)
        return events

    # ------------------------------------------------------------------
    # Model Monitoring
    # ------------------------------------------------------------------

    def evaluate_model_monitoring(self, monitoring_summary: dict) -> List[NotificationEvent]:
        """Evaluate model monitoring summary."""
        events = []
        try:
            if monitoring_summary.get("drift_detected"):
                events.append(NotificationEvent(
                    event_type=EVENT_MODEL_MONITORING_ALERT, severity=SEV_WARNING,
                    title="Model Monitoring: Drift Detected",
                    message=str(monitoring_summary.get("drift_detail", "Feature drift detected in model monitoring.")),
                    category=CAT_ML, action_required=True, can_ignore=True,
                    next_steps=["Review model monitoring report", "Check data pipeline for changes"],
                    source="model_monitoring",
                ))

            if monitoring_summary.get("signal_degradation"):
                events.append(NotificationEvent(
                    event_type=EVENT_MODEL_MONITORING_ALERT, severity=SEV_WARNING,
                    title="Model Monitoring: Signal Degradation Detected",
                    message="Model signal quality has degraded. Research review recommended.",
                    category=CAT_ML, action_required=True, can_ignore=True,
                    source="model_monitoring",
                ))

            if monitoring_summary.get("missing_prediction_log"):
                events.append(NotificationEvent(
                    event_type=EVENT_MODEL_MONITORING_ALERT, severity=SEV_NOTICE,
                    title="Model Monitoring: Missing Prediction Log",
                    message="No prediction log found. Run model monitoring to populate.",
                    category=CAT_ML, can_ignore=True,
                    source="model_monitoring",
                ))

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_model_monitoring: %s", exc)
        return events

    # ------------------------------------------------------------------
    # Intraday Replay
    # ------------------------------------------------------------------

    def evaluate_intraday_replay(self, replay_summary: dict) -> List[NotificationEvent]:
        """Evaluate intraday replay training status."""
        events = []
        try:
            if replay_summary.get("training_not_run_recently"):
                events.append(NotificationEvent(
                    event_type=EVENT_INTRADAY_REPLAY_REMINDER, severity=SEV_NOTICE,
                    title="Intraday Replay: Training Not Run Recently",
                    message="Consider running an intraday replay training session to improve pattern recognition.",
                    category=CAT_REPLAY, can_ignore=True,
                    next_steps=["Run intraday-replay --mode real"],
                    source="intraday_replay",
                ))

            if replay_summary.get("fake_breakout_scenario_available"):
                events.append(NotificationEvent(
                    event_type=EVENT_INTRADAY_REPLAY_REMINDER, severity=SEV_INFO,
                    title="Intraday Replay: Fake Breakout Training Scenario Available",
                    message="A fake breakout training scenario is available in the replay cockpit.",
                    category=CAT_REPLAY, can_ignore=True,
                    source="intraday_replay",
                ))

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_intraday_replay: %s", exc)
        return events

    # ------------------------------------------------------------------
    # Experiment Registry
    # ------------------------------------------------------------------

    def evaluate_experiment_registry(self, experiment_summary: dict) -> List[NotificationEvent]:
        """Evaluate experiment registry status."""
        events = []
        try:
            new_experiments = experiment_summary.get("new_experiments", [])
            for exp in (new_experiments[:3] if isinstance(new_experiments, list) else []):
                exp_id = exp if isinstance(exp, str) else exp.get("experiment_id", "")
                events.append(NotificationEvent(
                    event_type=EVENT_EXPERIMENT_CREATED, severity=SEV_INFO,
                    title=f"Experiment Created: {exp_id}",
                    message=f"New experiment registered: {exp_id}",
                    category=CAT_EXPERIMENT, can_ignore=True,
                    related_experiment_id=exp_id,
                    source="experiment_registry",
                ))

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_experiment_registry: %s", exc)
        return events

    # ------------------------------------------------------------------
    # Scheduler
    # ------------------------------------------------------------------

    def evaluate_scheduler_result(self, task_result: dict) -> List[NotificationEvent]:
        """Evaluate scheduler task result."""
        events = []
        try:
            task_name = task_result.get("task_name", "unknown")
            status    = task_result.get("status", "")
            if status in ("FAILED", "ERROR"):
                events.append(NotificationEvent(
                    event_type=EVENT_SYSTEM_HEALTH, severity=SEV_ERROR,
                    title=f"Scheduler: Task Failed — {task_name}",
                    message=f"Scheduler task '{task_name}' failed: {task_result.get('error', '')}",
                    category=CAT_SYSTEM, action_required=True, can_ignore=True,
                    source="scheduler",
                ))
            elif status in ("PARTIAL",):
                events.append(NotificationEvent(
                    event_type=EVENT_SYSTEM_HEALTH, severity=SEV_NOTICE,
                    title=f"Scheduler: Task Partial — {task_name}",
                    message=f"Scheduler task '{task_name}' completed partially.",
                    category=CAT_SYSTEM, can_ignore=True,
                    source="scheduler",
                ))

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_scheduler_result: %s", exc)
        return events

    # ------------------------------------------------------------------
    # Portfolio Journal (v0.4.6)
    # ------------------------------------------------------------------

    def evaluate_portfolio_journal(self, journal_summary: dict) -> List[NotificationEvent]:
        """
        Evaluate portfolio journal summary and produce notification events.

        Rules:
          review_required_count > 0  → NOTICE
          repeated mistake tag >= 3  → WARNING
        """
        events = []
        try:
            from notifications.notification_schema import CAT_REPORT
            review_req    = journal_summary.get("review_required_count", 0)
            mistake_counts = journal_summary.get("mistake_counts", {})
            most_common   = journal_summary.get("most_common_mistake", "")

            if review_req > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_SYSTEM_HEALTH, severity=SEV_NOTICE,
                    title=f"Portfolio Journal: {review_req} Entries Require Review",
                    message=(
                        f"{review_req} closed simulated entries are awaiting outcome review. "
                        "Run 'journal-list' to see them."
                    ),
                    category=CAT_REPORT, action_required=False, can_ignore=True,
                    source="portfolio_journal",
                    next_steps=["Run: python main.py journal-list",
                                "Use: python main.py journal-review --id JOURNAL-xxxx --outcome WIN"],
                ))

            # Repeated mistake tag >= 3
            for tag, count in mistake_counts.items():
                if count >= 3:
                    events.append(NotificationEvent(
                        event_type=EVENT_SYSTEM_HEALTH, severity=SEV_WARNING,
                        title=f"Repeated Mistake: '{tag}' ({count}×)",
                        message=(
                            f"Mistake tag '{tag}' appears in {count} journal entries. "
                            "Review MistakeTaxonomy for suggested fixes."
                        ),
                        category=CAT_REPORT, action_required=False, can_ignore=True,
                        source="portfolio_journal",
                        next_steps=[f"Study mistake: {tag}",
                                    "Review journal entries with this tag"],
                    ))
                    break  # only one warning per scan for top repeated mistake

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_portfolio_journal: %s", exc)
        return events

    # ------------------------------------------------------------------
    # v0.4.7 Research Review Dashboard notification rules
    # ------------------------------------------------------------------

    def evaluate_research_review(self, review_summary: dict) -> list:
        """
        Evaluate research review summary and produce notification events.

        Triggers:
          - critical_items > 0  => WARNING or CRITICAL notification
          - action_items_count > 0  => NOTICE notification
          - repeated top_mistake present => WARNING notification

        [!] Review Only. Research Only. No Real Orders.
        """
        events = []
        try:
            critical_items  = int(review_summary.get("critical_items", 0))
            action_items    = int(review_summary.get("action_items_count", 0))
            top_mistake     = review_summary.get("most_common_mistake", "")

            if critical_items > 0:
                sev = SEV_CRITICAL if critical_items >= 3 else SEV_WARNING
                events.append(NotificationEvent(
                    event_type=EVENT_SYSTEM_HEALTH, severity=sev,
                    title=f"Research Review: {critical_items} critical item(s)",
                    message=(
                        f"Research Review Dashboard detected {critical_items} critical review item(s). "
                        "Immediate review recommended."
                    ),
                    category=CAT_REPORT, action_required=True, can_ignore=False,
                    source="research_review",
                    next_steps=["python main.py research-review --mode real --period daily"],
                ))

            if action_items > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_SYSTEM_HEALTH, severity=SEV_NOTICE,
                    title=f"Research Review: {action_items} action item(s)",
                    message=(
                        f"Research Review Dashboard has {action_items} pending action item(s). "
                        "Review action plan."
                    ),
                    category=CAT_REPORT, action_required=False, can_ignore=True,
                    source="research_review",
                    next_steps=["python main.py research-review-actions"],
                ))

            if top_mistake:
                events.append(NotificationEvent(
                    event_type=EVENT_SYSTEM_HEALTH, severity=SEV_WARNING,
                    title=f"Repeated Mistake in Review: '{top_mistake}'",
                    message=(
                        f"Research Review Dashboard flagged '{top_mistake}' as the most repeated mistake. "
                        "Practice replay recommended."
                    ),
                    category=CAT_REPORT, action_required=False, can_ignore=True,
                    source="research_review",
                    next_steps=["python main.py intraday-replay --mode real"],
                ))

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_research_review: %s", exc)
        return events

    # ------------------------------------------------------------------
    # v0.4.8 Research Assistant / Coach notification rules
    # ------------------------------------------------------------------

    def evaluate_research_coach(self, coach_summary: dict) -> list:
        """
        Evaluate research coach summary and produce notification events.

        Triggers:
          - p0_count > 0        => WARNING/CRITICAL notification
          - replay_tasks > 0    => NOTICE notification
          - data_repair > 0     => NOTICE notification

        [!] Coaching Only. Research Only. No Real Orders.
        """
        events = []
        try:
            p0_count     = int(coach_summary.get("p0_count", 0))
            replay_tasks = int(coach_summary.get("replay_tasks_count", 0))
            data_repair  = int(coach_summary.get("data_repair_count", 0))

            if p0_count > 0:
                sev = SEV_CRITICAL if p0_count >= 3 else SEV_WARNING
                events.append(NotificationEvent(
                    event_type=EVENT_SYSTEM_HEALTH, severity=sev,
                    title=f"Research Coach: {p0_count} P0 task(s) require attention",
                    message=(
                        f"Research Coach found {p0_count} P0-priority task(s). "
                        "Resolve before any research session."
                    ),
                    category=CAT_REPORT, action_required=True, can_ignore=False,
                    source="research_coach",
                    next_steps=["python main.py research-coach --mode real --period daily"],
                ))

            if replay_tasks > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_SYSTEM_HEALTH, severity=SEV_NOTICE,
                    title=f"Research Coach: {replay_tasks} replay training task(s)",
                    message=f"Research Coach has {replay_tasks} replay training task(s) pending.",
                    category=CAT_REPORT, action_required=False, can_ignore=True,
                    source="research_coach",
                    next_steps=["python main.py research-coach-replay-plan"],
                ))

            if data_repair > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_SYSTEM_HEALTH, severity=SEV_NOTICE,
                    title=f"Research Coach: {data_repair} data repair task(s)",
                    message=f"Research Coach has {data_repair} data repair task(s) pending.",
                    category=CAT_REPORT, action_required=False, can_ignore=True,
                    source="research_coach",
                    next_steps=["python main.py research-coach-data-repair"],
                ))

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_research_coach: %s", exc)
        return events

    # ------------------------------------------------------------------
    # v0.4.9 Research Workflow Automation notification rules
    # ------------------------------------------------------------------

    def evaluate_research_workflow(self, workflow_summary: dict) -> list:
        """
        Evaluate research workflow summary and produce notification events.

        Triggers:
          - tasks_failed > 0    => WARNING notification
          - blocked_count > 0   => NOTICE notification
          - package ready        => INFO notification

        [!] Workflow Only. Research Only. No Real Orders.
        """
        events = []
        try:
            failed_count  = int(workflow_summary.get("tasks_failed", 0) or 0)
            blocked_count = int(workflow_summary.get("tasks_skipped", 0) or 0)
            pkg_path      = workflow_summary.get("output_package_path", "")

            if failed_count > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_SYSTEM_HEALTH, severity=SEV_WARNING,
                    title=f"Research Workflow: {failed_count} task(s) failed",
                    message=f"Research workflow has {failed_count} failed task(s). Review workflow output.",
                    category=CAT_REPORT, action_required=True, can_ignore=False,
                    source="research_workflow",
                    next_steps=["python main.py research-workflow-tasks"],
                ))

            if blocked_count > 0:
                events.append(NotificationEvent(
                    event_type=EVENT_SYSTEM_HEALTH, severity=SEV_NOTICE,
                    title=f"Research Workflow: {blocked_count} command(s) BLOCKED",
                    message=f"{blocked_count} workflow command(s) were blocked by SafeCommandRegistry.",
                    category=CAT_SAFETY, action_required=False, can_ignore=True,
                    source="research_workflow",
                    next_steps=["python main.py research-workflow-summary"],
                ))

            if pkg_path:
                events.append(NotificationEvent(
                    event_type=EVENT_DAILY_REPORT_READY, severity=SEV_INFO,
                    title="Research Workflow: Daily package ready",
                    message=f"Daily research package generated: {pkg_path}",
                    category=CAT_REPORT, action_required=False, can_ignore=True,
                    source="research_workflow",
                    next_steps=["python main.py research-workflow-package --type daily_research"],
                ))

        except Exception as exc:
            logger.warning("NotificationRuleEngine.evaluate_research_workflow: %s", exc)
        return events
