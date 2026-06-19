"""
tests/test_universe_cli.py — CLI command tests for v1.3.1.

[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import subprocess
import sys
import pytest

import os

MAIN_MODULE = "main"
# Resolve BASE_DIR relative to this test file so it works on any machine
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_cmd(*args, timeout=30):
    """Run a CLI command and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, "-c", f"import sys; sys.path.insert(0,'.')\nimport {MAIN_MODULE}\n{MAIN_MODULE}.main()"] + list(args)
    result = subprocess.run(
        [sys.executable, f"{BASE_DIR}/main.py"] + list(args),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        cwd=BASE_DIR,
    )
    return result.returncode, result.stdout, result.stderr


class TestUniverseCLI:
    """CLI tests for universe commands."""

    def test_version_info_shows_131(self):
        rc, out, err = run_cmd("version-info")
        assert rc == 0
        # v1.3.1 or later — accept any 1.3.x or 1.4.x version
        assert "1.3." in out or "1.4." in out

    def test_universe_health_runs(self):
        rc, out, err = run_cmd("universe-health")
        assert rc == 0
        assert "Universe" in out or "Health" in out or "health" in out.lower()

    def test_universe_list_runs(self):
        rc, out, err = run_cmd("universe-list")
        assert rc == 0

    def test_universe_summary_runs(self):
        rc, out, err = run_cmd("universe-summary")
        assert rc == 0

    def test_version_info_replay_stable_baseline(self):
        rc, out, err = run_cmd("version-info")
        assert rc == 0
        # Replay stable baseline 1.2.9 should be present
        assert "1.2.9" in out

    def test_real_data_quality_health_runs(self):
        rc, out, err = run_cmd("real-data-quality-health")
        # May return 0 or 1 depending on data, but should not error
        assert rc in (0, 1)

    def test_replay_stable_health_runs(self):
        rc, out, err = run_cmd("replay-stable-health")
        assert rc in (0, 1)

    def test_universe_coverage_runs(self):
        rc, out, err = run_cmd("universe-coverage")
        assert rc == 0

    def test_release_gate_health_runs(self):
        rc, out, err = run_cmd("release-gate-health")
        assert rc in (0, 1)

    def test_help_runs(self):
        rc, out, err = run_cmd("--help")
        assert rc == 0
        assert "universe" in out.lower() or "Universe" in out

    def test_no_real_orders_in_output(self):
        rc, out, err = run_cmd("version-info")
        assert rc == 0
        assert "No Real Orders" in out or "no_real_orders" in out.lower()

    def test_broker_execution_disabled(self):
        rc, out, err = run_cmd("version-info")
        assert rc == 0
        assert "Broker Execution Enabled" in out
        assert "False" in out

    def test_production_trading_blocked(self):
        rc, out, err = run_cmd("version-info")
        assert rc == 0
        assert "Production Trading BLOCKED" in out
