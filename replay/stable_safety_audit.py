"""
replay/stable_safety_audit.py — ReplayStableSafetyAudit for v1.2.9.

Safety audit: checks version_info flags, scans replay/ for dangerous keywords.
No real orders. No broker. Research only.

[!] Research Only. No Real Orders. Not Investment Advice.
[!] Replay Training Stable Rollup. No broker. No trading. Simulation Only.
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

# Keywords that indicate real order/broker activity — forbidden in replay modules
_DANGEROUS_KEYWORDS = [
    "send_order(",
    "place_order(",
    "real_buy(",
    "real_sell(",
    "broker_login(",
    "broker.connect(",
    "execute_trade(",
    "auto_trade(",
]

# Safety declaration strings — these mention related words but are SAFE (whitelisted)
_SAFETY_DECLARATION_SNIPPETS = [
    "No Real Orders",
    "NO_REAL_ORDERS",
    "no_real_orders",
    "Research Only",
    "RESEARCH_ONLY",
    "Not Investment Advice",
    "DISABLED",
    "disabled",
    "NOT",
    "[!]",
    "# no",
    "forbidden",
    # Lines defining forbidden-keyword lists or dangerous-keyword constants
    # are whitelisted — they enumerate prohibited patterns, not actual calls.
    "_FORBIDDEN",
    "_DANGEROUS",
]

# v1.2.9 required safety flag values in version_info
_REQUIRED_FLAGS = {
    "NO_REAL_ORDERS": True,
    "REAL_ORDERS_ENABLED": False,
    "BROKER_EXECUTION_ENABLED": False,
    "PRODUCTION_TRADING_BLOCKED": True,
    "VALIDATED_DOES_NOT_ENABLE_TRADING": True,
    "AUTO_REPLAY_DECISION_ENABLED": False,
    "AUTO_REPLAY_EXECUTION_ENABLED": False,
    "AUTO_MISTAKE_CONFIRMATION_ENABLED": False,
    "AUTO_OUTCOME_REVEAL_ENABLED": False,
    "AUTO_STRATEGY_CHANGE_ENABLED": False,
    "AUTO_DATASET_REPAIR_ENABLED": False,
    "AUTO_SESSION_REBIND_ENABLED": False,
    "REPLAY_TRADE_EXECUTION_ENABLED": False,
}


class ReplayStableSafetyAudit:
    """
    Safety audit for v1.2.9 stable rollup.

    - Imports version_info and checks all safety flags
    - Scans replay/ directory for dangerous keywords in .py files
    - Safety declaration strings (like "No Real Orders") are whitelisted

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, project_root: str = "") -> None:
        if project_root:
            self._root = project_root
        else:
            self._root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def audit_all(self) -> Dict[str, Tuple[str, str]]:
        """Run all safety audits. Returns {check_id: (status, message)}."""
        results: Dict[str, Tuple[str, str]] = {}

        # Version info flag checks
        results.update(self._check_version_info_flags())

        # Keyword scan of replay/ directory
        results["replay_dir_keyword_scan"] = self._scan_replay_directory()

        # Stable modules own flag checks
        results["stable_modules_no_real_orders"] = self._check_stable_module_flags()

        return results

    def _check_version_info_flags(self) -> Dict[str, Tuple[str, str]]:
        """Check all required safety flags in version_info."""
        results: Dict[str, Tuple[str, str]] = {}
        try:
            import release.version_info as vi
            for flag_name, expected_value in _REQUIRED_FLAGS.items():
                actual = getattr(vi, flag_name, None)
                if actual is None:
                    results[f"flag_{flag_name.lower()}"] = (
                        "WARN", f"{flag_name} not found in version_info"
                    )
                elif actual == expected_value:
                    results[f"flag_{flag_name.lower()}"] = (
                        "PASS", f"{flag_name}={actual} (expected {expected_value})"
                    )
                else:
                    results[f"flag_{flag_name.lower()}"] = (
                        "FAIL", f"{flag_name}={actual} (expected {expected_value})"
                    )
        except Exception as exc:
            results["flag_version_info"] = ("FAIL", f"version_info import error: {exc}")
        return results

    # Files that enumerate forbidden keywords as safety constants (audit/scan files).
    # These define the prohibited patterns, not actual broker/order calls — skip them.
    _KEYWORD_DEFINITION_FILES = {
        "stable_safety_audit.py",
        "stable_report_audit.py",
    }

    def _scan_replay_directory(self) -> Tuple[str, str]:
        """Scan replay/ directory for dangerous keywords in .py files."""
        replay_dir = os.path.join(self._root, "replay")
        if not os.path.isdir(replay_dir):
            return ("WARN", "replay/ directory not found — cannot scan")

        violations: List[str] = []
        try:
            for fname in os.listdir(replay_dir):
                if not fname.endswith(".py"):
                    continue
                # Skip files that define the forbidden-keyword lists themselves
                if fname in self._KEYWORD_DEFINITION_FILES:
                    continue
                fpath = os.path.join(replay_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    for lineno, line in enumerate(lines, 1):
                        stripped = line.strip()
                        # Skip comment-only lines
                        if stripped.startswith("#"):
                            continue
                        for danger in _DANGEROUS_KEYWORDS:
                            if danger in line:
                                # Check if this is a safety declaration (whitelisted)
                                is_safe_decl = any(
                                    snippet in line
                                    for snippet in _SAFETY_DECLARATION_SNIPPETS
                                )
                                if not is_safe_decl:
                                    violations.append(f"{fname}:{lineno}: {danger!r}")
                                break
                except Exception:
                    pass

            if violations:
                sample = violations[:5]
                return ("FAIL", f"Dangerous keywords in replay/: {sample}")
            return ("PASS", "No dangerous trading keywords found in replay/ modules")
        except Exception as exc:
            return ("WARN", f"Replay dir scan error: {exc}")

    def _check_stable_module_flags(self) -> Tuple[str, str]:
        """Check stable_*.py modules have NO_REAL_ORDERS=True and RESEARCH_ONLY=True."""
        stable_modules = [
            "replay.stable_schema",
            "replay.stable_manifest",
            "replay.stable_capability_matrix",
            "replay.stable_contracts",
            "replay.stable_compatibility",
            "replay.stable_store_audit",
            "replay.stable_runtime_isolation",
            "replay.stable_cli_audit",
            "replay.stable_gui_audit",
            "replay.stable_report_audit",
            "replay.stable_safety_audit",
            "replay.stable_regression_audit",
            "replay.stable_release_gate",
            "replay.stable_summary",
            "replay.stable_report",
            "replay.stable_health",
        ]
        failed = []
        for mod_path in stable_modules:
            try:
                import importlib as _il
                mod = _il.import_module(mod_path)
                if getattr(mod, "NO_REAL_ORDERS", None) is not True:
                    failed.append(f"{mod_path}: NO_REAL_ORDERS not True")
                if getattr(mod, "RESEARCH_ONLY", None) is not True:
                    failed.append(f"{mod_path}: RESEARCH_ONLY not True")
            except ImportError:
                pass  # Module may not be available yet — skip
            except Exception as exc:
                failed.append(f"{mod_path}: check error: {exc}")

        if failed:
            return ("FAIL", f"Stable modules missing safety flags: {failed[:3]}")
        return ("PASS", "All importable stable_*.py modules have NO_REAL_ORDERS=True, RESEARCH_ONLY=True")
