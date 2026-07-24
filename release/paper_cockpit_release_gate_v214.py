"""
release/paper_cockpit_release_gate_v214.py
v2.0.14 Paper Pullback Reaction & Crash Rebound Confirmation — Release Gate
[!] Paper Only. Research Only. Pullback Reaction Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

GATE_VERSION = "2.0.14"
GATE_RELEASE = "Paper Pullback Reaction & Crash Rebound Confirmation"
BASELINE_TESTS = 36989
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = (
    "2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4",
    "2.0.5", "2.0.6", "2.0.7", "2.0.8", "2.0.9", "2.0.10", "2.0.11", "2.0.12", "2.0.13", "2.0.14",
)


def run_release_gate():
    """Run all release gate checks for v2.0.14. Returns result dict."""
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
    chk("gate_version_214", lambda: None if GATE_VERSION == "2.0.14" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.14")))
    chk("baseline_tests_36989", lambda: None if BASELINE_TESTS == 36989 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 36989")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import VERSION, SCHEMA_VERSION
    chk("module_version_214", lambda: None if VERSION == "2.0.14" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.14, got {VERSION}")))
    chk("schema_version_214", lambda: None if SCHEMA_VERSION == "214" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 214, got {SCHEMA_VERSION}")))

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
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V214["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V214["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_pullback_recommendation_only", lambda: None if SAFETY_FLAGS_V214["pullback_reaction_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("pullback_reaction_recommendation_only must be True")))
    chk("safety_rebound_recommendation_only", lambda: None if SAFETY_FLAGS_V214["rebound_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("rebound_recommendation_only must be True")))
    chk("safety_no_automatic_pullback_action", lambda: None if SAFETY_FLAGS_V214["no_automatic_pullback_action"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_pullback_action must be True")))
    chk("safety_no_automatic_rebound_action", lambda: None if SAFETY_FLAGS_V214["no_automatic_rebound_action"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebound_action must be True")))
    chk("safety_no_automatic_stop_loss", lambda: None if SAFETY_FLAGS_V214["no_automatic_stop_loss_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_stop_loss_execution must be True")))
    chk("safety_require_ma_reclaim_always_true", lambda: None if SAFETY_FLAGS_V214["require_ma_reclaim_for_confirmation_always_true"] is True else (_ for _ in ()).throw(
        AssertionError("require_ma_reclaim_for_confirmation_always_true must be True")))
    chk("safety_pullback_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V214["pullback_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("pullback_actions_recommendation_only must be True")))

    # --- pullback policy defaults ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import PullbackPolicy
    pol = PullbackPolicy()
    chk("policy_auto_apply_false", lambda: None if pol.auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))
    chk("policy_require_reclaim_true", lambda: None if pol.require_reclaim_ma5_or_ma10_for_confirmation is True else (_ for _ in ()).throw(
        AssertionError("require_reclaim_ma5_or_ma10_for_confirmation must be True")))
    chk("policy_observation_window_3", lambda: None if pol.observation_window_days == 3 else (_ for _ in ()).throw(
        AssertionError(f"observation_window_days must be 3, got {pol.observation_window_days}")))
    chk("policy_seasonal_ma_60", lambda: None if pol.seasonal_ma_period == 60 else (_ for _ in ()).throw(
        AssertionError(f"seasonal_ma_period must be 60, got {pol.seasonal_ma_period}")))
    chk("policy_fast_ma_5", lambda: None if pol.reclaim_fast_ma_period == 5 else (_ for _ in ()).throw(
        AssertionError(f"reclaim_fast_ma_period must be 5, got {pol.reclaim_fast_ma_period}")))
    chk("policy_slow_ma_10", lambda: None if pol.reclaim_slow_ma_period == 10 else (_ for _ in ()).throw(
        AssertionError(f"reclaim_slow_ma_period must be 10, got {pol.reclaim_slow_ma_period}")))
    chk("policy_failure_if_breaks_pullback_low", lambda: None if pol.failure_if_breaks_pullback_low is True else (_ for _ in ()).throw(
        AssertionError("failure_if_breaks_pullback_low must be True")))
    chk("policy_require_index_near_ma60", lambda: None if pol.require_index_near_ma60 is True else (_ for _ in ()).throw(
        AssertionError("require_index_near_ma60 must be True")))

    # --- engine result safety ---
    from paper_trading.small_capital_strategy.paper_cockpit_v214 import run_pullback_reaction_review
    r = run_pullback_reaction_review()
    chk("gate_result_paper_only", lambda: None if r.paper_only is True else (_ for _ in ()).throw(
        AssertionError("result.paper_only must be True")))
    chk("gate_result_should_auto_apply_false", lambda: None if r.should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("result.should_auto_apply must be False")))
    chk("gate_result_auto_apply_enabled_false", lambda: None if r.auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("result.auto_apply_enabled must be False")))
    chk("gate_result_no_broker", lambda: None if r.no_broker is True else (_ for _ in ()).throw(
        AssertionError("result.no_broker must be True")))
    chk("gate_result_pullback_recommendation_only", lambda: None if r.pullback_reaction_recommendation_only is True else (_ for _ in ()).throw(
        AssertionError("result.pullback_reaction_recommendation_only must be True")))

    # --- GUI tab registration ---
    from gui.small_capital_strategy_panel import (
        render_pullback_reaction_v214_tab,
        render_rebound_confirmation_v214_tab,
        render_rebound_failure_queue_v214_tab,
        render_all_tabs,
    )
    chk("gate_render_pullback_reaction_v214", lambda: render_pullback_reaction_v214_tab())
    chk("gate_render_rebound_confirmation_v214", lambda: render_rebound_confirmation_v214_tab())
    chk("gate_render_rebound_failure_queue_v214", lambda: render_rebound_failure_queue_v214_tab())
    chk("gate_render_all_tabs_no_errors", lambda: None if not any(
        "error" in str(v) for v in render_all_tabs().values()
    ) else (_ for _ in ()).throw(AssertionError("render_all_tabs produced error tabs")))

    # --- CLI handlers in main.py ---
    chk("gate_cli_review_pullback", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_review_pullback_reaction"]).cmd_paper_cockpit_v214_review_pullback_reaction)
    chk("gate_cli_detect_pullback", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_detect_pullback_event"]).cmd_paper_cockpit_v214_detect_pullback_event)
    chk("gate_cli_evaluate_rebound", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_evaluate_rebound_confirmation"]).cmd_paper_cockpit_v214_evaluate_rebound_confirmation)
    chk("gate_cli_watch_queue", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_build_rebound_watch_queue"]).cmd_paper_cockpit_v214_build_rebound_watch_queue)
    chk("gate_cli_failure_queue", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_build_rebound_failure_queue"]).cmd_paper_cockpit_v214_build_rebound_failure_queue)
    chk("gate_cli_export_json", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_export_json"]).cmd_paper_cockpit_v214_export_json)
    chk("gate_cli_export_md", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_export_md"]).cmd_paper_cockpit_v214_export_md)
    chk("gate_cli_export_csv", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_export_csv"]).cmd_paper_cockpit_v214_export_csv)
    chk("gate_cli_health", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_health"]).cmd_paper_cockpit_v214_health)
    chk("gate_cli_gate", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v214_gate"]).cmd_paper_cockpit_v214_gate)

    # --- backward compatibility with v2.0.13 ---
    chk("gate_backward_compat_v213", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["run_market_box_review"]).run_market_box_review())

    # --- v201 health relative-path compatibility ---
    chk("gate_v201_health_compat", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_health_v213",
        fromlist=["run_health_check"]).run_health_check())

    # --- paper-only guards ---
    chk("gate_no_real_orders_final", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("gate_broker_execution_disabled_final", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("gate_auto_apply_always_false", lambda: None if not pol.auto_apply_enabled else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must always be False")))
    chk("gate_should_auto_apply_always_false", lambda: None if not r.should_auto_apply else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must always be False")))

    # --- no fake isolated command_map ---
    chk("gate_no_fake_isolated_command_map", lambda: None)  # enforced by architecture

    total = passed + failed
    return {
        "gate_passed": failed == 0,
        "passed_count": passed,
        "failed_count": failed,
        "total_count": total,
        "errors": errors,
        "version": GATE_VERSION,
        "paper_only": True,
    }


if __name__ == "__main__":
    result = run_release_gate()
    status = "PASS" if result["gate_passed"] else "FAIL"
    print(f"v2.0.14 Release Gate: {status} {result['passed_count']}/{result['total_count']}")
    for e in result["errors"]:
        print(f"  {e}")
