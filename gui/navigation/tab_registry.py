"""
gui/navigation/tab_registry.py — GUITabRegistry and GUITabMetadata for TW Quant Cockpit v0.5.2.

Registry of all known GUI tabs with metadata: group, priority, keywords, CLI mapping.

[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class GUITabMetadata:
    """Metadata for a single GUI tab in TW Quant Cockpit.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    tab_id: str
    tab_name: str
    display_name: str
    group: str
    priority: str                      # P0 / P1 / P2 / P3
    description: str = ""
    module_path: str = ""
    class_name: str = ""
    available_flag: str = ""
    safety_level: str = "RESEARCH_ONLY"
    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True
    keywords: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    related_cli_commands: List[str] = field(default_factory=list)
    report_types: List[str] = field(default_factory=list)
    maturity: str = "STABLE"           # STABLE / USABLE / EXPERIMENTAL
    default_visible: bool = True
    favorite_default: bool = False
    notes: str = ""


class GUITabRegistry:
    """Registry of all known GUI tabs with metadata.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self) -> None:
        self._tabs: dict[str, GUITabMetadata] = {}
        self._build_registry()

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def _build_registry(self) -> None:
        """Register all known tabs."""
        tabs = [
            # ----------------------------------------------------------------
            # Group: daily_research
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="daily_workflow",
                tab_name="daily_workflow",
                display_name="Daily Workflow",
                group="daily_research",
                priority="P0",
                description="Daily research workflow engine — run daily research checklist",
                module_path="gui.daily_workflow_panel",
                class_name="DailyWorkflowPanel",
                available_flag="_DAILY_WORKFLOW_AVAILABLE",
                keywords=["daily", "workflow", "research"],
                related_cli_commands=["daily-workflow", "workflow-daily"],
                maturity="STABLE",
                favorite_default=True,
            ),
            GUITabMetadata(
                tab_id="auto_report_center",
                tab_name="auto_report_center",
                display_name="Auto Report Center",
                group="daily_research",
                priority="P0",
                description="Auto Report Center — generate all research reports in one run",
                module_path="gui.auto_report_center_panel",
                class_name="AutoReportCenterPanel",
                available_flag="_AUTO_REPORT_AVAILABLE",
                keywords=["report", "auto", "daily"],
                related_cli_commands=["auto-report"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="research_workflow",
                tab_name="research_workflow",
                display_name="Research Workflow",
                group="daily_research",
                priority="P1",
                description="Research Workflow Automation — build and run automated workflow packages",
                module_path="gui.research_workflow_panel",
                class_name="ResearchWorkflowPanel",
                available_flag="_RESEARCH_WORKFLOW_AVAILABLE",
                keywords=["workflow", "automation", "research"],
                related_cli_commands=["research-workflow", "workflow-daily"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="research_coach",
                tab_name="research_coach",
                display_name="Research Coach",
                group="daily_research",
                priority="P1",
                description="Research Assistant / Coach — daily coaching recommendations and checklist",
                module_path="gui.research_assistant_panel",
                class_name="ResearchAssistantPanel",
                available_flag="_RESEARCH_ASSISTANT_AVAILABLE",
                keywords=["coach", "assistant", "research"],
                related_cli_commands=["research-coach", "coach-daily"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="research_review",
                tab_name="research_review",
                display_name="Research Review",
                group="daily_research",
                priority="P1",
                description="Research Review Dashboard — aggregated review scorecard and action planner",
                module_path="gui.research_review_dashboard_panel",
                class_name="ResearchReviewDashboardPanel",
                available_flag="_RESEARCH_REVIEW_AVAILABLE",
                keywords=["review", "dashboard", "research"],
                related_cli_commands=["research-review", "review-daily"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="notification_center",
                tab_name="notification_center",
                display_name="Notification Center",
                group="daily_research",
                priority="P2",
                description="Notification Center — research-only alerts and notification log",
                module_path="gui.notification_center_panel",
                class_name="NotificationCenterPanel",
                available_flag="_NOTIFICATION_CENTER_AVAILABLE",
                keywords=["notification", "alert", "notify"],
                related_cli_commands=["notification-list", "notify"],
                maturity="STABLE",
            ),
            # ----------------------------------------------------------------
            # Group: data_providers
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="api_fetch_status",
                tab_name="api_fetch_status",
                display_name="API Fetch Status",
                group="data_providers",
                priority="P1",
                description="API Fetch Status — provider diagnostics, cache stats, token health",
                module_path="gui.api_fetch_status_panel",
                class_name="APIFetchStatusPanel",
                available_flag="_API_FETCH_STATUS_AVAILABLE",
                keywords=["api", "fetch", "provider", "data"],
                related_cli_commands=["api-fetch-status"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="provider_health",
                tab_name="provider_health",
                display_name="Provider Health",
                group="data_providers",
                priority="P1",
                description="Provider Health — data provider token status and health monitoring",
                module_path="gui.provider_health_panel",
                class_name="ProviderHealthPanel",
                available_flag="_PROVIDER_HEALTH_AVAILABLE",
                keywords=["provider", "health", "token"],
                related_cli_commands=["provider-health"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="provider_reliability",
                tab_name="provider_reliability",
                display_name="Provider Reliability",
                group="data_providers",
                priority="P1",
                description="Provider Reliability — fallback matrix, reliability scores, mock detection",
                module_path="gui.provider_reliability_panel",
                class_name="ProviderReliabilityPanel",
                available_flag="_PROVIDER_RELIABILITY_AVAILABLE",
                keywords=["provider", "reliability", "fallback"],
                related_cli_commands=["provider-reliability", "providers"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="data_provider_fetch",
                tab_name="data_provider_fetch",
                display_name="Data Provider Fetch",
                group="data_providers",
                priority="P2",
                description="Data Provider Fetch — auto-fetch all data sources with retry and cache",
                module_path="gui.data_provider_fetch_panel",
                class_name="DataProviderFetchPanel",
                available_flag="_DATA_PROVIDER_FETCH_AVAILABLE",
                keywords=["data", "fetch", "provider", "download"],
                related_cli_commands=["data-provider-fetch"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="data_quality_gate",
                tab_name="data_quality_gate",
                display_name="Data Quality Gate",
                group="data_providers",
                priority="P0",
                description="Data Quality Gate — data completeness, mock-contamination, readiness scoring",
                module_path="gui.data_quality_gate_panel",
                class_name="DataQualityGatePanel",
                available_flag="_DATA_QUALITY_GATE_AVAILABLE",
                keywords=["data", "quality", "gate"],
                related_cli_commands=["data-quality-gate", "dq"],
                maturity="STABLE",
                favorite_default=True,
            ),
            GUITabMetadata(
                tab_id="universe_manager",
                tab_name="universe_manager",
                display_name="Universe Manager",
                group="data_providers",
                priority="P2",
                description="Universe Manager — stock universe, sector classification, universe expansion",
                module_path="gui.universe_manager_panel",
                class_name="UniverseManagerPanel",
                available_flag="_UNIVERSE_MANAGER_AVAILABLE",
                keywords=["universe", "stocks", "tickers"],
                related_cli_commands=["universe-manage"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="data_stabilization",
                tab_name="data_stabilization",
                display_name="Data Stabilization",
                group="data_providers",
                priority="P1",
                description="Data / Feature Store Stabilization — schema, lineage, readiness, health, leakage guard",
                module_path="gui.data_stabilization_panel",
                class_name="DataStabilizationPanel",
                available_flag="_DATA_STAB_PANEL_AVAILABLE",
                keywords=[
                    "data", "feature store", "lineage", "schema", "readiness",
                    "leakage", "freshness", "provider", "stabilization",
                    "資料", "特徵", "洩漏", "新鮮度", "schema",
                ],
                related_cli_commands=[
                    "data-stabilization", "data-stabilization-report",
                    "data-stabilization-summary", "data-lineage",
                    "feature-readiness", "feature-store-health", "leakage-guard",
                ],
                maturity="STABLE",
            ),
            # ----------------------------------------------------------------
            # Group: strategy_rules
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="rule_governance",
                tab_name="rule_governance",
                display_name="Rule Governance",
                group="strategy_rules",
                priority="P0",
                description="Rule Governance — rule registry, rule activation, rule confidence",
                module_path="gui.rule_governance_panel",
                class_name="RuleGovernancePanel",
                keywords=["rule", "governance", "strategy"],
                related_cli_commands=["rule-governance", "rules"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="signal_quality",
                tab_name="signal_quality",
                display_name="Signal Quality",
                group="strategy_rules",
                priority="P0",
                description="Signal Quality — signal hit rate, precision, false positive analysis",
                module_path="gui.signal_quality_panel",
                class_name="SignalQualityPanel",
                keywords=["signal", "quality", "strategy"],
                related_cli_commands=["signal-quality", "signals"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="rule_weight_tuning",
                tab_name="rule_weight_tuning",
                display_name="Rule Weight Tuning",
                group="strategy_rules",
                priority="P1",
                description="Rule Weight Tuning Lab — tune rule weights with backtesting (no auto-apply)",
                module_path="gui.rule_weight_tuning_panel",
                class_name="RuleWeightTuningPanel",
                keywords=["weight", "tuning", "rule"],
                related_cli_commands=["tune-rule-weights"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="strategy_knowledge",
                tab_name="strategy_knowledge",
                display_name="Strategy Knowledge",
                group="strategy_rules",
                priority="P1",
                description="Strategy Knowledge Ingestion — ingest transcripts, extract rules",
                module_path="gui.strategy_knowledge_ingestion_panel",
                class_name="StrategyKnowledgeIngestionPanel",
                available_flag="_STRATEGY_KNOWLEDGE_AVAILABLE",
                keywords=["knowledge", "strategy", "transcript"],
                related_cli_commands=["strategy-knowledge-list"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="ml_knowledge_integration",
                tab_name="ml_knowledge_integration",
                display_name="ML Knowledge Integration",
                group="strategy_rules",
                priority="P1",
                description="ML Knowledge Integration — bridge strategy knowledge to ML features",
                module_path="gui.ml_knowledge_integration_panel",
                class_name="MLKnowledgeIntegrationPanel",
                available_flag="_ML_KNOWLEDGE_AVAILABLE",
                keywords=["ml", "knowledge", "feature"],
                related_cli_commands=["ml-knowledge-catalog"],
                maturity="STABLE",
            ),
            # v0.5.2.1 — Strategy Filter integrated into Strategy & Rules group
            GUITabMetadata(
                tab_id="strategy_filter",
                tab_name="Strategy Filter",
                display_name="Strategy Filter / 財報翻多策略篩選",
                group="strategy_rules",
                priority="P1",
                description=(
                    "Financial Turnaround & Trend Discipline strategy filter. "
                    "Scores stocks using fundamentals (EPS, Q1 EPS×4, 月營收, 毛利率, 營益率), "
                    "technical trend (低位階, 底部翻多, 站回均線), chip support (法人, 籌碼), "
                    "moving-average discipline (月線, 季線), and risk conditions. "
                    "Three scenario archetypes: 財報好+低位階+技術翻多, 財報好但已大漲, 財報差+大盤創高個股不過高. "
                    "Research-only filter; no real orders."
                ),
                module_path="gui.dashboard",
                class_name="InlineDashboardTab",
                available_flag="_STRATEGY_FILTER_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "strategy", "filter", "strategy filter",
                    "financial", "turnaround", "trend discipline",
                    "EPS", "Q1 EPS", "revenue",
                    "財報", "財報翻多", "EPS成長", "Q1 EPS × 4",
                    "月營收", "毛利率", "營益率",
                    "低位階", "底部翻多", "趨勢紀律",
                    "第二波買點", "回測不破", "不追高",
                    "汰弱換強", "月線", "季線",
                ],
                aliases=[
                    "financial-turnaround", "trend-discipline",
                    "strategy-filter", "財報翻多", "第二波買點",
                ],
                related_cli_commands=[
                    "strategy-filter", "strategy-filter-pack",
                    "rule-governance", "signal-quality",
                    "strategy-knowledge-summary",
                ],
                report_types=["strategy_filter_report"],
                maturity="EXPERIMENTAL",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.5.2.1 to integrate v0.5.1.1 Strategy Filter Pack into GUI Navigation.",
            ),
            # ----------------------------------------------------------------
            # Group: backtest_simulation
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="hardened_backtest",
                tab_name="hardened_backtest",
                display_name="Hardened Backtest",
                group="backtest_simulation",
                priority="P0",
                description="Hardened Backtest Engine — walk-forward backtest with bias and overfitting guards",
                module_path="gui.hardened_backtest_panel",
                class_name="HardenedBacktestPanel",
                available_flag="_HARDENED_BACKTEST_AVAILABLE",
                keywords=["backtest", "hardened", "simulation"],
                related_cli_commands=["hardened-backtest"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="portfolio_cockpit",
                tab_name="portfolio_cockpit",
                display_name="Portfolio Cockpit",
                group="backtest_simulation",
                priority="P1",
                description="Portfolio Cockpit — simulated positions, P&L, and portfolio risk dashboard",
                module_path="gui.portfolio_cockpit_panel",
                class_name="PortfolioCockpitPanel",
                keywords=["portfolio", "cockpit", "positions"],
                related_cli_commands=["portfolio-positions"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="intraday_pipeline",
                tab_name="intraday_pipeline",
                display_name="Intraday Pipeline",
                group="backtest_simulation",
                priority="P1",
                description="Intraday Pipeline — tick data ingestion, VWAP, microstructure features",
                module_path="gui.intraday_pipeline_panel",
                class_name="IntradayPipelinePanel",
                available_flag="_INTRADAY_PIPELINE_AVAILABLE",
                keywords=["intraday", "pipeline", "tick"],
                related_cli_commands=["intraday-pipeline"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="intraday_replay",
                tab_name="intraday_replay",
                display_name="Intraday Replay",
                group="backtest_simulation",
                priority="P0",
                description="Intraday Replay — replay training scenarios, VWAP/breakout/opening range",
                module_path="gui.intraday_replay_panel",
                class_name="IntradayReplayPanel",
                available_flag="_INTRADAY_REPLAY_AVAILABLE",
                keywords=["replay", "intraday", "training"],
                related_cli_commands=["intraday-replay"],
                maturity="STABLE",
                favorite_default=True,
            ),
            GUITabMetadata(
                tab_id="replay_training",
                tab_name="replay_training",
                display_name="TW Replay Training Cockpit / 台股時光機復盤練習",
                group="backtest_simulation",
                priority="P0",
                description=(
                    "TW Replay Training Cockpit v0.5.6 — "
                    "bar-by-bar tape reading practice, AI rule-based review, scoring, drills"
                ),
                module_path="gui.replay_training_panel",
                class_name="ReplayTrainingPanel",
                available_flag="_REPLAY_TRAINING_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "replay", "training", "tape reading", "台股時光機", "復盤",
                    "盤感", "盤感訓練", "逐根K", "AI復盤", "VWAP", "假突破",
                    "開盤區間", "停損", "停利", "replay score", "drills",
                ],
                related_cli_commands=[
                    "replay-training", "replay-training-summary", "replay-training-next",
                    "replay-training-prev", "replay-training-marker", "replay-ai-review",
                    "replay-training-score", "replay-training-drills", "replay-training-report",
                ],
                maturity="STABLE",
                favorite_default=False,
                notes="v0.5.6 — Replay Training Only / Research Only / No Real Orders",
            ),
            # ----------------------------------------------------------------
            # Group: ml_monitoring
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="ml_feature_store",
                tab_name="ml_feature_store",
                display_name="ML Feature Store",
                group="ml_monitoring",
                priority="P1",
                description="ML Feature Store — feature catalog, snapshot builder, leakage checker",
                module_path="gui.ml_feature_store_panel",
                class_name="MLFeatureStorePanel",
                available_flag="_ML_FEATURE_STORE_AVAILABLE",
                keywords=["ml", "feature", "store", "dataset"],
                related_cli_commands=["ml-feature-catalog"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="model_monitoring",
                tab_name="model_monitoring",
                display_name="Model Monitoring",
                group="ml_monitoring",
                priority="P1",
                description="Model Monitoring — drift detection, prediction log, hit/miss review",
                module_path="gui.model_monitoring_panel",
                class_name="ModelMonitoringPanel",
                available_flag="_MODEL_MONITORING_AVAILABLE",
                keywords=["model", "monitoring", "drift", "prediction"],
                related_cli_commands=["model-monitoring"],
                maturity="STABLE",
            ),
            # ----------------------------------------------------------------
            # Group: journal_review
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="portfolio_journal",
                tab_name="portfolio_journal",
                display_name="Portfolio Journal",
                group="journal_review",
                priority="P1",
                description="Portfolio Journal — trade journal entries, signal outcome tracking, mistake taxonomy",
                module_path="gui.portfolio_journal_panel",
                class_name="PortfolioJournalPanel",
                available_flag="_PORTFOLIO_JOURNAL_AVAILABLE",
                keywords=["journal", "trade", "review", "outcome"],
                related_cli_commands=["journal-add", "journal"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="experiment_registry",
                tab_name="experiment_registry",
                display_name="Experiment Registry",
                group="journal_review",
                priority="P1",
                description="Experiment Registry — research experiments, hypotheses, parameter sets",
                module_path="gui.experiment_registry_panel",
                class_name="ExperimentRegistryPanel",
                keywords=["experiment", "registry", "research"],
                related_cli_commands=["exp-list"],
                maturity="STABLE",
            ),
            # ----------------------------------------------------------------
            # Group: research_os
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="research_os_planning",
                tab_name="research_os_planning",
                display_name="Research OS Planning",
                group="research_os",
                priority="P1",
                description="Research OS Planning — module inventory, CLI inventory, GUI tab inventory, safety matrix",
                module_path="gui.research_os_planning_panel",
                class_name="ResearchOSPlanningPanel",
                available_flag="_RESEARCH_OS_PLANNING_AVAILABLE",
                keywords=["os", "planning", "inventory", "modules"],
                related_cli_commands=["research-os-summary", "os"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="cli_ux",
                tab_name="cli_ux",
                display_name="CLI UX",
                group="research_os",
                priority="P2",
                description="CLI UX — command registry, alias map, help examples, command discovery",
                module_path="gui.cli_ux_panel",
                class_name="CLIUXPanel",
                available_flag="_CLI_UX_AVAILABLE",
                keywords=["cli", "alias", "command", "ux"],
                related_cli_commands=["cli-list", "cli-aliases"],
                maturity="STABLE",
            ),
            GUITabMetadata(
                tab_id="gui_navigation",
                tab_name="gui_navigation",
                display_name="GUI Navigation",
                group="research_os",
                priority="P2",
                description="GUI Navigation — tab registry, tab groups, search, favorites/recent",
                module_path="gui.gui_navigation_panel",
                class_name="GUINavigationPanel",
                available_flag="_GUI_NAVIGATION_AVAILABLE",
                keywords=["gui", "navigation", "tabs", "grouping"],
                related_cli_commands=["gui-nav-summary", "gui-nav-tabs"],
                maturity="STABLE",
            ),
            # ----------------------------------------------------------------
            # Group: release_qa
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="release_status",
                tab_name="release_status",
                display_name="Release Status",
                group="release_qa",
                priority="P1",
                description="Release Status — stable release checklist and regression suite dashboard",
                module_path="gui.release_status_panel",
                class_name="ReleaseStatusPanel",
                available_flag="_RELEASE_STATUS_AVAILABLE",
                keywords=["release", "status", "regression"],
                related_cli_commands=["stable-release-check", "regression-suite"],
                maturity="STABLE",
            ),
            # v0.6.0 Stable Release
            GUITabMetadata(
                tab_id="stable_release",
                tab_name="Stable Release",
                display_name="Research OS Stable Release",
                group="release_qa",
                priority="P0",
                description=(
                    "Research OS Stable Release v0.6.0 — stable capability matrix, "
                    "release checklist, known limitations, manifest builder. "
                    "Research Only. No Real Orders. Production Trading BLOCKED."
                ),
                module_path="gui.stable_release_panel",
                class_name="StableReleasePanel",
                available_flag="_STABLE_RELEASE_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "stable", "release", "v0.6.0", "checklist", "manifest",
                    "capability", "stable release", "limitations",
                    "穩定版", "發版", "封版",
                ],
                aliases=["stable-release", "v0.6.0", "release-v060"],
                related_cli_commands=[
                    "stable-v060-check", "stable-v060-report",
                    "stable-v060-manifest", "stable-v060-capabilities",
                    "stable-v060-limitations", "stable-v060-summary",
                ],
                report_types=["stable_release_v060_report", "release_manifest"],
                maturity="STABLE",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.6.0 — Research OS Stable Release consolidation.",
            ),
            GUITabMetadata(
                tab_id="usability_qa",
                tab_name="usability_qa",
                display_name="Usability QA",
                group="release_qa",
                priority="P2",
                description="Usability QA — smoke tests, error message clarity, empty state handling",
                module_path="gui.usability_qa_panel",
                class_name="UsabilityQAPanel",
                available_flag="_USABILITY_QA_AVAILABLE",
                keywords=["usability", "qa", "smoke", "test"],
                related_cli_commands=["usability-qa"],
                maturity="STABLE",
            ),
            # v0.5.3 Regression Suite Consolidation
            GUITabMetadata(
                tab_id="regression_suite",
                tab_name="regression_suite",
                display_name="Regression Suite",
                group="release_qa",
                priority="P1",
                description=(
                    "Regression Suite Consolidation \u2014 unified test suites "
                    "(quick/full/gui/report/safety/data/strategy/replay/research_os/release_gate), "
                    "coverage matrix, and markdown report. Regression Only. No Real Orders."
                ),
                module_path="gui.regression_suite_panel",
                class_name="RegressionSuitePanel",
                available_flag="_REGRESSION_SUITE_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "regression", "test", "suite", "quick", "full", "safety", "gui",
                    "report", "coverage", "\u6e2c\u8a66", "\u56de\u6b78\u6e2c\u8a66",
                    "coverage matrix",
                ],
                aliases=["regression-suite", "regression-run", "coverage"],
                related_cli_commands=[
                    "regression-list-suites", "regression-run",
                    "regression-coverage", "regression-report", "regression-suite",
                ],
                report_types=["regression_consolidation_report"],
                maturity="USABLE",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.5.3 \u2014 Regression Suite Consolidation.",
            ),
            # v0.6.2 Data Coverage Expansion
            GUITabMetadata(
                tab_id="data_coverage",
                tab_name="Data Coverage",
                display_name="Data Coverage Expansion",
                group="data_providers",
                priority="P1",
                description=(
                    "Data Coverage Expansion v0.6.2 — scan and track coverage across provider, "
                    "daily data, intraday, financial, feature store, replay, experiment, "
                    "rule governance, report pack, and stable release domains. "
                    "Classify gaps as READY, ENV_LIMITED, NOT_GENERATED, or MISSING. "
                    "Research Only. No Real Orders."
                ),
                module_path="gui.data_coverage_panel",
                class_name="DataCoveragePanel",
                available_flag="_DATA_COVERAGE_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "data coverage", "coverage", "provider", "intraday", "report pack",
                    "feature store", "env limited", "not generated",
                    "\u8cc7\u6599\u8986\u84cb", "\u8cc7\u6599\u7f3a\u53e3", "\u8986\u84cb\u7387",
                ],
                aliases=["data-coverage", "coverage-scan", "data-gaps"],
                related_cli_commands=[
                    "data-coverage", "data-coverage-summary",
                    "data-coverage-items", "data-coverage-report", "data-coverage-gaps",
                ],
                report_types=["data_coverage"],
                maturity="STABLE",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.6.2 \u2014 Data Coverage Expansion.",
            ),
            # v0.7.0 Research Intelligence (updated v0.7.1)
            GUITabMetadata(
                tab_id="research_intelligence",
                tab_name="research_intelligence",
                display_name="Research Intelligence",
                group="daily_research",
                priority="P0",
                description=(
                    "Research Intelligence v0.7.1 — aggregate signals from all Research OS modules, "
                    "build P0/P1/P2/P3 priority boards, generate daily (7 items) and weekly (12 items) "
                    "research plans. Today Focus, Why Now, Risk If Ignored, Safe Command labels, "
                    "Copy Command button, filter by priority/category/source. "
                    "Research Only. No Real Orders. No BUY/SELL/ORDER."
                ),
                module_path="gui.research_intelligence_panel",
                class_name="ResearchIntelligencePanel",
                available_flag="_RESEARCH_INTELLIGENCE_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "research intelligence", "priority board", "daily plan", "weekly plan",
                    "signals", "recommendations", "p0", "p1", "gaps",
                    "intelligence ux", "today focus", "safe command", "copy command",
                    "why now", "risk if ignored", "priority filter",
                    "\u7814\u7a76\u667a\u80fd", "\u512a\u5148\u7d1a", "\u8a08\u756b",
                    "\u4eca\u65e5\u91cd\u9ede", "\u5f85\u8655\u7406\u4e8b\u9805",
                    "\u5b89\u5168\u6307\u4ee4", "\u5de5\u4f5c\u6e05\u55ae",
                ],
                aliases=["research-intelligence", "ri", "intelligence"],
                related_cli_commands=[
                    "research-intelligence", "research-intelligence-summary",
                    "research-intelligence-signals", "research-intelligence-recommendations",
                    "research-intelligence-priority", "research-intelligence-daily-plan",
                    "research-intelligence-weekly-plan", "research-intelligence-report",
                ],
                report_types=["research_intelligence"],
                maturity="STABLE",
                default_visible=True,
                favorite_default=True,
                notes="Added in v0.7.0; UX polish in v0.7.1 — Today Focus, Why Now, Safe Command labels, Copy Command.",
            ),
            # v0.7.2 Strategy Research Memory
            GUITabMetadata(
                tab_id="strategy_memory",
                tab_name="strategy_memory",
                display_name="Strategy Memory",
                group="daily_research",
                priority="P1",
                description=(
                    "Strategy Research Memory v0.8.1 — extract and persist strategy hypotheses, "
                    "rule candidates, replay mistake patterns, journal patterns, data gaps, "
                    "report gaps, regression risks, provider limitations, research conclusions, "
                    "and follow-up tasks. Upsert deduplication, status/priority tracking, "
                    "memory linking, and Markdown report. "
                    "v0.8.1 UX: validation queue, active research threads, repeated patterns, "
                    "status flow (NEW→REVIEWING→VALIDATING→ACCEPTED/REJECTED), "
                    "needs_action / validation_ready UX fields, safe command labels. "
                    "ACCEPTED = research accepted, not trading enabled. "
                    "Research Only. No Real Orders. No BUY/SELL/ORDER."
                ),
                module_path="gui.strategy_memory_panel",
                class_name="StrategyMemoryPanel",
                available_flag="_STRATEGY_MEMORY_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "strategy memory", "research memory", "hypothesis", "rule memory",
                    "replay mistake memory", "journal pattern", "data gap", "report gap",
                    "regression risk", "research conclusion", "follow-up task",
                    "memory extract", "memory store", "memory links",
                    "memory ux", "validation queue", "active threads", "repeated patterns",
                    "status flow", "needs action", "memory detail", "safe commands",
                    "研究記憶", "策略記憶", "策略假設", "規則候選",
                    "復盤錯誤", "研究結論", "驗證佇列", "重複模式", "狀態流",
                ],
                aliases=["strategy-memory", "memory", "research-memory"],
                related_cli_commands=[
                    "strategy-memory", "strategy-memory-summary",
                    "strategy-memory-list", "strategy-memory-search",
                    "strategy-memory-show", "strategy-memory-update-status",
                    "strategy-memory-archive", "strategy-memory-report",
                    "strategy-memory-validation-queue",
                    "strategy-memory-active-threads",
                    "strategy-memory-repeated-patterns",
                ],
                report_types=["strategy_memory"],
                maturity="STABLE",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.7.2 — Strategy Research Memory. UX polish in v0.8.1: validation queue, active threads, repeated patterns, status flow, safe command labels.",
            ),
            # v0.7.3 Backtest-to-Coach Loop
            GUITabMetadata(
                tab_id="backtest_coach",
                tab_name="backtest_coach",
                display_name="Backtest Coach",
                group="daily_research",
                priority="P1",
                description=(
                    "Backtest-to-Coach Loop v0.7.3 — converts backtest weaknesses, replay mistakes, "
                    "journal patterns, rule issues, strategy memories, and data gaps into safe coach "
                    "training tasks (PRACTICE_REPLAY, REVIEW_RULE, REVIEW_JOURNAL, FIX_DATA, "
                    "BACKTEST_MORE, READ_REPORT, UPDATE_MEMORY, WAIT). "
                    "No BUY/SELL/ORDER. Research Only. No Real Orders."
                ),
                module_path="gui.backtest_coach_panel",
                class_name="BacktestCoachPanel",
                available_flag="_BACKTEST_COACH_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "backtest coach", "coach loop", "training tasks", "practice replay",
                    "review rule", "review journal", "fix data", "backtest more",
                    "coach signal", "coach task", "daily plan", "weekly plan",
                    "複盤教練", "回測教練", "訓練任務", "練習計畫",
                ],
                aliases=["backtest-coach", "coach", "training-loop"],
                related_cli_commands=[
                    "backtest-coach", "backtest-coach-summary",
                    "backtest-coach-signals", "backtest-coach-tasks",
                    "backtest-coach-daily-plan", "backtest-coach-weekly-plan",
                    "backtest-coach-report",
                ],
                report_types=["backtest_coach"],
                maturity="STABLE",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.7.3 — Backtest-to-Coach Loop.",
            ),
            # v0.8.0 Research Intelligence Stable
            GUITabMetadata(
                tab_id="intelligence_stable",
                tab_name="intelligence_stable",
                display_name="Intelligence Stable",
                group="research_os",
                priority="P0",
                description=(
                    "Research Intelligence Stable v0.8.0 — validates and stabilizes all Research "
                    "Intelligence capabilities: Research Intelligence (v0.7.0-0.7.1), Strategy Memory "
                    "(v0.7.2), and Backtest-to-Coach Loop (v0.7.3). 29 capabilities across 5 categories, "
                    "7-category stable checklist, release manifest, and safety audit. "
                    "No BUY/SELL/ORDER. Research Only. No Real Orders. Production Trading BLOCKED."
                ),
                module_path="gui.intelligence_stable_panel",
                class_name="IntelligenceStablePanel",
                available_flag="_INTELLIGENCE_STABLE_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "intelligence stable", "stable validation", "capability matrix",
                    "stable checklist", "release manifest", "safety audit",
                    "research intelligence", "strategy memory", "backtest coach",
                    "研究智能穩定", "穩定驗證", "能力矩陣", "穩定清單", "安全審計",
                ],
                aliases=["intelligence-stable", "stable", "research-stable"],
                related_cli_commands=[
                    "intelligence-stable", "intelligence-stable-summary",
                    "intelligence-stable-capabilities", "intelligence-stable-checks",
                    "intelligence-stable-manifest", "intelligence-stable-report",
                ],
                report_types=["intelligence_stable"],
                maturity="STABLE",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.8.0 — Research Intelligence Stable.",
            ),
            # v0.5.4 Report Pack Consolidation
            GUITabMetadata(
                tab_id="report_pack",
                tab_name="report_pack",
                display_name="Report Pack",
                group="daily_research",
                priority="P1",
                description=(
                    "Report Pack Consolidation \u2014 daily/weekly/full report bundles, "
                    "health check, link index, and manifest. Research Only. No Real Orders."
                ),
                module_path="gui.report_pack_panel",
                class_name="ReportPackPanel",
                available_flag="_REPORT_PACK_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "report", "pack", "daily", "weekly", "full", "manifest",
                    "index", "report health", "\u5831\u544a", "\u6bcf\u65e5\u5831\u544a",
                    "\u9031\u5831", "\u5b8c\u6574\u5831\u544a",
                ],
                aliases=["report-pack", "report-pack-summary", "report-health"],
                related_cli_commands=[
                    "report-pack", "report-pack-summary", "report-pack-items",
                    "report-pack-health", "report-pack-links", "report-pack-report",
                ],
                report_types=["report_pack_consolidation_report"],
                maturity="USABLE",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.5.4 \u2014 Report Pack Consolidation.",
            ),
            # v0.8.2 Backtest Training Metrics
            GUITabMetadata(
                tab_id="training_metrics",
                tab_name="training_metrics",
                display_name="Training Metrics",
                group="research_os",
                priority="P1",
                description=(
                    "Backtest Training Metrics \u2014 measures training effectiveness: "
                    "task completion, replay score, mistake reduction, memory validation. "
                    "Research Only. No Real Orders."
                ),
                module_path="gui.training_metrics_panel",
                class_name="TrainingMetricsPanel",
                available_flag="_TRAINING_METRICS_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "training", "metrics", "effectiveness", "progress", "trend",
                    "task completion", "replay score", "mistake reduction",
                    "memory validation", "backtest issues", "quality score",
                    "improving", "worsening", "insufficient data",
                ],
                aliases=["training-metrics", "training-metrics-summary", "training-metrics-trend"],
                related_cli_commands=[
                    "training-metrics", "training-metrics-summary",
                    "training-metrics-detail", "training-metrics-trend",
                    "training-metrics-report",
                ],
                report_types=["training_metrics"],
                maturity="USABLE",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.8.2 \u2014 Backtest Training Metrics.",
            ),
            # v0.8.3 Research Intelligence Evidence Graph
            GUITabMetadata(
                tab_id="evidence_graph",
                tab_name="evidence_graph",
                display_name="Research Intelligence Evidence Graph",
                group="research_os",
                priority="P1",
                description=(
                    "Research Intelligence Evidence Graph \u2014 links research recommendations, "
                    "strategy memories, backtest coach tasks, training metrics, replay mistakes, "
                    "journal patterns, data gaps, report results, and regression results into "
                    "evidence threads. Research Only. No Real Orders."
                ),
                module_path="gui.evidence_graph_panel",
                class_name="EvidenceGraphPanel",
                available_flag="_EVIDENCE_GRAPH_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "evidence graph", "research graph", "evidence thread", "node", "edge",
                    "requires backtest", "requires data", "requires replay",
                    "orphan", "contradiction", "supports", "validates",
                    "\u7814\u7a76\u8b49\u64da", "\u8b49\u64da\u5716\u8b5c",
                    "\u8b49\u64da\u93c8", "\u95dc\u806f\u5716", "\u56de\u6e2c\u8b49\u64da",
                    # v0.9.1 Evidence Graph UX keywords
                    "evidence graph ux", "thread quality", "evidence path", "graph gaps",
                    "crash reversal evidence", "\u8b49\u64da\u5716\u8b5cUX", "\u8b49\u64da\u93c8",
                    "\u8b49\u64da\u8def\u5f91", "\u5927\u8dcc\u8b49\u64da\u93c8", "\u95dc\u806f\u8def\u5f91",
                ],
                aliases=["evidence-graph", "evidence-graph-summary", "evidence-graph-nodes"],
                related_cli_commands=[
                    "evidence-graph", "evidence-graph-summary", "evidence-graph-nodes",
                    "evidence-graph-edges", "evidence-graph-threads",
                    "evidence-graph-orphans", "evidence-graph-requires-backtest",
                    "evidence-graph-requires-data", "evidence-graph-report",
                ],
                report_types=["evidence_graph"],
                maturity="USABLE",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.8.3 \u2014 Research Intelligence Evidence Graph.",
            ),
            # v0.9.0.1 crash reversal
            GUITabMetadata(
                tab_id="crash_reversal",
                tab_name="Crash Reversal",
                display_name="Crash Reversal & Risk Discipline",
                group="strategy_lab",
                priority="P1",
                description=(
                    "Crash Reversal & Risk Discipline Strategy Pack v0.9.0.1 — "
                    "crash cause classification, post-crash stabilization checklist, "
                    "relative strength after crash scoring, EPS-backed dip buy filtering, "
                    "MA profit discipline, high-risk industry guard. "
                    "Research Only. No Real Orders. Production BLOCKED."
                ),
                module_path="gui.crash_reversal_panel",
                class_name="CrashReversalPanel",
                available_flag=True,
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "crash reversal", "dip buy", "crash cause", "stabilization",
                    "relative strength after crash", "sakata", "EPS dip buy",
                    "risk discipline", "大跌", "送分題", "轉空頭", "抗跌股",
                    "阪田", "EPS低接", "高風險產業", "均線停利",
                ],
                related_cli_commands=[
                    "crash-reversal", "crash-reversal-summary",
                    "crash-reversal-report", "crash-reversal-score",
                    "crash-reversal-watchlist",
                ],
                maturity="v0.9.0.1",
                default_visible=True,
            ),
            # v0.9.2 Strategy Validation Score
            GUITabMetadata(
                tab_id="strategy_validation",
                tab_name="Strategy Validation",
                display_name="Strategy Validation Score",
                group="strategy_lab",
                priority="P0",
                module_path="gui.strategy_validation_panel",
                class_name="StrategyValidationPanel",
                available_flag=True,
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=["strategy validation","validation score","validated","observational",
                          "insufficient","conflicted","rejected","策略驗證","策略分數","驗證分數",
                          "已驗證","證據不足","策略評級"],
                related_cli_commands=["strategy-validation","strategy-validation-summary","strategy-validation-scores","strategy-validation-report","strategy-validation-top"],
                maturity="v0.9.2",
                default_visible=True,
            ),
            # v0.9.0 Strategy Lab Stable
            GUITabMetadata(
                tab_id="strategy_lab",
                tab_name="strategy_lab",
                display_name="Strategy Lab Stable",
                group="research_os",
                priority="P1",
                description=(
                    "Strategy Lab Stable \u2014 unified validation wrapper over Research Intelligence, "
                    "Strategy Memory, Backtest Coach, Training Metrics, and Evidence Graph. "
                    "47-capability matrix, 7-category checklist, release manifest, 13-section report. "
                    "Research Only. No Real Orders. Production BLOCKED."
                ),
                module_path="gui.strategy_lab_panel",
                class_name="StrategyLabPanel",
                available_flag="_STRATEGY_LAB_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "strategy lab", "stable", "capability matrix", "stable checklist",
                    "release manifest", "strategy lab stable", "validation",
                    "dashboard", "strategy lab dashboard", "validation board", "action board",
                    "evidence board", "module health",
                    # v1.0.0 Research Trading Cockpit Stable keywords
                    "v1.0.0", "research cockpit", "stable release",
                    "research trading cockpit", "stable report", "release checklist",
                    "No Real Orders", "\u7a69\u5b9a\u7248", "\u7814\u7a76\u63a7\u76e4",
                    "\u7814\u7a76\u63a7\u76e4\u7a69\u5b9a\u7248",
                    "\u7121\u5be6\u76e4\u4e0b\u55ae", "\u4e0d\u63a5\u5238\u5546",
                    "\u4e0d\u81ea\u52d5\u4ea4\u6613",
                    # v1.0.1 Maintenance & Polish keywords
                    "v1.0.1", "maintenance", "polish", "research cockpit stable",
                    "no real orders", "\u7dad\u8b77\u7248", "\u7dad\u8b77",
                    "\u7b56\u7565\u5be6\u9a57\u5ba4", "\u7a69\u5b9a\u6aa2\u67e5\u8868",
                    "\u5100\u8868\u677f", "\u7b56\u7565\u7e3d\u63a7", "\u7b56\u7565\u5100\u8868\u677f",
                    "\u9a57\u8b49\u770b\u677f", "\u884c\u52d5\u770b\u677f", "\u8b49\u64da\u770b\u677f",
                ],
                aliases=["strategy-lab", "strategy-lab-summary", "strategy-lab-capabilities"],
                related_cli_commands=[
                    "strategy-lab", "strategy-lab-summary", "strategy-lab-capabilities",
                    "strategy-lab-checks", "strategy-lab-manifest", "strategy-lab-report",
                ],
                report_types=["strategy_lab_stable"],
                maturity="STABLE",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.9.0 \u2014 Strategy Lab Stable.",
            ),
            # v0.9.3 Strategy Lab Dashboard
            GUITabMetadata(
                tab_id="strategy_lab_dashboard",
                tab_name="strategy_lab_dashboard",
                display_name="Strategy Lab Dashboard",
                group="strategy_lab",
                priority="P0",
                description=(
                    "Strategy Lab Dashboard v0.9.3 \u2014 unified single-view dashboard "
                    "summarizing validation grades, evidence graph health, crash reversal risks, "
                    "training metrics, coach tasks, strategy memories, and research intelligence. "
                    "Research Only. No Real Orders. Production BLOCKED."
                ),
                module_path="gui.strategy_lab_dashboard_panel",
                class_name="StrategyLabDashboardPanel",
                available_flag="_STRATEGY_LAB_DASHBOARD_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "dashboard", "strategy lab dashboard", "validation board", "action board",
                    "evidence board", "module health", "crash reversal board",
                    "strategy lab status", "grade mix", "needs backtest", "needs replay",
                    "gui polish", "gui stability", "usability", "qthread", "table layout",
                    "empty state", "copy safe command", "v1.0.3",
                    "user guide", "GUI guide", "cli cookbook", "daily workflow", "sop",
                    "troubleshooting", "safety guide", "version map", "handoff guide",
                    "documentation", "\u4f7f\u7528\u624b\u518a", "\u4ea4\u63a5", "\u4f7f\u7528\u6307\u5357",
                    "workflow templates", "examples", "templates", "daily example",
                    "release prompt", "handoff template", "\u7bc4\u4f8b\u6a21\u677f", "\u4ea4\u63a5\u6a21\u677f",
                    "\u5de5\u4f5c\u6d41",
                    "\u5100\u8868\u677f", "\u7b56\u7565\u7e3d\u63a7", "\u7b56\u7565\u5100\u8868\u677f",
                    "\u9a57\u8b49\u770b\u677f", "\u884c\u52d5\u770b\u677f", "\u8b49\u64da\u770b\u677f",
                    "GUI\u512a\u5316", "\u4ecb\u9762\u7a69\u5b9a", "\u8868\u683c\u6392\u7248",
                    "\u7a7a\u72c0\u614b", "\u5b89\u5168\u8907\u88fd", "QThread", "\u4f7f\u7528\u6027",
                ],
                aliases=["strategy-lab-dashboard", "strategy-lab-dashboard-summary"],
                related_cli_commands=[
                    "strategy-lab-dashboard", "strategy-lab-dashboard-summary",
                    "strategy-lab-dashboard-cards", "strategy-lab-dashboard-actions",
                    "strategy-lab-dashboard-priorities", "strategy-lab-dashboard-report",
                ],
                report_types=["strategy_lab_dashboard_report"],
                maturity="v0.9.3",
                default_visible=True,
                favorite_default=False,
                notes="Added in v0.9.3 \u2014 Strategy Lab Dashboard Polish.",
            ),
            # v1.0.2 Data & Report Hygiene
            GUITabMetadata(
                tab_id="data_report_hygiene",
                tab_name="data_report_hygiene",
                display_name="Data & Report Hygiene",
                group="maintenance",
                priority="P1",
                description=(
                    "Data & Report Hygiene \u2014 review-only inventory of runtime outputs, "
                    "report manifest, gitignore coverage. No deletion. No archive."
                ),
                module_path="gui.data_report_hygiene_panel",
                class_name="DataReportHygienePanel",
                available_flag="_DATA_REPORT_HYGIENE_AVAILABLE",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "data hygiene", "report hygiene", "report index", "gitignore",
                    "runtime output", "csv cleanup", "md report", "maintenance",
                    "data cleanup", "report cleanup",
                    "\u8cc7\u6599\u6e05\u7406", "\u5831\u544a\u6e05\u7406",
                    "\u7522\u7269\u6e05\u7406", "\u7dad\u8b77\u7248",
                    "runtime \u7522\u7269",
                ],
                related_cli_commands=[
                    "data-report-hygiene", "data-report-hygiene-summary",
                    "data-report-hygiene-inventory", "data-report-hygiene-reports",
                    "data-report-hygiene-gitignore", "data-report-hygiene-tracked",
                    "data-report-hygiene-report",
                ],
                report_types=["data_report_hygiene_report"],
                maturity="STABLE",
                notes="Added in v1.0.2 \u2014 Data & Report Hygiene.",
            ),
            # v1.0.3 GUI Stability & Usability Polish
            GUITabMetadata(
                tab_id="gui_stability_usability",
                tab_name="gui_stability_usability",
                display_name="GUI Stability & Usability",
                group="maintenance",
                priority="P1",
                description=(
                    "GUI Stability & Usability Polish v1.0.3 \u2014 GUI health check, "
                    "QThread safety, table usability, empty state, copy safety. "
                    "Research Only. No Real Orders."
                ),
                module_path="gui.gui_health_check",
                class_name="GuiHealthCheck",
                safety_level="RESEARCH_ONLY",
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
                keywords=[
                    "gui health check", "gui stability", "gui polish", "usability",
                    "qthread", "table layout", "empty state", "copy safe command",
                    "v1.0.3", "maintenance", "gui usability report",
                    "GUI\u512a\u5316", "\u4ecb\u9762\u7a69\u5b9a", "\u8868\u683c\u6392\u7248",
                    "\u7a7a\u72c0\u614b", "\u5b89\u5168\u8907\u88fd", "QThread", "\u4f7f\u7528\u6027",
                    # v1.0.4 Regression & Release Gate Hardening keywords
                    "regression hardening", "release gate", "safety scan", "safety scanner",
                    "known warn", "known blocked", "cp950", "paper smoke",
                    "release gate health",
                    "\u56de\u6b78\u6e2c\u8a66", "\u767c\u7248\u9598\u9580", "\u5b89\u5168\u6383\u63cf",
                    "\u767d\u540d\u55ae", "\u5df2\u77e5\u8b66\u544a", "\u5df2\u77e5\u963b\u64cb",
                ],
                related_cli_commands=[
                    "gui-health-check", "gui-usability-report",
                ],
                report_types=["gui_usability_report"],
                maturity="STABLE",
                notes="Added in v1.0.3 \u2014 GUI Stability & Usability Polish.",
            ),
            # ----------------------------------------------------------------
            # v1.0.7 Knowledge Base Search
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="knowledge_base_search",
                tab_name="knowledge_base_search",
                display_name="Knowledge Base Search",
                group="maintenance",
                priority="P1",
                description="Knowledge Base Search \u2014 search docs, examples, templates, reports, strategy memory, evidence graph metadata",
                module_path="gui.knowledge_base_search_panel",
                class_name="KnowledgeBaseSearchPanel",
                available_flag="_KNOWLEDGE_BASE_SEARCH_AVAILABLE",
                keywords=[
                    "knowledge base", "kb search", "docs search", "report search",
                    "examples search", "templates search", "strategy memory search",
                    "evidence search", "knowledge search",
                    "\u77e5\u8b58\u5eab", "\u641c\u5c0b", "\u6587\u4ef6\u641c\u5c0b", "\u5831\u544a\u641c\u5c0b", "\u7bc4\u4f8b\u641c\u5c0b", "\u6a21\u677f\u641c\u5c0b",
                    "\u4ea4\u63a5", "handoff", "release gate", "safety",
                ],
                related_cli_commands=["kb-index", "kb-summary", "kb-health-check", "kb-search", "kb-explain", "kb-report"],
                maturity="STABLE",
                no_real_orders=True,
                read_only=True,
                production_blocked=True,
            ),
            # ----------------------------------------------------------------
            # v1.0.8 Local Research Assistant
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="local_research_assistant",
                tab_name="local_research_assistant",
                display_name="Local Research Assistant",
                group="research",
                priority="P1",
                description="Local Research Assistant \u2014 safe research answers from knowledge base, module routing, safe next steps. No external API.",
                module_path="gui.local_research_assistant_panel",
                class_name="LocalResearchAssistantPanel",
                available_flag="_LOCAL_RESEARCH_ASSISTANT_AVAILABLE",
                keywords=[
                    "local assistant", "research assistant", "kb answer", "safe summary",
                    "local research", "assistant",
                    "\u672c\u5730\u52a9\u7406", "\u7814\u7a76\u52a9\u7406", "\u672c\u5730\u7814\u7a76\u52a9\u7406", "\u77e5\u8b58\u5eab\u56de\u7b54", "\u5b89\u5168\u6458\u8981", "\u4e0b\u4e00\u6b65\u7814\u7a76",
                ],
                related_cli_commands=["local-assistant", "local-assistant-summary", "local-assistant-health", "local-assistant-report"],
                maturity="STABLE",
                no_real_orders=True,
                read_only=True,
                production_blocked=True,
            ),
            # ----------------------------------------------------------------
            # v1.1.1 Data Import UX & Batch Onboarding
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="data_import_onboarding",
                tab_name="data_import_onboarding",
                display_name="Data Import & Batch Onboarding",
                group="data",
                priority="P1",
                description=(
                    "Data Import UX & Batch Onboarding v1.1.1 — XQ/CSV/Excel discovery, "
                    "column mapping, duplicate/conflict detection, safe merge planning, "
                    "retry manifests, universe coverage refresh. "
                    "Research Only. No Real Orders. dry_run=True default."
                ),
                module_path="gui.import_onboarding_panel",
                class_name="ImportOnboardingPanel",
                available_flag="_IMPORT_ONBOARDING_AVAILABLE",
                keywords=[
                    "import", "data import", "batch onboarding", "xq import", "csv import",
                    "excel import", "file discovery", "column mapping", "duplicate detection",
                    "conflict detection", "import plan", "retry manifest", "batch import",
                    "\u532f\u5165", "\u6279\u6b21\u532f\u5165", "\u8cc7\u6599\u532f\u5165",
                    "XQ\u532f\u5165", "\u91cd\u8907\u8cc7\u6599", "\u885d\u7a81\u8cc7\u6599",
                ],
                aliases=["import", "data-import", "batch-import", "onboarding"],
                related_cli_commands=[
                    "import-discover", "import-preview", "import-validate", "import-plan",
                    "import-batch", "import-retry-manifest", "import-onboarding-health",
                    "import-onboarding-report", "import-xq-export",
                ],
                report_types=["data_import_onboarding_report"],
                maturity="STABLE",
                default_visible=True,
                favorite_default=False,
                no_real_orders=True,
                read_only=True,
                production_blocked=True,
                notes="Added in v1.1.1 — Data Import UX & Batch Onboarding.",
            ),
            # ----------------------------------------------------------------
            # v1.1.2 Coverage Repair Workflow
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="coverage_repair",
                tab_name="coverage_repair",
                display_name="Coverage Repair Workflow",
                group="data",
                priority="P1",
                description=(
                    "Coverage Repair Workflow v1.1.2 — detect missing/partial/stale/duplicate/"
                    "conflict/invalid coverage issues, build prioritized repair tasks, dry-run "
                    "repair planning, safe deduplication & schema normalization, manual conflict "
                    "review, before/after validation. "
                    "Research Only. No Real Orders. dry_run=True default."
                ),
                module_path="gui.coverage_repair_panel",
                class_name="CoverageRepairPanel",
                available_flag="_COVERAGE_REPAIR_AVAILABLE",
                keywords=[
                    "coverage repair", "repair workflow", "missing data", "partial data",
                    "stale data", "conflict data", "duplicate repair", "source required",
                    "coverage task", "repair plan", "repair task", "safe repair",
                    "\u8986\u84cb\u4fee\u5fa9", "\u7f3a\u8cc7\u6599", "\u8cc7\u6599\u4e0d\u8db3",
                    "\u904e\u671f\u8cc7\u6599", "\u885d\u7a81\u8cc7\u6599",
                    "\u4fee\u5fa9\u4efb\u52d9", "\u88dc\u8cc7\u6599",
                ],
                aliases=["coverage-repair", "repair", "data-repair"],
                related_cli_commands=[
                    "coverage-repair-scan", "coverage-repair-issues", "coverage-repair-tasks",
                    "coverage-repair-plan", "coverage-repair-run", "coverage-repair-result",
                    "coverage-repair-unresolved", "coverage-repair-source-required",
                    "coverage-repair-health", "coverage-repair-report",
                ],
                report_types=["coverage_repair_report"],
                maturity="STABLE",
                default_visible=True,
                favorite_default=False,
                no_real_orders=True,
                read_only=True,
                production_blocked=True,
                notes="Added in v1.1.2 — Coverage Repair Workflow.",
            ),
            # ----------------------------------------------------------------
            # v1.1.0 Data Universe Expansion
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="data_universe",
                tab_name="data_universe",
                display_name="Data Universe Expansion",
                group="data",
                priority="P1",
                description=(
                    "Data Universe Expansion v1.1.0 \u2014 universe tiers, symbol coverage, "
                    "real data validation, missing data tracking, statistical confidence. "
                    "Research Only. No Real Orders. Production Trading BLOCKED."
                ),
                module_path="gui.universe_panel",
                class_name="UniversePanel",
                available_flag="_UNIVERSE_AVAILABLE",
                keywords=[
                    "universe", "data universe", "coverage", "symbols", "stock pool",
                    "sample expansion", "universe health", "universe report",
                    "\u80a1\u7968\u6c60", "\u6a23\u672c\u64f4\u5145", "\u8cc7\u6599\u8986\u84cb",
                    "\u80a1\u7968\u6e05\u55ae", "30\u6a94", "50\u6a94", "100\u6a94",
                    "CORE_10", "RESEARCH_30", "EXPANDED_50", "BROAD_100",
                ],
                aliases=["universe", "data-universe", "universe-expansion"],
                related_cli_commands=[
                    "universe-build", "universe-summary", "universe-health",
                    "universe-coverage", "universe-symbol", "universe-missing", "universe-report",
                ],
                report_types=["data_universe_expansion_report"],
                maturity="STABLE",
                default_visible=True,
                favorite_default=False,
                no_real_orders=True,
                read_only=True,
                production_blocked=True,
                notes="Added in v1.1.0 \u2014 Data Universe Expansion.",
            ),
            # ----------------------------------------------------------------
            # v1.0.9 Final Maintenance Rollup
            # ----------------------------------------------------------------
            GUITabMetadata(
                tab_id="final_maintenance_rollup",
                tab_name="final_maintenance_rollup",
                display_name="Final Maintenance Rollup",
                group="maintenance",
                priority="P1",
                description=(
                    "Final Maintenance Rollup v1.0.9 \u2014 v1.0.x release history, final health check, "
                    "long-term maintenance plan, final smoke summary. "
                    "Research Only. No Real Orders. Production Trading BLOCKED."
                ),
                module_path="gui.final_rollup_panel",
                class_name="FinalRollupPanel",
                available_flag="_FINAL_ROLLUP_AVAILABLE",
                keywords=[
                    "final rollup", "maintenance rollup", "v1.0 summary", "release summary",
                    "maintenance plan", "smoke summary", "final check",
                    "\u6700\u7d42\u5f59\u6574", "\u7dad\u8b77\u7e3d\u7d50", "\u7248\u672c\u7e3d\u7d50", "\u9577\u671f\u7dad\u8b77", "smoke test",
                ],
                aliases=["final-rollup", "maintenance-rollup", "rollup"],
                related_cli_commands=[
                    "final-rollup", "final-rollup-history", "final-rollup-health",
                    "final-rollup-maintenance-plan", "final-rollup-smoke", "final-rollup-report",
                ],
                report_types=["final_maintenance_rollup_report"],
                maturity="STABLE",
                default_visible=True,
                favorite_default=False,
                no_real_orders=True,
                read_only=True,
                production_blocked=True,
                notes="Added in v1.0.9 \u2014 Final Maintenance Rollup.",
            ),
        ]
        for tab in tabs:
            self._tabs[tab.tab_id] = tab

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register(self, tab: GUITabMetadata) -> None:
        """Add (or replace) a tab in the registry."""
        self._tabs[tab.tab_id] = tab

    def list_tabs(
        self,
        group: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> List[GUITabMetadata]:
        """Return list of matching tabs."""
        tabs = list(self._tabs.values())
        if group:
            tabs = [t for t in tabs if t.group == group]
        if priority:
            tabs = [t for t in tabs if t.priority == priority]
        return tabs

    def get_tab(self, tab_id: str) -> Optional[GUITabMetadata]:
        """Return a single tab or None."""
        return self._tabs.get(tab_id)

    def search_tabs(self, keyword: str) -> List[GUITabMetadata]:
        """Return tabs matching keyword (case-insensitive) in name/desc/keywords/group/cli."""
        kw = keyword.lower()
        result = []
        for tab in self._tabs.values():
            if (
                kw in tab.tab_id.lower()
                or kw in tab.display_name.lower()
                or kw in tab.description.lower()
                or kw in tab.group.lower()
                or any(kw in k.lower() for k in tab.keywords)
                or any(kw in c.lower() for c in tab.related_cli_commands)
            ):
                result.append(tab)
        return result

    def export_registry(self) -> dict:
        """Return dict summary of the registry."""
        by_group: dict[str, list[str]] = {}
        for tab in self._tabs.values():
            by_group.setdefault(tab.group, []).append(tab.tab_id)
        return {
            "total_tabs":    len(self._tabs),
            "groups_count":  len(by_group),
            "by_group":      by_group,
            "read_only":     self.read_only,
            "no_real_orders": self.no_real_orders,
            "production_blocked": self.production_blocked,
            "real_order_ready":   self.real_order_ready,
        }
