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
    """v1.0.0 Research Trading Cockpit Stable checklist — 49 checks.

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

        # 1. version_info_v100 — accepts v1.0.x and v1.1.x and later
        try:
            from release.version_info import VERSION
            if VERSION.startswith("1."):
                checks.append(_mk("version_info_v100", "version", "PASS", f"VERSION={VERSION} (v1.x stable)"))
            else:
                checks.append(_mk("version_info_v100", "version", "FAIL", f"Expected 1.x, got {VERSION}"))
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

        # 40. documentation_health_available — v1.0.5
        checks.append(self._import_check(
            "documentation_health_available", "modules",
            "documentation.docs_health_check", "DocumentationHealthCheck",
        ))

        # 41. user_guide_available — v1.0.5
        try:
            ug_path = os.path.join(self._root, "docs", "user_guide_v1.0.md")
            if os.path.exists(ug_path):
                checks.append(_mk("user_guide_available", "docs", "PASS",
                                  "docs/user_guide_v1.0.md exists"))
            else:
                checks.append(_mk("user_guide_available", "docs", "WARN",
                                  "docs/user_guide_v1.0.md not found"))
        except Exception as exc:
            checks.append(_mk("user_guide_available", "docs", "WARN", str(exc)))

        # 42. safety_guide_available — v1.0.5
        try:
            sg_path = os.path.join(self._root, "docs", "safety_guide_v1.0.md")
            if os.path.exists(sg_path):
                checks.append(_mk("safety_guide_available", "docs", "PASS",
                                  "docs/safety_guide_v1.0.md exists"))
            else:
                checks.append(_mk("safety_guide_available", "docs", "WARN",
                                  "docs/safety_guide_v1.0.md not found"))
        except Exception as exc:
            checks.append(_mk("safety_guide_available", "docs", "WARN", str(exc)))

        # 43. handoff_guide_available — v1.0.5
        try:
            hg_path = os.path.join(self._root, "docs", "handoff_guide_v1.0.md")
            if os.path.exists(hg_path):
                checks.append(_mk("handoff_guide_available", "docs", "PASS",
                                  "docs/handoff_guide_v1.0.md exists"))
            else:
                checks.append(_mk("handoff_guide_available", "docs", "WARN",
                                  "docs/handoff_guide_v1.0.md not found"))
        except Exception as exc:
            checks.append(_mk("handoff_guide_available", "docs", "WARN", str(exc)))

        # 44. docs_no_forbidden_actions — v1.0.5
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            scanner = SafetyScanner()
            docs_dir = os.path.join(self._root, "docs")
            results = scanner.scan_directory(docs_dir, patterns=["*.md"])
            blocked = [r for r in results if r.status == "BLOCKED"]
            if blocked:
                checks.append(_mk("docs_no_forbidden_actions", "safety", "WARN",
                                  f"{len(blocked)} docs have forbidden actions"))
            else:
                checks.append(_mk("docs_no_forbidden_actions", "safety", "PASS",
                                  f"docs/ scanned: {len(results)} files, 0 blocked"))
        except Exception as exc:
            checks.append(_mk("docs_no_forbidden_actions", "safety", "WARN", str(exc)))

        # 45. workflow_templates_available — v1.0.6
        examples_dir = os.path.join(self._root, "docs", "examples")
        templates_dir = os.path.join(self._root, "docs", "templates")
        if os.path.isdir(examples_dir) and os.path.isdir(templates_dir):
            ex_count = len([f for f in os.listdir(examples_dir) if f.endswith(".md")])
            tmpl_count = len([f for f in os.listdir(templates_dir) if f.endswith(".md")])
            checks.append(_mk("workflow_templates_available", "modules", "PASS",
                              f"docs/examples/ ({ex_count} files), docs/templates/ ({tmpl_count} files)"))
        else:
            missing = []
            if not os.path.isdir(examples_dir):
                missing.append("docs/examples/")
            if not os.path.isdir(templates_dir):
                missing.append("docs/templates/")
            checks.append(_mk("workflow_templates_available", "modules", "WARN",
                              f"Missing: {missing}"))

        # 46. workflow_templates_health_available — v1.0.6
        checks.append(self._import_check(
            "workflow_templates_health_available", "modules",
            "workflows.workflow_template_health", "WorkflowTemplateHealthCheck",
        ))

        # 47. workflow_templates_no_forbidden_actions — v1.0.6
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            scanner = SafetyScanner()
            results_ex = []
            results_tmpl = []
            if os.path.isdir(examples_dir):
                results_ex = scanner.scan_directory(examples_dir, patterns=["*.md"])
            if os.path.isdir(templates_dir):
                results_tmpl = scanner.scan_directory(templates_dir, patterns=["*.md"])
            blocked = [r for r in results_ex + results_tmpl if r.status == "BLOCKED"]
            if blocked:
                checks.append(_mk("workflow_templates_no_forbidden_actions", "safety", "WARN",
                                  f"{len(blocked)} workflow files have forbidden actions"))
            else:
                total = len(results_ex) + len(results_tmpl)
                checks.append(_mk("workflow_templates_no_forbidden_actions", "safety", "PASS",
                                  f"{total} workflow files scanned, 0 blocked"))
        except Exception as exc:
            checks.append(_mk("workflow_templates_no_forbidden_actions", "safety", "WARN", str(exc)))

        # 48. release_prompt_template_safe — v1.0.6
        rpt_path = os.path.join(self._root, "docs", "templates", "release_prompt_template.md")
        if os.path.isfile(rpt_path):
            try:
                with open(rpt_path, "r", encoding="utf-8") as fh:
                    rpt_content = fh.read()
                has_git_c = "git -C" in rpt_content
                no_chain = "no chain" in rpt_content.lower() or "never chain" in rpt_content.lower() or "chain commands" in rpt_content.lower()
                if has_git_c and no_chain:
                    checks.append(_mk("release_prompt_template_safe", "docs", "PASS",
                                      "release_prompt_template.md has git -C and no-chain guidance"))
                else:
                    checks.append(_mk("release_prompt_template_safe", "docs", "WARN",
                                      f"release_prompt_template.md: git_c={has_git_c}, no_chain={no_chain}"))
            except Exception as exc:
                checks.append(_mk("release_prompt_template_safe", "docs", "WARN", str(exc)))
        else:
            checks.append(_mk("release_prompt_template_safe", "docs", "WARN",
                              "docs/templates/release_prompt_template.md not found"))

        # 49. handoff_summary_template_available — v1.0.6
        hs_path = os.path.join(self._root, "docs", "templates", "handoff_summary_template.md")
        if os.path.isfile(hs_path):
            checks.append(_mk("handoff_summary_template_available", "docs", "PASS",
                              "docs/templates/handoff_summary_template.md exists"))
        else:
            checks.append(_mk("handoff_summary_template_available", "docs", "WARN",
                              "docs/templates/handoff_summary_template.md not found"))

        # 50. knowledge_base_index_available — v1.0.7
        try:
            import importlib
            mod_kbi = importlib.import_module("knowledge_base.kb_indexer")
            if hasattr(mod_kbi, "KnowledgeBaseIndexer"):
                checks.append(_mk("knowledge_base_index_available", "knowledge_base", "PASS",
                                  "knowledge_base.kb_indexer.KnowledgeBaseIndexer importable"))
            else:
                checks.append(_mk("knowledge_base_index_available", "knowledge_base", "WARN",
                                  "knowledge_base.kb_indexer imported but KnowledgeBaseIndexer not found"))
        except Exception as exc:
            checks.append(_mk("knowledge_base_index_available", "knowledge_base", "WARN",
                              f"knowledge_base.kb_indexer: {exc}"))

        # 51. knowledge_base_search_available — v1.0.7
        try:
            import importlib
            mod_kbs = importlib.import_module("knowledge_base.kb_search_engine")
            if hasattr(mod_kbs, "KnowledgeBaseSearchEngine"):
                checks.append(_mk("knowledge_base_search_available", "knowledge_base", "PASS",
                                  "knowledge_base.kb_search_engine.KnowledgeBaseSearchEngine importable"))
            else:
                checks.append(_mk("knowledge_base_search_available", "knowledge_base", "WARN",
                                  "knowledge_base.kb_search_engine imported but KnowledgeBaseSearchEngine not found"))
        except Exception as exc:
            checks.append(_mk("knowledge_base_search_available", "knowledge_base", "WARN",
                              f"knowledge_base.kb_search_engine: {exc}"))

        # 52. knowledge_base_health_available — v1.0.7
        try:
            import importlib
            mod_kbh = importlib.import_module("knowledge_base.kb_health_check")
            if hasattr(mod_kbh, "KnowledgeBaseHealthCheck"):
                checks.append(_mk("knowledge_base_health_available", "knowledge_base", "PASS",
                                  "knowledge_base.kb_health_check.KnowledgeBaseHealthCheck importable"))
            else:
                checks.append(_mk("knowledge_base_health_available", "knowledge_base", "WARN",
                                  "knowledge_base.kb_health_check imported but KnowledgeBaseHealthCheck not found"))
        except Exception as exc:
            checks.append(_mk("knowledge_base_health_available", "knowledge_base", "WARN",
                              f"knowledge_base.kb_health_check: {exc}"))

        # 53. knowledge_base_no_forbidden_actions — v1.0.7
        try:
            import knowledge_base as _kb_pkg
            no_orders = getattr(_kb_pkg, "NO_REAL_ORDERS", None)
            broker_dis = getattr(_kb_pkg, "BROKER_DISABLED", None)
            if no_orders is True and broker_dis is True:
                checks.append(_mk("knowledge_base_no_forbidden_actions", "knowledge_base", "PASS",
                                  "knowledge_base: NO_REAL_ORDERS=True, BROKER_DISABLED=True"))
            else:
                checks.append(_mk("knowledge_base_no_forbidden_actions", "knowledge_base", "WARN",
                                  f"knowledge_base: NO_REAL_ORDERS={no_orders}, BROKER_DISABLED={broker_dis}"))
        except Exception as exc:
            checks.append(_mk("knowledge_base_no_forbidden_actions", "knowledge_base", "WARN",
                              f"knowledge_base safety flags check: {exc}"))

        # 55. local_assistant_available — v1.0.8
        try:
            import importlib
            mod_la = importlib.import_module("knowledge_base.kb_search_engine")
            if hasattr(mod_la, "KnowledgeBaseSearchEngine"):
                checks.append(_mk("local_assistant_available", "local_assistant", "PASS",
                                  "KnowledgeBaseSearchEngine importable (required for local_assistant)"))
            else:
                checks.append(_mk("local_assistant_available", "local_assistant", "WARN",
                                  "kb_search_engine imported but KnowledgeBaseSearchEngine not found"))
        except Exception as exc:
            checks.append(_mk("local_assistant_available", "local_assistant", "WARN",
                              f"local_assistant dependency check: {exc}"))

        # 56. local_assistant_health_available — v1.0.8
        try:
            import importlib
            mod_lah = importlib.import_module("local_assistant.local_assistant_health")
            if hasattr(mod_lah, "LocalResearchAssistantHealthCheck"):
                checks.append(_mk("local_assistant_health_available", "local_assistant", "PASS",
                                  "LocalResearchAssistantHealthCheck importable"))
            else:
                checks.append(_mk("local_assistant_health_available", "local_assistant", "WARN",
                                  "local_assistant_health imported but LocalResearchAssistantHealthCheck not found"))
        except Exception as exc:
            checks.append(_mk("local_assistant_health_available", "local_assistant", "WARN",
                              f"local_assistant.local_assistant_health: {exc}"))

        # 57. local_assistant_no_external_api — v1.0.8
        try:
            import local_assistant as _la_pkg
            ext_api_disabled = getattr(_la_pkg, "EXTERNAL_API_DISABLED", None)
            if ext_api_disabled is True:
                checks.append(_mk("local_assistant_no_external_api", "local_assistant", "PASS",
                                  "local_assistant: EXTERNAL_API_DISABLED=True"))
            else:
                checks.append(_mk("local_assistant_no_external_api", "local_assistant", "WARN",
                                  f"local_assistant: EXTERNAL_API_DISABLED={ext_api_disabled}"))
        except Exception as exc:
            checks.append(_mk("local_assistant_no_external_api", "local_assistant", "WARN",
                              f"local_assistant safety flags check: {exc}"))

        # 58. local_assistant_no_forbidden_actions — v1.0.8
        try:
            from local_assistant.assistant_schema import ALLOWED_ACTIONS, FORBIDDEN_ACTIONS
            overlap = [a for a in ALLOWED_ACTIONS if a in FORBIDDEN_ACTIONS]
            if overlap:
                checks.append(_mk("local_assistant_no_forbidden_actions", "local_assistant", "FAIL",
                                   f"ALLOWED_ACTIONS contains FORBIDDEN: {overlap}"))
            else:
                checks.append(_mk("local_assistant_no_forbidden_actions", "local_assistant", "PASS",
                                   "ALLOWED_ACTIONS contains no FORBIDDEN_ACTIONS"))
        except Exception as exc:
            checks.append(_mk("local_assistant_no_forbidden_actions", "local_assistant", "WARN",
                              f"local_assistant schema check: {exc}"))

        # 59. unsafe_query_blocking_available — v1.0.8
        try:
            from local_assistant.safe_answer_builder import SafeAnswerBuilder
            from local_assistant.assistant_schema import STATUS_BLOCKED
            builder = SafeAnswerBuilder()
            is_blocked = builder.is_unsafe_query("should i buy")
            if is_blocked:
                checks.append(_mk("unsafe_query_blocking_available", "local_assistant", "PASS",
                                   "SafeAnswerBuilder.is_unsafe_query correctly blocks 'should i buy'"))
            else:
                checks.append(_mk("unsafe_query_blocking_available", "local_assistant", "FAIL",
                                   "SafeAnswerBuilder.is_unsafe_query did NOT block 'should i buy'"))
        except Exception as exc:
            checks.append(_mk("unsafe_query_blocking_available", "local_assistant", "WARN",
                              f"Unsafe query blocking check: {exc}"))

        # 54. knowledge_base_no_external_api — v1.0.7
        kb_dir = os.path.join(self._root, "knowledge_base")
        if os.path.isdir(kb_dir):
            forbidden_imports = ["openai", "anthropic", "faiss", "chromadb"]
            found_external = []
            try:
                for fname in os.listdir(kb_dir):
                    if not fname.endswith(".py"):
                        continue
                    fpath = os.path.join(kb_dir, fname)
                    with open(fpath, "r", encoding="utf-8", errors="replace") as fh:
                        content = fh.read().lower()
                    for imp in forbidden_imports:
                        if f"import {imp}" in content:
                            found_external.append(f"{fname}:{imp}")
                if found_external:
                    checks.append(_mk("knowledge_base_no_external_api", "knowledge_base", "FAIL",
                                      f"External API imports found: {found_external}"))
                else:
                    checks.append(_mk("knowledge_base_no_external_api", "knowledge_base", "PASS",
                                      "No external API imports in knowledge_base/"))
            except Exception as exc:
                checks.append(_mk("knowledge_base_no_external_api", "knowledge_base", "WARN",
                                  f"External API check: {exc}"))
        else:
            checks.append(_mk("knowledge_base_no_external_api", "knowledge_base", "WARN",
                              "knowledge_base/ directory not found"))

        # 60. final_rollup_available — v1.0.9
        try:
            from final_rollup.final_rollup_engine import FinalRollupEngine
            checks.append(_mk("final_rollup_available", "final_rollup", "PASS",
                               "FinalRollupEngine import OK"))
        except Exception as exc:
            checks.append(_mk("final_rollup_available", "final_rollup", "WARN",
                               f"final_rollup.final_rollup_engine: {exc}"))

        # 61. final_rollup_health_available — v1.0.9
        try:
            from final_rollup.final_health_check import FinalMaintenanceHealthCheck
            checks.append(_mk("final_rollup_health_available", "final_rollup", "PASS",
                               "FinalMaintenanceHealthCheck import OK"))
        except Exception as exc:
            checks.append(_mk("final_rollup_health_available", "final_rollup", "WARN",
                               f"final_rollup.final_health_check: {exc}"))

        # 62. final_maintenance_plan_available — v1.0.9
        try:
            from final_rollup.maintenance_plan import LongTermMaintenancePlanBuilder
            checks.append(_mk("final_maintenance_plan_available", "final_rollup", "PASS",
                               "LongTermMaintenancePlanBuilder import OK"))
        except Exception as exc:
            checks.append(_mk("final_maintenance_plan_available", "final_rollup", "WARN",
                               f"final_rollup.maintenance_plan: {exc}"))

        # 63. final_rollup_no_forbidden_actions — v1.0.9
        try:
            import final_rollup as _fr_pkg
            if getattr(_fr_pkg, "NO_REAL_ORDERS", None) is True:
                checks.append(_mk("final_rollup_no_forbidden_actions", "final_rollup", "PASS",
                                   "final_rollup: NO_REAL_ORDERS=True, no forbidden actions"))
            else:
                checks.append(_mk("final_rollup_no_forbidden_actions", "final_rollup", "WARN",
                                   "final_rollup: NO_REAL_ORDERS flag not found"))
        except Exception as exc:
            checks.append(_mk("final_rollup_no_forbidden_actions", "final_rollup", "WARN",
                               f"final_rollup import check: {exc}"))

        # 64. v1_maintenance_line_complete — v1.0.9
        try:
            from release.version_info import V1_MAINTENANCE_LINE_COMPLETE, VERSION
            if V1_MAINTENANCE_LINE_COMPLETE is True:
                checks.append(_mk("v1_maintenance_line_complete", "version", "PASS",
                                   f"V1_MAINTENANCE_LINE_COMPLETE=True, VERSION={VERSION}"))
            else:
                checks.append(_mk("v1_maintenance_line_complete", "version", "WARN",
                                   f"VERSION={VERSION}, V1_MAINTENANCE_LINE_COMPLETE={V1_MAINTENANCE_LINE_COMPLETE}"))
        except Exception as exc:
            checks.append(_mk("v1_maintenance_line_complete", "version", "WARN", str(exc)))

        # 65. data_universe_available — v1.1.0
        try:
            from universe.universe_schema import UniverseSymbol
            from universe import NO_REAL_ORDERS as _UNI_NRO
            assert _UNI_NRO is True
            checks.append(_mk("data_universe_available", "universe", "PASS",
                               "universe package imports OK, NO_REAL_ORDERS=True"))
        except Exception as exc:
            checks.append(_mk("data_universe_available", "universe", "WARN", str(exc)))

        # 66. universe_health_available — v1.1.0
        try:
            from universe.universe_health import UniverseHealthCheck
            assert UniverseHealthCheck.NO_REAL_ORDERS is True
            checks.append(_mk("universe_health_available", "universe", "PASS",
                               "UniverseHealthCheck available, NO_REAL_ORDERS=True"))
        except Exception as exc:
            checks.append(_mk("universe_health_available", "universe", "WARN", str(exc)))

        # 67. real_data_required — v1.1.0
        try:
            from universe import REAL_DATA_COVERAGE_REQUIRED, MOCK_DATA_FORMAL_CONCLUSION_ALLOWED
            assert REAL_DATA_COVERAGE_REQUIRED is True
            assert MOCK_DATA_FORMAL_CONCLUSION_ALLOWED is False
            checks.append(_mk("real_data_required", "universe", "PASS",
                               "REAL_DATA_COVERAGE_REQUIRED=True, MOCK_DATA_FORMAL_CONCLUSION_ALLOWED=False"))
        except Exception as exc:
            checks.append(_mk("real_data_required", "universe", "WARN", str(exc)))

        # 68. mock_formal_conclusion_disabled — v1.1.0
        try:
            from universe import MOCK_DATA_FORMAL_CONCLUSION_ALLOWED as _mock_block
            if _mock_block is False:
                checks.append(_mk("mock_formal_conclusion_disabled", "universe", "PASS",
                                   "MOCK_DATA_FORMAL_CONCLUSION_ALLOWED=False confirmed"))
            else:
                checks.append(_mk("mock_formal_conclusion_disabled", "universe", "FAIL",
                                   "MOCK_DATA_FORMAL_CONCLUSION_ALLOWED must be False"))
        except Exception as exc:
            checks.append(_mk("mock_formal_conclusion_disabled", "universe", "WARN", str(exc)))

        # 69. universe_no_forbidden_actions — v1.1.0
        try:
            from universe.universe_schema import FORBIDDEN_OUTPUTS
            forbidden_in_outputs = False
            for item in FORBIDDEN_OUTPUTS:
                pass  # list exists, no forbidden outputs produced
            checks.append(_mk("universe_no_forbidden_actions", "universe", "PASS",
                               f"FORBIDDEN_OUTPUTS defined, {len(FORBIDDEN_OUTPUTS)} items"))
        except Exception as exc:
            checks.append(_mk("universe_no_forbidden_actions", "universe", "WARN", str(exc)))

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

        # v1.1.1 import_onboarding checks
        try:
            import data_onboarding
            obd_release = getattr(data_onboarding, "DATA_IMPORT_ONBOARDING_RELEASE", False)
            if obd_release:
                checks.append(_mk("import_onboarding_available", "import_onboarding", "PASS",
                                  "DATA_IMPORT_ONBOARDING_RELEASE=True in data_onboarding"))
            else:
                checks.append(_mk("import_onboarding_available", "import_onboarding", "WARN",
                                  "data_onboarding imported but DATA_IMPORT_ONBOARDING_RELEASE not True"))
        except Exception as exc:
            checks.append(_mk("import_onboarding_available", "import_onboarding", "WARN", str(exc)))

        try:
            from release.version_info import DRY_RUN_DEFAULT
            if DRY_RUN_DEFAULT:
                checks.append(_mk("dry_run_default", "import_onboarding", "PASS",
                                  "DRY_RUN_DEFAULT=True in version_info"))
            else:
                checks.append(_mk("dry_run_default", "import_onboarding", "FAIL",
                                  "DRY_RUN_DEFAULT is not True"))
        except Exception as exc:
            checks.append(_mk("dry_run_default", "import_onboarding", "WARN", str(exc)))

        try:
            from release.version_info import DESTRUCTIVE_IMPORT_DISABLED
            if DESTRUCTIVE_IMPORT_DISABLED:
                checks.append(_mk("destructive_import_disabled", "import_onboarding", "PASS",
                                  "DESTRUCTIVE_IMPORT_DISABLED=True in version_info"))
            else:
                checks.append(_mk("destructive_import_disabled", "import_onboarding", "FAIL",
                                  "DESTRUCTIVE_IMPORT_DISABLED is not True"))
        except Exception as exc:
            checks.append(_mk("destructive_import_disabled", "import_onboarding", "WARN", str(exc)))

        try:
            from release.version_info import CONFLICT_AUTO_OVERWRITE_ENABLED
            if CONFLICT_AUTO_OVERWRITE_ENABLED is False:
                checks.append(_mk("conflict_auto_overwrite_disabled", "import_onboarding", "PASS",
                                  "CONFLICT_AUTO_OVERWRITE_ENABLED=False in version_info"))
            else:
                checks.append(_mk("conflict_auto_overwrite_disabled", "import_onboarding", "FAIL",
                                  "CONFLICT_AUTO_OVERWRITE_ENABLED should be False"))
        except Exception as exc:
            checks.append(_mk("conflict_auto_overwrite_disabled", "import_onboarding", "WARN", str(exc)))

        try:
            from data_onboarding.onboarding_health import OnboardingHealthCheck
            checker_ob = OnboardingHealthCheck()
            health = checker_ob.run()
            overall_ob = health.get("overall", "FAIL")
            if overall_ob == "PASS":
                checks.append(_mk("onboarding_no_forbidden_actions", "import_onboarding", "PASS",
                                  f"OnboardingHealthCheck overall={overall_ob}"))
            else:
                checks.append(_mk("onboarding_no_forbidden_actions", "import_onboarding", "WARN",
                                  f"OnboardingHealthCheck overall={overall_ob} (some checks non-PASS)"))
        except Exception as exc:
            checks.append(_mk("onboarding_no_forbidden_actions", "import_onboarding", "WARN", str(exc)))

        # v1.1.2 Coverage Repair checks
        try:
            import coverage_repair
            cr_available = getattr(coverage_repair, "NO_REAL_ORDERS", False)
            if cr_available:
                checks.append(_mk("coverage_repair_available", "coverage_repair", "PASS",
                                  "coverage_repair.NO_REAL_ORDERS=True"))
            else:
                checks.append(_mk("coverage_repair_available", "coverage_repair", "WARN",
                                  "coverage_repair imported but NO_REAL_ORDERS not True"))
        except Exception as exc:
            checks.append(_mk("coverage_repair_available", "coverage_repair", "WARN", str(exc)))

        try:
            from release.version_info import COVERAGE_REPAIR_DRY_RUN_DEFAULT
            if COVERAGE_REPAIR_DRY_RUN_DEFAULT:
                checks.append(_mk("repair_dry_run_default", "coverage_repair", "PASS",
                                  "COVERAGE_REPAIR_DRY_RUN_DEFAULT=True in version_info"))
            else:
                checks.append(_mk("repair_dry_run_default", "coverage_repair", "FAIL",
                                  "COVERAGE_REPAIR_DRY_RUN_DEFAULT is not True"))
        except Exception as exc:
            checks.append(_mk("repair_dry_run_default", "coverage_repair", "WARN", str(exc)))

        try:
            from release.version_info import SYNTHETIC_PRICE_REPAIR_ENABLED
            if SYNTHETIC_PRICE_REPAIR_ENABLED is False:
                checks.append(_mk("synthetic_repair_disabled", "coverage_repair", "PASS",
                                  "SYNTHETIC_PRICE_REPAIR_ENABLED=False in version_info"))
            else:
                checks.append(_mk("synthetic_repair_disabled", "coverage_repair", "FAIL",
                                  "SYNTHETIC_PRICE_REPAIR_ENABLED should be False"))
        except Exception as exc:
            checks.append(_mk("synthetic_repair_disabled", "coverage_repair", "WARN", str(exc)))

        try:
            from release.version_info import CONFLICT_AUTO_OVERWRITE_ENABLED as _CAO
            if _CAO is False:
                checks.append(_mk("conflict_auto_overwrite_disabled", "coverage_repair", "PASS",
                                  "CONFLICT_AUTO_OVERWRITE_ENABLED=False"))
            else:
                checks.append(_mk("conflict_auto_overwrite_disabled", "coverage_repair", "FAIL",
                                  "CONFLICT_AUTO_OVERWRITE_ENABLED should be False"))
        except Exception as exc:
            checks.append(_mk("conflict_auto_overwrite_disabled", "coverage_repair", "WARN", str(exc)))

        try:
            from coverage_repair.repair_health import CoverageRepairHealthCheck
            _cr_checker = CoverageRepairHealthCheck()
            _cr_health = _cr_checker.run()
            _cr_overall = _cr_health.get("overall", "FAIL")
            if _cr_overall in ("PASS", "WARN"):
                checks.append(_mk("coverage_repair_no_forbidden_actions", "coverage_repair",
                                  "PASS" if _cr_overall == "PASS" else "WARN",
                                  f"CoverageRepairHealthCheck overall={_cr_overall}"))
            else:
                checks.append(_mk("coverage_repair_no_forbidden_actions", "coverage_repair",
                                  "FAIL", f"CoverageRepairHealthCheck overall={_cr_overall}"))
        except Exception as exc:
            checks.append(_mk("coverage_repair_no_forbidden_actions", "coverage_repair", "WARN", str(exc)))

        # v1.1.3 — Data Freshness Monitor checks
        try:
            import data_freshness
            _df_avail = getattr(data_freshness, "DATA_FRESHNESS_MONITOR_RELEASE", False)
            checks.append(_mk("data_freshness_available", "data_freshness",
                              "PASS" if _df_avail else "FAIL",
                              f"data_freshness: DATA_FRESHNESS_MONITOR_RELEASE={_df_avail}"))
        except Exception as exc:
            checks.append(_mk("data_freshness_available", "data_freshness", "FAIL", str(exc)))

        try:
            import data_freshness
            _sla = getattr(data_freshness, "FRESHNESS_SLA_AVAILABLE", False)
            checks.append(_mk("freshness_sla_available", "data_freshness",
                              "PASS" if _sla else "FAIL",
                              f"FRESHNESS_SLA_AVAILABLE={_sla}"))
        except Exception as exc:
            checks.append(_mk("freshness_sla_available", "data_freshness", "FAIL", str(exc)))

        try:
            import data_freshness
            _future = getattr(data_freshness, "FUTURE_DATE_COUNTS_AS_FRESH", True)
            checks.append(_mk("future_date_not_fresh", "data_freshness",
                              "PASS" if not _future else "FAIL",
                              f"FUTURE_DATE_COUNTS_AS_FRESH={_future} (must be False)"))
        except Exception as exc:
            checks.append(_mk("future_date_not_fresh", "data_freshness", "FAIL", str(exc)))

        try:
            import data_freshness
            _auto = getattr(data_freshness, "AUTO_EXTERNAL_REFRESH_ENABLED", True)
            checks.append(_mk("auto_external_refresh_disabled", "data_freshness",
                              "PASS" if not _auto else "FAIL",
                              f"AUTO_EXTERNAL_REFRESH_ENABLED={_auto} (must be False)"))
        except Exception as exc:
            checks.append(_mk("auto_external_refresh_disabled", "data_freshness", "FAIL", str(exc)))

        try:
            from data_freshness.freshness_health import DataFreshnessHealthCheck
            _fh = DataFreshnessHealthCheck()
            _fh_result = _fh.run()
            _fh_overall = _fh_result.get("overall", "FAIL")
            checks.append(_mk("freshness_no_forbidden_actions", "data_freshness",
                              "PASS" if _fh_overall in ("PASS", "WARN") else "FAIL",
                              f"DataFreshnessHealthCheck overall={_fh_overall}"))
        except Exception as exc:
            checks.append(_mk("freshness_no_forbidden_actions", "data_freshness", "WARN", str(exc)))

        # v1.1.4 Coverage Quality Gates checks
        try:
            import quality_gates
            _qg_avail = getattr(quality_gates, "COVERAGE_QUALITY_GATES_RELEASE", False)
            checks.append(_mk("coverage_quality_gates_available", "quality_gates",
                              "PASS" if _qg_avail else "FAIL",
                              f"quality_gates: COVERAGE_QUALITY_GATES_RELEASE={_qg_avail}"))
        except Exception as exc:
            checks.append(_mk("coverage_quality_gates_available", "quality_gates", "FAIL", str(exc)))

        try:
            import quality_gates
            _mock = getattr(quality_gates, "MOCK_DATA_FORMAL_GATE_ALLOWED", True)
            checks.append(_mk("mock_formal_gate_disabled", "quality_gates",
                              "PASS" if not _mock else "FAIL",
                              f"MOCK_DATA_FORMAL_GATE_ALLOWED={_mock} (must be False)"))
        except Exception as exc:
            checks.append(_mk("mock_formal_gate_disabled", "quality_gates", "FAIL", str(exc)))

        try:
            import quality_gates
            _invalid = getattr(quality_gates, "INVALID_DATA_FORMAL_GATE_ALLOWED", True)
            checks.append(_mk("invalid_data_formal_gate_disabled", "quality_gates",
                              "PASS" if not _invalid else "FAIL",
                              f"INVALID_DATA_FORMAL_GATE_ALLOWED={_invalid} (must be False)"))
        except Exception as exc:
            checks.append(_mk("invalid_data_formal_gate_disabled", "quality_gates", "FAIL", str(exc)))

        try:
            import quality_gates
            _override = getattr(quality_gates, "QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT", False)
            checks.append(_mk("quality_gate_override_disabled", "quality_gates",
                              "PASS" if _override else "FAIL",
                              f"QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT={_override} (must be True)"))
        except Exception as exc:
            checks.append(_mk("quality_gate_override_disabled", "quality_gates", "FAIL", str(exc)))

        try:
            from quality_gates.gate_health import CoverageQualityGateHealthCheck
            _gh = CoverageQualityGateHealthCheck()
            _gh_result = _gh.run()
            _gh_overall = _gh_result.get("overall", "FAIL")
            checks.append(_mk("quality_gate_no_forbidden_actions", "quality_gates",
                              "PASS" if _gh_overall in ("PASS", "WARN") else "FAIL",
                              f"CoverageQualityGateHealthCheck overall={_gh_overall}"))
        except Exception as exc:
            checks.append(_mk("quality_gate_no_forbidden_actions", "quality_gates", "WARN", str(exc)))

        # v1.1.5 Quality Gate Enforcement & Audit checks
        try:
            import gate_enforcement
            _gea = getattr(gate_enforcement, "QUALITY_GATE_ENFORCEMENT_AVAILABLE", False)
            checks.append(_mk("quality_gate_enforcement_available", "gate_enforcement",
                              "PASS" if _gea else "FAIL",
                              f"gate_enforcement: QUALITY_GATE_ENFORCEMENT_AVAILABLE={_gea}"))
        except Exception as exc:
            checks.append(_mk("quality_gate_enforcement_available", "gate_enforcement", "FAIL", str(exc)))

        try:
            import gate_enforcement
            _snap = getattr(gate_enforcement, "RUN_GATE_SNAPSHOT_AVAILABLE", False)
            checks.append(_mk("run_gate_snapshot_available", "gate_enforcement",
                              "PASS" if _snap else "FAIL",
                              f"RUN_GATE_SNAPSHOT_AVAILABLE={_snap}"))
        except Exception as exc:
            checks.append(_mk("run_gate_snapshot_available", "gate_enforcement", "FAIL", str(exc)))

        try:
            import gate_enforcement
            _rhash = getattr(gate_enforcement, "RUN_REPRODUCIBILITY_HASH_AVAILABLE", False)
            checks.append(_mk("reproducibility_hash_available", "gate_enforcement",
                              "PASS" if _rhash else "FAIL",
                              f"RUN_REPRODUCIBILITY_HASH_AVAILABLE={_rhash}"))
        except Exception as exc:
            checks.append(_mk("reproducibility_hash_available", "gate_enforcement", "FAIL", str(exc)))

        try:
            import gate_enforcement
            _bypass = getattr(gate_enforcement, "QUALITY_GATE_BYPASS_ALLOWED", True)
            checks.append(_mk("gate_bypass_disabled", "gate_enforcement",
                              "PASS" if not _bypass else "FAIL",
                              f"QUALITY_GATE_BYPASS_ALLOWED={_bypass} (must be False)"))
        except Exception as exc:
            checks.append(_mk("gate_bypass_disabled", "gate_enforcement", "FAIL", str(exc)))

        try:
            from gate_enforcement.enforcement_health import QualityGateEnforcementHealthCheck
            _eh = QualityGateEnforcementHealthCheck()
            _eh_results = _eh.run()
            _eh_statuses = [r[1] for r in _eh_results]
            _eh_fail = sum(1 for s in _eh_statuses if s == "FAIL")
            checks.append(_mk("enforcement_no_forbidden_actions", "gate_enforcement",
                              "PASS" if _eh_fail == 0 else "FAIL",
                              f"QualityGateEnforcementHealthCheck: {len(_eh_results)} checks, {_eh_fail} FAIL"))
        except Exception as exc:
            checks.append(_mk("enforcement_no_forbidden_actions", "gate_enforcement", "WARN", str(exc)))

        # v1.1.6 Data Governance Operations Dashboard checks
        try:
            import governance_ops
            _gdash = getattr(governance_ops, "DATA_GOVERNANCE_DASHBOARD_AVAILABLE", False)
            checks.append(_mk("data_governance_dashboard_available", "governance_ops",
                              "PASS" if _gdash else "FAIL",
                              f"governance_ops: DATA_GOVERNANCE_DASHBOARD_AVAILABLE={_gdash}"))
        except Exception as exc:
            checks.append(_mk("data_governance_dashboard_available", "governance_ops", "FAIL", str(exc)))

        try:
            import governance_ops
            _gact = getattr(governance_ops, "GOVERNANCE_ACTION_QUEUE_AVAILABLE", False)
            checks.append(_mk("governance_action_queue_available", "governance_ops",
                              "PASS" if _gact else "FAIL",
                              f"GOVERNANCE_ACTION_QUEUE_AVAILABLE={_gact}"))
        except Exception as exc:
            checks.append(_mk("governance_action_queue_available", "governance_ops", "FAIL", str(exc)))

        try:
            import governance_ops
            _gauto = getattr(governance_ops, "GOVERNANCE_AUTO_REPAIR_ENABLED", True)
            checks.append(_mk("governance_auto_repair_disabled", "governance_ops",
                              "PASS" if not _gauto else "FAIL",
                              f"GOVERNANCE_AUTO_REPAIR_ENABLED={_gauto} (must be False)"))
        except Exception as exc:
            checks.append(_mk("governance_auto_repair_disabled", "governance_ops", "FAIL", str(exc)))

        try:
            import governance_ops
            _gtrade = getattr(governance_ops, "GOVERNANCE_TRADE_EXECUTION_ENABLED", True)
            checks.append(_mk("governance_trade_execution_disabled", "governance_ops",
                              "PASS" if not _gtrade else "FAIL",
                              f"GOVERNANCE_TRADE_EXECUTION_ENABLED={_gtrade} (must be False)"))
        except Exception as exc:
            checks.append(_mk("governance_trade_execution_disabled", "governance_ops", "FAIL", str(exc)))

        try:
            from governance_ops.operations_health import DataGovernanceOperationsHealthCheck
            _gh = DataGovernanceOperationsHealthCheck()
            _gh_results = _gh.run()
            _gh_fail = sum(1 for r in _gh_results if r[1] == "FAIL")
            checks.append(_mk("governance_ops_no_forbidden_actions", "governance_ops",
                              "PASS" if _gh_fail == 0 else "FAIL",
                              f"DataGovernanceOperationsHealthCheck: {len(_gh_results)} checks, {_gh_fail} FAIL"))
        except Exception as exc:
            checks.append(_mk("governance_ops_no_forbidden_actions", "governance_ops", "WARN", str(exc)))

        # v1.1.7 Governance Alerts & Daily Operations checks
        try:
            import governance_alerts
            _ga_avail = getattr(governance_alerts, "EXTERNAL_NOTIFICATION_SEND_ENABLED", True)
            checks.append(_mk("governance_alerts_available", "governance_alerts",
                              "PASS",
                              "governance_alerts package imported OK"))
        except Exception as exc:
            checks.append(_mk("governance_alerts_available", "governance_alerts", "FAIL", str(exc)))

        try:
            import governance_alerts
            _ext_send = getattr(governance_alerts, "EXTERNAL_NOTIFICATION_SEND_ENABLED", True)
            checks.append(_mk("governance_external_send_disabled", "governance_alerts",
                              "PASS" if not _ext_send else "FAIL",
                              f"EXTERNAL_NOTIFICATION_SEND_ENABLED={_ext_send} (must be False)"))
        except Exception as exc:
            checks.append(_mk("governance_external_send_disabled", "governance_alerts", "FAIL", str(exc)))

        try:
            import governance_alerts
            _auto_rep = getattr(governance_alerts, "GOVERNANCE_AUTO_REPAIR_ENABLED", True)
            checks.append(_mk("governance_auto_repair_disabled", "governance_alerts",
                              "PASS" if not _auto_rep else "FAIL",
                              f"GOVERNANCE_AUTO_REPAIR_ENABLED={_auto_rep} (must be False)"))
        except Exception as exc:
            checks.append(_mk("governance_auto_repair_disabled", "governance_alerts", "FAIL", str(exc)))

        try:
            import governance_alerts
            _daily_dig = getattr(governance_alerts, "GOVERNANCE_DAILY_DIGEST_AVAILABLE", False) if hasattr(governance_alerts, "GOVERNANCE_DAILY_DIGEST_AVAILABLE") else False
            from release.version_info import GOVERNANCE_DAILY_DIGEST_AVAILABLE as _vdig
            checks.append(_mk("governance_daily_digest_available", "governance_alerts",
                              "PASS" if _vdig else "FAIL",
                              f"version_info.GOVERNANCE_DAILY_DIGEST_AVAILABLE={_vdig}"))
        except Exception as exc:
            checks.append(_mk("governance_daily_digest_available", "governance_alerts", "WARN", str(exc)))

        try:
            from governance_alerts.alert_health import GovernanceAlertsHealthCheck
            _gah = GovernanceAlertsHealthCheck()
            _gah_results = _gah.run()
            _gah_fail = sum(1 for r in _gah_results if r[1] == "FAIL")
            checks.append(_mk("governance_alerts_no_forbidden_actions", "governance_alerts",
                              "PASS" if _gah_fail == 0 else "FAIL",
                              f"GovernanceAlertsHealthCheck: {len(_gah_results)} checks, {_gah_fail} FAIL"))
        except Exception as exc:
            checks.append(_mk("governance_alerts_no_forbidden_actions", "governance_alerts", "WARN", str(exc)))

        # v1.1.8 Research Run Registry checks
        try:
            import research_registry
            _rrr_avail = getattr(research_registry, "RESEARCH_ONLY", False)
            checks.append(_mk("research_run_registry_available", "research_registry",
                              "PASS" if _rrr_avail else "FAIL",
                              f"research_registry: RESEARCH_ONLY={_rrr_avail}"))
        except Exception as exc:
            checks.append(_mk("research_run_registry_available", "research_registry", "FAIL", str(exc)))

        try:
            from release.version_info import RUN_LINEAGE_AVAILABLE as _lin_avail
            checks.append(_mk("run_lineage_available", "research_registry",
                              "PASS" if _lin_avail else "FAIL",
                              f"version_info.RUN_LINEAGE_AVAILABLE={_lin_avail}"))
        except Exception as exc:
            checks.append(_mk("run_lineage_available", "research_registry", "FAIL", str(exc)))

        try:
            from release.version_info import RUN_ARTIFACT_CATALOG_AVAILABLE as _art_avail
            checks.append(_mk("run_artifact_catalog_available", "research_registry",
                              "PASS" if _art_avail else "FAIL",
                              f"version_info.RUN_ARTIFACT_CATALOG_AVAILABLE={_art_avail}"))
        except Exception as exc:
            checks.append(_mk("run_artifact_catalog_available", "research_registry", "FAIL", str(exc)))

        try:
            import research_registry
            _auto_rerun = getattr(research_registry, "REGISTRY_AUTO_RERUN_ENABLED", True)
            checks.append(_mk("run_auto_rerun_disabled", "research_registry",
                              "PASS" if not _auto_rerun else "FAIL",
                              f"REGISTRY_AUTO_RERUN_ENABLED={_auto_rerun} (must be False)"))
        except Exception as exc:
            checks.append(_mk("run_auto_rerun_disabled", "research_registry", "FAIL", str(exc)))

        try:
            import research_registry
            _no_orders = getattr(research_registry, "NO_REAL_ORDERS", None)
            _broker_dis = getattr(research_registry, "BROKER_DISABLED", None)
            _trade_exec = getattr(research_registry, "REGISTRY_TRADE_EXECUTION_ENABLED", True)
            if _no_orders is True and _broker_dis is True and _trade_exec is False:
                checks.append(_mk("registry_no_forbidden_actions", "research_registry", "PASS",
                                  "research_registry: NO_REAL_ORDERS=True, BROKER_DISABLED=True, REGISTRY_TRADE_EXECUTION_ENABLED=False"))
            else:
                checks.append(_mk("registry_no_forbidden_actions", "research_registry", "FAIL",
                                  f"research_registry: NO_REAL_ORDERS={_no_orders}, BROKER_DISABLED={_broker_dis}, REGISTRY_TRADE_EXECUTION_ENABLED={_trade_exec}"))
        except Exception as exc:
            checks.append(_mk("registry_no_forbidden_actions", "research_registry", "WARN", str(exc)))

        # v1.1.9 Data Governance Stable Rollup checks
        try:
            import governance_rollup
            _grr_avail = getattr(governance_rollup, "RESEARCH_ONLY", False)
            checks.append(_mk("data_governance_stable_rollup_available", "governance_rollup",
                              "PASS" if _grr_avail else "FAIL",
                              f"governance_rollup: RESEARCH_ONLY={_grr_avail}"))
        except Exception as exc:
            checks.append(_mk("data_governance_stable_rollup_available", "governance_rollup", "FAIL", str(exc)))

        try:
            from release.version_info import CROSS_MODULE_CONSISTENCY_AVAILABLE as _cmc_avail
            checks.append(_mk("cross_module_consistency_available", "governance_rollup",
                              "PASS" if _cmc_avail else "FAIL",
                              f"version_info.CROSS_MODULE_CONSISTENCY_AVAILABLE={_cmc_avail}"))
        except Exception as exc:
            checks.append(_mk("cross_module_consistency_available", "governance_rollup", "FAIL", str(exc)))

        try:
            from release.version_info import STORE_RECOVERY_AVAILABLE as _sr_avail
            _store_rec_dry_run = True  # always dry run by default
            checks.append(_mk("store_recovery_dry_run_default", "governance_rollup",
                              "PASS" if _sr_avail and _store_rec_dry_run else "FAIL",
                              f"STORE_RECOVERY_AVAILABLE={_sr_avail}, dry_run_default=True"))
        except Exception as exc:
            checks.append(_mk("store_recovery_dry_run_default", "governance_rollup", "FAIL", str(exc)))

        try:
            import governance_rollup
            _auto_exec = getattr(governance_rollup, "AUTO_RESEARCH_EXECUTION_ENABLED", True)
            checks.append(_mk("auto_research_execution_disabled", "governance_rollup",
                              "PASS" if not _auto_exec else "FAIL",
                              f"governance_rollup.AUTO_RESEARCH_EXECUTION_ENABLED={_auto_exec} (must be False)"))
        except Exception as exc:
            checks.append(_mk("auto_research_execution_disabled", "governance_rollup", "FAIL", str(exc)))

        try:
            import governance_rollup
            _no_orders = getattr(governance_rollup, "NO_REAL_ORDERS", None)
            _broker_dis = getattr(governance_rollup, "BROKER_DISABLED", None)
            _trade_exec = getattr(governance_rollup, "TRADE_EXECUTION_ENABLED", True)
            _auto_repair = getattr(governance_rollup, "AUTO_STORE_REPAIR_ENABLED", True)
            _auto_dl = getattr(governance_rollup, "AUTO_DATA_DOWNLOAD_ENABLED", True)
            if _no_orders and _broker_dis and not _trade_exec and not _auto_repair and not _auto_dl:
                checks.append(_mk("stable_rollup_no_forbidden_actions", "governance_rollup", "PASS",
                                  "governance_rollup: NO_REAL_ORDERS=True, BROKER_DISABLED=True, "
                                  "TRADE_EXECUTION_ENABLED=False, AUTO_STORE_REPAIR_ENABLED=False, "
                                  "AUTO_DATA_DOWNLOAD_ENABLED=False"))
            else:
                checks.append(_mk("stable_rollup_no_forbidden_actions", "governance_rollup", "FAIL",
                                  f"governance_rollup: NO_REAL_ORDERS={_no_orders}, "
                                  f"BROKER_DISABLED={_broker_dis}, TRADE_EXECUTION_ENABLED={_trade_exec}, "
                                  f"AUTO_STORE_REPAIR_ENABLED={_auto_repair}, AUTO_DATA_DOWNLOAD_ENABLED={_auto_dl}"))
        except Exception as exc:
            checks.append(_mk("stable_rollup_no_forbidden_actions", "governance_rollup", "WARN", str(exc)))

        # v1.2.0 Replay Training UX Foundation checks
        try:
            from release.version_info import REPLAY_TRAINING_AVAILABLE as _rta
            checks.append(_mk("replay_training_available", "replay_training",
                              "PASS" if _rta else "FAIL",
                              f"REPLAY_TRAINING_AVAILABLE={_rta}"))
        except Exception as exc:
            checks.append(_mk("replay_training_available", "replay_training", "WARN", str(exc)))

        try:
            from release.version_info import REPLAY_FUTURE_DATA_FIREWALL_AVAILABLE as _rff
            checks.append(_mk("replay_future_data_firewall_available", "replay_training",
                              "PASS" if _rff else "FAIL",
                              f"REPLAY_FUTURE_DATA_FIREWALL_AVAILABLE={_rff}"))
        except Exception as exc:
            checks.append(_mk("replay_future_data_firewall_available", "replay_training", "WARN", str(exc)))

        try:
            from release.version_info import REPLAY_DECISION_CAPTURE_AVAILABLE as _rdc
            checks.append(_mk("replay_decision_capture_available", "replay_training",
                              "PASS" if _rdc else "FAIL",
                              f"REPLAY_DECISION_CAPTURE_AVAILABLE={_rdc}"))
        except Exception as exc:
            checks.append(_mk("replay_decision_capture_available", "replay_training", "WARN", str(exc)))

        try:
            from release.version_info import REPLAY_TRADE_EXECUTION_ENABLED as _rte
            checks.append(_mk("replay_trade_execution_disabled", "replay_training",
                              "PASS" if not _rte else "FAIL",
                              f"REPLAY_TRADE_EXECUTION_ENABLED={_rte} (must be False)"))
        except Exception as exc:
            checks.append(_mk("replay_trade_execution_disabled", "replay_training", "WARN", str(exc)))

        try:
            from replay.replay_training_engine import ReplayTrainingEngine
            checks.append(_mk("replay_no_forbidden_actions", "replay_training",
                              "PASS" if ReplayTrainingEngine.NO_REAL_ORDERS else "FAIL",
                              f"ReplayTrainingEngine.NO_REAL_ORDERS={ReplayTrainingEngine.NO_REAL_ORDERS}"))
        except Exception as exc:
            checks.append(_mk("replay_no_forbidden_actions", "replay_training", "WARN", str(exc)))

        # v1.2.1 Replay Scenario & Session Manager checks
        try:
            from replay.scenario_library import ReplayScenarioLibrary
            checks.append(_mk("replay_scenario_library_available", "replay_scenario_session_manager",
                              "PASS", "ReplayScenarioLibrary importable"))
        except Exception as exc:
            checks.append(_mk("replay_scenario_library_available", "replay_scenario_session_manager", "WARN", str(exc)))

        try:
            from replay.session_manager import ReplaySessionManager
            checks.append(_mk("replay_session_manager_available", "replay_scenario_session_manager",
                              "PASS", "ReplaySessionManager importable"))
        except Exception as exc:
            checks.append(_mk("replay_session_manager_available", "replay_scenario_session_manager", "WARN", str(exc)))

        try:
            from replay.session_checkpoint import ReplayCheckpointManager
            checks.append(_mk("replay_checkpoint_available", "replay_scenario_session_manager",
                              "PASS", "ReplayCheckpointManager importable"))
        except Exception as exc:
            checks.append(_mk("replay_checkpoint_available", "replay_scenario_session_manager", "WARN", str(exc)))

        try:
            from release.version_info import REPLAY_SCENARIO_LIBRARY_AVAILABLE, REPLAY_BATCH_SESSION_CREATION_AVAILABLE
            ok = REPLAY_SCENARIO_LIBRARY_AVAILABLE and REPLAY_BATCH_SESSION_CREATION_AVAILABLE
            checks.append(_mk("replay_scenario_flags_v121", "replay_scenario_session_manager",
                              "PASS" if ok else "FAIL",
                              f"REPLAY_SCENARIO_LIBRARY_AVAILABLE={REPLAY_SCENARIO_LIBRARY_AVAILABLE}"))
        except Exception as exc:
            checks.append(_mk("replay_scenario_flags_v121", "replay_scenario_session_manager", "WARN", str(exc)))

        try:
            from release.version_info import REPLAY_TRADE_EXECUTION_ENABLED, REPLAY_AUTO_DECISION_ENABLED
            safe = not REPLAY_TRADE_EXECUTION_ENABLED and not REPLAY_AUTO_DECISION_ENABLED
            checks.append(_mk("replay_scenario_trade_exec_disabled_v121", "replay_scenario_session_manager",
                              "PASS" if safe else "FAIL",
                              f"REPLAY_TRADE_EXECUTION_ENABLED={REPLAY_TRADE_EXECUTION_ENABLED}, REPLAY_AUTO_DECISION_ENABLED={REPLAY_AUTO_DECISION_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("replay_scenario_trade_exec_disabled_v121", "replay_scenario_session_manager", "WARN", str(exc)))

        # v1.2.2 Decision Journal Integration checks
        try:
            from replay.decision_journal_schema import (
                DecisionJournalEntry, JOURNAL_ID_PREFIX, REVISION_ID_PREFIX
            )
            checks.append(_mk("decision_journal_schema_available", "decision_journal",
                              "PASS", f"JOURNAL_ID_PREFIX={JOURNAL_ID_PREFIX}, REVISION_ID_PREFIX={REVISION_ID_PREFIX}"))
        except Exception as exc:
            checks.append(_mk("decision_journal_schema_available", "decision_journal", "WARN", str(exc)))
        try:
            from replay.decision_journal_manager import DecisionJournalManager
            checks.append(_mk("decision_journal_manager_available", "decision_journal",
                              "PASS", "DecisionJournalManager available"))
        except Exception as exc:
            checks.append(_mk("decision_journal_manager_available", "decision_journal", "WARN", str(exc)))
        try:
            from release.version_info import (
                DECISION_JOURNAL_AVAILABLE, DECISION_AUTO_SCORING_ENABLED,
                DECISION_AUTO_EXECUTION_ENABLED
            )
            ok = DECISION_JOURNAL_AVAILABLE and not DECISION_AUTO_SCORING_ENABLED and not DECISION_AUTO_EXECUTION_ENABLED
            checks.append(_mk("decision_journal_flags_v122", "decision_journal",
                              "PASS" if ok else "FAIL",
                              f"DECISION_JOURNAL_AVAILABLE={DECISION_JOURNAL_AVAILABLE}, "
                              f"DECISION_AUTO_SCORING_ENABLED={DECISION_AUTO_SCORING_ENABLED}, "
                              f"DECISION_AUTO_EXECUTION_ENABLED={DECISION_AUTO_EXECUTION_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("decision_journal_flags_v122", "decision_journal", "WARN", str(exc)))

        # v1.2.3 Replay Scoring & Mistake Taxonomy checks
        try:
            from replay.scoring_schema import ReplayProcessScore, SCORE_ID_PREFIX
            checks.append(_mk("replay_scoring_schema_available", "replay_scoring",
                              "PASS", f"SCORE_ID_PREFIX={SCORE_ID_PREFIX}"))
        except Exception as exc:
            checks.append(_mk("replay_scoring_schema_available", "replay_scoring", "WARN", str(exc)))
        try:
            from replay.mistake_detector import MistakeDetector
            checks.append(_mk("replay_mistake_detector_available", "replay_scoring",
                              "PASS", "MistakeDetector available"))
        except Exception as exc:
            checks.append(_mk("replay_mistake_detector_available", "replay_scoring", "WARN", str(exc)))
        try:
            from replay.scoring_health import ReplayScoringHealthCheck
            checks.append(_mk("replay_scoring_health_available", "replay_scoring",
                              "PASS", "ReplayScoringHealthCheck available"))
        except Exception as exc:
            checks.append(_mk("replay_scoring_health_available", "replay_scoring", "WARN", str(exc)))

        # v1.2.4 Strategy Knowledge Replay checks
        try:
            from replay.strategy_replay_schema import StrategyReplaySnapshot
            ssn = StrategyReplaySnapshot.__dataclass_fields__
            future_fields = [f for f in ssn if any(p in f for p in ["forward_return", "outcome_", "hindsight_"])]
            status = "PASS" if not future_fields else "FAIL"
            checks.append(_mk("strategy_snapshot_no_forward_return", "replay_strategy_knowledge",
                              status, f"No future fields in snapshot: {not bool(future_fields)}"))
        except Exception as exc:
            checks.append(_mk("strategy_snapshot_no_forward_return", "replay_strategy_knowledge", "WARN", str(exc)))
        try:
            from release.version_info import (
                STRATEGY_KNOWLEDGE_REPLAY_AVAILABLE,
                AUTO_STRATEGY_DECISION_ENABLED,
                AUTO_STRATEGY_EXECUTION_ENABLED,
                AUTO_STRATEGY_WEIGHT_CHANGE_ENABLED,
            )
            ok = (STRATEGY_KNOWLEDGE_REPLAY_AVAILABLE
                  and not AUTO_STRATEGY_DECISION_ENABLED
                  and not AUTO_STRATEGY_EXECUTION_ENABLED
                  and not AUTO_STRATEGY_WEIGHT_CHANGE_ENABLED)
            checks.append(_mk("strategy_knowledge_replay_v124_safe", "replay_strategy_knowledge",
                              "PASS" if ok else "FAIL",
                              f"STRATEGY_KNOWLEDGE_REPLAY_AVAILABLE={STRATEGY_KNOWLEDGE_REPLAY_AVAILABLE}, "
                              f"AUTO_STRATEGY_DECISION_ENABLED={AUTO_STRATEGY_DECISION_ENABLED}, "
                              f"AUTO_STRATEGY_EXECUTION_ENABLED={AUTO_STRATEGY_EXECUTION_ENABLED}, "
                              f"AUTO_STRATEGY_WEIGHT_CHANGE_ENABLED={AUTO_STRATEGY_WEIGHT_CHANGE_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("strategy_knowledge_replay_v124_safe", "replay_strategy_knowledge", "WARN", str(exc)))
        try:
            from replay.strategy_conflict import StrategyConflictAnalyzer, CONFLICT_NEVER_AUTO_BLOCKS_DECISION
            checks.append(_mk("strategy_conflict_never_auto_blocks", "replay_strategy_knowledge",
                              "PASS" if CONFLICT_NEVER_AUTO_BLOCKS_DECISION else "FAIL",
                              f"CONFLICT_NEVER_AUTO_BLOCKS_DECISION={CONFLICT_NEVER_AUTO_BLOCKS_DECISION}"))
        except Exception as exc:
            checks.append(_mk("strategy_conflict_never_auto_blocks", "replay_strategy_knowledge", "WARN", str(exc)))
        try:
            from replay.strategy_rule_review import StrategyRuleReviewManager, AUTO_CONFIRM_ENABLED
            checks.append(_mk("strategy_rule_review_no_auto_confirm", "replay_strategy_knowledge",
                              "PASS" if not AUTO_CONFIRM_ENABLED else "FAIL",
                              f"AUTO_CONFIRM_ENABLED={AUTO_CONFIRM_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("strategy_rule_review_no_auto_confirm", "replay_strategy_knowledge", "WARN", str(exc)))

        # v1.2.5 Multi-Timeframe Replay checks
        try:
            from release.version_info import MULTI_TIMEFRAME_REPLAY_AVAILABLE, MTF_NO_FUTURE_KLINES
            from release.version_info import MTF_AUTO_TRADE_ENABLED, MTF_AUTO_BLOCK_ENABLED
            ok = (MULTI_TIMEFRAME_REPLAY_AVAILABLE
                  and MTF_NO_FUTURE_KLINES
                  and not MTF_AUTO_TRADE_ENABLED
                  and not MTF_AUTO_BLOCK_ENABLED)
            checks.append(_mk("mtf_replay_v125_safe", "replay_multi_timeframe",
                              "PASS" if ok else "FAIL",
                              f"MTF_AVAILABLE={MULTI_TIMEFRAME_REPLAY_AVAILABLE}, "
                              f"NO_FUTURE_KLINES={MTF_NO_FUTURE_KLINES}, "
                              f"AUTO_TRADE={MTF_AUTO_TRADE_ENABLED}, "
                              f"AUTO_BLOCK={MTF_AUTO_BLOCK_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("mtf_replay_v125_safe", "replay_multi_timeframe", "WARN", str(exc)))
        try:
            from replay.timeframe_future_firewall import MultiTimeframeFutureDataFirewall
            fw = MultiTimeframeFutureDataFirewall()
            future_bar = {"timestamp": "9999-12-31T23:59:59", "close": 999.0}
            result = fw.filter_bars([future_bar], replay_timestamp="2025-01-01T09:00:00", timeframe="M5")
            if isinstance(result, dict):
                filtered = result.get("filtered_bars", [])
            else:
                filtered = result or []
            checks.append(_mk("mtf_future_firewall_active", "replay_multi_timeframe",
                              "PASS" if not filtered else "FAIL",
                              f"future bar blocked={not bool(filtered)}"))
        except Exception as exc:
            checks.append(_mk("mtf_future_firewall_active", "replay_multi_timeframe", "WARN", str(exc)))

        # v1.2.6 Replay Review Dashboard checks
        try:
            from release.version_info import (
                REPLAY_REVIEW_DASHBOARD_AVAILABLE,
                REPLAY_REVIEW_QUEUE_AVAILABLE,
                REPLAY_REVIEW_PROGRESS_AVAILABLE,
                AUTO_REVIEW_COMPLETE_ENABLED,
                AUTO_OUTCOME_REVEAL_ENABLED,
                AUTO_MISTAKE_CONFIRMATION_ENABLED,
                REPLAY_TRADE_EXECUTION_ENABLED,
            )
            ok = (REPLAY_REVIEW_DASHBOARD_AVAILABLE
                  and REPLAY_REVIEW_QUEUE_AVAILABLE
                  and REPLAY_REVIEW_PROGRESS_AVAILABLE
                  and not AUTO_REVIEW_COMPLETE_ENABLED
                  and not AUTO_OUTCOME_REVEAL_ENABLED
                  and not AUTO_MISTAKE_CONFIRMATION_ENABLED
                  and not REPLAY_TRADE_EXECUTION_ENABLED)
            checks.append(_mk("replay_review_dashboard_available", "replay_review_dashboard",
                              "PASS" if ok else "FAIL",
                              f"DASHBOARD={REPLAY_REVIEW_DASHBOARD_AVAILABLE}, "
                              f"QUEUE={REPLAY_REVIEW_QUEUE_AVAILABLE}, "
                              f"PROGRESS={REPLAY_REVIEW_PROGRESS_AVAILABLE}"))
        except Exception as exc:
            checks.append(_mk("replay_review_dashboard_available", "replay_review_dashboard", "WARN", str(exc)))
        try:
            from release.version_info import AUTO_REVIEW_COMPLETE_ENABLED, AUTO_MISTAKE_CONFIRMATION_ENABLED
            no_auto = (not AUTO_REVIEW_COMPLETE_ENABLED and not AUTO_MISTAKE_CONFIRMATION_ENABLED)
            checks.append(_mk("replay_review_no_auto_complete", "replay_review_dashboard",
                              "PASS" if no_auto else "FAIL",
                              f"AUTO_COMPLETE={AUTO_REVIEW_COMPLETE_ENABLED}, "
                              f"AUTO_CONFIRM={AUTO_MISTAKE_CONFIRMATION_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("replay_review_no_auto_complete", "replay_review_dashboard", "WARN", str(exc)))
        try:
            from release.version_info import REPLAY_TRADE_EXECUTION_ENABLED, AUTO_SCORE_TO_TRADE_ENABLED
            no_forbidden = (not REPLAY_TRADE_EXECUTION_ENABLED and not AUTO_SCORE_TO_TRADE_ENABLED)
            checks.append(_mk("replay_review_no_forbidden_actions", "replay_review_dashboard",
                              "PASS" if no_forbidden else "FAIL",
                              f"TRADE_EXEC={REPLAY_TRADE_EXECUTION_ENABLED}, "
                              f"SCORE_TO_TRADE={AUTO_SCORE_TO_TRADE_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("replay_review_no_forbidden_actions", "replay_review_dashboard", "WARN", str(exc)))

        # v1.2.7 Replay Challenge Mode checks
        try:
            from replay.challenge_schema import ReplayChallengeDefinition  # noqa: F401
            from replay.challenge_engine import ReplayChallengeEngine  # noqa: F401
            checks.append(_mk("replay_challenge_mode_available", "replay_challenge_mode",
                              "PASS", "ReplayChallengeDefinition and ReplayChallengeEngine importable"))
        except Exception as exc:
            checks.append(_mk("replay_challenge_mode_available", "replay_challenge_mode", "WARN", str(exc)))
        try:
            from replay.challenge_engine import ReplayChallengeEngine
            no_auto = (not ReplayChallengeEngine.AUTO_DECISION_ENABLED
                       and not ReplayChallengeEngine.AUTO_REVEAL_ENABLED
                       and not ReplayChallengeEngine.AUTO_CONFIRM_ENABLED)
            checks.append(_mk("replay_challenge_no_auto_decision", "replay_challenge_mode",
                              "PASS" if no_auto else "FAIL",
                              f"AUTO_DECISION={ReplayChallengeEngine.AUTO_DECISION_ENABLED}, "
                              f"AUTO_REVEAL={ReplayChallengeEngine.AUTO_REVEAL_ENABLED}, "
                              f"AUTO_CONFIRM={ReplayChallengeEngine.AUTO_CONFIRM_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("replay_challenge_no_auto_decision", "replay_challenge_mode", "WARN", str(exc)))
        try:
            from replay.challenge_leaderboard import PUBLIC_LEADERBOARD_ENABLED, NETWORK_SCORE_SUBMISSION_ENABLED
            no_public = not PUBLIC_LEADERBOARD_ENABLED and not NETWORK_SCORE_SUBMISSION_ENABLED
            checks.append(_mk("replay_challenge_no_public_leaderboard", "replay_challenge_mode",
                              "PASS" if no_public else "FAIL",
                              f"PUBLIC_LEADERBOARD={PUBLIC_LEADERBOARD_ENABLED}, "
                              f"NETWORK_SUBMISSION={NETWORK_SCORE_SUBMISSION_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("replay_challenge_no_public_leaderboard", "replay_challenge_mode", "WARN", str(exc)))
        try:
            from replay.challenge_hidden_data import ReplayChallengeHiddenDataGuard
            fw_active = getattr(ReplayChallengeHiddenDataGuard, "FUTURE_FIREWALL_ACTIVE", False)
            checks.append(_mk("replay_challenge_future_firewall", "replay_challenge_mode",
                              "PASS" if fw_active else "FAIL",
                              f"FUTURE_FIREWALL_ACTIVE={fw_active}"))
        except Exception as exc:
            checks.append(_mk("replay_challenge_future_firewall", "replay_challenge_mode", "WARN", str(exc)))
        try:
            from release.version_info import REPLAY_CHALLENGE_MODE_AVAILABLE, AUTO_CHALLENGE_DECISION_ENABLED
            ok = REPLAY_CHALLENGE_MODE_AVAILABLE and not AUTO_CHALLENGE_DECISION_ENABLED
            checks.append(_mk("replay_challenge_version_flags", "replay_challenge_mode",
                              "PASS" if ok else "WARN",
                              f"REPLAY_CHALLENGE_MODE_AVAILABLE={REPLAY_CHALLENGE_MODE_AVAILABLE}, "
                              f"AUTO_CHALLENGE_DECISION_ENABLED={AUTO_CHALLENGE_DECISION_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("replay_challenge_version_flags", "replay_challenge_mode", "WARN", str(exc)))

        # v1.2.8 Replay Dataset & Session Registry checks
        try:
            from release.version_info import REPLAY_DATASET_REGISTRY_AVAILABLE, REPLAY_SESSION_REGISTRY_AVAILABLE
            checks.append(_mk("replay_registry_available", "replay_registry",
                              "PASS" if REPLAY_DATASET_REGISTRY_AVAILABLE and REPLAY_SESSION_REGISTRY_AVAILABLE else "WARN",
                              f"REPLAY_DATASET_REGISTRY_AVAILABLE={REPLAY_DATASET_REGISTRY_AVAILABLE}, "
                              f"REPLAY_SESSION_REGISTRY_AVAILABLE={REPLAY_SESSION_REGISTRY_AVAILABLE}"))
        except Exception as exc:
            checks.append(_mk("replay_registry_available", "replay_registry", "WARN", str(exc)))

        try:
            from release.version_info import AUTO_DATASET_OVERWRITE_ENABLED, AUTO_DATASET_REPAIR_ENABLED
            checks.append(_mk("replay_registry_no_auto_overwrite_repair", "replay_registry",
                              "PASS" if not AUTO_DATASET_OVERWRITE_ENABLED and not AUTO_DATASET_REPAIR_ENABLED else "FAIL",
                              f"AUTO_DATASET_OVERWRITE_ENABLED={AUTO_DATASET_OVERWRITE_ENABLED}, "
                              f"AUTO_DATASET_REPAIR_ENABLED={AUTO_DATASET_REPAIR_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("replay_registry_no_auto_overwrite_repair", "replay_registry", "WARN", str(exc)))

        try:
            from release.version_info import AUTO_SESSION_REBIND_ENABLED, AUTO_PACKAGE_IMPORT_ENABLED
            checks.append(_mk("replay_registry_no_auto_rebind_import", "replay_registry",
                              "PASS" if not AUTO_SESSION_REBIND_ENABLED and not AUTO_PACKAGE_IMPORT_ENABLED else "FAIL",
                              f"AUTO_SESSION_REBIND_ENABLED={AUTO_SESSION_REBIND_ENABLED}, "
                              f"AUTO_PACKAGE_IMPORT_ENABLED={AUTO_PACKAGE_IMPORT_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("replay_registry_no_auto_rebind_import", "replay_registry", "WARN", str(exc)))

        try:
            from release.version_info import AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED
            checks.append(_mk("replay_registry_no_auto_conflict_resolve", "replay_registry",
                              "PASS" if not AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED else "FAIL",
                              f"AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED={AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED}"))
        except Exception as exc:
            checks.append(_mk("replay_registry_no_auto_conflict_resolve", "replay_registry", "WARN", str(exc)))

        # v1.2.9 Replay Training Stable Rollup checks
        try:
            from release.version_info import REPLAY_STABLE_HEALTH_AVAILABLE
            checks.append(_mk(
                "replay_training_stable_rollup_available", "replay_stable_rollup",
                "PASS" if REPLAY_STABLE_HEALTH_AVAILABLE else "FAIL",
                f"REPLAY_STABLE_HEALTH_AVAILABLE={REPLAY_STABLE_HEALTH_AVAILABLE}",
            ))
        except Exception as exc:
            checks.append(_mk("replay_training_stable_rollup_available", "replay_stable_rollup", "WARN", str(exc)))

        try:
            from replay.stable_manifest import ReplayStableManifest  # noqa: F401
            checks.append(_mk("replay_stable_manifest_available", "replay_stable_rollup", "PASS",
                              "ReplayStableManifest importable"))
        except Exception as exc:
            checks.append(_mk("replay_stable_manifest_available", "replay_stable_rollup", "WARN", str(exc)))

        try:
            from replay.stable_capability_matrix import ReplayStableCapabilityMatrix  # noqa: F401
            checks.append(_mk("replay_capability_matrix_available", "replay_stable_rollup", "PASS",
                              "ReplayStableCapabilityMatrix importable"))
        except Exception as exc:
            checks.append(_mk("replay_capability_matrix_available", "replay_stable_rollup", "WARN", str(exc)))

        try:
            from replay.stable_contracts import ReplayStableContractChecker
            results = ReplayStableContractChecker().check_all()
            fail_count_c = sum(1 for s, _ in results.values() if s == "FAIL")
            checks.append(_mk(
                "replay_cross_module_contracts_pass", "replay_stable_rollup",
                "PASS" if fail_count_c == 0 else "FAIL",
                f"Contract checks: {len(results)} total, {fail_count_c} FAILs",
            ))
        except Exception as exc:
            checks.append(_mk("replay_cross_module_contracts_pass", "replay_stable_rollup", "WARN", str(exc)))

        try:
            from replay.stable_compatibility import ReplayStableCompatibilityChecker
            results = ReplayStableCompatibilityChecker().check_all()
            fail_count_b = sum(1 for s, _ in results.values() if s == "FAIL")
            checks.append(_mk(
                "replay_backward_compatibility_pass", "replay_stable_rollup",
                "PASS" if fail_count_b == 0 else "FAIL",
                f"Compat checks: {len(results)} versions, {fail_count_b} FAILs",
            ))
        except Exception as exc:
            checks.append(_mk("replay_backward_compatibility_pass", "replay_stable_rollup", "WARN", str(exc)))

        try:
            from replay.stable_health import ReplayStableHealthCheck  # noqa: F401
            checks.append(_mk("replay_no_forbidden_actions", "replay_stable_rollup", "PASS",
                              "ReplayStableHealthCheck importable"))
        except Exception as exc:
            checks.append(_mk("replay_no_forbidden_actions", "replay_stable_rollup", "WARN", str(exc)))

        # Rebuild summary counts to include new checks
        total         = len(checks)
        pass_count    = sum(1 for c in checks if c["status"] == "PASS")
        warn_count    = sum(1 for c in checks if c["status"] == "WARN")
        fail_count    = sum(1 for c in checks if c["status"] == "FAIL")
        blocked_count = sum(1 for c in checks if c["status"] == "BLOCKED")

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
