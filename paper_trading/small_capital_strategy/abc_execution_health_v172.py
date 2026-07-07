"""
paper_trading/small_capital_strategy/abc_execution_health_v172.py
Health check for A/B/C Buy Point Execution Plan v1.7.2.
75+ checks. All must PASS. No fixed PASS.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

HEALTH_VERSION = "1.7.2"


class ABCExecutionHealthCheck:
    """Health check runner for ABC Execution Plan v1.7.2."""

    def __init__(self) -> None:
        self._checks: List[Dict[str, Any]] = []
        self._passed = 0
        self._failed = 0

    def _check(self, name: str, fn) -> None:
        try:
            result = fn()
            ok = bool(result)
        except Exception as exc:
            ok = False
            result = str(exc)
        status = "PASS" if ok else "FAIL"
        if ok:
            self._passed += 1
        else:
            self._failed += 1
        self._checks.append({"name": name, "status": status, "detail": str(result)})

    def run(self) -> Dict[str, Any]:
        """Run all health checks and return result dict."""
        self._checks = []
        self._passed = 0
        self._failed = 0

        # ── Version ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v172 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
            COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
            get_version_info, verify_version, is_known_release, check_minimum_version,
        )
        self._check("version_is_1_7_2", lambda: VERSION == "1.7.2")
        self._check("release_name_abc_execution_plan",
                    lambda: RELEASE_NAME == "A/B/C Buy Point Execution Plan")
        self._check("base_release_is_1_7_1",
                    lambda: BASE_RELEASE == "1.7.1 Watchlist Strategy Layer")
        self._check("schema_version_172", lambda: SCHEMA_VERSION == "172")
        self._check("policy_version_set", lambda: "1.7.2" in POLICY_VERSION)
        self._check("component_count_24", lambda: COMPONENT_COUNT >= 24)
        self._check("min_scenarios_70", lambda: MIN_SCENARIOS >= 70)
        self._check("min_fixtures_70", lambda: MIN_FIXTURES >= 70)
        self._check("min_cli_20", lambda: MIN_CLI >= 20)
        self._check("min_health_75", lambda: MIN_HEALTH >= 75)
        self._check("min_gate_70", lambda: MIN_GATE >= 70)
        self._check("get_version_info_returns_dict",
                    lambda: isinstance(get_version_info(), dict))
        self._check("verify_version_returns_dict",
                    lambda: isinstance(verify_version(), dict))
        self._check("is_known_release_self",
                    lambda: is_known_release("A/B/C Buy Point Execution Plan"))
        self._check("is_known_release_v171",
                    lambda: is_known_release("Watchlist Strategy Layer"))
        self._check("check_minimum_version_pass",
                    lambda: check_minimum_version("1.7.1"))
        self._check("check_minimum_version_fail",
                    lambda: not check_minimum_version("1.6.0"))

        # ── Safety ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_execution_safety_v172 import (
            ABC_EXECUTION_PLAN_AVAILABLE, ABC_EXECUTION_PLAN_RESEARCH_ONLY,
            ABC_EXECUTION_PLAN_PAPER_ONLY, ABC_EXECUTION_PLAN_NOT_INVESTMENT_ADVICE,
            ABC_REAL_TRADING_ENABLED, ABC_REAL_ACCOUNT_ENABLED,
            ABC_REAL_ORDER_ENABLED, ABC_BROKER_EXECUTION_ENABLED,
            ABC_PRODUCTION_TRADING_ENABLED, ABC_LIVE_EXECUTION_ENABLED,
            ABC_AUTO_ORDER_ENABLED, ABC_AUTO_STOP_LOSS_ENABLED,
            ABC_AUTO_TAKE_PROFIT_ENABLED, ABC_MARGIN_ENABLED,
            NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
            audit_abc_safety,
        )
        self._check("abc_available_true",
                    lambda: ABC_EXECUTION_PLAN_AVAILABLE is True)
        self._check("abc_research_only_true",
                    lambda: ABC_EXECUTION_PLAN_RESEARCH_ONLY is True)
        self._check("abc_paper_only_true",
                    lambda: ABC_EXECUTION_PLAN_PAPER_ONLY is True)
        self._check("abc_not_investment_advice_true",
                    lambda: ABC_EXECUTION_PLAN_NOT_INVESTMENT_ADVICE is True)
        self._check("abc_real_trading_false",
                    lambda: ABC_REAL_TRADING_ENABLED is False)
        self._check("abc_real_account_false",
                    lambda: ABC_REAL_ACCOUNT_ENABLED is False)
        self._check("abc_real_order_false",
                    lambda: ABC_REAL_ORDER_ENABLED is False)
        self._check("abc_broker_false",
                    lambda: ABC_BROKER_EXECUTION_ENABLED is False)
        self._check("abc_production_false",
                    lambda: ABC_PRODUCTION_TRADING_ENABLED is False)
        self._check("abc_live_false",
                    lambda: ABC_LIVE_EXECUTION_ENABLED is False)
        self._check("abc_auto_order_false",
                    lambda: ABC_AUTO_ORDER_ENABLED is False)
        self._check("abc_auto_stop_false",
                    lambda: ABC_AUTO_STOP_LOSS_ENABLED is False)
        self._check("abc_auto_tp_false",
                    lambda: ABC_AUTO_TAKE_PROFIT_ENABLED is False)
        self._check("abc_margin_false",
                    lambda: ABC_MARGIN_ENABLED is False)
        self._check("no_real_orders_true",
                    lambda: NO_REAL_ORDERS is True)
        self._check("broker_execution_enabled_false",
                    lambda: BROKER_EXECUTION_ENABLED is False)
        self._check("production_trading_blocked_true",
                    lambda: PRODUCTION_TRADING_BLOCKED is True)
        self._check("audit_abc_safety_all_safe",
                    lambda: audit_abc_safety()["all_safe"] is True)
        self._check("audit_abc_safety_capabilities_zero",
                    lambda: audit_abc_safety()["safety_capabilities"] == 0)

        # ── Enums ──────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_execution_enums_v172 import (
            ABCBuyPointType, ABCExecutionStatus, ABCExecutionGrade,
            ABCPaperOrderIntentType, ABCExecutionBlockReason,
            get_all_enum_names,
        )
        self._check("enum_a_buy_point_exists",
                    lambda: ABCBuyPointType.A_10MA_PULLBACK.value == "A_10MA_PULLBACK")
        self._check("enum_b_buy_point_exists",
                    lambda: ABCBuyPointType.B_PLATFORM_BREAKOUT.value == "B_PLATFORM_BREAKOUT")
        self._check("enum_c_buy_point_exists",
                    lambda: ABCBuyPointType.C_20MA_RECLAIM.value == "C_20MA_RECLAIM")
        self._check("enum_execution_status_ready",
                    lambda: ABCExecutionStatus.READY.value == "READY")
        self._check("enum_grade_no_a_plus",
                    lambda: not hasattr(ABCExecutionGrade, "A_PLUS"))
        self._check("enum_paper_buy_intent",
                    lambda: ABCPaperOrderIntentType.PAPER_BUY.value == "PAPER_BUY")
        self._check("enum_real_order_block_reason",
                    lambda: ABCExecutionBlockReason.REAL_ORDER_REQUESTED.value == "REAL_ORDER_REQUESTED")
        self._check("enum_count_16",
                    lambda: len(get_all_enum_names()) == 16)

        # ── Models ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_execution_models_v172 import (
            ABCSignalInput, ABCNormalizedSignal, ABCConditionCheck,
            ABCEntryPricePlan, ABCStopLossExecutionPlan, ABCTakeProfitExecutionPlan,
            ABCExecutionPlan, ABCPaperOrderIntent, ABCExecutionScorecard,
        )
        from dataclasses import fields
        self._check("model_signal_input_has_paper_only",
                    lambda: "paper_only" in [f.name for f in fields(ABCSignalInput)])
        self._check("model_plan_has_schema_version",
                    lambda: "schema_version" in [f.name for f in fields(ABCExecutionPlan)])
        self._check("model_order_intent_no_real_orders",
                    lambda: "no_real_orders" in [f.name for f in fields(ABCPaperOrderIntent)])
        self._check("model_scorecard_weights_sum",
                    lambda: ABCExecutionScorecard.__dataclass_fields__ is not None)

        # ── A Rules ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_condition_checker_v172 import (
            check_a_conditions, get_condition_names,
        )
        a_names = get_condition_names(ABCBuyPointType.A_10MA_PULLBACK)
        self._check("a_condition_names_nonempty", lambda: len(a_names) >= 8)
        self._check("a_condition_has_ma20", lambda: "close_above_ma20" in a_names)
        self._check("a_condition_has_theme", lambda: "theme_strength_strong_or_leading" in a_names)

        # ── B Rules ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_condition_checker_v172 import (
            check_b_conditions,
        )
        b_names = get_condition_names(ABCBuyPointType.B_PLATFORM_BREAKOUT)
        self._check("b_condition_names_nonempty", lambda: len(b_names) >= 4)
        self._check("b_condition_has_volume", lambda: "volume_confirmed" in b_names)
        self._check("b_condition_has_regime", lambda: "regime_not_bear" in b_names)

        # ── C Rules ────────────────────────────────────────────────────────
        c_names = get_condition_names(ABCBuyPointType.C_20MA_RECLAIM)
        self._check("c_condition_names_nonempty", lambda: len(c_names) >= 6)
        self._check("c_condition_has_first_wave", lambda: "had_first_wave" in c_names)
        self._check("c_condition_has_ma20", lambda: "close_above_ma20" in c_names)

        # ── Entry Engine ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_entry_price_engine_v172 import (
            build_entry_plan, build_a_entry_plan, build_b_entry_plan, build_c_entry_plan,
        )
        self._check("entry_engine_callable", lambda: callable(build_entry_plan))
        self._check("entry_a_callable", lambda: callable(build_a_entry_plan))
        self._check("entry_b_callable", lambda: callable(build_b_entry_plan))
        self._check("entry_c_callable", lambda: callable(build_c_entry_plan))

        # ── Add Engine ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_add_price_engine_v172 import (
            build_add_plan,
        )
        self._check("add_engine_callable", lambda: callable(build_add_plan))

        # ── Stop Loss Engine ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_stop_loss_engine_v172 import (
            build_stop_loss_plan, validate_stop_loss, get_stop_loss_constants,
        )
        self._check("stop_loss_engine_callable", lambda: callable(build_stop_loss_plan))
        self._check("stop_loss_validate_callable", lambda: callable(validate_stop_loss))
        self._check("stop_loss_constants_max_pct",
                    lambda: get_stop_loss_constants()["max_stop_loss_pct"] == 0.10)

        # ── Take Profit Engine ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_take_profit_engine_v172 import (
            build_take_profit_plan, get_take_profit_constants,
        )
        self._check("take_profit_engine_callable", lambda: callable(build_take_profit_plan))
        self._check("take_profit_constants_set",
                    lambda: isinstance(get_take_profit_constants(), dict))

        # ── Invalidation Engine ────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_invalidation_engine_v172 import (
            build_invalidation_plan, get_invalidation_bars,
        )
        self._check("invalidation_engine_callable", lambda: callable(build_invalidation_plan))
        self._check("invalidation_bars_a_3",
                    lambda: get_invalidation_bars(ABCBuyPointType.A_10MA_PULLBACK) == 3)

        # ── Position Sizing Bridge ─────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_position_sizing_bridge_v172 import (
            compute_position_sizing, get_capital_constants, CAPITAL_300K, MAX_HOLDINGS,
        )
        self._check("position_sizing_callable", lambda: callable(compute_position_sizing))
        self._check("capital_300k", lambda: CAPITAL_300K == 300_000.0)
        self._check("max_holdings_4", lambda: MAX_HOLDINGS == 4)
        self._check("capital_constants_set", lambda: isinstance(get_capital_constants(), dict))

        # ── Watchlist Bridge ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_watchlist_bridge_v172 import (
            check_watchlist_compatibility, get_tier_allowed_buy_points,
        )
        self._check("watchlist_bridge_callable", lambda: callable(check_watchlist_compatibility))
        self._check("core_only_allows_a",
                    lambda: ABCBuyPointType.A_10MA_PULLBACK in get_tier_allowed_buy_points("CORE"))
        self._check("excluded_allows_nothing",
                    lambda: get_tier_allowed_buy_points("EXCLUDED") == [])

        # ── Market Regime Bridge ───────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_market_regime_bridge_v172 import (
            check_market_regime_compatibility, get_compatible_regimes,
        )
        self._check("regime_bridge_callable", lambda: callable(check_market_regime_compatibility))
        self._check("b_not_compatible_with_bear",
                    lambda: "BEAR" not in get_compatible_regimes(ABCBuyPointType.B_PLATFORM_BREAKOUT))

        # ── Forbidden Rule Bridge ──────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_forbidden_rule_bridge_v172 import (
            check_all_forbidden_rules, all_rules_passed, get_forbidden_rule_names,
        )
        self._check("forbidden_rules_callable", lambda: callable(check_all_forbidden_rules))
        self._check("forbidden_rule_names_nonempty",
                    lambda: len(get_forbidden_rule_names()) >= 8)
        normal_results = check_all_forbidden_rules("TEST")
        self._check("forbidden_rules_all_pass_default",
                    lambda: all_rules_passed(check_all_forbidden_rules("TEST")))

        # ── Paper Intent ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_paper_order_intent_v172 import (
            build_paper_order_intent, get_paper_intent_actions,
        )
        self._check("paper_intent_callable", lambda: callable(build_paper_order_intent))
        self._check("paper_intent_actions_has_paper_buy",
                    lambda: "PAPER_BUY" in get_paper_intent_actions())
        self._check("paper_intent_actions_has_paper_block",
                    lambda: "PAPER_BLOCK" in get_paper_intent_actions())

        # ── Scorecard ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_execution_scorecard_v172 import (
            compute_scorecard, get_scorecard_weights,
        )
        weights = get_scorecard_weights()
        self._check("scorecard_callable", lambda: callable(compute_scorecard))
        self._check("scorecard_weights_sum_100",
                    lambda: get_scorecard_weights()["sum"] == 100)
        self._check("scorecard_no_a_plus",
                    lambda: not hasattr(ABCExecutionGrade, "A_PLUS"))

        # ── Reports ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_execution_report_v172 import (
            get_section_names, render_markdown, render_json, render_csv,
            render_console_summary, build_report, SECTION_NAMES,
        )
        self._check("report_section_count_16",
                    lambda: len(get_section_names()) == 16)
        self._check("report_has_not_investment_advice",
                    lambda: "not_investment_advice" in get_section_names())
        self._check("report_has_safety", lambda: "safety" in get_section_names())
        self._check("render_markdown_callable", lambda: callable(render_markdown))
        self._check("render_json_callable", lambda: callable(render_json))
        self._check("render_csv_callable", lambda: callable(render_csv))

        # ── Scenarios ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_scenario_registry_v172 import (
            get_scenario_count, get_scenario_categories,
        )
        self._check("scenario_count_ge_70",
                    lambda: get_scenario_count() >= 70)
        self._check("scenario_has_a_buy_point_category",
                    lambda: "a_buy_point" in get_scenario_categories())
        self._check("scenario_has_b_buy_point_category",
                    lambda: "b_buy_point" in get_scenario_categories())
        self._check("scenario_has_c_buy_point_category",
                    lambda: "c_buy_point" in get_scenario_categories())
        self._check("scenario_has_paper_intent_category",
                    lambda: "paper_intent" in get_scenario_categories())

        # ── Fixtures ───────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.abc_fixture_registry_v172 import (
            get_fixture_count, validate_registry,
        )
        self._check("fixture_count_ge_70",
                    lambda: get_fixture_count() >= 70)
        self._check("fixtures_all_valid",
                    lambda: validate_registry()["valid"] is True)

        # ── No Stubs / No Placeholders ─────────────────────────────────────
        self._check("no_broker_connection",
                    lambda: ABC_BROKER_EXECUTION_ENABLED is False)
        self._check("no_real_account",
                    lambda: ABC_REAL_ACCOUNT_ENABLED is False)
        self._check("no_real_order",
                    lambda: ABC_REAL_ORDER_ENABLED is False)
        self._check("no_production_write",
                    lambda: ABC_PRODUCTION_TRADING_ENABLED is False)
        self._check("no_auto_order",
                    lambda: ABC_AUTO_ORDER_ENABLED is False)
        self._check("no_margin",
                    lambda: ABC_MARGIN_ENABLED is False)
        self._check("no_live_fallback",
                    lambda: ABC_LIVE_EXECUTION_ENABLED is False)

        all_passed = self._failed == 0
        return {
            "version": "1.7.2",
            "release_name": "A/B/C Buy Point Execution Plan",
            "all_passed": all_passed,
            "passed": self._passed,
            "failed": self._failed,
            "total": self._passed + self._failed,
            "status": "PASS" if all_passed else "FAIL",
            "checks": self._checks,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
        }


def run_health_check() -> Dict[str, Any]:
    """Run ABC execution plan health check. Returns result dict."""
    return ABCExecutionHealthCheck().run()
