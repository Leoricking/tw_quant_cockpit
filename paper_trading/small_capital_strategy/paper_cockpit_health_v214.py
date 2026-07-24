"""
paper_trading/small_capital_strategy/paper_cockpit_health_v214.py
v2.0.14 Paper Pullback Reaction & Crash Rebound Confirmation — Health Check
[!] Paper Only. Research Only. Pullback Reaction Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

HEALTH_VERSION = "2.0.14"
HEALTH_RELEASE = "Paper Pullback Reaction & Crash Rebound Confirmation"


def run_health_check():
    """Run all health checks for v2.0.14 paper cockpit. Returns result dict."""
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
    chk("version_title_214", lambda: None if HEALTH_VERSION == "2.0.14" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.14 got {HEALTH_VERSION}")))
    chk("release_name_pullback", lambda: None if "Pullback" in HEALTH_RELEASE or "Rebound" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Pullback': {HEALTH_RELEASE}")))
    chk("release_name_crash", lambda: None if "Crash" in HEALTH_RELEASE or "Confirmation" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Crash': {HEALTH_RELEASE}")))

    # --- module import ---
    chk("import_paper_cockpit_v214", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v214",
        fromlist=["VERSION"]))

    # --- version constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_214", lambda: None if VERSION == "2.0.14" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.14 got {VERSION}")))
    chk("schema_version_is_214", lambda: None if SCHEMA_VERSION == "214" else (_ for _ in ()).throw(
        AssertionError(f"Expected 214 got {SCHEMA_VERSION}")))
    chk("release_name_contains_pullback", lambda: None if "Pullback" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Pullback': {RELEASE_NAME}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import SAFETY_FLAGS_V214
    chk("safety_flags_count_25", lambda: None if len(SAFETY_FLAGS_V214) == 25 else (_ for _ in ()).throw(
        AssertionError(f"Expected 25 SAFETY_FLAGS_V214, got {len(SAFETY_FLAGS_V214)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V214["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V214["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V214["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V214["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_pullback_recommendation_only", lambda: None if SAFETY_FLAGS_V214["pullback_reaction_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("pullback_reaction_recommendation_only must be True")))
    chk("safety_rebound_recommendation_only", lambda: None if SAFETY_FLAGS_V214["rebound_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("rebound_recommendation_only must be True")))
    chk("safety_broker_execution_disabled", lambda: None if SAFETY_FLAGS_V214["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_trading_blocked", lambda: None if SAFETY_FLAGS_V214["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))
    chk("safety_no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V214["no_automatic_rebalance"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))
    chk("safety_no_real_account_sync", lambda: None if SAFETY_FLAGS_V214["no_real_account_sync"] is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))
    chk("safety_no_automatic_pullback_action", lambda: None if SAFETY_FLAGS_V214["no_automatic_pullback_action"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_pullback_action must be True")))
    chk("safety_no_automatic_rebound_action", lambda: None if SAFETY_FLAGS_V214["no_automatic_rebound_action"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebound_action must be True")))
    chk("safety_require_ma_reclaim_always_true", lambda: None if SAFETY_FLAGS_V214["require_ma_reclaim_for_confirmation_always_true"] is True else (_ for _ in ()).throw(
        AssertionError("require_ma_reclaim_for_confirmation_always_true must be True")))
    chk("safety_pullback_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V214["pullback_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("pullback_actions_recommendation_only must be True")))

    # --- REACTION_STATES ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import REACTION_STATES
    chk("reaction_states_count_6", lambda: None if len(REACTION_STATES) == 6 else (_ for _ in ()).throw(
        AssertionError(f"Expected 6 REACTION_STATES, got {len(REACTION_STATES)}")))
    for rs in ["no_pullback", "observation_rebound", "short_term_rebound_confirmed",
               "rebound_failed", "defensive_wait_second_confirmation", "human_review_required"]:
        chk(f"reaction_state_{rs}", lambda s=rs: None if s in REACTION_STATES else (_ for _ in ()).throw(
            AssertionError(f"Missing reaction state: {s}")))

    # --- RECOMMENDED_ACTIONS ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import RECOMMENDED_ACTIONS
    chk("recommended_actions_count_6", lambda: None if len(RECOMMENDED_ACTIONS) == 6 else (_ for _ in ()).throw(
        AssertionError(f"Expected 6 RECOMMENDED_ACTIONS, got {len(RECOMMENDED_ACTIONS)}")))
    for ra in ["observation_only", "wait_for_ma_reclaim", "short_term_rebound_confirmed",
               "defensive_mode", "rebound_failed_reduce_risk", "human_review_required"]:
        chk(f"recommended_action_{ra}", lambda a=ra: None if a in RECOMMENDED_ACTIONS else (_ for _ in ()).throw(
            AssertionError(f"Missing recommended action: {a}")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import CLI_COMMANDS_V214
    chk("cli_commands_count_10", lambda: None if len(CLI_COMMANDS_V214) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI_COMMANDS_V214, got {len(CLI_COMMANDS_V214)}")))
    for cmd in [
        "paper-cockpit-v214-review-pullback-reaction",
        "paper-cockpit-v214-detect-pullback-event",
        "paper-cockpit-v214-evaluate-rebound-confirmation",
        "paper-cockpit-v214-build-rebound-watch-queue",
        "paper-cockpit-v214-build-rebound-failure-queue",
        "paper-cockpit-v214-export-json",
        "paper-cockpit-v214-export-md",
        "paper-cockpit-v214-export-csv",
        "paper-cockpit-v214-health",
        "paper-cockpit-v214-gate",
    ]:
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V214 else (_ for _ in ()).throw(
            AssertionError(f"Missing CLI command: {c}")))

    # --- GUI tabs ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import GUI_TABS_V214
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V214) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI_TABS_V214, got {len(GUI_TABS_V214)}")))
    for tab in ["pullback_reaction_v214", "rebound_confirmation_v214", "rebound_failure_queue_v214"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in GUI_TABS_V214 else (_ for _ in ()).throw(
            AssertionError(f"Missing GUI tab: {t}")))

    # --- pullback policy callable ---
    chk("pullback_policy_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v214",
        fromlist=["PullbackPolicy"]).PullbackPolicy())

    # --- pullback event schema callable ---
    chk("pullback_event_schema_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v214",
        fromlist=["PullbackEvent"]).PullbackEvent())

    # --- confirmation signal schema callable ---
    chk("confirmation_signal_schema_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v214",
        fromlist=["ConfirmationSignal"]).ConfirmationSignal())

    # --- pullback summary callable ---
    chk("pullback_summary_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v214",
        fromlist=["PullbackSummary"]).PullbackSummary())

    # --- engine callable ---
    chk("pullback_engine_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v214",
        fromlist=["run_pullback_reaction_review"]).run_pullback_reaction_review())

    # --- detect_pullback_event callable ---
    chk("detect_pullback_event_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v214",
        fromlist=["detect_pullback_event"]).detect_pullback_event(43_000.0))

    # --- evaluate_rebound_confirmation callable ---
    chk("evaluate_rebound_confirmation_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v214",
        fromlist=["evaluate_rebound_confirmation"]).evaluate_rebound_confirmation())

    # --- build_rebound_watch_queue callable ---
    chk("build_rebound_watch_queue_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v214",
        fromlist=["build_rebound_watch_queue"]).build_rebound_watch_queue("observation_rebound"))

    # --- build_rebound_failure_queue callable ---
    chk("build_rebound_failure_queue_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v214",
        fromlist=["build_rebound_failure_queue"]).build_rebound_failure_queue("rebound_failed"))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import (
        run_pullback_reaction_review, export_pullback_json, export_pullback_markdown,
        export_pullback_csv,
    )
    r = run_pullback_reaction_review()
    chk("export_json_callable", lambda: export_pullback_json(r))
    chk("export_markdown_callable", lambda: export_pullback_markdown(r))
    chk("export_csv_callable", lambda: export_pullback_csv(r))

    # --- paper-only guard ---
    chk("paper_only_guard_enabled", lambda: None if r.paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("should_auto_apply_false", lambda: None if r.should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))
    chk("auto_apply_enabled_false", lambda: None if r.auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))

    # --- PullbackPolicy defaults ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import PullbackPolicy
    pol = PullbackPolicy()
    chk("policy_auto_apply_false", lambda: None if pol.auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))
    chk("policy_require_reclaim_always_true", lambda: None if pol.require_reclaim_ma5_or_ma10_for_confirmation is True else (_ for _ in ()).throw(
        AssertionError("require_reclaim_ma5_or_ma10_for_confirmation must be True")))
    chk("policy_observation_window_3", lambda: None if pol.observation_window_days == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected observation_window_days=3, got {pol.observation_window_days}")))
    chk("policy_seasonal_ma_60", lambda: None if pol.seasonal_ma_period == 60 else (_ for _ in ()).throw(
        AssertionError(f"Expected seasonal_ma_period=60, got {pol.seasonal_ma_period}")))
    chk("policy_reclaim_fast_ma_5", lambda: None if pol.reclaim_fast_ma_period == 5 else (_ for _ in ()).throw(
        AssertionError(f"Expected reclaim_fast_ma_period=5, got {pol.reclaim_fast_ma_period}")))
    chk("policy_reclaim_slow_ma_10", lambda: None if pol.reclaim_slow_ma_period == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected reclaim_slow_ma_period=10, got {pol.reclaim_slow_ma_period}")))
    chk("policy_failure_if_breaks_pullback_low", lambda: None if pol.failure_if_breaks_pullback_low is True else (_ for _ in ()).throw(
        AssertionError("failure_if_breaks_pullback_low must be True")))

    # --- broker execution disabled ---
    chk("broker_execution_disabled", lambda: None if SAFETY_FLAGS_V214["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))

    # --- production trading blocked ---
    chk("production_trading_blocked", lambda: None if SAFETY_FLAGS_V214["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))

    # --- backward compatibility with v2.0.13 ---
    chk("backward_compat_v213_import", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["VERSION"]))

    # --- v201 health relative-path compatibility ---
    chk("v201_health_relative_path_compat", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_health_v213",
        fromlist=["run_health_check"]))

    # --- GUI import safe ---
    chk("gui_import_safe", lambda: __import__(
        "gui.small_capital_strategy_panel",
        fromlist=["render_all_tabs"]))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import (
        render_pullback_reaction_v214_tab,
        render_rebound_confirmation_v214_tab,
        render_rebound_failure_queue_v214_tab,
    )
    chk("render_pullback_reaction_v214_tab", lambda: render_pullback_reaction_v214_tab())
    chk("render_rebound_confirmation_v214_tab", lambda: render_rebound_confirmation_v214_tab())
    chk("render_rebound_failure_queue_v214_tab", lambda: render_rebound_failure_queue_v214_tab())

    # --- render_all_tabs no error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    chk("render_all_tabs_no_errors", lambda: None if not any(
        "error" in str(v) for v in render_all_tabs().values()
    ) else (_ for _ in ()).throw(AssertionError("render_all_tabs produced error tabs")))

    # --- CLI handler in main.py ---
    chk("cli_handler_main_review_pullback", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_review_pullback_reaction"]).cmd_paper_cockpit_v214_review_pullback_reaction)
    chk("cli_handler_main_detect_pullback", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_detect_pullback_event"]).cmd_paper_cockpit_v214_detect_pullback_event)
    chk("cli_handler_main_evaluate_rebound", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_evaluate_rebound_confirmation"]).cmd_paper_cockpit_v214_evaluate_rebound_confirmation)
    chk("cli_handler_main_watch_queue", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_build_rebound_watch_queue"]).cmd_paper_cockpit_v214_build_rebound_watch_queue)
    chk("cli_handler_main_failure_queue", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_build_rebound_failure_queue"]).cmd_paper_cockpit_v214_build_rebound_failure_queue)
    chk("cli_handler_main_export_json", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_export_json"]).cmd_paper_cockpit_v214_export_json)
    chk("cli_handler_main_export_md", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_export_md"]).cmd_paper_cockpit_v214_export_md)
    chk("cli_handler_main_export_csv", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_export_csv"]).cmd_paper_cockpit_v214_export_csv)
    chk("cli_handler_main_health", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_health"]).cmd_paper_cockpit_v214_health)
    chk("cli_handler_main_gate", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_gate"]).cmd_paper_cockpit_v214_gate)

    # --- verify_version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import verify_version
    chk("verify_version_214", lambda: None if verify_version() is True else (_ for _ in ()).throw(
        AssertionError("verify_version() must return True")))

    total = passed + failed
    return {
        "all_passed": failed == 0,
        "passed": passed,
        "failed": failed,
        "total": total,
        "errors": errors,
        "version": HEALTH_VERSION,
        "paper_only": True,
    }


if __name__ == "__main__":
    result = run_health_check()
    status = "PASS" if result["all_passed"] else "FAIL"
    print(f"v2.0.14 Health: {status} {result['passed']}/{result['total']}")
    for e in result["errors"]:
        print(f"  {e}")
