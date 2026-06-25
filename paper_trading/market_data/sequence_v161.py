"""
paper_trading/market_data/sequence_v161.py — Sequence Validator v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Detects gaps, duplicates, out-of-order events per symbol.
"""
from __future__ import annotations
from typing import Dict, Optional, Tuple

from paper_trading.market_data.enums_v161 import SequenceStatus
from paper_trading.market_data.models_v161 import RawMarketDataEvent

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class SequenceValidator:
    """
    Tracks expected sequence numbers per symbol/adapter.
    Reports gaps, duplicates, out-of-order, resets.
    """

    def __init__(self) -> None:
        # key: (adapter_id, symbol) → last_seen_sequence
        self._last_seq: Dict[Tuple[str, str], Optional[int]] = {}

    def check(self, event: RawMarketDataEvent) -> SequenceStatus:
        """Determine sequence status for an incoming event."""
        seq = event.sequence_number
        if seq is None:
            return SequenceStatus.UNKNOWN

        key = (event.adapter_id, event.symbol)
        last = self._last_seq.get(key)

        if last is None:
            # First event for this key
            self._last_seq[key] = seq
            return SequenceStatus.IN_ORDER

        if seq == last:
            return SequenceStatus.DUPLICATE

        if seq == last + 1:
            self._last_seq[key] = seq
            return SequenceStatus.IN_ORDER

        if seq < last:
            return SequenceStatus.OUT_OF_ORDER

        if seq > last + 1:
            # Gap detected — update to latest seen
            self._last_seq[key] = seq
            return SequenceStatus.GAP_DETECTED

        return SequenceStatus.UNKNOWN

    def reset(self, adapter_id: str, symbol: str) -> None:
        """Reset sequence tracking for a symbol (e.g., after reconnect)."""
        key = (adapter_id, symbol)
        self._last_seq.pop(key, None)

    def reset_all(self) -> None:
        self._last_seq.clear()

    def get_last_seq(self, adapter_id: str, symbol: str) -> Optional[int]:
        return self._last_seq.get((adapter_id, symbol))
