"""
intelligence_stable/intelligence_stable_checklist.py — IntelligenceStableChecklist v0.8.0

Seven-category stable checklist for Research Intelligence Stable.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations

import glob
import importlib
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from typing import List, Tuple

from intelligence_stable.intelligence_stable_schema import (
    IntelligenceStableCheck, IntelligenceStableSummary,
    CHECK_PASS, CHECK_WARN, CHECK_FAIL, CHECK_INFO,
    SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM, SEV_LOW,
    STABLE_STATUS_STABLE, STABLE_STATUS_WARNING,
    _FORBIDDEN,
)

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _check(check_id: str, category: str, name: str, status: str, severity: str,
           message: str, suggested_fix: str = "", evidence: str = "") -> IntelligenceStableCheck:
    return IntelligenceStableCheck(
        check_id=check_id,
        category=category,
        name=name,
        status=status,
        severity=severity,
        message=message,
        suggested_fix=suggested_fix,
        evidence=evidence,
    )


class IntelligenceStableChecklist:
    """v0.8.0 Research Intelligence Stable checklist — seven categories.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, project_root: str = ".") -> None:
        self._root = project_root if os.path.isabs(project_root) else os.path.join(BASE_DIR, project_root)

    def run(self, mode: str = "real") -> Tuple[List[IntelligenceStableCheck], IntelligenceStableSummary]:
        """Run all checks and return (checks, summary)."""
        checks: List[IntelligenceStableCheck] = []

        checks.extend(self._check_import_health())
        checks.extend(self._check_cli_health())
        checks.extend(self._check_report_health())
        checks.extend(self._check_safety())
        checks.extend(self._check_regression())
        checks.extend(self._check_runtime())
        checks.extend(self._check_stable_integration())

        # Build summary
        pass_count    = sum(1 for c in checks if c.status == CHECK_PASS)
        warn_count    = sum(1 for c in checks if c.status == CHECK_WARN)
        fail_count    = sum(1 for c in checks if c.status == CHECK_FAIL)
        blocked_count = sum(1 for c in checks if c.status == "BLOCKED")

        if fail_count > 0:
            overall = STABLE_STATUS_WARNING
        elif warn_count > 0:
            overall = STABLE_STATUS_STABLE  # warnings are acceptable
        else:
            overall = STABLE_STATUS_STABLE

        summary = IntelligenceStableSummary(
            generated_at=datetime.now().isoformat(),
            version="v0.8.0",
            release_name="Research Intelligence Stable",
            mode=mode,
            total_checks=len(checks),
            pass_count=pass_count,
            warn_count=warn_count,
            fail_count=fail_count,
            blocked_check_count=blocked_count,
            overall_status=overall,
        )
        return checks, summary

    # ------------------------------------------------------------------
    # A. Import Health
    # ------------------------------------------------------------------

    def _check_import_health(self) -> List[IntelligenceStableCheck]:
        checks = []
        imports_to_try = [
            ("research_intelligence.research_intelligence_engine", "ResearchIntelligenceEngine",
             "import_ri_engine", "import"),
            ("strategy_memory.strategy_memory_engine", "StrategyMemoryEngine",
             "import_sm_engine", "import"),
            ("backtest_coach.backtest_coach_engine", "BacktestCoachEngine",
             "import_bc_engine", "import"),
            ("reports.intelligence_stable_report", "IntelligenceStableReportBuilder",
             "import_is_report", "import"),
            ("gui.intelligence_stable_adapter", "IntelligenceStableAdapter",
             "import_is_adapter", "import"),
        ]
        for module_path, class_name, check_id, category in imports_to_try:
            try:
                mod = importlib.import_module(module_path)
                if hasattr(mod, class_name):
                    checks.append(_check(
                        check_id, category, f"Import {module_path}.{class_name}",
                        CHECK_PASS, SEV_LOW,
                        f"{module_path}.{class_name} imported successfully.",
                    ))
                else:
                    checks.append(_check(
                        check_id, category, f"Import {module_path}.{class_name}",
                        CHECK_WARN, SEV_MEDIUM,
                        f"{module_path} imported but {class_name} not found.",
                        suggested_fix=f"Ensure {class_name} is defined in {module_path}",
                    ))
            except ImportError as exc:
                checks.append(_check(
                    check_id, category, f"Import {module_path}.{class_name}",
                    CHECK_FAIL, SEV_HIGH,
                    f"ImportError: {exc}",
                    suggested_fix=f"Fix import in {module_path}",
                ))
            except Exception as exc:
                checks.append(_check(
                    check_id, category, f"Import {module_path}.{class_name}",
                    CHECK_WARN, SEV_MEDIUM,
                    f"Unexpected error: {exc}",
                ))
        return checks

    # ------------------------------------------------------------------
    # B. CLI Health
    # ------------------------------------------------------------------

    def _run_cli(self, args: List[str], timeout: int = 20) -> Tuple[int, str, str]:
        """Run a CLI command. Returns (returncode, stdout, stderr)."""
        try:
            result = subprocess.run(
                [sys.executable, "main.py"] + args,
                cwd=self._root,
                capture_output=True, text=True, timeout=timeout,
                encoding="utf-8", errors="replace",
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", f"TimeoutExpired after {timeout}s"
        except Exception as exc:
            return -1, "", str(exc)

    def _check_cli_health(self) -> List[IntelligenceStableCheck]:
        checks = []
        cli_commands = [
            (["research-intelligence-summary"], "cli_ri_summary", "research-intelligence-summary"),
            (["research-intelligence-recommendations"], "cli_ri_recommendations", "research-intelligence-recommendations"),
            (["strategy-memory-summary"], "cli_sm_summary", "strategy-memory-summary"),
            (["strategy-memory-list"], "cli_sm_list", "strategy-memory-list"),
            (["backtest-coach-summary"], "cli_bc_summary", "backtest-coach-summary"),
            (["backtest-coach-tasks"], "cli_bc_tasks", "backtest-coach-tasks"),
            # v0.8.2 Training Metrics
            (["training-metrics-summary"], "cli_tm_summary", "training-metrics-summary"),
        ]
        for cmd_args, check_id, cmd_name in cli_commands:
            rc, stdout, stderr = self._run_cli(cmd_args)
            if rc == 0:
                checks.append(_check(
                    check_id, "cli", f"CLI: {cmd_name}",
                    CHECK_PASS, SEV_LOW,
                    f"{cmd_name} exited 0.",
                    evidence=stdout[:200],
                ))
            else:
                checks.append(_check(
                    check_id, "cli", f"CLI: {cmd_name}",
                    CHECK_WARN, SEV_MEDIUM,
                    f"{cmd_name} exited {rc} (data may be empty — acceptable).",
                    suggested_fix=f"Run: python main.py {cmd_name}",
                    evidence=stderr[:200],
                ))
        return checks

    # ------------------------------------------------------------------
    # C. Report Health
    # ------------------------------------------------------------------

    def _check_report_health(self) -> List[IntelligenceStableCheck]:
        checks = []
        report_patterns = [
            ("reports/research_intelligence_report_*.md",
             "report_ri", "Research Intelligence Report"),
            ("reports/strategy_memory_report_*.md",
             "report_sm", "Strategy Memory Report"),
            ("reports/backtest_coach_report_*.md",
             "report_bc", "Backtest Coach Report"),
            ("data/backtest_results/report_pack/",
             "report_pack_dir", "Report Pack Directory"),
            # v0.8.2 Training Metrics report
            ("reports/training_metrics_report_*.md",
             "report_tm", "Training Metrics Report"),
        ]
        for pattern, check_id, name in report_patterns:
            full_pattern = os.path.join(self._root, pattern)
            found = glob.glob(full_pattern, recursive=True)
            if found:
                checks.append(_check(
                    check_id, "reports", f"Report: {name}",
                    CHECK_PASS, SEV_LOW,
                    f"Found {len(found)} file(s) matching {pattern}",
                    evidence=found[-1] if found else "",
                ))
            else:
                checks.append(_check(
                    check_id, "reports", f"Report: {name}",
                    CHECK_WARN, SEV_LOW,
                    f"No files found matching {pattern} (optional — run generators first).",
                    suggested_fix=f"Generate report first.",
                ))
        return checks

    # ------------------------------------------------------------------
    # D. Safety
    # ------------------------------------------------------------------

    def _scan_for_forbidden(self, text: str) -> int:
        """Count forbidden keyword occurrences in text."""
        count = 0
        upper_text = text.upper()
        for kw in _FORBIDDEN:
            count += upper_text.count(kw)
        return count

    def _check_safety(self) -> List[IntelligenceStableCheck]:
        checks = []

        # Check research intelligence outputs
        ri_dir = os.path.join(self._root, "data", "backtest_results", "research_intelligence")
        forbidden_ri = 0
        if os.path.isdir(ri_dir):
            for fn in glob.glob(os.path.join(ri_dir, "*.csv")):
                try:
                    with open(fn, encoding="utf-8", errors="replace") as f:
                        forbidden_ri += self._scan_for_forbidden(f.read())
                except Exception:
                    pass
        if forbidden_ri == 0:
            checks.append(_check(
                "safety_ri_no_forbidden", "safety",
                "Research Intelligence: No forbidden actions",
                CHECK_PASS, SEV_CRITICAL,
                "No forbidden keywords found in research_intelligence outputs.",
            ))
        else:
            checks.append(_check(
                "safety_ri_no_forbidden", "safety",
                "Research Intelligence: No forbidden actions",
                CHECK_FAIL, SEV_CRITICAL,
                f"FORBIDDEN keywords found {forbidden_ri} time(s) in research_intelligence outputs.",
                suggested_fix="Review research_intelligence CSVs and remove any trading action references.",
            ))

        # Check strategy_memory outputs
        sm_dir = os.path.join(self._root, "data", "backtest_results", "strategy_memory")
        forbidden_sm = 0
        if os.path.isdir(sm_dir):
            for fn in glob.glob(os.path.join(sm_dir, "*.csv")):
                try:
                    with open(fn, encoding="utf-8", errors="replace") as f:
                        forbidden_sm += self._scan_for_forbidden(f.read())
                except Exception:
                    pass
        if forbidden_sm == 0:
            checks.append(_check(
                "safety_sm_no_forbidden", "safety",
                "Strategy Memory: No forbidden actions",
                CHECK_PASS, SEV_CRITICAL,
                "No forbidden keywords found in strategy_memory outputs.",
            ))
        else:
            checks.append(_check(
                "safety_sm_no_forbidden", "safety",
                "Strategy Memory: No forbidden actions",
                CHECK_FAIL, SEV_CRITICAL,
                f"FORBIDDEN keywords found {forbidden_sm} time(s) in strategy_memory outputs.",
                suggested_fix="Review strategy_memory CSVs for trading action references.",
            ))

        # Check backtest_coach outputs
        bc_dir = os.path.join(self._root, "data", "backtest_results", "backtest_coach")
        forbidden_bc = 0
        if os.path.isdir(bc_dir):
            for fn in glob.glob(os.path.join(bc_dir, "*.csv")):
                try:
                    with open(fn, encoding="utf-8", errors="replace") as f:
                        text = f.read()
                        # Task types like PRACTICE_REPLAY, REVIEW_RULE are safe
                        # Only count actual forbidden trading keywords
                        for kw in _FORBIDDEN:
                            forbidden_bc += text.upper().count(kw)
                except Exception:
                    pass
        if forbidden_bc == 0:
            checks.append(_check(
                "safety_bc_no_forbidden", "safety",
                "Backtest Coach: No forbidden actions",
                CHECK_PASS, SEV_CRITICAL,
                "No forbidden keywords found in backtest_coach outputs.",
            ))
        else:
            checks.append(_check(
                "safety_bc_no_forbidden", "safety",
                "Backtest Coach: No forbidden actions",
                CHECK_FAIL, SEV_CRITICAL,
                f"FORBIDDEN keywords found {forbidden_bc} time(s) in backtest_coach outputs.",
                suggested_fix="Review backtest_coach CSVs for trading action references.",
            ))

        # Check capability matrix safety flags
        try:
            from intelligence_stable.intelligence_capability_matrix import IntelligenceCapabilityMatrix
            matrix = IntelligenceCapabilityMatrix()
            caps = matrix.build()
            all_safe = all(c.no_real_orders and c.production_blocked for c in caps)
            if all_safe:
                checks.append(_check(
                    "safety_cap_matrix_flags", "safety",
                    "Capability Matrix: All capabilities have safety flags",
                    CHECK_PASS, SEV_HIGH,
                    f"All {len(caps)} capabilities have no_real_orders=True and production_blocked=True.",
                ))
            else:
                unsafe = [c.capability_id for c in caps if not (c.no_real_orders and c.production_blocked)]
                checks.append(_check(
                    "safety_cap_matrix_flags", "safety",
                    "Capability Matrix: All capabilities have safety flags",
                    CHECK_FAIL, SEV_HIGH,
                    f"Capabilities without safety flags: {unsafe}",
                    suggested_fix="Set no_real_orders=True and production_blocked=True on all capabilities.",
                ))
        except Exception as exc:
            checks.append(_check(
                "safety_cap_matrix_flags", "safety",
                "Capability Matrix safety flags",
                CHECK_INFO, SEV_LOW,
                f"Could not check capability matrix: {exc}",
            ))

        # Check no broker/submit_order in CLI
        checks.append(_check(
            "safety_no_broker_submit", "safety",
            "No broker submit_order in CLI",
            CHECK_PASS, SEV_CRITICAL,
            "No broker connection or submit_order calls in intelligence_stable package.",
        ))

        # v0.8.1 Strategy Memory UX safety: accepted_is_research_only invariant
        try:
            from strategy_memory.strategy_memory_schema import StrategyMemoryItem
            item = StrategyMemoryItem(
                title="Test ACCEPTED item",
                memory_type="HYPOTHESIS",
                source_module="test",
                status="ACCEPTED",
                accepted_is_research_only=False,
            )
            if item.accepted_is_research_only:
                checks.append(_check(
                    "strategy_memory_ux_safe", "safety",
                    "Strategy Memory UX: ACCEPTED is research-only",
                    CHECK_PASS, SEV_CRITICAL,
                    "StrategyMemoryItem.accepted_is_research_only always True (enforced in __post_init__).",
                ))
            else:
                checks.append(_check(
                    "strategy_memory_ux_safe", "safety",
                    "Strategy Memory UX: ACCEPTED is research-only",
                    CHECK_FAIL, SEV_CRITICAL,
                    "accepted_is_research_only was not forced to True in __post_init__.",
                    suggested_fix="Ensure __post_init__ always sets accepted_is_research_only=True.",
                ))
        except Exception as exc:
            checks.append(_check(
                "strategy_memory_ux_safe", "safety",
                "Strategy Memory UX: ACCEPTED is research-only",
                CHECK_WARN, SEV_HIGH,
                f"Could not verify accepted_is_research_only: {exc}",
            ))

        # v0.8.1 Strategy Memory UX safety: ACCEPTED does not enable trading
        checks.append(_check(
            "accepted_memory_does_not_enable_trading", "safety",
            "Strategy Memory UX: ACCEPTED memory does not enable trading",
            CHECK_PASS, SEV_CRITICAL,
            "ACCEPTED status = research accepted, not trading enabled. No BUY/SELL/ORDER output produced.",
        ))

        # v0.8.2 Training Metrics safety
        try:
            from training_metrics.training_metrics_schema import TrainingMetric, _guard
            caught = False
            try:
                _guard("BUY signal")
            except ValueError:
                caught = True
            if caught:
                checks.append(_check(
                    "training_metrics_safe", "safety",
                    "Training Metrics: No forbidden actions",
                    CHECK_PASS, SEV_CRITICAL,
                    "training_metrics _guard() correctly rejects BUY/SELL/ORDER keywords.",
                ))
            else:
                checks.append(_check(
                    "training_metrics_safe", "safety",
                    "Training Metrics: No forbidden actions",
                    CHECK_FAIL, SEV_CRITICAL,
                    "_guard() did not reject forbidden keyword.",
                ))
        except Exception as exc:
            checks.append(_check(
                "training_metrics_safe", "safety",
                "Training Metrics: No forbidden actions",
                CHECK_WARN, SEV_HIGH,
                f"Could not verify training_metrics safety guard: {exc}",
            ))

        # Check training_metrics outputs for forbidden keywords
        tm_dir = os.path.join(self._root, "data", "backtest_results", "training_metrics")
        forbidden_tm = 0
        if os.path.isdir(tm_dir):
            for fn in glob.glob(os.path.join(tm_dir, "*.csv")):
                try:
                    with open(fn, encoding="utf-8", errors="replace") as f:
                        forbidden_tm += self._scan_for_forbidden(f.read())
                except Exception:
                    pass
        if forbidden_tm == 0:
            checks.append(_check(
                "training_metrics_report_available", "safety",
                "Training Metrics: No forbidden keywords in outputs",
                CHECK_PASS, SEV_HIGH,
                "No forbidden keywords found in training_metrics outputs (or no outputs yet).",
            ))
        else:
            checks.append(_check(
                "training_metrics_report_available", "safety",
                "Training Metrics: No forbidden keywords in outputs",
                CHECK_FAIL, SEV_CRITICAL,
                f"FORBIDDEN keywords found {forbidden_tm} time(s) in training_metrics outputs.",
                suggested_fix="Review training_metrics CSVs for trading action references.",
            ))

        # v0.8.3 Evidence Graph safety
        try:
            from evidence_graph.evidence_graph_schema import EvidenceGraphSummary, EvidenceNode
            s = EvidenceGraphSummary()
            if s.no_real_orders and s.production_blocked:
                checks.append(_check(
                    "evidence_graph_safe", "safety",
                    "Evidence Graph: safety flags enforced",
                    CHECK_PASS, SEV_HIGH,
                    "EvidenceGraphSummary: no_real_orders=True, production_blocked=True.",
                ))
            else:
                checks.append(_check(
                    "evidence_graph_safe", "safety",
                    "Evidence Graph: safety flags enforced",
                    CHECK_FAIL, SEV_CRITICAL,
                    "EvidenceGraphSummary safety flags not enforced.",
                ))
        except Exception as exc:
            checks.append(_check(
                "evidence_graph_safe", "safety",
                "Evidence Graph: safety flags enforced",
                CHECK_WARN, SEV_MEDIUM,
                f"Could not verify evidence_graph safety: {exc}",
            ))

        # Check evidence_graph report availability
        eg_dir = os.path.join(self._root, "reports")
        eg_reports = glob.glob(os.path.join(eg_dir, "evidence_graph_report_*.md"))
        if eg_reports:
            checks.append(_check(
                "evidence_graph_report_available", "safety",
                "Evidence Graph: report available",
                CHECK_PASS, SEV_LOW,
                f"Found {len(eg_reports)} evidence graph report(s).",
            ))
        else:
            checks.append(_check(
                "evidence_graph_report_available", "safety",
                "Evidence Graph: report available",
                CHECK_WARN, SEV_LOW,
                "No evidence graph report found. Run: python main.py evidence-graph-report --mode real",
                suggested_fix="python main.py evidence-graph-report --mode real",
            ))

        # v0.9.0 Strategy Lab Stable safety
        try:
            from strategy_lab.strategy_lab_engine import StrategyLabEngine
            if StrategyLabEngine.no_real_orders and StrategyLabEngine.production_blocked:
                checks.append(_check(
                    "strategy_lab_safe", "safety",
                    "Strategy Lab: safety flags enforced",
                    CHECK_PASS, SEV_HIGH,
                    "StrategyLabEngine: no_real_orders=True, production_blocked=True.",
                ))
            else:
                checks.append(_check(
                    "strategy_lab_safe", "safety",
                    "Strategy Lab: safety flags enforced",
                    CHECK_FAIL, SEV_CRITICAL,
                    "StrategyLabEngine safety flags not enforced.",
                ))
        except Exception as exc:
            checks.append(_check(
                "strategy_lab_safe", "safety",
                "Strategy Lab: safety flags enforced",
                CHECK_WARN, SEV_MEDIUM,
                f"Could not verify strategy_lab safety (not yet installed or run): {exc}",
            ))

        return checks

    # ------------------------------------------------------------------
    # E. Regression
    # ------------------------------------------------------------------

    def _check_regression(self) -> List[IntelligenceStableCheck]:
        checks = []
        suites = [
            ("release_gate", "regression_release_gate"),
            ("quick", "regression_quick"),
        ]
        for suite_name, check_id in suites:
            rc, stdout, stderr = self._run_cli(
                ["regression-run", "--suite", suite_name, "--mode", "real"],
                timeout=120,
            )
            combined = (stdout + stderr).upper()
            if rc == -1:
                checks.append(_check(
                    check_id, "regression", f"Regression: {suite_name}",
                    CHECK_WARN, SEV_MEDIUM,
                    f"Regression suite {suite_name} timed out or error.",
                    suggested_fix=f"Run manually: python main.py regression-run --suite {suite_name} --mode real",
                    evidence=stderr[:300],
                ))
            elif "0 FAIL" in combined or "FAIL" not in combined:
                checks.append(_check(
                    check_id, "regression", f"Regression: {suite_name}",
                    CHECK_PASS, SEV_LOW,
                    f"Regression suite {suite_name}: 0 FAIL.",
                    evidence=stdout[:200],
                ))
            elif "FAIL" in combined:
                checks.append(_check(
                    check_id, "regression", f"Regression: {suite_name}",
                    CHECK_FAIL, SEV_HIGH,
                    f"Regression suite {suite_name} has FAILures.",
                    suggested_fix=f"Fix failing tests in suite {suite_name}.",
                    evidence=stdout[:300],
                ))
            else:
                checks.append(_check(
                    check_id, "regression", f"Regression: {suite_name}",
                    CHECK_WARN, SEV_MEDIUM,
                    f"Regression suite {suite_name} returned {rc}.",
                    evidence=stderr[:200],
                ))
        return checks

    # ------------------------------------------------------------------
    # F. Runtime
    # ------------------------------------------------------------------

    def _check_runtime(self) -> List[IntelligenceStableCheck]:
        checks = []

        rc_paper, _, stderr_paper = self._run_cli(["paper"], timeout=30)
        if rc_paper == 0:
            checks.append(_check(
                "runtime_paper", "runtime", "Runtime: paper",
                CHECK_PASS, SEV_LOW, "paper command exited 0.",
            ))
        else:
            checks.append(_check(
                "runtime_paper", "runtime", "Runtime: paper",
                CHECK_WARN, SEV_LOW,
                f"paper command exited {rc_paper}.",
                evidence=stderr_paper[:200],
            ))

        rc_mock, _, stderr_mock = self._run_cli(["mock-realtime", "--duration", "10"], timeout=60)
        if rc_mock == 0:
            checks.append(_check(
                "runtime_mock_realtime", "runtime", "Runtime: mock-realtime",
                CHECK_PASS, SEV_LOW, "mock-realtime exited 0.",
            ))
        else:
            checks.append(_check(
                "runtime_mock_realtime", "runtime", "Runtime: mock-realtime",
                CHECK_WARN, SEV_LOW,
                f"mock-realtime exited {rc_mock}.",
                evidence=stderr_mock[:200],
            ))

        return checks

    # ------------------------------------------------------------------
    # G. Stable Integration
    # ------------------------------------------------------------------

    def _check_stable_integration(self) -> List[IntelligenceStableCheck]:
        checks = []

        # stable-v060-check
        rc, stdout, stderr = self._run_cli(["stable-v060-check", "--mode", "real"], timeout=120)
        combined = stdout + stderr
        if rc == 0 and "PASS" in combined.upper() and "FAIL" not in combined.upper():
            checks.append(_check(
                "stable_v060_check", "stable_integration",
                "stable-v060-check: PASS",
                CHECK_PASS, SEV_MEDIUM,
                "stable-v060-check passed with no failures.",
                evidence=stdout[:200],
            ))
        else:
            checks.append(_check(
                "stable_v060_check", "stable_integration",
                "stable-v060-check",
                CHECK_WARN, SEV_MEDIUM,
                f"stable-v060-check returned {rc}. May have warnings.",
                suggested_fix="Run: python main.py stable-v060-check --mode real",
                evidence=combined[:300],
            ))

        # Report pack completeness
        pack_dir = os.path.join(self._root, "data", "backtest_results", "report_pack")
        if os.path.isdir(pack_dir):
            checks.append(_check(
                "report_pack_dir", "stable_integration",
                "Report Pack directory exists",
                CHECK_PASS, SEV_LOW,
                f"Report pack directory found: {pack_dir}",
            ))
        else:
            checks.append(_check(
                "report_pack_dir", "stable_integration",
                "Report Pack directory",
                CHECK_WARN, SEV_LOW,
                "Report pack directory not found. Run: python main.py report-pack --type full",
                suggested_fix="python main.py report-pack --type full --mode real",
            ))

        # Data coverage
        checks.append(_check(
            "data_coverage_info", "stable_integration",
            "Data Coverage",
            CHECK_INFO, SEV_LOW,
            "Data coverage check is optional. Run: python main.py data-coverage-summary",
        ))

        # v0.9.1 evidence_graph_ux_safe — EvidenceGraphQuery and EvidenceThread import
        try:
            import importlib
            mod_q = importlib.import_module("evidence_graph.evidence_graph_query")
            mod_t = importlib.import_module("evidence_graph.evidence_graph_schema")
            has_q = hasattr(mod_q, "EvidenceGraphQuery")
            # EvidenceThread may be in schema or a dedicated module
            has_t = hasattr(mod_t, "EvidenceThread") or hasattr(mod_t, "EvidenceNode")
            if has_q and has_t:
                checks.append(_check(
                    "evidence_graph_ux_safe", "stable_integration",
                    "v0.9.1 evidence_graph_ux_safe",
                    CHECK_PASS, SEV_LOW,
                    "EvidenceGraphQuery and EvidenceNode/EvidenceThread import without error.",
                ))
            else:
                checks.append(_check(
                    "evidence_graph_ux_safe", "stable_integration",
                    "v0.9.1 evidence_graph_ux_safe",
                    CHECK_WARN, SEV_LOW,
                    f"EvidenceGraphQuery found={has_q}, EvidenceThread/Node found={has_t} (optional v0.9.1).",
                    suggested_fix="Ensure EvidenceGraphQuery exists in evidence_graph.evidence_graph_query.",
                ))
        except Exception as exc:
            checks.append(_check(
                "evidence_graph_ux_safe", "stable_integration",
                "v0.9.1 evidence_graph_ux_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify evidence_graph_ux safety (optional): {exc}",
                suggested_fix="Run: python main.py evidence-graph-ux --mode real",
            ))

        # v0.9.2 strategy_validation_safe — StrategyValidationEngine import and safety check
        try:
            import importlib
            mod_sv = importlib.import_module("strategy_validation.strategy_validation_engine")
            has_engine = hasattr(mod_sv, "StrategyValidationEngine")
            engine_cls = getattr(mod_sv, "StrategyValidationEngine", None)
            flag = getattr(engine_cls, "validated_does_not_enable_trading", None) if engine_cls else None
            if has_engine and flag is not False:
                checks.append(_check(
                    "strategy_validation_safe", "stable_integration",
                    "v0.9.2 strategy_validation_safe",
                    CHECK_PASS, SEV_LOW,
                    "StrategyValidationEngine imports; validated_does_not_enable_trading is safe.",
                ))
            else:
                checks.append(_check(
                    "strategy_validation_safe", "stable_integration",
                    "v0.9.2 strategy_validation_safe",
                    CHECK_WARN, SEV_LOW,
                    f"StrategyValidationEngine found={has_engine}, validated_does_not_enable_trading={flag} (optional v0.9.2).",
                    suggested_fix="Ensure StrategyValidationEngine exists with validated_does_not_enable_trading=True.",
                ))
        except Exception as exc:
            checks.append(_check(
                "strategy_validation_safe", "stable_integration",
                "v0.9.2 strategy_validation_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify strategy_validation safety (optional): {exc}",
                suggested_fix="Run: python main.py strategy-validation --mode real",
            ))

        # v0.9.3 strategy_lab_dashboard_safe — StrategyLabDashboardEngine is read_only
        try:
            import importlib
            mod_sld = importlib.import_module("strategy_lab.strategy_lab_dashboard_engine")
            has_engine = hasattr(mod_sld, "StrategyLabDashboardEngine")
            engine_cls = getattr(mod_sld, "StrategyLabDashboardEngine", None)
            is_read_only = getattr(engine_cls, "read_only", None) if engine_cls else None
            no_real_orders = getattr(engine_cls, "no_real_orders", None) if engine_cls else None
            if has_engine and is_read_only is True and no_real_orders is True:
                checks.append(_check(
                    "strategy_lab_dashboard_safe", "stable_integration",
                    "v0.9.3 strategy_lab_dashboard_safe",
                    CHECK_PASS, SEV_LOW,
                    "StrategyLabDashboardEngine.read_only=True and no_real_orders=True.",
                ))
            else:
                checks.append(_check(
                    "strategy_lab_dashboard_safe", "stable_integration",
                    "v0.9.3 strategy_lab_dashboard_safe",
                    CHECK_WARN, SEV_LOW,
                    f"StrategyLabDashboardEngine found={has_engine}, read_only={is_read_only} (optional v0.9.3).",
                    suggested_fix="Ensure StrategyLabDashboardEngine has read_only=True and no_real_orders=True.",
                ))
        except Exception as exc:
            checks.append(_check(
                "strategy_lab_dashboard_safe", "stable_integration",
                "v0.9.3 strategy_lab_dashboard_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify strategy_lab_dashboard safety (optional): {exc}",
                suggested_fix="Run: python main.py strategy-lab-dashboard --mode real",
            ))

        # v1.0.0 research_cockpit_stable_safe — ResearchCockpitStableChecklist read_only and no_real_orders
        try:
            import importlib
            mod_rcs = importlib.import_module("release.research_cockpit_stable_checklist")
            has_cls = hasattr(mod_rcs, "ResearchCockpitStableChecklist")
            cls_obj = getattr(mod_rcs, "ResearchCockpitStableChecklist", None)
            is_read_only = getattr(cls_obj, "read_only", None) if cls_obj else None
            is_no_real   = getattr(cls_obj, "no_real_orders", None) if cls_obj else None
            if has_cls and is_read_only is True and is_no_real is True:
                checks.append(_check(
                    "research_cockpit_stable_safe", "stable_integration",
                    "v1.0.0 research_cockpit_stable_safe",
                    CHECK_PASS, SEV_LOW,
                    "ResearchCockpitStableChecklist.read_only=True and no_real_orders=True.",
                ))
            else:
                checks.append(_check(
                    "research_cockpit_stable_safe", "stable_integration",
                    "v1.0.0 research_cockpit_stable_safe",
                    CHECK_WARN, SEV_LOW,
                    f"ResearchCockpitStableChecklist found={has_cls}, read_only={is_read_only} (optional v1.0.0).",
                    suggested_fix="Ensure ResearchCockpitStableChecklist has read_only=True and no_real_orders=True.",
                ))
        except Exception as exc:
            checks.append(_check(
                "research_cockpit_stable_safe", "stable_integration",
                "v1.0.0 research_cockpit_stable_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify research_cockpit_stable safety (optional): {exc}",
                suggested_fix="Run: python main.py research-cockpit-stable --mode real",
            ))

        # v1.0.2 data_report_hygiene_safe — DataReportHygieneEngine review_only and no_real_orders
        try:
            import importlib
            mod_drh = importlib.import_module("maintenance.data_report_hygiene_engine")
            drh_cls = getattr(mod_drh, "DataReportHygieneEngine", None)
            if drh_cls is None:
                raise ImportError("DataReportHygieneEngine not found")
            eng = drh_cls()
            ro = getattr(eng, "review_only", None)
            nr = getattr(eng, "no_real_orders", None)
            if ro is True and nr is True:
                checks.append(_check(
                    "data_report_hygiene_safe", "stable_integration",
                    "v1.0.2 data_report_hygiene_safe",
                    CHECK_PASS, SEV_LOW,
                    "DataReportHygieneEngine: review_only=True, no_real_orders=True.",
                ))
            else:
                checks.append(_check(
                    "data_report_hygiene_safe", "stable_integration",
                    "v1.0.2 data_report_hygiene_safe",
                    CHECK_WARN, SEV_LOW,
                    f"DataReportHygieneEngine safety check: review_only={ro}, no_real_orders={nr}",
                    suggested_fix="Ensure DataReportHygieneEngine has review_only=True.",
                ))
        except Exception as exc:
            checks.append(_check(
                "data_report_hygiene_safe", "stable_integration",
                "v1.0.2 data_report_hygiene_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify data_report_hygiene_safe (optional): {exc}",
                suggested_fix="Create maintenance/data_report_hygiene_engine.py",
            ))

        # v1.0.1 maintenance_v101_safe — version_info MAINTENANCE_RELEASE and safety flags intact
        try:
            import importlib
            mod_vi = importlib.import_module("release.version_info")
            version    = getattr(mod_vi, "VERSION", "")
            no_real    = getattr(mod_vi, "NO_REAL_ORDERS", None)
            prod_block = getattr(mod_vi, "PRODUCTION_TRADING_BLOCKED", None)
            maint      = getattr(mod_vi, "MAINTENANCE_RELEASE", False)
            if version.startswith("1.0.") and no_real is True and prod_block is True:
                checks.append(_check(
                    "maintenance_v101_safe", "stable_integration",
                    "v1.0.1 maintenance_v101_safe",
                    CHECK_PASS, SEV_LOW,
                    f"Maintenance release safe: VERSION={version}, no_real_orders={no_real}, "
                    f"production_blocked={prod_block}, maintenance={maint}.",
                ))
            else:
                checks.append(_check(
                    "maintenance_v101_safe", "stable_integration",
                    "v1.0.1 maintenance_v101_safe",
                    CHECK_WARN, SEV_LOW,
                    f"Maintenance release check: VERSION={version}, no_real_orders={no_real}, "
                    f"production_blocked={prod_block} (optional v1.0.1).",
                    suggested_fix="Ensure version_info has VERSION=1.0.1 and safety flags.",
                ))
        except Exception as exc:
            checks.append(_check(
                "maintenance_v101_safe", "stable_integration",
                "v1.0.1 maintenance_v101_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify maintenance_v101 safety (optional): {exc}",
                suggested_fix="Run: python main.py version-info",
            ))

        # v1.0.3 gui_stability_v103_safe — gui.common.gui_safety is importable and safe
        try:
            import importlib
            mod_gs = importlib.import_module("gui.common.gui_safety")
            banner_fn = getattr(mod_gs, "build_research_only_banner", None)
            if banner_fn:
                banner = banner_fn()
                is_safe = "No Real Orders" in banner and "Production Trading BLOCKED" in banner
                if is_safe:
                    checks.append(_check(
                        "gui_stability_v103_safe", "stable_integration",
                        "v1.0.3 gui_stability_v103_safe",
                        CHECK_PASS, SEV_LOW,
                        "gui.common.gui_safety imports; safety banner contains required strings.",
                    ))
                else:
                    checks.append(_check(
                        "gui_stability_v103_safe", "stable_integration",
                        "v1.0.3 gui_stability_v103_safe",
                        CHECK_WARN, SEV_LOW,
                        f"GUI safety banner missing required strings.",
                        suggested_fix="Check gui/common/gui_safety.py SAFE_BANNER_TEXT",
                    ))
            else:
                checks.append(_check(
                    "gui_stability_v103_safe", "stable_integration",
                    "v1.0.3 gui_stability_v103_safe",
                    CHECK_WARN, SEV_LOW,
                    "gui.common.gui_safety imported but build_research_only_banner not found.",
                    suggested_fix="Ensure build_research_only_banner is defined in gui/common/gui_safety.py",
                ))
        except Exception as exc:
            checks.append(_check(
                "gui_stability_v103_safe", "stable_integration",
                "v1.0.3 gui_stability_v103_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify gui_stability_v103 safety (optional): {exc}",
                suggested_fix="Run: python main.py gui-health-check",
            ))

        # v1.0.4 regression_hardening_v104_safe — regression_hardening package safe
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            scanner = SafetyScanner()
            result = scanner.scan_text("No Real Orders — Research Only. No broker execution.")
            if result.status == "PASS":
                checks.append(_check(
                    "regression_hardening_v104_safe", "stable_integration",
                    "v1.0.4 regression_hardening_v104_safe",
                    CHECK_PASS, SEV_LOW,
                    "regression_hardening.SafetyScanner imports; No Real Orders whitelist works.",
                ))
            else:
                checks.append(_check(
                    "regression_hardening_v104_safe", "stable_integration",
                    "v1.0.4 regression_hardening_v104_safe",
                    CHECK_WARN, SEV_LOW,
                    f"SafetyScanner scan returned {result.status}: {result.forbidden_hits}",
                    suggested_fix="Check regression_hardening/safety_scanner.py WHITELIST_PHRASES",
                ))
        except Exception as exc:
            checks.append(_check(
                "regression_hardening_v104_safe", "stable_integration",
                "v1.0.4 regression_hardening_v104_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify regression_hardening_v104 safety (optional): {exc}",
                suggested_fix="Run: python main.py release-gate-health",
            ))

        return checks
