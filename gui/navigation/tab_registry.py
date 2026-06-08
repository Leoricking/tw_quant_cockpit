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
