"""
tests/test_portfolio_governance_models_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Model Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_governance_models_v198 import (
    _ALL_MODEL_NAMES,
    PaperPortfolioGovernanceInput, PaperPortfolioGovernanceResult,
    PaperPortfolioSnapshot, PaperPortfolioPosition,
    PaperPortfolioStrategyExposure, PaperPortfolioThemeExposure,
    PaperPortfolioIndustryExposure, PaperPortfolioMarketExposure,
    PaperPortfolioRiskOverlay, PaperPortfolioRiskLimit,
    PaperPortfolioRiskLimitResult, PaperPortfolioConcentrationRisk,
    PaperPortfolioCorrelationRisk, PaperPortfolioThemeOverlap,
    PaperPortfolioDecisionOverlap, PaperPortfolioExposureSummary,
    PaperPortfolioRiskScore, PaperPortfolioRiskGrade,
    PaperPortfolioRiskRecommendation, PaperPortfolioRiskBlock,
    PaperPortfolioGovernanceDecision, PaperPortfolioGovernanceDashboard,
    PaperPortfolioGovernanceReport, PaperPortfolioAuditTrail,
    PaperPortfolioHealthSummary, PaperPortfolioValidationResult,
)


class TestModelRegistry:
    def test_all_model_names_count_26(self):
        assert len(_ALL_MODEL_NAMES) == 26

    def test_all_model_names_are_strings(self):
        assert all(isinstance(n, str) for n in _ALL_MODEL_NAMES)

    def test_governance_input_in_names(self):
        assert "PaperPortfolioGovernanceInput" in _ALL_MODEL_NAMES

    def test_validation_result_in_names(self):
        assert "PaperPortfolioValidationResult" in _ALL_MODEL_NAMES


class TestGovernanceInput:
    def test_instantiate_defaults(self):
        obj = PaperPortfolioGovernanceInput()
        assert obj is not None

    def test_schema_version_198(self):
        assert PaperPortfolioGovernanceInput().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioGovernanceInput().paper_only is True

    def test_no_real_orders_True(self):
        assert PaperPortfolioGovernanceInput().no_real_orders is True

    def test_no_broker_True(self):
        assert PaperPortfolioGovernanceInput().no_broker is True

    def test_positions_default_list(self):
        assert isinstance(PaperPortfolioGovernanceInput().positions, list)

    def test_exposure_summary_default_dict(self):
        assert isinstance(PaperPortfolioGovernanceInput().exposure_summary, dict)

    def test_risk_limits_default_dict(self):
        assert isinstance(PaperPortfolioGovernanceInput().risk_limits, dict)


class TestGovernanceResult:
    def test_instantiate_defaults(self):
        assert PaperPortfolioGovernanceResult() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioGovernanceResult().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioGovernanceResult().paper_only is True

    def test_no_real_orders_True(self):
        assert PaperPortfolioGovernanceResult().no_real_orders is True

    def test_governance_passed_default_False(self):
        assert PaperPortfolioGovernanceResult().governance_passed is False

    def test_recommendations_default_list(self):
        assert isinstance(PaperPortfolioGovernanceResult().recommendations, list)

    def test_blocks_default_list(self):
        assert isinstance(PaperPortfolioGovernanceResult().blocks, list)


class TestSnapshot:
    def test_instantiate_defaults(self):
        assert PaperPortfolioSnapshot() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioSnapshot().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioSnapshot().paper_only is True

    def test_total_positions_default_0(self):
        assert PaperPortfolioSnapshot().total_positions == 0

    def test_cash_buffer_default_0(self):
        assert PaperPortfolioSnapshot().cash_buffer == 0.0


class TestPosition:
    def test_instantiate_defaults(self):
        assert PaperPortfolioPosition() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioPosition().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioPosition().paper_only is True

    def test_paper_weight_default_0(self):
        assert PaperPortfolioPosition().paper_weight == 0.0

    def test_symbol_default_str(self):
        assert isinstance(PaperPortfolioPosition().symbol, str)


class TestStrategyExposure:
    def test_instantiate_defaults(self):
        assert PaperPortfolioStrategyExposure() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioStrategyExposure().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioStrategyExposure().paper_only is True

    def test_position_count_default_0(self):
        assert PaperPortfolioStrategyExposure().position_count == 0


class TestThemeExposure:
    def test_instantiate_defaults(self):
        assert PaperPortfolioThemeExposure() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioThemeExposure().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioThemeExposure().paper_only is True

    def test_total_weight_default_0(self):
        assert PaperPortfolioThemeExposure().total_weight == 0.0


class TestIndustryExposure:
    def test_instantiate_defaults(self):
        assert PaperPortfolioIndustryExposure() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioIndustryExposure().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioIndustryExposure().paper_only is True


class TestMarketExposure:
    def test_instantiate_defaults(self):
        assert PaperPortfolioMarketExposure() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioMarketExposure().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioMarketExposure().paper_only is True

    def test_taiwan_index_beta_default_0(self):
        assert PaperPortfolioMarketExposure().taiwan_index_beta == 0.0

    def test_tsmc_sensitivity_default_0(self):
        assert PaperPortfolioMarketExposure().tsmc_sensitivity == 0.0


class TestRiskOverlay:
    def test_instantiate_defaults(self):
        assert PaperPortfolioRiskOverlay() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioRiskOverlay().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioRiskOverlay().paper_only is True

    def test_no_real_orders_True(self):
        assert PaperPortfolioRiskOverlay().no_real_orders is True

    def test_overlay_passed_default_False(self):
        assert PaperPortfolioRiskOverlay().overlay_passed is False


class TestRiskLimit:
    def test_instantiate_defaults(self):
        assert PaperPortfolioRiskLimit() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioRiskLimit().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioRiskLimit().paper_only is True

    def test_limit_value_default_1(self):
        assert PaperPortfolioRiskLimit().limit_value == 1.0


class TestRiskLimitResult:
    def test_instantiate_defaults(self):
        assert PaperPortfolioRiskLimitResult() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioRiskLimitResult().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioRiskLimitResult().paper_only is True

    def test_breached_default_False(self):
        assert PaperPortfolioRiskLimitResult().breached is False


class TestConcentrationRisk:
    def test_instantiate_defaults(self):
        assert PaperPortfolioConcentrationRisk() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioConcentrationRisk().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioConcentrationRisk().paper_only is True

    def test_breach_default_False(self):
        assert PaperPortfolioConcentrationRisk().breach is False


class TestCorrelationRisk:
    def test_instantiate_defaults(self):
        assert PaperPortfolioCorrelationRisk() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioCorrelationRisk().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioCorrelationRisk().paper_only is True

    def test_cluster_symbols_default_list(self):
        assert isinstance(PaperPortfolioCorrelationRisk().cluster_symbols, list)


class TestThemeOverlap:
    def test_instantiate_defaults(self):
        assert PaperPortfolioThemeOverlap() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioThemeOverlap().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioThemeOverlap().paper_only is True

    def test_overlap_score_default_0(self):
        assert PaperPortfolioThemeOverlap().overlap_score == 0.0


class TestDecisionOverlap:
    def test_instantiate_defaults(self):
        assert PaperPortfolioDecisionOverlap() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioDecisionOverlap().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioDecisionOverlap().paper_only is True

    def test_duplicate_exposure_default_False(self):
        assert PaperPortfolioDecisionOverlap().duplicate_exposure is False


class TestExposureSummary:
    def test_instantiate_defaults(self):
        assert PaperPortfolioExposureSummary() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioExposureSummary().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioExposureSummary().paper_only is True

    def test_symbol_count_default_0(self):
        assert PaperPortfolioExposureSummary().symbol_count == 0


class TestRiskScore:
    def test_instantiate_defaults(self):
        assert PaperPortfolioRiskScore() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioRiskScore().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioRiskScore().paper_only is True

    def test_score_default_0(self):
        assert PaperPortfolioRiskScore().score == 0.0

    def test_components_default_dict(self):
        assert isinstance(PaperPortfolioRiskScore().components, dict)


class TestRiskGrade:
    def test_instantiate_defaults(self):
        assert PaperPortfolioRiskGrade() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioRiskGrade().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioRiskGrade().paper_only is True

    def test_grade_default_LOW(self):
        assert PaperPortfolioRiskGrade().grade == "LOW"

    def test_threshold_low_0_2(self):
        assert PaperPortfolioRiskGrade().threshold_low == 0.2


class TestRiskRecommendation:
    def test_instantiate_defaults(self):
        assert PaperPortfolioRiskRecommendation() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioRiskRecommendation().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioRiskRecommendation().paper_only is True

    def test_priority_default_0(self):
        assert PaperPortfolioRiskRecommendation().priority == 0


class TestRiskBlock:
    def test_instantiate_defaults(self):
        assert PaperPortfolioRiskBlock() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioRiskBlock().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioRiskBlock().paper_only is True

    def test_no_real_orders_True(self):
        assert PaperPortfolioRiskBlock().no_real_orders is True

    def test_blocked_default_True(self):
        assert PaperPortfolioRiskBlock().blocked is True


class TestGovernanceDecision:
    def test_instantiate_defaults(self):
        assert PaperPortfolioGovernanceDecision() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioGovernanceDecision().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioGovernanceDecision().paper_only is True

    def test_no_real_orders_True(self):
        assert PaperPortfolioGovernanceDecision().no_real_orders is True


class TestGovernanceDashboard:
    def test_instantiate_defaults(self):
        assert PaperPortfolioGovernanceDashboard() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioGovernanceDashboard().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioGovernanceDashboard().paper_only is True

    def test_no_real_orders_True(self):
        assert PaperPortfolioGovernanceDashboard().no_real_orders is True

    def test_dashboard_mutates_strategy_False(self):
        assert PaperPortfolioGovernanceDashboard().dashboard_mutates_strategy is False

    def test_panels_default_list(self):
        assert isinstance(PaperPortfolioGovernanceDashboard().panels, list)


class TestGovernanceReport:
    def test_instantiate_defaults(self):
        assert PaperPortfolioGovernanceReport() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioGovernanceReport().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioGovernanceReport().paper_only is True

    def test_no_real_orders_True(self):
        assert PaperPortfolioGovernanceReport().no_real_orders is True

    def test_report_triggers_rebalance_False(self):
        assert PaperPortfolioGovernanceReport().report_triggers_rebalance is False

    def test_sections_default_list(self):
        assert isinstance(PaperPortfolioGovernanceReport().sections, list)


class TestAuditTrail:
    def test_instantiate_defaults(self):
        assert PaperPortfolioAuditTrail() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioAuditTrail().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioAuditTrail().paper_only is True

    def test_immutable_True(self):
        assert PaperPortfolioAuditTrail().immutable is True


class TestHealthSummary:
    def test_instantiate_defaults(self):
        assert PaperPortfolioHealthSummary() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioHealthSummary().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioHealthSummary().paper_only is True

    def test_all_passed_default_False(self):
        assert PaperPortfolioHealthSummary().all_passed is False


class TestValidationResult:
    def test_instantiate_defaults(self):
        assert PaperPortfolioValidationResult() is not None

    def test_schema_version_198(self):
        assert PaperPortfolioValidationResult().schema_version == "198"

    def test_paper_only_True(self):
        assert PaperPortfolioValidationResult().paper_only is True

    def test_valid_default_False(self):
        assert PaperPortfolioValidationResult().valid is False

    def test_errors_default_list(self):
        assert isinstance(PaperPortfolioValidationResult().errors, list)

    def test_warnings_default_list(self):
        assert isinstance(PaperPortfolioValidationResult().warnings, list)
