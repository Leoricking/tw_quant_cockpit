"""
test_multi_session_fairness_engine_v166.py — Fairness Engine tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


def _engine():
    from paper_trading.multi_session.fairness_engine_v166 import FairnessEngine
    return FairnessEngine()


class TestFairnessEngine:
    def test_instantiation(self):
        e = _engine()
        assert e is not None

    def test_record_grant_increments_grant_count(self):
        e = _engine()
        e.record_grant("s1")
        rec = e.get_record("s1")
        assert rec.grant_count == 1

    def test_record_grant_twice(self):
        e = _engine()
        e.record_grant("s1")
        e.record_grant("s1")
        rec = e.get_record("s1")
        assert rec.grant_count == 2

    def test_record_denial_increments_denial_count(self):
        e = _engine()
        e.record_denial("s1")
        rec = e.get_record("s1")
        assert rec.denial_count == 1

    def test_record_denial_increments_wait_rounds(self):
        e = _engine()
        e.record_denial("s1")
        e.record_denial("s1")
        rec = e.get_record("s1")
        assert rec.wait_rounds == 2

    def test_record_grant_resets_wait_rounds(self):
        e = _engine()
        e.record_denial("s1")
        e.record_denial("s1")
        e.record_grant("s1")
        rec = e.get_record("s1")
        assert rec.wait_rounds == 0

    def test_record_grant_resets_denial_count(self):
        e = _engine()
        e.record_denial("s1")
        e.record_grant("s1")
        rec = e.get_record("s1")
        assert rec.denial_count == 0

    def test_compute_aging_bonus_returns_nonnegative(self):
        e = _engine()
        bonus = e.compute_aging_bonus("s1")
        assert isinstance(bonus, float)
        assert bonus >= 0.0

    def test_compute_aging_bonus_increases_with_denials(self):
        e = _engine()
        e.record_denial("s1")
        e.record_denial("s1")
        bonus = e.compute_aging_bonus("s1")
        assert bonus > 0.0

    def test_compute_aging_bonus_proportional_to_wait_rounds(self):
        e = _engine()
        for _ in range(5):
            e.record_denial("s1")
        bonus_5 = e.compute_aging_bonus("s1")
        e2 = _engine()
        for _ in range(10):
            e2.record_denial("s1")
        bonus_10 = e2.compute_aging_bonus("s1")
        assert bonus_10 > bonus_5

    def test_detect_starvation_returns_list(self):
        e = _engine()
        result = e.detect_starvation()
        assert isinstance(result, list)

    def test_detect_starvation_empty_initially(self):
        e = _engine()
        result = e.detect_starvation()
        assert result == []

    def test_detect_starvation_after_threshold(self):
        e = _engine()
        for _ in range(FairnessEngine_THRESHOLD()):
            e.record_denial("s_starved")
        result = e.detect_starvation()
        assert "s_starved" in result

    def test_detect_starvation_not_triggered_below_threshold(self):
        e = _engine()
        threshold = FairnessEngine_THRESHOLD()
        for _ in range(threshold - 1):
            e.record_denial("s_below")
        result = e.detect_starvation()
        assert "s_below" not in result

    def test_fairness_summary_returns_dict(self):
        e = _engine()
        e.record_grant("s1")
        e.record_denial("s2")
        summary = e.fairness_summary()
        assert isinstance(summary, dict)

    def test_fairness_summary_contains_session_info(self):
        e = _engine()
        e.record_grant("s1")
        summary = e.fairness_summary()
        assert "s1" in summary

    def test_fairness_summary_grants_field(self):
        e = _engine()
        e.record_grant("s1")
        e.record_grant("s1")
        summary = e.fairness_summary()
        assert summary["s1"]["grants"] == 2

    def test_fairness_summary_denials_field(self):
        e = _engine()
        e.record_denial("s1")
        e.record_denial("s1")
        summary = e.fairness_summary()
        assert summary["s1"]["denials"] == 2

    def test_starvation_flag_set_after_threshold(self):
        e = _engine()
        threshold = FairnessEngine_THRESHOLD()
        for _ in range(threshold):
            e.record_denial("s_flag")
        rec = e.get_record("s_flag")
        assert rec.starvation_flag is True

    def test_starvation_flag_cleared_after_grant(self):
        e = _engine()
        threshold = FairnessEngine_THRESHOLD()
        for _ in range(threshold):
            e.record_denial("s_clear")
        e.record_grant("s_clear")
        rec = e.get_record("s_clear")
        assert rec.starvation_flag is False

    def test_starvation_threshold_constant_exists(self):
        from paper_trading.multi_session.fairness_engine_v166 import FairnessEngine
        assert hasattr(FairnessEngine, "STARVATION_THRESHOLD")
        assert FairnessEngine.STARVATION_THRESHOLD > 0

    def test_starvation_detector_starvation_threshold_constant(self):
        from paper_trading.multi_session.starvation_detector_v166 import StarvationDetector
        assert hasattr(StarvationDetector, "STARVATION_THRESHOLD")
        assert StarvationDetector.STARVATION_THRESHOLD > 0

    def test_no_infinite_starvation_flag(self):
        import paper_trading.multi_session.fairness_engine_v166 as m
        assert m.NO_INFINITE_STARVATION is True

    def test_max_consecutive_grants_exceeded_returns_bool(self):
        e = _engine()
        for _ in range(6):
            e.record_grant("s1")
        result = e.max_consecutive_grants_exceeded("s1", max_grants=5)
        assert result is True

    def test_max_consecutive_grants_not_exceeded(self):
        e = _engine()
        for _ in range(3):
            e.record_grant("s1")
        result = e.max_consecutive_grants_exceeded("s1", max_grants=5)
        assert result is False


def FairnessEngine_THRESHOLD():
    from paper_trading.multi_session.fairness_engine_v166 import FairnessEngine
    return FairnessEngine.STARVATION_THRESHOLD
