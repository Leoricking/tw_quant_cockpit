"""
data/providers/token_safe_config.py - Token-safe config loader (v0.3.18).

Reads API tokens from .env file without logging full token values.
Never commits tokens to repo. Never writes to real .env.

[!] Read Only. No Real Orders.
[!] Tokens are NEVER logged in full.
[!] .env is NEVER committed to git.
"""

from __future__ import annotations

import logging
import os
import re
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Supported token names and their metadata
_TOKEN_REGISTRY: Dict[str, dict] = {
    "FINMIND_TOKEN": {
        "required": False,
        "description": "FinMind API token (optional — limited public access without token)",
        "used_by": ["finmind"],
        "env_key": "FINMIND_TOKEN",
    },
    "TWSE_API_KEY": {
        "required": False,
        "description": "TWSE Open API key (optional / future v0.4)",
        "used_by": ["twse"],
        "env_key": "TWSE_API_KEY",
    },
    "MOPS_API_KEY": {
        "required": False,
        "description": "MOPS API key (optional / future v0.4)",
        "used_by": ["mops"],
        "env_key": "MOPS_API_KEY",
    },
    "MEGA_API_KEY": {
        "required": False,
        "description": "Mega read-only API key (planned v0.4+, read-only only)",
        "used_by": ["mega_readonly_planned"],
        "env_key": "MEGA_API_KEY",
    },
    "MEGA_ACCOUNT": {
        "required": False,
        "description": "Mega account ID (planned v0.4+, read-only only)",
        "used_by": ["mega_readonly_planned"],
        "env_key": "MEGA_ACCOUNT",
    },
}

# Patterns that suggest a value is a real token (not a placeholder)
_PLACEHOLDER_PATTERNS = [
    r"^$",
    r"^your[_-]",
    r"^<",
    r"^REPLACE",
    r"^INSERT",
    r"^xxx+$",
    r"^abc+$",
    r"^test[_-]",
    r"^placeholder",
    r"^example",
]


