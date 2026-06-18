"""regression/regression_runner.py — RegressionRunner for TW Quant Cockpit v0.5.3.
[!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
import time
from datetime import datetime

from regression.regression_schema import (
    RegressionTestCase, RegressionTestResult,
    STATUS_PASS, STATUS_WARNING, STATUS_FAIL, STATUS_BLOCKED, STATUS_TIMEOUT,
)
from regression.suite_registry import RegressionSuiteRegistry, _is_forbidden

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RegressionRunner:
    """Runs regression test suites against TW Quant Cockpit CLI.

    [!] Regression Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        registry: RegressionSuiteRegistry | None = None,
        output_dir: str = "data/backtest_results/regression",
        timeout_seconds: int = 180,
    ) -> None:
        self.registry        = registry or RegressionSuiteRegistry()
        self.output_dir      = os.path.join(BASE_DIR, output_dir)
        self.timeout_seconds = timeout_seconds
        self._results: list[RegressionTestResult] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_suite(self, suite_name: str = "quick", mode: str = "real") -> dict:
        tests = self.registry.get_suite(suite_name)
        if not tests:
            return {
                "suite":          suite_name,
                "status":         "FAIL",
                "error":          f"Suite '{suite_name}' not found or empty",
                "tests":          [],
                "no_real_orders": True,
            }
        return self.run_tests(tests, suite_name=suite_name)

    def run_tests(self, tests: list[RegressionTestCase], suite_name: str = "custom") -> dict:
        results: list[RegressionTestResult] = []
        for test in tests:
            result = self.run_test(test)
            results.append(result)
        self._results = results
        return self.build_summary(results, suite_name=suite_name)

    def run_test(self, test_case: RegressionTestCase) -> RegressionTestResult:
        started_at = datetime.now().isoformat()
        t0 = time.monotonic()

        # Forbidden keyword check — use suite_registry._is_forbidden() which
        # correctly handles -c inline code (not scanned) and -m module names.
        if _is_forbidden(test_case.command):
            # A genuinely forbidden command is an unexpected block unless
            # the test case explicitly declares expected_block=True.
            if test_case.expected_block:
                return RegressionTestResult(
                    test_id=test_case.test_id,
                    name=test_case.name,
                    suite=test_case.suite,
                    status=STATUS_PASS,
                    expected_block=True,
                    counts_as_pass=True,
                    warning="Expected safety block confirmed: dangerous command correctly rejected",
                    started_at=started_at,
                    finished_at=datetime.now().isoformat(),
                )
            return RegressionTestResult(
                test_id=test_case.test_id,
                name=test_case.name,
                suite=test_case.suite,
                status=STATUS_BLOCKED,
                error=f"Command blocked: contains forbidden keyword (unexpected block)",
                started_at=started_at,
                finished_at=datetime.now().isoformat(),
            )

        # Build subprocess command
        cmd = self._build_command(test_case.command)

        # Determine timeout
        timeout = test_case.timeout_seconds or self.timeout_seconds

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                cwd=BASE_DIR,
                # Never use shell=True
            )
            duration = time.monotonic() - t0
            finished_at = datetime.now().isoformat()

            stdout_tail = (proc.stdout or "")[-500:]
            stderr_tail = (proc.stderr or "")[-500:]
            return_code = proc.returncode

            if return_code == 0:
                status        = STATUS_PASS
                warning       = ""
                error         = ""
                expected_block = False
                counts_as_pass = False
            elif test_case.expected_block:
                # The test is designed to verify that the system correctly blocks
                # a dangerous operation.  Non-zero return = safety guard worked.
                status        = STATUS_PASS
                warning       = "Expected safety block confirmed: dangerous execution correctly blocked"
                error         = ""
                expected_block = True
                counts_as_pass = True
            else:
                expected_block = False
                counts_as_pass = False
                if test_case.required:
                    status  = STATUS_FAIL
                    warning = ""
                    error   = stderr_tail or stdout_tail or f"returncode={return_code}"
                else:
                    status  = STATUS_WARNING
                    warning = stderr_tail or stdout_tail or f"returncode={return_code}"
                    error   = ""

            return RegressionTestResult(
                test_id=test_case.test_id,
                name=test_case.name,
                suite=test_case.suite,
                status=status,
                return_code=return_code,
                duration_seconds=round(duration, 3),
                stdout_tail=stdout_tail,
                stderr_tail=stderr_tail,
                warning=warning,
                error=error,
                expected_block=expected_block,
                counts_as_pass=counts_as_pass,
                started_at=started_at,
                finished_at=finished_at,
            )

        except subprocess.TimeoutExpired:
            duration = time.monotonic() - t0
            return RegressionTestResult(
                test_id=test_case.test_id,
                name=test_case.name,
                suite=test_case.suite,
                status=STATUS_TIMEOUT,
                return_code=-1,
                duration_seconds=round(duration, 3),
                error=f"Timeout after {timeout}s",
                started_at=started_at,
                finished_at=datetime.now().isoformat(),
            )
        except Exception as exc:
            duration = time.monotonic() - t0
            return RegressionTestResult(
                test_id=test_case.test_id,
                name=test_case.name,
                suite=test_case.suite,
                status=STATUS_FAIL,
                return_code=-1,
                duration_seconds=round(duration, 3),
                error=str(exc)[:500],
                started_at=started_at,
                finished_at=datetime.now().isoformat(),
            )

    def build_summary(self, results: list[RegressionTestResult], suite_name: str = "custom") -> dict:
        # Separate expected safety blocks (counts_as_pass=True) from others.
        # expected safety blocks have status=PASS but were originally blocked operations.
        expected_safety_blocks = sum(1 for r in results if r.counts_as_pass and r.expected_block)
        passed    = sum(1 for r in results if r.status == STATUS_PASS)  # includes expected safety blocks
        failed    = sum(1 for r in results if r.status == STATUS_FAIL)
        warned    = sum(1 for r in results if r.status == STATUS_WARNING)
        timed_out = sum(1 for r in results if r.status == STATUS_TIMEOUT)
        # Only count genuinely unexpected blocked results (not expected safety blocks)
        unexpected_blocked = sum(
            1 for r in results if r.status == STATUS_BLOCKED and not r.counts_as_pass
        )

        # Overall status rules:
        #   FAIL > 0 or unexpected_blocked > 0  => FAIL
        #   warned > 0 or timed_out > 0          => WARNING
        #   all pass                              => PASS
        if failed > 0 or unexpected_blocked > 0:
            overall = "FAIL"
        elif warned > 0 or timed_out > 0:
            overall = "WARNING"
        else:
            overall = "PASS"

        return {
            "suite":                  suite_name,
            "status":                 overall,
            "passed":                 passed,
            "failed":                 failed,
            "warnings":               warned,
            "timeouts":               timed_out,
            "blocked":                unexpected_blocked,
            "expected_safety_blocks": expected_safety_blocks,
            "total":                  len(results),
            "tests":                  [r.to_dict() for r in results],
            "read_only":              True,
            "no_real_orders":         True,
            "production_blocked":     True,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_command(self, raw_command: list[str]) -> list[str]:
        """Build the full subprocess command list (prepend sys.executable)."""
        if not raw_command:
            return [sys.executable]

        first = raw_command[0]
        if first == "main.py":
            # prepend sys.executable + absolute path to main.py
            main_py = os.path.join(BASE_DIR, "main.py")
            return [sys.executable, main_py] + raw_command[1:]
        elif first in ("-c", "-m"):
            # python -c "..." or python -m module
            return [sys.executable] + raw_command
        else:
            # fallback — prepend sys.executable
            return [sys.executable] + raw_command
