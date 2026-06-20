"""
data/providers/tpex/cache_policy_v141.py — TPEx cache policy v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
[!] TPEx and TWSE cache MUST be isolated (different key prefix 'tpex:' vs 'twse:').
[!] Never cache credentials.
"""
from __future__ import annotations

from typing import Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TPExCachePolicy:
    """Cache TTL constants and key building for TPEx provider."""

    SECURITY_MASTER_TTL: int = 86400 * 7       # 7 days
    TRADING_CALENDAR_TTL: int = 86400 * 30     # 30 days
    HISTORICAL_DAILY_TTL: int = 86400 * 7      # 7 days
    CURRENT_DAY_TTL: int = 3600                # 1 hour
    INSTITUTIONAL_TTL: int = 14400             # 4 hours
    MARGIN_TTL: int = 14400                    # 4 hours
    VALUATION_TTL: int = 86400                 # 1 day

    # TPEx prefix is isolated from TWSE ("twse:real" vs "tpex:real")
    _REAL_PREFIX = "tpex:real"
    _MOCK_PREFIX = "tpex:mock"

    def build_cache_key(
        self,
        provider_id: Optional[str] = None,
        endpoint_id: Optional[str] = None,
        market: Optional[str] = None,
        board: Optional[str] = None,
        security_type: Optional[str] = None,
        symbol: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        schema_version: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> str:
        """Build a deterministic cache key for real data. Never includes credentials or passwords."""
        parts = [
            self._REAL_PREFIX,
            str(provider_id or ""),
            str(endpoint_id or ""),
            str(market or ""),
            str(board or ""),
            str(security_type or ""),
            str(symbol or ""),
            str(trade_date or ""),
            str(start_date or ""),
            str(end_date or ""),
            str(schema_version or ""),
            str(mode or ""),
        ]
        return ":".join(parts)

    def build_mock_cache_key(
        self,
        provider_id: Optional[str] = None,
        endpoint_id: Optional[str] = None,
        market: Optional[str] = None,
        board: Optional[str] = None,
        security_type: Optional[str] = None,
        symbol: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        schema_version: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> str:
        """Build a deterministic cache key for mock/fixture data. Isolated from real keys."""
        parts = [
            self._MOCK_PREFIX,
            str(provider_id or ""),
            str(endpoint_id or ""),
            str(market or ""),
            str(board or ""),
            str(security_type or ""),
            str(symbol or ""),
            str(trade_date or ""),
            str(start_date or ""),
            str(end_date or ""),
            str(schema_version or ""),
            str(mode or ""),
        ]
        return ":".join(parts)
