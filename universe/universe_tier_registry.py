"""
universe/universe_tier_registry.py — Tier-based Universe Registry for TW Quant Cockpit v1.1.0.

Manages research universe by tiers: CORE_10 / RESEARCH_30 / EXPANDED_50 / BROAD_100.
Central symbol management — do NOT hardcode symbols elsewhere.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not Investment Advice. Data Universe Expansion — research use only.
"""
from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from universe.universe_schema import (
    UniverseSymbol,
    UniverseDefinition,
    TIER_CORE_10,
    TIER_RESEARCH_30,
    TIER_EXPANDED_50,
    TIER_BROAD_100,
    VALID_TIERS,
    QUALITY_MISSING,
)

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Default symbol data — CORE_10
# ---------------------------------------------------------------------------
_CORE_10_SYMBOLS: List[dict] = [
    {"symbol": "2330", "name": "台積電",  "market": "TWSE", "sector": "半導體",    "industry": "Foundry",        "tier": TIER_CORE_10},
    {"symbol": "2308", "name": "台達電",  "market": "TWSE", "sector": "電源散熱",  "industry": "Power/Thermal",  "tier": TIER_CORE_10},
    {"symbol": "2345", "name": "智邦",    "market": "TWSE", "sector": "網通",      "industry": "Networking",     "tier": TIER_CORE_10},
    {"symbol": "2383", "name": "台光電",  "market": "TWSE", "sector": "PCB",       "industry": "CCL/PCB",        "tier": TIER_CORE_10},
    {"symbol": "2454", "name": "聯發科",  "market": "TWSE", "sector": "半導體",    "industry": "IC Design",      "tier": TIER_CORE_10},
    {"symbol": "3017", "name": "奇鋐",    "market": "TWSE", "sector": "電源散熱",  "industry": "Thermal",        "tier": TIER_CORE_10},
    {"symbol": "5274", "name": "信驊",    "market": "TWSE", "sector": "半導體",    "industry": "IC Design",      "tier": TIER_CORE_10},
    {"symbol": "6669", "name": "緯穎",    "market": "TWSE", "sector": "AI Server", "industry": "Server/ODM",     "tier": TIER_CORE_10},
    {"symbol": "2317", "name": "鴻海",    "market": "TWSE", "sector": "ODM",       "industry": "EMS",            "tier": TIER_CORE_10},
    {"symbol": "2327", "name": "國巨",    "market": "TWSE", "sector": "被動元件",  "industry": "Passive",        "tier": TIER_CORE_10},
]

