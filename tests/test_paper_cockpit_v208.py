"""
tests/test_paper_cockpit_v208.py
v2.0.8 Paper Portfolio Exposure & Theme Concentration Risk Control — Main Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


# =========================================================================
# Import tests
# =========================================================================
def test_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_v208

def test_version_is_208():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import VERSION
    assert VERSION == "2.0.8"

def test_schema_version_is_208():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "208"

def test_release_name_contains_exposure():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import RELEASE_NAME
    assert "Exposure" in RELEASE_NAME

def test_release_name_contains_concentration():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import RELEASE_NAME
    assert "Concentration" in RELEASE_NAME

def test_baseline_tests_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import BASELINE_TESTS
    assert BASELINE_TESTS == 35005

def test_min_new_tests_300():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import MIN_NEW_TESTS
    assert MIN_NEW_TESTS == 300

def test_verify_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import verify_version
    assert verify_version() is True


# =========================================================================
# Safety constants
# =========================================================================
def test_no_real_orders_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True


# =========================================================================
# Safety flags
# =========================================================================
def test_safety_flags_count_21():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert len(SAFETY_FLAGS_V208) == 21

def test_safety_flags_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["paper_only"] is True

def test_safety_flags_research_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["research_only"] is True

def test_safety_flags_exposure_analysis_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["exposure_analysis_only"] is True

def test_safety_flags_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["no_real_orders"] is True

def test_safety_flags_no_broker():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["no_broker"] is True

def test_safety_flags_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["no_automatic_rebalance"] is True

def test_safety_flags_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["no_real_account_sync"] is True

def test_safety_flags_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["should_auto_apply_always_false"] is True

def test_safety_flags_auto_apply_enabled_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["auto_apply_enabled_always_false"] is True

def test_safety_flags_broker_execution_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["broker_execution_disabled"] is True

def test_safety_flags_production_trading_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["production_trading_blocked"] is True

def test_safety_flags_exposure_actions_recommendation_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["exposure_actions_recommendation_only"] is True

def test_safety_flags_no_live_strategy_activation():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["no_live_strategy_activation"] is True


# =========================================================================
# Exposure types
# =========================================================================
def test_exposure_types_count_9():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_TYPES
    assert len(EXPOSURE_TYPES) == 9

def test_exposure_type_theme():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_TYPES
    assert "theme" in EXPOSURE_TYPES

def test_exposure_type_sector():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_TYPES
    assert "sector" in EXPOSURE_TYPES

def test_exposure_type_style():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_TYPES
    assert "style" in EXPOSURE_TYPES

def test_exposure_type_volatility():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_TYPES
    assert "volatility" in EXPOSURE_TYPES

def test_exposure_type_liquidity():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_TYPES
    assert "liquidity" in EXPOSURE_TYPES

def test_exposure_type_market_regime():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_TYPES
    assert "market_regime" in EXPOSURE_TYPES

def test_exposure_type_candidate_pool():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_TYPES
    assert "candidate_pool" in EXPOSURE_TYPES

def test_exposure_type_promotion_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_TYPES
    assert "promotion_queue" in EXPOSURE_TYPES

def test_exposure_type_watchlist():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_TYPES
    assert "watchlist" in EXPOSURE_TYPES


# =========================================================================
# Warning levels
# =========================================================================
def test_warning_levels_count_5():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import WARNING_LEVELS
    assert len(WARNING_LEVELS) == 5

def test_warning_level_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import WARNING_LEVELS
    assert "none" in WARNING_LEVELS

def test_warning_level_low():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import WARNING_LEVELS
    assert "low" in WARNING_LEVELS

def test_warning_level_medium():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import WARNING_LEVELS
    assert "medium" in WARNING_LEVELS

def test_warning_level_high():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import WARNING_LEVELS
    assert "high" in WARNING_LEVELS

def test_warning_level_critical():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import WARNING_LEVELS
    assert "critical" in WARNING_LEVELS


# =========================================================================
# Exposure actions
# =========================================================================
def test_exposure_actions_count_7():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_ACTIONS
    assert len(EXPOSURE_ACTIONS) == 7

def test_exposure_action_allow():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_ACTIONS
    assert "allow" in EXPOSURE_ACTIONS

def test_exposure_action_monitor():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_ACTIONS
    assert "monitor" in EXPOSURE_ACTIONS

def test_exposure_action_reduce_priority():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_ACTIONS
    assert "reduce_priority" in EXPOSURE_ACTIONS

def test_exposure_action_freeze_new_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_ACTIONS
    assert "freeze_new_candidates" in EXPOSURE_ACTIONS

def test_exposure_action_require_rescore():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_ACTIONS
    assert "require_rescore" in EXPOSURE_ACTIONS

def test_exposure_action_block_promotion():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_ACTIONS
    assert "block_promotion" in EXPOSURE_ACTIONS

def test_exposure_action_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import EXPOSURE_ACTIONS
    assert "human_review_required" in EXPOSURE_ACTIONS


# =========================================================================
# CLI commands
# =========================================================================
def test_cli_commands_count_10():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    assert len(CLI_COMMANDS_V208) == 10

def test_cli_cmd_review_exposure():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    assert "paper-cockpit-v208-review-exposure" in CLI_COMMANDS_V208

def test_cli_cmd_evaluate_concentration():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    assert "paper-cockpit-v208-evaluate-concentration" in CLI_COMMANDS_V208

def test_cli_cmd_build_warning_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    assert "paper-cockpit-v208-build-warning-queue" in CLI_COMMANDS_V208

def test_cli_cmd_build_risk_cap_queue():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    assert "paper-cockpit-v208-build-risk-cap-queue" in CLI_COMMANDS_V208

def test_cli_cmd_adjust_candidate_exposure():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    assert "paper-cockpit-v208-adjust-candidate-exposure" in CLI_COMMANDS_V208

def test_cli_cmd_export_json():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    assert "paper-cockpit-v208-export-json" in CLI_COMMANDS_V208

def test_cli_cmd_export_md():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    assert "paper-cockpit-v208-export-md" in CLI_COMMANDS_V208

def test_cli_cmd_export_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    assert "paper-cockpit-v208-export-csv" in CLI_COMMANDS_V208

def test_cli_cmd_health():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    assert "paper-cockpit-v208-health" in CLI_COMMANDS_V208

def test_cli_cmd_gate():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CLI_COMMANDS_V208
    assert "paper-cockpit-v208-gate" in CLI_COMMANDS_V208


# =========================================================================
# GUI tabs
# =========================================================================
def test_gui_tabs_count_3():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import GUI_TABS_V208
    assert len(GUI_TABS_V208) == 3

def test_gui_tab_portfolio_exposure_v208():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import GUI_TABS_V208
    assert "portfolio_exposure_v208" in GUI_TABS_V208

def test_gui_tab_theme_concentration_v208():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import GUI_TABS_V208
    assert "theme_concentration_v208" in GUI_TABS_V208

def test_gui_tab_exposure_warning_queue_v208():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import GUI_TABS_V208
    assert "exposure_warning_queue_v208" in GUI_TABS_V208


# =========================================================================
# Models
# =========================================================================
def test_model_exposure_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureItem
    item = ExposureItem()
    assert item.schema_version == "208"
    assert item.paper_only is True
    assert item.no_real_orders is True

def test_model_exposure_item_defaults():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureItem
    item = ExposureItem()
    assert item.exposure_type == "theme"
    assert item.warning_level == "none"
    assert item.exposure_action == "allow"
    assert item.over_limit is False

def test_model_portfolio_risk_cap_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import PortfolioRiskCapPolicy
    policy = PortfolioRiskCapPolicy()
    assert policy.schema_version == "208"
    assert policy.paper_only is True
    assert policy.auto_apply_enabled is False

def test_model_risk_cap_policy_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import PortfolioRiskCapPolicy
    policy = PortfolioRiskCapPolicy(auto_apply_enabled=True)
    assert policy.auto_apply_enabled is False

def test_model_candidate_exposure_adjustment():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CandidateExposureAdjustment
    adj = CandidateExposureAdjustment()
    assert adj.schema_version == "208"
    assert adj.paper_only is True
    assert adj.should_auto_apply is False

def test_model_candidate_exposure_adjustment_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CandidateExposureAdjustment
    adj = CandidateExposureAdjustment(should_auto_apply=True)
    assert adj.should_auto_apply is False

def test_model_exposure_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureSummary
    summary = ExposureSummary()
    assert summary.schema_version == "208"
    assert summary.paper_only is True

def test_model_exposure_review_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureReviewInput
    inp = ExposureReviewInput()
    assert inp.schema_version == "208"
    assert inp.paper_only is True

def test_model_exposure_review_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureReviewResult
    result = ExposureReviewResult()
    assert result.schema_version == "208"
    assert result.paper_only is True
    assert result.should_auto_apply is False
    assert result.auto_apply_enabled is False

def test_model_exposure_review_result_should_auto_apply_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureReviewResult
    result = ExposureReviewResult(should_auto_apply=True)
    assert result.should_auto_apply is False

def test_model_exposure_review_result_auto_apply_enabled_always_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureReviewResult
    result = ExposureReviewResult(auto_apply_enabled=True)
    assert result.auto_apply_enabled is False

def test_model_exposure_export_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureExportResult
    r = ExposureExportResult()
    assert r.schema_version == "208"
    assert r.paper_only is True
    assert r.should_auto_apply is False
    assert r.auto_apply_enabled is False

def test_model_exposure_audit_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureAuditSnapshot
    snap = ExposureAuditSnapshot()
    assert snap.schema_version == "208"
    assert snap.paper_only is True

def test_model_exposure_report():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureReport
    r = ExposureReport()
    assert r.schema_version == "208"
    assert r.paper_only is True

def test_model_exposure_item_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import ExposureItemCSV
    c = ExposureItemCSV()
    assert c.schema_version == "208"
    assert c.paper_only is True

def test_model_risk_cap_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import RiskCapCSV
    c = RiskCapCSV()
    assert c.schema_version == "208"
    assert c.paper_only is True

def test_model_candidate_exposure_csv():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import CandidateExposureCSV
    c = CandidateExposureCSV()
    assert c.schema_version == "208"
    assert c.paper_only is True

def test_model_v208_health_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import V208HealthSummary
    s = V208HealthSummary()
    assert s.schema_version == "208"
    assert s.version == "2.0.8"

def test_model_v208_release_summary():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import V208ReleaseSummary
    s = V208ReleaseSummary()
    assert s.schema_version == "208"
    assert s.version == "2.0.8"
    assert s.models_count == 14

def test_model_count_14():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import _ALL_MODEL_NAMES_V208
    assert len(_ALL_MODEL_NAMES_V208) == 14


# =========================================================================
# Warning level classification
# =========================================================================
def test_classify_warning_level_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_warning_level
    assert classify_warning_level(20.0, 0.40, 0.20) == "none"

def test_classify_warning_level_low():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_warning_level
    assert classify_warning_level(47.0, 0.40, 0.28) == "low"

def test_classify_warning_level_medium():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_warning_level
    assert classify_warning_level(62.0, 0.40, 0.36) == "medium"

def test_classify_warning_level_high_by_ratio():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_warning_level
    # 0.45 / 0.40 = 1.125 >= 1.10，避免浮點邊界問題
    result = classify_warning_level(50.0, 0.40, 0.45)
    assert result in ("high", "critical")

def test_classify_warning_level_critical_by_concentration():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_warning_level
    assert classify_warning_level(92.0, 0.40, 0.55) == "critical"

def test_classify_warning_level_critical_by_ratio():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_warning_level
    assert classify_warning_level(50.0, 0.40, 0.55) == "critical"


# =========================================================================
# Exposure action classification
# =========================================================================
def test_classify_exposure_action_none_allow():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_exposure_action
    assert classify_exposure_action("none", "theme", False) == "allow"

def test_classify_exposure_action_low_monitor():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_exposure_action
    assert classify_exposure_action("low", "theme", False) == "monitor"

def test_classify_exposure_action_medium_theme_reduce():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_exposure_action
    assert classify_exposure_action("medium", "theme", True) == "reduce_priority"

def test_classify_exposure_action_medium_sector_reduce():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_exposure_action
    assert classify_exposure_action("medium", "sector", True) == "reduce_priority"

def test_classify_exposure_action_medium_volatility_freeze():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_exposure_action
    assert classify_exposure_action("medium", "volatility", True) == "freeze_new_candidates"

def test_classify_exposure_action_high_human_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_exposure_action
    assert classify_exposure_action("high", "theme", True) == "human_review_required"

def test_classify_exposure_action_critical_human_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import classify_exposure_action
    assert classify_exposure_action("critical", "theme", True) == "human_review_required"


# =========================================================================
# Concentration score
# =========================================================================
def test_compute_concentration_score_zero():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import compute_concentration_score
    assert compute_concentration_score(0, 10) == 0.0

def test_compute_concentration_score_50():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import compute_concentration_score
    assert compute_concentration_score(5, 10) == 50.0

def test_compute_concentration_score_100():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import compute_concentration_score
    assert compute_concentration_score(10, 10) == 100.0

def test_compute_concentration_score_capped():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import compute_concentration_score
    assert compute_concentration_score(20, 10) == 100.0

def test_compute_concentration_score_zero_total():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import compute_concentration_score
    assert compute_concentration_score(5, 0) == 0.0


# =========================================================================
# Risk score
# =========================================================================
def test_compute_risk_score_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import compute_risk_score
    assert compute_risk_score(50.0, "none", "theme") == 0.0

def test_compute_risk_score_critical_high():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import compute_risk_score
    score = compute_risk_score(90.0, "critical", "theme")
    assert score > 0.0
    assert score <= 100.0

def test_compute_risk_score_capped_100():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import compute_risk_score
    score = compute_risk_score(100.0, "critical", "theme")
    assert score <= 100.0


# =========================================================================
# Theme concentration scoring
# =========================================================================
def test_score_theme_concentration_returns_exposure_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_theme_concentration, ExposureItem
    item = score_theme_concentration("THEME-AI", "人工智慧", 4, 8, 0, 8, 0, 8)
    assert isinstance(item, ExposureItem)

def test_score_theme_concentration_type():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_theme_concentration
    item = score_theme_concentration("THEME-AI", "人工智慧", 4, 8, 0, 8, 0, 8)
    assert item.exposure_type == "theme"

def test_score_theme_concentration_over_limit_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_theme_concentration
    item = score_theme_concentration("THEME-AI", "人工智慧", 5, 8, 0, 8, 0, 8, cap_limit=0.40)
    assert item.over_limit is True

def test_score_theme_concentration_over_limit_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_theme_concentration
    item = score_theme_concentration("THEME-EV", "電動車", 2, 10, 0, 10, 0, 10, cap_limit=0.40)
    assert item.over_limit is False

def test_score_theme_concentration_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_theme_concentration
    item = score_theme_concentration("THEME-AI", "人工智慧", 4, 8, 0, 8, 0, 8)
    assert item.paper_only is True

def test_score_theme_concentration_concentration_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_theme_concentration
    item = score_theme_concentration("THEME-AI", "人工智慧", 4, 8, 0, 8, 0, 8)
    assert item.concentration_score == 50.0

def test_score_theme_concentration_critical_warning():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_theme_concentration
    item = score_theme_concentration("THEME-CLOUD", "雲端運算", 8, 10, 0, 10, 0, 10, cap_limit=0.40)
    assert item.warning_level in ("high", "critical")
    assert item.over_limit is True


# =========================================================================
# Sector concentration scoring
# =========================================================================
def test_score_sector_concentration_returns_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_sector_concentration, ExposureItem
    item = score_sector_concentration("SECTOR-TECH", "科技業", 6, 8)
    assert isinstance(item, ExposureItem)

def test_score_sector_concentration_type():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_sector_concentration
    item = score_sector_concentration("SECTOR-TECH", "科技業", 6, 8)
    assert item.exposure_type == "sector"

def test_score_sector_concentration_over_limit():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_sector_concentration
    item = score_sector_concentration("SECTOR-TECH", "科技業", 6, 8, cap_limit=0.45)
    assert item.over_limit is True

def test_score_sector_concentration_no_warning():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_sector_concentration
    item = score_sector_concentration("SECTOR-FIN", "金融業", 2, 10, cap_limit=0.45)
    assert item.warning_level == "none"


# =========================================================================
# Style concentration scoring
# =========================================================================
def test_score_style_concentration_returns_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_style_concentration, ExposureItem
    item = score_style_concentration("STYLE-GROWTH", "成長型", 7, 10)
    assert isinstance(item, ExposureItem)

def test_score_style_concentration_type():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_style_concentration
    item = score_style_concentration("STYLE-GROWTH", "成長型", 7, 10)
    assert item.exposure_type == "style"

def test_score_style_concentration_over_limit():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_style_concentration
    item = score_style_concentration("STYLE-GROWTH", "成長型", 7, 10, cap_limit=0.50)
    assert item.over_limit is True

def test_score_style_concentration_none_warning():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_style_concentration
    item = score_style_concentration("STYLE-VALUE", "價值型", 2, 10, cap_limit=0.50)
    assert item.warning_level == "none"


# =========================================================================
# Volatility exposure scoring
# =========================================================================
def test_score_volatility_exposure_returns_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_volatility_exposure, ExposureItem
    item = score_volatility_exposure(2, 10)
    assert isinstance(item, ExposureItem)

def test_score_volatility_exposure_type():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_volatility_exposure
    item = score_volatility_exposure(2, 10)
    assert item.exposure_type == "volatility"

def test_score_volatility_exposure_safe():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_volatility_exposure
    item = score_volatility_exposure(2, 10, cap_limit=0.30)
    assert item.over_limit is False

def test_score_volatility_exposure_over_limit():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_volatility_exposure
    item = score_volatility_exposure(5, 10, cap_limit=0.30)
    assert item.over_limit is True

def test_score_volatility_exposure_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_volatility_exposure
    item = score_volatility_exposure(2, 10)
    assert item.paper_only is True


# =========================================================================
# Liquidity exposure scoring
# =========================================================================
def test_score_liquidity_exposure_returns_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_liquidity_exposure, ExposureItem
    item = score_liquidity_exposure(1, 10)
    assert isinstance(item, ExposureItem)

def test_score_liquidity_exposure_type():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_liquidity_exposure
    item = score_liquidity_exposure(1, 10)
    assert item.exposure_type == "liquidity"

def test_score_liquidity_exposure_safe():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_liquidity_exposure
    item = score_liquidity_exposure(1, 10, cap_limit=0.20)
    assert item.over_limit is False

def test_score_liquidity_exposure_over_limit():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_liquidity_exposure
    item = score_liquidity_exposure(3, 10, cap_limit=0.20)
    assert item.over_limit is True


# =========================================================================
# Market regime exposure scoring
# =========================================================================
def test_score_market_regime_exposure_returns_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_market_regime_exposure, ExposureItem
    item = score_market_regime_exposure(0, 10)
    assert isinstance(item, ExposureItem)

def test_score_market_regime_exposure_type():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_market_regime_exposure
    item = score_market_regime_exposure(0, 10)
    assert item.exposure_type == "market_regime"

def test_score_market_regime_exposure_safe():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_market_regime_exposure
    item = score_market_regime_exposure(0, 10, cap_limit=0.10)
    assert item.over_limit is False

def test_score_market_regime_exposure_over_limit():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_market_regime_exposure
    item = score_market_regime_exposure(2, 10, cap_limit=0.10)
    assert item.over_limit is True


# =========================================================================
# Candidate pool exposure scoring
# =========================================================================
def test_score_candidate_pool_exposure_returns_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_candidate_pool_exposure, ExposureItem
    item = score_candidate_pool_exposure(3, 10)
    assert isinstance(item, ExposureItem)

def test_score_candidate_pool_exposure_type():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_candidate_pool_exposure
    item = score_candidate_pool_exposure(3, 10)
    assert item.exposure_type == "candidate_pool"

def test_score_candidate_pool_exposure_over_limit():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_candidate_pool_exposure
    item = score_candidate_pool_exposure(5, 10, cap_limit=0.40)
    assert item.over_limit is True


# =========================================================================
# Promotion queue exposure scoring
# =========================================================================
def test_score_promotion_queue_exposure_returns_item():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_promotion_queue_exposure, ExposureItem
    item = score_promotion_queue_exposure(3, 10)
    assert isinstance(item, ExposureItem)

def test_score_promotion_queue_exposure_type():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_promotion_queue_exposure
    item = score_promotion_queue_exposure(3, 10)
    assert item.exposure_type == "promotion_queue"

def test_score_promotion_queue_exposure_over_limit():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_promotion_queue_exposure
    item = score_promotion_queue_exposure(4, 10, cap_limit=0.35)
    assert item.over_limit is True

def test_score_promotion_queue_exposure_safe():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import score_promotion_queue_exposure
    item = score_promotion_queue_exposure(3, 10, cap_limit=0.35)
    assert item.over_limit is False


# =========================================================================
# Candidate exposure adjustment
# =========================================================================
def test_adjust_candidate_exposure_returns_adj():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure, CandidateExposureAdjustment
    adj = adjust_candidate_exposure("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0)
    assert isinstance(adj, CandidateExposureAdjustment)

def test_adjust_candidate_exposure_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0)
    assert adj.should_auto_apply is False

def test_adjust_candidate_exposure_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2330", "台積電", "CAND-001", "THEME-SEMI", "SECTOR-TECH", 80.0)
    assert adj.paper_only is True

def test_adjust_candidate_exposure_theme_concentration_penalty_high():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2454", "聯發科", "CAND-2454", "THEME-AI", "SECTOR-TECH", 75.0,
                                    theme_concentration_score=92.0)
    assert adj.theme_concentration_penalty == 15.0

def test_adjust_candidate_exposure_theme_concentration_penalty_medium():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2330", "台積電", "CAND-2330", "THEME-SEMI", "SECTOR-TECH", 80.0,
                                    theme_concentration_score=75.0)
    assert adj.theme_concentration_penalty == 10.0

def test_adjust_candidate_exposure_theme_concentration_penalty_low():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2317", "鴻海", "CAND-2317", "THEME-EV", "SECTOR-MFGR", 58.0,
                                    theme_concentration_score=15.0)
    assert adj.theme_concentration_penalty == 0.0

def test_adjust_candidate_exposure_sector_concentration_penalty():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("3711", "日月光", "CAND-3711", "THEME-SEMI", "SECTOR-TECH", 72.0,
                                    sector_concentration_score=90.0)
    assert adj.sector_concentration_penalty == 12.0

def test_adjust_candidate_exposure_volatility_penalty():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2308", "台達電", "CAND-2308", "THEME-EV", "SECTOR-ELEC", 62.0,
                                    is_high_volatility=True)
    assert adj.volatility_penalty == 8.0

def test_adjust_candidate_exposure_liquidity_penalty():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2303", "聯電", "CAND-2303", "THEME-SEMI", "SECTOR-TECH", 65.0,
                                    is_low_liquidity=True)
    assert adj.liquidity_penalty == 10.0

def test_adjust_candidate_exposure_market_regime_penalty_downtrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2409", "友達", "CAND-2409", "THEME-SEMI", "SECTOR-TECH", 55.0,
                                    market_state="downtrend")
    assert adj.market_regime_penalty == 15.0

def test_adjust_candidate_exposure_market_regime_penalty_risk_off():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("6669", "緯穎", "CAND-6669", "THEME-AI", "SECTOR-TECH", 70.0,
                                    market_state="risk_off")
    assert adj.market_regime_penalty == 20.0

def test_adjust_candidate_exposure_market_regime_penalty_strong_uptrend():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2330", "台積電", "CAND-2330", "THEME-SEMI", "SECTOR-TECH", 80.0,
                                    market_state="strong_uptrend")
    assert adj.market_regime_penalty == 0.0

def test_adjust_candidate_exposure_blocked_requires_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2382", "廣達", "CAND-2382", "THEME-AI", "SECTOR-TECH", 70.0,
                                    blocked_by_exposure_cap=True)
    assert adj.blocked_by_exposure_cap is True
    assert adj.requires_human_review is True

def test_adjust_candidate_exposure_risk_off_requires_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2409", "友達", "CAND-2409", "THEME-FIN", "SECTOR-FIN", 55.0,
                                    market_state="risk_off")
    assert adj.requires_human_review is True

def test_adjust_candidate_exposure_final_score_reduced():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2454", "聯發科", "CAND-2454", "THEME-AI", "SECTOR-TECH", 75.0,
                                    theme_concentration_score=92.0, market_state="downtrend")
    assert adj.final_exposure_adjusted_score < 75.0

def test_adjust_candidate_exposure_final_score_not_negative():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2454", "聯發科", "CAND-2454", "THEME-AI", "SECTOR-TECH", 10.0,
                                    theme_concentration_score=100.0, sector_concentration_score=100.0,
                                    market_state="risk_off", is_high_volatility=True, is_low_liquidity=True)
    assert adj.final_exposure_adjusted_score >= 0.0

def test_adjust_candidate_exposure_reason_codes_populated():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import adjust_candidate_exposure
    adj = adjust_candidate_exposure("2330", "台積電", "CAND-2330", "THEME-SEMI", "SECTOR-TECH", 80.0,
                                    theme_concentration_score=92.0)
    assert len(adj.exposure_reason_codes) > 0


# =========================================================================
# Portfolio exposure engine
# =========================================================================
def test_run_exposure_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert result is not None

def test_run_exposure_review_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    assert run_exposure_review().paper_only is True

def test_run_exposure_review_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    assert run_exposure_review().all_passed is True

def test_run_exposure_review_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    assert run_exposure_review().should_auto_apply is False

def test_run_exposure_review_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    assert run_exposure_review().auto_apply_enabled is False

def test_run_exposure_review_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    assert run_exposure_review().exposure_version == "2.0.8"

def test_run_exposure_review_has_review_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert len(result.exposure_review_id) == 10

def test_run_exposure_review_has_theme_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert len(result.theme_concentration_snapshot) > 0

def test_run_exposure_review_has_sector_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert len(result.sector_concentration_snapshot) > 0

def test_run_exposure_review_has_volatility_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert len(result.volatility_exposure_snapshot) > 0

def test_run_exposure_review_has_market_regime_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert len(result.market_regime_exposure_snapshot) > 0

def test_run_exposure_review_has_candidate_pool_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert len(result.candidate_pool_exposure_snapshot) > 0

def test_run_exposure_review_has_promotion_queue_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert len(result.promotion_queue_exposure_snapshot) > 0

def test_run_exposure_review_has_candidate_adjustments():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert len(result.candidate_exposure_adjustments) > 0

def test_run_exposure_review_exposure_summary_not_none():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert result.exposure_summary is not None

def test_run_exposure_review_paper_only_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert result.paper_only_safety_snapshot is True

def test_run_exposure_review_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert result.no_real_orders is True

def test_run_exposure_review_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert result.human_review_required is True

def test_run_exposure_review_candidate_adj_all_no_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert all(adj.should_auto_apply is False for adj in result.candidate_exposure_adjustments)


# =========================================================================
# evaluate_concentration
# =========================================================================
def test_evaluate_concentration_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import evaluate_concentration
    items = evaluate_concentration()
    assert isinstance(items, list)

def test_evaluate_concentration_returns_items():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import evaluate_concentration
    items = evaluate_concentration()
    assert len(items) > 0

def test_evaluate_concentration_all_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import evaluate_concentration
    items = evaluate_concentration()
    assert all(i.paper_only is True for i in items)

def test_evaluate_concentration_types_covered():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import evaluate_concentration
    items = evaluate_concentration()
    types = {i.exposure_type for i in items}
    assert "theme" in types
    assert "sector" in types


# =========================================================================
# build_warning_queue
# =========================================================================
def test_build_warning_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import build_warning_queue
    queue = build_warning_queue()
    assert isinstance(queue, list)

def test_build_warning_queue_all_medium_or_above():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import build_warning_queue
    queue = build_warning_queue()
    for item in queue:
        assert item.warning_level in ("medium", "high", "critical")

def test_build_warning_queue_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import build_warning_queue
    queue = build_warning_queue()
    assert all(i.paper_only is True for i in queue)


# =========================================================================
# build_risk_cap_queue
# =========================================================================
def test_build_risk_cap_queue_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import build_risk_cap_queue
    queue = build_risk_cap_queue()
    assert isinstance(queue, list)

def test_build_risk_cap_queue_all_over_limit():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import build_risk_cap_queue
    queue = build_risk_cap_queue()
    assert all(i.over_limit is True for i in queue)

def test_build_risk_cap_queue_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import build_risk_cap_queue
    queue = build_risk_cap_queue()
    assert all(i.paper_only is True for i in queue)


# =========================================================================
# Exposure summary
# =========================================================================
def test_exposure_summary_total_groups():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    summary = result.exposure_summary
    assert summary.total_exposure_groups >= 0

def test_exposure_summary_grade_is_letter():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    summary = result.exposure_summary
    assert summary.exposure_quality_grade in ("A", "B", "C", "D")
    assert summary.diversification_grade in ("A", "B", "C", "D")
    assert summary.risk_cap_quality_grade in ("A", "B", "C", "D")

def test_exposure_summary_top_themes_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    summary = result.exposure_summary
    assert isinstance(summary.top_concentrated_themes, list)

def test_exposure_summary_top_sectors_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    summary = result.exposure_summary
    assert isinstance(summary.top_concentrated_sectors, list)

def test_exposure_summary_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert result.exposure_summary.paper_only is True


# =========================================================================
# Export JSON
# =========================================================================
def test_export_exposure_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_json
    result = export_exposure_json(run_exposure_review())
    assert result is not None

def test_export_exposure_json_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_json
    result = export_exposure_json(run_exposure_review())
    assert result.is_valid is True

def test_export_exposure_json_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_json
    result = export_exposure_json(run_exposure_review())
    assert result.export_format == "json"

def test_export_exposure_json_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_json
    result = export_exposure_json(run_exposure_review())
    assert result.export_status == "complete"

def test_export_exposure_json_contains_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_json
    result = export_exposure_json(run_exposure_review())
    assert "paper_only" in result.content

def test_export_exposure_json_contains_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_json
    result = export_exposure_json(run_exposure_review())
    assert "should_auto_apply" in result.content

def test_export_exposure_json_contains_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_json
    result = export_exposure_json(run_exposure_review())
    assert "auto_apply_enabled" in result.content

def test_export_exposure_json_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_json
    result = export_exposure_json(run_exposure_review())
    assert result.paper_only is True


# =========================================================================
# Export Markdown
# =========================================================================
def test_export_exposure_markdown_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_markdown
    result = export_exposure_markdown(run_exposure_review())
    assert result is not None

def test_export_exposure_markdown_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_markdown
    result = export_exposure_markdown(run_exposure_review())
    assert result.is_valid is True

def test_export_exposure_markdown_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_markdown
    result = export_exposure_markdown(run_exposure_review())
    assert result.export_format == "markdown"

def test_export_exposure_markdown_contains_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_markdown
    result = export_exposure_markdown(run_exposure_review())
    assert "[!] Paper Only" in result.content

def test_export_exposure_markdown_contains_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_markdown
    result = export_exposure_markdown(run_exposure_review())
    assert "2.0.8" in result.content


# =========================================================================
# Export CSV (exposure item)
# =========================================================================
def test_export_exposure_item_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_item_csv
    result = export_exposure_item_csv(run_exposure_review())
    assert result is not None

def test_export_exposure_item_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_item_csv
    result = export_exposure_item_csv(run_exposure_review())
    assert result.is_valid is True

def test_export_exposure_item_csv_header_has_should_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_item_csv
    result = export_exposure_item_csv(run_exposure_review())
    assert "should_auto_apply" in result.csv_content

def test_export_exposure_item_csv_row_count_positive():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_item_csv
    result = export_exposure_item_csv(run_exposure_review())
    assert result.row_count > 0


# =========================================================================
# Export risk cap CSV
# =========================================================================
def test_export_risk_cap_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_risk_cap_csv
    result = export_risk_cap_csv(run_exposure_review())
    assert result is not None

def test_export_risk_cap_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_risk_cap_csv
    result = export_risk_cap_csv(run_exposure_review())
    assert result.is_valid is True

def test_export_risk_cap_csv_header_has_auto_apply_enabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_risk_cap_csv
    result = export_risk_cap_csv(run_exposure_review())
    assert "auto_apply_enabled" in result.csv_content


# =========================================================================
# Export candidate exposure CSV
# =========================================================================
def test_export_candidate_exposure_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_candidate_exposure_csv
    result = export_candidate_exposure_csv(run_exposure_review())
    assert result is not None

def test_export_candidate_exposure_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_candidate_exposure_csv
    result = export_candidate_exposure_csv(run_exposure_review())
    assert result.is_valid is True

def test_export_candidate_exposure_csv_header_has_should_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_candidate_exposure_csv
    result = export_candidate_exposure_csv(run_exposure_review())
    assert "should_auto_apply" in result.csv_content

def test_export_candidate_exposure_csv_row_count_positive():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_candidate_exposure_csv
    result = export_candidate_exposure_csv(run_exposure_review())
    assert result.row_count > 0


# =========================================================================
# Export audit snapshot
# =========================================================================
def test_export_exposure_audit_snapshot_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_audit_snapshot
    snap = export_exposure_audit_snapshot(run_exposure_review())
    assert snap is not None

def test_export_exposure_audit_snapshot_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_audit_snapshot
    snap = export_exposure_audit_snapshot(run_exposure_review())
    assert snap.export_status == "complete"

def test_export_exposure_audit_snapshot_has_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_audit_snapshot
    snap = export_exposure_audit_snapshot(run_exposure_review())
    assert len(snap.reproducibility_hash) > 0

def test_export_exposure_audit_snapshot_safety_snapshot():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review, export_exposure_audit_snapshot
    snap = export_exposure_audit_snapshot(run_exposure_review())
    assert "paper_only=True" in snap.safety_snapshot
    assert "should_auto_apply=False" in snap.safety_snapshot
    assert "auto_apply_enabled=False" in snap.safety_snapshot


# =========================================================================
# CLI registry
# =========================================================================
def test_cli_registry_importable():
    from cli.command_registry import PROVIDER_COMMANDS
    assert PROVIDER_COMMANDS is not None

def test_cli_registry_has_review_exposure():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v208-review-exposure" in cmd_names

def test_cli_registry_has_evaluate_concentration():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v208-evaluate-concentration" in cmd_names

def test_cli_registry_has_build_warning_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v208-build-warning-queue" in cmd_names

def test_cli_registry_has_build_risk_cap_queue():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v208-build-risk-cap-queue" in cmd_names

def test_cli_registry_has_adjust_candidate_exposure():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v208-adjust-candidate-exposure" in cmd_names

def test_cli_registry_has_export_json():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v208-export-json" in cmd_names

def test_cli_registry_has_export_md():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v208-export-md" in cmd_names

def test_cli_registry_has_export_csv():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v208-export-csv" in cmd_names

def test_cli_registry_has_health():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v208-health" in cmd_names

def test_cli_registry_has_gate():
    from cli.command_registry import PROVIDER_COMMANDS
    cmd_names = [c.name for c in PROVIDER_COMMANDS]
    assert "paper-cockpit-v208-gate" in cmd_names


# =========================================================================
# CLI handler resolution (main.py)
# =========================================================================
def test_main_importable():
    import main

def test_main_handler_review_exposure_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v208_review_exposure")

def test_main_handler_evaluate_concentration_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v208_evaluate_concentration")

def test_main_handler_build_warning_queue_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v208_build_warning_queue")

def test_main_handler_build_risk_cap_queue_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v208_build_risk_cap_queue")

def test_main_handler_adjust_candidate_exposure_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v208_adjust_candidate_exposure")

def test_main_handler_export_json_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v208_export_json")

def test_main_handler_export_md_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v208_export_md")

def test_main_handler_export_csv_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v208_export_csv")

def test_main_handler_health_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v208_health")

def test_main_handler_gate_exists():
    import main
    assert hasattr(main, "cmd_paper_cockpit_v208_gate")

def test_main_handler_review_exposure_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v208_review_exposure)

def test_main_handler_evaluate_concentration_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v208_evaluate_concentration)

def test_main_handler_build_warning_queue_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v208_build_warning_queue)

def test_main_handler_build_risk_cap_queue_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v208_build_risk_cap_queue)

def test_main_handler_adjust_candidate_exposure_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v208_adjust_candidate_exposure)

def test_main_handler_export_json_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v208_export_json)

def test_main_handler_export_md_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v208_export_md)

def test_main_handler_export_csv_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v208_export_csv)

def test_main_handler_health_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v208_health)

def test_main_handler_gate_callable():
    import main
    assert callable(main.cmd_paper_cockpit_v208_gate)

def test_no_isolated_command_map_in_main():
    import main
    assert not hasattr(main, "_ISOLATED_V208_COMMAND_MAP")


# =========================================================================
# GUI compatibility
# =========================================================================
def test_gui_importable():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V208
    assert PANEL_VERSION_V208 is not None

def test_panel_version_208():
    from gui.small_capital_strategy_panel import PANEL_VERSION_V208
    assert PANEL_VERSION_V208 == "2.0.8"

def test_panel_version_still_200():
    from gui.small_capital_strategy_panel import PANEL_VERSION
    assert PANEL_VERSION == "2.0.0"

def test_get_tab_names_has_portfolio_exposure_v208():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "portfolio_exposure_v208" in get_tab_names()

def test_get_tab_names_has_theme_concentration_v208():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "theme_concentration_v208" in get_tab_names()

def test_get_tab_names_has_exposure_warning_queue_v208():
    from gui.small_capital_strategy_panel import get_tab_names
    assert "exposure_warning_queue_v208" in get_tab_names()

def test_get_v208_tab_names_count():
    from gui.small_capital_strategy_panel import get_v208_tab_names
    assert len(get_v208_tab_names()) == 3

def test_render_portfolio_exposure_v208_tab():
    from gui.small_capital_strategy_panel import render_portfolio_exposure_v208_tab
    result = render_portfolio_exposure_v208_tab()
    assert result["tab"] == "portfolio_exposure_v208"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False
    assert result["auto_apply_enabled"] is False

def test_render_theme_concentration_v208_tab():
    from gui.small_capital_strategy_panel import render_theme_concentration_v208_tab
    result = render_theme_concentration_v208_tab()
    assert result["tab"] == "theme_concentration_v208"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False
    assert result["auto_apply_enabled"] is False

def test_render_exposure_warning_queue_v208_tab():
    from gui.small_capital_strategy_panel import render_exposure_warning_queue_v208_tab
    result = render_exposure_warning_queue_v208_tab()
    assert result["tab"] == "exposure_warning_queue_v208"
    assert result["paper_only"] is True
    assert result["should_auto_apply"] is False
    assert result["auto_apply_enabled"] is False

def test_render_all_tabs_has_portfolio_exposure_v208():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "portfolio_exposure_v208" in result

def test_render_all_tabs_has_theme_concentration_v208():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "theme_concentration_v208" in result

def test_render_all_tabs_has_exposure_warning_queue_v208():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "exposure_warning_queue_v208" in result

def test_render_all_tabs_portfolio_exposure_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("portfolio_exposure_v208", {})

def test_render_all_tabs_theme_concentration_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("theme_concentration_v208", {})

def test_render_all_tabs_exposure_warning_queue_no_error():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "error" not in result.get("exposure_warning_queue_v208", {})

def test_render_all_tabs_v207_still_works():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    assert "theme_rotation_v207" in result
    assert "error" not in result.get("theme_rotation_v207", {})


# =========================================================================
# Backward compatibility with v2.0.7
# =========================================================================
def test_v207_still_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import VERSION
    assert VERSION == "2.0.7"

def test_v207_run_theme_rotation_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.paper_only is True

def test_v207_should_auto_apply_unchanged():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import run_theme_rotation_review
    result = run_theme_rotation_review()
    assert result.should_auto_apply is False

def test_v207_evaluate_market_regime_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v207 import evaluate_market_regime
    regime = evaluate_market_regime()
    assert regime.should_auto_apply is False

def test_v206_still_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import VERSION
    assert VERSION == "2.0.6"

def test_v206_run_lifecycle_review_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v206 import run_lifecycle_review
    result = run_lifecycle_review()
    assert result.paper_only is True


# =========================================================================
# v201 health relative-path compatibility
# =========================================================================
def test_v201_health_test_exists():
    import os
    base = os.path.dirname(__file__)
    path = os.path.normpath(os.path.join(base, "test_paper_cockpit_v201.py"))
    assert os.path.exists(path)


# =========================================================================
# Health check
# =========================================================================
def test_health_module_importable():
    import paper_trading.small_capital_strategy.paper_cockpit_health_v208

def test_health_run_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v208 import run_health_check
    result = run_health_check()
    assert "all_passed" in result

def test_health_all_passed():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v208 import run_health_check
    result = run_health_check()
    assert result["all_passed"] is True, f"Health failed: {result['errors']}"

def test_health_version_208():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v208 import HEALTH_VERSION
    assert HEALTH_VERSION == "2.0.8"

def test_health_release_name():
    from paper_trading.small_capital_strategy.paper_cockpit_health_v208 import HEALTH_RELEASE
    assert "Exposure" in HEALTH_RELEASE


# =========================================================================
# Release gate
# =========================================================================
def test_gate_module_importable():
    import release.paper_cockpit_release_gate_v208

def test_gate_run_callable():
    from release.paper_cockpit_release_gate_v208 import run_release_gate
    result = run_release_gate()
    assert "gate_passed" in result

def test_gate_all_passed():
    from release.paper_cockpit_release_gate_v208 import run_release_gate
    result = run_release_gate()
    assert result["gate_passed"] is True, f"Gate failed: {result['errors']}"

def test_gate_version_208():
    from release.paper_cockpit_release_gate_v208 import GATE_VERSION
    assert GATE_VERSION == "2.0.8"

def test_gate_baseline_tests():
    from release.paper_cockpit_release_gate_v208 import BASELINE_TESTS
    assert BASELINE_TESTS == 35005


# =========================================================================
# Fixtures
# =========================================================================
def test_fixtures_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v208 import FIXTURES
    assert FIXTURES is not None

def test_fixtures_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v208 import FIXTURES
    assert len(FIXTURES) == 80

def test_fixtures_schema_version_208():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v208 import FIXTURES
    assert all(f["schema_version"] == "208" for f in FIXTURES)

def test_fixtures_paper_only_all():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v208 import FIXTURES
    assert all(f["paper_only"] is True for f in FIXTURES)

def test_fixtures_have_fixture_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v208 import FIXTURES
    assert all("fixture_id" in f for f in FIXTURES)

def test_fixtures_unique_ids():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v208 import FIXTURES
    ids = [f["fixture_id"] for f in FIXTURES]
    assert len(ids) == len(set(ids))


# =========================================================================
# Scenarios
# =========================================================================
def test_scenarios_importable():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v208 import SCENARIOS
    assert SCENARIOS is not None

def test_scenarios_count_80():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v208 import SCENARIOS
    assert len(SCENARIOS) == 80

def test_scenarios_schema_version_208():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v208 import SCENARIOS
    assert all(s["schema_version"] == "208" for s in SCENARIOS)

def test_scenarios_paper_only_all():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v208 import SCENARIOS
    assert all(s["paper_only"] is True for s in SCENARIOS)

def test_scenarios_have_scenario_id():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v208 import SCENARIOS
    assert all("scenario_id" in s for s in SCENARIOS)

def test_scenarios_unique_ids():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v208 import SCENARIOS
    ids = [s["scenario_id"] for s in SCENARIOS]
    assert len(ids) == len(set(ids))

def test_scenarios_all_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v208 import SCENARIOS
    for s in SCENARIOS:
        if "should_auto_apply" in s:
            assert s["should_auto_apply"] is False

def test_scenarios_all_auto_apply_enabled_false():
    from paper_trading.small_capital_strategy.paper_cockpit_scenarios_v208 import SCENARIOS
    for s in SCENARIOS:
        if "auto_apply_enabled" in s:
            assert s["auto_apply_enabled"] is False


# =========================================================================
# Paper-only safety
# =========================================================================
def test_no_broker_guard():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import SAFETY_FLAGS_V208
    assert SAFETY_FLAGS_V208["no_broker"] is True

def test_no_real_orders_guard():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True

def test_broker_execution_enabled_false_guard():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import BROKER_EXECUTION_ENABLED
    assert BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked_guard():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True

def test_exposure_review_no_auto_remove_real_holdings():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    assert result.should_auto_apply is False
    assert result.auto_apply_enabled is False

def test_all_exposure_items_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import run_exposure_review
    result = run_exposure_review()
    all_items = (
        result.portfolio_exposure_snapshot
        + result.volatility_exposure_snapshot
        + result.market_regime_exposure_snapshot
    )
    assert all(i.paper_only is True for i in all_items)

def test_cockpit_summary_208():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import get_cockpit_summary_v208
    summary = get_cockpit_summary_v208()
    assert summary["version"] == "2.0.8"
    assert summary["paper_only"] is True
    assert summary["should_auto_apply"] is False
    assert summary["auto_apply_enabled"] is False
    assert summary["exposure_actions_recommendation_only"] is True

def test_version_info_208():
    from paper_trading.small_capital_strategy.paper_cockpit_v208 import get_version_info
    info = get_version_info()
    assert info["version"] == "2.0.8"
    assert info["should_auto_apply"] == "False"
    assert info["auto_apply_enabled"] == "False"
    assert info["exposure_actions_recommendation_only"] == "True"
