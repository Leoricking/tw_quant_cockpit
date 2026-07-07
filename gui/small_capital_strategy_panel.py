"""
gui/small_capital_strategy_panel.py
GUI panel for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
Headless-safe: no tkinter at module level. Renders to dict.
22 tabs.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

PANEL_VERSION = "1.7.0"
PANEL_TITLE = "Small Capital Growth Strategy Template v1.7.0"

_TABS = [
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

assert len(_TABS) == 22, f"Expected 22 tabs, got {len(_TABS)}"


def get_tab_names() -> List[str]:
    """Return list of tab names."""
    return list(_TABS)


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
    }
    result = {}
    for tab_name in _TABS:
        try:
            result[tab_name] = renderers[tab_name]()
        except Exception as exc:
            result[tab_name] = {"error": str(exc)}
    return result


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
