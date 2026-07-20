"""
release/paper_cockpit_release_gate_v205.py
v2.0.5 Paper Watchlist Rotation & Candidate Promotion Queue — Release Gate
[!] Paper Only. Research Only. Rotation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))

GATE_VERSION = "2.0.5"
GATE_RELEASE = "Paper Watchlist Rotation & Candidate Promotion Queue"
BASELINE_TESTS = 33984
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = ("2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4", "2.0.5")


def run_release_gate():
    """Run all release gate checks for v2.0.5. Returns result dict."""
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
    chk("gate_version_205", lambda: None if GATE_VERSION == "2.0.5" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.5")))
    chk("baseline_tests_33984", lambda: None if BASELINE_TESTS == 33984 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 33984")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import VERSION, SCHEMA_VERSION
    chk("module_version_205", lambda: None if VERSION == "2.0.5" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.5, got {VERSION}")))
    chk("schema_version_205", lambda: None if SCHEMA_VERSION == "205" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 205, got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import SAFETY_FLAGS_V205
    chk("safety_flags_count_20", lambda: None if len(SAFETY_FLAGS_V205) == 20 else (_ for _ in ()).throw(
        AssertionError(f"Expected 20 SAFETY_FLAGS_V205, got {len(SAFETY_FLAGS_V205)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V205["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V205["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))

    # --- watchlist rotation engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    chk("run_watchlist_rotation_callable", lambda: run_watchlist_rotation())
    chk("run_watchlist_rotation_paper_only", lambda: None if run_watchlist_rotation().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("run_watchlist_rotation_all_passed", lambda: None if run_watchlist_rotation().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("run_watchlist_rotation_should_auto_apply_false", lambda: None if run_watchlist_rotation().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))

    # --- promotion queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_promotion_queue
    chk("build_promotion_queue_callable", lambda: build_promotion_queue())
    chk("build_promotion_queue_is_list", lambda: None if isinstance(build_promotion_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_promotion_queue must return list")))

    # --- demotion queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_demotion_queue
    chk("build_demotion_queue_callable", lambda: build_demotion_queue())

    # --- quarantine queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_quarantine_queue
    chk("build_quarantine_queue_callable", lambda: build_quarantine_queue())

    # --- human review queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_human_review_queue
    chk("build_human_review_queue_callable", lambda: build_human_review_queue())

    # --- queue summary callable ---
    chk("queue_summary_not_none", lambda: None if run_watchlist_rotation().queue_summary is not None else (_ for _ in ()).throw(
        AssertionError("queue_summary must not be None")))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        export_rotation_json, export_rotation_markdown,
        export_promotion_queue_csv, export_demotion_queue_csv,
        export_rotation_audit_snapshot,
    )
    r = run_watchlist_rotation()
    chk("export_json_valid", lambda: None if export_rotation_json(r).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_rotation_json is_valid must be True")))
    chk("export_md_valid", lambda: None if export_rotation_markdown(r).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_rotation_markdown is_valid must be True")))
    chk("export_promo_csv_valid", lambda: None if export_promotion_queue_csv(r).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_promotion_queue_csv is_valid must be True")))
    chk("export_demotion_csv_valid", lambda: None if export_demotion_queue_csv(r).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_demotion_queue_csv is_valid must be True")))
    chk("export_audit_snapshot_callable", lambda: export_rotation_audit_snapshot(r))

    # --- CLI callable ---
    chk("cli_registry_importable", lambda: __import__("cli.command_registry", fromlist=["PROVIDER_COMMANDS"]))
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    for cmd in [
        "paper-cockpit-v205-rotate-watchlist",
        "paper-cockpit-v205-promote-candidates",
        "paper-cockpit-v205-demote-candidates",
        "paper-cockpit-v205-build-human-review-queue",
        "paper-cockpit-v205-build-quarantine-queue",
        "paper-cockpit-v205-export-json",
        "paper-cockpit-v205-export-md",
        "paper-cockpit-v205-export-csv",
        "paper-cockpit-v205-health",
        "paper-cockpit-v205-gate",
    ]:
        chk(f"cli_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"'{c}' not in PROVIDER_COMMANDS")))

    # --- GUI import safe ---
    chk("gui_importable", lambda: __import__("gui.small_capital_strategy_panel", fromlist=["PANEL_VERSION_V205"]))
    from gui.small_capital_strategy_panel import PANEL_VERSION_V205
    chk("panel_version_205", lambda: None if PANEL_VERSION_V205 == "2.0.5" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.5, got {PANEL_VERSION_V205}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, render_all_tabs
    tab_names = get_tab_names()
    for tab in ["watchlist_rotation_v205", "promotion_queue_v205", "human_review_queue_v205"]:
        chk(f"tab_{tab}_in_registry", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"tab '{t}' missing")))
    render_result = render_all_tabs()
    for tab in ["watchlist_rotation_v205", "promotion_queue_v205", "human_review_queue_v205"]:
        chk(f"tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"tab '{t}' has error: {render_result.get(t, {}).get('error')}")))

    # --- render_all_tabs has no error tabs ---
    chk("render_all_tabs_no_error_tabs", lambda: None if not any(
        "error" in v for v in render_result.values()
    ) else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has error tabs: {[k for k,v in render_result.items() if 'error' in v]}")))

    # --- paper-only guard enabled ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V205["paper_only"] is True else (_ for _ in ()).throw(
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
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V205["no_automatic_rebalance"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- should_auto_apply is always False ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import PromotionDecision
    chk("should_auto_apply_always_false", lambda: None if PromotionDecision(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must always be False")))

    # --- backward compatibility with v2.0.4 preserved ---
    chk("backward_compat_v204", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v204", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import VERSION as V204
    chk("v204_version_unchanged", lambda: None if V204 == "2.0.4" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.4 VERSION changed to {V204}")))

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    _health_dir = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..",
        "paper_trading", "small_capital_strategy"))
    chk("v201_health_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_health_dir, "paper_cockpit_health_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("paper_cockpit_health_v201.py not found")))

    # --- scenarios and fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_paper_only", lambda: None if all(s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("All scenarios must be paper_only=True")))

    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_paper_only", lambda: None if all(f["paper_only"] is True for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("All fixtures must be paper_only=True")))

    # --- model counts ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        _ALL_MODEL_NAMES_V205, CLI_COMMANDS_V205, GUI_TABS_V205,
        WATCHLIST_STATUSES,
    )
    chk("models_count_12", lambda: None if len(_ALL_MODEL_NAMES_V205) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 models, got {len(_ALL_MODEL_NAMES_V205)}")))
    chk("cli_commands_count_10", lambda: None if len(CLI_COMMANDS_V205) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI commands, got {len(CLI_COMMANDS_V205)}")))
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V205) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI tabs, got {len(GUI_TABS_V205)}")))
    chk("watchlist_statuses_count_9", lambda: None if len(WATCHLIST_STATUSES) == 9 else (_ for _ in ()).throw(
        AssertionError(f"Expected 9 statuses, got {len(WATCHLIST_STATUSES)}")))

    gate_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_release_gate_v205] {passed}/{total} passed  gate_passed={gate_passed}")
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
