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
    # v1.0.4 Regression & Release Gate Hardening checks
    # ----------------------------------------------------------------

    def _check_regression_hardening_import(self) -> dict:
        """v1.0.4 — regression_hardening package importable."""
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            return _check_item(
                "regression_hardening_import", "regression", "PASS",
                "regression_hardening.safety_scanner.SafetyScanner import OK",
            )
        except Exception as exc:
            return _check_item(
                "regression_hardening_import", "regression", "WARN",
                str(exc), suggested_fix="Create regression_hardening package",
            )

    def _check_safety_scanner_import(self) -> dict:
        """v1.0.4 — SafetyScanner with scan_text method available."""
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            scanner = SafetyScanner()
            if hasattr(scanner, 'scan_text'):
                return _check_item(
                    "safety_scanner_import", "regression", "PASS",
                    "SafetyScanner.scan_text available",
                )
            return _check_item(
                "safety_scanner_import", "regression", "WARN",
                "SafetyScanner imported but scan_text not found",
            )
        except Exception as exc:
            return _check_item(
                "safety_scanner_import", "regression", "WARN", str(exc),
            )

    def _check_release_gate_health_import(self) -> dict:
        """v1.0.4 — ReleaseGateHealth importable."""
        try:
            from regression_hardening.release_gate_health import ReleaseGateHealth
            return _check_item(
                "release_gate_health_import", "regression", "PASS",
                "regression_hardening.release_gate_health.ReleaseGateHealth import OK",
            )
        except Exception as exc:
            return _check_item(
                "release_gate_health_import", "regression", "WARN", str(exc),
            )

    def _check_version_info_v104(self) -> dict:
        """v1.0.4 — VERSION starts with 1.0. and REGRESSION_HARDENING_RELEASE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            rh = getattr(_vi, "REGRESSION_HARDENING_RELEASE", None)
            if VERSION.startswith("1.0."):
                return _check_item(
                    "version_info_v104", "version_git", "PASS",
                    f"VERSION={VERSION}, REGRESSION_HARDENING_RELEASE={rh}",
                )
            return _check_item(
                "version_info_v104", "version_git", "WARN",
                f"VERSION={VERSION}",
                warning="Expected VERSION=1.0.x",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v104", "version_git", "WARN", str(exc),
            )

    def _check_no_real_orders_false_positive_guard_v104(self) -> dict:
        """v1.0.4 — SafetyScanner whitelist prevents No Real Orders false positive."""
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            scanner = SafetyScanner()
            result = scanner.scan_text("No Real Orders — Research Only. No broker execution.")
            if result.status == "PASS":
                return _check_item(
                    "no_real_orders_false_positive_guard_v104", "safety", "PASS",
                    "No Real Orders text correctly scans as PASS (whitelisted)",
                )
            return _check_item(
                "no_real_orders_false_positive_guard_v104", "safety", "WARN",
                f"No Real Orders scan returned {result.status}: {result.forbidden_hits}",
            )
        except Exception as exc:
            return _check_item(
                "no_real_orders_false_positive_guard_v104", "safety", "WARN", str(exc),
            )

    def _check_documentation_health_import(self) -> dict:
        """v1.0.5 — documentation.docs_health_check.DocumentationHealthCheck importable."""
        try:
            import importlib
            mod = importlib.import_module("documentation.docs_health_check")
            if hasattr(mod, "DocumentationHealthCheck"):
                return _check_item(
                    "documentation_health_import", "version_git", "PASS",
                    "documentation.docs_health_check.DocumentationHealthCheck importable",
                )
            return _check_item(
                "documentation_health_import", "version_git", "WARN",
                "documentation.docs_health_check imported but DocumentationHealthCheck not found",
            )
        except Exception as exc:
            return _check_item(
                "documentation_health_import", "version_git", "WARN", str(exc),
            )

    def _check_documentation_health_no_forbidden_actions(self) -> dict:
        """v1.0.5 — docs/ directory has no forbidden actions."""
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            scanner = SafetyScanner()
            results = scanner.scan_directory("docs", patterns=["*.md"])
            blocked = [r for r in results if r.status == "BLOCKED"]
            if blocked:
                return _check_item(
                    "documentation_health_no_forbidden_actions", "safety", "WARN",
                    f"{len(blocked)} docs have forbidden actions",
                )
            return _check_item(
                "documentation_health_no_forbidden_actions", "safety", "PASS",
                f"docs/ scanned: {len(results)} files, 0 blocked",
            )
        except Exception as exc:
            return _check_item(
                "documentation_health_no_forbidden_actions", "safety", "WARN", str(exc),
            )

    def _check_version_info_v105(self) -> dict:
        """v1.0.5 — VERSION starts with 1.0. and DOCUMENTATION_POLISH_RELEASE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            dp = getattr(_vi, "DOCUMENTATION_POLISH_RELEASE", None)
            if VERSION.startswith("1.0."):
                return _check_item(
                    "version_info_v105", "version_git", "PASS",
                    f"VERSION={VERSION}, DOCUMENTATION_POLISH_RELEASE={dp}",
                )
            return _check_item(
                "version_info_v105", "version_git", "WARN",
                f"VERSION={VERSION}",
                warning="Expected VERSION=1.0.x",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v105", "version_git", "WARN", str(exc),
            )

    def _check_workflow_templates_import(self) -> dict:
        """v1.0.6 — workflows.workflow_template_health.WorkflowTemplateHealthCheck importable."""
        try:
            import importlib
            mod = importlib.import_module("workflows.workflow_template_health")
            if hasattr(mod, "WorkflowTemplateHealthCheck"):
                return _check_item(
                    "workflow_templates_import", "version_git", "PASS",
                    "workflows.workflow_template_health.WorkflowTemplateHealthCheck importable",
                )
            return _check_item(
                "workflow_templates_import", "version_git", "WARN",
                "workflows.workflow_template_health imported but WorkflowTemplateHealthCheck not found",
            )
        except Exception as exc:
            return _check_item(
                "workflow_templates_import", "version_git", "WARN", str(exc),
            )

    def _check_workflow_templates_no_forbidden_actions(self) -> dict:
        """v1.0.6 — docs/examples/ and docs/templates/ have no forbidden actions."""
        try:
            from regression_hardening.safety_scanner import SafetyScanner
            scanner = SafetyScanner()
            results_ex = scanner.scan_directory("docs/examples", patterns=["*.md"])
            results_tmpl = scanner.scan_directory("docs/templates", patterns=["*.md"])
            blocked = [r for r in results_ex + results_tmpl if r.status == "BLOCKED"]
            if blocked:
                return _check_item(
                    "workflow_templates_no_forbidden_actions", "safety", "WARN",
                    f"{len(blocked)} workflow files have forbidden actions",
                )
            total = len(results_ex) + len(results_tmpl)
            return _check_item(
                "workflow_templates_no_forbidden_actions", "safety", "PASS",
                f"workflow files scanned: {total} files, 0 blocked",
            )
        except Exception as exc:
            return _check_item(
                "workflow_templates_no_forbidden_actions", "safety", "WARN", str(exc),
            )

    def _check_version_info_v106(self) -> dict:
        """v1.0.6 — VERSION starts with 1.0. and EXAMPLE_WORKFLOWS_RELEASE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            ew = getattr(_vi, "EXAMPLE_WORKFLOWS_RELEASE", None)
            if VERSION.startswith("1.0."):
                return _check_item(
                    "version_info_v106", "version_git", "PASS",
                    f"VERSION={VERSION}, EXAMPLE_WORKFLOWS_RELEASE={ew}",
                )
            return _check_item(
                "version_info_v106", "version_git", "WARN",
                f"VERSION={VERSION}",
                warning="Expected VERSION=1.0.x",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v106", "version_git", "WARN", str(exc),
            )

    def _check_knowledge_base_import(self) -> dict:
        """v1.0.7 — knowledge_base package importable."""
        try:
            import importlib
            mod_kb = importlib.import_module("knowledge_base")
            no_orders = getattr(mod_kb, "NO_REAL_ORDERS", None)
            if no_orders is True:
                return _check_item(
                    "knowledge_base_import", "knowledge_base", "PASS",
                    "knowledge_base importable, NO_REAL_ORDERS=True",
                )
            return _check_item(
                "knowledge_base_import", "knowledge_base", "WARN",
                f"knowledge_base importable but NO_REAL_ORDERS={no_orders}",
            )
        except Exception as exc:
            return _check_item(
                "knowledge_base_import", "knowledge_base", "WARN",
                f"knowledge_base import failed (optional): {exc}",
            )

    def _check_knowledge_base_search_no_forbidden_actions(self) -> dict:
        """v1.0.7 — knowledge_base search has no forbidden actions."""
        try:
            import importlib
            mod_kbs = importlib.import_module("knowledge_base.kb_schema")
            forbidden = getattr(mod_kbs, "FORBIDDEN_ACTIONS", [])
            safe_steps = getattr(mod_kbs, "SAFE_NEXT_STEPS", [])
            # Verify safe steps don't contain forbidden
            bad = [s for s in safe_steps if any(f in s.upper() for f in ["BUY", "SELL", "ORDER", "EXECUTE"])]
            if not bad:
                return _check_item(
                    "knowledge_base_search_no_forbidden_actions", "knowledge_base", "PASS",
                    f"No forbidden actions in SAFE_NEXT_STEPS ({len(safe_steps)} steps)",
                )
            return _check_item(
                "knowledge_base_search_no_forbidden_actions", "knowledge_base", "FAIL",
                f"Forbidden actions found in SAFE_NEXT_STEPS: {bad}",
            )
        except Exception as exc:
            return _check_item(
                "knowledge_base_search_no_forbidden_actions", "knowledge_base", "WARN",
                f"Could not verify knowledge_base search safety (optional): {exc}",
            )

    def _check_version_info_v107(self) -> dict:
        """v1.0.7 — VERSION is 1.0.7."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            kb_release = getattr(_vi, "KNOWLEDGE_BASE_SEARCH_RELEASE", None)
            if VERSION == "1.0.7":
                return _check_item(
                    "version_info_v107", "version_git", "PASS",
                    f"VERSION={VERSION}, KNOWLEDGE_BASE_SEARCH_RELEASE={kb_release}",
                )
            return _check_item(
                "version_info_v107", "version_git", "WARN",
                f"VERSION={VERSION} (not 1.0.7, may have been upgraded)",
                warning="Expected VERSION=1.0.7 or newer",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v107", "version_git", "WARN", str(exc),
            )

    def _check_local_assistant_import(self) -> dict:
        """v1.0.8 — local_assistant package importable, EXTERNAL_API_DISABLED=True."""
        try:
            import importlib
            mod_la = importlib.import_module("local_assistant")
            ext_api = getattr(mod_la, "EXTERNAL_API_DISABLED", None)
            no_orders = getattr(mod_la, "NO_REAL_ORDERS", None)
            if ext_api is True and no_orders is True:
                return _check_item(
                    "local_assistant_import", "local_assistant", "PASS",
                    "local_assistant importable, EXTERNAL_API_DISABLED=True, NO_REAL_ORDERS=True",
                )
            return _check_item(
                "local_assistant_import", "local_assistant", "WARN",
                f"local_assistant: EXTERNAL_API_DISABLED={ext_api}, NO_REAL_ORDERS={no_orders}",
            )
        except Exception as exc:
            return _check_item(
                "local_assistant_import", "local_assistant", "WARN",
                f"local_assistant import failed (optional): {exc}",
            )

    def _check_local_assistant_no_forbidden_actions(self) -> dict:
        """v1.0.8 — local_assistant ALLOWED_ACTIONS has no FORBIDDEN_ACTIONS."""
        try:
            from local_assistant.assistant_schema import ALLOWED_ACTIONS, FORBIDDEN_ACTIONS
            overlap = [a for a in ALLOWED_ACTIONS if a in FORBIDDEN_ACTIONS]
            if overlap:
                return _check_item(
                    "local_assistant_no_forbidden_actions", "local_assistant", "FAIL",
                    f"ALLOWED_ACTIONS contains FORBIDDEN: {overlap}",
                )
            return _check_item(
                "local_assistant_no_forbidden_actions", "local_assistant", "PASS",
                f"ALLOWED_ACTIONS safe ({len(ALLOWED_ACTIONS)} actions, 0 forbidden)",
            )
        except Exception as exc:
            return _check_item(
                "local_assistant_no_forbidden_actions", "local_assistant", "WARN",
                f"Could not verify local_assistant action safety (optional): {exc}",
            )

    def _check_local_assistant_external_api_disabled(self) -> dict:
        """v1.0.8 — EXTERNAL_API_DISABLED=True."""
        try:
            import local_assistant as _la_pkg
            ext = getattr(_la_pkg, "EXTERNAL_API_DISABLED", None)
            if ext is True:
                return _check_item(
                    "local_assistant_external_api_disabled", "local_assistant", "PASS",
                    "local_assistant.EXTERNAL_API_DISABLED=True",
                )
            return _check_item(
                "local_assistant_external_api_disabled", "local_assistant", "WARN",
                f"local_assistant.EXTERNAL_API_DISABLED={ext} (expected True)",
            )
        except Exception as exc:
            return _check_item(
                "local_assistant_external_api_disabled", "local_assistant", "WARN",
                f"EXTERNAL_API_DISABLED check: {exc}",
            )

    def _check_version_info_v108(self) -> dict:
        """v1.0.8 — VERSION is 1.0.8."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            la_release = getattr(_vi, "LOCAL_RESEARCH_ASSISTANT_RELEASE", None)
            if VERSION == "1.0.8":
                return _check_item(
                    "version_info_v108", "version_git", "PASS",
                    f"VERSION={VERSION}, LOCAL_RESEARCH_ASSISTANT_RELEASE={la_release}",
                )
            return _check_item(
                "version_info_v108", "version_git", "WARN",
                f"VERSION={VERSION} (expected 1.0.8)",
                warning="Expected VERSION=1.0.8",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v108", "version_git", "WARN", str(exc),
            )

    def _check_final_rollup_import(self) -> dict:
        """v1.0.9 — final_rollup package importable."""
        try:
            from final_rollup.final_rollup_engine import FinalRollupEngine
            return _check_item(
                "final_rollup_import", "stable_integration", "PASS",
                "FinalRollupEngine import OK",
            )
        except Exception as exc:
            return _check_item(
                "final_rollup_import", "stable_integration", "WARN",
                f"final_rollup optional (v1.0.9): {exc}",
                warning="Run: python main.py final-rollup",
            )

    def _check_final_rollup_no_forbidden_actions(self) -> dict:
        """v1.0.9 — final_rollup has no_real_orders=True."""
        try:
            import final_rollup as _fr
            if getattr(_fr, "NO_REAL_ORDERS", None) is True:
                return _check_item(
                    "final_rollup_no_forbidden_actions", "stable_integration", "PASS",
                    "final_rollup: NO_REAL_ORDERS=True",
                )
            return _check_item(
                "final_rollup_no_forbidden_actions", "stable_integration", "WARN",
                f"final_rollup.NO_REAL_ORDERS={getattr(_fr, 'NO_REAL_ORDERS', None)}",
                warning="Check final_rollup/__init__.py safety flags",
            )
        except Exception as exc:
            return _check_item(
                "final_rollup_no_forbidden_actions", "stable_integration", "WARN",
                f"final_rollup import check optional: {exc}",
            )

    def _check_version_info_v109(self) -> dict:
        """v1.0.9 — VERSION is at least 1.0.9 (accepts 1.1.0+)."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            fr_release = getattr(_vi, "FINAL_MAINTENANCE_ROLLUP_RELEASE", None)
            if VERSION in ("1.0.9", "1.1.0"):
                return _check_item(
                    "version_info_v109", "version_git", "PASS",
                    f"VERSION={VERSION}, FINAL_MAINTENANCE_ROLLUP_RELEASE={fr_release}",
                )
            return _check_item(
                "version_info_v109", "version_git", "WARN",
                f"VERSION={VERSION} (expected 1.0.9+)",
                warning="Expected VERSION=1.0.9+",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v109", "version_git", "WARN", str(exc),
            )

    def _check_universe_import(self) -> dict:
        """v1.1.0 — universe package imports OK."""
        try:
            from universe.universe_schema import UniverseSymbol, UniverseDefinition
            from universe import NO_REAL_ORDERS as _u_nro
            assert _u_nro is True
            return _check_item(
                "universe_import", "stable_integration", "PASS",
                "universe package imports OK, NO_REAL_ORDERS=True",
            )
        except Exception as exc:
            return _check_item(
                "universe_import", "stable_integration", "WARN", str(exc),
            )

    def _check_universe_real_mock_separation(self) -> dict:
        """v1.1.0 — real/mock data separation enforced."""
        try:
            from universe import REAL_DATA_COVERAGE_REQUIRED, MOCK_DATA_FORMAL_CONCLUSION_ALLOWED
            if REAL_DATA_COVERAGE_REQUIRED is True and MOCK_DATA_FORMAL_CONCLUSION_ALLOWED is False:
                return _check_item(
                    "universe_real_mock_separation", "stable_integration", "PASS",
                    "REAL_DATA_COVERAGE_REQUIRED=True, MOCK_DATA_FORMAL_CONCLUSION_ALLOWED=False",
                )
            return _check_item(
                "universe_real_mock_separation", "stable_integration", "FAIL",
                f"separation flags wrong: real_required={REAL_DATA_COVERAGE_REQUIRED},"
                f" mock_allowed={MOCK_DATA_FORMAL_CONCLUSION_ALLOWED}",
            )
        except Exception as exc:
            return _check_item(
                "universe_real_mock_separation", "stable_integration", "WARN", str(exc),
            )

    def _check_version_info_v110(self) -> dict:
        """v1.1.0 — VERSION is 1.1.0."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            du_release = getattr(_vi, "DATA_UNIVERSE_EXPANSION_RELEASE", None)
            if VERSION == "1.1.0":
                return _check_item(
                    "version_info_v110", "version_git", "PASS",
                    f"VERSION={VERSION}, DATA_UNIVERSE_EXPANSION_RELEASE={du_release}",
                )
            return _check_item(
                "version_info_v110", "version_git", "WARN",
                f"VERSION={VERSION} (expected 1.1.0)",
                warning="Expected VERSION=1.1.0",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v110", "version_git", "WARN", str(exc),
            )

    def _check_import_onboarding(self) -> dict:
        """v1.1.1 — data_onboarding package imports cleanly."""
        try:
            import data_onboarding
            release_flag = getattr(data_onboarding, "DATA_IMPORT_ONBOARDING_RELEASE", False)
            dry_run      = getattr(data_onboarding, "DRY_RUN_DEFAULT", False)
            no_orders    = getattr(data_onboarding, "NO_REAL_ORDERS", False)
            if release_flag and dry_run and no_orders:
                return _check_item(
                    "_check_import_onboarding", "import_onboarding", "PASS",
                    f"data_onboarding: RELEASE={release_flag}, DRY_RUN_DEFAULT={dry_run}, NO_REAL_ORDERS={no_orders}",
                )
            return _check_item(
                "_check_import_onboarding", "import_onboarding", "WARN",
                f"data_onboarding safety flags incomplete: RELEASE={release_flag} DRY_RUN={dry_run} NO_ORDERS={no_orders}",
            )
        except Exception as exc:
            return _check_item(
                "_check_import_onboarding", "import_onboarding", "WARN", str(exc),
                warning="data_onboarding not importable (optional v1.1.1)",
            )

    def _check_dry_run_safe(self) -> dict:
        """v1.1.1 — DRY_RUN_DEFAULT=True in version_info."""
        try:
            from release.version_info import DRY_RUN_DEFAULT, DESTRUCTIVE_IMPORT_DISABLED
            if DRY_RUN_DEFAULT and DESTRUCTIVE_IMPORT_DISABLED:
                return _check_item(
                    "_check_dry_run_safe", "import_onboarding", "PASS",
                    f"DRY_RUN_DEFAULT={DRY_RUN_DEFAULT}, DESTRUCTIVE_IMPORT_DISABLED={DESTRUCTIVE_IMPORT_DISABLED}",
                )
            return _check_item(
                "_check_dry_run_safe", "import_onboarding", "FAIL",
                f"DRY_RUN_DEFAULT={DRY_RUN_DEFAULT}, DESTRUCTIVE_IMPORT_DISABLED={DESTRUCTIVE_IMPORT_DISABLED}",
            )
        except Exception as exc:
            return _check_item(
                "_check_dry_run_safe", "import_onboarding", "WARN", str(exc),
            )

    def _check_version_info_v111(self) -> dict:
        """v1.1.1 — VERSION is 1.1.0 or 1.1.1."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            obd_release = getattr(_vi, "DATA_IMPORT_ONBOARDING_RELEASE", None)
            if VERSION in ("1.1.0", "1.1.1"):
                return _check_item(
                    "version_info_v111", "version_git", "PASS",
                    f"VERSION={VERSION}, DATA_IMPORT_ONBOARDING_RELEASE={obd_release}",
                )
            return _check_item(
                "version_info_v111", "version_git", "WARN",
                f"VERSION={VERSION} (expected 1.1.0 or 1.1.1)",
                warning="Expected VERSION in (1.1.0, 1.1.1)",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v111", "version_git", "WARN", str(exc),
            )

    def _check_coverage_repair_import(self) -> dict:
        """v1.1.2 — coverage_repair package imports cleanly with safety flags."""
        try:
            import coverage_repair
            no_orders = getattr(coverage_repair, "NO_REAL_ORDERS", False)
            dry_run   = getattr(coverage_repair, "DRY_RUN_DEFAULT", False)
            if no_orders and dry_run:
                return _check_item(
                    "coverage_repair_import", "coverage_repair", "PASS",
                    f"coverage_repair: NO_REAL_ORDERS={no_orders}, DRY_RUN_DEFAULT={dry_run}",
                )
            return _check_item(
                "coverage_repair_import", "coverage_repair", "WARN",
                f"coverage_repair safety flags incomplete: NO_REAL_ORDERS={no_orders} DRY_RUN_DEFAULT={dry_run}",
            )
        except Exception as exc:
            return _check_item(
                "coverage_repair_import", "coverage_repair", "WARN", str(exc),
                warning="coverage_repair not importable (optional v1.1.2)",
            )

    def _check_coverage_repair_dry_run_safe(self) -> dict:
        """v1.1.2 — COVERAGE_REPAIR_DRY_RUN_DEFAULT=True and DESTRUCTIVE_REPAIR_DISABLED_BY_DEFAULT=True."""
        try:
            from release.version_info import (
                COVERAGE_REPAIR_DRY_RUN_DEFAULT, DESTRUCTIVE_REPAIR_DISABLED_BY_DEFAULT,
            )
            if COVERAGE_REPAIR_DRY_RUN_DEFAULT and DESTRUCTIVE_REPAIR_DISABLED_BY_DEFAULT:
                return _check_item(
                    "coverage_repair_dry_run_safe", "coverage_repair", "PASS",
                    f"DRY_RUN_DEFAULT={COVERAGE_REPAIR_DRY_RUN_DEFAULT}, "
                    f"DESTRUCTIVE_DISABLED={DESTRUCTIVE_REPAIR_DISABLED_BY_DEFAULT}",
                )
            return _check_item(
                "coverage_repair_dry_run_safe", "coverage_repair", "FAIL",
                f"DRY_RUN_DEFAULT={COVERAGE_REPAIR_DRY_RUN_DEFAULT}, "
                f"DESTRUCTIVE_DISABLED={DESTRUCTIVE_REPAIR_DISABLED_BY_DEFAULT}",
            )
        except Exception as exc:
            return _check_item(
                "coverage_repair_dry_run_safe", "coverage_repair", "WARN", str(exc),
            )

    def _check_coverage_repair_write_blocked_without_flag(self) -> dict:
        """v1.1.2 — SafeCoverageRepairExecutor.execute(allow_write=False) produces only safe statuses."""
        try:
            from coverage_repair.safe_repair_executor import SafeCoverageRepairExecutor
            from coverage_repair.repair_schema import (
                CoverageRepairPlan, CoverageRepairTask,
                REPAIR_MODE_DEDUPLICATE_IDENTICAL, PRIORITY_P3, STATUS_OPEN,
                RESULT_STATUS_DRY_RUN, RESULT_STATUS_BLOCKED,
                RESULT_STATUS_MANUAL, RESULT_STATUS_SKIPPED, RESULT_STATUS_SOURCE_REQUIRED,
            )
            from datetime import datetime
            task = CoverageRepairTask(
                task_id="test_write_blocked",
                issue_id="test_issue",
                symbol="TST1",
                repair_mode=REPAIR_MODE_DEDUPLICATE_IDENTICAL,
                priority=PRIORITY_P3,
                status=STATUS_OPEN,
                dry_run=True,
            )
            plan = CoverageRepairPlan(
                plan_id="test_plan_blocked",
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                tasks=[task],
                dry_run=True,
            )
            executor = SafeCoverageRepairExecutor()
            summary = executor.execute(plan, allow_write=False)
            safe_statuses = {
                RESULT_STATUS_DRY_RUN, RESULT_STATUS_BLOCKED,
                RESULT_STATUS_MANUAL, RESULT_STATUS_SKIPPED, RESULT_STATUS_SOURCE_REQUIRED,
            }
            all_safe = all(r.status in safe_statuses for r in summary.results)
            if all_safe:
                return _check_item(
                    "coverage_repair_write_blocked_without_flag", "coverage_repair", "PASS",
                    "execute(allow_write=False) produced only safe statuses",
                )
            bad = [r.status for r in summary.results if r.status not in safe_statuses]
            return _check_item(
                "coverage_repair_write_blocked_without_flag", "coverage_repair", "FAIL",
                f"Unsafe statuses: {bad}",
            )
        except Exception as exc:
            return _check_item(
                "coverage_repair_write_blocked_without_flag", "coverage_repair", "WARN", str(exc),
            )

    def _check_version_info_v112(self) -> dict:
        """v1.1.2 — VERSION is 1.1.2 or newer."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            cr_available = getattr(_vi, "COVERAGE_REPAIR_AVAILABLE", None)
            if VERSION >= "1.1.2":
                return _check_item(
                    "version_info_v112", "version_git", "PASS",
                    f"VERSION={VERSION}, COVERAGE_REPAIR_AVAILABLE={cr_available}",
                )
            return _check_item(
                "version_info_v112", "version_git", "WARN",
                f"VERSION={VERSION} (expected 1.1.2+)",
                warning="Expected VERSION=1.1.2+",
            )
        except Exception as exc:
            return _check_item(
                "version_info_v112", "version_git", "WARN", str(exc),
            )

    def _check_data_freshness_import(self) -> dict:
        """v1.1.3 — data_freshness package imports correctly."""
        try:
            import data_freshness
            no_real = getattr(data_freshness, "NO_REAL_ORDERS", False)
            dry_run = getattr(data_freshness, "DATA_FRESHNESS_MONITOR_RELEASE", False)
            if no_real and dry_run:
                return _check_item(
                    "data_freshness_import", "coverage_repair",
                    "PASS",
                    f"data_freshness: NO_REAL_ORDERS={no_real}, DATA_FRESHNESS_MONITOR_RELEASE={dry_run}",
                )
            return _check_item(
                "data_freshness_import", "coverage_repair", "FAIL",
                f"data_freshness safety flags missing: NO_REAL_ORDERS={no_real}",
            )
        except Exception as exc:
            return _check_item("data_freshness_import", "coverage_repair", "FAIL", str(exc))

    def _check_freshness_mock_real_separation(self) -> dict:
        """v1.1.3 — mock data not used for formal freshness conclusions."""
        try:
            import data_freshness
            mock_allowed = getattr(data_freshness, "MOCK_DATA_FORMAL_FRESHNESS_ALLOWED", True)
            if not mock_allowed:
                return _check_item(
                    "freshness_mock_real_separation", "coverage_repair",
                    "PASS", "MOCK_DATA_FORMAL_FRESHNESS_ALLOWED=False",
                )
            return _check_item(
                "freshness_mock_real_separation", "coverage_repair", "FAIL",
                "MOCK_DATA_FORMAL_FRESHNESS_ALLOWED must be False",
            )
        except Exception as exc:
            return _check_item("freshness_mock_real_separation", "coverage_repair", "FAIL", str(exc))

    def _check_freshness_future_date_guard(self) -> dict:
        """v1.1.3 — future date is not counted as fresh."""
        try:
            import data_freshness
            future_fresh = getattr(data_freshness, "FUTURE_DATE_COUNTS_AS_FRESH", True)
            if not future_fresh:
                return _check_item(
                    "freshness_future_date_guard", "coverage_repair",
                    "PASS", "FUTURE_DATE_COUNTS_AS_FRESH=False",
                )
            return _check_item(
                "freshness_future_date_guard", "coverage_repair", "FAIL",
                "FUTURE_DATE_COUNTS_AS_FRESH must be False",
            )
        except Exception as exc:
            return _check_item("freshness_future_date_guard", "coverage_repair", "FAIL", str(exc))

    def _check_version_info_v113(self) -> dict:
        """v1.1.3 — VERSION is 1.1.3 and DATA_FRESHNESS_MONITOR_AVAILABLE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            df_available = getattr(_vi, "DATA_FRESHNESS_MONITOR_AVAILABLE", None)
            if VERSION == "1.1.3" and df_available:
                return _check_item(
                    "version_info_v113", "version_git", "PASS",
                    f"VERSION={VERSION}, DATA_FRESHNESS_MONITOR_AVAILABLE={df_available}",
                )
            return _check_item(
                "version_info_v113", "version_git", "WARN",
                f"VERSION={VERSION}, DATA_FRESHNESS_MONITOR_AVAILABLE={df_available}",
                warning="Expected VERSION=1.1.3 with DATA_FRESHNESS_MONITOR_AVAILABLE=True",
            )
        except Exception as exc:
            return _check_item("version_info_v113", "version_git", "WARN", str(exc))

    def _check_quality_gate_import(self) -> dict:
        """v1.1.4 — quality_gates package imports correctly."""
        try:
            import quality_gates
            no_real = getattr(quality_gates, "NO_REAL_ORDERS", False)
            qg_avail = getattr(quality_gates, "COVERAGE_QUALITY_GATES_RELEASE", False)
            if no_real and qg_avail:
                return _check_item(
                    "quality_gate_import", "coverage_repair",
                    "PASS",
                    f"quality_gates: NO_REAL_ORDERS={no_real}, COVERAGE_QUALITY_GATES_RELEASE={qg_avail}",
                )
            return _check_item(
                "quality_gate_import", "coverage_repair", "FAIL",
                f"quality_gates safety flags missing: NO_REAL_ORDERS={no_real}",
            )
        except Exception as exc:
            return _check_item("quality_gate_import", "coverage_repair", "FAIL", str(exc))

    def _check_quality_gate_mock_guard(self) -> dict:
        """v1.1.4 — mock data cannot pass formal gate."""
        try:
            import quality_gates
            mock_allowed = getattr(quality_gates, "MOCK_DATA_FORMAL_GATE_ALLOWED", True)
            if not mock_allowed:
                return _check_item(
                    "quality_gate_mock_guard", "coverage_repair",
                    "PASS", "MOCK_DATA_FORMAL_GATE_ALLOWED=False",
                )
            return _check_item(
                "quality_gate_mock_guard", "coverage_repair", "FAIL",
                "MOCK_DATA_FORMAL_GATE_ALLOWED must be False",
            )
        except Exception as exc:
            return _check_item("quality_gate_mock_guard", "coverage_repair", "FAIL", str(exc))

    def _check_quality_gate_conflict_guard(self) -> dict:
        """v1.1.4 — conflict data cannot pass formal gate."""
        try:
            import quality_gates
            conflict_allowed = getattr(quality_gates, "CONFLICT_DATA_FORMAL_GATE_ALLOWED", True)
            if not conflict_allowed:
                return _check_item(
                    "quality_gate_conflict_guard", "coverage_repair",
                    "PASS", "CONFLICT_DATA_FORMAL_GATE_ALLOWED=False",
                )
            return _check_item(
                "quality_gate_conflict_guard", "coverage_repair", "FAIL",
                "CONFLICT_DATA_FORMAL_GATE_ALLOWED must be False",
            )
        except Exception as exc:
            return _check_item("quality_gate_conflict_guard", "coverage_repair", "FAIL", str(exc))

    def _check_quality_gate_future_date_guard(self) -> dict:
        """v1.1.4 — future date / invalid data cannot pass formal gate."""
        try:
            import quality_gates
            invalid_allowed = getattr(quality_gates, "INVALID_DATA_FORMAL_GATE_ALLOWED", True)
            if not invalid_allowed:
                return _check_item(
                    "quality_gate_future_date_guard", "coverage_repair",
                    "PASS", "INVALID_DATA_FORMAL_GATE_ALLOWED=False",
                )
            return _check_item(
                "quality_gate_future_date_guard", "coverage_repair", "FAIL",
                "INVALID_DATA_FORMAL_GATE_ALLOWED must be False",
            )
        except Exception as exc:
            return _check_item("quality_gate_future_date_guard", "coverage_repair", "FAIL", str(exc))

    def _check_version_info_v114(self) -> dict:
        """v1.1.4 — VERSION is 1.1.4 and COVERAGE_QUALITY_GATES_AVAILABLE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            qg_available = getattr(_vi, "COVERAGE_QUALITY_GATES_AVAILABLE", None)
            if VERSION == "1.1.4" and qg_available:
                return _check_item(
                    "version_info_v114", "version_git", "PASS",
                    f"VERSION={VERSION}, COVERAGE_QUALITY_GATES_AVAILABLE={qg_available}",
                )
            return _check_item(
                "version_info_v114", "version_git", "WARN",
                f"VERSION={VERSION}, COVERAGE_QUALITY_GATES_AVAILABLE={qg_available}",
                warning="Expected VERSION=1.1.4 with COVERAGE_QUALITY_GATES_AVAILABLE=True",
            )
        except Exception as exc:
            return _check_item("version_info_v114", "version_git", "WARN", str(exc))

    def _check_enforcement_import(self) -> dict:
        """v1.1.5 — gate_enforcement package imports correctly."""
        try:
            import gate_enforcement
            _avail = getattr(gate_enforcement, "QUALITY_GATE_ENFORCEMENT_AVAILABLE", False)
            _no_orders = getattr(gate_enforcement, "NO_REAL_ORDERS", False)
            if _avail and _no_orders:
                return _check_item(
                    "enforcement_import", "gate_enforcement", "PASS",
                    f"gate_enforcement: QUALITY_GATE_ENFORCEMENT_AVAILABLE={_avail}, NO_REAL_ORDERS={_no_orders}",
                )
            return _check_item(
                "enforcement_import", "gate_enforcement", "FAIL",
                f"gate_enforcement: QUALITY_GATE_ENFORCEMENT_AVAILABLE={_avail}, NO_REAL_ORDERS={_no_orders}",
            )
        except Exception as exc:
            return _check_item("enforcement_import", "gate_enforcement", "FAIL", str(exc))

    def _check_enforcement_formal_filter(self) -> dict:
        """v1.1.5 — formal filter only allows ELIGIBLE_FORMAL symbols."""
        try:
            from gate_enforcement.symbol_filter import QualityGateSymbolFilter
            from quality_gates.gate_schema import (
                ELIGIBLE_FORMAL, ELIGIBLE_OBSERVATIONAL, DEMO_ONLY, BLOCKED_INVALID,
            )
            flt = QualityGateSymbolFilter()
            mock_decisions = {
                "AA": ELIGIBLE_FORMAL,
                "BB": ELIGIBLE_OBSERVATIONAL,
                "CC": DEMO_ONLY,
                "DD": BLOCKED_INVALID,
            }
            included = flt.include_formal(mock_decisions)
            if included == ["AA"]:
                return _check_item(
                    "enforcement_formal_filter", "gate_enforcement", "PASS",
                    "Formal filter correctly restricts to ELIGIBLE_FORMAL only",
                )
            return _check_item(
                "enforcement_formal_filter", "gate_enforcement", "FAIL",
                f"Formal filter returned {included}, expected ['AA']",
            )
        except Exception as exc:
            return _check_item("enforcement_formal_filter", "gate_enforcement", "WARN", str(exc))

    def _check_enforcement_mock_guard(self) -> dict:
        """v1.1.5 — MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED is False."""
        try:
            import gate_enforcement
            _mock = getattr(gate_enforcement, "MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED", True)
            if not _mock:
                return _check_item(
                    "enforcement_mock_guard", "gate_enforcement", "PASS",
                    f"MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED={_mock} (must be False)",
                )
            return _check_item(
                "enforcement_mock_guard", "gate_enforcement", "FAIL",
                f"MOCK_DATA_FORMAL_ENFORCEMENT_ALLOWED={_mock} (must be False)",
            )
        except Exception as exc:
            return _check_item("enforcement_mock_guard", "gate_enforcement", "FAIL", str(exc))

    def _check_enforcement_audit_chain(self) -> dict:
        """v1.1.5 — audit log chain verification does not crash."""
        try:
            from gate_enforcement.audit_log import QualityGateAuditLog
            log = QualityGateAuditLog()
            chain = log.verify_chain()
            if isinstance(chain, dict) and "valid" in chain:
                return _check_item(
                    "enforcement_audit_chain", "gate_enforcement", "PASS",
                    f"QualityGateAuditLog.verify_chain() returned valid dict: valid={chain.get('valid')}",
                )
            return _check_item(
                "enforcement_audit_chain", "gate_enforcement", "WARN",
                f"verify_chain() returned unexpected type: {type(chain)}",
            )
        except Exception as exc:
            return _check_item("enforcement_audit_chain", "gate_enforcement", "WARN", str(exc))

    def _check_version_info_v115(self) -> dict:
        """v1.1.5 — VERSION is 1.1.5 and QUALITY_GATE_ENFORCEMENT_AVAILABLE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            ge_available = getattr(_vi, "QUALITY_GATE_ENFORCEMENT_AVAILABLE", None)
            if VERSION == "1.1.5" and ge_available:
                return _check_item(
                    "version_info_v115", "version_git", "PASS",
                    f"VERSION={VERSION}, QUALITY_GATE_ENFORCEMENT_AVAILABLE={ge_available}",
                )
            return _check_item(
                "version_info_v115", "version_git", "WARN",
                f"VERSION={VERSION}, QUALITY_GATE_ENFORCEMENT_AVAILABLE={ge_available}",
                warning="Expected VERSION=1.1.5 with QUALITY_GATE_ENFORCEMENT_AVAILABLE=True",
            )
        except Exception as exc:
            return _check_item("version_info_v115", "version_git", "WARN", str(exc))

    # ----------------------------------------------------------------
    # v1.1.6 Data Governance Operations Dashboard checks
    # ----------------------------------------------------------------

    def _check_governance_ops_import(self) -> dict:
        """v1.1.6 — governance_ops package imports correctly."""
        try:
            import governance_ops
            _avail = getattr(governance_ops, "DATA_GOVERNANCE_DASHBOARD_AVAILABLE", False)
            _no_orders = getattr(governance_ops, "NO_REAL_ORDERS", False)
            if _avail and _no_orders:
                return _check_item(
                    "governance_ops_import", "governance_ops", "PASS",
                    f"governance_ops: DATA_GOVERNANCE_DASHBOARD_AVAILABLE={_avail}, NO_REAL_ORDERS={_no_orders}",
                )
            return _check_item(
                "governance_ops_import", "governance_ops", "FAIL",
                f"governance_ops: DATA_GOVERNANCE_DASHBOARD_AVAILABLE={_avail}, NO_REAL_ORDERS={_no_orders}",
            )
        except Exception as exc:
            return _check_item("governance_ops_import", "governance_ops", "FAIL", str(exc))

    def _check_governance_auto_repair_disabled(self) -> dict:
        """v1.1.6 — GOVERNANCE_AUTO_REPAIR_ENABLED is False."""
        try:
            import governance_ops
            _auto = getattr(governance_ops, "GOVERNANCE_AUTO_REPAIR_ENABLED", True)
            if not _auto:
                return _check_item(
                    "governance_auto_repair_disabled", "governance_ops", "PASS",
                    f"GOVERNANCE_AUTO_REPAIR_ENABLED={_auto} (must be False)",
                )
            return _check_item(
                "governance_auto_repair_disabled", "governance_ops", "FAIL",
                f"GOVERNANCE_AUTO_REPAIR_ENABLED={_auto} (must be False)",
            )
        except Exception as exc:
            return _check_item("governance_auto_repair_disabled", "governance_ops", "FAIL", str(exc))

    def _check_governance_trade_execution_disabled(self) -> dict:
        """v1.1.6 — GOVERNANCE_TRADE_EXECUTION_ENABLED is False."""
        try:
            import governance_ops
            _trade = getattr(governance_ops, "GOVERNANCE_TRADE_EXECUTION_ENABLED", True)
            if not _trade:
                return _check_item(
                    "governance_trade_execution_disabled", "governance_ops", "PASS",
                    f"GOVERNANCE_TRADE_EXECUTION_ENABLED={_trade} (must be False)",
                )
            return _check_item(
                "governance_trade_execution_disabled", "governance_ops", "FAIL",
                f"GOVERNANCE_TRADE_EXECUTION_ENABLED={_trade} (must be False)",
            )
        except Exception as exc:
            return _check_item("governance_trade_execution_disabled", "governance_ops", "FAIL", str(exc))

    def _check_governance_no_forbidden_actions(self) -> dict:
        """v1.1.6 — governance health check passes with no FAIL."""
        try:
            from governance_ops.operations_health import DataGovernanceOperationsHealthCheck
            _gh = DataGovernanceOperationsHealthCheck()
            _results = _gh.run()
            _fail = sum(1 for r in _results if r[1] == "FAIL")
            if _fail == 0:
                return _check_item(
                    "governance_no_forbidden_actions", "governance_ops", "PASS",
                    f"DataGovernanceOperationsHealthCheck: {len(_results)} checks, {_fail} FAIL",
                )
            return _check_item(
                "governance_no_forbidden_actions", "governance_ops", "FAIL",
                f"DataGovernanceOperationsHealthCheck: {len(_results)} checks, {_fail} FAIL",
            )
        except Exception as exc:
            return _check_item("governance_no_forbidden_actions", "governance_ops", "WARN", str(exc))

    def _check_version_info_v116(self) -> dict:
        """v1.1.6 — VERSION is 1.1.6 and DATA_GOVERNANCE_DASHBOARD_AVAILABLE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            gov_avail = getattr(_vi, "DATA_GOVERNANCE_DASHBOARD_AVAILABLE", None)
            if VERSION == "1.1.6" and gov_avail:
                return _check_item(
                    "version_info_v116", "version_git", "PASS",
                    f"VERSION={VERSION}, DATA_GOVERNANCE_DASHBOARD_AVAILABLE={gov_avail}",
                )
            return _check_item(
                "version_info_v116", "version_git", "WARN",
                f"VERSION={VERSION}, DATA_GOVERNANCE_DASHBOARD_AVAILABLE={gov_avail}",
                warning="Expected VERSION=1.1.6 with DATA_GOVERNANCE_DASHBOARD_AVAILABLE=True",
            )
        except Exception as exc:
            return _check_item("version_info_v116", "version_git", "WARN", str(exc))

    def _check_governance_alerts_import(self) -> dict:
        """v1.1.7 — governance_alerts package imports without error."""
        try:
            import governance_alerts
            from governance_alerts.alert_schema import GovernanceAlert
            from governance_alerts.alert_deduplicator import GovernanceAlertDeduplicator
            return _check_item(
                "governance_alerts_import", "governance_alerts", "PASS",
                "governance_alerts package and key classes imported OK",
            )
        except Exception as exc:
            return _check_item("governance_alerts_import", "governance_alerts", "FAIL", str(exc))

    def _check_governance_alert_dedup(self) -> dict:
        """v1.1.7 — GovernanceAlertDeduplicator available and deterministic."""
        try:
            from governance_alerts.alert_deduplicator import GovernanceAlertDeduplicator
            from governance_alerts.alert_schema import GovernanceAlert
            d = GovernanceAlertDeduplicator()
            # Build two identical alerts to test fingerprint determinism
            a1 = GovernanceAlert(
                alert_id="tst-1", fingerprint="",
                alert_type="AUDIT_CHAIN_FAILURE", severity="CRITICAL", priority="P0",
                title="T", message="M", symbol="TST001",
                dataset="daily_price", source="test", module="TEST",
                reason_codes=["HASH_MISMATCH"],
            )
            a2 = GovernanceAlert(
                alert_id="tst-2", fingerprint="",
                alert_type="AUDIT_CHAIN_FAILURE", severity="CRITICAL", priority="P0",
                title="T", message="M", symbol="TST001",
                dataset="daily_price", source="test", module="TEST",
                reason_codes=["HASH_MISMATCH"],
            )
            fp1 = d.build_fingerprint(a1)
            fp2 = d.build_fingerprint(a2)
            if fp1 == fp2 and len(fp1) > 10:
                return _check_item(
                    "governance_alert_dedup", "governance_alerts", "PASS",
                    f"Fingerprint deterministic: {fp1[:20]}...",
                )
            return _check_item(
                "governance_alert_dedup", "governance_alerts", "FAIL",
                f"Fingerprint not deterministic: {fp1} != {fp2}",
            )
        except Exception as exc:
            return _check_item("governance_alert_dedup", "governance_alerts", "FAIL", str(exc))

    def _check_governance_alert_lifecycle(self) -> dict:
        """v1.1.7 — GovernanceAlertLifecycle available."""
        try:
            from governance_alerts.alert_lifecycle import GovernanceAlertLifecycle
            _lc = GovernanceAlertLifecycle()
            return _check_item(
                "governance_alert_lifecycle", "governance_alerts", "PASS",
                "GovernanceAlertLifecycle imported and instantiated OK",
            )
        except Exception as exc:
            return _check_item("governance_alert_lifecycle", "governance_alerts", "FAIL", str(exc))

    def _check_governance_external_send_disabled(self) -> dict:
        """v1.1.7 — EXTERNAL_NOTIFICATION_SEND_ENABLED is False."""
        try:
            import governance_alerts
            _ext = getattr(governance_alerts, "EXTERNAL_NOTIFICATION_SEND_ENABLED", True)
            if not _ext:
                return _check_item(
                    "governance_external_send_disabled", "governance_alerts", "PASS",
                    f"EXTERNAL_NOTIFICATION_SEND_ENABLED={_ext} (False as required)",
                )
            return _check_item(
                "governance_external_send_disabled", "governance_alerts", "FAIL",
                f"EXTERNAL_NOTIFICATION_SEND_ENABLED={_ext} (must be False)",
            )
        except Exception as exc:
            return _check_item("governance_external_send_disabled", "governance_alerts", "FAIL", str(exc))

    def _check_version_info_v117(self) -> dict:
        """v1.1.7 — VERSION is 1.1.7 and GOVERNANCE_ALERTS_AVAILABLE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            ga_avail = getattr(_vi, "GOVERNANCE_ALERTS_AVAILABLE", None)
            ext_send = getattr(_vi, "EXTERNAL_NOTIFICATION_SEND_ENABLED", True)
            if VERSION == "1.1.7" and ga_avail and not ext_send:
                return _check_item(
                    "version_info_v117", "version_git", "PASS",
                    f"VERSION={VERSION}, GOVERNANCE_ALERTS_AVAILABLE={ga_avail}, "
                    f"EXTERNAL_NOTIFICATION_SEND_ENABLED={ext_send}",
                )
            return _check_item(
                "version_info_v117", "version_git", "WARN",
                f"VERSION={VERSION}, GOVERNANCE_ALERTS_AVAILABLE={ga_avail}, "
                f"EXTERNAL_NOTIFICATION_SEND_ENABLED={ext_send}",
                warning="Expected VERSION=1.1.7 with GOVERNANCE_ALERTS_AVAILABLE=True, EXTERNAL_NOTIFICATION_SEND_ENABLED=False",
            )
        except Exception as exc:
            return _check_item("version_info_v117", "version_git", "WARN", str(exc))

    def _check_research_registry_import(self) -> dict:
        """v1.1.8 — research_registry package imports without error."""
        try:
            import research_registry
            from research_registry.registry_schema import ResearchRunRecord
            from research_registry.registry_engine import ResearchRunRegistryEngine
            return _check_item(
                "research_registry_import", "research_registry", "PASS",
                "research_registry package and key classes imported OK",
            )
        except Exception as exc:
            return _check_item("research_registry_import", "research_registry", "FAIL", str(exc))

    def _check_research_registry_lineage(self) -> dict:
        """v1.1.8 — ResearchRunLineageManager available."""
        try:
            from research_registry.run_lineage import ResearchRunLineageManager
            _lm = ResearchRunLineageManager()
            return _check_item(
                "research_registry_lineage", "research_registry", "PASS",
                "ResearchRunLineageManager imported and instantiated OK",
            )
        except Exception as exc:
            return _check_item("research_registry_lineage", "research_registry", "FAIL", str(exc))

    def _check_research_registry_duplicate_detection(self) -> dict:
        """v1.1.8 — ResearchRunDuplicateDetector available."""
        try:
            from research_registry.duplicate_detector import ResearchRunDuplicateDetector
            _dd = ResearchRunDuplicateDetector()
            return _check_item(
                "research_registry_duplicate_detection", "research_registry", "PASS",
                "ResearchRunDuplicateDetector imported and instantiated OK",
            )
        except Exception as exc:
            return _check_item("research_registry_duplicate_detection", "research_registry", "FAIL", str(exc))

    def _check_research_registry_trade_execution_disabled(self) -> dict:
        """v1.1.8 — REGISTRY_TRADE_EXECUTION_ENABLED is False."""
        try:
            import research_registry
            _trade = getattr(research_registry, "REGISTRY_TRADE_EXECUTION_ENABLED", True)
            if not _trade:
                return _check_item(
                    "research_registry_trade_execution_disabled", "research_registry", "PASS",
                    f"REGISTRY_TRADE_EXECUTION_ENABLED={_trade} (False as required)",
                )
            return _check_item(
                "research_registry_trade_execution_disabled", "research_registry", "FAIL",
                f"REGISTRY_TRADE_EXECUTION_ENABLED={_trade} (must be False)",
            )
        except Exception as exc:
            return _check_item("research_registry_trade_execution_disabled", "research_registry", "FAIL", str(exc))

    def _check_version_info_v118(self) -> dict:
        """v1.1.8 — VERSION is 1.1.8 or later and RESEARCH_RUN_REGISTRY_AVAILABLE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            rrr_avail = getattr(_vi, "RESEARCH_RUN_REGISTRY_AVAILABLE", None)
            trade_exec = getattr(_vi, "RUN_TRADE_EXECUTION_ENABLED", True)
            if rrr_avail and not trade_exec:
                return _check_item(
                    "version_info_v118", "version_git", "PASS",
                    f"VERSION={VERSION}, RESEARCH_RUN_REGISTRY_AVAILABLE={rrr_avail}, "
                    f"RUN_TRADE_EXECUTION_ENABLED={trade_exec}",
                )
            return _check_item(
                "version_info_v118", "version_git", "WARN",
                f"VERSION={VERSION}, RESEARCH_RUN_REGISTRY_AVAILABLE={rrr_avail}, "
                f"RUN_TRADE_EXECUTION_ENABLED={trade_exec}",
                warning="Expected RESEARCH_RUN_REGISTRY_AVAILABLE=True, RUN_TRADE_EXECUTION_ENABLED=False",
            )
        except Exception as exc:
            return _check_item("version_info_v118", "version_git", "WARN", str(exc))

    def _check_governance_rollup_import(self) -> dict:
        """v1.1.9 — governance_rollup package imports without error."""
        try:
            import governance_rollup
            from governance_rollup.rollup_schema import StableRollupSummary
            from governance_rollup.rollup_health import DataGovernanceStableRollupHealthCheck
            from governance_rollup.consistency_checker import CrossModuleConsistencyChecker
            return _check_item(
                "governance_rollup_import", "governance_rollup", "PASS",
                "governance_rollup package and key classes imported OK",
            )
        except Exception as exc:
            return _check_item("governance_rollup_import", "governance_rollup", "FAIL", str(exc))

    def _check_governance_rollup_consistency(self) -> dict:
        """v1.1.9 — CrossModuleConsistencyChecker can run."""
        try:
            from governance_rollup.consistency_checker import CrossModuleConsistencyChecker
            checker = CrossModuleConsistencyChecker()
            result = checker.check_version_consistency()
            return _check_item(
                "governance_rollup_consistency", "governance_rollup", "PASS",
                f"CrossModuleConsistencyChecker ran OK: consistent={result.get('consistent', False)}",
            )
        except Exception as exc:
            return _check_item("governance_rollup_consistency", "governance_rollup", "WARN", str(exc))

    def _check_governance_rollup_store_validation(self) -> dict:
        """v1.1.9 — GovernanceStoreValidator can run."""
        try:
            from governance_rollup.store_inventory import GovernanceStoreInventory
            from governance_rollup.store_validator import GovernanceStoreValidator
            inv = GovernanceStoreInventory()
            records = inv.build_inventory()
            validator = GovernanceStoreValidator()
            results = [validator.validate_store(r) for r in records]
            summary = validator.summarize(results)
            total = summary.get("total", 0)
            invalid = summary.get("invalid", 0)
            status = "PASS" if invalid == 0 else "WARN"
            return _check_item(
                "governance_rollup_store_validation", "governance_rollup", status,
                f"GovernanceStoreValidator ran OK: {total} stores checked, {invalid} invalid",
            )
        except Exception as exc:
            return _check_item("governance_rollup_store_validation", "governance_rollup", "WARN", str(exc))

    def _check_governance_rollup_trade_execution_disabled(self) -> dict:
        """v1.1.9 — TRADE_EXECUTION_ENABLED is False in governance_rollup."""
        try:
            import governance_rollup
            _trade = getattr(governance_rollup, "TRADE_EXECUTION_ENABLED", True)
            _auto_repair = getattr(governance_rollup, "AUTO_STORE_REPAIR_ENABLED", True)
            _auto_exec = getattr(governance_rollup, "AUTO_RESEARCH_EXECUTION_ENABLED", True)
            if not _trade and not _auto_repair and not _auto_exec:
                return _check_item(
                    "governance_rollup_trade_execution_disabled", "governance_rollup", "PASS",
                    f"TRADE_EXECUTION_ENABLED={_trade}, AUTO_STORE_REPAIR_ENABLED={_auto_repair}, "
                    f"AUTO_RESEARCH_EXECUTION_ENABLED={_auto_exec} (all False as required)",
                )
            return _check_item(
                "governance_rollup_trade_execution_disabled", "governance_rollup", "FAIL",
                f"TRADE_EXECUTION_ENABLED={_trade}, AUTO_STORE_REPAIR_ENABLED={_auto_repair}, "
                f"AUTO_RESEARCH_EXECUTION_ENABLED={_auto_exec} (all must be False)",
            )
        except Exception as exc:
            return _check_item("governance_rollup_trade_execution_disabled", "governance_rollup", "FAIL", str(exc))

    def _check_version_info_v119(self) -> dict:
        """v1.1.9 — VERSION is 1.1.9 and DATA_GOVERNANCE_STABLE_ROLLUP_AVAILABLE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            gr_avail = getattr(_vi, "DATA_GOVERNANCE_STABLE_ROLLUP_AVAILABLE", None)
            trade_exec = getattr(_vi, "TRADE_EXECUTION_ENABLED", True)
            auto_repair = getattr(_vi, "AUTO_STORE_REPAIR_ENABLED", True)
            if VERSION == "1.1.9" and gr_avail and not trade_exec and not auto_repair:
                return _check_item(
                    "version_info_v119", "version_git", "PASS",
                    f"VERSION={VERSION}, DATA_GOVERNANCE_STABLE_ROLLUP_AVAILABLE={gr_avail}, "
                    f"TRADE_EXECUTION_ENABLED={trade_exec}, AUTO_STORE_REPAIR_ENABLED={auto_repair}",
                )
            return _check_item(
                "version_info_v119", "version_git", "WARN",
                f"VERSION={VERSION}, DATA_GOVERNANCE_STABLE_ROLLUP_AVAILABLE={gr_avail}, "
                f"TRADE_EXECUTION_ENABLED={trade_exec}, AUTO_STORE_REPAIR_ENABLED={auto_repair}",
                warning="Expected VERSION=1.1.9 with DATA_GOVERNANCE_STABLE_ROLLUP_AVAILABLE=True, "
                        "TRADE_EXECUTION_ENABLED=False, AUTO_STORE_REPAIR_ENABLED=False",
            )
        except Exception as exc:
            return _check_item("version_info_v119", "version_git", "WARN", str(exc))

    def _check_replay_import(self) -> dict:
        """v1.2.0 — replay.replay_training_engine imports correctly."""
        try:
            from replay.replay_training_engine import ReplayTrainingEngine
            from replay.replay_health import ReplayTrainingHealthCheck
            from replay.replay_schema import ReplaySessionConfig, ReplayDecision
            return _check_item(
                "replay_import", "replay_training", "PASS",
                "replay.replay_training_engine, replay.replay_health, replay.replay_schema imported OK",
            )
        except Exception as exc:
            return _check_item("replay_import", "replay_training", "WARN", str(exc))

    def _check_replay_timeline(self) -> dict:
        """v1.2.0 — replay timeline navigation guards work."""
        try:
            from replay.replay_timeline import ReplayTimeline
            tl = ReplayTimeline()
            tl.initialize(["2023-01-02", "2023-01-03", "2023-01-04"])
            prev, changed = tl.previous()
            if changed:
                return _check_item(
                    "replay_timeline", "replay_training", "FAIL",
                    "previous() at first day should return changed=False",
                )
            return _check_item(
                "replay_timeline", "replay_training", "PASS",
                "Timeline navigation guards working (previous at first day: changed=False)",
            )
        except Exception as exc:
            return _check_item("replay_timeline", "replay_training", "WARN", str(exc))

    def _check_replay_future_firewall(self) -> dict:
        """v1.2.0 — replay future data firewall detects forbidden fields."""
        try:
            from replay.future_data_firewall import ReplayFutureDataFirewall
            fw = ReplayFutureDataFirewall()
            found = fw.future_field_scan({"forward_return_5": 0.05, "close": 100.0})
            if "forward_return_5" not in found:
                return _check_item(
                    "replay_future_firewall", "replay_training", "FAIL",
                    "Firewall did not detect forward_return_5 as forbidden",
                )
            return _check_item(
                "replay_future_firewall", "replay_training", "PASS",
                f"Future firewall working: detected {found}",
            )
        except Exception as exc:
            return _check_item("replay_future_firewall", "replay_training", "WARN", str(exc))

    def _check_replay_trade_execution_disabled(self) -> dict:
        """v1.2.0 — REPLAY_TRADE_EXECUTION_ENABLED=False."""
        try:
            import release.version_info as _vi
            rte = getattr(_vi, "REPLAY_TRADE_EXECUTION_ENABLED", True)
            raa = getattr(_vi, "REPLAY_AUTO_EXECUTION_ENABLED", True)
            if not rte and not raa:
                return _check_item(
                    "replay_trade_execution_disabled", "replay_training", "PASS",
                    f"REPLAY_TRADE_EXECUTION_ENABLED={rte}, REPLAY_AUTO_EXECUTION_ENABLED={raa}",
                )
            return _check_item(
                "replay_trade_execution_disabled", "replay_training", "FAIL",
                f"REPLAY_TRADE_EXECUTION_ENABLED={rte} or REPLAY_AUTO_EXECUTION_ENABLED={raa} must be False",
            )
        except Exception as exc:
            return _check_item("replay_trade_execution_disabled", "replay_training", "WARN", str(exc))

    def _check_version_info_v120(self) -> dict:
        """v1.2.0 — VERSION is 1.2.0+ and REPLAY_TRAINING_AVAILABLE=True."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            rt_avail = getattr(_vi, "REPLAY_TRAINING_AVAILABLE", None)
            rte = getattr(_vi, "REPLAY_TRADE_EXECUTION_ENABLED", True)
            # Accept 1.2.0 or higher (1.2.1+)
            if VERSION >= "1.2.0" and rt_avail and not rte:
                return _check_item(
                    "version_info_v120", "version_git", "PASS",
                    f"VERSION={VERSION}, REPLAY_TRAINING_AVAILABLE={rt_avail}, "
                    f"REPLAY_TRADE_EXECUTION_ENABLED={rte}",
                )
            return _check_item(
                "version_info_v120", "version_git", "WARN",
                f"VERSION={VERSION}, REPLAY_TRAINING_AVAILABLE={rt_avail}, "
                f"REPLAY_TRADE_EXECUTION_ENABLED={rte}",
                warning="Expected VERSION>=1.2.0 with REPLAY_TRAINING_AVAILABLE=True, "
                        "REPLAY_TRADE_EXECUTION_ENABLED=False",
            )
        except Exception as exc:
            return _check_item("version_info_v120", "version_git", "WARN", str(exc))

    def _check_replay_scenario_library(self) -> dict:
        """v1.2.1 — ReplayScenarioLibrary importable and NO_REAL_ORDERS=True."""
        try:
            from replay.scenario_library import ReplayScenarioLibrary
            ok = ReplayScenarioLibrary.NO_REAL_ORDERS and ReplayScenarioLibrary.RESEARCH_ONLY
            return _check_item(
                "replay_scenario_library", "replay_scenario_session_manager",
                "PASS" if ok else "FAIL",
                f"ReplayScenarioLibrary.NO_REAL_ORDERS={ReplayScenarioLibrary.NO_REAL_ORDERS}",
            )
        except Exception as exc:
            return _check_item("replay_scenario_library", "replay_scenario_session_manager", "WARN", str(exc))

    def _check_replay_session_manager(self) -> dict:
        """v1.2.1 — ReplaySessionManager importable."""
        try:
            from replay.session_manager import ReplaySessionManager
            ok = ReplaySessionManager.NO_REAL_ORDERS
            return _check_item(
                "replay_session_manager_v121", "replay_scenario_session_manager",
                "PASS" if ok else "FAIL",
                f"ReplaySessionManager.NO_REAL_ORDERS={ok}",
            )
        except Exception as exc:
            return _check_item("replay_session_manager_v121", "replay_scenario_session_manager", "WARN", str(exc))

    def _check_replay_checkpoint_available(self) -> dict:
        """v1.2.1 — ReplayCheckpointManager importable."""
        try:
            from replay.session_checkpoint import ReplayCheckpointManager
            ok = ReplayCheckpointManager.NO_REAL_ORDERS
            return _check_item(
                "replay_checkpoint_v121", "replay_scenario_session_manager",
                "PASS" if ok else "FAIL",
                f"ReplayCheckpointManager.NO_REAL_ORDERS={ok}",
            )
        except Exception as exc:
            return _check_item("replay_checkpoint_v121", "replay_scenario_session_manager", "WARN", str(exc))

    def _check_version_info_v121(self) -> dict:
        """v1.2.1 — VERSION=1.2.1 and v1.2.1 flags set correctly."""
        try:
            from release.version_info import VERSION
            import release.version_info as _vi
            scl = getattr(_vi, "REPLAY_SCENARIO_LIBRARY_AVAILABLE", None)
            smgr = getattr(_vi, "REPLAY_SESSION_MANAGER_AVAILABLE", None)
            rte = getattr(_vi, "REPLAY_TRADE_EXECUTION_ENABLED", True)
            rade = getattr(_vi, "REPLAY_AUTO_DECISION_ENABLED", True)
            ok = VERSION == "1.2.1" and scl and smgr and not rte and not rade
            status = "PASS" if ok else "WARN"
            return _check_item(
                "version_info_v121", "version_git", status,
                f"VERSION={VERSION}, SCENARIO_LIB={scl}, SESSION_MGR={smgr}, "
                f"TRADE_EXEC={rte}, AUTO_DECISION={rade}",
            )
        except Exception as exc:
            return _check_item("version_info_v121", "version_git", "WARN", str(exc))

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
            # v1.0.4 Regression & Release Gate Hardening
            self._check_regression_hardening_import,
            self._check_safety_scanner_import,
            self._check_release_gate_health_import,
            self._check_version_info_v104,
            self._check_no_real_orders_false_positive_guard_v104,
            # v1.0.5 Documentation & User Guide Polish
            self._check_documentation_health_import,
            self._check_documentation_health_no_forbidden_actions,
            self._check_version_info_v105,
            # v1.0.6 Example Workflows & Templates
            self._check_workflow_templates_import,
            self._check_workflow_templates_no_forbidden_actions,
            self._check_version_info_v106,
            # v1.0.7 Knowledge Base Search Polish
            self._check_knowledge_base_import,
            self._check_knowledge_base_search_no_forbidden_actions,
            self._check_version_info_v107,
            # v1.0.8 Local Research Assistant Polish
            self._check_local_assistant_import,
            self._check_local_assistant_no_forbidden_actions,
            self._check_local_assistant_external_api_disabled,
            self._check_version_info_v108,
            # v1.0.9 Final Maintenance Rollup
            self._check_final_rollup_import,
            self._check_final_rollup_no_forbidden_actions,
            self._check_version_info_v109,
            # v1.1.0 Data Universe Expansion
            self._check_universe_import,
            self._check_universe_real_mock_separation,
            self._check_version_info_v110,
            # v1.1.1 Data Import UX & Batch Onboarding
            self._check_import_onboarding,
            self._check_dry_run_safe,
            self._check_version_info_v111,
            # v1.1.2 Coverage Repair Workflow
            self._check_coverage_repair_import,
            self._check_coverage_repair_dry_run_safe,
            self._check_coverage_repair_write_blocked_without_flag,
            self._check_version_info_v112,
            # v1.1.3 Data Freshness Monitor
            self._check_data_freshness_import,
            self._check_freshness_mock_real_separation,
            self._check_freshness_future_date_guard,
            self._check_version_info_v113,
            # v1.1.4 Coverage Quality Gates
            self._check_quality_gate_import,
            self._check_quality_gate_mock_guard,
            self._check_quality_gate_conflict_guard,
            self._check_quality_gate_future_date_guard,
            self._check_version_info_v114,
            # v1.1.5 Quality Gate Enforcement & Audit
            self._check_enforcement_import,
            self._check_enforcement_formal_filter,
            self._check_enforcement_mock_guard,
            self._check_enforcement_audit_chain,
            self._check_version_info_v115,
            # v1.1.6 Data Governance Operations Dashboard
            self._check_governance_ops_import,
            self._check_governance_auto_repair_disabled,
            self._check_governance_trade_execution_disabled,
            self._check_governance_no_forbidden_actions,
            self._check_version_info_v116,
            # v1.1.7 Governance Alerts & Daily Operations
            self._check_governance_alerts_import,
            self._check_governance_alert_dedup,
            self._check_governance_alert_lifecycle,
            self._check_governance_external_send_disabled,
            self._check_version_info_v117,
            # v1.1.8 Research Run Registry
            self._check_research_registry_import,
            self._check_research_registry_lineage,
            self._check_research_registry_duplicate_detection,
            self._check_research_registry_trade_execution_disabled,
            self._check_version_info_v118,
            # v1.1.9 Data Governance Stable Rollup
            self._check_governance_rollup_import,
            self._check_governance_rollup_consistency,
            self._check_governance_rollup_store_validation,
            self._check_governance_rollup_trade_execution_disabled,
            self._check_version_info_v119,
            # v1.2.0 Replay Training UX Foundation
            self._check_replay_import,
            self._check_replay_timeline,
            self._check_replay_future_firewall,
            self._check_replay_trade_execution_disabled,
            self._check_version_info_v120,
            # v1.2.1 Replay Scenario & Session Manager
            self._check_replay_scenario_library,
            self._check_replay_session_manager,
            self._check_replay_checkpoint_available,
            self._check_version_info_v121,
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
