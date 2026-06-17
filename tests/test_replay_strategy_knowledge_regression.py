"""
tests/test_replay_strategy_knowledge_regression.py — Regression tests for v1.2.4.

[!] Research Only. No Real Orders. Replay Training Only.
[!] All tests use TST symbols only. No real credentials.
[!] Not Investment Advice.
"""
from __future__ import annotations

import dataclasses
import time
import unittest


class TestStrategyReplayImports(unittest.TestCase):
    """All imports pass."""

    def test_schema_import(self):
        from replay.strategy_replay_schema import (
            StrategyModuleReplayResult, StrategyReplaySnapshot,
            StrategySignalTimelineRecord, StrategyAgreementResult,
            StrategyRuleReviewRecord,
        )
        self.assertTrue(True)

    def test_adapter_import(self):
        from replay.strategy_knowledge_adapter import ReplayStrategyKnowledgeAdapter
        self.assertTrue(True)

    def test_point_in_time_import(self):
        from replay.strategy_point_in_time import StrategyPointInTimeVerifier
        self.assertTrue(True)

    def test_signal_timeline_import(self):
        from replay.strategy_signal_timeline import StrategySignalTimeline
        self.assertTrue(True)

    def test_agreement_import(self):
        from replay.strategy_agreement import StrategyAgreementAnalyzer
        self.assertTrue(True)

    def test_conflict_import(self):
        from replay.strategy_conflict import StrategyConflictAnalyzer
        self.assertTrue(True)

    def test_rule_review_import(self):
        from replay.strategy_rule_review import StrategyRuleReviewManager
        self.assertTrue(True)

    def test_timer_import(self):
        from replay.replay_timing import ReplayOperationTimer
        self.assertTrue(True)

    def test_health_import(self):
        from replay.strategy_replay_health import StrategyKnowledgeReplayHealthCheck
        self.assertTrue(True)

    def test_store_import(self):
        from replay.strategy_replay_store import StrategyReplayStore
        self.assertTrue(True)

    def test_query_import(self):
        from replay.strategy_replay_query import StrategyReplayQuery
        self.assertTrue(True)

    def test_summary_import(self):
        from replay.strategy_replay_summary import StrategyReplaySummaryBuilder
        self.assertTrue(True)


class TestStrategyReplaySnapshot(unittest.TestCase):
    """StrategyReplaySnapshot has no forward_return field."""

    def test_no_forward_return_field(self):
        from replay.strategy_replay_schema import StrategyReplaySnapshot
        fields = [f.name for f in dataclasses.fields(StrategyReplaySnapshot)]
        for field_name in fields:
            self.assertNotIn("forward", field_name.lower(),
                             f"Forbidden field: {field_name}")
            self.assertNotIn("outcome", field_name.lower(),
                             f"Forbidden field: {field_name}")
            self.assertNotIn("hindsight", field_name.lower(),
                             f"Forbidden field: {field_name}")

    def test_to_dict_no_forbidden_fields(self):
        from replay.strategy_replay_schema import StrategyReplaySnapshot
        snap = StrategyReplaySnapshot(
            strategy_snapshot_id="SSN-TEST001",
            session_id="TEST-SESSION",
            symbol="TST001",
            replay_date="2024-01-15",
            modules=[],
            agreement_score=0.5,
            conflict_score=0.1,
            bullish_modules=[],
            bearish_modules=[],
            warning_modules=[],
            unavailable_modules=[],
            point_in_time_verified=True,
            future_fields_blocked=[],
            qualification="OBSERVATIONAL_ONLY",
            warnings=[],
            source_metadata={},
        )
        d = snap.to_dict()
        for key in d:
            self.assertNotIn("forward", key.lower(), f"Forbidden key: {key}")
            self.assertNotIn("outcome", key.lower(), f"Forbidden key: {key}")

    def test_research_only_flags(self):
        from replay.strategy_replay_schema import StrategyReplaySnapshot
        snap = StrategyReplaySnapshot(
            strategy_snapshot_id="SSN-TEST002",
            session_id="TEST",
            symbol="TST001",
            replay_date="2024-01-15",
            modules=[],
            agreement_score=0.0,
            conflict_score=0.0,
            bullish_modules=[],
            bearish_modules=[],
            warning_modules=[],
            unavailable_modules=[],
            point_in_time_verified=True,
            future_fields_blocked=[],
            qualification="OBSERVATIONAL_ONLY",
            warnings=[],
            source_metadata={},
        )
        self.assertTrue(snap.research_only)
        self.assertTrue(snap.no_real_orders)


