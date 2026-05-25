"""
realtime/market_snapshot.py - Market snapshot data structure.

Represents a complete point-in-time market state for a single stock.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MarketSnapshot:
    """
    Complete market snapshot for a single stock at a point in time.

    Fields
    ------
    symbol : str
    name : str
    price : float
    prev_close : float
    change_pct : float
    volume : int
    bid_1 : float
    ask_1 : float
    timestamp : datetime or str
    daytrade_score : float (0-100)
    swing_score : float (0-100)
    risk_score : float (0-100, higher = more risk)
    decision : str (BUY/HOLD/SELL/WATCH/AVOID)
    """

    def __init__(
        self,
        symbol='',
        name='',
        price=0.0,
        prev_close=0.0,
        change_pct=0.0,
        volume=0,
        bid_1=0.0,
        ask_1=0.0,
        timestamp=None,
        daytrade_score=0.0,
        swing_score=0.0,
        risk_score=50.0,
        decision='WATCH',
    ):
        """Initialize market snapshot with all fields."""
        self.symbol = str(symbol)
        self.name = str(name)
        self.price = float(price or 0)
        self.prev_close = float(prev_close or 0)
        self.change_pct = float(change_pct or 0)
        self.volume = int(volume or 0)
        self.bid_1 = float(bid_1 or 0)
        self.ask_1 = float(ask_1 or 0)
        self.timestamp = timestamp or datetime.now().isoformat()
        self.daytrade_score = float(daytrade_score or 0)
        self.swing_score = float(swing_score or 0)
        self.risk_score = float(risk_score or 50)
        self.decision = str(decision or 'WATCH')

    def to_dict(self):
        """
        Convert snapshot to a plain dict.

        Returns
        -------
        dict
        """
        return {
            'symbol': self.symbol,
            'name': self.name,
            'price': self.price,
            'prev_close': self.prev_close,
            'change_pct': self.change_pct,
            'volume': self.volume,
            'bid_1': self.bid_1,
            'ask_1': self.ask_1,
            'timestamp': str(self.timestamp),
            'daytrade_score': self.daytrade_score,
            'swing_score': self.swing_score,
            'risk_score': self.risk_score,
            'decision': self.decision,
        }

    @classmethod
    def from_dict(cls, d):
        """Create a MarketSnapshot from a dict."""
        return cls(
            symbol=d.get('symbol', ''),
            name=d.get('name', ''),
            price=d.get('price', 0.0),
            prev_close=d.get('prev_close', 0.0),
            change_pct=d.get('change_pct', 0.0),
            volume=d.get('volume', 0),
            bid_1=d.get('bid_1', 0.0),
            ask_1=d.get('ask_1', 0.0),
            timestamp=d.get('timestamp'),
            daytrade_score=d.get('daytrade_score', 0.0),
            swing_score=d.get('swing_score', 0.0),
            risk_score=d.get('risk_score', 50.0),
            decision=d.get('decision', 'WATCH'),
        )

    def __repr__(self):
        return (
            f"MarketSnapshot({self.symbol} {self.name} price={self.price:.1f} "
            f"chg={self.change_pct:+.2f}% decision={self.decision})"
        )
