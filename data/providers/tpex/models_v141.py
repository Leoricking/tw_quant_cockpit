"""
data/providers/tpex/models_v141.py — TPEx Provider domain models v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
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

class TPExCapability(str, Enum):
    SECURITY_MASTER = "SECURITY_MASTER"
    DAILY_OHLCV = "DAILY_OHLCV"
    DAILY_TRADING_SUMMARY = "DAILY_TRADING_SUMMARY"
    INSTITUTIONAL = "INSTITUTIONAL"
    MARGIN = "MARGIN"
    MARKET_INDEX = "MARKET_INDEX"
    TRADING_CALENDAR = "TRADING_CALENDAR"
    SUSPENSION_RESUMPTION = "SUSPENSION_RESUMPTION"
    CORPORATE_ACTIONS = "CORPORATE_ACTIONS"
    VALUATION = "VALUATION"


class TPExSecurityType(str, Enum):
    COMMON_STOCK = "COMMON_STOCK"
    ETF = "ETF"
    ETN = "ETN"
    WARRANT = "WARRANT"
    REIT = "REIT"
    FOREIGN_STOCK = "FOREIGN_STOCK"
    TDR = "TDR"
    EMERGING_STOCK = "EMERGING_STOCK"
    PIONEER_STOCK = "PIONEER_STOCK"
    GO_INCUBATION = "GO_INCUBATION"
    BOND = "BOND"
    CONVERTIBLE_BOND = "CONVERTIBLE_BOND"
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"


class TPExBoard(str, Enum):
    MAINBOARD = "MAINBOARD"
    EMERGING = "EMERGING"
    PIONEER = "PIONEER"
    GO_INCUBATION = "GO_INCUBATION"
    UNKNOWN = "UNKNOWN"


class TPExAdjustedStatus(str, Enum):
    NOT_ADJUSTED = "NOT_ADJUSTED"
    EX_RIGHTS = "EX_RIGHTS"
    EX_DIVIDEND = "EX_DIVIDEND"
    EX_RIGHTS_AND_DIVIDEND = "EX_RIGHTS_AND_DIVIDEND"
    SUSPENDED = "SUSPENDED"
    UNKNOWN = "UNKNOWN"


class TPExFetchStatus(str, Enum):
    SUCCESS = "SUCCESS"
    RATE_LIMITED = "RATE_LIMITED"
    BLOCKED = "BLOCKED"
    UNAVAILABLE = "UNAVAILABLE"
    MALFORMED = "MALFORMED"
    TIMEOUT = "TIMEOUT"
    NETWORK_ERROR = "NETWORK_ERROR"
    SCHEMA_MISMATCH = "SCHEMA_MISMATCH"
    EMPTY_RESPONSE = "EMPTY_RESPONSE"
    MARKET_CONFLICT = "MARKET_CONFLICT"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class TPExProvenance:
    """Provenance record for a TPEx data fetch."""
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
    def from_dict(cls, d: Dict[str, Any]) -> "TPExProvenance":
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
            schema_version=d.get("schema_version", "1.4.1"),
            content_hash=d.get("content_hash"),
            request_id=d.get("request_id"),
            warnings=d.get("warnings", []),
        )


@dataclass
class TPExSecurity:
    """A security listed on TPEx."""
    symbol: str
    name: Optional[str]
    market: str
    board: Optional[str]
    security_type: Optional[str]
    industry_code: Optional[str]
    industry_name: Optional[str]
    listing_date: Optional[str]
    isin: Optional[str]
    currency: Optional[str]
    status: Optional[str]
    is_common_stock: bool
    universe_eligible: bool
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[TPExProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "market": self.market,
            "board": self.board,
            "security_type": self.security_type,
            "industry_code": self.industry_code,
            "industry_name": self.industry_name,
            "listing_date": self.listing_date,
            "isin": self.isin,
            "currency": self.currency,
            "status": self.status,
            "is_common_stock": self.is_common_stock,
            "universe_eligible": self.universe_eligible,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TPExSecurity":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            name=d.get("name"),
            market=d.get("market", "TPEx"),
            board=d.get("board"),
            security_type=d.get("security_type"),
            industry_code=d.get("industry_code"),
            industry_name=d.get("industry_name"),
            listing_date=d.get("listing_date"),
            isin=d.get("isin"),
            currency=d.get("currency"),
            status=d.get("status"),
            is_common_stock=d.get("is_common_stock", False),
            universe_eligible=d.get("universe_eligible", False),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "tpex_official"),
            provenance=TPExProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class TPExDailyBar:
    """A daily OHLCV bar for a TPEx security."""
    symbol: str
    trade_date: str
    open: Optional[str]
    high: Optional[str]
    low: Optional[str]
    close: Optional[str]
    previous_close: Optional[str]
    price_change: Optional[str]
    price_change_percent: Optional[str]
    volume: Optional[float]
    turnover: Optional[float]
    transaction_count: Optional[float]
    bid: Optional[str]
    ask: Optional[str]
    adjusted_status: Optional[str]
    trading_status: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provider_id: str
    provenance: Optional[TPExProvenance]
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
        if self.high is not None and self.open is not None:
            try:
                if float(self.high) < float(self.open):
                    errors.append(f"high ({self.high}) < open ({self.open})")
            except (TypeError, ValueError):
                pass
        if self.high is not None and self.close is not None:
            try:
                if float(self.high) < float(self.close):
                    errors.append(f"high ({self.high}) < close ({self.close})")
            except (TypeError, ValueError):
                pass
        if self.low is not None and self.open is not None:
            try:
                if float(self.low) > float(self.open):
                    errors.append(f"low ({self.low}) > open ({self.open})")
            except (TypeError, ValueError):
                pass
        if self.low is not None and self.close is not None:
            try:
                if float(self.low) > float(self.close):
                    errors.append(f"low ({self.low}) > close ({self.close})")
            except (TypeError, ValueError):
                pass
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
            "previous_close": self.previous_close,
            "price_change": self.price_change,
            "price_change_percent": self.price_change_percent,
            "volume": self.volume,
            "turnover": self.turnover,
            "transaction_count": self.transaction_count,
            "bid": self.bid,
            "ask": self.ask,
            "adjusted_status": self.adjusted_status,
            "trading_status": self.trading_status,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provider_id": self.provider_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TPExDailyBar":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            trade_date=d["trade_date"],
            open=d.get("open"),
            high=d.get("high"),
            low=d.get("low"),
            close=d.get("close"),
            previous_close=d.get("previous_close"),
            price_change=d.get("price_change"),
            price_change_percent=d.get("price_change_percent"),
            volume=d.get("volume"),
            turnover=d.get("turnover"),
            transaction_count=d.get("transaction_count"),
            bid=d.get("bid"),
            ask=d.get("ask"),
            adjusted_status=d.get("adjusted_status"),
            trading_status=d.get("trading_status"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provider_id=d.get("provider_id", "tpex_official"),
            provenance=TPExProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class TPExInstitutionalFlow:
    """Institutional investor flow data for a TPEx security (dealer split into separate fields)."""
    symbol: str
    trade_date: str
    foreign_buy: Optional[float]
    foreign_sell: Optional[float]
    foreign_net: Optional[float]
    investment_trust_buy: Optional[float]
    investment_trust_sell: Optional[float]
    investment_trust_net: Optional[float]
    dealer_proprietary_buy: Optional[float]
    dealer_proprietary_sell: Optional[float]
    dealer_proprietary_net: Optional[float]
    dealer_hedge_buy: Optional[float]
    dealer_hedge_sell: Optional[float]
    dealer_hedge_net: Optional[float]
    dealer_total_net: Optional[float]
    total_net: Optional[float]
    source_timestamp: Optional[str]
    published_at: Optional[str]
    fetched_at: str
    provenance: Optional[TPExProvenance]
    warnings: List[str] = field(default_factory=list)
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
            "dealer_proprietary_buy": self.dealer_proprietary_buy,
            "dealer_proprietary_sell": self.dealer_proprietary_sell,
            "dealer_proprietary_net": self.dealer_proprietary_net,
            "dealer_hedge_buy": self.dealer_hedge_buy,
            "dealer_hedge_sell": self.dealer_hedge_sell,
            "dealer_hedge_net": self.dealer_hedge_net,
            "dealer_total_net": self.dealer_total_net,
            "total_net": self.total_net,
            "source_timestamp": self.source_timestamp,
            "published_at": self.published_at,
            "fetched_at": self.fetched_at,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TPExInstitutionalFlow":
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
            dealer_proprietary_buy=d.get("dealer_proprietary_buy"),
            dealer_proprietary_sell=d.get("dealer_proprietary_sell"),
            dealer_proprietary_net=d.get("dealer_proprietary_net"),
            dealer_hedge_buy=d.get("dealer_hedge_buy"),
            dealer_hedge_sell=d.get("dealer_hedge_sell"),
            dealer_hedge_net=d.get("dealer_hedge_net"),
            dealer_total_net=d.get("dealer_total_net"),
            total_net=d.get("total_net"),
            source_timestamp=d.get("source_timestamp"),
            published_at=d.get("published_at"),
            fetched_at=d.get("fetched_at", ""),
            provenance=TPExProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class TPExMarginRecord:
    """Margin trading record for a TPEx security."""
    symbol: str
    trade_date: str
    margin_buy: Optional[float]
    margin_sell: Optional[float]
    cash_redemption: Optional[float]
    margin_previous_balance: Optional[float]
    margin_balance: Optional[float]
    margin_limit: Optional[float]
    short_sell: Optional[float]
    short_cover: Optional[float]
    stock_redemption: Optional[float]
    short_previous_balance: Optional[float]
    short_balance: Optional[float]
    short_limit: Optional[float]
    source_timestamp: Optional[str]
    fetched_at: str
    provenance: Optional[TPExProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "trade_date": self.trade_date,
            "margin_buy": self.margin_buy,
            "margin_sell": self.margin_sell,
            "cash_redemption": self.cash_redemption,
            "margin_previous_balance": self.margin_previous_balance,
            "margin_balance": self.margin_balance,
            "margin_limit": self.margin_limit,
            "short_sell": self.short_sell,
            "short_cover": self.short_cover,
            "stock_redemption": self.stock_redemption,
            "short_previous_balance": self.short_previous_balance,
            "short_balance": self.short_balance,
            "short_limit": self.short_limit,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TPExMarginRecord":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            trade_date=d["trade_date"],
            margin_buy=d.get("margin_buy"),
            margin_sell=d.get("margin_sell"),
            cash_redemption=d.get("cash_redemption"),
            margin_previous_balance=d.get("margin_previous_balance"),
            margin_balance=d.get("margin_balance"),
            margin_limit=d.get("margin_limit"),
            short_sell=d.get("short_sell"),
            short_cover=d.get("short_cover"),
            stock_redemption=d.get("stock_redemption"),
            short_previous_balance=d.get("short_previous_balance"),
            short_balance=d.get("short_balance"),
            short_limit=d.get("short_limit"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provenance=TPExProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )


@dataclass
class TPExMarketSummary:
    """Daily market summary for TPEx."""
    trade_date: str
    market: str
    board: Optional[str]
    trading_value: Optional[float]
    trading_volume: Optional[float]
    transaction_count: Optional[float]
    index_close: Optional[str]
    index_change: Optional[str]
    advancing: Optional[float]
    declining: Optional[float]
    unchanged: Optional[float]
    source_timestamp: Optional[str]
    fetched_at: str
    provenance: Optional[TPExProvenance]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trade_date": self.trade_date,
            "market": self.market,
            "board": self.board,
            "trading_value": self.trading_value,
            "trading_volume": self.trading_volume,
            "transaction_count": self.transaction_count,
            "index_close": self.index_close,
            "index_change": self.index_change,
            "advancing": self.advancing,
            "declining": self.declining,
            "unchanged": self.unchanged,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TPExMarketSummary":
        prov = d.get("provenance")
        return cls(
            trade_date=d["trade_date"],
            market=d.get("market", "TPEx"),
            board=d.get("board"),
            trading_value=d.get("trading_value"),
            trading_volume=d.get("trading_volume"),
            transaction_count=d.get("transaction_count"),
            index_close=d.get("index_close"),
            index_change=d.get("index_change"),
            advancing=d.get("advancing"),
            declining=d.get("declining"),
            unchanged=d.get("unchanged"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provenance=TPExProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            metadata=d.get("metadata", {}),
        )


@dataclass
class TPExIndexRecord:
    """An index record (e.g. TPEX composite index) for a given date."""
    index_code: str
    index_name: Optional[str]
    trade_date: str
    open: Optional[str]
    high: Optional[str]
    low: Optional[str]
    close: Optional[str]
    change: Optional[str]
    change_percent: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provenance: Optional[TPExProvenance]
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
            "change_percent": self.change_percent,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TPExIndexRecord":
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
            change_percent=d.get("change_percent"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provenance=TPExProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            metadata=d.get("metadata", {}),
        )


@dataclass
class TPExTradingDay:
    """A trading calendar entry for TPEx."""
    date: str
    is_trading_day: bool
    holiday_name: Optional[str]
    market: str
    source: str
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
    def from_dict(cls, d: Dict[str, Any]) -> "TPExTradingDay":
        return cls(
            date=d["date"],
            is_trading_day=d.get("is_trading_day", False),
            holiday_name=d.get("holiday_name"),
            market=d.get("market", "TPEx"),
            source=d.get("source", "heuristic"),
            approximate=d.get("approximate", True),
            fetched_at=d.get("fetched_at", ""),
            metadata=d.get("metadata", {}),
        )


@dataclass
class TPExSuspensionRecord:
    """A suspension or resumption record for a TPEx security."""
    symbol: str
    name: Optional[str]
    announcement_date: Optional[str]
    effective_date: Optional[str]
    resume_date: Optional[str]
    action: Optional[str]
    reason: Optional[str]
    status: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provenance: Optional[TPExProvenance]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "announcement_date": self.announcement_date,
            "effective_date": self.effective_date,
            "resume_date": self.resume_date,
            "action": self.action,
            "reason": self.reason,
            "status": self.status,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TPExSuspensionRecord":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            name=d.get("name"),
            announcement_date=d.get("announcement_date"),
            effective_date=d.get("effective_date"),
            resume_date=d.get("resume_date"),
            action=d.get("action"),
            reason=d.get("reason"),
            status=d.get("status"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provenance=TPExProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            metadata=d.get("metadata", {}),
        )


@dataclass
class TPExCorporateActionPreview:
    """A corporate action preview entry for TPEx."""
    symbol: str
    event_type: str
    announcement_date: Optional[str]
    effective_date: Optional[str]
    details: Optional[str]
    status: Optional[str]
    source_timestamp: Optional[str]
    fetched_at: str
    provenance: Optional[TPExProvenance]
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
    def from_dict(cls, d: Dict[str, Any]) -> "TPExCorporateActionPreview":
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
            provenance=TPExProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            metadata=d.get("metadata", {}),
        )


@dataclass
class TPExValuationRecord:
    """Valuation metrics for a TPEx security."""
    symbol: str
    trade_date: str
    pe_ratio: Optional[float]
    dividend_yield: Optional[float]
    price_to_book: Optional[float]
    market_cap: Optional[float]
    source_timestamp: Optional[str]
    fetched_at: str
    provenance: Optional[TPExProvenance]
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "trade_date": self.trade_date,
            "pe_ratio": self.pe_ratio,
            "dividend_yield": self.dividend_yield,
            "price_to_book": self.price_to_book,
            "market_cap": self.market_cap,
            "source_timestamp": self.source_timestamp,
            "fetched_at": self.fetched_at,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TPExValuationRecord":
        prov = d.get("provenance")
        return cls(
            symbol=d["symbol"],
            trade_date=d["trade_date"],
            pe_ratio=d.get("pe_ratio"),
            dividend_yield=d.get("dividend_yield"),
            price_to_book=d.get("price_to_book"),
            market_cap=d.get("market_cap"),
            source_timestamp=d.get("source_timestamp"),
            fetched_at=d.get("fetched_at", ""),
            provenance=TPExProvenance.from_dict(prov) if isinstance(prov, dict) else None,
            warnings=d.get("warnings", []),
            metadata=d.get("metadata", {}),
        )
