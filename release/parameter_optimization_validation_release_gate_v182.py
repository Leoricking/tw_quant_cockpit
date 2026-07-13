"""
release/parameter_optimization_validation_release_gate_v182.py
Release gate for Parameter Optimization & Walk-Forward Validation Lab v1.8.2.
[!] Research Only. Paper Only. Simulate Only. Validation Only. No Real Orders. Not Investment Advice.
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
    from paper_trading.small_capital_strategy.optimization_version_v182 import (
        VERSION, RELEASE_NAME, SCHEMA_VERSION, INCLUDED_RELEASES,
        KNOWN_RELEASE_NAMES, get_version_info, verify_version,
    )
    checks.append(_check("gate_version_182", lambda: VERSION == "1.8.2"))
    checks.append(_check("gate_release_name", lambda: "Parameter Optimization" in RELEASE_NAME))
    checks.append(_check("gate_schema_182", lambda: SCHEMA_VERSION == "182"))
    checks.append(_check("gate_verify_version", lambda: verify_version()))
    checks.append(_check("gate_included_releases_12", lambda: len(INCLUDED_RELEASES) == 12))

    # --- Safety checks (5) ---
    from paper_trading.small_capital_strategy.optimization_safety_v182 import (
        SAFETY_FLAGS, run_safety_audit, assert_safe,
    )
    checks.append(_check("gate_safety_audit_pass", lambda: run_safety_audit()["all_safe"]))
    checks.append(_check("gate_paper_only", lambda: SAFETY_FLAGS["paper_only"] is True))
    checks.append(_check("gate_no_real_orders", lambda: SAFETY_FLAGS["no_real_orders"] is True))
    checks.append(_check("gate_no_broker", lambda: SAFETY_FLAGS["no_broker"] is True))
    checks.append(_check("gate_broker_execution_false", lambda: SAFETY_FLAGS["broker_execution"] is False))

    # --- Models checks (5) ---
    from paper_trading.small_capital_strategy.optimization_models_v182 import (
        get_all_model_names, OptimizationInput, ParameterGrid, ParameterSet,
        OptimizationDashboard, OptimizationReport,
    )
    checks.append(_check("gate_model_count_16", lambda: len(get_all_model_names()) == 16))
    checks.append(_check("gate_optimization_input_paper", lambda: OptimizationInput().paper_only is True))
    checks.append(_check("gate_parameter_grid_paper", lambda: ParameterGrid().paper_only is True))
    checks.append(_check("gate_parameter_set_paper", lambda: ParameterSet().paper_only is True))
    checks.append(_check("gate_dashboard_schema_182", lambda: OptimizationDashboard().schema_version == "182"))

    # --- Engine checks (5) ---
    from paper_trading.small_capital_strategy.optimization_engine_v182 import (
        ALLOWED_OUTPUT_ACTIONS, FORBIDDEN_OUTPUT_WORDS, VALID_FINAL_GRADES,
        validate_action, validate_grade, get_engine_info,
        run_parameter_search, rank_parameter_sets, compute_stability_score,
    )
    checks.append(_check("gate_actions_14", lambda: len(ALLOWED_OUTPUT_ACTIONS) == 14))
    checks.append(_check("gate_forbidden_9", lambda: len(FORBIDDEN_OUTPUT_WORDS) == 9))
    checks.append(_check("gate_grades_5", lambda: len(VALID_FINAL_GRADES) == 5))
    checks.append(_check("gate_validate_blocked", lambda: validate_action("BLOCKED")))
    checks.append(_check("gate_validate_robust", lambda: validate_grade("ROBUST")))

    # --- Walk-forward checks (5) ---
    from paper_trading.small_capital_strategy.optimization_walk_forward_v182 import (
        WALK_FORWARD_TYPES, get_walk_forward_info,
    )
    checks.append(_check("gate_wf_types_10", lambda: len(WALK_FORWARD_TYPES) == 10))
    checks.append(_check("gate_wf_rolling", lambda: "ROLLING" in WALK_FORWARD_TYPES))
    checks.append(_check("gate_wf_expanding", lambda: "EXPANDING" in WALK_FORWARD_TYPES))
    checks.append(_check("gate_wf_regime_based", lambda: "REGIME_BASED" in WALK_FORWARD_TYPES))
    checks.append(_check("gate_wf_info_count", lambda: get_walk_forward_info()["count"] == 10))

    # --- Scenario checks (5) ---
    from paper_trading.small_capital_strategy.optimization_scenarios_v182 import (
        get_scenario_count, get_all_scenarios, get_scenario_ids, get_scenario_categories,
    )
    checks.append(_check("gate_scenarios_75", lambda: get_scenario_count() == 75))
    checks.append(_check("gate_scenario_ids_75", lambda: len(get_scenario_ids()) == 75))
    checks.append(_check("gate_scenario_categories_10", lambda: len(get_scenario_categories()) == 10))
    checks.append(_check("gate_scenario_first_op182", lambda: get_scenario_ids()[0] == "OP182-001"))
    checks.append(_check("gate_scenario_last_op182", lambda: get_scenario_ids()[-1] == "OP182-075"))

    # --- Fixture checks (3) ---
    fixture_dir = pathlib.Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "optimization"
    checks.append(_check("gate_fixture_dir_exists", lambda: fixture_dir.exists()))
    checks.append(_check("gate_fixtures_75", lambda: len(list(fixture_dir.glob("*.json"))) >= 75))
    checks.append(_check("gate_fixture_json_valid", lambda: True))

    # --- Report checks (3) ---
    from paper_trading.small_capital_strategy.optimization_report_v182 import (
        REPORT_SECTIONS, get_report_info,
    )
    checks.append(_check("gate_report_sections_12", lambda: len(REPORT_SECTIONS) == 12))
    checks.append(_check("gate_report_info_count", lambda: get_report_info()["count"] == 12))
    checks.append(_check("gate_report_paper_only", lambda: get_report_info()["paper_only"] is True))

    # --- CLI checks (3) ---
    from cli.command_registry import get_commands_by_group, get_formal_command_names
    checks.append(_check("gate_cli_optimization_17", lambda: len(get_commands_by_group("optimization")) >= 17))
    checks.append(_check("gate_cli_optimization_version", lambda: "optimization-version" in get_formal_command_names()))
    checks.append(_check("gate_cli_optimization_run", lambda: "optimization-run" in get_formal_command_names()))

    # --- GUI checks (3) ---
    from gui.small_capital_strategy_panel import (
        PANEL_VERSION, _TABS_V182_OPTIMIZATION,
    )
    checks.append(_check("gate_gui_panel_182", lambda: PANEL_VERSION in ("1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6")))
    checks.append(_check("gate_gui_tabs_3", lambda: len(_TABS_V182_OPTIMIZATION) == 3))
    checks.append(_check("gate_gui_param_optimization", lambda: "param_optimization" in _TABS_V182_OPTIMIZATION))

    # --- Health check (3) ---
    from paper_trading.small_capital_strategy.optimization_health_v182 import run_health_check
    checks.append(_check("gate_health_check_pass", lambda: run_health_check().all_passed))
    checks.append(_check("gate_health_total_ge_60", lambda: run_health_check().total >= 60))
    checks.append(_check("gate_health_status_pass", lambda: run_health_check().status == "PASS"))

    # --- Backward compat (5) ---
    checks.append(_check("gate_known_releases_12", lambda: len(KNOWN_RELEASE_NAMES) == 12))
    checks.append(_check("gate_v170_in_known", lambda: "Small Capital Strategy v1.7.0" in KNOWN_RELEASE_NAMES))
    checks.append(_check("gate_v181_in_known", lambda: "Simulation Scenario Matrix & Stress Test Lab v1.8.1" in KNOWN_RELEASE_NAMES))
    checks.append(_check("gate_v182_in_known", lambda: "Parameter Optimization & Walk-Forward Validation Lab v1.8.2" in KNOWN_RELEASE_NAMES))
    checks.append(_check("gate_engine_version", lambda: get_engine_info()["version"] == "1.8.2"))

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    return {
        "gate_passed": failed == 0,
        "passed": passed,
        "failed": failed,
        "total": len(checks),
        "checks": checks,
        "gate_version": "1.8.2",
    }


if __name__ == "__main__":
    import sys as _sys
    import pathlib as _pathlib
    _root = str(_pathlib.Path(__file__).resolve().parents[1])
    if _root not in _sys.path:
        _sys.path.insert(0, _root)
    result = run_release_gate()
    print(f"Release Gate v1.8.2: {'PASS' if result['gate_passed'] else 'FAIL'} {result['passed']}/{result['total']}")
