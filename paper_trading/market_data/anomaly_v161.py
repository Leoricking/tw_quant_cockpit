"""
paper_trading/market_data/anomaly_v161.py — Anomaly Detection v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Detects price and volume anomalies in canonical events.
"""
from __future__ import annotations
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from collections import deque

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True

DEFAULT_PRICE_SPIKE_RATIO: float = 0.10   # 10% price change
DEFAULT_VOLUME_SPIKE_RATIO: float = 5.0    # 5x average volume
DEFAULT_WINDOW_SIZE: int = 50


class AnomalyResult:
    def __init__(self, is_anomaly: bool, anomaly_type: str, reason: str) -> None:
        self.is_anomaly = is_anomaly
        self.anomaly_type = anomaly_type
        self.reason = reason


class MarketDataAnomalyDetector:
    """
    Detects price spikes and volume anomalies in canonical market data events.
    Uses rolling window statistics. Research only — detection only, no trading action.
    """

    def __init__(
        self,
        price_spike_ratio: float = DEFAULT_PRICE_SPIKE_RATIO,
        volume_spike_ratio: float = DEFAULT_VOLUME_SPIKE_RATIO,
        window_size: int = DEFAULT_WINDOW_SIZE,
    ) -> None:
        self._price_spike_ratio = price_spike_ratio
        self._volume_spike_ratio = volume_spike_ratio
        self._window_size = window_size
        # Per-symbol rolling windows
        self._price_windows: Dict[str, deque] = {}
        self._volume_windows: Dict[str, deque] = {}

    def check_price(self, symbol: str, price: Decimal) -> AnomalyResult:
        window = self._price_windows.setdefault(symbol, deque(maxlen=self._window_size))

        if len(window) < 2:
            window.append(price)
            return AnomalyResult(False, "", "")

        last_price = window[-1]
        if last_price > Decimal("0"):
            change_ratio = abs(price - last_price) / last_price
            if float(change_ratio) > self._price_spike_ratio:
                window.append(price)
                return AnomalyResult(
                    True, "PRICE_SPIKE",
                    f"{symbol}: price {last_price}→{price} ({float(change_ratio)*100:.1f}% change, threshold={self._price_spike_ratio*100:.1f}%)"
                )

        window.append(price)
        return AnomalyResult(False, "", "")

    def check_volume(self, symbol: str, volume: int) -> AnomalyResult:
        window = self._volume_windows.setdefault(symbol, deque(maxlen=self._window_size))

        if len(window) < 5:
            window.append(volume)
            return AnomalyResult(False, "", "")

        avg_volume = sum(window) / len(window)
        if avg_volume > 0 and volume > avg_volume * self._volume_spike_ratio:
            window.append(volume)
            return AnomalyResult(
                True, "VOLUME_SPIKE",
                f"{symbol}: volume {volume} is {volume/avg_volume:.1f}x average ({avg_volume:.0f})"
            )

        window.append(volume)
        return AnomalyResult(False, "", "")

    def reset(self, symbol: Optional[str] = None) -> None:
        if symbol:
            self._price_windows.pop(symbol, None)
            self._volume_windows.pop(symbol, None)
        else:
            self._price_windows.clear()
            self._volume_windows.clear()
