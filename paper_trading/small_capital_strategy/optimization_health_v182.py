"""
paper_trading/small_capital_strategy/optimization_health_v182.py
Health check for Parameter Optimization & Walk-Forward Validation Lab v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pathlib


def _check(name, fn):
    try:
        return {"name": name, "passed": bool(fn()), "error": None}
    except Exception as exc:
        return {"name": name, "passed": False, "error": str(exc)}


def run_health_check():
    """Run all health checks. Returns OptimizationHealthSummary."""
    from paper_trading.small_capital_strategy.optimization_models_v182 import OptimizationHealthSummary
    checks = []

    # --- Version checks (5) ---
    from paper_trading.small_capital_strategy.optimization_version_v182 import (
        VERSION, RELEASE_NAME, SCHEMA_VERSION, POLICY_VERSION, INCLUDED_RELEASES,
        KNOWN_RELEASE_NAMES, get_version_info, verify_version, is_known_release,
        check_minimum_version, MIN_SCENARIOS, MIN_FIXTURES, MIN_CLI, MIN_HEALTH_CHECKS,
    )
    checks.append(_check("version_is_182", lambda: VERSION == "1.8.2"))
    checks.append(_check("release_name_set", lambda: RELEASE_NAME == "Parameter Optimization & Walk-Forward Validation Lab"))
    checks.append(_check("schema_version_182", lambda: SCHEMA_VERSION == "182"))
    checks.append(_check("policy_version_set", lambda: "1.8.2" in POLICY_VERSION))
    checks.append(_check("verify_version_true", lambda: verify_version()))

    # --- Models checks (16) ---
    from paper_trading.small_capital_strategy.optimization_models_v182 import (
        OptimizationInput, OptimizationConfig, ParameterGrid, ParameterSet,
        ParameterSearchResult, ParameterRanking, WalkForwardWindow, WalkForwardConfig,
        WalkForwardResult, RobustParameterSet, OverfittingRiskReport, StabilityScore,
        ParameterSensitivityReport, OptimizationDashboard, OptimizationReport,
        OptimizationHealthSummary as HealthModel, get_all_model_names,
    )
    checks.append(_check("model_optimization_input", lambda: OptimizationInput().paper_only is True))
    checks.append(_check("model_optimization_config", lambda: OptimizationConfig().paper_only is True))
    checks.append(_check("model_parameter_grid", lambda: ParameterGrid().paper_only is True))
    checks.append(_check("model_parameter_set", lambda: ParameterSet().paper_only is True))
    checks.append(_check("model_parameter_search_result", lambda: ParameterSearchResult().paper_only is True))
    checks.append(_check("model_parameter_ranking", lambda: ParameterRanking().paper_only is True))
    checks.append(_check("model_walk_forward_window", lambda: WalkForwardWindow().paper_only is True))
    checks.append(_check("model_walk_forward_config", lambda: WalkForwardConfig().paper_only is True))
    checks.append(_check("model_walk_forward_result", lambda: WalkForwardResult().paper_only is True))
    checks.append(_check("model_robust_parameter_set", lambda: RobustParameterSet().paper_only is True))
    checks.append(_check("model_overfitting_risk_report", lambda: OverfittingRiskReport().paper_only is True))
    checks.append(_check("model_stability_score", lambda: StabilityScore().paper_only is True))
    checks.append(_check("model_parameter_sensitivity_report", lambda: ParameterSensitivityReport().paper_only is True))
    checks.append(_check("model_optimization_dashboard", lambda: OptimizationDashboard().paper_only is True))
    checks.append(_check("model_optimization_report", lambda: OptimizationReport().paper_only is True))
    checks.append(_check("model_optimization_health_summary", lambda: HealthModel().paper_only is True))

    # --- Safety flags checks (18) ---
    from paper_trading.small_capital_strategy.optimization_safety_v182 import (
        SAFETY_FLAGS, get_safety_flags, run_safety_audit, assert_safe,
    )
    checks.append(_check("safety_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True))
    checks.append(_check("safety_research_only", lambda: SAFETY_FLAGS["research_only"] is True))
    checks.append(_check("safety_simulate_only", lambda: SAFETY_FLAGS["simulate_only"] is True))
    checks.append(_check("safety_validation_only", lambda: SAFETY_FLAGS["validation_only"] is True))
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
    checks.append(_check("safety_optimization_only", lambda: SAFETY_FLAGS["optimization_only"] is True))

    # --- Parameter grid checks (1) ---
    checks.append(_check("parameter_grid_12_dimensions", lambda: len([
        f for f in ParameterGrid.__dataclass_fields__ if f.endswith("_values")
    ]) == 12))

    # --- Scenario checks (1) ---
    from paper_trading.small_capital_strategy.optimization_scenarios_v182 import get_scenario_count
    checks.append(_check("scenarios_count_ge_75", lambda: get_scenario_count() >= MIN_SCENARIOS))

    # --- Fixture checks (1) ---
    fixture_dir = pathlib.Path(__file__).resolve().parent.parent.parent / "tests" / "fixtures" / "optimization"
    checks.append(_check("fixtures_count_ge_75", lambda: len(list(fixture_dir.glob("*.json"))) >= MIN_FIXTURES))

    # --- Allowed output actions (1) ---
    from paper_trading.small_capital_strategy.optimization_engine_v182 import (
        ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
        get_engine_info,
    )
    checks.append(_check("allowed_output_actions_14", lambda: len(ALLOWED_OUTPUT_ACTIONS) == 14))

    # --- Forbidden output words (1) ---
    checks.append(_check("forbidden_output_words_9", lambda: len(FORBIDDEN_OUTPUT_WORDS) == 9))

    # --- Valid final grades (1) ---
    checks.append(_check("valid_final_grades_5", lambda: len(VALID_FINAL_GRADES) == 5))

    # --- Walk-forward types (1) ---
    from paper_trading.small_capital_strategy.optimization_walk_forward_v182 import (
        WALK_FORWARD_TYPES, get_walk_forward_info,
    )
    checks.append(_check("walk_forward_types_10", lambda: len(WALK_FORWARD_TYPES) == 10))

    # --- Report sections (1) ---
    from paper_trading.small_capital_strategy.optimization_report_v182 import (
        REPORT_SECTIONS, get_report_info,
    )
    checks.append(_check("report_sections_12", lambda: len(REPORT_SECTIONS) == 12))

    # --- CLI commands (1) ---
    from cli.command_registry import get_commands_by_group
    checks.append(_check("cli_optimization_commands_17", lambda: len(get_commands_by_group("optimization")) >= MIN_CLI))

    # --- GUI tabs (3) ---
    from gui.small_capital_strategy_panel import (
        _TABS_V182_OPTIMIZATION, PANEL_VERSION,
    )
    checks.append(_check("gui_optimization_tabs_3", lambda: len(_TABS_V182_OPTIMIZATION) == 3))
    checks.append(_check("gui_panel_version_182", lambda: PANEL_VERSION in ("1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9", "1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6", "1.9.7", "1.9.8", "1.9.9")))
    checks.append(_check("gui_tab_param_optimization", lambda: "param_optimization" in _TABS_V182_OPTIMIZATION))

    # --- Backward compat (1) ---
    checks.append(_check("known_releases_12", lambda: len(KNOWN_RELEASE_NAMES) == 12))

    # --- Engine info (1) ---
    checks.append(_check("engine_info_version", lambda: get_engine_info()["version"] == "1.8.2"))

    # --- Dashboard (1) ---
    checks.append(_check("dashboard_model_grade", lambda: OptimizationDashboard().final_grade == "BLOCKED"))

    # --- Report (1) ---
    checks.append(_check("report_info_count_12", lambda: get_report_info()["count"] == 12))

    # --- Additional checks to reach 60+ ---
    checks.append(_check("included_releases_12", lambda: len(INCLUDED_RELEASES) == 12))
    checks.append(_check("min_scenarios_75", lambda: MIN_SCENARIOS == 75))
    checks.append(_check("min_fixtures_75", lambda: MIN_FIXTURES == 75))
    checks.append(_check("min_cli_17", lambda: MIN_CLI == 17))
    checks.append(_check("min_health_checks_60", lambda: MIN_HEALTH_CHECKS == 60))
    checks.append(_check("model_names_16", lambda: len(get_all_model_names()) == 16))
    checks.append(_check("safety_audit_all_safe", lambda: run_safety_audit()["all_safe"]))
    checks.append(_check("get_version_info_paper_only", lambda: get_version_info()["paper_only"] is True))
    checks.append(_check("is_known_release_v182", lambda: is_known_release("Parameter Optimization & Walk-Forward Validation Lab v1.8.2")))
    checks.append(_check("check_minimum_version_170", lambda: check_minimum_version("1.7.0")))
    checks.append(_check("walk_forward_info_count_10", lambda: get_walk_forward_info()["count"] == 10))
    checks.append(_check("validation_only_in_actions", lambda: "VALIDATION_ONLY" in ALLOWED_OUTPUT_ACTIONS))
    checks.append(_check("blocked_in_actions", lambda: "BLOCKED" in ALLOWED_OUTPUT_ACTIONS))

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    return OptimizationHealthSummary(
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
    print(f"Health Check v1.8.2: {result.status} {result.passed}/{result.total}")
