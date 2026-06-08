"""
intelligence_stable/intelligence_capability_matrix.py — IntelligenceCapabilityMatrix v0.8.0

All 29 Research Intelligence Stable capabilities.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List

from intelligence_stable.intelligence_stable_schema import (
    IntelligenceStableCapability,
    CAT_RESEARCH_INTELLIGENCE, CAT_STRATEGY_MEMORY, CAT_BACKTEST_COACH,
    CAT_REPLAY_TRAINING, CAT_DATA_COVERAGE, CAT_REPORT_PACK,
    CAT_REGRESSION, CAT_STABLE_RELEASE, CAT_SAFETY,
    STABLE_STATUS_STABLE, STABLE_STATUS_USABLE,
)

logger = logging.getLogger(__name__)


class IntelligenceCapabilityMatrix:
    """Builds and summarizes the v0.8.0 intelligence stable capability matrix.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def build(self) -> List[IntelligenceStableCapability]:
        """Return hardcoded list of all Research Intelligence Stable capabilities."""
        return [
            # ------------------------------------------------------------------
            # Research Intelligence (8 capabilities)
            # ------------------------------------------------------------------
            IntelligenceStableCapability(
                capability_id="ri_engine",
                name="Research Intelligence Engine",
                category=CAT_RESEARCH_INTELLIGENCE,
                source_module="research_intelligence.research_intelligence_engine",
                version_added="v0.7.0",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["research-intelligence"],
                gui_tabs=["research_intelligence"],
                reports=["research_intelligence_report"],
                regression_suites=["research_os"],
                safety_checks=["read_only=True", "no_real_orders=True"],
                known_limitations=["Signal extraction depends on CSV outputs from other modules"],
            ),
            IntelligenceStableCapability(
                capability_id="ri_signal_aggregator",
                name="Signal Aggregator",
                category=CAT_RESEARCH_INTELLIGENCE,
                source_module="research_intelligence.signal_aggregator",
                version_added="v0.7.0",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=[],
                gui_tabs=["research_intelligence"],
                safety_checks=["no BUY/SELL/ORDER in signals"],
                known_limitations=["Aggregates from CSV only; no live feed"],
            ),
            IntelligenceStableCapability(
                capability_id="ri_recommendation_engine",
                name="Recommendation Engine",
                category=CAT_RESEARCH_INTELLIGENCE,
                source_module="research_intelligence.recommendation_engine",
                version_added="v0.7.0",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["research-intelligence-recommendations"],
                safety_checks=["no BUY/SELL/ORDER"],
                known_limitations=["Recommendations are research tasks only; no trading signals"],
            ),
            IntelligenceStableCapability(
                capability_id="ri_priority_planner",
                name="Priority Planner",
                category=CAT_RESEARCH_INTELLIGENCE,
                source_module="research_intelligence.priority_planner",
                version_added="v0.7.0",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["research-intelligence-priority"],
                safety_checks=["no BUY/SELL/ORDER"],
            ),
            IntelligenceStableCapability(
                capability_id="ri_daily_plan",
                name="Daily Research Plan",
                category=CAT_RESEARCH_INTELLIGENCE,
                source_module="research_intelligence.research_intelligence_engine",
                version_added="v0.7.0",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["research-intelligence-daily-plan"],
                safety_checks=["no BUY/SELL/ORDER"],
            ),
            IntelligenceStableCapability(
                capability_id="ri_weekly_plan",
                name="Weekly Research Plan",
                category=CAT_RESEARCH_INTELLIGENCE,
                source_module="research_intelligence.research_intelligence_engine",
                version_added="v0.7.0",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["research-intelligence-weekly-plan"],
                safety_checks=["no BUY/SELL/ORDER"],
            ),
            IntelligenceStableCapability(
                capability_id="ri_report",
                name="Research Intelligence Report",
                category=CAT_RESEARCH_INTELLIGENCE,
                source_module="reports.research_intelligence_report",
                version_added="v0.7.0",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["research-intelligence-report"],
                reports=["research_intelligence"],
                safety_checks=["no BUY/SELL/ORDER in report"],
            ),
            IntelligenceStableCapability(
                capability_id="ri_safe_command_guard",
                name="Safe Command Guard",
                category=CAT_RESEARCH_INTELLIGENCE,
                source_module="research_intelligence.research_intelligence_engine",
                version_added="v0.7.1",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                safety_checks=["no BUY/SELL/ORDER", "classify_command_safety"],
            ),

            # ------------------------------------------------------------------
            # Strategy Memory (8 capabilities — v0.8.1 UX added)
            # ------------------------------------------------------------------
            IntelligenceStableCapability(
                capability_id="sm_engine",
                name="Strategy Memory Engine",
                category=CAT_STRATEGY_MEMORY,
                source_module="strategy_memory.strategy_memory_engine",
                version_added="v0.7.2",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["strategy-memory"],
                gui_tabs=["strategy_memory"],
                reports=["strategy_memory"],
                regression_suites=["research_os"],
                safety_checks=["no_real_orders=True", "production_blocked=True"],
                known_limitations=["Extraction is pattern-based; no NLP/LLM extraction"],
            ),
            IntelligenceStableCapability(
                capability_id="sm_extractor",
                name="Memory Extractor",
                category=CAT_STRATEGY_MEMORY,
                source_module="strategy_memory.memory_extractor",
                version_added="v0.7.2",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                safety_checks=["no BUY/SELL/ORDER in extracted memories"],
                known_limitations=["CSV/JSON scan only; no cross-session merge"],
            ),
            IntelligenceStableCapability(
                capability_id="sm_store",
                name="Memory Store",
                category=CAT_STRATEGY_MEMORY,
                source_module="strategy_memory.memory_store",
                version_added="v0.7.2",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["strategy-memory-list"],
                safety_checks=["read_only=True"],
            ),
            IntelligenceStableCapability(
                capability_id="sm_linker",
                name="Memory Linker",
                category=CAT_STRATEGY_MEMORY,
                source_module="strategy_memory.memory_linker",
                version_added="v0.7.2",
                stable_status=STABLE_STATUS_USABLE,
                maturity="USABLE",
                known_limitations=["Link detection is keyword-heuristic only"],
            ),
            IntelligenceStableCapability(
                capability_id="sm_query",
                name="Memory Query",
                category=CAT_STRATEGY_MEMORY,
                source_module="strategy_memory.memory_store",
                version_added="v0.7.2",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["strategy-memory-search"],
            ),
            IntelligenceStableCapability(
                capability_id="sm_report",
                name="Strategy Memory Report",
                category=CAT_STRATEGY_MEMORY,
                source_module="reports.strategy_memory_report",
                version_added="v0.7.2",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["strategy-memory-report"],
                reports=["strategy_memory"],
            ),
            IntelligenceStableCapability(
                capability_id="sm_gui",
                name="Strategy Memory GUI",
                category=CAT_STRATEGY_MEMORY,
                source_module="gui.strategy_memory_panel",
                version_added="v0.7.2",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                gui_tabs=["strategy_memory"],
                safety_checks=["no BUY/SELL/ORDER displayed"],
            ),
            # v0.8.1 Strategy Memory UX polish
            IntelligenceStableCapability(
                capability_id="sm_ux_v081",
                name="Strategy Memory UX v0.8.1",
                category=CAT_STRATEGY_MEMORY,
                source_module="gui.strategy_memory_panel",
                version_added="v0.8.1",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=[
                    "strategy-memory-validation-queue",
                    "strategy-memory-active-threads",
                    "strategy-memory-repeated-patterns",
                    "strategy-memory-list --active-only",
                    "strategy-memory-search --needs-action",
                ],
                gui_tabs=["strategy_memory"],
                safety_checks=[
                    "ACCEPTED = research only, not trading enabled",
                    "no BUY/SELL/ORDER in safe commands",
                    "accepted_is_research_only=True enforced in __post_init__",
                ],
                known_limitations=[
                    "ACCEPTED status does not enable any trading",
                    "All commands are research-only (SAFE_READ_ONLY/SAFE_REPORT/etc.)",
                ],
            ),

            # ------------------------------------------------------------------
            # Backtest Coach (6 capabilities)
            # ------------------------------------------------------------------
            IntelligenceStableCapability(
                capability_id="bc_engine",
                name="Backtest Coach Engine",
                category=CAT_BACKTEST_COACH,
                source_module="backtest_coach.backtest_coach_engine",
                version_added="v0.7.3",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["backtest-coach"],
                gui_tabs=["backtest_coach"],
                reports=["backtest_coach"],
                regression_suites=["research_os"],
                safety_checks=["no_real_orders=True", "production_blocked=True", "no BUY/SELL/ORDER tasks"],
                known_limitations=["Task extraction depends on CSV outputs from other modules"],
            ),
            IntelligenceStableCapability(
                capability_id="bc_signal_extractor",
                name="Backtest Signal Extractor",
                category=CAT_BACKTEST_COACH,
                source_module="backtest_coach.backtest_signal_extractor",
                version_added="v0.7.3",
                stable_status=STABLE_STATUS_USABLE,
                maturity="USABLE",
                safety_checks=["no BUY/SELL/ORDER in signals"],
                known_limitations=["Pattern-based extraction; no ML inference"],
            ),
            IntelligenceStableCapability(
                capability_id="bc_task_builder",
                name="Coach Task Builder",
                category=CAT_BACKTEST_COACH,
                source_module="backtest_coach.coach_task_builder",
                version_added="v0.7.3",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["backtest-coach-tasks"],
                safety_checks=["tasks are PRACTICE_REPLAY/REVIEW/FIX/BACKTEST/READ/UPDATE/WAIT only"],
            ),
            IntelligenceStableCapability(
                capability_id="bc_store",
                name="Coach Training Task Store",
                category=CAT_BACKTEST_COACH,
                source_module="backtest_coach.backtest_coach_store",
                version_added="v0.7.3",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                safety_checks=["read_only=True"],
            ),
            IntelligenceStableCapability(
                capability_id="bc_report",
                name="Backtest Coach Report",
                category=CAT_BACKTEST_COACH,
                source_module="reports.backtest_coach_report",
                version_added="v0.7.3",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["backtest-coach-report"],
                reports=["backtest_coach"],
            ),
            IntelligenceStableCapability(
                capability_id="bc_gui",
                name="Backtest Coach GUI",
                category=CAT_BACKTEST_COACH,
                source_module="gui.backtest_coach_panel",
                version_added="v0.7.3",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                gui_tabs=["backtest_coach"],
                safety_checks=["no BUY/SELL/ORDER displayed"],
            ),

            # ------------------------------------------------------------------
            # Supporting (8 capabilities)
            # ------------------------------------------------------------------
            IntelligenceStableCapability(
                capability_id="replay_training",
                name="Replay Training UI",
                category=CAT_REPLAY_TRAINING,
                source_module="gui.replay_training_panel",
                version_added="v0.5.6",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                gui_tabs=["replay_training"],
                safety_checks=["hidden_future_data=True"],
            ),
            IntelligenceStableCapability(
                capability_id="data_coverage",
                name="Data Coverage Matrix",
                category=CAT_DATA_COVERAGE,
                source_module="data_coverage.data_coverage_registry",
                version_added="v0.6.2",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["data-coverage"],
                gui_tabs=["data_coverage"],
            ),
            IntelligenceStableCapability(
                capability_id="report_pack",
                name="Report Pack",
                category=CAT_REPORT_PACK,
                source_module="report_pack.report_pack_builder",
                version_added="v0.5.4",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["report-pack"],
            ),
            IntelligenceStableCapability(
                capability_id="regression_suite",
                name="Regression Suite",
                category=CAT_REGRESSION,
                source_module="regression.suite_registry",
                version_added="v0.5.3",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["regression-run"],
            ),
            IntelligenceStableCapability(
                capability_id="stable_release_check",
                name="Stable Release Checklist",
                category=CAT_STABLE_RELEASE,
                source_module="stable_release.stable_release_checklist_v060",
                version_added="v0.6.0",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["stable-v060-check"],
            ),
            IntelligenceStableCapability(
                capability_id="no_real_orders_safety",
                name="No Real Orders Safety",
                category=CAT_SAFETY,
                source_module="intelligence_stable.__init__",
                version_added="v0.8.0",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                safety_checks=["read_only=True", "no_real_orders=True", "production_blocked=True"],
            ),
            IntelligenceStableCapability(
                capability_id="production_blocked",
                name="Production Trading BLOCKED",
                category=CAT_SAFETY,
                source_module="intelligence_stable.__init__",
                version_added="v0.8.0",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                safety_checks=["PRODUCTION_BLOCKED=True", "REAL_ORDER_READY=False"],
            ),
            IntelligenceStableCapability(
                capability_id="intelligence_stable",
                name="Intelligence Stable v0.8.0",
                category=CAT_STABLE_RELEASE,
                source_module="intelligence_stable.intelligence_stable_engine",
                version_added="v0.8.0",
                stable_status=STABLE_STATUS_STABLE,
                maturity="STABLE",
                cli_commands=["intelligence-stable"],
                safety_checks=["no_real_orders=True", "production_blocked=True"],
            ),
            # v0.8.2 Backtest Training Metrics
            IntelligenceStableCapability(
                capability_id="training_metrics",
                name="Backtest Training Metrics",
                category=CAT_BACKTEST_COACH,
                source_module="training_metrics.training_metrics_engine",
                version_added="v0.8.2",
                stable_status=STABLE_STATUS_USABLE,
                maturity="USABLE",
                cli_commands=[
                    "training-metrics",
                    "training-metrics-summary",
                    "training-metrics-detail",
                    "training-metrics-trend",
                    "training-metrics-report",
                ],
                gui_tabs=["training_metrics"],
                reports=["training_metrics"],
                regression_suites=["research_os"],
                safety_checks=[
                    "no_real_orders=True",
                    "production_blocked=True",
                    "_guard() rejects BUY/SELL/ORDER",
                    "INSUFFICIENT_DATA shown gracefully",
                ],
                known_limitations=[
                    "Metrics collected from CSV outputs only — no live data feed",
                    "INSUFFICIENT_DATA shown when source module not yet run",
                    "Trend requires at least 2 historical data points",
                ],
            ),
            # v0.8.3 Research Intelligence Evidence Graph
            IntelligenceStableCapability(
                capability_id="evidence_graph",
                name="Research Intelligence Evidence Graph",
                category="research_os",
                source_module="evidence_graph.evidence_graph_engine",
                version_added="v0.8.3",
                stable_status=STABLE_STATUS_USABLE,
                maturity="USABLE",
                cli_commands=[
                    "evidence-graph",
                    "evidence-graph-summary",
                    "evidence-graph-nodes",
                    "evidence-graph-edges",
                    "evidence-graph-threads",
                    "evidence-graph-orphans",
                    "evidence-graph-requires-backtest",
                    "evidence-graph-requires-data",
                    "evidence-graph-report",
                ],
                gui_tabs=["evidence_graph"],
                reports=["evidence_graph"],
                regression_suites=["release_gate"],
                safety_checks=[
                    "no_real_orders=True",
                    "production_blocked=True",
                    "_guard() rejects BUY/SELL/ORDER in action fields",
                    "Does NOT modify memory/coach/rule/strategy status",
                    "Read-only evidence collection",
                ],
                known_limitations=[
                    "Nodes collected from CSV outputs only — requires source modules to have been run",
                    "Conservative edge building — may miss some links",
                    "Max 20 edges per node to keep graph readable",
                ],
            ),
        ]

    def summarize(self, capabilities: List[IntelligenceStableCapability]) -> dict:
        """Return count by stable_status."""
        counts: dict = {}
        for cap in capabilities:
            counts[cap.stable_status] = counts.get(cap.stable_status, 0) + 1
        return counts
