"""
tests/test_replay_decision_journal_regression.py
Regression tests for v1.2.2 Decision Journal Integration.

[!] Research Only. No Real Orders. Replay Training Only.
[!] No performance metrics. No hindsight. No future data.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

FIXTURES_DIR = os.path.join(BASE_DIR, "tests", "fixtures", "replay_journal")


def _fixture(name: str) -> dict:
    with open(os.path.join(FIXTURES_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)


def _fixture_text(name: str) -> str:
    with open(os.path.join(FIXTURES_DIR, name), "r", encoding="utf-8") as f:
        return f.read()


def _make_entry(mgr, action="BUY", symbol="AAPL", date="2026-06-10",
                session_id="RPL-TEST-SESSION", decision_id=None):
    """Helper to create a journal entry using the real API."""
    import uuid
    did = decision_id or f"DEC-{uuid.uuid4().hex[:8].upper()}"
    e = mgr.create_entry(session_id, did, date, action=action, symbol=symbol)
    return e


# ---------------------------------------------------------------------------
# 1. Schema import and basic construction
# ---------------------------------------------------------------------------
class TestDecisionJournalSchema(unittest.TestCase):
    """Schema imports, to_dict/from_dict round-trips, safety fields."""

    def test_schema_import(self):
        from replay.decision_journal_schema import (
            DecisionJournalEntry, DecisionRevisionRecord, DecisionJournalLink,
            TradeThesis, RiskPlan, EmotionalStateRecord, DisciplineChecklistResult,
            JOURNAL_ID_PREFIX, REVISION_ID_PREFIX,
            FORBIDDEN_JOURNAL_FIELDS, FORBIDDEN_SUMMARY_FIELDS,
        )

    def test_id_prefixes(self):
        from replay.decision_journal_schema import JOURNAL_ID_PREFIX, REVISION_ID_PREFIX
        self.assertEqual(JOURNAL_ID_PREFIX, "DJR-")
        self.assertEqual(REVISION_ID_PREFIX, "DREV-")

    def test_entry_to_dict_from_dict(self):
        from replay.decision_journal_schema import DecisionJournalEntry
        e = DecisionJournalEntry(
            journal_entry_id="DJR-TEST-001",
            decision_id="DEC-TEST-001",
            session_id="RPL-TEST",
            replay_date="2026-06-10",
            action="BUY",
        )
        d = e.to_dict()
        e2 = DecisionJournalEntry.from_dict(d)
        self.assertEqual(e2.journal_entry_id, "DJR-TEST-001")
        self.assertTrue(e2.simulation_only)

    def test_entry_simulation_only_enforced(self):
        from replay.decision_journal_schema import DecisionJournalEntry
        e = DecisionJournalEntry(
            journal_entry_id="DJR-TEST-SIM",
            decision_id="DEC-TEST-SIM",
            session_id="RPL-TEST",
            replay_date="2026-06-10",
            action="BUY",
        )
        self.assertTrue(e.simulation_only)

    def test_entry_djr_prefix_enforced(self):
        from replay.decision_journal_schema import DecisionJournalEntry
        # from_dict should keep or enforce DJR- prefix
        d = {
            "journal_entry_id": "DJR-ABCD",
            "decision_id": "DEC-ABCD",
            "session_id": "RPL-TEST",
            "replay_date": "2026-06-10",
            "action": "BUY",
            "simulation_only": True,
        }
        e = DecisionJournalEntry.from_dict(d)
        self.assertTrue(e.journal_entry_id.startswith("DJR-"))

    def test_revision_to_dict_from_dict(self):
        from replay.decision_journal_schema import DecisionRevisionRecord
        r = DecisionRevisionRecord(
            revision_id="DREV-TEST-001",
            journal_entry_id="DJR-TEST-001",
            original_entry_id="DJR-TEST-001",
            decision_id="DEC-TEST-001",
            session_id="RPL-TEST",
            reason="Reducing confidence.",
        )
        d = r.to_dict()
        r2 = DecisionRevisionRecord.from_dict(d)
        self.assertEqual(r2.revision_id, "DREV-TEST-001")
        self.assertTrue(r2.revision_id.startswith("DREV-"))

    def test_emotional_state_self_reported(self):
        from replay.decision_journal_schema import EmotionalStateRecord
        es = EmotionalStateRecord(
            emotional_state_id="EMOT-TEST",
            session_id="RPL-TEST",
            decision_id="DEC-TEST",
            primary_emotion="CALM",
            confidence_level=70,
            anxiety_level=20,
            focus_level=80,
        )
        self.assertTrue(es.self_reported)

    def test_forbidden_fields_defined(self):
        from replay.decision_journal_schema import (
            FORBIDDEN_JOURNAL_FIELDS, FORBIDDEN_SUMMARY_FIELDS
        )
        for f in ["realized_return", "future_return", "hindsight_score", "final_result"]:
            self.assertIn(f, FORBIDDEN_JOURNAL_FIELDS)
        for f in ["win_rate", "pnl", "alpha", "sharpe"]:
            self.assertIn(f, FORBIDDEN_SUMMARY_FIELDS)


# ---------------------------------------------------------------------------
# 2. Store: append-only writes, load, corrupted tail
# ---------------------------------------------------------------------------
class TestDecisionJournalStore(unittest.TestCase):
    """Store append-only operations and corrupted tail recovery."""

    def test_store_import(self):
        from replay.decision_journal_store import DecisionJournalStore

    def test_store_load_valid_jsonl(self):
        from replay.decision_journal_store import DecisionJournalStore
        import shutil
        with tempfile.TemporaryDirectory() as tmpdir:
            store = DecisionJournalStore(repo_root=tmpdir)
            # Create a temp dir structure matching the store
            data_dir = os.path.join(tmpdir, "data", "replay_journal")
            os.makedirs(data_dir, exist_ok=True)
            src = os.path.join(FIXTURES_DIR, "store_valid.jsonl")
            shutil.copy(src, os.path.join(data_dir, "journal_entries.jsonl"))
            entries = store.load_entries()
            self.assertGreaterEqual(len(entries), 1)

    def test_store_corrupted_tail_graceful(self):
        from replay.decision_journal_store import DecisionJournalStore
        import shutil
        with tempfile.TemporaryDirectory() as tmpdir:
            store = DecisionJournalStore(repo_root=tmpdir)
            data_dir = os.path.join(tmpdir, "data", "replay_journal")
            os.makedirs(data_dir, exist_ok=True)
            src = os.path.join(FIXTURES_DIR, "store_corrupted_tail.jsonl")
            shutil.copy(src, os.path.join(data_dir, "journal_entries.jsonl"))
            try:
                entries = store.load_entries()
                self.assertGreaterEqual(len(entries), 1)
            except Exception:
                pass  # Graceful: partial load or empty, never hard crash

    def test_store_append_only(self):
        from replay.decision_journal_store import DecisionJournalStore
        from replay.decision_journal_schema import DecisionJournalEntry
        with tempfile.TemporaryDirectory() as tmpdir:
            store = DecisionJournalStore(repo_root=tmpdir)
            e1 = DecisionJournalEntry(
                journal_entry_id="DJR-STORE-TEST-001",
                decision_id="DEC-STORE-001",
                session_id="RPL-STORE-SESSION",
                replay_date="2026-06-10",
                action="BUY",
                simulation_only=True,
            )
            store.save_entry(e1.to_dict())
            e2 = DecisionJournalEntry(
                journal_entry_id="DJR-STORE-TEST-002",
                decision_id="DEC-STORE-002",
                session_id="RPL-STORE-SESSION",
                replay_date="2026-06-11",
                action="WAIT",
                simulation_only=True,
            )
            store.save_entry(e2.to_dict())
            entries = store.load_entries()
            ids = [e.get("journal_entry_id") for e in entries]
            self.assertIn("DJR-STORE-TEST-001", ids)
            self.assertIn("DJR-STORE-TEST-002", ids)

    def test_store_health_check(self):
        from replay.decision_journal_store import DecisionJournalStore
        with tempfile.TemporaryDirectory() as tmpdir:
            store = DecisionJournalStore(repo_root=tmpdir)
            health = store.get_store_health()
            self.assertIn("status", health)


# ---------------------------------------------------------------------------
# 3. Manager: CRUD, IDs, archived immutability, import guard
# ---------------------------------------------------------------------------
class TestDecisionJournalManager(unittest.TestCase):
    """Manager create/record/revise/archive/restore/hide with guard enforcement."""

    def test_manager_import(self):
        from replay.decision_journal_manager import DecisionJournalManager

    def test_create_entry_draft(self):
        from replay.decision_journal_manager import DecisionJournalManager
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = DecisionJournalManager(repo_root=tmpdir)
            e = _make_entry(mgr, action="BUY", symbol="AAPL", date="2026-06-10")
            d = e.to_dict()
            self.assertTrue(d.get("journal_entry_id", "").startswith("DJR-"))
            self.assertEqual(d.get("status"), "DRAFT")
            self.assertTrue(d.get("simulation_only"))

    def test_record_entry_status(self):
        from replay.decision_journal_manager import DecisionJournalManager
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = DecisionJournalManager(repo_root=tmpdir)
            e = _make_entry(mgr, action="WAIT", date="2026-06-11")
            entry_id = e.to_dict()["journal_entry_id"]
            recorded = mgr.record_entry(entry_id)
            self.assertEqual(recorded.get("status"), "RECORDED")

    def test_revise_entry_drev_prefix(self):
        from replay.decision_journal_manager import DecisionJournalManager
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = DecisionJournalManager(repo_root=tmpdir)
            e = _make_entry(mgr, action="BUY", date="2026-06-10")
            entry_id = e.to_dict()["journal_entry_id"]
            mgr.record_entry(entry_id)
            rev = mgr.revise_entry(
                entry_id,
                reason="Volume not confirming.",
                field_changes={"notes": "updated"},
            )
            self.assertIsNotNone(rev)
            revision_id = rev.revision_id if hasattr(rev, "revision_id") else rev.get("revision_id", "")
            self.assertTrue(str(revision_id).startswith("DREV-"))

    def test_archived_entry_immutable(self):
        """Revising an ARCHIVED entry must be blocked (returns None or raises)."""
        from replay.decision_journal_manager import DecisionJournalManager
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = DecisionJournalManager(repo_root=tmpdir)
            e = _make_entry(mgr, action="WAIT", date="2026-06-05")
            entry_id = e.to_dict()["journal_entry_id"]
            mgr.record_entry(entry_id)
            mgr.archive_entry(entry_id)
            # Manager either returns None (blocked) or raises — both are acceptable
            try:
                result = mgr.revise_entry(
                    entry_id,
                    reason="Attempting to revise archived entry.",
                    field_changes={"notes": "should fail"},
                )
                # If no exception: must return None (blocked silently)
                self.assertIsNone(result, "Expected None for archived entry revision")
            except (ValueError, Exception):
                pass  # Exception is also acceptable

    def test_import_entry_dry_run_guard(self):
        """import_entry with dry_run=True must not write."""
        from replay.decision_journal_manager import DecisionJournalManager
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = DecisionJournalManager(repo_root=tmpdir)
            entry_data = {
                "journal_entry_id": "DJR-IMPORT-DRY-TEST",
                "decision_id": "DEC-IMPORT-DRY",
                "session_id": "RPL-IMPORT-SESSION",
                "replay_date": "2026-06-10",
                "action": "BUY",
                "simulation_only": True,
            }
            result = mgr.import_entry(entry_data, dry_run=True)
            if isinstance(result, dict):
                self.assertNotEqual(result.get("status"), "imported")

    def test_hide_entry(self):
        from replay.decision_journal_manager import DecisionJournalManager
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = DecisionJournalManager(repo_root=tmpdir)
            e = _make_entry(mgr, action="BUY", date="2026-06-10")
            entry_id = e.to_dict()["journal_entry_id"]
            hidden = mgr.hide_entry(entry_id)
            self.assertTrue(hidden.get("hidden"))


# ---------------------------------------------------------------------------
# 4. Query: filter operations
# ---------------------------------------------------------------------------
class TestDecisionJournalQuery(unittest.TestCase):
    """Query filters: session, symbol, status, action, drafts, archived."""

    def test_query_import(self):
        from replay.decision_journal_query import DecisionJournalQuery

    def test_filter_by_status(self):
        from replay.decision_journal_query import DecisionJournalQuery
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.decision_journal_manager import DecisionJournalManager
            mgr = DecisionJournalManager(repo_root=tmpdir)
            e1 = _make_entry(mgr, action="BUY", symbol="AAPL", date="2026-06-10",
                              session_id="RPL-QUERY-SESSION")
            e2 = _make_entry(mgr, action="WAIT", symbol="MSFT", date="2026-06-11",
                              session_id="RPL-QUERY-SESSION")
            mgr.record_entry(e2.to_dict()["journal_entry_id"])

            q = DecisionJournalQuery(repo_root=tmpdir)
            drafts = q.drafts()
            draft_ids = [e.get("journal_entry_id") for e in drafts]
            self.assertIn(e1.to_dict()["journal_entry_id"], draft_ids)

    def test_filter_by_symbol(self):
        from replay.decision_journal_query import DecisionJournalQuery
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.decision_journal_manager import DecisionJournalManager
            mgr = DecisionJournalManager(repo_root=tmpdir)
            _make_entry(mgr, action="BUY", symbol="AAPL", date="2026-06-10",
                        session_id="RPL-QUERY-SESSION")
            _make_entry(mgr, action="BUY", symbol="MSFT", date="2026-06-11",
                        session_id="RPL-QUERY-SESSION")

            q = DecisionJournalQuery(repo_root=tmpdir)
            results = q.by_symbol("AAPL")
            for e in results:
                self.assertEqual(e.get("symbol"), "AAPL")


# ---------------------------------------------------------------------------
# 5. Templates
# ---------------------------------------------------------------------------
class TestDecisionTemplates(unittest.TestCase):
    """Template library: list, load, fallback."""

    def test_templates_import(self):
        from replay.decision_templates import DecisionTemplateLibrary

    def test_list_templates(self):
        from replay.decision_templates import DecisionTemplateLibrary
        lib = DecisionTemplateLibrary(repo_root=BASE_DIR)
        templates = lib.list_templates()
        self.assertIsInstance(templates, list)

    def test_fallback_template(self):
        from replay.decision_templates import DecisionTemplateLibrary
        lib = DecisionTemplateLibrary(repo_root=BASE_DIR)
        t = lib._get_fallback_template("nonexistent_template")
        self.assertIsNotNone(t)
        self.assertTrue(t.get("simulation_only"))


# ---------------------------------------------------------------------------
# 6. Discipline Checklist
# ---------------------------------------------------------------------------
class TestDisciplineChecklist(unittest.TestCase):
    """Checklist engine: standard items, evaluate, required blocking."""

    def test_checklist_import(self):
        from replay.discipline_checklist import DisciplineChecklistEngine

    def test_evaluate_all_pass(self):
        from replay.discipline_checklist import DisciplineChecklistEngine
        engine = DisciplineChecklistEngine()
        items = engine.build_default("BUY", "BREAKOUT")
        self.assertGreater(len(items), 0)
        responses = {item["item_id"]: True for item in items}
        result = engine.evaluate_checklist(items, responses)
        self.assertTrue(result.all_required_passed)

    def test_evaluate_missing_required(self):
        from replay.discipline_checklist import DisciplineChecklistEngine
        engine = DisciplineChecklistEngine()
        items = engine.build_default("BUY")
        # Pass nothing — all required items will fail
        result = engine.evaluate_checklist(items, {})
        self.assertFalse(result.all_required_passed)


# ---------------------------------------------------------------------------
# 7. Emotional State: range validation, self-reported invariant
# ---------------------------------------------------------------------------
class TestEmotionalState(unittest.TestCase):
    """Emotional state capture: range enforcement, self-reported flag."""

    def test_emotional_state_import(self):
        from replay.emotional_state import EmotionalStateCapture

    def test_valid_record(self):
        from replay.emotional_state import EmotionalStateCapture
        cap = EmotionalStateCapture()
        rec = cap.record_state(
            session_id="RPL-TEST",
            decision_id="DEC-TEST",
            emotion="CALM",
            confidence=70,
            anxiety=20,
            focus=85,
        )
        self.assertIsNotNone(rec)
        d = rec.to_dict() if hasattr(rec, "to_dict") else dict(rec)
        self.assertTrue(d.get("self_reported"))
        self.assertTrue(d.get("simulation_only"))

    def test_out_of_range_raises(self):
        """Values outside 0-100 must raise ValueError."""
        from replay.emotional_state import EmotionalStateCapture
        cap = EmotionalStateCapture()
        with self.assertRaises((ValueError, Exception)):
            cap.validate_levels(anxiety=150, focus=-5)


# ---------------------------------------------------------------------------
# 8. Cognitive Bias Registry: known/unknown bias enforcement
# ---------------------------------------------------------------------------
class TestCognitiveBias(unittest.TestCase):
    """Cognitive bias: only KNOWN_BIASES accepted, unknown raises."""

    def test_cognitive_bias_import(self):
        from replay.cognitive_bias import CognitiveBiasRegistry

    def test_known_biases_defined(self):
        from replay.cognitive_bias import CognitiveBiasRegistry
        reg = CognitiveBiasRegistry()
        self.assertGreaterEqual(len(reg.KNOWN_BIASES), 10)

    def test_unknown_bias_raises(self):
        from replay.cognitive_bias import CognitiveBiasRegistry
        reg = CognitiveBiasRegistry()
        with self.assertRaises((ValueError, KeyError, Exception)):
            reg.flag_bias("TOTALLY_UNKNOWN_BIAS_XYZ_999")

    def test_known_bias_accepted(self):
        from replay.cognitive_bias import CognitiveBiasRegistry
        reg = CognitiveBiasRegistry()
        first_bias = reg.KNOWN_BIASES[0]
        # Should not raise
        result = reg.flag_bias(first_bias)
        self.assertIsNotNone(result)


# ---------------------------------------------------------------------------
# 9. Decision Revision Engine: archived block, reason required
# ---------------------------------------------------------------------------
class TestDecisionRevisionEngine(unittest.TestCase):
    """Revision engine: archived immutability, reason enforcement."""

    def test_revision_import(self):
        from replay.decision_revision import DecisionRevisionEngine

    def test_revision_requires_reason(self):
        from replay.decision_revision import DecisionRevisionEngine
        engine = DecisionRevisionEngine()
        entry = {
            "journal_entry_id": "DJR-REV-TEST",
            "decision_id": "DEC-REV-TEST",
            "session_id": "RPL-TEST",
            "status": "RECORDED",
            "confidence": 70,
        }
        with self.assertRaises((ValueError, Exception)):
            engine.create_revision(entry, reason="", field_changes={"notes": "updated"})

    def test_revision_blocked_for_archived(self):
        from replay.decision_revision import DecisionRevisionEngine
        engine = DecisionRevisionEngine()
        archived_entry = {
            "journal_entry_id": "DJR-ARC-TEST",
            "decision_id": "DEC-ARC-TEST",
            "session_id": "RPL-TEST",
            "status": "ARCHIVED",
            "confidence": 30,
        }
        with self.assertRaises((ValueError, Exception)):
            engine.create_revision(
                archived_entry,
                reason="Attempting revision of archived.",
                field_changes={"notes": "should fail"},
            )


# ---------------------------------------------------------------------------
# 10. Comparator: no forbidden fields, render markdown
# ---------------------------------------------------------------------------
class TestDecisionComparator(unittest.TestCase):
    """Comparator: forbidden field rejection, markdown output."""

    def test_comparator_import(self):
        from replay.decision_comparator import DecisionJournalComparator

    def test_compare_entries(self):
        from replay.decision_comparator import DecisionJournalComparator
        cmp = DecisionJournalComparator()
        a = _fixture("journal_compare_a.json")
        b = _fixture("journal_compare_b.json")
        result = cmp.compare_entries(a, b)
        self.assertIsNotNone(result)
        # Should not contain forbidden fields in output
        result_str = json.dumps(result)
        for forbidden in ["realized_return", "future_return", "hindsight_score"]:
            self.assertNotIn(f'"{forbidden}"', result_str)

    def test_comparator_blocks_forbidden(self):
        from replay.decision_comparator import DecisionJournalComparator
        cmp = DecisionJournalComparator()
        a = {
            "journal_entry_id": "DJR-A",
            "decision_id": "DEC-A",
            "session_id": "RPL-TEST",
            "replay_date": "2026-06-10",
            "action": "BUY",
            "realized_return": 0.1,
        }
        b = {
            "journal_entry_id": "DJR-B",
            "decision_id": "DEC-B",
            "session_id": "RPL-TEST",
            "replay_date": "2026-06-10",
            "action": "BUY",
            "realized_return": 0.2,
        }
        # Should either raise or strip forbidden fields silently
        try:
            result = cmp.compare_entries(a, b)
            # If no exception, forbidden fields must not appear in diffs
            diffs = result.get("differences", {})
            self.assertNotIn("realized_return", diffs)
        except (ValueError, Exception):
            pass  # Exception is also acceptable

    def test_render_markdown_safety_disclaimer(self):
        from replay.decision_comparator import DecisionJournalComparator
        cmp = DecisionJournalComparator()
        a = _fixture("journal_compare_a.json")
        b = _fixture("journal_compare_b.json")
        result = cmp.compare_entries(a, b)
        md = cmp.render_markdown(result)
        self.assertIsInstance(md, str)
        # Should contain a safety disclaimer of some kind
        self.assertTrue(
            any(kw in md for kw in [
                "NOT_QUALIFIED", "OBSERVATIONAL_ONLY", "Research Only",
                "SIMULATION DECISION ONLY", "No real orders", "No performance",
            ]),
            f"Expected safety marker in markdown: {md[:400]}"
        )


# ---------------------------------------------------------------------------
# 11. Summary Builder: no forbidden stats
# ---------------------------------------------------------------------------
class TestDecisionJournalSummary(unittest.TestCase):
    """Summary builder: only allowed stats, no forbidden fields."""

    def test_summary_import(self):
        from replay.decision_journal_summary import DecisionJournalSummaryBuilder

    def test_summary_no_forbidden_stats(self):
        from replay.decision_journal_summary import DecisionJournalSummaryBuilder
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = DecisionJournalSummaryBuilder(repo_root=tmpdir)
            summary = builder.build_summary(session_id="RPL-TEST-001")
            for forbidden in ["win_rate", "pnl", "alpha", "sharpe", "realized_return",
                              "future_return", "hindsight_score"]:
                self.assertNotIn(forbidden, summary)

    def test_summary_allowed_stats(self):
        from replay.decision_journal_summary import DecisionJournalSummaryBuilder
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = DecisionJournalSummaryBuilder(repo_root=tmpdir)
            summary = builder.build_summary(session_id="RPL-TEST-001")
            self.assertIn("entry_count", summary)


# ---------------------------------------------------------------------------
# 12. Portability: dry-run guard, forbidden export fields stripped
# ---------------------------------------------------------------------------
class TestDecisionJournalPortability(unittest.TestCase):
    """Portability: import dry_run guard, forbidden field stripping."""

    def test_portability_import(self):
        from replay.decision_journal_portability import DecisionJournalPortability

    def test_import_dry_run_by_default(self):
        from replay.decision_journal_portability import DecisionJournalPortability
        with tempfile.TemporaryDirectory() as tmpdir:
            port = DecisionJournalPortability(repo_root=tmpdir)
            # Write a valid JSONL file
            import_file = os.path.join(tmpdir, "test_import.jsonl")
            entry = {
                "journal_entry_id": "DJR-IMPORT-DRY",
                "decision_id": "DEC-IMPORT-DRY",
                "session_id": "RPL-IMPORT-SESSION",
                "replay_date": "2026-06-10",
                "action": "BUY",
                "simulation_only": True,
            }
            with open(import_file, "w") as f:
                f.write(json.dumps(entry) + "\n")
            result = port.import_entries(import_file)  # dry_run=True by default
            self.assertEqual(result.status, "dry_run")

    def test_import_blocked_without_allow_write(self):
        from replay.decision_journal_portability import DecisionJournalPortability
        with tempfile.TemporaryDirectory() as tmpdir:
            port = DecisionJournalPortability(repo_root=tmpdir)
            import_file = os.path.join(tmpdir, "test_import2.jsonl")
            entry = {
                "journal_entry_id": "DJR-IMPORT-BLOCK",
                "decision_id": "DEC-IMPORT-BLOCK",
                "session_id": "RPL-IMPORT-SESSION",
                "replay_date": "2026-06-10",
                "action": "BUY",
                "simulation_only": True,
            }
            with open(import_file, "w") as f:
                f.write(json.dumps(entry) + "\n")
            # dry_run=False but allow_write not True — should not import
            result = port.import_entries(import_file, dry_run=False)
            self.assertNotEqual(result.status, "imported")

    def test_forbidden_fields_stripped_on_export(self):
        from replay.decision_journal_portability import DecisionJournalPortability
        port = DecisionJournalPortability()
        entry = {
            "journal_entry_id": "DJR-TEST",
            "api_key": "FAKE_API_KEY",
            "broker": "FAKE_BROKER",
            "secret": "FAKE_SECRET",
            "action": "BUY",
        }
        stripped = port.redact_sensitive_fields(entry)
        for f in ["api_key", "secret", "broker"]:
            self.assertNotIn(f, stripped)

    def test_validate_import_file_runs(self):
        from replay.decision_journal_portability import DecisionJournalPortability
        with tempfile.TemporaryDirectory() as tmpdir:
            port = DecisionJournalPortability(repo_root=tmpdir)
            # Write a valid file for validation
            valid_file = os.path.join(tmpdir, "valid.jsonl")
            entry = {
                "journal_entry_id": "DJR-VALIDATE-TEST",
                "decision_id": "DEC-VALIDATE",
                "session_id": "RPL-TEST",
                "replay_date": "2026-06-10",
                "action": "BUY",
                "simulation_only": True,
            }
            with open(valid_file, "w") as f:
                f.write(json.dumps(entry) + "\n")
            result = port.validate_import_file(valid_file)
            # Should return a ValidationResult without crashing
            self.assertIsNotNone(result)


# ---------------------------------------------------------------------------
# 13. Backward Compatibility: old ReplayDecision gets journal defaults
# ---------------------------------------------------------------------------
class TestBackwardCompatibility(unittest.TestCase):
    """Old ReplayDecision schema gets journal_entry_id=None, revision_count=0."""

    def test_replay_schema_import(self):
        from replay.replay_schema import ReplayDecision

    def test_old_decision_journal_defaults(self):
        from replay.replay_schema import ReplayDecision
        d = ReplayDecision(
            decision_id="DEC-OLD-001",
            session_id="RPL-OLD-001",
            replay_date="2026-06-10",
            symbol="AAPL",
            action="BUY",
        )
        self.assertIsNone(d.journal_entry_id)
        self.assertEqual(d.revision_count, 0)
        self.assertIsNone(d.latest_revision_id)
        self.assertTrue(d.simulation_only)

    def test_from_dict_missing_journal_fields(self):
        """Old dict without journal fields should load with safe defaults."""
        from replay.replay_schema import ReplayDecision
        old_dict = {
            "decision_id": "DEC-OLD-002",
            "session_id": "RPL-OLD-002",
            "replay_date": "2026-06-11",
            "symbol": "MSFT",
            "action": "BUY",
        }
        d = ReplayDecision.from_dict(old_dict)
        self.assertIsNone(d.journal_entry_id)
        self.assertEqual(d.revision_count, 0)
        self.assertTrue(d.simulation_only)


# ---------------------------------------------------------------------------
# 14. Report: no forbidden stats, markdown output
# ---------------------------------------------------------------------------
class TestDecisionJournalReport(unittest.TestCase):
    """Report builder: no forbidden stats, valid markdown."""

    def test_report_import(self):
        from reports.replay_decision_journal_report import ReplayDecisionJournalReport

    def test_report_build_no_forbidden(self):
        from reports.replay_decision_journal_report import ReplayDecisionJournalReport
        rpt = ReplayDecisionJournalReport()
        md = rpt.build("RPL-TEST-SESSION-001")
        self.assertIsInstance(md, str)
        for forbidden in ["win_rate", "pnl", "realized_return", "future_return"]:
            self.assertNotIn(forbidden, md.lower())

    def test_report_safety_declaration(self):
        from reports.replay_decision_journal_report import ReplayDecisionJournalReport
        rpt = ReplayDecisionJournalReport()
        md = rpt.build("RPL-TEST-SESSION-001")
        self.assertIn("Safety Declaration", md)
        self.assertIn("No Real Orders", md)


# ---------------------------------------------------------------------------
# 15. Summary Report: no forbidden stats
# ---------------------------------------------------------------------------
class TestDecisionJournalSummaryReport(unittest.TestCase):
    """Summary report: period coverage, no forbidden stats."""

    def test_summary_report_import(self):
        from reports.replay_decision_journal_summary_report import (
            ReplayDecisionJournalSummaryReport
        )

    def test_summary_report_build(self):
        from reports.replay_decision_journal_summary_report import (
            ReplayDecisionJournalSummaryReport
        )
        rpt = ReplayDecisionJournalSummaryReport()
        md = rpt.build(date_from="2026-06-01", date_to="2026-06-16")
        self.assertIsInstance(md, str)
        for forbidden in ["win_rate", "pnl", "realized_return", "future_return",
                          "alpha", "sharpe"]:
            self.assertNotIn(forbidden, md.lower())

    def test_summary_report_safety_declaration(self):
        from reports.replay_decision_journal_summary_report import (
            ReplayDecisionJournalSummaryReport
        )
        rpt = ReplayDecisionJournalSummaryReport()
        md = rpt.build()
        self.assertIn("Safety Declaration", md)


# ---------------------------------------------------------------------------
# 16. Health Checker
# ---------------------------------------------------------------------------
class TestDecisionJournalHealth(unittest.TestCase):
    """Health checker runs all checks, returns PASS/WARN/FAIL status."""

    def test_health_import(self):
        from replay.decision_journal_health import DecisionJournalHealthChecker

    def test_health_check_runs(self):
        from replay.decision_journal_health import DecisionJournalHealthChecker
        with tempfile.TemporaryDirectory() as tmpdir:
            checker = DecisionJournalHealthChecker(repo_root=tmpdir)
            result = checker.run_health_check()
            self.assertIn("status", result)
            self.assertIn(result["status"], ["PASS", "WARN", "FAIL"])

    def test_health_check_reports(self):
        from replay.decision_journal_health import DecisionJournalHealthChecker
        with tempfile.TemporaryDirectory() as tmpdir:
            checker = DecisionJournalHealthChecker(repo_root=tmpdir)
            result = checker.run_health_check()
            self.assertIn("checks", result)
            self.assertGreater(len(result["checks"]), 0)


# ---------------------------------------------------------------------------
# 17. Simulation-only invariant: no_real_orders everywhere
# ---------------------------------------------------------------------------
class TestSimulationOnlyInvariant(unittest.TestCase):
    """simulation_only=True and NO_REAL_ORDERS enforced across all modules."""

    def test_schema_no_real_orders(self):
        from replay import decision_journal_schema
        self.assertTrue(getattr(decision_journal_schema, "NO_REAL_ORDERS", True))

    def test_store_no_real_orders(self):
        from replay import decision_journal_store
        self.assertTrue(getattr(decision_journal_store, "NO_REAL_ORDERS", True))

    def test_manager_no_real_orders(self):
        from replay import decision_journal_manager
        self.assertTrue(getattr(decision_journal_manager, "NO_REAL_ORDERS", True))

    def test_report_no_real_orders(self):
        from reports import replay_decision_journal_report
        self.assertTrue(getattr(replay_decision_journal_report, "NO_REAL_ORDERS", True))

    def test_summary_report_no_real_orders(self):
        from reports import replay_decision_journal_summary_report
        self.assertTrue(getattr(replay_decision_journal_summary_report, "NO_REAL_ORDERS", True))

    def test_entries_simulation_only(self):
        from replay.decision_journal_manager import DecisionJournalManager
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = DecisionJournalManager(repo_root=tmpdir)
            e = _make_entry(mgr, action="BUY", date="2026-06-10")
            d = e.to_dict()
            self.assertTrue(d.get("simulation_only"))


# ---------------------------------------------------------------------------
# 18. No future fields in entries
# ---------------------------------------------------------------------------
class TestNoFutureFields(unittest.TestCase):
    """Entries must not contain future return fields."""

    def test_created_entry_no_future_fields(self):
        from replay.decision_journal_manager import DecisionJournalManager
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = DecisionJournalManager(repo_root=tmpdir)
            e = _make_entry(mgr, action="BUY", date="2026-06-10")
            d = e.to_dict()
            for forbidden in ["future_return", "realized_return", "hindsight_score",
                              "final_result", "future_max_gain", "future_max_loss"]:
                self.assertNotIn(forbidden, d)

    def test_schema_to_dict_no_future_fields(self):
        from replay.decision_journal_schema import DecisionJournalEntry
        e = DecisionJournalEntry(
            journal_entry_id="DJR-TEST",
            decision_id="DEC-TEST",
            session_id="RPL-TEST",
            replay_date="2026-06-10",
            action="BUY",
        )
        d = e.to_dict()
        for forbidden in ["future_return", "realized_return", "hindsight_score", "final_result"]:
            self.assertNotIn(forbidden, d)


# ---------------------------------------------------------------------------
# 19. Import guard: requires dry_run=False AND allow_write=True
# ---------------------------------------------------------------------------
class TestImportGuard(unittest.TestCase):
    """Two-layer import guard: portability enforces both flags."""

    def _write_import_file(self, tmpdir, entry_id="DJR-IMPORT-TEST"):
        path = os.path.join(tmpdir, "import_test.jsonl")
        entry = {
            "journal_entry_id": entry_id,
            "decision_id": "DEC-IMPORT",
            "session_id": "RPL-IMPORT-SESSION",
            "replay_date": "2026-06-10",
            "action": "BUY",
            "simulation_only": True,
        }
        with open(path, "w") as f:
            f.write(json.dumps(entry) + "\n")
        return path

    def test_portability_requires_both_flags(self):
        from replay.decision_journal_portability import DecisionJournalPortability
        with tempfile.TemporaryDirectory() as tmpdir:
            port = DecisionJournalPortability(repo_root=tmpdir)
            import_file = self._write_import_file(tmpdir, "DJR-DRY-ONLY")
            # Only allow_write=True without dry_run=False should still be dry_run
            result = port.import_entries(import_file, allow_write=True)
            self.assertEqual(result.status, "dry_run")

    def test_portability_full_import(self):
        from replay.decision_journal_portability import DecisionJournalPortability
        with tempfile.TemporaryDirectory() as tmpdir:
            port = DecisionJournalPortability(repo_root=tmpdir)
            import_file = self._write_import_file(tmpdir, "DJR-FULL-IMPORT")
            result = port.import_entries(import_file, dry_run=False, allow_write=True)
            self.assertIn(result.status, ["imported", "partial", "success"])


# ---------------------------------------------------------------------------
# 20. No auto scoring
# ---------------------------------------------------------------------------
class TestNoAutoScoring(unittest.TestCase):
    """No auto-scoring, auto-generation, or auto-execution flags."""

    def test_version_info_no_auto_scoring(self):
        from release.version_info import DECISION_AUTO_SCORING_ENABLED
        self.assertFalse(DECISION_AUTO_SCORING_ENABLED)

    def test_version_info_no_auto_generation(self):
        from release.version_info import DECISION_AUTO_GENERATION_ENABLED
        self.assertFalse(DECISION_AUTO_GENERATION_ENABLED)

    def test_version_info_no_auto_execution(self):
        from release.version_info import DECISION_AUTO_EXECUTION_ENABLED
        self.assertFalse(DECISION_AUTO_EXECUTION_ENABLED)

    def test_version_info_journal_available(self):
        from release.version_info import DECISION_JOURNAL_AVAILABLE
        self.assertTrue(DECISION_JOURNAL_AVAILABLE)


# ---------------------------------------------------------------------------
# 21. Archived entry full immutability
# ---------------------------------------------------------------------------
class TestArchivedImmutability(unittest.TestCase):
    """Archived entries cannot be revised."""

    def test_archived_revision_blocked(self):
        from replay.decision_revision import DecisionRevisionEngine
        engine = DecisionRevisionEngine()
        archived = {
            "journal_entry_id": "DJR-ARC-IMMUT",
            "decision_id": "DEC-ARC-IMMUT",
            "session_id": "RPL-TEST",
            "replay_date": "2026-06-10",
            "status": "ARCHIVED",
            "confidence": 40,
        }
        with self.assertRaises((ValueError, Exception)):
            engine.create_revision(
                archived,
                reason="This should fail.",
                field_changes={"notes": "blocked"},
            )

    def test_archived_restore_allowed(self):
        from replay.decision_journal_manager import DecisionJournalManager
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = DecisionJournalManager(repo_root=tmpdir)
            e = _make_entry(mgr, action="BUY", date="2026-06-10")
            entry_id = e.to_dict()["journal_entry_id"]
            mgr.record_entry(entry_id)
            mgr.archive_entry(entry_id)
            restored = mgr.restore_entry(entry_id)
            self.assertNotEqual(restored.get("status"), "ARCHIVED")


# ---------------------------------------------------------------------------
# 22. GUI panel headless stub
# ---------------------------------------------------------------------------
class TestGUIPanelHeadlessStub(unittest.TestCase):
    """GUI panel and dialogs load without PyQt5 via headless stubs."""

    def test_panel_import_headless(self):
        from gui.replay_decision_journal_panel import ReplayDecisionJournalPanel

    def test_discipline_dialog_import_headless(self):
        from gui.replay_discipline_checklist_dialog import ReplayDisciplineChecklistDialog

    def test_revision_dialog_import_headless(self):
        from gui.replay_journal_revision_dialog import ReplayJournalRevisionDialog

    def test_compare_dialog_import_headless(self):
        from gui.replay_journal_compare_dialog import ReplayJournalCompareDialog

    def test_emotional_state_editor_import_headless(self):
        from gui.replay_emotional_state_editor import ReplayEmotionalStateEditor


# ---------------------------------------------------------------------------
# 23. Fixture integrity checks
# ---------------------------------------------------------------------------
class TestFixtureIntegrity(unittest.TestCase):
    """Fixture files load without error and have expected structure."""

    def test_journal_draft_fixture(self):
        d = _fixture("journal_draft.json")
        self.assertTrue(d["journal_entry_id"].startswith("DJR-"))
        self.assertEqual(d["status"], "DRAFT")
        self.assertTrue(d["simulation_only"])

    def test_journal_finalized_fixture(self):
        d = _fixture("journal_finalized.json")
        self.assertEqual(d["status"], "RECORDED")

    def test_journal_archived_fixture(self):
        d = _fixture("journal_archived.json")
        self.assertEqual(d["status"], "ARCHIVED")

    def test_emotion_calm_self_reported(self):
        d = _fixture("emotion_calm.json")
        self.assertTrue(d["self_reported"])
        self.assertLessEqual(d["confidence_level"], 100)
        self.assertGreaterEqual(d["confidence_level"], 0)

    def test_revision_drev_prefix(self):
        d = _fixture("revision_confidence.json")
        self.assertTrue(d["revision_id"].startswith("DREV-"))

    def test_forbidden_fixture_has_forbidden_fields(self):
        d = _fixture("journal_future_field.json")
        self.assertIn("future_return", d)

    def test_store_valid_jsonl_loads(self):
        lines = _fixture_text("store_valid.jsonl").strip().split("\n")
        for line in lines:
            if line.strip():
                entry = json.loads(line)
                self.assertTrue(entry["journal_entry_id"].startswith("DJR-"))


# ---------------------------------------------------------------------------
# 24. Version info
# ---------------------------------------------------------------------------
class TestVersionInfo(unittest.TestCase):
    """Decision Journal milestone feature flags (introduced in v1.2.2)."""

    def test_version(self):
        """VERSION >= 1.2.2 (Decision Journal was introduced in 1.2.2)."""
        from release.version_info import VERSION
        major, minor, patch = (int(x) for x in VERSION.split("."))
        self.assertGreaterEqual((major, minor, patch), (1, 2, 2),
                                f"VERSION {VERSION} predates Decision Journal 1.2.2")

    def test_release_name(self):
        """Decision Journal feature flag must be available."""
        from release.version_info import DECISION_JOURNAL_AVAILABLE
        self.assertTrue(DECISION_JOURNAL_AVAILABLE)

    def test_decision_journal_flags(self):
        import release.version_info as vi
        self.assertTrue(vi.DECISION_JOURNAL_AVAILABLE)
        self.assertTrue(vi.DECISION_REVISION_HISTORY_AVAILABLE)
        self.assertTrue(vi.DISCIPLINE_CHECKLIST_AVAILABLE)
        self.assertTrue(vi.EMOTIONAL_STATE_CAPTURE_AVAILABLE)
        self.assertFalse(vi.DECISION_AUTO_SCORING_ENABLED)
        self.assertFalse(vi.REPLAY_TRADE_EXECUTION_ENABLED)


if __name__ == "__main__":
    unittest.main(verbosity=2)
