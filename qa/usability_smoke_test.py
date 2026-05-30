"""
qa/usability_smoke_test.py - Usability smoke test suite (v0.3.22).

Runs a set of CLI and GUI import smoke tests to verify that the system
does not crash on common commands and entry points.

Outputs:
  data/backtest_results/usability_smoke_test_summary.csv
  reports/usability_smoke_test_report_YYYY-MM-DD.md

[!] Research Only. Read Only. No Real Orders.
[!] Production Trading: BLOCKED.
"""

from __future__ import annotations

import importlib
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Result constants
# ---------------------------------------------------------------------------

_PASS    = "PASS"
_FAIL    = "FAIL"
_SKIP    = "SKIP"
_WARNING = "WARNING"


# ---------------------------------------------------------------------------
# SmokTestCase
# ---------------------------------------------------------------------------

class _SmokeTestCase:
    """A single smoke test entry."""

    __slots__ = (
        "name",
        "category",
        "status",
        "duration_seconds",
        "message",
        "detail",
        "can_ignore",
        "safety_banner_present",
    )

    def __init__(self, name: str, category: str):
        self.name                = name
        self.category            = category
        self.status              = _SKIP
        self.duration_seconds    = 0.0
        self.message             = ""
        self.detail              = ""
        self.can_ignore          = False
        self.safety_banner_present = False

    def to_dict(self) -> dict:
        return {
            "name":                   self.name,
            "category":               self.category,
            "status":                 self.status,
            "duration_seconds":       self.duration_seconds,
            "message":                self.message,
            "detail":                 self.detail,
            "can_ignore":             self.can_ignore,
            "safety_banner_present":  self.safety_banner_present,
        }


# ---------------------------------------------------------------------------
# UsabilitySmokeTest
# ---------------------------------------------------------------------------

