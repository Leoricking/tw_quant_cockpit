"""
data/providers/mops/cache_policy_v142.py — MOPS cache policy v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
Real and mock caches are isolated. Real keys prefix "mops:real", mock "mops:mock".
"""
from __future__ import annotations

import hashlib
from typing import Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class MOPSCachePolicy:
    """Cache key policy for MOPS provider."""

    def build_cache_key(
        self,
        provider_id: str,
        endpoint_id: str,
        symbol: str,
        fiscal_year: Optional[int],
        fiscal_period: Optional[str],
        schema_version: str,
    ) -> str:
        """Build a real-mode cache key."""
        parts = [
            "mops:real",
            provider_id,
            endpoint_id,
            symbol or "",
            str(fiscal_year) if fiscal_year else "",
            fiscal_period or "",
            schema_version,
        ]
        raw = ":".join(parts)
        h = hashlib.sha256(raw.encode()).hexdigest()[:16]
        return f"mops:real:{endpoint_id}:{symbol}:{fiscal_period or 'none'}:{h}"

    def build_mock_cache_key(
        self,
        provider_id: str,
        endpoint_id: str,
        symbol: str,
        fiscal_year: Optional[int],
        fiscal_period: Optional[str],
        schema_version: str,
    ) -> str:
        """Build a mock-mode cache key (isolated from real)."""
        parts = [
            "mops:mock",
            provider_id,
            endpoint_id,
            symbol or "",
            str(fiscal_year) if fiscal_year else "",
            fiscal_period or "",
            schema_version,
        ]
        raw = ":".join(parts)
        h = hashlib.sha256(raw.encode()).hexdigest()[:16]
        return f"mops:mock:{endpoint_id}:{symbol}:{fiscal_period or 'none'}:{h}"

    def get_ttl_seconds(self, endpoint_id: str) -> int:
        """Return TTL in seconds for a given endpoint."""
        _ttl_map = {
            "company_profile": 86400 * 7,
            "monthly_revenue": 86400 * 30,
            "financial_report_announcement": 86400,
            "balance_sheet": 86400 * 90,
            "income_statement": 86400 * 90,
            "cash_flow": 86400 * 90,
            "equity_statement_index": 86400 * 90,
            "material_information": 3600,
            "investor_conference": 86400,
            "xbrl_index": 86400 * 90,
        }
        return _ttl_map.get(endpoint_id, 3600)
