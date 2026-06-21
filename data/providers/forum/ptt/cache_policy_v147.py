"""
data/providers/forum/ptt/cache_policy_v147.py — PTTCachePolicy v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] cache_preferred=True. TTL by type. No auto-refresh.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

NO_REAL_ORDERS = True
CACHE_AUTO_REFRESH_ENABLED = False  # ALWAYS FALSE


class PTTCachePolicy:
    """
    Cache policy for PTT data fetching.
    [!] cache_preferred=True: use cache before hitting server.
    [!] No auto-refresh. All refresh is explicit.
    """

    cache_preferred: bool = True
    auto_refresh_enabled: bool = False  # ALWAYS FALSE

    # TTL in seconds by content type
    TTL = {
        "board_index": 300,         # 5 minutes
        "article": 3600,            # 1 hour
        "article_hot": 600,         # 10 minutes (popular articles)
        "deleted_article": 86400,   # 24 hours (deleted = stable)
        "article_list_page": 600,   # 10 minutes
    }

    # Max cache size in items
    MAX_SIZE = {
        "board_index": 50,
        "article": 500,
        "article_hot": 100,
    }

    def get_ttl(self, content_type: str) -> int:
        """Get TTL in seconds for a content type."""
        return self.TTL.get(content_type, 1800)

    def get_max_size(self, content_type: str) -> int:
        """Get max cache size for a content type."""
        return self.MAX_SIZE.get(content_type, 200)

    def should_use_cache(self, content_type: str, age_seconds: float) -> bool:
        """
        Determine if cache should be used.
        [!] Returns True (prefer cache) if within TTL.
        """
        ttl = self.get_ttl(content_type)
        return age_seconds < ttl

    def describe(self) -> Dict[str, Any]:
        return {
            "cache_preferred": self.cache_preferred,
            "auto_refresh_enabled": self.auto_refresh_enabled,
            "ttl": self.TTL,
            "max_size": self.MAX_SIZE,
        }
