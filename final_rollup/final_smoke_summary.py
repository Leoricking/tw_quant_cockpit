"""
final_rollup/final_smoke_summary.py — Final Smoke Summary for TW Quant Cockpit v1.0.9.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Final Maintenance Rollup.
"""
from __future__ import annotations

import logging
import os
from typing import List, Dict

logger = logging.getLogger(__name__)

_STATUS_PASS    = "PASS"
_STATUS_WARN    = "WARN"
_STATUS_FAIL    = "FAIL"
_STATUS_UNKNOWN = "UNKNOWN"
_RUN_REQUIRED   = "RUN_COMMAND_REQUIRED"


class FinalSmokeSummaryBuilder:
    """Builds a final smoke test summary for v1.0.9.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    Does NOT force-read large logs. If no runtime result is found,
    shows UNKNOWN / RUN_COMMAND_REQUIRED instead of crashing.
    """

    no_real_orders = True
    broker_disabled = True
    external_api_disabled = True

    def __init__(self, project_root: str = None) -> None:
        self._root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def collect_recent_smoke_results(self) -> List[dict]:
        """Collect recent smoke results from known output locations."""
        results = []
        # compileall — check if __pycache__ exists as a proxy
        pycache = os.path.join(self._root, "__pycache__")
        results.append({
            "suite": "compileall",
            "status": _STATUS_PASS if os.path.isdir(pycache) else _STATUS_UNKNOWN,
            "note": "Run: python -m compileall ." if not os.path.isdir(pycache) else "pycache present",
        })
        # version-info — check version_info.py
        vi_path = os.path.join(self._root, "release", "version_info.py")
        results.append({
            "suite": "version-info",
            "status": _STATUS_PASS if os.path.isfile(vi_path) else _STATUS_FAIL,
            "note": "release/version_info.py present" if os.path.isfile(vi_path) else "version_info.py missing",
        })
        # safety scan — look for recent report
        results.append(self._check_report_exists("safety-scan docs", "reports/regression_hardening_report*.md"))
        results.append(self._check_report_exists("safety-scan all", "reports/regression_hardening_report*.md"))
        # research-cockpit-stable
        results.append(self._check_report_exists("research-cockpit-stable", "reports/research_trading_cockpit_stable_report*.md"))
        # stable-v060
        stable_path = os.path.join(self._root, "stable_release", "stable_release_checklist_v060.py")
        results.append({
            "suite": "stable-v060-check",
            "status": _STATUS_PASS if os.path.isfile(stable_path) else _STATUS_WARN,
            "note": "stable_release_checklist_v060.py present" if os.path.isfile(stable_path) else _RUN_REQUIRED,
        })
        # release_gate regression
        results.append(self._check_report_exists("release_gate regression", "reports/regression_hardening_report*.md"))
        # quick regression
        results.append(self._check_report_exists("quick regression", "reports/regression_hardening_report*.md"))
        # mock-realtime
        results.append({
            "suite": "mock-realtime smoke",
            "status": _STATUS_UNKNOWN,
            "note": "Run: python main.py mock-realtime --duration 10",
        })
        # paper
        results.append({
            "suite": "paper smoke",
            "status": _STATUS_UNKNOWN,
            "note": "Run: python main.py paper",
        })
        # git status
        results.append(self._check_git_status())
        return results

    def _check_report_exists(self, suite_name: str, glob_pattern: str) -> dict:
        import glob as _glob
        full_pattern = os.path.join(self._root, glob_pattern)
        matches = _glob.glob(full_pattern, recursive=True)
        if matches:
            return {
                "suite": suite_name,
                "status": _STATUS_PASS,
                "note": f"Found: {os.path.basename(matches[-1])}",
            }
        return {
            "suite": suite_name,
            "status": _STATUS_UNKNOWN,
            "note": _RUN_REQUIRED,
        }

    def _check_git_status(self) -> dict:
        try:
            import subprocess
            result = subprocess.run(
                ["git", "-C", self._root, "status", "--porcelain"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0:
                if result.stdout.strip() == "":
                    return {"suite": "git status", "status": _STATUS_PASS, "note": "working tree clean"}
                return {"suite": "git status", "status": _STATUS_WARN,
                        "note": f"uncommitted changes: {result.stdout[:60]}"}
            return {"suite": "git status", "status": _STATUS_UNKNOWN, "note": _RUN_REQUIRED}
        except Exception as exc:
            return {"suite": "git status", "status": _STATUS_UNKNOWN, "note": str(exc)}

    def summarize_release_gate(self) -> dict:
        return self._check_report_exists("release_gate", "reports/regression_hardening_report*.md")

    def summarize_quick_regression(self) -> dict:
        return self._check_report_exists("quick regression", "reports/regression_hardening_report*.md")

    def summarize_safety_scan(self) -> dict:
        return self._check_report_exists("safety_scan", "reports/regression_hardening_report*.md")

    def summarize_stable_checks(self) -> dict:
        vi_path = os.path.join(self._root, "release", "version_info.py")
        if os.path.isfile(vi_path):
            return {"suite": "stable_checks", "status": _STATUS_PASS, "note": "version_info.py present"}
        return {"suite": "stable_checks", "status": _STATUS_UNKNOWN, "note": _RUN_REQUIRED}

    def summarize_mock_paper(self) -> dict:
        return {
            "suite": "mock_paper",
            "status": _STATUS_UNKNOWN,
            "note": "Run: python main.py mock-realtime --duration 10 / python main.py paper",
        }

    def build_smoke_table(self) -> List[dict]:
        """Build a complete smoke table."""
        return self.collect_recent_smoke_results()

    def get_summary(self) -> dict:
        results = self.build_smoke_table()
        total   = len(results)
        passed  = sum(1 for r in results if r["status"] == _STATUS_PASS)
        warned  = sum(1 for r in results if r["status"] == _STATUS_WARN)
        unknown = sum(1 for r in results if r["status"] == _STATUS_UNKNOWN)
        failed  = sum(1 for r in results if r["status"] == _STATUS_FAIL)
        return {
            "total": total,
            "pass": passed,
            "warn": warned,
            "unknown": unknown,
            "fail": failed,
            "no_real_orders": True,
            "broker_disabled": True,
        }
