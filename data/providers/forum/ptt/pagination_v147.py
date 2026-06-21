"""
data/providers/forum/ptt/pagination_v147.py — PTTPagination v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] max_pages enforcement prevents excessive crawling.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class PTTPagination:
    """
    Handles PTT board pagination.
    [!] max_pages enforced to prevent excessive server load.
    """

    DEFAULT_MAX_PAGES = 10

    def __init__(self, max_pages: int = DEFAULT_MAX_PAGES) -> None:
        self._max_pages = max_pages

    def extract_links(self, html: str) -> Dict[str, Optional[str]]:
        """Extract prev/next page links from board HTML."""
        prev_page: Optional[str] = None
        next_page: Optional[str] = None

        # PTT pagination buttons: 上頁 (prev) and 下頁 (next)
        prev_m = re.search(
            r'<a[^>]*href="(/bbs/Stock/index(\d+)\.html)"[^>]*>[^<]*上頁[^<]*</a>',
            html
        )
        if prev_m:
            prev_page = "https://www.ptt.cc" + prev_m.group(1)

        next_m = re.search(
            r'<a[^>]*href="(/bbs/Stock/index(\d+)\.html)"[^>]*>[^<]*下頁[^<]*</a>',
            html
        )
        if next_m:
            next_page = "https://www.ptt.cc" + next_m.group(1)

        return {"prev_page": prev_page, "next_page": next_page}

    def get_page_urls(self, start_url: str, pages_requested: int) -> List[str]:
        """
        Generate a list of page URLs to fetch.
        [!] Capped at max_pages.
        """
        pages = min(pages_requested, self._max_pages)
        urls = [start_url]
        # Extract page number from start URL
        m = re.search(r'index(\d+)\.html', start_url)
        if m:
            start_page = int(m.group(1))
            for i in range(1, pages):
                page_num = start_page - i
                if page_num < 1:
                    break
                urls.append(f"https://www.ptt.cc/bbs/Stock/index{page_num}.html")
        return urls[:self._max_pages]

    def is_within_limit(self, pages_fetched: int) -> bool:
        """Check if pages fetched is within max_pages limit."""
        return pages_fetched < self._max_pages
