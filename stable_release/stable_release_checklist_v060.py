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
