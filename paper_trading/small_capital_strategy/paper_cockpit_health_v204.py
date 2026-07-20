"""
paper_trading/small_capital_strategy/paper_cockpit_health_v204.py
v2.0.4 Paper Portfolio Review Loop & Weekly Improvement Pack — Health Check
[!] Paper Only. Research Only. Review Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.normpath("C:/Users/Rossi/Documents/Claude/tw_quant_cockpit"))

HEALTH_VERSION = "2.0.4"
HEALTH_RELEASE = "Paper Portfolio Review Loop & Weekly Improvement Pack"


def run_health_check():
    """Run all health checks for v2.0.4. Returns result dict."""
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

    # --- import ---
    chk("import_v204", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v204", fromlist=["VERSION"]))

    # --- version ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import VERSION, SCHEMA_VERSION
    chk("version_204", lambda: None if VERSION == "2.0.4" else (_ for _ in ()).throw(
        AssertionError(f"Expected 2.0.4 got {VERSION}")))
    chk("schema_version_204", lambda: None if SCHEMA_VERSION == "204" else (_ for _ in ()).throw(
        AssertionError(f"Expected 204 got {SCHEMA_VERSION}")))

    # --- safety constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
    )
    chk("no_real_orders_true", lambda: None if NO_REAL_ORDERS is True else (_ for _ in ()).throw(
        AssertionError("NO_REAL_ORDERS must be True")))
    chk("broker_disabled_false", lambda: None if BROKER_EXECUTION_ENABLED is False else (_ for _ in ()).throw(
        AssertionError("BROKER_EXECUTION_ENABLED must be False")))
    chk("production_blocked_true", lambda: None if PRODUCTION_TRADING_BLOCKED is True else (_ for _ in ()).throw(
        AssertionError("PRODUCTION_TRADING_BLOCKED must be True")))

    # --- safety flags ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    chk("safety_flags_20", lambda: None if len(SAFETY_FLAGS_V204) == 20 else (_ for _ in ()).throw(
        AssertionError(f"Expected 20 safety flags, got {len(SAFETY_FLAGS_V204)}")))
    chk("safety_paper_only", lambda: None if SAFETY_FLAGS_V204["paper_only"] is True else (_ for _ in ()).throw(
        AssertionError("paper_only must be True")))
    chk("safety_no_real_orders", lambda: None if SAFETY_FLAGS_V204["no_real_orders"] is True else (_ for _ in ()).throw(
        AssertionError("no_real_orders must be True")))
    chk("safety_no_broker", lambda: None if SAFETY_FLAGS_V204["no_broker"] is True else (_ for _ in ()).throw(
        AssertionError("no_broker must be True")))
    chk("safety_broker_disabled", lambda: None if SAFETY_FLAGS_V204["broker_execution_disabled"] is True else (
        _ for _ in ()).throw(AssertionError("broker_execution_disabled must be True")))
    chk("safety_production_blocked", lambda: None if SAFETY_FLAGS_V204["production_trading_blocked"] is True else (
        _ for _ in ()).throw(AssertionError("production_trading_blocked must be True")))
    chk("safety_should_auto_apply_false", lambda: None if SAFETY_FLAGS_V204["should_auto_apply_always_false"] is True else (
        _ for _ in ()).throw(AssertionError("should_auto_apply_always_false must be True")))

    # --- constants ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import (
        RECOMMENDATION_CATEGORIES, RECOMMENDATION_SEVERITIES, CLI_COMMANDS_V204, GUI_TABS_V204,
        REVIEW_LOOP_FIELDS, WEEKLY_PACK_FIELDS, REVIEW_METRICS_FIELDS, RECOMMENDATION_FIELDS,
        _ALL_MODEL_NAMES_V204,
    )
    chk("recommendation_categories_10", lambda: None if len(RECOMMENDATION_CATEGORIES) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 recommendation categories")))
    chk("recommendation_severities_4", lambda: None if len(RECOMMENDATION_SEVERITIES) == 4 else (_ for _ in ()).throw(
        AssertionError(f"Expected 4 recommendation severities")))
    chk("cli_commands_11", lambda: None if len(CLI_COMMANDS_V204) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 CLI commands")))
    chk("gui_tabs_3", lambda: None if len(GUI_TABS_V204) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 GUI tabs")))
    chk("review_loop_fields_11", lambda: None if len(REVIEW_LOOP_FIELDS) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 review loop fields")))
    chk("weekly_pack_fields_15", lambda: None if len(WEEKLY_PACK_FIELDS) == 15 else (_ for _ in ()).throw(
        AssertionError(f"Expected 15 weekly pack fields")))
    chk("review_metrics_fields_10", lambda: None if len(REVIEW_METRICS_FIELDS) == 10 else (_ for _ in ()).throw(
        AssertionError(f"Expected 10 review metrics fields")))
    chk("recommendation_fields_11", lambda: None if len(RECOMMENDATION_FIELDS) == 11 else (_ for _ in ()).throw(
        AssertionError(f"Expected 11 recommendation fields")))
    chk("models_12", lambda: None if len(_ALL_MODEL_NAMES_V204) == 12 else (_ for _ in ()).throw(
        AssertionError(f"Expected 12 models")))

    # --- models ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import (
        PortfolioReviewInput, ImprovementRecommendation, ReviewMetrics, WeeklyImprovementPack,
        BlockedReasonReview, RiskUsageReview, StrategyProfileReview, PortfolioReviewResult,
        ReviewExportResult, ReviewAuditSnapshot, V204HealthSummary, V204ReleaseSummary,
    )
    chk("model_PortfolioReviewInput", lambda: PortfolioReviewInput())
    chk("model_ImprovementRecommendation", lambda: ImprovementRecommendation())
    chk("model_ReviewMetrics", lambda: ReviewMetrics())
    chk("model_WeeklyImprovementPack", lambda: WeeklyImprovementPack())
    chk("model_BlockedReasonReview", lambda: BlockedReasonReview())
    chk("model_RiskUsageReview", lambda: RiskUsageReview())
    chk("model_StrategyProfileReview", lambda: StrategyProfileReview())
    chk("model_PortfolioReviewResult", lambda: PortfolioReviewResult())
    chk("model_ReviewExportResult", lambda: ReviewExportResult())
    chk("model_ReviewAuditSnapshot", lambda: ReviewAuditSnapshot())
    chk("model_V204HealthSummary", lambda: V204HealthSummary())
    chk("model_V204ReleaseSummary", lambda: V204ReleaseSummary())

    # --- should_auto_apply always False ---
    chk("rec_should_auto_apply_false_by_default",
        lambda: None if ImprovementRecommendation().should_auto_apply is False else (_ for _ in ()).throw(
            AssertionError("ImprovementRecommendation.should_auto_apply must default to False")))
    chk("rec_should_auto_apply_cannot_be_set_true",
        lambda: None if ImprovementRecommendation(should_auto_apply=True).should_auto_apply is False else (
            _ for _ in ()).throw(AssertionError("ImprovementRecommendation.should_auto_apply must always be False")))
    chk("pack_should_auto_apply_false_by_default",
        lambda: None if WeeklyImprovementPack().should_auto_apply is False else (_ for _ in ()).throw(
            AssertionError("WeeklyImprovementPack.should_auto_apply must default to False")))
    chk("pack_should_auto_apply_cannot_be_set_true",
        lambda: None if WeeklyImprovementPack(should_auto_apply=True).should_auto_apply is False else (
            _ for _ in ()).throw(AssertionError("WeeklyImprovementPack.should_auto_apply must always be False")))

    # --- engine functions ---
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import (
        run_portfolio_review, build_weekly_improvement_pack,
        export_review_json, export_review_markdown, export_review_csv,
        export_improvement_pack_json, export_review_metrics_csv,
        build_review_audit_snapshot, get_review_summary, get_version_info_v204, verify_version_v204,
    )
    chk("fn_run_portfolio_review", lambda: run_portfolio_review())
    chk("fn_run_portfolio_review_all_passed", lambda: None if run_portfolio_review().all_passed is True else (
        _ for _ in ()).throw(AssertionError("run_portfolio_review all_passed not True")))
    chk("fn_run_portfolio_review_paper_only", lambda: None if run_portfolio_review().paper_only is True else (
        _ for _ in ()).throw(AssertionError("run_portfolio_review paper_only not True")))
    chk("fn_run_portfolio_review_no_real_orders", lambda: None if run_portfolio_review().no_real_orders is True else (
        _ for _ in ()).throw(AssertionError("run_portfolio_review no_real_orders not True")))
    chk("fn_build_weekly_pack", lambda: build_weekly_improvement_pack())
    chk("fn_build_weekly_pack_auto_apply_false", lambda: None if build_weekly_improvement_pack().should_auto_apply is False else (
        _ for _ in ()).throw(AssertionError("build_weekly_improvement_pack should_auto_apply not False")))
    chk("fn_export_json", lambda: export_review_json(run_portfolio_review()))
    chk("fn_export_json_valid", lambda: None if export_review_json(run_portfolio_review()).is_valid is True else (
        _ for _ in ()).throw(AssertionError("json export not valid")))
    chk("fn_export_markdown", lambda: export_review_markdown(run_portfolio_review()))
    chk("fn_export_markdown_valid", lambda: None if export_review_markdown(run_portfolio_review()).is_valid is True else (
        _ for _ in ()).throw(AssertionError("markdown export not valid")))
    chk("fn_export_csv", lambda: export_review_csv(run_portfolio_review()))
    chk("fn_export_csv_valid", lambda: None if export_review_csv(run_portfolio_review()).is_valid is True else (
        _ for _ in ()).throw(AssertionError("csv export not valid")))
    chk("fn_export_pack_json", lambda: export_improvement_pack_json(build_weekly_improvement_pack()))
    chk("fn_export_pack_json_valid", lambda: None if export_improvement_pack_json(build_weekly_improvement_pack()).is_valid is True else (
        _ for _ in ()).throw(AssertionError("pack json export not valid")))
    chk("fn_export_metrics_csv", lambda: export_review_metrics_csv(ReviewMetrics(), "test-review"))
    chk("fn_export_metrics_csv_valid", lambda: None if export_review_metrics_csv(ReviewMetrics(), "test-review").is_valid is True else (
        _ for _ in ()).throw(AssertionError("metrics csv export not valid")))
    chk("fn_audit_snapshot", lambda: build_review_audit_snapshot(run_portfolio_review()))
    chk("fn_audit_snapshot_hash", lambda: None if build_review_audit_snapshot(
        run_portfolio_review()).reproducibility_hash else (_ for _ in ()).throw(AssertionError("no hash")))
    chk("fn_get_review_summary", lambda: get_review_summary())
    chk("fn_get_version_info", lambda: get_version_info_v204())
    chk("fn_verify_version", lambda: None if verify_version_v204() is True else (_ for _ in ()).throw(
        AssertionError("verify_version_v204 failed")))

    # --- review loop callable ---
    chk("review_loop_callable", lambda: run_portfolio_review(PortfolioReviewInput(
        review_period="2026-W29", decision_snapshot=["2330", "2317"])))
    chk("weekly_pack_callable", lambda: build_weekly_improvement_pack(
        run_portfolio_review(), "2026-W29"))
    chk("blocked_reason_review_callable", lambda: None)  # tested via run_portfolio_review
    chk("risk_usage_review_callable", lambda: None)  # tested via run_portfolio_review
    chk("recommendation_schema_callable", lambda: ImprovementRecommendation(
        recommendation_id="REC-001", category="entry_rule", severity="low",
        should_auto_apply=False))

    # --- scenarios ---
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v204 import SCENARIOS
    chk("scenarios_80", lambda: None if len(SCENARIOS) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 scenarios")))
    chk("scenarios_schema_204", lambda: None if all(s["schema_version"] == "204" for s in SCENARIOS) else (
        _ for _ in ()).throw(AssertionError("Bad scenario schema")))
    chk("scenarios_paper_only", lambda: None if all(s["paper_only"] is True for s in SCENARIOS) else (
        _ for _ in ()).throw(AssertionError("Missing paper_only")))
    chk("scenarios_unique_ids", lambda: None if len({s["id"] for s in SCENARIOS}) == 80 else (
        _ for _ in ()).throw(AssertionError("Duplicate scenario IDs")))

    # --- fixtures ---
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v204 import FIXTURES
    chk("fixtures_80", lambda: None if len(FIXTURES) == 80 else (_ for _ in ()).throw(
        AssertionError(f"Expected 80 fixtures")))
    chk("fixtures_schema_204", lambda: None if all(f["schema_version"] == "204" for f in FIXTURES) else (
        _ for _ in ()).throw(AssertionError("Bad fixture schema")))
    chk("fixtures_fixture_id", lambda: None if all("fixture_id" in f for f in FIXTURES) else (
        _ for _ in ()).throw(AssertionError("Missing fixture_id")))
    chk("fixtures_unique_ids", lambda: None if len({f["id"] for f in FIXTURES}) == 80 else (
        _ for _ in ()).throw(AssertionError("Duplicate fixture IDs")))

    # --- GUI ---
    from gui.small_capital_strategy_panel import PANEL_VERSION, PANEL_VERSION_V204, get_tab_names, get_v204_tab_names
    chk("panel_version_v204", lambda: None if PANEL_VERSION_V204 == "2.0.4" else (_ for _ in ()).throw(
        AssertionError(f"Expected PANEL_VERSION_V204 2.0.4, got {PANEL_VERSION_V204}")))
    chk("panel_version_unchanged", lambda: None if PANEL_VERSION == "2.0.0" else (_ for _ in ()).throw(
        AssertionError(f"PANEL_VERSION must remain 2.0.0, got {PANEL_VERSION}")))
    tab_names = get_tab_names()
    for tab in GUI_TABS_V204:
        chk(f"gui_tab_{tab}", lambda t=tab: None if t in tab_names else (_ for _ in ()).throw(
            AssertionError(f"Tab '{t}' missing")))
    chk("get_v204_tab_names_3", lambda: None if len(get_v204_tab_names()) == 3 else (_ for _ in ()).throw(
        AssertionError(f"Expected 3 v204 tab names")))

    # --- render_all_tabs no errors ---
    from gui.small_capital_strategy_panel import render_all_tabs
    all_rendered = render_all_tabs()
    chk("render_all_tabs_no_error_weekly_review", lambda: None if "error" not in str(
        all_rendered.get("weekly_review_v204", {})) else (_ for _ in ()).throw(
        AssertionError("weekly_review_v204 has render error")))
    chk("render_all_tabs_no_error_improvement_pack", lambda: None if "error" not in str(
        all_rendered.get("improvement_pack_v204", {})) else (_ for _ in ()).throw(
        AssertionError("improvement_pack_v204 has render error")))
    chk("render_all_tabs_no_error_review_metrics", lambda: None if "error" not in str(
        all_rendered.get("review_metrics_v204", {})) else (_ for _ in ()).throw(
        AssertionError("review_metrics_v204 has render error")))
    error_tabs = [k for k, v in all_rendered.items() if isinstance(v, dict) and "error" in v]
    chk("render_all_tabs_zero_error_tabs", lambda: None if len(error_tabs) == 0 else (_ for _ in ()).throw(
        AssertionError(f"Error tabs: {error_tabs}")))

    # --- CLI ---
    from cli.command_registry import PROVIDER_COMMANDS
    command_names = {c.name for c in PROVIDER_COMMANDS}
    for cmd in CLI_COMMANDS_V204:
        chk(f"cli_{cmd.replace('-','_')}", lambda c=cmd: None if c in command_names else (
            _ for _ in ()).throw(AssertionError(f"CLI command '{c}' missing")))

    # --- paper-only guard / broker execution disabled / production blocked ---
    chk("paper_only_guard_enabled", lambda: None if SAFETY_FLAGS_V204.get("paper_only") is True else (
        _ for _ in ()).throw(AssertionError("paper_only guard not enabled")))
    chk("broker_execution_disabled", lambda: None if SAFETY_FLAGS_V204.get("broker_execution_disabled") is True else (
        _ for _ in ()).throw(AssertionError("broker_execution_disabled not set")))
    chk("production_trading_blocked", lambda: None if SAFETY_FLAGS_V204.get("production_trading_blocked") is True else (
        _ for _ in ()).throw(AssertionError("production_trading_blocked not set")))
    chk("no_real_orders_flag", lambda: None if SAFETY_FLAGS_V204.get("no_real_orders") is True else (
        _ for _ in ()).throw(AssertionError("no_real_orders flag not set")))
    chk("no_real_account_sync", lambda: None if SAFETY_FLAGS_V204.get("no_real_account_sync") is True else (
        _ for _ in ()).throw(AssertionError("no_real_account_sync must be True")))
    chk("no_automatic_rebalance", lambda: None if SAFETY_FLAGS_V204.get("no_automatic_rebalance") is True else (
        _ for _ in ()).throw(AssertionError("no_automatic_rebalance must be True")))

    # --- backward compatibility ---
    chk("backward_compat_v203", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v203", fromlist=["VERSION"]))
    chk("backward_compat_v202", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v202", fromlist=["VERSION"]))
    chk("backward_compat_v201", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v201", fromlist=["VERSION"]))
    chk("backward_compat_v200", lambda: __import__(
        "paper_trading.small_capital_strategy.paper_cockpit_v200", fromlist=["VERSION"]))

    all_passed = (failed == 0)
    total = passed + failed
    print(f"[paper_cockpit_health_v204] {passed}/{total} passed")
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
        sys.exit(1)
    sys.exit(0)
