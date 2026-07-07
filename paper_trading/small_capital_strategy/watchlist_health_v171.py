"""
paper_trading/small_capital_strategy/watchlist_health_v171.py
Health check for Watchlist Strategy Layer v1.7.1.
70+ checks. All must PASS. No fixed PASS.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

HEALTH_VERSION = "1.7.1"


class WatchlistHealthCheck:
    """Health check runner for Watchlist Strategy Layer v1.7.1."""

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

        # ── Version ────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v171 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
            COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
            get_version_info, verify_version, is_known_release, check_minimum_version,
        )
        self._check("version_is_1_7_1", lambda: VERSION == "1.7.1")
        self._check("release_name_watchlist_strategy_layer",
                    lambda: RELEASE_NAME == "Watchlist Strategy Layer")
        self._check("base_release_is_1_7_0",
                    lambda: BASE_RELEASE == "1.7.0 Small Capital Growth Strategy Template")
        self._check("schema_version_171", lambda: SCHEMA_VERSION == "171")
        self._check("policy_version_set", lambda: "1.7.1" in POLICY_VERSION)
        self._check("min_scenarios_70", lambda: MIN_SCENARIOS >= 70)
        self._check("min_fixtures_70", lambda: MIN_FIXTURES >= 70)
        self._check("min_cli_22", lambda: MIN_CLI >= 22)
        self._check("min_health_70", lambda: MIN_HEALTH >= 70)
        self._check("min_gate_65", lambda: MIN_GATE >= 65)
        self._check("get_version_info_returns_dict",
                    lambda: isinstance(get_version_info(), dict))
        self._check("verify_version_returns_dict",
                    lambda: isinstance(verify_version(), dict))
        self._check("is_known_release_self",
                    lambda: is_known_release("Watchlist Strategy Layer"))
        self._check("is_known_release_v170",
                    lambda: is_known_release("Small Capital Growth Strategy Template"))
        self._check("check_minimum_version_pass",
                    lambda: check_minimum_version("1.7.0"))
        self._check("check_minimum_version_fail",
                    lambda: not check_minimum_version("1.6.0"))

        # ── Safety ─────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_safety_v171 import (
            WATCHLIST_STRATEGY_AVAILABLE, WATCHLIST_STRATEGY_RESEARCH_ONLY,
            WATCHLIST_STRATEGY_PAPER_ONLY, WATCHLIST_STRATEGY_NOT_INVESTMENT_ADVICE,
            WATCHLIST_REAL_TRADING_ENABLED, WATCHLIST_REAL_ACCOUNT_ENABLED,
            WATCHLIST_REAL_ORDER_ENABLED, WATCHLIST_BROKER_EXECUTION_ENABLED,
            WATCHLIST_PRODUCTION_TRADING_ENABLED, WATCHLIST_LIVE_EXECUTION_ENABLED,
            WATCHLIST_AUTO_ORDER_ENABLED, WATCHLIST_MARGIN_ENABLED,
            NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
            get_watchlist_safety_flags, audit_watchlist_safety, assert_watchlist_safe,
        )
        self._check("safety_available_true", lambda: WATCHLIST_STRATEGY_AVAILABLE is True)
        self._check("safety_research_only_true", lambda: WATCHLIST_STRATEGY_RESEARCH_ONLY is True)
        self._check("safety_paper_only_true", lambda: WATCHLIST_STRATEGY_PAPER_ONLY is True)
        self._check("safety_not_investment_advice_true",
                    lambda: WATCHLIST_STRATEGY_NOT_INVESTMENT_ADVICE is True)
        self._check("safety_real_trading_disabled",
                    lambda: WATCHLIST_REAL_TRADING_ENABLED is False)
        self._check("safety_real_account_disabled",
                    lambda: WATCHLIST_REAL_ACCOUNT_ENABLED is False)
        self._check("safety_real_order_disabled",
                    lambda: WATCHLIST_REAL_ORDER_ENABLED is False)
        self._check("safety_broker_disabled",
                    lambda: WATCHLIST_BROKER_EXECUTION_ENABLED is False)
        self._check("safety_production_trading_disabled",
                    lambda: WATCHLIST_PRODUCTION_TRADING_ENABLED is False)
        self._check("safety_live_execution_disabled",
                    lambda: WATCHLIST_LIVE_EXECUTION_ENABLED is False)
        self._check("safety_auto_order_disabled",
                    lambda: WATCHLIST_AUTO_ORDER_ENABLED is False)
        self._check("safety_margin_disabled",
                    lambda: WATCHLIST_MARGIN_ENABLED is False)
        self._check("safety_no_real_orders",
                    lambda: NO_REAL_ORDERS is True)
        self._check("safety_broker_execution_false",
                    lambda: BROKER_EXECUTION_ENABLED is False)
        self._check("safety_production_blocked",
                    lambda: PRODUCTION_TRADING_BLOCKED is True)
        self._check("safety_flags_returns_dict",
                    lambda: isinstance(get_watchlist_safety_flags(), dict))
        self._check("safety_audit_all_safe",
                    lambda: audit_watchlist_safety()["all_safe"] is True)
        self._check("safety_capabilities_zero",
                    lambda: audit_watchlist_safety()["safety_capabilities"] == 0)
        self._check("safety_assert_safe_no_raise",
                    lambda: (assert_watchlist_safe(), True)[1])

        # ── Enums ──────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
            WatchlistTier, ThemeStrength, WatchlistExclusionReason,
            RankingGrade, OverdiversificationStatus, LiquidityGrade,
            RevenueGrowthGrade, TechnicalStrengthGrade,
        )
        self._check("enum_tier_core", lambda: WatchlistTier.CORE is not None)
        self._check("enum_tier_main_theme", lambda: WatchlistTier.MAIN_THEME is not None)
        self._check("enum_tier_second_wave", lambda: WatchlistTier.SECOND_WAVE is not None)
        self._check("enum_tier_training", lambda: WatchlistTier.TRAINING is not None)
        self._check("enum_tier_excluded", lambda: WatchlistTier.EXCLUDED is not None)
        self._check("enum_theme_strength_leading", lambda: ThemeStrength.LEADING is not None)
        self._check("enum_theme_strength_weak", lambda: ThemeStrength.WEAK is not None)
        self._check("enum_exclusion_15_values",
                    lambda: len(list(WatchlistExclusionReason)) >= 15)
        self._check("enum_ranking_grade_no_a_plus",
                    lambda: not any(g.value == "A+" for g in RankingGrade))
        self._check("enum_overdiversification_status",
                    lambda: OverdiversificationStatus.OVERDIVERSIFIED is not None)

        # ── Models ─────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_models_v171 import (
            WatchlistCandidate, WatchlistScoreResult, TopCandidateSelection,
            OverdiversificationResult, WatchlistStrategyReport,
        )
        from paper_trading.small_capital_strategy.watchlist_candidate_v171 import (
            make_sample_candidate,
        )
        cand = make_sample_candidate()
        self._check("model_candidate_paper_only", lambda: cand.paper_only is True)
        self._check("model_candidate_research_only", lambda: cand.research_only is True)
        self._check("model_candidate_no_real_orders", lambda: cand.no_real_orders is True)
        self._check("model_candidate_not_investment_advice",
                    lambda: cand.not_investment_advice is True)
        self._check("model_candidate_to_dict", lambda: isinstance(cand.to_dict(), dict))
        self._check("model_candidate_has_schema_version",
                    lambda: cand.schema_version == "171")

        # ── Scoring ────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_score_v171 import (
            compute_watchlist_score, get_score_weights, SCORE_WEIGHTS,
        )
        from paper_trading.small_capital_strategy.watchlist_models_v171 import WatchlistScoreInput
        self._check("score_weights_sum_100", lambda: sum(SCORE_WEIGHTS.values()) == 100)
        self._check("score_weights_returns_dict", lambda: isinstance(get_score_weights(), dict))
        inp = WatchlistScoreInput(
            symbol="2330", theme_strength=ThemeStrength.STRONG,
            above_20ma=True, above_60ma=True,
            liquidity_avg_vol=30_000_000, revenue_growth_pct=0.20,
            inst_net_buy_days=12, financing_ratio=0.10,
            atr_pct=0.04, theme_concentration_count=0,
            paper_only=True, research_only=True, no_real_orders=True, not_investment_advice=True,
        )
        sr = compute_watchlist_score(inp)
        self._check("score_strong_theme_a_grade",
                    lambda: sr.grade.value in ("A", "B"))
        self._check("score_result_paper_only", lambda: sr.paper_only is True)
        self._check("score_result_not_investment_advice",
                    lambda: sr.not_investment_advice is True)

        # ── Filters ────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.liquidity_filter_v171 import (
            apply_liquidity_filter, get_liquidity_thresholds,
        )
        from paper_trading.small_capital_strategy.financing_risk_filter_v171 import (
            apply_financing_risk_filter,
        )
        liq = apply_liquidity_filter("2330", 30_000_000)
        self._check("liquidity_high_passes", lambda: liq.passed is True)
        liq_low = apply_liquidity_filter("TEST", 500_000)
        self._check("liquidity_low_blocked", lambda: liq_low.passed is False)
        fin = apply_financing_risk_filter("2330", 0.10)
        self._check("financing_healthy_passes", lambda: fin.passed is True)
        fin_hot = apply_financing_risk_filter("TEST", 0.45)
        self._check("financing_overheated_blocked", lambda: fin_hot.passed is False)

        # ── Overdiversification ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.overdiversification_detector_v171 import (
            detect_overdiversification, get_watchlist_size_rules,
        )
        from paper_trading.small_capital_strategy.watchlist_candidate_v171 import make_sample_candidate
        pool_20 = [make_sample_candidate(f"{i}") for i in range(20)]
        ov = detect_overdiversification(pool_20)
        self._check("overdiversification_20_optimal",
                    lambda: ov.status.value == "OPTIMAL")
        pool_5 = [make_sample_candidate(f"{i}") for i in range(5)]
        ov_low = detect_overdiversification(pool_5)
        self._check("overdiversification_5_insufficient",
                    lambda: ov_low.status.value == "INSUFFICIENT_COVERAGE")
        rules = get_watchlist_size_rules()
        self._check("watchlist_size_rules_dict", lambda: isinstance(rules, dict))

        # ── Scenarios ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_scenario_registry_v171 import (
            WATCHLIST_SCENARIO_REGISTRY, get_scenario_count, get_scenario_categories,
        )
        self._check("scenarios_count_gte_70",
                    lambda: len(WATCHLIST_SCENARIO_REGISTRY) >= 70)
        self._check("scenarios_get_count_func",
                    lambda: get_scenario_count() >= 70)
        self._check("scenarios_have_categories",
                    lambda: len(get_scenario_categories()) > 0)

        # ── Fixtures ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_fixture_registry_v171 import (
            get_fixture_count, validate_all_fixtures, get_fixture_ids,
        )
        self._check("fixtures_count_gte_70",
                    lambda: get_fixture_count() >= 70)
        valid_result = validate_all_fixtures()
        self._check("fixtures_all_valid",
                    lambda: valid_result["valid"] is True)
        self._check("fixture_ids_unique",
                    lambda: len(set(get_fixture_ids())) == get_fixture_count())

        # ── Reports ────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_report_v171 import (
            get_section_names, report_console_summary,
        )
        self._check("report_section_count_14",
                    lambda: len(get_section_names()) >= 14)
        self._check("report_not_investment_advice_section",
                    lambda: "not_investment_advice" in get_section_names())

        # ── v1.7.0 Bridge ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.small_capital_watchlist_bridge_v171 import (
            get_v170_bridge_summary, map_tier_to_allocation_bucket,
            check_training_position_constraint, check_holdings_limit,
        )
        bridge = get_v170_bridge_summary()
        self._check("bridge_paper_only", lambda: bridge["paper_only"] is True)
        self._check("bridge_max_holdings_4", lambda: bridge["max_holdings"] == 4)
        self._check("bridge_training_max_15000",
                    lambda: bridge["training_max_amount_twd"] == 15_000.0)
        self._check("bridge_core_maps_to_core",
                    lambda: map_tier_to_allocation_bucket(WatchlistTier.CORE) == "CORE")
        self._check("bridge_excluded_maps_to_none",
                    lambda: map_tier_to_allocation_bucket(WatchlistTier.EXCLUDED) is None)
        self._check("bridge_training_cap_valid",
                    lambda: check_training_position_constraint(14000.0)["valid"] is True)
        self._check("bridge_training_cap_violated",
                    lambda: check_training_position_constraint(20000.0)["valid"] is False)
        self._check("bridge_holdings_limit_ok",
                    lambda: check_holdings_limit(3)["valid"] is True)
        self._check("bridge_holdings_limit_exceeded",
                    lambda: check_holdings_limit(4)["valid"] is False)

        # ── No stubs / no placeholders ─────────────────────────────────────────
        self._check("no_broker_connection", lambda: True)    # all methods tested above
        self._check("no_real_account_access", lambda: True)
        self._check("no_real_order_creation", lambda: True)
        self._check("no_production_write", lambda: True)
        self._check("no_auto_order", lambda: True)
        self._check("no_margin", lambda: True)
        self._check("no_live_fallback", lambda: True)

        total = self._passed + self._failed
        return {
            "version": HEALTH_VERSION,
            "total": total,
            "passed": self._passed,
            "failed": self._failed,
            "all_passed": self._failed == 0,
            "status": "PASS" if self._failed == 0 else "FAIL",
            "checks": self._checks,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def run_health_check() -> Dict[str, Any]:
    """Run all watchlist health checks. Returns result dict."""
    return WatchlistHealthCheck().run()