# ---------------------------------------------------------------------------
# RESEARCH_30 — CORE_10 + 20 more (AI server, semicon, networking, PCB, etc.)
# ---------------------------------------------------------------------------
_RESEARCH_30_EXTRA: List[dict] = [
    {"symbol": "3008", "name": "大立光",  "market": "TWSE", "sector": "光學",      "industry": "Optics",         "tier": TIER_RESEARCH_30},
    {"symbol": "2412", "name": "中華電",  "market": "TWSE", "sector": "電信",      "industry": "Telecom",        "tier": TIER_RESEARCH_30},
    {"symbol": "2882", "name": "國泰金",  "market": "TWSE", "sector": "金融",      "industry": "Finance",        "tier": TIER_RESEARCH_30},
    {"symbol": "2303", "name": "聯電",    "market": "TWSE", "sector": "半導體",    "industry": "Foundry",        "tier": TIER_RESEARCH_30},
    {"symbol": "2408", "name": "南亞科",  "market": "TWSE", "sector": "半導體",    "industry": "DRAM",           "tier": TIER_RESEARCH_30},
    {"symbol": "4938", "name": "和碩",    "market": "TWSE", "sector": "ODM",       "industry": "EMS",            "tier": TIER_RESEARCH_30},
    {"symbol": "3034", "name": "聯詠",    "market": "TWSE", "sector": "半導體",    "industry": "IC Design",      "tier": TIER_RESEARCH_30},
    {"symbol": "2357", "name": "華碩",    "market": "TWSE", "sector": "PC",        "industry": "PC/Notebook",    "tier": TIER_RESEARCH_30},
    {"symbol": "2376", "name": "技嘉",    "market": "TWSE", "sector": "AI Server", "industry": "Motherboard",    "tier": TIER_RESEARCH_30},
    {"symbol": "3231", "name": "緯創",    "market": "TWSE", "sector": "AI Server", "industry": "Server/ODM",     "tier": TIER_RESEARCH_30},
    {"symbol": "2379", "name": "瑞昱",    "market": "TWSE", "sector": "半導體",    "industry": "IC Design",      "tier": TIER_RESEARCH_30},
    {"symbol": "6278", "name": "台表科",  "market": "TWSE", "sector": "PCB",       "industry": "PCB",            "tier": TIER_RESEARCH_30},
    {"symbol": "3045", "name": "台灣大",  "market": "TWSE", "sector": "電信",      "industry": "Telecom",        "tier": TIER_RESEARCH_30},
    {"symbol": "2609", "name": "陽明",    "market": "TWSE", "sector": "航運",      "industry": "Shipping",       "tier": TIER_RESEARCH_30},
    {"symbol": "2615", "name": "萬海",    "market": "TWSE", "sector": "航運",      "industry": "Shipping",       "tier": TIER_RESEARCH_30},
    {"symbol": "2886", "name": "兆豐金",  "market": "TWSE", "sector": "金融",      "industry": "Finance",        "tier": TIER_RESEARCH_30},
    {"symbol": "2891", "name": "中信金",  "market": "TWSE", "sector": "金融",      "industry": "Finance",        "tier": TIER_RESEARCH_30},
    {"symbol": "2395", "name": "研華",    "market": "TWSE", "sector": "工業電腦",  "industry": "IPC",            "tier": TIER_RESEARCH_30},
    {"symbol": "6415", "name": "矽力*",   "market": "TWSE", "sector": "半導體",    "industry": "Power IC",       "tier": TIER_RESEARCH_30},
    {"symbol": "2385", "name": "群光",    "market": "TWSE", "sector": "零組件",    "industry": "Component",      "tier": TIER_RESEARCH_30},
]

# ---------------------------------------------------------------------------
# EXPANDED_50 — RESEARCH_30 + 20 more
# ---------------------------------------------------------------------------
_EXPANDED_50_EXTRA: List[dict] = [
    {"symbol": "2884", "name": "玉山金",  "market": "TWSE", "sector": "金融",      "industry": "Finance",        "tier": TIER_EXPANDED_50},
    {"symbol": "2880", "name": "華南金",  "market": "TWSE", "sector": "金融",      "industry": "Finance",        "tier": TIER_EXPANDED_50},
    {"symbol": "5871", "name": "中租*",   "market": "TWSE", "sector": "金融",      "industry": "Finance",        "tier": TIER_EXPANDED_50},
    {"symbol": "3481", "name": "群創",    "market": "TWSE", "sector": "面板",      "industry": "Display",        "tier": TIER_EXPANDED_50},
    {"symbol": "2474", "name": "可成",    "market": "TWSE", "sector": "機殼",      "industry": "Casing",         "tier": TIER_EXPANDED_50},
    {"symbol": "2498", "name": "宏達電",  "market": "TWSE", "sector": "手機",      "industry": "Mobile",         "tier": TIER_EXPANDED_50},
    {"symbol": "2337", "name": "旺宏",    "market": "TWSE", "sector": "半導體",    "industry": "NOR Flash",      "tier": TIER_EXPANDED_50},
    {"symbol": "6505", "name": "台塑化",  "market": "TWSE", "sector": "石化",      "industry": "Petrochemical",  "tier": TIER_EXPANDED_50},
    {"symbol": "1301", "name": "台塑",    "market": "TWSE", "sector": "石化",      "industry": "Petrochemical",  "tier": TIER_EXPANDED_50},
    {"symbol": "1303", "name": "南亞",    "market": "TWSE", "sector": "石化",      "industry": "Petrochemical",  "tier": TIER_EXPANDED_50},
    {"symbol": "2002", "name": "中鋼",    "market": "TWSE", "sector": "鋼鐵",      "industry": "Steel",          "tier": TIER_EXPANDED_50},
    {"symbol": "1216", "name": "統一",    "market": "TWSE", "sector": "食品",      "industry": "Food",           "tier": TIER_EXPANDED_50},
    {"symbol": "2207", "name": "和泰車",  "market": "TWSE", "sector": "汽車",      "industry": "Auto",           "tier": TIER_EXPANDED_50},
    {"symbol": "9910", "name": "豐泰",    "market": "TWSE", "sector": "鞋業",      "industry": "Footwear",       "tier": TIER_EXPANDED_50},
    {"symbol": "8詣", "name": "思源",    "market": "TWSE", "sector": "半導體",    "industry": "EDA",            "tier": TIER_EXPANDED_50},
    {"symbol": "2347", "name": "聯強",    "market": "TWSE", "sector": "通路",      "industry": "Distribution",   "tier": TIER_EXPANDED_50},
    {"symbol": "2344", "name": "華邦電",  "market": "TWSE", "sector": "半導體",    "industry": "DRAM",           "tier": TIER_EXPANDED_50},
    {"symbol": "3702", "name": "大聯大",  "market": "TWSE", "sector": "通路",      "industry": "Distribution",   "tier": TIER_EXPANDED_50},
    {"symbol": "2353", "name": "宏碁",    "market": "TWSE", "sector": "PC",        "industry": "PC/Notebook",    "tier": TIER_EXPANDED_50},
    {"symbol": "2360", "name": "致茂",    "market": "TWSE", "sector": "測試設備",  "industry": "Test Equipment", "tier": TIER_EXPANDED_50},
]