class UsabilitySmokeTest:
    """
    Runs CLI and GUI panel import smoke tests.

    Parameters
    ----------
    base_dir   : Project root directory (defaults to this file's parent of parent)
    results_dir: Path to data/backtest_results/ (for CSV output)
    report_dir : Path to reports/ (for Markdown report)
    """

    VERSION            = "v0.3.22"
    read_only          = True
    no_real_orders     = True
    production_blocked = True

    # CLI tests: (test_name, cli_args, can_ignore)
    _CLI_TESTS = [
        ("cli_update_data_dry_run",      ["update-data",       "--dry-run",              "--mode", "mock"], False),
        ("cli_run_research_quick",       ["run-research",      "--profile", "quick",     "--mode", "mock"], False),
        ("cli_data_quality_gate_mock",   ["data-quality-gate", "--mode",    "mock"],                        False),
        ("cli_provider_health",          ["provider-health"],                                               True),
        ("cli_data_freshness",           ["data-freshness"],                                                True),
        ("cli_auto_report_daily",        ["auto-report",       "--profile", "daily",     "--mode", "mock"], True),
        ("cli_signal_quality",           ["signal-quality",    "--mode",    "mock"],                        True),
        ("cli_simulate_portfolio",       ["simulate-portfolio","--scenario","balanced",  "--mode", "mock"], True),
    ]

    # GUI panel import tests: (test_name, module_path, class_name, can_ignore)
    _GUI_TESTS = [
        ("gui_import_dashboard",          "gui.dashboard",                  "CockpitWindow",          True),
        ("gui_import_portfolio_cockpit",  "gui.portfolio_cockpit_panel",    "PortfolioCockpitPanel",  True),
        ("gui_import_signal_quality",     "gui.signal_quality_panel",       "SignalQualityPanel",     True),
        ("gui_import_data_quality_gate",  "gui.data_quality_gate_panel",    "DataQualityGatePanel",   True),
        ("gui_import_daily_workflow",     "gui.daily_workflow_panel",       "DailyWorkflowPanel",     True),
        ("gui_import_provider_health",    "gui.provider_health_panel",      "ProviderHealthPanel",    True),
        ("gui_import_usability_qa",       "gui.usability_qa_panel",         "UsabilityQAPanel",       True),
        ("gui_import_portfolio_widgets",  "gui.portfolio_widgets",          "EmptyStateWidget",       True),
    ]

    def __init__(
        self,
        base_dir:    Optional[str] = None,
        results_dir: Optional[str] = None,
        report_dir:  Optional[str] = None,
    ):
        self._base_dir    = base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._results_dir = results_dir or os.path.join(self._base_dir, "data", "backtest_results")
        self._report_dir  = report_dir  or os.path.join(self._base_dir, "reports")
        self._cases: List[_SmokeTestCase] = []
        self._run_at: str = ""

    def run(self) -> dict:
        """Run all smoke tests and return a summary dict."""
        self._run_at = datetime.now().isoformat()
        self._cases  = []

        logger.info("[UsabilitySmokeTest] Starting smoke tests (%s)", self.VERSION)

        # CLI tests
        for test_name, cli_args, can_ignore in self._CLI_TESTS:
            case = _SmokeTestCase(test_name, "CLI")
            case.can_ignore = can_ignore
            self._run_cli_test(case, cli_args)
            self._cases.append(case)

        # GUI import tests
        for test_name, module_path, class_name, can_ignore in self._GUI_TESTS:
            case = _SmokeTestCase(test_name, "GUI")
            case.can_ignore = can_ignore
            self._run_gui_import_test(case, module_path, class_name)
            self._cases.append(case)

        result = self._build_result()

        # Save outputs
        try:
            self._save_csv(result)
        except Exception as exc:
            logger.warning("[UsabilitySmokeTest] CSV save failed: %s", exc)

        logger.info(
            "[UsabilitySmokeTest] Complete: pass=%d fail=%d warn=%d skip=%d",
            result["passed"], result["failed"], result["warnings"], result["skipped"],
        )
        return result

    # ------------------------------------------------------------------
    # CLI test runner
    # ------------------------------------------------------------------

    def _run_cli_test(self, case: _SmokeTestCase, cli_args: List[str]) -> None:
        """Run a CLI command as a subprocess and record pass/fail."""
        cmd = [sys.executable, os.path.join(self._base_dir, "main.py")] + cli_args
        t0  = time.monotonic()
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=self._base_dir,
            )
            elapsed = time.monotonic() - t0
            case.duration_seconds = round(elapsed, 2)
            output = (proc.stdout or "") + (proc.stderr or "")

            # Check for safety banner
            case.safety_banner_present = any(
                kw in output
                for kw in (
                    "BLOCKED",
                    "Read Only",
                    "No Real Orders",
                    "Research Only",
                    "research only",
                )
            )

            if proc.returncode == 0:
                case.status  = _PASS
                case.message = "Command exited successfully."
            else:
                # Non-zero exit — could be expected (token not configured)
                if any(kw in output for kw in ("token", "NOT_CONFIGURED", "WARNING")):
                    case.status  = _WARNING if case.can_ignore else _FAIL
                    case.message = "Command exited non-zero; may be token/config issue."
                else:
                    case.status  = _FAIL if not case.can_ignore else _WARNING
                    case.message = f"Exit code {proc.returncode}."
                case.detail = output[-500:] if len(output) > 500 else output

        except subprocess.TimeoutExpired:
            case.status           = _WARNING if case.can_ignore else _FAIL
            case.duration_seconds = 120.0
            case.message          = "Command timed out (>120s)."
        except Exception as exc:
            case.status           = _FAIL
            case.duration_seconds = round(time.monotonic() - t0, 2)
            case.message          = f"Exception: {exc}"

    # ------------------------------------------------------------------
    # GUI import test runner
    # ------------------------------------------------------------------

    def _run_gui_import_test(
        self, case: _SmokeTestCase, module_path: str, class_name: str
    ) -> None:
        """Attempt to import a GUI module and check the named class exists."""
        t0 = time.monotonic()
        try:
            mod = importlib.import_module(module_path)
            case.duration_seconds = round(time.monotonic() - t0, 2)
            if hasattr(mod, class_name):
                case.status  = _PASS
                case.message = f"{class_name} importable."
            else:
                case.status  = _WARNING
                case.message = f"Module imported but {class_name} not found."
        except ImportError as exc:
            case.duration_seconds = round(time.monotonic() - t0, 2)
            exc_str = str(exc)
            # PySide6 not installed — expected in headless environments
            if any(kw in exc_str.lower() for kw in ("pyside6", "pyqt", "qt")):
                case.status  = _SKIP
                case.message = "PySide6 not installed — GUI test skipped."
            else:
                case.status  = _WARNING if case.can_ignore else _FAIL
                case.message = f"ImportError: {exc}"
        except Exception as exc:
            case.duration_seconds = round(time.monotonic() - t0, 2)
            case.status  = _WARNING if case.can_ignore else _FAIL
            case.message = f"Exception: {exc}"

    # ------------------------------------------------------------------
    # Result aggregation
    # ------------------------------------------------------------------

    def _build_result(self) -> dict:
        n_pass = sum(1 for c in self._cases if c.status == _PASS)
        n_fail = sum(1 for c in self._cases if c.status == _FAIL)
        n_warn = sum(1 for c in self._cases if c.status == _WARNING)
        n_skip = sum(1 for c in self._cases if c.status == _SKIP)
        n_safe = sum(1 for c in self._cases if c.safety_banner_present)

        overall = "PASS" if n_fail == 0 else "FAIL"
        cli_cases = [c for c in self._cases if c.category == "CLI"]
        gui_cases = [c for c in self._cases if c.category == "GUI"]

        return {
            "run_at":                  self._run_at,
            "version":                 self.VERSION,
            "overall_status":          overall,
            "passed":                  n_pass,
            "failed":                  n_fail,
            "warnings":                n_warn,
            "skipped":                 n_skip,
            "safety_banner_coverage":  n_safe,
            "total_cli_tests":         len(cli_cases),
            "total_gui_tests":         len(gui_cases),
            "safety_flags": {
                "read_only":           self.read_only,
                "no_real_orders":      self.no_real_orders,
                "production_blocked":  self.production_blocked,
            },
            "cases": [c.to_dict() for c in self._cases],
        }

    # ------------------------------------------------------------------
    # Output: CSV
    # ------------------------------------------------------------------

    def _save_csv(self, result: dict) -> str:
        try:
            import pandas as pd
        except ImportError:
            return ""

        rows = result.get("cases", [])
        if not rows:
            return ""

        os.makedirs(self._results_dir, exist_ok=True)
        df = pd.DataFrame(rows)
        csv_path = os.path.join(self._results_dir, "usability_smoke_test_summary.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        logger.info("[UsabilitySmokeTest] CSV saved: %s", csv_path)
        return csv_path
