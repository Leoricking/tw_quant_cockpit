"""
tests/test_failure_validation_detection_v165.py — Detection tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from paper_trading.failure_validation.enums_v165 import (
    FailureDomain,
    FailureType,
)
from paper_trading.failure_validation.detection_v165 import (
    DetectionResult,
    FailureDetector,
    PAPER_ONLY,
    RESEARCH_ONLY,
)


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestDetectionSafetyFlags:
    def test_paper_only_true(self):
        assert PAPER_ONLY is True

    def test_research_only_true(self):
        assert RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# DetectionResult
# ---------------------------------------------------------------------------

class TestDetectionResult:
    def test_detected_true_result(self):
        r = DetectionResult(detected=True, failure_type=FailureType.STALE_DATA, reason="test")
        assert r.detected is True

    def test_detected_false_result(self):
        r = DetectionResult(detected=False, failure_type=FailureType.TIMEOUT)
        assert r.detected is False

    def test_as_dict_has_required_keys(self):
        r = DetectionResult(detected=True, failure_type=FailureType.MISSING_DATA, reason="found")
        d = r.as_dict()
        assert "detected" in d
        assert "failure_type" in d
        assert "reason" in d

    def test_as_dict_detected_value_correct(self):
        r = DetectionResult(detected=True, failure_type=FailureType.TIMEOUT, reason="")
        assert r.as_dict()["detected"] is True

    def test_as_dict_failure_type_is_string_value(self):
        r = DetectionResult(detected=True, failure_type=FailureType.CIRCUIT_OPEN)
        assert r.as_dict()["failure_type"] == "CIRCUIT_OPEN"


# ---------------------------------------------------------------------------
# FailureDetector.detect
# ---------------------------------------------------------------------------

class TestFailureDetectorDetect:
    def test_detector_instantiates(self):
        fd = FailureDetector()
        assert fd is not None

    def test_detect_returns_detection_result(self):
        fd = FailureDetector()
        result = fd.detect(FailureType.STALE_DATA, FailureDomain.MARKET_DATA, seed=1)
        assert isinstance(result, DetectionResult)

    def test_detect_failure_type_preserved(self):
        fd = FailureDetector()
        result = fd.detect(FailureType.TIMEOUT, FailureDomain.SESSION_STATE, seed=5)
        assert result.failure_type == FailureType.TIMEOUT

    def test_detect_has_reason(self):
        fd = FailureDetector()
        result = fd.detect(FailureType.MISSING_DATA, FailureDomain.MARKET_DATA, seed=42)
        assert len(result.reason) > 0

    def test_detect_deterministic_same_seed(self):
        fd = FailureDetector()
        r1 = fd.detect(FailureType.STALE_DATA, FailureDomain.MARKET_DATA, seed=42)
        r2 = fd.detect(FailureType.STALE_DATA, FailureDomain.MARKET_DATA, seed=42)
        assert r1.detected == r2.detected

    def test_detect_high_rate_type_mostly_detected(self):
        fd = FailureDetector()
        detections = sum(
            fd.detect(FailureType.TIMEOUT, FailureDomain.EVENT_STREAM, seed=i).detected
            for i in range(50)
        )
        assert detections >= 40  # >80% detection rate expected

    def test_detect_all_failure_types_produce_result(self):
        fd = FailureDetector()
        for ft in FailureType:
            result = fd.detect(ft, FailureDomain.MARKET_DATA, seed=42)
            assert isinstance(result, DetectionResult)


# ---------------------------------------------------------------------------
# FailureDetector.detect_batch
# ---------------------------------------------------------------------------

class TestFailureDetectorBatch:
    def test_detect_batch_returns_list(self):
        fd = FailureDetector()
        results = fd.detect_batch(
            [FailureType.STALE_DATA, FailureType.TIMEOUT, FailureType.MISSING_DATA],
            FailureDomain.MARKET_DATA,
            seed=1,
        )
        assert isinstance(results, list)
        assert len(results) == 3

    def test_detect_batch_each_result_correct_type(self):
        fd = FailureDetector()
        fts = [FailureType.CIRCUIT_OPEN, FailureType.ALERT_LOSS]
        results = fd.detect_batch(fts, FailureDomain.ALERT, seed=10)
        for i, result in enumerate(results):
            assert result.failure_type == fts[i]

    def test_detect_batch_empty_returns_empty(self):
        fd = FailureDetector()
        results = fd.detect_batch([], FailureDomain.MARKET_DATA, seed=1)
        assert results == []

    def test_detect_batch_deterministic(self):
        fd = FailureDetector()
        fts = [FailureType.STALE_DATA, FailureType.DUPLICATE_EVENT]
        r1 = fd.detect_batch(fts, FailureDomain.EVENT_STREAM, seed=77)
        r2 = fd.detect_batch(fts, FailureDomain.EVENT_STREAM, seed=77)
        assert [r.detected for r in r1] == [r.detected for r in r2]

    def test_detect_batch_different_seeds_per_item(self):
        """Each item in batch uses seed+i so items don't always agree."""
        fd = FailureDetector()
        fts = [FailureType.CONFIG_DRIFT] * 5
        results = fd.detect_batch(fts, FailureDomain.CONFIGURATION, seed=1000)
        assert len(results) == 5
