"""
tests/test_replay_review_dashboard_regression.py — Regression Tests v1.2.6

Regression tests for the Replay Review Dashboard.

[!] Research Only. No Real Orders. Tests only — no side effects.
[!] Not Investment Advice.
"""
from __future__ import annotations

import json
import os
import tempfile
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_DIR = os.path.join(BASE_DIR, "tests", "fixtures", "replay_review")

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def load_fixture(name: str) -> dict:
    path = os.path.join(FIXTURE_DIR, name)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class TestReplayReviewSchema(unittest.TestCase):
    """Test schema dataclasses."""

    def test_snapshot_instantiates(self):
        from replay.review_dashboard_schema import ReplayReviewDashboardSnapshot, _new_id
        snap = ReplayReviewDashboardSnapshot(snapshot_id=_new_id("RRD-"), mode="real")
        self.assertTrue(snap.research_only)
        self.assertTrue(snap.no_real_orders)
        self.assertFalse(snap.auto_review_complete_enabled)
        self.assertFalse(snap.auto_outcome_reveal_enabled)

    def test_session_row_outcome_hidden(self):
        from replay.review_dashboard_schema import ReplayReviewSessionRow
        row = ReplayReviewSessionRow(
            session_id="S1", symbol="TST",
            outcome_score=80.0, composite_score=75.0,
            outcome_revealed=False,
        )
        d = row.to_dict()
        self.assertIsNone(d["outcome_score"])
        self.assertTrue(d["outcome_score_hidden"])
        self.assertIsNone(d["composite_score"])

    def test_session_row_outcome_revealed(self):
        from replay.review_dashboard_schema import ReplayReviewSessionRow
        row = ReplayReviewSessionRow(
            session_id="S1", symbol="TST",
            outcome_score=80.0, outcome_revealed=True,
        )
        d = row.to_dict()
        self.assertEqual(d["outcome_score"], 80.0)
        self.assertFalse(d["outcome_score_hidden"])

    def test_queue_item_no_auto_confirm(self):
        from replay.review_dashboard_schema import ReplayReviewQueueItem, _new_id
        item = ReplayReviewQueueItem(
            queue_item_id=_new_id("QI-"),
            session_id="S1",
            queue_type="MISTAKE_REVIEW_PENDING",
            priority="P1",
            status="OPEN",
        )
        self.assertFalse(item.auto_confirm_on_complete)
        self.assertFalse(item.auto_reveal_on_complete)

    def test_progress_outcome_not_required(self):
        from replay.review_dashboard_schema import ReplayReviewProgress, _new_id
        prog = ReplayReviewProgress(
            progress_id=_new_id("PRG-"),
            session_id="S1",
            status="NOT_STARTED",
        )
        self.assertFalse(prog.outcome_reveal_required)

    def test_fixture_dashboard_empty(self):
        data = load_fixture("dashboard_empty.json")
        self.assertEqual(data["total_sessions"], 0)
        self.assertTrue(data["research_only"])

    def test_fixture_outcome_hidden(self):
        data = load_fixture("outcome_hidden.json")
        self.assertFalse(data["outcome_revealed"])
        self.assertTrue(data["outcome_score_hidden"])
        self.assertIsNone(data["outcome_score"])


class TestReplayReviewQueue(unittest.TestCase):
    """Test queue manager."""

    def setUp(self):
        from replay.review_queue import ReplayReviewQueueManager
        self.mgr = ReplayReviewQueueManager()

    def test_auto_flags_false(self):
        self.assertFalse(self.mgr.AUTO_CONFIRM_ON_COMPLETE)
        self.assertFalse(self.mgr.AUTO_REVEAL_ON_COMPLETE)

    def test_complete_no_auto_confirm(self):
        result = self.mgr.complete("NONEXISTENT", note="done")
        self.assertEqual(result["status"], "NOT_FOUND")

    def test_summary_no_auto(self):
        s = self.mgr.summary()
        self.assertFalse(s["auto_confirm_on_complete"])
        self.assertFalse(s["auto_reveal_on_complete"])

    def test_start_review(self):
        from replay.review_dashboard_schema import ReplayReviewQueueItem, QueueItemStatus, _new_id
        item = ReplayReviewQueueItem(
            queue_item_id="QI-TEST-001",
            session_id="S1",
            queue_type="MISTAKE_REVIEW_PENDING",
            priority="P1",
            status="OPEN",
        )
        self.mgr._items["QI-TEST-001"] = item
        result = self.mgr.start_review("QI-TEST-001")
        self.assertEqual(result["status"], "OK")
        self.assertEqual(item.status, QueueItemStatus.IN_REVIEW.value)

    def test_complete_no_side_effects(self):
        from replay.review_dashboard_schema import ReplayReviewQueueItem, _new_id
        item = ReplayReviewQueueItem(
            queue_item_id="QI-TEST-002",
            session_id="S1",
            queue_type="MISTAKE_REVIEW_PENDING",
            priority="P1",
            status="IN_REVIEW",
        )
        self.mgr._items["QI-TEST-002"] = item
        result = self.mgr.complete("QI-TEST-002", note="reviewed")
        self.assertEqual(result["status"], "OK")
        self.assertFalse(result["auto_confirm_mistake"])
        self.assertFalse(result["auto_reveal_outcome"])


