"""
paper_trading/small_capital_strategy/scenario_registry_v170.py
Scenario registry for Small Capital Growth Strategy Template v1.7.0.
[!] RESEARCH ONLY. PAPER ONLY. NO REAL ORDERS. NO BROKER. NOT INVESTMENT ADVICE.
80+ scenarios. No skip. No xfail.
"""
from __future__ import annotations
from typing import List, Optional, Dict

_DS = 42  # deterministic seed

SCENARIO_REGISTRY: List[dict] = [
    # ── Capital Profile (10) ─────────────────────────────────────────────────
    {"scenario_id": "sc_cp_001", "category": "capital_profile", "name": "default_300k",
     "description": "Capital = 300000 TWD, template_id = small_capital_300k_v170",
     "expected_status": "PASS", "fixture_id": "sc_001", "deterministic_seed": _DS},
    {"scenario_id": "sc_cp_002", "category": "capital_profile", "name": "min_risk_2400",
     "description": "max_loss_min = 2400 TWD",
     "expected_status": "PASS", "fixture_id": "sc_002", "deterministic_seed": _DS},
    {"scenario_id": "sc_cp_003", "category": "capital_profile", "name": "max_risk_4500",
     "description": "max_loss_max = 4500 TWD",
     "expected_status": "PASS", "fixture_id": "sc_003", "deterministic_seed": _DS},
    {"scenario_id": "sc_cp_004", "category": "capital_profile", "name": "invalid_capital_zero",
     "description": "capital_twd = 0 is invalid",
     "expected_status": "FAIL", "fixture_id": "sc_004", "deterministic_seed": _DS},
    {"scenario_id": "sc_cp_005", "category": "capital_profile", "name": "invalid_risk_pct",
     "description": "risk_pct_default outside [min, max] is invalid",
     "expected_status": "FAIL", "fixture_id": "sc_005", "deterministic_seed": _DS},
    {"scenario_id": "sc_cp_006", "category": "capital_profile", "name": "max_holdings_4",
     "description": "max_holdings_max = 4",
     "expected_status": "PASS", "fixture_id": "sc_006", "deterministic_seed": _DS},
    {"scenario_id": "sc_cp_007", "category": "capital_profile", "name": "over_max_holdings",
     "description": "max_holdings_max > 4 is invalid",
     "expected_status": "FAIL", "fixture_id": "sc_007", "deterministic_seed": _DS},
    {"scenario_id": "sc_cp_008", "category": "capital_profile", "name": "profile_type_small_300k",
     "description": "profile_type = SMALL_300K",
     "expected_status": "PASS", "fixture_id": "sc_008", "deterministic_seed": _DS},
    {"scenario_id": "sc_cp_009", "category": "capital_profile", "name": "paper_only_true",
     "description": "paper_only must be True",
     "expected_status": "PASS", "fixture_id": "sc_009", "deterministic_seed": _DS},
    {"scenario_id": "sc_cp_010", "category": "capital_profile", "name": "no_real_orders_true",
     "description": "no_real_orders must be True",
     "expected_status": "PASS", "fixture_id": "sc_010", "deterministic_seed": _DS},

    # ── Allocation (8) ───────────────────────────────────────────────────────
    {"scenario_id": "sc_al_001", "category": "allocation", "name": "bull_allocation",
     "description": "Bull regime: CORE=40%, SWING=35%, SECOND=15%, ST=5%, CASH=5%",
     "expected_status": "PASS", "fixture_id": "sc_011", "deterministic_seed": _DS},
    {"scenario_id": "sc_al_002", "category": "allocation", "name": "range_allocation",
     "description": "Range regime: CORE=35%, SWING=25%, SECOND=10%, ST=5%, CASH=25%",
     "expected_status": "PASS", "fixture_id": "sc_012", "deterministic_seed": _DS},
    {"scenario_id": "sc_al_003", "category": "allocation", "name": "bear_allocation",
     "description": "Bear regime: CORE=30%, SWING=15%, SECOND=5%, ST=0%, CASH=50%",
     "expected_status": "PASS", "fixture_id": "sc_013", "deterministic_seed": _DS},
    {"scenario_id": "sc_al_004", "category": "allocation", "name": "unknown_regime",
     "description": "Unknown regime: conservative allocation",
     "expected_status": "PASS", "fixture_id": "sc_014", "deterministic_seed": _DS},
    {"scenario_id": "sc_al_005", "category": "allocation", "name": "allocation_not_100pct",
     "description": "Allocation not summing to 100% is invalid",
     "expected_status": "FAIL", "fixture_id": "sc_015", "deterministic_seed": _DS},
    {"scenario_id": "sc_al_006", "category": "allocation", "name": "short_term_over_5pct",
     "description": "SHORT_TERM_TRAINING > 5% is invalid",
     "expected_status": "FAIL", "fixture_id": "sc_016", "deterministic_seed": _DS},
    {"scenario_id": "sc_al_007", "category": "allocation", "name": "cash_not_negative",
     "description": "Cash pct cannot be negative",
     "expected_status": "FAIL", "fixture_id": "sc_017", "deterministic_seed": _DS},
    {"scenario_id": "sc_al_008", "category": "allocation", "name": "no_margin_in_bucket",
     "description": "No bucket may enable margin",
     "expected_status": "PASS", "fixture_id": "sc_018", "deterministic_seed": _DS},

    # ── Position Sizing (8) ──────────────────────────────────────────────────
    {"scenario_id": "sc_ps_001", "category": "position_sizing", "name": "6pct_stop_50000",
     "description": "capital=300k, max_loss=3000, stop=6% => position=50000",
     "expected_status": "PASS", "fixture_id": "sc_019", "deterministic_seed": _DS},
    {"scenario_id": "sc_ps_002", "category": "position_sizing", "name": "3pct_stop",
     "description": "stop=3% => position=100000, capped by limits",
     "expected_status": "PASS", "fixture_id": "sc_020", "deterministic_seed": _DS},
    {"scenario_id": "sc_ps_003", "category": "position_sizing", "name": "10pct_stop",
     "description": "stop=10% => position=30000",
     "expected_status": "PASS", "fixture_id": "sc_021", "deterministic_seed": _DS},
    {"scenario_id": "sc_ps_004", "category": "position_sizing", "name": "zero_stop_blocked",
     "description": "stop_loss_pct = 0 => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_022", "deterministic_seed": _DS},
    {"scenario_id": "sc_ps_005", "category": "position_sizing", "name": "wide_stop_degraded",
     "description": "stop_loss_pct > 20% => DEGRADED",
     "expected_status": "DEGRADED", "fixture_id": "sc_023", "deterministic_seed": _DS},
    {"scenario_id": "sc_ps_006", "category": "position_sizing", "name": "bucket_cap",
     "description": "position capped by bucket_remaining_budget",
     "expected_status": "PASS", "fixture_id": "sc_024", "deterministic_seed": _DS},
    {"scenario_id": "sc_ps_007", "category": "position_sizing", "name": "single_position_cap",
     "description": "position capped by max_single_position_amount=105000",
     "expected_status": "PASS", "fixture_id": "sc_025", "deterministic_seed": _DS},
    {"scenario_id": "sc_ps_008", "category": "position_sizing", "name": "short_term_cap_15000",
     "description": "SHORT_TERM_TRAINING position capped at 15000 TWD",
     "expected_status": "PASS", "fixture_id": "sc_026", "deterministic_seed": _DS},

    # ── Buy Points (8) ───────────────────────────────────────────────────────
    {"scenario_id": "sc_bp_001", "category": "buy_points", "name": "a_valid",
     "description": "All A conditions met => VALID",
     "expected_status": "PASS", "fixture_id": "sc_027", "deterministic_seed": _DS},
    {"scenario_id": "sc_bp_002", "category": "buy_points", "name": "a_missing_ma20",
     "description": "A: close < MA20 => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_028", "deterministic_seed": _DS},
    {"scenario_id": "sc_bp_003", "category": "buy_points", "name": "a_financing_overheated",
     "description": "A: financing_overheated => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_029", "deterministic_seed": _DS},
    {"scenario_id": "sc_bp_004", "category": "buy_points", "name": "b_valid",
     "description": "All B conditions met => VALID",
     "expected_status": "PASS", "fixture_id": "sc_030", "deterministic_seed": _DS},
    {"scenario_id": "sc_bp_005", "category": "buy_points", "name": "b_third_extended_candle_blocked",
     "description": "B: third extended red candle => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_031", "deterministic_seed": _DS},
    {"scenario_id": "sc_bp_006", "category": "buy_points", "name": "b_low_volume_blocked",
     "description": "B: volume_ratio < 1.5 => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_032", "deterministic_seed": _DS},
    {"scenario_id": "sc_bp_007", "category": "buy_points", "name": "c_valid",
     "description": "All C conditions met => VALID",
     "expected_status": "PASS", "fixture_id": "sc_033", "deterministic_seed": _DS},
    {"scenario_id": "sc_bp_008", "category": "buy_points", "name": "c_reclaim_failed",
     "description": "C: close does not reclaim MA20 => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_034", "deterministic_seed": _DS},

    # ── Forbidden Checks (8) ─────────────────────────────────────────────────
    {"scenario_id": "sc_fb_001", "category": "forbidden", "name": "margin_blocked",
     "description": "margin_requested=True => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_035", "deterministic_seed": _DS},
    {"scenario_id": "sc_fb_002", "category": "forbidden", "name": "real_order_blocked",
     "description": "real_order_requested=True => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_036", "deterministic_seed": _DS},
    {"scenario_id": "sc_fb_003", "category": "forbidden", "name": "broker_blocked",
     "description": "broker_requested=True => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_037", "deterministic_seed": _DS},
    {"scenario_id": "sc_fb_004", "category": "forbidden", "name": "no_stop_blocked",
     "description": "stop_loss_price=0 => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_038", "deterministic_seed": _DS},
    {"scenario_id": "sc_fb_005", "category": "forbidden", "name": "day_trading_primary_blocked",
     "description": "day_trading_primary=True => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_039", "deterministic_seed": _DS},
    {"scenario_id": "sc_fb_006", "category": "forbidden", "name": "weak_theme_blocked",
     "description": "theme_strength=NONE => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_040", "deterministic_seed": _DS},
    {"scenario_id": "sc_fb_007", "category": "forbidden", "name": "too_many_holdings_blocked",
     "description": "current_holdings >= max_holdings => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_041", "deterministic_seed": _DS},
    {"scenario_id": "sc_fb_008", "category": "forbidden", "name": "risk_exceeds_budget_blocked",
     "description": "position_risk > risk_budget => BLOCKED",
     "expected_status": "BLOCKED", "fixture_id": "sc_042", "deterministic_seed": _DS},

    # ── Watchlist (8) ────────────────────────────────────────────────────────
    {"scenario_id": "sc_wl_001", "category": "watchlist", "name": "default_30",
     "description": "default_watchlist = 30",
     "expected_status": "PASS", "fixture_id": "sc_043", "deterministic_seed": _DS},
    {"scenario_id": "sc_wl_002", "category": "watchlist", "name": "max_50",
     "description": "max_watchlist = 50",
     "expected_status": "PASS", "fixture_id": "sc_044", "deterministic_seed": _DS},
    {"scenario_id": "sc_wl_003", "category": "watchlist", "name": "overdiversified",
     "description": "too many tradable candidates => overdiversification detected",
     "expected_status": "PASS", "fixture_id": "sc_045", "deterministic_seed": _DS},
    {"scenario_id": "sc_wl_004", "category": "watchlist", "name": "rank_top_10",
     "description": "rank_candidates returns top 10 by composite score",
     "expected_status": "PASS", "fixture_id": "sc_046", "deterministic_seed": _DS},
    {"scenario_id": "sc_wl_005", "category": "watchlist", "name": "exclude_weak_theme",
     "description": "filter_for_small_capital excludes low liquidity",
     "expected_status": "PASS", "fixture_id": "sc_047", "deterministic_seed": _DS},
    {"scenario_id": "sc_wl_006", "category": "watchlist", "name": "exclude_liquidity_poor",
     "description": "filter_for_small_capital excludes liquidity_score < 0.5",
     "expected_status": "PASS", "fixture_id": "sc_048", "deterministic_seed": _DS},
    {"scenario_id": "sc_wl_007", "category": "watchlist", "name": "core_tier",
     "description": "WatchlistTier.CORE candidates are prioritized",
     "expected_status": "PASS", "fixture_id": "sc_049", "deterministic_seed": _DS},
    {"scenario_id": "sc_wl_008", "category": "watchlist", "name": "training_tier",
     "description": "WatchlistTier.TRAINING candidates are lower priority",
     "expected_status": "PASS", "fixture_id": "sc_050", "deterministic_seed": _DS},

    # ── Market Regime (5) ────────────────────────────────────────────────────
    {"scenario_id": "sc_mr_001", "category": "market_regime", "name": "bull",
     "description": "BULL: max_invested=95%, cash_min=5%",
     "expected_status": "PASS", "fixture_id": "sc_051", "deterministic_seed": _DS},
    {"scenario_id": "sc_mr_002", "category": "market_regime", "name": "range",
     "description": "RANGE: max_invested=75%, cash_min=25%",
     "expected_status": "PASS", "fixture_id": "sc_052", "deterministic_seed": _DS},
    {"scenario_id": "sc_mr_003", "category": "market_regime", "name": "bear",
     "description": "BEAR: max_invested=50%, cash_min=50%",
     "expected_status": "PASS", "fixture_id": "sc_053", "deterministic_seed": _DS},
    {"scenario_id": "sc_mr_004", "category": "market_regime", "name": "risk_off",
     "description": "RISK_OFF: same as BEAR",
     "expected_status": "PASS", "fixture_id": "sc_054", "deterministic_seed": _DS},
    {"scenario_id": "sc_mr_005", "category": "market_regime", "name": "unknown",
     "description": "UNKNOWN: max_invested=60%, cash_min=40%",
     "expected_status": "PASS", "fixture_id": "sc_055", "deterministic_seed": _DS},

    # ── Reports (4) ─────────────────────────────────────────────────────────
    {"scenario_id": "sc_rp_001", "category": "reports", "name": "markdown",
     "description": "to_markdown returns non-empty string with disclaimer",
     "expected_status": "PASS", "fixture_id": "sc_056", "deterministic_seed": _DS},
    {"scenario_id": "sc_rp_002", "category": "reports", "name": "json",
     "description": "to_json returns valid JSON with paper_only=True",
     "expected_status": "PASS", "fixture_id": "sc_057", "deterministic_seed": _DS},
    {"scenario_id": "sc_rp_003", "category": "reports", "name": "csv",
     "description": "to_csv returns CSV with header and data rows",
     "expected_status": "PASS", "fixture_id": "sc_058", "deterministic_seed": _DS},
    {"scenario_id": "sc_rp_004", "category": "reports", "name": "not_investment_advice_marker",
     "description": "All report outputs include not_investment_advice marker",
     "expected_status": "PASS", "fixture_id": "sc_059", "deterministic_seed": _DS},

    # ── Safety (8) ──────────────────────────────────────────────────────────
    {"scenario_id": "sc_sa_001", "category": "safety", "name": "safety_all_safe",
     "description": "audit_safety returns all_safe=True",
     "expected_status": "PASS", "fixture_id": "sc_060", "deterministic_seed": _DS},
    {"scenario_id": "sc_sa_002", "category": "safety", "name": "no_broker",
     "description": "BROKER_ENABLED=False",
     "expected_status": "PASS", "fixture_id": "sc_061", "deterministic_seed": _DS},
    {"scenario_id": "sc_sa_003", "category": "safety", "name": "no_real_account",
     "description": "REAL_ACCOUNT_ENABLED=False",
     "expected_status": "PASS", "fixture_id": "sc_062", "deterministic_seed": _DS},
    {"scenario_id": "sc_sa_004", "category": "safety", "name": "no_real_order",
     "description": "REAL_ORDER_ENABLED=False",
     "expected_status": "PASS", "fixture_id": "sc_063", "deterministic_seed": _DS},
    {"scenario_id": "sc_sa_005", "category": "safety", "name": "no_margin",
     "description": "MARGIN_ENABLED=False",
     "expected_status": "PASS", "fixture_id": "sc_064", "deterministic_seed": _DS},
    {"scenario_id": "sc_sa_006", "category": "safety", "name": "no_auto_order",
     "description": "AUTO_ORDER_ENABLED=False",
     "expected_status": "PASS", "fixture_id": "sc_065", "deterministic_seed": _DS},
    {"scenario_id": "sc_sa_007", "category": "safety", "name": "no_live_fallback",
     "description": "LIVE_FALLBACK_ENABLED=False",
     "expected_status": "PASS", "fixture_id": "sc_066", "deterministic_seed": _DS},
    {"scenario_id": "sc_sa_008", "category": "safety", "name": "safety_capabilities_zero",
     "description": "safety_capabilities=0",
     "expected_status": "PASS", "fixture_id": "sc_067", "deterministic_seed": _DS},

    # ── Scorecard (5) ───────────────────────────────────────────────────────
    {"scenario_id": "sc_sc_001", "category": "scorecard", "name": "weights_sum_100",
     "description": "SCORE_WEIGHTS sum = 100",
     "expected_status": "PASS", "fixture_id": "sc_068", "deterministic_seed": _DS},
    {"scenario_id": "sc_sc_002", "category": "scorecard", "name": "grade_a_85_100",
     "description": "score 85-100 => grade A",
     "expected_status": "PASS", "fixture_id": "sc_069", "deterministic_seed": _DS},
    {"scenario_id": "sc_sc_003", "category": "scorecard", "name": "grade_f_below_40",
     "description": "score < 40 => grade F",
     "expected_status": "PASS", "fixture_id": "sc_070", "deterministic_seed": _DS},
    {"scenario_id": "sc_sc_004", "category": "scorecard", "name": "safety_blocked",
     "description": "safety failure => BLOCKED grade",
     "expected_status": "BLOCKED", "fixture_id": "sc_071", "deterministic_seed": _DS},
    {"scenario_id": "sc_sc_005", "category": "scorecard", "name": "no_a_plus_grade",
     "description": "Grade A+ must not exist",
     "expected_status": "PASS", "fixture_id": "sc_072", "deterministic_seed": _DS},

    # ── Version Identity (5) ─────────────────────────────────────────────────
    {"scenario_id": "sc_vi_001", "category": "version_identity", "name": "version_170",
     "description": "VERSION == '1.7.0'",
     "expected_status": "PASS", "fixture_id": "sc_073", "deterministic_seed": _DS},
    {"scenario_id": "sc_vi_002", "category": "version_identity", "name": "release_name",
     "description": "RELEASE_NAME == 'Small Capital Growth Strategy Template'",
     "expected_status": "PASS", "fixture_id": "sc_074", "deterministic_seed": _DS},
    {"scenario_id": "sc_vi_003", "category": "version_identity", "name": "base_release",
     "description": "BASE_RELEASE references v1.6.9.1",
     "expected_status": "PASS", "fixture_id": "sc_075", "deterministic_seed": _DS},
    {"scenario_id": "sc_vi_004", "category": "version_identity", "name": "known_release_names",
     "description": "KNOWN_RELEASE_NAMES contains all expected entries",
     "expected_status": "PASS", "fixture_id": "sc_076", "deterministic_seed": _DS},
    {"scenario_id": "sc_vi_005", "category": "version_identity", "name": "schema_version_170",
     "description": "SCHEMA_VERSION == '170'",
     "expected_status": "PASS", "fixture_id": "sc_077", "deterministic_seed": _DS},

    # ── Exit Plan (3) ────────────────────────────────────────────────────────
    {"scenario_id": "sc_ep_001", "category": "exit_plan", "name": "short_term_exit",
     "description": "Short-term: break 5MA=reduce, break 10MA=exit",
     "expected_status": "PASS", "fixture_id": "sc_078", "deterministic_seed": _DS},
    {"scenario_id": "sc_ep_002", "category": "exit_plan", "name": "swing_exit",
     "description": "Swing: break 10MA=reduce, break 20MA=exit, 25-40% staged",
     "expected_status": "PASS", "fixture_id": "sc_079", "deterministic_seed": _DS},
    {"scenario_id": "sc_ep_003", "category": "exit_plan", "name": "core_exit",
     "description": "Core: break 60MA=reduce, fundamental deterioration=exit",
     "expected_status": "PASS", "fixture_id": "sc_080", "deterministic_seed": _DS},
]

