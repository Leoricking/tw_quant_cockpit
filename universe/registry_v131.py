"""
universe/registry_v131.py — v1.3.1 Universe Symbol Registry.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Registration != data complete != tradeable. Not Investment Advice.
[!] No network auto-fetch. Runtime registry files must NOT be committed.
[!] Same symbol different market conflict -> NOT silently overwritten.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from universe.models import (
    UniverseMarket,
    UniverseMembership,
    UniverseSummary,
    UniverseTier,
    SecurityType,
    ListingStatus,
    CoverageStatus,
)
from universe.models import UniverseSymbol as UniverseSymbolV131
from universe.symbol_normalizer import SymbolNormalizer

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS             = True
BROKER_DISABLED            = True
PRODUCTION_TRADING_BLOCKED = True
MOCK_FALLBACK_ENABLED      = False

_SCHEMA_VERSION = "1.3.1"
_normalizer = SymbolNormalizer()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class UniverseRegistryV131:
    """
    v1.3.1 Universe Symbol Registry — lightweight JSON-backed.

    Rules:
    - Registration != data complete != tradeable
    - Duplicate symbol: safe merge (update non-source fields, preserve source)
    - Same symbol different market conflict: NOT silently overwritten — returns error
    - Missing stock name: don't crash, store as empty string
    - Missing fields: don't fill with invented values
    - Unknown -> don't convert to real values
    - No network auto-fetch
    - Runtime registry must NOT be committed (use tmp_path in tests)

    [!] Research Only. No Real Orders.
    """

    NO_REAL_ORDERS             = True
    BROKER_DISABLED            = True
    PRODUCTION_TRADING_BLOCKED = True

    def __init__(self, storage_dir: Optional[str] = None) -> None:
        """
        Parameters
        ----------
        storage_dir : Optional directory for JSON storage.
                      If None, uses in-memory only (not persisted).
                      Tests must use tmp_path.
        """
        self._storage_dir = storage_dir
        self._symbols: Dict[str, UniverseSymbolV131] = {}           # symbol -> UniverseSymbolV131
        self._memberships: Dict[str, Dict[str, UniverseMembership]] = {}  # universe_id -> {symbol -> membership}
        self._schema_version = _SCHEMA_VERSION
        if storage_dir:
            os.makedirs(storage_dir, exist_ok=True)
            self._load()

    # ------------------------------------------------------------------
    # Symbol operations
    # ------------------------------------------------------------------

    def register_symbol(self, symbol_data: dict) -> Tuple[bool, str]:
        """
        Register a symbol. Returns (success, message).

        - Registration != data complete != tradeable
        - Duplicate: safe merge
        - Market conflict: blocked (not silently overwritten)
        """
        sym_str = str(symbol_data.get("symbol", "")).strip()
        if not sym_str:
            return False, "Symbol field is empty or missing"

        norm_result = _normalizer.normalize(sym_str)
        if not norm_result.is_valid:
            return False, f"Invalid symbol '{sym_str}': {norm_result.warning}"

        normalized = norm_result.normalized_symbol
        incoming_market = str(symbol_data.get("market", norm_result.detected_market)).strip()

        # Check for market conflict with existing registration
        if normalized in self._symbols:
            existing = self._symbols[normalized]
            if (existing.market != UniverseMarket.UNKNOWN.value
                    and incoming_market != UniverseMarket.UNKNOWN.value
                    and existing.market != incoming_market):
                return (
                    False,
                    f"Market conflict for '{normalized}': registered as {existing.market}, "
                    f"incoming as {incoming_market}. Not silently overwritten.",
                )
            # Safe merge: update non-source/market fields
            if symbol_data.get("stock_name") or symbol_data.get("name"):
                existing.stock_name = str(
                    symbol_data.get("stock_name") or symbol_data.get("name") or existing.stock_name
                )
            if symbol_data.get("industry"):
                existing.industry = str(symbol_data["industry"])
            if symbol_data.get("sub_industry"):
                existing.sub_industry = str(symbol_data["sub_industry"])
            if symbol_data.get("tags"):
                for t in symbol_data["tags"]:
                    if t not in existing.tags:
                        existing.tags.append(t)
            existing.updated_at = _now_iso()
            self._persist()
            return True, f"Symbol '{normalized}' safely merged (already registered)"

        # New registration
        obj = UniverseSymbolV131.from_dict({
            **symbol_data,
            "symbol": normalized,
            "normalized_symbol": normalized,
            "market": incoming_market or norm_result.detected_market,
        })
        # Do not invent values for unknown fields
        if not obj.stock_name and not symbol_data.get("name"):
            obj.stock_name = ""  # empty, not invented

        # Warrant detection
        if obj.is_warrant:
            obj.listing_status = ListingStatus.UNKNOWN.value
            obj.is_active = False  # warrants typically not in formal universe

        self._symbols[normalized] = obj
        self._persist()
        return True, f"Symbol '{normalized}' registered (market={obj.market})"

    def update_symbol(self, symbol: str, updates: dict) -> Tuple[bool, str]:
        """Update fields on an existing symbol. Preserves source and timestamp."""
        norm_result = _normalizer.normalize(symbol)
        normalized = norm_result.normalized_symbol if norm_result.is_valid else symbol.strip()
        if normalized not in self._symbols:
            return False, f"Symbol '{normalized}' not found in registry"
        obj = self._symbols[normalized]
        # Update only non-source fields
        for k, v in updates.items():
            if k in ("source", "registered_at"):
                continue  # Preserve source and original registration timestamp
            if hasattr(obj, k):
                setattr(obj, k, v)
        obj.updated_at = _now_iso()
        self._persist()
        return True, f"Symbol '{normalized}' updated"

    def get_symbol(self, symbol: str) -> Optional[UniverseSymbolV131]:
        """Return UniverseSymbolV131 or None."""
        norm_result = _normalizer.normalize(symbol)
        normalized = norm_result.normalized_symbol if norm_result.is_valid else symbol.strip()
        return self._symbols.get(normalized)

    def list_symbols(self) -> List[UniverseSymbolV131]:
        """Return all registered symbols."""
        return list(self._symbols.values())

    def search_symbols(self, query: str) -> List[UniverseSymbolV131]:
        """Search by symbol code or stock name (case-insensitive)."""
        q = query.lower().strip()
        results = []
        for sym, obj in self._symbols.items():
            if (q in sym.lower()
                    or q in obj.stock_name.lower()
                    or any(q in alias.lower() for alias in obj.aliases)):
                results.append(obj)
        return results

    def deactivate_symbol(self, symbol: str) -> Tuple[bool, str]:
        """Mark a symbol as inactive (does not delete)."""
        obj = self.get_symbol(symbol)
        if obj is None:
            return False, f"Symbol '{symbol}' not found"
        obj.is_active = False
        obj.updated_at = _now_iso()
        self._persist()
        return True, f"Symbol '{symbol}' deactivated"

    def validate_symbol(self, symbol: str) -> Tuple[bool, str]:
        """
        Validate a symbol string for registry use.
        Returns (is_valid, message).
        Valid = parseable 4-6 digit Taiwan code. Does NOT mean data is available.
        """
        result = _normalizer.normalize(symbol)
        if result.is_valid:
            return True, f"'{result.normalized_symbol}' is a valid symbol (market={result.detected_market})"
        return False, f"'{symbol}' is not a valid symbol: {result.warning}"

    # ------------------------------------------------------------------
    # Tier / membership operations
    # ------------------------------------------------------------------

    def assign_tier(
        self,
        symbol: str,
        universe_id: str,
        tier: str,
        enabled: bool = True,
        priority: int = 0,
        inclusion_reason: str = "",
        source: str = "",
    ) -> Tuple[bool, str]:
        """Assign a symbol to a universe tier."""
        obj = self.get_symbol(symbol)
        if obj is None:
            return False, f"Symbol '{symbol}' not registered; register first"
        if universe_id not in self._memberships:
            self._memberships[universe_id] = {}
        norm = obj.symbol
        if norm in self._memberships[universe_id]:
            # Update existing
            m = self._memberships[universe_id][norm]
            m.tier = tier
            m.enabled = enabled
            m.priority = priority
            if inclusion_reason:
                m.inclusion_reason = inclusion_reason
            m.updated_at = _now_iso()
        else:
            self._memberships[universe_id][norm] = UniverseMembership(
                universe_id=universe_id,
                symbol=norm,
                tier=tier,
                enabled=enabled,
                priority=priority,
                inclusion_reason=inclusion_reason,
                source=source,
                added_at=_now_iso(),
                updated_at=_now_iso(),
            )
        self._persist()
        return True, f"'{norm}' assigned to {universe_id}/{tier}"

    def remove_from_tier(self, symbol: str, universe_id: str) -> Tuple[bool, str]:
        """Remove symbol from a universe tier."""
        obj = self.get_symbol(symbol)
        norm = obj.symbol if obj else symbol.strip()
        if universe_id not in self._memberships:
            return False, f"Universe '{universe_id}' not found"
        if norm not in self._memberships[universe_id]:
            return False, f"Symbol '{norm}' not in universe '{universe_id}'"
        del self._memberships[universe_id][norm]
        self._persist()
        return True, f"'{norm}' removed from {universe_id}"

    def list_by_tier(self, universe_id: str, tier: str) -> List[UniverseSymbolV131]:
        """Return all symbols in a universe/tier combination."""
        memberships = self._memberships.get(universe_id, {})
        result = []
        for sym, m in memberships.items():
            if m.tier == tier and m.enabled:
                obj = self._symbols.get(sym)
                if obj:
                    result.append(obj)
        return result

    def list_by_market(self, market: str) -> List[UniverseSymbolV131]:
        """Return all symbols in a given market."""
        return [s for s in self._symbols.values() if s.market == market]

    def list_by_industry(self, industry: str) -> List[UniverseSymbolV131]:
        """Return all symbols in a given industry."""
        return [s for s in self._symbols.values()
                if s.industry.lower() == industry.lower()]

    def list_active(self) -> List[UniverseSymbolV131]:
        """Return all active symbols."""
        return [s for s in self._symbols.values() if s.is_active]

    def list_excluded(self) -> List[UniverseSymbolV131]:
        """Return all symbols assigned to EXCLUDED tier in any universe."""
        excluded_syms = set()
        for uid, members in self._memberships.items():
            for sym, m in members.items():
                if m.tier == UniverseTier.EXCLUDED.value:
                    excluded_syms.add(sym)
        return [s for sym, s in self._symbols.items() if sym in excluded_syms]

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summarize(self, universe_id: Optional[str] = None) -> UniverseSummary:
        """
        Build a UniverseSummary for a universe or all symbols.
        [!] Summary does NOT indicate tradeable status.
        """
        if universe_id:
            memberships = self._memberships.get(universe_id, {})
            symbols = [self._symbols[s] for s in memberships if s in self._symbols]
        else:
            symbols = list(self._symbols.values())

        summary = UniverseSummary(
            universe_id=universe_id or "all",
            total_symbols=len(symbols),
            enabled_symbols=sum(1 for s in symbols if s.is_active),
            active_symbols=sum(1 for s in symbols if s.is_active),
        )

        # Market counts
        for s in symbols:
            if s.market == UniverseMarket.TWSE.value:
                summary.twse_count += 1
            elif s.market == UniverseMarket.TPEX.value:
                summary.tpex_count += 1
            elif s.market == UniverseMarket.EMERGING.value:
                summary.emerging_count += 1

        # Security type counts
        for s in symbols:
            if s.security_type == SecurityType.COMMON_STOCK.value:
                summary.common_stock_count += 1
            elif s.security_type == SecurityType.ETF.value:
                summary.etf_count += 1
            elif s.security_type == SecurityType.UNKNOWN.value:
                summary.unknown_type_count += 1

        # Tier counts (from universe memberships)
        if universe_id:
            for sym, m in self._memberships.get(universe_id, {}).items():
                t = m.tier
                if t == UniverseTier.CORE.value:
                    summary.core_count += 1
                elif t == UniverseTier.RESEARCH.value:
                    summary.research_count += 1
                elif t == UniverseTier.EXTENDED.value:
                    summary.extended_count += 1
                elif t == UniverseTier.WATCHLIST.value:
                    summary.watchlist_count += 1
                elif t == UniverseTier.EXCLUDED.value:
                    summary.excluded_count += 1

        return summary

    # ------------------------------------------------------------------
    # Persistence (JSON-based, lightweight)
    # ------------------------------------------------------------------

    def _persist(self) -> None:
        """Persist registry to JSON files (runtime only — NOT committed)."""
        if not self._storage_dir:
            return
        try:
            symbols_path = os.path.join(self._storage_dir, "symbols.json")
            memberships_path = os.path.join(self._storage_dir, "memberships.json")
            data = {
                "schema_version": self._schema_version,
                "updated_at": _now_iso(),
                "symbols": {k: v.to_dict() for k, v in self._symbols.items()},
            }
            with open(symbols_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            mem_data = {
                "schema_version": self._schema_version,
                "updated_at": _now_iso(),
                "memberships": {
                    uid: {sym: m.to_dict() for sym, m in members.items()}
                    for uid, members in self._memberships.items()
                },
            }
            with open(memberships_path, "w", encoding="utf-8") as f:
                json.dump(mem_data, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.warning("Registry persist error: %s", exc)

    def _load(self) -> None:
        """Load registry from JSON files. Gracefully handles old/unknown schemas."""
        if not self._storage_dir:
            return
        symbols_path = os.path.join(self._storage_dir, "symbols.json")
        memberships_path = os.path.join(self._storage_dir, "memberships.json")
        try:
            if os.path.isfile(symbols_path):
                with open(symbols_path, encoding="utf-8") as f:
                    data = json.load(f)
                # Forward compatible: unknown fields ignored via from_dict
                for k, v in data.get("symbols", {}).items():
                    try:
                        self._symbols[k] = UniverseSymbolV131.from_dict(v)
                    except Exception as e:
                        logger.warning("Skip symbol '%s' on load: %s", k, e)
        except Exception as exc:
            logger.warning("Registry load symbols error: %s", exc)
        try:
            if os.path.isfile(memberships_path):
                with open(memberships_path, encoding="utf-8") as f:
                    mem_data = json.load(f)
                for uid, members in mem_data.get("memberships", {}).items():
                    self._memberships[uid] = {}
                    for sym, m in members.items():
                        try:
                            self._memberships[uid][sym] = UniverseMembership.from_dict(m)
                        except Exception as e:
                            logger.warning("Skip membership '%s/%s' on load: %s", uid, sym, e)
        except Exception as exc:
            logger.warning("Registry load memberships error: %s", exc)
