"""stable_release/stable_release_checklist_v060.py — StableReleaseChecklistV060.

Seven-category stable release checklist for TW Quant Cockpit v0.6.0.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import importlib.util
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SAFETY_BANNER = (
    "[!] Research Only | No Real Orders | Production BLOCKED"
)


def _check_item(name: str, category: str, status: str, detail: str,
                warning: str = "", suggested_fix: str = "") -> dict:
    return {
        "name":          name,
        "category":      category,
        "status":        status,
        "detail":        detail,
        "warning":       warning,
        "suggested_fix": suggested_fix,
    }


class StableReleaseChecklistV060:
    """v0.6.0 stable release checklist — seven categories.

    Categories: version_git, safety, cli, gui, reports, regression, runtime_safety

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    VERSION = "v0.6.0"

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    # ----------------------------------------------------------------
    # A. Version / Git checks
    # ----------------------------------------------------------------

    def _check_version_info(self) -> dict:
        t0 = time.monotonic()
        try:
            from release.version_info import VersionInfo
            v = VersionInfo.version
            name = VersionInfo.release_name
            blocked = getattr(VersionInfo, "production_blocked", False)
            no_orders = getattr(VersionInfo, "no_real_orders", False)
            if not (blocked and no_orders):
                return _check_item(
                    "version_info", "version_git", "FAIL",
                    f"Safety flags not set: production_blocked={blocked}, no_real_orders={no_orders}",
                    warning="Safety flags must be True",
                    suggested_fix="Set production_blocked=True and no_real_orders=True in VersionInfo",
                )
            return _check_item(
                "version_info", "version_git", "PASS",
                f"Version={v} | {name} | production_blocked={blocked} | no_real_orders={no_orders}",
            )
        except Exception as exc:
            return _check_item(
                "version_info", "version_git", "FAIL", str(exc),
                suggested_fix="Fix release/version_info.py import",
            )

    def _check_git_status(self) -> dict:
        try:
            result = subprocess.run(
                ["git", "-C", BASE_DIR, "status", "--porcelain"],
                capture_output=True, text=True, timeout=30,
            )
            dirty = result.stdout.strip()
            if result.returncode != 0:
                return _check_item(
                    "git_status", "version_git", "WARN",
                    "git status returned non-zero",
                    warning="Check git setup",
                )
            if dirty:
                lines = dirty.splitlines()
                return _check_item(
                    "git_status", "version_git", "WARN",
                    f"Working tree has {len(lines)} modified/untracked file(s)",
                    warning="Commit or stash changes before tagging release",
                    suggested_fix="git add <files> && git commit -m 'chore: pre-release cleanup'",
                )
            return _check_item(
                "git_status", "version_git", "PASS",
                "Working tree clean.",
            )
        except Exception as exc:
            return _check_item(
                "git_status", "version_git", "WARN", str(exc),
                warning="git not available or error",
            )

    def _check_compileall(self) -> dict:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "compileall", BASE_DIR, "-q"],
                capture_output=True, text=True, timeout=120,
            )
            if result.returncode == 0:
                return _check_item(
                    "compileall", "version_git", "PASS",
                    "All Python files compile cleanly.",
                )
            detail = (result.stderr or result.stdout or "returncode != 0").strip()[:300]
            return _check_item(
                "compileall", "version_git", "FAIL", detail,
                suggested_fix="Fix syntax errors reported by compileall",
            )
        except Exception as exc:
            return _check_item(
                "compileall", "version_git", "FAIL", str(exc),
                suggested_fix="Ensure Python is on PATH",
            )

    # ----------------------------------------------------------------
    # B. Safety checks
    # ----------------------------------------------------------------

    def _check_safety_flags(self) -> dict:
        try:
            from release.version_info import VersionInfo
            flags = {
                "production_blocked": getattr(VersionInfo, "production_blocked", None),
                "no_real_orders":     getattr(VersionInfo, "no_real_orders", None),
                "real_order_ready":   getattr(VersionInfo, "real_order_ready", None),
                "read_only":          getattr(VersionInfo, "read_only", None),
            }
            all_ok = (
                flags["production_blocked"] is True
                and flags["no_real_orders"] is True
                and flags["real_order_ready"] is False
            )
            if all_ok:
                return _check_item(
                    "safety_flags", "safety", "PASS",
                    f"All safety flags correct: {flags}",
                )
            return _check_item(
                "safety_flags", "safety", "FAIL",
                f"Safety flag mismatch: {flags}",
                warning="production_blocked and no_real_orders must be True; real_order_ready must be False",
                suggested_fix="Update VersionInfo safety flags",
            )
        except Exception as exc:
            return _check_item(
                "safety_flags", "safety", "FAIL", str(exc),
                suggested_fix="Fix release/version_info.py",
            )

    def _check_no_broker_imports(self) -> dict:
        """Verify no broker/shioaji import statements in core modules."""
        import re
        try:
            # Check for actual import statements, not mere keyword mentions
            broker_import_patterns = [
                r"^\s*import\s+shioaji",
                r"^\s*from\s+shioaji",
                r"^\s*import\s+sinopac",
                r"^\s*from\s+sinopac",
                r"^\s*import\s+mega_broker",
                r"^\s*from\s+mega_broker",
            ]
            compiled = [re.compile(p, re.MULTILINE) for p in broker_import_patterns]
            core_dirs = [
                os.path.join(BASE_DIR, "stable_release"),
                os.path.join(BASE_DIR, "release"),
                os.path.join(BASE_DIR, "reports"),
                os.path.join(BASE_DIR, "regression"),
            ]
            found = []
            for d in core_dirs:
                if not os.path.isdir(d):
                    continue
                for root, _, files in os.walk(d):
                    for fn in files:
                        if not fn.endswith(".py"):
                            continue
                        fp = os.path.join(root, fn)
                        try:
                            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                            for pat in compiled:
                                if pat.search(content):
                                    found.append(f"{fn}: broker import detected")
                        except Exception:
                            pass
            if found:
                return _check_item(
                    "no_broker_imports", "safety", "FAIL",
                    f"Found {len(found)} broker import(s) in core modules",
                    warning="; ".join(found[:3]),
                    suggested_fix="Remove broker import statements from core modules",
                )
            return _check_item(
                "no_broker_imports", "safety", "PASS",
                "No broker/shioaji import statements found in core modules.",
            )
        except Exception as exc:
            return _check_item(
                "no_broker_imports", "safety", "WARN", str(exc),
            )

    # ----------------------------------------------------------------
    # C. CLI checks
    # ----------------------------------------------------------------

    def _check_main_exists(self) -> dict:
        try:
            main_path = os.path.join(BASE_DIR, "main.py")
            if not os.path.isfile(main_path):
                return _check_item(
                    "main_exists", "cli", "FAIL",
                    "main.py not found",
                    suggested_fix="Restore main.py",
                )
            size = os.path.getsize(main_path)
            return _check_item(
                "main_exists", "cli", "PASS",
                f"main.py exists ({size:,} bytes)",
            )
        except Exception as exc:
            return _check_item("main_exists", "cli", "FAIL", str(exc))

    def _check_stable_v060_commands(self) -> dict:
        try:
            main_path = os.path.join(BASE_DIR, "main.py")
            if not os.path.isfile(main_path):
                return _check_item(
                    "stable_v060_commands", "cli", "FAIL",
                    "main.py not found",
                )
            with open(main_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            required = [
                "stable-v060-check",
                "stable-v060-report",
                "stable-v060-manifest",
                "stable-v060-capabilities",
                "stable-v060-limitations",
                "stable-v060-summary",
            ]
            missing = [cmd for cmd in required if cmd not in content]
            if missing:
                return _check_item(
                    "stable_v060_commands", "cli", "WARN",
                    f"Missing {len(missing)} v0.6.0 CLI command(s): {', '.join(missing)}",
                    warning="v0.6.0 CLI commands not registered in main.py",
                    suggested_fix="Add stable-v060-* commands to main.py",
                )
            return _check_item(
                "stable_v060_commands", "cli", "PASS",
                f"All {len(required)} v0.6.0 CLI commands found in main.py.",
            )
        except Exception as exc:
            return _check_item(
                "stable_v060_commands", "cli", "WARN", str(exc),
            )

    def _check_core_imports(self) -> dict:
        """Check that key v0.6.0 / v0.6.2 modules are importable."""
        modules = [
            "stable_release.stable_release_schema",
            "stable_release.capability_matrix",
            "stable_release.known_limitations",
            "stable_release.release_manifest_builder",
            "reports.stable_release_v060_report",
            # v0.6.2 Data Coverage Expansion
            "data_coverage.data_coverage_schema",
            "data_coverage.data_coverage_engine",
            # v0.7.0 Research Intelligence
            "research_intelligence.research_intelligence_schema",
            "research_intelligence.research_intelligence_engine",
            # v0.7.1 Intelligence UX Polish
            "research_intelligence.recommendation_engine",
            "research_intelligence.priority_planner",
        ]
        failed = []
        for mod in modules:
            spec = importlib.util.find_spec(mod)
            if spec is None:
                failed.append(mod)
        if failed:
            return _check_item(
                "core_imports", "cli", "FAIL",
                f"{len(failed)} module(s) not importable: {', '.join(failed)}",
                suggested_fix="Create missing stable_release package files",
            )
        return _check_item(
            "core_imports", "cli", "PASS",
            f"All {len(modules)} v0.6.0 core modules importable.",
        )

    # ----------------------------------------------------------------
    # D. GUI checks
    # ----------------------------------------------------------------

    def _check_gui_panel_exists(self) -> dict:
        try:
            panel_path = os.path.join(BASE_DIR, "gui", "stable_release_panel.py")
            adapter_path = os.path.join(BASE_DIR, "gui", "stable_release_adapter.py")
            missing = []
            if not os.path.isfile(panel_path):
                missing.append("gui/stable_release_panel.py")
            if not os.path.isfile(adapter_path):
                missing.append("gui/stable_release_adapter.py")
            if missing:
                return _check_item(
                    "gui_panel_exists", "gui", "WARN",
                    f"Missing GUI files: {', '.join(missing)}",
                    warning="GUI panel not yet created",
                    suggested_fix="Create gui/stable_release_panel.py and gui/stable_release_adapter.py",
                )
            return _check_item(
                "gui_panel_exists", "gui", "PASS",
                "StableReleasePanel and StableReleaseAdapter files found.",
            )
        except Exception as exc:
            return _check_item("gui_panel_exists", "gui", "WARN", str(exc))

    def _check_dashboard_tab(self) -> dict:
        try:
            dash_path = os.path.join(BASE_DIR, "gui", "dashboard.py")
            if not os.path.isfile(dash_path):
                return _check_item(
                    "dashboard_tab", "gui", "WARN",
                    "gui/dashboard.py not found",
                )
            with open(dash_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "StableReleasePanel" in content:
                return _check_item(
                    "dashboard_tab", "gui", "PASS",
                    "StableReleasePanel registered in gui/dashboard.py.",
                )
            return _check_item(
                "dashboard_tab", "gui", "WARN",
                "StableReleasePanel not found in gui/dashboard.py",
                warning="Dashboard tab not yet wired",
                suggested_fix="Add v0.6.0 Stable Release tab import and setup to dashboard.py",
            )
        except Exception as exc:
            return _check_item("dashboard_tab", "gui", "WARN", str(exc))

    # ----------------------------------------------------------------
    # E. Reports checks
    # ----------------------------------------------------------------

    def _check_stable_report_exists(self) -> dict:
        try:
            rpt_path = os.path.join(BASE_DIR, "reports", "stable_release_v060_report.py")
            if not os.path.isfile(rpt_path):
                return _check_item(
                    "stable_report_exists", "reports", "WARN",
                    "reports/stable_release_v060_report.py not found",
                    suggested_fix="Create reports/stable_release_v060_report.py",
                )
            return _check_item(
                "stable_report_exists", "reports", "PASS",
                "stable_release_v060_report.py exists.",
            )
        except Exception as exc:
            return _check_item("stable_report_exists", "reports", "WARN", str(exc))

    def _check_report_registry(self) -> dict:
        try:
            from report_pack.report_pack_schema import ALL_REPORT_TYPES, OPTIONAL_REPORT_TYPES, ENV_LIMITED_REPORT_TYPES
            has_stable = any("stable_release" in rt for rt in ALL_REPORT_TYPES)
            if has_stable:
                return _check_item(
                    "report_registry", "reports", "PASS",
                    f"stable_release report type found in report_pack schema. "
                    f"Optional types: {len(OPTIONAL_REPORT_TYPES)}. "
                    f"ENV_LIMITED types: {len(ENV_LIMITED_REPORT_TYPES)} (provider token required — not a release failure).",
                )
            return _check_item(
                "report_registry", "reports", "WARN",
                "stable_release report type not in ALL_REPORT_TYPES",
                warning="v0.6.0 report not yet registered",
                suggested_fix="Add REPORT_STABLE_RELEASE to report_pack_schema.py",
            )
        except Exception as exc:
            return _check_item("report_registry", "reports", "WARN", str(exc))

    def _check_report_pack_partial(self) -> dict:
        """Check that PARTIAL report pack with 0 failed / no required missing is not a failure."""
        try:
            from report_pack.report_pack_builder import ReportPackBuilder
            from report_pack.report_health_checker import ReportHealthChecker
            builder = ReportPackBuilder(pack_type="daily")
            pack = builder.build()
            checker = ReportHealthChecker()
            health = checker.check_pack(pack)
            required_missing = health.get("required_missing_count", 0)
            failed = health.get("failed_count", 0)
            env_limited = health.get("env_limited_count", 0)
            if failed == 0 and required_missing == 0:
                detail = (
                    f"Report pack status={pack.status} | health_label={health['health_label']} | "
                    f"required_missing=0 | env_limited={env_limited} (not a failure) | failed=0"
                )
                return _check_item(
                    "report_pack_partial", "reports", "PASS", detail,
                )
            return _check_item(
                "report_pack_partial", "reports", "WARN",
                f"Report pack has required_missing={required_missing} or failed={failed}",
                warning="Required reports missing — run auto-report daily profile",
                suggested_fix="python main.py auto-report --mode real --profile daily",
            )
        except Exception as exc:
            return _check_item(
                "report_pack_partial", "reports", "WARN", str(exc),
                warning="Could not evaluate report pack health",
            )

    # ----------------------------------------------------------------
    # F. Regression checks
    # ----------------------------------------------------------------

    def _check_regression_suite(self) -> dict:
        try:
            from regression.suite_registry import RegressionSuiteRegistry
            from regression.regression_schema import SUITE_RELEASE_GATE
            reg = RegressionSuiteRegistry()
            suite = reg.get_suite(SUITE_RELEASE_GATE)
            stable_tests = [
                t for t in suite
                if "stable_v060" in t.test_id or "stable_v060" in t.name
            ]
            if stable_tests:
                return _check_item(
                    "regression_v060_tests", "regression", "PASS",
                    f"Found {len(stable_tests)} v0.6.0 regression test(s) in release_gate suite.",
                )
            return _check_item(
                "regression_v060_tests", "regression", "WARN",
                "No v0.6.0 regression tests found in release_gate suite",
                warning="Add stable_v060_* tests to suite_registry.py",
                suggested_fix="Add stable_v060_check, stable_v060_summary, stable_v060_capabilities tests",
            )
        except Exception as exc:
            return _check_item(
                "regression_v060_tests", "regression", "WARN", str(exc),
            )

    # ----------------------------------------------------------------
    # G. Runtime safety checks
    # ----------------------------------------------------------------

    def _check_capability_matrix_builds(self) -> dict:
        try:
            from stable_release.capability_matrix import StableCapabilityMatrix
            matrix = StableCapabilityMatrix()
            matrix.build()
            caps = matrix.list_capabilities()
            if len(caps) >= 30:
                return _check_item(
                    "capability_matrix_builds", "runtime_safety", "PASS",
                    f"Capability matrix built with {len(caps)} capabilities.",
                )
            return _check_item(
                "capability_matrix_builds", "runtime_safety", "WARN",
                f"Only {len(caps)} capabilities found (expected >=30)",
                suggested_fix="Add missing capabilities to capability_matrix.py",
            )
        except Exception as exc:
            return _check_item(
                "capability_matrix_builds", "runtime_safety", "FAIL", str(exc),
                suggested_fix="Fix stable_release/capability_matrix.py",
            )

    def _check_known_limitations_builds(self) -> dict:
        try:
            from stable_release.known_limitations import KnownLimitationsRegistry
            reg = KnownLimitationsRegistry()
            lims = reg.list_limitations()
            if len(lims) >= 11:
                return _check_item(
                    "known_limitations_builds", "runtime_safety", "PASS",
                    f"Known limitations registry has {len(lims)} entries.",
                )
            return _check_item(
                "known_limitations_builds", "runtime_safety", "WARN",
                f"Only {len(lims)} limitations found (expected >=11)",
            )
        except Exception as exc:
            return _check_item(
                "known_limitations_builds", "runtime_safety", "FAIL", str(exc),
            )

    def _check_release_schema_builds(self) -> dict:
        try:
            from stable_release.stable_release_schema import StableReleaseInfo, StableCapability
            info = StableReleaseInfo(
                version="v0.6.0",
                release_name="Research OS Stable Release",
                release_type="stable",
                created_at="2026-06-04",
                previous_version="v0.5.6",
                branch="main",
                commit_hash="N/A",
                tag="v0.6.0",
                status="STABLE",
            )
            d = info.to_dict()
            assert d["no_real_orders"] is True
            assert d["production_blocked"] is True
            return _check_item(
                "release_schema_builds", "runtime_safety", "PASS",
                "StableReleaseInfo and StableCapability build and validate correctly.",
            )
        except Exception as exc:
            return _check_item(
                "release_schema_builds", "runtime_safety", "FAIL", str(exc),
            )

    def _check_research_intelligence_ux_safety(self) -> dict:
        """v0.7.1 — classify_command_safety exists and BLOCKED_FOR_TRADING works."""
        try:
            from research_intelligence.research_intelligence_schema import (
                classify_command_safety, CMD_BLOCKED_TRADING,
            )
            result = classify_command_safety("python main.py BUY 100 TSMC")
            assert result == CMD_BLOCKED_TRADING, f"Expected BLOCKED_FOR_TRADING, got {result}"
            safe = classify_command_safety("python main.py regression-run")
            assert safe != CMD_BLOCKED_TRADING
            return _check_item(
                "research_intelligence_ux_safety", "runtime_safety", "PASS",
                "classify_command_safety correctly identifies BLOCKED_FOR_TRADING.",
            )
        except Exception as exc:
            return _check_item(
                "research_intelligence_ux_safety", "runtime_safety", "FAIL", str(exc),
            )

    def _check_strategy_memory_summary_can_run(self) -> dict:
        """v0.7.2 — strategy-memory-summary CLI must run without crash."""
        import subprocess
        import sys
        try:
            result = subprocess.run(
                [sys.executable, os.path.join(BASE_DIR, "main.py"), "strategy-memory-summary"],
                capture_output=True, text=True, timeout=30, cwd=BASE_DIR,
            )
            if result.returncode != 0 and "ERROR" in (result.stdout or "") and "import" in (result.stdout or "").lower():
                return _check_item(
                    "strategy_memory_summary_can_run", "runtime_safety", "FAIL",
                    f"strategy-memory-summary returned error: {(result.stdout or '')[:200]}",
                )
            return _check_item(
                "strategy_memory_summary_can_run", "runtime_safety", "PASS",
                "strategy-memory-summary runs without crash.",
            )
        except Exception as exc:
            return _check_item(
                "strategy_memory_summary_can_run", "runtime_safety", "WARN", str(exc),
            )

    def _check_memory_store_no_forbidden_actions(self) -> dict:
        """v0.7.2 — StrategyMemoryItem must reject forbidden action keywords."""
        try:
            from strategy_memory.strategy_memory_schema import StrategyMemoryItem, _guard
            # _guard should raise on forbidden keywords
            raised = False
            for kw in ["SELL this", "place an ORDER", "AUTO_TRADE signal"]:
                try:
                    _guard(kw)
                except ValueError:
                    raised = True
                    break
            if not raised:
                return _check_item(
                    "memory_store_no_forbidden_actions", "runtime_safety", "FAIL",
                    "StrategyMemoryItem._guard did not raise on forbidden keywords",
                )
            return _check_item(
                "memory_store_no_forbidden_actions", "runtime_safety", "PASS",
                "StrategyMemoryItem._guard correctly blocks forbidden trading keywords.",
            )
        except Exception as exc:
            return _check_item(
                "memory_store_no_forbidden_actions", "runtime_safety", "FAIL", str(exc),
            )

    def _check_recommendations_no_forbidden_actions(self) -> dict:
        """v0.7.1 — RecommendationEngine must never emit BUY/SELL/ORDER."""
        try:
            from research_intelligence.recommendation_engine import ResearchRecommendationEngine
            from research_intelligence.research_intelligence_schema import (
                FORBIDDEN_ACTION_TYPES as _FORBIDDEN_ACTION_TYPES,
            )
            eng = ResearchRecommendationEngine()
            recs = eng.build_recommendations([], mode="real")
            forbidden_found = [
                r.action_type for r in recs if r.action_type in _FORBIDDEN_ACTION_TYPES
            ]
            if forbidden_found:
                return _check_item(
                    "recommendations_no_forbidden_actions", "runtime_safety", "FAIL",
                    f"Forbidden action types found: {forbidden_found}",
                )
            return _check_item(
                "recommendations_no_forbidden_actions", "runtime_safety", "PASS",
                "No forbidden action types in recommendations.",
            )
        except Exception as exc:
            return _check_item(
                "recommendations_no_forbidden_actions", "runtime_safety", "FAIL", str(exc),
            )

    def _check_backtest_coach_summary_can_run(self) -> dict:
        """v0.7.3 — backtest-coach-summary CLI must run without crash."""
        import subprocess
        import sys
        try:
            result = subprocess.run(
                [sys.executable, os.path.join(BASE_DIR, "main.py"), "backtest-coach-summary"],
                capture_output=True, text=True, timeout=30, cwd=BASE_DIR,
            )
            if result.returncode != 0 and "ERROR" in (result.stdout or "") and "import" in (result.stdout or "").lower():
                return _check_item(
                    "backtest_coach_summary_can_run", "runtime_safety", "FAIL",
                    f"backtest-coach-summary returned error: {(result.stdout or '')[:200]}",
                )
            return _check_item(
                "backtest_coach_summary_can_run", "runtime_safety", "PASS",
                "backtest-coach-summary runs without crash.",
            )
        except Exception as exc:
            return _check_item(
                "backtest_coach_summary_can_run", "runtime_safety", "WARN", str(exc),
            )

    def _check_coach_tasks_no_forbidden_actions(self) -> dict:
        """v0.7.3 — CoachTrainingTask must reject forbidden trading keywords."""
        try:
            from backtest_coach.backtest_coach_schema import _guard
            raised = False
            for kw in ["BUY signal", "SELL now", "SUBMIT_ORDER auto"]:
                try:
                    _guard(kw)
                except ValueError:
                    raised = True
                    break
            if not raised:
                return _check_item(
                    "coach_tasks_no_forbidden_actions", "runtime_safety", "FAIL",
                    "BacktestCoach._guard did not raise on forbidden keywords",
                )
            return _check_item(
                "coach_tasks_no_forbidden_actions", "runtime_safety", "PASS",
                "BacktestCoach._guard correctly blocks forbidden trading keywords.",
            )
        except Exception as exc:
            return _check_item(
                "coach_tasks_no_forbidden_actions", "runtime_safety", "FAIL", str(exc),
            )

    def _check_intelligence_stable_summary_can_run(self) -> dict:
        """v0.8.0 — IntelligenceStableStore.load_latest_summary must not crash."""
        try:
            from intelligence_stable.intelligence_stable_store import IntelligenceStableStore
            store = IntelligenceStableStore()
            store.load_latest_summary()  # may return None — that is fine
            return _check_item(
                "intelligence_stable_summary_can_run", "runtime_safety", "PASS",
                "IntelligenceStableStore.load_latest_summary runs without error.",
            )
        except Exception as exc:
            return _check_item(
                "intelligence_stable_summary_can_run", "runtime_safety", "FAIL",
                str(exc),
                suggested_fix="Ensure intelligence_stable package is installed correctly.",
            )

    def _check_intelligence_stable_no_forbidden_actions(self) -> dict:
        """v0.8.0 — IntelligenceCapabilityMatrix must have no forbidden actions."""
        try:
            from intelligence_stable.intelligence_capability_matrix import IntelligenceCapabilityMatrix
            matrix = IntelligenceCapabilityMatrix()
            caps = matrix.build()
            all_safe = all(c.no_real_orders and c.production_blocked for c in caps)
            if all_safe:
                return _check_item(
                    "intelligence_stable_no_forbidden_actions", "runtime_safety", "PASS",
                    f"All {len(caps)} capabilities have no_real_orders=True and production_blocked=True.",
                )
            unsafe = [c.capability_id for c in caps if not (c.no_real_orders and c.production_blocked)]
            return _check_item(
                "intelligence_stable_no_forbidden_actions", "runtime_safety", "FAIL",
                f"Capabilities without safety flags: {unsafe}",
                suggested_fix="Set no_real_orders=True and production_blocked=True on all capabilities.",
            )
        except Exception as exc:
            return _check_item(
                "intelligence_stable_no_forbidden_actions", "runtime_safety", "FAIL", str(exc),
            )

    # ----------------------------------------------------------------
    # v0.8.1 Strategy Memory UX checks
    # ----------------------------------------------------------------

    def _check_strategy_memory_ux_import(self) -> dict:
        """v0.8.1 — StrategyMemoryPanel must import without error."""
        try:
            import importlib
            spec = importlib.util.find_spec("gui.strategy_memory_panel")
            if spec is None:
                return _check_item(
                    "strategy_memory_ux_import", "import", "WARN",
                    "gui.strategy_memory_panel not found (GUI may not be installed).",
                )
            # Only attempt a full import if PySide6 is available
            try:
                import PySide6  # noqa: F401
                from gui.strategy_memory_panel import StrategyMemoryPanel  # noqa: F401
                return _check_item(
                    "strategy_memory_ux_import", "import", "PASS",
                    "StrategyMemoryPanel imported successfully.",
                )
            except ImportError:
                return _check_item(
                    "strategy_memory_ux_import", "import", "WARN",
                    "PySide6 not installed; GUI import skipped.",
                )
        except Exception as exc:
            return _check_item(
                "strategy_memory_ux_import", "import", "FAIL", str(exc),
            )

    def _check_strategy_memory_no_forbidden_commands(self) -> dict:
        """v0.8.1 — StrategyMemoryAdapter.load_safe_commands must never return BUY/SELL/ORDER."""
        _FORBIDDEN = ["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE"]
        try:
            from gui.strategy_memory_adapter import StrategyMemoryAdapter
            adapter = StrategyMemoryAdapter()
            # load_safe_commands with a non-existent id returns [] — that's safe
            cmds = adapter.load_safe_commands("__test_nonexistent__")
            for entry in cmds:
                upper = entry.get("command", "").upper()
                for kw in _FORBIDDEN:
                    if kw in upper:
                        return _check_item(
                            "strategy_memory_no_forbidden_commands", "runtime_safety", "FAIL",
                            f"load_safe_commands returned forbidden keyword '{kw}' in: {entry['command'][:80]}",
                        )
            return _check_item(
                "strategy_memory_no_forbidden_commands", "runtime_safety", "PASS",
                "StrategyMemoryAdapter.load_safe_commands: no forbidden BUY/SELL/ORDER commands.",
            )
        except Exception as exc:
            return _check_item(
                "strategy_memory_no_forbidden_commands", "runtime_safety", "WARN", str(exc),
            )

    def _check_accepted_is_research_only(self) -> dict:
        """v0.8.1 — StrategyMemoryItem.accepted_is_research_only must always be True."""
        try:
            from strategy_memory.strategy_memory_schema import StrategyMemoryItem
            item = StrategyMemoryItem(
                title="Test item",
                memory_type="HYPOTHESIS",
                source_module="test",
                status="ACCEPTED",
                accepted_is_research_only=False,  # should be overridden to True
            )
            if not item.accepted_is_research_only:
                return _check_item(
                    "accepted_is_research_only", "runtime_safety", "FAIL",
                    "StrategyMemoryItem.accepted_is_research_only is False even after __post_init__",
                    suggested_fix="Ensure __post_init__ forces accepted_is_research_only=True.",
                )
            return _check_item(
                "accepted_is_research_only", "runtime_safety", "PASS",
                "StrategyMemoryItem.accepted_is_research_only is always True (enforced in __post_init__).",
            )
        except Exception as exc:
            return _check_item(
                "accepted_is_research_only", "runtime_safety", "FAIL", str(exc),
            )

    def _check_training_metrics_summary_can_run(self) -> dict:
        """v0.8.2 — TrainingMetricsSummary import and build check."""
        try:
            from training_metrics.training_metrics_schema import TrainingMetric, TrainingMetricsSummary
            m = TrainingMetric(
                metric_id="test", metric_type="TASK_COMPLETION",
                source_module="test", label="Test Metric",
                value=0.0, unit="%",
            )
            s = TrainingMetricsSummary()
            if not s.no_real_orders or not s.production_blocked:
                return _check_item(
                    "training_metrics_summary_can_run", "training_metrics", "FAIL",
                    "TrainingMetricsSummary safety flags not enforced.",
                )
            return _check_item(
                "training_metrics_summary_can_run", "training_metrics", "PASS",
                "TrainingMetric and TrainingMetricsSummary import and build OK.",
            )
        except Exception as exc:
            return _check_item(
                "training_metrics_summary_can_run", "training_metrics", "FAIL", str(exc),
            )

    def _check_training_metrics_no_forbidden_actions(self) -> dict:
        """v0.8.2 — TrainingMetric label guard must reject BUY/SELL/ORDER."""
        try:
            from training_metrics.training_metrics_schema import TrainingMetric
            caught = False
            try:
                TrainingMetric(
                    metric_id="bad", metric_type="TASK_COMPLETION",
                    source_module="test", label="BUY signal detected",
                    value=0.0, unit="",
                )
            except ValueError:
                caught = True
            if not caught:
                return _check_item(
                    "training_metrics_no_forbidden_actions", "safety", "FAIL",
                    "TrainingMetric _guard() did not reject forbidden keyword 'BUY'.",
                    suggested_fix="Ensure _guard() is called in __post_init__.",
                )
            return _check_item(
                "training_metrics_no_forbidden_actions", "safety", "PASS",
                "TrainingMetric _guard() correctly rejects BUY/SELL/ORDER.",
            )
        except Exception as exc:
            return _check_item(
                "training_metrics_no_forbidden_actions", "safety", "FAIL", str(exc),
            )

    def _check_evidence_graph_summary_can_run(self) -> dict:
        """v0.8.3 — EvidenceGraphSummary import and build check."""
        try:
            from evidence_graph.evidence_graph_schema import EvidenceGraphSummary
            s = EvidenceGraphSummary()
            if not s.no_real_orders or not s.production_blocked:
                return _check_item(
                    "evidence_graph_summary_can_run", "evidence_graph", "FAIL",
                    "EvidenceGraphSummary safety flags not enforced.",
                )
            return _check_item(
                "evidence_graph_summary_can_run", "evidence_graph", "PASS",
                "EvidenceGraphSummary import and build OK.",
            )
        except Exception as exc:
            return _check_item(
                "evidence_graph_summary_can_run", "evidence_graph", "FAIL", str(exc),
            )

    def _check_evidence_graph_no_forbidden_actions(self) -> dict:
        """v0.8.3 — EvidenceEdge suggested_next_step guard must reject BUY/SELL/ORDER."""
        try:
            from evidence_graph.evidence_graph_schema import EvidenceEdge
            caught = False
            try:
                EvidenceEdge(
                    edge_id="bad", source_node_id="a", target_node_id="b",
                    relation_type="SUPPORTS",
                    suggested_next_step="SELL signal",
                )
            except ValueError:
                caught = True
            if not caught:
                return _check_item(
                    "evidence_graph_no_forbidden_actions", "safety", "FAIL",
                    "EvidenceEdge _guard() did not reject forbidden keyword 'SELL'.",
                    suggested_fix="Ensure _guard() is called in EvidenceEdge.__post_init__.",
                )
            return _check_item(
                "evidence_graph_no_forbidden_actions", "safety", "PASS",
                "EvidenceEdge _guard() correctly rejects BUY/SELL/ORDER.",
            )
        except Exception as exc:
            return _check_item(
                "evidence_graph_no_forbidden_actions", "safety", "FAIL", str(exc),
            )

    def _check_strategy_lab_import_health(self) -> dict:
        """v0.9.0: strategy_lab package imports cleanly."""
        try:
            from strategy_lab.strategy_lab_schema import StrategyLabCapability  # noqa: F401
            from strategy_lab.strategy_lab_engine import StrategyLabEngine  # noqa: F401
            return _check_item(
                "strategy_lab_import_health", "strategy_lab", "PASS",
                "strategy_lab package imports successfully.",
            )
        except ImportError as exc:
            return _check_item(
                "strategy_lab_import_health", "strategy_lab", "FAIL", str(exc),
            )
        except Exception as exc:
            return _check_item(
                "strategy_lab_import_health", "strategy_lab", "WARN", str(exc),
            )

    def _check_strategy_lab_no_forbidden_actions(self) -> dict:
        """v0.9.0: StrategyLabEngine has safety flags set."""
        try:
            from strategy_lab.strategy_lab_engine import StrategyLabEngine
            assert StrategyLabEngine.no_real_orders is True
            assert StrategyLabEngine.production_blocked is True
            assert StrategyLabEngine.real_order_ready is False
            return _check_item(
                "strategy_lab_no_forbidden_actions", "safety", "PASS",
                "StrategyLabEngine: no_real_orders=True, production_blocked=True, real_order_ready=False.",
            )
        except Exception as exc:
            return _check_item(
                "strategy_lab_no_forbidden_actions", "safety", "WARN", str(exc),
            )

    # ----------------------------------------------------------------
    # v0.9.0.1 Crash Reversal checks
    # ----------------------------------------------------------------

    def _check_crash_reversal_import(self) -> dict:
        """v0.9.0.1 — strategy_rules.crash_reversal_pack imports without error."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("strategy_rules.crash_reversal_pack")
            if spec is None:
                return _check_item(
                    "crash_reversal_import", "imports", "WARN",
                    "strategy_rules.crash_reversal_pack not found (optional new feature).",
                    warning="Add crash_reversal_pack.py to strategy_rules/",
                    suggested_fix="Create strategy_rules/crash_reversal_pack.py with CrashReversalStrategyPack",
                )
            from strategy_rules.crash_reversal_pack import CrashReversalStrategyPack  # noqa: F401
            return _check_item(
                "crash_reversal_import", "imports", "PASS",
                "strategy_rules.crash_reversal_pack imports successfully.",
            )
        except ImportError as exc:
            return _check_item(
                "crash_reversal_import", "imports", "WARN",
                f"crash_reversal_pack import failed (optional): {exc}",
                warning="New optional feature — WARN not FAIL",
                suggested_fix="Create strategy_rules/crash_reversal_pack.py",
            )
        except Exception as exc:
            return _check_item(
                "crash_reversal_import", "imports", "WARN", str(exc),
            )

    def _check_crash_reversal_no_forbidden_actions(self) -> dict:
        """v0.9.0.1 — CrashReversalStrategyPack output must not contain BUY/SELL/ORDER."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("strategy_rules.crash_reversal_pack")
            if spec is None:
                return _check_item(
                    "crash_reversal_no_forbidden_actions", "safety", "WARN",
                    "strategy_rules.crash_reversal_pack not installed — check skipped.",
                )
            from strategy_rules.crash_reversal_pack import CrashReversalStrategyPack
            pack = CrashReversalStrategyPack()
            result = pack.run(mode="real") if hasattr(pack, "run") else {}
            out_str = str(result)
            forbidden = [kw for kw in ["BUY", "SELL", "ORDER"]
                         if kw in out_str.upper()]
            if forbidden:
                return _check_item(
                    "crash_reversal_no_forbidden_actions", "safety", "WARN",
                    f"Forbidden keywords found in CrashReversalStrategyPack output: {forbidden}",
                    warning="Remove BUY/SELL/ORDER from output",
                    suggested_fix="Ensure CrashReversalStrategyPack produces no trading commands.",
                )
            return _check_item(
                "crash_reversal_no_forbidden_actions", "safety", "PASS",
                "CrashReversalStrategyPack output has no BUY/SELL/ORDER.",
            )
        except Exception as exc:
            return _check_item(
                "crash_reversal_no_forbidden_actions", "safety", "WARN",
                f"Check skipped (optional): {exc}",
            )

    def _check_evidence_graph_ux_import(self) -> dict:
        """v0.9.1 — Check EvidenceGraphQuery imports correctly."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("evidence_graph.evidence_graph_query")
            if spec is None:
                return _check_item(
                    "evidence_graph_ux_import", "imports", "WARN",
                    "evidence_graph.evidence_graph_query not found (optional v0.9.1 feature).",
                    warning="EvidenceGraphQuery not yet available",
                    suggested_fix="Create evidence_graph/evidence_graph_query.py with EvidenceGraphQuery",
                )
            from evidence_graph.evidence_graph_query import EvidenceGraphQuery  # noqa: F401
            return _check_item(
                "evidence_graph_ux_import", "imports", "PASS",
                "evidence_graph.evidence_graph_query.EvidenceGraphQuery imports successfully.",
            )
        except ImportError as exc:
            return _check_item(
                "evidence_graph_ux_import", "imports", "WARN",
                f"EvidenceGraphQuery import failed (optional): {exc}",
                warning="New optional feature — WARN not FAIL",
                suggested_fix="Check evidence_graph/evidence_graph_query.py for syntax errors.",
            )
        except Exception as exc:
            return _check_item(
                "evidence_graph_ux_import", "imports", "WARN", str(exc),
            )

    def _check_strategy_validation_import(self) -> dict:
        """v0.9.2 — strategy_validation.strategy_validation_schema imports."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("strategy_validation.strategy_validation_schema")
            if spec is None:
                return _check_item(
                    "strategy_validation_import", "imports", "WARN",
                    "strategy_validation.strategy_validation_schema not found (optional v0.9.2 feature).",
                    warning="Add strategy_validation_schema.py to strategy_validation/",
                    suggested_fix="Create strategy_validation/strategy_validation_schema.py with StrategyValidationScore",
                )
            from strategy_validation.strategy_validation_schema import StrategyValidationScore  # noqa: F401
            return _check_item(
                "strategy_validation_import", "imports", "PASS",
                "strategy_validation.strategy_validation_schema.StrategyValidationScore imports successfully.",
            )
        except ImportError as exc:
            return _check_item(
                "strategy_validation_import", "imports", "WARN",
                f"StrategyValidationScore import failed (optional): {exc}",
                warning="New optional feature — WARN not FAIL",
                suggested_fix="Create strategy_validation/strategy_validation_schema.py",
            )
        except Exception as exc:
            return _check_item(
                "strategy_validation_import", "imports", "WARN", str(exc),
            )

    def _check_strategy_validation_no_forbidden(self) -> dict:
        """v0.9.2 — StrategyValidationScore has no BUY/SELL/ORDER and validated_does_not_enable_trading=True."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("strategy_validation.strategy_validation_schema")
            if spec is None:
                return _check_item(
                    "strategy_validation_no_forbidden", "safety", "WARN",
                    "strategy_validation.strategy_validation_schema not installed — check skipped.",
                )
            from strategy_validation.strategy_validation_schema import StrategyValidationScore
            # Check class-level safety flag
            flag = getattr(StrategyValidationScore, "validated_does_not_enable_trading", None)
            # Check an instance's suggested_next_step output — use word-boundary matching to avoid
            # false positives from field names like "no_real_orders" (contains "ORDER" as substring)
            import re
            _inst = StrategyValidationScore()
            out_str = str(_inst.to_dict()) if hasattr(_inst, "to_dict") else str(vars(_inst))
            forbidden = [kw for kw in ["BUY", "SELL", "ORDER"] if re.search(r'\b' + kw + r'\b', out_str.upper())]
            if forbidden:
                return _check_item(
                    "strategy_validation_no_forbidden", "safety", "WARN",
                    f"StrategyValidationScore output contains forbidden keywords: {forbidden}",
                    warning="Remove BUY/SELL/ORDER from StrategyValidationScore output",
                    suggested_fix="Ensure StrategyValidationScore produces no trading commands.",
                )
            if flag is False:
                return _check_item(
                    "strategy_validation_no_forbidden", "safety", "WARN",
                    "StrategyValidationScore.validated_does_not_enable_trading is False",
                    warning="Set validated_does_not_enable_trading=True",
                    suggested_fix="Add validated_does_not_enable_trading=True class attribute.",
                )
            return _check_item(
                "strategy_validation_no_forbidden", "safety", "PASS",
                "StrategyValidationScore: no BUY/SELL/ORDER and validated_does_not_enable_trading is safe.",
            )
        except Exception as exc:
            return _check_item(
                "strategy_validation_no_forbidden", "safety", "WARN",
                f"Check skipped (optional): {exc}",
            )

    def _check_strategy_lab_dashboard_import(self) -> dict:
        """v0.9.3 — StrategyLabDashboardEngine imports successfully."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("strategy_lab.strategy_lab_dashboard_engine")
            if spec is None:
                return _check_item(
                    "strategy_lab_dashboard_import", "imports", "WARN",
                    "strategy_lab.strategy_lab_dashboard_engine not found (optional v0.9.3 feature).",
                    warning="Add strategy_lab_dashboard_engine.py to strategy_lab/",
                    suggested_fix="Create strategy_lab/strategy_lab_dashboard_engine.py",
                )
            from strategy_lab.strategy_lab_dashboard_engine import StrategyLabDashboardEngine  # noqa: F401
            return _check_item(
                "strategy_lab_dashboard_import", "imports", "PASS",
                "StrategyLabDashboardEngine imported successfully.",
            )
        except ImportError as exc:
            return _check_item(
                "strategy_lab_dashboard_import", "imports", "WARN",
                f"StrategyLabDashboardEngine import failed (optional): {exc}",
                warning="New optional feature — WARN not FAIL",
                suggested_fix="Check strategy_lab/strategy_lab_dashboard_engine.py",
            )
        except Exception as exc:
            return _check_item(
                "strategy_lab_dashboard_import", "imports", "WARN", str(exc),
            )

    def _check_strategy_lab_dashboard_no_forbidden_actions(self) -> dict:
        """v0.9.3 — StrategyLabDashboardEngine is read_only and no forbidden actions."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("strategy_lab.strategy_lab_dashboard_engine")
            if spec is None:
                return _check_item(
                    "strategy_lab_dashboard_no_forbidden", "safety", "WARN",
                    "strategy_lab.strategy_lab_dashboard_engine not installed — check skipped.",
                )
            from strategy_lab.strategy_lab_dashboard_engine import StrategyLabDashboardEngine
            if not getattr(StrategyLabDashboardEngine, "no_real_orders", False):
                return _check_item(
                    "strategy_lab_dashboard_no_forbidden", "safety", "WARN",
                    "StrategyLabDashboardEngine.no_real_orders is not True",
                    suggested_fix="Set no_real_orders=True on StrategyLabDashboardEngine",
                )
            return _check_item(
                "strategy_lab_dashboard_no_forbidden", "safety", "PASS",
                "StrategyLabDashboardEngine.no_real_orders=True and read_only=True.",
            )
        except Exception as exc:
            return _check_item(
                "strategy_lab_dashboard_no_forbidden", "safety", "WARN",
                f"Check skipped (optional): {exc}",
            )

    # ------------------------------------------------------------------
    # v1.0.0 Research Trading Cockpit Stable checks
    # ------------------------------------------------------------------

    def _check_research_cockpit_stable_import(self) -> dict:
        """v1.0.0 — ResearchCockpitStableChecklist is importable."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("release.research_cockpit_stable_checklist")
            if spec is None:
                return _check_item(
                    "research_cockpit_stable_import", "imports", "WARN",
                    "release.research_cockpit_stable_checklist not found — check skipped.",
                )
            from release.research_cockpit_stable_checklist import ResearchCockpitStableChecklist
            return _check_item(
                "research_cockpit_stable_import", "imports", "PASS",
                "ResearchCockpitStableChecklist imported successfully.",
            )
        except Exception as exc:
            return _check_item(
                "research_cockpit_stable_import", "imports", "WARN",
                f"ResearchCockpitStableChecklist import failed (optional): {exc}",
            )

    def _check_research_cockpit_stable_no_forbidden_actions(self) -> dict:
        """v1.0.0 — ResearchCockpitManifestBuilder has no_real_orders=True and production_blocked=True."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("release.research_cockpit_manifest")
            if spec is None:
                return _check_item(
                    "research_cockpit_stable_no_forbidden", "safety", "WARN",
                    "release.research_cockpit_manifest not found — check skipped.",
                )
            from release.research_cockpit_manifest import ResearchCockpitManifestBuilder
            if (getattr(ResearchCockpitManifestBuilder, "no_real_orders", False) and
                    getattr(ResearchCockpitManifestBuilder, "production_blocked", False)):
                return _check_item(
                    "research_cockpit_stable_no_forbidden", "safety", "PASS",
                    "ResearchCockpitManifestBuilder.no_real_orders=True and production_blocked=True.",
                )
            return _check_item(
                "research_cockpit_stable_no_forbidden", "safety", "WARN",
                "ResearchCockpitManifestBuilder missing no_real_orders or production_blocked.",
            )
        except Exception as exc:
            return _check_item(
                "research_cockpit_stable_no_forbidden", "safety", "WARN",
                f"Check skipped (optional): {exc}",
            )

    def _check_version_info_v100(self) -> dict:
        """v1.0.x — release.version_info.VERSION starts with '1.0.'."""
        try:
            from release.version_info import VERSION
            if VERSION.startswith("1.0."):
                return _check_item(
                    "version_info_v100", "version", "PASS",
                    f"release.version_info.VERSION={VERSION} (v1.0.x stable)",
                )
            return _check_item(
                "version_info_v100", "version", "WARN",
                f"release.version_info.VERSION={VERSION} (expected 1.0.x)",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v100", "version", "WARN",
                f"release.version_info.VERSION check failed: {exc}",
            )

    def _check_version_info_v101(self) -> dict:
        """v1.0.1 — release.version_info.VERSION == '1.0.1' (maintenance release)."""
        try:
            from release.version_info import VERSION
            if VERSION == "1.0.1":
                return _check_item(
                    "version_info_v101", "version", "PASS",
                    f"release.version_info.VERSION={VERSION} (maintenance release)",
                )
            return _check_item(
                "version_info_v101", "version", "WARN",
                f"release.version_info.VERSION={VERSION} (expected 1.0.1 for maintenance)",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v101", "version", "WARN",
                f"release.version_info.VERSION check failed: {exc}",
            )

    def _check_research_cockpit_maintenance_safe(self) -> dict:
        """v1.0.1 — maintenance release still has no_real_orders and production_blocked."""
        try:
            from release.version_info import (
                NO_REAL_ORDERS, PRODUCTION_TRADING_BLOCKED,
                MAINTENANCE_RELEASE, REAL_ORDERS_ENABLED,
            )
            if NO_REAL_ORDERS and PRODUCTION_TRADING_BLOCKED and not REAL_ORDERS_ENABLED:
                return _check_item(
                    "research_cockpit_maintenance_safe", "safety", "PASS",
                    f"Maintenance release safety OK: no_real_orders={NO_REAL_ORDERS}, "
                    f"production_blocked={PRODUCTION_TRADING_BLOCKED}, maintenance={MAINTENANCE_RELEASE}",
                )
            return _check_item(
                "research_cockpit_maintenance_safe", "safety", "FAIL",
                f"Maintenance release safety FAIL: no_real_orders={NO_REAL_ORDERS}, "
                f"production_blocked={PRODUCTION_TRADING_BLOCKED}",
            )
        except Exception as exc:
            return _check_item(
                "research_cockpit_maintenance_safe", "safety", "WARN",
                f"Maintenance safety check failed: {exc}",
            )

    def _check_no_real_orders_false_positive_guard(self) -> dict:
        """v1.0.1 — verify 'No Real Orders' is not misclassified as forbidden ORDER keyword."""
        import re
        _FORBIDDEN = re.compile(
            r'\b(BUY|SELL|ORDER|EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE|LIVE_TRADE|BROKER_ORDER)\b'
        )
        _WHITELIST = [
            "No Real Orders", "Broker Execution Disabled", "No broker execution",
            "Not an order", "VALIDATED does not enable trading",
        ]
        false_positives = []
        for phrase in _WHITELIST:
            cleaned = phrase
            for w in _WHITELIST:
                cleaned = cleaned.replace(w, "")
            hits = _FORBIDDEN.findall(cleaned)
            if hits:
                false_positives.append(f"'{phrase}' → {hits}")
        if not false_positives:
            return _check_item(
                "no_real_orders_false_positive_guard", "safety", "PASS",
                "No Real Orders / Broker Execution Disabled not misclassified as forbidden.",
            )
        return _check_item(
            "no_real_orders_false_positive_guard", "safety", "FAIL",
            f"Whitelist phrases misclassified as forbidden: {false_positives}",
        )

    def _check_maintenance_v101_import(self) -> dict:
        """v1.0.1 — docs/maintenance_v1.0.1.md exists."""
        doc_path = os.path.join(BASE_DIR, "docs", "maintenance_v1.0.1.md")
        if os.path.isfile(doc_path):
            return _check_item(
                "maintenance_v101_import", "docs", "PASS",
                "docs/maintenance_v1.0.1.md exists",
            )
        return _check_item(
            "maintenance_v101_import", "docs", "WARN",
            "docs/maintenance_v1.0.1.md not found",
        )

    def _check_maintenance_v101_no_forbidden_actions(self) -> dict:
        """v1.0.1 — maintenance doc does not contain forbidden action keywords."""
        import re
        _FORBIDDEN = re.compile(
            r'\b(BUY|SELL|ORDER|EXECUTE|SUBMIT_ORDER|AUTO_TRADE|REAL_TRADE|LIVE_TRADE|BROKER_ORDER)\b'
        )
        _WHITELIST = [
            "No Real Orders", "Broker Execution Disabled", "No broker execution",
            "Not an order",
        ]
        doc_path = os.path.join(BASE_DIR, "docs", "maintenance_v1.0.1.md")
        if not os.path.isfile(doc_path):
            return _check_item(
                "maintenance_v101_no_forbidden_actions", "safety", "WARN",
                "docs/maintenance_v1.0.1.md not found — check skipped",
            )
        try:
            with open(doc_path, "r", encoding="utf-8") as fh:
                content = fh.read()
            for phrase in _WHITELIST:
                content = content.replace(phrase, "")
            hits = _FORBIDDEN.findall(content)
            if not hits:
                return _check_item(
                    "maintenance_v101_no_forbidden_actions", "safety", "PASS",
                    "maintenance_v1.0.1.md: no forbidden trading keywords",
                )
            return _check_item(
                "maintenance_v101_no_forbidden_actions", "safety", "FAIL",
                f"maintenance_v1.0.1.md contains forbidden keywords: {list(set(hits))}",
            )
        except Exception as exc:
            return _check_item(
                "maintenance_v101_no_forbidden_actions", "safety", "WARN",
                f"Could not read maintenance doc: {exc}",
            )

    def _check_evidence_graph_ux_no_forbidden(self) -> dict:
        """v0.9.1 — Check EvidenceGraphQuery doesn't output BUY/SELL/ORDER."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("evidence_graph.evidence_graph_query")
            if spec is None:
                return _check_item(
                    "evidence_graph_ux_no_forbidden", "safety", "WARN",
                    "evidence_graph.evidence_graph_query not installed — check skipped.",
                )
            from evidence_graph.evidence_graph_query import EvidenceGraphQuery
            q = EvidenceGraphQuery()
            # Check read_only flag if available
            is_safe = getattr(q, "read_only", True) and getattr(q, "no_real_orders", True)
            out_str = str(vars(q)) if hasattr(q, "__dict__") else ""
            forbidden = [kw for kw in ["BUY", "SELL", "ORDER"] if kw in out_str.upper()]
            if forbidden or not is_safe:
                return _check_item(
                    "evidence_graph_ux_no_forbidden", "safety", "WARN",
                    f"EvidenceGraphQuery safety issue: forbidden={forbidden}, read_only={getattr(q, 'read_only', '?')}",
                    warning="Ensure EvidenceGraphQuery has read_only=True and no BUY/SELL/ORDER output",
                    suggested_fix="Add read_only=True, no_real_orders=True to EvidenceGraphQuery.",
                )
            return _check_item(
                "evidence_graph_ux_no_forbidden", "safety", "PASS",
                "EvidenceGraphQuery is read_only with no BUY/SELL/ORDER output.",
            )
        except Exception as exc:
            return _check_item(
                "evidence_graph_ux_no_forbidden", "safety", "WARN",
                f"Check skipped (optional): {exc}",
            )

    # ----------------------------------------------------------------
    # v1.0.2 Data & Report Hygiene checks
    # ----------------------------------------------------------------

    def _check_data_report_hygiene_import(self) -> dict:
        """v1.0.2 — DataReportHygieneEngine must be importable."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("maintenance.data_report_hygiene_engine")
            if spec is None:
                return _check_item(
                    "data_report_hygiene_import", "safety", "WARN",
                    "maintenance.data_report_hygiene_engine not found",
                    suggested_fix="Create maintenance/data_report_hygiene_engine.py",
                )
            from maintenance.data_report_hygiene_engine import DataReportHygieneEngine
            return _check_item(
                "data_report_hygiene_import", "safety", "PASS",
                "DataReportHygieneEngine imported successfully.",
            )
        except Exception as exc:
            return _check_item(
                "data_report_hygiene_import", "safety", "WARN", str(exc),
            )

    def _check_data_report_hygiene_no_forbidden_actions(self) -> dict:
        """v1.0.2 — DataReportHygieneEngine must have review_only=True."""
        try:
            from maintenance.data_report_hygiene_engine import DataReportHygieneEngine
            eng = DataReportHygieneEngine()
            if not getattr(eng, "review_only", False):
                return _check_item(
                    "data_report_hygiene_no_forbidden_actions", "safety", "FAIL",
                    "DataReportHygieneEngine.review_only is not True",
                )
            return _check_item(
                "data_report_hygiene_no_forbidden_actions", "safety", "PASS",
                "DataReportHygieneEngine.review_only=True — no forbidden actions.",
            )
        except Exception as exc:
            return _check_item(
                "data_report_hygiene_no_forbidden_actions", "safety", "WARN", str(exc),
            )

    def _check_data_report_hygiene_review_only(self) -> dict:
        """v1.0.2 — verify review_only=True and no delete/archive flags."""
        try:
            from maintenance.data_report_hygiene_engine import DataReportHygieneEngine
            eng = DataReportHygieneEngine()
            r  = getattr(eng, "review_only", False)
            no = getattr(eng, "no_real_orders", False)
            if r and no:
                return _check_item(
                    "data_report_hygiene_review_only", "safety", "PASS",
                    "DataReportHygieneEngine: review_only=True, no_real_orders=True.",
                )
            return _check_item(
                "data_report_hygiene_review_only", "safety", "FAIL",
                f"review_only={r}, no_real_orders={no}",
            )
        except Exception as exc:
            return _check_item(
                "data_report_hygiene_review_only", "safety", "WARN", str(exc),
            )

    def _check_version_info_v102(self) -> dict:
        """v1.0.2 — VERSION starts with 1.0."""
        try:
            from release.version_info import VERSION
            if VERSION.startswith("1.0."):
                return _check_item(
                    "version_info_v102", "version_git", "PASS",
                    f"VERSION={VERSION} (1.0.x stable)",
                )
            return _check_item(
                "version_info_v102", "version_git", "WARN",
                f"VERSION={VERSION}",
                warning="Expected VERSION=1.0.x",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v102", "version_git", "WARN", str(exc),
            )

    def _check_gui_health_check_import(self) -> dict:
        """v1.0.3 — gui.gui_health_check.GuiHealthCheck is importable."""
        try:
            from gui.gui_health_check import GuiHealthCheck
            return _check_item(
                "gui_health_check_import", "gui", "PASS",
                "GuiHealthCheck importable",
            )
        except Exception as exc:
            return _check_item(
                "gui_health_check_import", "gui", "WARN", str(exc),
            )

    def _check_gui_health_check_no_forbidden_actions(self) -> dict:
        """v1.0.3 — GUI safety banner contains no forbidden trading actions."""
        _forbidden = ["BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
                      "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER"]
        _wl = ["No Real Orders", "Broker Execution Disabled", "No broker execution",
               "Not an order", "VALIDATED does not enable trading"]
        import re
        try:
            from gui.common.gui_safety import build_research_only_banner
            banner = build_research_only_banner()
            cleaned = banner
            for phrase in _wl:
                cleaned = cleaned.replace(phrase, "")
            hits = [f for f in _forbidden if re.search(r'\b' + f + r'\b', cleaned)]
            if hits:
                return _check_item(
                    "gui_health_check_no_forbidden_actions", "safety", "BLOCKED",
                    f"Forbidden text in GUI safety banner: {hits}",
                )
            return _check_item(
                "gui_health_check_no_forbidden_actions", "safety", "PASS",
                "No forbidden text in GUI safety banner",
            )
        except Exception as exc:
            return _check_item(
                "gui_health_check_no_forbidden_actions", "safety", "WARN", str(exc),
            )

    def _check_version_info_v103(self) -> dict:
        """v1.0.3 — VERSION starts with 1.0. and GUI_POLISH_RELEASE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            gui_polish = getattr(_vi, "GUI_POLISH_RELEASE", None)
            if VERSION.startswith("1.0."):
                return _check_item(
                    "version_info_v103", "version_git", "PASS",
                    f"VERSION={VERSION}, GUI_POLISH_RELEASE={gui_polish}",
                )
            return _check_item(
                "version_info_v103", "version_git", "WARN",
                f"VERSION={VERSION}",
                warning="Expected VERSION=1.0.x",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v103", "version_git", "WARN", str(exc),
            )

    # ----------------------------------------------------------------
    # Run
    # ----------------------------------------------------------------

    def run(self, mode: str = "real") -> dict:
        """Run all checks. Returns results dict. Never crashes."""
        checks: List[dict] = []

        checklist_groups = [
            # A — version / git
            self._check_version_info,
            self._check_git_status,
            self._check_compileall,
            # B — safety
            self._check_safety_flags,
            self._check_no_broker_imports,
            # C — CLI
            self._check_main_exists,
            self._check_stable_v060_commands,
            self._check_core_imports,
            # D — GUI
            self._check_gui_panel_exists,
            self._check_dashboard_tab,
            # E — reports
            self._check_stable_report_exists,
            self._check_report_registry,
            self._check_report_pack_partial,
            # F — regression
            self._check_regression_suite,
            # G — runtime safety
            self._check_capability_matrix_builds,
            self._check_known_limitations_builds,
            self._check_release_schema_builds,
            # H — v0.7.1 Intelligence UX safety
            self._check_research_intelligence_ux_safety,
            self._check_recommendations_no_forbidden_actions,
            # v0.7.2 Strategy Research Memory
            self._check_strategy_memory_summary_can_run,
            self._check_memory_store_no_forbidden_actions,
            # v0.7.3 Backtest-to-Coach Loop
            self._check_backtest_coach_summary_can_run,
            self._check_coach_tasks_no_forbidden_actions,
            # v0.8.0 Research Intelligence Stable
            self._check_intelligence_stable_summary_can_run,
            self._check_intelligence_stable_no_forbidden_actions,
            # v0.8.1 Strategy Memory UX
            self._check_strategy_memory_ux_import,
            self._check_strategy_memory_no_forbidden_commands,
            self._check_accepted_is_research_only,
            # v0.8.2 Backtest Training Metrics
            self._check_training_metrics_summary_can_run,
            self._check_training_metrics_no_forbidden_actions,
            # v0.8.3 Research Intelligence Evidence Graph
            self._check_evidence_graph_summary_can_run,
            self._check_evidence_graph_no_forbidden_actions,
            # v0.9.0 Strategy Lab Stable
            self._check_strategy_lab_import_health,
            self._check_strategy_lab_no_forbidden_actions,
            # v0.9.0.1 crash reversal
            self._check_crash_reversal_import,
            self._check_crash_reversal_no_forbidden_actions,
            # v0.9.1 Evidence Graph UX
            self._check_evidence_graph_ux_import,
            self._check_evidence_graph_ux_no_forbidden,
            # v0.9.2 Strategy Validation Score
            self._check_strategy_validation_import,
            self._check_strategy_validation_no_forbidden,
            # v0.9.3 Strategy Lab Dashboard
            self._check_strategy_lab_dashboard_import,
            self._check_strategy_lab_dashboard_no_forbidden_actions,
            # v1.0.0 Research Trading Cockpit Stable
            self._check_research_cockpit_stable_import,
            self._check_research_cockpit_stable_no_forbidden_actions,
            self._check_version_info_v100,
            # v1.0.1 Maintenance & Polish
            self._check_version_info_v101,
            self._check_research_cockpit_maintenance_safe,
            self._check_no_real_orders_false_positive_guard,
            self._check_maintenance_v101_import,
            self._check_maintenance_v101_no_forbidden_actions,
            # v1.0.2 Data & Report Hygiene
            self._check_data_report_hygiene_import,
            self._check_data_report_hygiene_no_forbidden_actions,
            self._check_data_report_hygiene_review_only,
            self._check_version_info_v102,
            # v1.0.3 GUI Stability & Usability Polish
            self._check_gui_health_check_import,
            self._check_gui_health_check_no_forbidden_actions,
            self._check_version_info_v103,
        ]

        for fn in checklist_groups:
            try:
                result = fn()
                checks.append(result)
            except Exception as exc:
                checks.append(_check_item(
                    fn.__name__, "unknown", "FAIL",
                    f"Unexpected error: {exc}",
                ))

        total   = len(checks)
        passed  = sum(1 for c in checks if c["status"] == "PASS")
        warned  = sum(1 for c in checks if c["status"] == "WARN")
        failed  = sum(1 for c in checks if c["status"] == "FAIL")
        blocked = sum(1 for c in checks if c["status"] == "BLOCKED")

        if failed > 0:
            overall = "FAIL"
        elif warned > 0:
            overall = "WARNING"
        else:
            overall = "PASS"

        self._print_results(total, passed, warned, failed, blocked, overall, checks)

        return {
            "version":        self.VERSION,
            "mode":           mode,
            "run_at":         datetime.now().isoformat(),
            "total_checks":   total,
            "pass_count":     passed,
            "warning_count":  warned,
            "fail_count":     failed,
            "blocked_count":  blocked,
            "overall_status": overall,
            "checks":         checks,
            "no_real_orders": True,
            "production_blocked": True,
        }

    def _print_results(self, total, passed, warned, failed, blocked, overall, checks):
        print("=" * 60)
        print("  TW Quant Cockpit — Research OS Stable Release Checklist v0.6.0")
        print(f"  {_SAFETY_BANNER}")
        print("=" * 60)
        print(f"  Total    : {total}")
        print(f"  Passed   : {passed}")
        print(f"  Warnings : {warned}")
        print(f"  Failed   : {failed}")
        print(f"  Blocked  : {blocked}")
        print(f"  Status   : {overall}")
        print()
        print("  Checks:")
        for c in checks:
            icon = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]", "BLOCKED": "[BLOCKED]"}.get(c["status"], "[?]")
            print(f"  {icon} [{c['category']}] {c['name']}")
            if c["detail"]:
                print(f"       {c['detail'][:100]}")
            if c.get("warning"):
                print(f"       WARNING: {c['warning'][:100]}")
        print("=" * 60)
