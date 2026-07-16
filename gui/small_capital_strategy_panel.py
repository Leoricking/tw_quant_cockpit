"""
gui/small_capital_strategy_panel.py
GUI panel for Small Capital Growth Strategy Template v1.7.0 +
Watchlist Strategy Layer v1.7.1 +
A/B/C Buy Point Execution Plan v1.7.2 +
Market Regime Position Control v1.7.3 +
Small Account Risk Dashboard v1.7.4 +
Small Account Trade Journal v1.7.5 +
Mistake Taxonomy & Weekly Review Dashboard v1.7.6 +
Theme Rotation Scanner v1.7.7 +
Small Capital Strategy Integration v1.7.8.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
Headless-safe: no tkinter at module level. Renders to dict.
22 v1.7.0 tabs + 15 watchlist tabs + 18 abc tabs + 14 regime tabs + 15 risk dashboard tabs + 14 trade journal tabs + 13 mistake taxonomy tabs + 3 theme rotation tabs + 3 integrated strategy tabs + 3 stable rollup tabs = 120 tabs total.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

PANEL_VERSION = "1.8.9"
PANEL_TITLE = "Small Capital Strategy v1.8.9 — Paper Decision Journal & Review Loop"

# v1.7.0 tabs (preserved unchanged)
_TABS_V170 = [
    "overview",
    "version_info",
    "safety",
    "capital_profile",
    "risk_budget",
    "allocation",
    "market_regime",
    "watchlist",
    "theme_filter",
    "buy_points_abc",
    "entry_plan",
    "exit_plan",
    "stop_loss",
    "take_profit",
    "position_sizing",
    "forbidden_checks",
    "cash_control",
    "scorecard",
    "strategy_template",
    "paper_simulation",
    "scenarios",
    "health_gate",
]

# v1.7.1 watchlist tabs
_TABS_V171_WATCHLIST = [
    "watchlist_overview",
    "watchlist_candidate_pool",
    "watchlist_theme_rotation",
    "watchlist_score_weights",
    "watchlist_ranking",
    "watchlist_top_10_focus",
    "watchlist_top_5_tradable",
    "watchlist_tier_classification",
    "watchlist_excluded",
    "watchlist_overdiversification",
    "watchlist_allocation_mapping",
    "watchlist_safety",
    "watchlist_report",
    "watchlist_health",
    "watchlist_gate",
]

# v1.7.2 A/B/C execution tabs
_TABS_V172_ABC = [
    "abc_execution_overview",
    "abc_a_10ma_pullback",
    "abc_b_platform_breakout",
    "abc_c_20ma_reclaim",
    "abc_candidate_compatibility",
    "abc_market_regime_compatibility",
    "abc_entry_plan",
    "abc_add_plan",
    "abc_stop_loss_plan",
    "abc_take_profit_plan",
    "abc_position_sizing",
    "abc_forbidden_checks",
    "abc_paper_order_intent",
    "abc_scorecard",
    "abc_report",
    "abc_health",
    "abc_gate",
    "abc_safety",
]

# v1.7.3 Market Regime Position Control tabs
_TABS_V173_REGIME = [
    "regime_overview",
    "regime_detection",
    "regime_trend_filter",
    "regime_volatility_filter",
    "regime_breadth_filter",
    "regime_risk_off_detection",
    "regime_cash_ratio",
    "regime_exposure_control",
    "regime_bucket_adjustment",
    "regime_candidate_permission",
    "regime_abc_compatibility",
    "regime_scorecard",
    "regime_report",
    "regime_health_gate",
]

# v1.7.4 Small Account Risk Dashboard tabs
_TABS_V174_RISK_DASHBOARD = [
    "risk_dashboard_overview",
    "risk_capital",
    "risk_single_trade",
    "risk_portfolio_exposure",
    "risk_cash_ratio",
    "risk_position_count",
    "risk_drawdown",
    "risk_losing_streak",
    "risk_concentration",
    "risk_theme_exposure",
    "risk_stop_loss_coverage",
    "risk_abc_risk",
    "risk_watchlist_risk",
    "risk_market_regime_risk",
    "risk_scorecard",
]

# v1.7.5 Trade Journal tabs
_TABS_V175_TRADE_JOURNAL = [
    "trade_journal_overview",
    "trade_journal_entry",
    "trade_journal_review_entry",
    "trade_journal_review_exit",
    "trade_journal_abc_review",
    "trade_journal_watchlist_review",
    "trade_journal_risk_review",
    "trade_journal_regime_review",
    "trade_journal_mistake_taxonomy",
    "trade_journal_scorecard",
    "trade_journal_report",
    "trade_journal_scenarios",
    "trade_journal_health",
    "trade_journal_gate",
]

# v1.7.7 Theme Rotation Scanner tabs
_TABS_V177_THEME_ROTATION = [
    "theme_rotation",
    "theme_ranking",
    "theme_watchlist",
]

# v1.7.6 Mistake Taxonomy & Weekly Review Dashboard tabs
_TABS_V176_MISTAKE_TAXONOMY = [
    "mistake_review_overview",
    "mistake_taxonomy_classify",
    "mistake_taxonomy_cost",
    "mistake_taxonomy_repeat",
    "weekly_review",
    "monthly_review",
    "behavior_risk_score",
    "behavior_risk_actions",
    "review_dashboard",
    "review_report",
    "review_scenarios",
    "review_health",
    "review_gate",
]

# v1.7.8 Integrated Strategy / Decision Dashboard / Paper Plan tabs
_TABS_V178_INTEGRATED_STRATEGY = [
    "integrated_strategy",
    "integrated_decision_dashboard",
    "integrated_paper_plan",
]

_TABS_V179_STABLE_ROLLUP = [
    "stable_rollup",
    "stable_health",
    "stable_report",
]

_TABS_V180_PAPER_SIM = [
    "paper_sim_lab",
    "paper_sim_equity_curve",
    "paper_sim_performance",
]

# v1.8.1 Simulation Scenario Matrix & Stress Test Lab tabs
_TABS_V181_SIM_MATRIX = [
    "sim_matrix_lab",
    "sim_stress_test",
    "sim_robustness_score",
]

_TABS_V182_OPTIMIZATION = [
    "param_optimization",
    "walk_forward_validation",
    "overfitting_risk",
]

# v1.8.3 Monte Carlo Risk-of-Ruin & Robustness Lab tabs
_TABS_V183_MONTE_CARLO = [
    "monte_carlo",
    "risk_of_ruin",
    "robustness_probability",
]

# v1.8.4 Position Sizing & Capital Allocation Lab tabs
_TABS_V184_POSITION_SIZING = [
    "position_sizing_lab",
    "risk_budget_allocation",
    "capital_allocation",
]

# v1.8.5 Portfolio Construction & Rebalancing Lab tabs
_TABS_V185_PORTFOLIO_CONSTRUCTION = [
    "portfolio_construction_lab",
    "portfolio_rebalancing",
    "portfolio_exposure_control",
]

# v1.8.6 End-to-End Small Capital Decision Cockpit tabs
_TABS_V186_DECISION_COCKPIT = [
    "daily_decision_cockpit",
    "weekly_decision_review",
    "block_reasons",
]

# v1.8.7 Decision Report Export & Evidence Pack tabs
_TABS_V187_DECISION_REPORT = [
    "decision_report",
    "evidence_pack",
    "audit_trail_report",
]

assert len(_TABS_V187_DECISION_REPORT) == 3, f"Expected 3 decision report tabs, got {len(_TABS_V187_DECISION_REPORT)}"

# v1.8.8 Paper Decision Workflow Runner tabs
_TABS_V188_DECISION_WORKFLOW = [
    "decision_workflow",
    "daily_workflow",
    "weekly_workflow",
]

assert len(_TABS_V188_DECISION_WORKFLOW) == 3, f"Expected 3 decision workflow tabs, got {len(_TABS_V188_DECISION_WORKFLOW)}"

# v1.8.9 Paper Decision Journal & Review Loop tabs
_TABS_V189_DECISION_JOURNAL = [
    "decision_journal",
    "daily_review",
    "weekly_review",
]

assert len(_TABS_V189_DECISION_JOURNAL) == 3, f"Expected 3 decision journal tabs, got {len(_TABS_V189_DECISION_JOURNAL)}"

_TABS = (
    _TABS_V170
    + _TABS_V171_WATCHLIST
    + _TABS_V172_ABC
    + _TABS_V173_REGIME
    + _TABS_V174_RISK_DASHBOARD
    + _TABS_V175_TRADE_JOURNAL
    + _TABS_V176_MISTAKE_TAXONOMY
    + _TABS_V177_THEME_ROTATION
    + _TABS_V178_INTEGRATED_STRATEGY
    + _TABS_V179_STABLE_ROLLUP
    + _TABS_V180_PAPER_SIM
    + _TABS_V181_SIM_MATRIX
    + _TABS_V182_OPTIMIZATION
    + _TABS_V183_MONTE_CARLO
    + _TABS_V184_POSITION_SIZING
    + _TABS_V185_PORTFOLIO_CONSTRUCTION
    + _TABS_V186_DECISION_COCKPIT
    + _TABS_V187_DECISION_REPORT
    + _TABS_V188_DECISION_WORKFLOW
    + ["decision_journal", "daily_review"]  # v1.8.9: weekly_review already present from v1.7.6
)

assert len(_TABS_V170) == 22, f"Expected 22 v1.7.0 tabs, got {len(_TABS_V170)}"
assert len(_TABS_V171_WATCHLIST) == 15, f"Expected 15 watchlist tabs, got {len(_TABS_V171_WATCHLIST)}"
assert len(_TABS_V172_ABC) == 18, f"Expected 18 ABC tabs, got {len(_TABS_V172_ABC)}"
assert len(_TABS_V173_REGIME) == 14, f"Expected 14 regime tabs, got {len(_TABS_V173_REGIME)}"
assert len(_TABS_V174_RISK_DASHBOARD) == 15, f"Expected 15 risk dashboard tabs, got {len(_TABS_V174_RISK_DASHBOARD)}"
assert len(_TABS_V175_TRADE_JOURNAL) == 14, f"Expected 14 trade journal tabs, got {len(_TABS_V175_TRADE_JOURNAL)}"
assert len(_TABS_V176_MISTAKE_TAXONOMY) == 13, f"Expected 13 mistake taxonomy tabs, got {len(_TABS_V176_MISTAKE_TAXONOMY)}"
assert len(_TABS_V177_THEME_ROTATION) == 3, f"Expected 3 theme rotation tabs, got {len(_TABS_V177_THEME_ROTATION)}"
assert len(_TABS_V178_INTEGRATED_STRATEGY) == 3, f"Expected 3 integrated strategy tabs, got {len(_TABS_V178_INTEGRATED_STRATEGY)}"
assert len(_TABS_V179_STABLE_ROLLUP) == 3, f"Expected 3 stable rollup tabs, got {len(_TABS_V179_STABLE_ROLLUP)}"
assert len(_TABS_V180_PAPER_SIM) == 3, f"Expected 3 paper sim tabs, got {len(_TABS_V180_PAPER_SIM)}"
assert len(_TABS_V181_SIM_MATRIX) == 3, f"Expected 3 sim matrix tabs, got {len(_TABS_V181_SIM_MATRIX)}"
assert len(_TABS_V182_OPTIMIZATION) == 3, f"Expected 3 optimization tabs, got {len(_TABS_V182_OPTIMIZATION)}"
assert len(_TABS_V183_MONTE_CARLO) == 3, f"Expected 3 monte carlo tabs, got {len(_TABS_V183_MONTE_CARLO)}"
assert len(_TABS_V184_POSITION_SIZING) == 3, f"Expected 3 position sizing tabs, got {len(_TABS_V184_POSITION_SIZING)}"
assert len(_TABS_V185_PORTFOLIO_CONSTRUCTION) == 3, f"Expected 3 portfolio construction tabs, got {len(_TABS_V185_PORTFOLIO_CONSTRUCTION)}"
assert len(_TABS_V186_DECISION_COCKPIT) == 3, f"Expected 3 decision cockpit tabs, got {len(_TABS_V186_DECISION_COCKPIT)}"


def get_tab_names() -> List[str]:
    """Return list of all tab names (v1.7.0 + v1.7.1 watchlist)."""
    return list(_TABS)


def get_watchlist_tab_names() -> List[str]:
    """Return list of v1.7.1 watchlist tab names."""
    return list(_TABS_V171_WATCHLIST)


def render_daily_decision_cockpit_tab() -> Dict[str, Any]:
    """Render daily decision cockpit tab data (headless-safe, decision-only)."""
    return {
        "tab": "daily_decision_cockpit",
        "version": PANEL_VERSION,
        "release_name": "End-to-End Small Capital Decision Cockpit",
        "description": "Daily paper-only decision cockpit: regime, candidates, A/B/C buy points, risk, portfolio, Monte Carlo.",
        "paper_only": True,
        "research_only": True,
        "decision_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No daily decision data available. Run decision-cockpit-daily to populate.",
        "schema_version": "186",
    }


def render_weekly_decision_review_tab() -> Dict[str, Any]:
    """Render weekly decision review tab data (headless-safe, decision-only)."""
    return {
        "tab": "weekly_decision_review",
        "version": PANEL_VERSION,
        "release_name": "End-to-End Small Capital Decision Cockpit",
        "description": "Weekly review: portfolio health, exposure, regime, block reasons, rebalance decisions.",
        "paper_only": True,
        "research_only": True,
        "decision_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No weekly review data available. Run decision-cockpit-weekly to populate.",
        "schema_version": "186",
    }


def render_block_reasons_tab() -> Dict[str, Any]:
    """Render block reasons tab data (headless-safe, decision-only)."""
    return {
        "tab": "block_reasons",
        "version": PANEL_VERSION,
        "release_name": "End-to-End Small Capital Decision Cockpit",
        "description": "Block reason registry: hard block conditions, triggered blocks, resolution guidance.",
        "paper_only": True,
        "research_only": True,
        "decision_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No block reasons recorded. All conditions clear.",
        "schema_version": "186",
    }


def render_overview_tab() -> Dict[str, Any]:
    """Render overview tab data."""
    return {
        "title": PANEL_TITLE,
        "version": PANEL_VERSION,
        "release_name": "Small Capital Growth Strategy Template",
        "base_release": "1.6.9.1 Stable Rollup Compatibility Hotfix",
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
        "tab_count": len(_TABS),
    }


def render_version_info_tab() -> Dict[str, Any]:
    """Render version info tab data."""
    from paper_trading.small_capital_strategy.version_v170 import get_version_info
    return get_version_info()


def render_safety_tab() -> Dict[str, Any]:
    """Render safety tab data."""
    from paper_trading.small_capital_strategy.safety_v170 import get_safety_flags, audit_safety
    return {
        "flags": get_safety_flags(),
        "audit": audit_safety(),
    }


def render_capital_profile_tab() -> Dict[str, Any]:
    """Render capital profile tab data."""
    from paper_trading.small_capital_strategy.capital_profile_v170 import (
        get_300k_template, validate_capital_profile,
    )
    profile = get_300k_template()
    validation = validate_capital_profile(profile)
    return {
        "template_id": profile.template_id,
        "capital_twd": profile.capital_twd,
        "max_loss_default": profile.max_loss_default,
        "risk_pct_default": profile.risk_pct_default,
        "max_holdings_default": profile.max_holdings_default,
        "validation": validation,
    }


def render_risk_budget_tab() -> Dict[str, Any]:
    """Render risk budget tab data."""
    from paper_trading.small_capital_strategy.capital_profile_v170 import get_300k_template
    from paper_trading.small_capital_strategy.risk_budget_v170 import compute_risk_budget, validate_risk_budget
    profile = get_300k_template()
    budget = compute_risk_budget(profile)
    return {
        "max_loss_per_trade": budget.max_loss_per_trade,
        "risk_pct_per_trade": budget.risk_pct_per_trade,
        "max_total_risk_pct": budget.max_total_risk_pct,
        "validation": validate_risk_budget(budget),
    }


def render_allocation_tab(regime_str: str = "BULL") -> Dict[str, Any]:
    """Render allocation tab data for given regime."""
    from paper_trading.small_capital_strategy.enums_v170 import MarketRegime
    from paper_trading.small_capital_strategy.capital_profile_v170 import (
        get_300k_template, TEMPLATE_300K_ID,
    )
    from paper_trading.small_capital_strategy.allocation_template_v170 import (
        get_allocation_for_regime, validate_allocation,
    )
    try:
        regime = MarketRegime[regime_str.upper()]
    except KeyError:
        regime = MarketRegime.BULL
    profile = get_300k_template()
    alloc = get_allocation_for_regime(regime, TEMPLATE_300K_ID, profile.capital_twd)
    buckets_data = {b.bucket.value: b.target_pct for b in alloc.buckets}
    return {
        "regime": regime.value,
        "buckets": buckets_data,
        "cash_pct": alloc.cash_pct,
        "total_invested_pct": alloc.total_invested_pct,
        "validation": validate_allocation(alloc),
    }


def render_market_regime_tab(regime_str: str = "BULL") -> Dict[str, Any]:
    """Render market regime tab data."""
    from paper_trading.small_capital_strategy.enums_v170 import MarketRegime
    from paper_trading.small_capital_strategy.market_regime_filter_v170 import (
        get_regime_control, is_trade_allowed_in_regime,
    )
    try:
        regime = MarketRegime[regime_str.upper()]
    except KeyError:
        regime = MarketRegime.UNKNOWN
    result = get_regime_control(regime)
    return {
        "regime": regime.value,
        "max_invested_pct": result.max_invested_pct,
        "cash_min_pct": result.cash_min_pct,
        "short_term_training_allowed": result.short_term_training_allowed,
        "trade_allowed": is_trade_allowed_in_regime(regime),
    }


def render_watchlist_tab() -> Dict[str, Any]:
    """Render watchlist tab data."""
    from paper_trading.small_capital_strategy.watchlist_profile_v170 import (
        create_default_watchlist_profile,
        MAX_WATCHLIST, DEFAULT_WATCHLIST, FOCUS_CANDIDATES, TRADABLE_CANDIDATES,
    )
    wp = create_default_watchlist_profile()
    return {
        "max_watchlist": MAX_WATCHLIST,
        "default_watchlist": DEFAULT_WATCHLIST,
        "focus_candidates": FOCUS_CANDIDATES,
        "tradable_candidates": TRADABLE_CANDIDATES,
        "profile": wp.to_dict() if hasattr(wp, "to_dict") else str(wp),
    }


def render_theme_filter_tab() -> Dict[str, Any]:
    """Render theme filter tab data."""
    from paper_trading.small_capital_strategy.theme_filter_v170 import (
        MINIMUM_THEME_STRENGTH,
    )
    return {
        "minimum_theme_strength": MINIMUM_THEME_STRENGTH.value,
        "description": "Filters candidates below minimum theme strength threshold.",
    }


def render_buy_points_tab() -> Dict[str, Any]:
    """Render A/B/C buy points tab data."""
    from paper_trading.small_capital_strategy.buy_point_rules_v170 import (
        check_a_buy_point, check_b_buy_point, check_c_buy_point,
    )
    return {
        "a_buy_point": "10MA pullback — theme STRONG, close>MA20&MA60, low<=MA10, volume contracting",
        "b_buy_point": "Platform breakout — 2-6 week consolidation, close>platform_high, volume_ratio>=1.5",
        "c_buy_point": "20MA second wave reclaim — had first wave, pullback done, KD golden cross",
    }


def render_entry_plan_tab() -> Dict[str, Any]:
    """Render entry plan tab data."""
    from paper_trading.small_capital_strategy.entry_plan_v170 import build_entry_plan
    return {
        "description": "Entry plan builder for A/B/C buy points.",
        "paper_only": True,
    }


def render_exit_plan_tab() -> Dict[str, Any]:
    """Render exit plan tab data."""
    return {
        "short_term_target_pct": "10-15%",
        "swing_target_pct": "25-40%",
        "core_target_pct": "40%+",
        "paper_only": True,
    }


def render_stop_loss_tab() -> Dict[str, Any]:
    """Render stop loss tab data."""
    return {
        "types": ["MA-based", "Swing low", "Platform", "Fixed pct"],
        "paper_only": True,
    }


def render_take_profit_tab() -> Dict[str, Any]:
    """Render take profit tab data."""
    return {
        "short_term_min_pct": 0.10,
        "short_term_max_pct": 0.15,
        "swing_min_pct": 0.25,
        "swing_max_pct": 0.40,
        "paper_only": True,
    }


def render_position_sizing_tab() -> Dict[str, Any]:
    """Render position sizing tab data."""
    return {
        "formula": "position_size = max_loss_amount / stop_loss_pct",
        "example": "3000 / 0.06 = 50000 TWD",
        "max_single_position_pct": 0.35,
        "max_single_position_twd": 105000,
        "short_term_training_cap_twd": 15000,
        "paper_only": True,
    }


def render_forbidden_checks_tab() -> Dict[str, Any]:
    """Render forbidden checks tab data."""
    from paper_trading.small_capital_strategy.forbidden_trade_rules_v170 import (
        run_all_forbidden_checks, get_permission_status, TradePermissionStatus,
    )
    from paper_trading.small_capital_strategy.enums_v170 import ThemeStrength
    context = {
        "margin_requested": False,
        "is_day_trading_primary": False,
        "financing_overheated": False,
        "real_order_requested": False,
        "broker_requested": False,
        "stop_loss_price": 470.0,
        "current_holdings": 0,
        "max_holdings": 4,
        "theme_strength": ThemeStrength.STRONG.value,
        "close_gt_ma20": True,
        "close_gt_ma60": True,
        "current_cash_pct": 0.30,
        "required_cash_min_pct": 0.20,
        "position_risk_twd": 0.0,
        "risk_budget_twd": 3000.0,
    }
    checks = run_all_forbidden_checks("_template_", context)
    status = get_permission_status(checks)
    return {
        "permission_status": status.value,
        "blocked_count": sum(1 for c in checks if c.blocked),
        "total_checks": len(checks),
        "paper_only": True,
        "no_real_orders": True,
    }


def render_cash_control_tab() -> Dict[str, Any]:
    """Render cash control tab data."""
    from paper_trading.small_capital_strategy.cash_control_v170 import get_cash_control_plan
    from paper_trading.small_capital_strategy.enums_v170 import MarketRegime
    plan = get_cash_control_plan(MarketRegime.BULL, 300000.0)
    return plan.to_dict() if hasattr(plan, "to_dict") else {"plan": str(plan)}


def render_scorecard_tab() -> Dict[str, Any]:
    """Render scorecard tab data."""
    from paper_trading.small_capital_strategy.small_capital_scorecard_v170 import (
        get_scorecard_weights, SCORE_WEIGHTS,
    )
    return {
        "weights": get_scorecard_weights(),
        "weights_sum": sum(SCORE_WEIGHTS.values()),
        "grade_thresholds": {
            "A": "85-100",
            "B": "70-84",
            "C": "55-69",
            "D": "40-54",
            "F": "0-39",
            "BLOCKED": "safety failure",
        },
        "note": "No A+ grade.",
    }


def render_strategy_template_tab() -> Dict[str, Any]:
    """Render strategy template tab data."""
    from paper_trading.small_capital_strategy.enums_v170 import MarketRegime
    from paper_trading.small_capital_strategy.strategy_template_v170 import (
        build_300k_template, get_template_summary,
    )
    tmpl = build_300k_template(regime=MarketRegime.BULL)
    return get_template_summary(tmpl)


def render_paper_simulation_tab() -> Dict[str, Any]:
    """Render paper simulation tab data."""
    from paper_trading.small_capital_strategy.paper_simulation_bridge_v170 import (
        get_simulation_safety_summary,
    )
    return get_simulation_safety_summary()


def render_scenarios_tab() -> Dict[str, Any]:
    """Render scenarios tab data."""
    from paper_trading.small_capital_strategy.scenario_registry_v170 import (
        SCENARIO_REGISTRY, get_scenarios_by_category,
    )
    categories = sorted(set(s["category"] for s in SCENARIO_REGISTRY))
    return {
        "total": len(SCENARIO_REGISTRY),
        "categories": {cat: len(get_scenarios_by_category(cat)) for cat in categories},
    }


def render_health_gate_tab() -> Dict[str, Any]:
    """Render health and gate tab data."""
    from paper_trading.small_capital_strategy.health_v170 import run_health_check
    from release.small_capital_growth_strategy_release_gate_v170 import run_release_gate
    health = run_health_check()
    gate = run_release_gate()
    return {
        "health_all_passed": health["all_passed"],
        "health_passed": health["passed"],
        "health_failed": health["failed"],
        "gate_passed": gate["gate_passed"],
        "gate_passed_count": gate["passed_count"],
        "gate_failed_count": gate["failed_count"],
    }


def render_watchlist_overview_tab() -> Dict[str, Any]:
    """Render watchlist overview tab. v1.7.1."""
    from paper_trading.small_capital_strategy.version_v171 import get_version_info
    from paper_trading.small_capital_strategy.overdiversification_detector_v171 import (
        get_watchlist_size_rules,
    )
    return {
        "version": "1.7.1",
        "release_name": "Watchlist Strategy Layer",
        "watchlist_rules": get_watchlist_size_rules(),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
    }


def render_watchlist_candidate_pool_tab() -> Dict[str, Any]:
    """Render watchlist candidate pool tab. v1.7.1."""
    from paper_trading.small_capital_strategy.watchlist_candidate_v171 import (
        get_required_candidate_fields,
    )
    return {
        "required_fields": get_required_candidate_fields(),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def render_watchlist_theme_rotation_tab() -> Dict[str, Any]:
    """Render theme rotation tab. v1.7.1."""
    from paper_trading.small_capital_strategy.theme_rotation_v171 import (
        get_sample_theme_signals,
    )
    signals = get_sample_theme_signals()
    return {
        "theme_signals": [s.to_dict() for s in signals],
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def render_watchlist_score_weights_tab() -> Dict[str, Any]:
    """Render score weights tab. v1.7.1."""
    from paper_trading.small_capital_strategy.watchlist_score_v171 import get_score_weights
    return {
        "score_weights": get_score_weights(),
        "max_grade": "A",
        "blocked_grade": "BLOCKED",
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def render_watchlist_ranking_tab() -> Dict[str, Any]:
    """Render ranking tab. v1.7.1."""
    from paper_trading.small_capital_strategy.watchlist_ranking_v171 import get_ranking_rules
    return {
        "ranking_rules": get_ranking_rules(),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def render_watchlist_top_10_focus_tab() -> Dict[str, Any]:
    """Render top 10 focus candidates tab. v1.7.1."""
    return {
        "max_focus": 10,
        "note": "Provide candidate data via watchlist-top-focus CLI command",
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def render_watchlist_top_5_tradable_tab() -> Dict[str, Any]:
    """Render top 5 tradable candidates tab. v1.7.1."""
    return {
        "max_tradable": 5,
        "note": "Provide candidate data via watchlist-top-tradable CLI command",
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def render_watchlist_tier_classification_tab() -> Dict[str, Any]:
    """Render tier classification tab. v1.7.1."""
    from paper_trading.small_capital_strategy.watchlist_tier_classifier_v171 import (
        get_tier_thresholds,
    )
    return {
        "tier_thresholds": get_tier_thresholds(),
        "tiers": ["CORE", "MAIN_THEME", "SECOND_WAVE", "TRAINING", "EXCLUDED"],
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def render_watchlist_excluded_tab() -> Dict[str, Any]:
    """Render excluded candidates tab. v1.7.1."""
    from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
        WatchlistExclusionReason,
    )
    return {
        "exclusion_reasons": [r.value for r in WatchlistExclusionReason],
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def render_watchlist_overdiversification_tab() -> Dict[str, Any]:
    """Render overdiversification tab. v1.7.1."""
    from paper_trading.small_capital_strategy.overdiversification_detector_v171 import (
        get_watchlist_size_rules,
    )
    return {
        "size_rules": get_watchlist_size_rules(),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def render_watchlist_allocation_mapping_tab() -> Dict[str, Any]:
    """Render allocation mapping tab. v1.7.1."""
    from paper_trading.small_capital_strategy.small_capital_watchlist_bridge_v171 import (
        get_v170_bridge_summary,
    )
    return get_v170_bridge_summary()


def render_watchlist_safety_tab() -> Dict[str, Any]:
    """Render watchlist safety tab. v1.7.1."""
    from paper_trading.small_capital_strategy.watchlist_safety_v171 import (
        get_watchlist_safety_flags, audit_watchlist_safety,
    )
    return {
        "flags": get_watchlist_safety_flags(),
        "audit": audit_watchlist_safety(),
    }


def render_watchlist_report_tab() -> Dict[str, Any]:
    """Render watchlist report tab. v1.7.1."""
    from paper_trading.small_capital_strategy.watchlist_report_v171 import get_section_names
    return {
        "section_names": get_section_names(),
        "formats": ["MARKDOWN", "JSON", "CSV", "CONSOLE", "GUI"],
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def render_watchlist_health_tab() -> Dict[str, Any]:
    """Render watchlist health tab. v1.7.1."""
    from paper_trading.small_capital_strategy.watchlist_health_v171 import run_health_check
    health = run_health_check()
    return {
        "all_passed": health["all_passed"],
        "passed": health["passed"],
        "failed": health["failed"],
        "total": health["total"],
        "status": health["status"],
    }


def render_watchlist_gate_tab() -> Dict[str, Any]:
    """Render watchlist gate tab. v1.7.1."""
    from release.watchlist_strategy_layer_release_gate_v171 import run_release_gate
    gate = run_release_gate()
    return {
        "gate_passed": gate["gate_passed"],
        "passed_count": gate["passed_count"],
        "failed_count": gate["failed_count"],
        "total_count": gate["total_count"],
        "status": gate["status"],
    }


def render_abc_execution_overview_tab() -> Dict[str, Any]:
    """Render ABC execution overview tab. v1.7.2."""
    from paper_trading.small_capital_strategy.version_v172 import get_version_info
    info = get_version_info()
    return {
        "version": info["version"],
        "release_name": info["release_name"],
        "base_release": info["base_release"],
        "buy_point_types": ["A_10MA_PULLBACK", "B_PLATFORM_BREAKOUT", "C_20MA_RECLAIM"],
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
    }


def render_abc_a_10ma_pullback_tab() -> Dict[str, Any]:
    """Render A buy point (10MA Pullback) tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_condition_checker_v172 import (
        get_condition_names,
    )
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCBuyPointType
    return {
        "buy_point_type": "A_10MA_PULLBACK",
        "description": "10MA Pullback: close >= MA10 after pullback, theme STRONG+, above MA20 & MA60",
        "required_conditions": get_condition_names(ABCBuyPointType.A_10MA_PULLBACK),
        "entry_mode": "MA10_RECLAIM",
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_b_platform_breakout_tab() -> Dict[str, Any]:
    """Render B buy point (Platform Breakout) tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_condition_checker_v172 import (
        get_condition_names,
    )
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCBuyPointType
    return {
        "buy_point_type": "B_PLATFORM_BREAKOUT",
        "description": "Platform Breakout: 2-6 week consolidation, close > platform high, volume_ratio >= 1.5",
        "required_conditions": get_condition_names(ABCBuyPointType.B_PLATFORM_BREAKOUT),
        "entry_mode": "BREAKOUT_CONFIRMATION",
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_c_20ma_reclaim_tab() -> Dict[str, Any]:
    """Render C buy point (20MA Reclaim) tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_condition_checker_v172 import (
        get_condition_names,
    )
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCBuyPointType
    return {
        "buy_point_type": "C_20MA_RECLAIM",
        "description": "20MA Second Wave Reclaim: had first wave, pullback completed, KD improving",
        "required_conditions": get_condition_names(ABCBuyPointType.C_20MA_RECLAIM),
        "entry_mode": "MA20_RECLAIM",
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_candidate_compatibility_tab() -> Dict[str, Any]:
    """Render candidate/watchlist tier compatibility tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_watchlist_bridge_v172 import (
        get_tier_allowed_buy_points, get_tier_preferred_buy_points,
    )
    tiers = ["CORE", "MAIN_THEME", "SECOND_WAVE", "TRAINING", "EXCLUDED"]
    return {
        "tiers": tiers,
        "allowed": {t: [b.value for b in get_tier_allowed_buy_points(t)] for t in tiers},
        "preferred": {t: [b.value for b in get_tier_preferred_buy_points(t)] for t in tiers},
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_market_regime_compatibility_tab() -> Dict[str, Any]:
    """Render market regime compatibility tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_market_regime_bridge_v172 import (
        get_compatible_regimes,
    )
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCBuyPointType
    return {
        "A_compatible_regimes": get_compatible_regimes(ABCBuyPointType.A_10MA_PULLBACK),
        "B_compatible_regimes": get_compatible_regimes(ABCBuyPointType.B_PLATFORM_BREAKOUT),
        "C_compatible_regimes": get_compatible_regimes(ABCBuyPointType.C_20MA_RECLAIM),
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_entry_plan_tab() -> Dict[str, Any]:
    """Render ABC entry plan tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCEntryMode
    return {
        "entry_modes": [m.value for m in ABCEntryMode],
        "a_entry_mode": "MA10_RECLAIM",
        "b_entry_mode": "BREAKOUT_CONFIRMATION",
        "c_entry_mode": "MA20_RECLAIM",
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_add_plan_tab() -> Dict[str, Any]:
    """Render ABC add plan tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCAddMode
    return {
        "add_modes": [m.value for m in ABCAddMode],
        "a_add_mode": "MA5_RECLAIM",
        "b_add_mode": "SECOND_DAY_HOLD",
        "c_add_mode": "REACTION_HIGH",
        "max_add_units": 1,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_stop_loss_plan_tab() -> Dict[str, Any]:
    """Render ABC stop loss plan tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_stop_loss_engine_v172 import (
        get_stop_loss_constants,
    )
    return {
        "constants": get_stop_loss_constants(),
        "a_stop_mode": "MA10_BREAK_REF",
        "b_stop_mode": "PLATFORM_LOWER",
        "c_stop_mode": "BELOW_MA20",
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_take_profit_plan_tab() -> Dict[str, Any]:
    """Render ABC take profit plan tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_take_profit_engine_v172 import (
        get_take_profit_constants,
    )
    return {
        "constants": get_take_profit_constants(),
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_position_sizing_tab() -> Dict[str, Any]:
    """Render ABC position sizing tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_position_sizing_bridge_v172 import (
        get_capital_constants,
    )
    return {
        "constants": get_capital_constants(),
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_forbidden_checks_tab() -> Dict[str, Any]:
    """Render ABC forbidden checks tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_forbidden_rule_bridge_v172 import (
        check_all_forbidden_rules, all_rules_passed, get_forbidden_rule_names,
    )
    results = check_all_forbidden_rules("_gui_sample_")
    return {
        "rule_names": get_forbidden_rule_names(),
        "all_passed": all_rules_passed(results),
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_paper_order_intent_tab() -> Dict[str, Any]:
    """Render ABC paper order intent tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_paper_order_intent_v172 import (
        get_paper_intent_actions,
    )
    return {
        "actions": get_paper_intent_actions(),
        "paper_only": True,
        "no_real_orders": True,
        "broker_execution_enabled": False,
        "not_investment_advice": True,
    }


def render_abc_scorecard_tab() -> Dict[str, Any]:
    """Render ABC scorecard tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_execution_scorecard_v172 import (
        get_scorecard_weights,
    )
    weights = get_scorecard_weights()
    return {
        "weights": weights,
        "grades": ["A", "B", "C", "D", "F", "BLOCKED"],
        "note": "No A+ grade. Max grade is A (85-100).",
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_report_tab() -> Dict[str, Any]:
    """Render ABC report tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_execution_report_v172 import (
        get_section_names,
    )
    return {
        "section_names": get_section_names(),
        "section_count": len(get_section_names()),
        "formats": ["MARKDOWN", "JSON", "CSV", "CONSOLE", "GUI"],
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_abc_health_tab() -> Dict[str, Any]:
    """Render ABC health check tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_execution_health_v172 import run_health_check
    health = run_health_check()
    return {
        "all_passed": health["all_passed"],
        "passed": health["passed"],
        "failed": health["failed"],
        "total": health["total"],
        "status": health["status"],
    }


def render_abc_gate_tab() -> Dict[str, Any]:
    """Render ABC release gate tab. v1.7.2."""
    from release.abc_buy_point_execution_plan_release_gate_v172 import run_release_gate
    gate = run_release_gate()
    return {
        "gate_passed": gate["gate_passed"],
        "passed": gate["passed"],
        "failed_count": gate["failed_count"],
        "total_count": gate["total_count"],
        "status": gate["status"],
    }


def render_abc_safety_tab() -> Dict[str, Any]:
    """Render ABC safety tab. v1.7.2."""
    from paper_trading.small_capital_strategy.abc_execution_safety_v172 import (
        get_abc_safety_flags, audit_abc_safety,
    )
    return {
        "flags": get_abc_safety_flags(),
        "audit": audit_abc_safety(),
    }


def get_abc_tab_names() -> List[str]:
    """Return list of v1.7.2 ABC execution tab names."""
    return list(_TABS_V172_ABC)


# ── v1.7.3 Market Regime Position Control render functions ──────────────────

def render_regime_overview_tab() -> Dict[str, Any]:
    """Render regime overview tab. v1.7.3."""
    return {
        "title": "Market Regime Position Control v1.7.3",
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "regimes": ["BULL", "RANGE", "BEAR", "RISK_OFF", "UNKNOWN"],
    }


def render_regime_detection_tab() -> Dict[str, Any]:
    """Render regime detection tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
    from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
    from paper_trading.small_capital_strategy.market_regime_detector_v173 import detect_market_regime
    inp = MarketRegimeInput()
    result = detect_market_regime(inp)
    return {
        "regime": result.regime.value,
        "status": result.status.value,
        "confidence": result.confidence,
        "paper_only": True,
        "no_real_orders": True,
    }


def render_regime_trend_filter_tab() -> Dict[str, Any]:
    """Render regime trend filter tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
    from paper_trading.small_capital_strategy.trend_filter_v173 import evaluate_trend_filter
    result = evaluate_trend_filter(MarketRegimeInput())
    return {
        "trend_signal": result.trend_signal.value,
        "trend_score": result.trend_score,
        "paper_only": True,
    }


def render_regime_volatility_filter_tab() -> Dict[str, Any]:
    """Render regime volatility filter tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
    from paper_trading.small_capital_strategy.volatility_filter_v173 import evaluate_volatility_filter
    result = evaluate_volatility_filter(MarketRegimeInput())
    return {
        "volatility_level": result.volatility_level.value,
        "volatility_score": result.volatility_score,
        "volatility_controlled": result.volatility_controlled,
        "paper_only": True,
    }


def render_regime_breadth_filter_tab() -> Dict[str, Any]:
    """Render regime breadth filter tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
    from paper_trading.small_capital_strategy.breadth_filter_v173 import evaluate_breadth_filter
    result = evaluate_breadth_filter(MarketRegimeInput())
    return {
        "breadth_signal": result.breadth_signal.value,
        "advance_decline_ratio": result.advance_decline_ratio,
        "breadth_healthy": result.breadth_healthy,
        "paper_only": True,
    }


def render_regime_risk_off_detection_tab() -> Dict[str, Any]:
    """Render regime risk-off detection tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_models_v173 import MarketRegimeInput
    from paper_trading.small_capital_strategy.risk_off_detector_v173 import detect_risk_off
    result = detect_risk_off(MarketRegimeInput())
    return {
        "risk_off_signal": result.risk_off_signal.value,
        "volatility_spike": result.volatility_spike,
        "risk_event_active": result.risk_event_active,
        "paper_only": True,
    }


def render_regime_cash_ratio_tab(regime_str: str = "BULL") -> Dict[str, Any]:
    """Render regime cash ratio tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
    from paper_trading.small_capital_strategy.cash_ratio_engine_v173 import build_cash_ratio_plan
    try:
        regime = MarketRegime[regime_str.upper()]
    except KeyError:
        regime = MarketRegime.UNKNOWN
    plan = build_cash_ratio_plan(regime)
    return {
        "regime": plan.regime.value,
        "cash_pct": plan.cash_pct,
        "total_pct": plan.total_pct,
        "allocation_valid": plan.allocation_valid,
        "paper_only": True,
        "no_real_orders": True,
    }


def render_regime_exposure_control_tab(regime_str: str = "BULL") -> Dict[str, Any]:
    """Render regime exposure control tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
    from paper_trading.small_capital_strategy.exposure_control_engine_v173 import build_exposure_control_plan
    try:
        regime = MarketRegime[regime_str.upper()]
    except KeyError:
        regime = MarketRegime.UNKNOWN
    plan = build_exposure_control_plan(regime)
    return {
        "regime": plan.regime.value,
        "max_total_exposure_pct": plan.max_total_exposure_pct,
        "max_single_position_pct": plan.max_single_position_pct,
        "margin_allowed": plan.margin_allowed,
        "leverage_allowed": plan.leverage_allowed,
        "paper_only": True,
    }


def render_regime_bucket_adjustment_tab(regime_str: str = "BULL") -> Dict[str, Any]:
    """Render regime bucket adjustment tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
    from paper_trading.small_capital_strategy.bucket_adjustment_engine_v173 import build_bucket_adjustment_plan
    try:
        regime = MarketRegime[regime_str.upper()]
    except KeyError:
        regime = MarketRegime.UNKNOWN
    plan = build_bucket_adjustment_plan(regime)
    return {
        "regime": plan.regime.value,
        "capital_twd": plan.capital_twd,
        "core_amount": plan.core_amount,
        "cash_amount": plan.cash_amount,
        "total_amount": plan.total_amount,
        "paper_only": True,
    }


def render_regime_candidate_permission_tab(regime_str: str = "BULL") -> Dict[str, Any]:
    """Render regime candidate permission tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
    from paper_trading.small_capital_strategy.candidate_permission_engine_v173 import get_candidate_permission
    try:
        regime = MarketRegime[regime_str.upper()]
    except KeyError:
        regime = MarketRegime.UNKNOWN
    perm = get_candidate_permission(regime, "CORE")
    return {
        "regime": perm.regime.value,
        "tier": perm.tier,
        "permission": perm.permission.value,
        "max_candidates": perm.max_candidates,
        "buy_points_allowed": perm.buy_points_allowed,
        "paper_only": True,
    }


def render_regime_abc_compatibility_tab(regime_str: str = "BULL") -> Dict[str, Any]:
    """Render regime ABC compatibility tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_enums_v173 import MarketRegime
    from paper_trading.small_capital_strategy.candidate_permission_engine_v173 import get_abc_regime_permission
    try:
        regime = MarketRegime[regime_str.upper()]
    except KeyError:
        regime = MarketRegime.UNKNOWN
    perm = get_abc_regime_permission(regime)
    return {
        "regime": perm.regime.value,
        "a_allowed": perm.a_allowed,
        "b_allowed": perm.b_allowed,
        "c_allowed": perm.c_allowed,
        "paper_only": True,
    }


def render_regime_scorecard_tab() -> Dict[str, Any]:
    """Render regime scorecard tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_scorecard_v173 import get_weight_table, WEIGHTS_SUM
    return {
        "weight_table": get_weight_table(),
        "weights_sum": WEIGHTS_SUM,
        "grade_thresholds": {"A": 85, "B": 70, "C": 55, "D": 40, "F": 0},
        "paper_only": True,
    }


def render_regime_report_tab() -> Dict[str, Any]:
    """Render regime report tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_report_v173 import get_section_names
    return {
        "section_count": 14,
        "section_names": get_section_names(),
        "paper_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
    }


def render_regime_health_gate_tab() -> Dict[str, Any]:
    """Render regime health and gate tab. v1.7.3."""
    from paper_trading.small_capital_strategy.market_regime_health_v173 import run_health_check
    health = run_health_check()
    return {
        "all_passed": health.all_passed,
        "passed": health.passed,
        "failed": health.failed,
        "total": health.total,
        "status": health.status,
        "paper_only": True,
    }


def get_regime_tab_names() -> List[str]:
    """Return list of v1.7.3 regime tab names."""
    return list(_TABS_V173_REGIME)


def render_all_tabs() -> Dict[str, Any]:
    """Render all tabs and return a dict of tab_name -> data."""
    renderers = {
        "overview": render_overview_tab,
        "version_info": render_version_info_tab,
        "safety": render_safety_tab,
        "capital_profile": render_capital_profile_tab,
        "risk_budget": render_risk_budget_tab,
        "allocation": render_allocation_tab,
        "market_regime": render_market_regime_tab,
        "watchlist": render_watchlist_tab,
        "theme_filter": render_theme_filter_tab,
        "buy_points_abc": render_buy_points_tab,
        "entry_plan": render_entry_plan_tab,
        "exit_plan": render_exit_plan_tab,
        "stop_loss": render_stop_loss_tab,
        "take_profit": render_take_profit_tab,
        "position_sizing": render_position_sizing_tab,
        "forbidden_checks": render_forbidden_checks_tab,
        "cash_control": render_cash_control_tab,
        "scorecard": render_scorecard_tab,
        "strategy_template": render_strategy_template_tab,
        "paper_simulation": render_paper_simulation_tab,
        "scenarios": render_scenarios_tab,
        "health_gate": render_health_gate_tab,
        # v1.7.1 watchlist tabs
        "watchlist_overview": render_watchlist_overview_tab,
        "watchlist_candidate_pool": render_watchlist_candidate_pool_tab,
        "watchlist_theme_rotation": render_watchlist_theme_rotation_tab,
        "watchlist_score_weights": render_watchlist_score_weights_tab,
        "watchlist_ranking": render_watchlist_ranking_tab,
        "watchlist_top_10_focus": render_watchlist_top_10_focus_tab,
        "watchlist_top_5_tradable": render_watchlist_top_5_tradable_tab,
        "watchlist_tier_classification": render_watchlist_tier_classification_tab,
        "watchlist_excluded": render_watchlist_excluded_tab,
        "watchlist_overdiversification": render_watchlist_overdiversification_tab,
        "watchlist_allocation_mapping": render_watchlist_allocation_mapping_tab,
        "watchlist_safety": render_watchlist_safety_tab,
        "watchlist_report": render_watchlist_report_tab,
        "watchlist_health": render_watchlist_health_tab,
        "watchlist_gate": render_watchlist_gate_tab,
        # v1.7.2 ABC execution tabs
        "abc_execution_overview": render_abc_execution_overview_tab,
        "abc_a_10ma_pullback": render_abc_a_10ma_pullback_tab,
        "abc_b_platform_breakout": render_abc_b_platform_breakout_tab,
        "abc_c_20ma_reclaim": render_abc_c_20ma_reclaim_tab,
        "abc_candidate_compatibility": render_abc_candidate_compatibility_tab,
        "abc_market_regime_compatibility": render_abc_market_regime_compatibility_tab,
        "abc_entry_plan": render_abc_entry_plan_tab,
        "abc_add_plan": render_abc_add_plan_tab,
        "abc_stop_loss_plan": render_abc_stop_loss_plan_tab,
        "abc_take_profit_plan": render_abc_take_profit_plan_tab,
        "abc_position_sizing": render_abc_position_sizing_tab,
        "abc_forbidden_checks": render_abc_forbidden_checks_tab,
        "abc_paper_order_intent": render_abc_paper_order_intent_tab,
        "abc_scorecard": render_abc_scorecard_tab,
        "abc_report": render_abc_report_tab,
        "abc_health": render_abc_health_tab,
        "abc_gate": render_abc_gate_tab,
        "abc_safety": render_abc_safety_tab,
        # v1.7.3 regime tabs
        "regime_overview": render_regime_overview_tab,
        "regime_detection": render_regime_detection_tab,
        "regime_trend_filter": render_regime_trend_filter_tab,
        "regime_volatility_filter": render_regime_volatility_filter_tab,
        "regime_breadth_filter": render_regime_breadth_filter_tab,
        "regime_risk_off_detection": render_regime_risk_off_detection_tab,
        "regime_cash_ratio": render_regime_cash_ratio_tab,
        "regime_exposure_control": render_regime_exposure_control_tab,
        "regime_bucket_adjustment": render_regime_bucket_adjustment_tab,
        "regime_candidate_permission": render_regime_candidate_permission_tab,
        "regime_abc_compatibility": render_regime_abc_compatibility_tab,
        "regime_scorecard": render_regime_scorecard_tab,
        "regime_report": render_regime_report_tab,
        "regime_health_gate": render_regime_health_gate_tab,
        # v1.7.4 risk dashboard tabs
        "risk_dashboard_overview": render_risk_dashboard_overview_tab,
        "risk_capital": render_risk_capital_tab,
        "risk_single_trade": render_risk_single_trade_tab,
        "risk_portfolio_exposure": render_risk_portfolio_exposure_tab,
        "risk_cash_ratio": render_risk_cash_ratio_tab,
        "risk_position_count": render_risk_position_count_tab,
        "risk_drawdown": render_risk_drawdown_tab,
        "risk_losing_streak": render_risk_losing_streak_tab,
        "risk_concentration": render_risk_concentration_tab,
        "risk_theme_exposure": render_risk_theme_exposure_tab,
        "risk_stop_loss_coverage": render_risk_stop_loss_coverage_tab,
        "risk_abc_risk": render_risk_abc_tab,
        "risk_watchlist_risk": render_risk_watchlist_tab,
        "risk_market_regime_risk": render_risk_market_regime_tab,
        "risk_scorecard": render_risk_scorecard_tab,
        # v1.7.5 trade journal tabs
        "trade_journal_overview":        render_trade_journal_overview_tab,
        "trade_journal_entry":           render_trade_journal_entry_tab,
        "trade_journal_review_entry":    render_trade_journal_review_entry_tab,
        "trade_journal_review_exit":     render_trade_journal_review_exit_tab,
        "trade_journal_abc_review":      render_trade_journal_abc_review_tab,
        "trade_journal_watchlist_review": render_trade_journal_watchlist_review_tab,
        "trade_journal_risk_review":     render_trade_journal_risk_review_tab,
        "trade_journal_regime_review":   render_trade_journal_regime_review_tab,
        "trade_journal_mistake_taxonomy": render_trade_journal_mistake_taxonomy_tab,
        "trade_journal_scorecard":       render_trade_journal_scorecard_tab,
        "trade_journal_report":          render_trade_journal_report_tab,
        "trade_journal_scenarios":       render_trade_journal_scenarios_tab,
        "trade_journal_health":          render_trade_journal_health_tab,
        "trade_journal_gate":            render_trade_journal_gate_tab,
        # v1.7.6 mistake taxonomy tabs
        "mistake_review_overview":       render_mistake_review_overview_tab,
        "mistake_taxonomy_classify":     render_mistake_review_overview_tab,
        "mistake_taxonomy_cost":         render_mistake_review_overview_tab,
        "mistake_taxonomy_repeat":       render_mistake_review_overview_tab,
        "weekly_review":                 render_mistake_review_overview_tab,
        "monthly_review":                render_mistake_review_overview_tab,
        "behavior_risk_score":           render_behavior_risk_score_tab,
        "behavior_risk_actions":         render_behavior_risk_score_tab,
        "review_dashboard":              render_mistake_review_overview_tab,
        "review_report":                 render_mistake_review_overview_tab,
        "review_scenarios":              render_mistake_review_overview_tab,
        "review_health":                 render_review_health_tab,
        "review_gate":                   render_review_gate_tab,
        # v1.7.7 theme rotation tabs
        "theme_rotation":                render_theme_rotation_tab,
        "theme_ranking":                 render_theme_ranking_tab,
        "theme_watchlist":               render_theme_watchlist_tab,
        # v1.7.8 integrated strategy tabs
        "integrated_strategy":               render_integrated_strategy_tab,
        "integrated_decision_dashboard":     render_integrated_decision_dashboard_tab,
        "integrated_paper_plan":             render_integrated_paper_plan_tab,
        # v1.7.9 stable rollup tabs
        "stable_rollup":                     render_stable_rollup_tab,
        "stable_health":                     render_stable_health_tab,
        "stable_report":                     render_stable_report_tab,
        # v1.8.0 paper simulation tabs
        "paper_sim_lab":                     render_paper_sim_lab_tab,
        "paper_sim_equity_curve":            render_paper_sim_equity_curve_tab,
        "paper_sim_performance":             render_paper_sim_performance_tab,
        # v1.8.1 simulation scenario matrix tabs
        "sim_matrix_lab":                    render_sim_matrix_lab_tab,
        "sim_stress_test":                   render_sim_stress_test_tab,
        "sim_robustness_score":              render_sim_robustness_score_tab,
        # v1.8.2 optimization tabs
        "param_optimization":                render_param_optimization_tab,
        "walk_forward_validation":           render_walk_forward_validation_tab,
        "overfitting_risk":                  render_overfitting_risk_tab,
        # v1.8.3 Monte Carlo tabs
        "monte_carlo":                       render_monte_carlo_tab,
        "risk_of_ruin":                      render_risk_of_ruin_tab,
        "robustness_probability":            render_robustness_probability_tab,
        # v1.8.4 Position Sizing tabs
        "position_sizing_lab":               render_position_sizing_tab,
        "risk_budget_allocation":            render_risk_budget_allocation_tab,
        "capital_allocation":               render_capital_allocation_tab,
        # v1.8.5 Portfolio Construction tabs
        "portfolio_construction_lab":        render_portfolio_construction_lab_tab,
        "portfolio_rebalancing":             render_portfolio_rebalancing_tab,
        "portfolio_exposure_control":        render_portfolio_exposure_control_tab,
        # v1.8.6 Decision Cockpit tabs
        "daily_decision_cockpit":            render_daily_decision_cockpit_tab,
        "weekly_decision_review":            render_weekly_decision_review_tab,
        "block_reasons":                     render_block_reasons_tab,
        # v1.8.7 Decision Report Export & Evidence Pack tabs
        "decision_report":                   render_decision_report_tab,
        "evidence_pack":                     render_evidence_pack_tab,
        "audit_trail_report":                render_audit_trail_report_tab,
        # v1.8.8 Paper Decision Workflow Runner tabs
        "decision_workflow":                 render_decision_workflow_tab,
        "daily_workflow":                    render_daily_workflow_tab,
        "weekly_workflow":                   render_weekly_workflow_tab,
        # v1.8.9 Paper Decision Journal tabs
        "decision_journal":                  render_decision_journal_tab,
        "daily_review":                      render_daily_review_tab,
    }
    result = {}
    for tab_name in _TABS:
        try:
            result[tab_name] = renderers[tab_name]()
        except Exception as exc:
            result[tab_name] = {"error": str(exc)}
    return result


def render_risk_dashboard_overview_tab() -> Dict[str, Any]:
    """Render Risk Dashboard Overview tab. v1.7.4."""
    return {
        "title": "Small Account Risk Dashboard v1.7.4",
        "version": "1.7.4",
        "release_name": "Small Account Risk Dashboard",
        "base_release": "1.7.3 Market Regime Position Control",
        "capital_twd": 300_000,
        "tab_count": len(_TABS_V174_RISK_DASHBOARD),
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
    }


def render_risk_capital_tab() -> Dict[str, Any]:
    """Render capital risk tab. v1.7.4."""
    from paper_trading.small_capital_strategy.single_trade_risk_monitor_v174 import get_single_trade_risk_thresholds
    return {
        "capital_twd": 300_000,
        "max_single_trade_loss_twd": 3000,
        "max_holdings": 4,
        "thresholds": get_single_trade_risk_thresholds(),
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_single_trade_tab(
    position_size_amount: float = 50000.0,
    stop_loss_pct: float = 0.05,
    has_stop_loss: bool = True,
) -> Dict[str, Any]:
    """Render single trade risk tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.single_trade_risk_monitor_v174 import evaluate_single_trade_risk
    inp = SmallAccountRiskInput(
        position_size_amount=position_size_amount,
        stop_loss_pct=stop_loss_pct,
        has_stop_loss=has_stop_loss,
    )
    result = evaluate_single_trade_risk(inp)
    return {
        "status": result.status.value,
        "loss_amount": result.single_trade_loss_amount,
        "risk_pct": result.risk_pct,
        "has_stop_loss": result.has_stop_loss,
        "block_reasons": [r.value for r in result.block_reasons],
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_portfolio_exposure_tab(
    market_regime: str = "BULL",
    invested_pct: float = 30.0,
    cash_pct: float = 70.0,
) -> Dict[str, Any]:
    """Render portfolio exposure tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.portfolio_exposure_monitor_v174 import evaluate_portfolio_exposure
    inp = SmallAccountRiskInput(
        market_regime=market_regime,
        total_invested_pct=invested_pct,
        cash_pct=cash_pct,
    )
    result = evaluate_portfolio_exposure(inp)
    return {
        "status": result.status.value,
        "invested_pct": result.invested_pct,
        "cash_pct": result.cash_pct,
        "max_invested_pct": result.max_invested_pct,
        "min_cash_pct": result.min_cash_pct,
        "regime": result.market_regime,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_cash_ratio_tab(
    market_regime: str = "BULL",
    cash_pct: float = 70.0,
) -> Dict[str, Any]:
    """Render cash ratio risk tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.cash_ratio_risk_monitor_v174 import evaluate_cash_ratio
    inp = SmallAccountRiskInput(market_regime=market_regime, cash_pct=cash_pct)
    result = evaluate_cash_ratio(inp)
    return {
        "status": result.status.value,
        "cash_pct": result.cash_pct,
        "min_cash_pct": result.min_cash_pct,
        "regime": result.market_regime,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_position_count_tab(holdings_count: int = 2) -> Dict[str, Any]:
    """Render position count tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.position_count_monitor_v174 import evaluate_position_count
    inp = SmallAccountRiskInput(holdings_count=holdings_count)
    result = evaluate_position_count(inp)
    return {
        "status": result.status.value,
        "holdings_count": result.holdings_count,
        "max_holdings": result.max_holdings,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_drawdown_tab(drawdown_pct: float = 2.0) -> Dict[str, Any]:
    """Render drawdown risk tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.drawdown_monitor_v174 import evaluate_drawdown
    inp = SmallAccountRiskInput(current_drawdown_pct=drawdown_pct)
    result = evaluate_drawdown(inp)
    return {
        "status": result.status.value,
        "drawdown_pct": result.drawdown_pct,
        "level": result.level.value,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_losing_streak_tab(losing_streak_count: int = 0) -> Dict[str, Any]:
    """Render losing streak tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.losing_streak_monitor_v174 import evaluate_losing_streak
    inp = SmallAccountRiskInput(losing_streak_count=losing_streak_count)
    result = evaluate_losing_streak(inp)
    return {
        "status": result.status.value,
        "losing_streak_count": result.losing_streak_count,
        "level": result.level.value,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_concentration_tab(
    single_position_pct: float = 20.0,
    sector_pct: float = 40.0,
) -> Dict[str, Any]:
    """Render concentration risk tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.concentration_risk_monitor_v174 import evaluate_concentration_risk
    inp = SmallAccountRiskInput(
        max_single_position_pct=single_position_pct,
        sector_exposure_pct=sector_pct,
    )
    result = evaluate_concentration_risk(inp)
    return {
        "status": result.status.value,
        "single_position_pct": result.max_single_position_pct,
        "sector_pct": result.sector_exposure_pct,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_theme_exposure_tab(
    theme_pct: float = 30.0,
    training_amount: float = 5000.0,
) -> Dict[str, Any]:
    """Render theme exposure tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.theme_exposure_monitor_v174 import evaluate_theme_exposure
    inp = SmallAccountRiskInput(
        theme_exposure_pct=theme_pct,
        short_term_training_amount=training_amount,
    )
    result = evaluate_theme_exposure(inp)
    return {
        "status": result.status.value,
        "theme_pct": result.theme_exposure_pct,
        "training_amount": result.training_amount,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_stop_loss_coverage_tab(
    has_stop_loss: bool = True,
    stop_loss_pct: float = 0.05,
) -> Dict[str, Any]:
    """Render stop loss coverage tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.stop_loss_coverage_monitor_v174 import evaluate_stop_loss_coverage
    inp = SmallAccountRiskInput(has_stop_loss=has_stop_loss, stop_loss_pct=stop_loss_pct)
    result = evaluate_stop_loss_coverage(inp)
    return {
        "status": result.status.value,
        "all_covered": result.all_positions_covered,
        "missing_count": result.missing_stop_loss_count,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_abc_tab(abc_plan_blocked: bool = False) -> Dict[str, Any]:
    """Render ABC risk tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.abc_execution_risk_adapter_v174 import evaluate_abc_execution_risk
    inp = SmallAccountRiskInput(abc_plan_blocked=abc_plan_blocked)
    result = evaluate_abc_execution_risk(inp)
    return {
        "status": result["status"],
        "abc_plan_blocked": abc_plan_blocked,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_watchlist_tab(candidate_excluded: bool = False) -> Dict[str, Any]:
    """Render watchlist risk tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.watchlist_risk_adapter_v174 import evaluate_watchlist_risk
    inp = SmallAccountRiskInput(watchlist_candidate_excluded=candidate_excluded)
    result = evaluate_watchlist_risk(inp)
    return {
        "status": result["status"],
        "candidate_excluded": candidate_excluded,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_market_regime_tab(
    market_regime: str = "BULL",
    cash_pct: float = 70.0,
) -> Dict[str, Any]:
    """Render market regime risk tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
    from paper_trading.small_capital_strategy.market_regime_risk_adapter_v174 import evaluate_market_regime_risk
    inp = SmallAccountRiskInput(market_regime=market_regime, cash_pct=cash_pct)
    result = evaluate_market_regime_risk(inp)
    return {
        "status": result["status"],
        "regime": market_regime,
        "cash_pct": cash_pct,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_risk_scorecard_tab() -> Dict[str, Any]:
    """Render risk scorecard tab. v1.7.4. Headless-safe."""
    from paper_trading.small_capital_strategy.small_capital_risk_adapter_v174 import (
        build_risk_dashboard, get_default_pass_input,
    )
    from paper_trading.small_capital_strategy.risk_dashboard_scorecard_v174 import (
        compute_scorecard, get_weight_table,
    )
    dashboard = build_risk_dashboard(get_default_pass_input())
    scorecard = compute_scorecard(dashboard)
    return {
        "total_score": scorecard.total_score,
        "grade": scorecard.grade.value,
        "weights": get_weight_table(),
        "paper_only": True,
        "not_investment_advice": True,
    }


def get_risk_dashboard_tab_names() -> List[str]:
    """Return list of v1.7.4 risk dashboard tab names."""
    return list(_TABS_V174_RISK_DASHBOARD)


def get_trade_journal_tab_names() -> List[str]:
    """Return list of v1.7.5 trade journal tab names."""
    return list(_TABS_V175_TRADE_JOURNAL)


# ---------------------------------------------------------------------------
# v1.7.5 Trade Journal tab renderers
# ---------------------------------------------------------------------------

def render_trade_journal_overview_tab() -> Dict[str, Any]:
    """Render Trade Journal Overview tab. v1.7.5."""
    from paper_trading.small_capital_strategy.version_v175 import get_version_info
    info = get_version_info()
    return {
        "title":          "Small Account Trade Journal v1.7.5",
        "version":        "1.7.5",
        "release_name":   "Small Account Trade Journal",
        "base_release":   "1.7.4 Small Account Risk Dashboard",
        "tab_count":      len(_TABS_V175_TRADE_JOURNAL),
        "paper_only":     True,
        "research_only":  True,
        "no_real_orders": True,
        "no_broker":      True,
        "not_investment_advice": True,
        "version_info":   info,
    }


def render_trade_journal_entry_tab() -> Dict[str, Any]:
    """Render Trade Journal Entry tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection, ABCPattern
    from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry, validate_entry
    sample = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                  580.0, 50000.0, 552.0, 0.05, ABCPattern.B_BREAKOUT, "BULL", 1)
    return {
        "sample_entry_symbol":   sample.symbol,
        "sample_entry_valid":    validate_entry(sample),
        "paper_only":            sample.paper_only,
        "no_real_orders":        sample.no_real_orders,
        "not_investment_advice": True,
    }


def render_trade_journal_review_entry_tab() -> Dict[str, Any]:
    """Render Trade Journal Review Entry tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection, ABCPattern
    from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry
    from paper_trading.small_capital_strategy.trade_journal_review_entry_v175 import review_entry, score_entry
    from paper_trading.small_capital_strategy.trade_journal_models_v175 import TradeDecisionSnapshot
    entry = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                 580.0, 50000.0, 552.0, 0.05, ABCPattern.B_BREAKOUT, "BULL", 1)
    snap  = TradeDecisionSnapshot(entry_trigger="B_BREAKOUT", market_regime="BULL",
                                  stop_loss_pct=0.05, position_size_twd=50000.0, watchlist_tier=1)
    result = review_entry(entry, snap)
    return {
        "entry_quality":  result.entry_quality.value,
        "entry_score":    result.entry_score,
        "review_status":  result.review_status.value,
        "paper_only":     result.paper_only,
        "not_investment_advice": True,
    }


def render_trade_journal_review_exit_tab() -> Dict[str, Any]:
    """Render Trade Journal Review Exit tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection
    from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry, close_journal_entry
    from paper_trading.small_capital_strategy.trade_journal_review_exit_v175 import review_exit
    entry  = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05", 580.0, 50000.0, 552.0, 0.05)
    closed = close_journal_entry(entry, "2026-01-20", 638.0)
    result = review_exit(closed)
    return {
        "exit_quality":  result.exit_quality.value,
        "exit_score":    result.exit_score,
        "review_status": result.review_status.value,
        "paper_only":    result.paper_only,
        "not_investment_advice": True,
    }


def render_trade_journal_abc_review_tab() -> Dict[str, Any]:
    """Render Trade Journal ABC Review tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection, ABCPattern
    from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry
    from paper_trading.small_capital_strategy.trade_journal_abc_review_v175 import review_abc_execution
    from paper_trading.small_capital_strategy.trade_journal_models_v175 import TradeDecisionSnapshot
    entry = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                 580.0, 50000.0, 552.0, 0.05, ABCPattern.C_RECLAIM, "BULL", 1)
    snap  = TradeDecisionSnapshot(stop_loss_pct=0.05, position_size_twd=50000.0)
    result = review_abc_execution(entry, snap)
    return {
        "abc_pattern":     result.abc_pattern.value,
        "execution_score": result.execution_score,
        "review_status":   result.review_status.value,
        "paper_only":      result.paper_only,
        "not_investment_advice": True,
    }


def render_trade_journal_watchlist_review_tab() -> Dict[str, Any]:
    """Render Trade Journal Watchlist Review tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_watchlist_review_v175 import (
        review_watchlist_conversion, calculate_conversion_rate,
    )
    result = review_watchlist_conversion("2330", 1, True, "", 5, 3, 4)
    return {
        "symbol":             result.symbol,
        "watchlist_tier":     result.watchlist_tier,
        "converted":          result.converted_to_trade,
        "conversion_score":   result.conversion_score,
        "conversion_rate_pct": calculate_conversion_rate(5, 3, 4),
        "paper_only":         result.paper_only,
        "not_investment_advice": True,
    }


def render_trade_journal_risk_review_tab() -> Dict[str, Any]:
    """Render Trade Journal Risk Review tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection, ABCPattern
    from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry
    from paper_trading.small_capital_strategy.trade_journal_risk_review_v175 import review_risk_violations
    entry  = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                  580.0, 50000.0, 552.0, 0.05, ABCPattern.B_BREAKOUT, "BULL", 1)
    result = review_risk_violations(entry)
    return {
        "violation_type":  result.violation_type,
        "severity":        result.severity,
        "review_status":   result.review_status.value,
        "paper_only":      result.paper_only,
        "not_investment_advice": True,
    }


def render_trade_journal_regime_review_tab() -> Dict[str, Any]:
    """Render Trade Journal Regime Review tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection, ABCPattern
    from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry, close_journal_entry
    from paper_trading.small_capital_strategy.trade_journal_regime_review_v175 import review_regime_outcome
    e1 = close_journal_entry(
        create_journal_entry("2330", TradeDirection.LONG, "2026-01-05", 580.0, 50000.0, 552.0, 0.05,
                             ABCPattern.B_BREAKOUT, "BULL", 1), "2026-01-20", 638.0)
    result = review_regime_outcome("BULL", [e1])
    return {
        "regime":          result.regime,
        "trade_count":     result.trade_count,
        "win_rate_pct":    result.win_rate_pct,
        "review_status":   result.review_status.value,
        "paper_only":      result.paper_only,
        "not_investment_advice": True,
    }


def render_trade_journal_mistake_taxonomy_tab() -> Dict[str, Any]:
    """Render Trade Journal Mistake Taxonomy tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection, ABCPattern
    from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry
    from paper_trading.small_capital_strategy.trade_journal_mistake_taxonomy_v175 import classify_mistakes
    entry  = create_journal_entry("2330", TradeDirection.LONG, "2026-01-05",
                                  580.0, 50000.0, 552.0, 0.05, ABCPattern.B_BREAKOUT, "BULL", 1)
    result = classify_mistakes(entry)
    return {
        "primary_mistake":  result.primary_mistake.value,
        "severity_score":   result.severity_score,
        "corrective_action": result.corrective_action,
        "review_status":    result.review_status.value,
        "paper_only":       result.paper_only,
        "not_investment_advice": True,
    }


def render_trade_journal_scorecard_tab() -> Dict[str, Any]:
    """Render Trade Journal Scorecard tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection
    from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry, close_journal_entry
    from paper_trading.small_capital_strategy.trade_journal_scorecard_v175 import build_scorecard, get_weight_table
    e1 = close_journal_entry(
        create_journal_entry("2330", TradeDirection.LONG, "2026-01-05", 580.0, 50000.0, 552.0, 0.05),
        "2026-01-20", 638.0)
    sc = build_scorecard([e1])
    return {
        "total_score":  sc.total_score,
        "grade":        sc.grade,
        "win_rate_pct": sc.win_rate_pct,
        "weights":      get_weight_table(),
        "paper_only":   sc.paper_only,
        "not_investment_advice": True,
    }


def render_trade_journal_report_tab() -> Dict[str, Any]:
    """Render Trade Journal Report tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_enums_v175 import TradeDirection
    from paper_trading.small_capital_strategy.trade_journal_entry_v175 import create_journal_entry, close_journal_entry
    from paper_trading.small_capital_strategy.trade_journal_dashboard_v175 import build_dashboard
    from paper_trading.small_capital_strategy.trade_journal_report_v175 import build_report, get_report_sections
    e1 = close_journal_entry(
        create_journal_entry("2330", TradeDirection.LONG, "2026-01-05", 580.0, 50000.0, 552.0, 0.05),
        "2026-01-20", 638.0)
    dash   = build_dashboard([e1])
    report = build_report(dash)
    return {
        "sections_count": len(report.sections),
        "section_names":  get_report_sections(),
        "paper_only":     report.paper_only,
        "not_investment_advice": True,
    }


def render_trade_journal_scenarios_tab() -> Dict[str, Any]:
    """Render Trade Journal Scenarios tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_scenarios_v175 import (
        get_scenarios, count_scenarios,
    )
    return {
        "scenario_count": count_scenarios(),
        "all_paper_only": all(s["paper_only"] for s in get_scenarios()),
        "paper_only":     True,
        "not_investment_advice": True,
    }


def render_trade_journal_health_tab() -> Dict[str, Any]:
    """Render Trade Journal Health tab. v1.7.5."""
    from paper_trading.small_capital_strategy.trade_journal_health_v175 import run_health_check
    result = run_health_check()
    return {
        "all_passed": result.all_passed,
        "passed":     result.passed,
        "failed":     result.failed,
        "total":      result.total,
        "status":     result.status,
        "paper_only": result.paper_only,
        "not_investment_advice": True,
    }


def render_trade_journal_gate_tab() -> Dict[str, Any]:
    """Render Trade Journal Gate tab. v1.7.5."""
    from release.small_account_trade_journal_release_gate_v175 import run_gate
    result = run_gate()
    return {
        "gate_passed": result["gate_passed"],
        "passed":      result["passed"],
        "failed":      result["failed"],
        "total":       result["total"],
        "paper_only":  True,
        "not_investment_advice": True,
    }


def render_mistake_review_overview_tab() -> Dict[str, Any]:
    """Render Mistake Review Overview tab. v1.7.6."""
    from paper_trading.small_capital_strategy.version_v176 import get_version_info
    info = get_version_info()
    return {
        "version": info["version"],
        "release_name": info["release_name"],
        "paper_only": True,
        "not_investment_advice": True,
        "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
    }


def render_behavior_risk_score_tab() -> Dict[str, Any]:
    """Render Behavior Risk Score tab. v1.7.6."""
    from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import MistakeCategory
    from paper_trading.small_capital_strategy.mistake_taxonomy_classifier_v176 import classify_event
    from paper_trading.small_capital_strategy.mistake_taxonomy_repeat_v176 import detect_repeated_patterns
    from paper_trading.small_capital_strategy.mistake_taxonomy_behavior_score_v176 import compute_behavior_score
    events = [classify_event("2330", "2026-01-05", MistakeCategory.FOMO_CHASE, -2000.0)]
    patterns = detect_repeated_patterns(events)
    score = compute_behavior_score(events, patterns, 3)
    return {
        "score": score.score,
        "level": score.level.value,
        "description": score.description,
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_review_health_tab() -> Dict[str, Any]:
    """Render Review Health tab. v1.7.6."""
    from paper_trading.small_capital_strategy.mistake_taxonomy_health_v176 import run_health_check
    result = run_health_check()
    return {
        "all_passed": result.all_passed,
        "passed":     result.passed,
        "failed":     result.failed,
        "total":      result.total,
        "status":     result.status,
        "paper_only": result.paper_only,
        "not_investment_advice": True,
    }


def render_review_gate_tab() -> Dict[str, Any]:
    """Render Review Gate tab. v1.7.6."""
    from release.mistake_taxonomy_weekly_review_release_gate_v176 import run_gate
    result = run_gate()
    return {
        "gate_passed": result["gate_passed"],
        "passed":      result["passed"],
        "failed":      result["failed"],
        "total":       result["total"],
        "paper_only":  True,
        "not_investment_advice": True,
    }


def get_mistake_taxonomy_tab_names() -> List[str]:
    """Return v1.7.6 mistake taxonomy tab names."""
    return list(_TABS_V176_MISTAKE_TAXONOMY)


def render_theme_rotation_tab() -> Dict[str, Any]:
    """Render Theme Rotation tab. v1.7.7."""
    from paper_trading.small_capital_strategy.version_v177 import get_version_info
    info = get_version_info()
    return {
        "version": info["version"],
        "release_name": info["release_name"],
        "paper_only": True,
        "not_investment_advice": True,
        "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
    }


def render_theme_ranking_tab() -> Dict[str, Any]:
    """Render Theme Ranking tab. v1.7.7."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory
    from paper_trading.small_capital_strategy.theme_rotation_models_v177 import ThemeStrengthScore, ThemeGrade
    from paper_trading.small_capital_strategy.theme_rotation_rank_v177 import rank_themes
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeGrade as TGrade
    ss_list = [
        ThemeStrengthScore(theme=ThemeCategory.AI_SERVER, score=88.0, grade=TGrade.LEADER),
        ThemeStrengthScore(theme=ThemeCategory.SEMICONDUCTOR, score=72.0, grade=TGrade.STRONG),
    ]
    ranks = rank_themes(ss_list)
    return {
        "rank_count": len(ranks),
        "top_theme": ranks[0].theme.value if ranks else "UNKNOWN",
        "paper_only": True,
        "not_investment_advice": True,
    }


def render_theme_watchlist_tab() -> Dict[str, Any]:
    """Render Theme Watchlist tab. v1.7.7."""
    from paper_trading.small_capital_strategy.theme_rotation_enums_v177 import ThemeCategory, ThemeGrade
    from paper_trading.small_capital_strategy.theme_rotation_watchlist_v177 import (
        build_watchlist_candidate, filter_eligible_candidates,
    )
    candidates = [
        build_watchlist_candidate("2330", ThemeCategory.SEMICONDUCTOR, ThemeGrade.LEADER, "Leader stock"),
        build_watchlist_candidate("2317", ThemeCategory.AI_SERVER, ThemeGrade.WATCH, "Watch only"),
    ]
    eligible = filter_eligible_candidates(candidates)
    return {
        "candidate_count": len(candidates),
        "eligible_count":  len(eligible),
        "paper_only":      True,
        "not_investment_advice": True,
    }


def get_theme_rotation_tab_names() -> List[str]:
    """Return v1.7.7 theme rotation tab names."""
    return list(_TABS_V177_THEME_ROTATION)


def get_integrated_strategy_tab_names() -> List[str]:
    """Return v1.7.8 integrated strategy tab names."""
    return list(_TABS_V178_INTEGRATED_STRATEGY)


def render_integrated_strategy_tab(
    symbol: str = "",
    date: str = "",
) -> Dict[str, Any]:
    """
    Render integrated strategy tab. Paper/research only.
    Headless-safe. Empty state handled. Malformed input does not crash.
    """
    try:
        from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
            IntegratedRegimeStatus, IntegratedWatchlistStatus, IntegratedABCStatus,
            IntegratedThemeStatus, IntegratedRiskLevel, IntegratedBehaviorStatus,
        )
        from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
            IntegratedStrategyInput,
        )
        from paper_trading.small_capital_strategy.integrated_strategy_engine_v178 import (
            run_integrated_strategy,
        )
        inp = IntegratedStrategyInput(
            symbol=symbol or "",
            date=date or "",
            has_stop_loss=False,
        )
        decision = run_integrated_strategy(inp)
        return {
            "tab": "integrated_strategy",
            "symbol": symbol,
            "date": date,
            "action": decision.action.value,
            "final_score": decision.final_score,
            "grade": decision.grade.value,
            "no_trade_reasons": [r.value for r in decision.no_trade_reasons],
            "block_reasons": [b.value for b in decision.block_reasons],
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
        }
    except Exception as exc:
        return {
            "tab": "integrated_strategy",
            "symbol": symbol,
            "date": date,
            "action": "OBSERVE",
            "error": str(exc),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def render_integrated_decision_dashboard_tab(
    symbol: str = "",
    date: str = "",
) -> Dict[str, Any]:
    """
    Render integrated decision dashboard tab. Paper/research only.
    Headless-safe. Empty state handled. No broker. No live session.
    """
    try:
        from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
            IntegratedStrategyInput,
        )
        from paper_trading.small_capital_strategy.integrated_strategy_engine_v178 import (
            build_integrated_dashboard,
        )
        inp = IntegratedStrategyInput(symbol=symbol or "", date=date or "")
        dashboard = build_integrated_dashboard(inp)
        return {
            "tab": "integrated_decision_dashboard",
            "symbol": symbol,
            "date": date,
            "action": (dashboard.decision.action.value if dashboard.decision else "OBSERVE"),
            "final_score": (dashboard.decision.final_score if dashboard.decision else 0.0),
            "sections_count": len(dashboard.sections),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
        }
    except Exception as exc:
        return {
            "tab": "integrated_decision_dashboard",
            "symbol": symbol,
            "date": date,
            "action": "OBSERVE",
            "error": str(exc),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def render_integrated_paper_plan_tab(
    symbol: str = "",
    date: str = "",
) -> Dict[str, Any]:
    """
    Render integrated paper plan tab. Paper/research only.
    Headless-safe. No real orders. No broker execution.
    """
    try:
        from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
            IntegratedStrategyInput,
        )
        from paper_trading.small_capital_strategy.integrated_strategy_engine_v178 import (
            run_integrated_strategy,
        )
        from paper_trading.small_capital_strategy.integrated_strategy_paper_plan_v178 import (
            build_paper_plan,
        )
        inp = IntegratedStrategyInput(symbol=symbol or "", date=date or "")
        decision = run_integrated_strategy(inp)
        plan = build_paper_plan(inp, decision)
        return {
            "tab": "integrated_paper_plan",
            "symbol": symbol,
            "date": date,
            "plan_valid": plan.plan_valid,
            "buy_point_type": plan.buy_point_type,
            "broker_execution_enabled": False,
            "no_real_orders": True,
            "paper_only": True,
            "research_only": True,
            "not_investment_advice": True,
        }
    except Exception as exc:
        return {
            "tab": "integrated_paper_plan",
            "symbol": symbol,
            "date": date,
            "plan_valid": False,
            "error": str(exc),
            "broker_execution_enabled": False,
            "no_real_orders": True,
            "paper_only": True,
            "research_only": True,
            "not_investment_advice": True,
        }


def render_stable_rollup_tab() -> Dict[str, Any]:
    """Render Stable Rollup overview tab. v1.7.9."""
    return {
        "tab": "stable_rollup",
        "title": "Small Capital Strategy Stable Rollup v1.7.9",
        "version": "1.7.9",
        "release_name": "Small Capital Strategy Stable Rollup",
        "base_release": "1.7.8 Small Capital Strategy Integration",
        "included_releases": 9,
        "schema_version": "179",
        "policy_version": "1.7.9-small-capital-strategy-stable-rollup",
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
    }


def render_stable_health_tab() -> Dict[str, Any]:
    """Render Stable Health check tab. v1.7.9. Headless-safe. Does not call run_health_check to avoid circular dependency."""
    return {
        "tab": "stable_health",
        "title": "Stable Rollup Health v1.7.9",
        "description": "Run 'small-capital-stable-health' CLI command for full health check.",
        "version": "1.7.9",
        "status": "READY",
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
    }


def render_stable_report_tab() -> Dict[str, Any]:
    """Render Stable Report summary tab. v1.7.9."""
    return {
        "tab": "stable_report",
        "title": "Stable Rollup Report v1.7.9",
        "version": "1.7.9",
        "release_name": "Small Capital Strategy Stable Rollup",
        "report_sections": 11,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "demo_only": True,
        "not_for_production": True,
        "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
    }


def get_stable_rollup_tab_names() -> List[str]:
    """Return list of v1.7.9 stable rollup tab names."""
    return list(_TABS_V179_STABLE_ROLLUP)


# ---------------------------------------------------------------------------
# v1.8.0 Paper Simulation & Performance Lab tab renderers
# Headless-safe. No broker. No real orders. No production DB writes.
# ---------------------------------------------------------------------------

def render_paper_sim_lab_tab() -> Dict[str, Any]:
    """Render Paper Simulation Lab tab. v1.8.0. Headless-safe."""
    try:
        from paper_trading.small_capital_strategy.paper_simulation_version_v180 import (
            VERSION, RELEASE_NAME, get_version_info,
        )
        from paper_trading.small_capital_strategy.paper_simulation_scenarios_v180 import (
            get_scenario_count, get_scenario_categories,
        )
        version_info = get_version_info()
        return {
            "tab": "paper_sim_lab",
            "title": "Paper Simulation Lab v1.8.0",
            "version": VERSION,
            "release_name": RELEASE_NAME,
            "description": "Paper-only simulation engine for 300K small capital strategy research.",
            "scenario_count": get_scenario_count(),
            "categories": get_scenario_categories(),
            "status": "READY",
            "paper_only": version_info["paper_only"],
            "research_only": version_info["research_only"],
            "no_real_orders": version_info["no_real_orders"],
            "no_broker": True,
            "not_investment_advice": version_info["not_investment_advice"],
            "demo_only": version_info["demo_only"],
            "not_for_production": version_info["not_for_production"],
            "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
        }
    except Exception as exc:
        return {
            "tab": "paper_sim_lab",
            "title": "Paper Simulation Lab v1.8.0",
            "status": "EMPTY",
            "error": str(exc),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def render_paper_sim_equity_curve_tab() -> Dict[str, Any]:
    """Render Paper Simulation Equity Curve tab. v1.8.0. Headless-safe."""
    try:
        from paper_trading.small_capital_strategy.paper_simulation_models_v180 import (
            PaperSimulationInput,
        )
        from paper_trading.small_capital_strategy.paper_simulation_engine_v180 import (
            run_paper_simulation,
        )
        from paper_trading.small_capital_strategy.paper_simulation_metrics_v180 import (
            compute_equity_curve,
        )
        inp = PaperSimulationInput()
        result = run_paper_simulation(inp)
        curve = compute_equity_curve(result.trades, inp.initial_capital)
        return {
            "tab": "paper_sim_equity_curve",
            "title": "Paper Simulation Equity Curve v1.8.0",
            "version": "1.8.0",
            "point_count": len(curve.values),
            "initial_capital": inp.initial_capital,
            "final_value": curve.values[-1] if curve.values else inp.initial_capital,
            "max_drawdown_pct": max(curve.drawdowns) if curve.drawdowns else 0.0,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
            "demo_only": True,
            "not_for_production": True,
        }
    except Exception as exc:
        return {
            "tab": "paper_sim_equity_curve",
            "title": "Paper Simulation Equity Curve v1.8.0",
            "status": "EMPTY",
            "error": str(exc),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def render_paper_sim_performance_tab() -> Dict[str, Any]:
    """Render Paper Simulation Performance Lab tab. v1.8.0. Headless-safe."""
    try:
        from paper_trading.small_capital_strategy.paper_simulation_models_v180 import (
            PaperSimulationInput,
        )
        from paper_trading.small_capital_strategy.paper_simulation_engine_v180 import (
            run_paper_simulation,
        )
        from paper_trading.small_capital_strategy.paper_simulation_metrics_v180 import (
            compute_metrics,
        )
        inp = PaperSimulationInput()
        result = run_paper_simulation(inp)
        metrics = compute_metrics(result.trades, inp.initial_capital)
        return {
            "tab": "paper_sim_performance",
            "title": "Paper Simulation Performance Lab v1.8.0",
            "version": "1.8.0",
            "trade_count": metrics.trade_count,
            "total_return_pct": metrics.total_return_pct,
            "win_rate_pct": metrics.win_rate_pct,
            "max_drawdown_pct": metrics.max_drawdown_pct,
            "profit_factor": metrics.profit_factor,
            "expectancy_r": metrics.expectancy_r,
            "final_grade": metrics.final_grade,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "not_investment_advice": True,
            "demo_only": True,
            "not_for_production": True,
            "disclaimer": "Research Only | Paper Only | No Real Orders | Not Investment Advice",
        }
    except Exception as exc:
        return {
            "tab": "paper_sim_performance",
            "title": "Paper Simulation Performance Lab v1.8.0",
            "status": "EMPTY",
            "error": str(exc),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def get_paper_sim_tab_names() -> List[str]:
    """Return list of v1.8.0 paper simulation tab names."""
    return list(_TABS_V180_PAPER_SIM)


# ---------------------------------------------------------------------------
# v1.8.1 Simulation Scenario Matrix & Stress Test Lab tab renderers
# Headless-safe. No broker. No real orders. Stress test only. Research only.
# ---------------------------------------------------------------------------

def render_sim_matrix_lab_tab() -> Dict[str, Any]:
    """Render Simulation Matrix Lab tab. v1.8.1. Headless-safe."""
    try:
        from paper_trading.small_capital_strategy.simulation_matrix_version_v181 import (
            VERSION, RELEASE_NAME, get_version_info,
        )
        from paper_trading.small_capital_strategy.simulation_matrix_scenarios_v181 import (
            get_scenario_count, get_scenario_categories,
        )
        version_info = get_version_info()
        return {
            "tab": "sim_matrix_lab",
            "title": "Simulation Scenario Matrix Lab v1.8.1",
            "version": VERSION,
            "release_name": RELEASE_NAME,
            "description": "Scenario matrix across 10 dimensions for 300K paper strategy research.",
            "scenario_count": get_scenario_count(),
            "categories": get_scenario_categories(),
            "status": "READY",
            "paper_only": version_info["paper_only"],
            "research_only": version_info["research_only"],
            "simulate_only": version_info["simulate_only"],
            "stress_test_only": version_info["stress_test_only"],
            "no_real_orders": version_info["no_real_orders"],
            "no_broker": True,
            "not_investment_advice": version_info["not_investment_advice"],
            "disclaimer": "Research Only | Paper Only | Stress Test Only | No Real Orders | Not Investment Advice",
        }
    except Exception as exc:
        return {
            "tab": "sim_matrix_lab",
            "title": "Simulation Scenario Matrix Lab v1.8.1",
            "status": "EMPTY",
            "error": str(exc),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def render_sim_stress_test_tab() -> Dict[str, Any]:
    """Render Simulation Stress Test tab. v1.8.1. Headless-safe."""
    try:
        from paper_trading.small_capital_strategy.simulation_stress_engine_v181 import (
            STRESS_TEST_TYPES, run_all_stress_tests, get_stress_engine_info,
        )
        results = run_all_stress_tests()
        survived = sum(1 for r in results if r.survived)
        info = get_stress_engine_info()
        return {
            "tab": "sim_stress_test",
            "title": "Simulation Stress Test Lab v1.8.1",
            "version": "1.8.1",
            "stress_test_count": len(results),
            "survived_count": survived,
            "failed_count": len(results) - survived,
            "stress_test_types": STRESS_TEST_TYPES,
            "paper_only": info["paper_only"],
            "research_only": info["research_only"],
            "simulate_only": info["simulate_only"],
            "stress_test_only": info["stress_test_only"],
            "no_real_orders": info["no_real_orders"],
            "no_broker": True,
            "not_investment_advice": info["not_investment_advice"],
            "disclaimer": "Research Only | Paper Only | Stress Test Only | No Real Orders | Not Investment Advice",
        }
    except Exception as exc:
        return {
            "tab": "sim_stress_test",
            "title": "Simulation Stress Test Lab v1.8.1",
            "status": "EMPTY",
            "error": str(exc),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def render_sim_robustness_score_tab() -> Dict[str, Any]:
    """Render Simulation Robustness Score tab. v1.8.1. Headless-safe."""
    try:
        from paper_trading.small_capital_strategy.simulation_matrix_models_v181 import (
            SimulationMatrixInput,
        )
        from paper_trading.small_capital_strategy.simulation_matrix_engine_v181 import (
            run_matrix_cell, compute_robustness_score, run_scenario_matrix,
        )
        from paper_trading.small_capital_strategy.simulation_stress_engine_v181 import (
            run_all_stress_tests,
        )
        inp = SimulationMatrixInput()
        matrix_result = run_scenario_matrix([inp])
        stress_results = run_all_stress_tests()
        robustness = compute_robustness_score(matrix_result, stress_results)
        return {
            "tab": "sim_robustness_score",
            "title": "Simulation Robustness Score v1.8.1",
            "version": "1.8.1",
            "score": robustness.score,
            "final_grade": robustness.final_grade,
            "stress_survival_rate_pct": robustness.stress_survival_rate_pct,
            "scenario_pass_rate_pct": robustness.scenario_pass_rate_pct,
            "average_max_drawdown_pct": robustness.average_max_drawdown_pct,
            "worst_case_return_pct": robustness.worst_case_return_pct,
            "behavior_resilience_score": robustness.behavior_resilience_score,
            "paper_only": robustness.paper_only,
            "research_only": robustness.research_only,
            "simulate_only": robustness.simulate_only,
            "stress_test_only": robustness.stress_test_only,
            "no_real_orders": robustness.no_real_orders,
            "no_broker": True,
            "not_investment_advice": robustness.not_investment_advice,
            "disclaimer": "Research Only | Paper Only | Stress Test Only | No Real Orders | Not Investment Advice",
        }
    except Exception as exc:
        return {
            "tab": "sim_robustness_score",
            "title": "Simulation Robustness Score v1.8.1",
            "status": "EMPTY",
            "error": str(exc),
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def get_sim_matrix_tab_names() -> List[str]:
    """Return list of v1.8.1 simulation matrix tab names."""
    return list(_TABS_V181_SIM_MATRIX)


def render_param_optimization_tab() -> Dict[str, Any]:
    """Render parameter optimization tab. v1.8.2."""
    from paper_trading.small_capital_strategy.optimization_version_v182 import get_version_info
    from paper_trading.small_capital_strategy.optimization_engine_v182 import get_engine_info
    info = get_version_info()
    engine = get_engine_info()
    return {
        "tab": "param_optimization",
        "title": "Parameter Optimization Lab v1.8.2",
        "version": "1.8.2",
        "paper_only": True,
        "research_only": True,
        "validation_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "stress_test_only": True,
        "no_broker": True,
        "parameter_dimensions": 12,
        "allowed_actions_count": len(engine["allowed_output_actions"]),
        "headless_safe": True,
    }


def render_walk_forward_validation_tab() -> Dict[str, Any]:
    """Render walk-forward validation tab. v1.8.2."""
    from paper_trading.small_capital_strategy.optimization_walk_forward_v182 import get_walk_forward_info
    info = get_walk_forward_info()
    return {
        "tab": "walk_forward_validation",
        "title": "Walk-Forward Validation Lab v1.8.2",
        "version": "1.8.2",
        "paper_only": True,
        "research_only": True,
        "validation_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "stress_test_only": True,
        "no_broker": True,
        "walk_forward_types_count": info["count"],
        "headless_safe": True,
    }


def render_overfitting_risk_tab() -> Dict[str, Any]:
    """Render overfitting risk dashboard tab. v1.8.2."""
    from paper_trading.small_capital_strategy.optimization_report_v182 import build_dashboard_report
    from paper_trading.small_capital_strategy.optimization_engine_v182 import run_parameter_search
    from paper_trading.small_capital_strategy.optimization_models_v182 import ParameterGrid, OptimizationConfig
    grid = ParameterGrid()
    config = OptimizationConfig()
    result = run_parameter_search(grid, config)
    dashboard = build_dashboard_report(result)
    return {
        "tab": "overfitting_risk",
        "title": "Overfitting Risk Dashboard v1.8.2",
        "version": "1.8.2",
        "paper_only": True,
        "research_only": True,
        "validation_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "stress_test_only": True,
        "no_broker": True,
        "final_grade": dashboard.final_grade,
        "overfitting_risk_score": dashboard.overfitting_risk_score,
        "walk_forward_pass_rate_pct": dashboard.walk_forward_pass_rate_pct,
        "headless_safe": True,
    }


def get_optimization_tab_names() -> List[str]:
    """Return list of v1.8.2 optimization tab names."""
    return list(_TABS_V182_OPTIMIZATION)


def get_monte_carlo_tab_names() -> List[str]:
    """Return list of v1.8.3 Monte Carlo tab names."""
    return list(_TABS_V183_MONTE_CARLO)


def render_monte_carlo_tab() -> Dict[str, Any]:
    """Render v1.8.3 Monte Carlo tab. Headless-safe."""
    return {
        "tab": "monte_carlo",
        "version": "1.8.3",
        "paper_only": True,
        "monte_carlo_only": True,
        "no_real_orders": True,
        "headless_safe": True,
        "trial_counts": [100, 500, 1000, 5000],
        "deterministic_seed": True,
    }


def render_risk_of_ruin_tab() -> Dict[str, Any]:
    """Render v1.8.3 Risk-of-Ruin tab. Headless-safe."""
    return {
        "tab": "risk_of_ruin",
        "version": "1.8.3",
        "paper_only": True,
        "monte_carlo_only": True,
        "no_real_orders": True,
        "headless_safe": True,
        "capital_floor_options": [50, 60, 70],
        "max_drawdown_limit_options": [10, 15, 20, 25],
    }


def render_robustness_probability_tab() -> Dict[str, Any]:
    """Render v1.8.3 Robustness Probability tab. Headless-safe."""
    return {
        "tab": "robustness_probability",
        "version": "1.8.3",
        "paper_only": True,
        "monte_carlo_only": True,
        "no_real_orders": True,
        "headless_safe": True,
        "bootstrap_enabled": True,
    }


def get_position_sizing_tab_names() -> List[str]:
    """Return list of v1.8.4 position sizing tab names."""
    return list(_TABS_V184_POSITION_SIZING)


def render_position_sizing_tab() -> Dict[str, Any]:
    """Render v1.8.4 Position Sizing tab. Headless-safe."""
    return {
        "tab": "position_sizing",
        "version": "1.8.4",
        "paper_only": True,
        "allocation_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "no_margin": True,
        "no_leverage": True,
        "headless_safe": True,
        "capital_stages": [300000, 500000, 1000000, 3000000],
        "sizing_methods": 10,
    }


def render_risk_budget_allocation_tab() -> Dict[str, Any]:
    """Render v1.8.4 Risk Budget Allocation tab. Headless-safe."""
    return {
        "tab": "risk_budget_allocation",
        "version": "1.8.4",
        "paper_only": True,
        "allocation_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "headless_safe": True,
        "per_trade_risk_options": [0.5, 0.8, 1.0, 1.5, 2.0],
        "max_drawdown_options": [10, 15, 20, 25],
    }


def render_capital_allocation_tab() -> Dict[str, Any]:
    """Render v1.8.4 Capital Allocation tab. Headless-safe."""
    return {
        "tab": "capital_allocation",
        "version": "1.8.4",
        "paper_only": True,
        "allocation_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "headless_safe": True,
        "abc_buy_points": ["A_10MA_PULLBACK", "B_BREAKOUT", "C_20MA_RECLAIM"],
        "final_grades": ["SAFE", "ACCEPTABLE", "CAUTION", "HIGH_RISK", "BLOCKED"],
    }


def render_portfolio_construction_lab_tab() -> Dict[str, Any]:
    """Render v1.8.5 Portfolio Construction Lab tab. Headless-safe."""
    return {
        "tab": "portfolio_construction_lab",
        "version": "1.8.5",
        "paper_only": True,
        "research_only": True,
        "portfolio_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "headless_safe": True,
        "capital_stages": [300000, 500000, 1000000, 3000000],
        "weighting_methods": [
            "equal_weight", "risk_budget_weight", "conviction_weight",
            "volatility_adjusted_weight", "monte_carlo_ruin_risk_adjusted_weight",
        ],
        "final_grades": ["BALANCED", "ACCEPTABLE", "CONCENTRATED", "OVEREXPOSED", "HIGH_RISK", "BLOCKED"],
    }


def render_portfolio_rebalancing_tab() -> Dict[str, Any]:
    """Render v1.8.5 Portfolio Rebalancing tab. Headless-safe."""
    return {
        "tab": "portfolio_rebalancing",
        "version": "1.8.5",
        "paper_only": True,
        "research_only": True,
        "portfolio_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "headless_safe": True,
        "rebalance_thresholds": [5, 10, 15],
        "actions": ["OBSERVE", "REVIEW_REQUIRED", "REDUCE_RISK", "PORTFOLIO_ONLY"],
    }


def render_portfolio_exposure_control_tab() -> Dict[str, Any]:
    """Render v1.8.5 Portfolio Exposure Control tab. Headless-safe."""
    return {
        "tab": "portfolio_exposure_control",
        "version": "1.8.5",
        "paper_only": True,
        "research_only": True,
        "portfolio_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "headless_safe": True,
        "max_total_exposure_options": [40, 50, 60, 70, 80],
        "max_sector_exposure_options": [25, 35, 45],
        "max_theme_exposure_options": [30, 40, 50],
        "min_cash_reserve_options": [10, 20, 30, 50],
    }


def get_portfolio_construction_tab_names() -> List[str]:
    """Return list of v1.8.5 portfolio construction tab names."""
    return list(_TABS_V185_PORTFOLIO_CONSTRUCTION)


def get_portfolio_construction_tab_names_v187() -> List[str]:
    """Return list of v1.8.7 decision report tab names."""
    return list(_TABS_V187_DECISION_REPORT)


def render_decision_report_tab() -> Dict[str, Any]:
    """Render decision report tab data (headless-safe, report-only)."""
    return {
        "tab": "decision_report",
        "version": PANEL_VERSION,
        "release_name": "Decision Report Export & Evidence Pack",
        "description": "Daily/weekly decision reports: JSON, Markdown, CSV-like rows, console summary, dashboard payload.",
        "paper_only": True,
        "research_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No decision report data available. Run decision-report-run to populate.",
        "schema_version": "187",
    }


def render_evidence_pack_tab() -> Dict[str, Any]:
    """Render evidence pack tab data (headless-safe, report-only)."""
    return {
        "tab": "evidence_pack",
        "version": PANEL_VERSION,
        "release_name": "Decision Report Export & Evidence Pack",
        "description": "Candidate evidence pack: traceable decision evidence for all candidates.",
        "paper_only": True,
        "research_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No evidence pack data available. Run decision-report-evidence to populate.",
        "schema_version": "187",
    }


def render_audit_trail_report_tab() -> Dict[str, Any]:
    """Render audit trail report tab data (headless-safe, audit-only)."""
    return {
        "tab": "audit_trail_report",
        "version": PANEL_VERSION,
        "release_name": "Decision Report Export & Evidence Pack",
        "description": "Audit trail: traceable decision audit log for all decisions.",
        "paper_only": True,
        "research_only": True,
        "report_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No audit trail data available. Run decision-report-audit-trail to populate.",
        "schema_version": "187",
    }


def get_decision_workflow_tab_names() -> List[str]:
    """Return list of v1.8.8 decision workflow tab names."""
    return list(_TABS_V188_DECISION_WORKFLOW)


def render_decision_workflow_tab() -> Dict[str, Any]:
    """Render decision workflow tab data (headless-safe, workflow-only)."""
    return {
        "tab": "decision_workflow",
        "version": PANEL_VERSION,
        "release_name": "Paper Decision Workflow Runner",
        "description": "Paper-only deterministic decision workflow runner: daily and weekly workflow orchestration.",
        "paper_only": True,
        "research_only": True,
        "workflow_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No workflow data available. Run decision-workflow-run to populate.",
        "schema_version": "188",
    }


def render_daily_workflow_tab() -> Dict[str, Any]:
    """Render daily workflow tab data (headless-safe, workflow-only)."""
    return {
        "tab": "daily_workflow",
        "version": PANEL_VERSION,
        "release_name": "Paper Decision Workflow Runner",
        "description": "Daily paper-only workflow: regime, candidates, A/B/C, risk, portfolio, Monte Carlo, report.",
        "paper_only": True,
        "research_only": True,
        "workflow_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No daily workflow data available. Run decision-workflow-daily to populate.",
        "schema_version": "188",
    }


def render_weekly_workflow_tab() -> Dict[str, Any]:
    """Render weekly workflow tab data (headless-safe, workflow-only)."""
    return {
        "tab": "weekly_workflow",
        "version": PANEL_VERSION,
        "release_name": "Paper Decision Workflow Runner",
        "description": "Weekly paper-only workflow: portfolio review, exposure, regime, risk, rebalance decisions.",
        "paper_only": True,
        "research_only": True,
        "workflow_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No weekly workflow data available. Run decision-workflow-weekly to populate.",
        "schema_version": "188",
    }


def get_decision_journal_tab_names() -> List[str]:
    """Return list of v1.8.9 decision journal tab names."""
    return list(_TABS_V189_DECISION_JOURNAL)


def render_decision_journal_tab() -> Dict[str, Any]:
    """Render decision journal tab data (headless-safe, journal-only)."""
    return {
        "tab": "decision_journal",
        "version": PANEL_VERSION,
        "release_name": "Paper Decision Journal & Review Loop",
        "description": "Paper-only decision journal: record, review and audit all paper decisions.",
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "review_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No journal data available. Run decision-journal-create to populate.",
        "schema_version": "189",
    }


def render_daily_review_tab() -> Dict[str, Any]:
    """Render daily review tab data (headless-safe, review-only)."""
    return {
        "tab": "daily_review",
        "version": PANEL_VERSION,
        "release_name": "Paper Decision Journal & Review Loop",
        "description": "Daily paper decision review: score all 20 dimensions and tag mistakes.",
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "review_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No daily review data available. Run decision-journal-daily-review to populate.",
        "schema_version": "189",
    }


def render_weekly_review_v189_tab() -> Dict[str, Any]:
    """Render weekly review tab data (headless-safe, review-only)."""
    return {
        "tab": "weekly_review",
        "version": PANEL_VERSION,
        "release_name": "Paper Decision Journal & Review Loop",
        "description": "Weekly paper decision review: aggregate findings, recurring mistakes, action items.",
        "paper_only": True,
        "research_only": True,
        "journal_only": True,
        "review_only": True,
        "audit_only": True,
        "no_real_orders": True,
        "no_broker": True,
        "not_investment_advice": True,
        "production_trading_blocked": True,
        "empty_state": "No weekly review data available. Run decision-journal-weekly-review to populate.",
        "schema_version": "189",
    }


def get_panel_info() -> Dict[str, Any]:
    """Return panel metadata."""
    return {
        "panel_version": PANEL_VERSION,
        "panel_title": PANEL_TITLE,
        "tab_count": len(_TABS),
        "tabs": _TABS,
        "paper_only": True,
        "research_only": True,
        "no_real_orders": True,
        "not_investment_advice": True,
        "headless_safe": True,
    }
