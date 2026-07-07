"""
paper_trading/small_capital_strategy/health_v170.py
Health check for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
80+ checks. All must PASS.
"""
from __future__ import annotations
from typing import Any, Dict, List, Tuple

HEALTH_VERSION = "1.7.0"


class SmallCapitalHealthCheck:
    """Health check runner for Small Capital Growth Strategy v1.7.0."""

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

        # ── Version identity ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v170 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
            COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH,
            get_version_info, verify_version, is_known_release, check_minimum_version,
        )
        self._check("version_is_1_7_0", lambda: VERSION == "1.7.0")
        self._check("release_name_correct", lambda: RELEASE_NAME == "Small Capital Growth Strategy Template")
        self._check("base_release_correct", lambda: BASE_RELEASE == "1.6.9.1 Stable Rollup Compatibility Hotfix")
        self._check("schema_version_170", lambda: SCHEMA_VERSION == "170")
        self._check("policy_version_set", lambda: "1.7.0" in POLICY_VERSION)
        self._check("component_count_28", lambda: COMPONENT_COUNT == 28)
        self._check("min_scenarios_80", lambda: MIN_SCENARIOS == 80)
        self._check("min_fixtures_80", lambda: MIN_FIXTURES == 80)
        self._check("min_cli_25", lambda: MIN_CLI == 25)
        self._check("min_health_80", lambda: MIN_HEALTH == 80)
        self._check("get_version_info_returns_dict", lambda: isinstance(get_version_info(), dict))
        self._check("verify_version_returns_dict", lambda: isinstance(verify_version(), dict))
        self._check("is_known_release_self", lambda: is_known_release("Small Capital Growth Strategy Template"))
        self._check("is_known_release_v169", lambda: is_known_release("Live Paper Trading Stable Rollup"))
        self._check("check_minimum_version_pass", lambda: check_minimum_version("1.6.9.1"))
        self._check("check_minimum_version_fail", lambda: not check_minimum_version("1.5.0"))

        # ── Package init ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy import (
            VERSION as PKG_VERSION,
            SMALL_CAPITAL_STRATEGY_AVAILABLE,
            SMALL_CAPITAL_STRATEGY_RESEARCH_ONLY,
            NO_REAL_ORDERS,
            BROKER_EXECUTION_ENABLED,
            PRODUCTION_TRADING_BLOCKED,
        )
        self._check("pkg_version_1_7_0", lambda: PKG_VERSION == "1.7.0")
        self._check("pkg_available_true", lambda: SMALL_CAPITAL_STRATEGY_AVAILABLE is True)
        self._check("pkg_research_only_true", lambda: SMALL_CAPITAL_STRATEGY_RESEARCH_ONLY is True)
        self._check("pkg_no_real_orders_true", lambda: NO_REAL_ORDERS is True)
        self._check("pkg_broker_disabled", lambda: BROKER_EXECUTION_ENABLED is False)
        self._check("pkg_production_blocked", lambda: PRODUCTION_TRADING_BLOCKED is True)

        # ── Safety ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.safety_v170 import (
            get_safety_flags, audit_safety, assert_safe,
            LIVE_FALLBACK_ENABLED, RESEARCH_ONLY, BROKER_ENABLED,
        )
        self._check("safety_live_fallback_disabled", lambda: LIVE_FALLBACK_ENABLED is False)
        self._check("safety_research_only_true", lambda: RESEARCH_ONLY is True)
        self._check("safety_broker_disabled", lambda: BROKER_ENABLED is False)
        self._check("safety_get_flags_dict", lambda: isinstance(get_safety_flags(), dict))
        self._check("safety_audit_all_safe", lambda: audit_safety()["all_safe"] is True)
        self._check("safety_assert_safe_no_raise", lambda: (assert_safe(), True)[1])

        # ── Enums ──────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.enums_v170 import (
            BuyPointType, MarketRegime, AllocationBucket, SmallCapitalGrade,
            WatchlistTier, ThemeStrength, ForbiddenTradeReason,
        )
        self._check("enum_buy_point_a", lambda: BuyPointType.A_10MA_PULLBACK is not None)
        self._check("enum_buy_point_b", lambda: BuyPointType.B_PLATFORM_BREAKOUT is not None)
        self._check("enum_buy_point_c", lambda: BuyPointType.C_20MA_RECLAIM is not None)
        self._check("enum_market_regime_bull", lambda: MarketRegime.BULL is not None)
        self._check("enum_market_regime_bear", lambda: MarketRegime.BEAR is not None)
        self._check("enum_allocation_bucket_core", lambda: AllocationBucket.CORE is not None)
        self._check("enum_grade_a", lambda: SmallCapitalGrade.A is not None)
        self._check("enum_grade_blocked", lambda: SmallCapitalGrade.BLOCKED is not None)
        self._check("enum_watchlist_tier_core", lambda: WatchlistTier.CORE is not None)
        self._check("enum_theme_strong", lambda: ThemeStrength.STRONG is not None)
        self._check("enum_forbidden_margin", lambda: ForbiddenTradeReason.MARGIN_NOT_ALLOWED is not None)

        # ── Capital profile ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.capital_profile_v170 import (
            get_300k_template, validate_capital_profile,
            TEMPLATE_300K_ID, TEMPLATE_300K_CAPITAL,
            TEMPLATE_300K_MAX_LOSS_DEFAULT, TEMPLATE_300K_RISK_PCT_DEFAULT,
        )
        profile = get_300k_template()
        self._check("capital_profile_template_id", lambda: TEMPLATE_300K_ID == "small_capital_300k_v170")
        self._check("capital_profile_300k", lambda: TEMPLATE_300K_CAPITAL == 300000.0)
        self._check("capital_profile_max_loss", lambda: TEMPLATE_300K_MAX_LOSS_DEFAULT == 3000.0)
        self._check("capital_profile_risk_pct", lambda: TEMPLATE_300K_RISK_PCT_DEFAULT == 0.01)
        self._check("capital_profile_get_template", lambda: profile is not None)
        self._check("capital_profile_validate_pass", lambda: validate_capital_profile(profile)["valid"] is True)

        # ── Risk budget ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.risk_budget_v170 import (
            compute_risk_budget, validate_risk_budget,
        )
        budget = compute_risk_budget(profile)
        self._check("risk_budget_compute", lambda: budget is not None)
        self._check("risk_budget_max_loss_3000", lambda: budget.max_loss_per_trade == 3000.0)
        self._check("risk_budget_validate_pass", lambda: validate_risk_budget(budget)["valid"] is True)

        # ── Allocation ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.allocation_template_v170 import (
            get_allocation_for_regime, validate_allocation,
        )
        alloc = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, 300000.0)
        self._check("allocation_bull_returns", lambda: alloc is not None)
        self._check("allocation_validate_pass", lambda: validate_allocation(alloc)["valid"] is True)
        alloc_bear = get_allocation_for_regime(MarketRegime.BEAR, TEMPLATE_300K_ID, 300000.0)
        self._check("allocation_bear_cash_50pct", lambda: alloc_bear.cash_pct >= 0.49)

        # ── Position sizing ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.position_sizing_v170 import (
            compute_position_size, PositionSizingInput,
        )
        sizing_inp = PositionSizingInput(
            symbol="2330",
            capital_twd=300000.0,
            max_loss_amount=3000.0,
            stop_loss_pct=0.06,
            bucket=AllocationBucket.MAIN_THEME_SWING,
            bucket_remaining_budget=105000.0,
        )
        sizing = compute_position_size(sizing_inp)
        self._check("position_sizing_compute", lambda: sizing is not None)
        self._check("position_sizing_formula", lambda: abs(sizing.position_size_twd - 50000.0) < 1.0)

        # ── Watchlist ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_profile_v170 import (
            create_default_watchlist_profile, rank_candidates,
            filter_for_small_capital, recommend_top_candidates,
            MAX_WATCHLIST, FOCUS_CANDIDATES, TRADABLE_CANDIDATES,
        )
        self._check("watchlist_max_50", lambda: MAX_WATCHLIST == 50)
        self._check("watchlist_focus_10", lambda: FOCUS_CANDIDATES == 10)
        self._check("watchlist_tradable_5", lambda: TRADABLE_CANDIDATES == 5)
        wp = create_default_watchlist_profile()
        self._check("watchlist_profile_create", lambda: wp is not None)

        # ── Market regime ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.market_regime_filter_v170 import (
            get_regime_control, is_trade_allowed_in_regime,
        )
        regime_result = get_regime_control(MarketRegime.BULL)
        self._check("regime_bull_control", lambda: regime_result is not None)
        self._check("regime_bull_max_invested_95", lambda: regime_result.max_invested_pct >= 0.94)
        self._check("regime_trade_allowed_bull", lambda: is_trade_allowed_in_regime(MarketRegime.BULL) is True)

        # ── Scorecard ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.small_capital_scorecard_v170 import (
            compute_scorecard, get_scorecard_weights, validate_scorecard,
            SCORE_WEIGHTS,
        )
        self._check("scorecard_weights_sum_100", lambda: sum(SCORE_WEIGHTS.values()) == 100)
        sc = compute_scorecard(TEMPLATE_300K_ID, {k: 1.0 for k in SCORE_WEIGHTS})
        self._check("scorecard_perfect_score_100", lambda: sc.score == 100.0)
        self._check("scorecard_grade_a", lambda: sc.grade == SmallCapitalGrade.A)
        sc_blocked = compute_scorecard(TEMPLATE_300K_ID, {}, safety_blocked=True)
        self._check("scorecard_safety_blocked_grade", lambda: sc_blocked.grade == SmallCapitalGrade.BLOCKED)
        self._check("scorecard_validate_pass", lambda: validate_scorecard(sc)["valid"] is True)

        # ── Fixture schema ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.fixture_schema_v170 import (
            REQUIRED_MARKERS, REQUIRED_FIELDS, validate_fixture,
        )
        self._check("fixture_schema_10_markers", lambda: len(REQUIRED_MARKERS) == 10)
        self._check("fixture_schema_all_markers_true", lambda: all(v is True for v in REQUIRED_MARKERS.values()))
        self._check("fixture_schema_has_small_capital_only", lambda: "small_capital_strategy_only" in REQUIRED_MARKERS)
        self._check("fixture_schema_required_fields", lambda: len(REQUIRED_FIELDS) >= 18)

        # ── Fixture registry ──────────────────────────────────────────────
        from paper_trading.small_capital_strategy.fixture_registry_v170 import (
            FIXTURE_REGISTRY, count_fixtures, get_all_categories,
        )
        self._check("fixture_registry_80", lambda: count_fixtures() == 80)
        self._check("fixture_registry_has_sc_001", lambda: "sc_001" in FIXTURE_REGISTRY)
        self._check("fixture_registry_has_sc_080", lambda: "sc_080" in FIXTURE_REGISTRY)
        self._check("fixture_registry_categories", lambda: len(get_all_categories()) >= 8)

        # ── Scenario registry ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.scenario_registry_v170 import (
            SCENARIO_REGISTRY, get_scenarios_by_category,
        )
        self._check("scenario_registry_80", lambda: len(SCENARIO_REGISTRY) == 80)
        self._check("scenario_registry_list", lambda: isinstance(SCENARIO_REGISTRY, list))
        self._check("scenario_registry_capital_profile_10", lambda: len(get_scenarios_by_category("capital_profile")) == 10)

        # ── Paper simulation bridge ───────────────────────────────────────
        from paper_trading.small_capital_strategy.paper_simulation_bridge_v170 import (
            get_simulation_safety_summary,
        )
        safety_summary = get_simulation_safety_summary()
        self._check("sim_bridge_real_exec_false", lambda: safety_summary["real_execution_enabled"] is False)
        self._check("sim_bridge_broker_false", lambda: safety_summary["broker_connected"] is False)
        self._check("sim_bridge_paper_only", lambda: safety_summary["paper_only"] is True)

        # ── Strategy template ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_template_v170 import (
            build_300k_template, validate_strategy_template, get_template_summary,
        )
        tmpl = build_300k_template(regime=MarketRegime.BULL)
        self._check("strategy_template_build", lambda: tmpl is not None)
        self._check("strategy_template_validate", lambda: validate_strategy_template(tmpl)["valid"] is True)
        self._check("strategy_template_summary", lambda: isinstance(get_template_summary(tmpl), dict))

        # ── Strategy report ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_report_v170 import (
            build_report, to_markdown, to_json, to_csv, to_console_summary,
            get_section_names,
        )
        scorecard = compute_scorecard(TEMPLATE_300K_ID, {k: 0.8 for k in SCORE_WEIGHTS})
        report = build_report(TEMPLATE_300K_ID, scorecard)
        self._check("report_build", lambda: report is not None)
        self._check("report_markdown_contains_disclaimer", lambda: "Not Investment Advice" in to_markdown(report))
        self._check("report_json_valid", lambda: isinstance(to_json(report), str))
        self._check("report_csv_valid", lambda: "template_id" in to_csv(report))
        self._check("report_console_summary", lambda: isinstance(to_console_summary(report), str))
        self._check("report_section_names_15", lambda: len(get_section_names()) == 15)

        # ── Safety flags (paper only markers on report) ───────────────────
        self._check("report_paper_only_true", lambda: report.paper_only is True)
        self._check("report_research_only_true", lambda: report.research_only is True)
        self._check("report_no_real_orders_true", lambda: report.no_real_orders is True)
        self._check("report_not_investment_advice_true", lambda: report.not_investment_advice is True)

        all_passed = self._failed == 0
        return {
            "health_version": HEALTH_VERSION,
            "checks": self._checks,
            "passed": self._passed,
            "failed": self._failed,
            "total": len(self._checks),
            "all_passed": all_passed,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def run_health_check() -> Dict[str, Any]:
    """Convenience function to run health check and return result."""
    return SmallCapitalHealthCheck().run()
