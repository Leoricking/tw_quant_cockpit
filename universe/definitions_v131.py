"""
universe/definitions_v131.py — Built-in universe definitions for v1.3.1.

[!] BUILT_IN_SEED — NOT REAL_MARKET_MASTER.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] These are seed research definitions, not official market data. Not Investment Advice.
"""
from __future__ import annotations

from universe.models import UniverseDefinition, UniverseMarket, SecurityType, UniverseTier

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS             = True
BROKER_DISABLED            = True
PRODUCTION_TRADING_BLOCKED = True

# ---------------------------------------------------------------------------
# BUILT_IN_SEED core 14 symbols
# Source: existing config/universe/core_14.csv and watchlist.csv
# [!] NOT REAL_MARKET_MASTER. Research seed only.
# ---------------------------------------------------------------------------
CORE_14_SYMBOLS = [
    "2330",   # 台積電 TSMC
    "2308",   # 台達電 Delta Electronics
    "2345",   # 智邦 Accton
    "2454",   # 聯發科 MediaTek
    "6669",   # 緯穎 Wiwynn
    "3661",   # 世芯-KY Alchip
    "3228",   # 金麗科 Sinorich
    "5274",   # 信驊 ASPEED
    "2376",   # 技嘉 Gigabyte
    "2383",   # 台光電 Elite Material
    "6213",   # 聯茂 EMC
    "2382",   # 廣達 Quanta
    "2356",   # 英業達 Inventec
    "3706",   # 神達 Synnex
]

CORE_14_METADATA = {
    "2330": {"name": "台積電", "market": UniverseMarket.TWSE.value, "industry": "Foundry"},
    "2308": {"name": "台達電", "market": UniverseMarket.TWSE.value, "industry": "Power/Thermal"},
    "2345": {"name": "智邦",   "market": UniverseMarket.TWSE.value, "industry": "Networking"},
    "2454": {"name": "聯發科", "market": UniverseMarket.TWSE.value, "industry": "IC Design"},
    "6669": {"name": "緯穎",   "market": UniverseMarket.TWSE.value, "industry": "Server/ODM"},
    "3661": {"name": "世芯-KY","market": UniverseMarket.TWSE.value, "industry": "ASIC Design"},
    "3228": {"name": "金麗科", "market": UniverseMarket.TWSE.value, "industry": "IC Design"},
    "5274": {"name": "信驊",   "market": UniverseMarket.TWSE.value, "industry": "IC Design"},
    "2376": {"name": "技嘉",   "market": UniverseMarket.TWSE.value, "industry": "PC/Motherboard"},
    "2383": {"name": "台光電", "market": UniverseMarket.TWSE.value, "industry": "CCL/PCB"},
    "6213": {"name": "聯茂",   "market": UniverseMarket.TPEX.value, "industry": "CCL/PCB"},
    "2382": {"name": "廣達",   "market": UniverseMarket.TWSE.value, "industry": "ODM/Server"},
    "2356": {"name": "英業達", "market": UniverseMarket.TWSE.value, "industry": "ODM/Server"},
    "3706": {"name": "神達",   "market": UniverseMarket.TWSE.value, "industry": "IT Services"},
}

# Research tier adds more symbols from the existing tier registry
RESEARCH_EXTRA_SYMBOLS = [
    "2317",   # 鴻海 Hon Hai
    "3017",   # 奇鋐 Auras
    "3008",   # 大立光
    "2412",   # 中華電
    "2882",   # 國泰金
]

# Extended universe allows large registration — quality gate required for formal analysis
EXTENDED_SYMBOLS: list = []  # empty by default — must be explicitly added by user


def get_core_universe() -> UniverseDefinition:
    """
    Return the built-in CORE universe definition.
    [!] BUILT_IN_SEED. NOT REAL_MARKET_MASTER. Research Only.
    """
    return UniverseDefinition(
        universe_id="core",
        name="Core 14 Research Universe",
        description=(
            "Built-in seed universe: 14 core Taiwan stocks for research. "
            "BUILT_IN_SEED — NOT REAL_MARKET_MASTER. Not Investment Advice."
        ),
        market_scope=[UniverseMarket.TWSE.value, UniverseMarket.TPEX.value],
        security_types=[SecurityType.COMMON_STOCK.value],
        tiers=[UniverseTier.CORE.value],
        symbols=list(CORE_14_SYMBOLS),
        active_only=True,
        source="BUILT_IN_SEED",
        version="1.3.1",
        metadata={
            "note": "BUILT_IN_SEED — NOT REAL_MARKET_MASTER",
            "research_only": True,
            "no_real_orders": True,
        },
    )


