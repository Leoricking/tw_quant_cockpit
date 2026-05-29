"""
data/api_cache.py - Simple TTL-based file cache for public API calls.

Avoids hammering public websites by caching responses to disk.

Usage:
    from data.api_cache import APICache
    cache = APICache()
    cached = cache.read_cache(key)
    if cached is None:
        data = fetch_from_api(...)
        cache.write_cache(key, data)
"""

import hashlib
import json
import logging
import os
import time
from typing import Any, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_CACHE_DIR = os.path.join(_BASE_DIR, "data_cache", "api")
_DEFAULT_TTL = 3600  # 1 hour


class APICache:
    """TTL-based file cache for public API call results."""

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        ttl_seconds: int = _DEFAULT_TTL,
    ):
        self.cache_dir = cache_dir or _DEFAULT_CACHE_DIR
        self.ttl_seconds = ttl_seconds
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_cache_key(self, *parts: str) -> str:
        """Generate a deterministic cache key from arbitrary string parts."""
        raw = "|".join(str(p) for p in parts)
        return hashlib.md5(raw.encode("utf-8")).hexdigest()

    def _cache_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{key}.json")

    def read_cache(
        self, key: str, force_refresh: bool = False
    ) -> Optional[Any]:
        """
        Return cached value if present and not expired, else None.

        Parameters
        ----------
        key : str
            Cache key (use get_cache_key to generate).
        force_refresh : bool
            If True, ignore existing cache and return None.
        """
        if force_refresh:
            return None
        path = self._cache_path(key)
        if not os.path.isfile(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as fh:
                payload = json.load(fh)
            ts = payload.get("_ts", 0)
            if time.time() - ts > self.ttl_seconds:
                logger.debug("APICache: expired key=%s", key)
                return None
            return payload.get("data")
        except Exception as exc:
            logger.debug("APICache.read_cache error key=%s: %s", key, exc)
            return None

    def write_cache(self, key: str, data: Any) -> None:
        """Write data to cache with current timestamp."""
        path = self._cache_path(key)
        try:
            payload = {"_ts": time.time(), "data": data}
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, default=str)
            logger.debug("APICache: wrote key=%s", key)
        except Exception as exc:
            logger.warning("APICache.write_cache error key=%s: %s", key, exc)

    def invalidate(self, key: str) -> None:
        """Remove a specific cache entry."""
        path = self._cache_path(key)
        try:
            if os.path.isfile(path):
                os.remove(path)
        except Exception as exc:
            logger.debug("APICache.invalidate error key=%s: %s", key, exc)

    def clear_all(self) -> int:
        """Remove all cache files. Returns count removed."""
        count = 0
        try:
            for fname in os.listdir(self.cache_dir):
                if fname.endswith(".json"):
                    os.remove(os.path.join(self.cache_dir, fname))
                    count += 1
        except Exception as exc:
            logger.warning("APICache.clear_all error: %s", exc)
        return count
