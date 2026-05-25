"""
realtime/realtime_engine.py - Real-time market data engine.

In mock mode, uses MockBroker to generate simulated market data.
In real mode, would use ShioajiClient (not implemented in v0.1).
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class RealtimeEngine:
    """
    Orchestrates real-time (or simulated) market data feeds.

    In mock_mode=True: uses MockBroker for all data.
    In mock_mode=False: attempts real broker (not implemented in v0.1, falls back to mock).
    """

    def __init__(self, mock_mode=True):
        """
        Initialize the engine.

        Parameters
        ----------
        mock_mode : bool
            If True, use MockBroker. If False, attempt real broker.
        """
        self.mock_mode = mock_mode
        self._running = False
        self._broker = None
        self._tick_buffers = {}
        self._bidask_buffer = None

        self._init_broker()
        self._init_buffers()

    def _init_broker(self):
        """Initialize broker (mock or real)."""
        from broker.mock_broker import MockBroker
        watchlist_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'config', 'watchlist.csv'
        )
        self._broker = MockBroker(watchlist_path=watchlist_path)

        if not self.mock_mode:
            logger.warning(
                "Real broker not implemented in v0.1. Falling back to MockBroker."
            )
        logger.info("RealtimeEngine initialized (mock_mode=%s).", self.mock_mode)

    def _init_buffers(self):
        """Initialize tick and bid/ask buffers."""
        from realtime.tick_buffer import TickBuffer
        from realtime.bidask_buffer import BidAskBuffer

        self._bidask_buffer = BidAskBuffer()
        for sym in self._broker._symbols:
            self._tick_buffers[sym] = TickBuffer(maxsize=500)

    def start(self):
        """
        Start the data feed.

        In mock mode, this simply marks the engine as running.
        Data is generated on-demand via get_snapshot().
        """
        self._running = True
        logger.info("RealtimeEngine started (mock_mode=%s).", self.mock_mode)

    def stop(self):
        """Stop the data feed."""
        self._running = False
        logger.info("RealtimeEngine stopped.")

    def get_snapshot(self, symbol):
        """
        Get the current market snapshot for a symbol.

        Parameters
        ----------
        symbol : str

        Returns
        -------
        MarketSnapshot
        """
        from realtime.market_snapshot import MarketSnapshot

        sym = str(symbol)
        snap_dict = self._broker.get_snapshot(sym)

        # Push tick to buffer
        if sym in self._tick_buffers:
            self._tick_buffers[sym].push({
                'price': snap_dict.get('price', 0),
                'volume': snap_dict.get('volume', 0),
                'timestamp': snap_dict.get('timestamp', datetime.now().isoformat()),
            })

        # Update bid/ask buffer
        self._bidask_buffer.update(sym, snap_dict)

        # Compute basic scores from mock data
        change_pct = float(snap_dict.get('change_pct', 0))
        volume = int(snap_dict.get('volume', 0))

        # Simple mock scoring based on change_pct
        daytrade_score = max(0, min(100, 50 + change_pct * 10))
        swing_score = max(0, min(100, 50 + change_pct * 5))
        risk_score = max(0, min(100, 50 - change_pct * 3))

        if change_pct > 2:
            decision = 'BUY'
        elif change_pct > 0.5:
            decision = 'WATCH'
        elif change_pct < -2:
            decision = 'AVOID'
        else:
            decision = 'HOLD'

        return MarketSnapshot(
            symbol=sym,
            name=snap_dict.get('name', sym),
            price=snap_dict.get('price', 0),
            prev_close=snap_dict.get('prev_close', 0),
            change_pct=change_pct,
            volume=volume,
            bid_1=snap_dict.get('bid_1', 0),
            ask_1=snap_dict.get('ask_1', 0),
            timestamp=snap_dict.get('timestamp', datetime.now().isoformat()),
            daytrade_score=round(daytrade_score, 1),
            swing_score=round(swing_score, 1),
            risk_score=round(risk_score, 1),
            decision=decision,
        )

    def get_all_snapshots(self):
        """
        Get market snapshots for all watchlist symbols.

        Returns
        -------
        list of MarketSnapshot
        """
        return [self.get_snapshot(sym) for sym in self._broker._symbols]