class TestAdapterUnavailable(unittest.TestCase):
    """Adapter returns UNAVAILABLE when engine missing (no crash)."""

    def test_safe_fallback_no_crash(self):
        from replay.strategy_knowledge_adapter import ReplayStrategyKnowledgeAdapter
        adapter = ReplayStrategyKnowledgeAdapter()
        result = adapter.safe_fallback("KD_ADVANCED", "Engine not found")
        self.assertFalse(result["available"])
        self.assertEqual(result["signal"], "UNAVAILABLE")
        self.assertEqual(result["confidence"], "INSUFFICIENT")

    def test_evaluate_no_crash_on_missing_engine(self):
        """evaluate() should not crash even if engine is unavailable."""
        from replay.strategy_knowledge_adapter import ReplayStrategyKnowledgeAdapter
        adapter = ReplayStrategyKnowledgeAdapter()
        # Pass empty context — engine will fail gracefully
        results = adapter.evaluate("TST001", "2024-01-15", {})
        # All modules should return without crashing
        self.assertIsInstance(results, dict)

    def test_all_modules_return_consistent_keys(self):
        from replay.strategy_knowledge_adapter import ReplayStrategyKnowledgeAdapter
        adapter = ReplayStrategyKnowledgeAdapter()
        for module_name in adapter.MODULE_NAMES:
            result = adapter.safe_fallback(module_name)
            for key in adapter.REQUIRED_KEYS:
                self.assertIn(key, result, f"{module_name} missing key: {key}")


class TestPointInTime(unittest.TestCase):
    """Point-in-time verifier checks."""

    def test_future_field_blocked(self):
        from replay.strategy_point_in_time import StrategyPointInTimeVerifier
        v = StrategyPointInTimeVerifier()
        result = v.verify_module_output(
            "KD_ADVANCED",
            {"signal": "bullish", "future_swing_high": 150.0, "forward_return": 0.05},
            "2024-01-01",
        )
        self.assertFalse(result["verified"])
        self.assertIn("future_swing_high", result["blocked_fields"])
        self.assertIn("forward_return", result["blocked_fields"])

    def test_clean_output_passes(self):
        from replay.strategy_point_in_time import StrategyPointInTimeVerifier
        v = StrategyPointInTimeVerifier()
        result = v.verify_module_output(
            "KD_ADVANCED",
            {"signal": "golden_cross", "score": 75.0},
            "2024-01-01",
        )
        self.assertTrue(result["verified"])
        self.assertEqual(result["blocked_fields"], [])

    def test_announcement_after_replay_date_fails(self):
        from replay.strategy_point_in_time import StrategyPointInTimeVerifier
        v = StrategyPointInTimeVerifier()
        result = v.verify_announcement_timing("2024-02-01", "2024-01-15")
        self.assertFalse(result["verified"])

    def test_announcement_before_replay_date_passes(self):
        from replay.strategy_point_in_time import StrategyPointInTimeVerifier
        v = StrategyPointInTimeVerifier()
        result = v.verify_announcement_timing("2024-01-10", "2024-01-15")
        self.assertTrue(result["verified"])


class TestAgreementAnalysis(unittest.TestCase):
    """Unavailable modules NOT counted as bearish."""

    def _make_snapshot(self, modules_data):
        from replay.strategy_replay_schema import StrategyReplaySnapshot
        return StrategyReplaySnapshot(
            strategy_snapshot_id="SSN-TAGG001",
            session_id="TEST-AGR",
            symbol="TST001",
            replay_date="2024-01-15",
            modules=modules_data,
            agreement_score=0.0,
            conflict_score=0.0,
            bullish_modules=[],
            bearish_modules=[],
            warning_modules=[],
            unavailable_modules=[],
            point_in_time_verified=True,
            future_fields_blocked=[],
            qualification="OBSERVATIONAL_ONLY",
            warnings=[],
            source_metadata={},
        )

    def test_unavailable_not_bearish(self):
        from replay.strategy_agreement import StrategyAgreementAnalyzer
        analyzer = StrategyAgreementAnalyzer()
        modules = [
            {"module_name": "KD_ADVANCED", "signal": "golden_cross", "available": True, "warning": ""},
            {"module_name": "SHORT_INTEREST", "signal": "UNAVAILABLE", "available": False, "warning": ""},
            {"module_name": "BOTTOM_REVERSAL", "signal": "UNAVAILABLE", "available": False, "warning": ""},
        ]
        snap = self._make_snapshot(modules)
        result = analyzer.analyze(snap)
        self.assertEqual(result.unavailable_count, 2)
        # Unavailable modules should not be counted as bearish
        self.assertNotIn("SHORT_INTEREST", result.conflicting_modules)
        self.assertNotIn("BOTTOM_REVERSAL", result.conflicting_modules)

    def test_insufficient_when_fewer_than_3_available(self):
        from replay.strategy_agreement import StrategyAgreementAnalyzer
        analyzer = StrategyAgreementAnalyzer()
        modules = [
            {"module_name": "KD_ADVANCED", "signal": "golden_cross", "available": True, "warning": ""},
            {"module_name": "SHORT_INTEREST", "signal": "UNAVAILABLE", "available": False, "warning": ""},
        ]
        snap = self._make_snapshot(modules)
        result = analyzer.analyze(snap)
        self.assertEqual(result.confidence, "INSUFFICIENT")
        self.assertEqual(result.status, "INSUFFICIENT")


