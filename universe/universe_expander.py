"""
universe/universe_expander.py - Universe expansion proposal engine (v0.3.25).

Proposes expansion candidates for research universes.
First version uses static seed list + existing import data symbols.
Does NOT fetch external data. Does NOT overwrite without --write flag.

[!] Research Only. Not investment advice. Not for trading.
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UniverseExpander:
    """
    Proposes expansion candidates for a universe.

    Parameters
    ----------
    source_universe : starting universe name (e.g., 'core_30')
    target_size     : desired universe size
    import_root     : data/import/ path
    results_dir     : data/backtest_results/ path
    config_dir      : config/universe/ path
    """

    read_only         = True
    no_real_orders    = True
    production_blocked = True

    def __init__(
        self,
        source_universe: str = "core_30",
        target_size:     int = 50,
        import_root:     str = "data/import",
        results_dir:     str = "data/backtest_results",
        config_dir:      str = "config/universe",
    ):
        self.source_universe = source_universe
        self.target_size     = target_size
        self._import_root    = os.path.join(_BASE_DIR, import_root) if not os.path.isabs(import_root) else import_root
        self._results_dir    = os.path.join(_BASE_DIR, results_dir) if not os.path.isabs(results_dir) else results_dir
        self._config_dir     = os.path.join(_BASE_DIR, config_dir)  if not os.path.isabs(config_dir)  else config_dir

        self._source_symbols: List[str] = []
        self._all_candidates: List[dict] = []

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def propose_expansion(self) -> dict:
        """
        Propose expansion candidates.
        Returns dict with candidates, reasoning, and warnings.
        Does NOT auto-write to universe config.
        """
        from universe.universe_registry import UniverseRegistry
        reg = UniverseRegistry(config_dir=self._config_dir)
        source_rows = reg.load_universe(self.source_universe)
        self._source_symbols = [r["symbol"] for r in source_rows if r.get("symbol")]

        # Load seed for candidates
        all_seed = reg._load_seed()
        seed_symbols = {r["symbol"] for r in all_seed}

        # Candidates = symbols in seed but not in source
        existing = set(self._source_symbols)
        candidate_rows = [r for r in all_seed if r.get("symbol") not in existing]

        # Rank candidates
        ranked = self.rank_candidates(candidate_rows)
        filtered = self.filter_by_data_coverage(ranked)
        needed = max(0, self.target_size - len(existing))
        proposed = filtered[:needed]

        # Build result list
        result_rows = []
        for row in proposed:
            sym = row.get("symbol", "")
            has_data = self._has_import_data(sym)
            result_rows.append({
                "symbol":          sym,
                "name":            row.get("name", sym),
                "sector":          row.get("sector", ""),
                "theme_primary":   row.get("theme_primary", ""),
                "theme_secondary": row.get("theme_secondary", ""),
                "supply_chain_role": row.get("supply_chain_role", ""),
                "data_coverage":   "AVAILABLE" if has_data else "MISSING",
                "liquidity_tier":  row.get("liquidity_tier", "UNKNOWN"),
                "reason":          "From seed list" + ("" if has_data else " — data missing"),
                "warning":         "" if has_data else f"No import data found for {sym}",
            })

        return {
            "source_universe":   self.source_universe,
            "source_size":       len(existing),
            "target_size":       self.target_size,
            "proposed_count":    len(proposed),
            "candidates":        result_rows,
            "note":              "Proposal only — use universe-build-defaults or --write to apply",
            "not_investment_advice": True,
            "read_only":         True,
            "no_real_orders":    True,
        }

    def rank_candidates(self, rows: List[dict]) -> List[dict]:
        """Rank candidates: prefer AI-exposure, then data availability."""
        def _score(r):
            ai = r.get("ai_exposure", "LOW")
            ai_score = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(ai, 0)
            has_data = 1 if self._has_import_data(r.get("symbol", "")) else 0
            return (ai_score * 2 + has_data * 3)
        return sorted(rows, key=_score, reverse=True)

    def filter_by_liquidity(self, rows: List[dict]) -> List[dict]:
        """Keep symbols with known or LARGE/MID liquidity tier."""
        return [r for r in rows if r.get("liquidity_tier", "UNKNOWN") != "SMALL"]

    def filter_by_data_coverage(self, rows: List[dict]) -> List[dict]:
        """Prefer symbols with existing import data, but include all."""
        with_data = [r for r in rows if self._has_import_data(r.get("symbol", ""))]
        without   = [r for r in rows if not self._has_import_data(r.get("symbol", ""))]
        return with_data + without

    def filter_by_theme(self, rows: List[dict], themes: List[str]) -> List[dict]:
        """Filter rows to only include specified themes."""
        return [r for r in rows if r.get("theme_primary") in themes or r.get("theme_secondary") in themes]

    def build_core_50(self) -> List[dict]:
        """Return proposed core_50 symbols."""
        from universe.universe_registry import UniverseRegistry
        reg = UniverseRegistry(config_dir=self._config_dir)
        seed = reg._load_seed()
        return seed[:50]

    def build_core_100(self) -> List[dict]:
        from universe.universe_registry import UniverseRegistry
        reg = UniverseRegistry(config_dir=self._config_dir)
        return reg._load_seed()[:100]

    def build_core_200(self) -> List[dict]:
        from universe.universe_registry import UniverseRegistry
        reg = UniverseRegistry(config_dir=self._config_dir)
        return reg._load_seed()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _has_import_data(self, symbol: str) -> bool:
        daily_path = os.path.join(_BASE_DIR, "data", "import", "daily", "daily_k.csv")
        if not os.path.isfile(daily_path):
            return False
        try:
            import pandas as pd
            df = pd.read_csv(daily_path, low_memory=False, usecols=["symbol"])
            return str(symbol) in set(df["symbol"].dropna().astype(str).unique())
        except Exception:
            return False
