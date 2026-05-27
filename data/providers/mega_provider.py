"""
data/providers/mega_provider.py - Chiao-Tung Securities (兆豐證券) API provider skeleton.

STATUS: PLANNED — DISABLED in v0.3.4.

╔══════════════════════════════════════════════════════════════════════╗
║  READ ONLY FUTURE PROVIDER                                          ║
║  REAL ORDER DISABLED                                                ║
║  TWQC_ENABLE_REAL_ORDER = False  (permanent for v1)                ║
╚══════════════════════════════════════════════════════════════════════╝

This file reserves the interface for future Chiao-Tung Securities API
integration.  The provider will supply:

    - Real-time quote (即時行情)
    - 5-level bid/ask book (五檔委買委賣)
    - Tick-by-tick data (逐筆成交)
    - Intraday OHLCV bars (分K)

Roadmap (v0.4+):
    1. Implement get_daily() with historical OHLCV from Mega API.
    2. Implement get_intraday() with per-minute bars.
    3. Implement get_ticks() with tick stream.
    4. Implement get_bidask() with 5-level book snapshot.
    5. DO NOT implement submit_order() — orders remain disabled.

Safety guarantees:
    - This provider will never submit real orders.
    - No API credentials are stored or read in this file.
    - No connection is attempted in v0.3.4.
    - All methods return None until explicitly implemented.

DO NOT:
    - Add Shioaji (永豐API) integration here.
    - Add any order-submission capability, ever, without explicit approval.
    - Hard-code any API key or password.
    - Connect to broker systems from this file in v0.3.x.
"""

from __future__ import annotations

import logging
from typing import Optional

from data.providers.base_provider import BaseMarketDataProvider

logger = logging.getLogger(__name__)

# Safety flag — must remain False forever in v1.
_MEGA_ORDER_ENABLED: bool = False


class MegaProvider(BaseMarketDataProvider):
    """
    Skeleton provider for Chiao-Tung Securities (兆豐證券) API.

    DISABLED: No connection is made.  All methods return None.

    When implemented (v0.4+), this class will:
        - Call the Mega read-only API for real-time quotes and history.
        - Never call any order-submission endpoint.
        - Require explicit opt-in via environment variable (not set in v1).
    """

    name = "mega"
    is_available = False
    is_planned = True

    def get_daily(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ):
        """
        TODO (v0.4): Fetch daily OHLCV from Chiao-Tung Securities API.
        Returns None until implemented.
        """
        logger.debug("MegaProvider.get_daily: disabled in v0.3.x — returning None.")
        return None

    def get_intraday(self, symbol: str, date: Optional[str] = None):
        """
        TODO (v0.4): Fetch per-minute bars from Mega API.
        Returns None until implemented.
        """
        return None

    def get_ticks(self, symbol: str, date: Optional[str] = None):
        """
        TODO (v0.4): Fetch tick stream from Mega API.
        Returns None until implemented.
        """
        return None

    def get_bidask(self, symbol: str):
        """
        TODO (v0.4): Fetch 5-level bid/ask snapshot from Mega API.
        Returns None until implemented.
        """
        return None

    def health_check(self) -> dict:
        return {
            "ok": False,
            "provider": self.name,
            "available": False,
            "planned": True,
            "real_order": False,
            "order_enabled": _MEGA_ORDER_ENABLED,
            "note": (
                "PLANNED for v0.4+ — Chiao-Tung Securities (兆豐證券) read-only API. "
                "Real order execution permanently disabled. "
                "No connection attempted in v0.3.x."
            ),
        }

    def submit_order(self, *args, **kwargs):
        """Order submission is permanently disabled — raises RuntimeError."""
        raise RuntimeError(
            "MegaProvider: Real order execution is DISABLED. "
            "TWQC_ENABLE_REAL_ORDER=False. "
            "This provider is read-only and will never submit orders."
        )
