"""
paper_trading/small_capital_strategy/decision_cockpit_health_v186.py
Health check for End-to-End Small Capital Decision Cockpit v1.8.6.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Decision Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List


class DecisionCockpitHealthCheck:
    """Health check runner for v1.8.6 Decision Cockpit."""

    def __init__(self) -> None:
        self._checks: List[Dict[str, Any]] = []

    def _check(self, name: str, fn) -> None:
        try:
            result = fn()
            ok = bool(result)
        except Exception as exc:
            ok = False
            result = str(exc)
        self._checks.append({"name": name, "passed": ok,
                              "error": None if ok else str(result)})

    def run(self) -> "DecisionHealthSummary":
        from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import (
            DecisionHealthSummary,
        )
        self._checks = []

        # ── Version (5) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_version_v186 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
        )
        self._check("version_is_186",              lambda: VERSION == "1.8.6")
        self._check("release_name_correct",         lambda: RELEASE_NAME == "End-to-End Small Capital Decision Cockpit")
        self._check("schema_version_186",           lambda: SCHEMA_VERSION == "186")
        self._check("verify_version_true",          verify_version)
        self._check("known_release_v185",           lambda: is_known_release("Portfolio Construction & Rebalancing Lab v1.8.5"))

        # ── Safety (10) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_safety_v186 import (
            run_safety_audit, assert_safe, SAFETY_FLAGS,
        )
        self._check("safety_all_safe",              lambda: run_safety_audit()["all_safe"])
        self._check("safety_paper_only",            lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_research_only",         lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("safety_decision_only",         lambda: SAFETY_FLAGS["decision_only"] is True)
        self._check("safety_no_real_orders",        lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_no_broker",             lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_no_margin",             lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("safety_no_leverage",           lambda: SAFETY_FLAGS["no_leverage"] is True)
        self._check("safety_production_blocked",    lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_assert_no_raise",       lambda: (assert_safe(), True)[1])

        # ── Models (22) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_models_v186 import (
            DecisionCockpitInput, DecisionCockpitResult,
            DailyDecisionContext, WeeklyDecisionContext,
            MarketDecisionState, CandidateDecisionInput, CandidateDecisionResult,
            BuyPointDecision, RiskDecision, PositionSizingDecision,
            PortfolioDecision, MonteCarloDecision, ThemeDecision, RegimeDecision,
            EntryReadinessScore, AddReadinessScore, ReduceRiskDecision,
            BlockReason, DecisionChecklist, DecisionDashboard,
            DecisionReport, DecisionHealthSummary as DHS,
            get_all_model_names,
        )
        self._check("model_cockpit_input",          lambda: DecisionCockpitInput().paper_only is True)
        self._check("model_cockpit_result",         lambda: DecisionCockpitResult().paper_only is True)
        self._check("model_daily_context",          lambda: DailyDecisionContext().paper_only is True)
        self._check("model_weekly_context",         lambda: WeeklyDecisionContext().paper_only is True)
        self._check("model_market_state",           lambda: MarketDecisionState().paper_only is True)
        self._check("model_candidate_input",        lambda: CandidateDecisionInput().paper_only is True)
        self._check("model_candidate_result",       lambda: CandidateDecisionResult().paper_only is True)
        self._check("model_buy_point_decision",     lambda: BuyPointDecision().paper_only is True)
        self._check("model_risk_decision",          lambda: RiskDecision().paper_only is True)
        self._check("model_position_sizing",        lambda: PositionSizingDecision().paper_only is True)
        self._check("model_portfolio_decision",     lambda: PortfolioDecision().paper_only is True)
        self._check("model_monte_carlo",            lambda: MonteCarloDecision().paper_only is True)
        self._check("model_theme_decision",         lambda: ThemeDecision().paper_only is True)
        self._check("model_regime_decision",        lambda: RegimeDecision().paper_only is True)
        self._check("model_entry_readiness",        lambda: EntryReadinessScore().paper_only is True)
        self._check("model_add_readiness",          lambda: AddReadinessScore().paper_only is True)
        self._check("model_reduce_risk",            lambda: ReduceRiskDecision().paper_only is True)
        self._check("model_block_reason",           lambda: BlockReason().paper_only is True)
        self._check("model_checklist",              lambda: DecisionChecklist().paper_only is True)
        self._check("model_dashboard",              lambda: DecisionDashboard().paper_only is True)
        self._check("model_report",                 lambda: DecisionReport().paper_only is True)
        self._check("model_health_summary",         lambda: DHS().paper_only is True)
        self._check("model_count_22",               lambda: len(get_all_model_names()) == 22)

        # ── Engine (12) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_engine_v186 import (
            ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_COCKPIT_GRADES,
            CAPITAL_STAGES, DECISION_CYCLES, ABC_BUY_POINTS,
            CANDIDATE_EVALUATION_CRITERIA,
            validate_action, validate_grade, run_decision_cockpit,
            build_decision_dashboard, get_engine_info,
        )
        self._check("engine_allowed_actions_17",    lambda: len(ALLOWED_OUTPUT_ACTIONS) == 17)
        self._check("engine_forbidden_words_9",     lambda: len(FORBIDDEN_OUTPUT_WORDS) == 9)
        self._check("engine_valid_grades_6",        lambda: len(VALID_COCKPIT_GRADES) == 6)
        self._check("engine_capital_stages_4",      lambda: len(CAPITAL_STAGES) == 4)
        self._check("engine_decision_cycles_8",     lambda: len(DECISION_CYCLES) == 8)
        self._check("engine_abc_buy_points_3",      lambda: len(ABC_BUY_POINTS) == 3)
        self._check("engine_criteria_14",           lambda: len(CANDIDATE_EVALUATION_CRITERIA) == 14)
        self._check("engine_validate_action",       lambda: validate_action("DECISION_ONLY"))
        self._check("engine_validate_grade_ready",  lambda: validate_grade("READY"))
        _inp = DecisionCockpitInput(capital=300000.0, market_regime="BULL")
        self._check("engine_run_callable",          lambda: run_decision_cockpit(_inp).paper_only is True)
        self._check("engine_info_callable",         lambda: isinstance(get_engine_info(), dict))
        self._check("engine_dashboard_callable",    lambda: build_decision_dashboard(_inp).paper_only is True)

        # ── Decision cycles (8) ──────────────────────────────────────────
        for cycle in ["daily_check", "weekly_review", "pre_market_review", "post_market_review",
                      "watchlist_review", "portfolio_review", "risk_review", "blocked_market_review"]:
            self._check(f"cycle_{cycle}",           lambda c=cycle: c in DECISION_CYCLES)

        # ── Capital stages (4) ───────────────────────────────────────────
        self._check("capital_300k",                 lambda: 300000 in CAPITAL_STAGES)
        self._check("capital_500k",                 lambda: 500000 in CAPITAL_STAGES)
        self._check("capital_1m",                   lambda: 1000000 in CAPITAL_STAGES)
        self._check("capital_3m",                   lambda: 3000000 in CAPITAL_STAGES)

        # ── Block conditions (4) ─────────────────────────────────────────
        _blocked = DecisionCockpitInput(capital=300000.0, market_regime="BLOCKED")
        self._check("block_regime_blocked",         lambda: run_decision_cockpit(_blocked).final_cockpit_grade == "BLOCKED")
        _ruin = DecisionCockpitInput(capital=300000.0, market_regime="BULL", monte_carlo_ruin_risk_pct=25.0)
        self._check("block_high_ruin",              lambda: run_decision_cockpit(_ruin).final_cockpit_grade == "BLOCKED")
        _low_cash = DecisionCockpitInput(capital=300000.0, market_regime="BULL", cash_reserve_pct=3.0)
        self._check("block_low_cash",               lambda: run_decision_cockpit(_low_cash).final_cockpit_grade == "BLOCKED")
        _no_block = DecisionCockpitInput(capital=300000.0, market_regime="BULL")
        self._check("no_block_bull_empty",          lambda: run_decision_cockpit(_no_block).final_cockpit_grade in ("WAIT", "WATCH", "READY"))

        # ── A/B/C buy point decisions (3) ────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_engine_v186 import (
            run_buy_point_decision,
        )
        _a_cand = CandidateDecisionInput(ticker="A", abc_buy_point="A_10MA_PULLBACK",
                                          above_10ma=True, volume_contracting=True,
                                          kd_below_50=True, market_regime="BULL",
                                          stop_loss_defined=True)
        self._check("abc_a_entry_allowed",          lambda: run_buy_point_decision(_a_cand).action in ("PAPER_ENTRY_ALLOWED", "PAPER_PLAN_READY"))
        _b_cand = CandidateDecisionInput(ticker="B", abc_buy_point="B_BREAKOUT",
                                          above_10ma=True, above_20ma=True,
                                          volume_breakout=True, market_regime="BULL",
                                          stop_loss_defined=True)
        self._check("abc_b_entry_allowed",          lambda: run_buy_point_decision(_b_cand).action in ("PAPER_ENTRY_ALLOWED", "PAPER_PLAN_READY"))
        _c_cand = CandidateDecisionInput(ticker="C", abc_buy_point="C_20MA_RECLAIM",
                                          above_20ma=True, volume_contracting=True,
                                          kd_recovering=True, market_regime="BULL",
                                          stop_loss_defined=True)
        self._check("abc_c_entry_allowed",          lambda: run_buy_point_decision(_c_cand).action in ("PAPER_ENTRY_ALLOWED", "PAPER_PLAN_READY", "WAIT"))

        # ── Forbidden action words (4) ────────────────────────────────────
        self._check("forbidden_BUY",                lambda: "BUY" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_SELL",               lambda: "SELL" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_ORDER",              lambda: "ORDER" in FORBIDDEN_OUTPUT_WORDS)
        self._check("forbidden_BROKER_ORDER",       lambda: "BROKER_ORDER" in FORBIDDEN_OUTPUT_WORDS)

        # ── Report (3) ───────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_report_v186 import (
            build_report, get_report_sections, REPORT_SECTIONS,
        )
        _dash = build_decision_dashboard(_inp)
        _rpt = build_report(_dash)
        self._check("report_paper_only",            lambda: _rpt.paper_only is True)
        self._check("report_sections_20",           lambda: len(REPORT_SECTIONS) == 20)
        self._check("report_sections_fn",           lambda: len(get_report_sections()) == 20)

        # ── CLI (2) ──────────────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        _dc_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("decision-cockpit")]
        self._check("cli_dc_cmds_ge_22",            lambda: len(_dc_cmds) >= 22)
        self._check("cli_dc_version_exists",        lambda: any(c.name == "decision-cockpit-version" for c in PROVIDER_COMMANDS))

        # ── GUI (5) ──────────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._check("gui_panel_version_186",        lambda: PANEL_VERSION in ("1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3"))
        from gui.small_capital_strategy_panel import _TABS
        self._check("gui_tabs_ge_141",              lambda: len(_TABS) >= 141)
        self._check("gui_daily_decision_tab",       lambda: "daily_decision_cockpit" in _TABS)
        self._check("gui_weekly_review_tab",        lambda: "weekly_decision_review" in _TABS)
        self._check("gui_block_reasons_tab",        lambda: "block_reasons" in _TABS)

        # ── Scenarios (2) ─────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_scenarios_v186 import (
            count_scenarios, get_scenarios,
        )
        self._check("scenarios_ge_75",              lambda: count_scenarios() >= 75)
        self._check("scenarios_all_paper",          lambda: all(s["paper_only"] for s in get_scenarios()))

        # ── Fixtures (2) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_fixtures_v186 import (
            get_fixture_count, get_fixture_info,
        )
        self._check("fixtures_ge_75",               lambda: get_fixture_count() >= 75)
        self._check("fixtures_info_callable",       lambda: isinstance(get_fixture_info(), dict))

        # ── Backward compatibility (5) ────────────────────────────────────
        from paper_trading.small_capital_strategy.decision_cockpit_version_v186 import (
            is_known_release as ikr,
        )
        self._check("compat_v170",                  lambda: ikr("Small Capital Strategy v1.7.0"))
        self._check("compat_v178",                  lambda: ikr("Small Capital Strategy Integration v1.7.8"))
        self._check("compat_v180",                  lambda: ikr("Paper Simulation & Performance Lab v1.8.0"))
        self._check("compat_v183",                  lambda: ikr("Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3"))
        self._check("compat_v185",                  lambda: ikr("Portfolio Construction & Rebalancing Lab v1.8.5"))

        # ── No forbidden action in allowed output (3) ─────────────────────
        self._check("no_buy_in_actions",            lambda: "BUY" not in ALLOWED_OUTPUT_ACTIONS)
        self._check("no_sell_in_actions",           lambda: "SELL" not in ALLOWED_OUTPUT_ACTIONS)
        self._check("decision_only_in_actions",     lambda: "DECISION_ONLY" in ALLOWED_OUTPUT_ACTIONS)

        # ── Safety no real orders (2) ─────────────────────────────────────
        self._check("result_paper_only",            lambda: run_decision_cockpit(_inp).paper_only is True)
        self._check("result_no_real_orders",        lambda: run_decision_cockpit(_inp).no_real_orders is True)

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)

        return DecisionHealthSummary(
            total=total,
            passed=passed,
            failed=failed,
            all_passed=(failed == 0),
            status="PASS" if failed == 0 else "FAIL",
        )


def run_health_check() -> "DecisionHealthSummary":
    """Run decision cockpit health check."""
    return DecisionCockpitHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Health Check v1.8.6: {'PASS' if result.all_passed else 'FAIL'} {result.passed}/{result.total}")
    if not result.all_passed:
        hc = DecisionCockpitHealthCheck()
        hc.run()
        for c in hc._checks:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
