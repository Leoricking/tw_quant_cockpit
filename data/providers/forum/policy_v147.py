"""
data/providers/forum/policy_v147.py — Forum Fetch Policy v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No proxy rotation. No login. No CAPTCHA bypass.
[!] Conservative rate limits. cache_preferred=True.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
PROXY_ROTATION_ENABLED = False
LOGIN_ENABLED = False
CAPTCHA_BYPASS_ENABLED = False


@dataclass
class SourceFetchPolicy:
    """Per-source fetch policy."""
    source_id: str
    rate_limit_sec: float = 2.0  # minimum seconds between requests
    max_pages: int = 10
    max_articles: int = 100
    max_comments: int = 500
    request_budget: int = 50  # max requests per fetch run
    cache_preferred: bool = True
    dry_run_default: bool = True
    proxy_rotation: bool = False  # MUST be False
    login_required: bool = False  # MUST be False for PTT Stock
    captcha_bypass: bool = False  # MUST be False
    timeout_sec: float = 10.0
    retry_max: int = 2
    retry_after_sec: float = 5.0


# Default PTT Stock policy — conservative
_PTT_STOCK_POLICY = SourceFetchPolicy(
    source_id="ptt_stock",
    rate_limit_sec=2.0,
    max_pages=10,
    max_articles=100,
    max_comments=500,
    request_budget=50,
    cache_preferred=True,
    dry_run_default=True,
    proxy_rotation=False,
    login_required=False,
    captcha_bypass=False,
    timeout_sec=10.0,
    retry_max=2,
    retry_after_sec=5.0,
)


class ForumPolicy:
    """
    Forum fetch policy manager.
    [!] No proxy rotation. No login. No CAPTCHA bypass.
    """

    def __init__(self) -> None:
        self._policies: Dict[str, SourceFetchPolicy] = {
            "ptt_stock": _PTT_STOCK_POLICY,
        }

    def get_policy(self, source_id: str) -> SourceFetchPolicy:
        return self._policies.get(source_id, _PTT_STOCK_POLICY)

    def set_policy(self, policy: SourceFetchPolicy) -> None:
        # Enforce safety — never allow proxy/login/captcha bypass
        policy.proxy_rotation = False
        policy.captcha_bypass = False
        self._policies[policy.source_id] = policy

    def check_safety(self, source_id: str) -> bool:
        p = self.get_policy(source_id)
        return (
            not p.proxy_rotation
            and not p.captcha_bypass
        )
