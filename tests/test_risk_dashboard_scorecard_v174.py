"""
tests/test_risk_dashboard_scorecard_v174.py
Tests for risk dashboard scorecard v1.7.4.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
import pytest
from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskInput
from paper_trading.small_capital_strategy.risk_dashboard_enums_v174 import RiskStatus, RiskDashboardScorecardGrade
from paper_trading.small_capital_strategy.risk_dashboard_scorecard_v174 import (
    compute_scorecard, get_weight_table, WEIGHTS_SUM, GRADE_A_MIN, GRADE_B_MIN,
)
from paper_trading.small_capital_strategy.small_capital_risk_adapter_v174 import (
    build_risk_dashboard, get_default_pass_input,
)


class TestWeights:
    def test_weights_sum_100(self):
        assert WEIGHTS_SUM == 100

    def test_grade_a_min_85(self):
        assert GRADE_A_MIN == 85.0

    def test_grade_b_min_70(self):
        assert GRADE_B_MIN == 70.0

    def test_weight_table_total_100(self):
        assert get_weight_table()["total"] == 100

    def test_weight_table_has_single_trade(self):
        assert "single_trade_risk_compliance" in get_weight_table()

    def test_weight_table_has_safety(self):
        assert "safety_compliance" in get_weight_table()


class TestPassInputScorecard:
    def setup_method(self):
        self.dashboard = build_risk_dashboard(get_default_pass_input())
        self.scorecard = compute_scorecard(self.dashboard)

    def test_overall_not_blocked(self):
        assert self.dashboard.overall_status != RiskStatus.BLOCKED

    def test_total_score_positive(self):
        assert self.scorecard.total_score > 0

    def test_total_score_le_100(self):
        assert self.scorecard.total_score <= 100.0

    def test_grade_not_blocked(self):
        assert self.scorecard.grade != RiskDashboardScorecardGrade.BLOCKED

    def test_no_aplus(self):
        assert self.scorecard.grade.value != "A+"

    def test_paper_only(self):
        assert self.scorecard.paper_only is True

    def test_weights_sum_100(self):
        assert self.scorecard.weights_sum == 100

    def test_not_investment_advice(self):
        assert self.scorecard.not_investment_advice is True


class TestBlockedInputScorecard:
    def test_blocked_dashboard_grade_blocked(self):
        from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskDashboard
        dashboard = SmallAccountRiskDashboard(overall_status=RiskStatus.BLOCKED)
        scorecard = compute_scorecard(dashboard)
        assert scorecard.grade == RiskDashboardScorecardGrade.BLOCKED

    def test_blocked_score_zero(self):
        from paper_trading.small_capital_strategy.risk_dashboard_models_v174 import SmallAccountRiskDashboard
        dashboard = SmallAccountRiskDashboard(overall_status=RiskStatus.BLOCKED)
        scorecard = compute_scorecard(dashboard)
        assert scorecard.total_score == 0.0


class TestGradeRanges:
    def test_grade_a_requires_85_plus(self):
        assert GRADE_A_MIN == 85.0

    def test_grade_b_requires_70_plus(self):
        assert GRADE_B_MIN == 70.0

    def test_grade_values_valid(self):
        valid = {"A", "B", "C", "D", "F", "BLOCKED"}
        assert RiskDashboardScorecardGrade.A.value in valid
        assert RiskDashboardScorecardGrade.BLOCKED.value in valid
