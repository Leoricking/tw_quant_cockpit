"""
data/providers/forum/source_registry_v147.py — Forum Source Registry v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Only allowlisted public sources permitted. Private boards rejected.
[!] PTT Stock pre-registered as SUPPLEMENTARY.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from data.providers.forum.models_v147 import ForumSource

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# Pre-registered sources
_PTT_STOCK_SOURCE = ForumSource(
    source_id="ptt_stock",
    display_name="PTT Stock Board",
    base_url="https://www.ptt.cc/bbs/Stock/",
    board_id="Stock",
    authority_level="SUPPLEMENTARY",
    is_public=True,
    is_private=False,
    requires_login=False,
    allowlisted=True,
    max_pages=10,
    max_articles=100,
    rate_limit_sec=2.0,
    notes="PTT公開股票板，僅供研究參考，非正式投資建議。",
)


class ForumSourceRegistry:
    """
    Registry of approved forum sources.
    [!] Only public, allowlisted boards may be registered.
    [!] Private boards are rejected automatically.
    """

    def __init__(self) -> None:
        self._sources: Dict[str, ForumSource] = {}
        # Pre-register PTT Stock
        self._sources[_PTT_STOCK_SOURCE.source_id] = _PTT_STOCK_SOURCE

    def register_source(self, source: ForumSource) -> bool:
        """
        Register a forum source. Returns True if registered, False if rejected.
        Rejects: private boards, non-allowlisted sources.
        """
        if source.is_private:
            logger.warning("ForumSourceRegistry: rejected private board source_id=%s", source.source_id)
            return False
        if not source.allowlisted:
            logger.warning("ForumSourceRegistry: rejected non-allowlisted source_id=%s", source.source_id)
            return False
        if source.authority_level not in ("SUPPLEMENTARY", "UNVERIFIED_PUBLIC_DISCUSSION"):
            logger.warning(
                "ForumSourceRegistry: rejected source_id=%s with invalid authority=%s",
                source.source_id, source.authority_level,
            )
            return False
        self._sources[source.source_id] = source
        return True

    def get_source(self, source_id: str) -> Optional[ForumSource]:
        return self._sources.get(source_id)

    def list_sources(self) -> List[ForumSource]:
        return list(self._sources.values())

    def is_allowlisted(self, source_id: str) -> bool:
        src = self._sources.get(source_id)
        return src is not None and src.allowlisted and not src.is_private
