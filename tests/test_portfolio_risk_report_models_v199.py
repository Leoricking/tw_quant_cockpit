"""
tests/test_portfolio_risk_report_models_v199.py
v1.9.9 Paper Portfolio Risk Report & Position Sizing Policy Lab — Models Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from paper_trading.small_capital_strategy.portfolio_risk_report_models_v199 import (
    PaperPortfolioRiskReportInput,
    PaperPortfolioRiskReportResult,
    PaperCapitalProfile,
    PaperRiskBudget,
    PaperTradeRiskBudget,
    PaperPositionSizingPolicy,
    PaperPositionSizingResult,
    PaperEntryType,
    PaperEntrySizingRule,
    PaperStopDistanceRule,
    PaperCashBufferPolicy,
    PaperExposureLimitPolicy,
    PaperThemeSizingLimit,
    PaperIndustrySizingLimit,
    PaperStrategySizingLimit,
    PaperRiskOffSizingPolicy,
    PaperNoEntryCondition,
    PaperAddPositionRule,
    PaperReducePositionRule,
    PaperPositionSizingAuditTrail,
    PaperRiskReportDashboard,
    PaperRiskReportExport,
    PaperRiskReportHealthSummary,
    PaperRiskReportValidationResult,
    PaperRiskReportRecommendation,
    _ALL_MODEL_NAMES,
)


def test_all_model_names_count_is_25():
    assert len(_ALL_MODEL_NAMES) == 25


def test_all_model_names_are_strings():
    assert all(isinstance(n, str) for n in _ALL_MODEL_NAMES)


def test_paper_portfolio_risk_report_input_default_schema_version():
    assert PaperPortfolioRiskReportInput().schema_version == "199"


def test_paper_portfolio_risk_report_input_paper_only_True():
    assert PaperPortfolioRiskReportInput().paper_only is True


def test_paper_portfolio_risk_report_input_no_real_orders_True():
    assert PaperPortfolioRiskReportInput().no_real_orders is True


def test_paper_portfolio_risk_report_input_not_investment_advice_True():
    assert PaperPortfolioRiskReportInput().not_investment_advice is True


def test_paper_portfolio_risk_report_input_production_trading_blocked_True():
    assert PaperPortfolioRiskReportInput().production_trading_blocked is True


def test_paper_portfolio_risk_report_input_capital_base_300k():
    assert PaperPortfolioRiskReportInput().capital_base == 300_000.0


def test_paper_portfolio_risk_report_result_schema_version_199():
    assert PaperPortfolioRiskReportResult().schema_version == "199"


def test_paper_portfolio_risk_report_result_paper_only_True():
    assert PaperPortfolioRiskReportResult().paper_only is True


def test_paper_portfolio_risk_report_result_sizing_executes_order_False():
    assert PaperPortfolioRiskReportResult().sizing_executes_order is False


def test_paper_portfolio_risk_report_result_sizing_mutates_strategy_False():
    assert PaperPortfolioRiskReportResult().sizing_mutates_strategy is False


def test_paper_portfolio_risk_report_result_sizing_rebalances_real_portfolio_False():
    assert PaperPortfolioRiskReportResult().sizing_rebalances_real_portfolio is False


def test_paper_capital_profile_default_schema_version():
    assert PaperCapitalProfile().schema_version == "199"


def test_paper_capital_profile_paper_only_True():
    assert PaperCapitalProfile().paper_only is True


def test_paper_capital_profile_default_capital_base():
    assert PaperCapitalProfile().capital_base == 300_000.0


def test_paper_capital_profile_min_cash_buffer_pct():
    assert PaperCapitalProfile().min_cash_buffer_pct == 0.05


def test_paper_capital_profile_weak_market_cash_buffer_pct():
    assert PaperCapitalProfile().weak_market_cash_buffer_pct == 0.50


def test_paper_capital_profile_max_single_symbol_weight():
    assert PaperCapitalProfile().max_single_symbol_weight == 0.20


def test_paper_capital_profile_max_single_theme_weight():
    assert PaperCapitalProfile().max_single_theme_weight == 0.35


def test_paper_capital_profile_not_investment_advice_True():
    assert PaperCapitalProfile().not_investment_advice is True


def test_paper_risk_budget_schema_version_199():
    assert PaperRiskBudget().schema_version == "199"


def test_paper_risk_budget_paper_only_True():
    assert PaperRiskBudget().paper_only is True


def test_paper_trade_risk_budget_schema_version_199():
    assert PaperTradeRiskBudget().schema_version == "199"


def test_paper_trade_risk_budget_paper_only_True():
    assert PaperTradeRiskBudget().paper_only is True


def test_paper_position_sizing_policy_schema_version_199():
    assert PaperPositionSizingPolicy().schema_version == "199"


def test_paper_position_sizing_policy_sizing_executes_order_False():
    assert PaperPositionSizingPolicy().sizing_executes_order is False


def test_paper_position_sizing_result_schema_version_199():
    assert PaperPositionSizingResult().schema_version == "199"


def test_paper_position_sizing_result_sizing_executes_order_False():
    assert PaperPositionSizingResult().sizing_executes_order is False


def test_paper_position_sizing_result_sizing_mutates_strategy_False():
    assert PaperPositionSizingResult().sizing_mutates_strategy is False


def test_paper_entry_type_schema_version_199():
    assert PaperEntryType().schema_version == "199"


def test_paper_entry_sizing_rule_sizing_executes_order_False():
    assert PaperEntrySizingRule().sizing_executes_order is False


def test_paper_stop_distance_rule_schema_version_199():
    assert PaperStopDistanceRule().schema_version == "199"


def test_paper_cash_buffer_policy_schema_version_199():
    assert PaperCashBufferPolicy().schema_version == "199"


def test_paper_cash_buffer_policy_min_cash_buffer_pct():
    assert PaperCashBufferPolicy().min_cash_buffer_pct == 0.05


def test_paper_exposure_limit_policy_schema_version_199():
    assert PaperExposureLimitPolicy().schema_version == "199"


def test_paper_theme_sizing_limit_schema_version_199():
    assert PaperThemeSizingLimit().schema_version == "199"


def test_paper_industry_sizing_limit_schema_version_199():
    assert PaperIndustrySizingLimit().schema_version == "199"


def test_paper_strategy_sizing_limit_schema_version_199():
    assert PaperStrategySizingLimit().schema_version == "199"


def test_paper_risk_off_sizing_policy_sizing_executes_order_False():
    assert PaperRiskOffSizingPolicy().sizing_executes_order is False


def test_paper_no_entry_condition_executes_real_order_False():
    assert PaperNoEntryCondition().executes_real_order is False


def test_paper_add_position_rule_executes_real_order_False():
    assert PaperAddPositionRule().executes_real_order is False


def test_paper_reduce_position_rule_executes_real_order_False():
    assert PaperReducePositionRule().executes_real_order is False


def test_paper_position_sizing_audit_trail_sizing_executes_order_False():
    assert PaperPositionSizingAuditTrail().sizing_executes_order is False


def test_paper_position_sizing_audit_trail_sizing_mutates_strategy_False():
    assert PaperPositionSizingAuditTrail().sizing_mutates_strategy is False


def test_paper_risk_report_dashboard_dashboard_mutates_strategy_False():
    assert PaperRiskReportDashboard().dashboard_mutates_strategy is False


def test_paper_risk_report_dashboard_dashboard_places_real_order_False():
    assert PaperRiskReportDashboard().dashboard_places_real_order is False


def test_paper_risk_report_export_export_triggers_real_order_False():
    assert PaperRiskReportExport().export_triggers_real_order is False


def test_paper_risk_report_export_export_mutates_production_False():
    assert PaperRiskReportExport().export_mutates_production is False


def test_paper_risk_report_health_summary_schema_version_199():
    assert PaperRiskReportHealthSummary().schema_version == "199"


def test_paper_risk_report_validation_result_schema_version_199():
    assert PaperRiskReportValidationResult().schema_version == "199"


def test_paper_risk_report_recommendation_executes_order_False():
    assert PaperRiskReportRecommendation().recommendation_executes_order is False


def test_paper_risk_report_recommendation_mutates_strategy_False():
    assert PaperRiskReportRecommendation().recommendation_mutates_strategy is False
