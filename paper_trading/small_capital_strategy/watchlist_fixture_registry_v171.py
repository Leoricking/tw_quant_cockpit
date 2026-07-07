"""
paper_trading/small_capital_strategy/watchlist_fixture_registry_v171.py
Fixture registry for Watchlist Strategy Layer v1.7.1.
70+ fixtures. All marked with required safety markers.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

_SCHEMA  = "171"
_POLICY  = "1.7.1-watchlist-strategy-layer"
_LINEAGE = "v1.7.1"
_DS      = 42  # deterministic seed

_BASE_MARKERS: Dict[str, Any] = {
    "test_fixture":           True,
    "demo_only":              True,
    "paper_only":             True,
    "research_only":          True,
    "not_live":               True,
    "no_broker":              True,
    "no_real_account":        True,
    "no_real_orders":         True,
    "not_for_production":     True,
    "not_investment_advice":  True,
    "watchlist_strategy_only": True,
    "schema_version":         _SCHEMA,
    "policy_version":         _POLICY,
    "source_lineage":         _LINEAGE,
    "deterministic_seed":     _DS,
}


def _f(
    fixture_id: str,
    scenario_id: str,
    purpose: str,
    usage_type: str,
    referenced_by: str,
    expected_status: str,
    expected_score_range: str,
    expected_tier: str,
    expected_exclusion_reasons: List[str],
) -> Dict[str, Any]:
    """Helper to build a fixture dict with all required fields."""
    d = dict(_BASE_MARKERS)
    d.update({
        "fixture_id": fixture_id,
        "scenario_id": scenario_id,
        "purpose": purpose,
        "usage_type": usage_type,
        "referenced_by": referenced_by,
        "expected_status": expected_status,
        "expected_score_range": expected_score_range,
        "expected_tier": expected_tier,
        "expected_exclusion_reasons": expected_exclusion_reasons,
    })
    return d


# ── 70 fixtures ───────────────────────────────────────────────────────────────

WATCHLIST_FIXTURE_REGISTRY: List[Dict[str, Any]] = [
    # ── Profile (6) ──────────────────────────────────────────────────────────
    _f("wl_001", "wl_sc_001", "default 30 watchlist profile",          "profile",  "test_watchlist_profile_v171", "PASS", "[0,100]", "CORE",        []),
    _f("wl_002", "wl_sc_002", "max 50 watchlist profile",              "profile",  "test_watchlist_profile_v171", "PASS", "[0,100]", "CORE",        []),
    _f("wl_003", "wl_sc_003", "below 10 watchlist insufficient",       "profile",  "test_watchlist_profile_v171", "FAIL", "[0,100]", "EXCLUDED",    []),
    _f("wl_004", "wl_sc_004", "over 50 watchlist overdiversified",     "profile",  "test_watchlist_profile_v171", "FAIL", "[0,100]", "EXCLUDED",    []),
    _f("wl_005", "wl_sc_005", "focus top 10 candidates",               "profile",  "test_watchlist_profile_v171", "PASS", "[0,100]", "MAIN_THEME",  []),
    _f("wl_006", "wl_sc_006", "tradable top 5 candidates",             "profile",  "test_watchlist_profile_v171", "PASS", "[0,100]", "CORE",        []),

    # ── Scoring (10) ─────────────────────────────────────────────────────────
    _f("wl_007", "wl_sc_007", "strong theme high score",               "scoring",  "test_watchlist_score_v171",   "PASS", "[85,100]","MAIN_THEME",  []),
    _f("wl_008", "wl_sc_008", "weak theme excluded",                   "scoring",  "test_watchlist_score_v171",   "FAIL", "[0,0]",   "EXCLUDED",    ["WEAK_THEME"]),
    _f("wl_009", "wl_sc_009", "below 20MA score capped",               "scoring",  "test_watchlist_score_v171",   "PASS", "[40,69]", "SECOND_WAVE", ["BELOW_20MA"]),
    _f("wl_010", "wl_sc_010", "below 60MA score capped",               "scoring",  "test_watchlist_score_v171",   "PASS", "[40,54]", "SECOND_WAVE", ["BELOW_60MA"]),
    _f("wl_011", "wl_sc_011", "financing overheated excluded",         "scoring",  "test_watchlist_score_v171",   "FAIL", "[0,0]",   "EXCLUDED",    ["FINANCING_OVERHEATED"]),
    _f("wl_012", "wl_sc_012", "liquidity poor excluded",               "scoring",  "test_watchlist_score_v171",   "FAIL", "[0,0]",   "EXCLUDED",    ["LOW_LIQUIDITY"]),
    _f("wl_013", "wl_sc_013", "institutional heavy selling excluded",  "scoring",  "test_watchlist_score_v171",   "FAIL", "[0,0]",   "EXCLUDED",    ["INSTITUTIONAL_HEAVY_SELLING"]),
    _f("wl_014", "wl_sc_014", "revenue weak downgraded",               "scoring",  "test_watchlist_score_v171",   "PASS", "[40,69]", "TRAINING",    ["REVENUE_GROWTH_WEAK"]),
    _f("wl_015", "wl_sc_015", "technical weak downgraded",             "scoring",  "test_watchlist_score_v171",   "PASS", "[40,54]", "TRAINING",    ["TECHNICAL_STRUCTURE_WEAK"]),
    _f("wl_016", "wl_sc_016", "high volatility downgraded",            "scoring",  "test_watchlist_score_v171",   "PASS", "[40,54]", "TRAINING",    ["TOO_VOLATILE_FOR_SMALL_CAPITAL"]),

    # ── Tier (7) ──────────────────────────────────────────────────────────────
    _f("wl_017", "wl_sc_017", "CORE tier valid",                       "tier",     "test_watchlist_tier_classifier_v171", "PASS", "[70,100]","CORE",       []),
    _f("wl_018", "wl_sc_018", "MAIN_THEME tier valid",                 "tier",     "test_watchlist_tier_classifier_v171", "PASS", "[65,100]","MAIN_THEME", []),
    _f("wl_019", "wl_sc_019", "SECOND_WAVE tier valid",                "tier",     "test_watchlist_tier_classifier_v171", "PASS", "[50,64]", "SECOND_WAVE",[]),
    _f("wl_020", "wl_sc_020", "TRAINING tier valid",                   "tier",     "test_watchlist_tier_classifier_v171", "PASS", "[40,49]", "TRAINING",   []),
    _f("wl_021", "wl_sc_021", "EXCLUDED weak theme",                   "tier",     "test_watchlist_tier_classifier_v171", "FAIL", "[0,0]",   "EXCLUDED",   ["WEAK_THEME"]),
    _f("wl_022", "wl_sc_022", "EXCLUDED low liquidity",                "tier",     "test_watchlist_tier_classifier_v171", "FAIL", "[0,0]",   "EXCLUDED",   ["LOW_LIQUIDITY"]),
    _f("wl_023", "wl_sc_023", "EXCLUDED financing overheated",         "tier",     "test_watchlist_tier_classifier_v171", "FAIL", "[0,0]",   "EXCLUDED",   ["FINANCING_OVERHEATED"]),

    # ── Regime (5) ────────────────────────────────────────────────────────────
    _f("wl_024", "wl_sc_024", "bull normal ranking",                   "regime",   "test_watchlist_ranking_v171",         "PASS", "[0,100]", "CORE",        []),
    _f("wl_025", "wl_sc_025", "range conservative ranking",            "regime",   "test_watchlist_ranking_v171",         "PASS", "[0,100]", "MAIN_THEME",  []),
    _f("wl_026", "wl_sc_026", "bear only core",                        "regime",   "test_top_candidate_selector_v171",    "PASS", "[70,100]","CORE",        []),
    _f("wl_027", "wl_sc_027", "risk off cash preference",              "regime",   "test_top_candidate_selector_v171",    "PASS", "[85,100]","CORE",        []),
    _f("wl_028", "wl_sc_028", "unknown conservative",                  "regime",   "test_top_candidate_selector_v171",    "PASS", "[70,100]","CORE",        []),

    # ── v1.7.0 Mapping (7) ────────────────────────────────────────────────────
    _f("wl_029", "wl_sc_029", "CORE maps to CORE bucket",              "mapping",  "test_watchlist_bridge_v171",          "PASS", "[70,100]","CORE",        []),
    _f("wl_030", "wl_sc_030", "MAIN_THEME maps to MAIN_THEME_SWING",   "mapping",  "test_watchlist_bridge_v171",          "PASS", "[65,100]","MAIN_THEME",  []),
    _f("wl_031", "wl_sc_031", "SECOND_WAVE maps to SECOND_WAVE_SETUP", "mapping",  "test_watchlist_bridge_v171",          "PASS", "[50,64]", "SECOND_WAVE", []),
    _f("wl_032", "wl_sc_032", "TRAINING maps to SHORT_TERM_TRAINING",  "mapping",  "test_watchlist_bridge_v171",          "PASS", "[40,49]", "TRAINING",    []),
    _f("wl_033", "wl_sc_033", "EXCLUDED maps to none",                 "mapping",  "test_watchlist_bridge_v171",          "FAIL", "[0,0]",   "EXCLUDED",    []),
    _f("wl_034", "wl_sc_034", "training cap 15000 TWD",                "mapping",  "test_watchlist_bridge_v171",          "PASS", "[40,49]", "TRAINING",    []),
    _f("wl_035", "wl_sc_035", "max holdings 4",                        "mapping",  "test_watchlist_bridge_v171",          "PASS", "[0,100]", "CORE",        []),

    # ── Reports (4) ───────────────────────────────────────────────────────────
    _f("wl_036", "wl_sc_036", "markdown report",                       "report",   "test_watchlist_report_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_037", "wl_sc_037", "json report",                           "report",   "test_watchlist_report_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_038", "wl_sc_038", "csv report",                            "report",   "test_watchlist_report_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_039", "wl_sc_039", "not investment advice marker",          "report",   "test_watchlist_report_v171",          "PASS", "[0,100]", "CORE",        []),

    # ── Safety (10) ───────────────────────────────────────────────────────────
    _f("wl_040", "wl_sc_040", "safety flags all correct",              "safety",   "test_watchlist_safety_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_041", "wl_sc_041", "watchlist real trading disabled",       "safety",   "test_watchlist_safety_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_042", "wl_sc_042", "watchlist broker disabled",             "safety",   "test_watchlist_safety_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_043", "wl_sc_043", "watchlist margin disabled",             "safety",   "test_watchlist_safety_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_044", "wl_sc_044", "watchlist auto order disabled",         "safety",   "test_watchlist_safety_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_045", "wl_sc_045", "watchlist no real account",             "safety",   "test_watchlist_safety_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_046", "wl_sc_046", "watchlist no production trading",       "safety",   "test_watchlist_safety_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_047", "wl_sc_047", "audit returns all safe",                "safety",   "test_watchlist_safety_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_048", "wl_sc_048", "assert safe passes",                    "safety",   "test_watchlist_safety_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_049", "wl_sc_049", "safety capabilities = 0",               "safety",   "test_watchlist_safety_v171",          "PASS", "[0,100]", "CORE",        []),

    # ── Enums (5) ─────────────────────────────────────────────────────────────
    _f("wl_050", "wl_sc_050", "WatchlistTier enum values",             "enum",     "test_watchlist_enums_v171",           "PASS", "[0,100]", "CORE",        []),
    _f("wl_051", "wl_sc_051", "ThemeStrength LEADING value",           "enum",     "test_watchlist_enums_v171",           "PASS", "[0,100]", "CORE",        []),
    _f("wl_052", "wl_sc_052", "WatchlistExclusionReason all values",   "enum",     "test_watchlist_enums_v171",           "PASS", "[0,100]", "CORE",        []),
    _f("wl_053", "wl_sc_053", "RankingGrade no A+ grade",              "enum",     "test_watchlist_enums_v171",           "PASS", "[0,100]", "CORE",        []),
    _f("wl_054", "wl_sc_054", "OverdiversificationStatus all values",  "enum",     "test_watchlist_enums_v171",           "PASS", "[0,100]", "CORE",        []),

    # ── Models (5) ────────────────────────────────────────────────────────────
    _f("wl_055", "wl_sc_055", "WatchlistCandidate paper_only=True",    "model",    "test_watchlist_models_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_056", "wl_sc_056", "WatchlistScoreResult to_dict",          "model",    "test_watchlist_models_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_057", "wl_sc_057", "TopCandidateSelection to_dict",         "model",    "test_watchlist_models_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_058", "wl_sc_058", "OverdiversificationResult to_dict",     "model",    "test_watchlist_models_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_059", "wl_sc_059", "WatchlistStrategyReport to_dict",       "model",    "test_watchlist_models_v171",          "PASS", "[0,100]", "CORE",        []),

    # ── Ranking (4) ───────────────────────────────────────────────────────────
    _f("wl_060", "wl_sc_060", "rank by total score",                   "ranking",  "test_watchlist_ranking_v171",         "PASS", "[0,100]", "CORE",        []),
    _f("wl_061", "wl_sc_061", "CORE tier ranks above MAIN_THEME",      "ranking",  "test_watchlist_ranking_v171",         "PASS", "[0,100]", "CORE",        []),
    _f("wl_062", "wl_sc_062", "EXCLUDED ranks last",                   "ranking",  "test_watchlist_ranking_v171",         "FAIL", "[0,0]",   "EXCLUDED",    []),
    _f("wl_063", "wl_sc_063", "rank candidates returns ordered list",  "ranking",  "test_watchlist_ranking_v171",         "PASS", "[0,100]", "CORE",        []),

    # ── Overdiversification (4) ───────────────────────────────────────────────
    _f("wl_064", "wl_sc_064", "optimal range 10-30 candidates",        "overdiversification", "test_overdiversification_detector_v171", "PASS", "[0,100]","CORE", []),
    _f("wl_065", "wl_sc_065", "insufficient coverage below 10",        "overdiversification", "test_overdiversification_detector_v171", "FAIL", "[0,100]","CORE", []),
    _f("wl_066", "wl_sc_066", "overdiversified above 50",              "overdiversification", "test_overdiversification_detector_v171", "FAIL", "[0,100]","CORE", []),
    _f("wl_067", "wl_sc_067", "acceptable range 30-50 candidates",     "overdiversification", "test_overdiversification_detector_v171", "PASS", "[0,100]","CORE", []),

    # ── Version / Health / Gate (6) ───────────────────────────────────────────
    _f("wl_068", "wl_sc_068", "version 1.7.1 correct",                 "version",  "test_watchlist_version_v171",         "PASS", "[0,100]", "CORE",        []),
    _f("wl_069", "wl_sc_069", "release name Watchlist Strategy Layer", "version",  "test_watchlist_version_v171",         "PASS", "[0,100]", "CORE",        []),
    _f("wl_070", "wl_sc_070", "base release 1.7.0 correct",            "version",  "test_watchlist_version_v171",         "PASS", "[0,100]", "CORE",        []),
    _f("wl_071", "wl_sc_071", "health all passed",                     "health",   "test_watchlist_health_v171",          "PASS", "[0,100]", "CORE",        []),
    _f("wl_072", "wl_sc_072", "gate gate_passed=True",                 "gate",     "test_watchlist_gate_v171",            "PASS", "[0,100]", "CORE",        []),
    _f("wl_073", "wl_sc_073", "watchlist bridge v170 summary",         "bridge",   "test_watchlist_bridge_v171",          "PASS", "[0,100]", "CORE",        []),
]

# Validate no duplicate IDs
_fixture_ids = [f["fixture_id"] for f in WATCHLIST_FIXTURE_REGISTRY]
assert len(_fixture_ids) == len(set(_fixture_ids)), "Duplicate fixture IDs found"


def get_fixture_registry() -> List[Dict[str, Any]]:
    """Return a copy of the watchlist fixture registry."""
    return list(WATCHLIST_FIXTURE_REGISTRY)


def get_fixture_by_id(fixture_id: str):
    """Return a fixture by its fixture_id, or None if not found."""
    for f in WATCHLIST_FIXTURE_REGISTRY:
        if f["fixture_id"] == fixture_id:
            return dict(f)
    return None


def get_fixture_count() -> int:
    """Return total fixture count."""
    return len(WATCHLIST_FIXTURE_REGISTRY)


def get_fixture_ids() -> List[str]:
    """Return all fixture IDs."""
    return [f["fixture_id"] for f in WATCHLIST_FIXTURE_REGISTRY]


def validate_all_fixtures() -> Dict[str, Any]:
    """Validate all fixtures against the schema. Returns {valid, total, issues}."""
    from paper_trading.small_capital_strategy.watchlist_fixture_schema_v171 import (
        validate_watchlist_fixture,
    )
    all_issues = []
    for f in WATCHLIST_FIXTURE_REGISTRY:
        result = validate_watchlist_fixture(f)
        if not result["valid"]:
            all_issues.append({"fixture_id": result["fixture_id"], "issues": result["issues"]})
    return {
        "valid": len(all_issues) == 0,
        "total": len(WATCHLIST_FIXTURE_REGISTRY),
        "invalid_count": len(all_issues),
        "issues": all_issues,
    }
