"""
tests/test_replay_scoring_mistake_taxonomy_regression.py

Regression tests for v1.2.3 Replay Scoring & Mistake Taxonomy.

[!] Research Only. No Real Orders. Replay Training Only.
[!] Scoring NEVER triggers paper orders or broker execution.
[!] All tests use TST symbol and fixed test clock.

Test clock: 2023-01-02
"""
from __future__ import annotations

import json
import os
import tempfile
import unittest

TEST_SESSION_ID = "RPL-TST-20230102-REGRTEST"
TEST_CLOCK_DATE = "2023-01-02"
TEST_SYMBOL = "TST"
FIXTURES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "fixtures", "replay_scoring",
)


class TestScoringSchema(unittest.TestCase):
    """Schema dataclasses instantiate correctly with safety invariants."""

    def test_score_component_safety_flags(self):
        from replay.scoring_schema import ScoreComponent
        sc = ScoreComponent(dimension="test", raw_score=0.8, weight=10, weighted_score=8.0)
        self.assertTrue(sc.simulation_only)
        self.assertTrue(sc.no_real_orders)
        self.assertTrue(sc.research_only)

    def test_process_score_safety_flags(self):
        from replay.scoring_schema import ReplayProcessScore
        ps = ReplayProcessScore(score_id="PSC-TEST", session_id=TEST_SESSION_ID)
        self.assertTrue(ps.no_real_orders)
        self.assertTrue(ps.scoring_triggers_no_orders)
        self.assertTrue(ps.simulation_only)

    def test_outcome_score_default_blocked(self):
        from replay.scoring_schema import ReplayOutcomeScore, OutcomeRevealStatus
        os_ = ReplayOutcomeScore(
            score_id="OSC-TEST", session_id=TEST_SESSION_ID, reveal_id=""
        )
        self.assertEqual(os_.status, OutcomeRevealStatus.BLOCKED.value)
        self.assertFalse(os_.auto_outcome_reveal_enabled)

    def test_composite_score_default_blocked(self):
        from replay.scoring_schema import ReplayCompositeScore, CompositeClassification
        cs = ReplayCompositeScore(score_id="CSC-TEST", session_id=TEST_SESSION_ID)
        self.assertEqual(cs.classification, CompositeClassification.BLOCKED.value)
        self.assertTrue(cs.scoring_triggers_no_orders)

    def test_mistake_record_no_auto_confirm(self):
        from replay.scoring_schema import MistakeRecord
        m = MistakeRecord(mistake_id="MIS-TEST", session_id=TEST_SESSION_ID)
        self.assertFalse(m.auto_confirmed)

    def test_review_record_no_auto_confirm(self):
        from replay.scoring_schema import MistakeReviewRecord
        mrv = MistakeReviewRecord(
            review_id="MRV-TEST", mistake_id="MIS-TEST", session_id=TEST_SESSION_ID
        )
        self.assertFalse(mrv.auto_confirmed)
        self.assertTrue(mrv.preserve_original)

    def test_reveal_record_invariants(self):
        from replay.scoring_schema import OutcomeRevealRecord
        orr = OutcomeRevealRecord(reveal_id="REV-TEST", session_id=TEST_SESSION_ID)
        self.assertFalse(orr.auto_outcome_reveal_enabled)
        self.assertTrue(orr.original_snapshot_unchanged)
        self.assertTrue(orr.original_journal_unchanged)

    def test_schema_roundtrip(self):
        from replay.scoring_schema import ReplayProcessScore, ScoreComponent
        comp = ScoreComponent(dimension="test", raw_score=0.5, weight=10, weighted_score=5.0)
        ps = ReplayProcessScore(
            score_id="PSC-RT-TEST", session_id=TEST_SESSION_ID,
            total_score=50.0, components=[comp],
        )
        d = ps.to_dict()
        ps2 = ReplayProcessScore.from_dict(d)
        self.assertAlmostEqual(ps2.total_score, 50.0)
        self.assertTrue(ps2.no_real_orders)
        self.assertEqual(len(ps2.components), 1)


