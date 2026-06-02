"""
review/review_aggregator.py — ResearchReviewAggregator (v0.4.7).

Aggregates research results from all subsystems into a unified Research
Review Dashboard. No trading actions, no auto-weight changes, no broker
connection.

[!] Review Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from review.review_schema import (
    ReviewItem,
    REVIEW_TYPE_DAILY, REVIEW_TYPE_WEEKLY,
    REVIEW_TYPE_MISTAKE, REVIEW_TYPE_WEAK_RULE,
    REVIEW_TYPE_DATA_BLOCKER, REVIEW_TYPE_PROVIDER,
    REVIEW_TYPE_MODEL_MONITORING, REVIEW_TYPE_REPLAY_TRAINING,
    REVIEW_TYPE_SIGNAL_QUALITY, REVIEW_TYPE_JOURNAL,
    REVIEW_TYPE_EXPERIMENT, REVIEW_TYPE_SAFETY,
    SEV_INFO, SEV_NOTICE, SEV_WARNING, SEV_ERROR, SEV_CRITICAL, SEV_BLOCKED,
    CAT_MISTAKE, CAT_RULE, CAT_DATA, CAT_PROVIDER, CAT_MODEL,
    CAT_REPLAY, CAT_JOURNAL, CAT_EXPERIMENT, CAT_SAFETY,
    STATUS_OPEN,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchReviewAggregator:
    """
    Research Review Dashboard main aggregator.

    Collects summaries from all research subsystems and builds
    unified ReviewItems and a dashboard summary dict.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
      No broker calls. No auto-weight changes. No order submission.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(
        self,
        results_dir:           str = "data/backtest_results",
        report_dir:            str = "reports",
        journal_root:          str = "journal_data",
        notification_log_dir:  str = "logs/notifications",
        experiments_root:      str = "experiments",
    ):
        self._results_dir          = os.path.join(BASE_DIR, results_dir)
        self._report_dir           = os.path.join(BASE_DIR, report_dir)
        self._journal_root         = os.path.join(BASE_DIR, journal_root)
        self._notification_log_dir = os.path.join(BASE_DIR, notification_log_dir)
        self._experiments_root     = os.path.join(BASE_DIR, experiments_root)

        self._notification_summary:  Optional[dict] = None
        self._journal_summary:       Optional[dict] = None
        self._experiment_summary:    Optional[dict] = None
        self._rule_governance_summary: Optional[dict] = None
        self._model_monitoring_summary: Optional[dict] = None
        self._intraday_replay_summary: Optional[dict] = None
        self._data_quality_summary:  Optional[dict] = None
        self._provider_reliability_summary: Optional[dict] = None
        self._signal_quality_summary: Optional[dict] = None

        self._review_items: List[ReviewItem] = []

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(self, mode: str = "real", period: str = "daily") -> dict:
        """
        Run the full aggregation pipeline.

        Returns a dashboard summary dict. Never raises — subsystem
        failures are caught and logged as warnings.
        """
        self.collect_notifications()
        self.collect_journal_summary()
        self.collect_experiment_summary()
        self.collect_rule_governance_summary()
        self.collect_model_monitoring_summary()
        self.collect_intraday_replay_summary()
        self.collect_data_quality_summary()
        self.collect_provider_reliability_summary()
        self.collect_signal_quality_summary()
        self.build_review_items()
        summary = self.build_dashboard_summary()
        summary["mode"]   = mode
        summary["period"] = period
        return summary

    # ------------------------------------------------------------------
    # Subsystem collectors
    # ------------------------------------------------------------------

    def collect_notifications(self) -> None:
        try:
            from notifications.notification_center import NotificationCenter
            nc = NotificationCenter(log_dir=self._notification_log_dir)
            # Use get_review_summary if available, else build from list_events
            if hasattr(nc, "get_review_summary"):
                self._notification_summary = nc.get_review_summary()
            else:
                events = nc.list_events(limit=500)
                warnings  = [e for e in events if getattr(e, "severity", "") in ("WARNING", "ERROR", "CRITICAL", "BLOCKED")]
                critical  = [e for e in events if getattr(e, "severity", "") in ("CRITICAL", "BLOCKED")]
                unread    = [e for e in events if getattr(e, "status",   "") == "UNREAD"]
                self._notification_summary = {
                    "total":     len(events),
                    "warnings":  len(warnings),
                    "critical":  len(critical),
                    "unread":    len(unread),
                    "categories": {},
                }
            logger.info("[review] Notifications collected: %s", self._notification_summary)
        except Exception as exc:
            logger.warning("[review] collect_notifications failed: %s", exc)
            self._notification_summary = {"total": 0, "warnings": 0, "critical": 0, "unread": 0, "categories": {}}

    def collect_journal_summary(self) -> None:
        try:
            from journal.journal_analytics import JournalAnalytics
            ja = JournalAnalytics()
            if hasattr(ja, "build_review_summary"):
                self._journal_summary = ja.build_review_summary()
            else:
                result = ja.run()
                by_mistake = result.get("by_mistake_tag", [])
                top_mistake = by_mistake[0]["mistake_tag"] if by_mistake else ""
                self._journal_summary = {
                    "total_entries":       result.get("total_entries", 0),
                    "review_required":     result.get("review_required_count", 0),
                    "top_mistakes":        by_mistake[:5],
                    "most_common_mistake": top_mistake,
                    "process_quality":     result.get("process_quality", []),
                    "open_simulated":      result.get("open_simulated_count", 0),
                }
            logger.info("[review] Journal summary collected")
        except Exception as exc:
            logger.warning("[review] collect_journal_summary failed: %s", exc)
            self._journal_summary = {
                "total_entries": 0, "review_required": 0,
                "top_mistakes": [], "most_common_mistake": "",
                "process_quality": [], "open_simulated": 0,
            }

    def collect_experiment_summary(self) -> None:
        try:
            from experiments.experiment_registry import ExperimentRegistry
            reg = ExperimentRegistry(registry_root=self._experiments_root)
            experiments = reg.list_experiments() if hasattr(reg, "list_experiments") else []
            failed = [e for e in experiments if getattr(e, "status", "") in ("FAILED", "PARTIAL")]
            self._experiment_summary = {
                "total":   len(experiments),
                "failed":  len(failed),
                "partial": len([e for e in experiments if getattr(e, "status", "") == "PARTIAL"]),
                "latest":  getattr(experiments[0], "experiment_id", "") if experiments else "",
            }
            logger.info("[review] Experiment summary collected: %d experiments", len(experiments))
        except Exception as exc:
            logger.warning("[review] collect_experiment_summary failed: %s", exc)
            self._experiment_summary = {"total": 0, "failed": 0, "partial": 0, "latest": ""}

    def collect_rule_governance_summary(self) -> None:
        try:
            from governance.rule_registry import RuleRegistry
            from governance.rule_confidence import RuleConfidenceScorer
            reg = RuleRegistry()
            reg.load_builtin_rules()
            scorer = RuleConfidenceScorer(registry=reg, results_dir=self._results_dir)
            if hasattr(scorer, "rules_needing_review"):
                self._rule_governance_summary = scorer.rules_needing_review()
            else:
                result = scorer.run()
                weak   = result.get("weak_confidence", [])
                low    = result.get("low_confidence",  [])
                unkn   = result.get("unknown_confidence", [])
                exp    = result.get("experimental", [])
                self._rule_governance_summary = {
                    "total_rules":         result.get("rules_scored", 0),
                    "rules_needing_review": weak + low + unkn,
                    "experimental_rules":  exp,
                    "weak_count":          len(weak),
                    "low_count":           len(low),
                    "unknown_count":       len(unkn),
                }
            logger.info("[review] Rule governance summary collected")
        except Exception as exc:
            logger.warning("[review] collect_rule_governance_summary failed: %s", exc)
            self._rule_governance_summary = {
                "total_rules": 0, "rules_needing_review": [],
                "experimental_rules": [], "weak_count": 0,
                "low_count": 0, "unknown_count": 0,
            }

    def collect_model_monitoring_summary(self) -> None:
        try:
            from monitoring.model_monitor import ModelMonitor
            mm = ModelMonitor(results_dir=self._results_dir)
            if hasattr(mm, "get_review_summary"):
                self._model_monitoring_summary = mm.get_review_summary()
            else:
                result = mm.run() if hasattr(mm, "run") else {}
                self._model_monitoring_summary = {
                    "drift_warnings":        result.get("drift_warnings", 0),
                    "degradation_warnings":  result.get("degradation_warnings", 0),
                    "missing_logs":          result.get("missing_logs", 0),
                    "model_health":          result.get("model_health", "UNKNOWN"),
                }
            logger.info("[review] Model monitoring summary collected")
        except Exception as exc:
            logger.warning("[review] collect_model_monitoring_summary failed (graceful): %s", exc)
            self._model_monitoring_summary = {
                "drift_warnings": 0, "degradation_warnings": 0,
                "missing_logs": 0, "model_health": "UNKNOWN",
            }

    def collect_intraday_replay_summary(self) -> None:
        try:
            from replay.replay_engine import IntradayReplayEngine
            engine = IntradayReplayEngine(results_dir=self._results_dir)
            if hasattr(engine, "get_training_summary"):
                self._intraday_replay_summary = engine.get_training_summary()
            else:
                self._intraday_replay_summary = {
                    "recent_sessions":    0,
                    "fake_breakout_done": False,
                    "vwap_done":          False,
                    "opening_range_done": False,
                    "training_overdue":   True,
                }
            logger.info("[review] Intraday replay summary collected")
        except Exception as exc:
            logger.warning("[review] collect_intraday_replay_summary failed (graceful): %s", exc)
            self._intraday_replay_summary = {
                "recent_sessions":    0,
                "fake_breakout_done": False,
                "vwap_done":          False,
                "opening_range_done": False,
                "training_overdue":   True,
            }

    def collect_data_quality_summary(self) -> None:
        try:
            from quality.data_quality_gate import DataQualityGate
            dqg = DataQualityGate(mode="real", results_dir=self._results_dir)
            if hasattr(dqg, "get_blockers_summary"):
                self._data_quality_summary = dqg.get_blockers_summary()
            else:
                result = dqg.run()
                gates  = result.get("gates", {})
                blockers = [k for k, v in gates.items() if v is False]
                self._data_quality_summary = {
                    "production_blocked":   result.get("production_blocked", True),
                    "real_order_ready":     result.get("real_order_ready", False),
                    "blockers":             blockers,
                    "blocker_count":        len(blockers),
                    "backtest_score":       result.get("backtest_readiness_score", 0),
                    "production_score":     result.get("production_readiness_score", 0),
                }
            logger.info("[review] Data quality summary collected")
        except Exception as exc:
            logger.warning("[review] collect_data_quality_summary failed: %s", exc)
            self._data_quality_summary = {
                "production_blocked": True, "real_order_ready": False,
                "blockers": [], "blocker_count": 0,
                "backtest_score": 0, "production_score": 0,
            }

    def collect_provider_reliability_summary(self) -> None:
        try:
            from data.providers.reliability_matrix import ProviderReliabilityMatrix
            prm = ProviderReliabilityMatrix(
                results_dir=self._results_dir,
                import_root=os.path.join(BASE_DIR, "data", "import"),
                report_dir=self._report_dir,
                mode="real",
            )
            if hasattr(prm, "get_warning_summary"):
                self._provider_reliability_summary = prm.get_warning_summary()
            else:
                result = prm.run()
                recs   = result.get("recommendations", [])
                failed = [r for r in recs if "fail" in str(r).lower() or "missing" in str(r).lower()]
                self._provider_reliability_summary = {
                    "provider_warnings": len(recs),
                    "failed_providers":  len(failed),
                    "fallback_used":     result.get("fallback_used", False),
                    "recommendations":   recs[:5],
                }
            logger.info("[review] Provider reliability summary collected")
        except Exception as exc:
            logger.warning("[review] collect_provider_reliability_summary failed: %s", exc)
            self._provider_reliability_summary = {
                "provider_warnings": 0, "failed_providers": 0,
                "fallback_used": False, "recommendations": [],
            }

    def collect_signal_quality_summary(self) -> None:
        try:
            from analysis.signal_quality_engine import SignalQualityEngine
            sqe = SignalQualityEngine(
                results_dir=self._results_dir,
                reports_dir=self._report_dir,
                mode="real",
            )
            if hasattr(sqe, "get_weak_signal_summary"):
                self._signal_quality_summary = sqe.get_weak_signal_summary()
            else:
                result = sqe.run()
                recs_df = result.get("recommendations_df")
                disable = reduce = insuff = []
                if recs_df is not None and hasattr(recs_df, "iterrows"):
                    try:
                        for _, row in recs_df.iterrows():
                            rec = str(row.get("recommendation", ""))
                            if rec == "DISABLE":
                                disable.append(str(row.get("signal_name", "")))
                            elif rec == "REDUCE":
                                reduce.append(str(row.get("signal_name", "")))
                            elif rec == "INSUFFICIENT_SAMPLE":
                                insuff.append(str(row.get("signal_name", "")))
                    except Exception:
                        pass
                self._signal_quality_summary = {
                    "disable_signals":      disable,
                    "reduce_signals":       reduce,
                    "insufficient_signals": insuff,
                    "total_weak":           len(disable) + len(reduce) + len(insuff),
                }
            logger.info("[review] Signal quality summary collected")
        except Exception as exc:
            logger.warning("[review] collect_signal_quality_summary failed: %s", exc)
            self._signal_quality_summary = {
                "disable_signals": [], "reduce_signals": [],
                "insufficient_signals": [], "total_weak": 0,
            }

    # ------------------------------------------------------------------
    # Review item builder
    # ------------------------------------------------------------------

    def build_review_items(self) -> List[ReviewItem]:
        """Build ReviewItem list from all collected summaries."""
        items: List[ReviewItem] = []

        # --- Notifications ---
        ns = self._notification_summary or {}
        if ns.get("critical", 0) > 0:
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_DAILY,
                severity=SEV_CRITICAL,
                category=CAT_SAFETY,
                title=f"Critical notifications: {ns['critical']}",
                summary="There are unresolved critical notification events requiring immediate review.",
                source="notification_center",
                source_module="notifications.notification_center",
                action_required=True,
                recommended_action="python main.py notification-list",
                priority=1,
                tags=["notification", "critical"],
            ))
        if ns.get("warnings", 0) > 0:
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_DAILY,
                severity=SEV_WARNING,
                category=CAT_SAFETY,
                title=f"Warning notifications: {ns['warnings']}",
                summary="Warning-level notification events detected.",
                source="notification_center",
                source_module="notifications.notification_center",
                action_required=True,
                recommended_action="python main.py notification-list",
                priority=2,
                tags=["notification", "warning"],
            ))

        # --- Journal ---
        js = self._journal_summary or {}
        if js.get("review_required", 0) > 0:
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_JOURNAL,
                severity=SEV_WARNING,
                category=CAT_JOURNAL,
                title=f"Journal entries requiring review: {js['review_required']}",
                summary="Closed simulated trades have not been reviewed yet.",
                source="portfolio_journal",
                source_module="journal.journal_analytics",
                action_required=True,
                recommended_action="python main.py journal-summary",
                priority=2,
                tags=["journal", "review_required"],
            ))
        if js.get("most_common_mistake", ""):
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_MISTAKE,
                severity=SEV_WARNING,
                category=CAT_MISTAKE,
                title=f"Repeated mistake: {js['most_common_mistake']}",
                summary=f"Most common mistake tag: {js['most_common_mistake']}. Practice replay recommended.",
                source="portfolio_journal",
                source_module="journal.journal_analytics",
                action_required=True,
                recommended_action="python main.py intraday-replay --mode real",
                priority=2,
                tags=["mistake", "replay"],
            ))

        # --- Rule Governance ---
        rg = self._rule_governance_summary or {}
        weak_rules = rg.get("rules_needing_review", [])
        if weak_rules:
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_WEAK_RULE,
                severity=SEV_NOTICE,
                category=CAT_RULE,
                title=f"Rules needing review: {len(weak_rules)}",
                summary=f"{len(weak_rules)} rules have low/weak/unknown confidence and need manual review.",
                source="rule_governance",
                source_module="governance.rule_confidence",
                action_required=True,
                recommended_action="python main.py rule-governance --mode real",
                priority=2,
                tags=["rule", "weak", "review"],
            ))

        # --- Model Monitoring ---
        mm = self._model_monitoring_summary or {}
        if mm.get("drift_warnings", 0) > 0:
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_MODEL_MONITORING,
                severity=SEV_WARNING,
                category=CAT_MODEL,
                title=f"Model drift warnings: {mm['drift_warnings']}",
                summary="Model drift detected. Inspect model monitoring logs.",
                source="model_monitoring",
                source_module="monitoring.model_monitor",
                action_required=True,
                recommended_action="python main.py model-monitoring --mode real",
                priority=2,
                tags=["model", "drift"],
            ))
        if mm.get("degradation_warnings", 0) > 0:
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_MODEL_MONITORING,
                severity=SEV_WARNING,
                category=CAT_MODEL,
                title=f"Model degradation warnings: {mm['degradation_warnings']}",
                summary="Prediction degradation detected in model monitoring.",
                source="model_monitoring",
                source_module="monitoring.model_monitor",
                action_required=True,
                recommended_action="python main.py model-monitoring-report --mode real",
                priority=2,
                tags=["model", "degradation"],
            ))

        # --- Intraday Replay ---
        ir = self._intraday_replay_summary or {}
        if ir.get("training_overdue", False):
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_REPLAY_TRAINING,
                severity=SEV_NOTICE,
                category=CAT_REPLAY,
                title="Replay training overdue",
                summary="Intraday replay training has not been run recently. Practice recommended.",
                source="intraday_replay",
                source_module="replay.replay_engine",
                action_required=True,
                recommended_action="python main.py intraday-replay --mode real",
                priority=3,
                tags=["replay", "training"],
            ))

        # --- Data Quality ---
        dq = self._data_quality_summary or {}
        if dq.get("blocker_count", 0) > 0:
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_DATA_BLOCKER,
                severity=SEV_ERROR,
                category=CAT_DATA,
                title=f"Data quality blockers: {dq['blocker_count']}",
                summary=f"Data quality gates failed: {dq.get('blockers', [])}",
                source="data_quality_gate",
                source_module="quality.data_quality_gate",
                action_required=True,
                recommended_action="python main.py data-quality-gate --mode real",
                priority=1,
                tags=["data", "blocker"],
            ))

        # --- Provider Reliability ---
        pr = self._provider_reliability_summary or {}
        if pr.get("failed_providers", 0) > 0:
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_PROVIDER,
                severity=SEV_ERROR,
                category=CAT_PROVIDER,
                title=f"Provider failures: {pr['failed_providers']}",
                summary="One or more data providers failed with no valid fallback.",
                source="provider_reliability",
                source_module="data.providers.reliability_matrix",
                action_required=True,
                recommended_action="python main.py provider-reliability --mode real",
                priority=1,
                tags=["provider", "failure"],
            ))
        elif pr.get("provider_warnings", 0) > 0:
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_PROVIDER,
                severity=SEV_WARNING,
                category=CAT_PROVIDER,
                title=f"Provider warnings: {pr['provider_warnings']}",
                summary="Data provider warnings detected.",
                source="provider_reliability",
                source_module="data.providers.reliability_matrix",
                action_required=True,
                recommended_action="python main.py provider-reliability --mode real",
                priority=2,
                tags=["provider", "warning"],
            ))

        # --- Signal Quality ---
        sq = self._signal_quality_summary or {}
        if sq.get("total_weak", 0) > 0:
            items.append(ReviewItem(
                review_type=REVIEW_TYPE_SIGNAL_QUALITY,
                severity=SEV_NOTICE,
                category=CAT_RULE,
                title=f"Weak signals: {sq['total_weak']}",
                summary=f"DISABLE:{len(sq.get('disable_signals', []))} REDUCE:{len(sq.get('reduce_signals', []))} INSUFFICIENT:{len(sq.get('insufficient_signals', []))}",
                source="signal_quality",
                source_module="analysis.signal_quality_engine",
                action_required=False,
                recommended_action="python main.py signal-quality --mode real",
                priority=3,
                tags=["signal", "weak"],
            ))

        # --- Safety check ---
        items.append(ReviewItem(
            review_type=REVIEW_TYPE_SAFETY,
            severity=SEV_INFO,
            category=CAT_SAFETY,
            title="Production Trading BLOCKED",
            summary="REAL_ORDER_READY=False. Production Trading permanently blocked. Research Only.",
            source="system",
            source_module="review.review_aggregator",
            action_required=False,
            recommended_action="",
            priority=0,
            tags=["safety", "blocked"],
        ))

        self._review_items = items
        return items

    # ------------------------------------------------------------------
    # Dashboard summary builder
    # ------------------------------------------------------------------

    def build_dashboard_summary(self) -> dict:
        """Build the top-level dashboard summary dict."""
        items = self._review_items
        open_items     = [i for i in items if i.status == STATUS_OPEN]
        critical_items = [i for i in items if i.severity in (SEV_CRITICAL, SEV_BLOCKED)]
        warning_items  = [i for i in items if i.severity == SEV_WARNING]
        action_items   = [i for i in items if i.action_required]

        ns = self._notification_summary or {}
        js = self._journal_summary     or {}
        rg = self._rule_governance_summary or {}
        dq = self._data_quality_summary   or {}
        sq = self._signal_quality_summary or {}

        top_mistakes = []
        for m in js.get("top_mistakes", []):
            if isinstance(m, dict):
                top_mistakes.append(m.get("mistake_tag", str(m)))
            else:
                top_mistakes.append(str(m))

        return {
            "generated_at":           datetime.now().isoformat(timespec="seconds"),
            "total_review_items":     len(items),
            "open_items":             len(open_items),
            "critical_items":         len(critical_items),
            "warning_items":          len(warning_items),
            "top_mistakes":           top_mistakes[:5],
            "most_common_mistake":    js.get("most_common_mistake", ""),
            "weak_rules":             len(rg.get("rules_needing_review", [])),
            "data_blockers":          dq.get("blocker_count", 0),
            "provider_warnings":      (self._provider_reliability_summary or {}).get("provider_warnings", 0),
            "model_warnings":         (self._model_monitoring_summary or {}).get("drift_warnings", 0),
            "replay_training_overdue": (self._intraday_replay_summary or {}).get("training_overdue", False),
            "journal_review_required": js.get("review_required", 0),
            "experiment_count":        (self._experiment_summary or {}).get("total", 0),
            "action_items_count":      len(action_items),
            "safety_status":           "PRODUCTION_BLOCKED",
            "notification_critical":   ns.get("critical", 0),
            "notification_warnings":   ns.get("warnings", 0),
            "total_weak_signals":      sq.get("total_weak", 0),
            # Safety flags
            "read_only":          True,
            "no_real_orders":     True,
            "production_blocked": True,
            "real_order_ready":   False,
        }

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    def get_review_items(self) -> List[ReviewItem]:
        return self._review_items

    def get_notification_summary(self) -> dict:
        return self._notification_summary or {}

    def get_journal_summary(self) -> dict:
        return self._journal_summary or {}

    def get_rule_governance_summary(self) -> dict:
        return self._rule_governance_summary or {}

    def get_signal_quality_summary(self) -> dict:
        return self._signal_quality_summary or {}

    def get_data_quality_summary(self) -> dict:
        return self._data_quality_summary or {}

    def get_provider_reliability_summary(self) -> dict:
        return self._provider_reliability_summary or {}

    def get_model_monitoring_summary(self) -> dict:
        return self._model_monitoring_summary or {}

    def get_intraday_replay_summary(self) -> dict:
        return self._intraday_replay_summary or {}
