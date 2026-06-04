"""regression/coverage_matrix.py — RegressionCoverageMatrix for TW Quant Cockpit v0.5.3.
[!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module catalog — all known modules and their CLI/GUI/Report keys
# ---------------------------------------------------------------------------

_MODULES = [
    {"module": "Data Quality Gate",           "cli_key": "data-quality-gate",           "gui_key": "data_quality_gate",            "report_key": "data_quality_gate"},
    {"module": "Provider Health",             "cli_key": "provider-health",             "gui_key": "provider_health",              "report_key": "provider_health"},
    {"module": "Provider Reliability",        "cli_key": "provider-reliability",        "gui_key": "provider_reliability",         "report_key": "provider_reliability"},
    {"module": "API Fetch Diagnostics",       "cli_key": "api-fetch-diagnostics",       "gui_key": "api_fetch_status",             "report_key": "api_fetch_production"},
    {"module": "Data Freshness",              "cli_key": "data-freshness",              "gui_key": "data_quality_gate",            "report_key": "data_freshness"},
    {"module": "Strategy Filter",             "cli_key": "strategy-filter",             "gui_key": "strategy_filter",              "report_key": "strategy_filter_report"},
    {"module": "Strategy Filter Pack",        "cli_key": "strategy-filter-pack",        "gui_key": "strategy_filter",              "report_key": "strategy_filter_pack"},
    {"module": "Rule Governance",             "cli_key": "rule-governance",             "gui_key": "rule_governance",              "report_key": "rule_governance"},
    {"module": "Signal Quality",              "cli_key": "signal-quality",              "gui_key": "signal_quality",               "report_key": "signal_quality"},
    {"module": "Strategy Knowledge",          "cli_key": "strategy-knowledge-summary",  "gui_key": "strategy_knowledge_ingestion", "report_key": "strategy_knowledge"},
    {"module": "ML Knowledge",                "cli_key": "ml-knowledge-feature-summary","gui_key": "ml_knowledge_integration",     "report_key": "ml_knowledge_integration"},
    {"module": "ML Leakage Check",            "cli_key": "ml-knowledge-leakage-check",  "gui_key": "ml_feature_store",             "report_key": "ml_leakage"},
    {"module": "Intraday Replay",             "cli_key": "intraday-replay",             "gui_key": "intraday_replay",              "report_key": "intraday_replay"},
    {"module": "Intraday Pipeline",           "cli_key": "intraday-pipeline",           "gui_key": "intraday_pipeline",            "report_key": "intraday_pipeline"},
    {"module": "Replay Session",              "cli_key": "replay-session-list",         "gui_key": "intraday_replay",              "report_key": "intraday_replay"},
    {"module": "Research OS",                 "cli_key": "research-os-audit",           "gui_key": "research_os_planning",         "report_key": "research_os_stabilization"},
    {"module": "Research Workflow",           "cli_key": "research-workflow-summary",   "gui_key": "research_workflow",            "report_key": "research_workflow_report"},
    {"module": "Research Coach",              "cli_key": "research-coach-summary",      "gui_key": "research_assistant",           "report_key": "research_assistant_report"},
    {"module": "Research Review",             "cli_key": "research-review-summary",     "gui_key": "research_review_dashboard",    "report_key": "research_review_dashboard"},
    {"module": "Portfolio Journal",           "cli_key": "journal-summary",             "gui_key": "portfolio_journal",            "report_key": "portfolio_journal_report"},
    {"module": "Notification Center",         "cli_key": "notification-list",           "gui_key": "notification_center",          "report_key": "notification_center_report"},
    {"module": "CLI UX",                      "cli_key": "cli-list",                    "gui_key": "cli_ux",                       "report_key": "cli_ux_report"},
    {"module": "GUI Navigation",              "cli_key": "gui-nav-summary",             "gui_key": "gui_navigation",               "report_key": "gui_navigation_report"},
]


class RegressionCoverageMatrix:
    """Builds a coverage matrix for all known modules against the regression suites.

    [!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, registry=None) -> None:
        if registry is None:
            from regression.suite_registry import RegressionSuiteRegistry
            registry = RegressionSuiteRegistry()
        self._registry = registry

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self) -> List[dict]:
        """Build coverage matrix — returns list of coverage dicts."""
        rows: list[dict] = []
        try:
            quick_tests    = self._registry.get_suite("quick")
            data_tests     = self._registry.get_suite("data")
            strategy_tests = self._registry.get_suite("strategy")
            replay_tests   = self._registry.get_suite("replay")
            report_tests   = self._registry.get_suite("report")
            safety_tests   = self._registry.get_suite("safety")
            gui_tests      = self._registry.get_suite("gui")
            ros_tests      = self._registry.get_suite("research_os")

            all_cli_tests     = quick_tests + data_tests + strategy_tests + replay_tests + ros_tests
            all_report_tests  = report_tests
            all_safety_tests  = safety_tests
            all_gui_tests     = gui_tests

            for mod in _MODULES:
                cli_key    = mod["cli_key"]
                gui_key    = mod["gui_key"]
                report_key = mod["report_key"]

                cli_covered    = self._check_covered(all_cli_tests,    cli_key)
                gui_covered    = self._check_gui_covered(all_gui_tests, gui_key)
                report_covered = self._check_covered(all_report_tests, report_key)
                safety_covered = self._check_covered(all_safety_tests, cli_key)
                data_covered   = self._check_covered(data_tests,       cli_key)
                strategy_covered = self._check_covered(strategy_tests, cli_key)
                replay_covered = self._check_covered(replay_tests,     cli_key)

                dimensions = [cli_covered, gui_covered, report_covered, safety_covered,
                              data_covered, strategy_covered, replay_covered]
                score = int(round(sum(1 for d in dimensions if d) / len(dimensions) * 100))

                missing = []
                if not cli_covered:
                    missing.append(f"CLI({cli_key})")
                if not gui_covered:
                    missing.append(f"GUI({gui_key})")
                if not report_covered:
                    missing.append(f"Report({report_key})")
                if not safety_covered:
                    missing.append(f"Safety")

                rows.append({
                    "module":           mod["module"],
                    "cli_covered":      cli_covered,
                    "gui_covered":      gui_covered,
                    "report_covered":   report_covered,
                    "safety_covered":   safety_covered,
                    "data_covered":     data_covered,
                    "strategy_covered": strategy_covered,
                    "replay_covered":   replay_covered,
                    "coverage_score":   score,
                    "missing_tests":    ", ".join(missing) if missing else "",
                    "no_real_orders":   True,
                })
        except Exception as exc:
            logger.warning("RegressionCoverageMatrix.build() error: %s", exc)
        return rows

    def summary_score(self) -> float:
        """Return average coverage score across all modules (0-100)."""
        try:
            rows = self.build()
            if not rows:
                return 0.0
            return round(sum(r["coverage_score"] for r in rows) / len(rows), 1)
        except Exception:
            return 0.0

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _check_covered(self, tests: list, key: str) -> bool:
        """Check if any test command contains the key."""
        try:
            for tc in tests:
                cmd_str = " ".join(tc.command).lower()
                if key.lower() in cmd_str:
                    return True
        except Exception:
            pass
        return False

    def _check_gui_covered(self, tests: list, key: str) -> bool:
        """Check if any GUI test command references the module key."""
        try:
            for tc in tests:
                cmd_str = " ".join(tc.command).lower()
                if key.lower() in cmd_str:
                    return True
        except Exception:
            pass
        return False
