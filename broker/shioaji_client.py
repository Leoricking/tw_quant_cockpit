"""
broker/shioaji_client.py - Safe skeleton for Shioaji real broker client.

Real broker functionality is NOT implemented in v0.1.
All methods that would execute real orders raise NotImplementedError.
"""

import os
import logging

logger = logging.getLogger(__name__)


class ShioajiClient:
    """
    Safe skeleton client for the Shioaji broker API.

    Real trading is disabled in v0.1. This class exists only to provide
    the interface shape and safety guards.
    """

    def __init__(self):
        """Initialize and read environment config. Never connects automatically."""
        self.api_key = os.environ.get('SHIOAJI_API_KEY', '')
        self.secret_key = os.environ.get('SHIOAJI_SECRET_KEY', '')
        self.person_id = os.environ.get('SHIOAJI_PERSON_ID', '')
        self.enable_real_order = os.environ.get('TWQC_ENABLE_REAL_ORDER', 'false').lower() == 'true'
        self._logged_in = False

        if self.enable_real_order:
            logger.error(
                "TWQC_ENABLE_REAL_ORDER is set to true — this is FORBIDDEN in v0.1. "
                "Real orders will still be blocked by NotImplementedError."
            )

        logger.info("ShioajiClient (skeleton) initialized. Real trading: DISABLED.")

    def login(self):
        """
        Attempt broker login.

        Raises
        ------
        NotImplementedError
            Always. Real broker login is not implemented in v0.1.
        """
        raise NotImplementedError(
            "Real broker login not implemented in v0.1"
        )

    def place_order(self, *args, **kwargs):
        """
        Place a real order.

        Raises
        ------
        NotImplementedError
            Always. Real order placement is permanently disabled in v0.1.
        """
        raise NotImplementedError(
            "Real order placement is DISABLED. "
            "TWQC_ENABLE_REAL_ORDER must never be true in v0.1"
        )

    def get_quote(self, symbol):
        """
        Get real-time quote for a symbol.

        Returns None in v0.1. Use MockBroker for simulated quotes.

        Parameters
        ----------
        symbol : str
            Stock symbol.

        Returns
        -------
        None
        """
        logger.warning(
            "ShioajiClient.get_quote('%s') called — returning None. "
            "Use MockBroker for simulated data in v0.1.",
            symbol,
        )
        return None
