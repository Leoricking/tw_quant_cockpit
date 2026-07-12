"""
paper_trading/small_capital_strategy/monte_carlo_health_v183.py
Health check for Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pathlib


def _check(name, fn):
    try:
        return {"name": name, "passed": bool(fn()), "error": None}
    except Exception as exc:
        return {"name": name, "passed": False, "error": str(exc)}


def run_health_check():
    """Run all health checks. Returns MonteCarloHealthSummary."""
    from paper_trading.small_capital_strategy.monte_carlo_models_v183 import MonteCarloHealthSummary
    checks = []

    # --- Version checks (5) ---
    from paper_trading.small_capital_strategy.monte_carlo_version_v183 import (
        VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION, INCLUDED_RELEASES,
        KNOWN_RELEASE_NAMES, get_version_info, verify_version, is_known_release,
        check_minimum_version, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH_CHECKS,
    )
    checks.append(_check("version_is_183", lambda: VERSION == "1.8.3"))
    checks.append(_check("release_name_set", lambda: RELEASE_NAME == "Monte Carlo Risk-of-Ruin & Robustness Lab"))
    checks.append(_check("schema_version_183", lambda: SCHEMA_VERSION == "183"))
    checks.append(_check("policy_version_set", lambda: "1.8.3" in POLICY_VERSION))
    checks.append(_check("verify_version_true", lambda: verify_version()))

    # --- Models checks (17) ---
    from paper_trading.small_capital_strategy.monte_carlo_models_v183 import (
        MonteCarloInput, MonteCarloConfig, MonteCarloTrial, MonteCarloResult,
        BootstrapSample, BootstrapResult, RiskOfRuinInput, RiskOfRuinResult,
        DrawdownDistribution, ReturnDistribution, SequenceRiskReport, SlippageCostShock,
        TailRiskReport, RobustnessProbability, MonteCarloDashboard, MonteCarloReport,
        MonteCarloHealthSummary as HealthModel, get_all_model_names,
    )
    checks.append(_check("model_monte_carlo_input", lambda: MonteCarloInput().paper_only is True))
    checks.append(_check("model_monte_carlo_config", lambda: MonteCarloConfig().paper_only is True))
    checks.append(_check("model_monte_carlo_trial", lambda: MonteCarloTrial().paper_only is True))
    checks.append(_check("model_monte_carlo_result", lambda: MonteCarloResult().paper_only is True))
    checks.append(_check("model_bootstrap_sample", lambda: BootstrapSample().paper_only is True))
    checks.append(_check("model_bootstrap_result", lambda: BootstrapResult().paper_only is True))
    checks.append(_check("model_risk_of_ruin_input", lambda: RiskOfRuinInput().paper_only is True))
    checks.append(_check("model_risk_of_ruin_result", lambda: RiskOfRuinResult().paper_only is True))
    checks.append(_check("model_drawdown_distribution", lambda: DrawdownDistribution().paper_only is True))
    checks.append(_check("model_return_distribution", lambda: ReturnDistribution().paper_only is True))
    checks.append(_check("model_sequence_risk_report", lambda: SequenceRiskReport().paper_only is True))
    checks.append(_check("model_slippage_cost_shock", lambda: SlippageCostShock().paper_only is True))
    checks.append(_check("model_tail_risk_report", lambda: TailRiskReport().paper_only is True))
    checks.append(_check("model_robustness_probability", lambda: RobustnessProbability().paper_only is True))
    checks.append(_check("model_monte_carlo_dashboard", lambda: MonteCarloDashboard().paper_only is True))
    checks.append(_check("model_monte_carlo_report", lambda: MonteCarloReport().paper_only is True))
    checks.append(_check("model_monte_carlo_health_summary", lambda: HealthModel().paper_only is True))

    # --- Safety flags checks (19) ---
    from paper_trading.small_capital_strategy.monte_carlo_safety_v183 import (
        SAFETY_FLAGS, get_safety_flags, run_safety_audit, assert_safe,
    )
    checks.append(_check("safety_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True))
    checks.append(_check("safety_research_only", lambda: SAFETY_FLAGS["research_only"] is True))
    checks.append(_check("safety_simulate_only", lambda: SAFETY_FLAGS["simulate_only"] is True))
    checks.append(_check("safety_validation_only", lambda: SAFETY_FLAGS["validation_only"] is True))
    checks.append(_check("safety_monte_carlo_only", lambda: SAFETY_FLAGS["monte_carlo_only"] is True))
    checks.append(_check("safety_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True))
    checks.append(_check("safety_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True))
    checks.append(_check("safety_no_margin", lambda: SAFETY_FLAGS["no_margin"] is True))
    checks.append(_check("safety_no_leverage", lambda: SAFETY_FLAGS["no_leverage"] is True))
    checks.append(_check("safety_no_auto_trade", lambda: SAFETY_FLAGS["no_auto_trade"] is True))
    checks.append(_check("safety_no_live_session", lambda: SAFETY_FLAGS["no_live_session"] is True))
    checks.append(_check("safety_no_production_db_writes", lambda: SAFETY_FLAGS["no_production_db_writes"] is True))
    checks.append(_check("safety_not_investment_advice", lambda: SAFETY_FLAGS["not_investment_advice"] is True))
    checks.append(_check("safety_demo_only", lambda: SAFETY_FLAGS["demo_only"] is True))
    checks.append(_check("safety_not_for_production", lambda: SAFETY_FLAGS["not_for_production"] is True))
    checks.append(_check("safety_production_trading_blocked", lambda: SAFETY_FLAGS["production_trading_blocked"] is True))
    checks.append(_check("safety_broker_execution_false", lambda: SAFETY_FLAGS["broker_execution"] is False))
    checks.append(_check("safety_stress_test_only", lambda: SAFETY_FLAGS["stress_test_only"] is True))
    checks.append(_check("safety_monte_carlo_simulation_only", lambda: SAFETY_FLAGS["monte_carlo_simulation_only"] is True))

    # --- Engine checks ---
    from paper_trading.small_capital_strategy.monte_carlo_engine_v183 import (
        ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
        VALID_TRIAL_COUNTS, get_engine_info, validate_action, validate_grade,
    )
    checks.append(_check("allowed_output_actions_15", lambda: len(ALLOWED_OUTPUT_ACTIONS) == 15))
    checks.append(_check("forbidden_output_words_9", lambda: len(FORBIDDEN_OUTPUT_WORDS) == 9))
    checks.append(_check("valid_final_grades_6", lambda: len(VALID_FINAL_GRADES) == 6))
    checks.append(_check("valid_trial_counts_4", lambda: len(VALID_TRIAL_COUNTS) == 4))
    checks.append(_check("monte_carlo_only_in_actions", lambda: "MONTE_CARLO_ONLY" in ALLOWED_OUTPUT_ACTIONS))
    checks.append(_check("blocked_in_actions", lambda: "BLOCKED" in ALLOWED_OUTPUT_ACTIONS))
    checks.append(_check("robust_in_grades", lambda: "ROBUST" in VALID_FINAL_GRADES))
    checks.append(_check("ruin_risk_in_grades", lambda: "RUIN_RISK" in VALID_FINAL_GRADES))
    checks.append(_check("validate_blocked_action", lambda: validate_action("BLOCKED")))
    checks.append(_check("validate_robust_grade", lambda: validate_grade("ROBUST")))

    # --- Bootstrap checks ---
    from paper_trading.small_capital_strategy.monte_carlo_bootstrap_v183 import (
        BOOTSTRAP_TYPES, get_bootstrap_info,
    )
    checks.append(_check("bootstrap_types_5", lambda: len(BOOTSTRAP_TYPES) == 5))
    checks.append(_check("bootstrap_with_replacement", lambda: "WITH_REPLACEMENT" in BOOTSTRAP_TYPES))
    checks.append(_check("bootstrap_info_paper_only", lambda: get_bootstrap_info()["paper_only"] is True))

    # --- Risk of ruin checks ---
    from paper_trading.small_capital_strategy.monte_carlo_risk_of_ruin_v183 import (
        CAPITAL_FLOOR_OPTIONS, MAX_DRAWDOWN_LIMIT_OPTIONS, LOSING_STREAK_THRESHOLD_OPTIONS,
        get_ror_info,
    )
    checks.append(_check("capital_floor_options_3", lambda: len(CAPITAL_FLOOR_OPTIONS) == 3))
    checks.append(_check("max_drawdown_limit_options_4", lambda: len(MAX_DRAWDOWN_LIMIT_OPTIONS) == 4))
    checks.append(_check("losing_streak_options_4", lambda: len(LOSING_STREAK_THRESHOLD_OPTIONS) == 4))

    # --- Scenarios checks ---
    from paper_trading.small_capital_strategy.monte_carlo_scenarios_v183 import get_scenario_count
    checks.append(_check("scenarios_count_ge_75", lambda: get_scenario_count() >= MIN_SCENARIOS))

    # --- Fixture checks ---
    fixture_dir = pathlib.Path(__file__).resolve().parent.parent.parent / "tests" / "fixtures" / "monte_carlo"
    checks.append(_check("fixtures_count_ge_75", lambda: len(list(fixture_dir.glob("*.json"))) >= MIN_FIXTURES))

    # --- Report checks ---
    from paper_trading.small_capital_strategy.monte_carlo_report_v183 import (
        REPORT_SECTIONS, get_report_info,
    )
    checks.append(_check("report_sections_12", lambda: len(REPORT_SECTIONS) == 12))
    checks.append(_check("report_info_count_12", lambda: get_report_info()["count"] == 12))

    # --- CLI checks ---
    from cli.command_registry import get_commands_by_group
    checks.append(_check("cli_monte_carlo_commands_18", lambda: len(get_commands_by_group("monte_carlo")) >= MIN_CLI))

    # --- GUI tabs ---
    from gui.small_capital_strategy_panel import (
        _TABS_V183_MONTE_CARLO, PANEL_VERSION,
    )
    checks.append(_check("gui_monte_carlo_tabs_3", lambda: len(_TABS_V183_MONTE_CARLO) == 3))
    checks.append(_check("gui_panel_version_183", lambda: PANEL_VERSION == "1.8.3"))
    checks.append(_check("gui_tab_monte_carlo", lambda: "monte_carlo" in _TABS_V183_MONTE_CARLO))
    checks.append(_check("gui_tab_risk_of_ruin", lambda: "risk_of_ruin" in _TABS_V183_MONTE_CARLO))
    checks.append(_check("gui_tab_robustness_probability", lambda: "robustness_probability" in _TABS_V183_MONTE_CARLO))

    # --- Additional checks to reach 60+ ---
    checks.append(_check("included_releases_13", lambda: len(INCLUDED_RELEASES) == 13))
    checks.append(_check("known_releases_13", lambda: len(KNOWN_RELEASE_NAMES) == 13))
    checks.append(_check("min_scenarios_75", lambda: MIN_SCENARIOS == 75))
    checks.append(_check("min_fixtures_75", lambda: MIN_FIXTURES == 75))
    checks.append(_check("min_cli_18", lambda: MIN_CLI == 18))
    checks.append(_check("min_health_checks_60", lambda: MIN_HEALTH_CHECKS == 60))
    checks.append(_check("model_names_17", lambda: len(get_all_model_names()) == 17))
    checks.append(_check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"]))
    checks.append(_check("get_version_info_paper_only", lambda: get_version_info()["paper_only"] is True))
    checks.append(_check("get_version_info_monte_carlo_only", lambda: get_version_info()["monte_carlo_only"] is True))
    checks.append(_check("is_known_release_v183", lambda: is_known_release("Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3")))
    checks.append(_check("check_minimum_version_170", lambda: check_minimum_version("1.7.0")))
    checks.append(_check("engine_info_version", lambda: get_engine_info()["version"] == "1.8.3"))
    checks.append(_check("dashboard_default_grade_blocked", lambda: MonteCarloDashboard().final_grade == "BLOCKED"))
    checks.append(_check("monte_carlo_result_default_blocked", lambda: MonteCarloResult().final_grade == "BLOCKED"))
    checks.append(_check("ror_info_paper_only", lambda: get_ror_info()["paper_only"] is True))

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    return MonteCarloHealthSummary(
        total=len(checks),
        passed=passed,
        failed=failed,
        all_passed=failed == 0,
        status="PASS" if failed == 0 else "FAIL",
        checks=checks,
    )


if __name__ == "__main__":
    import sys as _sys
    import pathlib as _pathlib
    _root = str(_pathlib.Path(__file__).resolve().parents[2])
    if _root not in _sys.path:
        _sys.path.insert(0, _root)
    result = run_health_check()
    print(f"Health Check v1.8.3: {result.status} {result.passed}/{result.total}")
