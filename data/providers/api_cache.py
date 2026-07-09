"""
data/providers/api_cache.py - Provider-level API response cache (v0.4.1).

Stores API responses to disk with TTL expiry.
Cache keys never include full tokens.
Cache directory is excluded from git.

[!] Read Only. No Real Orders.
[!] Cache key must not contain full token.
[!] Cache metadata must not contain full token.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DEFAULT_CACHE_ROOT = os.path.join(_BASE_DIR, "data_cache", "api")
_DEFAULT_TTL = 86400  # 24 hours


class APICache:
    """
    Provider-level TTL-based file cache for API responses.

    Parameters
    ----------
    cache_root   : Root directory for cache files
    ttl_seconds  : Default TTL in seconds (default: 86400 = 24h)
    enabled      : If False, all get() calls return None (cache disabled)

    Safety:
        - cache key never contains full token
        - metadata never contains full token
        - cache directory is gitignored
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        cache_root:   str = _DEFAULT_CACHE_ROOT,
        ttl_seconds:  int = _DEFAULT_TTL,
        enabled:      bool = True,
    ):
        self._root       = cache_root
        self._ttl        = max(1, ttl_seconds)
        self._enabled    = enabled
        self._hits       = 0
        self._misses     = 0
        self._writes     = 0
        self._errors     = 0

        if self._enabled:
            try:
                os.makedirs(self._root, exist_ok=True)
            except Exception as exc:
                logger.warning("APICache: cannot create cache dir %s: %s", self._root, exc)
                self._enabled = False

    # ------------------------------------------------------------------
    # Key building
    # ------------------------------------------------------------------

    def build_key(self, provider: str, dataset: str, params: Any) -> str:
        """
        Build a deterministic cache key.
        Never includes full token values — params are hashed.
        """
        # Sanitize params to remove any token-like fields
        safe_params = self._sanitize_params(params)
        raw = f"{provider}|{dataset}|{json.dumps(safe_params, sort_keys=True, default=str)}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]

    @staticmethod
    def _sanitize_params(params: Any) -> Any:
        """Remove token/password fields from params before hashing."""
        if isinstance(params, dict):
            cleaned = {}
            for k, v in params.items():
                k_lower = str(k).lower()
                if any(kw in k_lower for kw in ("token", "password", "secret", "key", "auth")):
                    cleaned[k] = "<redacted>"
                else:
                    cleaned[k] = v
            return cleaned
        return params

    # ------------------------------------------------------------------
    # Get / Set
    # ------------------------------------------------------------------

    def get(
        self,
        provider: str,
        dataset:  str,
        params:   Any,
    ) -> Optional[Any]:
        """
        Return cached value if present and not expired.
        Returns None on cache miss, expiry, or if disabled.
        """
        if not self._enabled:
            return None

        key  = self.build_key(provider, dataset, params)
        path = self._cache_path(key)

        if not os.path.isfile(path):
            self._misses += 1
            return None

        try:
            with open(path, encoding="utf-8") as f:
                envelope = json.load(f)
            stored_at = envelope.get("stored_at_ts", 0)
            ttl       = envelope.get("ttl_seconds",  self._ttl)
            if time.time() - stored_at > ttl:
                self._misses += 1
                return None  # expired
            self._hits += 1
            return envelope.get("data")
        except Exception as exc:
            logger.debug("APICache.get: read error %s: %s", path, exc)
            self._errors += 1
            self._misses += 1
            return None

    def set(
        self,
        provider:  str,
        dataset:   str,
        params:    Any,
        data:      Any,
        metadata:  Optional[dict] = None,
    ) -> bool:
        """
        Write data to cache.
        metadata must not contain full token (enforced by _sanitize_params).
        """
        if not self._enabled:
            return False

        key  = self.build_key(provider, dataset, params)
        path = self._cache_path(key)

        safe_meta = {}
        if metadata:
            safe_meta = {
                k: v for k, v in metadata.items()
                if not any(kw in str(k).lower() for kw in ("token", "password", "secret", "key", "auth"))
            }

        envelope = {
            "provider":    provider,
            "dataset":     dataset,
            "stored_at":   datetime.now(timezone.utc).isoformat(),
            "stored_at_ts": time.time(),
            "ttl_seconds": self._ttl,
            "metadata":    safe_meta,
            "data":        data,
        }

        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(envelope, f, default=str)
            self._writes += 1
            return True
        except Exception as exc:
            logger.debug("APICache.set: write error %s: %s", path, exc)
            self._errors += 1
            return False

    # ------------------------------------------------------------------
    # Invalidate / cleanup
    # ------------------------------------------------------------------

    def invalidate(
        self,
        provider: Optional[str] = None,
        dataset:  Optional[str] = None,
    ) -> int:
        """
        Invalidate cache entries.
        If provider+dataset given: invalidate matching entries.
        If only provider: invalidate all entries for that provider.
        If neither: invalidate ALL entries.
        Returns count of files removed.
        """
        if not self._enabled or not os.path.isdir(self._root):
            return 0

        removed = 0
        try:
            for fname in os.listdir(self._root):
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(self._root, fname)
                if provider is None and dataset is None:
                    try:
                        os.remove(fpath)
                        removed += 1
                    except Exception:
                        pass
                    continue
                # Read envelope to check provider/dataset
                try:
                    with open(fpath, encoding="utf-8") as f:
                        envelope = json.load(f)
                    ep = envelope.get("provider", "")
                    ed = envelope.get("dataset",  "")
                    match_p = (provider is None or ep == provider)
                    match_d = (dataset  is None or ed == dataset)
                    if match_p and match_d:
                        os.remove(fpath)
                        removed += 1
                except Exception:
                    pass
        except Exception as exc:
            logger.debug("APICache.invalidate: %s", exc)

        return removed

    def cleanup_expired(self) -> int:
        """Remove all expired cache entries. Returns count removed."""
        if not self._enabled or not os.path.isdir(self._root):
            return 0

        removed = 0
        now     = time.time()
        try:
            for fname in os.listdir(self._root):
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(self._root, fname)
                try:
                    with open(fpath, encoding="utf-8") as f:
                        envelope = json.load(f)
                    stored_at = envelope.get("stored_at_ts", 0)
                    ttl       = envelope.get("ttl_seconds",  self._ttl)
                    if now - stored_at > ttl:
                        os.remove(fpath)
                        removed += 1
                except Exception:
                    pass
        except Exception as exc:
            logger.debug("APICache.cleanup_expired: %s", exc)

        return removed

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        """Return cache statistics."""
        total_entries = 0
        expired       = 0
        size_bytes    = 0
        now           = time.time()

        if self._enabled and os.path.isdir(self._root):
            try:
                for fname in os.listdir(self._root):
                    if not fname.endswith(".json"):
                        continue
                    fpath = os.path.join(self._root, fname)
                    total_entries += 1
                    try:
                        size_bytes += os.path.getsize(fpath)
                        with open(fpath, encoding="utf-8") as f:
                            envelope = json.load(f)
                        stored_at = envelope.get("stored_at_ts", 0)
                        ttl       = envelope.get("ttl_seconds",  self._ttl)
                        if now - stored_at > ttl:
                            expired += 1
                    except Exception:
                        pass
            except Exception as exc:
                logger.debug("APICache.stats: %s", exc)

        return {
            "enabled":       self._enabled,
            "cache_root":    self._root,
            "ttl_seconds":   self._ttl,
            "total_entries": total_entries,
            "expired":       expired,
            "active":        max(0, total_entries - expired),
            "size_bytes":    size_bytes,
            "hits":          self._hits,
            "misses":        self._misses,
            "writes":        self._writes,
            "errors":        self._errors,
            "hit_rate":      round(self._hits / max(1, self._hits + self._misses), 3),
            "no_token_in_keys": True,
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _cache_path(self, key: str) -> str:
        return os.path.join(self._root, f"{key}.json")
