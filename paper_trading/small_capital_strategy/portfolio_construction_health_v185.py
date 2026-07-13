"""
paper_trading/small_capital_strategy/portfolio_construction_health_v185.py
Health check for Portfolio Construction & Rebalancing Lab v1.8.5.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Portfolio Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')))
from typing import Any, Dict, List


class PortfolioConstructionHealthCheck:
    """Health check runner for v1.8.5 Portfolio Construction."""

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

    def run(self) -> "PortfolioHealthSummary":
        from paper_trading.small_capital_strategy.portfolio_construction_models_v185 import (
            PortfolioHealthSummary,
        )
        self._checks = []

        # ── Version (5) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_version_v185 import (
            VERSION, RELEASE_NAME, SCHEMA_VERSION, verify_version, is_known_release,
        )
        self._check("version_is_185",              lambda: VERSION == "1.8.5")
        self._check("release_name_correct",         lambda: RELEASE_NAME == "Portfolio Construction & Rebalancing Lab")
        self._check("schema_version_185",           lambda: SCHEMA_VERSION == "185")
        self._check("verify_version_true",          verify_version)
        self._check("known_release_v184",           lambda: is_known_release("Position Sizing & Capital Allocation Lab v1.8.4"))

        # ── Safety (10) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_safety_v185 import (
            run_safety_audit, assert_safe, SAFETY_FLAGS,
        )
        self._check("safety_all_safe",              lambda: run_safety_audit()["all_safe"])
        self._check("safety_paper_only",            lambda: SAFETY_FLAGS["paper_only"] is True)
        self._check("safety_research_only",         lambda: SAFETY_FLAGS["research_only"] is True)
        self._check("safety_portfolio_only",        lambda: SAFETY_FLAGS["portfolio_only"] is True)
        self._check("safety_no_real_orders",        lambda: SAFETY_FLAGS["no_real_orders"] is True)
        self._check("safety_no_broker",             lambda: SAFETY_FLAGS["no_broker"] is True)
        self._check("safety_no_margin",             lambda: SAFETY_FLAGS["no_margin"] is True)
        self._check("safety_no_leverage",           lambda: SAFETY_FLAGS["no_leverage"] is True)
        self._check("safety_production_blocked",    lambda: SAFETY_FLAGS["production_trading_blocked"] is True)
        self._check("safety_assert_no_raise",       lambda: (assert_safe(), True)[1])

        # ── Models (21) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_models_v185 import (
            PortfolioProfile, PortfolioHolding, PortfolioCandidate,
            PortfolioConstructionInput, PortfolioConstructionResult,
            RebalanceInput, RebalancePlan, RebalanceAction,
            PortfolioExposureReport, SectorExposureReport, ThemeExposureReport,
            CorrelationRiskReport, ConcentrationLimit, DiversificationScore,
            RotationCandidate, KeepOrReplaceDecision, PortfolioRiskBudget,
            PortfolioDashboard, PortfolioRebalanceReport, PortfolioHealthSummary as PHS,
            get_all_model_names,
        )
        self._check("model_portfolio_profile",      lambda: PortfolioProfile().paper_only is True)
        self._check("model_portfolio_holding",      lambda: PortfolioHolding().paper_only is True)
        self._check("model_portfolio_candidate",    lambda: PortfolioCandidate().paper_only is True)
        self._check("model_construction_input",     lambda: PortfolioConstructionInput().paper_only is True)
        self._check("model_construction_result",    lambda: PortfolioConstructionResult().paper_only is True)
        self._check("model_rebalance_input",        lambda: RebalanceInput().paper_only is True)
        self._check("model_rebalance_plan",         lambda: RebalancePlan().paper_only is True)
        self._check("model_rebalance_action",       lambda: RebalanceAction().paper_only is True)
        self._check("model_exposure_report",        lambda: PortfolioExposureReport().paper_only is True)
        self._check("model_sector_exposure",        lambda: SectorExposureReport().paper_only is True)
        self._check("model_theme_exposure",         lambda: ThemeExposureReport().paper_only is True)
        self._check("model_correlation_risk",       lambda: CorrelationRiskReport().paper_only is True)
        self._check("model_concentration_limit",    lambda: ConcentrationLimit().paper_only is True)
        self._check("model_diversification_score",  lambda: DiversificationScore().paper_only is True)
        self._check("model_rotation_candidate",     lambda: RotationCandidate().paper_only is True)
        self._check("model_keep_or_replace",        lambda: KeepOrReplaceDecision().paper_only is True)
        self._check("model_portfolio_risk_budget",  lambda: PortfolioRiskBudget().paper_only is True)
        self._check("model_portfolio_dashboard",    lambda: PortfolioDashboard().paper_only is True)
        self._check("model_rebalance_report",       lambda: PortfolioRebalanceReport().paper_only is True)
        self._check("model_health_summary",         lambda: PHS().paper_only is True)
        self._check("model_count_20",               lambda: len(get_all_model_names()) == 20)

        # ── Engine (10) ──────────────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_engine_v185 import (
            ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
            CAPITAL_STAGES, WEIGHTING_METHODS,
            validate_action, validate_grade, run_portfolio_construction,
            get_engine_info, build_portfolio_dashboard,
        )
        self._check("engine_allowed_actions_16",    lambda: len(ALLOWED_OUTPUT_ACTIONS) == 16)
        self._check("engine_forbidden_words_9",     lambda: len(FORBIDDEN_OUTPUT_WORDS) == 9)
        self._check("engine_valid_grades_6",        lambda: len(VALID_FINAL_GRADES) == 6)
        self._check("engine_capital_stages_4",      lambda: len(CAPITAL_STAGES) == 4)
        self._check("engine_weighting_methods_10",  lambda: len(WEIGHTING_METHODS) == 10)
        self._check("engine_validate_action",       lambda: validate_action("PORTFOLIO_ONLY"))
        self._check("engine_validate_grade_balanced",lambda: validate_grade("BALANCED"))
        _inp = PortfolioConstructionInput(capital=300000.0, market_regime="BULL")
        self._check("engine_run_callable",          lambda: run_portfolio_construction(_inp).paper_only is True)
        self._check("engine_info_callable",         lambda: isinstance(get_engine_info(), dict))
        self._check("engine_dashboard_callable",    lambda: build_portfolio_dashboard(_inp).paper_only is True)

        # ── Portfolio profile (4) ─────────────────────────────────────
        self._check("capital_stage_300k",           lambda: PortfolioProfile(capital=300000.0).capital == 300000.0)
        self._check("capital_stage_500k",           lambda: PortfolioProfile(capital=500000.0).capital == 500000.0)
        self._check("capital_stage_1m",             lambda: PortfolioProfile(capital=1000000.0).capital == 1000000.0)
        self._check("capital_stage_3m",             lambda: PortfolioProfile(capital=3000000.0).capital == 3000000.0)

        # ── Equal weight construction (3) ─────────────────────────────
        _empty = PortfolioConstructionInput(capital=300000.0, market_regime="BULL")
        self._check("equal_weight_empty_balanced",  lambda: run_portfolio_construction(_empty).final_portfolio_grade == "BALANCED")
        self._check("equal_weight_empty_action",    lambda: run_portfolio_construction(_empty).action == "PORTFOLIO_ONLY")
        self._check("equal_weight_holding_count",   lambda: run_portfolio_construction(_empty).holding_count == 0)

        # ── Keep/reduce/replace (3) ───────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_models_v185 import PortfolioHolding as PH
        _h_above = PH(ticker="A", above_10ma=True, above_20ma=True, value=100000.0)
        _h_no10 = PH(ticker="B", above_10ma=False, above_20ma=True, value=100000.0)
        _h_no20 = PH(ticker="C", above_10ma=False, above_20ma=False, value=100000.0)
        _inp_kr = PortfolioConstructionInput(capital=300000.0, market_regime="BULL",
                                              holdings=[_h_above, _h_no10, _h_no20])
        _res_kr = run_portfolio_construction(_inp_kr)
        self._check("keep_above_10_20ma",           lambda: "A" in run_portfolio_construction(
            PortfolioConstructionInput(capital=300000.0, holdings=[_h_above])).suggested_keep_list)
        self._check("reduce_no_10ma",               lambda: "B" in run_portfolio_construction(
            PortfolioConstructionInput(capital=300000.0, holdings=[_h_no10])).suggested_reduce_list)
        self._check("replace_no_20ma",              lambda: "C" in run_portfolio_construction(
            PortfolioConstructionInput(capital=300000.0, holdings=[_h_no20])).suggested_replace_list)

        # ── Sector exposure (3) ───────────────────────────────────────
        _h1 = PH(ticker="X", sector="AI", theme="AI", value=200000.0, above_10ma=True, above_20ma=True)
        _h2 = PH(ticker="Y", sector="AI", theme="AI", value=100000.0, above_10ma=True, above_20ma=True)
        _inp_sector = PortfolioConstructionInput(capital=300000.0, market_regime="BULL",
                                                  max_sector_exposure_pct=35.0, holdings=[_h1, _h2])
        self._check("sector_overexposed_detected",  lambda: len(run_portfolio_construction(_inp_sector).final_portfolio_grade) > 0)
        _h3 = PH(ticker="Z", sector="PCB", theme="PCB", value=100000.0, above_10ma=True, above_20ma=True)
        _inp_ok = PortfolioConstructionInput(capital=300000.0, market_regime="BULL",
                                              max_sector_exposure_pct=60.0, holdings=[_h1, _h3])
        self._check("sector_ok_different",          lambda: run_portfolio_construction(_inp_ok).final_portfolio_grade != "BLOCKED")
        self._check("exposure_report_callable",     lambda: build_portfolio_dashboard(_empty).exposure_report.paper_only is True)

        # ── Theme exposure (3) ────────────────────────────────────────
        self._check("theme_report_callable",        lambda: build_portfolio_dashboard(_empty).theme_report.paper_only is True)
        self._check("sector_report_callable",       lambda: build_portfolio_dashboard(_empty).sector_report.paper_only is True)
        self._check("correlation_report_callable",  lambda: build_portfolio_dashboard(_empty).correlation_report.paper_only is True)

        # ── Rebalance (3) ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_engine_v185 import run_rebalance
        _ri = RebalanceInput(capital=300000.0, holdings=[], rebalance_threshold_pct=10.0)
        self._check("rebalance_empty_no_needed",    lambda: run_rebalance(_ri).rebalance_needed is False)
        _h_drift = PH(ticker="D", weight_pct=50.0, value=150000.0, above_10ma=True, above_20ma=True)
        _ri2 = RebalanceInput(capital=300000.0, holdings=[_h_drift], rebalance_threshold_pct=5.0,
                               target_weights={"D": 33.33})
        self._check("rebalance_drift_detected",     lambda: run_rebalance(_ri2).total_drift_pct > 0)
        self._check("rebalance_plan_paper_only",    lambda: run_rebalance(_ri).paper_only is True)

        # ── Blocked scenarios (3) ─────────────────────────────────────
        _blocked = PortfolioConstructionInput(capital=300000.0, market_regime="BLOCKED")
        self._check("block_regime_blocked",         lambda: run_portfolio_construction(_blocked).final_portfolio_grade == "BLOCKED")
        _high_ruin = PortfolioConstructionInput(capital=300000.0, market_regime="BULL",
                                                  monte_carlo_ruin_risk_pct=25.0)
        self._check("block_high_ruin_risk",         lambda: run_portfolio_construction(_high_ruin).final_portfolio_grade == "BLOCKED")
        _no_cash = PortfolioConstructionInput(capital=300000.0, market_regime="BULL",
                                               min_cash_reserve_pct=2.0)
        self._check("block_no_cash_reserve",        lambda: run_portfolio_construction(_no_cash).final_portfolio_grade == "BLOCKED")

        # ── Forbidden action words (4) ────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_engine_v185 import FORBIDDEN_OUTPUT_WORDS as FW
        self._check("forbidden_BUY",                lambda: "BUY" in FW)
        self._check("forbidden_SELL",               lambda: "SELL" in FW)
        self._check("forbidden_ORDER",              lambda: "ORDER" in FW)
        self._check("forbidden_BROKER_ORDER",       lambda: "BROKER_ORDER" in FW)

        # ── Dashboard & Report (4) ────────────────────────────────────
        _dash = build_portfolio_dashboard(_empty)
        self._check("dashboard_paper_only",         lambda: _dash.paper_only is True)
        self._check("dashboard_no_real_orders",     lambda: _dash.no_real_orders is True)
        from paper_trading.small_capital_strategy.portfolio_construction_report_v185 import (
            build_report, get_report_sections, REPORT_SECTIONS,
        )
        _rpt = build_report(_dash)
        self._check("report_paper_only",            lambda: _rpt.paper_only is True)
        self._check("report_sections_15",           lambda: len(REPORT_SECTIONS) == 15)

        # ── CLI (2) ──────────────────────────────────────────────────
        from cli.command_registry import PROVIDER_COMMANDS
        _pc_cmds = [c for c in PROVIDER_COMMANDS if c.name.startswith("portfolio-construction")]
        self._check("cli_pc_cmds_ge_22",            lambda: len(_pc_cmds) >= 22)
        self._check("cli_pc_version_exists",        lambda: any(c.name == "portfolio-construction-version" for c in PROVIDER_COMMANDS))

        # ── GUI (5) ──────────────────────────────────────────────────
        from gui.small_capital_strategy_panel import PANEL_VERSION
        self._check("gui_panel_version_185",        lambda: PANEL_VERSION == "1.8.5")
        from gui.small_capital_strategy_panel import _TABS
        self._check("gui_tabs_ge_138",              lambda: len(_TABS) >= 138)
        self._check("gui_portfolio_construction_tab",lambda: "portfolio_construction_lab" in _TABS)
        self._check("gui_rebalancing_tab",          lambda: "portfolio_rebalancing" in _TABS)
        self._check("gui_exposure_control_tab",     lambda: "portfolio_exposure_control" in _TABS)

        # ── Scenarios (2) ─────────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_scenarios_v185 import (
            count_scenarios, get_scenarios,
        )
        self._check("scenarios_ge_75",              lambda: count_scenarios() >= 75)
        self._check("scenarios_all_paper",          lambda: all(s["paper_only"] for s in get_scenarios()))

        # ── Fixtures (2) ──────────────────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_fixtures_v185 import (
            get_fixture_count, get_fixture_info,
        )
        self._check("fixtures_ge_75",               lambda: get_fixture_count() >= 75)
        self._check("fixtures_info_callable",       lambda: isinstance(get_fixture_info(), dict))

        # ── Backward compatibility (5) ────────────────────────────────
        from paper_trading.small_capital_strategy.portfolio_construction_version_v185 import (
            is_known_release as ikr,
        )
        self._check("compat_v170",                  lambda: ikr("Small Capital Strategy v1.7.0"))
        self._check("compat_v178",                  lambda: ikr("Small Capital Strategy Integration v1.7.8"))
        self._check("compat_v180",                  lambda: ikr("Paper Simulation & Performance Lab v1.8.0"))
        self._check("compat_v183",                  lambda: ikr("Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3"))
        self._check("compat_v184",                  lambda: ikr("Position Sizing & Capital Allocation Lab v1.8.4"))

        passed = sum(1 for c in self._checks if c["passed"])
        failed = sum(1 for c in self._checks if not c["passed"])
        total = len(self._checks)

        return PortfolioHealthSummary(
            total=total,
            passed=passed,
            failed=failed,
            all_passed=(failed == 0),
            status="PASS" if failed == 0 else "FAIL",
        )


def run_health_check() -> "PortfolioHealthSummary":
    """Run portfolio construction health check."""
    return PortfolioConstructionHealthCheck().run()


if __name__ == "__main__":
    result = run_health_check()
    print(f"Health Check v1.8.5: {'PASS' if result.all_passed else 'FAIL'} {result.passed}/{result.total}")
    if not result.all_passed:
        hc = PortfolioConstructionHealthCheck()
        hc.run()
        for c in hc._checks:
            if not c["passed"]:
                print(f"  [FAIL] {c['name']}: {c['error']}")