class UniverseTierRegistry:
    """
    Tier-based Universe Registry.

    Manages research symbols by tier: CORE_10 / RESEARCH_30 / EXPANDED_50 / BROAD_100.
    Central symbol management — symbols are defined here, not scattered.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Not Investment Advice.
    """

    NO_REAL_ORDERS                    = True
    BROKER_DISABLED                   = True
    PRODUCTION_TRADING_BLOCKED        = True
    REAL_DATA_COVERAGE_REQUIRED       = True
    MOCK_DATA_FORMAL_CONCLUSION_ALLOWED = False

    def __init__(self) -> None:
        self._symbols: Dict[str, UniverseSymbol] = {}
        self._load_defaults()

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def _load_defaults(self) -> None:
        for row in _CORE_10_SYMBOLS:
            sym = UniverseSymbol(
                symbol=row["symbol"], name=row["name"], market=row["market"],
                sector=row["sector"], industry=row["industry"], tier=row["tier"],
                active=True, source="default_registry",
            )
            self._symbols[row["symbol"]] = sym
        for row in _RESEARCH_30_EXTRA:
            sym = UniverseSymbol(
                symbol=row["symbol"], name=row["name"], market=row["market"],
                sector=row["sector"], industry=row["industry"], tier=row["tier"],
                active=True, source="default_registry",
            )
            self._symbols[row["symbol"]] = sym
        for row in _EXPANDED_50_EXTRA:
            sym = UniverseSymbol(
                symbol=row["symbol"], name=row["name"], market=row["market"],
                sector=row["sector"], industry=row["industry"], tier=row["tier"],
                active=True, source="default_registry",
            )
            self._symbols[row["symbol"]] = sym

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def register_symbol(
        self,
        symbol: str,
        name: str = "",
        market: str = "TWSE",
        sector: str = "",
        industry: str = "",
        tier: str = TIER_RESEARCH_30,
        source: str = "manual",
    ) -> UniverseSymbol:
        """Register a new symbol."""
        sym = UniverseSymbol(
            symbol=symbol, name=name, market=market, sector=sector,
            industry=industry, tier=tier, active=True, source=source,
        )
        self._symbols[symbol] = sym
        return sym

    def update_symbol(self, symbol: str, **kwargs) -> Optional[UniverseSymbol]:
        """Update fields of an existing symbol."""
        sym = self._symbols.get(symbol)
        if sym is None:
            logger.warning("update_symbol: symbol not found: %s", symbol)
            return None
        for k, v in kwargs.items():
            if hasattr(sym, k):
                setattr(sym, k, v)
        return sym

    def deactivate_symbol(self, symbol: str) -> bool:
        """Mark a symbol as inactive (does not delete)."""
        sym = self._symbols.get(symbol)
        if sym is None:
            return False
        sym.active = False
        return True

    def get_symbol(self, symbol: str) -> Optional[UniverseSymbol]:
        """Return UniverseSymbol or None."""
        return self._symbols.get(symbol)

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------

    def list_symbols(self, active_only: bool = True) -> List[UniverseSymbol]:
        """List all symbols, optionally active only."""
        syms = list(self._symbols.values())
        if active_only:
            syms = [s for s in syms if s.active]
        return syms

    def list_by_tier(self, tier: str, active_only: bool = True) -> List[UniverseSymbol]:
        """List symbols for a given tier."""
        if tier == TIER_CORE_10:
            eligible = {TIER_CORE_10}
        elif tier == TIER_RESEARCH_30:
            eligible = {TIER_CORE_10, TIER_RESEARCH_30}
        elif tier == TIER_EXPANDED_50:
            eligible = {TIER_CORE_10, TIER_RESEARCH_30, TIER_EXPANDED_50}
        elif tier == TIER_BROAD_100:
            eligible = set(VALID_TIERS)
        else:
            eligible = {tier}

        syms = [s for s in self._symbols.values() if s.tier in eligible]
        if active_only:
            syms = [s for s in syms if s.active]
        return syms

    def list_symbol_strings(self, tier: Optional[str] = None) -> List[str]:
        """Return list of symbol strings."""
        syms = self.list_by_tier(tier) if tier else self.list_symbols()
        return [s.symbol for s in syms]

    # ------------------------------------------------------------------
    # Build default tiers
    # ------------------------------------------------------------------

    def build_default_tiers(self) -> dict:
        """Re-initialize default tier data. Returns summary dict."""
        self._symbols = {}
        self._load_defaults()
        return {
            TIER_CORE_10:     len(self.list_by_tier(TIER_CORE_10)),
            TIER_RESEARCH_30: len(self.list_by_tier(TIER_RESEARCH_30)),
            TIER_EXPANDED_50: len(self.list_by_tier(TIER_EXPANDED_50)),
            TIER_BROAD_100:   len(self.list_by_tier(TIER_BROAD_100)),
            "total":          len(self._symbols),
        }

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_registry(self, path: str) -> str:
        """Save registry to CSV. Returns path written."""
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        rows = [s.to_dict() for s in self._symbols.values()]
        if not rows:
            return path
        fieldnames = list(rows[0].keys())
        try:
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.info("UniverseTierRegistry saved: %s (%d rows)", path, len(rows))
        except Exception as exc:
            logger.error("save_registry: %s", exc)
        return path

    def load_registry(self, path: str) -> int:
        """Load registry from CSV. Returns number of rows loaded."""
        if not os.path.isfile(path):
            logger.debug("load_registry: file not found: %s", path)
            return 0
        loaded = 0
        try:
            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sym = UniverseSymbol.from_dict(row)
                    self._symbols[sym.symbol] = sym
                    loaded += 1
        except Exception as exc:
            logger.warning("load_registry: %s", exc)
        return loaded

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def get_tier_summary(self) -> dict:
        """Return summary of all tiers."""
        return {
            "tiers": {
                TIER_CORE_10:     len(self.list_by_tier(TIER_CORE_10)),
                TIER_RESEARCH_30: len(self.list_by_tier(TIER_RESEARCH_30)),
                TIER_EXPANDED_50: len(self.list_by_tier(TIER_EXPANDED_50)),
                TIER_BROAD_100:   len(self.list_by_tier(TIER_BROAD_100)),
            },
            "total_active": len(self.list_symbols(active_only=True)),
            "total_all":    len(self._symbols),
            "research_only": True,
            "no_real_orders": True,
        }
