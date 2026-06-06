"""
os_planning/module_inventory.py — ResearchOSModuleInventory (v0.5.0).

Inventories all v0.4.x modules across the TW Quant Cockpit codebase,
classifies them by layer, and exports a feature matrix CSV for OS planning.

[!] OS Planning Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Hardcoded module inventory — all known v0.4.x modules
# ---------------------------------------------------------------------------

_MODULES: list[dict] = [
    # ------------------------------------------------------------------
    # A. Data Layer
    # ------------------------------------------------------------------
    {
        "module_name":        "data_providers",
        "package":            "data.providers",
        "category":           "A. Data Layer",
        "cli_commands":       "download,import-csv,data-provider-fetch",
        "gui_tab":            "Data Provider Fetch",
        "report":             "no",
        "maturity":           "STABLE",
        "known_limitations":  "No real-time streaming; TWSE/TPEX only",
        "next_action":        "Add more provider adapters in v0.5.x",
    },
    {
        "module_name":        "data_quality",
        "package":            "quality",
        "category":           "A. Data Layer",
        "cli_commands":       "data-quality-gate",
        "gui_tab":            "Data Quality Gate",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Threshold tuning is manual",
        "next_action":        "Auto-threshold calibration",
    },
    {
        "module_name":        "data_freshness",
        "package":            "quality",
        "category":           "A. Data Layer",
        "cli_commands":       "data-freshness-check",
        "gui_tab":            "Data Quality Gate",
        "report":             "no",
        "maturity":           "USABLE",
        "known_limitations":  "Embedded in data_quality module; not standalone",
        "next_action":        "Expose as dedicated CLI command",
    },
    {
        "module_name":        "api_fetch",
        "package":            "data.providers",
        "category":           "A. Data Layer",
        "cli_commands":       "api-fetch-status,api-fetch-diagnostics,api-fetch-report",
        "gui_tab":            "API Fetch Status",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Token setup requires manual .env editing",
        "next_action":        "Guided token wizard in GUI",
    },
    {
        "module_name":        "provider_reliability",
        "package":            "data.providers",
        "category":           "A. Data Layer",
        "cli_commands":       "provider-reliability,provider-reliability-report",
        "gui_tab":            "Provider Reliability",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Historical reliability scores require backfill",
        "next_action":        "Auto-backfill on first run",
    },
    {
        "module_name":        "intraday_pipeline",
        "package":            "intraday",
        "category":           "A. Data Layer",
        "cli_commands":       "intraday-pipeline,intraday-pipeline-status",
        "gui_tab":            "Intraday Pipeline",
        "report":             "no",
        "maturity":           "USABLE",
        "known_limitations":  "Only supports CSV intraday import; no live feed",
        "next_action":        "Add live WebSocket ingest scaffold",
    },
    # ------------------------------------------------------------------
    # B. Strategy / Rule Layer
    # ------------------------------------------------------------------
    {
        "module_name":        "strategy_knowledge",
        "package":            "knowledge",
        "category":           "B. Strategy/Rule Layer",
        "cli_commands":       "strategy-knowledge-ingest,strategy-knowledge-list,strategy-knowledge-report",
        "gui_tab":            "Strategy Knowledge",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "NLP extraction is heuristic; no LLM integration",
        "next_action":        "Add LLM-assisted extraction scaffold",
    },
    {
        "module_name":        "rule_governance",
        "package":            "governance",
        "category":           "B. Strategy/Rule Layer",
        "cli_commands":       "rule-governance,rule-list,rule-add,rule-disable",
        "gui_tab":            "Rule Governance",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "No rule version history beyond current file",
        "next_action":        "Add rule versioning / changelog",
    },
    {
        "module_name":        "signal_quality",
        "package":            "analysis",
        "category":           "B. Strategy/Rule Layer",
        "cli_commands":       "signal-quality,signal-quality-report",
        "gui_tab":            "Signal Quality",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Requires backtest data; empty on fresh install",
        "next_action":        "Generate seed data on first run",
    },
    {
        "module_name":        "rule_weight_tuning",
        "package":            "tuning",
        "category":           "B. Strategy/Rule Layer",
        "cli_commands":       "tune-rule-weights,rule-weight-report",
        "gui_tab":            "Rule Weight Tuning",
        "report":             "yes",
        "maturity":           "USABLE",
        "known_limitations":  "Grid search only; no Bayesian optimization",
        "next_action":        "Add Optuna-based tuning scaffold",
    },
    # ------------------------------------------------------------------
    # C. ML / Monitoring Layer
    # ------------------------------------------------------------------
    {
        "module_name":        "ml_feature_store",
        "package":            "ml",
        "category":           "C. ML/Monitoring Layer",
        "cli_commands":       "ml-feature-catalog,ml-feature-snapshot,ml-feature-quality,ml-feature-store-report",
        "gui_tab":            "ML Knowledge Integration",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "No automated feature selection",
        "next_action":        "Add SHAP-based importance pipeline",
    },
    {
        "module_name":        "ml_knowledge_integration",
        "package":            "ml",
        "category":           "C. ML/Monitoring Layer",
        "cli_commands":       "ml-knowledge-catalog,ml-knowledge-readiness,ml-knowledge-bridge,ml-knowledge-report",
        "gui_tab":            "ML Knowledge Integration",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "auto_enabled=False; manual activation only",
        "next_action":        "Add readiness scoring dashboard",
    },
    {
        "module_name":        "model_monitoring",
        "package":            "monitoring",
        "category":           "C. ML/Monitoring Layer",
        "cli_commands":       "model-monitoring,model-monitoring-report,drift-detect",
        "gui_tab":            "ML Knowledge Integration",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Returns INSUFFICIENT_DATA on fresh install",
        "next_action":        "Add demo prediction log seeder",
    },
    # ------------------------------------------------------------------
    # D. Backtest / Simulation Layer
    # ------------------------------------------------------------------
    {
        "module_name":        "hardened_backtest",
        "package":            "backtest",
        "category":           "D. Backtest/Simulation Layer",
        "cli_commands":       "hardened-backtest,backtest-report,backtest-summary",
        "gui_tab":            "Hardened Backtest",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Single-symbol only; no multi-leg strategies",
        "next_action":        "Add multi-symbol portfolio backtest mode",
    },
    {
        "module_name":        "portfolio_simulation",
        "package":            "sim",
        "category":           "D. Backtest/Simulation Layer",
        "cli_commands":       "simulate-portfolio,paper,mock-realtime",
        "gui_tab":            "Portfolio Cockpit",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Mock only; no real broker connection",
        "next_action":        "Maintain BLOCKED; improve mock accuracy",
    },
    {
        "module_name":        "intraday_replay",
        "package":            "replay",
        "category":           "D. Backtest/Simulation Layer",
        "cli_commands":       "intraday-replay,replay-session-list,replay-session-export,replay-metrics",
        "gui_tab":            "Intraday Replay",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Requires CSV intraday import first",
        "next_action":        "Add replay speed controls to GUI",
    },
    {
        "module_name":        "replay_training_cockpit",
        "package":            "replay_training",
        "category":           "D. Backtest/Simulation Layer",
        "cli_commands":       (
            "replay-training,replay-training-summary,replay-training-next,"
            "replay-training-prev,replay-training-marker,replay-ai-review,"
            "replay-training-score,replay-training-drills,replay-training-report"
        ),
        "gui_tab":            "Replay Training",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  (
            "AI review is rule-based only (no external LLM). "
            "Hidden future data enforced by default."
        ),
        "next_action":        "Add multi-symbol drill scheduling in v0.6.x",
    },
    {
        "module_name":        "paper_mock_realtime",
        "package":            "sim",
        "category":           "D. Backtest/Simulation Layer",
        "cli_commands":       "paper,mock-realtime",
        "gui_tab":            "Portfolio Cockpit",
        "report":             "no",
        "maturity":           "STABLE",
        "known_limitations":  "No real-time feed; CSV-driven only",
        "next_action":        "Maintain mock; document clearly",
    },
    # ------------------------------------------------------------------
    # E. Research OS Layer
    # ------------------------------------------------------------------
    {
        "module_name":        "stable_release_v060",
        "package":            "stable_release",
        "category":           "E. Research OS Layer",
        "cli_commands":       (
            "stable-v060-check,stable-v060-report,stable-v060-manifest,"
            "stable-v060-capabilities,stable-v060-limitations,stable-v060-summary"
        ),
        "gui_tab":            "Stable Release",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Checklist is point-in-time; must re-run after changes",
        "next_action":        "v0.6.1 UX polish — add chart icons, improve empty states",
    },
    {
        "module_name":        "experiment_registry",
        "package":            "experiments",
        "category":           "E. Research OS Layer",
        "cli_commands":       "exp-list,exp-new,exp-update,exp-close,exp-report",
        "gui_tab":            "Experiment Registry",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "JSON storage only; no DB backend",
        "next_action":        "Add search/filter to GUI panel",
    },
    {
        "module_name":        "notification_center",
        "package":            "notifications",
        "category":           "E. Research OS Layer",
        "cli_commands":       "notification-scan,notification-list,notification-report,notification-clear",
        "gui_tab":            "Notification Center",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "External send permanently disabled",
        "next_action":        "Add notification rule editor in GUI",
    },
    {
        "module_name":        "portfolio_journal",
        "package":            "journal",
        "category":           "E. Research OS Layer",
        "cli_commands":       "journal-add,journal-list,journal-export,journal-analytics,journal-report",
        "gui_tab":            "Portfolio Journal",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "No rich-text entry; plain text only",
        "next_action":        "Add structured entry templates",
    },
    {
        "module_name":        "research_review_dashboard",
        "package":            "review",
        "category":           "E. Research OS Layer",
        "cli_commands":       "research-review,research-review-summary,research-review-report",
        "gui_tab":            "Research Review",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Aggregation is pull-based; no push triggers",
        "next_action":        "Add scheduled daily aggregation cron",
    },
    {
        "module_name":        "research_assistant_coach",
        "package":            "coach",
        "category":           "E. Research OS Layer",
        "cli_commands":       "research-coach,research-coach-summary,research-coach-report",
        "gui_tab":            "Research Coach",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Recommendations are heuristic; no LLM",
        "next_action":        "Add LLM suggestion scaffold for v0.6.x",
    },
    {
        "module_name":        "research_workflow_automation",
        "package":            "workflow_automation",
        "category":           "E. Research OS Layer",
        "cli_commands":       "research-workflow,research-workflow-run,research-workflow-summary,research-workflow-report",
        "gui_tab":            "Research Workflow",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Only safe/read-only commands allowed; compound shell blocked",
        "next_action":        "Add workflow template library",
    },
    # ------------------------------------------------------------------
    # F. Report / GUI Layer
    # ------------------------------------------------------------------
    {
        "module_name":        "auto_report_center",
        "package":            "reports",
        "category":           "F. Report/GUI Layer",
        "cli_commands":       "auto-report,stock-report,screener",
        "gui_tab":            "Auto Report Center",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "PDF export not yet implemented",
        "next_action":        "Add PDF export via WeasyPrint scaffold",
    },
    {
        "module_name":        "dashboard_gui",
        "package":            "gui",
        "category":           "F. Report/GUI Layer",
        "cli_commands":       "cockpit,ui",
        "gui_tab":            "All tabs",
        "report":             "no",
        "maturity":           "USABLE",
        "known_limitations":  "Tab count growing; needs grouping in v0.5.0",
        "next_action":        "Implement collapsible tab groups",
    },
    {
        "module_name":        "reports",
        "package":            "reports",
        "category":           "F. Report/GUI Layer",
        "cli_commands":       "auto-report,stock-report",
        "gui_tab":            "Auto Report Center",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  "Markdown only; no HTML/PDF output",
        "next_action":        "Add HTML report renderer",
    },
    {
        "module_name":        "docs",
        "package":            "docs",
        "category":           "F. Report/GUI Layer",
        "cli_commands":       "",
        "gui_tab":            "",
        "report":             "no",
        "maturity":           "EXPERIMENTAL",
        "known_limitations":  "Partially auto-generated; needs manual curation",
        "next_action":        "Generate from docstrings in v0.5.x",
    },
    # v0.5.3
    {
        "module_name":        "regression_suite_consolidation",
        "package":            "regression",
        "category":           "F. QA/Release Layer",
        "cli_commands":       "regression-list-suites,regression-run,regression-coverage,regression-report",
        "gui_tab":            "Regression Suite",
        "report":             "yes",
        "maturity":           "USABLE",
        "known_limitations":  "Coverage matrix based on static analysis; runtime coverage requires prior test run",
        "next_action":        "Add CI integration hook for automatic regression on commit",
    },
    {
        "module_name":        "data_stabilization",
        "package":            "data_stabilization",
        "category":           "A. Data Layer",
        "cli_commands":       "data-stabilization,data-stabilization-report,data-stabilization-summary,data-lineage,feature-readiness,feature-store-health,leakage-guard",
        "gui_tab":            "Data Stabilization",
        "report":             "yes",
        "maturity":           "USABLE",
        "known_limitations":  "Schema validation is static; actual data not loaded — metadata only",
        "next_action":        "Integrate with provider fetch pipeline for auto-refresh on data update",
    },
    # v0.7.2 Strategy Research Memory
    {
        "module_name":        "strategy_research_memory",
        "package":            "strategy_memory",
        "category":           "E. Research OS Layer",
        "cli_commands":       (
            "strategy-memory,strategy-memory-summary,strategy-memory-list,"
            "strategy-memory-search,strategy-memory-show,"
            "strategy-memory-update-status,strategy-memory-archive,strategy-memory-report"
        ),
        "gui_tab":            "Strategy Memory",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  (
            "Extraction is pattern-based (CSV/JSON scan); no NLP/LLM extraction. "
            "Link detection is keyword-heuristic only. "
            "No cross-session memory merge yet."
        ),
        "next_action":        "Add LLM-assisted extraction scaffold in v0.8.x",
    },
    # v0.7.3 Backtest-to-Coach Loop
    {
        "module_name":        "backtest_to_coach_loop",
        "package":            "backtest_coach",
        "category":           "E. Research OS Layer",
        "cli_commands":       (
            "backtest-coach,backtest-coach-summary,backtest-coach-signals,"
            "backtest-coach-tasks,backtest-coach-daily-plan,"
            "backtest-coach-weekly-plan,backtest-coach-report"
        ),
        "gui_tab":            "Backtest Coach",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  (
            "Coach task extraction depends on CSV outputs from other modules. "
            "No BUY/SELL/ORDER — research coach actions only. "
            "Daily plan capped at 7 items; weekly plan capped at 12 items."
        ),
        "next_action":        "Add LLM-assisted task description enrichment in v0.8.x",
    },
    # v0.8.0 Research Intelligence Stable
    {
        "module_name":        "research_intelligence_stable",
        "package":            "intelligence_stable",
        "category":           "E. Research OS Layer",
        "cli_commands":       (
            "intelligence-stable,intelligence-stable-summary,"
            "intelligence-stable-capabilities,intelligence-stable-checks,"
            "intelligence-stable-manifest,intelligence-stable-report"
        ),
        "gui_tab":            "Intelligence Stable",
        "report":             "yes",
        "maturity":           "STABLE",
        "known_limitations":  (
            "Validates Research Intelligence v0.7.0-v0.8.0 capabilities only. "
            "No BUY/SELL/ORDER — research validation only. "
            "Release manifest requires git subprocess (may be limited in CI). "
            "Stable checks may show WARN if some CSV outputs not yet generated."
        ),
        "next_action":        "Add LLM-assisted capability scoring in v0.8.1",
    },
    # v0.8.2 Backtest Training Metrics
    {
        "module_name":        "training_metrics",
        "package":            "training_metrics",
        "category":           "E. Research OS Layer",
        "cli_commands":       (
            "training-metrics,training-metrics-summary,"
            "training-metrics-detail,training-metrics-trend,"
            "training-metrics-report"
        ),
        "gui_tab":            "Training Metrics",
        "report":             "yes",
        "maturity":           "USABLE",
        "known_limitations":  (
            "Metrics collected from CSV outputs only — no live data feed. "
            "INSUFFICIENT_DATA shown when source module not yet run. "
            "Trend direction requires at least 2 historical data points. "
            "No BUY/SELL/ORDER — research metrics only."
        ),
        "next_action":        "Improve trend window and add weekly aggregation in v0.8.3",
    },
]


class ResearchOSModuleInventory:
    """Inventories all v0.4.x modules in TW Quant Cockpit.

    [!] OS Planning Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True
    real_order_ready:   bool = False

    _CATEGORIES = [
        "A. Data Layer",
        "B. Strategy/Rule Layer",
        "C. ML/Monitoring Layer",
        "D. Backtest/Simulation Layer",
        "E. Research OS Layer",
        "F. Report/GUI Layer",
    ]

    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = base_dir or BASE_DIR

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_inventory(self) -> list[dict]:
        """Return the full list of module inventory dicts."""
        try:
            return list(_MODULES)
        except Exception as exc:
            logger.warning("build_inventory error: %s", exc)
            return []

    def scan_packages(self) -> dict:
        """Scan which packages exist on disk under base_dir."""
        packages: dict[str, bool] = {}
        try:
            for mod in _MODULES:
                pkg_root = mod["package"].split(".")[0]
                pkg_path = os.path.join(self.base_dir, pkg_root)
                packages[pkg_root] = os.path.isdir(pkg_path)
        except Exception as exc:
            logger.warning("scan_packages error: %s", exc)
        return packages

    def classify_modules(self) -> list[dict]:
        """Return modules grouped by layer category."""
        try:
            result: list[dict] = []
            for cat in self._CATEGORIES:
                for mod in _MODULES:
                    if mod["category"] == cat:
                        result.append(dict(mod))
            return result
        except Exception as exc:
            logger.warning("classify_modules error: %s", exc)
            return []

    def build_feature_matrix(self) -> dict:
        """Build a feature presence matrix: {category: {feature: present}}."""
        matrix: dict[str, dict[str, bool]] = {}
        try:
            pkg_scan = self.scan_packages()
            for cat in self._CATEGORIES:
                cat_mods = [m for m in _MODULES if m["category"] == cat]
                matrix[cat] = {
                    m["module_name"]: pkg_scan.get(m["package"].split(".")[0], False)
                    for m in cat_mods
                }
        except Exception as exc:
            logger.warning("build_feature_matrix error: %s", exc)
        return matrix

    def export_inventory(self, output_dir: str) -> str:
        """Write module_inventory.csv to output_dir. Returns path."""
        fieldnames = [
            "module_name", "package", "category", "cli_commands",
            "gui_tab", "report", "maturity", "known_limitations", "next_action",
        ]
        try:
            os.makedirs(output_dir, exist_ok=True)
            today = datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(output_dir, f"module_inventory_{today}.csv")
            rows = self.classify_modules()
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.info("module_inventory CSV saved: %s", path)
            return path
        except Exception as exc:
            logger.warning("export_inventory error: %s", exc)
            fallback = os.path.join(output_dir or ".", "module_inventory_error.csv")
            return fallback