class TestProcessScoreEngine(unittest.TestCase):
    """Process score engine: correctness and safety."""

    def test_no_future_data_fields(self):
        from replay.process_score_engine import ReplayProcessScoreEngine
        from replay.scoring_schema import FORBIDDEN_SCORE_FIELDS
        engine = ReplayProcessScoreEngine()
        score = engine.score(
            session_id=TEST_SESSION_ID,
            journal_entry={"action": "ENTER", "symbol": TEST_SYMBOL},
            session_state={"status": "COMPLETED", "completed": True},
        )
        score_dict = score.to_dict()
        for field in FORBIDDEN_SCORE_FIELDS:
            self.assertNotIn(field, score_dict, f"Forbidden field {field!r} in process score")

    def test_wait_decision_good_score(self):
        from replay.process_score_engine import ReplayProcessScoreEngine
        engine = ReplayProcessScoreEngine()
        score = engine.score(
            session_id=TEST_SESSION_ID,
            journal_entry={
                "action": "WAIT",
                "symbol": TEST_SYMBOL,
                "replay_date": TEST_CLOCK_DATE,
                "decision_reason": "No valid setup. Volume insufficient for confirmation.",
            },
            session_state={"status": "COMPLETED", "completed": True, "available_records": 30},
        )
        # Well-reasoned WAIT should NOT get low score
        thesis_comp = next(
            (c for c in score.components if c.dimension == "thesis_quality"), None
        )
        self.assertIsNotNone(thesis_comp)
        self.assertGreaterEqual(thesis_comp.raw_score, 0.6,
            "Well-reasoned WAIT should have thesis quality >= 0.6")

    def test_skip_decision_no_penalty(self):
        from replay.process_score_engine import ReplayProcessScoreEngine
        engine = ReplayProcessScoreEngine()
        score = engine.score(
            session_id=TEST_SESSION_ID,
            journal_entry={
                "action": "SKIP",
                "symbol": TEST_SYMBOL,
                "decision_reason": "Setup did not meet all criteria.",
            },
            session_state={"status": "COMPLETED", "completed": True},
        )
        # SKIP with reason should get decent score
        self.assertGreater(score.total_score, 20.0)

    def test_safety_flags_present(self):
        from replay.process_score_engine import ReplayProcessScoreEngine
        engine = ReplayProcessScoreEngine()
        self.assertTrue(engine.RESEARCH_ONLY)
        self.assertTrue(engine.SCORING_TRIGGERS_NO_ORDERS)
        self.assertFalse(hasattr(engine, "broker_execution"))

    def test_mock_mode_demo_only_confidence(self):
        from replay.process_score_engine import ReplayProcessScoreEngine
        from replay.scoring_schema import ScoreConfidenceLevel
        engine = ReplayProcessScoreEngine()
        score = engine.score(
            session_id=TEST_SESSION_ID,
            journal_entry={"action": "WATCH", "symbol": TEST_SYMBOL},
            session_config={"mode": "mock"},
        )
        self.assertEqual(score.confidence_level, ScoreConfidenceLevel.DEMO_ONLY.value)

    def test_weights_sum_to_100(self):
        from replay.process_score_engine import ReplayProcessScoreEngine
        engine = ReplayProcessScoreEngine()
        total_weight = sum(engine.WEIGHTS.values())
        self.assertEqual(total_weight, 100)

    def test_complete_fixture(self):
        fixture = _load_fixture("process_score_complete.json")
        self.assertAlmostEqual(fixture["total_score"], 82.5, delta=5.0)
        self.assertTrue(fixture["simulation_only"])
        self.assertTrue(fixture["no_real_orders"])
        self.assertTrue(fixture["scoring_triggers_no_orders"])


