"""
data/providers/token_setup_assistant.py - FinMind / future API token setup assistant (v0.4.1).

[!] Read Only. No Real Orders.
[!] Never modifies real .env.
[!] Never displays full token.
[!] Never writes token to code.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_REQUIRED_TOKENS = ["FINMIND_TOKEN"]
_OPTIONAL_TOKENS = ["MOPS_API_KEY", "MEGA_API_KEY"]

_TOKEN_DOCS: Dict[str, dict] = {
    "FINMIND_TOKEN": {
        "label":       "FinMind API Token",
        "purpose":     "Access FinMind public market data API (TaiwanStockPrice, Revenue, Institutional, etc.)",
        "signup_url":  "https://finmindtrade.com/",
        "env_key":     "FINMIND_TOKEN",
        "required":    True,
        "note":        "Without token: limited / rate-limited public access. With token: full dataset access.",
    },
    "MOPS_API_KEY": {
        "label":   "MOPS API Key (Optional)",
        "purpose": "MOPS public disclosure (planned — not yet active)",
        "env_key": "MOPS_API_KEY",
        "required": False,
        "note":    "Planned for v0.4+. Public data may not require a key.",
    },
    "MEGA_API_KEY": {
        "label":   "Mega Read-Only API Key (Planned)",
        "purpose": "兆豐證券 read-only account query (planned — NO ORDER EXECUTION)",
        "env_key": "MEGA_API_KEY",
        "required": False,
        "note":    "Planned for v0.4+. Read-only only. Production trading BLOCKED.",
    },
}


class TokenSetupAssistant:
    """
    FinMind / future API token setup assistant.

    Parameters
    ----------
    env_path             : Path to .env file (read-only inspection)
    env_example_path     : Path to .env.example (may be updated)
    config_example_path  : Alternative config/env.example path

    Safety:
        - Does NOT modify the real .env file.
        - Does NOT prompt user to enter token in terminal.
        - Does NOT log or display full token value.
        - .env.example may be written with placeholder values only.
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        env_path: str = ".env",
        env_example_path: str = ".env.example",
        config_example_path: str = "config/env.example",
    ):
        self._env_path          = env_path
        self._env_example_path  = env_example_path
        self._config_example    = config_example_path
        self._loaded_env: Dict[str, str] = {}
        self._load_env_file()

    # ------------------------------------------------------------------
    # Env loading (read-only)
    # ------------------------------------------------------------------

    def _load_env_file(self) -> None:
        """Load .env file without modifying it. Only read masked values."""
        for path in [self._env_path, self._config_example]:
            if os.path.isfile(path):
                try:
                    with open(path, encoding="utf-8", errors="replace") as f:
                        for line in f:
                            line = line.strip()
                            if not line or line.startswith("#"):
                                continue
                            if "=" in line:
                                key, _, val = line.partition("=")
                                key = key.strip()
                                val = val.strip().strip('"').strip("'")
                                if key and val and key not in self._loaded_env:
                                    self._loaded_env[key] = val
                except Exception as exc:
                    logger.debug("TokenSetupAssistant: cannot read %s: %s", path, exc)
        # Also check os.environ (already-set vars take precedence)
        for key in list(_REQUIRED_TOKENS) + list(_OPTIONAL_TOKENS):
            env_val = os.environ.get(key, "").strip()
            if env_val:
                self._loaded_env[key] = env_val

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def inspect(self) -> dict:
        """Full inspection of token configuration state."""
        required = self.check_required_tokens()
        optional = self.check_optional_tokens()
        safety   = self.validate_env_safety()
        instructions = self.generate_setup_instructions()
        all_configured = all(v.get("configured", False) for v in required.values())
        return {
            "required_tokens":  required,
            "optional_tokens":  optional,
            "env_safety":       safety,
            "setup_instructions": instructions,
            "all_required_configured": all_configured,
            "read_only":        True,
            "no_real_orders":   True,
        }

    def check_required_tokens(self) -> Dict[str, dict]:
        """Return status of all required tokens (masked)."""
        result = {}
        for key in _REQUIRED_TOKENS:
            val = self._loaded_env.get(key, "")
            configured = bool(val and not val.startswith("your_") and len(val) > 4)
            doc = _TOKEN_DOCS.get(key, {})
            result[key] = {
                "configured":   configured,
                "masked_value": self.mask_token(val) if configured else "(not configured)",
                "label":        doc.get("label", key),
                "note":         doc.get("note", ""),
                "next_step":    "" if configured else self._next_step(key),
            }
        return result

    def check_optional_tokens(self) -> Dict[str, dict]:
        """Return status of optional tokens (masked). Never require these."""
        result = {}
        for key in _OPTIONAL_TOKENS:
            val = self._loaded_env.get(key, "")
            configured = bool(val and not val.startswith("your_") and len(val) > 4)
            doc = _TOKEN_DOCS.get(key, {})
            result[key] = {
                "configured":   configured,
                "masked_value": self.mask_token(val) if configured else "(not configured)",
                "label":        doc.get("label", key),
                "note":         doc.get("note", ""),
                "status":       "configured" if configured else "planned",
            }
        return result

    def generate_setup_instructions(self) -> dict:
        """Return setup instructions for missing tokens. Never auto-fills .env."""
        instructions = {}
        for key in _REQUIRED_TOKENS:
            val = self._loaded_env.get(key, "")
            configured = bool(val and not val.startswith("your_") and len(val) > 4)
            if not configured:
                doc = _TOKEN_DOCS.get(key, {})
                instructions[key] = {
                    "status": "MISSING",
                    "steps": [
                        f"1. Sign up at {doc.get('signup_url', '—')}",
                        "2. Copy your API token from the dashboard",
                        "3. Add to your .env file: " + key + "=<your_token_here>",
                        "4. Do NOT commit .env to git",
                        "5. Re-run: python main.py api-token-check",
                    ],
                    "note": doc.get("note", ""),
                    "warning": "Never paste token into code or share it publicly.",
                }
            else:
                instructions[key] = {"status": "OK", "steps": []}
        return instructions

    def validate_env_safety(self) -> dict:
        """
        Check that the .env file itself is safe (not committed to git, etc.).
        Does NOT modify any file.
        """
        issues = []
        safe   = True

        env_path = self._env_path
        if os.path.isfile(env_path):
            # Check if env_path is in .gitignore
            gitignore_path = os.path.join(os.path.dirname(env_path) or ".", ".gitignore")
            if not os.path.isfile(gitignore_path):
                # Try project root
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                gitignore_path = os.path.join(project_root, ".gitignore")

            env_ignored = False
            if os.path.isfile(gitignore_path):
                try:
                    with open(gitignore_path, encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    # Simple check for .env pattern
                    env_ignored = (".env" in content) or ("*.env" in content)
                except Exception:
                    pass

            if not env_ignored:
                issues.append(".env may not be in .gitignore — check before committing")
                safe = False
        else:
            issues.append(f".env file not found at {env_path} — create it manually")

        # Check that .env.example exists (good practice)
        example_exists = os.path.isfile(self._env_example_path)

        return {
            "safe":             safe,
            "env_file_exists":  os.path.isfile(env_path),
            "env_ignored":      safe,
            "env_example_exists": example_exists,
            "issues":           issues,
            "note":             "Never commit your real .env to git.",
        }

    def create_safe_env_example(self) -> dict:
        """
        Create or update .env.example with placeholder values only.
        NEVER writes real token values.
        """
        lines = [
            "# .env.example — TW Quant Cockpit",
            "# Copy this file to .env and fill in your real values.",
            "# NEVER commit your real .env to git.",
            "# NEVER paste real tokens here.",
            "",
            "# FinMind API token (required for full data access)",
            "# Sign up at https://finmindtrade.com/",
            "FINMIND_TOKEN=your_finmind_token_here",
            "",
            "# MOPS API Key (optional — planned for v0.4+)",
            "# MOPS_API_KEY=your_mops_api_key_here",
            "",
            "# Mega Read-Only API Key (optional — planned for v0.4+)",
            "# Production trading PERMANENTLY DISABLED",
            "# MEGA_API_KEY=your_mega_api_key_here",
        ]
        try:
            with open(self._env_example_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            return {"ok": True, "path": self._env_example_path,
                    "note": "Only placeholder values written. No real tokens."}
        except Exception as exc:
            return {"ok": False, "error": str(exc), "path": self._env_example_path}

    def mask_token(self, token: Optional[str]) -> str:
        """Mask a token for safe display. Never show full value."""
        if not token:
            return "(not configured)"
        token = str(token)
        if len(token) <= 4:
            return "****"
        visible = min(4, len(token) // 4)
        return token[:visible] + "*" * (len(token) - visible)

    def _next_step(self, key: str) -> str:
        doc = _TOKEN_DOCS.get(key, {})
        url = doc.get("signup_url", "")
        if url:
            return f"Sign up at {url}, copy token, add to .env as {key}=<token>"
        return f"Add {key}=<your_token> to your .env file"
