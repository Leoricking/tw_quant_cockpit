"""
workflow_automation/safe_command_registry.py — SafeCommandRegistry (v0.4.9).

Defines allowlist of research-only commands that can be executed by the
Research Workflow Automation system. Any command not on the allowlist
or containing a forbidden keyword is BLOCKED and never executed.

[!] Workflow Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] All commands are research-only. No buy/sell/order/broker execution.
"""
from __future__ import annotations

import logging
import re
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Allowed command prefixes (research-only whitelist)
# ---------------------------------------------------------------------------
_ALLOWED_COMMANDS: List[str] = [
    "python main.py data-quality-gate",
    "python main.py provider-reliability",
    "python main.py provider-health",
    "python main.py api-fetch-diagnostics",
    "python main.py data-freshness",
    "python main.py notification-list",
    "python main.py notification-scan",
    "python main.py research-review",
    "python main.py research-review-summary",
    "python main.py research-review-actions",
    "python main.py research-review-report",
    "python main.py research-coach",
    "python main.py research-coach-summary",
    "python main.py research-coach-checklist",
    "python main.py research-coach-replay-plan",
    "python main.py research-coach-rule-queue",
    "python main.py research-coach-data-repair",
    "python main.py research-coach-report",
    "python main.py journal-summary",
    "python main.py rule-governance",
    "python main.py signal-quality",
    "python main.py ml-knowledge-feature-summary",
    "python main.py ml-knowledge-leakage-check",
    "python main.py experiment-list",
    "python main.py auto-report",
    "python main.py intraday-replay",
    "python main.py stable-release-check",
    "python main.py model-monitoring",
    "python main.py replay-training-summary",
    "python main.py research-workflow-summary",
    "python main.py research-workflow-tasks",
]

# ---------------------------------------------------------------------------
# Forbidden keywords — any match BLOCKS execution
# ---------------------------------------------------------------------------
_FORBIDDEN_KEYWORDS: List[str] = [
    # Trading words
    "buy", "sell", "order", "submit_order", "place_order",
    "broker", "shioaji", "live trade", "auto trade", "execute trade",
    "real order", "margin order", "short sell", "cover order",
    # Shell compound operators
    "&&", "||", ";", "|", ">", "<", "`",
    # Shell navigation / control
    " cd ", "powershell", "cmd.exe", " bash ", " sh ",
    # git
    " git ",
    # Secret / env
    ".env", "password", "api_key",
    # Arbitrary code execution
    "python -c ",
]

# Extra patterns (regex) for more precise blocking
_FORBIDDEN_PATTERNS: List[str] = [
    r"\bcd\b",
    r"\bgit\b",
    r"\btoken\b",
]


class SafeCommandRegistry:
    """
    Registry of research-only safe commands.

    Only commands that:
      1. Match the allowed prefix list
      2. Do NOT contain any forbidden keyword
      3. Do NOT match any forbidden regex pattern

    are allowed for execution by the workflow runner.

    Safety:
      read_only          = True
      no_real_orders     = True
      production_blocked = True
    """

    read_only:          bool = True
    no_real_orders:     bool = True
    production_blocked: bool = True

    def __init__(self):
        self._allowed   = list(_ALLOWED_COMMANDS)
        self._forbidden = list(_FORBIDDEN_KEYWORDS)
        self._patterns  = [re.compile(p, re.IGNORECASE) for p in _FORBIDDEN_PATTERNS]

    def is_allowed(self, command: str) -> bool:
        """Return True if command is safe to execute."""
        if not command or not command.strip():
            return False
        cmd = command.strip()
        # Check forbidden keywords first
        cmd_lower = cmd.lower()
        for kw in self._forbidden:
            if kw.lower() in cmd_lower:
                return False
        # Check forbidden regex patterns
        for pat in self._patterns:
            if pat.search(cmd):
                return False
        # Check allowlist prefix
        for allowed in self._allowed:
            if cmd.startswith(allowed):
                return True
        return False

    def explain_block_reason(self, command: str) -> str:
        """Return a human-readable block reason for a command."""
        if not command or not command.strip():
            return "Empty command."
        cmd = command.strip()
        cmd_lower = cmd.lower()
        for kw in self._forbidden:
            if kw.lower() in cmd_lower:
                return f"Forbidden keyword: '{kw}'"
        for i, pat in enumerate(self._patterns):
            if pat.search(cmd):
                return f"Forbidden pattern: '{_FORBIDDEN_PATTERNS[i]}'"
        return "Command not in allowed research command list."

    def sanitize_command(self, command: str) -> Optional[str]:
        """Return command if safe, else None."""
        if self.is_allowed(command):
            return command.strip()
        return None

    def list_allowed_commands(self) -> List[str]:
        """Return copy of the allowed command prefix list."""
        return list(self._allowed)

    def check_and_report(self, command: str) -> dict:
        """
        Check a command and return a result dict.
        Returns: {allowed, command, reason}
        """
        allowed = self.is_allowed(command)
        return {
            "allowed":          allowed,
            "command":          command,
            "reason":           "" if allowed else self.explain_block_reason(command),
            "workflow_only":    True,
            "no_real_orders":   True,
        }