assert len(SCENARIO_REGISTRY) >= 80, f"Need >= 80 scenarios, got {len(SCENARIO_REGISTRY)}"


def get_registry() -> List[dict]:
    """Return a copy of the scenario registry."""
    return list(SCENARIO_REGISTRY)


def get_scenario(scenario_id: str) -> Optional[dict]:
    """Return scenario by ID, or None."""
    for s in SCENARIO_REGISTRY:
        if s["scenario_id"] == scenario_id:
            return dict(s)
    return None


def get_scenarios_by_category(category: str) -> List[dict]:
    """Return all scenarios in the given category."""
    return [s for s in SCENARIO_REGISTRY if s["category"] == category]


def validate_registry() -> Dict[str, object]:
    """Validate the scenario registry for uniqueness and completeness."""
    ids = [s["scenario_id"] for s in SCENARIO_REGISTRY]
    fixture_ids = [s["fixture_id"] for s in SCENARIO_REGISTRY]
    duplicate_ids = [sid for sid in ids if ids.count(sid) > 1]
    issues = []
    if duplicate_ids:
        issues.append(f"Duplicate scenario_ids: {set(duplicate_ids)}")
    for s in SCENARIO_REGISTRY:
        for field in ("scenario_id", "category", "name", "description", "expected_status", "fixture_id"):
            if not s.get(field):
                issues.append(f"scenario {s.get('scenario_id', '?')} missing {field}")
    return {
        "total": len(SCENARIO_REGISTRY),
        "duplicate_ids": sorted(set(duplicate_ids)),
        "issues": issues,
        "valid": len(issues) == 0,
    }
