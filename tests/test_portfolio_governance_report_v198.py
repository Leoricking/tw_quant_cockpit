"""
tests/test_portfolio_governance_report_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Report Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.portfolio_governance_report_v198 import (
    REPORT_SECTIONS, _PAPER_HEADER,
    export_portfolio_snapshot, export_exposure_summary,
    export_theme_risk, export_industry_risk,
    export_concentration_risk, export_correlation_risk,
    export_risk_limits, export_risk_score_and_grade,
    export_recommendations, export_risk_overlay_decisions,
    export_audit_trail, export_full_governance_pack,
)


class TestReportSections:
    def test_count_is_12(self):
        assert len(REPORT_SECTIONS) == 12

    def test_has_portfolio_snapshot(self):
        assert "portfolio_snapshot" in REPORT_SECTIONS

    def test_has_exposure_summary(self):
        assert "exposure_summary" in REPORT_SECTIONS

    def test_has_theme_risk_analysis(self):
        assert "theme_risk_analysis" in REPORT_SECTIONS

    def test_has_industry_risk_analysis(self):
        assert "industry_risk_analysis" in REPORT_SECTIONS

    def test_has_concentration_risk(self):
        assert "concentration_risk" in REPORT_SECTIONS

    def test_has_correlation_risk(self):
        assert "correlation_risk" in REPORT_SECTIONS

    def test_has_risk_limits_evaluation(self):
        assert "risk_limits_evaluation" in REPORT_SECTIONS

    def test_has_risk_score_and_grade(self):
        assert "risk_score_and_grade" in REPORT_SECTIONS

    def test_has_governance_recommendations(self):
        assert "governance_recommendations" in REPORT_SECTIONS

    def test_has_risk_overlay_decisions(self):
        assert "risk_overlay_decisions" in REPORT_SECTIONS

    def test_has_audit_trail(self):
        assert "audit_trail" in REPORT_SECTIONS

    def test_all_strings(self):
        assert all(isinstance(s, str) for s in REPORT_SECTIONS)


class TestExportPortfolioSnapshot:
    def test_returns_dict(self):
        assert isinstance(export_portfolio_snapshot({}), dict)

    def test_section_key_correct(self):
        assert export_portfolio_snapshot({})["section"] == "portfolio_snapshot"

    def test_paper_only_True(self):
        assert export_portfolio_snapshot({})["paper_only"] is True

    def test_no_real_orders_True(self):
        assert export_portfolio_snapshot({})["no_real_orders"] is True

    def test_report_triggers_rebalance_False(self):
        assert export_portfolio_snapshot({})["report_triggers_rebalance"] is False


class TestExportExposureSummary:
    def test_returns_dict(self):
        assert isinstance(export_exposure_summary({}), dict)

    def test_section_key_correct(self):
        assert export_exposure_summary({})["section"] == "exposure_summary"

    def test_paper_only_True(self):
        assert export_exposure_summary({})["paper_only"] is True


class TestExportThemeRisk:
    def test_returns_dict(self):
        assert isinstance(export_theme_risk([]), dict)

    def test_section_key_correct(self):
        assert export_theme_risk([])["section"] == "theme_risk_analysis"

    def test_paper_only_True(self):
        assert export_theme_risk([])["paper_only"] is True


class TestExportIndustryRisk:
    def test_returns_dict(self):
        assert isinstance(export_industry_risk([]), dict)

    def test_section_key_correct(self):
        assert export_industry_risk([])["section"] == "industry_risk_analysis"

    def test_paper_only_True(self):
        assert export_industry_risk([])["paper_only"] is True


class TestExportConcentrationRisk:
    def test_returns_dict(self):
        assert isinstance(export_concentration_risk({}), dict)

    def test_section_key_correct(self):
        assert export_concentration_risk({})["section"] == "concentration_risk"

    def test_paper_only_True(self):
        assert export_concentration_risk({})["paper_only"] is True


class TestExportCorrelationRisk:
    def test_returns_dict(self):
        assert isinstance(export_correlation_risk({}), dict)

    def test_section_key_correct(self):
        assert export_correlation_risk({})["section"] == "correlation_risk"

    def test_paper_only_True(self):
        assert export_correlation_risk({})["paper_only"] is True


class TestExportRiskLimits:
    def test_returns_dict(self):
        assert isinstance(export_risk_limits({}), dict)

    def test_section_key_correct(self):
        assert export_risk_limits({})["section"] == "risk_limits_evaluation"

    def test_paper_only_True(self):
        assert export_risk_limits({})["paper_only"] is True


class TestExportRiskScoreAndGrade:
    def test_returns_dict(self):
        assert isinstance(export_risk_score_and_grade(0.0, "LOW"), dict)

    def test_section_key_correct(self):
        assert export_risk_score_and_grade(0.0, "LOW")["section"] == "risk_score_and_grade"

    def test_score_present(self):
        assert export_risk_score_and_grade(0.5, "ELEVATED")["score"] == 0.5

    def test_grade_present(self):
        assert export_risk_score_and_grade(0.5, "ELEVATED")["grade"] == "ELEVATED"

    def test_paper_only_True(self):
        assert export_risk_score_and_grade(0.0, "LOW")["paper_only"] is True


class TestExportRecommendations:
    def test_returns_dict(self):
        assert isinstance(export_recommendations([]), dict)

    def test_section_key_correct(self):
        assert export_recommendations([])["section"] == "governance_recommendations"

    def test_recommendations_present(self):
        assert "recommendations" in export_recommendations(["NO_CHANGE"])

    def test_paper_only_True(self):
        assert export_recommendations([])["paper_only"] is True


class TestExportRiskOverlayDecisions:
    def test_returns_dict(self):
        assert isinstance(export_risk_overlay_decisions([]), dict)

    def test_section_key_correct(self):
        assert export_risk_overlay_decisions([])["section"] == "risk_overlay_decisions"

    def test_paper_only_True(self):
        assert export_risk_overlay_decisions([])["paper_only"] is True


class TestExportAuditTrail:
    def test_returns_dict(self):
        assert isinstance(export_audit_trail([]), dict)

    def test_section_key_correct(self):
        assert export_audit_trail([])["section"] == "audit_trail"

    def test_immutable_True(self):
        assert export_audit_trail([])["immutable"] is True

    def test_paper_only_True(self):
        assert export_audit_trail([])["paper_only"] is True


class TestExportFullGovernancePack:
    def test_returns_dict(self):
        assert isinstance(export_full_governance_pack(), dict)

    def test_paper_only_True(self):
        assert export_full_governance_pack()["paper_only"] is True

    def test_no_real_orders_True(self):
        assert export_full_governance_pack()["no_real_orders"] is True

    def test_report_triggers_rebalance_False(self):
        assert export_full_governance_pack()["report_triggers_rebalance"] is False

    def test_dashboard_mutates_strategy_False(self):
        assert export_full_governance_pack()["dashboard_mutates_strategy"] is False

    def test_section_count_12(self):
        assert export_full_governance_pack()["section_count"] == 12

    def test_has_portfolio_snapshot_key(self):
        assert "portfolio_snapshot" in export_full_governance_pack()

    def test_has_exposure_summary_key(self):
        assert "exposure_summary" in export_full_governance_pack()

    def test_has_risk_score_and_grade_key(self):
        assert "risk_score_and_grade" in export_full_governance_pack()

    def test_has_audit_trail_key(self):
        assert "audit_trail" in export_full_governance_pack()

    def test_has_recommendations_key(self):
        assert "recommendations" in export_full_governance_pack()

    def test_not_investment_advice_True(self):
        assert export_full_governance_pack()["not_investment_advice"] is True
