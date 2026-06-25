"""
paper_trading/market_data/validation_v161.py — Market Data validation v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Validates raw events before normalization. bid<=ask enforced. Decimal-safe.
"""
from __future__ import annotations
from decimal import Decimal, InvalidOperation
from typing import Dict, Any, List, Tuple

from paper_trading.market_data.enums_v161 import SourceClass, MarketDataEventType

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True


class MarketDataValidationError(Exception):
    pass


class MarketDataValidator:
    """Validates raw market data events before normalization."""

    REQUIRED_FIELDS_QUOTE = {"symbol", "bid", "ask", "timestamp"}
    REQUIRED_FIELDS_TRADE = {"symbol", "price", "volume", "timestamp"}

    def validate_quote_payload(self, payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        for f in self.REQUIRED_FIELDS_QUOTE:
            if f not in payload:
                errors.append(f"Missing required field: {f}")

        if not errors:
            try:
                bid = Decimal(str(payload["bid"]))
                ask = Decimal(str(payload["ask"]))
            except (InvalidOperation, TypeError) as e:
                errors.append(f"Non-numeric bid/ask: {e}")
                return False, errors

            if bid <= Decimal("0"):
                errors.append(f"bid must be > 0, got {bid}")
            if ask <= Decimal("0"):
                errors.append(f"ask must be > 0, got {ask}")
            if bid > ask:
                errors.append(f"bid ({bid}) > ask ({ask}): bid<=ask invariant violated")

        return len(errors) == 0, errors

    def validate_trade_payload(self, payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        for f in self.REQUIRED_FIELDS_TRADE:
            if f not in payload:
                errors.append(f"Missing required field: {f}")

        if not errors:
            try:
                price = Decimal(str(payload["price"]))
            except (InvalidOperation, TypeError) as e:
                errors.append(f"Non-numeric price: {e}")
                return False, errors

            if price <= Decimal("0"):
                errors.append(f"price must be > 0, got {price}")

            try:
                volume = int(payload["volume"])
            except (ValueError, TypeError) as e:
                errors.append(f"Invalid volume: {e}")
                return False, errors

            if volume < 0:
                errors.append(f"volume must be >= 0, got {volume}")

        return len(errors) == 0, errors

    def validate_source_class(self, source_class: SourceClass) -> Tuple[bool, str]:
        if source_class == SourceClass.UNKNOWN:
            return False, "UNKNOWN source_class is not trusted as LIVE — explicit classification required"
        return True, ""

    def validate_symbol(self, symbol: str) -> Tuple[bool, str]:
        if not symbol or not symbol.strip():
            return False, "symbol must be non-empty"
        return True, ""

    def validate_timestamp_utc(self, ts: str) -> Tuple[bool, str]:
        if not ts or not isinstance(ts, str):
            return False, "timestamp_utc must be a non-empty string"
        if "T" not in ts:
            return False, f"timestamp_utc must be ISO-8601 with T separator, got: {ts!r}"
        return True, ""
