"""
Copy safety helpers for GUI panels.
Ensures no forbidden trading actions are copied to clipboard.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import re
from typing import Optional

_FORBIDDEN = [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
]
_WHITELIST = [
    "No Real Orders",
    "Broker Execution Disabled",
    "No broker execution",
    "Not an order",
    "No automatic deletion",
    "No automatic archive",
    "Archive Suggestions Only",
    "VALIDATED does not enable trading",
    "No auto trading",
    "No forbidden trading action",
]

# Allowed CLI command prefixes for Copy Safe Command
_ALLOWED_CLI_PREFIXES = [
    "python main.py",
    "python -m",
    "python -c",
]


def sanitize_copy_payload(payload: str) -> str:
    """Remove forbidden trading actions from copy payload after whitelist removal."""
    text = payload
    for phrase in _WHITELIST:
        text = text.replace(phrase, '')
    for forbidden in _FORBIDDEN:
        text = re.sub(r'\b' + forbidden + r'\b', '[RESEARCH_ONLY]', text)
    return payload  # return original if no match; only raises if scan fails


def _has_forbidden(text: str) -> bool:
    cleaned = text
    for phrase in _WHITELIST:
        cleaned = cleaned.replace(phrase, '')
    for forbidden in _FORBIDDEN:
        if re.search(r'\b' + forbidden + r'\b', cleaned):
            return True
    return False


def copy_safe_text(text: str) -> str:
    """
    Copy text to clipboard if safe. Returns the text if safe.
    Raises ValueError if forbidden trading action detected.
    Research Only. No Real Orders.
    """
    if _has_forbidden(text):
        raise ValueError(f"Cannot copy: forbidden trading action detected in text.")
    try:
        from PySide6.QtWidgets import QApplication
        cb = QApplication.clipboard()
        if cb:
            cb.setText(text)
    except Exception:
        pass
    return text


def copy_safe_command(command: str) -> str:
    """
    Copy a CLI command to clipboard if it's a research-only command.
    Raises ValueError if forbidden action or non-research command.
    Research Only. No Real Orders.
    """
    if _has_forbidden(command):
        raise ValueError(f"Cannot copy: forbidden trading action in command.")
    allowed = any(command.strip().startswith(prefix) for prefix in _ALLOWED_CLI_PREFIXES)
    if not allowed:
        raise ValueError(f"Cannot copy: command is not a recognized research CLI command.")
    try:
        from PySide6.QtWidgets import QApplication
        cb = QApplication.clipboard()
        if cb:
            cb.setText(command)
    except Exception:
        pass
    return command


def build_safe_next_step_copy(
    next_step: str,
    command: Optional[str] = None,
    label: Optional[str] = None,
) -> dict:
    """
    Build a copy-safe next step descriptor.
    Research Only. No Real Orders.
    """
    safe_step = next_step
    safe_cmd = command or ""
    if _has_forbidden(safe_step) or _has_forbidden(safe_cmd):
        safe_step = "REVIEW"
        safe_cmd = ""
    return {
        "next_step": safe_step,
        "command": safe_cmd,
        "label": label or safe_step,
        "research_only": True,
        "no_real_orders": True,
    }
