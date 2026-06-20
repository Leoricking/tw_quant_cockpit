"""
data/providers/finmind/auth_v144.py — FinMind token/auth management v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Token read from env var only. Never log/expose full token.
[!] token_optional=True. Anonymous mode supported.
[!] AUTH_INVALID → no retry, no token display, no token rotation.
"""
from __future__ import annotations

import hashlib
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FINMIND_TOKEN_OPTIONAL = True
FINMIND_TOKEN_STORAGE_SECURE = True


class FinMindAuthManager:
    """
    Manages FinMind API token from environment variables.
    Token is optional — anonymous mode is supported.
    Never logs or exposes the full token.
    """

    _ENV_VARS = ["FINMIND_API_TOKEN", "FINMIND_TOKEN"]

    def __init__(self) -> None:
        self._token: Optional[str] = None
        self._token_source: Optional[str] = None
        self._load_token()

    def _load_token(self) -> None:
        for env_var in self._ENV_VARS:
            val = os.environ.get(env_var, "").strip()
            if val:
                self._token = val
                self._token_source = env_var
                logger.debug("FinMind token loaded from %s (fingerprint: %s)", env_var, self.token_fingerprint)
                return
        self._token = None
        self._token_source = None

    @property
    def token_present(self) -> bool:
        """Return True if a token was found in environment."""
        return self._token is not None and len(self._token) > 0

    @property
    def token_source(self) -> Optional[str]:
        """Return the env var name from which the token was loaded."""
        return self._token_source

    @property
    def token_fingerprint(self) -> Optional[str]:
        """Return first 8 chars of SHA256 of token, or None if no token."""
        if not self._token:
            return None
        digest = hashlib.sha256(self._token.encode("utf-8")).hexdigest()
        return digest[:8]

    @property
    def anonymous_mode(self) -> bool:
        """Return True if running without a token."""
        return not self.token_present

    @property
    def authenticated_mode(self) -> bool:
        """Return True if a valid token is present."""
        return self.token_present

    def get_token_for_request(self) -> Optional[str]:
        """Return the raw token for use in API requests (never log this value)."""
        return self._token

    def get_auth_summary(self) -> dict:
        """Return a safe summary (no token value exposed)."""
        return {
            "token_present": self.token_present,
            "token_source": self.token_source,
            "token_fingerprint": self.token_fingerprint,
            "anonymous_mode": self.anonymous_mode,
            "authenticated_mode": self.authenticated_mode,
            "token_optional": FINMIND_TOKEN_OPTIONAL,
            "token_storage_secure": FINMIND_TOKEN_STORAGE_SECURE,
        }
