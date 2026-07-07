"""
release/small_capital_growth_strategy_release_gate_v170.py
Release gate for Small Capital Growth Strategy Template v1.7.0.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
70+ gate checks. gate_passed=True required.
"""
from __future__ import annotations
from typing import Any, Dict, List

GATE_VERSION = "1.7.0"
MIN_CHECKS = 70


class SmallCapitalGrowthStrategyReleaseGate:
    """Release gate for Small Capital Growth Strategy v1.7.0."""

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

        # ── Version checks ─────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.version_v170 import (
            VERSION, RELEASE_NAME, BASE_RELEASE, SCHEMA_VERSION, POLICY_VERSION,
            COMPONENT_COUNT, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH, MIN_GATE,
            get_version_info, is_known_release, check_minimum_version,
        )
        self._check("gate_version_1_7_0", lambda: VERSION == "1.7.0")
        self._check("gate_release_name", lambda: RELEASE_NAME == "Small Capital Growth Strategy Template")
        self._check("gate_base_release", lambda: BASE_RELEASE == "1.6.9.1 Stable Rollup Compatibility Hotfix")
        self._check("gate_schema_version_170", lambda: SCHEMA_VERSION == "170")
        self._check("gate_component_count_28", lambda: COMPONENT_COUNT == 28)
        self._check("gate_min_scenarios_80", lambda: MIN_SCENARIOS == 80)
        self._check("gate_min_fixtures_80", lambda: MIN_FIXTURES == 80)
        self._check("gate_min_cli_25", lambda: MIN_CLI == 25)
        self._check("gate_min_health_80", lambda: MIN_HEALTH == 80)
        self._check("gate_min_gate_70", lambda: MIN_GATE == 70)
        self._check("gate_version_info_dict", lambda: isinstance(get_version_info(), dict))
        self._check("gate_is_known_release_self", lambda: is_known_release("Small Capital Growth Strategy Template"))
        self._check("gate_check_min_version_pass", lambda: check_minimum_version("1.6.9.1"))

        # ── Safety ─────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.safety_v170 import (
            get_safety_flags, audit_safety, LIVE_FALLBACK_ENABLED,
            RESEARCH_ONLY, BROKER_ENABLED,
        )
        self._check("gate_safety_live_fallback_disabled", lambda: LIVE_FALLBACK_ENABLED is False)
        self._check("gate_safety_broker_disabled", lambda: BROKER_ENABLED is False)
        self._check("gate_safety_research_only", lambda: RESEARCH_ONLY is True)
        self._check("gate_safety_audit_all_safe", lambda: audit_safety()["all_safe"] is True)
        self._check("gate_safety_flags_dict", lambda: isinstance(get_safety_flags(), dict))

        # ── Package ────────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy import (
            VERSION as PKG_VERSION,
            SMALL_CAPITAL_STRATEGY_AVAILABLE,
            NO_REAL_ORDERS,
            BROKER_EXECUTION_ENABLED,
            PRODUCTION_TRADING_BLOCKED,
        )
        self._check("gate_pkg_version", lambda: PKG_VERSION == "1.7.0")
        self._check("gate_pkg_available", lambda: SMALL_CAPITAL_STRATEGY_AVAILABLE is True)
        self._check("gate_pkg_no_real_orders", lambda: NO_REAL_ORDERS is True)
        self._check("gate_pkg_broker_disabled", lambda: BROKER_EXECUTION_ENABLED is False)
        self._check("gate_pkg_prod_blocked", lambda: PRODUCTION_TRADING_BLOCKED is True)

        # ── Capital profile ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.capital_profile_v170 import (
            get_300k_template, validate_capital_profile,
            TEMPLATE_300K_ID, TEMPLATE_300K_CAPITAL, TEMPLATE_300K_MAX_LOSS_DEFAULT,
        )
        profile = get_300k_template()
        self._check("gate_capital_300k", lambda: TEMPLATE_300K_CAPITAL == 300000.0)
        self._check("gate_max_loss_3000", lambda: TEMPLATE_300K_MAX_LOSS_DEFAULT == 3000.0)
        self._check("gate_capital_profile_valid", lambda: validate_capital_profile(profile)["valid"] is True)

        # ── Risk budget ────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.risk_budget_v170 import (
            compute_risk_budget, validate_risk_budget,
        )
        budget = compute_risk_budget(profile)
        self._check("gate_risk_budget_compute", lambda: budget is not None)
        self._check("gate_risk_budget_max_loss_3000", lambda: budget.max_loss_per_trade == 3000.0)
        self._check("gate_risk_budget_valid", lambda: validate_risk_budget(budget)["valid"] is True)

        # ── Allocation ─────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.enums_v170 import MarketRegime, AllocationBucket
        from paper_trading.small_capital_strategy.allocation_template_v170 import (
            get_allocation_for_regime, validate_allocation,
        )
        alloc_bull = get_allocation_for_regime(MarketRegime.BULL, TEMPLATE_300K_ID, 300000.0)
        alloc_bear = get_allocation_for_regime(MarketRegime.BEAR, TEMPLATE_300K_ID, 300000.0)
        self._check("gate_alloc_bull_valid", lambda: validate_allocation(alloc_bull)["valid"] is True)
        self._check("gate_alloc_bear_valid", lambda: validate_allocation(alloc_bear)["valid"] is True)
        self._check("gate_alloc_bear_cash_50pct", lambda: alloc_bear.cash_pct >= 0.49)

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
        self._check("gate_position_sizing_compute", lambda: sizing is not None)
        self._check("gate_position_sizing_formula", lambda: abs(sizing.position_size_twd - 50000.0) < 1.0)

        # ── Market regime ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.market_regime_filter_v170 import (
            get_regime_control, is_trade_allowed_in_regime,
        )
        self._check("gate_regime_bull_allowed", lambda: is_trade_allowed_in_regime(MarketRegime.BULL) is True)
        self._check("gate_regime_bear_control", lambda: get_regime_control(MarketRegime.BEAR) is not None)

        # ── Scorecard ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.small_capital_scorecard_v170 import (
            compute_scorecard, get_scorecard_weights, SCORE_WEIGHTS,
        )
        from paper_trading.small_capital_strategy.enums_v170 import SmallCapitalGrade
        self._check("gate_scorecard_weights_sum_100", lambda: sum(SCORE_WEIGHTS.values()) == 100)
        sc = compute_scorecard(TEMPLATE_300K_ID, {k: 1.0 for k in SCORE_WEIGHTS})
        self._check("gate_scorecard_perfect_100", lambda: sc.score == 100.0)
        self._check("gate_scorecard_grade_a", lambda: sc.grade == SmallCapitalGrade.A)

        # ── Fixture schema ─────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.fixture_schema_v170 import (
            REQUIRED_MARKERS, REQUIRED_FIELDS,
        )
        self._check("gate_fixture_markers_10", lambda: len(REQUIRED_MARKERS) == 10)
        self._check("gate_fixture_markers_all_true", lambda: all(v is True for v in REQUIRED_MARKERS.values()))
        self._check("gate_fixture_has_small_capital_only", lambda: "small_capital_strategy_only" in REQUIRED_MARKERS)

        # ── Fixture registry ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.fixture_registry_v170 import (
            count_fixtures, FIXTURE_REGISTRY,
        )
        self._check("gate_fixture_registry_80", lambda: count_fixtures() == 80)
        self._check("gate_fixture_registry_sc_001", lambda: "sc_001" in FIXTURE_REGISTRY)
        self._check("gate_fixture_registry_sc_080", lambda: "sc_080" in FIXTURE_REGISTRY)

        # ── Scenario registry ──────────────────────────────────────────────
        from paper_trading.small_capital_strategy.scenario_registry_v170 import (
            SCENARIO_REGISTRY,
        )
        self._check("gate_scenario_registry_80", lambda: len(SCENARIO_REGISTRY) == 80)
        self._check("gate_scenario_list_type", lambda: isinstance(SCENARIO_REGISTRY, list))

        # ── Strategy template ──────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_template_v170 import (
            build_300k_template, validate_strategy_template,
        )
        tmpl = build_300k_template(regime=MarketRegime.BULL)
        self._check("gate_template_build", lambda: tmpl is not None)
        self._check("gate_template_valid", lambda: validate_strategy_template(tmpl)["valid"] is True)
        self._check("gate_template_paper_only", lambda: tmpl.paper_only is True)

        # ── Strategy report ────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.strategy_report_v170 import (
            build_report, to_markdown, to_json, to_csv, get_section_names,
        )
        scorecard = compute_scorecard(TEMPLATE_300K_ID, {k: 0.8 for k in SCORE_WEIGHTS})
        report = build_report(TEMPLATE_300K_ID, scorecard)
        self._check("gate_report_build", lambda: report is not None)
        self._check("gate_report_markdown", lambda: "Not Investment Advice" in to_markdown(report))
        self._check("gate_report_json", lambda: "template_id" in to_json(report))
        self._check("gate_report_csv", lambda: "template_id" in to_csv(report))
        self._check("gate_report_sections_15", lambda: len(get_section_names()) == 15)

        # ── Paper simulation ───────────────────────────────────────────────
        from paper_trading.small_capital_strategy.paper_simulation_bridge_v170 import (
            get_simulation_safety_summary,
        )
        sim_safety = get_simulation_safety_summary()
        self._check("gate_sim_real_exec_false", lambda: sim_safety["real_execution_enabled"] is False)
        self._check("gate_sim_broker_false", lambda: sim_safety["broker_connected"] is False)
        self._check("gate_sim_paper_only", lambda: sim_safety["paper_only"] is True)

        # ── Backward compat ────────────────────────────────────────────────
        self._check("gate_compat_known_v169", lambda: is_known_release("Live Paper Trading Stable Rollup"))
        self._check("gate_compat_known_v168", lambda: is_known_release("Operational Integration Hardening"))
        self._check("gate_compat_known_v167", lambda: is_known_release("Paper Performance Attribution"))
        self._check("gate_compat_min_version_pass", lambda: check_minimum_version("1.7.0"))

        # ── ABC buy points ─────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.enums_v170 import BuyPointType
        from paper_trading.small_capital_strategy.buy_point_rules_v170 import (
            check_a_buy_point, check_b_buy_point, check_c_buy_point,
        )
        a_sig = {
            "theme_strength": "STRONG", "close_gt_ma20": True, "close_gt_ma60": True,
            "low_lte_ma10": True, "close_gte_ma10": True, "volume_contracting": True,
            "kd_not_dead_cross": True, "institutional_not_net_selling": True,
            "financing_not_overheated": True,
        }
        self._check("gate_abc_a_buy_point_passes", lambda: check_a_buy_point(a_sig)["passed"] is True)
        self._check("gate_abc_a_buy_point_type", lambda: check_a_buy_point(a_sig)["buy_point_type"] == BuyPointType.A_10MA_PULLBACK.value)

        # ── Exit plan ──────────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.exit_plan_v170 import build_exit_plan, validate_exit_plan
        exit_plan = build_exit_plan("2330", "SWING")
        self._check("gate_exit_plan_build", lambda: exit_plan is not None)
        self._check("gate_exit_plan_paper_only", lambda: exit_plan.paper_only is True)
        self._check("gate_exit_plan_valid", lambda: validate_exit_plan(exit_plan)["valid"] is True)

        # ── Health check passes ────────────────────────────────────────────
        from paper_trading.small_capital_strategy.health_v170 import run_health_check
        health = run_health_check()
        self._check("gate_health_all_passed", lambda: health["all_passed"] is True)
        self._check("gate_health_passed_gte_80", lambda: health["passed"] >= 80)
        self._check("gate_health_failed_zero", lambda: health["failed"] == 0)

        passed = [c for c in self._checks if c["passed"]]
        failed = [c for c in self._checks if not c["passed"]]
        gate_passed = len(failed) == 0

        return {
            "gate_version": GATE_VERSION,
            "checks": self._checks,
            "passed_count": len(passed),
            "failed_count": len(failed),
            "total_count": len(self._checks),
            "gate_passed": gate_passed,
            "paper_only": True,
            "research_only": True,
            "no_real_orders": True,
            "not_investment_advice": True,
        }


def run_release_gate() -> Dict[str, Any]:
    """Convenience function to run the release gate and return result."""
    return SmallCapitalGrowthStrategyReleaseGate().run()
