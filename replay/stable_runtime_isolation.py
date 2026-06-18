"""
replay/stable_runtime_isolation.py — ReplayStableRuntimeIsolation for v1.2.9.

Runtime isolation checks: .gitignore coverage, sys.path safety.
Lightweight read-based checks only. No real orders.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
import os
import sys
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Patterns that should be in .gitignore for replay runtime isolation
_REQUIRED_GITIGNORE_PATTERNS = [
    "data/replay_sessions/",
    "data/replay_scenarios/",
    "data/replay_journal/",
    "data/replay_scoring/",
    "data/replay_strategy/",
    "data/replay_timeframes/",
    "data/replay_review/",
    "data/replay_challenges/",
    "data/replay_registry/",
    "reports/",
    "*.csv",
    "*.db",
    "*.xlsx",
    "logs/",
    "cache/",
]


class ReplayStableRuntimeIsolation:
    """
    Runtime isolation checks for v1.2.9 stable rollup.

    Checks that .gitignore covers all replay runtime data directories.
    Checks that sys.path doesn't leak absolute user paths into module names.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, project_root: str = "") -> None:
        if project_root:
            self._root = project_root
        else:
            # Derive from this file's location (replay/ → project root)
            self._root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def check_all(self) -> Dict[str, Tuple[str, str]]:
        """Run all isolation checks. Returns {check_id: (status, message)}."""
        results: Dict[str, Tuple[str, str]] = {}
        results["gitignore_exists"]              = self._check_gitignore_exists()
        results["gitignore_replay_sessions"]     = self._check_pattern("data/replay_sessions/", "replay sessions store")
        results["gitignore_replay_scenarios"]    = self._check_pattern("data/replay_scenarios/", "replay scenarios store")
        results["gitignore_replay_journal"]      = self._check_pattern("data/replay_journal/", "journal store")
        results["gitignore_replay_scoring"]      = self._check_pattern("data/replay_scoring/", "scoring store")
        results["gitignore_replay_strategy"]     = self._check_pattern("data/replay_strategy/", "strategy store")
        results["gitignore_replay_timeframes"]   = self._check_pattern("data/replay_timeframes/", "timeframe store")
        results["gitignore_replay_review"]       = self._check_pattern("data/replay_review/", "review store")
        results["gitignore_replay_challenges"]   = self._check_pattern("data/replay_challenges/", "challenge store")
        results["gitignore_replay_registry"]     = self._check_pattern("data/replay_registry/", "registry store")
        results["gitignore_reports"]             = self._check_pattern("reports/", "reports dir")
        results["gitignore_csv"]                 = self._check_pattern("*.csv", "csv files")
        results["gitignore_db"]                  = self._check_pattern("*.db", "db files")
        results["gitignore_xlsx"]                = self._check_pattern("*.xlsx", "xlsx files")
        results["gitignore_logs"]                = self._check_pattern("logs/", "logs dir")
        results["sys_path_no_user_leak"]         = self._check_sys_path_no_user_leak()
        return results

    def _read_gitignore(self) -> List[str]:
        """Read .gitignore lines. Returns empty list if not found."""
        gi_path = os.path.join(self._root, ".gitignore")
        try:
            with open(gi_path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines()]
        except Exception:
            return []

    def _check_gitignore_exists(self) -> Tuple[str, str]:
        gi_path = os.path.join(self._root, ".gitignore")
        if os.path.isfile(gi_path):
            return ("PASS", ".gitignore exists")
        return ("FAIL", f".gitignore not found at {gi_path}")

    def _check_pattern(self, pattern: str, description: str) -> Tuple[str, str]:
        lines = self._read_gitignore()
        if not lines:
            return ("WARN", ".gitignore not readable — cannot verify pattern")
        # Check if any line matches the pattern (exact or close)
        for line in lines:
            if line.startswith("#") or not line:
                continue
            if pattern in line or line.rstrip("/") == pattern.rstrip("/"):
                return ("PASS", f".gitignore covers {description} ({pattern!r} found)")
        # Broader check: *.csv, *.db etc might cover via wildcard
        if pattern.startswith("*."):
            ext = pattern[1:]  # e.g. .csv
            for line in lines:
                if ext in line:
                    return ("PASS", f".gitignore covers {description} ({ext!r} found in line)")
        return ("WARN", f".gitignore may not cover {description} ({pattern!r} not found)")

    def _check_sys_path_no_user_leak(self) -> Tuple[str, str]:
        """Check sys.path doesn't leak absolute user-specific paths into module names."""
        try:
            suspicious = []
            for path in sys.path:
                if not path:
                    continue
                # Flag paths that look like absolute user home directories
                norm = path.replace("\\", "/").lower()
                if "/users/" in norm and "/site-packages" not in norm and "tw_quant_cockpit" not in norm:
                    suspicious.append(path)
            if suspicious:
                return ("WARN", f"sys.path contains user-specific paths: {suspicious[:3]}")
            return ("PASS", "sys.path has no suspicious user-specific absolute paths")
        except Exception as exc:
            return ("WARN", f"sys.path check error: {exc}")
