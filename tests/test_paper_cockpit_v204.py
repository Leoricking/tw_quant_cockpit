"""
tests/test_paper_cockpit_v204.py
v2.0.4 Paper Portfolio Review Loop & Weekly Improvement Pack — Core Module Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# import
# ---------------------------------------------------------------------------

def test_import_v204():
    import paper_trading.small_capital_strategy.paper_cockpit_v204

def test_version_is_204():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import VERSION
    assert VERSION == "2.0.4"

def test_schema_version_204():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "204"

def test_release_name():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RELEASE_NAME
    assert "Review" in RELEASE_NAME or "Improvement" in RELEASE_NAME or "Portfolio" in RELEASE_NAME

# ---------------------------------------------------------------------------
# safety constants
# ---------------------------------------------------------------------------

def test_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True

# ---------------------------------------------------------------------------
# safety flags
# ---------------------------------------------------------------------------

def test_safety_flags_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert len(SAFETY_FLAGS_V204) == 20

def test_safety_flag_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["paper_only"] is True

def test_safety_flag_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["no_real_orders"] is True

def test_safety_flag_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["no_broker"] is True

def test_safety_flag_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["broker_execution_disabled"] is True

def test_safety_flag_production_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["production_trading_blocked"] is True

def test_safety_flag_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["no_real_account_sync"] is True

def test_safety_flag_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["no_automatic_rebalance"] is True

def test_safety_flag_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204["should_auto_apply_always_false"] is True

def test_safety_flags_are_dict():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert isinstance(SAFETY_FLAGS_V204, dict)

def test_all_safety_flags_bool():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    for k, v in SAFETY_FLAGS_V204.items():
        assert isinstance(v, bool), f"Flag {k} is not bool"

def test_safety_flag_no_margin():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204.get("no_margin") is True

def test_safety_flag_no_leverage():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import SAFETY_FLAGS_V204
    assert SAFETY_FLAGS_V204.get("no_leverage") is True

# ---------------------------------------------------------------------------
# recommendation categories
# ---------------------------------------------------------------------------

def test_recommendation_categories_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    assert len(RECOMMENDATION_CATEGORIES) == 10

def test_has_entry_rule_category():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    assert "entry_rule" in RECOMMENDATION_CATEGORIES

def test_has_add_rule_category():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    assert "add_rule" in RECOMMENDATION_CATEGORIES

def test_has_reduce_rule_category():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    assert "reduce_rule" in RECOMMENDATION_CATEGORIES

def test_has_exit_rule_category():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    assert "exit_rule" in RECOMMENDATION_CATEGORIES

def test_has_no_entry_rule_category():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    assert "no_entry_rule" in RECOMMENDATION_CATEGORIES

def test_has_risk_budget_category():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    assert "risk_budget" in RECOMMENDATION_CATEGORIES

def test_has_position_sizing_category():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    assert "position_sizing" in RECOMMENDATION_CATEGORIES

def test_has_human_review_category():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    assert "human_review" in RECOMMENDATION_CATEGORIES

def test_has_reporting_category():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    assert "reporting" in RECOMMENDATION_CATEGORIES

def test_has_simulation_category():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_CATEGORIES
    assert "simulation" in RECOMMENDATION_CATEGORIES

# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def test_cli_commands_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert len(CLI_COMMANDS_V204) == 11

def test_cli_review_weekly_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert "paper-cockpit-v204-review-weekly" in CLI_COMMANDS_V204

def test_cli_review_portfolio_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert "paper-cockpit-v204-review-portfolio" in CLI_COMMANDS_V204

def test_cli_review_strategy_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert "paper-cockpit-v204-review-strategy" in CLI_COMMANDS_V204

def test_cli_review_blocked_reasons_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert "paper-cockpit-v204-review-blocked-reasons" in CLI_COMMANDS_V204

def test_cli_review_risk_usage_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert "paper-cockpit-v204-review-risk-usage" in CLI_COMMANDS_V204

def test_cli_generate_improvement_pack_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert "paper-cockpit-v204-generate-improvement-pack" in CLI_COMMANDS_V204

def test_cli_export_json_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert "paper-cockpit-v204-export-json" in CLI_COMMANDS_V204

def test_cli_export_md_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert "paper-cockpit-v204-export-md" in CLI_COMMANDS_V204

def test_cli_export_csv_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert "paper-cockpit-v204-export-csv" in CLI_COMMANDS_V204

def test_cli_health_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert "paper-cockpit-v204-health" in CLI_COMMANDS_V204

def test_cli_gate_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import CLI_COMMANDS_V204
    assert "paper-cockpit-v204-gate" in CLI_COMMANDS_V204

# ---------------------------------------------------------------------------
# GUI tabs
# ---------------------------------------------------------------------------

def test_gui_tabs_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import GUI_TABS_V204
    assert len(GUI_TABS_V204) == 3

def test_gui_tab_weekly_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import GUI_TABS_V204
    assert "weekly_review_v204" in GUI_TABS_V204

def test_gui_tab_improvement_pack():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import GUI_TABS_V204
    assert "improvement_pack_v204" in GUI_TABS_V204

def test_gui_tab_review_metrics():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import GUI_TABS_V204
    assert "review_metrics_v204" in GUI_TABS_V204

# ---------------------------------------------------------------------------
# field lists
# ---------------------------------------------------------------------------

def test_review_loop_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import REVIEW_LOOP_FIELDS
    assert len(REVIEW_LOOP_FIELDS) == 11

def test_review_loop_has_review_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import REVIEW_LOOP_FIELDS
    assert "review_id" in REVIEW_LOOP_FIELDS

def test_review_loop_has_review_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import REVIEW_LOOP_FIELDS
    assert "review_version" in REVIEW_LOOP_FIELDS

def test_review_loop_has_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import REVIEW_LOOP_FIELDS
    assert "paper_only_safety_snapshot" in REVIEW_LOOP_FIELDS

def test_weekly_pack_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import WEEKLY_PACK_FIELDS
    assert len(WEEKLY_PACK_FIELDS) == 15

def test_weekly_pack_has_week_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import WEEKLY_PACK_FIELDS
    assert "week_id" in WEEKLY_PACK_FIELDS

def test_weekly_pack_has_simulation_vs_decision_gap():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import WEEKLY_PACK_FIELDS
    assert "simulation_vs_decision_gap" in WEEKLY_PACK_FIELDS

def test_weekly_pack_has_do_not_change_rules():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import WEEKLY_PACK_FIELDS
    assert "do_not_change_rules" in WEEKLY_PACK_FIELDS

def test_review_metrics_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import REVIEW_METRICS_FIELDS
    assert len(REVIEW_METRICS_FIELDS) == 10

def test_review_metrics_has_actionability():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import REVIEW_METRICS_FIELDS
    assert "actionability_score" in REVIEW_METRICS_FIELDS

def test_review_metrics_has_final_review_grade():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import REVIEW_METRICS_FIELDS
    assert "final_review_grade" in REVIEW_METRICS_FIELDS

def test_recommendation_fields_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_FIELDS
    assert len(RECOMMENDATION_FIELDS) == 11

def test_recommendation_fields_has_should_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_FIELDS
    assert "should_auto_apply" in RECOMMENDATION_FIELDS

def test_recommendation_fields_has_requires_human_approval():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RECOMMENDATION_FIELDS
    assert "requires_human_approval" in RECOMMENDATION_FIELDS

# ---------------------------------------------------------------------------
# models
# ---------------------------------------------------------------------------

def test_model_portfolio_review_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import PortfolioReviewInput
    m = PortfolioReviewInput()
    assert m.paper_only is True
    assert m.no_real_orders is True
    assert m.schema_version == "204"

def test_model_improvement_recommendation_defaults():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ImprovementRecommendation
    m = ImprovementRecommendation()
    assert m.paper_only is True
    assert m.schema_version == "204"
    assert m.should_auto_apply is False
    assert m.requires_human_approval is True

def test_model_review_metrics():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ReviewMetrics
    m = ReviewMetrics()
    assert m.paper_only is True
    assert m.schema_version == "204"
    assert m.final_review_grade == "C"

def test_model_weekly_improvement_pack():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import WeeklyImprovementPack
    m = WeeklyImprovementPack()
    assert m.paper_only is True
    assert m.schema_version == "204"
    assert m.should_auto_apply is False

def test_model_blocked_reason_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import BlockedReasonReview
    m = BlockedReasonReview()
    assert m.paper_only is True
    assert m.schema_version == "204"

def test_model_risk_usage_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import RiskUsageReview
    m = RiskUsageReview()
    assert m.paper_only is True
    assert m.schema_version == "204"

def test_model_strategy_profile_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import StrategyProfileReview
    m = StrategyProfileReview()
    assert m.paper_only is True
    assert m.schema_version == "204"

def test_model_portfolio_review_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import PortfolioReviewResult
    m = PortfolioReviewResult()
    assert m.paper_only is True
    assert m.no_real_orders is True
    assert m.schema_version == "204"

def test_model_review_export_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ReviewExportResult
    m = ReviewExportResult()
    assert m.paper_only is True
    assert m.schema_version == "204"

def test_model_review_audit_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ReviewAuditSnapshot
    m = ReviewAuditSnapshot()
    assert m.paper_only is True
    assert m.schema_version == "204"

def test_model_v204_health_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import V204HealthSummary
    m = V204HealthSummary()
    assert m.version == "2.0.4"
    assert m.paper_only is True

def test_model_v204_release_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import V204ReleaseSummary
    m = V204ReleaseSummary()
    assert m.version == "2.0.4"
    assert m.paper_only is True

def test_all_model_names_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _ALL_MODEL_NAMES_V204
    assert len(_ALL_MODEL_NAMES_V204) == 12

# ---------------------------------------------------------------------------
# should_auto_apply always False
# ---------------------------------------------------------------------------

def test_recommendation_should_auto_apply_default_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ImprovementRecommendation
    rec = ImprovementRecommendation()
    assert rec.should_auto_apply is False

def test_recommendation_should_auto_apply_cannot_be_set_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ImprovementRecommendation
    rec = ImprovementRecommendation(should_auto_apply=True)
    assert rec.should_auto_apply is False

def test_weekly_pack_should_auto_apply_default_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import WeeklyImprovementPack
    pack = WeeklyImprovementPack()
    assert pack.should_auto_apply is False

def test_weekly_pack_should_auto_apply_cannot_be_set_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import WeeklyImprovementPack
    pack = WeeklyImprovementPack(should_auto_apply=True)
    assert pack.should_auto_apply is False

def test_recommendation_requires_human_approval_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ImprovementRecommendation
    rec = ImprovementRecommendation()
    assert rec.requires_human_approval is True

# ---------------------------------------------------------------------------
# portfolio review engine
# ---------------------------------------------------------------------------

def test_run_portfolio_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result is not None

def test_run_portfolio_review_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.all_passed is True

def test_run_portfolio_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.paper_only is True

def test_run_portfolio_review_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.no_real_orders is True

def test_run_portfolio_review_not_investment_advice():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.not_investment_advice is True

def test_run_portfolio_review_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.human_review_required is True

def test_run_portfolio_review_review_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.review_version == "2.0.4"

def test_run_portfolio_review_has_blocked_reason_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.blocked_reason_summary is not None

def test_run_portfolio_review_has_risk_usage_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.risk_usage_summary is not None

def test_run_portfolio_review_has_strategy_profiles():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert isinstance(result.strategy_profile_summary, list)

def test_run_portfolio_review_has_recommendations():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert isinstance(result.improvement_recommendations, list)

def test_run_portfolio_review_recs_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    for rec in result.improvement_recommendations:
        assert rec.should_auto_apply is False

def test_run_portfolio_review_with_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, PortfolioReviewInput
    inp = PortfolioReviewInput(
        review_period="2026-W29",
        decision_snapshot=["2330", "2317"],
        strategy_profile_ids=["P001"],
    )
    result = run_portfolio_review(inp)
    assert result.all_passed is True
    assert result.review_period == "2026-W29"

def test_run_portfolio_review_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.paper_only_safety_snapshot is True

# ---------------------------------------------------------------------------
# weekly improvement pack
# ---------------------------------------------------------------------------

def test_build_weekly_pack_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack is not None

def test_build_weekly_pack_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack.paper_only is True

def test_build_weekly_pack_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack.no_real_orders is True

def test_build_weekly_pack_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack.should_auto_apply is False

def test_build_weekly_pack_has_week_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack.week_id != ""

def test_build_weekly_pack_has_do_not_change_rules():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert isinstance(pack.do_not_change_rules, list)
    assert len(pack.do_not_change_rules) > 0

def test_build_weekly_pack_has_human_review_required_items():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert isinstance(pack.human_review_required_items, list)
    assert len(pack.human_review_required_items) > 0

def test_build_weekly_pack_recs_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    for rec in pack.suggested_rule_adjustments:
        assert rec.should_auto_apply is False

def test_build_weekly_pack_has_review_metrics():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack.review_metrics is not None

def test_build_weekly_pack_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack.schema_version == "204"

# ---------------------------------------------------------------------------
# review metrics
# ---------------------------------------------------------------------------

def test_compute_review_metrics_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _compute_review_metrics
    metrics = _compute_review_metrics(["2330", "2317"], [])
    assert metrics is not None

def test_compute_review_metrics_grade_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _compute_review_metrics
    metrics = _compute_review_metrics(["2330", "2317"], [])
    assert metrics.final_review_grade in ("A", "B", "C", "D")

def test_compute_review_metrics_scores_bounded():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _compute_review_metrics
    metrics = _compute_review_metrics(["2330", "2317"], ["low_score"])
    assert 0.0 <= metrics.actionability_score <= 100.0
    assert 0.0 <= metrics.discipline_score <= 100.0
    assert 0.0 <= metrics.selectivity_score <= 100.0

def test_compute_review_metrics_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _compute_review_metrics
    metrics = _compute_review_metrics([], [])
    assert metrics.paper_only is True

# ---------------------------------------------------------------------------
# blocked reason review
# ---------------------------------------------------------------------------

def test_blocked_reason_review_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _build_blocked_reason_review
    review = _build_blocked_reason_review("R001", [])
    assert review.total_blocked == 0
    assert review.paper_only is True

def test_blocked_reason_review_with_blocks():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _build_blocked_reason_review
    review = _build_blocked_reason_review("R001", ["low_score", "high_risk", "low_score"])
    assert review.total_blocked == 3
    assert "low_score" in review.blocked_reason_counts
    assert review.blocked_reason_counts["low_score"] == 2

def test_blocked_reason_review_most_common():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _build_blocked_reason_review
    review = _build_blocked_reason_review("R001", ["low_score"] * 5 + ["high_risk"] * 2)
    assert "low_score" in review.most_common_reasons

def test_blocked_reason_review_has_recommendations():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _build_blocked_reason_review
    review = _build_blocked_reason_review("R001", ["low_score"])
    assert isinstance(review.recommendations, list)

# ---------------------------------------------------------------------------
# risk usage review
# ---------------------------------------------------------------------------

def test_risk_usage_review_zero():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _build_risk_usage_review
    review = _build_risk_usage_review("R001", {"total_risk_budget_pct": 20.0, "used_risk_pct": 0.0})
    assert review.used_risk_pct == 0.0
    assert review.available_risk_pct == 20.0

def test_risk_usage_review_high_usage():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _build_risk_usage_review
    review = _build_risk_usage_review("R001", {"total_risk_budget_pct": 20.0, "used_risk_pct": 18.0})
    assert "risk_budget_near_limit" in review.risk_budget_findings

def test_risk_usage_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import _build_risk_usage_review
    review = _build_risk_usage_review("R001", {})
    assert review.paper_only is True

# ---------------------------------------------------------------------------
# export integration
# ---------------------------------------------------------------------------

def test_export_review_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, export_review_json
    result = run_portfolio_review()
    export = export_review_json(result)
    assert export is not None

def test_export_review_json_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, export_review_json
    result = run_portfolio_review()
    export = export_review_json(result)
    assert export.is_valid is True

def test_export_review_json_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, export_review_json
    result = run_portfolio_review()
    export = export_review_json(result)
    assert export.export_format == "json"

def test_export_review_json_no_auto_apply_in_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, export_review_json
    result = run_portfolio_review()
    export = export_review_json(result)
    assert "false" in export.content.lower() or "False" in export.content

def test_export_review_markdown_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, export_review_markdown
    result = run_portfolio_review()
    export = export_review_markdown(result)
    assert export is not None

def test_export_review_markdown_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, export_review_markdown
    result = run_portfolio_review()
    export = export_review_markdown(result)
    assert export.is_valid is True

def test_export_review_markdown_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, export_review_markdown
    result = run_portfolio_review()
    export = export_review_markdown(result)
    assert export.export_format == "markdown"

def test_export_review_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, export_review_csv
    result = run_portfolio_review()
    export = export_review_csv(result)
    assert export is not None

def test_export_review_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, export_review_csv
    result = run_portfolio_review()
    export = export_review_csv(result)
    assert export.is_valid is True

def test_export_improvement_pack_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack, export_improvement_pack_json
    pack = build_weekly_improvement_pack()
    export = export_improvement_pack_json(pack)
    assert export is not None

def test_export_improvement_pack_json_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack, export_improvement_pack_json
    pack = build_weekly_improvement_pack()
    export = export_improvement_pack_json(pack)
    assert export.is_valid is True

def test_export_review_metrics_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ReviewMetrics, export_review_metrics_csv
    metrics = ReviewMetrics()
    export = export_review_metrics_csv(metrics, "test-review")
    assert export is not None

def test_export_review_metrics_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ReviewMetrics, export_review_metrics_csv
    metrics = ReviewMetrics()
    export = export_review_metrics_csv(metrics, "test-review")
    assert export.is_valid is True

def test_export_review_metrics_csv_has_all_fields():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import ReviewMetrics, export_review_metrics_csv
    metrics = ReviewMetrics()
    export = export_review_metrics_csv(metrics, "test-review")
    assert "actionability_score" in export.content
    assert "final_review_grade" in export.content

# ---------------------------------------------------------------------------
# audit snapshot
# ---------------------------------------------------------------------------

def test_build_review_audit_snapshot_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, build_review_audit_snapshot
    result = run_portfolio_review()
    snapshot = build_review_audit_snapshot(result)
    assert snapshot is not None

def test_build_review_audit_snapshot_has_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, build_review_audit_snapshot
    result = run_portfolio_review()
    snapshot = build_review_audit_snapshot(result)
    assert snapshot.reproducibility_hash != ""

def test_build_review_audit_snapshot_has_safety():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, build_review_audit_snapshot
    result = run_portfolio_review()
    snapshot = build_review_audit_snapshot(result)
    assert "NO_REAL_ORDERS=True" in snapshot.safety_snapshot

def test_build_review_audit_snapshot_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review, build_review_audit_snapshot
    result = run_portfolio_review()
    snapshot = build_review_audit_snapshot(result)
    assert snapshot.paper_only is True

# ---------------------------------------------------------------------------
# summary / info / verify
# ---------------------------------------------------------------------------

def test_get_review_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import get_review_summary
    summary = get_review_summary()
    assert summary["version"] == "2.0.4"
    assert summary["paper_only"] is True
    assert summary["should_auto_apply"] is False

def test_get_version_info_v204():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import get_version_info_v204
    info = get_version_info_v204()
    assert info["version"] == "2.0.4"
    assert info["paper_only"] is True
    assert info["should_auto_apply"] is False

def test_verify_version_v204():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import verify_version_v204
    assert verify_version_v204() is True
