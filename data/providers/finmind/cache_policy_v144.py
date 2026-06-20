"""
data/providers/finmind/cache_policy_v144.py — FinMind cache policy v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Real/mock isolated. Token mode = "anonymous" or "authenticated" — never actual token.
[!] Stale cache does not masquerade as fresh.
"""
from __future__ import annotations

import hashlib
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Default TTL by policy type (seconds)
_POLICY_TTL = {
    "DAILY_OHLCV": 86400,          # 24 hours
    "INSTITUTIONAL": 86400,
    "MARGIN": 86400,
    "MONTHLY_REVENUE": 86400 * 7,  # 1 week
    "FINANCIAL_STATEMENT": 86400 * 30,  # 30 days
    "DEFAULT": 3600,               # 1 hour
}


class FinMindCachePolicy:
    """
    Cache policy for FinMind data.
    Keys include token_mode (not actual token), mode (real/mock), and schema version.
    Stale entries are flagged as stale, not returned as fresh.
    """

    def make_cache_key(
        self,
        provider_id: str,
        api_version: str,
        dataset: str,
        data_id: Optional[str],
        start_date: Optional[str],
        end_date: Optional[str],
        schema_version: Optional[str],
        mode: str,
        token_mode: str,
    ) -> str:
        """
        Build a stable cache key.
        token_mode must be "anonymous" or "authenticated" — never the actual token.
        mode must be "real" or "mock" — these are isolated.
        """
        assert token_mode in ("anonymous", "authenticated"), f"Invalid token_mode: {token_mode!r}"
        assert mode in ("real", "mock"), f"Invalid mode: {mode!r}"

        parts = [
            f"provider={provider_id}",
            f"api={api_version}",
            f"dataset={dataset}",
            f"data_id={data_id or ''}",
            f"start={start_date or ''}",
            f"end={end_date or ''}",
            f"schema={schema_version or ''}",
            f"mode={mode}",
            f"token={token_mode}",  # Never actual token
        ]
        raw = "|".join(parts)
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]
        return f"finmind:{mode}:{dataset}:{digest}"

    def is_stale(
        self,
        cache_entry: Dict[str, Any],
        policy: str,
        current_timestamp: Optional[float] = None,
    ) -> bool:
        """
        Return True if cache entry is stale.
        Stale entries are not returned as fresh — caller must handle accordingly.
        """
        import time
        now = current_timestamp if current_timestamp is not None else time.time()
        cached_at = cache_entry.get("cached_at")
        if cached_at is None:
            return True  # No timestamp → treat as stale

        ttl = _POLICY_TTL.get(policy, _POLICY_TTL["DEFAULT"])
        age = now - float(cached_at)
        return age > ttl

    def get_ttl(self, policy: str) -> int:
        """Return TTL in seconds for a given freshness policy."""
        return _POLICY_TTL.get(policy, _POLICY_TTL["DEFAULT"])

    def build_cache_metadata(
        self,
        provider_id: str,
        dataset: str,
        mode: str,
        token_mode: str,
        schema_version: Optional[str] = None,
        fetched_at: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Build metadata dict for a cache entry."""
        import time
        return {
            "provider_id": provider_id,
            "dataset": dataset,
            "mode": mode,
            "token_mode": token_mode,  # "anonymous" or "authenticated" only
            "schema_version": schema_version,
            "cached_at": fetched_at if fetched_at is not None else time.time(),
            "no_real_orders": True,
        }
