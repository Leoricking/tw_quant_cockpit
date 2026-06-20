"""
data/providers/twse/cache_policy_v140.py — TWSE cache policy v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mock cache and real cache MUST be isolated.
[!] Never cache credentials.
"""
from __future__ import annotations

from typing import Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TWSECachePolicy:
    """Cache TTL constants and key building for TWSE provider."""

    SECURITY_MASTER_TTL: int = 86400 * 7       # 7 days
    TRADING_CALENDAR_TTL: int = 86400 * 30     # 30 days
    HISTORICAL_DAILY_TTL: int = 86400 * 7      # 7 days
    CURRENT_DAY_TTL: int = 3600                # 1 hour
    INSTITUTIONAL_TTL: int = 14400             # 4 hours
    MARGIN_TTL: int = 14400                    # 4 hours

    _REAL_PREFIX = "twse:real"
    _MOCK_PREFIX = "twse:mock"

    def build_cache_key(
        self,
        provider_id: Optional[str],
        endpoint_id: Optional[str],
        symbol: Optional[str],
        market: Optional[str],
        date: Optional[str],
        start_date: Optional[str],
        end_date: Optional[str],
        schema_version: Optional[str],
    ) -> str:
        """Build a deterministic cache key for real data. Never includes credentials."""
        parts = [
            self._REAL_PREFIX,
            str(provider_id or ""),
            str(endpoint_id or ""),
            str(market or ""),
            str(symbol or ""),
            str(date or ""),
            str(start_date or ""),
            str(end_date or ""),
            str(schema_version or ""),
        ]
        return ":".join(parts)

    def build_mock_cache_key(
        self,
        provider_id: Optional[str],
        endpoint_id: Optional[str],
        symbol: Optional[str],
        market: Optional[str],
        date: Optional[str],
        start_date: Optional[str],
        end_date: Optional[str],
        schema_version: Optional[str],
    ) -> str:
        """Build a deterministic cache key for mock/fixture data. Isolated from real keys."""
        parts = [
            self._MOCK_PREFIX,
            str(provider_id or ""),
            str(endpoint_id or ""),
            str(market or ""),
            str(symbol or ""),
            str(date or ""),
            str(start_date or ""),
            str(end_date or ""),
            str(schema_version or ""),
        ]
        return ":".join(parts)
