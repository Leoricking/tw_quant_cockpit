"""
tests/test_operational_integration_scorecard_v168.py — Integration Scorecard tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.integration_scorecard_v168 import (
    IntegrationScorecard, _WEIGHTS, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.models_v168 import IntegrationScore


class TestScorecardSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestIntegrationScorecardCore:
    def setup_method(self):
        self.scorecard = IntegrationScorecard()

    def test_weights_sum_to_100(self):
        assert sum(_WEIGHTS.values()) == 100

    def test_weights_is_dict(self):
        assert isinstance(_WEIGHTS, dict)
        assert len(_WEIGHTS) > 0

    def test_weights_has_contract(self):
        assert "contract" in _WEIGHTS

    def test_weights_has_safety(self):
        assert "safety" in _WEIGHTS

    def test_compute_returns_score(self):
        result = self.scorecard.compute({})
        assert isinstance(result, IntegrationScore)

    def test_compute_perfect_score(self):
        run_result = {
            "run_id": "R001",
            "contract_score": 100.0,
            "data_flow_score": 100.0,
            "lineage_score": 100.0,
            "identity_score": 100.0,
            "timestamp_score": 100.0,
            "reconciliation_score": 100.0,
            "determinism_score": 100.0,
            "failure_isolation_score": 100.0,
            "safety_score": 100.0,
        }
        result = self.scorecard.compute(run_result)
        assert abs(result.total_score - 100.0) < 1e-6

    def test_compute_perfect_grade_a(self):
        run_result = {
            "run_id": "R001",
            "contract_score": 100.0, "data_flow_score": 100.0,
            "lineage_score": 100.0, "identity_score": 100.0,
            "timestamp_score": 100.0, "reconciliation_score": 100.0,
            "determinism_score": 100.0, "failure_isolation_score": 100.0,
            "safety_score": 100.0,
        }
        result = self.scorecard.compute(run_result)
        assert result.grade == "A"

    def test_compute_not_for_real_trading(self):
        result = self.scorecard.compute({})
        assert result.not_for_real_trading is True

    def test_compute_paper_only(self):
        result = self.scorecard.compute({})
        assert result.paper_only is True

    def test_compute_empty_run_result(self):
        result = self.scorecard.compute({})
        assert isinstance(result.total_score, float)

    def test_get_grade_a(self):
        assert self.scorecard.get_grade(90.0) == "A"
        assert self.scorecard.get_grade(100.0) == "A"

    def test_get_grade_b(self):
        assert self.scorecard.get_grade(80.0) == "B"
        assert self.scorecard.get_grade(89.9) == "B"

    def test_get_grade_c(self):
        grade = self.scorecard.get_grade(70.0)
        assert grade in ("B", "C")

    def test_get_grade_f(self):
        assert self.scorecard.get_grade(0.0) == "F"

    def test_summarize_returns_dict(self):
        score = self.scorecard.compute({"run_id": "R001"})
        summary = self.scorecard.summarize(score)
        assert isinstance(summary, dict)

    def test_summarize_paper_only(self):
        score = self.scorecard.compute({})
        summary = self.scorecard.summarize(score)
        assert summary.get("paper_only") is True

    def test_safety_blocking_zero_score(self):
        run_result = {
            "run_id": "R001",
            "contract_score": 100.0,
            "safety_violations": ["broker_enabled"],
        }
        result = self.scorecard.compute(run_result)
        assert result.total_score == 0.0
        assert result.grade == "F"

    def test_compute_run_id_stored(self):
        result = self.scorecard.compute({"run_id": "MY_RUN_001"})
        assert result.run_id == "MY_RUN_001"

    def test_compute_score_bounded_0_to_100(self):
        run_result = {
            "contract_score": 200.0,  # out of range
            "data_flow_score": -50.0,  # out of range
        }
        result = self.scorecard.compute(run_result)
        assert 0.0 <= result.total_score <= 100.0

    def test_usable_for_research_high_score(self):
        run_result = {
            "contract_score": 100.0, "data_flow_score": 100.0,
            "lineage_score": 100.0, "identity_score": 100.0,
            "timestamp_score": 100.0, "reconciliation_score": 100.0,
            "determinism_score": 100.0, "failure_isolation_score": 100.0,
            "safety_score": 100.0,
        }
        result = self.scorecard.compute(run_result)
        assert result.usable_for_research is True
