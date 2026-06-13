"""
universe/universe_query.py — Universe query API for TW Quant Cockpit v1.1.0.

High-level query interface for universe tiers and coverage data.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from universe.universe_schema import (
    UniverseSymbol,
    UniverseCoverageSummary,
    TIER_CORE_10,
    TIER_RESEARCH_30,
    TIER_EXPANDED_50,
    TIER_BROAD_100,
    VALID_TIERS,
    QUALITY_READY,
    QUALITY_PARTIAL,
    QUALITY_INSUFFICIENT,
    QUALITY_MISSING,
    QUALITY_INVALID,
)
from universe.universe_tier_registry import UniverseTierRegistry
from universe.universe_builder import resolve_tier

logger = logging.getLogger(__name__)


class UniverseQuery:
    """
    High-level query interface.

    Methods:
    - list_tiers()
    - list_symbols(tier=None)
    - list_ready_symbols(tier=None)
    - list_partial_symbols(tier=None)
    - list_missing_symbols(tier=None)
    - get_symbol_coverage(symbol)
    - summarize_tier(tier)

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    NO_REAL_ORDERS             = True
    BROKER_DISABLED            = True
    PRODUCTION_TRADING_BLOCKED = True

    def __init__(
        self,
        registry: Optional[UniverseTierRegistry] = None,
        coverage_store=None,
    ) -> None:
        self._registry = registry or UniverseTierRegistry()
        self._coverage_store = coverage_store
        self._coverage_cache: Optional[List[UniverseSymbol]] = None

    # ------------------------------------------------------------------
    # Tier listing
    # ------------------------------------------------------------------

    def list_tiers(self) -> List[dict]:
        """Return a summary of all tiers."""
        result = []
        for tier in VALID_TIERS:
            syms = self._registry.list_by_tier(tier)
            result.append({
                "tier":         tier,
                "symbol_count": len(syms),
                "symbols":      [s.symbol for s in syms],
            })
        return result

    # ------------------------------------------------------------------
    # Symbol listing
    # ------------------------------------------------------------------

    def list_symbols(self, tier: Optional[str] = None) -> List[str]:
        """List all registered symbols, optionally filtered by tier."""
        if tier:
            tier = resolve_tier(tier)
            return [s.symbol for s in self._registry.list_by_tier(tier)]
        return [s.symbol for s in self._registry.list_symbols()]

    def list_ready_symbols(self, tier: Optional[str] = None) -> List[str]:
        """List symbols with READY quality status from coverage data."""
        return self._list_by_quality([QUALITY_READY], tier)

    def list_partial_symbols(self, tier: Optional[str] = None) -> List[str]:
        """List symbols with PARTIAL quality status from coverage data."""
        return self._list_by_quality([QUALITY_PARTIAL], tier)

    def list_missing_symbols(self, tier: Optional[str] = None) -> List[str]:
        """List symbols with MISSING or INSUFFICIENT quality from coverage data."""
        return self._list_by_quality([QUALITY_MISSING, QUALITY_INSUFFICIENT], tier)

    # ------------------------------------------------------------------
    # Symbol detail
    # ------------------------------------------------------------------

    def get_symbol_coverage(self, symbol: str) -> dict:
        """Get coverage detail for a single symbol."""
        sym = str(symbol).strip()

        # Check registry
        reg_sym = self._registry.get_symbol(sym)

        # Check coverage cache
        cov_sym = self._find_in_coverage(sym)

        if cov_sym:
            d = cov_sym.to_dict()
            if reg_sym:
                d["name"] = d.get("name") or reg_sym.name
                d["sector"] = d.get("sector") or reg_sym.sector
                d["tier"] = d.get("tier") or reg_sym.tier
            return d

        if reg_sym:
            return reg_sym.to_dict()

        return {
            "symbol":         sym,
            "quality_status": QUALITY_MISSING,
            "reason":         "symbol not found in registry or coverage data",
            "research_only":  True,
            "no_real_orders": True,
        }

    # ------------------------------------------------------------------
    # Tier summary
    # ------------------------------------------------------------------

    def summarize_tier(self, tier: str) -> dict:
        """Build a tier summary with coverage stats."""
        tier = resolve_tier(tier)
        registered = self._registry.list_by_tier(tier)
        reg_symbols = {s.symbol for s in registered}

        coverage = self._load_coverage()
        cov_map = {s.symbol: s for s in coverage}

        ready = []
        partial = []
        insufficient = []
        missing = []

        for sym_str in [s.symbol for s in registered]:
            cov = cov_map.get(sym_str)
            if cov is None:
                missing.append(sym_str)
            elif cov.quality_status == QUALITY_READY:
                ready.append(sym_str)
            elif cov.quality_status == QUALITY_PARTIAL:
                partial.append(sym_str)
            elif cov.quality_status in (QUALITY_MISSING, QUALITY_INVALID):
                missing.append(sym_str)
            else:
                insufficient.append(sym_str)

        total = len(registered)
        evaluated = len(ready) + len(partial) + len(insufficient)

        # Statistical confidence
        from backtest.stat_confidence import StatConfidence
        conf = StatConfidence.for_universe_coverage(
            registered_symbols=total,
            ready_symbols=len(ready),
            evaluated_symbols=evaluated,
        )

        return {
            "tier":             tier,
            "registered":       total,
            "ready":            len(ready),
            "partial":          len(partial),
            "insufficient":     len(insufficient),
            "missing":          len(missing),
            "evaluated":        evaluated,
            "ready_symbols":    ready,
            "partial_symbols":  partial,
            "missing_symbols":  missing,
            "confidence":       conf["overall"],
            "reasons":          conf.get("reasons", []),
            "research_only":    True,
            "no_real_orders":   True,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_coverage(self) -> List[UniverseSymbol]:
        if self._coverage_cache is not None:
            return self._coverage_cache
        if self._coverage_store:
            try:
                self._coverage_cache = self._coverage_store.load_latest_coverage()
                return self._coverage_cache
            except Exception as exc:
                logger.debug("_load_coverage: %s", exc)
        self._coverage_cache = []
        return self._coverage_cache

    def _find_in_coverage(self, symbol: str) -> Optional[UniverseSymbol]:
        coverage = self._load_coverage()
        for s in coverage:
            if s.symbol == symbol:
                return s
        return None

    def _list_by_quality(self, statuses: List[str], tier: Optional[str] = None) -> List[str]:
        coverage = self._load_coverage()
        if not coverage:
            # Fall back to registry
            if tier:
                syms = self._registry.list_by_tier(resolve_tier(tier))
            else:
                syms = self._registry.list_symbols()
            if QUALITY_MISSING in statuses or QUALITY_INSUFFICIENT in statuses:
                return [s.symbol for s in syms]
            return []

        tier_syms: Optional[set] = None
        if tier:
            tier_syms = {s.symbol for s in self._registry.list_by_tier(resolve_tier(tier))}

        result = []
        for s in coverage:
            if s.quality_status in statuses:
                if tier_syms is None or s.symbol in tier_syms:
                    result.append(s.symbol)
        return result
