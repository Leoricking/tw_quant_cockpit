"""
tests/test_paper_attribution_scorecard_v167.py
Tests for paper attribution scorecard engine v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from paper_trading.performance_attribution.attribution_scorecard_v167 import (
    AttributionScorecardEngine,
    SCORE_WEIGHTS,
    _grade,
)
from paper_trading.performance_attribution.enums_v167 import (
    ReconciliationStatus,
    DataQualityStatus,
    ConfidenceLevel,
)


def _full_score(
    reconciliation_status=ReconciliationStatus.RECONCILED,
    residual_pct=0.0,
    data_quality=DataQualityStatus.COMPLETE,
    has_execution_data=True,
    execution_simulated=True,
    cost_quality="KNOWN",
    has_benchmark=True,
    benchmark_stale=False,
    has_risk_data=True,
    risk_data_complete=True,
    has_source_lineage=True,
    deterministic=True,
    has_real_markers=False,
    has_credentials=False,
    fixture_only=False,
):
    engine = AttributionScorecardEngine()
    return engine.compute(
        entity_id="test_entity",
        reconciliation_status=reconciliation_status,
        residual_pct=residual_pct,
        data_quality=data_quality,
        has_execution_data=has_execution_data,
        execution_simulated=execution_simulated,
        cost_quality=cost_quality,
        has_benchmark=has_benchmark,
        benchmark_stale=benchmark_stale,
        has_risk_data=has_risk_data,
        risk_data_complete=risk_data_complete,
        has_source_lineage=has_source_lineage,
        deterministic=deterministic,
        has_real_markers=has_real_markers,
        has_credentials=has_credentials,
        fixture_only=fixture_only,
    )


class TestScoreWeights:
    def test_weights_sum_to_100(self):
        assert sum(SCORE_WEIGHTS.values()) == 100

    def test_reconciliation_is_highest(self):
        assert SCORE_WEIGHTS["reconciliation_quality"] == 25

    def test_data_completeness_second(self):
        assert SCORE_WEIGHTS["data_completeness"] == 20

    def test_execution_quality_third(self):
        assert SCORE_WEIGHTS["execution_data_quality"] == 15

    def test_all_weights_positive(self):
        for k, v in SCORE_WEIGHTS.items():
            assert v > 0, f"Weight for {k} is {v}"


class TestGradeFunction:
    def test_90_plus_is_a(self):
        assert _grade(95.0) == "A"

    def test_80_plus_is_b(self):
        assert _grade(85.0) == "B"

    def test_70_plus_is_c(self):
        assert _grade(75.0) == "C"

    def test_60_plus_is_d(self):
        assert _grade(65.0) == "D"

    def test_below_60_is_f(self):
        assert _grade(55.0) == "F"

    def test_exactly_90_is_a(self):
        assert _grade(90.0) == "A"

    def test_exactly_80_is_b(self):
        assert _grade(80.0) == "B"

    def test_zero_is_f(self):
        assert _grade(0.0) == "F"


class TestRealMarkersBlocking:
    def test_real_markers_score_zero(self):
        sc = _full_score(has_real_markers=True)
        assert sc.total_score == 0.0

    def test_real_markers_grade_f(self):
        sc = _full_score(has_real_markers=True)
        assert sc.grade == "F"

    def test_real_markers_not_usable(self):
        sc = _full_score(has_real_markers=True)
        assert sc.usable_for_research is False
        assert sc.usable_for_paper_review is False

    def test_credentials_score_zero(self):
        sc = _full_score(has_credentials=True)
        assert sc.total_score == 0.0

    def test_credentials_grade_f(self):
        sc = _full_score(has_credentials=True)
        assert sc.grade == "F"

    def test_real_markers_blocking_issues(self):
        sc = _full_score(has_real_markers=True)
        assert len(sc.blocking_issues) > 0

    def test_not_for_real_trading_always_true(self):
        sc = _full_score(has_real_markers=True)
        assert sc.not_for_real_trading is True


class TestHighScore:
    def test_all_complete_score_above_80(self):
        sc = _full_score()
        assert sc.total_score > 80.0

    def test_all_complete_grade_a_or_b(self):
        sc = _full_score()
        assert sc.grade in ("A", "B")

    def test_all_complete_confidence_high(self):
        sc = _full_score()
        assert sc.confidence == ConfidenceLevel.HIGH

    def test_all_complete_usable_for_research(self):
        sc = _full_score()
        assert sc.usable_for_research is True

    def test_all_complete_usable_for_paper_review(self):
        sc = _full_score()
        assert sc.usable_for_paper_review is True


class TestFixturePenalty:
    def test_fixture_score_less_than_full(self):
        sc_full = _full_score()
        sc_fix = _full_score(fixture_only=True)
        assert sc_fix.total_score < sc_full.total_score

    def test_fixture_score_below_100(self):
        sc = _full_score(fixture_only=True)
        assert sc.total_score < 100.0

    def test_fixture_warning_in_warnings(self):
        sc = _full_score(fixture_only=True)
        assert any("fixture" in w.lower() for w in sc.warnings)


class TestBenchmarkPenalty:
    def test_missing_benchmark_reduces_score(self):
        sc_with = _full_score(has_benchmark=True)
        sc_without = _full_score(has_benchmark=False)
        assert sc_without.total_score < sc_with.total_score

    def test_missing_benchmark_warning(self):
        sc = _full_score(has_benchmark=False)
        assert any("benchmark" in w.lower() for w in sc.warnings)

    def test_stale_benchmark_reduces_score(self):
        sc_fresh = _full_score(has_benchmark=True, benchmark_stale=False)
        sc_stale = _full_score(has_benchmark=True, benchmark_stale=True)
        assert sc_stale.total_score < sc_fresh.total_score


class TestDataQualityScoring:
    def test_partial_data_lower_score(self):
        sc_complete = _full_score(data_quality=DataQualityStatus.COMPLETE)
        sc_partial  = _full_score(data_quality=DataQualityStatus.PARTIAL)
        assert sc_partial.total_score < sc_complete.total_score

    def test_insufficient_data_lower_than_complete(self):
        sc_complete = _full_score(data_quality=DataQualityStatus.COMPLETE)
        sc_insuf = _full_score(data_quality=DataQualityStatus.INSUFFICIENT)
        assert sc_insuf.total_score <= sc_complete.total_score


class TestReconciliationScoring:
    def test_failed_reconciliation_lowers_score(self):
        sc_ok   = _full_score(reconciliation_status=ReconciliationStatus.RECONCILED)
        sc_fail = _full_score(reconciliation_status=ReconciliationStatus.FAILED)
        assert sc_fail.total_score < sc_ok.total_score

    def test_large_residual_penalizes(self):
        sc_ok    = _full_score(residual_pct=0.0)
        sc_large = _full_score(residual_pct=0.05)
        assert sc_large.total_score <= sc_ok.total_score

    def test_large_residual_warning(self):
        sc = _full_score(residual_pct=0.05)
        assert any("residual" in w.lower() for w in sc.warnings)


class TestExecutionScoring:
    def test_no_execution_data_warning(self):
        sc = _full_score(has_execution_data=False)
        assert any("execution" in w.lower() for w in sc.warnings)

    def test_not_simulated_blocking(self):
        sc = _full_score(has_execution_data=True, execution_simulated=False)
        assert len(sc.blocking_issues) > 0


class TestCostScoring:
    def test_unknown_cost_warning(self):
        sc = _full_score(cost_quality="UNKNOWN")
        assert any("cost" in w.lower() for w in sc.warnings)

    def test_estimated_cost_lower_than_known(self):
        sc_known = _full_score(cost_quality="KNOWN")
        sc_est   = _full_score(cost_quality="ESTIMATED")
        assert sc_est.total_score <= sc_known.total_score


class TestScorecardSafetyFlags:
    def test_paper_only_always_true(self):
        sc = _full_score()
        assert sc.paper_only is True

    def test_research_only_always_true(self):
        sc = _full_score()
        assert sc.research_only is True

    def test_no_real_orders_always_true(self):
        sc = _full_score()
        assert sc.no_real_orders is True

    def test_not_for_production_always_true(self):
        sc = _full_score()
        assert sc.not_for_production is True

    def test_not_for_real_trading_always_true(self):
        sc = _full_score()
        assert sc.not_for_real_trading is True


class TestDeterminism:
    def test_non_deterministic_attribution_blocking(self):
        sc = _full_score(deterministic=False)
        assert len(sc.blocking_issues) > 0

    def test_deterministic_no_blocking_from_determinism(self):
        sc = _full_score(deterministic=True)
        det_blocks = [b for b in sc.blocking_issues if "deterministic" in b.lower()]
        assert len(det_blocks) == 0


class TestComponentScores:
    def test_component_scores_dict_present(self):
        sc = _full_score()
        assert isinstance(sc.component_scores, dict)

    def test_all_weight_keys_present(self):
        sc = _full_score()
        for key in SCORE_WEIGHTS:
            assert key in sc.component_scores

    def test_failed_dimensions_subset_of_weights(self):
        sc = _full_score()
        for dim in sc.failed_dimensions:
            assert dim in SCORE_WEIGHTS
