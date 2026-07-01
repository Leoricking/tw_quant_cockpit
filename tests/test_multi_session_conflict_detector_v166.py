"""
test_multi_session_conflict_detector_v166.py — Conflict Detector tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


def _policy():
    from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
    return make_default_policy()


def _make_desc(name, owner="owner", symbols=None, strategies=None, capital=0.0, session_id=None):
    from paper_trading.multi_session.session_descriptor_v166 import make_session_descriptor
    return make_session_descriptor(
        name, owner,
        symbols=symbols or [],
        strategies=strategies or [],
        capital_budget=capital,
        session_id=session_id or name,
    )


class TestConflictDetector:
    def test_detect_returns_list(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        result = cd.detect([], _policy())
        assert isinstance(result, list)

    def test_detect_with_no_sessions_returns_empty(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        result = cd.detect([], _policy())
        assert result == []

    def test_detect_with_single_session_no_conflicts(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d = _make_desc("s1", symbols=["2330"])
        result = cd.detect([d], _policy())
        # No symbol conflict for single session
        symbol_conflicts = [c for c in result if c.conflict_type.value == "SYMBOL_OVERLAP"]
        assert len(symbol_conflicts) == 0

    def test_symbol_overlap_detection_warn_level(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        from paper_trading.multi_session.enums_v166 import ConflictSeverity
        cd = ConflictDetector()
        d1 = _make_desc("s1", symbols=["2330"], session_id="s1")
        d2 = _make_desc("s2", symbols=["2330"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        symbol_conflicts = [c for c in conflicts if c.conflict_type.value == "SYMBOL_OVERLAP"]
        assert len(symbol_conflicts) == 1
        assert symbol_conflicts[0].severity == ConflictSeverity.WARN

    def test_symbol_overlap_not_blocking(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", symbols=["0050"], session_id="s1")
        d2 = _make_desc("s2", symbols=["0050"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        overlap = [c for c in conflicts if c.conflict_type.value == "SYMBOL_OVERLAP"]
        assert all(c.blocking is False for c in overlap)

    def test_strategy_conflict_detection_warn_level(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        from paper_trading.multi_session.enums_v166 import ConflictSeverity
        cd = ConflictDetector()
        d1 = _make_desc("s1", strategies=["momentum"], session_id="s1")
        d2 = _make_desc("s2", strategies=["momentum"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        strategy_conflicts = [c for c in conflicts if c.conflict_type.value == "STRATEGY_CONFLICT"]
        assert len(strategy_conflicts) == 1
        assert strategy_conflicts[0].severity == ConflictSeverity.WARN

    def test_capital_overallocation_detection_block_level(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        from paper_trading.multi_session.enums_v166 import ConflictSeverity
        cd = ConflictDetector()
        d1 = _make_desc("s1", capital=6_000_000.0, session_id="s1")
        d2 = _make_desc("s2", capital=6_000_000.0, session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        cap_conflicts = [c for c in conflicts if c.conflict_type.value == "CAPITAL_OVERALLOCATION"]
        assert len(cap_conflicts) == 1
        assert cap_conflicts[0].severity == ConflictSeverity.BLOCK

    def test_capital_overallocation_is_blocking(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", capital=6_000_000.0, session_id="s1")
        d2 = _make_desc("s2", capital=6_000_000.0, session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        cap_conflicts = [c for c in conflicts if c.conflict_type.value == "CAPITAL_OVERALLOCATION"]
        assert all(c.blocking is True for c in cap_conflicts)

    def test_no_overlap_no_symbol_conflict(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", symbols=["2330"], session_id="s1")
        d2 = _make_desc("s2", symbols=["0050"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        symbol_conflicts = [c for c in conflicts if c.conflict_type.value == "SYMBOL_OVERLAP"]
        assert len(symbol_conflicts) == 0

    def test_conflict_has_policy_version(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", symbols=["2330"], session_id="s1")
        d2 = _make_desc("s2", symbols=["2330"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        assert all(c.policy_version == "1.6.6" for c in conflicts)

    def test_conflict_has_session_ids(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", symbols=["2330"], session_id="s1")
        d2 = _make_desc("s2", symbols=["2330"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        overlap = [c for c in conflicts if c.conflict_type.value == "SYMBOL_OVERLAP"]
        assert len(overlap[0].session_ids) >= 2

    def test_multiple_conflicts_detected(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", symbols=["2330"], strategies=["momentum"], session_id="s1")
        d2 = _make_desc("s2", symbols=["2330"], strategies=["momentum"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        assert len(conflicts) >= 2

    def test_conflict_has_evidence_dict(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", symbols=["2330"], session_id="s1")
        d2 = _make_desc("s2", symbols=["2330"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        assert all(isinstance(c.evidence, dict) for c in conflicts)


class TestConflictDetectSessionStateConflict:
    def test_function_importable(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        assert hasattr(cd, "detect_session_state_conflict")

    def test_returns_list(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        result = cd.detect_session_state_conflict("RUNNING", "RUNNING", "1.6.6")
        assert isinstance(result, list)

    def test_running_vs_recovering_creates_conflict(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        result = cd.detect_session_state_conflict("RUNNING", "RECOVERING", "1.6.6")
        assert len(result) == 1

    def test_no_conflict_same_state(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        result = cd.detect_session_state_conflict("RUNNING", "RUNNING", "1.6.6")
        assert len(result) == 0

    def test_conflict_has_session_state_conflict_type(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        from paper_trading.multi_session.enums_v166 import ConflictType
        cd = ConflictDetector()
        result = cd.detect_session_state_conflict("RUNNING", "RECOVERING", "1.6.6")
        assert result[0].conflict_type == ConflictType.SESSION_STATE_CONFLICT

    def test_symbol_conflict_contains_symbol_name(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", symbols=["2317"], session_id="s1")
        d2 = _make_desc("s2", symbols=["2317"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        sym_conflicts = [c for c in conflicts if c.conflict_type.value == "SYMBOL_OVERLAP"]
        assert sym_conflicts[0].symbol == "2317"

    def test_strategy_conflict_contains_strategy_name(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", strategies=["value_invest"], session_id="s1")
        d2 = _make_desc("s2", strategies=["value_invest"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        strat_conflicts = [c for c in conflicts if c.conflict_type.value == "STRATEGY_CONFLICT"]
        assert strat_conflicts[0].strategy == "value_invest"

    def test_three_sessions_multiple_symbol_overlaps(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", symbols=["2330", "0050"], session_id="s1")
        d2 = _make_desc("s2", symbols=["2330"], session_id="s2")
        d3 = _make_desc("s3", symbols=["0050"], session_id="s3")
        conflicts = cd.detect([d1, d2, d3], _policy())
        sym_conflicts = [c for c in conflicts if c.conflict_type.value == "SYMBOL_OVERLAP"]
        assert len(sym_conflicts) >= 2

    def test_capital_conflict_evidence_contains_total_capital(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", capital=6_000_000.0, session_id="s1")
        d2 = _make_desc("s2", capital=6_000_000.0, session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        cap_conflicts = [c for c in conflicts if c.conflict_type.value == "CAPITAL_OVERALLOCATION"]
        assert "total_capital" in cap_conflicts[0].evidence

    def test_conflict_detected_at_is_datetime(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        from datetime import datetime
        cd = ConflictDetector()
        d1 = _make_desc("s1", symbols=["2330"], session_id="s1")
        d2 = _make_desc("s2", symbols=["2330"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        assert isinstance(conflicts[0].detected_at, datetime)

    def test_conflict_resolution_options_is_list(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", symbols=["2330"], session_id="s1")
        d2 = _make_desc("s2", symbols=["2330"], session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        assert all(isinstance(c.resolution_options, list) for c in conflicts)

    def test_capital_within_budget_no_cap_conflict(self):
        from paper_trading.multi_session.conflict_detector_v166 import ConflictDetector
        cd = ConflictDetector()
        d1 = _make_desc("s1", capital=100_000.0, session_id="s1")
        d2 = _make_desc("s2", capital=100_000.0, session_id="s2")
        conflicts = cd.detect([d1, d2], _policy())
        cap_conflicts = [c for c in conflicts if c.conflict_type.value == "CAPITAL_OVERALLOCATION"]
        assert len(cap_conflicts) == 0
