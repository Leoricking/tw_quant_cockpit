"""
data/providers/forum/ptt/provider_v147.py — PTTStockProvider v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] dry_run=True default. SUPPLEMENTARY authority. Public board only.
[!] No login, no proxy, no CAPTCHA bypass, no credentials.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FORUM_CAN_GENERATE_BUY_SELL = False
FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE = False
FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED = False


class PTTStockProvider:
    """
    Data provider for PTT Stock public board.
    [!] dry_run=True by default.
    [!] authority=SUPPLEMENTARY always.
    [!] public=True, is_private=False always.
    [!] No login bypass, no proxy, no credentials.
    """

    AUTHORITY = "SUPPLEMENTARY"
    IS_PUBLIC = True
    IS_PRIVATE = False
    REQUIRES_LOGIN = False
    BOARD = "Stock"
    BASE_URL = "https://www.ptt.cc/bbs/Stock/"

    def __init__(
        self,
        dry_run: bool = True,
        max_pages: int = 10,
        max_articles: int = 100,
        store=None,
        governance=None,
    ) -> None:
        self._dry_run = dry_run
        self._max_pages = max_pages
        self._max_articles = max_articles
        from data.providers.forum.ptt.client_v147 import PTTClient
        self._client = PTTClient(dry_run=dry_run, governance=governance)
        from data.providers.forum.ptt.list_parser_v147 import PTTListParser
        self._list_parser = PTTListParser()
        from data.providers.forum.ptt.article_parser_v147 import PTTArticleParser
        self._article_parser = PTTArticleParser()
        from data.providers.forum.ptt.push_parser_v147 import PTTPushParser
        self._push_parser = PTTPushParser()
        from data.providers.forum.ptt.pagination_v147 import PTTPagination
        self._pagination = PTTPagination(max_pages=max_pages)
        if store is None:
            from data.providers.forum.store_v147 import ForumStore
            store = ForumStore()
        self._store = store

    def plan(self, pages: int = 2) -> Dict[str, Any]:
        """
        Build a dry-run fetch plan. Returns plan without executing.
        [!] No real HTTP in plan mode.
        """
        return {
            "provider": "ptt_stock",
            "authority": self.AUTHORITY,
            "board": self.BOARD,
            "base_url": self.BASE_URL,
            "pages_requested": pages,
            "pages_actual": min(pages, self._max_pages),
            "max_articles": self._max_articles,
            "dry_run": True,
            "requires_login": False,
            "proxy_used": False,
            "captcha_bypass": False,
            "credentials_stored": False,
            "formal_standalone_allowed": False,
            "can_generate_buy_sell": False,
            "can_override_official": False,
        }

    def fetch(self, pages: int = 2) -> Dict[str, Any]:
        """
        Fetch PTT board index and articles.
        [!] dry_run=True: returns plan only, no real HTTP.
        [!] authority=SUPPLEMENTARY always.
        """
        run_id = self._store.start_fetch_run("ptt_stock", dry_run=self._dry_run)
        articles_found = 0
        pages_fetched = 0
        errors = []

        if self._dry_run:
            self._store.complete_fetch_run(run_id, 0, 0, "DRY_RUN")
            return {
                "run_id": run_id,
                "status": "DRY_RUN",
                "articles_found": 0,
                "pages_fetched": 0,
                "dry_run": True,
                "authority": self.AUTHORITY,
                "formal_standalone_allowed": False,
                "message": "Dry run: no real HTTP fetch performed.",
            }

        pages_to_fetch = min(pages, self._max_pages)

        for page_num in range(1, pages_to_fetch + 1):
            response = self._client.fetch_board_index(page=page_num)
            if response.get("status") not in ("OK",):
                errors.append(f"Page {page_num}: {response.get('error', response.get('status'))}")
                break
            pages_fetched += 1
            parse_result = self._list_parser.parse(response.get("html", ""))
            for row in parse_result.get("articles", []):
                articles_found += 1
                if articles_found >= self._max_articles:
                    break
            if articles_found >= self._max_articles:
                break

        self._store.complete_fetch_run(run_id, articles_found, pages_fetched,
                                       "COMPLETE" if not errors else "PARTIAL",
                                       "; ".join(errors))
        return {
            "run_id": run_id,
            "status": "COMPLETE" if not errors else "PARTIAL",
            "articles_found": articles_found,
            "pages_fetched": pages_fetched,
            "errors": errors,
            "dry_run": self._dry_run,
            "authority": self.AUTHORITY,
            "formal_standalone_allowed": False,
        }

    def health_check(self) -> Dict[str, Any]:
        """Offline health check for PTT provider."""
        checks = {}
        checks["authority_supplementary"] = self.AUTHORITY == "SUPPLEMENTARY"
        checks["is_public"] = self.IS_PUBLIC is True
        checks["is_private"] = self.IS_PRIVATE is False
        checks["no_login"] = self.REQUIRES_LOGIN is False
        checks["dry_run_default"] = self._dry_run is True
        checks["no_buy_sell"] = FORUM_CAN_GENERATE_BUY_SELL is False
        checks["no_override_official"] = FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE is False
        checks["no_formal_standalone"] = FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED is False
        all_pass = all(checks.values())
        return {
            "provider": "ptt_stock",
            "authority": self.AUTHORITY,
            "board": self.BOARD,
            "dry_run": self._dry_run,
            "checks": checks,
            "healthy": all_pass,
        }
