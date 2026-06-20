"""
data/providers/twse/models_v140.py — TWSE Provider domain models v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TWSECapability(str, Enum):
    SECURITY_MASTER = "SECURITY_MASTER"
    DAILY_OHLCV = "DAILY_OHLCV"
    DAILY_TRADING_SUMMARY = "DAILY_TRADING_SUMMARY"
    INSTITUTIONAL = "INSTITUTIONAL"
    MARGIN = "MARGIN"
    MARKET_INDEX = "MARKET_INDEX"
    TRADING_CALENDAR = "TRADING_CALENDAR"
    CORPORATE_ACTIONS = "CORPORATE_ACTIONS"
    VALUATION = "VALUATION"


class TWSESecurityType(str, Enum):
    COMMON_STOCK = "COMMON_STOCK"
    ETF = "ETF"
    WARRANT = "WARRANT"
    TDR = "TDR"
    FOREIGN_STOCK = "FOREIGN_STOCK"
    PREFERRED_STOCK = "PREFERRED_STOCK"
    BOND = "BOND"
    INDEX = "INDEX"
    UNKNOWN = "UNKNOWN"


class TWSEAdjustedStatus(str, Enum):
    NOT_ADJUSTED = "NOT_ADJUSTED"
    EX_RIGHTS = "EX_RIGHTS"
    EX_DIVIDEND = "EX_DIVIDEND"
    EX_RIGHTS_AND_DIVIDEND = "EX_RIGHTS_AND_DIVIDEND"
    SUSPENDED = "SUSPENDED"
    UNKNOWN = "UNKNOWN"


class TWSEFetchStatus(str, Enum):
    SUCCESS = "SUCCESS"
    RATE_LIMITED = "RATE_LIMITED"
    BLOCKED = "BLOCKED"
    UNAVAILABLE = "UNAVAILABLE"
    MALFORMED = "MALFORMED"
    TIMEOUT = "TIMEOUT"
    NETWORK_ERROR = "NETWORK_ERROR"
    SCHEMA_MISMATCH = "SCHEMA_MISMATCH"
    EMPTY_RESPONSE = "EMPTY_RESPONSE"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class TWSEProvenance:
    """Provenance record for a TWSE data fetch."""
    provider_id: str
    official_source: bool
    endpoint_id: str
    source_url: str
    requested_at: str
    received_at: str
    source_timestamp: Optional[str]
    trading_date: Optional[str]
    response_format: str
    schema_version: str
    content_hash: Optional[str]
    request_id: Optional[str]
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "official_source": self.official_source,
            "endpoint_id": self.endpoint_id,
            "source_url": self.source_url,
            "requested_at": self.requested_at,
            "received_at": self.received_at,
            "source_timestamp": self.source_timestamp,
            "trading_date": self.trading_date,
            "response_format": self.response_format,
            "schema_version": self.schema_version,
            "content_hash": self.content_hash,
            "request_id": self.request_id,
            "warnings": list(self.warnings),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TWSEProvenance":
        return cls(
            provider_id=d.get("provider_id", ""),
            official_source=d.get("official_source", True),
            endpoint_id=d.get("endpoint_id", ""),
            source_url=d.get("source_url", ""),
            requested_at=d.get("requested_at", ""),
            received_at=d.get("received_at", ""),
            source_timestamp=d.get("source_timestamp"),
            trading_date=d.get("trading_date"),
            response_format=d.get("response_format", "JSON"),
            schema_version=d.get("schema_version", "1.4.0"),
            content_hash=d.get("content_hash"),
            request_id=d.get("request_id"),
            warnings=d.get("warnings", []),
        )


@dataclass
class TWSESecurity:
    """A security listed on TWSE."""
    symbol: str
    name: Optional[str]
    market: str
    security_type: Optional[str]
    industry_code: Optional[str]
    industry_name: Optional[str]
    listing_date: Optional[str]
    isin: Optional[str]
    currency: Optional[str]
    status: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[TWSEProvenance]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "market": self.market,
            "security_type": self.security_type,
            "industry_code": self.industry_code,
            "industry_name": self.industry_name,
            "listing_date": self.listing_date,
            "isin": self.isin,
            "currency": self.currency,
            "status": self.status,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TWSESecurity":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            name=d.get("name"),
            market=d.get("market", "TWSE"),
            security_type=d.get("security_type"),
            industry_code=d.get("industry_code"),
            industry_name=d.get("industry_name"),
            listing_date=d.get("listing_date"),
            isin=d.get("isin"),
            currency=d.get("currency"),
            status=d.get("status"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "twse_official"),
            provenance=TWSEProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            metadata=d.get("metadata", {}),
        )


@dataclass
class TWSEDailyBar:
    """A daily OHLCV bar for a TWSE security."""
    symbol: str
    trade_date: str
    open: Optional[str]
    high: Optional[str]
    low: Optional[str]
    close: Optional[str]
    volume: Optional[float]
    turnover: Optional[float]
    transaction_count: Optional[float]
    price_change: Optional[str]
    adjusted_status: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[TWSEProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def validate_ohlc(self) -> Dict[str, Any]:
        errors: List[str] = []
        if self.high is not None and self.low is not None:
            try:
                if float(self.high) < float(self.low):
                    errors.append(f"high ({self.high}) < low ({self.low})")
            except (TypeError, ValueError) as e:
                errors.append(f"OHLC parse error: {e}")
        if self.volume is not None and self.volume > 0:
            if self.open is not None:
                try:
                    if float(self.open) <= 0:
                        errors.append(f"open ({self.open}) <= 0 with volume > 0")
                except (TypeError, ValueError):
                    pass
            if self.close is not None:
                try:
                    if float(self.close) <= 0:
                        errors.append(f"close ({self.close}) <= 0 with volume > 0")
                except (TypeError, ValueError):
                    pass
        return {"valid": len(errors) == 0, "errors": errors}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "trade_date": self.trade_date,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "turnover": self.turnover,
            "transaction_count": self.transaction_count,
            "price_change": self.price_change,
            "adjusted_status": self.adjusted_status,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TWSEDailyBar":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            trade_date=d["trade_date"],
            open=d.get("open"),
            high=d.get("high"),
            low=d.get("low"),
            close=d.get("close"),
            volume=d.get("volume"),
            turnover=d.get("turnover"),
            transaction_count=d.get("transaction_count"),
            price_change=d.get("price_change"),
            adjusted_status=d.get("adjusted_status"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "twse_official"),
            provenance=TWSEProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class TWSEInstitutionalFlow:
    """Institutional investor flow data for a TWSE security."""
    symbol: str
    trade_date: str
    foreign_buy: Optional[float]
    foreign_sell: Optional[float]
    foreign_net: Optional[float]
    investment_trust_buy: Optional[float]
    investment_trust_sell: Optional[float]
    investment_trust_net: Optional[float]
    dealer_buy: Optional[float]
    dealer_sell: Optional[float]
    dealer_net: Optional[float]
    total_net: Optional[float]
    source_timestamp: Optional[str]
    fetched_at: str
    provenance: Optional[TWSEProvenance]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "trade_date": self.trade_date,
            "foreign_buy": self.foreign_buy,
            "foreign_sell": self.foreign_sell,
            "foreign_net": self.foreign_net,
            "investment_trust_buy": self.investment_trust_buy,
            "investment_trust_sell": self.investment_trust_sell,
            "investment_trust_net": self.investment_trust_net,
            "dealer_buy": self.dealer_buy,
            "dealer_sell": self.dealer_sell,
            "dealer_net": self.dealer_net,
            "total_net": self.total_net,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TWSEInstitutionalFlow":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            trade_date=d["trade_date"],
            foreign_buy=d.get("foreign_buy"),
            foreign_sell=d.get("foreign_sell"),
            foreign_net=d.get("foreign_net"),
            investment_trust_buy=d.get("investment_trust_buy"),
            investment_trust_sell=d.get("investment_trust_sell"),
            investment_trust_net=d.get("investment_trust_net"),
            dealer_buy=d.get("dealer_buy"),
            dealer_sell=d.get("dealer_sell"),
            dealer_net=d.get("dealer_net"),
            total_net=d.get("total_net"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provenance=TWSEProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            metadata=d.get("metadata", {}),
        )


@dataclass
class TWSEMarginRecord:
    """Margin trading record for a TWSE security."""
    symbol: str
    trade_date: str
    margin_buy: Optional[float]
    margin_sell: Optional[float]
    margin_redemption: Optional[float]
    margin_balance: Optional[float]
    short_sell: Optional[float]
    short_cover: Optional[float]
    short_balance: Optional[float]
    source_timestamp: Optional[str]
    fetched_at: str
    provenance: Optional[TWSEProvenance]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "trade_date": self.trade_date,
            "margin_buy": self.margin_buy,
            "margin_sell": self.margin_sell,
            "margin_redemption": self.margin_redemption,
            "margin_balance": self.margin_balance,
            "short_sell": self.short_sell,
            "short_cover": self.short_cover,
            "short_balance": self.short_balance,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TWSEMarginRecord":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            trade_date=d["trade_date"],
            margin_buy=d.get("margin_buy"),
            margin_sell=d.get("margin_sell"),
            margin_redemption=d.get("margin_redemption"),
            margin_balance=d.get("margin_balance"),
            short_sell=d.get("short_sell"),
            short_cover=d.get("short_cover"),
            short_balance=d.get("short_balance"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provenance=TWSEProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            metadata=d.get("metadata", {}),
        )


@dataclass
class TWSEMarketSummary:
    """Daily market summary for TWSE."""
    trade_date: str
    market: str
    trading_value: Optional[str]
    trading_volume: Optional[str]
    transaction_count: Optional[str]
    index_close: Optional[str]
    index_change: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provenance: Optional[TWSEProvenance]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trade_date": self.trade_date,
            "market": self.market,
            "trading_value": self.trading_value,
            "trading_volume": self.trading_volume,
            "transaction_count": self.transaction_count,
            "index_close": self.index_close,
            "index_change": self.index_change,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TWSEMarketSummary":
        prov = d.get("provenance")
        return cls(
            trade_date=d["trade_date"],
            market=d.get("market", "TWSE"),
            trading_value=d.get("trading_value"),
            trading_volume=d.get("trading_volume"),
            transaction_count=d.get("transaction_count"),
            index_close=d.get("index_close"),
            index_change=d.get("index_change"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provenance=TWSEProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            metadata=d.get("metadata", {}),
        )


@dataclass
class TWSEIndexRecord:
    """An index record (e.g. TAIEX) for a given date."""
    index_code: str
    index_name: Optional[str]
    trade_date: str
    open: Optional[str]
    high: Optional[str]
    low: Optional[str]
    close: Optional[str]
    change: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provenance: Optional[TWSEProvenance]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index_code": self.index_code,
            "index_name": self.index_name,
            "trade_date": self.trade_date,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "change": self.change,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TWSEIndexRecord":
        prov = d.get("provenance")
        return cls(
            index_code=d["index_code"],
            index_name=d.get("index_name"),
            trade_date=d["trade_date"],
            open=d.get("open"),
            high=d.get("high"),
            low=d.get("low"),
            close=d.get("close"),
            change=d.get("change"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provenance=TWSEProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            metadata=d.get("metadata", {}),
        )


@dataclass
class TWSETradingDay:
    """A trading calendar entry."""
    date: str
    is_trading_day: bool
    holiday_name: Optional[str]
    market: str
    source: str  # "official" or "heuristic"
    approximate: bool
    fetched_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "is_trading_day": self.is_trading_day,
            "holiday_name": self.holiday_name,
            "market": self.market,
            "source": self.source,
            "approximate": self.approximate,
            "fetched_at": self.fetched_at,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TWSETradingDay":
        return cls(
            date=d["date"],
            is_trading_day=d.get("is_trading_day", False),
            holiday_name=d.get("holiday_name"),
            market=d.get("market", "TWSE"),
            source=d.get("source", "heuristic"),
            approximate=d.get("approximate", True),
            fetched_at=d.get("fetched_at", ""),
            metadata=d.get("metadata", {}),
        )


@dataclass
class TWSECorporateActionPreview:
    """A corporate action preview entry."""
    symbol: str
    event_type: str
    announcement_date: Optional[str]
    effective_date: Optional[str]
    details: Optional[str]
    status: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provenance: Optional[TWSEProvenance]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "event_type": self.event_type,
            "announcement_date": self.announcement_date,
            "effective_date": self.effective_date,
            "details": self.details,
            "status": self.status,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TWSECorporateActionPreview":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            event_type=d.get("event_type", "UNKNOWN"),
            announcement_date=d.get("announcement_date"),
            effective_date=d.get("effective_date"),
            details=d.get("details"),
            status=d.get("status"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provenance=TWSEProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            metadata=d.get("metadata", {}),
        )
