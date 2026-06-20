"""
data/providers/twse/daily_ohlcv_v140.py — TWSE daily OHLCV service v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from data.providers.twse.models_v140 import TWSEDailyBar
from data.providers.twse.normalizer_v140 import TWSENormalizer

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TWSEDailyOHLCVService:
    """In-memory daily OHLCV service for TWSE."""

    max_date_range_days: int = 365
    max_symbols: int = 100

    def __init__(self, dry_run: bool = True) -> None:
        self.dry_run = dry_run
        self._store: Dict[Tuple[str, str], TWSEDailyBar] = {}
        self._normalizer = TWSENormalizer()

    def get_bar(self, symbol: str, trade_date: str) -> Optional[TWSEDailyBar]:
        canonical = self._normalizer.canonical_symbol(symbol)
        return self._store.get((canonical, trade_date))

    def get_bars(self, symbol: str, start_date: str, end_date: str) -> List[TWSEDailyBar]:
        canonical = self._normalizer.canonical_symbol(symbol)
        return sorted(
            [
                bar
                for (sym, d), bar in self._store.items()
                if sym == canonical and start_date <= d <= end_date
            ],
            key=lambda b: b.trade_date,
        )

    def get_latest_bar(self, symbol: str) -> Optional[TWSEDailyBar]:
        canonical = self._normalizer.canonical_symbol(symbol)
        bars = [bar for (sym, _), bar in self._store.items() if sym == canonical]
        if not bars:
            return None
        return max(bars, key=lambda b: b.trade_date)

    def get_market_snapshot(self, trade_date: str) -> List[TWSEDailyBar]:
        return [bar for (_, d), bar in self._store.items() if d == trade_date]

    def upsert_bar(self, bar: TWSEDailyBar) -> None:
        canonical = self._normalizer.canonical_symbol(bar.symbol)
        self._store[(canonical, bar.trade_date)] = bar
