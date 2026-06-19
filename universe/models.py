"""
universe/models.py — Universe data models for TW Quant Cockpit v1.3.1.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Universe Ready does NOT enable trading. Universe Registered != data complete.
[!] Universe Covered != can generate precise prices.
[!] No Real API Connected. No Auto Download. Not Investment Advice.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS             = True
BROKER_DISABLED            = True
PRODUCTION_TRADING_BLOCKED = True
MOCK_FALLBACK_ENABLED      = False
UNIVERSE_REAL_API_CONNECTED    = False
UNIVERSE_AUTO_DOWNLOAD_ENABLED = False


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class UniverseMarket(str, Enum):
    """Taiwan stock exchange market constants."""
    TWSE     = "TWSE"
    TPEX     = "TPEx"
    EMERGING = "EMERGING"
    UNKNOWN  = "UNKNOWN"


class SecurityType(str, Enum):
    """Security classification."""
    COMMON_STOCK   = "COMMON_STOCK"
    ETF            = "ETF"
    PREFERRED_STOCK = "PREFERRED_STOCK"
    TDR            = "TDR"
    REIT           = "REIT"
    WARRANT        = "WARRANT"
    OTHER          = "OTHER"
    UNKNOWN        = "UNKNOWN"


class ListingStatus(str, Enum):
    """Current listing status."""
    LISTED   = "LISTED"
    SUSPENDED = "SUSPENDED"
    DELISTED  = "DELISTED"
    EMERGING  = "EMERGING"
    UNKNOWN   = "UNKNOWN"


class UniverseTier(str, Enum):
    """Universe tier for prioritization."""
    CORE      = "core"
    RESEARCH  = "research"
    EXTENDED  = "extended"
    WATCHLIST = "watchlist"
    EXCLUDED  = "excluded"


class CoverageStatus(str, Enum):
    """Data coverage status for a symbol under a profile."""
    READY       = "READY"
    PARTIAL     = "PARTIAL"
    MISSING     = "MISSING"
    STALE       = "STALE"
    BLOCKED     = "BLOCKED"
    UNAVAILABLE = "UNAVAILABLE"
    DEMO_ONLY   = "DEMO_ONLY"
    EXCLUDED    = "EXCLUDED"


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class UniverseSymbol:
    """
    A symbol registered in the research universe.

    [!] Registration != data complete != tradeable.
    [!] Research Only. No Real Orders.
    """
    symbol: str = ""
    normalized_symbol: str = ""
    stock_name: str = ""
    market: str = UniverseMarket.UNKNOWN.value
    exchange: str = ""
    security_type: str = SecurityType.UNKNOWN.value
    industry: str = ""
    sub_industry: str = ""
    listing_status: str = ListingStatus.UNKNOWN.value
    listing_date: str = ""
    delisting_date: str = ""
    currency: str = "TWD"
    lot_size: int = 1000
    is_active: bool = True
    is_etf: bool = False
    is_preferred: bool = False
    is_warrant: bool = False
    is_dr: bool = False
    source: str = "BUILT_IN_SEED"
    source_updated_at: str = ""
    registered_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    aliases: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    # Safety
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "normalized_symbol": self.normalized_symbol,
            "stock_name": self.stock_name,
            "market": self.market,
            "exchange": self.exchange,
            "security_type": self.security_type,
            "industry": self.industry,
            "sub_industry": self.sub_industry,
            "listing_status": self.listing_status,
            "listing_date": self.listing_date,
            "delisting_date": self.delisting_date,
            "currency": self.currency,
            "lot_size": self.lot_size,
            "is_active": self.is_active,
            "is_etf": self.is_etf,
            "is_preferred": self.is_preferred,
            "is_warrant": self.is_warrant,
            "is_dr": self.is_dr,
            "source": self.source,
            "source_updated_at": self.source_updated_at,
            "registered_at": self.registered_at,
            "updated_at": self.updated_at,
            "aliases": self.aliases,
            "tags": self.tags,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "UniverseSymbol":
        return cls(
            symbol=str(d.get("symbol", "")),
            normalized_symbol=str(d.get("normalized_symbol", "")),
            stock_name=str(d.get("stock_name", d.get("name", ""))),
            market=str(d.get("market", UniverseMarket.UNKNOWN.value)),
            exchange=str(d.get("exchange", "")),
            security_type=str(d.get("security_type", SecurityType.UNKNOWN.value)),
            industry=str(d.get("industry", "")),
            sub_industry=str(d.get("sub_industry", "")),
            listing_status=str(d.get("listing_status", ListingStatus.UNKNOWN.value)),
            listing_date=str(d.get("listing_date", "")),
            delisting_date=str(d.get("delisting_date", "")),
            currency=str(d.get("currency", "TWD")),
            lot_size=int(d.get("lot_size", 1000)),
            is_active=bool(d.get("is_active", True)),
            is_etf=bool(d.get("is_etf", False)),
            is_preferred=bool(d.get("is_preferred", False)),
            is_warrant=bool(d.get("is_warrant", False)),
            is_dr=bool(d.get("is_dr", False)),
            source=str(d.get("source", "BUILT_IN_SEED")),
            source_updated_at=str(d.get("source_updated_at", "")),
            registered_at=str(d.get("registered_at", _now_iso())),
            updated_at=str(d.get("updated_at", _now_iso())),
            aliases=list(d.get("aliases", [])),
            tags=list(d.get("tags", [])),
            metadata=dict(d.get("metadata", {})),
        )


@dataclass
class UniverseMembership:
    """
    Membership of a symbol in a specific universe tier.

    [!] Membership != data complete != tradeable. Research Only.
    """
    universe_id: str = ""
    symbol: str = ""
    tier: str = UniverseTier.CORE.value
    enabled: bool = True
    priority: int = 0
    inclusion_reason: str = ""
    exclusion_reason: str = ""
    added_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    source: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "universe_id": self.universe_id,
            "symbol": self.symbol,
            "tier": self.tier,
            "enabled": self.enabled,
            "priority": self.priority,
            "inclusion_reason": self.inclusion_reason,
            "exclusion_reason": self.exclusion_reason,
            "added_at": self.added_at,
            "updated_at": self.updated_at,
            "source": self.source,
            "tags": self.tags,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "UniverseMembership":
        return cls(
            universe_id=str(d.get("universe_id", "")),
            symbol=str(d.get("symbol", "")),
            tier=str(d.get("tier", UniverseTier.CORE.value)),
            enabled=bool(d.get("enabled", True)),
            priority=int(d.get("priority", 0)),
            inclusion_reason=str(d.get("inclusion_reason", "")),
            exclusion_reason=str(d.get("exclusion_reason", "")),
            added_at=str(d.get("added_at", _now_iso())),
            updated_at=str(d.get("updated_at", _now_iso())),
            source=str(d.get("source", "")),
            tags=list(d.get("tags", [])),
            metadata=dict(d.get("metadata", {})),
        )


@dataclass
class UniverseDefinition:
    """
    Definition of a named universe group (core/research/extended/etc.).

    [!] Research Only. Universe definitions are NOT market master data.
    """
    universe_id: str = ""
    name: str = ""
    description: str = ""
    market_scope: List[str] = field(default_factory=list)
    security_types: List[str] = field(default_factory=list)
    tiers: List[str] = field(default_factory=list)
    symbols: List[str] = field(default_factory=list)
    active_only: bool = True
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    source: str = "BUILT_IN_SEED"
    version: str = "1.3.1"
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "universe_id": self.universe_id,
            "name": self.name,
            "description": self.description,
            "market_scope": self.market_scope,
            "security_types": self.security_types,
            "tiers": self.tiers,
            "symbols": self.symbols,
            "active_only": self.active_only,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "source": self.source,
            "version": self.version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "UniverseDefinition":
        syms = d.get("symbols", [])
        if isinstance(syms, str):
            syms = [s.strip() for s in syms.split(",") if s.strip()]
        return cls(
            universe_id=str(d.get("universe_id", "")),
            name=str(d.get("name", "")),
            description=str(d.get("description", "")),
            market_scope=list(d.get("market_scope", [])),
            security_types=list(d.get("security_types", [])),
            tiers=list(d.get("tiers", [])),
            symbols=list(syms),
            active_only=bool(d.get("active_only", True)),
            created_at=str(d.get("created_at", _now_iso())),
            updated_at=str(d.get("updated_at", _now_iso())),
            source=str(d.get("source", "BUILT_IN_SEED")),
            version=str(d.get("version", "1.3.1")),
            metadata=dict(d.get("metadata", {})),
        )


@dataclass
class UniverseCoverageRecord:
    """
    Per-symbol coverage record for a specific quality profile.

    [!] Coverage != can generate precise prices. Research Only.
    [!] Missing values must NOT be filled with 0.
    """
    symbol: str = ""
    universe_id: str = ""
    tier: str = ""
    registry_status: str = "UNREGISTERED"
    quality_status: str = CoverageStatus.UNAVAILABLE.value
    quality_score: Optional[float] = None
    data_mode: str = "UNAVAILABLE"

    # Latest data timestamps (None = truly unknown, not filled with 0)
    latest_price_date: Optional[str] = None
    latest_institutional_date: Optional[str] = None
    latest_margin_date: Optional[str] = None
    latest_revenue_period: Optional[str] = None
    latest_financial_period: Optional[str] = None

    # Availability flags
    ohlcv_available: bool = False
    technical_available: bool = False
    institutional_available: bool = False
    margin_available: bool = False
    fundamental_available: bool = False
    shareholder_available: bool = False
    etf_overlap_available: bool = False

    # Profile-specific allowances
    precise_price_allowed: bool = False
    backtest_allowed: bool = False
    abc_buy_point_allowed: bool = False

    # Issues
    blocking_reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    checked_at: str = field(default_factory=_now_iso)
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "universe_id": self.universe_id,
            "tier": self.tier,
            "registry_status": self.registry_status,
            "quality_status": self.quality_status,
            "quality_score": self.quality_score,
            "data_mode": self.data_mode,
            "latest_price_date": self.latest_price_date,
            "latest_institutional_date": self.latest_institutional_date,
            "latest_margin_date": self.latest_margin_date,
            "latest_revenue_period": self.latest_revenue_period,
            "latest_financial_period": self.latest_financial_period,
            "ohlcv_available": self.ohlcv_available,
            "technical_available": self.technical_available,
            "institutional_available": self.institutional_available,
            "margin_available": self.margin_available,
            "fundamental_available": self.fundamental_available,
            "shareholder_available": self.shareholder_available,
            "etf_overlap_available": self.etf_overlap_available,
            "precise_price_allowed": self.precise_price_allowed,
            "backtest_allowed": self.backtest_allowed,
            "abc_buy_point_allowed": self.abc_buy_point_allowed,
            "blocking_reasons": self.blocking_reasons,
            "warnings": self.warnings,
            "checked_at": self.checked_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "UniverseCoverageRecord":
        return cls(
            symbol=str(d.get("symbol", "")),
            universe_id=str(d.get("universe_id", "")),
            tier=str(d.get("tier", "")),
            registry_status=str(d.get("registry_status", "UNREGISTERED")),
            quality_status=str(d.get("quality_status", CoverageStatus.UNAVAILABLE.value)),
            quality_score=d.get("quality_score"),
            data_mode=str(d.get("data_mode", "UNAVAILABLE")),
            latest_price_date=d.get("latest_price_date"),
            latest_institutional_date=d.get("latest_institutional_date"),
            latest_margin_date=d.get("latest_margin_date"),
            latest_revenue_period=d.get("latest_revenue_period"),
            latest_financial_period=d.get("latest_financial_period"),
            ohlcv_available=bool(d.get("ohlcv_available", False)),
            technical_available=bool(d.get("technical_available", False)),
            institutional_available=bool(d.get("institutional_available", False)),
            margin_available=bool(d.get("margin_available", False)),
            fundamental_available=bool(d.get("fundamental_available", False)),
            shareholder_available=bool(d.get("shareholder_available", False)),
            etf_overlap_available=bool(d.get("etf_overlap_available", False)),
            precise_price_allowed=bool(d.get("precise_price_allowed", False)),
            backtest_allowed=bool(d.get("backtest_allowed", False)),
            abc_buy_point_allowed=bool(d.get("abc_buy_point_allowed", False)),
            blocking_reasons=list(d.get("blocking_reasons", [])),
            warnings=list(d.get("warnings", [])),
            checked_at=str(d.get("checked_at", _now_iso())),
            metadata=dict(d.get("metadata", {})),
        )


@dataclass
class UniverseSummary:
    """
    Aggregate summary of a universe scan.

    [!] Summary counts do NOT indicate tradeable status. Research Only.
    """
    universe_id: str = ""
    total_symbols: int = 0
    enabled_symbols: int = 0
    active_symbols: int = 0

    # Tier counts
    core_count: int = 0
    research_count: int = 0
    extended_count: int = 0
    watchlist_count: int = 0
    excluded_count: int = 0

    # Market counts
    twse_count: int = 0
    tpex_count: int = 0
    emerging_count: int = 0

    # Security type counts
    common_stock_count: int = 0
    etf_count: int = 0
    unknown_type_count: int = 0

    # Coverage status counts
    ready_count: int = 0
    partial_count: int = 0
    missing_count: int = 0
    stale_count: int = 0
    blocked_count: int = 0
    unavailable_count: int = 0
    demo_only_count: int = 0

    latest_scan_at: Optional[str] = None
    profile: str = ""
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "universe_id": self.universe_id,
            "total_symbols": self.total_symbols,
            "enabled_symbols": self.enabled_symbols,
            "active_symbols": self.active_symbols,
            "core_count": self.core_count,
            "research_count": self.research_count,
            "extended_count": self.extended_count,
            "watchlist_count": self.watchlist_count,
            "excluded_count": self.excluded_count,
            "twse_count": self.twse_count,
            "tpex_count": self.tpex_count,
            "emerging_count": self.emerging_count,
            "common_stock_count": self.common_stock_count,
            "etf_count": self.etf_count,
            "unknown_type_count": self.unknown_type_count,
            "ready_count": self.ready_count,
            "partial_count": self.partial_count,
            "missing_count": self.missing_count,
            "stale_count": self.stale_count,
            "blocked_count": self.blocked_count,
            "unavailable_count": self.unavailable_count,
            "demo_only_count": self.demo_only_count,
            "latest_scan_at": self.latest_scan_at,
            "profile": self.profile,
            "metadata": self.metadata,
        }
