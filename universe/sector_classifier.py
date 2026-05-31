"""
universe/sector_classifier.py - Sector / theme classifier (v0.3.25).

Classifies Taiwan stocks into sector, industry group, and theme taxonomy.

[!] Research Only. Not investment advice.
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Built-in fallback taxonomy (used if YAML not found)
_BUILTIN_TAXONOMY = {
    "semiconductor": {
        "name": "半導體",
        "themes": ["AI", "IC_DESIGN", "FOUNDRY", "MEMORY", "PACKAGING"],
        "keywords": ["半導體", "ic設計", "晶圓", "封測", "memory"],
    },
    "high_speed_interconnect": {
        "name": "高速傳輸",
        "themes": ["CCL", "PCB", "ABF", "OPTICAL"],
        "keywords": ["ccl", "pcb", "abf", "copper clad", "電路板"],
    },
    "server_supply_chain": {
        "name": "伺服器供應鏈",
        "themes": ["ODM", "SERVER", "RACK", "AI_SERVER"],
        "keywords": ["伺服器", "server", "odm", "ai server", "rack"],
    },
    "power_thermal": {
        "name": "電源散熱",
        "themes": ["POWER", "COOLING", "THERMAL"],
        "keywords": ["電源", "散熱", "cooling", "thermal", "power supply"],
    },
    "network": {
        "name": "網通",
        "themes": ["SWITCH", "ROUTER", "800G"],
        "keywords": ["網通", "交換器", "switch", "router", "網路"],
    },
    "financial": {
        "name": "金融",
        "themes": ["BANK", "INSURANCE", "SECURITIES"],
        "keywords": ["金融", "銀行", "壽險", "保險", "金控"],
    },
    "traditional": {
        "name": "傳產 / 其他",
        "themes": ["STEEL", "PLASTIC", "CEMENT", "FOOD"],
        "keywords": ["傳產", "鋼鐵", "塑膠", "水泥", "食品"],
    },
}

# Symbol → sector mapping for known core symbols
_KNOWN_SYMBOLS: Dict[str, dict] = {
    "2330": {"sector": "semiconductor",           "theme_primary": "FOUNDRY",    "theme_secondary": "AI",         "supply_chain_role": "foundry",       "ai_exposure": "HIGH"},
    "2454": {"sector": "semiconductor",           "theme_primary": "IC_DESIGN",  "theme_secondary": "AI",         "supply_chain_role": "ic_design",      "ai_exposure": "HIGH"},
    "2383": {"sector": "high_speed_interconnect", "theme_primary": "CCL",        "theme_secondary": "AI",         "supply_chain_role": "ccl",            "ai_exposure": "HIGH"},
    "6669": {"sector": "server_supply_chain",     "theme_primary": "AI_SERVER",  "theme_secondary": "ODM",        "supply_chain_role": "odm",            "ai_exposure": "HIGH"},
    "2345": {"sector": "network",                 "theme_primary": "SWITCH",     "theme_secondary": "800G",       "supply_chain_role": "switch",         "ai_exposure": "HIGH"},
    "2308": {"sector": "power_thermal",           "theme_primary": "POWER",      "theme_secondary": "COOLING",    "supply_chain_role": "power_supply",   "ai_exposure": "HIGH"},
    "2317": {"sector": "server_supply_chain",     "theme_primary": "ODM",        "theme_secondary": "AI_SERVER",  "supply_chain_role": "odm",            "ai_exposure": "HIGH"},
    "3017": {"sector": "power_thermal",           "theme_primary": "COOLING",    "theme_secondary": "AI",         "supply_chain_role": "cooling",        "ai_exposure": "HIGH"},
    "3037": {"sector": "high_speed_interconnect", "theme_primary": "ABF",        "theme_secondary": "PCB",        "supply_chain_role": "pcb",            "ai_exposure": "HIGH"},
    "3081": {"sector": "semiconductor",           "theme_primary": "IC_DESIGN",  "theme_secondary": "AI",         "supply_chain_role": "ic_design",      "ai_exposure": "MEDIUM"},
    "3228": {"sector": "semiconductor",           "theme_primary": "IC_DESIGN",  "theme_secondary": "AI",         "supply_chain_role": "ic_design",      "ai_exposure": "MEDIUM"},
    "3661": {"sector": "semiconductor",           "theme_primary": "IC_DESIGN",  "theme_secondary": "AI",         "supply_chain_role": "asic",           "ai_exposure": "HIGH"},
    "5274": {"sector": "semiconductor",           "theme_primary": "IC_DESIGN",  "theme_secondary": "AI",         "supply_chain_role": "bmc_chip",       "ai_exposure": "HIGH"},
    "8358": {"sector": "high_speed_interconnect", "theme_primary": "CCL",        "theme_secondary": "PCB",        "supply_chain_role": "ccl",            "ai_exposure": "MEDIUM"},
    "2327": {"sector": "high_speed_interconnect", "theme_primary": "PASSIVE",    "theme_secondary": "EV",         "supply_chain_role": "mlcc",           "ai_exposure": "LOW"},
    "2382": {"sector": "server_supply_chain",     "theme_primary": "AI_SERVER",  "theme_secondary": "ODM",        "supply_chain_role": "odm",            "ai_exposure": "HIGH"},
    "2376": {"sector": "server_supply_chain",     "theme_primary": "AI_SERVER",  "theme_secondary": "ODM",        "supply_chain_role": "motherboard",    "ai_exposure": "HIGH"},
    "2357": {"sector": "server_supply_chain",     "theme_primary": "AI_PC",      "theme_secondary": "ODM",        "supply_chain_role": "brand",          "ai_exposure": "MEDIUM"},
    "3231": {"sector": "server_supply_chain",     "theme_primary": "AI_SERVER",  "theme_secondary": "ODM",        "supply_chain_role": "odm",            "ai_exposure": "HIGH"},
    "2881": {"sector": "financial",               "theme_primary": "BANK",       "theme_secondary": "INSURANCE",  "supply_chain_role": "financial",      "ai_exposure": "LOW"},
    "2882": {"sector": "financial",               "theme_primary": "INSURANCE",  "theme_secondary": "BANK",       "supply_chain_role": "financial",      "ai_exposure": "LOW"},
    "2886": {"sector": "financial",               "theme_primary": "BANK",       "theme_secondary": "FOREX",      "supply_chain_role": "financial",      "ai_exposure": "LOW"},
    "2891": {"sector": "financial",               "theme_primary": "BANK",       "theme_secondary": "SECURITIES", "supply_chain_role": "financial",      "ai_exposure": "LOW"},
    "2884": {"sector": "financial",               "theme_primary": "BANK",       "theme_secondary": "DIGITAL",    "supply_chain_role": "financial",      "ai_exposure": "LOW"},
    "2885": {"sector": "financial",               "theme_primary": "SECURITIES", "theme_secondary": "BANK",       "supply_chain_role": "financial",      "ai_exposure": "LOW"},
}


class SectorClassifier:
    """
    Classifies Taiwan stocks into sector, industry group, and theme.

    Parameters
    ----------
    taxonomy_path : config/universe/sector_taxonomy.yaml
    """

    read_only = True

    def __init__(self, taxonomy_path: str = "config/universe/sector_taxonomy.yaml"):
        if not os.path.isabs(taxonomy_path):
            taxonomy_path = os.path.join(_BASE_DIR, taxonomy_path)
        self._taxonomy_path = taxonomy_path
        self._taxonomy = self._load_taxonomy()

    def _load_taxonomy(self) -> dict:
        if os.path.isfile(self._taxonomy_path):
            try:
                import yaml
                with open(self._taxonomy_path, encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except Exception as exc:
                logger.debug("_load_taxonomy: %s — using builtin", exc)
        return _BUILTIN_TAXONOMY

    def classify_symbol(self, symbol: str, name: Optional[str] = None, sector_hint: Optional[str] = None) -> dict:
        """Return classification dict for a single symbol."""
        sym = str(symbol)
        # Use known mapping first
        if sym in _KNOWN_SYMBOLS:
            base = dict(_KNOWN_SYMBOLS[sym])
            base.update({
                "symbol":             sym,
                "name":               name or sym,
                "etf_relevance":      "1" if base.get("ai_exposure") == "HIGH" else "0",
                "institutional_focus":"1" if base.get("ai_exposure") in ("HIGH", "MEDIUM") else "0",
                "liquidity_tier":     "LARGE" if sym in ("2330", "2454", "2317", "2382") else "MID",
                "market_cap_tier":    "LARGE" if sym in ("2330", "2454") else "MID",
            })
            return base

        # Fallback: classify by sector_hint or name keywords
        sector = "other"
        theme_primary = "GENERAL"
        theme_secondary = ""
        ai_exposure = "LOW"

        if sector_hint:
            sh = sector_hint.lower()
            for sec, info in self._taxonomy.items():
                kws = info.get("keywords", [])
                if any(k in sh for k in kws) or sec in sh:
                    sector = sec
                    themes = info.get("themes", [])
                    theme_primary = themes[0] if themes else "GENERAL"
                    theme_secondary = themes[1] if len(themes) > 1 else ""
                    if "AI" in str(themes):
                        ai_exposure = "MEDIUM"
                    break

        return {
            "symbol":             sym,
            "name":               name or sym,
            "sector":             sector,
            "theme_primary":      theme_primary,
            "theme_secondary":    theme_secondary,
            "supply_chain_role":  sector,
            "ai_exposure":        ai_exposure,
            "etf_relevance":      "0",
            "institutional_focus":"0",
            "liquidity_tier":     "UNKNOWN",
            "market_cap_tier":    "UNKNOWN",
        }

    def classify_universe(self, rows: List[dict]) -> List[dict]:
        """Add classification fields to each row in a universe list."""
        enriched = []
        for row in rows:
            sym = str(row.get("symbol", ""))
            name = row.get("name", "")
            sector_hint = row.get("sector", "") or row.get("industry", "")
            classification = self.classify_symbol(sym, name, sector_hint)
            merged = dict(row)
            # Only fill missing fields
            for k, v in classification.items():
                if not merged.get(k):
                    merged[k] = v
            enriched.append(merged)
        return enriched

    def get_sector_summary(self, rows: List[dict]) -> dict:
        """Return sector distribution summary."""
        from collections import Counter
        sectors = [r.get("sector", "other") for r in rows]
        counts = dict(Counter(sectors))
        total = len(rows)
        return {
            "total":       total,
            "by_sector":   counts,
            "top_sector":  max(counts, key=counts.get) if counts else "",
            "concentration": max(counts.values()) / total if total else 0.0,
        }

    def get_theme_summary(self, rows: List[dict]) -> dict:
        """Return theme distribution summary."""
        from collections import Counter
        themes = [r.get("theme_primary", "GENERAL") for r in rows]
        ai_exp = [r.get("ai_exposure", "LOW") for r in rows]
        return {
            "by_theme":    dict(Counter(themes)),
            "ai_high":     ai_exp.count("HIGH"),
            "ai_medium":   ai_exp.count("MEDIUM"),
            "ai_low":      ai_exp.count("LOW"),
            "ai_exposure_ratio": (ai_exp.count("HIGH") + ai_exp.count("MEDIUM")) / len(rows) if rows else 0.0,
        }

    def validate_taxonomy(self) -> dict:
        """Validate the loaded taxonomy."""
        issues = []
        if not self._taxonomy:
            issues.append("Empty taxonomy")
        for sec, info in self._taxonomy.items():
            if not info.get("name"):
                issues.append(f"Sector '{sec}' missing name")
            if not info.get("themes"):
                issues.append(f"Sector '{sec}' has no themes")
        return {"ok": not issues, "issues": issues, "sector_count": len(self._taxonomy)}
