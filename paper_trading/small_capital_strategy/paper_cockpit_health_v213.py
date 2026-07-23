"""
paper_trading/small_capital_strategy/paper_cockpit_health_v213.py
v2.0.13 Paper Market Box Range & Index Regime Control — Health Check
[!] Paper Only. Research Only. Market Box Recommendation Only. Validation Only.
[!] No Real Orders. No Broker. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

HEALTH_VERSION = "2.0.13"
HEALTH_RELEASE = "Paper Market Box Range & Index Regime Control"


def run_health_check():
    """Run all health checks for v2.0.13 paper cockpit. Returns result dict."""
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
    chk("version_title_213", lambda: None if HEALTH_VERSION == "2.0.13" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.13 got {HEALTH_VERSION}")))
    chk("release_name_market_box", lambda: None if "Market" in HEALTH_RELEASE or "Box" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Market Box': {HEALTH_RELEASE}")))
    chk("release_name_regime", lambda: None if "Regime" in HEALTH_RELEASE or "Range" in HEALTH_RELEASE else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Regime': {HEALTH_RELEASE}")))

    # --- module import ---
    chk("import_paper_cockpit_v213", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["VERSION"]))

    # --- version constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import (
        VERSION, SCHEMA_VERSION, RELEASE_NAME,
    )
    chk("version_is_213", lambda: None if VERSION == "2.0.13" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.13 got {VERSION}")))
    chk("schema_version_is_213", lambda: None if SCHEMA_VERSION == "213" else (_ for _ in ()).throw(
        AssertionError(f"Expected 213 got {SCHEMA_VERSION}")))
    chk("release_name_contains_market_box", lambda: None if "Market" in RELEASE_NAME or "Box" in RELEASE_NAME else (_ for _ in ()).throw(
        AssertionError(f"Release name missing 'Market Box': {RELEASE_NAME}")))

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
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V213["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_should_auto_apply_always_false", lambda: None if SAFETY_FLAGS_V213["should_auto_apply_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("should_auto_apply_always_false must be True")))
    chk("safety_auto_apply_enabled_always_false", lambda: None if SAFETY_FLAGS_V213["auto_apply_enabled_always_false"] is True else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled_always_false must be True")))
    chk("safety_market_box_recommendation_only", lambda: None if SAFETY_FLAGS_V213["market_box_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("market_box_recommendation_only must be True")))
    chk("safety_exposure_recommendation_only", lambda: None if SAFETY_FLAGS_V213["exposure_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("exposure_recommendation_only must be True")))
    chk("safety_broker_execution_disabled", lambda: None if SAFETY_FLAGS_V213["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_trading_blocked", lambda: None if SAFETY_FLAGS_V213["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))
    chk("safety_no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V213["no_automatic_rebalance"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_rebalance must be True")))
    chk("safety_no_real_account_sync", lambda: None if SAFETY_FLAGS_V213["no_real_account_sync"] is True else (_ for _ in ()).throw(
        AssertionError("no_real_account_sync must be True")))
    chk("safety_no_automatic_market_action", lambda: None if SAFETY_FLAGS_V213["no_automatic_market_action"] is True else (_ for _ in ()).throw(
        AssertionError("no_automatic_market_action must be True")))
    chk("safety_require_box_check_always_true", lambda: None if SAFETY_FLAGS_V213["require_box_check_before_entry_always_true"] is True else (_ for _ in ()).throw(
        AssertionError("require_box_check_before_entry_always_true must be True")))
    chk("safety_market_box_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V213["market_box_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("market_box_actions_recommendation_only must be True")))
    chk("safety_exposure_actions_recommendation_only", lambda: None if SAFETY_FLAGS_V213["exposure_actions_recommendation_only"] is True else (_ for _ in ()).throw(
        AssertionError("exposure_actions_recommendation_only must be True")))

    # --- ZONE_NAMES ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import ZONE_NAMES
    chk("zone_names_count_6", lambda: None if len(ZONE_NAMES) == 6 else (_ for _ in ()).throw(
        AssertionError(f"Expected 6 ZONE_NAMES, got {len(ZONE_NAMES)}")))
    for zn in ["upper_zone", "neutral_zone", "lower_zone", "extreme_risk_zone", "below_box", "above_box"]:
        chk(f"zone_name_{zn}", lambda z=zn: None if z in ZONE_NAMES else (_ for _ in ()).throw(
            AssertionError(f"Missing zone: {z}")))

    # --- EXPOSURE_ACTIONS ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import EXPOSURE_ACTIONS
    chk("exposure_actions_count_8", lambda: None if len(EXPOSURE_ACTIONS) == 8 else (_ for _ in ()).throw(
        AssertionError(f"Expected 8 EXPOSURE_ACTIONS, got {len(EXPOSURE_ACTIONS)}")))
    for ea in [
        "hold_current_exposure", "reduce_exposure_near_upper_box", "normal_selective_exposure",
        "core_only_low_zone", "defensive_extreme_risk", "below_box_defense",
        "overheating_above_box", "human_review_required",
    ]:
        chk(f"exposure_action_{ea}", lambda a=ea: None if a in EXPOSURE_ACTIONS else (_ for _ in ()).throw(
            AssertionError(f"Missing exposure action: {a}")))

    # --- CLI commands ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import CLI_COMMANDS_V213
    chk("cli_commands_count_10", lambda: None if len(CLI_COMMANDS_V213) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 CLI_COMMANDS_V213, got {len(CLI_COMMANDS_V213)}")))
    for cmd in [
        "paper-cockpit-v213-review-market-box",
        "paper-cockpit-v213-classify-index-zone",
        "paper-cockpit-v213-build-exposure-control",
        "paper-cockpit-v213-build-chase-risk-queue",
        "paper-cockpit-v213-build-defensive-review-queue",
        "paper-cockpit-v213-export-json",
        "paper-cockpit-v213-export-md",
        "paper-cockpit-v213-export-csv",
        "paper-cockpit-v213-health",
        "paper-cockpit-v213-gate",
    ]:
        chk(f"cli_cmd_{cmd}", lambda c=cmd: None if c in CLI_COMMANDS_V213 else (_ for _ in ()).throw(
            AssertionError(f"Missing CLI command: {c}")))

    # --- GUI tabs ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import GUI_TABS_V213
    chk("gui_tabs_count_3", lambda: None if len(GUI_TABS_V213) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI_TABS_V213, got {len(GUI_TABS_V213)}")))
    for tab in ["market_box_v213", "exposure_control_v213", "defensive_review_queue_v213"]:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in GUI_TABS_V213 else (_ for _ in ()).throw(
            AssertionError(f"Missing GUI tab: {t}")))

    # --- market box policy callable ---
    chk("market_box_policy_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["MarketBoxPolicy"]).MarketBoxPolicy())

    # --- index snapshot schema callable ---
    chk("index_snapshot_schema_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["IndexSnapshot"]).IndexSnapshot())

    # --- exposure recommendation schema callable ---
    chk("exposure_recommendation_schema_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["ExposureRecommendation"]).ExposureRecommendation())

    # --- market box summary callable ---
    chk("market_box_summary_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["MarketBoxSummary"]).MarketBoxSummary())

    # --- engine callable ---
    chk("market_box_engine_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["run_market_box_review"]).run_market_box_review())

    # --- classify_index_zone callable ---
    chk("classify_index_zone_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["classify_index_zone"]).classify_index_zone(43_500.0))

    # --- build_exposure_recommendation callable ---
    chk("build_exposure_recommendation_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["build_exposure_recommendation"]).build_exposure_recommendation("neutral_zone"))

    # --- build_chase_risk_queue callable ---
    chk("build_chase_risk_queue_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["build_chase_risk_queue"]).build_chase_risk_queue("upper_zone"))

    # --- build_defensive_review_queue callable ---
    chk("build_defensive_review_queue_callable", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v213",
        fromlist=["build_defensive_review_queue"]).build_defensive_review_queue("extreme_risk_zone"))

    # --- export integration callable ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import (
        run_market_box_review, export_market_box_json, export_market_box_markdown,
        export_market_box_csv,
    )
    r = run_market_box_review()
    chk("export_json_callable", lambda: export_market_box_json(r))
    chk("export_markdown_callable", lambda: export_market_box_markdown(r))
    chk("export_csv_callable", lambda: export_market_box_csv(r))

    # --- paper-only guard ---
    chk("paper_only_guard_enabled", lambda: None if r.paper_only is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("should_auto_apply_false", lambda: None if r.should_auto_apply is False else (_ for _ in ()).throw(
        AssertionError("should_auto_apply must be False")))
    chk("auto_apply_enabled_false", lambda: None if r.auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))

    # --- MarketBoxPolicy defaults ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import MarketBoxPolicy
    pol = MarketBoxPolicy()
    chk("policy_auto_apply_false", lambda: None if pol.auto_apply_enabled is False else (_ for _ in ()).throw(
        AssertionError("auto_apply_enabled must be False")))
    chk("policy_require_box_check_true", lambda: None if pol.require_box_check_before_entry is True else (_ for _ in ()).throw(
        AssertionError("require_box_check_before_entry must be True")))
    chk("policy_upper_zone_min_45000", lambda: None if pol.upper_zone_min == 45_000 else (_ for _ in ()).throw(
        AssertionError(f"Expected upper_zone_min=45000, got {pol.upper_zone_min}")))
    chk("policy_upper_zone_max_47000", lambda: None if pol.upper_zone_max == 47_000 else (_ for _ in ()).throw(
        AssertionError(f"Expected upper_zone_max=47000, got {pol.upper_zone_max}")))
    chk("policy_below_box_threshold_38000", lambda: None if pol.below_box_threshold == 38_000 else (_ for _ in ()).throw(
        AssertionError(f"Expected below_box_threshold=38000, got {pol.below_box_threshold}")))
    chk("policy_above_box_threshold_47000", lambda: None if pol.above_box_threshold == 47_000 else (_ for _ in ()).throw(
        AssertionError(f"Expected above_box_threshold=47000, got {pol.above_box_threshold}")))

    # --- zone classification correctness ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import classify_zone
    chk("classify_upper_zone", lambda: None if classify_zone(46_000.0) == "upper_zone" else (_ for _ in ()).throw(
        AssertionError(f"Expected upper_zone, got {classify_zone(46_000.0)}")))
    chk("classify_neutral_zone", lambda: None if classify_zone(43_500.0) == "neutral_zone" else (_ for _ in ()).throw(
        AssertionError(f"Expected neutral_zone, got {classify_zone(43_500.0)}")))
    chk("classify_lower_zone", lambda: None if classify_zone(41_000.0) == "lower_zone" else (_ for _ in ()).throw(
        AssertionError(f"Expected lower_zone, got {classify_zone(41_000.0)}")))
    chk("classify_extreme_risk_zone", lambda: None if classify_zone(39_000.0) == "extreme_risk_zone" else (_ for _ in ()).throw(
        AssertionError(f"Expected extreme_risk_zone, got {classify_zone(39_000.0)}")))
    chk("classify_below_box", lambda: None if classify_zone(36_000.0) == "below_box" else (_ for _ in ()).throw(
        AssertionError(f"Expected below_box, got {classify_zone(36_000.0)}")))
    chk("classify_above_box", lambda: None if classify_zone(48_000.0) == "above_box" else (_ for _ in ()).throw(
        AssertionError(f"Expected above_box, got {classify_zone(48_000.0)}")))

    # --- broker execution disabled ---
    chk("broker_execution_disabled", lambda: None if SAFETY_FLAGS_V213["broker_execution_disabled"] is True else (_ for _ in ()).throw(
        AssertionError("broker_execution_disabled must be True")))

    # --- production trading blocked ---
    chk("production_trading_blocked", lambda: None if SAFETY_FLAGS_V213["production_trading_blocked"] is True else (_ for _ in ()).throw(
        AssertionError("production_trading_blocked must be True")))

    # --- backward compatibility with v2.0.12 ---
    chk("backward_compat_v212_import", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v212",
        fromlist=["VERSION"]))

    # --- v201 health relative-path compatibility ---
    chk("v201_health_relative_path_compat", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_health_v212",
        fromlist=["run_health_check"]))

    # --- GUI import safe ---
    chk("gui_import_safe", lambda: __import__(
        "gui.small_capital_strategy_panel",
        fromlist=["render_all_tabs"]))

    # --- new tabs render clean ---
    from gui.small_capital_strategy_panel import (
        render_market_box_v213_tab,
        render_exposure_control_v213_tab,
        render_defensive_review_queue_v213_tab,
    )
    chk("render_market_box_v213_tab", lambda: render_market_box_v213_tab())
    chk("render_exposure_control_v213_tab", lambda: render_exposure_control_v213_tab())
    chk("render_defensive_review_queue_v213_tab", lambda: render_defensive_review_queue_v213_tab())

    # --- render_all_tabs no error tabs ---
    from gui.small_capital_strategy_panel import render_all_tabs
    chk("render_all_tabs_no_errors", lambda: None if not any(
        "error" in str(v) for v in render_all_tabs().values()
    ) else (_ for _ in ()).throw(AssertionError("render_all_tabs produced error tabs")))

    # --- CLI handler in main.py ---
    chk("cli_handler_main_review_market_box", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_review_market_box"]).cmd_paper_cockpit_v213_review_market_box)
    chk("cli_handler_main_classify_index_zone", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_classify_index_zone"]).cmd_paper_cockpit_v213_classify_index_zone)
    chk("cli_handler_main_build_exposure_control", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_build_exposure_control"]).cmd_paper_cockpit_v213_build_exposure_control)
    chk("cli_handler_main_build_chase_risk_queue", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_build_chase_risk_queue"]).cmd_paper_cockpit_v213_build_chase_risk_queue)
    chk("cli_handler_main_build_defensive_review_queue", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_build_defensive_review_queue"]).cmd_paper_cockpit_v213_build_defensive_review_queue)
    chk("cli_handler_main_export_json", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_export_json"]).cmd_paper_cockpit_v213_export_json)
    chk("cli_handler_main_export_md", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_export_md"]).cmd_paper_cockpit_v213_export_md)
    chk("cli_handler_main_export_csv", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_export_csv"]).cmd_paper_cockpit_v213_export_csv)
    chk("cli_handler_main_health", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_health"]).cmd_paper_cockpit_v213_health)
    chk("cli_handler_main_gate", lambda: __import__(
        "main", fromlist=["cmd_paper_cockpit_v213_gate"]).cmd_paper_cockpit_v213_gate)

    # --- verify_version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v213 import verify_version
    chk("verify_version_213", lambda: None if verify_version() is True else (_ for _ in ()).throw(
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
    print(f"v2.0.13 Health: {status} {result['passed']}/{result['total']}")
    for e in result["errors"]:
        print(f"  {e}")
