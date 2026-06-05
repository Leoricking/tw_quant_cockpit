"""stable_release/capability_matrix.py — StableCapabilityMatrix for v0.6.0.

Lists all 30+ stable capabilities across the TW Quant Cockpit research platform.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

from stable_release.stable_release_schema import StableCapability

logger = logging.getLogger(__name__)


class StableCapabilityMatrix:
    """Builds and summarizes the v0.6.0 stable capability matrix.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    VERSION = "v0.6.0"

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self) -> None:
        self._capabilities: List[StableCapability] = []

    def build(self) -> "StableCapabilityMatrix":
        """Build the full capability list."""
        self._capabilities = [
            # ------------------------------------------------------------------
            # Data / Provider Capabilities
            # ------------------------------------------------------------------
            StableCapability(
                capability_id="data_quality_gate",
                name="Data Quality Gate",
                category="data",
                version_added="v0.3.20",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["data-quality-gate", "dq"],
                gui_tabs=["Data Quality Gate"],
                reports=["data_quality"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["Manual threshold tuning required"],
            ),
            StableCapability(
                capability_id="provider_health",
                name="Provider Health",
                category="provider",
                version_added="v0.4.1",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["api-fetch-status"],
                gui_tabs=["Provider Health", "API Fetch Status"],
                reports=["provider"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="provider_reliability",
                name="Provider Reliability",
                category="provider",
                version_added="v0.3.24",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["provider-reliability", "providers"],
                gui_tabs=["Provider Reliability"],
                reports=["provider"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["No real-time streaming; TWSE/TPEX only"],
            ),
            StableCapability(
                capability_id="api_fetch_diagnostics",
                name="API Fetch Diagnostics",
                category="provider",
                version_added="v0.4.1",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["api-fetch-status", "data-provider-fetch"],
                gui_tabs=["API Fetch Status", "Data Provider Fetch"],
                reports=["provider"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="data_stabilization",
                name="Data Stabilization",
                category="data",
                version_added="v0.5.5",
                status="STABLE",
                maturity="STABLE",
                cli_commands=[
                    "data-stabilization", "data-stabilization-report",
                    "data-stabilization-summary", "data-lineage",
                    "feature-readiness", "feature-store-health",
                ],
                gui_tabs=["Data Stabilization"],
                reports=["data_stabilization"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["Schema lineage tracking is append-only"],
            ),
            StableCapability(
                capability_id="feature_store_health",
                name="Feature Store Health",
                category="data",
                version_added="v0.5.5",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["feature-store-health", "feature-readiness"],
                gui_tabs=["Data Stabilization"],
                reports=["data_stabilization"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="leakage_guard",
                name="Leakage Guard",
                category="data",
                version_added="v0.5.5",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["leakage-guard"],
                gui_tabs=["Data Stabilization"],
                reports=["data_stabilization"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["Leakage detection is heuristic-based, not exhaustive"],
            ),
            # ------------------------------------------------------------------
            # Strategy Capabilities
            # ------------------------------------------------------------------
            StableCapability(
                capability_id="strategy_filter_pack",
                name="Strategy Filter Pack",
                category="strategy",
                version_added="v0.5.1.1",
                status="USABLE",
                maturity="EXPERIMENTAL",
                cli_commands=["strategy-filter", "strategy-filter-pack"],
                gui_tabs=["Strategy Filter"],
                reports=["strategy_filter"],
                regression_coverage=False,
                safety_status="OK",
                known_limitations=["Filter criteria are manually defined; no ML weighting"],
            ),
            StableCapability(
                capability_id="strategy_knowledge_ingestion",
                name="Strategy Knowledge Ingestion",
                category="strategy",
                version_added="v0.4.1.1",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["strategy-knowledge-ingest", "strategy-knowledge-summary"],
                gui_tabs=["Strategy Knowledge"],
                reports=[],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["Requires manual transcript input"],
            ),
            StableCapability(
                capability_id="rule_governance",
                name="Rule Governance",
                category="strategy",
                version_added="v0.3.28",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["rule-governance", "rules"],
                gui_tabs=["Rule Governance"],
                reports=["rule_governance"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="signal_quality",
                name="Signal Quality",
                category="strategy",
                version_added="v0.3.14",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["signal-quality", "signals"],
                gui_tabs=["Signal Quality"],
                reports=["signal_quality"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="rule_weight_tuning",
                name="Rule Weight Tuning",
                category="strategy",
                version_added="v0.3.15",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["tune-rule-weights"],
                gui_tabs=["Rule Weight Tuning"],
                reports=[],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["No auto-apply of weights; manual review required"],
            ),
            StableCapability(
                capability_id="ml_knowledge_integration",
                name="ML Knowledge Integration",
                category="strategy",
                version_added="v0.4.2.1",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["ml-knowledge-integrate", "ml-knowledge-feature-summary"],
                gui_tabs=["ML Knowledge Integration"],
                reports=[],
                regression_coverage=True,
                safety_status="OK",
            ),
            # ------------------------------------------------------------------
            # Replay / Training Capabilities
            # ------------------------------------------------------------------
            StableCapability(
                capability_id="intraday_replay_cockpit",
                name="Intraday Replay Cockpit",
                category="replay",
                version_added="v0.4.4",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["intraday-replay", "intraday-replay-report"],
                gui_tabs=["Intraday Replay"],
                reports=["intraday_replay"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="tw_replay_training_cockpit",
                name="TW Replay Training Cockpit",
                category="replay",
                version_added="v0.5.6",
                status="STABLE",
                maturity="STABLE",
                cli_commands=[
                    "replay-training", "replay-training-summary",
                    "replay-training-next", "replay-training-prev",
                    "replay-training-marker", "replay-ai-review",
                    "replay-training-score", "replay-training-drills",
                    "replay-training-report",
                ],
                gui_tabs=["Replay Training"],
                reports=["replay_training"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["Bar data requires manual CSV import; no live feed"],
            ),
            StableCapability(
                capability_id="ai_replay_review",
                name="AI Replay Review",
                category="replay",
                version_added="v0.5.6",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["replay-ai-review"],
                gui_tabs=["Replay Training"],
                reports=["replay_training"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["Rule-based review only; no GPT/LLM integration"],
            ),
            StableCapability(
                capability_id="replay_score",
                name="Replay Score",
                category="replay",
                version_added="v0.5.6",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["replay-training-score"],
                gui_tabs=["Replay Training"],
                reports=["replay_training"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="replay_drills",
                name="Replay Drills",
                category="replay",
                version_added="v0.5.6",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["replay-training-drills"],
                gui_tabs=["Replay Training"],
                reports=["replay_training"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="replay_training_ui_enhancement",
                name="Replay Training UI Enhancement",
                category="replay",
                version_added="v0.6.3",
                status="STABLE",
                maturity="STABLE",
                cli_commands=[
                    "replay-training", "replay-ai-review",
                    "replay-training-score", "replay-training-drills",
                    "replay-training-report",
                ],
                gui_tabs=["Replay Training"],
                reports=["replay_training"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=[
                    "Table-based chart view; no candlestick drawing",
                    "Bar data requires manual CSV import; no live feed",
                ],
            ),
            # ------------------------------------------------------------------
            # Journal / Review Capabilities
            # ------------------------------------------------------------------
            StableCapability(
                capability_id="portfolio_journal",
                name="Portfolio Journal",
                category="journal",
                version_added="v0.4.6",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["journal-add", "journal-list", "journal-review", "journal"],
                gui_tabs=["Portfolio Journal"],
                reports=["portfolio_journal"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="research_review_dashboard",
                name="Research Review Dashboard",
                category="review",
                version_added="v0.4.7",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["research-review", "research-review-report", "review-daily"],
                gui_tabs=["Research Review"],
                reports=["research_review"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="research_assistant_coach",
                name="Research Assistant / Coach",
                category="coach",
                version_added="v0.4.8",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["research-coach", "research-coach-report", "coach-daily"],
                gui_tabs=["Research Coach"],
                reports=["research_coach"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="research_workflow_automation",
                name="Research Workflow Automation",
                category="workflow",
                version_added="v0.4.9",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["research-workflow", "research-workflow-report", "workflow-daily"],
                gui_tabs=["Research Workflow"],
                reports=["research_workflow"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="notification_center",
                name="Notification Center",
                category="workflow",
                version_added="v0.4.5",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["notification-scan", "notification-list", "notify"],
                gui_tabs=["Notification Center"],
                reports=["notification"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["No external push notifications"],
            ),
            # ------------------------------------------------------------------
            # Report Capabilities
            # ------------------------------------------------------------------
            StableCapability(
                capability_id="auto_report_center",
                name="Auto Report Center",
                category="report",
                version_added="v0.3.16",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["auto-report"],
                gui_tabs=["Auto Report Center"],
                reports=["auto_report"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="report_pack_consolidation",
                name="Report Pack Consolidation",
                category="report",
                version_added="v0.5.4",
                status="STABLE",
                maturity="USABLE",
                cli_commands=["report-pack", "report-pack-summary", "report-pack-report"],
                gui_tabs=["Report Pack"],
                reports=["report_pack_consolidation_report"],
                regression_coverage=True,
                safety_status="OK",
            ),
            # ------------------------------------------------------------------
            # Regression / OS Capabilities
            # ------------------------------------------------------------------
            StableCapability(
                capability_id="regression_suite_consolidation",
                name="Regression Suite Consolidation",
                category="regression",
                version_added="v0.5.3",
                status="STABLE",
                maturity="USABLE",
                cli_commands=["regression-list-suites", "regression-run", "regression-coverage", "regression-report"],
                gui_tabs=["Regression Suite"],
                reports=["regression"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="release_status",
                name="Release Status",
                category="research_os",
                version_added="v0.4.0",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["stable-release-check", "version-info"],
                gui_tabs=["Release Status"],
                reports=["release"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="research_os_planning",
                name="Research OS Planning",
                category="research_os",
                version_added="v0.5.0",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["research-os-audit", "research-os-summary", "research-os-modules", "os"],
                gui_tabs=["Research OS Planning"],
                reports=["research_os"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="cli_ux",
                name="CLI UX",
                category="cli",
                version_added="v0.5.1",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["cli-list", "cli-aliases", "cli-examples", "cli-ux-report"],
                gui_tabs=["CLI UX"],
                reports=["cli_ux"],
                regression_coverage=True,
                safety_status="OK",
            ),
            StableCapability(
                capability_id="gui_navigation",
                name="GUI Navigation",
                category="gui",
                version_added="v0.5.2",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["gui-nav-summary", "gui-nav-tabs", "gui-nav-groups", "gui-nav-report"],
                gui_tabs=["GUI Navigation"],
                reports=["gui_navigation"],
                regression_coverage=True,
                safety_status="OK",
            ),
            # ------------------------------------------------------------------
            # Safety / Simulation Capabilities
            # ------------------------------------------------------------------
            StableCapability(
                capability_id="paper_trading",
                name="Paper Trading",
                category="safety",
                version_added="v0.3.0",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["paper"],
                gui_tabs=["Portfolio Cockpit"],
                reports=[],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["Simulated only — no real broker connection"],
            ),
            StableCapability(
                capability_id="mock_realtime",
                name="Mock Realtime",
                category="safety",
                version_added="v0.3.4",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["mock-realtime"],
                gui_tabs=[],
                reports=[],
                regression_coverage=False,
                safety_status="OK",
                known_limitations=["Uses synthetic tick data only"],
            ),
            StableCapability(
                capability_id="backtest_engine_hardening",
                name="Backtest Engine Hardening",
                category="safety",
                version_added="v0.3.26",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["hardened-backtest"],
                gui_tabs=["Hardened Backtest"],
                reports=[],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["Walk-forward windows are configurable but not auto-tuned"],
            ),
            StableCapability(
                capability_id="portfolio_simulation",
                name="Portfolio Simulation",
                category="safety",
                version_added="v0.3.12",
                status="STABLE",
                maturity="STABLE",
                cli_commands=["portfolio-positions"],
                gui_tabs=["Portfolio Cockpit"],
                reports=[],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["No multi-currency support"],
            ),
            StableCapability(
                capability_id="no_real_orders_safety_layer",
                name="No Real Orders Safety Layer",
                category="safety",
                version_added="v0.1.0",
                status="STABLE",
                maturity="STABLE",
                cli_commands=[],
                gui_tabs=[],
                reports=["safety"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=["System-wide block; cannot be disabled"],
            ),
            StableCapability(
                capability_id="production_trading_blocked",
                name="Production Trading BLOCKED",
                category="safety",
                version_added="v0.1.0",
                status="BLOCKED",
                maturity="STABLE",
                cli_commands=[],
                gui_tabs=[],
                reports=["safety"],
                regression_coverage=True,
                safety_status="BLOCKED",
                known_limitations=["Intentionally blocked for research safety"],
                no_real_orders=True,
                production_blocked=True,
            ),
            # ------------------------------------------------------------------
            # v0.6.2 Data Coverage Expansion
            # ------------------------------------------------------------------
            StableCapability(
                capability_id="data_coverage_expansion",
                name="Data Coverage Expansion",
                category="data",
                version_added="v0.6.2",
                status="STABLE",
                maturity="STABLE",
                cli_commands=[
                    "data-coverage", "data-coverage-summary",
                    "data-coverage-items", "data-coverage-report", "data-coverage-gaps",
                ],
                gui_tabs=["Data Coverage"],
                reports=["data_coverage"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=[
                    "Coverage status is filesystem-scan only; no live API validation",
                    "ENV_LIMITED items require manual token setup",
                ],
            ),
            StableCapability(
                capability_id="research_intelligence_upgrade",
                name="Research Intelligence Upgrade",
                category="research_os",
                version_added="v0.7.0",
                status="STABLE",
                maturity="STABLE",
                cli_commands=[
                    "research-intelligence", "research-intelligence-summary",
                    "research-intelligence-signals", "research-intelligence-recommendations",
                    "research-intelligence-priority", "research-intelligence-daily-plan",
                    "research-intelligence-weekly-plan", "research-intelligence-report",
                ],
                gui_tabs=["Research Intelligence"],
                reports=["research_intelligence"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=[
                    "Signal aggregation depends on availability of CSV outputs from other modules",
                    "Provider-limited signals require environment variable configuration",
                    "No BUY/SELL/ORDER — research actions only",
                ],
            ),
            StableCapability(
                capability_id="intelligence_ux_polish",
                name="Intelligence UX Polish",
                category="research_os",
                version_added="v0.7.1",
                status="STABLE",
                maturity="STABLE",
                cli_commands=[
                    "research-intelligence-summary", "research-intelligence-recommendations",
                    "research-intelligence-priority", "research-intelligence-daily-plan",
                    "research-intelligence-weekly-plan", "research-intelligence-report",
                ],
                gui_tabs=["Research Intelligence"],
                reports=["research_intelligence"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=[
                    "Copy Command button requires PySide6 clipboard support",
                    "Filter dropdowns populate only after Run Intelligence is executed",
                    "No BUY/SELL/ORDER — research actions only",
                ],
            ),
            # v0.7.2 Strategy Research Memory
            StableCapability(
                capability_id="strategy_research_memory",
                name="Strategy Research Memory",
                category="research_os",
                version_added="v0.7.2",
                status="USABLE",
                maturity="STABLE",
                cli_commands=[
                    "strategy-memory", "strategy-memory-summary",
                    "strategy-memory-list", "strategy-memory-search",
                    "strategy-memory-show", "strategy-memory-update-status",
                    "strategy-memory-archive", "strategy-memory-report",
                ],
                gui_tabs=["Strategy Memory"],
                reports=["strategy_memory"],
                regression_coverage=True,
                safety_status="OK",
                known_limitations=[
                    "Memory extraction depends on CSV outputs from other Research OS modules",
                    "No auto-accept/reject — all memory status changes are manual",
                    "Research Only — no trading actions, no real orders",
                ],
                no_real_orders=True,
                production_blocked=True,
            ),
        ]
        return self

    def list_capabilities(self, category: Optional[str] = None) -> List[StableCapability]:
        """Return capabilities, optionally filtered by category."""
        if not self._capabilities:
            self.build()
        if category:
            return [c for c in self._capabilities if c.category == category]
        return list(self._capabilities)

    def summarize(self) -> dict:
        """Return summary counts and status by status/category."""
        caps = self.list_capabilities()
        by_status: dict[str, int] = {}
        by_category: dict[str, int] = {}
        for c in caps:
            by_status[c.status] = by_status.get(c.status, 0) + 1
            by_category[c.category] = by_category.get(c.category, 0) + 1

        total        = len(caps)
        stable_count = by_status.get("STABLE", 0)
        usable_count = by_status.get("USABLE", 0)
        partial_count = by_status.get("PARTIAL", 0)
        experimental_count = by_status.get("EXPERIMENTAL", 0)
        blocked_count = by_status.get("BLOCKED", 0)

        print("=" * 60)
        print("  TW Quant Cockpit — Research OS Stable Release v0.6.0")
        print("  [!] Research Only | No Real Orders | Production BLOCKED")
        print("=" * 60)
        print(f"  Capability Matrix Summary")
        print(f"  Total Capabilities : {total}")
        print(f"  STABLE             : {stable_count}")
        print(f"  USABLE             : {usable_count}")
        print(f"  PARTIAL            : {partial_count}")
        print(f"  EXPERIMENTAL       : {experimental_count}")
        print(f"  BLOCKED            : {blocked_count}")
        print()
        print(f"  By Category:")
        for cat, count in sorted(by_category.items()):
            print(f"    {cat:<20} : {count}")
        print("=" * 60)

        return {
            "version":             self.VERSION,
            "total":               total,
            "stable_count":        stable_count,
            "usable_count":        usable_count,
            "partial_count":       partial_count,
            "experimental_count":  experimental_count,
            "blocked_count":       blocked_count,
            "by_status":           by_status,
            "by_category":         by_category,
            "no_real_orders":      True,
            "production_blocked":  True,
        }
