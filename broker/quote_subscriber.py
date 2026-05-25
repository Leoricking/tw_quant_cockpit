"""
broker/quote_subscriber.py - Quote subscription interface.

Falls back to MockBroker when real broker is unavailable or mode is 'mock'.
"""

import os
import logging

logger = logging.getLogger(__name__)


class QuoteSubscriber:
    """
    Interface for subscribing to real-time tick and bid/ask data.

    In mock mode (TWQC_MODE=mock or no real broker), uses MockBroker
    to generate simulated data.
    """

    def __init__(self):
        """Initialize subscriber, selecting mock or real broker."""
        mode = os.environ.get('TWQC_MODE', 'mock').lower()
        self._use_mock = (mode == 'mock')
        self._mock_broker = None
        self._real_broker = None
        self._subscribed_tick = []
        self._subscribed_bidask = []

        if self._use_mock:
            self._init_mock()
        else:
            self._try_init_real()

    def _init_mock(self):
        """Initialize the mock broker."""
        try:
            from broker.mock_broker import MockBroker
            watchlist_path = os.environ.get(
                'TWQC_DEFAULT_WATCHLIST',
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             'config', 'watchlist.csv')
            )
            self._mock_broker = MockBroker(watchlist_path=watchlist_path)
            logger.info("QuoteSubscriber: using MockBroker.")
        except Exception as exc:
            logger.error("Failed to initialize MockBroker: %s", exc)

    def _try_init_real(self):
        """Attempt to initialize real broker; fall back to mock on failure."""
        try:
            from broker.shioaji_client import ShioajiClient
            self._real_broker = ShioajiClient()
            logger.info("QuoteSubscriber: real broker client created (login not attempted).")
        except Exception as exc:
            logger.warning("Real broker init failed (%s). Falling back to MockBroker.", exc)
            self._use_mock = True
            self._init_mock()

    def subscribe_tick(self, symbols):
        """
        Subscribe to tick data for a list of symbols.

        In mock mode, records the subscription list; data is polled via get_tick().

        Parameters
        ----------
        symbols : list of str
        """
        self._subscribed_tick = [str(s) for s in symbols]
        logger.info("Subscribed to tick data for %d symbols (mock=%s).", len(symbols), self._use_mock)

    def subscribe_bidask(self, symbols):
        """
        Subscribe to bid/ask data for a list of symbols.

        Parameters
        ----------
        symbols : list of str
        """
        self._subscribed_bidask = [str(s) for s in symbols]
        logger.info("Subscribed to bid/ask data for %d symbols (mock=%s).", len(symbols), self._use_mock)

    def unsubscribe(self, symbols):
        """
        Unsubscribe from tick and bid/ask data for given symbols.

        Parameters
        ----------
        symbols : list of str
        """
        sym_set = set(str(s) for s in symbols)
        self._subscribed_tick = [s for s in self._subscribed_tick if s not in sym_set]
        self._subscribed_bidask = [s for s in self._subscribed_bidask if s not in sym_set]
        logger.info("Unsubscribed from %d symbols.", len(sym_set))

    def reconnect(self):
        """
        Reconnect to the broker. In mock mode, reinitializes MockBroker.
        """
        logger.info("QuoteSubscriber.reconnect() called.")
        if self._use_mock:
            self._init_mock()
        else:
            self._try_init_real()

    def get_tick(self, symbol):
        """
        Get latest tick for a symbol (mock mode only).

        Returns
        -------
        dict or None
        """
        if self._mock_broker:
            return self._mock_broker.generate_mock_tick(symbol)
        return None

    def get_bidask(self, symbol):
        """
        Get latest bid/ask for a symbol (mock mode only).

        Returns
        -------
        dict or None
        """
        if self._mock_broker:
            return self._mock_broker.generate_mock_bidask(symbol)
        return None