class TokenSafeConfig:
    """
    Reads API tokens from a .env file safely.

    - Never logs full token values.
    - Never writes to the real .env.
    - Can create a safe .env.example template.
    - Warns if a tracked config file might contain a real token.
    """

    def __init__(self, env_path: str = ".env"):
        self._env_path = os.path.abspath(env_path)
        self._loaded: Dict[str, str] = {}
        self._load_attempted = False

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_env(self) -> None:
        """Load .env file into memory. Safe to call multiple times."""
        self._loaded = {}
        self._load_attempted = True

        if not os.path.isfile(self._env_path):
            logger.debug(
                "TokenSafeConfig: .env not found at %s — tokens will be empty",
                self._env_path,
            )
            return

        try:
            with open(self._env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    key, _, val = line.partition("=")
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key:
                        self._loaded[key] = val
            logger.debug(
                "TokenSafeConfig: loaded %d keys from %s",
                len(self._loaded), self._env_path,
            )
        except Exception as exc:
            logger.warning("TokenSafeConfig: failed to read %s: %s", self._env_path, exc)

    def _ensure_loaded(self) -> None:
        if not self._load_attempted:
            self.load_env()

    # ------------------------------------------------------------------
    # Token access (never logs full value)
    # ------------------------------------------------------------------

    def get_token(self, name: str) -> Optional[str]:
        """Return raw token value or None. Never logs the value."""
        self._ensure_loaded()
        val = self._loaded.get(name, "").strip()
        if not val or self._is_placeholder(val):
            return None
        return val

    def get_masked_token(self, name: str) -> str:
        """Return masked token string for display (e.g. 'abc****xyz')."""
        token = self.get_token(name)
        if token is None:
            return "(not configured)"
        return self.mask_token(token)

    def has_token(self, name: str) -> bool:
        """Return True if the token is configured and non-placeholder."""
        return self.get_token(name) is not None

    def mask_token(self, token: str) -> str:
        """Mask a token for safe display: show first 3 + last 3 chars."""
        if not token:
            return "(empty)"
        if len(token) <= 6:
            return "***"
        return f"{token[:3]}{'*' * (len(token) - 6)}{token[-3:]}"

    def _is_placeholder(self, value: str) -> bool:
        """Return True if the value looks like a placeholder, not a real token."""
        val = value.strip().lower()
        for pattern in _PLACEHOLDER_PATTERNS:
            if re.match(pattern, val, re.IGNORECASE):
                return True
        return False

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_required_tokens(self) -> dict:
        """
        Check which required tokens are configured.
        Returns dict: {token_name: {"required": bool, "configured": bool, "warning": str}}
        """
        self._ensure_loaded()
        results = {}
        for name, meta in _TOKEN_REGISTRY.items():
            configured = self.has_token(name)
            warning = ""
            if meta["required"] and not configured:
                warning = f"{name} is required but not configured"
            elif not configured:
                info = meta.get("description", "")
                warning = f"{name} not set — {info}" if info else f"{name} not set"
            results[name] = {
                "required": meta["required"],
                "configured": configured,
                "masked": self.get_masked_token(name) if configured else "(not configured)",
                "used_by": meta.get("used_by", []),
                "description": meta.get("description", ""),
                "warning": warning,
            }
        return results

    def get_all_token_status(self) -> Dict[str, dict]:
        """Return status dict for all known tokens (masked)."""
        return self.validate_required_tokens()

    # ------------------------------------------------------------------
    # .env.example creation
    # ------------------------------------------------------------------

    def create_env_example(self, path: str = ".env.example") -> str:
        """
        Create a safe .env.example template at the given path.
        Never contains real tokens. Safe to commit.
        Returns the path written.
        """
        abs_path = os.path.abspath(path)

        # Safety: never write to the real .env
        if os.path.basename(abs_path) == ".env" and not abs_path.endswith(".example"):
            raise ValueError(
                "create_env_example() refuses to write to '.env' directly. "
                "Use '.env.example' or 'config/env.example'."
            )

        lines = [
            "# TW Quant Cockpit — Environment Variable Example",
            "# Copy this file to .env and fill in your values.",
            "# NEVER commit your real .env to version control.",
            "# This .env.example contains NO real tokens.",
            "",
            "# FinMind API token (optional — public data available without token)",
            "# Get yours at: https://finmindtrade.com/",
            "FINMIND_TOKEN=",
            "",
            "# TWSE Open API key (optional / planned for v0.4)",
            "TWSE_API_KEY=",
            "",
            "# MOPS API key (optional / planned for v0.4)",
            "MOPS_API_KEY=",
            "",
            "# Mega Securities read-only API key (planned for v0.4+, read-only only)",
            "# Real order execution is PERMANENTLY DISABLED.",
            "MEGA_API_KEY=",
            "",
            "# Mega account ID (planned for v0.4+, read-only only)",
            "MEGA_ACCOUNT=",
            "",
            "# ====================================================",
            "# SAFETY NOTES",
            "# ====================================================",
            "# 1. This system is READ ONLY — no real orders are placed.",
            "# 2. Never set TWQC_ENABLE_REAL_ORDER=True.",
            "# 3. Never commit your .env file.",
            "# 4. Never share your tokens in logs or reports.",
        ]

        try:
            os.makedirs(os.path.dirname(abs_path) or ".", exist_ok=True)
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            logger.info("TokenSafeConfig: created %s", abs_path)
        except Exception as exc:
            logger.error("TokenSafeConfig: failed to create %s: %s", abs_path, exc)
            raise

        return abs_path

    # ------------------------------------------------------------------
    # Tracked-file token leak warning
    # ------------------------------------------------------------------

    def warn_if_token_in_tracked_file(self, file_path: str) -> list:
        """
        Check a file for suspicious token-like strings.
        Returns list of warning strings (empty if clean).
        """
        warnings = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # Look for long alphanumeric strings that look like tokens
            candidates = re.findall(r'["\']([A-Za-z0-9_\-]{20,})["\']', content)
            for cand in candidates:
                if not self._is_placeholder(cand):
                    warnings.append(
                        f"Potential token in tracked file {file_path}: "
                        f"{self.mask_token(cand)}"
                    )
        except Exception:
            pass
        return warnings