class TestReplayReviewProgress(unittest.TestCase):
    """Test progress calculator."""

    def setUp(self):
        from replay.review_progress import ReplayReviewProgressCalculator
        self.calc = ReplayReviewProgressCalculator()

    def test_outcome_not_required(self):
        self.assertFalse(self.calc.OUTCOME_REVEAL_REQUIRED)

    def test_outcome_not_in_required_steps(self):
        req = self.calc.required_steps()
        self.assertNotIn("outcome_revealed", req)
        self.assertIn("session_completed", req)
        self.assertIn("review_note_added", req)

    def test_process_complete_without_outcome(self):
        session_data = {
            "session_completed": True,
            "journal_exists": True,
            "process_score_calculated": True,
            "suggested_mistakes_reviewed": True,
            "strategy_conflicts_reviewed": True,
            "timeframe_conflicts_reviewed": True,
            "point_in_time_verified": True,
            "review_note_added": True,
            "outcome_revealed": False,
        }
        prog = self.calc.calculate("S1", session_data)
        self.assertTrue(prog.process_review_complete)
        self.assertFalse(prog.full_review_complete)
        self.assertFalse(prog.outcome_reveal_required)

    def test_not_started(self):
        prog = self.calc.calculate("S1", {})
        self.assertFalse(prog.process_review_complete)
        self.assertFalse(prog.outcome_reveal_required)


class TestReplayReviewChecklist(unittest.TestCase):
    """Test checklist."""

    def setUp(self):
        from replay.review_checklist import ReplayReviewChecklist
        self.cl = ReplayReviewChecklist("S1")

    def test_auto_complete_false(self):
        self.assertFalse(self.cl.AUTO_COMPLETE)

    def test_outcome_reveal_manual_required(self):
        items = self.cl.items()
        outcome_items = [i for i in items if "Outcome reveal" in i.label]
        self.assertGreaterEqual(len(outcome_items), 1)
        result = self.cl.complete_item(outcome_items[0].item_id)
        self.assertEqual(result["status"], "MANUAL_REQUIRED")

    def test_mistake_confirm_manual_required(self):
        items = self.cl.items()
        mistake_items = [i for i in items if "Mistake confirmation" in i.label]
        if mistake_items:
            result = self.cl.complete_item(mistake_items[0].item_id)
            self.assertEqual(result["status"], "MANUAL_REQUIRED")


class TestReplayReviewBatch(unittest.TestCase):
    """Test batch runner guard."""

    def setUp(self):
        from replay.review_batch import ReplayReviewBatchRunner
        self.runner = ReplayReviewBatchRunner()

    def test_default_preview(self):
        self.assertTrue(self.runner.DEFAULT_PREVIEW_MODE)

    def test_blocked_without_allow_write(self):
        result = self.runner.run(["S1"], execute=True, allow_write=False)
        self.assertEqual(result["status"], "BLOCKED")

    def test_blocked_without_execute(self):
        result = self.runner.run(["S1"], execute=False, allow_write=True)
        self.assertEqual(result["status"], "BLOCKED")

    def test_preview_mode(self):
        preview = self.runner.preview(["S1"])
        self.assertEqual(preview["mode"], "PREVIEW")
        self.assertFalse(preview["allow_write"])

    def test_no_auto_reveal(self):
        self.assertTrue(self.runner.NO_AUTO_REVEAL)
        self.assertTrue(self.runner.NO_AUTO_CONFIRM)


