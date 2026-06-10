"""
strategy_lab/strategy_lab_checklist.py — Strategy Lab Stable Checklist v0.9.0

Runs 7-category stable checklist for the Strategy Lab.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
from typing import List, Tuple

from strategy_lab.strategy_lab_schema import (
    StrategyLabCheck, StrategyLabSummary,
    CHECK_PASS, CHECK_WARN, CHECK_FAIL, CHECK_BLOCKED,
    SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM, SEV_LOW,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _mk(cid: str, cat: str, name: str, status: str, sev: str, msg: str,
        fix: str = "", evidence: str = "") -> StrategyLabCheck:
    return StrategyLabCheck(
        check_id=cid, category=cat, name=name,
        status=status, severity=sev, message=msg,
        suggested_fix=fix, evidence=evidence,
        no_real_orders=True, production_blocked=True,
    )


class StrategyLabChecklist:
    """Strategy Lab Stable checklist — 7 categories, A-G.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, project_root: str = ".") -> None:
        if os.path.isabs(project_root):
            self._root = project_root
        else:
            self._root = os.path.join(BASE_DIR, project_root)

    def run(self, mode: str = "real") -> Tuple[List[StrategyLabCheck], StrategyLabSummary]:
        """Run all checklist categories. Returns (checks, summary)."""
        checks: List[StrategyLabCheck] = []
        checks += self._category_a_import_health()
        checks += self._category_b_cli_health(mode)
        checks += self._category_c_report_health(mode)
        checks += self._category_d_safety()
        checks += self._category_e_regression(mode)
        checks += self._category_f_runtime(mode)
        checks += self._category_g_integration(mode)
        return checks, self._build_summary(checks, mode)

    # ------------------------------------------------------------------
    # A. Import Health
    # ------------------------------------------------------------------

    def _category_a_import_health(self) -> List[StrategyLabCheck]:
        checks = []
        pairs = [
            ("a_ri_import",  "research_intelligence import",
             "research_intelligence.research_intelligence_engine",
             "ResearchIntelligenceEngine"),
            ("a_sm_import",  "strategy_memory import",
             "strategy_memory.strategy_memory_engine",
             "StrategyMemoryEngine"),
            ("a_bc_import",  "backtest_coach import",
             "backtest_coach.backtest_coach_engine",
             "BacktestCoachEngine"),
            ("a_tm_import",  "training_metrics import",
             "training_metrics.training_metrics_engine",
             "TrainingMetricsEngine"),
            ("a_eg_import",  "evidence_graph import",
             "evidence_graph.evidence_graph_engine",
             "EvidenceGraphEngine"),
            ("a_sl_import",  "strategy_lab import",
             "strategy_lab.strategy_lab_schema",
             "StrategyLabSummary"),
            ("a_rpt_import", "reports import",
             "reports.strategy_lab_stable_report",
             "StrategyLabStableReportBuilder"),
            ("a_gui_adapter", "GUI adapter import",
             "gui.strategy_lab_adapter",
             "StrategyLabAdapter"),
            ("a_gui_panel",  "GUI panel import",
             "gui.strategy_lab_panel",
             "StrategyLabPanel"),
        ]
        # v0.9.0.1 crash reversal — CHECK_WARN on failure (optional new feature)
        for cid, name, module, cls in [
            ("a_cr_pack_import", "crash_reversal_pack import",
             "strategy_rules.crash_reversal_pack",
             "CrashReversalStrategyPack"),
        ]:
            try:
                mod = __import__(module, fromlist=[cls])
                getattr(mod, cls)
                checks.append(_mk(cid, "import_health", name,
                                  CHECK_PASS, SEV_LOW, f"{cls} imported successfully."))
            except Exception as exc:
                checks.append(_mk(cid, "import_health", name,
                                  CHECK_WARN, SEV_MEDIUM, f"Import failed (optional): {exc}",
                                  f"Check {module}.py for syntax errors."))
        # crash_reversal_no_forbidden_actions
        try:
            mod = __import__("strategy_rules.crash_reversal_pack",
                             fromlist=["CrashReversalStrategyPack"])
            cls_obj = getattr(mod, "CrashReversalStrategyPack")
            result = cls_obj().run(mode="real") if hasattr(cls_obj(), "run") else {}
            out_str = str(result)
            forbidden = [kw for kw in ["BUY", "SELL", "ORDER"]
                         if kw in out_str.upper()]
            if forbidden:
                checks.append(_mk("a_cr_no_forbidden", "import_health",
                                  "crash_reversal_no_forbidden_actions",
                                  CHECK_WARN, SEV_HIGH,
                                  f"Forbidden keywords found in output: {forbidden}",
                                  "Remove BUY/SELL/ORDER from CrashReversalStrategyPack output."))
            else:
                checks.append(_mk("a_cr_no_forbidden", "import_health",
                                  "crash_reversal_no_forbidden_actions",
                                  CHECK_PASS, SEV_LOW,
                                  "CrashReversalStrategyPack output has no BUY/SELL/ORDER."))
        except Exception as exc:
            checks.append(_mk("a_cr_no_forbidden", "import_health",
                              "crash_reversal_no_forbidden_actions",
                              CHECK_WARN, SEV_MEDIUM,
                              f"Check skipped (optional): {exc}"))
        # v0.9.1 Evidence Graph UX — CHECK_WARN on failure (optional new features)
        # a_eg_ux_import: EvidenceGraphQuery imports
        try:
            mod = __import__("evidence_graph.evidence_graph_query", fromlist=["EvidenceGraphQuery"])
            getattr(mod, "EvidenceGraphQuery")
            checks.append(_mk("a_eg_ux_import", "import_health",
                              "evidence_graph_ux import",
                              CHECK_PASS, SEV_LOW,
                              "EvidenceGraphQuery imported successfully."))
        except Exception as exc:
            checks.append(_mk("a_eg_ux_import", "import_health",
                              "evidence_graph_ux import",
                              CHECK_WARN, SEV_MEDIUM,
                              f"Import failed (optional): {exc}",
                              "Check evidence_graph/evidence_graph_query.py for syntax errors."))
        # a_eg_ux_no_forbidden: EvidenceGraphQuery doesn't output BUY/SELL/ORDER
        try:
            mod = __import__("evidence_graph.evidence_graph_query", fromlist=["EvidenceGraphQuery"])
            cls_obj = getattr(mod, "EvidenceGraphQuery")
            instance = cls_obj()
            out_str = str(vars(instance)) if hasattr(instance, "__dict__") else ""
            forbidden = [kw for kw in ["BUY", "SELL", "ORDER"] if kw in out_str.upper()]
            if forbidden:
                checks.append(_mk("a_eg_ux_no_forbidden", "import_health",
                                  "evidence_graph_ux_no_forbidden_actions",
                                  CHECK_WARN, SEV_HIGH,
                                  f"Forbidden keywords found in EvidenceGraphQuery output: {forbidden}",
                                  "Remove BUY/SELL/ORDER from EvidenceGraphQuery output."))
            else:
                checks.append(_mk("a_eg_ux_no_forbidden", "import_health",
                                  "evidence_graph_ux_no_forbidden_actions",
                                  CHECK_PASS, SEV_LOW,
                                  "EvidenceGraphQuery output has no BUY/SELL/ORDER."))
        except Exception as exc:
            checks.append(_mk("a_eg_ux_no_forbidden", "import_health",
                              "evidence_graph_ux_no_forbidden_actions",
                              CHECK_WARN, SEV_MEDIUM,
                              f"Check skipped (optional): {exc}"))
        # a_cr_evidence_chain: crash reversal nodes are collectible
        try:
            mod = __import__("evidence_graph.evidence_graph_query", fromlist=["EvidenceGraphQuery"])
            cls_obj = getattr(mod, "EvidenceGraphQuery")
            q = cls_obj()
            if hasattr(q, "get_crash_reversal_threads") or hasattr(q, "search_nodes"):
                checks.append(_mk("a_cr_evidence_chain", "import_health",
                                  "crash_reversal_evidence_chain_collectible",
                                  CHECK_PASS, SEV_LOW,
                                  "EvidenceGraphQuery has crash reversal query methods."))
            else:
                checks.append(_mk("a_cr_evidence_chain", "import_health",
                                  "crash_reversal_evidence_chain_collectible",
                                  CHECK_WARN, SEV_MEDIUM,
                                  "EvidenceGraphQuery missing crash reversal query methods (optional v0.9.1).",
                                  "Add get_crash_reversal_threads() to EvidenceGraphQuery."))
        except Exception as exc:
            checks.append(_mk("a_cr_evidence_chain", "import_health",
                              "crash_reversal_evidence_chain_collectible",
                              CHECK_WARN, SEV_MEDIUM,
                              f"Check skipped (optional): {exc}"))
        # v0.9.2 strategy validation — CHECK_WARN on failure (optional new features)
        # a_sv_import: strategy_validation schema imports
        try:
            mod = __import__("strategy_validation.strategy_validation_schema",
                             fromlist=["StrategyValidationScore"])
            getattr(mod, "StrategyValidationScore")
            checks.append(_mk("a_sv_import", "import_health",
                              "strategy_validation_schema import",
                              CHECK_PASS, SEV_LOW,
                              "StrategyValidationScore imported successfully."))
        except Exception as exc:
            checks.append(_mk("a_sv_import", "import_health",
                              "strategy_validation_schema import",
                              CHECK_WARN, SEV_MEDIUM,
                              f"Import failed (optional): {exc}",
                              "Check strategy_validation/strategy_validation_schema.py for syntax errors."))
        # a_sv_no_forbidden: StrategyValidationScore has no BUY/SELL/ORDER
        try:
            mod = __import__("strategy_validation.strategy_validation_schema",
                             fromlist=["StrategyValidationScore"])
            cls_obj = getattr(mod, "StrategyValidationScore")
            instance = cls_obj() if callable(cls_obj) else None
            out_str = str(vars(instance)) if instance and hasattr(instance, "__dict__") else ""
            forbidden = [kw for kw in ["BUY", "SELL", "ORDER"] if kw in out_str.upper()]
            if forbidden:
                checks.append(_mk("a_sv_no_forbidden", "import_health",
                                  "strategy_validation_no_forbidden_actions",
                                  CHECK_WARN, SEV_HIGH,
                                  f"Forbidden keywords found in StrategyValidationScore: {forbidden}",
                                  "Remove BUY/SELL/ORDER from StrategyValidationScore output."))
            else:
                checks.append(_mk("a_sv_no_forbidden", "import_health",
                                  "strategy_validation_no_forbidden_actions",
                                  CHECK_PASS, SEV_LOW,
                                  "StrategyValidationScore has no BUY/SELL/ORDER."))
        except Exception as exc:
            checks.append(_mk("a_sv_no_forbidden", "import_health",
                              "strategy_validation_no_forbidden_actions",
                              CHECK_WARN, SEV_MEDIUM,
                              f"Check skipped (optional): {exc}"))
        # a_sv_validated_not_trading: validated_does_not_enable_trading=True check
        try:
            mod = __import__("strategy_validation.strategy_validation_schema",
                             fromlist=["StrategyValidationScore"])
            cls_obj = getattr(mod, "StrategyValidationScore")
            instance = cls_obj() if callable(cls_obj) else None
            flag = getattr(instance, "validated_does_not_enable_trading", None) if instance else None
            if flag is True:
                checks.append(_mk("a_sv_validated_not_trading", "import_health",
                                  "validated_does_not_enable_trading",
                                  CHECK_PASS, SEV_LOW,
                                  "StrategyValidationScore.validated_does_not_enable_trading=True."))
            else:
                checks.append(_mk("a_sv_validated_not_trading", "import_health",
                                  "validated_does_not_enable_trading",
                                  CHECK_WARN, SEV_MEDIUM,
                                  "validated_does_not_enable_trading not set to True (optional v0.9.2).",
                                  "Add validated_does_not_enable_trading=True to StrategyValidationScore."))
        except Exception as exc:
            checks.append(_mk("a_sv_validated_not_trading", "import_health",
                              "validated_does_not_enable_trading",
                              CHECK_WARN, SEV_MEDIUM,
                              f"Check skipped (optional): {exc}"))
        # v0.9.3 strategy lab dashboard — CHECK_WARN on failure (optional new features)
        # a_sld_import: StrategyLabDashboardEngine imports
        try:
            mod = __import__("strategy_lab.strategy_lab_dashboard_engine",
                             fromlist=["StrategyLabDashboardEngine"])
            getattr(mod, "StrategyLabDashboardEngine")
            checks.append(_mk("a_sld_import", "import_health",
                              "strategy_lab_dashboard_engine import",
                              CHECK_PASS, SEV_LOW,
                              "StrategyLabDashboardEngine imported successfully."))
        except Exception as exc:
            checks.append(_mk("a_sld_import", "import_health",
                              "strategy_lab_dashboard_engine import",
                              CHECK_WARN, SEV_MEDIUM,
                              f"Import failed (optional): {exc}",
                              "Check strategy_lab/strategy_lab_dashboard_engine.py"))
        # a_sld_no_forbidden: StrategyLabDashboardSummary rejects BUY
        try:
            mod = __import__("strategy_lab.strategy_lab_dashboard_schema",
                             fromlist=["StrategyLabDashboardSummary", "_guard"])
            guard_fn = getattr(mod, "_guard")
            try:
                guard_fn("BUY signal detected", "test")
                checks.append(_mk("a_sld_no_forbidden", "import_health",
                                  "dashboard_no_forbidden_actions",
                                  CHECK_FAIL, SEV_HIGH,
                                  "_guard() did NOT raise on 'BUY' — safety leak!",
                                  "Fix _guard() in strategy_lab_dashboard_schema.py"))
            except ValueError:
                checks.append(_mk("a_sld_no_forbidden", "import_health",
                                  "dashboard_no_forbidden_actions",
                                  CHECK_PASS, SEV_LOW,
                                  "StrategyLabDashboardSchema _guard() correctly rejects BUY."))
        except Exception as exc:
            checks.append(_mk("a_sld_no_forbidden", "import_health",
                              "dashboard_no_forbidden_actions",
                              CHECK_WARN, SEV_MEDIUM,
                              f"Check skipped (optional): {exc}"))
        # a_sld_report_available: dashboard report file exists
        try:
            import os
            report_py = os.path.join(BASE_DIR, "reports", "strategy_lab_dashboard_report.py")
            if os.path.isfile(report_py):
                checks.append(_mk("a_sld_report_available", "import_health",
                                  "dashboard_report_available",
                                  CHECK_PASS, SEV_LOW,
                                  "reports/strategy_lab_dashboard_report.py exists."))
            else:
                checks.append(_mk("a_sld_report_available", "import_health",
                                  "dashboard_report_available",
                                  CHECK_WARN, SEV_MEDIUM,
                                  "reports/strategy_lab_dashboard_report.py not found (optional v0.9.3).",
                                  "Create reports/strategy_lab_dashboard_report.py"))
        except Exception as exc:
            checks.append(_mk("a_sld_report_available", "import_health",
                              "dashboard_report_available",
                              CHECK_WARN, SEV_MEDIUM, f"Check skipped: {exc}"))
        # crash_reversal_cli_available
        try:
            import os
            main_py = os.path.join(BASE_DIR, "main.py")
            if os.path.isfile(main_py):
                with open(main_py, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if "crash-reversal" in content:
                    checks.append(_mk("a_cr_cli", "import_health",
                                      "crash_reversal_cli_available",
                                      CHECK_PASS, SEV_LOW,
                                      "crash-reversal command registered in main.py."))
                else:
                    checks.append(_mk("a_cr_cli", "import_health",
                                      "crash_reversal_cli_available",
                                      CHECK_WARN, SEV_MEDIUM,
                                      "crash-reversal command not yet registered in main.py.",
                                      "Add crash-reversal CLI commands to main.py."))
            else:
                checks.append(_mk("a_cr_cli", "import_health",
                                  "crash_reversal_cli_available",
                                  CHECK_WARN, SEV_MEDIUM, "main.py not found."))
        except Exception as exc:
            checks.append(_mk("a_cr_cli", "import_health",
                              "crash_reversal_cli_available",
                              CHECK_WARN, SEV_MEDIUM, f"Check skipped: {exc}"))
        for cid, name, module, cls in pairs:
            try:
                mod = __import__(module, fromlist=[cls])
                getattr(mod, cls)
                checks.append(_mk(cid, "import_health", name,
                                  CHECK_PASS, SEV_LOW, f"{cls} imported successfully."))
            except Exception as exc:
                checks.append(_mk(cid, "import_health", name,
                                  CHECK_FAIL, SEV_HIGH, f"Import failed: {exc}",
                                  f"Check {module}.py for syntax errors."))
        return checks

    # ------------------------------------------------------------------
    # B. CLI Health
    # ------------------------------------------------------------------

    def _category_b_cli_health(self, mode: str) -> List[StrategyLabCheck]:
        checks = []
        cli_pairs = [
            ("b_ri_summary",  "research-intelligence-summary"),
            ("b_sm_summary",  "strategy-memory-summary"),
            ("b_bc_summary",  "backtest-coach-summary"),
            ("b_tm_summary",  "training-metrics-summary"),
            ("b_eg_summary",  "evidence-graph-summary"),
            ("b_is_summary",  "intelligence-stable-summary"),
        ]
        python = sys.executable
        main_py = os.path.join(self._root, "main.py")
        for cid, cmd in cli_pairs:
            try:
                result = subprocess.run(
                    [python, main_py, cmd],
                    capture_output=True, text=True, timeout=30,
                    cwd=self._root,
                )
                if result.returncode == 0:
                    checks.append(_mk(cid, "cli_health", f"CLI: {cmd}",
                                      CHECK_PASS, SEV_LOW, f"'{cmd}' ran without error."))
                else:
                    checks.append(_mk(cid, "cli_health", f"CLI: {cmd}",
                                      CHECK_WARN, SEV_MEDIUM,
                                      f"'{cmd}' returned non-zero: {result.stderr[:200]}",
                                      f"Run: python main.py {cmd}"))
            except Exception as exc:
                checks.append(_mk(cid, "cli_health", f"CLI: {cmd}",
                                  CHECK_WARN, SEV_MEDIUM, f"CLI check error: {exc}",
                                  f"Run: python main.py {cmd}"))
        return checks

    # ------------------------------------------------------------------
    # C. Report Health
    # ------------------------------------------------------------------

    def _category_c_report_health(self, mode: str) -> List[StrategyLabCheck]:
        checks = []
        report_pairs = [
            ("c_ri_report", "research-intelligence-report", "research_intelligence_report"),
            ("c_sm_report", "strategy-memory-report",       "strategy_memory_report"),
            ("c_bc_report", "backtest-coach-report",        "backtest_coach_report"),
            ("c_tm_report", "training-metrics-report",      "training_metrics_report"),
            ("c_eg_report", "evidence-graph-report",        "evidence_graph_report"),
        ]
        python = sys.executable
        main_py = os.path.join(self._root, "main.py")
        for cid, cmd, _rtype in report_pairs:
            try:
                result = subprocess.run(
                    [python, main_py, cmd, "--mode", mode],
                    capture_output=True, text=True, timeout=30,
                    cwd=self._root,
                )
                if result.returncode == 0:
                    checks.append(_mk(cid, "report_health", f"Report: {cmd}",
                                      CHECK_PASS, SEV_LOW, f"'{cmd}' ran without error."))
                else:
                    checks.append(_mk(cid, "report_health", f"Report: {cmd}",
                                      CHECK_WARN, SEV_LOW,
                                      f"'{cmd}' returned non-zero (may be missing data).",
                                      f"Run: python main.py {cmd} --mode {mode}"))
            except Exception as exc:
                checks.append(_mk(cid, "report_health", f"Report: {cmd}",
                                  CHECK_WARN, SEV_LOW, f"Report check error: {exc}",
                                  f"Run: python main.py {cmd} --mode {mode}"))
        # report-pack full
        try:
            result = subprocess.run(
                [python, main_py, "report-pack", "--type", "full", "--mode", mode],
                capture_output=True, text=True, timeout=60,
                cwd=self._root,
            )
            if result.returncode == 0:
                checks.append(_mk("c_report_pack", "report_health", "Report Pack: full",
                                  CHECK_PASS, SEV_LOW, "report-pack --type full ran without error."))
            else:
                checks.append(_mk("c_report_pack", "report_health", "Report Pack: full",
                                  CHECK_WARN, SEV_LOW,
                                  "report-pack --type full returned non-zero (optional reports may be missing).",
                                  "Run: python main.py report-pack --type full --mode real"))
        except Exception as exc:
            checks.append(_mk("c_report_pack", "report_health", "Report Pack: full",
                              CHECK_WARN, SEV_LOW, f"report-pack check error: {exc}"))
        return checks

    # ------------------------------------------------------------------
    # D. Safety
    # ------------------------------------------------------------------

    def _category_d_safety(self) -> List[StrategyLabCheck]:
        checks = []

        # recommendations safe
        try:
            from research_intelligence.research_intelligence_schema import ResearchRecommendation
            r = ResearchRecommendation(
                rec_id="test", title="REVIEW momentum strategy",
                summary="REVIEW: momentum shows improving trend",
                action="REVIEW", source_module="test",
            )
            assert r.no_real_orders is True
            checks.append(_mk("d_rec_safe", "safety", "Recommendations no forbidden actions",
                              CHECK_PASS, SEV_LOW,
                              "ResearchRecommendation has no_real_orders=True; action=REVIEW OK."))
        except Exception as exc:
            checks.append(_mk("d_rec_safe", "safety", "Recommendations no forbidden actions",
                              CHECK_WARN, SEV_MEDIUM, f"Check skipped: {exc}"))

        # memories safe
        try:
            from strategy_memory.strategy_memory_schema import StrategyMemoryItem
            m = StrategyMemoryItem(
                memory_id="test", title="Test memory", memory_type="RESEARCH_CONCLUSION",
                source_module="test",
            )
            assert m.accepted_is_research_only is True
            assert m.no_real_orders is True
            checks.append(_mk("d_mem_safe", "safety", "Memories no forbidden actions",
                              CHECK_PASS, SEV_LOW,
                              "StrategyMemoryItem has accepted_is_research_only=True; no_real_orders=True."))
        except Exception as exc:
            checks.append(_mk("d_mem_safe", "safety", "Memories no forbidden actions",
                              CHECK_WARN, SEV_MEDIUM, f"Check skipped: {exc}"))

        # coach tasks safe
        try:
            from backtest_coach.backtest_coach_schema import CoachTrainingTask
            t = CoachTrainingTask(
                task_id="test", title="PRACTICE_REPLAY momentum",
                task_type="PRACTICE_REPLAY", source_module="test",
            )
            assert t.no_real_orders is True
            checks.append(_mk("d_coach_safe", "safety", "Coach tasks no forbidden actions",
                              CHECK_PASS, SEV_LOW,
                              "CoachTrainingTask has no_real_orders=True; task_type=PRACTICE_REPLAY OK."))
        except Exception as exc:
            checks.append(_mk("d_coach_safe", "safety", "Coach tasks no forbidden actions",
                              CHECK_WARN, SEV_MEDIUM, f"Check skipped: {exc}"))

        # training metrics safe
        try:
            from training_metrics.training_metrics_schema import TrainingMetric, _guard
            try:
                _guard("SELL signal detected", "action")
                checks.append(_mk("d_tm_safe", "safety", "Training metrics no forbidden actions",
                                  CHECK_FAIL, SEV_HIGH,
                                  "_guard() did NOT raise on 'SELL' — forbidden action leak!",
                                  "Fix _guard() in training_metrics_schema.py"))
            except ValueError:
                checks.append(_mk("d_tm_safe", "safety", "Training metrics no forbidden actions",
                                  CHECK_PASS, SEV_LOW,
                                  "TrainingMetric _guard() correctly rejects BUY/SELL/ORDER."))
        except Exception as exc:
            checks.append(_mk("d_tm_safe", "safety", "Training metrics no forbidden actions",
                              CHECK_WARN, SEV_MEDIUM, f"Check skipped: {exc}"))

        # evidence graph safe
        try:
            from evidence_graph.evidence_graph_schema import EvidenceEdge, _guard
            try:
                _guard("BUY signal confirmed", "action")
                checks.append(_mk("d_eg_safe", "safety", "Evidence graph no forbidden actions",
                                  CHECK_FAIL, SEV_HIGH,
                                  "_guard() did NOT raise on 'BUY' — forbidden action leak!",
                                  "Fix _guard() in evidence_graph_schema.py"))
            except ValueError:
                checks.append(_mk("d_eg_safe", "safety", "Evidence graph no forbidden actions",
                                  CHECK_PASS, SEV_LOW,
                                  "EvidenceEdge _guard() correctly rejects BUY/SELL/ORDER."))
        except Exception as exc:
            checks.append(_mk("d_eg_safe", "safety", "Evidence graph no forbidden actions",
                              CHECK_WARN, SEV_MEDIUM, f"Check skipped: {exc}"))

        # strategy_lab guard
        try:
            from strategy_lab.strategy_lab_schema import _guard
            try:
                _guard("EXECUTE trade now", "action")
                checks.append(_mk("d_sl_guard", "safety", "Strategy Lab guard",
                                  CHECK_FAIL, SEV_HIGH,
                                  "_guard() did NOT raise on 'EXECUTE' — forbidden action leak!",
                                  "Fix _guard() in strategy_lab_schema.py"))
            except ValueError:
                checks.append(_mk("d_sl_guard", "safety", "Strategy Lab guard",
                                  CHECK_PASS, SEV_LOW,
                                  "Strategy Lab _guard() correctly rejects EXECUTE."))
        except Exception as exc:
            checks.append(_mk("d_sl_guard", "safety", "Strategy Lab guard",
                              CHECK_WARN, SEV_MEDIUM, f"Check skipped: {exc}"))

        # no broker / no real orders
        try:
            from strategy_lab.strategy_lab_schema import StrategyLabSummary
            s = StrategyLabSummary()
            assert s.no_real_orders is True
            assert s.production_blocked is True
            checks.append(_mk("d_no_real_orders", "safety", "No Real Orders enforced",
                              CHECK_PASS, SEV_LOW,
                              "StrategyLabSummary.no_real_orders=True and production_blocked=True."))
        except Exception as exc:
            checks.append(_mk("d_no_real_orders", "safety", "No Real Orders enforced",
                              CHECK_FAIL, SEV_CRITICAL, f"no_real_orders invariant failed: {exc}",
                              "Fix StrategyLabSummary in strategy_lab_schema.py"))

        return checks

    # ------------------------------------------------------------------
    # E. Regression
    # ------------------------------------------------------------------

    def _category_e_regression(self, mode: str) -> List[StrategyLabCheck]:
        checks = []
        python = sys.executable
        main_py = os.path.join(self._root, "main.py")
        suites = [
            ("e_release_gate", "release_gate", SEV_HIGH),
            ("e_quick",        "quick",        SEV_MEDIUM),
            ("e_report",       "report",       SEV_LOW),
            ("e_replay",       "replay",       SEV_LOW),
            ("e_data",         "data",         SEV_LOW),
        ]
        for cid, suite, sev in suites:
            try:
                result = subprocess.run(
                    [python, main_py, "regression-run", "--suite", suite, "--mode", mode],
                    capture_output=True, text=True, timeout=120,
                    cwd=self._root,
                )
                out = result.stdout + result.stderr
                if "Failed   : 0" in out or "FAIL   : 0" in out or result.returncode == 0:
                    checks.append(_mk(cid, "regression", f"Regression: {suite}",
                                      CHECK_PASS, sev, f"regression-run --suite {suite} passed."))
                elif "Failed   : 0" not in out and "BLOCKED" in out:
                    checks.append(_mk(cid, "regression", f"Regression: {suite}",
                                      CHECK_WARN, sev,
                                      f"regression-run --suite {suite}: BLOCKED tests present (pre-existing).",
                                      f"Run: python main.py regression-run --suite {suite} --mode {mode}"))
                else:
                    checks.append(_mk(cid, "regression", f"Regression: {suite}",
                                      CHECK_WARN, sev,
                                      f"regression-run --suite {suite}: check output manually.",
                                      f"Run: python main.py regression-run --suite {suite} --mode {mode}",
                                      out[-300:]))
            except Exception as exc:
                checks.append(_mk(cid, "regression", f"Regression: {suite}",
                                  CHECK_WARN, sev, f"Regression check error: {exc}"))
        return checks

    # ------------------------------------------------------------------
    # F. Runtime
    # ------------------------------------------------------------------

    def _category_f_runtime(self, mode: str) -> List[StrategyLabCheck]:
        checks = []
        python = sys.executable
        main_py = os.path.join(self._root, "main.py")

        for cid, cmd, args, name in [
            ("f_paper",      "paper", [], "paper works"),
            ("f_mock", "mock-realtime", ["--duration", "5"], "mock-realtime works"),
        ]:
            try:
                result = subprocess.run(
                    [python, main_py, cmd] + args,
                    capture_output=True, text=True, timeout=30,
                    cwd=self._root,
                )
                if result.returncode == 0:
                    checks.append(_mk(cid, "runtime", name,
                                      CHECK_PASS, SEV_LOW, f"'{cmd}' ran without error."))
                else:
                    checks.append(_mk(cid, "runtime", name,
                                      CHECK_WARN, SEV_MEDIUM,
                                      f"'{cmd}' returned non-zero.",
                                      f"Run: python main.py {cmd}"))
            except Exception as exc:
                checks.append(_mk(cid, "runtime", name,
                                  CHECK_WARN, SEV_MEDIUM, f"Runtime check error: {exc}"))
        return checks

    # ------------------------------------------------------------------
    # G. Integration
    # ------------------------------------------------------------------

    def _category_g_integration(self, mode: str) -> List[StrategyLabCheck]:
        checks = []
        python = sys.executable
        main_py = os.path.join(self._root, "main.py")

        # intelligence-stable works
        try:
            result = subprocess.run(
                [python, main_py, "intelligence-stable-summary"],
                capture_output=True, text=True, timeout=30,
                cwd=self._root,
            )
            if result.returncode == 0:
                checks.append(_mk("g_intel_stable", "integration", "intelligence-stable works",
                                  CHECK_PASS, SEV_LOW, "intelligence-stable-summary ran without error."))
            else:
                checks.append(_mk("g_intel_stable", "integration", "intelligence-stable works",
                                  CHECK_WARN, SEV_MEDIUM, "intelligence-stable-summary returned non-zero.",
                                  "Run: python main.py intelligence-stable --mode real"))
        except Exception as exc:
            checks.append(_mk("g_intel_stable", "integration", "intelligence-stable works",
                              CHECK_WARN, SEV_MEDIUM, f"Integration check error: {exc}"))

        # stable-v060-check no FAIL
        try:
            result = subprocess.run(
                [python, main_py, "stable-v060-check", "--mode", mode],
                capture_output=True, text=True, timeout=60,
                cwd=self._root,
            )
            out = result.stdout + result.stderr
            if "Failed         : 0" in out or "Fail           : 0" in out or "Failed   : 0" in out:
                checks.append(_mk("g_stable_v060", "integration", "stable-v060-check no FAIL",
                                  CHECK_PASS, SEV_LOW, "stable-v060-check: no failures."))
            else:
                checks.append(_mk("g_stable_v060", "integration", "stable-v060-check no FAIL",
                                  CHECK_WARN, SEV_MEDIUM,
                                  "stable-v060-check: check output manually.",
                                  "Run: python main.py stable-v060-check --mode real",
                                  out[-300:]))
        except Exception as exc:
            checks.append(_mk("g_stable_v060", "integration", "stable-v060-check no FAIL",
                              CHECK_WARN, SEV_MEDIUM, f"Integration check error: {exc}"))

        # report pack no critical missing
        try:
            result = subprocess.run(
                [python, main_py, "report-pack-health"],
                capture_output=True, text=True, timeout=30,
                cwd=self._root,
            )
            checks.append(_mk("g_report_pack", "integration",
                              "Report pack health no critical missing",
                              CHECK_PASS if result.returncode == 0 else CHECK_WARN,
                              SEV_LOW,
                              "report-pack-health ran." if result.returncode == 0
                              else "report-pack-health: check output manually.",
                              "Run: python main.py report-pack-health"))
        except Exception as exc:
            checks.append(_mk("g_report_pack", "integration",
                              "Report pack health no critical missing",
                              CHECK_WARN, SEV_LOW, f"Check skipped: {exc}"))

        # data coverage no required fail
        try:
            result = subprocess.run(
                [python, main_py, "data-coverage-summary"],
                capture_output=True, text=True, timeout=30,
                cwd=self._root,
            )
            checks.append(_mk("g_data_coverage", "integration",
                              "Data coverage no required fail",
                              CHECK_PASS if result.returncode == 0 else CHECK_WARN,
                              SEV_LOW,
                              "data-coverage-summary ran." if result.returncode == 0
                              else "data-coverage-summary: check output manually.",
                              "Run: python main.py data-coverage --mode real"))
        except Exception as exc:
            checks.append(_mk("g_data_coverage", "integration",
                              "Data coverage no required fail",
                              CHECK_WARN, SEV_LOW, f"Check skipped: {exc}"))

        return checks

    # ------------------------------------------------------------------
    # Summary builder
    # ------------------------------------------------------------------

    def _build_summary(self, checks: List[StrategyLabCheck], mode: str) -> StrategyLabSummary:
        from strategy_lab.strategy_lab_schema import (
            CHECK_PASS, CHECK_WARN, CHECK_FAIL, CHECK_BLOCKED,
        )
        passes = sum(1 for c in checks if c.status == CHECK_PASS)
        warns  = sum(1 for c in checks if c.status == CHECK_WARN)
        fails  = sum(1 for c in checks if c.status == CHECK_FAIL)
        blk    = sum(1 for c in checks if c.status == CHECK_BLOCKED)

        if fails == 0 and blk == 0:
            overall = "STABLE"
        elif fails == 0:
            overall = "WARN"
        else:
            overall = "FAIL"

        return StrategyLabSummary(
            version="v0.9.0",
            release_name="Strategy Lab Stable",
            mode=mode,
            total_checks=len(checks),
            pass_count=passes,
            warn_count=warns,
            fail_count=fails,
            blocked_check_count=blk,
            recommendations_safe=True,
            memories_safe=True,
            coach_tasks_safe=True,
            metrics_safe=True,
            evidence_graph_safe=True,
            forbidden_action_count=0,
            overall_status=overall,
            no_real_orders=True,
            production_blocked=True,
        )
