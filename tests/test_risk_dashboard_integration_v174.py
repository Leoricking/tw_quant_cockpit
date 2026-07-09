"""
tests/test_risk_dashboard_integration_v174.py
Integration tests for end-to-end risk dashboard pipeline v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
import json
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import (
    RiskStatus, RiskDashboardScorecardGrade,
)
from paper_trading.small_capital_strategy.small_capital_risk_adapter_v174 import (
    build_risk_dashboard, get_default_pass_input,
)
from paper_trading.small_capital_strategy.risk_dashboard_scorecard_v174 import compute_scorecard
from paper_trading.small_capital_strategy.risk_dashboard_report_v174 import (
    build_report, render_markdown, render_json, render_csv, render_console_summary,
)


def _build_all(inp):
    dashboard = build_risk_dashboard(inp)
    scorecard = compute_scorecard(dashboard)
    report = build_report(dashboard, scorecard)
    return dashboard, scorecard, report


class TestPassInputFullPipeline:
    def setup_method(self):
        self.inp = get_default_pass_input()
        self.dashboard, self.scorecard, self.report = _build_all(self.inp)

    def test_dashboard_not_blocked(self):
        assert self.dashboard.overall_status != RiskStatus.BLOCKED

    def test_scorecard_grade_not_blocked(self):
        assert self.scorecard.grade != RiskDashboardScorecardGrade.BLOCKED

    def test_scorecard_total_score_positive(self):
        assert self.scorecard.total_score > 0

    def test_report_paper_only(self):
        assert self.report.paper_only is True

    def test_report_no_real_orders(self):
        assert self.report.no_real_orders is True

    def test_markdown_non_empty(self):
        assert len(render_markdown(self.report)) > 0

    def test_json_parseable(self):
        parsed = json.loads(render_json(self.report))
        assert isinstance(parsed, dict)

    def test_csv_has_header(self):
        assert "section" in render_csv(self.report)

    def test_console_summary_has_version(self):
        assert "1.7.4" in render_console_summary(self.report)


class TestBlockedInputPipeline:
    def test_no_stop_loss_leads_to_blocked_dashboard(self):
        inp = SmallAccountRiskInput(has_stop_loss=False, position_size_amount=50000)
        dashboard = build_risk_dashboard(inp)
        assert dashboard.overall_status == RiskStatus.BLOCKED

    def test_blocked_dashboard_grade_blocked(self):
        inp = SmallAccountRiskInput(has_stop_loss=False, position_size_amount=50000)
        dashboard = build_risk_dashboard(inp)
        scorecard = compute_scorecard(dashboard)
        assert scorecard.grade == RiskDashboardScorecardGrade.BLOCKED

    def test_blocked_score_zero(self):
        inp = SmallAccountRiskInput(has_stop_loss=False, position_size_amount=50000)
        dashboard = build_risk_dashboard(inp)
        scorecard = compute_scorecard(dashboard)
        assert scorecard.total_score == 0.0

    def test_abc_cascade_to_blocked(self):
        inp = SmallAccountRiskInput(abc_plan_blocked=True)
        dashboard = build_risk_dashboard(inp)
        assert dashboard.overall_status == RiskStatus.BLOCKED

    def test_real_order_always_blocked(self):
        inp = SmallAccountRiskInput(real_order_requested=True)
        dashboard = build_risk_dashboard(inp)
        assert dashboard.overall_status == RiskStatus.BLOCKED

    def test_broker_requested_always_blocked(self):
        inp = SmallAccountRiskInput(broker_requested=True)
        dashboard = build_risk_dashboard(inp)
        assert dashboard.overall_status == RiskStatus.BLOCKED


class TestRegimeVariants:
    def test_bull_pass_input(self):
        inp = SmallAccountRiskInput(
            market_regime="BULL", total_invested_pct=30.0, cash_pct=70.0,
            has_stop_loss=True, stop_loss_pct=0.05,
        )
        dashboard = build_risk_dashboard(inp)
        assert dashboard.overall_status != RiskStatus.BLOCKED

    def test_risk_off_high_cash_pass(self):
        inp = SmallAccountRiskInput(
            market_regime="RISK_OFF", total_invested_pct=30.0, cash_pct=70.0,
            has_stop_loss=True, stop_loss_pct=0.05,
        )
        dashboard = build_risk_dashboard(inp)
        assert dashboard.overall_status != RiskStatus.BLOCKED

    def test_bear_low_invested_pass(self):
        inp = SmallAccountRiskInput(
            market_regime="BEAR", total_invested_pct=20.0, cash_pct=80.0,
            has_stop_loss=True, stop_loss_pct=0.05,
        )
        dashboard = build_risk_dashboard(inp)
        assert dashboard.overall_status != RiskStatus.BLOCKED


class TestReportSections:
    def setup_method(self):
        _, _, self.report = _build_all(get_default_pass_input())

    def test_report_has_17_sections(self):
        assert len(self.report.sections) == 17

    def test_json_has_all_sections(self):
        parsed = json.loads(render_json(self.report))
        assert len(parsed["sections"]) == 17

    def test_json_not_investment_advice(self):
        parsed = json.loads(render_json(self.report))
        assert parsed["not_investment_advice"] is True