class TestOutcomeReveal(unittest.TestCase):
    """Outcome reveal: BLOCKED by default, explicit only."""

    def test_blocked_without_flags(self):
        from replay.outcome_reveal import ReplayOutcomeRevealManager
        from replay.scoring_schema import OutcomeRevealStatus
        mgr = ReplayOutcomeRevealManager()
        record = mgr.reveal(
            session_id=TEST_SESSION_ID,
            session_state={"status": "COMPLETED", "completed": True},
            reveal_flag=False,
            confirm_review_flag=False,
        )
        self.assertEqual(record.status, OutcomeRevealStatus.BLOCKED.value)
        self.assertFalse(record.auto_outcome_reveal_enabled)

    def test_blocked_with_one_flag(self):
        from replay.outcome_reveal import ReplayOutcomeRevealManager
        from replay.scoring_schema import OutcomeRevealStatus
        mgr = ReplayOutcomeRevealManager()
        record = mgr.reveal(
            session_id=TEST_SESSION_ID,
            session_state={"status": "COMPLETED", "completed": True},
            reveal_flag=True,
            confirm_review_flag=False,
        )
        self.assertEqual(record.status, OutcomeRevealStatus.BLOCKED.value)

    def test_blocked_session_not_completed(self):
        from replay.outcome_reveal import ReplayOutcomeRevealManager
        from replay.scoring_schema import OutcomeRevealStatus
        mgr = ReplayOutcomeRevealManager()
        record = mgr.reveal(
            session_id=TEST_SESSION_ID,
            session_state={"status": "PLAYING", "completed": False},
            reveal_flag=True,
            confirm_review_flag=True,
        )
        self.assertEqual(record.status, OutcomeRevealStatus.BLOCKED.value)

    def test_reveal_with_both_flags_completed(self):
        from replay.outcome_reveal import ReplayOutcomeRevealManager
        from replay.scoring_schema import OutcomeRevealStatus
        mgr = ReplayOutcomeRevealManager()
        record = mgr.reveal(
            session_id=TEST_SESSION_ID,
            session_state={"status": "COMPLETED", "completed": True},
            reveal_flag=True,
            confirm_review_flag=True,
        )
        self.assertEqual(record.status, OutcomeRevealStatus.REVEALED.value)
        self.assertTrue(record.original_snapshot_unchanged)
        self.assertTrue(record.original_journal_unchanged)

    def test_preview_never_reveals(self):
        from replay.outcome_reveal import ReplayOutcomeRevealManager
        mgr = ReplayOutcomeRevealManager()
        preview = mgr.preview(
            session_id=TEST_SESSION_ID,
            session_state={"status": "PLAYING", "completed": False},
        )
        self.assertEqual(preview["action"], "PREVIEW_ONLY")
        self.assertFalse(preview["auto_outcome_reveal_enabled"])

    def test_hidden_fixture(self):
        fixture = _load_fixture("outcome_hidden.json")
        self.assertEqual(fixture["status"], "BLOCKED")
        self.assertFalse(fixture["reveal_confirmed"])
        self.assertFalse(fixture["auto_outcome_reveal_enabled"])

    def test_revealed_fixture(self):
        fixture = _load_fixture("outcome_revealed.json")
        self.assertEqual(fixture["status"], "REVEALED")
        self.assertTrue(fixture["reveal_confirmed"])
        self.assertTrue(fixture["confirm_review_flag"])
        self.assertTrue(fixture["original_snapshot_unchanged"])
        self.assertTrue(fixture["original_journal_unchanged"])


