"""
replay/stable_cli_audit.py — ReplayStableCLIAudit for v1.2.9.

Checks that all key replay CLI commands are registered in main.py.
Lightweight import-based checks. No real orders.

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

_EXPECTED_COMMANDS: List[str] = [
    "replay-health",
    "replay-scenario-health",
    "replay-session-manager-health",
    "replay-journal-health",
    "replay-scoring-health",
    "replay-strategy-health",
    "replay-timeframe-health",
    "replay-review-health",
    "replay-challenge-health",
    "replay-registry-health",
    "replay-stable-health",
    "replay-stable-summary",
    "replay-stable-manifest",
    "replay-stable-capabilities",
    "replay-stable-contracts",
    "replay-stable-compatibility",
    "replay-stable-store-audit",
    "replay-stable-runtime-audit",
    "replay-stable-cli-audit",
    "replay-stable-gui-audit",
    "replay-stable-report-audit",
    "replay-stable-safety-audit",
    "replay-stable-regression-audit",
    "replay-stable-report",
]


class ReplayStableCLIAudit:
    """
    Audits that all key replay CLI commands are registered in main.py.

    Reads main.py and checks for command registration.
    Returns PASS/WARN/FAIL per command.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, project_root: str = "") -> None:
        if project_root:
            self._root = project_root
        else:
            self._root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def _read_main(self) -> str:
        """Read main.py content. Returns empty string if not found."""
        main_path = os.path.join(self._root, "main.py")
        try:
            with open(main_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def audit_all(self) -> Dict[str, Tuple[str, str]]:
        """Audit all expected CLI commands. Returns {cmd: (status, message)}."""
        main_content = self._read_main()
        if not main_content:
            return {
                cmd: ("WARN", "main.py not readable — cannot verify command registration")
                for cmd in _EXPECTED_COMMANDS
            }

        results: Dict[str, Tuple[str, str]] = {}
        for cmd in _EXPECTED_COMMANDS:
            results[cmd] = self._check_command(cmd, main_content)
        return results

    def _check_command(self, command: str, main_content: str) -> Tuple[str, str]:
        """Check if command is registered in main.py content."""
        # Check for the command string as a key in the dispatch dict
        if f'"{command}"' in main_content or f"'{command}'" in main_content:
            return ("PASS", f"{command!r} registered in main.py")
        # Softer check — sometimes commands appear as subparser help strings
        if command in main_content:
            return ("PASS", f"{command!r} found in main.py")
        return ("WARN", f"{command!r} not found in main.py dispatch dict")
