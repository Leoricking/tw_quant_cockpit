"""
tests/test_decision_report_models_v187.py
Tests for decision_report_models_v187 — v1.8.7 Decision Report Export & Evidence Pack.
[!] Research Only. Paper Only. Report Only. Audit Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.decision_report_models_v187 import (
    DecisionReportInput, DecisionReportResult,
    DailyDecisionReport, WeeklyDecisionReport,
    CandidateEvidenceItem, CandidateEvidencePack,
    BlockReasonEvidence, BuyPointEvidence,
    RiskEvidence, PositionSizingEvidence,
    PortfolioEvidence, MonteCarloEvidence,
    ThemeEvidence, MarketRegimeEvidence,
    WatchlistReport, BlockedCandidateReport,
    ReduceRiskReport, PaperPlanReadyReport,
    DecisionAuditTrail, ReportExportManifest,
    ReportValidationResult, ReportHealthSummary,
    get_all_model_names,
)


# ── get_all_model_names ───────────────────────────────────────────────────────

def test_model_count_22():
    assert len(get_all_model_names()) == 22


def test_model_names_contains_all_key_models():
    names = get_all_model_names()
    for expected in ["DecisionReportInput", "DecisionReportResult", "DailyDecisionReport",
                     "WeeklyDecisionReport", "CandidateEvidenceItem", "ReportHealthSummary"]:
        assert expected in names


# ── DecisionReportInput ───────────────────────────────────────────────────────

def test_decision_report_input_paper_only():
    assert DecisionReportInput().paper_only is True


def test_decision_report_input_no_real_orders():
    assert DecisionReportInput().no_real_orders is True


def test_decision_report_input_not_investment_advice():
    assert DecisionReportInput().not_investment_advice is True


def test_decision_report_input_production_trading_blocked():
    assert DecisionReportInput().production_trading_blocked is True


def test_decision_report_input_schema_version():
    assert DecisionReportInput().schema_version == "187"


def test_decision_report_input_default_report_type():
    assert DecisionReportInput().report_type == "daily_decision_report"


# ── DecisionReportResult ──────────────────────────────────────────────────────

def test_decision_report_result_paper_only():
    assert DecisionReportResult().paper_only is True


def test_decision_report_result_no_real_orders():
    assert DecisionReportResult().no_real_orders is True


def test_decision_report_result_not_investment_advice():
    assert DecisionReportResult().not_investment_advice is True


def test_decision_report_result_production_trading_blocked():
    assert DecisionReportResult().production_trading_blocked is True


def test_decision_report_result_schema_version():
    assert DecisionReportResult().schema_version == "187"


def test_decision_report_result_default_grade():
    assert DecisionReportResult().final_report_grade == "COMPLETE"


# ── DailyDecisionReport ───────────────────────────────────────────────────────

def test_daily_decision_report_paper_only():
    assert DailyDecisionReport().paper_only is True


def test_daily_decision_report_no_real_orders():
    assert DailyDecisionReport().no_real_orders is True


def test_daily_decision_report_production_trading_blocked():
    assert DailyDecisionReport().production_trading_blocked is True


def test_daily_decision_report_report_type():
    assert DailyDecisionReport().report_type == "daily_decision_report"


def test_daily_decision_report_schema_version():
    assert DailyDecisionReport().schema_version == "187"


# ── WeeklyDecisionReport ──────────────────────────────────────────────────────

def test_weekly_decision_report_paper_only():
    assert WeeklyDecisionReport().paper_only is True


def test_weekly_decision_report_no_real_orders():
    assert WeeklyDecisionReport().no_real_orders is True


def test_weekly_decision_report_not_investment_advice():
    assert WeeklyDecisionReport().not_investment_advice is True


def test_weekly_decision_report_report_type():
    assert WeeklyDecisionReport().report_type == "weekly_decision_report"


# ── CandidateEvidenceItem ─────────────────────────────────────────────────────

def test_candidate_evidence_item_paper_only():
    assert CandidateEvidenceItem().paper_only is True


def test_candidate_evidence_item_no_real_orders():
    assert CandidateEvidenceItem().no_real_orders is True


def test_candidate_evidence_item_default_decision():
    assert CandidateEvidenceItem().decision_action == "WAIT"


def test_candidate_evidence_item_custom_ticker():
    item = CandidateEvidenceItem(ticker="2330")
    assert item.ticker == "2330"


# ── CandidateEvidencePack ─────────────────────────────────────────────────────

def test_candidate_evidence_pack_paper_only():
    assert CandidateEvidencePack().paper_only is True


def test_candidate_evidence_pack_no_real_orders():
    assert CandidateEvidencePack().no_real_orders is True


def test_candidate_evidence_pack_production_trading_blocked():
    assert CandidateEvidencePack().production_trading_blocked is True


def test_candidate_evidence_pack_audit_complete():
    assert CandidateEvidencePack().audit_complete is True


# ── BlockReasonEvidence ───────────────────────────────────────────────────────

def test_block_reason_evidence_paper_only():
    assert BlockReasonEvidence().paper_only is True


def test_block_reason_evidence_default_severity():
    assert BlockReasonEvidence().severity == "HIGH"


def test_block_reason_evidence_custom():
    ev = BlockReasonEvidence(block_code="BEAR_REGIME", block_description="Bear market blocked")
    assert ev.block_code == "BEAR_REGIME"
    assert ev.block_description == "Bear market blocked"


# ── BuyPointEvidence ──────────────────────────────────────────────────────────

def test_buy_point_evidence_paper_only():
    assert BuyPointEvidence().paper_only is True


def test_buy_point_evidence_stop_loss_defined():
    assert BuyPointEvidence().stop_loss_defined is True


def test_buy_point_evidence_default_type():
    assert BuyPointEvidence().buy_point_type == "A_10MA_PULLBACK"


# ── RiskEvidence ──────────────────────────────────────────────────────────────

def test_risk_evidence_paper_only():
    assert RiskEvidence().paper_only is True


def test_risk_evidence_default_cash_ok():
    assert RiskEvidence().cash_ok is True


def test_risk_evidence_default_exposure_ok():
    assert RiskEvidence().exposure_ok is True


# ── PositionSizingEvidence ────────────────────────────────────────────────────

def test_position_sizing_evidence_paper_only():
    assert PositionSizingEvidence().paper_only is True


def test_position_sizing_evidence_default_capital():
    assert PositionSizingEvidence().capital == 300000.0


# ── PortfolioEvidence ─────────────────────────────────────────────────────────

def test_portfolio_evidence_paper_only():
    assert PortfolioEvidence().paper_only is True


def test_portfolio_evidence_default_portfolio_ok():
    assert PortfolioEvidence().portfolio_ok is True


# ── MonteCarloEvidence ────────────────────────────────────────────────────────

def test_monte_carlo_evidence_paper_only():
    assert MonteCarloEvidence().paper_only is True


def test_monte_carlo_evidence_default_entry_allowed():
    assert MonteCarloEvidence().entry_allowed is True


def test_monte_carlo_evidence_default_risk_level():
    assert MonteCarloEvidence().ruin_risk_level == "LOW"


# ── ThemeEvidence ─────────────────────────────────────────────────────────────

def test_theme_evidence_paper_only():
    assert ThemeEvidence().paper_only is True


def test_theme_evidence_default_concentration_blocked():
    assert ThemeEvidence().concentration_blocked is False


# ── MarketRegimeEvidence ──────────────────────────────────────────────────────

def test_market_regime_evidence_paper_only():
    assert MarketRegimeEvidence().paper_only is True


def test_market_regime_evidence_default_regime():
    assert MarketRegimeEvidence().market_regime == "BULL"


# ── WatchlistReport ───────────────────────────────────────────────────────────

def test_watchlist_report_paper_only():
    assert WatchlistReport().paper_only is True


def test_watchlist_report_production_trading_blocked():
    assert WatchlistReport().production_trading_blocked is True


def test_watchlist_report_type():
    assert WatchlistReport().report_type == "watchlist_report"


# ── BlockedCandidateReport ────────────────────────────────────────────────────

def test_blocked_candidate_report_paper_only():
    assert BlockedCandidateReport().paper_only is True


def test_blocked_candidate_report_production_trading_blocked():
    assert BlockedCandidateReport().production_trading_blocked is True


# ── ReduceRiskReport ──────────────────────────────────────────────────────────

def test_reduce_risk_report_paper_only():
    assert ReduceRiskReport().paper_only is True


def test_reduce_risk_report_not_investment_advice():
    assert ReduceRiskReport().not_investment_advice is True


# ── PaperPlanReadyReport ──────────────────────────────────────────────────────

def test_paper_plan_ready_report_paper_only():
    assert PaperPlanReadyReport().paper_only is True


def test_paper_plan_ready_report_no_real_orders():
    assert PaperPlanReadyReport().no_real_orders is True


def test_paper_plan_ready_report_type():
    assert PaperPlanReadyReport().report_type == "paper_plan_ready_report"


# ── DecisionAuditTrail ────────────────────────────────────────────────────────

def test_decision_audit_trail_paper_only():
    assert DecisionAuditTrail().paper_only is True


def test_decision_audit_trail_audit_complete():
    assert DecisionAuditTrail().audit_complete is True


def test_decision_audit_trail_type():
    assert DecisionAuditTrail().report_type == "audit_trail"


# ── ReportExportManifest ──────────────────────────────────────────────────────

def test_report_export_manifest_paper_only():
    assert ReportExportManifest().paper_only is True


def test_report_export_manifest_all_exports_safe():
    assert ReportExportManifest().all_exports_safe is True


def test_report_export_manifest_type():
    assert ReportExportManifest().report_type == "export_manifest"


# ── ReportValidationResult ────────────────────────────────────────────────────

def test_report_validation_result_paper_only():
    assert ReportValidationResult().paper_only is True


def test_report_validation_result_default_valid():
    assert ReportValidationResult().valid is True


def test_report_validation_result_no_real_orders():
    assert ReportValidationResult().no_real_orders is True


# ── ReportHealthSummary ───────────────────────────────────────────────────────

def test_report_health_summary_paper_only():
    assert ReportHealthSummary().paper_only is True


def test_report_health_summary_no_real_orders():
    assert ReportHealthSummary().no_real_orders is True


def test_report_health_summary_default_status():
    assert ReportHealthSummary().status == "FAIL"


def test_report_health_summary_custom():
    s = ReportHealthSummary(total=10, passed=10, failed=0, all_passed=True, status="PASS")
    assert s.all_passed is True
    assert s.status == "PASS"
    assert s.total == 10