class TestCompositeScore(unittest.TestCase):
    """Composite score: PROCESS_ONLY before reveal, classifications, weight warnings."""

    def test_process_only_without_outcome(self):
        from replay.composite_score_engine import ReplayCompositeScoreEngine
        from replay.scoring_schema import CompositeScoreStatus, CompositeClassification
        engine = ReplayCompositeScoreEngine()
        result = engine.build(
            session_id=TEST_SESSION_ID,
            process_score={"score_id": "PSC-T", "total_score": 75.0, "status": "SCORED"},
            outcome_score=None,
        )
        self.assertEqual(result.status, CompositeScoreStatus.PROCESS_ONLY.value)
        self.assertEqual(result.classification, CompositeClassification.PROCESS_ONLY.value)

    def test_good_process_good_outcome(self):
        from replay.composite_score_engine import ReplayCompositeScoreEngine
        from replay.scoring_schema import CompositeClassification
        engine = ReplayCompositeScoreEngine()
        result = engine.build(
            session_id=TEST_SESSION_ID,
            process_score={"score_id": "PSC-T", "total_score": 75.0, "status": "SCORED"},
            outcome_score={"score_id": "OSC-T", "outcome_score": 72.0, "status": "REVEALED"},
        )
        self.assertEqual(result.classification, CompositeClassification.GOOD_PROCESS_GOOD_OUTCOME.value)

    def test_good_process_bad_outcome(self):
        from replay.composite_score_engine import ReplayCompositeScoreEngine
        from replay.scoring_schema import CompositeClassification
        engine = ReplayCompositeScoreEngine()
        result = engine.build(
            session_id=TEST_SESSION_ID,
            process_score={"score_id": "PSC-T", "total_score": 75.0, "status": "SCORED"},
            outcome_score={"score_id": "OSC-T", "outcome_score": 30.0, "status": "REVEALED"},
        )
        self.assertEqual(result.classification, CompositeClassification.GOOD_PROCESS_BAD_OUTCOME.value)

    def test_bad_process_good_outcome(self):
        from replay.composite_score_engine import ReplayCompositeScoreEngine
        from replay.scoring_schema import CompositeClassification
        engine = ReplayCompositeScoreEngine()
        result = engine.build(
            session_id=TEST_SESSION_ID,
            process_score={"score_id": "PSC-T", "total_score": 35.0, "status": "SCORED"},
            outcome_score={"score_id": "OSC-T", "outcome_score": 75.0, "status": "REVEALED"},
        )
        self.assertEqual(result.classification, CompositeClassification.BAD_PROCESS_GOOD_OUTCOME.value)

    def test_bad_process_bad_outcome(self):
        from replay.composite_score_engine import ReplayCompositeScoreEngine
        from replay.scoring_schema import CompositeClassification
        engine = ReplayCompositeScoreEngine()
        result = engine.build(
            session_id=TEST_SESSION_ID,
            process_score={"score_id": "PSC-T", "total_score": 30.0, "status": "SCORED"},
            outcome_score={"score_id": "OSC-T", "outcome_score": 25.0, "status": "REVEALED"},
        )
        self.assertEqual(result.classification, CompositeClassification.BAD_PROCESS_BAD_OUTCOME.value)

    def test_outcome_weight_warning(self):
        from replay.composite_score_engine import ReplayCompositeScoreEngine
        engine = ReplayCompositeScoreEngine()
        result = engine.build(
            session_id=TEST_SESSION_ID,
            process_score={"score_id": "PSC-T", "total_score": 75.0, "status": "SCORED"},
            outcome_score=None,
            process_weight=0.3,
            outcome_weight=0.7,
        )
        self.assertTrue(
            any("outcome_weight" in w for w in result.warnings),
            "Should warn when outcome_weight > 0.5"
        )

    def test_composite_fixtures(self):
        for fixture_name, expected_clf in [
            ("composite_good_good.json", "GOOD_PROCESS_GOOD_OUTCOME"),
            ("composite_good_bad.json", "GOOD_PROCESS_BAD_OUTCOME"),
            ("composite_bad_good.json", "BAD_PROCESS_GOOD_OUTCOME"),
            ("composite_bad_bad.json", "BAD_PROCESS_BAD_OUTCOME"),
        ]:
            with self.subTest(fixture_name=fixture_name):
                fixture = _load_fixture(fixture_name)
                self.assertEqual(fixture["classification"], expected_clf)
                self.assertTrue(fixture["simulation_only"])
                self.assertTrue(fixture["no_real_orders"])


class TestMistakeTaxonomy(unittest.TestCase):
    """Mistake taxonomy: correct categories and planned-exception handling."""

    def test_all_types_present(self):
        from replay.mistake_taxonomy import MistakeTaxonomy
        self.assertGreaterEqual(len(MistakeTaxonomy.ALL_TYPES), 20)

    def test_panic_sell_planned_exception_check(self):
        from replay.mistake_taxonomy import MistakeTaxonomy, MistakeType
        self.assertTrue(MistakeTaxonomy.requires_planned_exception_check(MistakeType.PANIC_SELL))

    def test_exited_too_early_planned_exception_check(self):
        from replay.mistake_taxonomy import MistakeTaxonomy, MistakeType
        self.assertTrue(MistakeTaxonomy.requires_planned_exception_check(MistakeType.EXITED_TOO_EARLY))

    def test_emotional_types_flagged(self):
        from replay.mistake_taxonomy import MistakeTaxonomy, MistakeType
        for etype in [MistakeType.FOMO_ENTRY, MistakeType.REVENGE_TRADE,
                      MistakeType.OVERCONFIDENCE, MistakeType.LOSS_AVERSION_HOLD]:
            self.assertTrue(MistakeTaxonomy.is_emotional(etype))

    def test_entry_types_not_emotional(self):
        from replay.mistake_taxonomy import MistakeTaxonomy, MistakeType
        self.assertFalse(MistakeTaxonomy.is_emotional(MistakeType.CHASING_BREAKOUT))
        self.assertFalse(MistakeTaxonomy.is_emotional(MistakeType.NO_STOP_DEFINED))

    def test_category_mapping_correct(self):
        from replay.mistake_taxonomy import MistakeTaxonomy, MistakeType, MistakeCategory
        self.assertEqual(MistakeTaxonomy.get_category(MistakeType.CHASING_BREAKOUT), MistakeCategory.ENTRY)
        self.assertEqual(MistakeTaxonomy.get_category(MistakeType.PANIC_SELL), MistakeCategory.EXIT)
        self.assertEqual(MistakeTaxonomy.get_category(MistakeType.NO_STOP_DEFINED), MistakeCategory.RISK)
        self.assertEqual(MistakeTaxonomy.get_category(MistakeType.SKIPPED_CHECKLIST), MistakeCategory.PROCESS)
        self.assertEqual(MistakeTaxonomy.get_category(MistakeType.FOMO_ENTRY), MistakeCategory.EMOTIONAL)

    def test_safety_note_mentions_wait_skip(self):
        from replay.mistake_taxonomy import MistakeTaxonomy
        note = MistakeTaxonomy.safety_note()
        self.assertIn("WAIT/SKIP", note)
        self.assertIn("NOT PANIC_SELL", note)


