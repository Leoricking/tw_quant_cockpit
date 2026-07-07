"""
release/watchlist_strategy_layer_release_gate_v171.py
Release gate for Watchlist Strategy Layer v1.7.1.
65+ gate checks. gate_passed=True required.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

GATE_VERSION = "1.7.1"
MIN_CHECKS   = 65


class WatchlistStrategyLayerReleaseGate:
    """Release gate for Watchlist Strategy Layer v1.7.1."""

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

        # ── Version ────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v171 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION,
            COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
            get_version_info, is_known_release, check_minimum_version,
        )
        self._check("gate_version_1_7_1", lambda: VERSION == "1.7.1")
        self._check("gate_release_name",
                    lambda: RELEASE_NAME == "Watchlist Strategy Layer")
        self._check("gate_base_release",
                    lambda: BASE_RELEASE == "1.7.0 Small Capital Growth Strategy Template")
        self._check("gate_schema_version_171", lambda: SCHEMA_VERSION == "171")
        self._check("gate_min_scenarios_70", lambda: MIN_SCENARIOS >= 70)
        self._check("gate_min_fixtures_70", lambda: MIN_FIXTURES >= 70)
        self._check("gate_min_cli_22", lambda: MIN_CLI >= 22)
        self._check("gate_min_health_70", lambda: MIN_HEALTH >= 70)
        self._check("gate_min_gate_65", lambda: MIN_GATE >= 65)
        self._check("gate_version_info_dict",
                    lambda: isinstance(get_version_info(), dict))
        self._check("gate_is_known_release_self",
                    lambda: is_known_release("Watchlist Strategy Layer"))
        self._check("gate_check_min_version_pass",
                    lambda: check_minimum_version("1.7.0"))

        # ── Safety ─────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_safety_v171 import (
            WATCHLIST_REAL_TRADING_ENABLED, WATCHLIST_BROKER_EXECUTION_ENABLED,
            WATCHLIST_MARGIN_ENABLED, WATCHLIST_AUTO_ORDER_ENABLED,
            WATCHLIST_PRODUCTION_TRADING_ENABLED, WATCHLIST_REAL_ACCOUNT_ENABLED,
            WATCHLIST_STRATEGY_RESEARCH_ONLY, WATCHLIST_STRATEGY_PAPER_ONLY,
            NO_REAL_ORDERS, PRODUCTION_TRADING_BLOCKED,
            get_watchlist_safety_flags, audit_watchlist_safety,
        )
        self._check("gate_real_trading_disabled",
                    lambda: WATCHLIST_REAL_TRADING_ENABLED is False)
        self._check("gate_broker_disabled",
                    lambda: WATCHLIST_BROKER_EXECUTION_ENABLED is False)
        self._check("gate_margin_disabled",
                    lambda: WATCHLIST_MARGIN_ENABLED is False)
        self._check("gate_auto_order_disabled",
                    lambda: WATCHLIST_AUTO_ORDER_ENABLED is False)
        self._check("gate_production_disabled",
                    lambda: WATCHLIST_PRODUCTION_TRADING_ENABLED is False)
        self._check("gate_real_account_disabled",
                    lambda: WATCHLIST_REAL_ACCOUNT_ENABLED is False)
        self._check("gate_research_only_true",
                    lambda: WATCHLIST_STRATEGY_RESEARCH_ONLY is True)
        self._check("gate_paper_only_true",
                    lambda: WATCHLIST_STRATEGY_PAPER_ONLY is True)
        self._check("gate_no_real_orders",
                    lambda: NO_REAL_ORDERS is True)
        self._check("gate_production_blocked",
                    lambda: PRODUCTION_TRADING_BLOCKED is True)
        self._check("gate_safety_audit_all_safe",
                    lambda: audit_watchlist_safety()["all_safe"] is True)
        self._check("gate_safety_capabilities_zero",
                    lambda: audit_watchlist_safety()["safety_capabilities"] == 0)
        self._check("gate_safety_flags_dict",
                    lambda: isinstance(get_watchlist_safety_flags(), dict))

        # ── Watchlist Profile ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.overdiversification_detector_v171 import (
            get_watchlist_size_rules, DEFAULT_WATCHLIST, MAX_WATCHLIST,
            FOCUS_CANDIDATES, TRADABLE_CANDIDATES,
        )
        rules = get_watchlist_size_rules()
        self._check("gate_default_watchlist_30", lambda: DEFAULT_WATCHLIST == 30)
        self._check("gate_max_watchlist_50", lambda: MAX_WATCHLIST == 50)
        self._check("gate_focus_candidates_10", lambda: FOCUS_CANDIDATES == 10)
        self._check("gate_tradable_candidates_5", lambda: TRADABLE_CANDIDATES == 5)
        self._check("gate_size_rules_dict", lambda: isinstance(rules, dict))

        # ── Scoring ────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_score_v171 import (
            SCORE_WEIGHTS, get_score_weights,
        )
        self._check("gate_score_weights_sum_100",
                    lambda: sum(SCORE_WEIGHTS.values()) == 100)
        self._check("gate_score_weights_has_theme",
                    lambda: "theme_strength" in SCORE_WEIGHTS)
        self._check("gate_score_weights_has_technical",
                    lambda: "technical" in SCORE_WEIGHTS)

        # ── Ranking ────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_ranking_v171 import (
            rank_candidates, get_ranking_rules,
        )
        from paper_trading.small_capital_strategy.watchlist_candidate_v171 import (
            make_sample_candidate,
        )
        from paper_trading.small_capital_strategy.watchlist_enums_v171 import WatchlistTier
        candidates = [make_sample_candidate(f"S{i}", WatchlistTier.CORE) for i in range(3)]
        ranked = rank_candidates(candidates)
        self._check("gate_rank_candidates_works",
                    lambda: len(ranked) == 3)
        self._check("gate_ranking_rules_dict",
                    lambda: isinstance(get_ranking_rules(), dict))

        # ── Filtering ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_filter_v171 import (
            filter_for_small_capital, exclude_untradable,
        )
        cand = make_sample_candidate()
        fr = filter_for_small_capital(cand)
        self._check("gate_filter_small_capital_works",
                    lambda: fr.passed is True)

        # ── Tier Classification ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_tier_classifier_v171 import (
            classify_watchlist_tier, get_tier_thresholds,
        )
        from paper_trading.small_capital_strategy.watchlist_enums_v171 import ThemeStrength
        tier_result = classify_watchlist_tier(
            total_score=88.0, theme_strength=ThemeStrength.STRONG,
            liquidity_score=85.0, exclusion_reasons=[], is_core_eligible=True,
        )
        self._check("gate_tier_classifier_core",
                    lambda: tier_result.tier == WatchlistTier.CORE)
        self._check("gate_tier_thresholds_dict",
                    lambda: isinstance(get_tier_thresholds(), dict))

        # ── Exclusion Rules ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
            WatchlistExclusionReason,
        )
        self._check("gate_exclusion_reason_weak_theme",
                    lambda: WatchlistExclusionReason.WEAK_THEME is not None)
        self._check("gate_exclusion_reason_low_liquidity",
                    lambda: WatchlistExclusionReason.LOW_LIQUIDITY is not None)
        self._check("gate_exclusion_reason_financing",
                    lambda: WatchlistExclusionReason.FINANCING_OVERHEATED is not None)

        # ── Overdiversification ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.overdiversification_detector_v171 import (
            detect_overdiversification,
        )
        pool = [make_sample_candidate(f"{i}") for i in range(20)]
        ov = detect_overdiversification(pool)
        self._check("gate_overdiversification_20_optimal",
                    lambda: ov.status.value == "OPTIMAL")

        # ── Top Candidates ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.top_candidate_selector_v171 import (
            recommend_top_candidates, get_selection_limits,
        )
        top = recommend_top_candidates(pool, regime="BULL")
        self._check("gate_recommend_focus_max_10",
                    lambda: len(top.focus_candidates) <= 10)
        self._check("gate_recommend_tradable_max_5",
                    lambda: len(top.tradable_candidates) <= 5)
        self._check("gate_selection_limits_dict",
                    lambda: isinstance(get_selection_limits(), dict))

        # ── v1.7.0 Mapping ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.small_capital_watchlist_bridge_v171 import (
            get_v170_bridge_summary, map_tier_to_allocation_bucket,
        )
        bridge = get_v170_bridge_summary()
        self._check("gate_bridge_paper_only",
                    lambda: bridge["paper_only"] is True)
        self._check("gate_bridge_max_holdings_4",
                    lambda: bridge["max_holdings"] == 4)
        self._check("gate_bridge_training_max_15k",
                    lambda: bridge["training_max_amount_twd"] == 15_000.0)
        self._check("gate_bridge_core_maps",
                    lambda: map_tier_to_allocation_bucket(WatchlistTier.CORE) == "CORE")

        # ── Reports ────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_report_v171 import (
            get_section_names,
        )
        self._check("gate_report_sections_14",
                    lambda: len(get_section_names()) >= 14)
        self._check("gate_report_has_not_investment_advice",
                    lambda: "not_investment_advice" in get_section_names())

        # ── Scenarios ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_scenario_registry_v171 import (
            WATCHLIST_SCENARIO_REGISTRY, get_scenario_count,
        )
        self._check("gate_scenario_count_gte_70",
                    lambda: len(WATCHLIST_SCENARIO_REGISTRY) >= 70)
        self._check("gate_scenarios_have_fixture_ids",
                    lambda: all("fixture_id" in s for s in WATCHLIST_SCENARIO_REGISTRY))

        # ── Fixtures ───────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_fixture_registry_v171 import (
            get_fixture_count, validate_all_fixtures,
        )
        self._check("gate_fixture_count_gte_70",
                    lambda: get_fixture_count() >= 70)
        valid_result = validate_all_fixtures()
        self._check("gate_all_fixtures_valid",
                    lambda: valid_result["valid"] is True)

        # ── Filters ────────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.liquidity_filter_v171 import (
            LIQUIDITY_HIGH_THRESHOLD, LIQUIDITY_MEDIUM_THRESHOLD, LIQUIDITY_LOW_THRESHOLD,
        )
        self._check("gate_liquidity_high_threshold_correct",
                    lambda: LIQUIDITY_HIGH_THRESHOLD == 20_000_000)
        self._check("gate_liquidity_low_threshold_correct",
                    lambda: LIQUIDITY_LOW_THRESHOLD == 1_000_000)

        from paper_trading.small_capital_strategy.financing_risk_filter_v171 import (
            FINANCING_OVERHEATED_THRESHOLD,
        )
        self._check("gate_financing_overheated_threshold_correct",
                    lambda: FINANCING_OVERHEATED_THRESHOLD == 0.30)

        from paper_trading.small_capital_strategy.institutional_filter_v171 import (
            INST_ACCUMULATING_THRESHOLD,
        )
        self._check("gate_institutional_accumulating_threshold_correct",
                    lambda: INST_ACCUMULATING_THRESHOLD == 10)

        from paper_trading.small_capital_strategy.theme_rotation_v171 import (
            get_sample_theme_signals, ROTATION_PHASES,
        )
        self._check("gate_rotation_phases_has_four",
                    lambda: len(ROTATION_PHASES) == 4)
        self._check("gate_sample_theme_signals_5",
                    lambda: len(get_sample_theme_signals()) == 5)

        from paper_trading.small_capital_strategy.watchlist_report_v171 import (
            SECTION_NAMES,
        )
        self._check("gate_section_names_has_safety",
                    lambda: "safety" in SECTION_NAMES)
        self._check("gate_section_names_has_v170_allocation",
                    lambda: "v170_allocation_mapping" in SECTION_NAMES)

        # ── Health PASS ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.watchlist_health_v171 import (
            run_health_check,
        )
        health = run_health_check()
        self._check("gate_health_all_passed",
                    lambda: health["all_passed"] is True)
        self._check("gate_health_status_pass",
                    lambda: health["status"] == "PASS")
        self._check("gate_health_failed_zero",
                    lambda: health["failed"] == 0)

        # ── Tally ──────────────────────────────────────────────────────────────
        total = len(self._checks)
        passed = sum(1 for c in self._checks if c["passed"])
        failed = total - passed
        gate_passed = failed == 0

        return {
            "gate_version": GATE_VERSION,
            "gate_passed": gate_passed,
            "total_count": total,
            "passed_count": passed,
            "failed_count": failed,
            "status": "PASS" if gate_passed else "FAIL",
            "checks": self._checks,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def run_release_gate() -> Dict[str, Any]:
    """Run watchlist strategy layer release gate. Returns result dict."""
    return WatchlistStrategyLayerReleaseGate().run()
