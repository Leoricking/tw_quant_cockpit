"""
os_planning/regression_audit.py — RegressionAudit (v0.5.0).

Audits regression suite coverage across all v0.4.x modules.
Compares against known tests in regression_suite.py and
stable_release_checklist.py.

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
# Hardcoded coverage data — indexed by module name
# covered = True  → test exists in regression_suite.py or stable_release_checklist.py
# ---------------------------------------------------------------------------

_COVERAGE: list[dict] = [
    # module, command_covered, import_covered, gui_covered, report_covered, safety_covered,
    # missing_checks, recommended_test
    {
        "module":            "data_providers",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "partial",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for provider fallback on timeout",
        "recommended_test":  "_test_provider_fallback_timeout",
    },
    {
        "module":            "data_quality",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "partial",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for empty universe gate",
        "recommended_test":  "_test_data_quality_gate_empty_universe",
    },
    {
        "module":            "data_freshness",
        "command_covered":   "no",
        "import_covered":    "partial",
        "gui_covered":       "no",
        "report_covered":    "no",
        "safety_covered":    "partial",
        "missing_checks":    "No dedicated freshness test; embedded in data_quality only",
        "recommended_test":  "_test_data_freshness_check_standalone",
    },
    {
        "module":            "api_fetch",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for TWSE parser edge cases",
        "recommended_test":  "_test_twse_parser_malformed_csv",
    },
    {
        "module":            "provider_reliability",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "partial",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for reliability backfill on fresh install",
        "recommended_test":  "_test_provider_reliability_fresh_install",
    },
    {
        "module":            "intraday_pipeline",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "partial",
        "report_covered":    "no",
        "safety_covered":    "yes",
        "missing_checks":    "No test for corrupt intraday CSV import",
        "recommended_test":  "_test_intraday_pipeline_corrupt_csv",
    },
    {
        "module":            "strategy_knowledge",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for duplicate transcript ingestion",
        "recommended_test":  "_test_strategy_knowledge_duplicate_transcript",
    },
    {
        "module":            "rule_governance",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "partial",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for rule conflict detection",
        "recommended_test":  "_test_rule_governance_conflict_detection",
    },
    {
        "module":            "signal_quality",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "partial",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for signal quality on all-NaN features",
        "recommended_test":  "_test_signal_quality_all_nan_features",
    },
    {
        "module":            "rule_weight_tuning",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "no",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No GUI panel import test",
        "recommended_test":  "_test_rule_weight_tuning_gui_import",
    },
    {
        "module":            "ml_feature_store",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for feature snapshot with all-zero data",
        "recommended_test":  "_test_ml_feature_snapshot_all_zero",
    },
    {
        "module":            "ml_knowledge_integration",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for bridge with corrupt knowledge store",
        "recommended_test":  "_test_ml_knowledge_bridge_corrupt_store",
    },
    {
        "module":            "model_monitoring",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for DRIFT_CRITICAL path with seeded data",
        "recommended_test":  "_test_model_monitoring_drift_critical_seeded",
    },
    {
        "module":            "hardened_backtest",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "partial",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for backtest with insufficient data window",
        "recommended_test":  "_test_hardened_backtest_insufficient_window",
    },
    {
        "module":            "portfolio_simulation",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "partial",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for portfolio with zero capital",
        "recommended_test":  "_test_portfolio_simulation_zero_capital",
    },
    {
        "module":            "intraday_replay",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for replay with malformed tick data",
        "recommended_test":  "_test_intraday_replay_malformed_ticks",
    },
    {
        "module":            "paper_mock_realtime",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "no",
        "report_covered":    "no",
        "safety_covered":    "yes",
        "missing_checks":    "No GUI import test for mock_realtime panel",
        "recommended_test":  "_test_mock_realtime_gui_import",
    },
    {
        "module":            "experiment_registry",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for concurrent write to registry.json",
        "recommended_test":  "_test_experiment_registry_concurrent_write",
    },
    {
        "module":            "notification_center",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for notification rule with regex pattern",
        "recommended_test":  "_test_notification_rule_regex_pattern",
    },
    {
        "module":            "portfolio_journal",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for analytics with single entry",
        "recommended_test":  "_test_journal_analytics_single_entry",
    },
    {
        "module":            "research_review_dashboard",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for scorecard with all-zero module scores",
        "recommended_test":  "_test_research_review_scorecard_all_zero",
    },
    {
        "module":            "research_assistant_coach",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for coach with all checklist items completed",
        "recommended_test":  "_test_research_coach_all_complete",
    },
    {
        "module":            "research_workflow_automation",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for workflow with all-blocked commands",
        "recommended_test":  "_test_research_workflow_all_blocked_commands",
    },
    {
        "module":            "auto_report_center",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "partial",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for report with missing upstream data",
        "recommended_test":  "_test_auto_report_missing_upstream_data",
    },
    {
        "module":            "dashboard_gui",
        "command_covered":   "partial",
        "import_covered":    "yes",
        "gui_covered":       "yes",
        "report_covered":    "no",
        "safety_covered":    "yes",
        "missing_checks":    "No test for tab loading with PySide6 present",
        "recommended_test":  "_test_dashboard_gui_all_tabs_load",
    },
    {
        "module":            "release",
        "command_covered":   "yes",
        "import_covered":    "yes",
        "gui_covered":       "partial",
        "report_covered":    "yes",
        "safety_covered":    "yes",
        "missing_checks":    "No test for regression suite CSV output integrity",
        "recommended_test":  "_test_regression_suite_csv_integrity",
    },
    {
        "module":            "research_os_planning",
        "command_covered":   "no",
        "import_covered":    "no",
        "gui_covered":       "no",
        "report_covered":    "no",
        "safety_covered":    "no",
        "missing_checks":    "NEW in v0.5.0 — all tests pending",
        "recommended_test":  "_test_os_planning_module_inventory; _test_os_planning_cli_inventory; _test_os_planning_safety_matrix",
    },
]


class RegressionAudit:
    """Audits regression suite coverage for all v0.4.x modules.

    [!] OS Planning Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True
    real_order_ready:   bool = False

    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = base_dir or BASE_DIR

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """Run all coverage checks and return summary dict."""
        try:
            command_rows  = self.check_command_coverage()
            import_rows   = self.check_import_coverage()
            gui_rows      = self.check_gui_import_coverage()
            report_rows   = self.check_report_generation_coverage()
            safety_rows   = self.check_safety_coverage()

            total = len(_COVERAGE)
            fully_covered  = sum(1 for r in _COVERAGE if self._is_fully_covered(r))
            missing_any    = total - fully_covered

            return {
                "status":              "OK",
                "total_modules":       total,
                "fully_covered":       fully_covered,
                "missing_any":         missing_any,
                "command_issues":      sum(1 for r in command_rows  if r.get("covered") != "yes"),
                "import_issues":       sum(1 for r in import_rows   if r.get("covered") != "yes"),
                "gui_issues":          sum(1 for r in gui_rows      if r.get("covered") != "yes"),
                "report_issues":       sum(1 for r in report_rows   if r.get("covered") != "yes"),
                "safety_issues":       sum(1 for r in safety_rows   if r.get("covered") != "yes"),
                "read_only":           True,
                "no_real_orders":      True,
                "production_blocked":  True,
            }
        except Exception as exc:
            logger.warning("RegressionAudit.run error: %s", exc)
            return {
                "status":             "ERROR",
                "error":              str(exc),
                "read_only":          True,
                "no_real_orders":     True,
                "production_blocked": True,
            }

    def check_command_coverage(self) -> list[dict]:
        """Return command coverage status per module."""
        try:
            return [
                {"module": r["module"], "covered": r["command_covered"],
                 "missing_checks": r["missing_checks"] if r["command_covered"] != "yes" else ""}
                for r in _COVERAGE
            ]
        except Exception as exc:
            logger.warning("check_command_coverage error: %s", exc)
            return []

    def check_import_coverage(self) -> list[dict]:
        """Return import coverage status per module."""
        try:
            return [
                {"module": r["module"], "covered": r["import_covered"],
                 "missing_checks": r["missing_checks"] if r["import_covered"] != "yes" else ""}
                for r in _COVERAGE
            ]
        except Exception as exc:
            logger.warning("check_import_coverage error: %s", exc)
            return []

    def check_gui_import_coverage(self) -> list[dict]:
        """Return GUI import coverage status per module."""
        try:
            return [
                {"module": r["module"], "covered": r["gui_covered"],
                 "missing_checks": r["missing_checks"] if r["gui_covered"] != "yes" else ""}
                for r in _COVERAGE
            ]
        except Exception as exc:
            logger.warning("check_gui_import_coverage error: %s", exc)
            return []

    def check_report_generation_coverage(self) -> list[dict]:
        """Return report generation coverage status per module."""
        try:
            return [
                {"module": r["module"], "covered": r["report_covered"],
                 "missing_checks": r["missing_checks"] if r["report_covered"] != "yes" else ""}
                for r in _COVERAGE
            ]
        except Exception as exc:
            logger.warning("check_report_generation_coverage error: %s", exc)
            return []

    def check_safety_coverage(self) -> list[dict]:
        """Return safety flag coverage status per module."""
        try:
            return [
                {"module": r["module"], "covered": r["safety_covered"],
                 "missing_checks": r["missing_checks"] if r["safety_covered"] != "yes" else ""}
                for r in _COVERAGE
            ]
        except Exception as exc:
            logger.warning("check_safety_coverage error: %s", exc)
            return []

    def export_audit(self, output_dir: str) -> str:
        """Write regression_audit.csv to output_dir. Returns path."""
        fieldnames = [
            "module", "command_covered", "import_covered", "gui_covered",
            "report_covered", "safety_covered", "missing_checks", "recommended_test",
        ]
        try:
            os.makedirs(output_dir, exist_ok=True)
            today = datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(output_dir, f"regression_audit_{today}.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(_COVERAGE)
            logger.info("regression_audit CSV saved: %s", path)
            return path
        except Exception as exc:
            logger.warning("export_audit error: %s", exc)
            fallback = os.path.join(output_dir or ".", "regression_audit_error.csv")
            return fallback

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_fully_covered(row: dict) -> bool:
        """Return True if all coverage dimensions are 'yes'."""
        try:
            return all(
                row.get(k) == "yes"
                for k in ("command_covered", "import_covered", "gui_covered",
                          "report_covered", "safety_covered")
            )
        except Exception:
            return False
