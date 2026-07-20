"""
paper_trading/small_capital_strategy/paper_cockpit_health_v205.py
v2.0.5 Paper Watchlist Rotation & Candidate Promotion Queue — Health Check
[!] Paper Only. Research Only. Rotation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

# Ensure repo root is importable when run directly
_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

HEALTH_VERSION = "2.0.5"
HEALTH_RELEASE = "Paper Watchlist Rotation & Candidate Promotion Queue"


def run_health_check():
    """Run all health checks for v2.0.5 paper cockpit. Returns result dict."""
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

    # --- version / title ---
    chk("version_title_205", lambda: None if HEALTH_VERSION == "2.0.5" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.5 got {HEALTH_VERSION}")))
    chk("release_name_rotation", lambda: None if "Watchlist Rotation" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Watchlist Rotation': {HEALTH_RELEASE}")))

    # --- module import ---
    chk("import_paper_cockpit_v205", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v205",
        fromlist=["VERSION"]))

    # --- version constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_205", lambda: None if VERSION == "2.0.5" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.5 got {VERSION}")))
    chk("schema_version_is_205", lambda: None if SCHEMA_VERSION == "205" else (_ for _ in ()).throw(
        AssertionError(f"Expected 205 got {SCHEMA_VERSION}")))
    chk("release_name_correct", lambda: None if "Watchlist Rotation" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Watchlist Rotation': {RELEASE_NAME}")))

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
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V205["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V205["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_broker_execution_disabled", lambda: None if SAFETY_FLAGS_V205["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_trading_blocked", lambda: None if SAFETY_FLAGS_V205["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))

    # --- watchlist statuses ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WATCHLIST_STATUSES
    chk("watchlist_statuses_count_9", lambda: None if len(WATCHLIST_STATUSES) == 9 else (_ for _ in ()).throw(
        AssertionError(f"Expected 9 WATCHLIST_STATUSES, got {len(WATCHLIST_STATUSES)}")))
    for status in [
        "active_watchlist", "promoted_candidate", "second_wave_candidate",
        "abc_pullback_candidate", "breakout_candidate", "quarantined_no_entry",
        "downgraded", "removed", "human_review_required",
    ]:
        chk(f"watchlist_status_{status}", lambda s=status: None if s in WATCHLIST_STATUSES else (
            _ for _ in ()).throw(AssertionError(f"Missing status: {s}")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import CLI_COMMANDS_V205
    chk("cli_commands_count_10", lambda: None if len(CLI_COMMANDS_V205) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI_COMMANDS_V205, got {len(CLI_COMMANDS_V205)}")))
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
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V205 else (
            _ for _ in ()).throw(AssertionError(f"Missing CLI command: {c}")))

    # --- GUI tabs ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import GUI_TABS_V205
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V205) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI_TABS_V205, got {len(GUI_TABS_V205)}")))
    for tab in ["watchlist_rotation_v205", "promotion_queue_v205", "human_review_queue_v205"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in GUI_TABS_V205 else (
            _ for _ in ()).throw(AssertionError(f"Missing GUI tab: {t}")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        WatchlistItem, PromotionDecision, QueueSummary, WatchlistRotationInput,
        WatchlistRotationResult, RotationExportResult, RotationAuditSnapshot,
        WatchlistRotationReport, PromotionQueueCSV, V205HealthSummary,
        V205ReleaseSummary, DemotionQueueCSV,
        _ALL_MODEL_NAMES_V205,
    )
    chk("model_WatchlistItem", lambda: WatchlistItem())
    chk("model_PromotionDecision", lambda: PromotionDecision())
    chk("model_QueueSummary", lambda: QueueSummary())
    chk("model_WatchlistRotationInput", lambda: WatchlistRotationInput())
    chk("model_WatchlistRotationResult", lambda: WatchlistRotationResult())
    chk("model_RotationExportResult", lambda: RotationExportResult())
    chk("model_RotationAuditSnapshot", lambda: RotationAuditSnapshot())
    chk("model_WatchlistRotationReport", lambda: WatchlistRotationReport())
    chk("model_PromotionQueueCSV", lambda: PromotionQueueCSV())
    chk("model_DemotionQueueCSV", lambda: DemotionQueueCSV())
    chk("model_V205HealthSummary", lambda: V205HealthSummary())
    chk("model_V205ReleaseSummary", lambda: V205ReleaseSummary())
    chk("model_count_12", lambda: None if len(_ALL_MODEL_NAMES_V205) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 models, got {len(_ALL_MODEL_NAMES_V205)}")))

    # --- should_auto_apply invariant ---
    chk("promotion_decision_auto_apply_false", lambda: None if PromotionDecision(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("PromotionDecision.should_auto_apply must always be False")))
    chk("rotation_result_auto_apply_false", lambda: None if WatchlistRotationResult(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("WatchlistRotationResult.should_auto_apply must always be False")))

    # --- watchlist rotation callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    chk("rotation_callable", lambda: run_watchlist_rotation())
    chk("rotation_paper_only", lambda: None if run_watchlist_rotation().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("rotation_no_real_orders", lambda: None if run_watchlist_rotation().no_real_orders is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders must be True")))
    chk("rotation_no_broker", lambda: None if run_watchlist_rotation().no_broker is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("rotation_all_passed", lambda: None if run_watchlist_rotation().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("rotation_should_auto_apply_false", lambda: None if run_watchlist_rotation().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))

    # --- promotion queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_promotion_queue
    chk("promotion_queue_callable", lambda: build_promotion_queue())
    chk("promotion_queue_is_list", lambda: None if isinstance(build_promotion_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_promotion_queue() must return a list")))

    # --- demotion queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_demotion_queue
    chk("demotion_queue_callable", lambda: build_demotion_queue())
    chk("demotion_queue_is_list", lambda: None if isinstance(build_demotion_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_demotion_queue() must return a list")))

    # --- quarantine queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_quarantine_queue
    chk("quarantine_queue_callable", lambda: build_quarantine_queue())
    chk("quarantine_queue_is_list", lambda: None if isinstance(build_quarantine_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_quarantine_queue() must return a list")))

    # --- human review queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import build_human_review_queue
    chk("human_review_queue_callable", lambda: build_human_review_queue())
    chk("human_review_queue_is_list", lambda: None if isinstance(build_human_review_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_human_review_queue() must return a list")))

    # --- queue summary callable ---
    chk("queue_summary_not_none", lambda: None if run_watchlist_rotation().queue_summary is not None else (_ for _ in ()).throw(
        AssertionError("queue_summary must not be None")))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        export_rotation_json, export_rotation_markdown,
        export_promotion_queue_csv, export_demotion_queue_csv,
        export_rotation_audit_snapshot,
    )
    result = run_watchlist_rotation()
    chk("export_json_callable", lambda: export_rotation_json(result))
    chk("export_json_valid", lambda: None if export_rotation_json(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_rotation_json is_valid must be True")))
    chk("export_md_callable", lambda: export_rotation_markdown(result))
    chk("export_md_valid", lambda: None if export_rotation_markdown(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_rotation_markdown is_valid must be True")))
    chk("export_promo_csv_callable", lambda: export_promotion_queue_csv(result))
    chk("export_promo_csv_valid", lambda: None if export_promotion_queue_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_promotion_queue_csv is_valid must be True")))
    chk("export_demo_csv_callable", lambda: export_demotion_queue_csv(result))
    chk("export_audit_callable", lambda: export_rotation_audit_snapshot(result))

    # --- CLI callable (from command_registry) ---
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
        chk(f"cli_registry_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- GUI import safe ---
    chk("gui_importable", lambda: __import__("gui.small_capital_strategy_panel", fromlist=["PANEL_VERSION_V205"]))
    from gui.small_capital_strategy_panel import PANEL_VERSION_V205
    chk("panel_version_205", lambda: None if PANEL_VERSION_V205 == "2.0.5" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V205 2.0.5, got {PANEL_VERSION_V205}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v205_tab_names
    tab_names = get_tab_names()
    for tab in ["watchlist_rotation_v205", "promotion_queue_v205", "human_review_queue_v205"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing from tab_names")))
    chk("get_v205_tab_names_3", lambda: None if len(get_v205_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v205 tab names, got {len(get_v205_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    render_result = render_all_tabs()
    for tab in ["watchlist_rotation_v205", "promotion_queue_v205", "human_review_queue_v205"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' rendered with error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_global_no_error_tabs", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has global error tabs: {error_tabs}")))

    # --- paper-only guard enabled ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V205.get("paper_only") is True else (_ for _ in ()).throw(
        AssertionError("paper_only guard must be enabled")))

    # --- broker execution disabled ---
    chk("broker_execution_disabled", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("broker execution must be disabled")))

    # --- production trading blocked ---
    chk("production_trading_blocked", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("production trading must be blocked")))

    # --- no real orders ---
    chk("no_real_orders_global", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))

    # --- no automatic rebalance ---
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V205.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- no real account sync ---
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V205.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))

    # --- should_auto_apply is always False ---
    chk("should_auto_apply_always_false_flag", lambda: None if SAFETY_FLAGS_V205.get("should_auto_apply_always_false") is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false flag must be True")))

    # --- backward compatibility with v2.0.4 ---
    chk("import_v204_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v204", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import VERSION as V204
    chk("v204_version_unchanged", lambda: None if V204 == "2.0.4" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.4 VERSION changed to {V204}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    chk("v204_run_portfolio_review_callable", lambda: run_portfolio_review())

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found via relative path")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v205 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_version_205", lambda: None if all(
        s["schema_version"] == "205" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios have wrong schema_version")))
    chk("scenarios_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing paper_only=True")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v205 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_version_205", lambda: None if all(
        f["schema_version"] == "205" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures have wrong schema_version")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures missing fixture_id")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v205] {passed}/{total} passed")
    return {
        "all_passed": all_passed,
        "passed": passed,
        "failed": failed,
        "total": total,
        "errors": errors,
        "version": HEALTH_VERSION,
        "release": HEALTH_RELEASE,
    }


if __name__ == "__main__":
    result = run_health_check()
    if not result["all_passed"]:
        for e in result["errors"]:
            print(e)
    sys.exit(0 if result["all_passed"] else 1)
