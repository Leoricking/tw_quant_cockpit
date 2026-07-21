"""
paper_trading/small_capital_strategy/paper_cockpit_health_v206.py
v2.0.6 Paper Candidate Lifecycle & Setup Aging Control — Health Check
[!] Paper Only. Research Only. Lifecycle Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

# Ensure repo root is importable when run directly
_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

HEALTH_VERSION = "2.0.6"
HEALTH_RELEASE = "Paper Candidate Lifecycle & Setup Aging Control"


def run_health_check():
    """Run all health checks for v2.0.6 paper cockpit. Returns result dict."""
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
    chk("version_title_206", lambda: None if HEALTH_VERSION == "2.0.6" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.6 got {HEALTH_VERSION}")))
    chk("release_name_lifecycle", lambda: None if "Lifecycle" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Lifecycle': {HEALTH_RELEASE}")))

    # --- module import ---
    chk("import_paper_cockpit_v206", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v206",
        fromlist=["VERSION"]))

    # --- version constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_206", lambda: None if VERSION == "2.0.6" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.6 got {VERSION}")))
    chk("schema_version_is_206", lambda: None if SCHEMA_VERSION == "206" else (_ for _ in ()).throw(
        AssertionError(f"Expected 206 got {SCHEMA_VERSION}")))
    chk("release_name_correct", lambda: None if "Lifecycle" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Lifecycle': {RELEASE_NAME}")))

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
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V206["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V206["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V206["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_broker_execution_disabled", lambda: None if SAFETY_FLAGS_V206["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_trading_blocked", lambda: None if SAFETY_FLAGS_V206["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))

    # --- lifecycle states ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import LIFECYCLE_STATES
    chk("lifecycle_states_count_13", lambda: None if len(LIFECYCLE_STATES) == 13 else (_ for _ in ()).throw(
        AssertionError(f"Expected 13 LIFECYCLE_STATES, got {len(LIFECYCLE_STATES)}")))
    for st in ["newly_promoted", "active_candidate", "waiting_buy_point", "cooling_down",
               "stale_setup", "expired_candidate", "rescore_required",
               "downgraded_to_watchlist", "removed_from_pool", "human_review_required"]:
        chk(f"lifecycle_state_{st}", lambda s=st: None if s in LIFECYCLE_STATES else (
            _ for _ in ()).throw(AssertionError(f"Missing state: {s}")))

    # --- aging buckets ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import AGING_BUCKETS
    chk("aging_buckets_count_5", lambda: None if len(AGING_BUCKETS) == 5 else (_ for _ in ()).throw(
        AssertionError(f"Expected 5 AGING_BUCKETS, got {len(AGING_BUCKETS)}")))
    for bk in ["fresh", "normal", "aging", "stale", "expired"]:
        chk(f"aging_bucket_{bk}", lambda b=bk: None if b in AGING_BUCKETS else (
            _ for _ in ()).throw(AssertionError(f"Missing bucket: {b}")))

    # --- action types ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import ACTION_TYPES
    chk("action_types_count_8", lambda: None if len(ACTION_TYPES) == 8 else (_ for _ in ()).throw(
        AssertionError(f"Expected 8 ACTION_TYPES, got {len(ACTION_TYPES)}")))
    for at in ["keep_active", "keep_waiting", "move_to_cooldown", "mark_stale",
               "require_rescore", "downgrade_to_watchlist", "remove_from_candidate_pool",
               "require_human_review"]:
        chk(f"action_type_{at}", lambda a=at: None if a in ACTION_TYPES else (
            _ for _ in ()).throw(AssertionError(f"Missing action type: {a}")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import CLI_COMMANDS_V206
    chk("cli_commands_count_11", lambda: None if len(CLI_COMMANDS_V206) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 CLI_COMMANDS_V206, got {len(CLI_COMMANDS_V206)}")))
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
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V206 else (
            _ for _ in ()).throw(AssertionError(f"Missing CLI command: {c}")))

    # --- GUI tabs ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import GUI_TABS_V206
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V206) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI_TABS_V206, got {len(GUI_TABS_V206)}")))
    for tab in ["candidate_lifecycle_v206", "setup_aging_v206", "stale_candidate_queue_v206"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in GUI_TABS_V206 else (
            _ for _ in ()).throw(AssertionError(f"Missing GUI tab: {t}")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        CandidateLifecycleItem, SetupAgingPolicy, LifecycleAction, LifecycleSummary,
        LifecycleReviewInput, LifecycleReviewResult, LifecycleExportResult,
        LifecycleAuditSnapshot, LifecycleReport, StaleSetupCSV, ExpiredCandidateCSV,
        V206HealthSummary, V206ReleaseSummary, _ALL_MODEL_NAMES_V206,
    )
    chk("model_CandidateLifecycleItem", lambda: CandidateLifecycleItem())
    chk("model_SetupAgingPolicy", lambda: SetupAgingPolicy())
    chk("model_LifecycleAction", lambda: LifecycleAction())
    chk("model_LifecycleSummary", lambda: LifecycleSummary())
    chk("model_LifecycleReviewInput", lambda: LifecycleReviewInput())
    chk("model_LifecycleReviewResult", lambda: LifecycleReviewResult())
    chk("model_LifecycleExportResult", lambda: LifecycleExportResult())
    chk("model_LifecycleAuditSnapshot", lambda: LifecycleAuditSnapshot())
    chk("model_LifecycleReport", lambda: LifecycleReport())
    chk("model_StaleSetupCSV", lambda: StaleSetupCSV())
    chk("model_ExpiredCandidateCSV", lambda: ExpiredCandidateCSV())
    chk("model_V206HealthSummary", lambda: V206HealthSummary())
    chk("model_V206ReleaseSummary", lambda: V206ReleaseSummary())
    chk("model_count_13", lambda: None if len(_ALL_MODEL_NAMES_V206) == 13 else (_ for _ in ()).throw(
        AssertionError(f"Expected 13 models, got {len(_ALL_MODEL_NAMES_V206)}")))

    # --- should_auto_apply invariant ---
    chk("lifecycle_action_auto_apply_false", lambda: None if LifecycleAction(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("LifecycleAction.should_auto_apply must always be False")))
    chk("lifecycle_review_result_auto_apply_false", lambda: None if LifecycleReviewResult(should_auto_apply=True).should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("LifecycleReviewResult.should_auto_apply must always be False")))

    # --- auto_apply_enabled invariant ---
    chk("aging_policy_auto_apply_false", lambda: None if SetupAgingPolicy(auto_apply_enabled=True).auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("SetupAgingPolicy.auto_apply_enabled must always be False")))

    # --- candidate lifecycle engine callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    chk("lifecycle_review_callable", lambda: run_lifecycle_review())
    chk("lifecycle_review_paper_only", lambda: None if run_lifecycle_review().paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("lifecycle_review_no_real_orders", lambda: None if run_lifecycle_review().no_real_orders is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders must be True")))
    chk("lifecycle_review_all_passed", lambda: None if run_lifecycle_review().all_passed is True else (_ for _ in ()).throw(
        AssertionError("all_passed must be True")))
    chk("lifecycle_review_should_auto_apply_false", lambda: None if run_lifecycle_review().should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))

    # --- setup aging policy callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import SetupAgingPolicy
    chk("setup_aging_policy_callable", lambda: SetupAgingPolicy())
    chk("setup_aging_policy_auto_apply_false", lambda: None if SetupAgingPolicy().auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))

    # --- lifecycle action callable ---
    chk("lifecycle_action_callable", lambda: LifecycleAction())

    # --- lifecycle summary callable ---
    chk("lifecycle_summary_not_none", lambda: None if run_lifecycle_review().lifecycle_summary is not None else (_ for _ in ()).throw(
        AssertionError("lifecycle_summary must not be None")))

    # --- stale queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_stale_queue
    chk("stale_queue_callable", lambda: build_stale_queue())
    chk("stale_queue_is_list", lambda: None if isinstance(build_stale_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_stale_queue() must return a list")))

    # --- expired queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_expired_queue
    chk("expired_queue_callable", lambda: build_expired_queue())
    chk("expired_queue_is_list", lambda: None if isinstance(build_expired_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_expired_queue() must return a list")))

    # --- rescore queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_rescore_queue
    chk("rescore_queue_callable", lambda: build_rescore_queue())
    chk("rescore_queue_is_list", lambda: None if isinstance(build_rescore_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_rescore_queue() must return a list")))

    # --- cooldown queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_cooldown_queue
    chk("cooldown_queue_callable", lambda: build_cooldown_queue())
    chk("cooldown_queue_is_list", lambda: None if isinstance(build_cooldown_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_cooldown_queue() must return a list")))

    # --- human review queue callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import build_human_review_queue
    chk("human_review_queue_callable", lambda: build_human_review_queue())
    chk("human_review_queue_is_list", lambda: None if isinstance(build_human_review_queue(), list) else (_ for _ in ()).throw(
        AssertionError("build_human_review_queue() must return a list")))

    # --- evaluate_aging callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import evaluate_aging
    chk("evaluate_aging_callable", lambda: evaluate_aging())
    chk("evaluate_aging_is_list", lambda: None if isinstance(evaluate_aging(), list) else (_ for _ in ()).throw(
        AssertionError("evaluate_aging() must return a list")))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import (
        export_lifecycle_json, export_lifecycle_markdown,
        export_stale_setup_csv, export_expired_candidate_csv,
        export_lifecycle_action_csv, export_lifecycle_audit_snapshot,
    )
    result = run_lifecycle_review()
    chk("export_json_callable", lambda: export_lifecycle_json(result))
    chk("export_json_valid", lambda: None if export_lifecycle_json(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_lifecycle_json is_valid must be True")))
    chk("export_md_callable", lambda: export_lifecycle_markdown(result))
    chk("export_md_valid", lambda: None if export_lifecycle_markdown(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_lifecycle_markdown is_valid must be True")))
    chk("export_stale_csv_callable", lambda: export_stale_setup_csv(result))
    chk("export_stale_csv_valid", lambda: None if export_stale_setup_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_stale_setup_csv is_valid must be True")))
    chk("export_expired_csv_callable", lambda: export_expired_candidate_csv(result))
    chk("export_expired_csv_valid", lambda: None if export_expired_candidate_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_expired_candidate_csv is_valid must be True")))
    chk("export_action_csv_callable", lambda: export_lifecycle_action_csv(result))
    chk("export_action_csv_valid", lambda: None if export_lifecycle_action_csv(result).is_valid is True else (_ for _ in ()).throw(
        AssertionError("export_lifecycle_action_csv is_valid must be True")))
    chk("export_audit_callable", lambda: export_lifecycle_audit_snapshot(result))

    # --- CLI callable (from command_registry) ---
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
        chk(f"cli_registry_{cmd}", lambda c=cmd: None if c in cmd_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' not in PROVIDER_COMMANDS")))

    # --- GUI import safe ---
    chk("gui_importable", lambda: __import__("gui.small_capital_strategy_panel", fromlist=["PANEL_VERSION_V206"]))
    from gui.small_capital_strategy_panel import PANEL_VERSION_V206
    chk("panel_version_206", lambda: None if PANEL_VERSION_V206 == "2.0.6" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V206 2.0.6, got {PANEL_VERSION_V206}")))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import get_tab_names, get_v206_tab_names
    tab_names = get_tab_names()
    for tab in ["candidate_lifecycle_v206", "setup_aging_v206", "stale_candidate_queue_v206"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"GUI tab '{t}' missing from tab_names")))
    chk("get_v206_tab_names_3", lambda: None if len(get_v206_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v206 tab names, got {len(get_v206_tab_names())}")))

    # --- render_all_tabs no error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    render_result = render_all_tabs()
    for tab in ["candidate_lifecycle_v206", "setup_aging_v206", "stale_candidate_queue_v206"]:
        chk(f"render_tab_{tab}_no_error", lambda t=tab: None if "error" not in render_result.get(t, {}) else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' rendered with error: {render_result.get(t, {}).get('error')}")))
    error_tabs = [k for k, v in render_result.items() if "error" in v]
    chk("render_all_tabs_global_no_error_tabs", lambda: None if not error_tabs else (_ for _ in ()).throw(
        AssertionError(f"render_all_tabs has global error tabs: {error_tabs}")))

    # --- paper-only guard enabled ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V206.get("paper_only") is True else (_ for _ in ()).throw(
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
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V206.get("no_automatic_rebalance") is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))

    # --- no real account sync ---
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V206.get("no_real_account_sync") is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))

    # --- auto_apply_enabled is always False ---
    chk("auto_apply_enabled_always_false_flag", lambda: None if SAFETY_FLAGS_V206.get("auto_apply_enabled_always_false") is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false flag must be True")))

    # --- backward compatibility with v2.0.5 ---
    chk("import_v205_still_works", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v205", fromlist=["VERSION"]))
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import VERSION as V205
    chk("v205_version_unchanged", lambda: None if V205 == "2.0.5" else (_ for _ in ()).throw(
        AssertionError(f"v2.0.5 VERSION changed to {V205}")))
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation
    chk("v205_run_watchlist_rotation_callable", lambda: run_watchlist_rotation())

    # --- v201 health relative-path compatibility preserved ---
    import os as _os
    chk("v201_health_test_relative_path", lambda: None if _os.path.exists(
        _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "..", "tests", "test_paper_cockpit_v201.py"))
    ) else (_ for _ in ()).throw(AssertionError("test_paper_cockpit_v201.py not found via relative path")))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v206 import SCENARIOS
    chk("scenarios_count_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios, got {len(SCENARIOS)}")))
    chk("scenarios_schema_version_206", lambda: None if all(
        s["schema_version"] == "206" for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios have wrong schema_version")))
    chk("scenarios_paper_only", lambda: None if all(
        s["paper_only"] is True for s in SCENARIOS) else (_ for _ in ()).throw(
        AssertionError("Some scenarios missing paper_only=True")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v206 import FIXTURES
    chk("fixtures_count_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures, got {len(FIXTURES)}")))
    chk("fixtures_schema_version_206", lambda: None if all(
        f["schema_version"] == "206" for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures have wrong schema_version")))
    chk("fixtures_have_fixture_id", lambda: None if all(
        "fixture_id" in f for f in FIXTURES) else (_ for _ in ()).throw(
        AssertionError("Some fixtures missing fixture_id")))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v206] {passed}/{total} passed")
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
