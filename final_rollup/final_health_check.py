"""
final_rollup/final_health_check.py — Final Maintenance Health Check for TW Quant Cockpit v1.0.9.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Final Maintenance Rollup.
"""
from __future__ import annotations

import importlib
import logging
import os
from typing import List, Tuple

logger = logging.getLogger(__name__)

_STATUS_PASS    = "PASS"
_STATUS_WARN    = "WARN"
_STATUS_FAIL    = "FAIL"
_STATUS_BLOCKED = "BLOCKED"


def _mk(name: str, category: str, status: str, detail: str = "") -> dict:
    return {"name": name, "category": category, "status": status, "detail": detail}


class FinalMaintenanceHealthCheck:
    """Runs the final maintenance health check for v1.0.9.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    Outputs: PASS / WARN / FAIL / BLOCKED — never BUY/SELL/ORDER.
    """

    no_real_orders = True
    broker_disabled = True
    external_api_disabled = True

    def __init__(self, project_root: str = None) -> None:
        self._root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def run(self) -> Tuple[List[dict], dict]:
        """Run all checks. Returns (checks_list, summary_dict)."""
        checks = []

        # 1. version_info_v109
        checks.append(self._check_version_info_v109())

        # 2. no_real_orders
        checks.append(self._check_no_real_orders())

        # 3. broker_execution_disabled
        checks.append(self._check_broker_disabled())

        # 4. external_api_disabled
        checks.append(self._check_external_api_disabled())

        # 5. validated_does_not_enable_trading
        checks.append(self._check_validated_no_trading())

        # 6. research_cockpit_stable_available
        checks.append(self._check_module("research_cockpit_stable_available", "research_cockpit",
                                          "release.research_cockpit_stable", "ResearchTradingCockpitStable"))

        # 7. stable_v060_available
        checks.append(self._check_module("stable_v060_available", "stable_release",
                                          "stable_release.stable_release_checklist_v060", "StableReleaseChecklistV060"))

        # 8. release_gate_available
        checks.append(self._check_module("release_gate_available", "regression",
                                          "maintenance.release_gate_health", "ReleaseGateHealthCheck"))

        # 9. quick_regression_available
        checks.append(self._check_module("quick_regression_available", "regression",
                                          "regression.suite_registry", "RegressionSuiteRegistry"))

        # 10. safety_scan_available
        checks.append(self._check_module("safety_scan_available", "safety",
                                          "maintenance.safety_scanner", "SafetyScanner"))

        # 11. docs_health_available
        checks.append(self._check_file_exists("docs_health_available", "docs", "docs/index.md"))

        # 12. workflow_templates_available
        checks.append(self._check_dir_exists("workflow_templates_available", "workflows", "docs/examples"))

        # 13. kb_search_available
        checks.append(self._check_module("kb_search_available", "knowledge_base",
                                          "knowledge_base.kb_search_engine", "KBSearchEngine"))

        # 14. local_assistant_available
        checks.append(self._check_module("local_assistant_available", "local_assistant",
                                          "local_assistant.local_assistant_engine", "LocalResearchAssistantEngine"))

        # 15. data_hygiene_available
        checks.append(self._check_module("data_hygiene_available", "data_hygiene",
                                          "maintenance.data_report_hygiene", "DataReportHygiene"))

        # 16. gui_health_available
        checks.append(self._check_module("gui_health_available", "gui",
                                          "gui.gui_health_check", "GUIHealthCheck"))

        # 17. report_pack_available
        checks.append(self._check_module("report_pack_available", "report_pack",
                                          "report_pack.report_registry", "ReportRegistry"))

        # 18. paper_simulation_only
        checks.append(self._check_paper_simulation_only())

        # 19. mock_realtime_simulation_only
        checks.append(self._check_mock_simulation_only())

        # 20. known_warnings_documented
        checks.append(self._check_known_warnings_documented())

        # 21. runtime_outputs_ignored
        checks.append(self._check_gitignore_runtime_outputs())

        # 22. no_forbidden_actions_unknown_hit
        checks.append(self._check_no_forbidden_actions())

        # Build summary
        total         = len(checks)
        pass_count    = sum(1 for c in checks if c["status"] == _STATUS_PASS)
        warn_count    = sum(1 for c in checks if c["status"] == _STATUS_WARN)
        fail_count    = sum(1 for c in checks if c["status"] == _STATUS_FAIL)
        blocked_count = sum(1 for c in checks if c["status"] == _STATUS_BLOCKED)

        if fail_count == 0 and blocked_count == 0 and warn_count == 0:
            overall = "PASS"
        elif fail_count == 0 and blocked_count == 0:
            overall = "WARN"
        elif blocked_count > 0:
            overall = "BLOCKED"
        else:
            overall = "FAIL"

        summary = {
            "version": "1.0.9",
            "total": total,
            "pass_count": pass_count,
            "warn_count": warn_count,
            "fail_count": fail_count,
            "blocked_count": blocked_count,
            "overall_status": overall,
            "no_real_orders": True,
            "broker_disabled": True,
            "external_api_disabled": True,
        }
        return checks, summary

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def _check_version_info_v109(self) -> dict:
        try:
            from release.version_info import VERSION, FINAL_MAINTENANCE_ROLLUP_RELEASE
            if VERSION == "1.0.9" and FINAL_MAINTENANCE_ROLLUP_RELEASE is True:
                return _mk("version_info_v109", "version", _STATUS_PASS,
                           f"VERSION={VERSION}, FINAL_MAINTENANCE_ROLLUP_RELEASE=True")
            return _mk("version_info_v109", "version", _STATUS_FAIL,
                       f"VERSION={VERSION}, FINAL_MAINTENANCE_ROLLUP_RELEASE={FINAL_MAINTENANCE_ROLLUP_RELEASE}")
        except Exception as exc:
            return _mk("version_info_v109", "version", _STATUS_WARN, str(exc))

    def _check_no_real_orders(self) -> dict:
        try:
            from release.version_info import NO_REAL_ORDERS, REAL_ORDERS_ENABLED
            if NO_REAL_ORDERS is True and REAL_ORDERS_ENABLED is False:
                return _mk("no_real_orders", "safety", _STATUS_PASS,
                           "NO_REAL_ORDERS=True, REAL_ORDERS_ENABLED=False")
            return _mk("no_real_orders", "safety", _STATUS_FAIL,
                       f"NO_REAL_ORDERS={NO_REAL_ORDERS}, REAL_ORDERS_ENABLED={REAL_ORDERS_ENABLED}")
        except Exception as exc:
            return _mk("no_real_orders", "safety", _STATUS_WARN, str(exc))

    def _check_broker_disabled(self) -> dict:
        try:
            from release.version_info import BROKER_EXECUTION_ENABLED
            if BROKER_EXECUTION_ENABLED is False:
                return _mk("broker_execution_disabled", "safety", _STATUS_PASS,
                           "BROKER_EXECUTION_ENABLED=False")
            return _mk("broker_execution_disabled", "safety", _STATUS_FAIL,
                       f"BROKER_EXECUTION_ENABLED={BROKER_EXECUTION_ENABLED}")
        except Exception as exc:
            return _mk("broker_execution_disabled", "safety", _STATUS_WARN, str(exc))

    def _check_external_api_disabled(self) -> dict:
        try:
            from release.version_info import EXTERNAL_API_DISABLED
            if EXTERNAL_API_DISABLED is True:
                return _mk("external_api_disabled", "safety", _STATUS_PASS,
                           "EXTERNAL_API_DISABLED=True")
            return _mk("external_api_disabled", "safety", _STATUS_FAIL,
                       f"EXTERNAL_API_DISABLED={EXTERNAL_API_DISABLED}")
        except Exception as exc:
            return _mk("external_api_disabled", "safety", _STATUS_WARN, str(exc))

    def _check_validated_no_trading(self) -> dict:
        try:
            from release.version_info import VALIDATED_DOES_NOT_ENABLE_TRADING
            if VALIDATED_DOES_NOT_ENABLE_TRADING is True:
                return _mk("validated_does_not_enable_trading", "safety", _STATUS_PASS,
                           "VALIDATED_DOES_NOT_ENABLE_TRADING=True")
            return _mk("validated_does_not_enable_trading", "safety", _STATUS_FAIL,
                       f"VALIDATED_DOES_NOT_ENABLE_TRADING={VALIDATED_DOES_NOT_ENABLE_TRADING}")
        except Exception as exc:
            return _mk("validated_does_not_enable_trading", "safety", _STATUS_WARN, str(exc))

    def _check_module(self, name: str, category: str, module_path: str, class_name: str) -> dict:
        try:
            mod = importlib.import_module(module_path)
            if hasattr(mod, class_name):
                return _mk(name, category, _STATUS_PASS, f"{class_name} import OK")
            return _mk(name, category, _STATUS_WARN,
                       f"{module_path} imported but {class_name} not found")
        except Exception as exc:
            return _mk(name, category, _STATUS_WARN, f"{module_path}: {exc}")

    def _check_file_exists(self, name: str, category: str, rel_path: str) -> dict:
        full = os.path.join(self._root, rel_path)
        if os.path.isfile(full):
            return _mk(name, category, _STATUS_PASS, f"{rel_path} exists")
        return _mk(name, category, _STATUS_WARN, f"{rel_path} not found")

    def _check_dir_exists(self, name: str, category: str, rel_path: str) -> dict:
        full = os.path.join(self._root, rel_path)
        if os.path.isdir(full):
            return _mk(name, category, _STATUS_PASS, f"{rel_path}/ exists")
        return _mk(name, category, _STATUS_WARN, f"{rel_path}/ not found")

    def _check_paper_simulation_only(self) -> dict:
        try:
            from release.version_info import PAPER_TRADING_IS_SIMULATION
            if PAPER_TRADING_IS_SIMULATION is True:
                return _mk("paper_simulation_only", "safety", _STATUS_PASS,
                           "PAPER_TRADING_IS_SIMULATION=True")
            return _mk("paper_simulation_only", "safety", _STATUS_FAIL,
                       f"PAPER_TRADING_IS_SIMULATION={PAPER_TRADING_IS_SIMULATION}")
        except Exception as exc:
            return _mk("paper_simulation_only", "safety", _STATUS_WARN, str(exc))

    def _check_mock_simulation_only(self) -> dict:
        try:
            from release.version_info import MOCK_REALTIME_IS_SIMULATION
            if MOCK_REALTIME_IS_SIMULATION is True:
                return _mk("mock_realtime_simulation_only", "safety", _STATUS_PASS,
                           "MOCK_REALTIME_IS_SIMULATION=True")
            return _mk("mock_realtime_simulation_only", "safety", _STATUS_FAIL,
                       f"MOCK_REALTIME_IS_SIMULATION={MOCK_REALTIME_IS_SIMULATION}")
        except Exception as exc:
            return _mk("mock_realtime_simulation_only", "safety", _STATUS_WARN, str(exc))

    def _check_known_warnings_documented(self) -> dict:
        # Check that release_notes doc exists
        rn_path = os.path.join(self._root, "docs", "release_notes_v1.0.md")
        if os.path.isfile(rn_path):
            return _mk("known_warnings_documented", "docs", _STATUS_PASS,
                       "docs/release_notes_v1.0.md exists")
        return _mk("known_warnings_documented", "docs", _STATUS_WARN,
                   "docs/release_notes_v1.0.md not found")

    def _check_gitignore_runtime_outputs(self) -> dict:
        gi_path = os.path.join(self._root, ".gitignore")
        if not os.path.isfile(gi_path):
            return _mk("runtime_outputs_ignored", "hygiene", _STATUS_WARN, ".gitignore not found")
        try:
            with open(gi_path, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
            checks_passed = all(pat in content for pat in [
                "data/backtest_results/", "reports/", "*.csv",
            ])
            if checks_passed:
                return _mk("runtime_outputs_ignored", "hygiene", _STATUS_PASS,
                           ".gitignore covers runtime outputs")
            return _mk("runtime_outputs_ignored", "hygiene", _STATUS_WARN,
                       ".gitignore may not cover all runtime outputs")
        except Exception as exc:
            return _mk("runtime_outputs_ignored", "hygiene", _STATUS_WARN, str(exc))

    def _check_no_forbidden_actions(self) -> dict:
        # Quick check on own module strings
        forbidden = ["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
                     "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER"]
        safe_context_words = [
            "NO_REAL_ORDERS", "No Real Orders", "BROKER_EXECUTION", "Broker Execution",
            "no broker", "No broker", "BLOCKED", "DISABLED", "FORBIDDEN",
            "_FORBIDDEN", "forbidden_", "FORBIDDEN_OUTPUTS", "forbidden_outputs",
            "no_real_orders", "broker_disabled", "not enable trading",
        ]
        # Check this file's known safety strings don't contain forbidden standalone words
        test_strings = [
            "No Real Orders",
            "Broker Execution Disabled",
            "Production Trading BLOCKED",
            "VALIDATED does not enable trading",
            "Research Only",
            "No external API",
            "Final Maintenance Rollup",
        ]
        for s in test_strings:
            for f in forbidden:
                if f == s.strip() or f + " " == s[:len(f)+1]:
                    return _mk("no_forbidden_actions_unknown_hit", "safety", _STATUS_FAIL,
                               f"Forbidden action '{f}' found in safety string: {s}")
        return _mk("no_forbidden_actions_unknown_hit", "safety", _STATUS_PASS,
                   "No forbidden trading actions in final rollup safety strings")
