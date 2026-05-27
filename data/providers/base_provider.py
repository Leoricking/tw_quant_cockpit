"""
data/providers/base_provider.py - Abstract base class for all market data providers.

Every data source (CSV, XQ export, TWSE OpenAPI, Mega, etc.) must subclass
``BaseMarketDataProvider`` and implement the methods it needs.

Design principles:
    1. Missing data returns None — never raises an exception.
    2. Providers are read-only — no order submission, ever.
    3. All methods accept standard Python types (str, int, date) so callers
       do not need to know provider internals.
    4. ``health_check()`` must always succeed and return a dict.

TWQC_ENABLE_REAL_ORDER is permanently False.  No provider may submit orders.
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Safety constant — must never be set True in v1.
TWQC_ENABLE_REAL_ORDER: bool = False


class BaseMarketDataProvider:
    """
    Abstract base for all TW Quant Cockpit data providers.

    Subclasses override only the methods they support.  Every method that
    is not overridden returns ``None`` silently — callers must handle None.
    """

    # Human-readable name shown in provider-status output.
    name: str = "base"

    # Whether the provider can actually deliver data in the current session.
    is_available: bool = False

    # Whether the provider is scheduled / planned but not yet wired.
    is_planned: bool = False

    # ---------------------------------------------------------------------------
    # Core daily OHLCV
    # ---------------------------------------------------------------------------

    def get_daily(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ):
        """
        Return daily OHLCV data as a pandas DataFrame or None.

        Columns expected: date, open, high, low, close, volume, [symbol].
        """
        raise NotImplementedError

    # ---------------------------------------------------------------------------
    # Intraday / tick / bid-ask (optional — default None)
    # ---------------------------------------------------------------------------

    def get_intraday(self, symbol: str, date: Optional[str] = None):
        """Return intraday bars (per-minute) for one trading date, or None."""
        return None

    def get_ticks(self, symbol: str, date: Optional[str] = None):
        """Return tick-by-tick data for one trading date, or None."""
        return None

    def get_bidask(self, symbol: str):
        """Return latest 5-level bid/ask snapshot as dict, or None."""
        return None

    # ---------------------------------------------------------------------------
    # Chip / institutional data
    # ---------------------------------------------------------------------------

    def get_institutional(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ):
        """Return institutional flows DataFrame or None."""
        return None

    def get_margin(
        self,
        symbol: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ):
        """Return margin balance DataFrame or None."""
        return None

    # ---------------------------------------------------------------------------
    # Fundamentals
    # ---------------------------------------------------------------------------

    def get_monthly_revenue(self, symbol: str, months: int = 24):
        """Return monthly revenue DataFrame or None."""
        return None

    def get_holder(self, symbol: str):
        """Return holder structure DataFrame or None."""
        return None

    def get_trust_cost(self, symbol: str):
        """Return trust cost DataFrame or None."""
        return None

    def get_profile(self, symbol: str):
        """Return stock profile dict (name, market, industry, …) or None."""
        return None

    # ---------------------------------------------------------------------------
    # Health check
    # ---------------------------------------------------------------------------

    def health_check(self) -> dict:
        """
        Return a status dict describing this provider's availability.

        Must never raise an exception.  Returns at minimum:
            { "ok": bool, "provider": str, "available": bool, "note": str }
        """
        return {
            "ok": self.is_available,
            "provider": self.name,
            "available": self.is_available,
            "planned": self.is_planned,
            "real_order": False,
            "note": "Base provider — not implemented",
        }

    # ---------------------------------------------------------------------------
    # Order safety guard (read-only enforcement)
    # ---------------------------------------------------------------------------

    def submit_order(self, *args, **kwargs):  # noqa: ANN
        """
        Order submission is permanently disabled.

        This method exists to give a clear error when a caller mistakenly
        tries to submit an order via the provider interface.
        """
        raise RuntimeError(
            "Real order execution is DISABLED (TWQC_ENABLE_REAL_ORDER=False). "
            f"Provider '{self.name}' is read-only."
        )