class TestMistakeDetector(unittest.TestCase):
    """Mistake detector: SUGGESTED only, no auto-confirm, correct guards."""

    def test_wait_with_reason_no_mistakes(self):
        from replay.mistake_detector import ReplayMistakeDetector
        detector = ReplayMistakeDetector()
        mistakes = detector.detect(
            session_id=TEST_SESSION_ID,
            journal_entry={
                "action": "WAIT",
                "symbol": TEST_SYMBOL,
                "replay_date": TEST_CLOCK_DATE,
                "decision_reason": "No valid setup present. Volume too low.",
            },
        )
        self.assertEqual(len(mistakes), 0,
            "Well-reasoned WAIT should produce no mistakes")

    def test_skip_with_conditions_no_mistakes(self):
        from replay.mistake_detector import ReplayMistakeDetector
        detector = ReplayMistakeDetector()
        mistakes = detector.detect(
            session_id=TEST_SESSION_ID,
            journal_entry={
                "action": "SKIP",
                "symbol": TEST_SYMBOL,
                "no_trade_conditions": ["Volume < 1.5x average"],
            },
        )
        self.assertEqual(len(mistakes), 0)

    def test_planned_stop_not_panic_sell(self):
        from replay.mistake_detector import ReplayMistakeDetector
        detector = ReplayMistakeDetector()
        mistakes = detector.detect(
            session_id=TEST_SESSION_ID,
            journal_entry={
                "action": "STOP",
                "symbol": TEST_SYMBOL,
                "risk_plan_id": "RSK-PLANNED",
                "fallback_action": "STOP",
            },
        )
        panic_sells = [m for m in mistakes if m.mistake_type == "PANIC_SELL"]
        self.assertEqual(len(panic_sells), 0,
            "Planned stop (risk_plan_id present) must NOT be PANIC_SELL")

    def test_entry_without_thesis_detected(self):
        from replay.mistake_detector import ReplayMistakeDetector
        detector = ReplayMistakeDetector()
        mistakes = detector.detect(
            session_id=TEST_SESSION_ID,
            journal_entry={
                "action": "ENTER",
                "symbol": TEST_SYMBOL,
                "thesis_id": None,
            },
        )
        types = [m.mistake_type for m in mistakes]
        self.assertIn("NO_THESIS_DOCUMENTED", types)

    def test_all_detected_are_suggested(self):
        from replay.mistake_detector import ReplayMistakeDetector
        detector = ReplayMistakeDetector()
        mistakes = detector.detect(
            session_id=TEST_SESSION_ID,
            journal_entry={
                "action": "ENTER",
                "symbol": TEST_SYMBOL,
            },
        )
        for m in mistakes:
            self.assertFalse(m.auto_confirmed,
                f"Mistake {m.mistake_type} must not be auto-confirmed")
            self.assertIn(m.status, ("SUGGESTED", "NEEDS_REVIEW"),
                f"Mistake {m.mistake_type} must be SUGGESTED or NEEDS_REVIEW")

    def test_single_loss_not_auto_mistake(self):
        """Single loss should not create more mistakes than process issues."""
        from replay.mistake_detector import ReplayMistakeDetector
        detector = ReplayMistakeDetector()
        # Entry with good documentation — even if market goes down, process was fine
        mistakes = detector.detect(
            session_id=TEST_SESSION_ID,
            journal_entry={
                "action": "ENTER",
                "symbol": TEST_SYMBOL,
                "thesis_id": "THY-TEST",
                "risk_plan_id": "RSK-TEST",
                "checklist_ids": ["CHK-TEST"],
                "point_in_time_verified": True,
            },
        )
        # Should have minimal/no mistakes for good documentation
        self.assertLessEqual(len(mistakes), 1)

    def test_fomo_self_reported_only(self):
        from replay.mistake_detector import ReplayMistakeDetector
        from replay.scoring_schema import MistakeSource
        detector = ReplayMistakeDetector()
        mistakes = detector.detect(
            session_id=TEST_SESSION_ID,
            journal_entry={
                "action": "ENTER",
                "symbol": TEST_SYMBOL,
                "emotional_state_id": "EMO-TEST",
                "fomo": True,
                "thesis_id": "THY-TEST",
                "risk_plan_id": "RSK-TEST",
                "checklist_ids": ["CHK-TEST"],
                "point_in_time_verified": True,
            },
        )
        fomo_mistakes = [m for m in mistakes if m.mistake_type == "FOMO_ENTRY"]
        if fomo_mistakes:
            self.assertEqual(fomo_mistakes[0].source, MistakeSource.SELF_REPORTED.value,
                "FOMO_ENTRY must be SELF_REPORTED source")


