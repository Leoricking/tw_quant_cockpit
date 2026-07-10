"""
paper_trading/small_capital_strategy/stable_rollup_version_v179.py
Version metadata for Small Capital Strategy Stable Rollup v1.7.9.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Dict, Any

VERSION      = "1.7.9"
RELEASE_NAME = "Small Capital Strategy Stable Rollup"
BASE_RELEASE = "1.7.8 Small Capital Strategy Integration"
SCHEMA_VERSION  = "179"
POLICY_VERSION  = "1.7.9-small-capital-strategy-stable-rollup"

INCLUDED_RELEASES = [
    "v1.7.0", "v1.7.1", "v1.7.2", "v1.7.3",
    "v1.7.4", "v1.7.5", "v1.7.6", "v1.7.7", "v1.7.8",
]

MIN_SCENARIOS   = 50
MIN_FIXTURES    = 50
MIN_CLI         = 12
MIN_HEALTH      = 50
MIN_GATE        = 50

KNOWN_RELEASE_NAMES: frozenset = frozenset({
    "Live Paper Trading Stable Rollup",
    "Small Capital Growth Strategy",
    "Watchlist Strategy Layer",
    "A/B/C Buy Point Execution Plan",
    "Market Regime Position Control",
    "Small Account Risk Dashboard",
    "Small Account Trade Journal",
    "Mistake Taxonomy & Weekly Review Dashboard",
    "Theme Rotation Scanner",
    "Small Capital Strategy Integration",
    "Small Capital Strategy Stable Rollup",
})


def get_version_info() -> Dict[str, Any]:
    return {
        "version": VERSION,
        "release_name": RELEASE_NAME,
        "base_release": BASE_RELEASE,
        "schema_version": SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "included_releases": INCLUDED_RELEASES,
        "min_scenarios": MIN_SCENARIOS,
        "min_fixtures": MIN_FIXTURES,
        "min_cli": MIN_CLI,
        "min_health": MIN_HEALTH,
        "min_gate": MIN_GATE,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
    }


def verify_version() -> bool:
    parts = VERSION.split(".")
    return len(parts) == 3 and all(p.isdigit() for p in parts)


def is_known_release(name: str) -> bool:
    return name in KNOWN_RELEASE_NAMES


def check_minimum_version(version_str: str) -> bool:
    def _parse(v: str):
        return tuple(int(x) for x in v.split("."))
    try:
        return _parse(version_str) >= _parse(VERSION)
    except (ValueError, AttributeError):
        return False
