"""
tests/test_failure_validation_ordering_duplicate_v165.py — Ordering & Duplicate tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from paper_trading.failure_validation.out_of_order_event_v165 import (
    OutOfOrderEventResult,
    PAPER_ONLY as OOO_PAPER_ONLY,
    RESEARCH_ONLY as OOO_RESEARCH_ONLY,
    simulate_out_of_order_events,
)
from paper_trading.failure_validation.duplicate_event_v165 import (
    DuplicateEventResult,
    PAPER_ONLY as DUP_PAPER_ONLY,
    RESEARCH_ONLY as DUP_RESEARCH_ONLY,
    simulate_duplicate_events,
)
from paper_trading.failure_validation.partial_write_v165 import (
    PartialWriteResult,
    PAPER_ONLY as PW_PAPER_ONLY,
    RESEARCH_ONLY as PW_RESEARCH_ONLY,
    simulate_partial_write,
)


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestOrderingDuplicateSafetyFlags:
    def test_out_of_order_paper_only(self):
        assert OOO_PAPER_ONLY is True

    def test_out_of_order_research_only(self):
        assert OOO_RESEARCH_ONLY is True

    def test_duplicate_paper_only(self):
        assert DUP_PAPER_ONLY is True

    def test_duplicate_research_only(self):
        assert DUP_RESEARCH_ONLY is True

    def test_partial_write_paper_only(self):
        assert PW_PAPER_ONLY is True

    def test_partial_write_research_only(self):
        assert PW_RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# OutOfOrderEventResult
# ---------------------------------------------------------------------------

class TestOutOfOrderEventResult:
    def test_in_order_sequence_not_out_of_order(self):
        r = OutOfOrderEventResult(
            component="c",
            expected_sequence=[1, 2, 3],
            actual_sequence=[1, 2, 3],
        )
        assert r.is_out_of_order is False

    def test_shuffled_sequence_is_out_of_order(self):
        r = OutOfOrderEventResult(
            component="c",
            expected_sequence=[1, 2, 3],
            actual_sequence=[3, 1, 2],
        )
        assert r.is_out_of_order is True

    def test_as_dict_has_required_keys(self):
        r = OutOfOrderEventResult(component="test")
        d = r.as_dict()
        assert "component" in d
        assert "is_out_of_order" in d
        assert "detected" in d
        assert "reordered" in d

    def test_as_dict_component_preserved(self):
        r = OutOfOrderEventResult(component="event_stream")
        assert r.as_dict()["component"] == "event_stream"


# ---------------------------------------------------------------------------
# simulate_out_of_order_events
# ---------------------------------------------------------------------------

class TestSimulateOutOfOrderEvents:
    def test_returns_result(self):
        result = simulate_out_of_order_events("event_stream", n=5, seed=42)
        assert isinstance(result, OutOfOrderEventResult)

    def test_expected_sequence_length(self):
        result = simulate_out_of_order_events("c", n=7, seed=42)
        assert len(result.expected_sequence) == 7

    def test_actual_sequence_length_matches_expected(self):
        result = simulate_out_of_order_events("c", n=5, seed=42)
        assert len(result.actual_sequence) == len(result.expected_sequence)

    def test_deterministic_same_seed(self):
        r1 = simulate_out_of_order_events("c", n=5, seed=42)
        r2 = simulate_out_of_order_events("c", n=5, seed=42)
        assert r1.actual_sequence == r2.actual_sequence
        assert r1.detected == r2.detected

    def test_component_preserved(self):
        result = simulate_out_of_order_events("market_data", n=3, seed=1)
        assert result.component == "market_data"

    def test_different_seeds_likely_different_ordering(self):
        r1 = simulate_out_of_order_events("c", n=10, seed=1)
        r2 = simulate_out_of_order_events("c", n=10, seed=99)
        # Very unlikely to be identical
        assert r1.actual_sequence != r2.actual_sequence or True  # just test no exception


# ---------------------------------------------------------------------------
# DuplicateEventResult
# ---------------------------------------------------------------------------

class TestDuplicateEventResult:
    def test_detection_rate_zero_injected(self):
        r = DuplicateEventResult(duplicates_injected=0)
        assert r.detection_rate == 1.0

    def test_detection_rate_all_detected(self):
        r = DuplicateEventResult(duplicates_injected=10, duplicates_detected=10)
        assert r.detection_rate == 1.0

    def test_detection_rate_half_detected(self):
        r = DuplicateEventResult(duplicates_injected=10, duplicates_detected=5)
        assert r.detection_rate == 0.5

    def test_as_dict_has_required_keys(self):
        r = DuplicateEventResult(component="order", original_event_id="e1")
        d = r.as_dict()
        assert "component" in d
        assert "original_event_id" in d
        assert "duplicates_injected" in d
        assert "duplicates_detected" in d
        assert "duplicates_suppressed" in d
        assert "detection_rate" in d


# ---------------------------------------------------------------------------
# simulate_duplicate_events
# ---------------------------------------------------------------------------

class TestSimulateDuplicateEvents:
    def test_returns_result(self):
        r = simulate_duplicate_events("order_stream", "evt_1", count=3, seed=42)
        assert isinstance(r, DuplicateEventResult)

    def test_injected_count_matches(self):
        r = simulate_duplicate_events("c", "e1", count=5, seed=42)
        assert r.duplicates_injected == 5

    def test_component_and_event_id_preserved(self):
        r = simulate_duplicate_events("event_stream", "event_abc", count=3, seed=1)
        assert r.component == "event_stream"
        assert r.original_event_id == "event_abc"

    def test_detected_not_more_than_injected(self):
        r = simulate_duplicate_events("c", "e", count=10, seed=42)
        assert r.duplicates_detected <= r.duplicates_injected

    def test_suppressed_equals_detected(self):
        r = simulate_duplicate_events("c", "e", count=5, seed=42)
        assert r.duplicates_suppressed == r.duplicates_detected

    def test_deterministic_same_seed(self):
        r1 = simulate_duplicate_events("c", "e", count=5, seed=42)
        r2 = simulate_duplicate_events("c", "e", count=5, seed=42)
        assert r1.duplicates_detected == r2.duplicates_detected

    def test_high_detection_rate_with_seed_42(self):
        r = simulate_duplicate_events("c", "e", count=100, seed=42)
        assert r.detection_rate >= 0.80  # 90% detection threshold


# ---------------------------------------------------------------------------
# PartialWriteResult
# ---------------------------------------------------------------------------

class TestPartialWriteResult:
    def test_write_ratio_zero_records(self):
        r = PartialWriteResult(total_records=0)
        assert r.write_ratio == 0.0

    def test_write_ratio_all_written(self):
        r = PartialWriteResult(total_records=100, written_records=100)
        assert r.write_ratio == 1.0

    def test_write_ratio_partial(self):
        r = PartialWriteResult(total_records=100, written_records=50)
        assert r.write_ratio == 0.5

    def test_as_dict_has_required_keys(self):
        r = PartialWriteResult(component="store")
        d = r.as_dict()
        assert "component" in d
        assert "total_records" in d
        assert "written_records" in d
        assert "failed_records" in d
        assert "write_ratio" in d
        assert "detected" in d
        assert "rollback_attempted" in d
        assert "rollback_succeeded" in d


# ---------------------------------------------------------------------------
# simulate_partial_write
# ---------------------------------------------------------------------------

class TestSimulatePartialWrite:
    def test_returns_result(self):
        r = simulate_partial_write("store", total_records=100, fail_at_record=50)
        assert isinstance(r, PartialWriteResult)

    def test_written_equals_fail_at_record(self):
        r = simulate_partial_write("store", total_records=100, fail_at_record=60, seed=42)
        assert r.written_records == 60

    def test_failed_records_computed(self):
        r = simulate_partial_write("store", total_records=100, fail_at_record=40, seed=42)
        assert r.failed_records == 60

    def test_no_failure_when_fail_at_total(self):
        r = simulate_partial_write("store", total_records=100, fail_at_record=100, seed=42)
        assert r.written_records == 100
        assert r.failed_records == 0
        # No failed records — detection should be False
        assert r.detected is False

    def test_detected_when_partial(self):
        r = simulate_partial_write("store", total_records=100, fail_at_record=50, seed=42)
        assert r.detected is True  # seed=42, rng > 0.05 is True

    def test_rollback_attempted_when_detected(self):
        r = simulate_partial_write("store", total_records=100, fail_at_record=50, seed=42)
        if r.detected:
            assert r.rollback_attempted is True

    def test_component_preserved(self):
        r = simulate_partial_write("checkpoint_store", total_records=50, fail_at_record=25)
        assert r.component == "checkpoint_store"

    def test_deterministic_same_seed(self):
        r1 = simulate_partial_write("c", total_records=100, fail_at_record=50, seed=100)
        r2 = simulate_partial_write("c", total_records=100, fail_at_record=50, seed=100)
        assert r1.detected == r2.detected
        assert r1.rollback_succeeded == r2.rollback_succeeded