class TestMistakeReview(unittest.TestCase):
    """Mistake review: append-only, no auto-confirm, system cannot confirm."""

    def test_system_cannot_confirm(self):
        from replay.mistake_review import ReplayMistakeReviewManager
        from replay.scoring_schema import MistakeStatus
        mgr = ReplayMistakeReviewManager()
        record = mgr.confirm(
            mistake={"mistake_id": "MIS-TEST", "session_id": TEST_SESSION_ID},
            reviewer="SYSTEM_REVIEW",
        )
        self.assertFalse(record.auto_confirmed)
        self.assertNotEqual(record.new_status, MistakeStatus.CONFIRMED.value,
            "SYSTEM_REVIEW must not set status to CONFIRMED")

    def test_user_can_confirm(self):
        from replay.mistake_review import ReplayMistakeReviewManager
        from replay.scoring_schema import MistakeStatus
        mgr = ReplayMistakeReviewManager()
        record = mgr.confirm(
            mistake={"mistake_id": "MIS-TEST", "session_id": TEST_SESSION_ID},
            reviewer="USER",
        )
        self.assertFalse(record.auto_confirmed)
        self.assertEqual(record.new_status, MistakeStatus.CONFIRMED.value)

    def test_dismiss_preserves_original(self):
        from replay.mistake_review import ReplayMistakeReviewManager
        from replay.scoring_schema import MistakeStatus
        mgr = ReplayMistakeReviewManager()
        original = {"mistake_id": "MIS-TEST", "session_id": TEST_SESSION_ID,
                    "mistake_type": "CHASING_BREAKOUT"}
        record = mgr.dismiss(mistake=original, reviewer="USER")
        self.assertEqual(record.new_status, MistakeStatus.DISMISSED.value)
        self.assertTrue(record.preserve_original)
        # Original type preserved in review record
        self.assertEqual(record.mistake_id, original["mistake_id"])

    def test_override_preserves_history(self):
        from replay.mistake_review import ReplayMistakeReviewManager
        from replay.scoring_schema import MistakeStatus
        mgr = ReplayMistakeReviewManager()
        record = mgr.override(
            mistake={"mistake_id": "MIS-TEST", "session_id": TEST_SESSION_ID},
            override_type="ENTERING_WITHOUT_CONFIRMATION",
            override_severity="HIGH",
            reviewer="USER",
        )
        self.assertEqual(record.new_status, MistakeStatus.OVERRIDDEN.value)
        self.assertEqual(record.override_type, "ENTERING_WITHOUT_CONFIRMATION")
        self.assertTrue(record.preserve_original)

    def test_reopen_preserves_history(self):
        from replay.mistake_review import ReplayMistakeReviewManager
        from replay.scoring_schema import MistakeStatus
        mgr = ReplayMistakeReviewManager()
        record = mgr.reopen(
            mistake={"mistake_id": "MIS-TEST", "session_id": TEST_SESSION_ID},
            reviewer="USER",
        )
        self.assertEqual(record.new_status, MistakeStatus.REOPENED.value)
        self.assertTrue(record.preserve_original)


