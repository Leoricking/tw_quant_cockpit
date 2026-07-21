"""
release/paper_cockpit_release_gate_v206.py
v2.0.6 Paper Candidate Lifecycle & Setup Aging Control — Release Gate
[!] Paper Only. Research Only. Lifecycle Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))

GATE_VERSION = "2.0.6"
GATE_RELEASE = "Paper Candidate Lifecycle & Setup Aging Control"
BASELINE_TESTS = 34332
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = ("2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4", "2.0.5", "2.0.6")


def run_release_gate():
    """Run all release gate checks for v2.0.6. Returns result dict."""
    passed = 0
    failed = 0
    errors = []

    def chk(name, fn):
        nonlocal passed, failed
        try:
            fn()
            passed += 1
        except Exception as e:
            failed += 1
            errors.append(f"FAIL:{name}:{e}")

    # --- gate version checks ---
    chk("gate_version_206", lambda: None if GATE_VERSION == "2.0.6" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.6")))
    chk("baseline_tests_34332", lambda: None if BASELINE_TESTS == 34332 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 34332")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import VERSION, SCHEMA_VERSION
    chk("module_version_206", lambda: None if VERSION == "2.0.6" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.6, got {VERSION}")))
    chk("schema_version_206", lambda: None if SCHEMA_VERSION == "206" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 206, got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SAFETY_FLAGS_V206
    chk("safety_flags_count_20", lambda: None if len(SAFETY_FLAGS_V206) == 20 else (_ for _ in ()).throw(
        AssertionError(f"Expected 20 SAFETY_FLAGS_V206, got {len(SAFETY_FLAGS_V206)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V206["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V206["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V206["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))

    # --- candidate lifecycle engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    chk("run_lifecycle_review_callable", lambda: run_lifecycle_review())
    chk("run_lifecycle_review_paper_only", lambda: None if run_lifecycle_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("run_lifecycle_review_all_passed", lambda: None if run_lifecycle_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("run_lifecycle_review_should_auto_apply_false", lambda: None if run_lifecycle_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))

    # --- setup aging policy callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    chk("setup_aging_policy_callable", lambda: SetupAgingPolicy())
    chk("setup_aging_policy_auto_apply_false", lambda: None if SetupAgingPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must always be False")))

    # --- lifecycle action callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LifecycleAction
    chk("lifecycle_action_callable", lambda: LifecycleAction())
    chk("lifecycle_action_should_auto_apply_false", lambda: None if LifecycleAction(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must always be False")))

    # --- lifecycle summary callable ---
    chk("lifecycle_summary_not_none", lambda: None if run_lifecycle_review().lifecycle_summary is not None else (_ for _ in ()).throw(
        AssertionError("lifecycle_summary must not be None")))

    # --- stale queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_stale_queue
    chk("build_stale_queue_callable", lambda: build_stale_queue())
    chk("build_stale_queue_is_list", lambda: None if isinstance(build_stale_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_stale_queue must return list")))

    # --- expired queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_expired_queue
    chk("build_expired_queue_callable", lambda: build_expired_queue())

    # --- rescore queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_rescore_queue
    chk("build_rescore_queue_callable", lambda: build_rescore_queue())

    # --- cooldown queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_cooldown_queue
    chk("build_cooldown_queue_callable", lambda: build_cooldown_queue())

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        export_lifecycle_json, export_lifecycle_markdown,
        export_stale_setup_csv, export_expired_candidate_csv,
        export_lifecycle_action_csv, export_lifecycle_audit_snapshot,
    )
    r = run_lifecycle_review()
    chk("export_json_valid", lambda: None if export_lifecycle_json(r).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_lifecycle_json is_valid must be True")))
    chk("export_md_valid", lambda: None if export_lifecycle_markdown(r).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_lifecycle_markdown is_valid must be True")))
    chk("export_stale_csv_valid", lambda: None if export_stale_setup_csv(r).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_stale_setup_csv is_valid must be True")))
    chk("export_expired_csv_valid", lambda: None if export_expired_candidate_csv(r).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_expired_candidate_csv is_valid must be True")))
    chk("export_action_csv_valid", lambda: None if export_lifecycle_action_csv(r).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_lifecycle_action_csv is_valid must be True")))
    chk("export_audit_snapshot_callable", lambda: export_lifecycle_audit_snapshot(r))

    # --- CLI callable ---
    chk("cli_registry_importable", lambda: __import__("cli.command_registry", fromlist=["PROVIDER_COMMANDS"]))
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v206-review-lifecycle",
        "paper-cockpit-v206-evaluate-aging",
        "paper-cockpit-v206-build-stale-queue",
        "paper-cockpit-v206-build-expired-queue",
        "paper-cockpit-v206-build-rescore-queue",
        "paper-cockpit-v206-build-cooldown-queue",
        "paper-cockpit-v206-export-json",
        "paper-cockpit-v206-export-md",
        "paper-cockpit-v206-export-csv",
        "paper-cockpit-v206-health",
        "paper-cockpit-v206-gate",
    ]:
        chk(f"cli_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"'{c}' not in PROVIDER_COMMANDS")))

    # --- GUI import safe ---
    chk("gui_importable", lambda: __import__("gui.small_capital_strategy_panel", fromlist=["PANEL_VERSION_V206"]))
    from gui.small_capital_strategy_panel import PANEL_VERSION_V206
    chk("panel_version_206", lambda: None if PANEL_VERSION_V206 == "2.0.6" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.6, got {PANEL_VERSION_V206}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, render_all_tabs
    tab_names = get_tab_names()
    for tab in ["candidate_lifecycle_v206", "setup_aging_v206", "stale_candidate_queue_v206"]:
        chk(f"tab_{tab}_in_registry", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"tab '{t}' missing")))
    render_result = render_all_tabs()
    for tab in ["candidate_lifecycle_v206", "setup_aging_v206", "stale_candidate_queue_v206"]:
        chk(f"tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"tab '{t}' has error: {render_result.get(t, {}).get('error')}")))

    # --- render_all_tabs has no error tabs ---
    chk("render_all_tabs_no_error_tabs", lambda: None if not any(
        "error" in v for v in render_result.values()
    ) else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has error tabs: {[k for k,v in render_result.items() if 'error' in v]}")))

    # --- paper-only guard enabled ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V206["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))

    # --- broker execution disabled ---
    chk("broker_execution_disabled", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("broker execution must be disabled")))

    # --- production trading blocked ---
    chk("production_trading_blocked", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("production trading must be blocked")))

    # --- no real orders ---
    chk("no_real_orders", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))

    # --- no automatic rebalance ---
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V206["no_automatic_rebalance"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- auto_apply_enabled is always False ---
    chk("auto_apply_enabled_always_false", lambda: None if SetupAgingPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must always be False")))

    # --- should_auto_apply is always False ---
    chk("should_auto_apply_always_false", lambda: None if LifecycleAction(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must always be False")))

    # --- backward compatibility with v2.0.5 preserved ---
    chk("backward_compat_v205", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v205", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import VERSION as V205
    chk("v205_version_unchanged", lambda: None if V205 == "2.0.5" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.5 VERSION changed to {V205}")))

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    _health_dir = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..",
        "paper_trading", "small_capital_strategy"))
    chk("v201_health_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_health_dir, "paper_cockpit_health_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("paper_cockpit_health_v201.py not found")))

    # --- scenarios and fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v206 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_paper_only", lambda: None if all(s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("All scenarios must be paper_only=True")))

    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v206 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_paper_only", lambda: None if all(f["paper_only"] is True for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("All fixtures must be paper_only=True")))

    # --- model counts ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        _ALL_MODEL_NAMES_V206, CLI_COMMANDS_V206, GUI_TABS_V206,
        LIFECYCLE_STATES, AGING_BUCKETS, ACTION_TYPES,
    )
    chk("models_count_13", lambda: None if len(_ALL_MODEL_NAMES_V206) == 13 else (_ for _ in ()).throw(
        AssertionError(f"Expected 13 models, got {len(_ALL_MODEL_NAMES_V206)}")))
    chk("cli_commands_count_11", lambda: None if len(CLI_COMMANDS_V206) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 CLI commands, got {len(CLI_COMMANDS_V206)}")))
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V206) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI tabs, got {len(GUI_TABS_V206)}")))
    chk("lifecycle_states_count_13", lambda: None if len(LIFECYCLE_STATES) == 13 else (_ for _ in ()).throw(
        AssertionError(f"Expected 13 lifecycle states, got {len(LIFECYCLE_STATES)}")))
    chk("aging_buckets_count_5", lambda: None if len(AGING_BUCKETS) == 5 else (_ for _ in ()).throw(
        AssertionError(f"Expected 5 aging buckets, got {len(AGING_BUCKETS)}")))
    chk("action_types_count_8", lambda: None if len(ACTION_TYPES) == 8 else (_ for _ in ()).throw(
        AssertionError(f"Expected 8 action types, got {len(ACTION_TYPES)}")))

    gate_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_release_gate_v206] {passed}/{total} passed  gate_passed={gate_passed}")
    return {
        "gate_passed": gate_passed,
        "passed_count": passed,
        "failed_count": failed,
        "total_count": total,
        "errors": errors,
        "gate_version": GATE_VERSION,
        "gate_release": GATE_RELEASE,
        "baseline_tests": BASELINE_TESTS,
        "min_new_tests": MIN_NEW_TESTS,
    }


if __name__ == "__main__":
    result = run_release_gate()
    if not result["gate_passed"]:
        for e in result["errors"]:
            print(e)
    sys.exit(0 if result["gate_passed"] else 1)
