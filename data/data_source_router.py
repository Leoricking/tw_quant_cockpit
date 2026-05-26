"""
data/data_source_router.py - Routes data requests to real or mock sources.

In mock mode  : returns stable synthetic data for demo purposes.
In real mode  : queries the local SQLite DB / FinMind; returns None when
                data is unavailable so callers can apply DataCompletenessGate.

Usage
-----
    router = DataSourceRouter(mode='mock')
    price_data = router.get_price_data('2330', n_bars=60)
    chip_data  = router.get_chip_data('2330')

    router_real = DataSourceRouter(mode='real')
    price_data  = router_real.get_price_data('2330')   # None if DB empty
"""

import logging

logger = logging.getLogger(__name__)

__all__ = ["DataSourceRouter"]

# Seed prices used only for mock generation
_MOCK_BASE_PRICES = {
    '2330': 850.0, '2454': 1050.0, '2382': 280.0, '2317': 210.0,
    '6669': 1200.0, '3661': 2100.0, '2345': 580.0, '3017': 190.0,
    '2308': 390.0, '2383': 470.0, '3231': 95.0,   '2356': 55.0,
    '3443': 980.0, '3035': 210.0,  '2368': 75.0,  '3037': 135.0,
    '6213': 110.0, '3324': 320.0,  '3653': 400.0, '2421': 85.0,
    '2301': 95.0,  '6412': 260.0,  '2359': 210.0, '8374': 155.0,
    '1593': 55.0,  '2464': 75.0,   '2327': 580.0, '3036': 55.0,
    '3702': 50.0,  '6196': 180.0,
}