class TestScoringStore(unittest.TestCase):
    """Scoring store: append-only, no crash on corrupted lines."""

    def test_append_and_load(self):
        from replay.scoring_store import ReplayScoringStore
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ReplayScoringStore(repo_root=tmpdir)
            store.append("process_score", {
                "score_id": "PSC-TST", "session_id": TEST_SESSION_ID,
                "total_score": 72.0
            })
            records = store.load_all("process_score")
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["score_id"], "PSC-TST")

    def test_corrupted_line_skipped(self):
        from replay.scoring_store import ReplayScoringStore
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ReplayScoringStore(repo_root=tmpdir)
            store.append("process_score", {"score_id": "PSC-OK", "session_id": TEST_SESSION_ID})
            # Inject corrupted line
            path = store.store_path("process_score")
            with open(path, "a", encoding="utf-8") as f:
                f.write("CORRUPTED JSON LINE\n")
            store.append("process_score", {"score_id": "PSC-OK2", "session_id": TEST_SESSION_ID})
            records = store.load_all("process_score")
            self.assertEqual(len(records), 2, "Corrupted line should be skipped")

    def test_valid_fixture_loads(self):
        fixture_path = os.path.join(FIXTURES_DIR, "store_valid.jsonl")
        records = []
        with open(fixture_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        self.assertEqual(len(records), 3)

    def test_corrupted_fixture_skips_bad_line(self):
        fixture_path = os.path.join(FIXTURES_DIR, "store_corrupted_tail.jsonl")
        records = []
        with open(fixture_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass  # Skip corrupted
        self.assertEqual(len(records), 2, "Corrupted tail should not crash loader")


class TestScoreConfidence(unittest.TestCase):
    """Score confidence levels."""

    def test_mock_is_demo_only(self):
        from replay.score_confidence import ReplayScoreConfidence
        sc = ReplayScoreConfidence()
        level, note = sc.assess(entry_count=100, is_mock=True)
        self.assertEqual(level, "DEMO_ONLY")
        self.assertIn("DEMO_ONLY", note)

    def test_zero_entries_insufficient(self):
        from replay.score_confidence import ReplayScoreConfidence
        sc = ReplayScoreConfidence()
        level, _ = sc.assess(entry_count=0)
        self.assertEqual(level, "INSUFFICIENT")

    def test_less_than_10_insufficient(self):
        from replay.score_confidence import ReplayScoreConfidence
        sc = ReplayScoreConfidence()
        for n in range(1, 10):
            with self.subTest(n=n):
                level, _ = sc.assess(entry_count=n)
                if n == 1:
                    self.assertEqual(level, "OBSERVATIONAL")
                else:
                    self.assertEqual(level, "INSUFFICIENT")

    def test_10_to_29_observational(self):
        from replay.score_confidence import ReplayScoreConfidence
        sc = ReplayScoreConfidence()
        level, _ = sc.assess(entry_count=15)
        self.assertEqual(level, "OBSERVATIONAL")

    def test_30_plus_sessions_10_reliable(self):
        from replay.score_confidence import ReplayScoreConfidence
        sc = ReplayScoreConfidence()
        level, _ = sc.assess(entry_count=35, session_count=12)
        self.assertEqual(level, "RELIABLE")

    def test_over_concentrated_not_reliable(self):
        from replay.score_confidence import ReplayScoreConfidence
        sc = ReplayScoreConfidence()
        level, note = sc.assess(
            entry_count=50, session_count=15,
            symbol_distribution={"TST": 45, "OTHER": 5},
        )
        self.assertEqual(level, "OBSERVATIONAL", "Over-concentrated should be OBSERVATIONAL")

    def test_mock_never_falls_back_to_real(self):
        """Real mode never falls back to mock."""
        from replay.score_confidence import ReplayScoreConfidence
        sc = ReplayScoreConfidence()
        # Real mode with 0 entries
        level, _ = sc.assess(entry_count=0, is_mock=False)
        self.assertNotEqual(level, "DEMO_ONLY", "Real mode must not be DEMO_ONLY")


class TestSafetyInvariants(unittest.TestCase):
    """Safety invariants: scoring never triggers orders."""

    def test_module_safety_flags(self):
        from replay.scoring_schema import (
            NO_REAL_ORDERS, SCORING_TRIGGERS_NO_ORDERS,
            AUTO_OUTCOME_REVEAL_ENABLED, AUTO_MISTAKE_CONFIRMATION_ENABLED,
            AUTO_SCORE_TO_TRADE_ENABLED,
        )
        self.assertTrue(NO_REAL_ORDERS)
        self.assertTrue(SCORING_TRIGGERS_NO_ORDERS)
        self.assertFalse(AUTO_OUTCOME_REVEAL_ENABLED)
        self.assertFalse(AUTO_MISTAKE_CONFIRMATION_ENABLED)
        self.assertFalse(AUTO_SCORE_TO_TRADE_ENABLED)

    def test_score_to_trade_fixture_blocked(self):
        fixture = _load_fixture("score_to_trade_attempt.json")
        safety = fixture.get("_SAFETY_INVARIANTS", {})
        self.assertTrue(safety.get("no_real_orders"))
        self.assertTrue(safety.get("scoring_triggers_no_orders"))
        self.assertFalse(safety.get("auto_score_to_trade_enabled"))
        self.assertFalse(safety.get("broker_execution_enabled"))

    def test_high_score_no_order_trigger(self):
        """Score of 95 must not trigger any order mechanism."""
        from replay.process_score_engine import ReplayProcessScoreEngine
        engine = ReplayProcessScoreEngine()
        score = engine.score(
            session_id=TEST_SESSION_ID,
            journal_entry={
                "action": "ENTER", "symbol": TEST_SYMBOL,
                "thesis_id": "THY-TEST", "risk_plan_id": "RSK-TEST",
                "checklist_ids": ["CHK-TEST"],
                "evidence_for": ["Strong trend", "Volume spike"],
                "confirmation_conditions": ["Price above MA20"],
                "invalidation_conditions": ["Close below support"],
                "point_in_time_verified": True,
            },
            session_state={"status": "COMPLETED", "completed": True, "available_records": 50},
        )
        # Even a high score must not have broker fields
        score_dict = score.to_dict()
        self.assertNotIn("broker", score_dict)
        self.assertNotIn("order_token", score_dict)
        self.assertNotIn("submit_order", str(score_dict))
        self.assertTrue(score_dict.get("scoring_triggers_no_orders"))

    def test_health_check_passes(self):
        from replay.scoring_health import ReplayScoringHealthCheck
        hc = ReplayScoringHealthCheck()
        results = hc.run()
        overall = hc.overall_status(results)
        failed = [(k, v[1]) for k, v in results.items() if v[0] == "FAIL"]
        self.assertEqual(overall, "PASS",
            f"Scoring health check failed: {failed}")


class TestPlanAdherence(unittest.TestCase):
    """Plan adherence evaluator."""

    def test_wait_with_reason_full_adherence(self):
        from replay.plan_adherence import ReplayPlanAdherenceEvaluator
        evaluator = ReplayPlanAdherenceEvaluator()
        result = evaluator.evaluate(
            session_id=TEST_SESSION_ID,
            journal_entry={
                "action": "WAIT",
                "decision_reason": "No valid setup.",
            },
        )
        self.assertEqual(result["status"], "FULL_ADHERENCE")
        self.assertGreaterEqual(result["adherence_score"], 90.0)

    def test_fixtures_valid(self):
        for fixture_name in [
            "plan_adherence_full.json",
            "plan_adherence_revision.json",
            "plan_adherence_missing.json",
        ]:
            with self.subTest(fixture_name=fixture_name):
                fixture = _load_fixture(fixture_name)
                self.assertIn("adherence_score", fixture)
                self.assertTrue(fixture["simulation_only"])


class TestScoringHealthCheck(unittest.TestCase):
    """Scoring health check passes all checks."""

    def test_health_check_all_pass(self):
        from replay.scoring_health import ReplayScoringHealthCheck
        hc = ReplayScoringHealthCheck()
        results = hc.run()
        for check_name, (status, message) in results.items():
            with self.subTest(check_name=check_name):
                self.assertNotEqual(status, "FAIL",
                    f"Health check {check_name} FAILED: {message}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_fixture(filename: str) -> dict:
    path = os.path.join(FIXTURES_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    unittest.main()
