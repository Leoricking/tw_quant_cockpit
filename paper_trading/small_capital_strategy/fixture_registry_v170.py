"""
paper_trading/small_capital_strategy/fixture_registry_v170.py
Fixture registry for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
Maps fixture IDs to their metadata. Actual fixture data lives in tests/fixtures/small_capital_strategy/.
"""
from __future__ import annotations
from typing import Any, Dict, List

FIXTURE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "sc_001": {"category": "capital_profile", "description": "300k capital profile default"},
    "sc_002": {"category": "capital_profile", "description": "300k capital profile min loss"},
    "sc_003": {"category": "capital_profile", "description": "300k capital profile max loss"},
    "sc_004": {"category": "capital_profile", "description": "capital profile validation pass"},
    "sc_005": {"category": "capital_profile", "description": "capital profile validation fail negative capital"},
    "sc_006": {"category": "capital_profile", "description": "capital profile validation fail zero capital"},
    "sc_007": {"category": "capital_profile", "description": "capital profile risk pct min boundary"},
    "sc_008": {"category": "capital_profile", "description": "capital profile risk pct max boundary"},
    "sc_009": {"category": "capital_profile", "description": "capital profile max holdings min"},
    "sc_010": {"category": "capital_profile", "description": "capital profile max holdings max"},
    "sc_011": {"category": "allocation", "description": "bull regime allocation"},
    "sc_012": {"category": "allocation", "description": "range regime allocation"},
    "sc_013": {"category": "allocation", "description": "bear regime allocation"},
    "sc_014": {"category": "allocation", "description": "risk_off regime allocation"},
    "sc_015": {"category": "allocation", "description": "unknown regime allocation"},
    "sc_016": {"category": "allocation", "description": "allocation total equals 100 pct"},
    "sc_017": {"category": "allocation", "description": "allocation cash minimum bear"},
    "sc_018": {"category": "allocation", "description": "allocation short term training max"},
    "sc_019": {"category": "position_sizing", "description": "standard position sizing 6pct stop"},
    "sc_020": {"category": "position_sizing", "description": "position sizing 3pct stop"},
    "sc_021": {"category": "position_sizing", "description": "position sizing 10pct stop"},
    "sc_022": {"category": "position_sizing", "description": "position sizing blocked zero stop"},
    "sc_023": {"category": "position_sizing", "description": "position sizing degraded over 20pct stop"},
    "sc_024": {"category": "position_sizing", "description": "position sizing short term training cap 15k"},
    "sc_025": {"category": "position_sizing", "description": "position sizing max single position 35pct"},
    "sc_026": {"category": "position_sizing", "description": "position sizing bucket budget constraint"},
    "sc_027": {"category": "buy_points", "description": "A buy point 10MA pullback valid"},
    "sc_028": {"category": "buy_points", "description": "A buy point theme not strong blocked"},
    "sc_029": {"category": "buy_points", "description": "B buy point platform breakout valid"},
    "sc_030": {"category": "buy_points", "description": "B buy point volume ratio insufficient"},
    "sc_031": {"category": "buy_points", "description": "C buy point 20MA reclaim valid"},
    "sc_032": {"category": "buy_points", "description": "C buy point no first wave blocked"},
    "sc_033": {"category": "buy_points", "description": "buy point evaluate all ABC"},
    "sc_034": {"category": "buy_points", "description": "buy point get best buy point"},
    "sc_035": {"category": "forbidden", "description": "forbidden check margin not allowed"},
    "sc_036": {"category": "forbidden", "description": "forbidden check day trading not primary"},
    "sc_037": {"category": "forbidden", "description": "forbidden check short selling blocked"},
    "sc_038": {"category": "forbidden", "description": "forbidden check leverage blocked"},
    "sc_039": {"category": "forbidden", "description": "forbidden check overdiversification"},
    "sc_040": {"category": "forbidden", "description": "forbidden check all clear pass"},
    "sc_041": {"category": "forbidden", "description": "forbidden check financing overheated"},
    "sc_042": {"category": "forbidden", "description": "forbidden check unsupported buy point"},
    "sc_043": {"category": "watchlist", "description": "watchlist rank candidates composite score"},
    "sc_044": {"category": "watchlist", "description": "watchlist filter small capital liquidity"},
    "sc_045": {"category": "watchlist", "description": "watchlist exclude untradable"},
    "sc_046": {"category": "watchlist", "description": "watchlist detect overdiversification"},
    "sc_047": {"category": "watchlist", "description": "watchlist recommend top 5 candidates"},
    "sc_048": {"category": "watchlist", "description": "watchlist theme filter strong"},
    "sc_049": {"category": "watchlist", "description": "watchlist theme filter weak blocked"},
    "sc_050": {"category": "watchlist", "description": "watchlist max 50 cap"},
    "sc_051": {"category": "market_regime", "description": "market regime bull control"},
    "sc_052": {"category": "market_regime", "description": "market regime bear control"},
    "sc_053": {"category": "market_regime", "description": "market regime range control"},
    "sc_054": {"category": "market_regime", "description": "market regime risk_off control"},
    "sc_055": {"category": "market_regime", "description": "market regime unknown control"},
    "sc_056": {"category": "reports", "description": "report to markdown"},
    "sc_057": {"category": "reports", "description": "report to json"},
    "sc_058": {"category": "reports", "description": "report to csv"},
    "sc_059": {"category": "reports", "description": "report console summary"},
    "sc_060": {"category": "safety", "description": "safety flags all correct"},
    "sc_061": {"category": "safety", "description": "safety audit all safe"},
    "sc_062": {"category": "safety", "description": "safety assert safe pass"},
    "sc_063": {"category": "safety", "description": "safety live fallback disabled"},
    "sc_064": {"category": "safety", "description": "safety broker disabled"},
    "sc_065": {"category": "safety", "description": "safety production blocked"},
    "sc_066": {"category": "safety", "description": "safety no real orders"},
    "sc_067": {"category": "safety", "description": "safety paper only true"},
    "sc_068": {"category": "scorecard", "description": "scorecard grade A score 90"},
    "sc_069": {"category": "scorecard", "description": "scorecard grade B score 75"},
    "sc_070": {"category": "scorecard", "description": "scorecard grade F score 30"},
    "sc_071": {"category": "scorecard", "description": "scorecard safety blocked grade BLOCKED"},
    "sc_072": {"category": "scorecard", "description": "scorecard weights sum 100"},
    "sc_073": {"category": "version_identity", "description": "version 1.7.0 identity"},
    "sc_074": {"category": "version_identity", "description": "known release names includes v1.7.0"},
    "sc_075": {"category": "version_identity", "description": "minimum version check 1.6.9.1"},
    "sc_076": {"category": "version_identity", "description": "schema version 170"},
    "sc_077": {"category": "version_identity", "description": "policy version string"},
    "sc_078": {"category": "exit_plan", "description": "exit plan short term 10-15pct"},
    "sc_079": {"category": "exit_plan", "description": "exit plan swing 25-40pct"},
    "sc_080": {"category": "exit_plan", "description": "exit plan stop loss ma based"},
}


def count_fixtures() -> int:
    """Return total number of registered fixtures."""
    return len(FIXTURE_REGISTRY)


def get_fixtures_by_category(category: str) -> List[str]:
    """Return fixture IDs for a given category."""
    return [fid for fid, meta in FIXTURE_REGISTRY.items() if meta["category"] == category]


def get_all_categories() -> List[str]:
    """Return sorted list of unique categories."""
    return sorted(set(meta["category"] for meta in FIXTURE_REGISTRY.values()))


def list_fixtures() -> List[Dict[str, Any]]:
    """Return list of all fixture metadata dicts."""
    return [
        {"fixture_id": fid, **meta}
        for fid, meta in FIXTURE_REGISTRY.items()
    ]
