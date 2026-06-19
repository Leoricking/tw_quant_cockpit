"""
data/providers/real_data_provider_cache.py — Provider cache abstraction v1.3.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Never caches credentials. Never marks stale as fresh.
[!] Runtime cache never committed. Tests use temp directory.
"""
from __future__ import annotations

import hashlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from data.providers.real_data_provider_models import (
    CacheStatus,
    ProviderCapability,
    ProviderRequest,
    ProviderResponse,
    _now_iso,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_iso(s: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# ProviderCacheKey
# ---------------------------------------------------------------------------

@dataclass
class ProviderCacheKey:
    """Deterministic cache key for a provider request."""
    provider_id: str = ""
    capability: str = ""
    symbol: str = ""
    market: str = ""
    start_date: str = ""
    end_date: str = ""
    interval: str = "1d"
    fields_hash: str = ""
    schema_version: str = "1.3.2"

    def to_string(self) -> str:
        """Deterministic string representation for use as dict key."""
        parts = [
            self.provider_id,
            self.capability,
            self.symbol,
            self.market,
            self.start_date,
            self.end_date,
            self.interval,
            self.fields_hash,
            self.schema_version,
        ]
        return "|".join(parts)

    @classmethod
    def from_request(cls, request: ProviderRequest, schema_version: str = "1.3.2") -> "ProviderCacheKey":
        """Build a cache key from a ProviderRequest."""
        symbol = request.symbols[0] if request.symbols else ""
        fields_hash = hashlib.sha256("|".join(sorted(request.fields)).encode()).hexdigest()[:12]
        return cls(
            provider_id=request.provider_id,
            capability=request.capability,
            symbol=symbol,
            market=request.market,
            start_date=request.start_date,
            end_date=request.end_date,
            interval=request.interval,
            fields_hash=fields_hash,
            schema_version=schema_version,
        )


# ---------------------------------------------------------------------------
# ProviderCacheEntry
# ---------------------------------------------------------------------------

@dataclass
class ProviderCacheEntry:
    """A single cached provider response."""
    key: ProviderCacheKey = field(default_factory=ProviderCacheKey)
    response: ProviderResponse = field(default_factory=ProviderResponse)
    cached_at: str = field(default_factory=_now_iso)
    expires_at: str = ""
    ttl_seconds: int = 1800
    is_stale: bool = False


# ---------------------------------------------------------------------------
# Abstract cache
# ---------------------------------------------------------------------------

class ProviderCacheAbstraction(ABC):
    """Abstract interface for provider response caching."""

    @abstractmethod
    def get(self, key: ProviderCacheKey) -> Optional[Tuple[ProviderResponse, str]]:
        """Return (response, CacheStatus) or None on miss."""
        raise NotImplementedError

    @abstractmethod
    def set(self, key: ProviderCacheKey, response: ProviderResponse, ttl_seconds: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def invalidate(self, key: ProviderCacheKey) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear_expired(self) -> int:
        """Clear expired entries, return count cleared."""
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def stats(self) -> dict:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# InMemoryProviderCache
# ---------------------------------------------------------------------------

class InMemoryProviderCache(ProviderCacheAbstraction):
    """
    Simple dict-based in-memory provider response cache.

    [!] Never caches credentials.
    [!] Stale entries return STALE status, not fresh.
    [!] Corrupted entries return INVALID status.
    """

    # Default TTLs by capability (seconds)
    TTL_BY_CAPABILITY: Dict[str, int] = {
        ProviderCapability.DAILY_OHLCV: 3600,
        ProviderCapability.INTRADAY_OHLCV: 60,
        ProviderCapability.MONTHLY_REVENUE: 86400,
        ProviderCapability.FINANCIAL_STATEMENT: 86400,
    }
    DEFAULT_TTL = 1800

    def __init__(self) -> None:
        self._store: Dict[str, ProviderCacheEntry] = {}
        self._hits = 0
        self._misses = 0
        self._stale_hits = 0
        self._bypasses = 0

    def get_ttl_for_capability(self, capability: str) -> int:
        return self.TTL_BY_CAPABILITY.get(capability, self.DEFAULT_TTL)

    def get(self, key: ProviderCacheKey) -> Optional[Tuple[ProviderResponse, str]]:
        """
        Returns (response, CacheStatus).
        - HIT: fresh entry found
        - STALE: entry exists but expired — returns STALE, not HIT
        - INVALID: corruption detected
        - None implies MISS (caller handles)
        """
        k = key.to_string()
        entry = self._store.get(k)
        if entry is None:
            self._misses += 1
            return None

        # Corruption check
        if not isinstance(entry, ProviderCacheEntry) or entry.response is None:
            self._store.pop(k, None)
            return (ProviderResponse(), CacheStatus.INVALID)

        # Check expiry
        now = _utc_now()
        expires = _parse_iso(entry.expires_at)
        if expires is not None and now > expires:
            entry.is_stale = True
            self._stale_hits += 1
            return (entry.response, CacheStatus.STALE)

        self._hits += 1
        return (entry.response, CacheStatus.HIT)

    def set(self, key: ProviderCacheKey, response: ProviderResponse, ttl_seconds: int) -> None:
        """Store a response in cache with TTL."""
        from datetime import timedelta
        now = _utc_now()
        expires = now + timedelta(seconds=ttl_seconds)
        entry = ProviderCacheEntry(
            key=key,
            response=response,
            cached_at=now.isoformat(),
            expires_at=expires.isoformat(),
            ttl_seconds=ttl_seconds,
            is_stale=False,
        )
        self._store[key.to_string()] = entry

    def invalidate(self, key: ProviderCacheKey) -> None:
        self._store.pop(key.to_string(), None)

    def clear_expired(self) -> int:
        """Remove expired entries, return count removed."""
        now = _utc_now()
        to_remove = []
        for k, entry in self._store.items():
            expires = _parse_iso(entry.expires_at)
            if expires is not None and now > expires:
                to_remove.append(k)
        for k in to_remove:
            self._store.pop(k, None)
        return len(to_remove)

    def get_metadata(self) -> dict:
        return {
            "cache_type": "InMemoryProviderCache",
            "schema_version": "1.3.2",
            "entry_count": len(self._store),
            "ttl_by_capability": dict(self.TTL_BY_CAPABILITY),
            "default_ttl": self.DEFAULT_TTL,
        }

    def stats(self) -> dict:
        return {
            "hits": self._hits,
            "misses": self._misses,
            "stale_hits": self._stale_hits,
            "bypasses": self._bypasses,
            "entry_count": len(self._store),
        }

    def bypass_note(self) -> None:
        """Track a force_refresh bypass."""
        self._bypasses += 1
