"""
strategy_lab/strategy_lab_capability_matrix.py — Strategy Lab Capability Matrix v0.9.0

Defines all Strategy Lab capabilities across 5 research layers + supporting infrastructure.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

from typing import List

from strategy_lab.strategy_lab_schema import (
    StrategyLabCapability,
    CAT_RESEARCH_INTELLIGENCE, CAT_STRATEGY_MEMORY, CAT_BACKTEST_COACH,
    CAT_TRAINING_METRICS, CAT_EVIDENCE_GRAPH, CAT_REPLAY_TRAINING,
    CAT_DATA_COVERAGE, CAT_REPORT_PACK, CAT_REGRESSION, CAT_STABLE_RELEASE,
    CAT_SAFETY,
    STABLE_STATUS_STABLE, STABLE_STATUS_USABLE,
)


def _cap(cid: str, name: str, cat: str, src: str,
         version: str = "v0.9.0",
         status: str = STABLE_STATUS_STABLE,
         maturity: str = "STABLE",
         cli: list = None, gui: list = None,
         reports: list = None, reg: list = None,
         deps: list = None, safety: list = None,
         limits: list = None) -> StrategyLabCapability:
    return StrategyLabCapability(
        capability_id=cid, name=name, category=cat, source_module=src,
        version_added=version, stable_status=status, maturity=maturity,
        cli_commands=cli or [], gui_tabs=gui or [],
        reports=reports or [], regression_suites=reg or [],
        dependencies=deps or [], safety_checks=safety or [],
        known_limitations=limits or [],
        no_real_orders=True, production_blocked=True,
    )


class StrategyLabCapabilityMatrix:
    """Strategy Lab Stable capability matrix — v0.9.0.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self) -> None:
        self._capabilities: List[StrategyLabCapability] = []

    def build(self) -> List[StrategyLabCapability]:
        """Build and return full capability list."""
        self._capabilities = (
            self._research_intelligence_caps()
            + self._strategy_memory_caps()
            + self._backtest_coach_caps()
            + self._training_metrics_caps()
            + self._evidence_graph_caps()
            + self._supporting_caps()
            + self._crash_reversal_caps()  # v0.9.0.1 crash reversal
            + self._evidence_graph_ux_caps()  # v0.9.1 Evidence Graph UX
            + self._strategy_validation_caps()  # v0.9.2 strategy validation
            + self._strategy_lab_dashboard_caps()  # v0.9.3 strategy lab dashboard
        )
        return self._capabilities

    def summarize(self) -> dict:
        """Return summary statistics."""
        caps = self._capabilities or self.build()
        return {
            "total":   len(caps),
            "stable":  sum(1 for c in caps if c.stable_status == STABLE_STATUS_STABLE),
            "usable":  sum(1 for c in caps if c.stable_status == STABLE_STATUS_USABLE),
            "partial": sum(1 for c in caps if c.stable_status not in (STABLE_STATUS_STABLE, STABLE_STATUS_USABLE)),
        }

    # ------------------------------------------------------------------
    # Research Intelligence (9 capabilities)
    # ------------------------------------------------------------------

    def _research_intelligence_caps(self) -> List[StrategyLabCapability]:
        src = "research_intelligence"
        ri_cli = ["research-intelligence", "research-intelligence-summary",
                  "research-intelligence-recommendations", "research-intelligence-priority",
                  "research-intelligence-daily-plan", "research-intelligence-weekly-plan",
                  "research-intelligence-report"]
        ri_gui = ["Research Intelligence"]
        ri_rep = ["research_intelligence_report"]
        ri_reg = ["release_gate", "quick"]
        ri_dep = ["data_coverage", "rule_governance", "portfolio_journal"]
        ri_saf = ["_guard() blocks BUY/SELL/ORDER", "no_real_orders=True", "production_blocked=True"]
        ri_lim = ["Signal extraction depends on CSV outputs from other modules",
                  "No live market feed", "Recommendations are research tasks only"]
        return [
            _cap("ri_engine", "Research Intelligence Engine", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.7.0", STABLE_STATUS_STABLE, "STABLE",
                 ri_cli, ri_gui, ri_rep, ri_reg, ri_dep, ri_saf, ri_lim),
            _cap("ri_signal_aggregator", "Signal Aggregator", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.7.0", STABLE_STATUS_STABLE, "STABLE",
                 ["research-intelligence"], ri_gui, ri_rep, ri_reg, ri_dep, ri_saf,
                 ["Aggregates from 8 source modules; missing modules show empty signals"]),
            _cap("ri_recommendation_engine", "Recommendation Engine", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.7.0", STABLE_STATUS_STABLE, "STABLE",
                 ["research-intelligence-recommendations"], ri_gui, ri_rep, ri_reg, ri_dep, ri_saf,
                 ["Max 20 recommendations per run"]),
            _cap("ri_priority_planner", "Priority Planner", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.7.0", STABLE_STATUS_STABLE, "STABLE",
                 ["research-intelligence-priority"], ri_gui, ri_rep, ri_reg, ri_dep, ri_saf,
                 ["P0-P3 priority board; max 5 P0 items"]),
            _cap("ri_daily_plan", "Daily Research Plan", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.7.0", STABLE_STATUS_STABLE, "STABLE",
                 ["research-intelligence-daily-plan"], ri_gui, ri_rep, ri_reg, ri_dep, ri_saf,
                 ["Daily plan capped at 7 items"]),
            _cap("ri_weekly_plan", "Weekly Research Plan", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.7.0", STABLE_STATUS_STABLE, "STABLE",
                 ["research-intelligence-weekly-plan"], ri_gui, ri_rep, ri_reg, ri_dep, ri_saf,
                 ["Weekly plan capped at 12 items"]),
            _cap("ri_report", "Research Intelligence Report", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.7.0", STABLE_STATUS_STABLE, "STABLE",
                 ["research-intelligence-report"], ri_gui, ri_rep, ri_reg, ri_dep, ri_saf,
                 ["Report depends on CSV outputs being available"]),
            _cap("ri_gui", "Research Intelligence GUI", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.7.1", STABLE_STATUS_STABLE, "STABLE",
                 ri_cli, ri_gui, ri_rep, ri_reg, ri_dep, ri_saf,
                 ["Requires PySide6; graceful stub if unavailable"]),
            _cap("ri_safe_guard", "Safe Command Guard", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.7.0", STABLE_STATUS_STABLE, "STABLE",
                 [], [], [], [], ri_dep,
                 ["_guard() rejects BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE/REAL_TRADE"],
                 ["Safety declaration phrases exempt from guard"]),
        ]

    # ------------------------------------------------------------------
    # Strategy Memory (8 capabilities)
    # ------------------------------------------------------------------

    def _strategy_memory_caps(self) -> List[StrategyLabCapability]:
        src = "strategy_memory"
        sm_cli = ["strategy-memory", "strategy-memory-summary", "strategy-memory-list",
                  "strategy-memory-search", "strategy-memory-validation-queue",
                  "strategy-memory-active-threads", "strategy-memory-repeated-patterns",
                  "strategy-memory-report"]
        sm_gui = ["Strategy Memory"]
        sm_rep = ["strategy_memory_report"]
        sm_reg = ["release_gate", "quick"]
        sm_saf = ["accepted_is_research_only=True invariant", "ACCEPTED != trading enabled",
                  "no_real_orders=True", "production_blocked=True"]
        sm_lim = ["Pattern-based extraction only; no NLP/LLM",
                  "ACCEPTED status never enables trading"]
        return [
            _cap("sm_engine", "Strategy Memory Engine", CAT_STRATEGY_MEMORY, src,
                 "v0.7.2", STABLE_STATUS_STABLE, "STABLE",
                 sm_cli, sm_gui, sm_rep, sm_reg, ["research_intelligence"], sm_saf, sm_lim),
            _cap("sm_extractor", "Memory Extractor", CAT_STRATEGY_MEMORY, src,
                 "v0.7.2", STABLE_STATUS_STABLE, "STABLE",
                 ["strategy-memory"], sm_gui, sm_rep, sm_reg, ["research_intelligence"], sm_saf,
                 ["Extracts 10 memory types from CSV outputs"]),
            _cap("sm_store", "Memory Store", CAT_STRATEGY_MEMORY, src,
                 "v0.7.2", STABLE_STATUS_STABLE, "STABLE",
                 ["strategy-memory-summary"], sm_gui, sm_rep, sm_reg, [], sm_saf,
                 ["CSV/JSON persistence; upsert deduplication by normalized key"]),
            _cap("sm_linker", "Memory Linker", CAT_STRATEGY_MEMORY, src,
                 "v0.7.2", STABLE_STATUS_STABLE, "STABLE",
                 ["strategy-memory-active-threads"], sm_gui, sm_rep, sm_reg, ["sm_store"], sm_saf,
                 ["Keyword-heuristic linking; no semantic NLP"]),
            _cap("sm_query", "Memory Query", CAT_STRATEGY_MEMORY, src,
                 "v0.7.2", STABLE_STATUS_STABLE, "STABLE",
                 ["strategy-memory-search", "strategy-memory-list"], sm_gui, sm_rep, sm_reg,
                 ["sm_store"], sm_saf, ["Full-text keyword search"]),
            _cap("sm_ux", "Strategy Memory UX", CAT_STRATEGY_MEMORY, src,
                 "v0.8.1", STABLE_STATUS_STABLE, "STABLE",
                 ["strategy-memory-validation-queue", "strategy-memory-repeated-patterns"],
                 sm_gui, sm_rep, sm_reg, ["sm_store", "sm_linker"], sm_saf,
                 ["Status lifecycle: NEW→REVIEWING→VALIDATING→ACCEPTED/REJECTED/NEEDS_MORE_EVIDENCE"]),
            _cap("sm_report", "Strategy Memory Report", CAT_STRATEGY_MEMORY, src,
                 "v0.7.2", STABLE_STATUS_STABLE, "STABLE",
                 ["strategy-memory-report"], sm_gui, sm_rep, sm_reg, ["sm_store"], sm_saf,
                 ["8-section Markdown report"]),
            _cap("sm_gui", "Strategy Memory GUI", CAT_STRATEGY_MEMORY, src,
                 "v0.7.2", STABLE_STATUS_STABLE, "STABLE",
                 sm_cli, sm_gui, sm_rep, sm_reg, ["sm_engine"], sm_saf,
                 ["7-tab detail view; requires PySide6"]),
        ]

    # ------------------------------------------------------------------
    # Backtest Coach (7 capabilities)
    # ------------------------------------------------------------------

    def _backtest_coach_caps(self) -> List[StrategyLabCapability]:
        src = "backtest_coach"
        bc_cli = ["backtest-coach", "backtest-coach-summary", "backtest-coach-tasks",
                  "backtest-coach-daily-plan", "backtest-coach-weekly-plan", "backtest-coach-report"]
        bc_gui = ["Backtest Coach"]
        bc_rep = ["backtest_coach_report"]
        bc_reg = ["release_gate", "quick"]
        bc_saf = ["Task types: PRACTICE_REPLAY/REVIEW_RULE/REVIEW_JOURNAL/FIX_DATA/"
                  "BACKTEST_MORE/READ_REPORT/UPDATE_MEMORY/WAIT — no trading actions",
                  "no_real_orders=True", "production_blocked=True"]
        bc_lim = ["Task extraction depends on CSV outputs",
                  "Daily plan capped at 7 items; weekly plan capped at 12"]
        return [
            _cap("bc_engine", "Backtest Coach Engine", CAT_BACKTEST_COACH, src,
                 "v0.7.3", STABLE_STATUS_STABLE, "STABLE",
                 bc_cli, bc_gui, bc_rep, bc_reg, ["research_intelligence", "strategy_memory"],
                 bc_saf, bc_lim),
            _cap("bc_signal_extractor", "Backtest Signal Extractor", CAT_BACKTEST_COACH, src,
                 "v0.7.3", STABLE_STATUS_STABLE, "STABLE",
                 ["backtest-coach"], bc_gui, bc_rep, bc_reg,
                 ["research_intelligence"], bc_saf, bc_lim),
            _cap("bc_task_builder", "Coach Task Builder", CAT_BACKTEST_COACH, src,
                 "v0.7.3", STABLE_STATUS_STABLE, "STABLE",
                 ["backtest-coach-tasks"], bc_gui, bc_rep, bc_reg,
                 ["bc_signal_extractor"], bc_saf, bc_lim),
            _cap("bc_daily_plan", "Daily Training Plan", CAT_BACKTEST_COACH, src,
                 "v0.7.3", STABLE_STATUS_STABLE, "STABLE",
                 ["backtest-coach-daily-plan"], bc_gui, bc_rep, bc_reg,
                 ["bc_task_builder"], bc_saf, ["Daily plan capped at 7 items"]),
            _cap("bc_weekly_plan", "Weekly Training Plan", CAT_BACKTEST_COACH, src,
                 "v0.7.3", STABLE_STATUS_STABLE, "STABLE",
                 ["backtest-coach-weekly-plan"], bc_gui, bc_rep, bc_reg,
                 ["bc_task_builder"], bc_saf, ["Weekly plan capped at 12 items"]),
            _cap("bc_report", "Backtest Coach Report", CAT_BACKTEST_COACH, src,
                 "v0.7.3", STABLE_STATUS_STABLE, "STABLE",
                 ["backtest-coach-report"], bc_gui, bc_rep, bc_reg,
                 ["bc_engine"], bc_saf, ["8-section Markdown report"]),
            _cap("bc_gui", "Backtest Coach GUI", CAT_BACKTEST_COACH, src,
                 "v0.7.3", STABLE_STATUS_STABLE, "STABLE",
                 bc_cli, bc_gui, bc_rep, bc_reg, ["bc_engine"], bc_saf,
                 ["Requires PySide6"]),
        ]

    # ------------------------------------------------------------------
    # Training Metrics (6 capabilities)
    # ------------------------------------------------------------------

    def _training_metrics_caps(self) -> List[StrategyLabCapability]:
        src = "training_metrics"
        tm_cli = ["training-metrics", "training-metrics-summary", "training-metrics-detail",
                  "training-metrics-trend", "training-metrics-report"]
        tm_gui = ["Training Metrics"]
        tm_rep = ["training_metrics_report"]
        tm_reg = ["release_gate", "quick"]
        tm_saf = ["_guard() blocks forbidden tokens", "INSUFFICIENT_DATA shown gracefully",
                  "no_real_orders=True", "production_blocked=True"]
        tm_lim = ["Metrics from CSV only; no live data",
                  "INSUFFICIENT_DATA when source module not yet run",
                  "Trend requires at least 2 historical points"]
        return [
            _cap("tm_collector", "Training Metrics Collector", CAT_TRAINING_METRICS, src,
                 "v0.8.2", STABLE_STATUS_USABLE, "USABLE",
                 tm_cli, tm_gui, tm_rep, tm_reg,
                 ["backtest_coach", "replay_training", "strategy_memory"],
                 tm_saf, tm_lim),
            _cap("tm_tracker", "Progress Tracker", CAT_TRAINING_METRICS, src,
                 "v0.8.2", STABLE_STATUS_USABLE, "USABLE",
                 ["training-metrics-trend"], tm_gui, tm_rep, tm_reg,
                 ["tm_collector"], tm_saf,
                 ["IMPROVING/STABLE/WORSENING trend per metric"]),
            _cap("tm_engine", "Training Metrics Engine", CAT_TRAINING_METRICS, src,
                 "v0.8.2", STABLE_STATUS_USABLE, "USABLE",
                 tm_cli, tm_gui, tm_rep, tm_reg,
                 ["tm_collector", "tm_tracker"], tm_saf, tm_lim),
            _cap("tm_report", "Training Metrics Report", CAT_TRAINING_METRICS, src,
                 "v0.8.2", STABLE_STATUS_USABLE, "USABLE",
                 ["training-metrics-report"], tm_gui, tm_rep, tm_reg,
                 ["tm_engine"], tm_saf, ["Full metrics table + trend analysis"]),
            _cap("tm_gui", "Training Metrics GUI", CAT_TRAINING_METRICS, src,
                 "v0.8.2", STABLE_STATUS_USABLE, "USABLE",
                 tm_cli, tm_gui, tm_rep, tm_reg,
                 ["tm_engine"], tm_saf, ["Requires PySide6"]),
            _cap("tm_insufficient_data", "INSUFFICIENT_DATA Handling", CAT_TRAINING_METRICS, src,
                 "v0.8.2", STABLE_STATUS_STABLE, "STABLE",
                 [], [], [], [],
                 ["tm_collector"], tm_saf,
                 ["INSUFFICIENT_DATA shown when source module not yet run — never crashes"]),
        ]

    # ------------------------------------------------------------------
    # Evidence Graph (8 capabilities)
    # ------------------------------------------------------------------

    def _evidence_graph_caps(self) -> List[StrategyLabCapability]:
        src = "evidence_graph"
        eg_cli = ["evidence-graph", "evidence-graph-summary", "evidence-graph-nodes",
                  "evidence-graph-edges", "evidence-graph-threads", "evidence-graph-orphans",
                  "evidence-graph-requires-backtest", "evidence-graph-requires-data",
                  "evidence-graph-report"]
        eg_gui = ["Evidence Graph"]
        eg_rep = ["evidence_graph_report"]
        eg_reg = ["release_gate"]
        eg_saf = ["_guard() blocks forbidden tokens", "No auto-modify of any module status",
                  "suggested_next_step: REVIEW/VALIDATE/BACKTEST_MORE/PRACTICE_REPLAY/FIX_DATA/READ_REPORT/WAIT",
                  "no_real_orders=True", "production_blocked=True"]
        eg_lim = ["Edge building is heuristic-based",
                  "Conservative contradiction detection",
                  "Orphan nodes appear when source modules not yet run",
                  "Max 2000 total edges; max 20 per node"]
        return [
            _cap("eg_collector", "Evidence Collector", CAT_EVIDENCE_GRAPH, src,
                 "v0.8.3", STABLE_STATUS_USABLE, "USABLE",
                 ["evidence-graph"], eg_gui, eg_rep, eg_reg,
                 ["research_intelligence", "strategy_memory", "backtest_coach", "training_metrics"],
                 eg_saf, eg_lim),
            _cap("eg_builder", "Evidence Graph Builder", CAT_EVIDENCE_GRAPH, src,
                 "v0.8.3", STABLE_STATUS_USABLE, "USABLE",
                 ["evidence-graph"], eg_gui, eg_rep, eg_reg,
                 ["eg_collector"], eg_saf,
                 ["Heuristic edge building; symbol/strategy/rule linkers"]),
            _cap("eg_engine", "Evidence Graph Engine", CAT_EVIDENCE_GRAPH, src,
                 "v0.8.3", STABLE_STATUS_USABLE, "USABLE",
                 eg_cli, eg_gui, eg_rep, eg_reg,
                 ["eg_collector", "eg_builder"], eg_saf, eg_lim),
            _cap("eg_query", "Evidence Graph Query", CAT_EVIDENCE_GRAPH, src,
                 "v0.8.3", STABLE_STATUS_USABLE, "USABLE",
                 ["evidence-graph-nodes", "evidence-graph-edges", "evidence-graph-orphans"],
                 eg_gui, eg_rep, eg_reg, ["eg_engine"], eg_saf,
                 ["Lazy-loads from store on first call"]),
            _cap("eg_report", "Evidence Graph Report", CAT_EVIDENCE_GRAPH, src,
                 "v0.8.3", STABLE_STATUS_USABLE, "USABLE",
                 ["evidence-graph-report"], eg_gui, eg_rep, eg_reg,
                 ["eg_engine"], eg_saf, ["9-section Markdown report"]),
            _cap("eg_gui", "Evidence Graph GUI", CAT_EVIDENCE_GRAPH, src,
                 "v0.8.3", STABLE_STATUS_USABLE, "USABLE",
                 eg_cli, eg_gui, eg_rep, eg_reg,
                 ["eg_engine"], eg_saf, ["Requires PySide6"]),
            _cap("eg_threads", "Evidence Threads", CAT_EVIDENCE_GRAPH, src,
                 "v0.8.3", STABLE_STATUS_USABLE, "USABLE",
                 ["evidence-graph-threads"], eg_gui, eg_rep, eg_reg,
                 ["eg_builder"], eg_saf,
                 ["BFS max depth 3 from anchor nodes (RESEARCH_RECOMMENDATION/STRATEGY_HYPOTHESIS)"]),
            _cap("eg_gaps", "Orphan / Requires Data / Requires Backtest Tracking",
                 CAT_EVIDENCE_GRAPH, src, "v0.8.3", STABLE_STATUS_USABLE, "USABLE",
                 ["evidence-graph-orphans", "evidence-graph-requires-data",
                  "evidence-graph-requires-backtest"],
                 eg_gui, eg_rep, eg_reg, ["eg_engine"], eg_saf,
                 ["Orphan nodes appear when source modules not yet run"]),
        ]

    # ------------------------------------------------------------------
    # Supporting (9 capabilities)
    # ------------------------------------------------------------------

    # v0.9.0.1 crash reversal
    def _crash_reversal_caps(self) -> List[StrategyLabCapability]:
        src = "strategy_rules.crash_reversal_pack"
        cr_cli = ["crash-reversal", "crash-reversal-summary", "crash-reversal-report",
                  "crash-reversal-score", "crash-reversal-watchlist"]
        cr_gui = ["Crash Reversal"]
        cr_rep = ["crash_reversal_strategy_report"]
        cr_reg = ["release_gate", "quick"]
        cr_saf = ["no_real_orders=True", "production_blocked=True",
                  "No BUY/SELL/ORDER output"]
        cr_lim = ["Framework/registration nodes only — no live data feed",
                  "Crash cause classification requires historical context",
                  "Relative strength scoring requires comparative index data"]
        return [
            _cap("cr_pack", "Crash Reversal & Risk Discipline Strategy Pack",
                 CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.9.0.1", STABLE_STATUS_USABLE, "v0.9.0.1",
                 cr_cli, cr_gui, cr_rep, cr_reg, [], cr_saf,
                 cr_lim),
        ]

    # ------------------------------------------------------------------
    # Evidence Graph UX (3 capabilities) — v0.9.1
    # ------------------------------------------------------------------

    def _evidence_graph_ux_caps(self) -> List[StrategyLabCapability]:
        src = "evidence_graph"
        eg_ux_cli = [
            "evidence-graph-ux", "evidence-graph-thread-quality",
            "evidence-graph-gaps", "evidence-graph-crash-reversal",
            "evidence-graph-explain-node", "evidence-graph-explain-thread",
            "evidence-graph-search",
        ]
        eg_ux_saf = ["no_real_orders=True", "production_blocked=True",
                     "No BUY/SELL/ORDER output", "read_only=True"]
        return [
            _cap("eg_ux", "Evidence Graph UX", CAT_EVIDENCE_GRAPH, src,
                 "v0.9.1", STABLE_STATUS_USABLE, "v0.9.1",
                 eg_ux_cli, ["Evidence Graph"], ["evidence_graph_report"],
                 ["release_gate", "quick"], ["evidence_graph"], eg_ux_saf,
                 ["Evidence thread quality scoring, graph gap analysis, crash reversal evidence chains, node/thread explanations"]),
            _cap("eg_crash_chain", "Crash Reversal Evidence Chain", CAT_EVIDENCE_GRAPH, src,
                 "v0.9.1", STABLE_STATUS_USABLE, "v0.9.1",
                 ["evidence-graph-crash-reversal"], ["Evidence Graph"],
                 ["evidence_graph_report"], ["release_gate"], ["evidence_graph", "crash_reversal"],
                 eg_ux_saf,
                 ["Evidence chain view: Crash Cause → Stabilization → Relative Strength → EPS Dip Filter → MA Discipline → Risk Guard"]),
            _cap("eg_thread_quality", "Thread Quality Board & Graph Gap View", CAT_EVIDENCE_GRAPH, src,
                 "v0.9.1", STABLE_STATUS_USABLE, "v0.9.1",
                 ["evidence-graph-thread-quality", "evidence-graph-gaps"],
                 ["Evidence Graph"], ["evidence_graph_report"], ["release_gate", "quick"],
                 ["evidence_graph"], eg_ux_saf,
                 ["Thread quality scoring (STRONG/PARTIAL/NEEDS_DATA/NEEDS_BACKTEST/CONFLICTED/ORPHANED), gap detection (orphans, missing data, contradictions)"]),
        ]

    # v0.9.2 strategy validation
    def _strategy_validation_caps(self) -> List[StrategyLabCapability]:
        return [
            StrategyLabCapability(
                capability_id="sv_score",
                name="Strategy Validation Score",
                category=CAT_RESEARCH_INTELLIGENCE,
                source_module="strategy_validation",
                version_added="v0.9.2",
                stable_status=STABLE_STATUS_USABLE,
                maturity="v0.9.2",
                cli_commands=[],
                gui_tabs=[],
                reports=[],
                regression_suites=[],
                dependencies=[],
                safety_checks=["no_real_orders=True", "production_blocked=True",
                                "VALIDATED does not enable trading"],
                known_limitations=[
                    "Score strategy candidates as INSUFFICIENT/OBSERVATIONAL/VALIDATING/"
                    "VALIDATED/CONFLICTED/REJECTED across evidence graph, backtest, replay, "
                    "journal, training metrics, and risk guards. VALIDATED does not enable trading.",
                ],
                no_real_orders=True,
                production_blocked=True,
            )
        ]

    # v0.9.3 strategy lab dashboard
    def _strategy_lab_dashboard_caps(self) -> List[StrategyLabCapability]:
        src = "strategy_lab.strategy_lab_dashboard"
        sld_cli = [
            "strategy-lab-dashboard", "strategy-lab-dashboard-summary",
            "strategy-lab-dashboard-cards", "strategy-lab-dashboard-actions",
            "strategy-lab-dashboard-priorities", "strategy-lab-dashboard-needs-backtest",
            "strategy-lab-dashboard-needs-replay", "strategy-lab-dashboard-needs-data",
            "strategy-lab-dashboard-report",
        ]
        sld_gui  = ["StrategyLabDashboardPanel"]
        sld_rep  = ["strategy_lab_dashboard_report"]
        sld_reg  = ["release_gate", "quick"]
        sld_saf  = ["no_real_orders=True", "production_blocked=True",
                    "_guard() blocks BUY/SELL/ORDER", "read_only=True"]
        sld_lim  = ["Dashboard reads from existing module stores — run sub-modules first",
                    "Graceful fallback when sub-module stores are empty"]
        return [
            _cap("sld_engine", "Strategy Lab Dashboard Engine", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.9.3", STABLE_STATUS_USABLE, "v0.9.3",
                 sld_cli, sld_gui, sld_rep, sld_reg, [], sld_saf, sld_lim),
            _cap("sld_cards", "Dashboard Cards", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.9.3", STABLE_STATUS_USABLE, "v0.9.3",
                 ["strategy-lab-dashboard-cards"], sld_gui, sld_rep, sld_reg,
                 ["sld_engine"], sld_saf,
                 ["12 summary cards covering all Strategy Lab modules"]),
            _cap("sld_validation_board", "Validation Board", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.9.3", STABLE_STATUS_USABLE, "v0.9.3",
                 ["strategy-lab-dashboard"], sld_gui, sld_rep, sld_reg,
                 ["sld_engine", "strategy_validation"], sld_saf,
                 ["Shows top 10 strategy validation rows"]),
            _cap("sld_evidence_board", "Evidence Board", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.9.3", STABLE_STATUS_USABLE, "v0.9.3",
                 ["strategy-lab-dashboard"], sld_gui, sld_rep, sld_reg,
                 ["sld_engine", "evidence_graph"], sld_saf,
                 ["Shows evidence graph rows and crash reversal rows"]),
            _cap("sld_action_board", "Action Board", CAT_RESEARCH_INTELLIGENCE, src,
                 "v0.9.3", STABLE_STATUS_USABLE, "v0.9.3",
                 ["strategy-lab-dashboard-actions", "strategy-lab-dashboard-priorities"],
                 sld_gui, sld_rep, sld_reg, ["sld_engine"], sld_saf,
                 ["Research-only action types; no BUY/SELL/ORDER"]),
        ]

    def _supporting_caps(self) -> List[StrategyLabCapability]:
        return [
            _cap("sup_replay", "Replay Training UI", CAT_REPLAY_TRAINING, "replay_training",
                 "v0.5.6", STABLE_STATUS_STABLE, "STABLE",
                 ["intraday-replay", "replay-training-summary", "replay-session-list"],
                 ["TW Replay Training"], ["intraday_replay_report"], ["release_gate", "replay"],
                 ["intraday_pipeline"], ["No real orders", "Training annotations only"],
                 ["Requires intraday CSV data; INSUFFICIENT_INTRADAY_DATA graceful"]),
            _cap("sup_data_coverage", "Data Coverage Matrix", CAT_DATA_COVERAGE, "data_coverage",
                 "v0.6.2", STABLE_STATUS_STABLE, "STABLE",
                 ["data-coverage", "data-coverage-summary", "data-coverage-items",
                  "data-coverage-report", "data-coverage-gaps"],
                 ["Data Coverage"], ["data_coverage_report"], ["release_gate", "data"],
                 ["data_providers"], ["read_only=True", "no_real_orders=True"],
                 ["Provider token env limits may affect some items"]),
            _cap("sup_report_pack", "Report Pack", CAT_REPORT_PACK, "report_pack",
                 "v0.5.4", STABLE_STATUS_STABLE, "STABLE",
                 ["report-pack", "report-pack-summary", "report-pack-items",
                  "report-pack-health", "report-pack-links", "report-pack-report"],
                 ["Report Pack"], ["report_pack_consolidation_report"], ["release_gate", "report"],
                 ["auto_report_center"], ["No forbidden actions"],
                 ["Optional reports may be missing if source module not yet run"]),
            _cap("sup_regression", "Regression Suite", CAT_REGRESSION, "regression",
                 "v0.5.3", STABLE_STATUS_STABLE, "STABLE",
                 ["regression-run", "regression-summary", "regression-list",
                  "regression-suite-list"],
                 ["Regression Suite"], ["regression_suite_consolidation_report"],
                 ["release_gate", "quick", "report", "replay", "data"],
                 ["suite_registry"], ["No forbidden actions"],
                 ["Pre-existing BLOCKED test in release_gate is not new"]),
            _cap("sup_intelligence_stable", "Intelligence Stable", CAT_STABLE_RELEASE,
                 "intelligence_stable", "v0.8.0", STABLE_STATUS_STABLE, "STABLE",
                 ["intelligence-stable", "intelligence-stable-summary",
                  "intelligence-stable-capabilities", "intelligence-stable-checks",
                  "intelligence-stable-manifest", "intelligence-stable-report"],
                 ["Intelligence Stable"], ["intelligence_stable_report"],
                 ["release_gate"], ["intelligence_stable", "strategy_lab"],
                 ["Safety audit across all capabilities"],
                 ["29 capabilities tracked across v0.7.x-v0.8.x"]),
            _cap("sup_stable_checklist", "Stable Release Checklist", CAT_STABLE_RELEASE,
                 "stable_release", "v0.6.0", STABLE_STATUS_STABLE, "STABLE",
                 ["stable-v060-check", "stable-v060-summary", "stable-v060-capabilities"],
                 ["Release Status"], ["stable_release_v060_report"],
                 ["release_gate"], ["stable_release"],
                 ["No forbidden actions"],
                 ["32 checks across 8 categories"]),
            _cap("sup_no_real_orders", "No Real Orders Safety", CAT_SAFETY, "all_modules",
                 "v0.3.0", STABLE_STATUS_STABLE, "STABLE",
                 [], [], [], [],
                 ["all_modules"],
                 ["no_real_orders=True enforced on all classes",
                  "production_blocked=True enforced on all classes",
                  "_guard() rejects BUY/SELL/ORDER/EXECUTE/SUBMIT_ORDER/AUTO_TRADE/REAL_TRADE"],
                 ["Safety declaration phrases exempt from _guard()"]),
            _cap("sup_production_blocked", "Production Trading BLOCKED", CAT_SAFETY, "all_modules",
                 "v0.3.0", STABLE_STATUS_STABLE, "STABLE",
                 [], [], [], [],
                 ["all_modules"],
                 ["REAL_ORDER_READY=False", "No broker connection", "No auto-trading"],
                 ["Real order execution permanently blocked in v1"]),
            _cap("sup_strategy_lab", "Strategy Lab Stable", CAT_STABLE_RELEASE, "strategy_lab",
                 "v0.9.0", STABLE_STATUS_STABLE, "STABLE",
                 ["strategy-lab", "strategy-lab-summary", "strategy-lab-capabilities",
                  "strategy-lab-checks", "strategy-lab-manifest", "strategy-lab-report"],
                 ["Strategy Lab"], ["strategy_lab_stable_report"],
                 ["release_gate"],
                 ["research_intelligence", "strategy_memory", "backtest_coach",
                  "training_metrics", "evidence_graph"],
                 ["Stable validation only; no auto-modify of any module status"],
                 ["Does not auto-run sub-modules; reads existing CSV outputs"]),
        ]
