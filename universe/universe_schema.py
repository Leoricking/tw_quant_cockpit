"""
universe/universe_schema.py — Universe schema dataclasses for TW Quant Cockpit v1.1.0.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] VALIDATED does not enable trading. Broker Execution Disabled.
[!] Not Investment Advice. Data Universe Expansion — research use only.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

# ---------------------------------------------------------------------------
# Tier constants
# ---------------------------------------------------------------------------
TIER_CORE_10      = "CORE_10"
TIER_RESEARCH_30  = "RESEARCH_30"
TIER_EXPANDED_50  = "EXPANDED_50"
TIER_BROAD_100    = "BROAD_100"

VALID_TIERS = [TIER_CORE_10, TIER_RESEARCH_30, TIER_EXPANDED_50, TIER_BROAD_100]

# ---------------------------------------------------------------------------
# Quality status constants
# ---------------------------------------------------------------------------
QUALITY_READY        = "READY"
QUALITY_PARTIAL      = "PARTIAL"
QUALITY_INSUFFICIENT = "INSUFFICIENT"
QUALITY_MISSING      = "MISSING"
QUALITY_INVALID      = "INVALID"

VALID_QUALITY_STATUSES = [
    QUALITY_READY, QUALITY_PARTIAL, QUALITY_INSUFFICIENT,
    QUALITY_MISSING, QUALITY_INVALID,
]

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS                    = True
BROKER_DISABLED                   = True
PRODUCTION_TRADING_BLOCKED        = True
REAL_DATA_COVERAGE_REQUIRED       = True
MOCK_DATA_FORMAL_CONCLUSION_ALLOWED = False

# ---------------------------------------------------------------------------
# Forbidden outputs (never produce these)
# ---------------------------------------------------------------------------
FORBIDDEN_OUTPUTS = [
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER",
    "AUTO_TRADE", "REAL_TRADE", "LIVE_TRADE", "BROKER_ORDER",
]


@dataclass
class UniverseSymbol:
    """
    A single symbol entry in the research universe.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    symbol: str = ""
    name: str = ""
    market: str = ""
    sector: str = ""
    industry: str = ""
    tier: str = TIER_CORE_10
    active: bool = True
    source: str = ""

    # Data availability flags
    daily_available: bool = False
    volume_available: bool = False
    chips_available: bool = False
    revenue_available: bool = False
    fundamental_available: bool = False

    # Coverage metrics
    first_date: str = ""
    last_date: str = ""
    trading_days: int = 0
    missing_ratio: float = 0.0

    # Quality assessment
    quality_status: str = QUALITY_MISSING
    reason: str = ""

    # Safety flags
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "symbol":               self.symbol,
            "name":                 self.name,
            "market":               self.market,
            "sector":               self.sector,
            "industry":             self.industry,
            "tier":                 self.tier,
            "active":               self.active,
            "source":               self.source,
            "daily_available":      self.daily_available,
            "volume_available":     self.volume_available,
            "chips_available":      self.chips_available,
            "revenue_available":    self.revenue_available,
            "fundamental_available": self.fundamental_available,
            "first_date":           self.first_date,
            "last_date":            self.last_date,
            "trading_days":         self.trading_days,
            "missing_ratio":        self.missing_ratio,
            "quality_status":       self.quality_status,
            "reason":               self.reason,
            "research_only":        self.research_only,
            "no_real_orders":       self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "UniverseSymbol":
        return cls(
            symbol=str(d.get("symbol", "")),
            name=str(d.get("name", "")),
            market=str(d.get("market", "")),
            sector=str(d.get("sector", "")),
            industry=str(d.get("industry", "")),
            tier=str(d.get("tier", TIER_CORE_10)),
            active=bool(d.get("active", True)),
            source=str(d.get("source", "")),
            daily_available=bool(d.get("daily_available", False)),
            volume_available=bool(d.get("volume_available", False)),
            chips_available=bool(d.get("chips_available", False)),
            revenue_available=bool(d.get("revenue_available", False)),
            fundamental_available=bool(d.get("fundamental_available", False)),
            first_date=str(d.get("first_date", "")),
            last_date=str(d.get("last_date", "")),
            trading_days=int(d.get("trading_days", 0)),
            missing_ratio=float(d.get("missing_ratio", 0.0)),
            quality_status=str(d.get("quality_status", QUALITY_MISSING)),
            reason=str(d.get("reason", "")),
        )


