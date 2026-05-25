"""
broker/mock_broker.py - Mock broker for paper trading simulation.

Generates realistic mock ticks, bid/ask data, and market snapshots for
Taiwan stocks based on random-walk price simulation.
"""

import os
import random
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Seed prices for well-known Taiwan stocks
_SEED_PRICES = {
    '2330': 850.0,
    '2454': 1050.0,
    '2382': 280.0,
    '2317': 210.0,
    '6669': 1200.0,
    '3661': 2100.0,
    '2345': 580.0,
    '3017': 190.0,
    '2308': 390.0,
    '2383': 470.0,
}

_STOCK_NAMES = {
    '2330': '台積電',
    '2454': '聯發科',
    '2382': '廣達',
    '2317': '鴻海',
    '6669': '緯穎',
    '3661': '世芯-KY',
    '2345': '智邦',
    '3017': '奇鋐',
    '2308': '台達電',
    '2383': '台光電',
}


class MockBroker:
    """
    Mock broker that generates simulated market data for Taiwan stocks.

    Uses a random-walk model seeded per symbol to produce consistent
    but slightly varying prices across calls.
    """

    def __init__(self, watchlist_path=None, tick_interval=1.0):
        """
        Initialize MockBroker.

        Parameters
        ----------
        watchlist_path : str, optional
            Path to watchlist CSV file. If None, uses default seed price symbols.
        tick_interval : float
            Simulation tick interval in seconds (not used for sleep, just metadata).
        """
        self.tick_interval = tick_interval
        self._prices = dict(_SEED_PRICES)
        self._symbols = list(_SEED_PRICES.keys())
        self._names = dict(_STOCK_NAMES)

        if watchlist_path and os.path.isfile(watchlist_path):
            self._load_watchlist(watchlist_path)

        logger.info("MockBroker initialized with %d symbols.", len(self._symbols))

    def _load_watchlist(self, path):
        """Load symbols from a CSV watchlist file."""
        try:
            import pandas as pd
            df = pd.read_csv(path, dtype={'symbol': str})
            if 'enabled' in df.columns:
                df = df[df['enabled'].astype(str) == '1']
            self._symbols = [str(s).strip() for s in df['symbol'].tolist()]
            if 'name' in df.columns:
                for _, row in df.iterrows():
                    sym = str(row['symbol']).strip()
                    self._names[sym] = str(row.get('name', sym))
            # Ensure seed prices exist for all symbols
            for sym in self._symbols:
                if sym not in self._prices:
                    self._prices[sym] = 100.0  # default seed
            logger.debug("Loaded watchlist with %d symbols from %s.", len(self._symbols), path)
        except Exception as exc:
            logger.warning("Failed to load watchlist from %s: %s", path, exc)

    def _get_current_price(self, symbol):
        """Get the current simulated price for a symbol with small random walk."""
        sym = str(symbol)
        base = self._prices.get(sym, 100.0)
        # Daily drift: small random walk bounded within ±3%
        seed_val = hash(sym + str(datetime.now().minute)) % 1000
        rng = random.Random(seed_val)
        change_pct = rng.gauss(0.0002, 0.008)  # slight upward drift
        change_pct = max(-0.03, min(0.03, change_pct))
        new_price = round(base * (1 + change_pct), 1)
        self._prices[sym] = new_price
        return new_price

    def generate_mock_tick(self, symbol):
        """
        Generate a mock market tick for a symbol.

        Parameters
        ----------
        symbol : str or int
            Stock symbol.

        Returns
        -------
        dict with keys: symbol, price, volume, timestamp, change_pct
        """
        sym = str(symbol)
        base_price = _SEED_PRICES.get(sym, 100.0)
        price = self._get_current_price(sym)
        change_pct = (price - base_price) / base_price * 100.0

        seed_vol = hash(sym + str(datetime.now().second)) % 10000
        rng = random.Random(seed_vol)
        volume = rng.randint(100, 5000) * 1000  # in shares

        return {
            'symbol': sym,
            'price': price,
            'volume': volume,
            'timestamp': datetime.now().isoformat(),
            'change_pct': round(change_pct, 2),
        }

    def generate_mock_bidask(self, symbol):
        """
        Generate a 5-level mock bid/ask order book for a symbol.

        Parameters
        ----------
        symbol : str or int
            Stock symbol.

        Returns
        -------
        dict with keys: bid_price_1..5, bid_volume_1..5, ask_price_1..5, ask_volume_1..5
        """
        sym = str(symbol)
        price = self._get_current_price(sym)
        tick_size = self._get_tick_size(price)

        seed_ob = hash(sym + str(datetime.now().minute) + 'ob') % 9999
        rng = random.Random(seed_ob)

        result = {}
        for i in range(1, 6):
            bid_p = round(price - tick_size * i, 1)
            ask_p = round(price + tick_size * i, 1)
            bid_v = rng.randint(50, 800)
            ask_v = rng.randint(50, 800)
            result[f'bid_price_{i}'] = bid_p
            result[f'bid_volume_{i}'] = bid_v
            result[f'ask_price_{i}'] = ask_p
            result[f'ask_volume_{i}'] = ask_v

        return result

    def _get_tick_size(self, price):
        """Return Taiwan stock exchange tick size for a given price level."""
        if price < 10:
            return 0.01
        elif price < 50:
            return 0.05
        elif price < 100:
            return 0.1
        elif price < 500:
            return 0.5
        elif price < 1000:
            return 1.0
        else:
            return 5.0

    def get_all_ticks(self):
        """
        Get mock ticks for all watchlist symbols.

        Returns
        -------
        list of dicts (one per symbol)
        """
        return [self.generate_mock_tick(sym) for sym in self._symbols]

    def get_snapshot(self, symbol):
        """
        Get a complete mock market snapshot for a symbol.

        Returns
        -------
        dict with: symbol, name, price, prev_close, change_pct, volume,
                   bid_1, ask_1, timestamp, plus full bidask dict
        """
        sym = str(symbol)
        tick = self.generate_mock_tick(sym)
        bidask = self.generate_mock_bidask(sym)

        base_price = _SEED_PRICES.get(sym, 100.0)
        prev_close = round(base_price * (1 + random.gauss(0, 0.005)), 1)

        snapshot = {
            'symbol': sym,
            'name': self._names.get(sym, sym),
            'price': tick['price'],
            'prev_close': prev_close,
            'change_pct': tick['change_pct'],
            'volume': tick['volume'],
            'bid_1': bidask.get('bid_price_1', tick['price'] * 0.999),
            'ask_1': bidask.get('ask_price_1', tick['price'] * 1.001),
            'timestamp': tick['timestamp'],
        }
        snapshot.update(bidask)
        return snapshot
