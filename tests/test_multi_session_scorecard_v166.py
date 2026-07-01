"""
test_multi_session_scorecard_v166.py — Scorecard tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


class TestScorecardWeights:
    def test_weights_sum_to_100(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert sum(SCORECARD_WEIGHTS.values()) == 100

    def test_weights_has_12_dimensions(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert len(SCORECARD_WEIGHTS) == 12

    def test_all_weights_positive(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert all(w > 0 for w in SCORECARD_WEIGHTS.values())

    def test_registration_integrity_present(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert "registration_integrity" in SCORECARD_WEIGHTS

    def test_resource_coordination_present(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert "resource_coordination" in SCORECARD_WEIGHTS

    def test_conflict_detection_present(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert "conflict_detection" in SCORECARD_WEIGHTS

    def test_fairness_present(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert "fairness" in SCORECARD_WEIGHTS

    def test_event_ordering_present(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert "event_ordering" in SCORECARD_WEIGHTS

    def test_data_isolation_present(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert "data_isolation" in SCORECARD_WEIGHTS

    def test_risk_coordination_present(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert "risk_coordination" in SCORECARD_WEIGHTS

    def test_replay_reproducibility_present(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert "replay_reproducibility" in SCORECARD_WEIGHTS

    def test_lifecycle_safety_present(self):
        from paper_trading.multi_session.scorecard_v166 import SCORECARD_WEIGHTS
        assert "lifecycle_safety" in SCORECARD_WEIGHTS


class TestMultiSessionScorecard:
    def test_instantiation(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        assert sc is not None

    def test_compute_returns_scorecard_result(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard, ScorecardResult
        sc = MultiSessionScorecard()
        result = sc.compute({})
        assert isinstance(result, ScorecardResult)

    def test_compute_all_pass(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard, SCORECARD_WEIGHTS
        sc = MultiSessionScorecard()
        all_pass = {dim: True for dim in SCORECARD_WEIGHTS}
        result = sc.compute(all_pass)
        assert result.total_score == 100

    def test_compute_all_unknown_scores_zero(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        result = sc.compute({})
        assert result.total_score == 0

    def test_blocking_failure_caps_score_at_60(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard, SCORECARD_WEIGHTS
        sc = MultiSessionScorecard()
        # Pass most dimensions but fail one
        dims = {dim: True for dim in SCORECARD_WEIGHTS}
        dims["data_isolation"] = False  # Blocking failure
        result = sc.compute(dims)
        assert result.total_score <= 60
        assert result.capped is True

    def test_unknown_dimension_scores_zero(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        result = sc.compute({"unknown_dim": "weird_value"})
        # unknown_dim is not in SCORECARD_WEIGHTS so ignored
        assert result.total_score == 0

    def test_warn_gives_partial_credit(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        result = sc.compute({"fairness": "WARN"})
        # fairness weight is 8, WARN gives 8 * 0.7 = 5.6
        assert result.dimension_scores["fairness"] > 0
        assert result.dimension_scores["fairness"] < 8

    def test_score_between_0_and_100(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard, SCORECARD_WEIGHTS
        sc = MultiSessionScorecard()
        dims = {dim: "WARN" for dim in SCORECARD_WEIGHTS}
        result = sc.compute(dims)
        assert 0 <= result.total_score <= 100

    def test_blocking_failures_list_populated(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        result = sc.compute({"data_isolation": False})
        assert "data_isolation" in result.blocking_failures

    def test_is_blocking_with_failures(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        result = sc.compute({"risk_coordination": False})
        assert result.is_blocking() is True

    def test_is_not_blocking_all_pass(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard, SCORECARD_WEIGHTS
        sc = MultiSessionScorecard()
        all_pass = {dim: True for dim in SCORECARD_WEIGHTS}
        result = sc.compute(all_pass)
        assert result.is_blocking() is False

    def test_explanation_dict_populated(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        result = sc.compute({"fairness": True})
        assert isinstance(result.explanation, dict)

    def test_no_auto_production_action_flag(self):
        import paper_trading.multi_session.scorecard_v166 as m
        assert m.NO_AUTO_PRODUCTION_ACTION is True

    def test_partial_score_with_numeric_result(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        result = sc.compute({"fairness": 5})
        assert result.dimension_scores["fairness"] == 5.0

    def test_unknown_dimensions_list_populated(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        result = sc.compute({})
        assert len(result.unknown_dimensions) == 12

    def test_score_result_has_dimension_scores_dict(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        result = sc.compute({})
        assert isinstance(result.dimension_scores, dict)

    def test_capped_false_when_no_blocking_failures(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard, SCORECARD_WEIGHTS
        sc = MultiSessionScorecard()
        all_pass = {dim: True for dim in SCORECARD_WEIGHTS}
        result = sc.compute(all_pass)
        assert result.capped is False

    def test_multiple_blocking_failures(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        result = sc.compute({"data_isolation": False, "risk_coordination": False})
        assert len(result.blocking_failures) == 2
        assert result.total_score <= 60

    def test_fail_string_treated_as_blocking(self):
        from paper_trading.multi_session.scorecard_v166 import MultiSessionScorecard
        sc = MultiSessionScorecard()
        result = sc.compute({"fairness": "FAIL"})
        assert "fairness" in result.blocking_failures