class TestReplayReviewStore(unittest.TestCase):
    """Test store with corrupted tail recovery."""

    def test_append_and_load(self):
        from replay.review_store import ReplayReviewStore
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ReplayReviewStore(base_dir=tmpdir)
            self.assertTrue(store.append_snapshot({"snapshot_id": "RRD-001"}))
            snaps = store.get_snapshots()
            self.assertEqual(len(snaps), 1)

    def test_corrupted_tail_recovery(self):
        import json as _json
        from replay.review_store import ReplayReviewStore
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ReplayReviewStore(base_dir=tmpdir)
            store.append_snapshot({"snapshot_id": "RRD-001"})
            path = store._path("dashboard_snapshots.jsonl")
            with open(path, "a", encoding="utf-8") as f:
                f.write("{CORRUPTED\n")
            store.append_snapshot({"snapshot_id": "RRD-002"})
            snaps = store.get_snapshots()
            self.assertEqual(len(snaps), 2)

    def test_state_atomic_write(self):
        from replay.review_store import ReplayReviewStore
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ReplayReviewStore(base_dir=tmpdir)
            self.assertTrue(store.write_state({"version": "1.2.6"}))
            state = store.read_state()
            self.assertEqual(state.get("version"), "1.2.6")


class TestReplayReviewComparator(unittest.TestCase):
    """Test comparator outcome hiding."""

    def test_outcome_not_available_when_not_revealed(self):
        from replay.review_comparator import ReplayReviewComparator, NOT_AVAILABLE
        comp = ReplayReviewComparator()
        row_a = {"session_id": "A", "symbol": "TST", "outcome_revealed": False, "outcome_score": 80.0}
        row_b = {"session_id": "B", "symbol": "TST", "outcome_revealed": True, "outcome_score": 60.0}
        result = comp.compare_sessions(row_a, row_b)
        self.assertEqual(result["comparison"]["outcome_score"]["session_a"], NOT_AVAILABLE)
        self.assertEqual(result["comparison"]["outcome_score"]["session_b"], 60.0)


class TestReplayReviewVersionInfo(unittest.TestCase):
    """Test version info flags for v1.2.6."""

    def test_version_is_1_2_6(self):
        """VERSION >= 1.2.6 (Review Dashboard was introduced in 1.2.6)."""
        from release.version_info import VERSION
        major, minor, patch = (int(x) for x in VERSION.split("."))
        self.assertGreaterEqual((major, minor, patch), (1, 2, 6),
                                f"VERSION {VERSION} predates Review Dashboard 1.2.6")

    def test_all_auto_flags_false(self):
        from release.version_info import (
            AUTO_REVIEW_COMPLETE_ENABLED, AUTO_OUTCOME_REVEAL_ENABLED,
            AUTO_MISTAKE_CONFIRMATION_ENABLED, AUTO_SCORE_TO_TRADE_ENABLED,
            REPLAY_TRADE_EXECUTION_ENABLED, BROKER_EXECUTION_ENABLED,
        )
        self.assertFalse(AUTO_REVIEW_COMPLETE_ENABLED)
        self.assertFalse(AUTO_OUTCOME_REVEAL_ENABLED)
        self.assertFalse(AUTO_MISTAKE_CONFIRMATION_ENABLED)
        self.assertFalse(AUTO_SCORE_TO_TRADE_ENABLED)
        self.assertFalse(REPLAY_TRADE_EXECUTION_ENABLED)
        self.assertFalse(BROKER_EXECUTION_ENABLED)

    def test_dashboard_available(self):
        from release.version_info import REPLAY_REVIEW_DASHBOARD_AVAILABLE
        self.assertTrue(REPLAY_REVIEW_DASHBOARD_AVAILABLE)


class TestReplayReviewHealth(unittest.TestCase):
    """Test health check runs without crash."""

    def test_health_check_runs(self):
        from replay.review_health import ReplayReviewDashboardHealthCheck
        hc = ReplayReviewDashboardHealthCheck()
        results = hc.run()
        self.assertIsInstance(results, dict)
        self.assertGreater(len(results), 0)
        # No component should CRASH (all return (status, message) tuples)
        for name, (status, message) in results.items():
            self.assertIn(status, ("PASS", "WARN", "FAIL", "BLOCKED"), f"Invalid status for {name}")
            self.assertIsInstance(message, str)


if __name__ == "__main__":
    unittest.main()
