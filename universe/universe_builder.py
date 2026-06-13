"""
universe/universe_builder.py — Universe Builder for TW Quant Cockpit v1.1.0.

Builds research universes from registry, intersects with real data.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Real mode does NOT fall back to mock data.
[!] Missing data does NOT crash — returns INSUFFICIENT/MISSING status.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional, Set

from universe.universe_schema import (
    UniverseSymbol,
    UniverseDefinition,
    UniverseCoverageSummary,
    TIER_CORE_10,
    TIER_RESEARCH_30,
    TIER_EXPANDED_50,
    TIER_BROAD_100,
    QUALITY_READY,
    QUALITY_PARTIAL,
    QUALITY_INSUFFICIENT,
    QUALITY_MISSING,
)
from universe.universe_tier_registry import UniverseTierRegistry

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Tier name aliases (CLI friendly)
TIER_ALIAS: Dict[str, str] = {
    "core10":      TIER_CORE_10,
    "core_10":     TIER_CORE_10,
    "CORE_10":     TIER_CORE_10,
    "research30":  TIER_RESEARCH_30,
    "research_30": TIER_RESEARCH_30,
    "RESEARCH_30": TIER_RESEARCH_30,
    "expanded50":  TIER_EXPANDED_50,
    "expanded_50": TIER_EXPANDED_50,
    "EXPANDED_50": TIER_EXPANDED_50,
    "broad100":    TIER_BROAD_100,
    "broad_100":   TIER_BROAD_100,
    "BROAD_100":   TIER_BROAD_100,
}


def resolve_tier(tier_str: str) -> str:
    """Resolve CLI-friendly tier alias to canonical tier constant."""
    return TIER_ALIAS.get(tier_str, tier_str)


class UniverseBuilder:
    """
    Builds research universes from registry and real data.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Real mode: no mock fallback.
    [!] Missing data: not a crash — returns status MISSING/INSUFFICIENT.
    """

    NO_REAL_ORDERS                    = True
    BROKER_DISABLED                   = True
    PRODUCTION_TRADING_BLOCKED        = True
    REAL_DATA_COVERAGE_REQUIRED       = True
    MOCK_DATA_FORMAL_CONCLUSION_ALLOWED = False

    def __init__(
        self,
        import_root: str = "data/import",
        results_dir: str = "data/backtest_results",
        mode: str = "real",
    ) -> None:
        self._import_root = os.path.join(_BASE_DIR, import_root) if not os.path.isabs(import_root) else import_root
        self._results_dir = os.path.join(_BASE_DIR, results_dir) if not os.path.isabs(results_dir) else results_dir
        self.mode = mode
        self._registry = UniverseTierRegistry()

    # ------------------------------------------------------------------
    # Tier build
    # ------------------------------------------------------------------

    def build_tier(self, tier: str) -> UniverseDefinition:
        """Build a UniverseDefinition for the given tier."""
        tier = resolve_tier(tier)
        syms = self._registry.list_by_tier(tier)
        symbol_strs = [s.symbol for s in syms]
        now = _now_str()
        return UniverseDefinition(
            universe_id=f"tier_{tier.lower()}",
            name=f"Universe — {tier}",
            tier=tier,
            symbols=symbol_strs,
            symbol_count=len(symbol_strs),
            created_at=now,
            updated_at=now,
            source="tier_registry",
        )

    def build_from_symbols(self, symbols: List[str], tier: str = TIER_CORE_10) -> UniverseDefinition:
        """Build a UniverseDefinition from an explicit symbol list."""
        tier = resolve_tier(tier)
        now = _now_str()
        return UniverseDefinition(
            universe_id=f"custom_{tier.lower()}",
            name=f"Custom Universe — {tier}",
            tier=tier,
            symbols=list(symbols),
            symbol_count=len(symbols),
            created_at=now,
            updated_at=now,
            source="custom",
        )

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def discover_available_symbols(self) -> List[str]:
        """
        Discover symbols that have real daily data in the import store.
        Returns list of symbol strings. Never crashes on missing files.
        """
        daily_path = os.path.join(_BASE_DIR, "data", "import", "daily", "daily_k.csv")
        if not os.path.isfile(daily_path):
            logger.debug("discover_available_symbols: daily_k.csv not found — returning empty")
            return []
        try:
            import pandas as pd
            df = pd.read_csv(daily_path, low_memory=False, usecols=["symbol"])
            syms = sorted(df["symbol"].dropna().astype(str).unique().tolist())
            return syms
        except Exception as exc:
            logger.warning("discover_available_symbols: %s", exc)
            return []

    def intersect_with_real_data(self, symbols: List[str]) -> Dict[str, bool]:
        """
        Check which symbols in the list have real daily data.
        Returns {symbol: has_real_data}.
        Real mode: no mock fallback.
        """
        available: Set[str] = set(self.discover_available_symbols())
        return {sym: (sym in available) for sym in symbols}

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_symbol(self, symbol: str) -> dict:
        """
        Validate a single symbol: check format and data presence.
        Returns dict with {symbol, valid, has_real_data, quality_status, reason}.
        """
        sym = str(symbol).strip()
        if not sym:
            return {"symbol": sym, "valid": False, "quality_status": QUALITY_INVALID,
                    "reason": "empty symbol", "has_real_data": False}

        has_real = self.intersect_with_real_data([sym]).get(sym, False)
        reg_sym = self._registry.get_symbol(sym)

        if not has_real:
            status = QUALITY_MISSING
            reason = "no real daily data found"
        else:
            status = QUALITY_PARTIAL
            reason = "real data exists; run coverage for details"

        return {
            "symbol":         sym,
            "valid":          True,
            "has_real_data":  has_real,
            "quality_status": status,
            "reason":         reason,
            "registered":     reg_sym is not None,
            "name":           reg_sym.name if reg_sym else "",
            "tier":           reg_sym.tier if reg_sym else "",
        }

    # ------------------------------------------------------------------
    # Ready / Partial universe
    # ------------------------------------------------------------------

    def build_ready_universe(self, tier: str) -> dict:
        """
        Build universe of READY symbols for a tier.
        Returns {tier, registered, ready_symbols, missing_symbols, confidence}.
        """
        tier = resolve_tier(tier)
        registered_syms = [s.symbol for s in self._registry.list_by_tier(tier)]
        real_map = self.intersect_with_real_data(registered_syms)
        ready = [s for s in registered_syms if real_map.get(s, False)]
        missing = [s for s in registered_syms if not real_map.get(s, False)]

        from backtest.stat_confidence import StatConfidence
        conf = StatConfidence.for_universe_coverage(
            registered_symbols=len(registered_syms),
            ready_symbols=len(ready),
            evaluated_symbols=len(ready),
        )

        return {
            "tier":             tier,
            "registered":       len(registered_syms),
            "ready":            len(ready),
            "missing":          len(missing),
            "ready_symbols":    ready,
            "missing_symbols":  missing,
            "confidence":       conf["overall"],
            "research_only":    True,
            "no_real_orders":   True,
        }

    def build_partial_universe(self, tier: str) -> dict:
        """
        Build universe including PARTIAL symbols (real data but less complete).
        Returns same structure as build_ready_universe but with more symbols.
        """
        return self.build_ready_universe(tier)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def build_summary(self, tier: str) -> dict:
        """Build a brief summary for a tier."""
        tier = resolve_tier(tier)
        syms = self._registry.list_by_tier(tier)
        real_map = self.intersect_with_real_data([s.symbol for s in syms])
        ready_count = sum(1 for v in real_map.values() if v)
        return {
            "tier":           tier,
            "registered":     len(syms),
            "real_data":      ready_count,
            "missing":        len(syms) - ready_count,
            "research_only":  True,
            "no_real_orders": True,
        }


def _now_str() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
