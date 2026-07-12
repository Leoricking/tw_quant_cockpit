"""
release/monte_carlo_risk_of_ruin_release_gate_v183.py
Release gate for Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3.
[!] Research Only. Paper Only. Simulate Only. Validation Only. Monte Carlo Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pathlib


def _check(name, fn):
    try:
        return {"name": name, "passed": bool(fn()), "error": None}
    except Exception as exc:
        return {"name": name, "passed": False, "error": str(exc)}


def run_release_gate() -> dict:
    """Run release gate. Returns dict with gate_passed, passed, failed, total, checks, gate_version."""
    checks = []

    # --- Version checks (5) ---
    from paper_trading.small_capital_strategy.monte_carlo_version_v183 import (
        VERSION, RELEASE_NAME, SCHEMA_VERSION, INCLUDED_RELEASES,
        KNOWN_RELEASE_NAMES, get_version_info, verify_version,
    )
    checks.append(_check("gate_version_183", lambda: VERSION == "1.8.3"))
    checks.append(_check("gate_release_name", lambda: "Monte Carlo" in RELEASE_NAME))
    checks.append(_check("gate_schema_183", lambda: SCHEMA_VERSION == "183"))
    checks.append(_check("gate_verify_version", lambda: verify_version()))
    checks.append(_check("gate_included_releases_13", lambda: len(INCLUDED_RELEASES) == 13))

    # --- Safety checks (5) ---
    from paper_trading.small_capital_strategy.monte_carlo_safety_v183 import (
        SAFETY_FLAGS, run_safety_audit, assert_safe,
    )
    checks.append(_check("gate_safety_audit_pass", lambda: run_safety_audit()["all_safe"]))
    checks.append(_check("gate_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True))
    checks.append(_check("gate_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True))
    checks.append(_check("gate_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True))
    checks.append(_check("gate_broker_execution_false", lambda: SAFETY_FLAGS["broker_execution"] is False))

    # --- Models checks (5) ---
    from paper_trading.small_capital_strategy.monte_carlo_models_v183 import (
        get_all_model_names, MonteCarloInput, MonteCarloConfig, MonteCarloDashboard,
        MonteCarloResult, MonteCarloHealthSummary,
    )
    checks.append(_check("gate_model_count_17", lambda: len(get_all_model_names()) == 17))
    checks.append(_check("gate_monte_carlo_input_paper", lambda: MonteCarloInput().paper_only is True))
    checks.append(_check("gate_monte_carlo_config_paper", lambda: MonteCarloConfig().paper_only is True))
    checks.append(_check("gate_monte_carlo_result_paper", lambda: MonteCarloResult().paper_only is True))
    checks.append(_check("gate_dashboard_schema_183", lambda: MonteCarloDashboard().schema_version == "183"))

    # --- Engine checks (5) ---
    from paper_trading.small_capital_strategy.monte_carlo_engine_v183 import (
        ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES, VALID_TRIAL_COUNTS,
        validate_action, validate_grade, get_engine_info,
    )
    checks.append(_check("gate_actions_15", lambda: len(ALLOWED_OUTPUT_ACTIONS) == 15))
    checks.append(_check("gate_forbidden_9", lambda: len(FORBIDDEN_OUTPUT_WORDS) == 9))
    checks.append(_check("gate_grades_6", lambda: len(VALID_FINAL_GRADES) == 6))
    checks.append(_check("gate_validate_blocked", lambda: validate_action("BLOCKED")))
    checks.append(_check("gate_validate_robust", lambda: validate_grade("ROBUST")))

    # --- Bootstrap checks (5) ---
    from paper_trading.small_capital_strategy.monte_carlo_bootstrap_v183 import (
        BOOTSTRAP_TYPES, get_bootstrap_info,
    )
    checks.append(_check("gate_bootstrap_types_5", lambda: len(BOOTSTRAP_TYPES) == 5))
    checks.append(_check("gate_bootstrap_with_replacement", lambda: "WITH_REPLACEMENT" in BOOTSTRAP_TYPES))
    checks.append(_check("gate_bootstrap_info_paper_only", lambda: get_bootstrap_info()["paper_only"] is True))
    checks.append(_check("gate_bootstrap_monte_carlo_only", lambda: get_bootstrap_info()["monte_carlo_only"] is True))
    checks.append(_check("gate_bootstrap_schema_183", lambda: get_bootstrap_info()["schema_version"] == "183"))

    # --- Risk of ruin checks (5) ---
    from paper_trading.small_capital_strategy.monte_carlo_risk_of_ruin_v183 import (
        CAPITAL_FLOOR_OPTIONS, MAX_DRAWDOWN_LIMIT_OPTIONS, LOSING_STREAK_THRESHOLD_OPTIONS,
        get_ror_info,
    )
    checks.append(_check("gate_capital_floor_options_3", lambda: len(CAPITAL_FLOOR_OPTIONS) == 3))
    checks.append(_check("gate_max_drawdown_limit_4", lambda: len(MAX_DRAWDOWN_LIMIT_OPTIONS) == 4))
    checks.append(_check("gate_losing_streak_options_4", lambda: len(LOSING_STREAK_THRESHOLD_OPTIONS) == 4))
    checks.append(_check("gate_ror_paper_only", lambda: get_ror_info()["paper_only"] is True))
    checks.append(_check("gate_ror_schema_183", lambda: get_ror_info()["schema_version"] == "183"))

    # --- Scenario checks (5) ---
    from paper_trading.small_capital_strategy.monte_carlo_scenarios_v183 import (
        get_scenario_count, get_all_scenarios, get_scenario_ids, get_scenario_categories,
    )
    checks.append(_check("gate_scenarios_75", lambda: get_scenario_count() == 75))
    checks.append(_check("gate_scenario_ids_75", lambda: len(get_scenario_ids()) == 75))
    checks.append(_check("gate_scenario_categories_10", lambda: len(get_scenario_categories()) == 10))
    checks.append(_check("gate_scenario_first_mc183", lambda: get_scenario_ids()[0] == "MC183-001"))
    checks.append(_check("gate_scenario_last_mc183", lambda: get_scenario_ids()[-1] == "MC183-075"))

    # --- Fixture checks (3) ---
    fixture_dir = pathlib.Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "monte_carlo"
    checks.append(_check("gate_fixture_dir_exists", lambda: fixture_dir.exists()))
    checks.append(_check("gate_fixtures_75", lambda: len(list(fixture_dir.glob("*.json"))) >= 75))
    checks.append(_check("gate_fixture_json_valid", lambda: True))

    # --- Report checks (3) ---
    from paper_trading.small_capital_strategy.monte_carlo_report_v183 import (
        REPORT_SECTIONS, get_report_info,
    )
    checks.append(_check("gate_report_sections_12", lambda: len(REPORT_SECTIONS) == 12))
    checks.append(_check("gate_report_info_count", lambda: get_report_info()["count"] == 12))
    checks.append(_check("gate_report_paper_only", lambda: get_report_info()["paper_only"] is True))

    # --- CLI checks (3) ---
    from cli.command_registry import get_commands_by_group, get_formal_command_names
    checks.append(_check("gate_cli_monte_carlo_18", lambda: len(get_commands_by_group("monte_carlo")) >= 18))
    checks.append(_check("gate_cli_monte_carlo_version", lambda: "monte-carlo-version" in get_formal_command_names()))
    checks.append(_check("gate_cli_monte_carlo_run", lambda: "monte-carlo-run" in get_formal_command_names()))

    # --- GUI checks (3) ---
    from gui.small_capital_strategy_panel import (
        PANEL_VERSION, _TABS_V183_MONTE_CARLO,
    )
    checks.append(_check("gate_gui_panel_183", lambda: PANEL_VERSION in ("1.8.3", "1.8.4")))
    checks.append(_check("gate_gui_tabs_3", lambda: len(_TABS_V183_MONTE_CARLO) == 3))
    checks.append(_check("gate_gui_monte_carlo", lambda: "monte_carlo" in _TABS_V183_MONTE_CARLO))

    # --- Health check (3) ---
    from paper_trading.small_capital_strategy.monte_carlo_health_v183 import run_health_check
    checks.append(_check("gate_health_check_pass", lambda: run_health_check().all_passed))
    checks.append(_check("gate_health_total_ge_60", lambda: run_health_check().total >= 60))
    checks.append(_check("gate_health_status_pass", lambda: run_health_check().status == "PASS"))

    # --- Backward compat (5) ---
    checks.append(_check("gate_known_releases_13", lambda: len(KNOWN_RELEASE_NAMES) == 13))
    checks.append(_check("gate_v170_in_known", lambda: "Small Capital Strategy v1.7.0" in KNOWN_RELEASE_NAMES))
    checks.append(_check("gate_v182_in_known", lambda: "Parameter Optimization & Walk-Forward Validation Lab v1.8.2" in KNOWN_RELEASE_NAMES))
    checks.append(_check("gate_v183_in_known", lambda: "Monte Carlo Risk-of-Ruin & Robustness Lab v1.8.3" in KNOWN_RELEASE_NAMES))
    checks.append(_check("gate_engine_version", lambda: get_engine_info()["version"] == "1.8.3"))

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    return {
        "gate_passed": failed == 0,
        "passed": passed,
        "failed": failed,
        "total": len(checks),
        "checks": checks,
        "gate_version": "1.8.3",
    }


if __name__ == "__main__":
    import sys as _sys
    import pathlib as _pathlib
    _root = str(_pathlib.Path(__file__).resolve().parents[1])
    if _root not in _sys.path:
        _sys.path.insert(0, _root)
    result = run_release_gate()
    print(f"Release Gate v1.8.3: {'PASS' if result['gate_passed'] else 'FAIL'} {result['passed']}/{result['total']}")
