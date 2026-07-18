"""
release/abc_buy_point_execution_plan_release_gate_v172.py
Release gate for A/B/C Buy Point Execution Plan v1.7.2.
70+ gate checks. gate_passed=True required.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

GATE_VERSION = "1.7.2"
MIN_CHECKS   = 70


class ABCBuyPointExecutionPlanReleaseGate:
    """Release gate for A/B/C Buy Point Execution Plan v1.7.2."""

    def __init__(self) -> None:
        self._checks: List[Dict[str, Any]] = []

    def _check(self, name: str, fn) -> None:
        try:
            result = fn()
            ok = bool(result)
        except Exception as exc:
            ok = False
            result = str(exc)
        self._checks.append({
            "name": name,
            "passed": ok,
            "detail": str(result) if not ok else "OK",
        })

    def run(self) -> Dict[str, Any]:
        """Run all gate checks and return result dict."""
        self._checks = []

        # ── Health PASS ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_execution_health_v172 import (
            run_health_check,
        )
        health = run_health_check()
        self._check("health_all_passed",
                    lambda: run_health_check()["all_passed"] is True)
        self._check("health_status_pass",
                    lambda: run_health_check()["status"] == "PASS")
        self._check("health_failed_zero",
                    lambda: run_health_check()["failed"] == 0)
        self._check("health_total_ge_75",
                    lambda: run_health_check()["total"] >= 75)

        # ── Version Identity ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v172 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION,
            COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
            get_version_info, is_known_release,
        )
        self._check("gate_version_1_7_2", lambda: VERSION == "1.7.2")
        self._check("gate_release_name",
                    lambda: RELEASE_NAME == "A/B/C Buy Point Execution Plan")
        self._check("gate_base_release",
                    lambda: BASE_RELEASE == "1.7.1 Watchlist Strategy Layer")
        self._check("gate_schema_version_172", lambda: SCHEMA_VERSION == "172")
        self._check("gate_component_count_24", lambda: COMPONENT_COUNT >= 24)
        self._check("gate_min_scenarios_70", lambda: MIN_SCENARIOS >= 70)
        self._check("gate_min_fixtures_70", lambda: MIN_FIXTURES >= 70)
        self._check("gate_min_cli_20", lambda: MIN_CLI >= 20)
        self._check("gate_min_health_75", lambda: MIN_HEALTH >= 75)
        self._check("gate_min_gate_70", lambda: MIN_GATE >= 70)
        self._check("gate_known_release_self",
                    lambda: is_known_release("A/B/C Buy Point Execution Plan"))
        self._check("gate_known_release_v171",
                    lambda: is_known_release("Watchlist Strategy Layer"))
        self._check("gate_version_info_dict",
                    lambda: isinstance(get_version_info(), dict))

        # ── Safety ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_execution_safety_v172 import (
            audit_abc_safety,
            ABC_REAL_TRADING_ENABLED, ABC_REAL_ORDER_ENABLED,
            ABC_BROKER_EXECUTION_ENABLED, ABC_AUTO_ORDER_ENABLED,
            NO_REAL_ORDERS, PRODUCTION_TRADING_BLOCKED,
        )
        self._check("safety_all_safe",
                    lambda: audit_abc_safety()["all_safe"] is True)
        self._check("safety_capabilities_zero",
                    lambda: audit_abc_safety()["safety_capabilities"] == 0)
        self._check("no_real_trading",
                    lambda: ABC_REAL_TRADING_ENABLED is False)
        self._check("no_real_order",
                    lambda: ABC_REAL_ORDER_ENABLED is False)
        self._check("no_broker",
                    lambda: ABC_BROKER_EXECUTION_ENABLED is False)
        self._check("no_auto_order",
                    lambda: ABC_AUTO_ORDER_ENABLED is False)
        self._check("no_real_orders_flag",
                    lambda: NO_REAL_ORDERS is True)
        self._check("production_trading_blocked",
                    lambda: PRODUCTION_TRADING_BLOCKED is True)

        # ── A Rules ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
            ABCBuyPointType,
        )
        from paper_trading.small_capital_strategy.abc_condition_checker_v172 import (
            get_condition_names,
        )
        a_names = get_condition_names(ABCBuyPointType.A_10MA_PULLBACK)
        self._check("a_rules_nonempty", lambda: len(a_names) >= 8)
        self._check("a_rule_ma20", lambda: "close_above_ma20" in a_names)
        self._check("a_rule_ma60", lambda: "close_above_ma60" in a_names)
        self._check("a_rule_theme", lambda: "theme_strength_strong_or_leading" in a_names)
        self._check("a_rule_financing", lambda: "financing_not_overheated" in a_names)
        self._check("a_rule_institutional", lambda: "institutional_not_selling" in a_names)

        # ── B Rules ────────────────────────────────────────────────────────
        b_names = get_condition_names(ABCBuyPointType.B_PLATFORM_BREAKOUT)
        self._check("b_rules_nonempty", lambda: len(b_names) >= 4)
        self._check("b_rule_volume", lambda: "volume_confirmed" in b_names)
        self._check("b_rule_regime", lambda: "regime_not_bear" in b_names)
        self._check("b_rule_breakout", lambda: "close_above_prior_platform_high" in b_names)

        # ── C Rules ────────────────────────────────────────────────────────
        c_names = get_condition_names(ABCBuyPointType.C_20MA_RECLAIM)
        self._check("c_rules_nonempty", lambda: len(c_names) >= 6)
        self._check("c_rule_first_wave", lambda: "had_first_wave" in c_names)
        self._check("c_rule_ma20", lambda: "close_above_ma20" in c_names)
        self._check("c_rule_regime", lambda: "regime_not_risk_off" in c_names)

        # ── Entry Plan ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_entry_price_engine_v172 import (
            build_entry_plan,
        )
        self._check("entry_plan_callable", lambda: callable(build_entry_plan))

        # ── Add Plan ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_add_price_engine_v172 import (
            build_add_plan,
        )
        self._check("add_plan_callable", lambda: callable(build_add_plan))

        # ── Stop Loss ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_stop_loss_engine_v172 import (
            build_stop_loss_plan, validate_stop_loss,
        )
        self._check("stop_loss_callable", lambda: callable(build_stop_loss_plan))
        self._check("stop_loss_validation_callable", lambda: callable(validate_stop_loss))
        self._check("stop_loss_valid_check",
                    lambda: validate_stop_loss(90.0, 100.0) is True)
        self._check("stop_loss_invalid_above_entry",
                    lambda: validate_stop_loss(110.0, 100.0) is False)

        # ── Take Profit ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_take_profit_engine_v172 import (
            build_take_profit_plan, get_take_profit_constants,
        )
        self._check("take_profit_callable", lambda: callable(build_take_profit_plan))
        self._check("take_profit_partial_pct",
                    lambda: get_take_profit_constants()["partial_pct_low"] == 0.10)

        # ── Invalidation ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_invalidation_engine_v172 import (
            build_invalidation_plan, get_invalidation_bars,
        )
        self._check("invalidation_callable", lambda: callable(build_invalidation_plan))
        self._check("invalidation_bars_c_3",
                    lambda: get_invalidation_bars(ABCBuyPointType.C_20MA_RECLAIM) == 3)

        # ── Position Sizing ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_position_sizing_bridge_v172 import (
            get_capital_constants, CAPITAL_300K, MAX_HOLDINGS, TRAINING_MAX_AMOUNT,
        )
        self._check("capital_300k_correct", lambda: CAPITAL_300K == 300_000.0)
        self._check("max_holdings_4", lambda: MAX_HOLDINGS == 4)
        self._check("training_max_15000", lambda: TRAINING_MAX_AMOUNT == 15_000.0)

        # ── Watchlist Integration ──────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_watchlist_bridge_v172 import (
            get_tier_allowed_buy_points, get_tier_preferred_buy_points,
        )
        self._check("watchlist_excluded_blocked",
                    lambda: get_tier_allowed_buy_points("EXCLUDED") == [])
        self._check("watchlist_main_theme_allows_abc",
                    lambda: len(get_tier_allowed_buy_points("MAIN_THEME")) == 3)
        self._check("watchlist_second_wave_prefers_c",
                    lambda: ABCBuyPointType.C_20MA_RECLAIM in get_tier_preferred_buy_points("SECOND_WAVE"))

        # ── Market Regime Integration ──────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_market_regime_bridge_v172 import (
            get_compatible_regimes,
        )
        self._check("b_not_bear_compatible",
                    lambda: "BEAR" not in get_compatible_regimes(ABCBuyPointType.B_PLATFORM_BREAKOUT))
        self._check("a_bear_compatible",
                    lambda: "BEAR" in get_compatible_regimes(ABCBuyPointType.A_10MA_PULLBACK))

        # ── Forbidden Checks ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_forbidden_rule_bridge_v172 import (
            check_all_forbidden_rules, all_rules_passed, get_forbidden_rule_names,
        )
        self._check("forbidden_rules_8",
                    lambda: len(get_forbidden_rule_names()) >= 8)
        self._check("forbidden_rules_default_pass",
                    lambda: all_rules_passed(check_all_forbidden_rules("TEST")))

        # ── Paper Order Intent ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_paper_order_intent_v172 import (
            get_paper_intent_actions,
        )
        self._check("paper_intent_has_buy",
                    lambda: "PAPER_BUY" in get_paper_intent_actions())
        self._check("paper_intent_has_block",
                    lambda: "PAPER_BLOCK" in get_paper_intent_actions())
        self._check("paper_intent_has_wait",
                    lambda: "PAPER_WAIT" in get_paper_intent_actions())

        # ── Report ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_execution_report_v172 import (
            get_section_names,
        )
        self._check("report_sections_16",
                    lambda: len(get_section_names()) == 16)
        self._check("report_has_safety",
                    lambda: "safety" in get_section_names())
        self._check("report_has_nia",
                    lambda: "not_investment_advice" in get_section_names())

        # ── Scenario Coverage ──────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_scenario_registry_v172 import (
            get_scenario_count,
        )
        self._check("scenario_count_ge_70", lambda: get_scenario_count() >= 70)

        # ── Fixture Coverage ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_fixture_registry_v172 import (
            get_fixture_count, validate_registry,
        )
        self._check("fixture_count_ge_70", lambda: get_fixture_count() >= 70)
        self._check("fixtures_valid", lambda: validate_registry()["valid"] is True)

        # ── Scorecard ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_execution_scorecard_v172 import (
            get_scorecard_weights,
        )
        from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
            ABCExecutionGrade,
        )
        self._check("scorecard_weights_100",
                    lambda: get_scorecard_weights()["sum"] == 100)
        self._check("scorecard_no_a_plus",
                    lambda: not hasattr(ABCExecutionGrade, "A_PLUS"))

        # ── GUI Headless ───────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import (
            get_panel_info, get_tab_names, PANEL_VERSION,
        )
        self._check("gui_panel_version_172",
                    lambda: PANEL_VERSION in ("1.7.2", "1.7.3", "1.7.4", "1.7.5", "1.7.6", "1.7.7", "1.7.8", "1.7.9", "1.8.0", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4"))
        self._check("gui_has_abc_tabs",
                    lambda: any("abc" in t for t in get_tab_names()))
        self._check("gui_panel_info_dict",
                    lambda: isinstance(get_panel_info(), dict))
        self._check("gui_headless_safe",
                    lambda: get_panel_info().get("headless_safe") is True)

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        gate_passed = failed == 0

        return {
            "version": "1.7.2",
            "release_name": "A/B/C Buy Point Execution Plan",
            "gate_passed": gate_passed,
            "passed": passed,
            "failed_count": failed,
            "total_count": len(self._checks),
            "status": "PASS" if gate_passed else "FAIL",
            "checks": self._checks,
        }


def run_release_gate() -> Dict[str, Any]:
    """Run ABC execution plan release gate. Returns result dict."""
    return ABCBuyPointExecutionPlanReleaseGate().run()