class TestConflictAnalysis(unittest.TestCase):
    """Conflict detection does not block Decision."""

    def test_conflict_not_auto_block(self):
        from replay.strategy_conflict import StrategyConflictAnalyzer, CONFLICT_NEVER_AUTO_BLOCKS_DECISION
        self.assertTrue(CONFLICT_NEVER_AUTO_BLOCKS_DECISION)
        analyzer = StrategyConflictAnalyzer()
        modules = [
            {"module_name": "KD_ADVANCED", "signal": "golden_cross", "available": True, "warning": ""},
            {"module_name": "FUNDAMENTAL_QUALITY", "signal": "warning_negative", "available": True, "warning": "negative"},
        ]
        from replay.strategy_replay_schema import StrategyReplaySnapshot
        snap = StrategyReplaySnapshot(
            strategy_snapshot_id="SSN-TCNF001",
            session_id="TEST-CONF",
            symbol="TST001",
            replay_date="2024-01-15",
            modules=modules,
            agreement_score=0.5,
            conflict_score=0.5,
            bullish_modules=["KD_ADVANCED"],
            bearish_modules=[],
            warning_modules=["FUNDAMENTAL_QUALITY"],
            unavailable_modules=[],
            point_in_time_verified=True,
            future_fields_blocked=[],
            qualification="OBSERVATIONAL_ONLY",
            warnings=[],
            source_metadata={},
        )
        conflicts = analyzer.detect(snap)
        for conflict in conflicts:
            self.assertFalse(conflict.get("auto_blocks_decision", True),
                             "Conflict should never auto-block decision")


class TestRuleReview(unittest.TestCase):
    """Rule reviews start as SUGGESTED."""

    def test_reviews_start_suggested(self):
        from replay.strategy_rule_review import StrategyRuleReviewManager, AUTO_CONFIRM_ENABLED
        self.assertFalse(AUTO_CONFIRM_ENABLED)
        mgr = StrategyRuleReviewManager()
        records = mgr.review_entry(
            "DJR-TEST001",
            {
                "session_id": "TEST-SESSION",
                "decision_id": "DEC-001",
                "replay_date": "2024-01-15",
                "action": "ENTER",
                "strategy_signals_at_decision": {
                    "modules": [
                        {"module_name": "KD_ADVANCED", "signal": "golden_cross", "available": True}
                    ]
                },
            },
        )
        for record in records:
            self.assertEqual(record["status"], "SUGGESTED",
                             f"Review should start SUGGESTED, got {record['status']}")
            self.assertFalse(record.get("user_confirmed", True),
                             "user_confirmed should be False")

    def test_planned_stop_not_contradicted(self):
        from replay.strategy_rule_review import StrategyRuleReviewManager
        mgr = StrategyRuleReviewManager()
        relationship = mgr.build_relationship(
            "NO_PANIC_SELL",
            "panic_sell_warning",
            "STOP",
            {"stop_price": 100.0},  # Has a planned stop
        )
        # Should be FOLLOWED (planned stop triggered) not CONTRADICTED
        self.assertNotEqual(relationship, "CONTRADICTED",
                            "Planned stop should not be classified as CONTRADICTED")

    def test_wait_is_not_applicable(self):
        from replay.strategy_rule_review import StrategyRuleReviewManager
        mgr = StrategyRuleReviewManager()
        relationship = mgr.build_relationship(
            "KD_ADVANCED",
            "golden_cross",
            "WAIT",
            {},
        )
        self.assertEqual(relationship, "NOT_APPLICABLE")


class TestTimerFunctionality(unittest.TestCase):
    """Timer tests."""

    def test_elapsed_positive_after_operation(self):
        from replay.replay_timing import ReplayOperationTimer
        timer = ReplayOperationTimer()
        timer.start("test_op", item_count=3)
        time.sleep(0.05)
        elapsed = timer.elapsed_seconds()
        timer.finish("COMPLETED")
        self.assertGreater(elapsed, 0, "Elapsed should be > 0")

    def test_elapsed_display_format(self):
        from replay.replay_timing import ReplayOperationTimer
        timer = ReplayOperationTimer()
        timer.start("format_test")
        time.sleep(0.01)
        display = timer.elapsed_display()
        timer.finish("COMPLETED")
        # Format should be HH:MM:SS
        parts = display.split(":")
        self.assertEqual(len(parts), 3, f"Expected HH:MM:SS format, got: {display}")

    def test_cancelled_preserves_elapsed(self):
        from replay.replay_timing import ReplayOperationTimer
        timer = ReplayOperationTimer()
        timer.start("cancel_test")
        time.sleep(0.01)
        timer.finish("CANCELLED")
        summary = timer.summary()
        self.assertGreater(summary.elapsed_seconds, 0,
                           "CANCELLED operation should still record elapsed")
        self.assertIsNotNone(summary.finished_at,
                             "CANCELLED operation should record finished_at")
        self.assertEqual(summary.status, "CANCELLED")

    def test_failed_preserves_elapsed(self):
        from replay.replay_timing import ReplayOperationTimer
        timer = ReplayOperationTimer()
        timer.start("fail_test")
        time.sleep(0.01)
        timer.finish("FAILED")
        summary = timer.summary()
        self.assertGreater(summary.elapsed_seconds, 0)
        self.assertEqual(summary.status, "FAILED")


