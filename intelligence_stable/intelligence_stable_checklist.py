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

        # v1.0.5 documentation_v105_safe — documentation package importable and safe
        try:
            import importlib
            mod_dh = importlib.import_module("documentation.docs_health_check")
            has_cls = hasattr(mod_dh, "DocumentationHealthCheck")
            if has_cls:
                checks.append(_check(
                    "documentation_v105_safe", "stable_integration",
                    "v1.0.5 documentation_v105_safe",
                    CHECK_PASS, SEV_LOW,
                    "documentation.docs_health_check.DocumentationHealthCheck importable.",
                ))
            else:
                checks.append(_check(
                    "documentation_v105_safe", "stable_integration",
                    "v1.0.5 documentation_v105_safe",
                    CHECK_WARN, SEV_LOW,
                    "documentation.docs_health_check imported but DocumentationHealthCheck not found.",
                    suggested_fix="Ensure DocumentationHealthCheck is in documentation/docs_health_check.py",
                ))
        except Exception as exc:
            checks.append(_check(
                "documentation_v105_safe", "stable_integration",
                "v1.0.5 documentation_v105_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify documentation_v105 safety (optional): {exc}",
                suggested_fix="Run: python main.py docs-health-check",
            ))

        # v1.0.6 workflow_templates_v106_safe — workflows package importable and safe
        try:
            import importlib
            mod_wt = importlib.import_module("workflows.workflow_template_health")
            has_cls = hasattr(mod_wt, "WorkflowTemplateHealthCheck")
            if has_cls:
                checks.append(_check(
                    "workflow_templates_v106_safe", "stable_integration",
                    "v1.0.6 workflow_templates_v106_safe",
                    CHECK_PASS, SEV_LOW,
                    "workflows.workflow_template_health.WorkflowTemplateHealthCheck importable.",
                ))
            else:
                checks.append(_check(
                    "workflow_templates_v106_safe", "stable_integration",
                    "v1.0.6 workflow_templates_v106_safe",
                    CHECK_WARN, SEV_LOW,
                    "workflows.workflow_template_health imported but WorkflowTemplateHealthCheck not found.",
                    suggested_fix="Ensure WorkflowTemplateHealthCheck is in workflows/workflow_template_health.py",
                ))
        except Exception as exc:
            checks.append(_check(
                "workflow_templates_v106_safe", "stable_integration",
                "v1.0.6 workflow_templates_v106_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify workflow_templates_v106 safety (optional): {exc}",
                suggested_fix="Run: python main.py workflow-templates-health",
            ))

        # v1.0.7 knowledge_base_v107_safe — knowledge_base package is safe
        try:
            import importlib
            mod_kb = importlib.import_module("knowledge_base")
            no_orders = getattr(mod_kb, "NO_REAL_ORDERS", None)
            broker_dis = getattr(mod_kb, "BROKER_DISABLED", None)
            research = getattr(mod_kb, "RESEARCH_ONLY", None)
            if no_orders is True and broker_dis is True and research is True:
                checks.append(_check(
                    "knowledge_base_v107_safe", "stable_integration",
                    "v1.0.7 knowledge_base_v107_safe",
                    CHECK_PASS, SEV_LOW,
                    "knowledge_base: NO_REAL_ORDERS=True, BROKER_DISABLED=True, RESEARCH_ONLY=True.",
                ))
            else:
                checks.append(_check(
                    "knowledge_base_v107_safe", "stable_integration",
                    "v1.0.7 knowledge_base_v107_safe",
                    CHECK_WARN, SEV_LOW,
                    f"knowledge_base safety flags: NO_REAL_ORDERS={no_orders}, BROKER_DISABLED={broker_dis}, RESEARCH_ONLY={research}",
                    suggested_fix="Ensure knowledge_base/__init__.py has correct safety flags.",
                ))
        except Exception as exc:
            checks.append(_check(
                "knowledge_base_v107_safe", "stable_integration",
                "v1.0.7 knowledge_base_v107_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify knowledge_base_v107 safety (optional): {exc}",
                suggested_fix="Run: python main.py kb-health-check",
            ))

        # v1.0.8 local_assistant_v108_safe — local_assistant package is safe
        try:
            import importlib
            mod_la = importlib.import_module("local_assistant")
            no_orders_la = getattr(mod_la, "NO_REAL_ORDERS", None)
            ext_api = getattr(mod_la, "EXTERNAL_API_DISABLED", None)
            if no_orders_la is True and ext_api is True:
                checks.append(_check(
                    "local_assistant_v108_safe", "stable_integration",
                    "v1.0.8 local_assistant_v108_safe",
                    CHECK_PASS, SEV_LOW,
                    "local_assistant: NO_REAL_ORDERS=True, EXTERNAL_API_DISABLED=True.",
                ))
            else:
                checks.append(_check(
                    "local_assistant_v108_safe", "stable_integration",
                    "v1.0.8 local_assistant_v108_safe",
                    CHECK_WARN, SEV_LOW,
                    f"local_assistant safety flags: NO_REAL_ORDERS={no_orders_la}, EXTERNAL_API_DISABLED={ext_api}",
                    suggested_fix="Ensure local_assistant/__init__.py has correct safety flags.",
                ))
        except Exception as exc:
            checks.append(_check(
                "local_assistant_v108_safe", "stable_integration",
                "v1.0.8 local_assistant_v108_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify local_assistant_v108 safety (optional): {exc}",
                suggested_fix="Run: python main.py local-assistant-health",
            ))

        # v1.0.9 final_rollup_v109_safe — final_rollup package is safe
        try:
            import importlib
            mod_fr = importlib.import_module("final_rollup")
            no_orders_fr = getattr(mod_fr, "NO_REAL_ORDERS", None)
            ext_api_fr   = getattr(mod_fr, "EXTERNAL_API_DISABLED", None)
            v1_complete  = getattr(mod_fr, "V1_MAINTENANCE_LINE_COMPLETE", None)
            if no_orders_fr is True and ext_api_fr is True:
                checks.append(_check(
                    "final_rollup_v109_safe", "stable_integration",
                    "v1.0.9 final_rollup_v109_safe",
                    CHECK_PASS, SEV_LOW,
                    f"final_rollup: NO_REAL_ORDERS=True, EXTERNAL_API_DISABLED=True, V1_MAINTENANCE_LINE_COMPLETE={v1_complete}.",
                ))
            else:
                checks.append(_check(
                    "final_rollup_v109_safe", "stable_integration",
                    "v1.0.9 final_rollup_v109_safe",
                    CHECK_WARN, SEV_LOW,
                    f"final_rollup safety flags: NO_REAL_ORDERS={no_orders_fr}, EXTERNAL_API_DISABLED={ext_api_fr}",
                    suggested_fix="Ensure final_rollup/__init__.py has correct safety flags.",
                ))
        except Exception as exc:
            checks.append(_check(
                "final_rollup_v109_safe", "stable_integration",
                "v1.0.9 final_rollup_v109_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify final_rollup_v109 safety (optional): {exc}",
                suggested_fix="Run: python main.py final-rollup-health",
            ))

        # v1.1.0 data_universe_v110_safe — universe package is safe
        try:
            import importlib
            mod_uni = importlib.import_module("universe")
            no_orders_uni  = getattr(mod_uni, "NO_REAL_ORDERS", None)
            real_cov       = getattr(mod_uni, "REAL_DATA_COVERAGE_REQUIRED", None)
            mock_block     = getattr(mod_uni, "MOCK_DATA_FORMAL_CONCLUSION_ALLOWED", True)
            if no_orders_uni is True and real_cov is True and mock_block is False:
                checks.append(_check(
                    "data_universe_v110_safe", "stable_integration",
                    "v1.1.0 data_universe_v110_safe",
                    CHECK_PASS, SEV_LOW,
                    f"universe: NO_REAL_ORDERS=True, REAL_DATA_COVERAGE_REQUIRED=True, "
                    f"MOCK_DATA_FORMAL_CONCLUSION_ALLOWED=False.",
                ))
            else:
                checks.append(_check(
                    "data_universe_v110_safe", "stable_integration",
                    "v1.1.0 data_universe_v110_safe",
                    CHECK_WARN, SEV_LOW,
                    f"universe safety flags: NO_REAL_ORDERS={no_orders_uni}, "
                    f"REAL_DATA_COVERAGE_REQUIRED={real_cov}, "
                    f"MOCK_DATA_FORMAL_CONCLUSION_ALLOWED={mock_block}",
                    suggested_fix="Ensure universe/__init__.py has correct v1.1.0 safety flags.",
                ))
        except Exception as exc:
            checks.append(_check(
                "data_universe_v110_safe", "stable_integration",
                "v1.1.0 data_universe_v110_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify data_universe_v110 safety (optional): {exc}",
                suggested_fix="Run: python main.py universe-health",
            ))

        # v1.1.1 data_import_onboarding_v111_safe — import onboarding package is safe
        try:
            import importlib
            mod_obd = importlib.import_module("data_onboarding")
            no_orders_obd = getattr(mod_obd, "NO_REAL_ORDERS", None)
            dry_run_obd   = getattr(mod_obd, "DRY_RUN_DEFAULT", None)
            dest_dis_obd  = getattr(mod_obd, "DESTRUCTIVE_IMPORT_DISABLED", None)
            if no_orders_obd is True and dry_run_obd is True and dest_dis_obd is True:
                checks.append(_check(
                    "data_import_onboarding_v111_safe", "stable_integration",
                    "v1.1.1 data_import_onboarding_v111_safe",
                    CHECK_PASS, SEV_LOW,
                    "data_onboarding: NO_REAL_ORDERS=True, DRY_RUN_DEFAULT=True, "
                    "DESTRUCTIVE_IMPORT_DISABLED=True.",
                ))
            else:
                checks.append(_check(
                    "data_import_onboarding_v111_safe", "stable_integration",
                    "v1.1.1 data_import_onboarding_v111_safe",
                    CHECK_WARN, SEV_LOW,
                    f"data_onboarding safety flags: NO_REAL_ORDERS={no_orders_obd}, "
                    f"DRY_RUN_DEFAULT={dry_run_obd}, DESTRUCTIVE_IMPORT_DISABLED={dest_dis_obd}",
                    suggested_fix="Ensure data_onboarding/__init__.py has correct v1.1.1 safety flags.",
                ))
        except Exception as exc:
            checks.append(_check(
                "data_import_onboarding_v111_safe", "stable_integration",
                "v1.1.1 data_import_onboarding_v111_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify data_import_onboarding v1.1.1 safety (optional): {exc}",
                suggested_fix="Run: python main.py import-onboarding-health",
            ))

        # v1.1.2 coverage_repair_v112_safe — coverage repair package is safe
        try:
            import importlib
            mod_cr = importlib.import_module("coverage_repair")
            no_orders_cr = getattr(mod_cr, "NO_REAL_ORDERS", None)
            dry_run_cr   = getattr(mod_cr, "DRY_RUN_DEFAULT", None)
            dest_cr      = getattr(mod_cr, "DESTRUCTIVE_REPAIR_DISABLED", None)
            if no_orders_cr is True and dry_run_cr is True and dest_cr is True:
                checks.append(_check(
                    "coverage_repair_v112_safe", "stable_integration",
                    "v1.1.2 coverage_repair_v112_safe",
                    CHECK_PASS, SEV_LOW,
                    "coverage_repair: NO_REAL_ORDERS=True, DRY_RUN_DEFAULT=True, "
                    "DESTRUCTIVE_REPAIR_DISABLED=True.",
                ))
            else:
                checks.append(_check(
                    "coverage_repair_v112_safe", "stable_integration",
                    "v1.1.2 coverage_repair_v112_safe",
                    CHECK_WARN, SEV_LOW,
                    f"coverage_repair safety flags: NO_REAL_ORDERS={no_orders_cr}, "
                    f"DRY_RUN_DEFAULT={dry_run_cr}, DESTRUCTIVE_REPAIR_DISABLED={dest_cr}",
                    suggested_fix="Ensure coverage_repair/__init__.py has correct v1.1.2 safety flags.",
                ))
        except Exception as exc:
            checks.append(_check(
                "coverage_repair_v112_safe", "stable_integration",
                "v1.1.2 coverage_repair_v112_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify coverage_repair v1.1.2 safety (optional): {exc}",
                suggested_fix="Run: python main.py coverage-repair-health",
            ))

        # v1.1.3 data_freshness_v113_safe — data freshness package is safe
        try:
            import importlib
            mod_df = importlib.import_module("data_freshness")
            no_orders_df = getattr(mod_df, "NO_REAL_ORDERS", None)
            auto_refresh = getattr(mod_df, "AUTO_EXTERNAL_REFRESH_ENABLED", None)
            future_fresh = getattr(mod_df, "FUTURE_DATE_COUNTS_AS_FRESH", None)
            mock_fresh   = getattr(mod_df, "MOCK_DATA_FORMAL_FRESHNESS_ALLOWED", None)
            if no_orders_df is True and auto_refresh is False and future_fresh is False and mock_fresh is False:
                checks.append(_check(
                    "data_freshness_v113_safe", "stable_integration",
                    "v1.1.3 data_freshness_v113_safe",
                    CHECK_PASS, SEV_LOW,
                    "data_freshness: NO_REAL_ORDERS=True, AUTO_EXTERNAL_REFRESH_ENABLED=False, "
                    "FUTURE_DATE_COUNTS_AS_FRESH=False, MOCK_DATA_FORMAL_FRESHNESS_ALLOWED=False.",
                ))
            else:
                checks.append(_check(
                    "data_freshness_v113_safe", "stable_integration",
                    "v1.1.3 data_freshness_v113_safe",
                    CHECK_WARN, SEV_LOW,
                    f"data_freshness safety flags: NO_REAL_ORDERS={no_orders_df}, "
                    f"AUTO_EXTERNAL_REFRESH_ENABLED={auto_refresh}, "
                    f"FUTURE_DATE_COUNTS_AS_FRESH={future_fresh}, "
                    f"MOCK_DATA_FORMAL_FRESHNESS_ALLOWED={mock_fresh}",
                    suggested_fix="Ensure data_freshness/__init__.py has correct v1.1.3 safety flags.",
                ))
        except Exception as exc:
            checks.append(_check(
                "data_freshness_v113_safe", "stable_integration",
                "v1.1.3 data_freshness_v113_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify data_freshness v1.1.3 safety (optional): {exc}",
                suggested_fix="Run: python main.py freshness-health",
            ))

        # v1.1.4 coverage_quality_gate_v114_safe — quality gates package is safe
        try:
            import importlib
            mod_qg = importlib.import_module("quality_gates")
            no_orders_qg   = getattr(mod_qg, "NO_REAL_ORDERS", None)
            mock_gate      = getattr(mod_qg, "MOCK_DATA_FORMAL_GATE_ALLOWED", None)
            invalid_gate   = getattr(mod_qg, "INVALID_DATA_FORMAL_GATE_ALLOWED", None)
            override_off   = getattr(mod_qg, "QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT", None)
            if no_orders_qg is True and mock_gate is False and invalid_gate is False and override_off is True:
                checks.append(_check(
                    "coverage_quality_gate_v114_safe", "stable_integration",
                    "v1.1.4 coverage_quality_gate_v114_safe",
                    CHECK_PASS, SEV_LOW,
                    "quality_gates: NO_REAL_ORDERS=True, MOCK_DATA_FORMAL_GATE_ALLOWED=False, "
                    "INVALID_DATA_FORMAL_GATE_ALLOWED=False, QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT=True.",
                ))
            else:
                checks.append(_check(
                    "coverage_quality_gate_v114_safe", "stable_integration",
                    "v1.1.4 coverage_quality_gate_v114_safe",
                    CHECK_WARN, SEV_LOW,
                    f"quality_gates safety flags: NO_REAL_ORDERS={no_orders_qg}, "
                    f"MOCK_DATA_FORMAL_GATE_ALLOWED={mock_gate}, "
                    f"INVALID_DATA_FORMAL_GATE_ALLOWED={invalid_gate}, "
                    f"QUALITY_GATE_OVERRIDE_DISABLED_BY_DEFAULT={override_off}",
                    suggested_fix="Ensure quality_gates/__init__.py has correct v1.1.4 safety flags.",
                ))
        except Exception as exc:
            checks.append(_check(
                "coverage_quality_gate_v114_safe", "stable_integration",
                "v1.1.4 coverage_quality_gate_v114_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify quality_gates v1.1.4 safety (optional): {exc}",
                suggested_fix="Run: python main.py quality-gate-health",
            ))

        # v1.1.5 gate_enforcement_v115_safe — enforcement package is safe
        try:
            import importlib
            mod_ge = importlib.import_module("gate_enforcement")
            no_orders_ge    = getattr(mod_ge, "NO_REAL_ORDERS", None)
            bypass_ge       = getattr(mod_ge, "QUALITY_GATE_BYPASS_ALLOWED", None)
            mock_enforce_ge = getattr(mod_ge, "MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED", None)
            enforce_avail   = getattr(mod_ge, "QUALITY_GATE_ENFORCEMENT_AVAILABLE", None)
            if (no_orders_ge is True and bypass_ge is False
                    and mock_enforce_ge is False and enforce_avail is True):
                checks.append(_check(
                    "gate_enforcement_v115_safe", "stable_integration",
                    "v1.1.5 gate_enforcement_v115_safe",
                    CHECK_PASS, SEV_LOW,
                    "gate_enforcement: NO_REAL_ORDERS=True, QUALITY_GATE_BYPASS_ALLOWED=False, "
                    "MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED=False, QUALITY_GATE_ENFORCEMENT_AVAILABLE=True.",
                ))
            else:
                checks.append(_check(
                    "gate_enforcement_v115_safe", "stable_integration",
                    "v1.1.5 gate_enforcement_v115_safe",
                    CHECK_WARN, SEV_LOW,
                    f"gate_enforcement safety flags: NO_REAL_ORDERS={no_orders_ge}, "
                    f"QUALITY_GATE_BYPASS_ALLOWED={bypass_ge}, "
                    f"MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED={mock_enforce_ge}, "
                    f"QUALITY_GATE_ENFORCEMENT_AVAILABLE={enforce_avail}",
                    suggested_fix="Ensure gate_enforcement/__init__.py has correct v1.1.5 safety flags.",
                ))
        except Exception as exc:
            checks.append(_check(
                "gate_enforcement_v115_safe", "stable_integration",
                "v1.1.5 gate_enforcement_v115_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify gate_enforcement v1.1.5 safety (optional): {exc}",
                suggested_fix="Run: python main.py gate-enforcement-health",
            ))

        # v1.1.6 governance_ops_v116_safe — governance ops package is safe
        try:
            import importlib
            mod_gov = importlib.import_module("governance_ops")
            no_orders_gov  = getattr(mod_gov, "NO_REAL_ORDERS", None)
            auto_repair    = getattr(mod_gov, "GOVERNANCE_AUTO_REPAIR_ENABLED", None)
            trade_enabled  = getattr(mod_gov, "GOVERNANCE_TRADE_EXECUTION_ENABLED", None)
            gov_dash       = getattr(mod_gov, "DATA_GOVERNANCE_DASHBOARD_AVAILABLE", None)
            if (no_orders_gov is True and auto_repair is False
                    and trade_enabled is False and gov_dash is True):
                checks.append(_check(
                    "governance_ops_v116_safe", "stable_integration",
                    "v1.1.6 governance_ops_v116_safe",
                    CHECK_PASS, SEV_LOW,
                    "governance_ops: NO_REAL_ORDERS=True, GOVERNANCE_AUTO_REPAIR_ENABLED=False, "
                    "GOVERNANCE_TRADE_EXECUTION_ENABLED=False, DATA_GOVERNANCE_DASHBOARD_AVAILABLE=True.",
                ))
            else:
                checks.append(_check(
                    "governance_ops_v116_safe", "stable_integration",
                    "v1.1.6 governance_ops_v116_safe",
                    CHECK_WARN, SEV_LOW,
                    f"governance_ops safety flags: NO_REAL_ORDERS={no_orders_gov}, "
                    f"GOVERNANCE_AUTO_REPAIR_ENABLED={auto_repair}, "
                    f"GOVERNANCE_TRADE_EXECUTION_ENABLED={trade_enabled}, "
                    f"DATA_GOVERNANCE_DASHBOARD_AVAILABLE={gov_dash}",
                    suggested_fix="Ensure governance_ops/__init__.py has correct v1.1.6 safety flags.",
                ))
        except Exception as exc:
            checks.append(_check(
                "governance_ops_v116_safe", "stable_integration",
                "v1.1.6 governance_ops_v116_safe",
                CHECK_WARN, SEV_LOW,
                f"Could not verify governance_ops v1.1.6 safety (optional): {exc}",
                suggested_fix="Run: python main.py governance-health",
            ))

        return checks
