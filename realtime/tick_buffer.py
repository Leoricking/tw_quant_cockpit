"""
realtime/tick_buffer.py - Circular buffer for real-time tick data.

Stores recent ticks and computes OHLCV aggregates.
"""

import logging
from collections import deque
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TickBuffer:
    """
    Circular buffer storing the most recent ticks for a single symbol.

    Parameters
    ----------
    maxsize : int
        Maximum number of ticks to retain (circular, oldest evicted).
    """

    def __init__(self, maxsize=1000):
        """Initialize the buffer with a maximum size."""
        self.maxsize = maxsize
        self._buffer = deque(maxlen=maxsize)

    def push(self, tick_dict):
        """
        Add a tick to the buffer.

        Parameters
        ----------
        tick_dict : dict
            Tick data with at minimum: price (float), volume (int), timestamp (str or datetime).
        """
        if not isinstance(tick_dict, dict):
            logger.warning("TickBuffer.push: expected dict, got %s", type(tick_dict))
            return
        # Ensure timestamp is datetime
        ts = tick_dict.get('timestamp')
        if ts is None:
            tick_dict = dict(tick_dict)
            tick_dict['timestamp'] = datetime.now()
        elif isinstance(ts, str):
            tick_dict = dict(tick_dict)
            try:
                tick_dict['timestamp'] = datetime.fromisoformat(ts)
            except Exception:
                tick_dict['timestamp'] = datetime.now()
        self._buffer.append(tick_dict)

    def get_recent(self, n=60):
        """
        Get the last n ticks.

        Parameters
        ----------
        n : int
            Number of recent ticks to return.

        Returns
        -------
        list of dicts
        """
        buf = list(self._buffer)
        return buf[-n:] if len(buf) >= n else buf

    def get_ohlcv(self, window_seconds=60):
        """
        Compute OHLCV aggregate from recent ticks within a time window.

        Parameters
        ----------
        window_seconds : int
            Number of seconds to look back.

        Returns
        -------
        dict with keys: open, high, low, close, volume, tick_count
            Returns None if no ticks in window.
        """
        cutoff = datetime.now() - timedelta(seconds=window_seconds)
        ticks = [t for t in self._buffer if t.get('timestamp', datetime.min) >= cutoff]

        if not ticks:
            return None

        prices = []
        volumes = []
        for t in ticks:
            p = t.get('price')
            v = t.get('volume', 0)
            if p is not None:
                try:
                    prices.append(float(p))
                    volumes.append(int(v or 0))
                except (TypeError, ValueError):
                    pass

        if not prices:
            return None

        return {
            'open': prices[0],
            'high': max(prices),
            'low': min(prices),
            'close': prices[-1],
            'volume': sum(volumes),
            'tick_count': len(ticks),
        }

    def clear(self):
        """Clear all ticks from the buffer."""
        self._buffer.clear()

    def __len__(self):
        return len(self._buffer)
