"""
universe/universe_registry.py - Universe Registry main engine (v0.3.25).

Manages research universe configurations: load, save, validate, and
export universe manifests.

[!] Research Universe Only. Read Only. No Real Orders.
[!] These are safe research configurations, not live trading lists.
[!] Not investment advice.
"""

from __future__ import annotations

import csv
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default universe group names
_DEFAULT_UNIVERSE_GROUPS = [
    "core_14", "core_30", "core_50", "core_100", "core_200",
    "ai_mainstream", "semiconductor", "high_speed_interconnect",
    "server_supply_chain", "power_thermal", "financial",
    "etf_candidates", "institutional_focus",
]

# CSV schema for universe files
_UNIVERSE_SCHEMA = [
    "symbol", "name", "sector", "theme_primary", "theme_secondary",
    "supply_chain_role", "ai_exposure", "etf_relevance",
    "institutional_focus", "liquidity_tier", "market_cap_tier", "notes",
]

# Readiness thresholds
_READINESS_LEVELS = [
    (90, "STRONG_RESEARCH_UNIVERSE"),
    (75, "BACKTEST_READY"),
    (60, "RESEARCH_READY"),
    (40, "OBSERVATIONAL"),
    (0,  "INSUFFICIENT"),
]


class UniverseRegistry:
    """
    Universe Registry: manages research universe configurations.

    Parameters
    ----------
    config_dir   : config/universe/ path
    import_root  : data/import/ path
    results_dir  : data/backtest_results/ path
    """

    read_only         = True
    no_real_orders    = True
    production_blocked = True

    def __init__(
        self,
        config_dir:  str = "config/universe",
        import_root: str = "data/import",
        results_dir: str = "data/backtest_results",
    ):
        self._config_dir  = os.path.join(_BASE_DIR, config_dir) if not os.path.isabs(config_dir) else config_dir
        self._import_root = os.path.join(_BASE_DIR, import_root) if not os.path.isabs(import_root) else import_root
        self._results_dir = os.path.join(_BASE_DIR, results_dir) if not os.path.isabs(results_dir) else results_dir
        self._themes_dir  = os.path.join(self._config_dir, "themes")

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------

    def list_universes(self) -> List[dict]:
        """Return list of all known universe configurations."""
        results = []
        for name in _DEFAULT_UNIVERSE_GROUPS:
            path = self._universe_path(name)
            exists = os.path.isfile(path)
            symbols = self.get_symbols(name) if exists else []
            results.append({
                "name":         name,
                "path":         path,
                "exists":       exists,
                "symbol_count": len(symbols),
                "readiness":    self._quick_readiness(name, symbols),
            })
        return results

    def _quick_readiness(self, name: str, symbols: list) -> str:
        n = len(symbols)
        if n >= 100:
            return "BACKTEST_READY"
        if n >= 50:
            return "RESEARCH_READY"
        if n >= 30:
            return "OBSERVATIONAL"
        if n >= 10:
            return "OBSERVATIONAL"
        return "INSUFFICIENT"

    # ------------------------------------------------------------------
    # Load / save
    # ------------------------------------------------------------------

    def load_universe(self, universe_name: str) -> List[dict]:
        """Load a universe CSV and return list of row dicts."""
        path = self._universe_path(universe_name)
        if not os.path.isfile(path):
            logger.debug("Universe not found: %s", path)
            return []
        try:
            rows = []
            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(dict(row))
            return rows
        except Exception as exc:
            logger.warning("load_universe %s: %s", universe_name, exc)
            return []

    def save_universe(self, universe_name: str, rows: List[dict]) -> str:
        """Save universe rows to CSV. Returns path written."""
        path = self._universe_path(universe_name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not rows:
            return path
        fieldnames = list(rows[0].keys())
        try:
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            logger.info("Universe saved: %s (%d symbols)", path, len(rows))
        except Exception as exc:
            logger.error("save_universe %s: %s", universe_name, exc)
        return path

    def get_symbols(self, universe_name: str) -> List[str]:
        """Return list of symbol strings for a universe."""
        rows = self.load_universe(universe_name)
        return [str(r["symbol"]) for r in rows if r.get("symbol")]

    def get_universe_metadata(self, universe_name: str) -> dict:
        """Return metadata dict for a universe."""
        rows = self.load_universe(universe_name)
        symbols = [r["symbol"] for r in rows if r.get("symbol")]
        sectors = list({r.get("sector", "") for r in rows if r.get("sector")})
        themes  = list({r.get("theme_primary", "") for r in rows if r.get("theme_primary")})
        return {
            "name":         universe_name,
            "symbol_count": len(symbols),
            "symbols":      symbols,
            "sectors":      sectors,
            "themes":       themes,
            "path":         self._universe_path(universe_name),
            "exists":       os.path.isfile(self._universe_path(universe_name)),
            "read_only":    True,
            "research_only": True,
            "not_investment_advice": True,
        }

    def validate_universe(self, universe_name: str) -> dict:
        """Validate a universe config and return validation result."""
        rows = self.load_universe(universe_name)
        issues = []
        if not rows:
            return {"ok": False, "issues": ["Universe file not found or empty"], "symbol_count": 0}
        symbols = [r.get("symbol", "") for r in rows]
        dups = [s for s in set(symbols) if symbols.count(s) > 1]
        if dups:
            issues.append(f"Duplicate symbols: {dups[:5]}")
        missing_name = [r.get("symbol") for r in rows if not r.get("name")]
        if missing_name:
            issues.append(f"{len(missing_name)} symbols missing name")
        return {
            "ok":           not issues,
            "issues":       issues,
            "symbol_count": len(rows),
            "universe_name": universe_name,
        }

    # ------------------------------------------------------------------
    # Build defaults
    # ------------------------------------------------------------------

    def build_default_universes(self, force: bool = False) -> dict:
        """
        Build safe default universe configs from the seed list.
        Does not overwrite existing files unless force=True.
        Returns dict of {name: path} for created files.
        """
        seed = self._load_seed()
        if not seed:
            return {"error": "No seed data found"}

        os.makedirs(self._config_dir, exist_ok=True)
        os.makedirs(self._themes_dir, exist_ok=True)

        created = {}

        # core_14 — first 14 symbols from seed (existing core)
        created.update(self._write_if_needed("core_14", seed[:14], force))
        # core_30 — first 30
        created.update(self._write_if_needed("core_30", seed[:30], force))
        # core_50 — first 50
        created.update(self._write_if_needed("core_50", seed[:50], force))
        # core_100 — first 100 (or all if < 100)
        created.update(self._write_if_needed("core_100", seed[:100], force))
        # core_200 — all
        created.update(self._write_if_needed("core_200", seed, force))

        # Theme universes
        theme_groups = {
            "ai_mainstream":           [r for r in seed if "AI" in str(r.get("theme_primary", "")) or "AI" in str(r.get("theme_secondary", ""))],
            "semiconductor":           [r for r in seed if r.get("sector", "").lower() in ("半導體", "semiconductor", "ic design", "ic設計")],
            "high_speed_interconnect": [r for r in seed if r.get("sector", "").lower() in ("ccl", "pcb", "高速傳輸", "abf")],
            "server_supply_chain":     [r for r in seed if r.get("sector", "").lower() in ("ai server", "odm", "伺服器", "server")],
            "power_thermal":           [r for r in seed if r.get("sector", "").lower() in ("電源散熱", "散熱", "電源", "power", "thermal", "cooling")],
            "financial":               [r for r in seed if r.get("sector", "").lower() in ("金融", "financial", "bank", "insurance")],
            "etf_candidates":          [r for r in seed if r.get("etf_relevance", "0") in ("1", "true", "True", True)],
            "institutional_focus":     [r for r in seed if r.get("institutional_focus", "0") in ("1", "true", "True", True)],
        }
        for tname, trows in theme_groups.items():
            if trows:
                tpath = os.path.join(self._themes_dir, f"{tname}.csv")
                if force or not os.path.isfile(tpath):
                    os.makedirs(self._themes_dir, exist_ok=True)
                    self.save_universe(tname, trows)
                    created[tname] = tpath

        # Write manifest
        manifest_path = self.export_universe_manifest()
        created["manifest"] = manifest_path

        return created

    def _write_if_needed(self, name: str, rows: list, force: bool) -> dict:
        path = self._universe_path(name)
        if not force and os.path.isfile(path):
            return {}
        self.save_universe(name, rows)
        return {name: path}

    def export_universe_manifest(self) -> str:
        """Write config/universe/universe_manifest.yaml and return path."""
        try:
            import yaml as _yaml
        except ImportError:
            _yaml = None

        manifest = {
            "version":        "v0.3.25",
            "generated_at":   datetime.now().isoformat(),
            "read_only":      True,
            "no_real_orders": True,
            "research_only":  True,
            "not_investment_advice": True,
            "universes":      {},
        }
        for name in _DEFAULT_UNIVERSE_GROUPS:
            symbols = self.get_symbols(name)
            manifest["universes"][name] = {
                "symbol_count": len(symbols),
                "path":         f"config/universe/{name}.csv" if not name in ("ai_mainstream","semiconductor","high_speed_interconnect","server_supply_chain","power_thermal","financial","etf_candidates","institutional_focus") else f"config/universe/themes/{name}.csv",
            }

        path = os.path.join(self._config_dir, "universe_manifest.yaml")
        try:
            if _yaml:
                with open(path, "w", encoding="utf-8") as f:
                    _yaml.dump(manifest, f, allow_unicode=True, default_flow_style=False)
            else:
                # Fallback: write as simple text
                lines = [f"# Universe Manifest v0.3.25\n", f"generated_at: {manifest['generated_at']}\n"]
                for k, v in manifest["universes"].items():
                    lines.append(f"{k}:\n  symbol_count: {v['symbol_count']}\n  path: {v['path']}\n")
                with open(path, "w", encoding="utf-8") as f:
                    f.writelines(lines)
            logger.info("Universe manifest written: %s", path)
        except Exception as exc:
            logger.error("export_universe_manifest: %s", exc)
        return path

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _universe_path(self, universe_name: str) -> str:
        theme_names = {"ai_mainstream","semiconductor","high_speed_interconnect",
                       "server_supply_chain","power_thermal","financial",
                       "etf_candidates","institutional_focus"}
        if universe_name in theme_names:
            return os.path.join(self._themes_dir, f"{universe_name}.csv")
        return os.path.join(self._config_dir, f"{universe_name}.csv")

    def _load_seed(self) -> List[dict]:
        """Load from default_universe_seed.csv."""
        seed_path = os.path.join(self._config_dir, "default_universe_seed.csv")
        if not os.path.isfile(seed_path):
            return []
        try:
            rows = []
            with open(seed_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(dict(row))
            return rows
        except Exception as exc:
            logger.warning("_load_seed: %s", exc)
            return []