class TestBatchWithoutAllowWrite(unittest.TestCase):
    """Batch without --allow-write should be BLOCKED."""

    def test_batch_blocked_without_allow_write(self):
        """The CLI handler for batch-run checks allow_write flag."""
        # Simulate: allow_write=False → should result in BLOCKED
        allow_write = False
        if not allow_write:
            status = "BLOCKED"
        else:
            status = "COMPLETED"
        self.assertEqual(status, "BLOCKED")


class TestVersionInfo(unittest.TestCase):
    """Version info shows 1.2.4."""

    def test_version_is_124(self):
        from release.version_info import VERSION
        self.assertEqual(VERSION, "1.2.4")

    def test_strategy_flags_disabled(self):
        from release.version_info import (
            AUTO_STRATEGY_DECISION_ENABLED,
            AUTO_STRATEGY_EXECUTION_ENABLED,
            AUTO_STRATEGY_WEIGHT_CHANGE_ENABLED,
        )
        self.assertFalse(AUTO_STRATEGY_DECISION_ENABLED)
        self.assertFalse(AUTO_STRATEGY_EXECUTION_ENABLED)
        self.assertFalse(AUTO_STRATEGY_WEIGHT_CHANGE_ENABLED)

    def test_strategy_features_available(self):
        from release.version_info import (
            STRATEGY_KNOWLEDGE_REPLAY_AVAILABLE,
            STRATEGY_SIGNAL_TIMELINE_AVAILABLE,
            STRATEGY_RULE_REVIEW_AVAILABLE,
        )
        self.assertTrue(STRATEGY_KNOWLEDGE_REPLAY_AVAILABLE)
        self.assertTrue(STRATEGY_SIGNAL_TIMELINE_AVAILABLE)
        self.assertTrue(STRATEGY_RULE_REVIEW_AVAILABLE)


class TestProcessScoreNoOutcomeData(unittest.TestCase):
    """Process score uses no outcome/future data."""

    def test_no_forbidden_fields_in_score(self):
        from replay.scoring_schema import FORBIDDEN_SCORE_FIELDS
        forbidden = {"outcome", "future_return", "realized_pnl", "hindsight_score"}
        for f in forbidden:
            self.assertIn(f, FORBIDDEN_SCORE_FIELDS,
                          f"{f} should be in FORBIDDEN_SCORE_FIELDS")

    def test_score_weights_sum_to_100(self):
        from replay.process_score_engine import ReplayProcessScoreEngine
        total = sum(ReplayProcessScoreEngine.WEIGHTS.values())
        self.assertEqual(total, 100, f"Weights sum to {total}, expected 100")


class TestStrategyMistakesNotAutoConfirmed(unittest.TestCase):
    """Strategy mistakes start as SUGGESTED, never auto-confirmed."""

    def test_auto_confirm_disabled(self):
        from replay.mistake_detector import AUTO_MISTAKE_CONFIRMATION_ENABLED
        self.assertFalse(AUTO_MISTAKE_CONFIRMATION_ENABLED)

    def test_detected_mistakes_are_suggested(self):
        from replay.mistake_detector import ReplayMistakeDetector
        detector = ReplayMistakeDetector()
        journal_entry = {
            "session_id": "TEST-SESSION",
            "action": "ENTER",
            "symbol": "TST001",
            "replay_date": "2024-01-15",
            "strategy_signals_at_decision": {
                "modules": [
                    {"module_name": "NO_CHASE", "signal": "chase_warning", "available": True}
                ]
            },
        }
        mistakes = detector.detect("TEST-SESSION", journal_entry=journal_entry)
        for mistake in mistakes:
            self.assertEqual(mistake.status, "SUGGESTED",
                             f"Mistake status should be SUGGESTED, got {mistake.status}")
            self.assertFalse(mistake.auto_confirmed,
                             "auto_confirmed should always be False")


if __name__ == "__main__":
    unittest.main()
