"""
realtime/bidask_buffer.py - Latest bid/ask snapshot storage.

Stores the most recent bid/ask data for each symbol.
"""

import logging

logger = logging.getLogger(__name__)


class BidAskBuffer:
    """
    Stores the latest bid/ask snapshot for each subscribed symbol.

    Thread-safe for single-writer, multiple-reader usage in mock mode.
    """

    def __init__(self):
        """Initialize empty bid/ask buffer."""
        self._data = {}

    def update(self, symbol, bidask_dict):
        """
        Update the latest bid/ask snapshot for a symbol.

        Parameters
        ----------
        symbol : str
            Stock symbol.
        bidask_dict : dict
            Standard 5-level bid/ask dict.
        """
        sym = str(symbol)
        if not isinstance(bidask_dict, dict):
            logger.warning("BidAskBuffer.update: expected dict for symbol %s.", sym)
            return
        self._data[sym] = dict(bidask_dict)

    def get(self, symbol):
        """
        Get the latest bid/ask snapshot for a symbol.

        Parameters
        ----------
        symbol : str

        Returns
        -------
        dict or None
        """
        return self._data.get(str(symbol))

    def get_all(self):
        """
        Get all latest bid/ask snapshots.

        Returns
        -------
        dict mapping symbol -> bidask_dict
        """
        return dict(self._data)

    def clear(self):
        """Clear all stored bid/ask data."""
        self._data.clear()

    def __len__(self):
        return len(self._data)