def get_research_universe() -> UniverseDefinition:
    """
    Return the built-in RESEARCH universe (extends core).
    [!] BUILT_IN_SEED. NOT REAL_MARKET_MASTER. Research Only.
    """
    symbols = list(CORE_14_SYMBOLS) + RESEARCH_EXTRA_SYMBOLS
    return UniverseDefinition(
        universe_id="research",
        name="Research Universe (Core + Extra)",
        description=(
            "Built-in research universe: extends core with additional symbols. "
            "BUILT_IN_SEED — NOT REAL_MARKET_MASTER. Not Investment Advice."
        ),
        market_scope=[UniverseMarket.TWSE.value, UniverseMarket.TPEX.value],
        security_types=[SecurityType.COMMON_STOCK.value],
        tiers=[UniverseTier.CORE.value, UniverseTier.RESEARCH.value],
        symbols=symbols,
        active_only=True,
        source="BUILT_IN_SEED",
        version="1.3.1",
        metadata={
            "note": "BUILT_IN_SEED — NOT REAL_MARKET_MASTER",
            "research_only": True,
            "no_real_orders": True,
        },
    )


def get_extended_universe() -> UniverseDefinition:
    """
    Return the EXTENDED universe definition.
    [!] Large registration — quality gate required for formal analysis.
    [!] BUILT_IN_SEED. NOT REAL_MARKET_MASTER. Research Only.
    """
    symbols = list(CORE_14_SYMBOLS) + RESEARCH_EXTRA_SYMBOLS + list(EXTENDED_SYMBOLS)
    return UniverseDefinition(
        universe_id="extended",
        name="Extended Universe",
        description=(
            "Extended research universe. Quality gate required before formal analysis. "
            "BUILT_IN_SEED — NOT REAL_MARKET_MASTER. Not Investment Advice."
        ),
        market_scope=[
            UniverseMarket.TWSE.value,
            UniverseMarket.TPEX.value,
            UniverseMarket.EMERGING.value,
        ],
        security_types=[
            SecurityType.COMMON_STOCK.value,
            SecurityType.ETF.value,
            SecurityType.UNKNOWN.value,
        ],
        tiers=[
            UniverseTier.CORE.value,
            UniverseTier.RESEARCH.value,
            UniverseTier.EXTENDED.value,
        ],
        symbols=symbols,
        active_only=True,
        source="BUILT_IN_SEED",
        version="1.3.1",
        metadata={
            "note": "Quality gate required for formal analysis. NOT REAL_MARKET_MASTER.",
            "research_only": True,
            "no_real_orders": True,
        },
    )


def get_watchlist_universe(watchlist_symbols: list = None) -> UniverseDefinition:
    """
    Return the WATCHLIST universe.
    Follows existing user watchlist (config/watchlist.csv).
    [!] Research Only. Not Investment Advice.
    """
    if watchlist_symbols is None:
        watchlist_symbols = _load_watchlist()
    return UniverseDefinition(
        universe_id="watchlist",
        name="User Watchlist",
        description=(
            "User watchlist universe. Follows config/watchlist.csv. "
            "Research Only. Not Investment Advice."
        ),
        market_scope=[UniverseMarket.TWSE.value, UniverseMarket.TPEX.value],
        security_types=[SecurityType.COMMON_STOCK.value, SecurityType.ETF.value],
        tiers=[UniverseTier.WATCHLIST.value],
        symbols=list(watchlist_symbols),
        active_only=True,
        source="user_watchlist",
        version="1.3.1",
        metadata={
            "note": "Follows user config/watchlist.csv. Research Only.",
            "research_only": True,
            "no_real_orders": True,
        },
    )


def get_excluded_universe() -> UniverseDefinition:
    """
    Return the EXCLUDED universe definition.
    Used to mark warrants, delisted, unsupported, invalid symbols, etc.
    [!] Research Only. Not Investment Advice.
    """
    return UniverseDefinition(
        universe_id="excluded",
        name="Excluded Symbols",
        description=(
            "Symbols excluded from formal research universe: warrants, delisted, "
            "duplicate conflicts, permanently unavailable, unsupported. "
            "Research Only. Not Investment Advice."
        ),
        market_scope=[],
        security_types=[
            SecurityType.WARRANT.value,
            SecurityType.UNKNOWN.value,
        ],
        tiers=[UniverseTier.EXCLUDED.value],
        symbols=[],
        active_only=False,
        source="EXCLUDED",
        version="1.3.1",
        metadata={
            "note": "Excluded from formal analysis. Research Only.",
            "research_only": True,
            "no_real_orders": True,
        },
    )


def get_all_builtin_universes() -> dict:
    """Return dict of all built-in universe definitions."""
    return {
        "core": get_core_universe(),
        "research": get_research_universe(),
        "extended": get_extended_universe(),
        "watchlist": get_watchlist_universe(),
        "excluded": get_excluded_universe(),
    }


def _load_watchlist() -> list:
    """Load watchlist from config/watchlist.csv. Returns list of symbol strings."""
    import csv
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    watchlist_path = os.path.join(base_dir, "config", "watchlist.csv")
    symbols = []
    try:
        if os.path.isfile(watchlist_path):
            with open(watchlist_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sym = str(row.get("symbol", "")).strip()
                    enabled = str(row.get("enabled", "1")).strip()
                    if sym and enabled not in ("0", "false", "False"):
                        symbols.append(sym)
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning("Could not load watchlist: %s", exc)
    return symbols
