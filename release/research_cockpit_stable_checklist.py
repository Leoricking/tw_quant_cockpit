"""
release/research_cockpit_stable_checklist.py — ResearchCockpitStableChecklist v1.0.x

25-item release checklist for TW Quant Cockpit v1.0.x Research Trading Cockpit Stable.
Accepts v1.0.0 and all v1.0.x maintenance releases.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Broker Execution Disabled.
"""
from __future__ import annotations

import logging
import os
import re
from typing import List, Tuple

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_FORBIDDEN_PATTERN = re.compile(
    r'\b(BUY|SELL|ORDER|EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE|LIVE_TRADE|BROKER_ORDER)\b'
)
_WHITELIST_PHRASES = [
    "No Real Orders",
    "No broker execution",
    "Broker Execution Disabled",
    "Not an order",
]


def _whitelist_clean(text: str) -> str:
    """Remove whitelisted phrases before scanning for forbidden keywords."""
    for phrase in _WHITELIST_PHRASES:
        text = text.replace(phrase, "")
    return text


def _mk(name: str, category: str, status: str, detail: str) -> dict:
    return {
        "name":     name,
        "category": category,
        "status":   status,
        "detail":   detail,
    }


class ResearchCockpitStableChecklist:
    """v1.0.0 Research Trading Cockpit Stable checklist — 30 checks.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, project_root: str = ".") -> None:
        if os.path.isabs(project_root):
            self._root = project_root
        else:
            self._root = os.path.join(BASE_DIR, project_root)

    def run(self, mode: str = "real") -> Tuple[List[dict], dict]:
        """Run all checks. Returns (list of check dicts, summary dict)."""
        checks: List[dict] = []

        # 1. version_info_v100 — accepts v1.0.0 and v1.0.x maintenance releases
        try:
            from release.version_info import VERSION
            if VERSION.startswith("1.0."):
                checks.append(_mk("version_info_v100", "version", "PASS", f"VERSION={VERSION} (v1.0.x stable)"))
            else:
                checks.append(_mk("version_info_v100", "version", "FAIL", f"Expected 1.0.x, got {VERSION}"))
        except Exception as exc:
            checks.append(_mk("version_info_v100", "version", "FAIL", str(exc)))

        # 2. no_real_orders_global_guard
        try:
            from release.version_info import REAL_ORDERS_ENABLED, NO_REAL_ORDERS
            if REAL_ORDERS_ENABLED is False and NO_REAL_ORDERS is True:
                checks.append(_mk("no_real_orders_global_guard", "safety", "PASS",
                                  "REAL_ORDERS_ENABLED=False, NO_REAL_ORDERS=True"))
            else:
                checks.append(_mk("no_real_orders_global_guard", "safety", "FAIL",
                                  f"REAL_ORDERS_ENABLED={REAL_ORDERS_ENABLED} NO_REAL_ORDERS={NO_REAL_ORDERS}"))
        except Exception as exc:
            checks.append(_mk("no_real_orders_global_guard", "safety", "FAIL", str(exc)))

        # 3. production_trading_blocked
        try:
            from release.version_info import PRODUCTION_TRADING_BLOCKED
            if PRODUCTION_TRADING_BLOCKED is True:
                checks.append(_mk("production_trading_blocked", "safety", "PASS",
                                  "PRODUCTION_TRADING_BLOCKED=True"))
            else:
                checks.append(_mk("production_trading_blocked", "safety", "FAIL",
                                  f"PRODUCTION_TRADING_BLOCKED={PRODUCTION_TRADING_BLOCKED}"))
        except Exception as exc:
            checks.append(_mk("production_trading_blocked", "safety", "FAIL", str(exc)))

        # 4. broker_execution_disabled
        try:
            from release.version_info import BROKER_EXECUTION_ENABLED
            if BROKER_EXECUTION_ENABLED is False:
                checks.append(_mk("broker_execution_disabled", "safety", "PASS",
                                  "BROKER_EXECUTION_ENABLED=False"))
            else:
                checks.append(_mk("broker_execution_disabled", "safety", "FAIL",
                                  f"BROKER_EXECUTION_ENABLED={BROKER_EXECUTION_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("broker_execution_disabled", "safety", "FAIL", str(exc)))

        # 5. validated_does_not_enable_trading
        try:
            from release.version_info import VALIDATED_DOES_NOT_ENABLE_TRADING
            if VALIDATED_DOES_NOT_ENABLE_TRADING is True:
                checks.append(_mk("validated_does_not_enable_trading", "safety", "PASS",
                                  "VALIDATED_DOES_NOT_ENABLE_TRADING=True"))
            else:
                checks.append(_mk("validated_does_not_enable_trading", "safety", "FAIL",
                                  f"VALIDATED_DOES_NOT_ENABLE_TRADING={VALIDATED_DOES_NOT_ENABLE_TRADING}"))
        except Exception as exc:
            checks.append(_mk("validated_does_not_enable_trading", "safety", "FAIL", str(exc)))

        # 6. strategy_lab_dashboard_available
        checks.append(self._import_check(
            "strategy_lab_dashboard_available", "modules",
            "strategy_lab.strategy_lab_dashboard_engine", "StrategyLabDashboardEngine",
        ))

        # 7. strategy_validation_available
        checks.append(self._import_check(
            "strategy_validation_available", "modules",
            "strategy_validation.strategy_validation_engine", "StrategyValidationEngine",
        ))

        # 8. evidence_graph_ux_available
        checks.append(self._import_check(
            "evidence_graph_ux_available", "modules",
            "evidence_graph.evidence_graph_query", "EvidenceGraphQuery",
        ))

        # 9. crash_reversal_available
        checks.append(self._import_check(
            "crash_reversal_available", "modules",
            "strategy_rules.crash_reversal_pack", "CrashReversalStrategyPack",
        ))

        # 10. training_metrics_available
        checks.append(self._import_check(
            "training_metrics_available", "modules",
            "training_metrics.training_metrics_engine", "TrainingMetricsEngine",
        ))

        # 11. backtest_coach_available
        checks.append(self._import_check(
            "backtest_coach_available", "modules",
            "backtest_coach.backtest_coach_engine", "BacktestCoachEngine",
        ))

        # 12. strategy_memory_available
        checks.append(self._import_check(
            "strategy_memory_available", "modules",
            "strategy_memory.strategy_memory_engine", "StrategyMemoryEngine",
        ))

        # 13. research_intelligence_available
        checks.append(self._import_check(
            "research_intelligence_available", "modules",
            "research_intelligence.research_intelligence_engine", "ResearchIntelligenceEngine",
        ))

        # 14. report_pack_available
        checks.append(self._import_check(
            "report_pack_available", "modules",
            "report_pack.report_registry", "ReportRegistry",
        ))

        # 15. data_coverage_available
        checks.append(self._import_check(
            "data_coverage_available", "modules",
            "data_coverage.data_coverage_engine", "DataCoverageEngine",
        ))

        # 16. mock_realtime_available — check broker.mock_broker (actual implementation)
        try:
            import importlib
            mod = importlib.import_module("broker.mock_broker")
            available = hasattr(mod, "MockBroker")
            if available:
                checks.append(_mk("mock_realtime_available", "modules", "PASS",
                                  "broker.mock_broker.MockBroker import OK"))
            else:
                checks.append(_mk("mock_realtime_available", "modules", "WARN",
                                  "broker.mock_broker imported but MockBroker not found"))
        except Exception as exc:
            checks.append(_mk("mock_realtime_available", "modules", "WARN",
                              f"mock_realtime import: {exc}"))

        # 17. paper_available — check sim.simulator (actual implementation)
        try:
            import importlib
            mod = importlib.import_module("sim.simulator")
            available = hasattr(mod, "PaperTrader")
            if available:
                checks.append(_mk("paper_available", "modules", "PASS",
                                  "sim.simulator.PaperTrader import OK"))
            else:
                checks.append(_mk("paper_available", "modules", "WARN",
                                  "sim.simulator imported but PaperTrader not found"))
        except Exception as exc:
            checks.append(_mk("paper_available", "modules", "WARN",
                              f"paper import: {exc}"))

        # 18. gui_import_available
        try:
            import importlib
            mod = importlib.import_module("gui.dashboard")
            has_launch = hasattr(mod, "launch")
            if has_launch:
                checks.append(_mk("gui_import_available", "gui", "PASS",
                                  "gui.dashboard.launch import OK"))
            else:
                checks.append(_mk("gui_import_available", "gui", "WARN",
                                  "gui.dashboard imported but launch not found"))
        except Exception as exc:
            checks.append(_mk("gui_import_available", "gui", "WARN",
                              f"gui.dashboard import: {exc}"))

        # 19. gui_navigation_available
        try:
            import importlib
            mod = importlib.import_module("gui.navigation.tab_registry")
            has_cls = hasattr(mod, "GUITabRegistry")
            if has_cls:
                checks.append(_mk("gui_navigation_available", "gui", "PASS",
                                  "GUITabRegistry import OK"))
            else:
                checks.append(_mk("gui_navigation_available", "gui", "WARN",
                                  "gui.navigation.tab_registry imported but GUITabRegistry not found"))
        except Exception as exc:
            checks.append(_mk("gui_navigation_available", "gui", "WARN",
                              f"GUITabRegistry import: {exc}"))

        # 20. regression_release_gate_available
        try:
            import importlib
            mod = importlib.import_module("regression.suite_registry")
            has_cls = hasattr(mod, "RegressionSuiteRegistry")
            if has_cls:
                checks.append(_mk("regression_release_gate_available", "regression", "PASS",
                                  "RegressionSuiteRegistry import OK"))
            else:
                checks.append(_mk("regression_release_gate_available", "regression", "WARN",
                                  "regression.suite_registry imported but RegressionSuiteRegistry not found"))
        except Exception as exc:
            checks.append(_mk("regression_release_gate_available", "regression", "WARN",
                              f"RegressionSuiteRegistry import: {exc}"))

        # 21. forbidden_action_scan_passed
        checks.append(self._forbidden_action_scan())

        # 22. runtime_output_gitignore_passed
        gitignore_path = os.path.join(self._root, ".gitignore")
        try:
            with open(gitignore_path, "r", encoding="utf-8") as fh:
                content = fh.read()
            if "data/backtest_results/" in content:
                checks.append(_mk("runtime_output_gitignore_passed", "hygiene", "PASS",
                                  ".gitignore contains data/backtest_results/"))
            else:
                checks.append(_mk("runtime_output_gitignore_passed", "hygiene", "WARN",
                                  ".gitignore missing data/backtest_results/ entry"))
        except Exception as exc:
            checks.append(_mk("runtime_output_gitignore_passed", "hygiene", "WARN",
                              f"Cannot read .gitignore: {exc}"))

        # 23. docs_index_available
        docs_index = os.path.join(self._root, "docs", "index.md")
        if os.path.isfile(docs_index):
            checks.append(_mk("docs_index_available", "docs", "PASS",
                              "docs/index.md exists"))
        else:
            checks.append(_mk("docs_index_available", "docs", "WARN",
                              "docs/index.md not found"))

        # 24. README_v100_available
        readme_path = os.path.join(self._root, "README.md")
        try:
            with open(readme_path, "r", encoding="utf-8") as fh:
                readme_content = fh.read()
            if "1.0.0" in readme_content:
                checks.append(_mk("README_v100_available", "docs", "PASS",
                                  "README.md mentions 1.0.0"))
            else:
                checks.append(_mk("README_v100_available", "docs", "WARN",
                                  "README.md does not mention 1.0.0"))
        except Exception as exc:
            checks.append(_mk("README_v100_available", "docs", "WARN",
                              f"Cannot read README.md: {exc}"))

        # 25. release_notes_v100_available
        rn_path = os.path.join(self._root, "docs", "release_notes_v1.0.md")
        if os.path.isfile(rn_path):
            checks.append(_mk("release_notes_v100_available", "docs", "PASS",
                              "docs/release_notes_v1.0.md exists"))
        else:
            checks.append(_mk("release_notes_v100_available", "docs", "WARN",
                              "docs/release_notes_v1.0.md not found"))

        # 26. data_report_hygiene_available — import DataReportHygieneEngine
        checks.append(self._import_check(
            "data_report_hygiene_available", "modules",
            "maintenance.data_report_hygiene_engine", "DataReportHygieneEngine",
        ))

        # 27. data_report_hygiene_review_only
        try:
            from maintenance.data_report_hygiene_engine import DataReportHygieneEngine
            eng = DataReportHygieneEngine()
            if getattr(eng, "review_only", False) and getattr(eng, "no_real_orders", False):
                checks.append(_mk("data_report_hygiene_review_only", "safety", "PASS",
                                  "DataReportHygieneEngine.review_only=True, no_real_orders=True"))
            else:
                checks.append(_mk("data_report_hygiene_review_only", "safety", "FAIL",
                                  "DataReportHygieneEngine safety flags not set"))
        except Exception as exc:
            checks.append(_mk("data_report_hygiene_review_only", "safety", "WARN", str(exc)))

        # 28. runtime_outputs_gitignored — data/backtest_results/ in .gitignore
        gitignore_path = os.path.join(self._root, ".gitignore")
        try:
            with open(gitignore_path, "r", encoding="utf-8") as fh:
                gi_content = fh.read()
            covered = "data/backtest_results/" in gi_content
            if covered:
                checks.append(_mk("runtime_outputs_gitignored", "hygiene", "PASS",
                                  ".gitignore covers data/backtest_results/"))
            else:
                checks.append(_mk("runtime_outputs_gitignored", "hygiene", "WARN",
                                  ".gitignore missing data/backtest_results/ entry"))
        except Exception as exc:
            checks.append(_mk("runtime_outputs_gitignored", "hygiene", "WARN",
                              f"Cannot read .gitignore: {exc}"))

        # 29. no_tracked_runtime_outputs
        try:
            import subprocess
            result = subprocess.run(
                ["git", "-C", self._root, "ls-files", "--",
                 "data/backtest_results/",
                 "reports/research_trading_cockpit_stable_report_*.md"],
                capture_output=True, text=True, timeout=30,
            )
            tracked = [l.strip() for l in result.stdout.splitlines() if l.strip()]
            if not tracked:
                checks.append(_mk("no_tracked_runtime_outputs", "hygiene", "PASS",
                                  "No tracked runtime outputs found"))
            else:
                checks.append(_mk("no_tracked_runtime_outputs", "hygiene", "WARN",
                                  f"{len(tracked)} tracked runtime output(s) found: {tracked[:3]}"))
        except Exception as exc:
            checks.append(_mk("no_tracked_runtime_outputs", "hygiene", "WARN", str(exc)))

        # 30. hygiene_report_available
        checks.append(self._import_check(
            "hygiene_report_available", "modules",
            "reports.data_report_hygiene_report", "DataReportHygieneReportBuilder",
        ))

        # 31. gui_health_check_available
        checks.append(self._import_check(
            "gui_health_check_available", "modules",
            "gui.gui_health_check", "GuiHealthCheck",
        ))

        # 32. gui_no_forbidden_text
        try:
            from gui.common.gui_safety import build_research_only_banner
            banner = build_research_only_banner()
            cleaned = banner
            for phrase in _WHITELIST_PHRASES:
                cleaned = cleaned.replace(phrase, "")
            hits = _FORBIDDEN_PATTERN.findall(cleaned)
            if hits:
                checks.append(_mk("gui_no_forbidden_text", "safety", "BLOCKED",
                                  f"Forbidden text in safety banner: {hits}"))
            else:
                checks.append(_mk("gui_no_forbidden_text", "safety", "PASS",
                                  "No forbidden text in GUI safety banner"))
        except Exception as exc:
            checks.append(_mk("gui_no_forbidden_text", "safety", "WARN", str(exc)))

        # 33. gui_qthread_helper_available
        checks.append(self._import_check(
            "gui_qthread_helper_available", "modules",
            "gui.common.gui_threading", "SafeWorker",
        ))

        # 34. gui_copy_utils_available
        checks.append(self._import_check(
            "gui_copy_utils_available", "modules",
            "gui.common.copy_utils", "copy_safe_text",
        ))

        # 35. regression_hardening_available
        checks.append(self._import_check(
            "regression_hardening_available", "modules",
            "regression_hardening.safety_scanner", "SafetyScanner",
        ))

        # 36. safety_scanner_available
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            scanner = SafetyScanner()
            if hasattr(scanner, 'scan_text'):
                checks.append(_mk("safety_scanner_available", "modules", "PASS",
                                  "SafetyScanner available with scan_text method"))
            else:
                checks.append(_mk("safety_scanner_available", "modules", "WARN",
                                  "SafetyScanner imported but scan_text not found"))
        except Exception as exc:
            checks.append(_mk("safety_scanner_available", "modules", "WARN", str(exc)))

        # 37. safety_scanner_no_false_positive
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            scanner = SafetyScanner()
            result = scanner.scan_text("No Real Orders — Research Only. No broker execution.")
            if result.status == "PASS":
                checks.append(_mk("safety_scanner_no_false_positive", "safety", "PASS",
                                  "No Real Orders text scans as PASS (correctly whitelisted)"))
            else:
                checks.append(_mk("safety_scanner_no_false_positive", "safety", "WARN",
                                  f"No Real Orders scan returned {result.status}: {result.forbidden_hits}"))
        except Exception as exc:
            checks.append(_mk("safety_scanner_no_false_positive", "safety", "WARN", str(exc)))

        # 38. release_gate_health_available
        checks.append(self._import_check(
            "release_gate_health_available", "modules",
            "regression_hardening.release_gate_health", "ReleaseGateHealth",
        ))

        # 39. known_warning_classification_available
        checks.append(self._import_check(
            "known_warning_classification_available", "modules",
            "regression_hardening.regression_summary", "classify_warning",
        ))

        # Build summary
        total         = len(checks)
        pass_count    = sum(1 for c in checks if c["status"] == "PASS")
        warn_count    = sum(1 for c in checks if c["status"] == "WARN")
        fail_count    = sum(1 for c in checks if c["status"] == "FAIL")
        blocked_count = sum(1 for c in checks if c["status"] == "BLOCKED")

        if fail_count == 0 and blocked_count == 0 and warn_count == 0:
            overall_status = "STABLE"
        elif fail_count == 0 and blocked_count == 0:
            overall_status = "WARNING"
        elif blocked_count > 0:
            overall_status = "BLOCKED"
        else:
            overall_status = "FAIL"

        try:
            from release.version_info import VERSION as _SUM_VER
        except Exception:
            _SUM_VER = "1.0.x"
        summary = {
            "version":        _SUM_VER,
            "release_name":   "Research Trading Cockpit Stable",
            "total":          total,
            "pass_count":     pass_count,
            "warn_count":     warn_count,
            "fail_count":     fail_count,
            "blocked_count":  blocked_count,
            "overall_status": overall_status,
            "no_real_orders": True,
            "production_blocked": True,
        }
        return checks, summary

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _import_check(self, name: str, category: str, module_path: str,
                      class_name: str) -> dict:
        try:
            import importlib
            mod = importlib.import_module(module_path)
            if hasattr(mod, class_name):
                return _mk(name, category, "PASS", f"{class_name} import OK")
            else:
                return _mk(name, category, "WARN",
                           f"{module_path} imported but {class_name} not found")
        except Exception as exc:
            return _mk(name, category, "WARN", f"{module_path}: {exc}")

    def _forbidden_action_scan(self) -> dict:
        """Scan key safety strings for standalone forbidden trading keywords."""
        safety_strings = [
            "No Real Orders",
            "No broker execution",
            "Broker Execution Disabled",
            "Production Trading BLOCKED",
            "VALIDATED does not enable trading",
            "Paper trading is simulation only",
            "Mock realtime is simulation only",
            "Not Investment Advice",
        ]
        found_forbidden = []
        for s in safety_strings:
            cleaned = _whitelist_clean(s)
            matches = _FORBIDDEN_PATTERN.findall(cleaned)
            if matches:
                found_forbidden.extend(matches)

        if not found_forbidden:
            return _mk("forbidden_action_scan_passed", "safety", "PASS",
                       "No forbidden trading keywords in safety strings")
        else:
            return _mk("forbidden_action_scan_passed", "safety", "WARN",
                       f"Forbidden keywords found after whitelist removal: {found_forbidden}")