@dataclass
class UniverseDefinition:
    """
    A universe tier definition.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    universe_id: str = ""
    name: str = ""
    tier: str = TIER_CORE_10
    symbols: List[str] = field(default_factory=list)
    symbol_count: int = 0
    created_at: str = ""
    updated_at: str = ""
    source: str = "registry"
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "universe_id":   self.universe_id,
            "name":          self.name,
            "tier":          self.tier,
            "symbols":       self.symbols,
            "symbol_count":  len(self.symbols),
            "created_at":    self.created_at,
            "updated_at":    self.updated_at,
            "source":        self.source,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "UniverseDefinition":
        syms = d.get("symbols", [])
        if isinstance(syms, str):
            syms = [s.strip() for s in syms.split(",") if s.strip()]
        return cls(
            universe_id=str(d.get("universe_id", "")),
            name=str(d.get("name", "")),
            tier=str(d.get("tier", TIER_CORE_10)),
            symbols=list(syms),
            symbol_count=int(d.get("symbol_count", len(syms))),
            created_at=str(d.get("created_at", "")),
            updated_at=str(d.get("updated_at", "")),
            source=str(d.get("source", "registry")),
        )


@dataclass
class UniverseCoverageSummary:
    """
    Coverage summary for a universe tier.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    universe_id: str = ""
    symbol_count: int = 0

    # Ready counts per data type
    daily_ready: int = 0
    volume_ready: int = 0
    chips_ready: int = 0
    revenue_ready: int = 0
    fundamental_ready: int = 0

    # Quality metrics
    average_trading_days: float = 0.0
    average_missing_ratio: float = 0.0

    # Symbol buckets
    ready_symbols: List[str] = field(default_factory=list)
    partial_symbols: List[str] = field(default_factory=list)
    insufficient_symbols: List[str] = field(default_factory=list)
    missing_symbols: List[str] = field(default_factory=list)

    # Statistical confidence
    confidence: str = "INSUFFICIENT"

    # Safety
    research_only: bool = True
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "universe_id":            self.universe_id,
            "symbol_count":           self.symbol_count,
            "daily_ready":            self.daily_ready,
            "volume_ready":           self.volume_ready,
            "chips_ready":            self.chips_ready,
            "revenue_ready":          self.revenue_ready,
            "fundamental_ready":      self.fundamental_ready,
            "average_trading_days":   self.average_trading_days,
            "average_missing_ratio":  self.average_missing_ratio,
            "ready_symbols":          self.ready_symbols,
            "partial_symbols":        self.partial_symbols,
            "insufficient_symbols":   self.insufficient_symbols,
            "missing_symbols":        self.missing_symbols,
            "confidence":             self.confidence,
            "research_only":          self.research_only,
            "no_real_orders":         self.no_real_orders,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "UniverseCoverageSummary":
        def _list(v):
            if isinstance(v, list):
                return v
            if isinstance(v, str):
                return [s.strip() for s in v.split(",") if s.strip()]
            return []
        return cls(
            universe_id=str(d.get("universe_id", "")),
            symbol_count=int(d.get("symbol_count", 0)),
            daily_ready=int(d.get("daily_ready", 0)),
            volume_ready=int(d.get("volume_ready", 0)),
            chips_ready=int(d.get("chips_ready", 0)),
            revenue_ready=int(d.get("revenue_ready", 0)),
            fundamental_ready=int(d.get("fundamental_ready", 0)),
            average_trading_days=float(d.get("average_trading_days", 0.0)),
            average_missing_ratio=float(d.get("average_missing_ratio", 0.0)),
            ready_symbols=_list(d.get("ready_symbols", [])),
            partial_symbols=_list(d.get("partial_symbols", [])),
            insufficient_symbols=_list(d.get("insufficient_symbols", [])),
            missing_symbols=_list(d.get("missing_symbols", [])),
            confidence=str(d.get("confidence", "INSUFFICIENT")),
        )
