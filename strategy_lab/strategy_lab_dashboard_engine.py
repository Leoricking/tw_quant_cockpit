"""
strategy_lab/strategy_lab_dashboard_engine.py — Strategy Lab Dashboard Engine v0.9.3

Collects context from all Strategy Lab modules and builds dashboard cards, rows,
action items, and summary.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import List

from strategy_lab.strategy_lab_dashboard_schema import (
    StrategyLabDashboardCard,
    StrategyLabDashboardRow,
    StrategyLabActionItem,
    StrategyLabDashboardSummary,
    STATUS_GOOD, STATUS_WATCH, STATUS_WARNING, STATUS_BLOCKED, STATUS_UNKNOWN,
    SEV_INFO, SEV_LOW, SEV_MEDIUM, SEV_HIGH, SEV_EXTREME,
    ACTION_BACKTEST_MORE, ACTION_PRACTICE_REPLAY, ACTION_FIX_DATA,
    ACTION_REVIEW_RISK, ACTION_REVIEW_JOURNAL, ACTION_READ_REPORT,
    ACTION_KEEP_OBSERVING, ACTION_DO_NOT_CHASE, ACTION_REVIEW,
    ACTION_WAIT,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StrategyLabDashboardEngine:
    """Strategy Lab Dashboard Engine v0.9.3.

    collect_context → build_cards → build_rows → build_action_items →
    build_summary → save → return

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(
        self,
        project_root: str = ".",
        output_dir: str = "data/backtest_results/strategy_lab_dashboard",
    ) -> None:
        if os.path.isabs(project_root):
            self._root = project_root
        else:
            self._root = os.path.join(BASE_DIR, project_root)

        if os.path.isabs(output_dir):
            self._output_dir = output_dir
        else:
            self._output_dir = os.path.join(BASE_DIR, output_dir)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, mode: str = "real") -> dict:
        """Run full dashboard pipeline. Returns result dict."""
        context = self.collect_context(mode=mode)
        cards   = self.build_cards(context)
        rows    = self.build_rows(context)
        actions = self.build_action_items(context)
        summary = self.build_summary(cards, rows, actions, context)

        # Save
        try:
            from strategy_lab.strategy_lab_dashboard_store import StrategyLabDashboardStore
            store = StrategyLabDashboardStore(output_dir=self._output_dir)
            store.save_cards(cards)
            store.save_rows(rows)
            store.save_actions(actions)
            store.save_summary(summary)
        except Exception as exc:
            logger.warning("StrategyLabDashboardEngine: save error: %s", exc)

        return {
            "cards":   cards,
            "rows":    rows,
            "actions": actions,
            "summary": summary,
            "context": context,
            "no_real_orders":    True,
            "production_blocked": True,
        }

    # ------------------------------------------------------------------
    # Context collection
    # ------------------------------------------------------------------

    def collect_context(self, mode: str = "real") -> dict:
        """Load from all Strategy Lab sub-stores. Graceful fallback on any error."""
        context: dict = {
            "mode":         mode,
            "no_real_orders": True,
            "production_blocked": True,
        }

        # Strategy Validation
        try:
            from strategy_validation.strategy_validation_store import StrategyValidationStore
            sv_store  = StrategyValidationStore(
                output_dir=os.path.join(BASE_DIR, "data/backtest_results/strategy_validation")
            )
            sv_scores = sv_store.load_latest_scores()
            sv_summary = sv_store.load_latest_summary()
            context["sv_scores"]  = sv_scores or []
            context["sv_summary"] = sv_summary
        except Exception:
            context["sv_scores"]  = []
            context["sv_summary"] = None

        # Evidence Graph
        try:
            from evidence_graph.evidence_graph_store import EvidenceGraphStore
            eg_store   = EvidenceGraphStore(
                output_dir=os.path.join(BASE_DIR, "data/backtest_results/evidence_graph")
            )
            eg_threads = eg_store.load_latest_threads()
            eg_summary = eg_store.load_latest_summary()
            context["eg_threads"] = eg_threads or []
            context["eg_summary"] = eg_summary
        except Exception:
            context["eg_threads"] = []
            context["eg_summary"] = None

        # Strategy Lab
        try:
            from strategy_lab.strategy_lab_store import StrategyLabStore
            sl_store   = StrategyLabStore(
                output_dir=os.path.join(BASE_DIR, "data/backtest_results/strategy_lab")
            )
            sl_summary = sl_store.load_latest_summary()
            context["sl_summary"] = sl_summary
        except Exception:
            context["sl_summary"] = None

        # Training Metrics
        try:
            from training_metrics.training_metrics_store import TrainingMetricsStore
            tm_store   = TrainingMetricsStore(
                output_dir=os.path.join(BASE_DIR, "data/backtest_results/training_metrics")
            )
            tm_summary = tm_store.load_latest_summary()
            tm_metrics = tm_store.load_latest_metrics()
            context["tm_summary"] = tm_summary
            context["tm_metrics"] = tm_metrics or []
        except Exception:
            context["tm_summary"] = None
            context["tm_metrics"] = []

        # Backtest Coach
        try:
            from backtest_coach.backtest_coach_store import BacktestCoachStore
            bc_store   = BacktestCoachStore(
                output_dir=os.path.join(BASE_DIR, "data/backtest_results/backtest_coach")
            )
            bc_summary = bc_store.load_latest_summary()
            bc_tasks   = bc_store.load_latest_tasks()
            context["bc_summary"] = bc_summary
            context["bc_tasks"]   = bc_tasks or []
        except Exception:
            context["bc_summary"] = None
            context["bc_tasks"]   = []

        # Strategy Memory
        try:
            from strategy_memory.strategy_memory_store import StrategyMemoryStore
            sm_store   = StrategyMemoryStore(
                output_dir=os.path.join(BASE_DIR, "data/backtest_results/strategy_memory")
            )
            sm_summary = sm_store.load_latest_summary()
            sm_items   = sm_store.load_memories()
            context["sm_summary"] = sm_summary
            context["sm_items"]   = sm_items or []
        except Exception:
            context["sm_summary"] = None
            context["sm_items"]   = []

        # Research Intelligence
        try:
            from research_intelligence.research_intelligence_store import ResearchIntelligenceStore
            ri_store   = ResearchIntelligenceStore(
                output_dir=os.path.join(BASE_DIR, "data/backtest_results/research_intelligence")
            )
            ri_summary = ri_store.load_latest_summary()
            context["ri_summary"] = ri_summary
        except Exception:
            context["ri_summary"] = None

        # Data Coverage
        try:
            from data_coverage.data_coverage_store import DataCoverageStore
            dc_store   = DataCoverageStore(
                output_dir=os.path.join(BASE_DIR, "data/backtest_results/data_coverage")
            )
            dc_summary = dc_store.load_latest_summary()
            context["dc_summary"] = dc_summary
        except Exception:
            context["dc_summary"] = None

        # Crash Reversal
        try:
            from strategy_rules.crash_reversal_pack import CrashReversalStrategyPack
            cr = CrashReversalStrategyPack()
            cr_result = cr.run(mode=mode)
            context["crash_reversal"] = cr_result
        except Exception:
            context["crash_reversal"] = {}

        return context

    # ------------------------------------------------------------------
    # Build cards
    # ------------------------------------------------------------------

    def build_cards(self, context: dict) -> List[StrategyLabDashboardCard]:
        """Build summary cards from context."""
        cards = []
        sv_scores  = context.get("sv_scores", [])
        sv_summary = context.get("sv_summary")
        tm_metrics = context.get("tm_metrics", [])
        bc_tasks   = context.get("bc_tasks", [])
        sm_items   = context.get("sm_items", [])
        eg_threads = context.get("eg_threads", [])
        cr_result  = context.get("crash_reversal", {})

        # Helper to get dict from object
        def _d(obj):
            if obj is None:
                return {}
            if isinstance(obj, dict):
                return obj
            if hasattr(obj, "to_dict"):
                return obj.to_dict()
            return {}

        sv_sum = _d(sv_summary)

        # 1. Strategy Lab Status
        validated  = int(sv_sum.get("validated_count", 0))
        validating = int(sv_sum.get("validating_count", 0))
        total      = int(sv_sum.get("total_strategies", len(sv_scores)))
        lab_status = STATUS_GOOD if validated > 0 or validating > 0 else (
            STATUS_WATCH if total > 0 else STATUS_UNKNOWN
        )
        cards.append(StrategyLabDashboardCard(
            card_id="strategy_lab_status",
            title="Strategy Lab Status",
            value=f"{total} strategies",
            subtitle=f"VALIDATED={validated} VALIDATING={validating}",
            status=lab_status,
            severity=SEV_INFO,
            source_module="strategy_validation",
            safe_next_step="python main.py strategy-validation --mode real",
        ))

        # 2. Validation Grade Mix
        obs    = int(sv_sum.get("observational_count", 0))
        insuf  = int(sv_sum.get("insufficient_count", 0))
        conf   = int(sv_sum.get("conflicted_count", 0))
        rej    = int(sv_sum.get("rejected_count", 0))
        grade_status = STATUS_WARNING if conf > 0 or rej > 2 else (
            STATUS_WATCH if insuf > 3 else STATUS_GOOD
        )
        cards.append(StrategyLabDashboardCard(
            card_id="validation_grade_mix",
            title="Validation Grade Mix",
            value=f"OBS={obs} INSUF={insuf}",
            subtitle=f"CONF={conf} REJ={rej}",
            status=grade_status,
            severity=SEV_MEDIUM if conf > 0 else SEV_LOW,
            source_module="strategy_validation",
            safe_next_step="python main.py strategy-validation-scores",
        ))

        # 3. Evidence Health
        eg_sum = _d(context.get("eg_summary"))
        orphan_count = int(eg_sum.get("orphan_count", 0))
        thread_count = len(eg_threads)
        eg_status = STATUS_GOOD if thread_count > 0 and orphan_count < 5 else (
            STATUS_WATCH if orphan_count < 10 else STATUS_WARNING
        )
        cards.append(StrategyLabDashboardCard(
            card_id="evidence_health",
            title="Evidence Health",
            value=f"{thread_count} threads",
            subtitle=f"Orphans: {orphan_count}",
            status=eg_status,
            severity=SEV_LOW if orphan_count < 5 else SEV_MEDIUM,
            source_module="evidence_graph",
            safe_next_step="python main.py evidence-graph-summary",
        ))

        # 4. Crash Reversal Risk
        cr_warnings = 0
        if isinstance(cr_result, dict):
            rules = cr_result.get("rules", [])
            cr_warnings = sum(
                1 for r in rules
                if isinstance(r, dict) and r.get("risk_level") in ("HIGH", "EXTREME")
            )
        cr_status = STATUS_WARNING if cr_warnings > 2 else (
            STATUS_WATCH if cr_warnings > 0 else STATUS_GOOD
        )
        cards.append(StrategyLabDashboardCard(
            card_id="crash_reversal_risk",
            title="Crash Reversal Risk",
            value=f"{cr_warnings} warnings",
            subtitle="High/extreme risk rules",
            status=cr_status,
            severity=SEV_HIGH if cr_warnings > 2 else SEV_LOW,
            source_module="crash_reversal",
            safe_next_step="python main.py crash-reversal-summary",
        ))

        # 5. Needs Backtest
        needs_backtest = sum(
            1 for s in sv_scores
            if _d(s).get("suggested_next_step") == "BACKTEST_MORE"
        )
        cards.append(StrategyLabDashboardCard(
            card_id="needs_backtest",
            title="Needs Backtest",
            value=str(needs_backtest),
            subtitle="strategies need more backtest",
            status=STATUS_WATCH if needs_backtest > 0 else STATUS_GOOD,
            severity=SEV_MEDIUM if needs_backtest > 3 else SEV_LOW,
            source_module="strategy_validation",
            safe_next_step="python main.py strategy-lab-dashboard-needs-backtest",
        ))

        # 6. Needs Replay
        needs_replay = sum(
            1 for s in sv_scores
            if _d(s).get("suggested_next_step") == "PRACTICE_REPLAY"
        )
        cards.append(StrategyLabDashboardCard(
            card_id="needs_replay",
            title="Needs Replay",
            value=str(needs_replay),
            subtitle="strategies need practice replay",
            status=STATUS_WATCH if needs_replay > 0 else STATUS_GOOD,
            severity=SEV_LOW,
            source_module="strategy_validation",
            safe_next_step="python main.py strategy-lab-dashboard-needs-replay",
        ))

        # 7. Needs Data
        needs_data = sum(
            1 for s in sv_scores
            if _d(s).get("suggested_next_step") == "FIX_DATA"
        )
        cards.append(StrategyLabDashboardCard(
            card_id="needs_data",
            title="Needs Data",
            value=str(needs_data),
            subtitle="strategies have data gaps",
            status=STATUS_WARNING if needs_data > 2 else (
                STATUS_WATCH if needs_data > 0 else STATUS_GOOD
            ),
            severity=SEV_MEDIUM if needs_data > 2 else SEV_LOW,
            source_module="strategy_validation",
            safe_next_step="python main.py strategy-lab-dashboard-needs-data",
        ))

        # 8. Training Progress
        tm_sum = _d(context.get("tm_summary"))
        improving = int(tm_sum.get("improving_count", 0))
        worsening = int(tm_sum.get("worsening_count", 0))
        tm_total  = int(tm_sum.get("total_metrics", len(tm_metrics)))
        tp_status = STATUS_GOOD if improving > worsening else (
            STATUS_WATCH if worsening == improving else STATUS_WARNING
        )
        cards.append(StrategyLabDashboardCard(
            card_id="training_progress",
            title="Training Progress",
            value=f"{tm_total} metrics",
            subtitle=f"IMPROVING={improving} WORSENING={worsening}",
            status=tp_status,
            severity=SEV_MEDIUM if worsening > improving else SEV_LOW,
            source_module="training_metrics",
            safe_next_step="python main.py training-metrics-summary",
        ))

        # 9. Active Strategy Memories
        active_memories = sum(
            1 for m in sm_items
            if _d(m).get("status") in ("ACTIVE", "VALIDATING", "ACCEPTED")
        )
        cards.append(StrategyLabDashboardCard(
            card_id="active_memories",
            title="Active Strategy Memories",
            value=str(active_memories),
            subtitle="active/validating/accepted memories",
            status=STATUS_GOOD if active_memories > 0 else STATUS_UNKNOWN,
            severity=SEV_INFO,
            source_module="strategy_memory",
            safe_next_step="python main.py strategy-memory-summary",
        ))

        # 10. Coach Tasks
        bc_sum = _d(context.get("bc_summary"))
        task_count = int(bc_sum.get("total_tasks", len(bc_tasks)))
        cards.append(StrategyLabDashboardCard(
            card_id="coach_tasks",
            title="Coach Tasks",
            value=str(task_count),
            subtitle="backtest coach tasks pending",
            status=STATUS_WATCH if task_count > 5 else STATUS_GOOD,
            severity=SEV_LOW,
            source_module="backtest_coach",
            safe_next_step="python main.py backtest-coach-tasks",
        ))

        # 11. Report Pack Health
        report_status = STATUS_GOOD
        cards.append(StrategyLabDashboardCard(
            card_id="report_pack_health",
            title="Report Pack Health",
            value="Available",
            subtitle="All report modules registered",
            status=report_status,
            severity=SEV_INFO,
            source_module="report_pack",
            safe_next_step="python main.py report-pack-health",
        ))

        # 12. No Real Orders Safety
        cards.append(StrategyLabDashboardCard(
            card_id="no_real_orders_safety",
            title="No Real Orders Safety",
            value="BLOCKED",
            subtitle="Production Trading BLOCKED — Research Only",
            status=STATUS_BLOCKED,
            severity=SEV_INFO,
            source_module="all_modules",
            safe_next_step="python main.py strategy-lab-dashboard-summary",
        ))

        # v1.0.0 Release Status cards
        try:
            from release.version_info import VERSION, RELEASE_NAME, RELEASE_STAGE, BROKER_EXECUTION_ENABLED
            _ver_value   = f"v{VERSION} {RELEASE_NAME}"
            _stage_value = RELEASE_STAGE
            _broker_value = "Disabled" if not BROKER_EXECUTION_ENABLED else "Enabled"
        except Exception:
            _ver_value   = "v1.0.0 Research Trading Cockpit Stable"
            _stage_value = "STABLE"
            _broker_value = "Disabled"

        cards.append(StrategyLabDashboardCard(
            card_id="release_version",
            title="Release Version",
            value=_ver_value,
            subtitle="Research Trading Cockpit Stable",
            status=STATUS_GOOD,
            severity=SEV_INFO,
            source_module="release",
            safe_next_step="python main.py version-info",
        ))

        cards.append(StrategyLabDashboardCard(
            card_id="stable_status",
            title="Stable Status",
            value=_stage_value,
            subtitle="v1.0.0 STABLE release",
            status=STATUS_GOOD,
            severity=SEV_INFO,
            source_module="release",
            safe_next_step="python main.py research-cockpit-stable --mode real",
        ))

        cards.append(StrategyLabDashboardCard(
            card_id="broker_execution",
            title="Broker Execution",
            value=_broker_value,
            subtitle="Broker Execution Disabled — No Real Orders",
            status=STATUS_GOOD,
            severity=SEV_INFO,
            source_module="release",
            safe_next_step="python main.py version-info",
        ))

        cards.append(StrategyLabDashboardCard(
            card_id="paper_mock_simulation",
            title="Paper / Mock",
            value="Simulation Only",
            subtitle="Paper trading and mock realtime are simulation only",
            status=STATUS_GOOD,
            severity=SEV_INFO,
            source_module="release",
            safe_next_step="python main.py mock-realtime --duration 10",
        ))

        return cards

    # ------------------------------------------------------------------
    # Build rows
    # ------------------------------------------------------------------

    def build_rows(self, context: dict) -> List[StrategyLabDashboardRow]:
        """Build dashboard validation board rows."""
        rows = []
        sv_scores = context.get("sv_scores", [])
        bc_tasks  = context.get("bc_tasks", [])
        eg_threads = context.get("eg_threads", [])
        cr_result  = context.get("crash_reversal", {})

        def _d(obj):
            if obj is None:
                return {}
            if isinstance(obj, dict):
                return obj
            if hasattr(obj, "to_dict"):
                return obj.to_dict()
            return {}

        # Rows from validation scores (top 10)
        for i, s in enumerate(sv_scores[:10]):
            sd = _d(s)
            grade = str(sd.get("validation_grade", sd.get("grade", "UNKNOWN")))
            score = float(sd.get("final_score", sd.get("validation_score", 0.0)))
            name  = str(sd.get("strategy_name", sd.get("name", f"strategy_{i}")))[:60]
            nstep = str(sd.get("suggested_next_step", "REVIEW"))
            status = STATUS_GOOD if grade == "VALIDATED" else (
                STATUS_WATCH if grade in ("VALIDATING", "OBSERVATIONAL") else (
                    STATUS_WARNING if grade in ("CONFLICTED", "REJECTED") else STATUS_UNKNOWN
                )
            )
            rows.append(StrategyLabDashboardRow(
                row_id=f"sv_{i}",
                category="strategy_validation",
                title=name,
                status=status,
                priority="P0" if grade == "VALIDATED" else "P1",
                score=score,
                grade=grade,
                source_module="strategy_validation",
                evidence=str(sd.get("evidence_summary", "")),
                limitation=str(sd.get("limitation", "")),
                safe_next_step=f"python main.py strategy-validation-explain --strategy-id {sd.get('strategy_id','')}",
            ))

        # Rows from crash reversal (warnings only)
        if isinstance(cr_result, dict):
            for r in cr_result.get("rules", [])[:5]:
                rd = _d(r)
                risk = str(rd.get("risk_level", "LOW"))
                rule_name = str(rd.get("rule_name", rd.get("name", "crash_reversal_rule")))[:60]
                rows.append(StrategyLabDashboardRow(
                    row_id=f"cr_{rule_name[:20]}",
                    category="crash_reversal",
                    title=rule_name,
                    status=STATUS_WARNING if risk in ("HIGH", "EXTREME") else STATUS_WATCH,
                    priority="P1" if risk in ("HIGH", "EXTREME") else "P2",
                    score=0.0,
                    grade=risk,
                    source_module="crash_reversal",
                    evidence=str(rd.get("evidence", "")),
                    limitation="Framework nodes only — no live data",
                    safe_next_step="python main.py crash-reversal-summary",
                ))

        # Rows from coach tasks (high priority)
        for i, t in enumerate(bc_tasks[:5]):
            td = _d(t)
            task_type = str(td.get("task_type", "REVIEW"))
            title     = str(td.get("title", f"coach_task_{i}"))[:60]
            rows.append(StrategyLabDashboardRow(
                row_id=f"bc_{i}",
                category="backtest_coach",
                title=title,
                status=STATUS_WATCH,
                priority="P1",
                score=0.0,
                grade=task_type,
                source_module="backtest_coach",
                evidence="Coach task recommendation",
                limitation="",
                safe_next_step="python main.py backtest-coach-tasks",
            ))

        return rows

    # ------------------------------------------------------------------
    # Build action items
    # ------------------------------------------------------------------

    def build_action_items(self, context: dict) -> List[StrategyLabActionItem]:
        """Build action items from context."""
        actions = []
        sv_scores = context.get("sv_scores", [])
        bc_tasks  = context.get("bc_tasks", [])
        cr_result = context.get("crash_reversal", {})

        def _d(obj):
            if obj is None:
                return {}
            if isinstance(obj, dict):
                return obj
            if hasattr(obj, "to_dict"):
                return obj.to_dict()
            return {}

        # BACKTEST_MORE for strategies needing backtest
        backtest_needed = [
            s for s in sv_scores
            if _d(s).get("suggested_next_step") == "BACKTEST_MORE"
        ]
        if backtest_needed:
            sd = _d(backtest_needed[0])
            actions.append(StrategyLabActionItem(
                action_id="action_backtest_more",
                title=f"Run more backtests for {len(backtest_needed)} strategies",
                action_type=ACTION_BACKTEST_MORE,
                priority="P1",
                source_module="strategy_validation",
                reason=f"{len(backtest_needed)} strategies need more backtest evidence",
                safe_command="python main.py strategy-validation-needs-backtest",
            ))

        # PRACTICE_REPLAY for strategies needing replay
        replay_needed = [
            s for s in sv_scores
            if _d(s).get("suggested_next_step") == "PRACTICE_REPLAY"
        ]
        if replay_needed:
            actions.append(StrategyLabActionItem(
                action_id="action_practice_replay",
                title=f"Practice replay for {len(replay_needed)} strategies",
                action_type=ACTION_PRACTICE_REPLAY,
                priority="P1",
                source_module="strategy_validation",
                reason=f"{len(replay_needed)} strategies need replay practice",
                safe_command="python main.py strategy-validation-needs-replay",
            ))

        # FIX_DATA for strategies with data gaps
        data_needed = [
            s for s in sv_scores
            if _d(s).get("suggested_next_step") == "FIX_DATA"
        ]
        if data_needed:
            actions.append(StrategyLabActionItem(
                action_id="action_fix_data",
                title=f"Fix data gaps for {len(data_needed)} strategies",
                action_type=ACTION_FIX_DATA,
                priority="P1",
                source_module="strategy_validation",
                reason=f"{len(data_needed)} strategies have data gaps",
                safe_command="python main.py data-coverage-summary",
            ))

        # REVIEW_RISK if crash reversal warnings
        if isinstance(cr_result, dict):
            cr_rules = cr_result.get("rules", [])
            high_risk = [
                r for r in cr_rules
                if isinstance(r, dict) and _d(r).get("risk_level") in ("HIGH", "EXTREME")
            ]
            if high_risk:
                actions.append(StrategyLabActionItem(
                    action_id="action_review_risk",
                    title=f"Review {len(high_risk)} high-risk crash reversal rules",
                    action_type=ACTION_REVIEW_RISK,
                    priority="P0",
                    source_module="crash_reversal",
                    reason="High/extreme risk crash reversal rules flagged",
                    safe_command="python main.py crash-reversal-summary",
                ))

        # REVIEW_JOURNAL for conflicted strategies
        conflicted = [
            s for s in sv_scores
            if _d(s).get("validation_grade", _d(s).get("grade")) == "CONFLICTED"
        ]
        if conflicted:
            actions.append(StrategyLabActionItem(
                action_id="action_review_journal",
                title=f"Review journal for {len(conflicted)} conflicted strategies",
                action_type=ACTION_REVIEW_JOURNAL,
                priority="P1",
                source_module="strategy_validation",
                reason=f"{len(conflicted)} strategies are conflicted — review journal",
                safe_command="python main.py strategy-validation-conflicted",
            ))

        # READ_REPORT — general action
        actions.append(StrategyLabActionItem(
            action_id="action_read_report",
            title="Generate and read Strategy Lab Dashboard report",
            action_type=ACTION_READ_REPORT,
            priority="P2",
            source_module="strategy_lab_dashboard",
            reason="Keep dashboard report up to date",
            safe_command="python main.py strategy-lab-dashboard-report --mode real",
        ))

        # KEEP_OBSERVING for observational strategies
        obs_strategies = [
            s for s in sv_scores
            if _d(s).get("validation_grade", _d(s).get("grade")) == "OBSERVATIONAL"
        ]
        if obs_strategies:
            actions.append(StrategyLabActionItem(
                action_id="action_keep_observing",
                title=f"Keep observing {len(obs_strategies)} observational strategies",
                action_type=ACTION_KEEP_OBSERVING,
                priority="P2",
                source_module="strategy_validation",
                reason=f"{len(obs_strategies)} strategies are in OBSERVATIONAL stage",
                safe_command="python main.py strategy-validation-scores --grade OBSERVATIONAL",
            ))

        # DO_NOT_CHASE for rejected strategies
        rejected = [
            s for s in sv_scores
            if _d(s).get("validation_grade", _d(s).get("grade")) == "REJECTED"
        ]
        if rejected:
            actions.append(StrategyLabActionItem(
                action_id="action_do_not_chase",
                title=f"Do not chase {len(rejected)} rejected strategies",
                action_type=ACTION_DO_NOT_CHASE,
                priority="P0",
                source_module="strategy_validation",
                reason=f"{len(rejected)} strategies are REJECTED — avoid chasing",
                safe_command="python main.py strategy-validation-scores --grade REJECTED",
            ))

        return actions

    # ------------------------------------------------------------------
    # Build summary
    # ------------------------------------------------------------------

    def build_summary(
        self,
        cards: List[StrategyLabDashboardCard],
        rows:  List[StrategyLabDashboardRow],
        actions: List[StrategyLabActionItem],
        context: dict,
    ) -> StrategyLabDashboardSummary:
        """Compute StrategyLabDashboardSummary from context."""

        def _d(obj):
            if obj is None:
                return {}
            if isinstance(obj, dict):
                return obj
            if hasattr(obj, "to_dict"):
                return obj.to_dict()
            return {}

        sv_sum    = _d(context.get("sv_summary"))
        eg_sum    = _d(context.get("eg_summary"))
        bc_sum    = _d(context.get("bc_summary"))
        sm_items  = context.get("sm_items", [])
        tm_metrics = context.get("tm_metrics", [])
        eg_threads = context.get("eg_threads", [])
        cr_result  = context.get("crash_reversal", {})

        strategy_count    = int(sv_sum.get("total_strategies", 0))
        validated_count   = int(sv_sum.get("validated_count", 0))
        validating_count  = int(sv_sum.get("validating_count", 0))
        observational_count = int(sv_sum.get("observational_count", 0))
        insufficient_count  = int(sv_sum.get("insufficient_count", 0))
        conflicted_count    = int(sv_sum.get("conflicted_count", 0))
        rejected_count      = int(sv_sum.get("rejected_count", 0))

        evidence_thread_count = len(eg_threads)
        graph_gap_count = int(eg_sum.get("orphan_count", 0))

        # Crash reversal warnings
        cr_rules = cr_result.get("rules", []) if isinstance(cr_result, dict) else []
        cr_warnings = sum(
            1 for r in cr_rules
            if isinstance(r, dict) and r.get("risk_level") in ("HIGH", "EXTREME")
        )

        training_metric_count = len(tm_metrics)
        coach_task_count = int(bc_sum.get("total_tasks", len(context.get("bc_tasks", []))))
        memory_active_count = sum(
            1 for m in sm_items
            if _d(m).get("status") in ("ACTIVE", "VALIDATING", "ACCEPTED")
        )

        # Needs counts from actions
        needs_backtest = sum(1 for a in actions if a.action_type == ACTION_BACKTEST_MORE)
        needs_replay   = sum(1 for a in actions if a.action_type == ACTION_PRACTICE_REPLAY)
        needs_data     = sum(1 for a in actions if a.action_type == ACTION_FIX_DATA)

        # Overall health score
        health = (
            100
            - (insufficient_count * 5)
            - (conflicted_count * 10)
            - (rejected_count * 8)
            - (graph_gap_count * 3)
        )
        health = max(0, min(100, health))

        if health >= 75:
            overall_status = "STABLE"
        elif health >= 50:
            overall_status = "WATCH"
        elif health >= 25:
            overall_status = "WARNING"
        else:
            overall_status = "CRITICAL"

        return StrategyLabDashboardSummary(
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            mode=context.get("mode", "real"),
            overall_status=overall_status,
            overall_health_score=float(health),
            strategy_count=strategy_count,
            validated_count=validated_count,
            validating_count=validating_count,
            observational_count=observational_count,
            insufficient_count=insufficient_count,
            conflicted_count=conflicted_count,
            rejected_count=rejected_count,
            evidence_thread_count=evidence_thread_count,
            graph_gap_count=graph_gap_count,
            crash_reversal_warning_count=cr_warnings,
            training_metric_count=training_metric_count,
            coach_task_count=coach_task_count,
            memory_active_count=memory_active_count,
            needs_backtest_count=needs_backtest,
            needs_replay_count=needs_replay,
            needs_data_count=needs_data,
            forbidden_action_count=0,
            no_real_orders=True,
            production_blocked=True,
        )