class DataSourceRouter:
    """
    Routes data requests to real or mock data sources.

    Parameters
    ----------
    mode : str
        ``'mock'`` — use stable synthetic data (always available).
        ``'real'`` — query DB / FinMind; return ``None`` if unavailable.
    """

    def __init__(self, mode: str = 'mock'):
        if mode not in ('mock', 'real'):
            raise ValueError(f"mode must be 'mock' or 'real', got: {mode!r}")
        self.mode = mode

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get_price_data(self, symbol: str, n_bars: int = 60):
        """
        Return a list of OHLCV dicts (newest last), or None if unavailable.

        In mock mode always returns synthetic data.
        In real mode: tries CSV import first, then DB. Returns None if both fail.
        No mock fallback in real mode.
        """
        if self.mode == 'mock':
            return self._mock_price(symbol, n_bars)
        return self._real_price(symbol, n_bars)

    def get_chip_data(self, symbol: str):
        """
        Return a chip data dict, or None if unavailable.

        Mock mode always returns None (chip scoring uses mock fallback).
        Real mode: tries CSV import first, then DB. Returns None if both fail.
        """
        if self.mode == 'mock':
            return None  # screener mock path uses mock scoring
        return self._real_chip(symbol)

    def get_fundamental_data(self, symbol: str):
        """Return fundamental dict or None."""
        if self.mode == 'mock':
            return None
        return self._real_fundamental(symbol)

    def get_profile(self, symbol: str):
        """
        Return stock profile dict (name, market, industry, theme_tags) or None.

        Real mode: reads CSV import. Mock mode: returns None (caller uses _STOCK_NAMES).
        """
        if self.mode == 'mock':
            return None
        try:
            from data.real_data_loader import RealDataLoader
            return RealDataLoader().load_profile(symbol)
        except Exception as exc:
            logger.debug("DataSourceRouter.get_profile error for %s: %s", symbol, exc)
            return None

    # ------------------------------------------------------------------
    # Mock generators
    # ------------------------------------------------------------------

    def _mock_price(self, symbol: str, n_bars: int):
        """Generate a stable synthetic OHLCV series."""
        import random as _rand
        from utils.stable_hash import stable_hash_int

        sym_str = str(symbol)
        base = _MOCK_BASE_PRICES.get(sym_str, 100.0)
        rng = _rand.Random(stable_hash_int(sym_str, mod=88888))
        price = base * rng.uniform(0.7, 0.9)
        bars = []
        for _ in range(n_bars):
            change = rng.gauss(0.003, 0.015)
            price = max(price * (1 + change), 1.0)
            h = round(price * rng.uniform(1.001, 1.02), 1)
            l = round(price * rng.uniform(0.98,  0.999), 1)
            o = round(price * rng.uniform(0.99,  1.01),  1)
            bars.append({
                'open': o, 'high': h, 'low': l,
                'close': round(price, 1),
                'volume': rng.randint(100, 10_000) * 1_000,
            })
        return bars

    # ------------------------------------------------------------------
    # Real data loaders (return None gracefully when DB is empty)
    # ------------------------------------------------------------------

    def _real_price(self, symbol: str, n_bars: int):
        # 1. Try CSV import first
        try:
            from data.real_data_loader import RealDataLoader
            rows = RealDataLoader().load_daily_k(symbol, n_bars=n_bars)
            if rows:
                logger.info("DataSourceRouter: loaded %d bars from CSV for %s", len(rows), symbol)
                return rows
        except Exception as exc:
            logger.debug("DataSourceRouter._real_price CSV error for %s: %s", symbol, exc)

        # 2. Fallback to DB
        try:
            from data.database import load_prices
            df = load_prices(stock_id=symbol)
            if df is None or df.empty:
                logger.info("DataSourceRouter: no real price data for %s in DB", symbol)
                return None
            df = df.tail(n_bars).reset_index(drop=True)
            records = []
            for _, row in df.iterrows():
                records.append({
                    'open':   float(row.get('open',   row.get('Open',   0))),
                    'high':   float(row.get('high',   row.get('High',   0))),
                    'low':    float(row.get('low',    row.get('Low',    0))),
                    'close':  float(row.get('close',  row.get('Close',  0))),
                    'volume': float(row.get('volume', row.get('Volume', 0))),
                })
            return records if records else None
        except Exception as exc:
            logger.debug("DataSourceRouter._real_price DB error for %s: %s", symbol, exc)
            return None

    def _real_chip(self, symbol: str):
        # 1. Try CSV import first
        try:
            from data.real_data_loader import RealDataLoader
            data = RealDataLoader().load_institutional(symbol)
            if data:
                logger.info("DataSourceRouter: loaded institutional data from CSV for %s", symbol)
                return data
        except Exception as exc:
            logger.debug("DataSourceRouter._real_chip CSV error for %s: %s", symbol, exc)

        # 2. Fallback to DB
        try:
            from data.database import load_chip_data
            data = load_chip_data(stock_id=symbol)
            if data is None or (hasattr(data, 'empty') and data.empty):
                return None
            return data if isinstance(data, dict) else data.to_dict(orient='records')
        except Exception as exc:
            logger.debug("DataSourceRouter._real_chip DB error for %s: %s", symbol, exc)
            return None

    def _real_fundamental(self, symbol: str):
        # 1. Try CSV import first
        try:
            from data.real_data_loader import RealDataLoader
            loader = RealDataLoader()
            rev = loader.load_monthly_revenue(symbol)
            if rev:
                logger.info("DataSourceRouter: loaded revenue data from CSV for %s", symbol)
                return rev
        except Exception as exc:
            logger.debug("DataSourceRouter._real_fundamental CSV error for %s: %s", symbol, exc)

        # 2. Fallback to DB
        try:
            from data.database import load_fundamental_data
            data = load_fundamental_data(stock_id=symbol)
            if data is None or (hasattr(data, 'empty') and data.empty):
                return None
            return data if isinstance(data, dict) else data.to_dict(orient='records')
        except Exception as exc:
            logger.debug("DataSourceRouter._real_fundamental DB error for %s: %s", symbol, exc)
            return None
