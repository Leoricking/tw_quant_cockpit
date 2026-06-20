"""
data/providers/data_gov_tw/cache_policy_v143.py — Cache key policy v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] real/mock isolation. dataset isolation. agency host isolation.
[!] Stale cache does not masquerade as fresh.
[!] No credentials stored in cache keys.
[!] fixture cache must not enter real mode.
"""
from __future__ import annotations

import hashlib
from typing import Any, Dict, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class DataGovTwCachePolicy:
    """
    Defines cache key structure and TTL policies for data.gov.tw.

    Cache key includes:
    - provider_id
    - dataset_id
    - resource_id
    - agency
    - endpoint
    - format
    - normalized parameters
    - reporting period
    - observation date
    - schema version
    - contract hash
    - mode (real/mock) — real and mock are isolated

    Rules:
    - real/mock isolated
    - dataset isolated
    - agency host isolated
    - stale cache not treated as fresh
    - revision can invalidate cache
    - corrupted cache → graceful (skip, fetch again)
    - no credentials in cache key
    - runtime cache gitignored
    - fixture cache NEVER in real mode
    """

    def build_key(
        self,
        provider_id: str,
        dataset_id: str,
        resource_id: Optional[str],
        agency: Optional[str],
        endpoint: Optional[str],
        format: Optional[str],
        params: Optional[Dict[str, Any]] = None,
        reporting_period: Optional[str] = None,
        observation_date: Optional[str] = None,
        schema_version: Optional[str] = None,
        contract_hash: Optional[str] = None,
        mode: str = "real",
    ) -> str:
        """Build a cache key. Never includes credentials."""
        parts = [
            f"provider={provider_id}",
            f"dataset={dataset_id}",
            f"resource={resource_id or ''}",
            f"agency={agency or ''}",
            f"endpoint={endpoint or ''}",
            f"format={format or ''}",
            f"period={reporting_period or ''}",
            f"date={observation_date or ''}",
            f"schema_ver={schema_version or ''}",
            f"contract={contract_hash or ''}",
            f"mode={mode}",
        ]
        if params:
            sorted_params = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
            parts.append(f"params={sorted_params}")

        key_str = "|".join(parts)
        return hashlib.sha256(key_str.encode()).hexdigest()

    def get_ttl_seconds(self, update_frequency: Optional[str]) -> int:
        """Return cache TTL in seconds based on dataset update frequency."""
        from data.providers.data_gov_tw.models_v143 import UpdateFrequency
        ttl_map = {
            UpdateFrequency.DAILY.value: 3600,          # 1 hour
            UpdateFrequency.WEEKLY.value: 14400,        # 4 hours
            UpdateFrequency.MONTHLY.value: 86400,       # 1 day
            UpdateFrequency.QUARTERLY.value: 86400 * 3, # 3 days
            UpdateFrequency.YEARLY.value: 86400 * 7,    # 7 days
            UpdateFrequency.IRREGULAR.value: 86400,     # 1 day
            UpdateFrequency.UNSCHEDULED.value: 86400,   # 1 day
            UpdateFrequency.UNKNOWN.value: 3600,        # 1 hour (conservative)
        }
        return ttl_map.get((update_frequency or "").upper(), 3600)

    def is_fixture_key(self, key: str) -> bool:
        """Fixture cache keys should never be used in real mode."""
        return "fixture" in key.lower() or "mock" in key.lower() or "test" in key.lower()
