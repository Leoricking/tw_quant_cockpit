"""
paper_trading/small_capital_strategy/watchlist_scenario_registry_v171.py
Scenario registry for Watchlist Strategy Layer v1.7.1.
70+ scenarios. No skip. No xfail.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Dict

_DS = 42  # deterministic seed

WATCHLIST_SCENARIO_REGISTRY: List[Dict] = [
    # ── Profile (6) ──────────────────────────────────────────────────────────
    {"scenario_id": "wl_sc_001", "category": "profile", "name": "default_30_watchlist",
     "description": "default watchlist size is 30", "expected_status": "PASS",
     "fixture_id": "wl_001", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_002", "category": "profile", "name": "max_50_watchlist",
     "description": "max watchlist size is 50", "expected_status": "PASS",
     "fixture_id": "wl_002", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_003", "category": "profile", "name": "below_10_insufficient",
     "description": "watchlist below 10 triggers INSUFFICIENT_COVERAGE", "expected_status": "FAIL",
     "fixture_id": "wl_003", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_004", "category": "profile", "name": "over_50_overdiversified",
     "description": "watchlist over 50 triggers OVERDIVERSIFIED", "expected_status": "FAIL",
     "fixture_id": "wl_004", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_005", "category": "profile", "name": "focus_top_10",
     "description": "focus candidates limited to 10", "expected_status": "PASS",
     "fixture_id": "wl_005", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_006", "category": "profile", "name": "tradable_top_5",
     "description": "tradable candidates limited to 5", "expected_status": "PASS",
     "fixture_id": "wl_006", "deterministic_seed": _DS},

    # ── Scoring (10) ─────────────────────────────────────────────────────────
    {"scenario_id": "wl_sc_007", "category": "scoring", "name": "strong_theme_high_score",
     "description": "STRONG/LEADING theme => score >= 85", "expected_status": "PASS",
     "fixture_id": "wl_007", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_008", "category": "scoring", "name": "weak_theme_excluded",
     "description": "WEAK theme => blocked, score=0, EXCLUDED", "expected_status": "FAIL",
     "fixture_id": "wl_008", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_009", "category": "scoring", "name": "below_20ma_capped",
     "description": "below 20MA => technical score max C grade", "expected_status": "PASS",
     "fixture_id": "wl_009", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_010", "category": "scoring", "name": "below_60ma_capped",
     "description": "below 60MA => technical score max D grade", "expected_status": "PASS",
     "fixture_id": "wl_010", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_011", "category": "scoring", "name": "financing_overheated_excluded",
     "description": "financing ratio > 40% => blocked, EXCLUDED", "expected_status": "FAIL",
     "fixture_id": "wl_011", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_012", "category": "scoring", "name": "liquidity_poor_excluded",
     "description": "avg vol < 1M TWD => blocked, EXCLUDED", "expected_status": "FAIL",
     "fixture_id": "wl_012", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_013", "category": "scoring", "name": "institutional_heavy_selling_excluded",
     "description": "inst_net_buy_days < 0 => blocked, EXCLUDED", "expected_status": "FAIL",
     "fixture_id": "wl_013", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_014", "category": "scoring", "name": "revenue_weak_downgraded",
     "description": "negative revenue growth => score downgraded", "expected_status": "PASS",
     "fixture_id": "wl_014", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_015", "category": "scoring", "name": "technical_weak_downgraded",
     "description": "poor technicals => score downgraded", "expected_status": "PASS",
     "fixture_id": "wl_015", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_016", "category": "scoring", "name": "high_volatility_downgraded",
     "description": "ATR > 12% => small_capital_fit score low", "expected_status": "PASS",
     "fixture_id": "wl_016", "deterministic_seed": _DS},

    # ── Tier (7) ──────────────────────────────────────────────────────────────
    {"scenario_id": "wl_sc_017", "category": "tier", "name": "core_valid",
     "description": "core-eligible with high liquidity and score => CORE", "expected_status": "PASS",
     "fixture_id": "wl_017", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_018", "category": "tier", "name": "main_theme_valid",
     "description": "STRONG theme, score >= 65 => MAIN_THEME", "expected_status": "PASS",
     "fixture_id": "wl_018", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_019", "category": "tier", "name": "second_wave_valid",
     "description": "score >= 50 => SECOND_WAVE", "expected_status": "PASS",
     "fixture_id": "wl_019", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_020", "category": "tier", "name": "training_valid",
     "description": "score >= 40 => TRAINING", "expected_status": "PASS",
     "fixture_id": "wl_020", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_021", "category": "tier", "name": "excluded_weak_theme",
     "description": "WEAK theme => EXCLUDED", "expected_status": "FAIL",
     "fixture_id": "wl_021", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_022", "category": "tier", "name": "excluded_low_liquidity",
     "description": "LOW_LIQUIDITY => EXCLUDED", "expected_status": "FAIL",
     "fixture_id": "wl_022", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_023", "category": "tier", "name": "excluded_financing_overheated",
     "description": "FINANCING_OVERHEATED => EXCLUDED", "expected_status": "FAIL",
     "fixture_id": "wl_023", "deterministic_seed": _DS},

    # ── Regime (5) ────────────────────────────────────────────────────────────
    {"scenario_id": "wl_sc_024", "category": "regime", "name": "bull_normal_ranking",
     "description": "BULL regime: all tiers eligible for tradable", "expected_status": "PASS",
     "fixture_id": "wl_024", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_025", "category": "regime", "name": "range_conservative_ranking",
     "description": "RANGE regime: standard ranking", "expected_status": "PASS",
     "fixture_id": "wl_025", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_026", "category": "regime", "name": "bear_only_core",
     "description": "BEAR regime: tradable only CORE or very strong MAIN_THEME", "expected_status": "PASS",
     "fixture_id": "wl_026", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_027", "category": "regime", "name": "risk_off_cash_preference",
     "description": "RISK_OFF: tradable only CORE or score >= 85 MAIN_THEME", "expected_status": "PASS",
     "fixture_id": "wl_027", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_028", "category": "regime", "name": "unknown_conservative",
     "description": "UNKNOWN: only CORE and MAIN_THEME with score >= 70", "expected_status": "PASS",
     "fixture_id": "wl_028", "deterministic_seed": _DS},

    # ── v1.7.0 Mapping (7) ────────────────────────────────────────────────────
    {"scenario_id": "wl_sc_029", "category": "v170_mapping", "name": "core_maps_to_core_bucket",
     "description": "CORE tier => CORE AllocationBucket", "expected_status": "PASS",
     "fixture_id": "wl_029", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_030", "category": "v170_mapping", "name": "main_theme_maps_to_swing",
     "description": "MAIN_THEME tier => MAIN_THEME_SWING bucket", "expected_status": "PASS",
     "fixture_id": "wl_030", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_031", "category": "v170_mapping", "name": "second_wave_maps_to_setup",
     "description": "SECOND_WAVE tier => SECOND_WAVE_SETUP bucket", "expected_status": "PASS",
     "fixture_id": "wl_031", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_032", "category": "v170_mapping", "name": "training_maps_to_st_training",
     "description": "TRAINING tier => SHORT_TERM_TRAINING bucket", "expected_status": "PASS",
     "fixture_id": "wl_032", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_033", "category": "v170_mapping", "name": "excluded_maps_to_none",
     "description": "EXCLUDED tier => None (no bucket)", "expected_status": "FAIL",
     "fixture_id": "wl_033", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_034", "category": "v170_mapping", "name": "training_cap_15000",
     "description": "training position max 15000 TWD enforced", "expected_status": "PASS",
     "fixture_id": "wl_034", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_035", "category": "v170_mapping", "name": "max_holdings_4",
     "description": "max holdings = 4 from v1.7.0 capital profile", "expected_status": "PASS",
     "fixture_id": "wl_035", "deterministic_seed": _DS},

    # ── Reports (4) ───────────────────────────────────────────────────────────
    {"scenario_id": "wl_sc_036", "category": "reports", "name": "markdown_report",
     "description": "generate Markdown report", "expected_status": "PASS",
     "fixture_id": "wl_036", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_037", "category": "reports", "name": "json_report",
     "description": "generate JSON report", "expected_status": "PASS",
     "fixture_id": "wl_037", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_038", "category": "reports", "name": "csv_report",
     "description": "generate CSV report", "expected_status": "PASS",
     "fixture_id": "wl_038", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_039", "category": "reports", "name": "not_investment_advice_marker",
     "description": "all reports carry not_investment_advice marker", "expected_status": "PASS",
     "fixture_id": "wl_039", "deterministic_seed": _DS},

    # ── Safety (10) ───────────────────────────────────────────────────────────
    {"scenario_id": "wl_sc_040", "category": "safety", "name": "safety_flags_correct",
     "description": "all watchlist safety flags are correct", "expected_status": "PASS",
     "fixture_id": "wl_040", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_041", "category": "safety", "name": "real_trading_disabled",
     "description": "WATCHLIST_REAL_TRADING_ENABLED = False", "expected_status": "PASS",
     "fixture_id": "wl_041", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_042", "category": "safety", "name": "broker_disabled",
     "description": "WATCHLIST_BROKER_EXECUTION_ENABLED = False", "expected_status": "PASS",
     "fixture_id": "wl_042", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_043", "category": "safety", "name": "margin_disabled",
     "description": "WATCHLIST_MARGIN_ENABLED = False", "expected_status": "PASS",
     "fixture_id": "wl_043", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_044", "category": "safety", "name": "auto_order_disabled",
     "description": "WATCHLIST_AUTO_ORDER_ENABLED = False", "expected_status": "PASS",
     "fixture_id": "wl_044", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_045", "category": "safety", "name": "no_real_account",
     "description": "WATCHLIST_REAL_ACCOUNT_ENABLED = False", "expected_status": "PASS",
     "fixture_id": "wl_045", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_046", "category": "safety", "name": "production_trading_disabled",
     "description": "WATCHLIST_PRODUCTION_TRADING_ENABLED = False", "expected_status": "PASS",
     "fixture_id": "wl_046", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_047", "category": "safety", "name": "audit_all_safe",
     "description": "audit_watchlist_safety all_safe = True", "expected_status": "PASS",
     "fixture_id": "wl_047", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_048", "category": "safety", "name": "assert_safe_no_raise",
     "description": "assert_watchlist_safe() does not raise", "expected_status": "PASS",
     "fixture_id": "wl_048", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_049", "category": "safety", "name": "safety_capabilities_zero",
     "description": "safety_capabilities = 0", "expected_status": "PASS",
     "fixture_id": "wl_049", "deterministic_seed": _DS},

    # ── Enums (5) ─────────────────────────────────────────────────────────────
    {"scenario_id": "wl_sc_050", "category": "enums", "name": "watchlist_tier_core",
     "description": "WatchlistTier.CORE value is 'CORE'", "expected_status": "PASS",
     "fixture_id": "wl_050", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_051", "category": "enums", "name": "theme_strength_leading",
     "description": "ThemeStrength.LEADING exists", "expected_status": "PASS",
     "fixture_id": "wl_051", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_052", "category": "enums", "name": "exclusion_reason_all_15",
     "description": "WatchlistExclusionReason has all 15 required values", "expected_status": "PASS",
     "fixture_id": "wl_052", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_053", "category": "enums", "name": "ranking_grade_no_a_plus",
     "description": "RankingGrade has no A+ value", "expected_status": "PASS",
     "fixture_id": "wl_053", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_054", "category": "enums", "name": "overdiversification_status_all",
     "description": "OverdiversificationStatus has all required values", "expected_status": "PASS",
     "fixture_id": "wl_054", "deterministic_seed": _DS},

    # ── Models (5) ────────────────────────────────────────────────────────────
    {"scenario_id": "wl_sc_055", "category": "models", "name": "candidate_paper_only",
     "description": "WatchlistCandidate.paper_only is always True", "expected_status": "PASS",
     "fixture_id": "wl_055", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_056", "category": "models", "name": "score_result_to_dict",
     "description": "WatchlistScoreResult.to_dict() returns valid dict", "expected_status": "PASS",
     "fixture_id": "wl_056", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_057", "category": "models", "name": "top_selection_to_dict",
     "description": "TopCandidateSelection.to_dict() returns valid dict", "expected_status": "PASS",
     "fixture_id": "wl_057", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_058", "category": "models", "name": "overdiversification_to_dict",
     "description": "OverdiversificationResult.to_dict() returns valid dict", "expected_status": "PASS",
     "fixture_id": "wl_058", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_059", "category": "models", "name": "report_to_dict",
     "description": "WatchlistStrategyReport.to_dict() returns valid dict", "expected_status": "PASS",
     "fixture_id": "wl_059", "deterministic_seed": _DS},

    # ── Ranking (4) ───────────────────────────────────────────────────────────
    {"scenario_id": "wl_sc_060", "category": "ranking", "name": "rank_by_total_score",
     "description": "rank_candidates returns list sorted by total_score desc", "expected_status": "PASS",
     "fixture_id": "wl_060", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_061", "category": "ranking", "name": "core_ranks_above_main_theme",
     "description": "CORE tier ranks above MAIN_THEME even at same score", "expected_status": "PASS",
     "fixture_id": "wl_061", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_062", "category": "ranking", "name": "excluded_ranks_last",
     "description": "EXCLUDED tier ranks last", "expected_status": "FAIL",
     "fixture_id": "wl_062", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_063", "category": "ranking", "name": "ranked_candidate_has_rank",
     "description": "RankedCandidate.rank is 1-indexed", "expected_status": "PASS",
     "fixture_id": "wl_063", "deterministic_seed": _DS},

    # ── Overdiversification (4) ───────────────────────────────────────────────
    {"scenario_id": "wl_sc_064", "category": "overdiversification", "name": "optimal_10_to_30",
     "description": "10-30 candidates => OPTIMAL", "expected_status": "PASS",
     "fixture_id": "wl_064", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_065", "category": "overdiversification", "name": "insufficient_below_10",
     "description": "< 10 candidates => INSUFFICIENT_COVERAGE", "expected_status": "FAIL",
     "fixture_id": "wl_065", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_066", "category": "overdiversification", "name": "overdiversified_above_50",
     "description": "> 50 candidates => OVERDIVERSIFIED", "expected_status": "FAIL",
     "fixture_id": "wl_066", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_067", "category": "overdiversification", "name": "acceptable_30_to_50",
     "description": "30-50 candidates => OPTIMAL", "expected_status": "PASS",
     "fixture_id": "wl_067", "deterministic_seed": _DS},

    # ── Version (5) ───────────────────────────────────────────────────────────
    {"scenario_id": "wl_sc_068", "category": "version", "name": "version_1_7_1",
     "description": "VERSION == '1.7.1'", "expected_status": "PASS",
     "fixture_id": "wl_068", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_069", "category": "version", "name": "release_name_watchlist",
     "description": "RELEASE_NAME == 'Watchlist Strategy Layer'", "expected_status": "PASS",
     "fixture_id": "wl_069", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_070", "category": "version", "name": "base_release_1_7_0",
     "description": "BASE_RELEASE == '1.7.0 Small Capital Growth Strategy Template'", "expected_status": "PASS",
     "fixture_id": "wl_070", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_071", "category": "version", "name": "health_all_pass",
     "description": "watchlist health: all_passed = True", "expected_status": "PASS",
     "fixture_id": "wl_071", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_072", "category": "version", "name": "gate_gate_passed",
     "description": "watchlist gate: gate_passed = True", "expected_status": "PASS",
     "fixture_id": "wl_072", "deterministic_seed": _DS},
    {"scenario_id": "wl_sc_073", "category": "bridge", "name": "bridge_v170_summary",
     "description": "get_v170_bridge_summary returns correct dict", "expected_status": "PASS",
     "fixture_id": "wl_073", "deterministic_seed": _DS},
]

assert len(WATCHLIST_SCENARIO_REGISTRY) >= 70, (
    f"Expected >= 70 scenarios, got {len(WATCHLIST_SCENARIO_REGISTRY)}"
)


def get_scenario_registry() -> List[Dict]:
    """Return a copy of the scenario registry."""
    return list(WATCHLIST_SCENARIO_REGISTRY)


def get_scenario_count() -> int:
    """Return total scenario count."""
    return len(WATCHLIST_SCENARIO_REGISTRY)


def get_scenario_categories() -> List[str]:
    """Return sorted list of unique categories."""
    return sorted(set(s["category"] for s in WATCHLIST_SCENARIO_REGISTRY))
