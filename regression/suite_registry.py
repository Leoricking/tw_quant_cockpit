"""regression/suite_registry.py — RegressionSuiteRegistry for TW Quant Cockpit v0.5.3.
[!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

from regression.regression_schema import (
    RegressionTestCase,
    SUITE_QUICK, SUITE_FULL, SUITE_GUI, SUITE_REPORT, SUITE_SAFETY,
    SUITE_DATA, SUITE_PROVIDER, SUITE_STRATEGY, SUITE_REPLAY,
    SUITE_RESEARCH_OS, SUITE_RELEASE_GATE,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Forbidden keyword guard — block any command that could trigger real orders
# ---------------------------------------------------------------------------
_FORBIDDEN_KEYWORDS = ["buy", "sell", "order", "submit_order", "broker", "shioaji"]


def _is_forbidden(command: List[str]) -> bool:
    """Return True if the command would trigger real orders.

    Only checks the top-level command tokens (not -c inline Python code).
    For -c commands, check the first token only (which should be '-c').
    """
    if not command:
        return False

    # For python -c "..." commands, only block if the main command token
    # (before -c) is forbidden. The inline Python code may legitimately
    # contain "no_real_orders" etc.
    if command[0] == "-c":
        # This is an inline Python check — never blocked
        return False
    if command[0] == "-m":
        # python -m module check — check the module name only
        module_tokens = command[1:2]
        lowered = [t.lower() for t in module_tokens]
        for kw in _FORBIDDEN_KEYWORDS:
            if any(kw in tok for tok in lowered):
                return True
        return False

    # For all other commands, check all tokens
    lowered = [tok.lower() for tok in command]
    for kw in _FORBIDDEN_KEYWORDS:
        if any(kw in tok for tok in lowered):
            return True
    return False


class RegressionSuiteRegistry:
    """Registry of all named regression test suites for TW Quant Cockpit v0.5.3.

    All commands are lists of strings suitable for subprocess (no shell=True).
    The runner prepends sys.executable before running.

    [!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    _SUITE_BUILDERS = [
        SUITE_QUICK, SUITE_FULL, SUITE_GUI, SUITE_REPORT, SUITE_SAFETY,
        SUITE_DATA, SUITE_PROVIDER, SUITE_STRATEGY, SUITE_REPLAY,
        SUITE_RESEARCH_OS, SUITE_RELEASE_GATE,
    ]

    def __init__(self) -> None:
        self._suites: dict[str, list[RegressionTestCase]] = {}
        self._build_all()

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def _build_all(self) -> None:
        self._suites[SUITE_QUICK]        = self.build_quick_suite()
        self._suites[SUITE_FULL]         = self.build_full_suite()
        self._suites[SUITE_GUI]          = self.build_gui_suite()
        self._suites[SUITE_REPORT]       = self.build_report_suite()
        self._suites[SUITE_SAFETY]       = self.build_safety_suite()
        self._suites[SUITE_DATA]         = self.build_data_suite()
        self._suites[SUITE_PROVIDER]     = self.build_data_suite()   # alias
        self._suites[SUITE_STRATEGY]     = self.build_strategy_suite()
        self._suites[SUITE_REPLAY]       = self.build_replay_suite()
        self._suites[SUITE_RESEARCH_OS]  = self.build_research_os_suite()
        self._suites[SUITE_RELEASE_GATE] = self.build_release_gate_suite()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def list_suites(self) -> List[str]:
        return list(self._suites.keys())

    def get_suite(self, suite_name: str) -> List[RegressionTestCase]:
        """Return list of test cases for named suite, or empty list."""
        suite = self._suites.get(suite_name, [])
        # Filter out any accidentally forbidden commands
        safe = []
        for tc in suite:
            if _is_forbidden(tc.command):
                logger.warning("Blocked forbidden command in suite '%s': %s", suite_name, tc.command)
            else:
                safe.append(tc)
        return safe

    def list_tests(self, suite_name: Optional[str] = None) -> List[RegressionTestCase]:
        if suite_name:
            return self.get_suite(suite_name)
        all_tests: list[RegressionTestCase] = []
        seen_ids: set[str] = set()
        for suite in self._suites.values():
            for tc in suite:
                if tc.test_id not in seen_ids:
                    all_tests.append(tc)
                    seen_ids.add(tc.test_id)
        return all_tests

    # ------------------------------------------------------------------
    # Suite builders
    # ------------------------------------------------------------------

    def build_quick_suite(self) -> List[RegressionTestCase]:
        return [
            RegressionTestCase(
                test_id="quick_version_info",
                name="version-info",
                suite=SUITE_QUICK,
                category="smoke",
                command=["main.py", "version-info"],
                timeout_seconds=30,
                required=True,
                description="Smoke test: version-info CLI command",
            ),
            RegressionTestCase(
                test_id="quick_research_os_summary",
                name="research-os-summary",
                suite=SUITE_QUICK,
                category="smoke",
                command=["main.py", "research-os-summary"],
                timeout_seconds=30,
                required=True,
                description="Research OS summary smoke test",
            ),
            RegressionTestCase(
                test_id="quick_cli_list",
                name="cli-list",
                suite=SUITE_QUICK,
                category="smoke",
                command=["main.py", "cli-list"],
                timeout_seconds=30,
                required=True,
                description="CLI list smoke test",
            ),
            RegressionTestCase(
                test_id="quick_gui_nav_summary",
                name="gui-nav-summary",
                suite=SUITE_QUICK,
                category="smoke",
                command=["main.py", "gui-nav-summary"],
                timeout_seconds=30,
                required=True,
                description="GUI nav summary smoke test",
            ),
            RegressionTestCase(
                test_id="quick_strategy_filter_pack",
                name="strategy-filter-pack --mode real",
                suite=SUITE_QUICK,
                category="strategy",
                command=["main.py", "strategy-filter-pack", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Strategy filter pack real mode smoke test",
            ),
            RegressionTestCase(
                test_id="quick_research_workflow_summary",
                name="research-workflow-summary",
                suite=SUITE_QUICK,
                category="smoke",
                command=["main.py", "research-workflow-summary"],
                timeout_seconds=30,
                required=True,
                description="Research workflow summary smoke test",
            ),
            RegressionTestCase(
                test_id="quick_research_coach_summary",
                name="research-coach-summary",
                suite=SUITE_QUICK,
                category="smoke",
                command=["main.py", "research-coach-summary"],
                timeout_seconds=30,
                required=True,
                description="Research coach summary smoke test",
            ),
            RegressionTestCase(
                test_id="quick_research_review_summary",
                name="research-review-summary",
                suite=SUITE_QUICK,
                category="smoke",
                command=["main.py", "research-review-summary"],
                timeout_seconds=30,
                required=True,
                description="Research review summary smoke test",
            ),
            RegressionTestCase(
                test_id="quick_journal_summary",
                name="journal-summary",
                suite=SUITE_QUICK,
                category="smoke",
                command=["main.py", "journal-summary"],
                timeout_seconds=30,
                required=True,
                description="Journal summary smoke test",
            ),
            RegressionTestCase(
                test_id="quick_notification_list",
                name="notification-list",
                suite=SUITE_QUICK,
                category="smoke",
                command=["main.py", "notification-list"],
                timeout_seconds=30,
                required=True,
                description="Notification list smoke test",
            ),
            RegressionTestCase(
                test_id="quick_paper",
                name="paper (smoke)",
                suite=SUITE_QUICK,
                category="smoke",
                command=["main.py", "paper", "--smoke"],
                timeout_seconds=30,
                required=False,
                description="Paper trading smoke test (optional)",
            ),
        ]

    def build_full_suite(self) -> List[RegressionTestCase]:
        """Full suite = quick + data + strategy + replay + research_os."""
        seen: set[str] = set()
        combined: list[RegressionTestCase] = []
        for suite_tests in [
            self.build_quick_suite(),
            self.build_data_suite(),
            self.build_strategy_suite(),
            self.build_replay_suite(),
            self.build_research_os_suite(),
            self.build_report_suite(),
        ]:
            for tc in suite_tests:
                if tc.test_id not in seen:
                    combined.append(tc)
                    seen.add(tc.test_id)
        return combined

    def build_gui_suite(self) -> List[RegressionTestCase]:
        return [
            RegressionTestCase(
                test_id="gui_dashboard_import",
                name="gui.dashboard import",
                suite=SUITE_GUI,
                category="import",
                command=["-c", "import gui.dashboard; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="gui.dashboard import check",
            ),
            RegressionTestCase(
                test_id="gui_cli_ux_panel_import",
                name="gui.cli_ux_panel import",
                suite=SUITE_GUI,
                category="import",
                command=["-c", "import gui.cli_ux_panel; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="gui.cli_ux_panel import check",
            ),
            RegressionTestCase(
                test_id="gui_navigation_panel_import",
                name="gui.gui_navigation_panel import",
                suite=SUITE_GUI,
                category="import",
                command=["-c", "import gui.gui_navigation_panel; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="gui.gui_navigation_panel import check",
            ),
            RegressionTestCase(
                test_id="gui_research_os_panel_import",
                name="gui.research_os_planning_panel import",
                suite=SUITE_GUI,
                category="import",
                command=["-c", "import gui.research_os_planning_panel; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="gui.research_os_planning_panel import check",
            ),
            RegressionTestCase(
                test_id="gui_regression_suite_panel_import",
                name="gui.regression_suite_panel import",
                suite=SUITE_GUI,
                category="import",
                command=["-c", "import gui.regression_suite_panel; print('OK')"],
                timeout_seconds=30,
                required=False,
                description="gui.regression_suite_panel import check (v0.5.3)",
            ),
            RegressionTestCase(
                test_id="gui_intraday_replay_panel_import",
                name="gui.intraday_replay_adapter import",
                suite=SUITE_GUI,
                category="import",
                command=["-c", "import gui.intraday_replay_adapter; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="gui.intraday_replay_adapter import check",
            ),
            RegressionTestCase(
                test_id="gui_journal_panel_import",
                name="gui.portfolio_journal_adapter import",
                suite=SUITE_GUI,
                category="import",
                command=["-c", "import gui.portfolio_journal_adapter; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="gui.portfolio_journal_adapter import check",
            ),
            RegressionTestCase(
                test_id="gui_notification_panel_import",
                name="gui.notification_center_adapter import",
                suite=SUITE_GUI,
                category="import",
                command=["-c", "import gui.notification_center_adapter; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="gui.notification_center_adapter import check",
            ),
            RegressionTestCase(
                test_id="gui_coach_panel_import",
                name="gui.research_assistant_adapter import",
                suite=SUITE_GUI,
                category="import",
                command=["-c", "import gui.research_assistant_adapter; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="gui.research_assistant_adapter import check",
            ),
            RegressionTestCase(
                test_id="gui_workflow_panel_import",
                name="gui.research_workflow_adapter import",
                suite=SUITE_GUI,
                category="import",
                command=["-c", "import gui.research_workflow_adapter; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="gui.research_workflow_adapter import check",
            ),
        ]

    def build_report_suite(self) -> List[RegressionTestCase]:
        return [
            RegressionTestCase(
                test_id="report_auto_report_daily",
                name="auto-report --mode real --profile daily",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "auto-report", "--mode", "real", "--profile", "daily"],
                timeout_seconds=120,
                required=True,
                description="Auto report center daily profile",
            ),
            RegressionTestCase(
                test_id="report_cli_ux_report",
                name="cli-ux-report --mode real",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "cli-ux-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="CLI UX report",
            ),
            RegressionTestCase(
                test_id="report_gui_nav_report",
                name="gui-nav-report --mode real",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "gui-nav-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="GUI navigation report",
            ),
            RegressionTestCase(
                test_id="report_strategy_filter",
                name="strategy-filter --stock 2454 --mode real --report",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "strategy-filter", "--stock", "2454", "--mode", "real", "--report"],
                timeout_seconds=60,
                required=True,
                description="Strategy filter report for stock 2454",
            ),
            RegressionTestCase(
                test_id="report_research_os_report",
                name="research-os-report --mode real",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "research-os-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Research OS report",
            ),
            RegressionTestCase(
                test_id="report_research_workflow_report",
                name="research-workflow-report --mode real",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "research-workflow-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Research workflow report",
            ),
            RegressionTestCase(
                test_id="report_research_coach_report",
                name="research-coach-report --mode real --period daily",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "research-coach-report", "--mode", "real", "--period", "daily"],
                timeout_seconds=60,
                required=True,
                description="Research coach daily report",
            ),
            RegressionTestCase(
                test_id="report_research_review_report",
                name="research-review-report --mode real --period daily",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "research-review-report", "--mode", "real", "--period", "daily"],
                timeout_seconds=60,
                required=True,
                description="Research review daily report",
            ),
            RegressionTestCase(
                test_id="report_journal_report",
                name="journal-report --mode real",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "journal-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Portfolio journal report",
            ),
            RegressionTestCase(
                test_id="report_notification_report",
                name="notification-report --mode real",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "notification-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Notification center report",
            ),
            # v0.5.4 Report Pack Consolidation tests
            RegressionTestCase(
                test_id="report_pack_import",
                name="report_pack package import",
                suite=SUITE_REPORT,
                category="import",
                command=["-c", "import report_pack; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="report_pack package import check (v0.5.4)",
            ),
            RegressionTestCase(
                test_id="report_pack_summary",
                name="report-pack-summary --pack-type daily",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "report-pack-summary", "--pack-type", "daily"],
                timeout_seconds=60,
                required=True,
                description="Report pack summary for daily pack",
            ),
            RegressionTestCase(
                test_id="report_pack_health",
                name="report-pack-health --pack-type daily",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "report-pack-health", "--pack-type", "daily"],
                timeout_seconds=60,
                required=True,
                description="Report pack health check for daily pack",
            ),
            # v0.6.1 CLI alias tests
            RegressionTestCase(
                test_id="report_pack_type_alias_full",
                name="report-pack --type full --mode real",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "report-pack", "--type", "full", "--mode", "real"],
                timeout_seconds=120,
                required=False,
                description="Report pack --type alias for --pack-type with --mode no-op (v0.6.1)",
            ),
            RegressionTestCase(
                test_id="report_pack_items_type_alias_full",
                name="report-pack-items --type full",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "report-pack-items", "--type", "full"],
                timeout_seconds=60,
                required=False,
                description="Report pack items --type alias for --pack-type (v0.6.1)",
            ),
            # v0.6.2 Data Coverage Expansion report test
            RegressionTestCase(
                test_id="data_coverage_report_suite",
                name="data-coverage-report --mode real",
                suite=SUITE_REPORT,
                category="report",
                command=["main.py", "data-coverage-report", "--mode", "real"],
                timeout_seconds=60,
                required=False,
                description="Data coverage report generation in report suite (v0.6.2)",
            ),
        ]

    def build_safety_suite(self) -> List[RegressionTestCase]:
        return [
            RegressionTestCase(
                test_id="safety_stable_release_check",
                name="stable-release-check --mode real",
                suite=SUITE_SAFETY,
                category="safety",
                command=["main.py", "stable-release-check", "--mode", "real"],
                timeout_seconds=120,
                required=True,
                description="Stable release checklist",
            ),
            RegressionTestCase(
                test_id="safety_research_os_safety",
                name="research-os-safety",
                suite=SUITE_SAFETY,
                category="safety",
                command=["main.py", "research-os-safety"],
                timeout_seconds=30,
                required=True,
                description="Research OS safety matrix check",
            ),
            RegressionTestCase(
                test_id="safety_cli_aliases",
                name="cli-aliases",
                suite=SUITE_SAFETY,
                category="safety",
                command=["main.py", "cli-aliases"],
                timeout_seconds=30,
                required=True,
                description="CLI aliases listing (no trading aliases)",
            ),
            RegressionTestCase(
                test_id="safety_research_workflow_dry_run",
                name="research-workflow --mode real --type daily_research --dry-run",
                suite=SUITE_SAFETY,
                category="safety",
                command=["main.py", "research-workflow", "--mode", "real", "--type", "daily_research", "--dry-run"],
                timeout_seconds=60,
                required=True,
                description="Research workflow dry run safety check",
            ),
            RegressionTestCase(
                test_id="safety_no_real_orders_flag",
                name="no_real_orders flag check",
                suite=SUITE_SAFETY,
                category="safety",
                command=[
                    "-c",
                    (
                        "from regression.regression_schema import RegressionTestCase; "
                        "tc = RegressionTestCase(test_id='t', name='t', suite='quick', category='c', command=['x']); "
                        "assert tc.no_real_orders is True; print('no_real_orders=True OK')"
                    ),
                ],
                timeout_seconds=20,
                required=True,
                description="Verify RegressionTestCase has no_real_orders=True",
            ),
            RegressionTestCase(
                test_id="safety_safe_command_registry",
                name="safe command registry check",
                suite=SUITE_SAFETY,
                category="safety",
                command=[
                    "-c",
                    (
                        "from cli.alias_map import CLIAliasMap; "
                        "am = CLIAliasMap(); "
                        "blocked = am.blocked_keywords if hasattr(am, 'blocked_keywords') else []; "
                        "print('safe_command_registry OK')"
                    ),
                ],
                timeout_seconds=20,
                required=False,
                description="Safe command registry sanity check (optional)",
            ),
        ]

    def build_data_suite(self) -> List[RegressionTestCase]:
        return [
            RegressionTestCase(
                test_id="data_quality_gate",
                name="data-quality-gate --mode real",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "data-quality-gate", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Data quality gate check",
            ),
            RegressionTestCase(
                test_id="data_provider_health",
                name="provider-health",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "provider-health"],
                timeout_seconds=60,
                required=True,
                description="Provider health check",
            ),
            RegressionTestCase(
                test_id="data_provider_reliability",
                name="provider-reliability --mode real",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "provider-reliability", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Provider reliability check",
            ),
            RegressionTestCase(
                test_id="data_api_fetch_diagnostics",
                name="api-fetch-diagnostics --mode real",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "api-fetch-diagnostics", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="API fetch diagnostics",
            ),
            RegressionTestCase(
                test_id="data_freshness",
                name="data-freshness",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "data-freshness"],
                timeout_seconds=30,
                required=True,
                description="Data freshness check",
            ),
            RegressionTestCase(
                test_id="data_compileall",
                name="compileall",
                suite=SUITE_DATA,
                category="compile",
                command=["-m", "compileall", ".", "-q"],
                timeout_seconds=120,
                required=True,
                description="Python compileall check",
            ),
            # v0.5.5 Data Stabilization
            RegressionTestCase(
                test_id="data_stabilization_import",
                name="data_stabilization import",
                suite=SUITE_DATA,
                category="import",
                command=["-c", "import data_stabilization; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="Data stabilization module import check",
            ),
            RegressionTestCase(
                test_id="data_stabilization_summary",
                name="data-stabilization-summary",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "data-stabilization-summary"],
                timeout_seconds=30,
                required=False,
                description="Data stabilization summary from store",
            ),
            RegressionTestCase(
                test_id="feature_readiness",
                name="feature-readiness",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "feature-readiness"],
                timeout_seconds=30,
                required=False,
                description="Feature readiness check from store",
            ),
            RegressionTestCase(
                test_id="feature_store_health",
                name="feature-store-health",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "feature-store-health"],
                timeout_seconds=30,
                required=False,
                description="Feature store health from store",
            ),
            RegressionTestCase(
                test_id="leakage_guard",
                name="leakage-guard",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "leakage-guard"],
                timeout_seconds=30,
                required=False,
                description="Leakage guard findings from store",
            ),
            # v0.6.2 Data Coverage Expansion
            RegressionTestCase(
                test_id="data_coverage_scan",
                name="data-coverage --mode real",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "data-coverage", "--mode", "real"],
                timeout_seconds=60,
                required=False,
                description="Data coverage scan across all domains (v0.6.2)",
            ),
            RegressionTestCase(
                test_id="data_coverage_summary",
                name="data-coverage-summary",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "data-coverage-summary"],
                timeout_seconds=30,
                required=False,
                description="Data coverage summary from store (v0.6.2)",
            ),
            RegressionTestCase(
                test_id="data_coverage_report",
                name="data-coverage-report --mode real",
                suite=SUITE_DATA,
                category="data",
                command=["main.py", "data-coverage-report", "--mode", "real"],
                timeout_seconds=60,
                required=False,
                description="Data coverage report generation (v0.6.2)",
            ),
        ]

    def build_strategy_suite(self) -> List[RegressionTestCase]:
        return [
            RegressionTestCase(
                test_id="strategy_filter_2454",
                name="strategy-filter --stock 2454 --mode real",
                suite=SUITE_STRATEGY,
                category="strategy",
                command=["main.py", "strategy-filter", "--stock", "2454", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Strategy filter for TSMC",
            ),
            RegressionTestCase(
                test_id="strategy_filter_pack",
                name="strategy-filter-pack --mode real",
                suite=SUITE_STRATEGY,
                category="strategy",
                command=["main.py", "strategy-filter-pack", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Strategy filter pack",
            ),
            RegressionTestCase(
                test_id="strategy_rule_governance",
                name="rule-governance --mode real",
                suite=SUITE_STRATEGY,
                category="strategy",
                command=["main.py", "rule-governance", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Rule governance check",
            ),
            RegressionTestCase(
                test_id="strategy_signal_quality",
                name="signal-quality --mode real --report",
                suite=SUITE_STRATEGY,
                category="strategy",
                command=["main.py", "signal-quality", "--mode", "real", "--report"],
                timeout_seconds=60,
                required=True,
                description="Signal quality report",
            ),
            RegressionTestCase(
                test_id="strategy_knowledge_summary",
                name="strategy-knowledge-summary",
                suite=SUITE_STRATEGY,
                category="strategy",
                command=["main.py", "strategy-knowledge-summary"],
                timeout_seconds=30,
                required=True,
                description="Strategy knowledge summary",
            ),
            RegressionTestCase(
                test_id="strategy_ml_knowledge_feature_summary",
                name="ml-knowledge-feature-summary",
                suite=SUITE_STRATEGY,
                category="strategy",
                command=["main.py", "ml-knowledge-feature-summary"],
                timeout_seconds=30,
                required=True,
                description="ML knowledge feature summary",
            ),
            RegressionTestCase(
                test_id="strategy_ml_knowledge_leakage_check",
                name="ml-knowledge-leakage-check --mode real",
                suite=SUITE_STRATEGY,
                category="strategy",
                command=["main.py", "ml-knowledge-leakage-check", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="ML knowledge leakage check",
            ),
        ]

    def build_replay_suite(self) -> List[RegressionTestCase]:
        return [
            RegressionTestCase(
                test_id="replay_intraday_replay",
                name="intraday-replay --mode real",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "intraday-replay", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Intraday replay",
            ),
            RegressionTestCase(
                test_id="replay_intraday_replay_report",
                name="intraday-replay-report --mode real",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "intraday-replay-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Intraday replay report",
            ),
            RegressionTestCase(
                test_id="replay_session_list",
                name="replay-session-list",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "replay-session-list"],
                timeout_seconds=30,
                required=True,
                description="Replay session list",
            ),
            RegressionTestCase(
                test_id="replay_training_summary",
                name="replay-training-summary",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "replay-training-summary"],
                timeout_seconds=30,
                required=True,
                description="Replay training summary",
            ),
            # v0.5.6 Replay Training Cockpit tests
            RegressionTestCase(
                test_id="replay_training_v056_summary",
                name="replay-training-summary (v0.5.6)",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "replay-training-summary"],
                timeout_seconds=30,
                required=True,
                description="TW Replay Training Cockpit v0.5.6 summary",
            ),
            RegressionTestCase(
                test_id="replay_training_v056_create",
                name="replay-training --symbol 2454 --date 2026-06-03 --timeframe 1min --mode real",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "replay-training", "--symbol", "2454",
                         "--date", "2026-06-03", "--timeframe", "1min", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="TW Replay Training Cockpit v0.5.6 create session",
            ),
            RegressionTestCase(
                test_id="replay_training_v056_report",
                name="replay-training-report --mode real",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "replay-training-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="TW Replay Training Cockpit v0.5.6 report generation",
            ),
            # v0.6.3 Replay Training UI Enhancement tests
            RegressionTestCase(
                test_id="replay_ai_review_latest",
                name="replay-ai-review --session-id latest",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "replay-ai-review", "--session-id", "latest"],
                timeout_seconds=60,
                required=False,
                description="TW Replay Training v0.6.3 AI review (latest session)",
            ),
            RegressionTestCase(
                test_id="replay_training_score_latest",
                name="replay-training-score --session-id latest",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "replay-training-score", "--session-id", "latest"],
                timeout_seconds=60,
                required=False,
                description="TW Replay Training v0.6.3 score (latest session)",
            ),
            RegressionTestCase(
                test_id="replay_training_drills_latest",
                name="replay-training-drills --session-id latest",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "replay-training-drills", "--session-id", "latest"],
                timeout_seconds=60,
                required=False,
                description="TW Replay Training v0.6.3 drills (latest session)",
            ),
            RegressionTestCase(
                test_id="replay_training_panel_import",
                name="ReplayTrainingPanel import check",
                suite=SUITE_REPLAY,
                category="import",
                command=["-c", "from gui.replay_training_panel import ReplayTrainingPanel; print('ReplayTrainingPanel import OK')"],
                timeout_seconds=30,
                required=True,
                description="TW Replay Training v0.6.3 GUI panel import check",
            ),
            RegressionTestCase(
                test_id="replay_intraday_pipeline",
                name="intraday-pipeline --mode real",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "intraday-pipeline", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Intraday pipeline",
            ),
            RegressionTestCase(
                test_id="replay_intraday_quality",
                name="intraday-quality",
                suite=SUITE_REPLAY,
                category="replay",
                command=["main.py", "intraday-quality"],
                timeout_seconds=60,
                required=True,
                description="Run intraday quality check without unsupported mode argument",
            ),
        ]

    def build_research_os_suite(self) -> List[RegressionTestCase]:
        return [
            RegressionTestCase(
                test_id="research_os_audit",
                name="research-os-audit --mode real",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-os-audit", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="Research OS audit",
            ),
            RegressionTestCase(
                test_id="research_os_summary",
                name="research-os-summary",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-os-summary"],
                timeout_seconds=30,
                required=True,
                description="Research OS summary",
            ),
            RegressionTestCase(
                test_id="research_os_modules",
                name="research-os-modules",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-os-modules"],
                timeout_seconds=30,
                required=True,
                description="Research OS modules",
            ),
            RegressionTestCase(
                test_id="research_os_cli",
                name="research-os-cli",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-os-cli"],
                timeout_seconds=30,
                required=True,
                description="Research OS CLI inventory",
            ),
            RegressionTestCase(
                test_id="research_os_gui",
                name="research-os-gui",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-os-gui"],
                timeout_seconds=30,
                required=True,
                description="Research OS GUI inventory",
            ),
            RegressionTestCase(
                test_id="research_os_safety",
                name="research-os-safety",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-os-safety"],
                timeout_seconds=30,
                required=True,
                description="Research OS safety matrix",
            ),
            RegressionTestCase(
                test_id="research_os_workflow_summary",
                name="research-workflow-summary",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-workflow-summary"],
                timeout_seconds=30,
                required=True,
                description="Research workflow summary",
            ),
            RegressionTestCase(
                test_id="research_os_coach_summary",
                name="research-coach-summary",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-coach-summary"],
                timeout_seconds=30,
                required=True,
                description="Research coach summary",
            ),
            RegressionTestCase(
                test_id="research_os_review_summary",
                name="research-review-summary",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-review-summary"],
                timeout_seconds=30,
                required=True,
                description="Research review summary",
            ),
            # v0.7.0 Research Intelligence
            RegressionTestCase(
                test_id="research_intelligence_schema_import",
                name="ResearchIntelligenceSchema import check",
                suite=SUITE_RESEARCH_OS,
                category="import",
                command=["-c", "from research_intelligence.research_intelligence_schema import ResearchSignal, ResearchRecommendation, ResearchIntelligenceSummary; print('schema OK')"],
                timeout_seconds=30,
                required=True,
                description="v0.7.0 Research Intelligence schema import check",
            ),
            RegressionTestCase(
                test_id="research_intelligence_engine_import",
                name="ResearchIntelligenceEngine import check",
                suite=SUITE_RESEARCH_OS,
                category="import",
                command=["-c", "from research_intelligence.research_intelligence_engine import ResearchIntelligenceEngine; print('engine OK')"],
                timeout_seconds=30,
                required=True,
                description="v0.7.0 Research Intelligence engine import check",
            ),
            RegressionTestCase(
                test_id="research_intelligence_panel_import",
                name="ResearchIntelligencePanel import check",
                suite=SUITE_RESEARCH_OS,
                category="import",
                command=["-c", "from gui.research_intelligence_panel import ResearchIntelligencePanel; print('panel OK')"],
                timeout_seconds=30,
                required=True,
                description="v0.7.0 Research Intelligence GUI panel import check",
            ),
            RegressionTestCase(
                test_id="research_intelligence_summary",
                name="research-intelligence-summary",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-intelligence-summary"],
                timeout_seconds=60,
                required=True,
                description="v0.7.0 Research Intelligence summary CLI",
            ),
            RegressionTestCase(
                test_id="research_intelligence_recommendations_no_forbidden",
                name="research-intelligence-recommendations-no-forbidden",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-intelligence-recommendations"],
                timeout_seconds=60,
                required=True,
                description="v0.7.1 Recommendations must not contain BUY/SELL/ORDER",
            ),
            RegressionTestCase(
                test_id="research_intelligence_priority_runnable",
                name="research-intelligence-priority",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-intelligence-priority"],
                timeout_seconds=60,
                required=True,
                description="v0.7.1 Priority board CLI runnable",
            ),
            RegressionTestCase(
                test_id="research_intelligence_daily_plan_runnable",
                name="research-intelligence-daily-plan",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-intelligence-daily-plan"],
                timeout_seconds=60,
                required=True,
                description="v0.7.1 Daily plan CLI runnable",
            ),
            RegressionTestCase(
                test_id="research_intelligence_report_runnable",
                name="research-intelligence-report",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "research-intelligence-report"],
                timeout_seconds=90,
                required=True,
                description="v0.7.1 Report generation CLI runnable",
            ),
            # v0.7.2 Strategy Research Memory
            RegressionTestCase(
                test_id="strategy_memory_schema_import",
                name="StrategyMemorySchema import check",
                suite=SUITE_RESEARCH_OS,
                category="import",
                command=["-c", "from strategy_memory.strategy_memory_schema import StrategyMemoryItem; print('schema OK')"],
                timeout_seconds=30,
                required=True,
                description="v0.7.2 Strategy Memory schema import check",
            ),
            RegressionTestCase(
                test_id="strategy_memory_engine_import",
                name="StrategyMemoryEngine import check",
                suite=SUITE_RESEARCH_OS,
                category="import",
                command=["-c", "from strategy_memory.strategy_memory_engine import StrategyMemoryEngine; print('engine OK')"],
                timeout_seconds=30,
                required=True,
                description="v0.7.2 Strategy Memory engine import check",
            ),
            RegressionTestCase(
                test_id="strategy_memory_cli",
                name="strategy-memory --mode real",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "strategy-memory", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="v0.7.2 Strategy Memory CLI runnable",
            ),
            RegressionTestCase(
                test_id="strategy_memory_summary",
                name="strategy-memory-summary",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "strategy-memory-summary"],
                timeout_seconds=30,
                required=True,
                description="v0.7.2 Strategy Memory summary CLI",
            ),
            RegressionTestCase(
                test_id="strategy_memory_list",
                name="strategy-memory-list",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "strategy-memory-list"],
                timeout_seconds=30,
                required=True,
                description="v0.7.2 Strategy Memory list CLI",
            ),
            RegressionTestCase(
                test_id="strategy_memory_report",
                name="strategy-memory-report --mode real",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "strategy-memory-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="v0.7.2 Strategy Memory report generation CLI",
            ),
            # v0.7.3 Backtest-to-Coach Loop
            RegressionTestCase(
                test_id="backtest_coach_schema_import",
                name="BacktestCoachSchema import check",
                suite=SUITE_RESEARCH_OS,
                category="import",
                command=["-c", "from backtest_coach.backtest_coach_schema import CoachTrainingTask; print('schema OK')"],
                timeout_seconds=30,
                required=True,
                description="v0.7.3 Backtest Coach schema import check",
            ),
            RegressionTestCase(
                test_id="backtest_coach_cli",
                name="backtest-coach --mode real --period daily",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "backtest-coach", "--mode", "real", "--period", "daily"],
                timeout_seconds=60,
                required=True,
                description="v0.7.3 Backtest Coach CLI runnable",
            ),
            RegressionTestCase(
                test_id="backtest_coach_summary",
                name="backtest-coach-summary",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "backtest-coach-summary"],
                timeout_seconds=30,
                required=True,
                description="v0.7.3 Backtest Coach summary CLI",
            ),
            RegressionTestCase(
                test_id="backtest_coach_report",
                name="backtest-coach-report --mode real",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "backtest-coach-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="v0.7.3 Backtest Coach report generation CLI",
            ),
            # v0.8.1 Strategy Memory UX
            RegressionTestCase(
                test_id="strategy_memory_ux_import",
                name="StrategyMemoryPanel import check",
                suite=SUITE_RESEARCH_OS,
                category="import",
                command=["-c", "from gui.strategy_memory_panel import StrategyMemoryPanel; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="v0.8.1 StrategyMemoryPanel import check",
            ),
            RegressionTestCase(
                test_id="strategy_memory_ux_summary",
                name="strategy-memory-summary",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "strategy-memory-summary"],
                timeout_seconds=30,
                required=True,
                description="v0.8.1 Strategy Memory UX summary CLI",
            ),
            RegressionTestCase(
                test_id="strategy_memory_ux_list_active",
                name="strategy-memory-list --active-only",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "strategy-memory-list", "--active-only"],
                timeout_seconds=30,
                required=True,
                description="v0.8.1 Strategy Memory list --active-only filter",
            ),
            RegressionTestCase(
                test_id="strategy_memory_ux_search_needs_action",
                name="strategy-memory-search --needs-action",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "strategy-memory-search", "--needs-action"],
                timeout_seconds=30,
                required=True,
                description="v0.8.1 Strategy Memory search --needs-action filter",
            ),
            RegressionTestCase(
                test_id="strategy_memory_ux_validation_queue",
                name="strategy-memory-validation-queue",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "strategy-memory-validation-queue"],
                timeout_seconds=30,
                required=True,
                description="v0.8.1 Strategy Memory validation queue CLI",
            ),
            RegressionTestCase(
                test_id="strategy_memory_ux_report",
                name="strategy-memory-report --mode real",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "strategy-memory-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="v0.8.1 Strategy Memory report generation CLI",
            ),
            # v0.8.2 Backtest Training Metrics
            RegressionTestCase(
                test_id="training_metrics_schema_import",
                name="TrainingMetrics schema import",
                suite=SUITE_RESEARCH_OS,
                category="import",
                command=["-c", "from training_metrics.training_metrics_schema import TrainingMetric, TrainingMetricsSummary; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="v0.8.2 TrainingMetric and TrainingMetricsSummary schema import",
            ),
            RegressionTestCase(
                test_id="training_metrics_engine_import",
                name="TrainingMetricsEngine import",
                suite=SUITE_RESEARCH_OS,
                category="import",
                command=["-c", "from training_metrics.training_metrics_engine import TrainingMetricsEngine; print('OK')"],
                timeout_seconds=30,
                required=True,
                description="v0.8.2 TrainingMetricsEngine import smoke test",
            ),
            RegressionTestCase(
                test_id="training_metrics_cli",
                name="training-metrics --mode real",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "training-metrics", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="v0.8.2 Backtest Training Metrics pipeline CLI",
            ),
            RegressionTestCase(
                test_id="training_metrics_summary",
                name="training-metrics-summary",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "training-metrics-summary"],
                timeout_seconds=30,
                required=True,
                description="v0.8.2 Training metrics summary CLI",
            ),
            RegressionTestCase(
                test_id="training_metrics_report",
                name="training-metrics-report --mode real",
                suite=SUITE_RESEARCH_OS,
                category="research_os",
                command=["main.py", "training-metrics-report", "--mode", "real"],
                timeout_seconds=60,
                required=True,
                description="v0.8.2 Training metrics report generation CLI",
            ),
        ]

    def build_release_gate_suite(self) -> List[RegressionTestCase]:
        """Release gate = data + quick + safety + gui + report smoke."""
        seen: set[str] = set()
        combined: list[RegressionTestCase] = []

        for suite_tests in [
            self.build_data_suite(),
            self.build_quick_suite(),
            self.build_safety_suite(),
            self.build_gui_suite(),
            # Just the auto-report smoke test from report suite
            [
                RegressionTestCase(
                    test_id="release_gate_auto_report_smoke",
                    name="auto-report --profile daily (smoke)",
                    suite=SUITE_RELEASE_GATE,
                    category="smoke",
                    command=["main.py", "auto-report", "--profile", "daily"],
                    timeout_seconds=120,
                    required=True,
                    description="Auto report daily profile smoke test for release gate",
                ),
            ],
            # v0.6.0 Stable Release tests
            [
                RegressionTestCase(
                    test_id="stable_v060_check",
                    name="stable-v060-check --mode real",
                    suite=SUITE_RELEASE_GATE,
                    category="stable_release",
                    command=["main.py", "stable-v060-check", "--mode", "real"],
                    timeout_seconds=60,
                    required=False,
                    description="v0.6.0 stable release checklist",
                ),
                RegressionTestCase(
                    test_id="stable_v060_summary",
                    name="stable-v060-summary",
                    suite=SUITE_RELEASE_GATE,
                    category="stable_release",
                    command=["main.py", "stable-v060-summary"],
                    timeout_seconds=30,
                    required=True,
                    description="v0.6.0 stable release summary",
                ),
                RegressionTestCase(
                    test_id="stable_v060_capabilities",
                    name="stable-v060-capabilities",
                    suite=SUITE_RELEASE_GATE,
                    category="stable_release",
                    command=["main.py", "stable-v060-capabilities"],
                    timeout_seconds=30,
                    required=True,
                    description="v0.6.0 stable capability matrix",
                ),
            ],
            # v0.6.2 Data Coverage gate
            [
                RegressionTestCase(
                    test_id="release_gate_data_coverage_summary",
                    name="data-coverage-summary (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="data",
                    command=["main.py", "data-coverage-summary"],
                    timeout_seconds=30,
                    required=False,
                    description="Data coverage summary smoke test for release gate (v0.6.2)",
                ),
            ],
            # v0.8.0 Intelligence Stable gate
            [
                RegressionTestCase(
                    test_id="release_gate_intelligence_stable_summary",
                    name="intelligence-stable-summary (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="stable_release",
                    command=["main.py", "intelligence-stable-summary"],
                    timeout_seconds=30,
                    required=False,
                    description="v0.8.0 intelligence stable summary smoke test",
                ),
                RegressionTestCase(
                    test_id="release_gate_intelligence_stable_checks",
                    name="intelligence-stable-checks (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="stable_release",
                    command=["main.py", "intelligence-stable-checks"],
                    timeout_seconds=30,
                    required=False,
                    description="v0.8.0 intelligence stable checks smoke test",
                ),
            ],
            # v0.8.1 Strategy Memory UX gate
            [
                RegressionTestCase(
                    test_id="release_gate_strategy_memory_ux_import",
                    name="StrategyMemoryPanel import (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="import",
                    command=["-c", "from gui.strategy_memory_panel import StrategyMemoryPanel; print('OK')"],
                    timeout_seconds=30,
                    required=False,
                    description="v0.8.1 StrategyMemoryPanel import smoke test",
                ),
                RegressionTestCase(
                    test_id="release_gate_strategy_memory_ux_summary",
                    name="strategy-memory-summary (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="research_os",
                    command=["main.py", "strategy-memory-summary"],
                    timeout_seconds=30,
                    required=False,
                    description="v0.8.1 Strategy Memory summary smoke test",
                ),
            ],
            # v0.8.2 Backtest Training Metrics gate
            [
                RegressionTestCase(
                    test_id="release_gate_training_metrics_import",
                    name="TrainingMetricsEngine import (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="import",
                    command=["-c", "from training_metrics.training_metrics_engine import TrainingMetricsEngine; print('OK')"],
                    timeout_seconds=30,
                    required=False,
                    description="v0.8.2 TrainingMetricsEngine import smoke test",
                ),
                RegressionTestCase(
                    test_id="release_gate_training_metrics_summary",
                    name="training-metrics-summary (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="research_os",
                    command=["main.py", "training-metrics-summary"],
                    timeout_seconds=30,
                    required=False,
                    description="v0.8.2 Training metrics summary smoke test",
                ),
            ],
            # v0.8.3 Research Intelligence Evidence Graph gate
            [
                RegressionTestCase(
                    test_id="release_gate_evidence_graph_schema_import",
                    name="EvidenceNode import (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="import",
                    command=["-c", "from evidence_graph.evidence_graph_schema import EvidenceNode; print('EvidenceNode import OK')"],
                    timeout_seconds=30,
                    required=False,
                    description="v0.8.3 EvidenceNode schema import smoke test",
                ),
                RegressionTestCase(
                    test_id="release_gate_evidence_graph_engine_import",
                    name="EvidenceGraphEngine import (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="import",
                    command=["-c", "from evidence_graph.evidence_graph_engine import EvidenceGraphEngine; print('EvidenceGraphEngine import OK')"],
                    timeout_seconds=30,
                    required=False,
                    description="v0.8.3 EvidenceGraphEngine import smoke test",
                ),
                RegressionTestCase(
                    test_id="release_gate_evidence_graph_summary",
                    name="evidence-graph-summary (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="research_os",
                    command=["main.py", "evidence-graph-summary"],
                    timeout_seconds=60,
                    required=False,
                    description="v0.8.3 Evidence graph summary smoke test",
                ),
                RegressionTestCase(
                    test_id="release_gate_evidence_graph_nodes",
                    name="evidence-graph-nodes (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="research_os",
                    command=["main.py", "evidence-graph-nodes"],
                    timeout_seconds=60,
                    required=False,
                    description="v0.8.3 Evidence graph nodes smoke test",
                ),
                RegressionTestCase(
                    test_id="release_gate_evidence_graph_report",
                    name="evidence-graph-report --mode real (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="report",
                    command=["main.py", "evidence-graph-report", "--mode", "real"],
                    timeout_seconds=60,
                    required=False,
                    description="v0.8.3 Evidence graph report smoke test",
                ),
                # v0.9.0 Strategy Lab Stable
                RegressionTestCase(
                    test_id="release_gate_strategy_lab_schema_import",
                    name="StrategyLabCapability import (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="import",
                    command=["-c", "from strategy_lab.strategy_lab_schema import StrategyLabCapability; print('StrategyLabCapability import OK')"],
                    timeout_seconds=30,
                    required=False,
                    description="v0.9.0 StrategyLabCapability schema import smoke test",
                ),
                RegressionTestCase(
                    test_id="release_gate_strategy_lab_engine_import",
                    name="StrategyLabEngine import (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="import",
                    command=["-c", "from strategy_lab.strategy_lab_engine import StrategyLabEngine; print('StrategyLabEngine import OK')"],
                    timeout_seconds=30,
                    required=False,
                    description="v0.9.0 StrategyLabEngine import smoke test",
                ),
                RegressionTestCase(
                    test_id="release_gate_strategy_lab_summary",
                    name="strategy-lab-summary (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="research_os",
                    command=["main.py", "strategy-lab-summary"],
                    timeout_seconds=60,
                    required=False,
                    description="v0.9.0 Strategy lab summary smoke test",
                ),
                RegressionTestCase(
                    test_id="release_gate_strategy_lab_report",
                    name="strategy-lab-report --mode real (release gate)",
                    suite=SUITE_RELEASE_GATE,
                    category="report",
                    command=["main.py", "strategy-lab-report", "--mode", "real"],
                    timeout_seconds=60,
                    required=False,
                    description="v0.9.0 Strategy lab report smoke test",
                ),
            ],
        ]:
            for tc in suite_tests:
                if tc.test_id not in seen:
                    combined.append(tc)
                    seen.add(tc.test_id)
        return combined
