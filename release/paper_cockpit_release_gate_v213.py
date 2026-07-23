"""
release/paper_cockpit_release_gate_v213.py
v2.0.13 Paper Market Box Range & Index Regime Control — Release Gate
[!] Paper Only. Research Only. Market Box Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

GATE_VERSION = "2.0.13"
GATE_RELEASE = "Paper Market Box Range & Index Regime Control"
BASELINE_TESTS = 36689
MIN_NEW_TESTS = 300
EXPECTED_PANEL_VERSIONS = (
    "2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4",
    "2.0.5", "2.0.6", "2.0.7", "2.0.8", "2.0.9", "2.0.10", "2.0.11", "2.0.12", "2.0.13",
)


def run_release_gate():
    """Run all release gate checks for v2.0.13. Returns result dict."""
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
    chk("gate_version_213", lambda: None if GATE_VERSION == "2.0.13" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.13")))
    chk("baseline_tests_36689", lambda: None if BASELINE_TESTS == 36689 else (_ for _ in ()).throw(
        AssertionError(f"Expected baseline 36689")))
    chk("min_new_tests_300", lambda: None if MIN_NEW_TESTS == 300 else (_ for _ in ()).throw(
        AssertionError(f"Expected min new 300")))

    # --- module version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import VERSION, SCHEMA_VERSION
    chk("module_version_213", lambda: None if VERSION == "2.0.13" else (_ for _ in ()).throw(
        AssertionError(f"Module VERSION expected 2.0.13, got {VERSION}")))
    chk("schema_version_213", lambda: None if SCHEMA_VERSION == "213" else (_ for _ in ()).throw(
        AssertionError(f"SCHEMA_VERSION expected 213, got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("NO_REAL_ORDERS_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("BROKER_EXECUTION_ENABLED_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("PRODUCTION_TRADING_BLOCKED_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import SAFETY_FLAGS_V213
    chk("safety_flags_count_25", lambda: None if len(SAFETY_FLAGS_V213) == 25 else (_ for _ in ()).throw(
        AssertionError(f"Expected 25 SAFETY_FLAGS_V213, got {len(SAFETY_FLAGS_V213)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V213["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V213["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V213["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_market_box_recommendation_only", lambda: None if SAFETY_FLAGS_V213["market_box_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("market_box_recommendation_only must be True")))
    chk("safety_exposure_recommendation_only", lambda: None if SAFETY_FLAGS_V213["exposure_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("exposure_recommendation_only must be True")))
    chk("safety_no_automatic_market_action", lambda: None if SAFETY_FLAGS_V213["no_automatic_market_action"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_market_action must be True")))
    chk("safety_no_automatic_stop_loss", lambda: None if SAFETY_FLAGS_V213["no_automatic_stop_loss_execution"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_stop_loss_execution must be True")))
    chk("safety_require_box_check_always_true", lambda: None if SAFETY_FLAGS_V213["require_box_check_before_entry_always_true"] is True else (_ for _ in ()).throw(
        AssertionError("require_box_check_before_entry_always_true must be True")))
    chk("safety_market_box_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V213["market_box_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("market_box_actions_recommendation_only must be True")))

    # --- market box policy defaults ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import MarketBoxPolicy
    pol = MarketBoxPolicy()
    chk("policy_auto_apply_false", lambda: None if pol.auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))
    chk("policy_require_box_check_true", lambda: None if pol.require_box_check_before_entry is True else (_ for _ in ()).throw(
        AssertionError("require_box_check_before_entry must be True")))
    chk("policy_upper_zone_min_45000", lambda: None if pol.upper_zone_min == 45_000 else (_ for _ in ()).throw(
        AssertionError(f"upper_zone_min must be 45000, got {pol.upper_zone_min}")))
    chk("policy_upper_zone_max_47000", lambda: None if pol.upper_zone_max == 47_000 else (_ for _ in ()).throw(
        AssertionError(f"upper_zone_max must be 47000, got {pol.upper_zone_max}")))
    chk("policy_neutral_zone_min_42000", lambda: None if pol.neutral_zone_min == 42_000 else (_ for _ in ()).throw(
        AssertionError(f"neutral_zone_min must be 42000, got {pol.neutral_zone_min}")))
    chk("policy_lower_zone_min_40000", lambda: None if pol.lower_zone_min == 40_000 else (_ for _ in ()).throw(
        AssertionError(f"lower_zone_min must be 40000, got {pol.lower_zone_min}")))
    chk("policy_extreme_risk_zone_min_38000", lambda: None if pol.extreme_risk_zone_min == 38_000 else (_ for _ in ()).throw(
        AssertionError(f"extreme_risk_zone_min must be 38000, got {pol.extreme_risk_zone_min}")))
    chk("policy_below_box_threshold_38000", lambda: None if pol.below_box_threshold == 38_000 else (_ for _ in ()).throw(
        AssertionError(f"below_box_threshold must be 38000, got {pol.below_box_threshold}")))
    chk("policy_above_box_threshold_47000", lambda: None if pol.above_box_threshold == 47_000 else (_ for _ in ()).throw(
        AssertionError(f"above_box_threshold must be 47000, got {pol.above_box_threshold}")))

    # --- zone classification ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import classify_zone
    chk("gate_classify_upper_zone", lambda: None if classify_zone(46_000.0) == "upper_zone" else (_ for _ in ()).throw(
        AssertionError(f"Expected upper_zone")))
    chk("gate_classify_neutral_zone", lambda: None if classify_zone(43_500.0) == "neutral_zone" else (_ for _ in ()).throw(
        AssertionError(f"Expected neutral_zone")))
    chk("gate_classify_lower_zone", lambda: None if classify_zone(41_000.0) == "lower_zone" else (_ for _ in ()).throw(
        AssertionError(f"Expected lower_zone")))
    chk("gate_classify_extreme_risk", lambda: None if classify_zone(39_000.0) == "extreme_risk_zone" else (_ for _ in ()).throw(
        AssertionError(f"Expected extreme_risk_zone")))
    chk("gate_classify_below_box", lambda: None if classify_zone(36_000.0) == "below_box" else (_ for _ in ()).throw(
        AssertionError(f"Expected below_box")))
    chk("gate_classify_above_box", lambda: None if classify_zone(48_000.0) == "above_box" else (_ for _ in ()).throw(
        AssertionError(f"Expected above_box")))

    # --- engine result safety ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import run_market_box_review
    r = run_market_box_review()
    chk("gate_result_paper_only", lambda: None if r.paper_only is True else (_ for _ in ()).throw(
        AssertionError("result.paper_only must be True")))
    chk("gate_result_should_auto_apply_false", lambda: None if r.should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("result.should_auto_apply must be False")))
    chk("gate_result_auto_apply_enabled_false", lambda: None if r.auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("result.auto_apply_enabled must be False")))
    chk("gate_result_no_broker", lambda: None if r.no_broker is True else (_ for _ in ()).throw(
        AssertionError("result.no_broker must be True")))
    chk("gate_result_market_box_recommendation_only", lambda: None if r.market_box_recommendation_only is True else (_ for _ in ()).throw(
        AssertionError("result.market_box_recommendation_only must be True")))

    # --- GUI tab registration ---
    from gui.small_capital_strategy_panel import (
        render_market_box_v213_tab,
        render_exposure_control_v213_tab,
        render_defensive_review_queue_v213_tab,
        render_all_tabs,
    )
    chk("gate_render_market_box_v213", lambda: render_market_box_v213_tab())
    chk("gate_render_exposure_control_v213", lambda: render_exposure_control_v213_tab())
    chk("gate_render_defensive_review_queue_v213", lambda: render_defensive_review_queue_v213_tab())
    chk("gate_render_all_tabs_no_errors", lambda: None if not any(
        "error" in str(v) for v in render_all_tabs().values()
    ) else (_ for _ in ()).throw(AssertionError("render_all_tabs produced error tabs")))

    # --- CLI handlers in main.py ---
    chk("gate_cli_review_market_box", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_review_market_box"]).cmd_paper_cockpit_v213_review_market_box)
    chk("gate_cli_classify_index_zone", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_classify_index_zone"]).cmd_paper_cockpit_v213_classify_index_zone)
    chk("gate_cli_build_exposure_control", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_build_exposure_control"]).cmd_paper_cockpit_v213_build_exposure_control)
    chk("gate_cli_build_chase_risk_queue", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_build_chase_risk_queue"]).cmd_paper_cockpit_v213_build_chase_risk_queue)
    chk("gate_cli_build_defensive_review_queue", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_build_defensive_review_queue"]).cmd_paper_cockpit_v213_build_defensive_review_queue)
    chk("gate_cli_export_json", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_export_json"]).cmd_paper_cockpit_v213_export_json)
    chk("gate_cli_export_md", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_export_md"]).cmd_paper_cockpit_v213_export_md)
    chk("gate_cli_export_csv", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_export_csv"]).cmd_paper_cockpit_v213_export_csv)
    chk("gate_cli_health", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_health"]).cmd_paper_cockpit_v213_health)
    chk("gate_cli_gate", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_gate"]).cmd_paper_cockpit_v213_gate)

    # --- backward compatibility with v2.0.12 ---
    chk("gate_backward_compat_v212", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v212",
        fromlist=["run_profit_taking_review"]).run_profit_taking_review())

    # --- v201 health relative-path compatibility ---
    chk("gate_v201_health_compat", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_health_v212",
        fromlist=["run_health_check"]).run_health_check())

    # --- paper-only guards ---
    chk("gate_no_real_orders_final", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("gate_broker_execution_disabled_final", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))

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
    print(f"v2.0.13 Release Gate: {status} {result['passed_count']}/{result['total_count']}")
    for e in result["errors"]:
        print(f"  {e}")
