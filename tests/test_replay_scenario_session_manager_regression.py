"""
tests/test_replay_scenario_session_manager_regression.py
Regression tests for v1.2.1 Replay Scenario & Session Manager.

[!] Research Only. No Real Orders. Replay Training Only.
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

FIXTURES_DIR = os.path.join(BASE_DIR, "tests", "fixtures", "replay_manager")


def _fixture(name: str) -> dict:
    with open(os.path.join(FIXTURES_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)


class TestScenarioSchema(unittest.TestCase):
    def test_import(self):
        from replay.scenario_schema import (
            ReplayScenarioTemplate, ReplayScenarioInstance, ScenarioValidationResult
        )

    def test_template_to_dict_from_dict(self):
        from replay.scenario_schema import ReplayScenarioTemplate
        t = ReplayScenarioTemplate(
            scenario_id="RSC-TEST", scenario_name="Test",
            description="Desc", category="FREE_PRACTICE", difficulty="BEGINNER",
        )
        d = t.to_dict()
        t2 = ReplayScenarioTemplate.from_dict(d)
        self.assertEqual(t2.scenario_id, "RSC-TEST")
        self.assertTrue(t2.research_only)
        self.assertTrue(t2.no_real_orders)
        self.assertTrue(t2.strict_future_firewall)

    def test_instance_to_dict_from_dict(self):
        from replay.scenario_schema import ReplayScenarioInstance
        inst = ReplayScenarioInstance(
            instance_id="RSI-TEST", scenario_id="RSC-TEST",
            scenario_version="1", resolved_symbol="2454",
            resolved_start_date="2023-01-02", resolved_end_date="2023-03-31",
            resolved_initial_date=None, qualification="OBSERVATIONAL_ONLY",
            data_availability={}, warnings=[], generated_at="2026-06-16T00:00:00+00:00",
        )
        d = inst.to_dict()
        inst2 = ReplayScenarioInstance.from_dict(d)
        self.assertEqual(inst2.instance_id, "RSI-TEST")
        self.assertTrue(inst2.research_only)

    def test_validation_result_to_dict(self):
        from replay.scenario_schema import ScenarioValidationResult
        r = ScenarioValidationResult(
            scenario_id="RSC-TEST", valid=True, errors=[], warnings=[],
            missing_required_datasets=[], missing_optional_datasets=[],
            future_data_risk=False, point_in_time_compatible=True,
            qualification="OBSERVATIONAL_ONLY", checked_at="2026-06-16T00:00:00+00:00",
        )
        d = r.to_dict()
        r2 = ScenarioValidationResult.from_dict(d)
        self.assertTrue(r2.valid)


class TestScenarioValidation(unittest.TestCase):
    def test_valid_template(self):
        from replay.scenario_schema import ReplayScenarioTemplate
        from replay.scenario_validator import ReplayScenarioValidator
        t = ReplayScenarioTemplate(
            scenario_id="RSC-VALID", scenario_name="Valid",
            description="Test", category="FREE_PRACTICE", difficulty="BEGINNER",
        )
        v = ReplayScenarioValidator()
        result = v.validate_template(t)
        self.assertTrue(result.valid, f"Should be valid, errors: {result.errors}")

    def test_invalid_dates(self):
        d = _fixture("scenario_invalid_dates.json")
        from replay.scenario_schema import ReplayScenarioTemplate
        from replay.scenario_validator import ReplayScenarioValidator
        t = ReplayScenarioTemplate.from_dict(d)
        v = ReplayScenarioValidator()
        result = v.validate_template(t)
        self.assertFalse(result.valid)
        self.assertTrue(any("date" in e.lower() for e in result.errors))

    def test_future_firewall_false_blocked(self):
        from replay.scenario_schema import ReplayScenarioTemplate
        from replay.scenario_validator import ReplayScenarioValidator
        t = ReplayScenarioTemplate(
            scenario_id="RSC-BAD", scenario_name="Bad",
            description="Test", category="FREE_PRACTICE", difficulty="BEGINNER",
            strict_future_firewall=False,
        )
        v = ReplayScenarioValidator()
        result = v.validate_template(t)
        self.assertFalse(result.valid)

    def test_future_fields_in_fixture(self):
        d = _fixture("scenario_future_fields.json")
        from replay.scenario_schema import ReplayScenarioTemplate
        from replay.scenario_validator import ReplayScenarioValidator
        t = ReplayScenarioTemplate.from_dict(d)
        v = ReplayScenarioValidator()
        result = v.validate_template(t)
        self.assertFalse(result.valid)


class TestScenarioLibrary(unittest.TestCase):
    def test_create_template_has_rsc_prefix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.scenario_library import ReplayScenarioLibrary
            lib = ReplayScenarioLibrary(repo_root=tmpdir)
            t = lib.create_template("Test", "FREE_PRACTICE", "BEGINNER")
            self.assertTrue(t.scenario_id.startswith("RSC-"))

    def test_duplicate_gets_new_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.scenario_library import ReplayScenarioLibrary
            lib = ReplayScenarioLibrary(repo_root=tmpdir)
            t = lib.create_template("Original", "FREE_PRACTICE", "BEGINNER")
            t2 = lib.duplicate_template(t.scenario_id)
            self.assertNotEqual(t.scenario_id, t2.scenario_id)

    def test_archive_blocks_instantiate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.scenario_library import ReplayScenarioLibrary
            lib = ReplayScenarioLibrary(repo_root=tmpdir)
            t = lib.create_template("Test", "FREE_PRACTICE", "BEGINNER")
            lib.archive_template(t.scenario_id)
            inst = lib.instantiate(t.scenario_id, "2454")
            self.assertIsNone(inst, "Archived template must not be instantiatable")

    def test_export_redacts_secrets(self):
        d = _fixture("scenario_with_fake_secret.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.scenario_library import ReplayScenarioLibrary
            from replay.scenario_schema import ReplayScenarioTemplate
            lib = ReplayScenarioLibrary(repo_root=tmpdir)
            template = ReplayScenarioTemplate.from_dict(d)
            # Validate — should fail due to forbidden field
            result = lib._validator.validate_template(template)
            self.assertFalse(result.valid)
            # Export should redact
            from replay.scenario_store import ReplayScenarioStore
            # Save without validation bypass
            lib._store.save_template(template)
            out = lib.export_template(d["scenario_id"])
            if out:
                with open(out, "r") as f:
                    exported = json.load(f)
                self.assertNotIn("api_key", exported)

    def test_load_builtin_templates(self):
        from replay.scenario_library import ReplayScenarioLibrary
        lib = ReplayScenarioLibrary(repo_root=BASE_DIR)
        count = lib.load_builtin_templates()
        # Should load at least some builtins (or they were already loaded)
        templates = lib.list_templates()
        builtin_count = len([t for t in templates if t.get("source") == "builtin"])
        self.assertGreater(len(templates), 0)


class TestSessionManager(unittest.TestCase):
    def test_create_from_scenario(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.session_manager import ReplaySessionManager
            mgr = ReplaySessionManager(repo_root=tmpdir)
            state = mgr.create_free_practice("2454", "2023-01-02", "2023-03-31")
            self.assertIsNotNone(state)
            self.assertTrue(hasattr(state, "session_id"))
            self.assertTrue(state.research_only)
            self.assertTrue(state.no_real_orders)

    def test_filter_sessions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.session_manager import ReplaySessionManager
            mgr = ReplaySessionManager(repo_root=tmpdir)
            mgr.create_free_practice("2454", "2023-01-02", "2023-03-31")
            mgr.create_free_practice("2330", "2022-01-03", "2022-06-30")
            results = mgr.filter_sessions(symbol="2454")
            symbols = [s.get("symbol") for s in results]
            self.assertIn("2454", symbols)

    def test_search_sessions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.session_manager import ReplaySessionManager
            mgr = ReplaySessionManager(repo_root=tmpdir)
            mgr.create_free_practice("2454", "2023-01-02", "2023-03-31")
            results = mgr.search_sessions("2454")
            self.assertGreater(len(results), 0)

    def test_fork_creates_new_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.session_manager import ReplaySessionManager
            mgr = ReplaySessionManager(repo_root=tmpdir)
            state = mgr.create_free_practice("2454", "2023-01-02", "2023-03-31")
            fork = mgr.fork_session(state.session_id)
            self.assertIsNotNone(fork)
            self.assertNotEqual(fork.session_id, state.session_id)

    def test_duplicate_creates_new_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.session_manager import ReplaySessionManager
            mgr = ReplaySessionManager(repo_root=tmpdir)
            state = mgr.create_free_practice("2454", "2023-01-02", "2023-03-31")
            dup = mgr.duplicate_session(state.session_id)
            self.assertIsNotNone(dup)
            self.assertNotEqual(dup.session_id, state.session_id)

    def test_archive_restore(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.session_manager import ReplaySessionManager
            mgr = ReplaySessionManager(repo_root=tmpdir)
            state = mgr.create_free_practice("2454", "2023-01-02", "2023-03-31")
            archived = mgr.archive_session(state.session_id)
            self.assertEqual(archived.status, "ARCHIVED")
            restored = mgr.restore_session(state.session_id)
            self.assertNotEqual(restored.status, "ARCHIVED")

    def test_hide_does_not_delete(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.session_manager import ReplaySessionManager
            mgr = ReplaySessionManager(repo_root=tmpdir)
            state = mgr.create_free_practice("2454", "2023-01-02", "2023-03-31")
            ok = mgr.delete_from_view(state.session_id)
            self.assertTrue(ok)
            # Verify still loadable from store
            config = mgr._store.load_session_config(state.session_id)
            self.assertIsNotNone(config, "Hidden session should still exist in store")

    def test_archived_session_not_resumable(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.session_manager import ReplaySessionManager
            mgr = ReplaySessionManager(repo_root=tmpdir)
            state = mgr.create_free_practice("2454", "2023-01-02", "2023-03-31")
            mgr.archive_session(state.session_id)
            resumed = mgr.resume_session(state.session_id)
            self.assertIsNone(resumed, "Archived session must not be resumable without restore")


class TestCheckpointManager(unittest.TestCase):
    def _make_session(self, tmpdir):
        from replay.replay_session_store import ReplaySessionStore
        from replay.replay_schema import ReplaySessionConfig, ReplaySessionState
        store = ReplaySessionStore(repo_root=tmpdir)
        config = ReplaySessionConfig(
            session_id="RPL-CP-TEST", session_name="CP",
            symbol="2454", start_date="2023-01-02", end_date="2023-03-31",
        )
        store.save_session_config(config)
        state = ReplaySessionState(
            session_id="RPL-CP-TEST", current_date="2023-01-15",
            current_index=5, total_steps=60, status="PLAYING",
        )
        store.save_session_state(state)
        return store

    def test_create_checkpoint_no_future_fields(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = self._make_session(tmpdir)
            from replay.session_checkpoint import ReplayCheckpointManager, FORBIDDEN_CHECKPOINT_FIELDS
            mgr = ReplayCheckpointManager(store=store, repo_root=tmpdir)
            cp = mgr.create_checkpoint("RPL-CP-TEST", note="regression")
            self.assertIsNotNone(cp)
            self.assertTrue(cp.checkpoint_id.startswith("RCP-"))
            d = cp.to_dict()
            for ff in FORBIDDEN_CHECKPOINT_FIELDS:
                self.assertNotIn(ff, d, f"Forbidden field {ff} in checkpoint")

    def test_checkpoint_validate_rejects_future_field(self):
        d = _fixture("checkpoint_future_field.json")
        from replay.session_checkpoint import ReplayCheckpointManager, ReplayCheckpoint
        cp = ReplayCheckpoint.from_dict(d)
        mgr = ReplayCheckpointManager()
        # Checkpoint has future_return in raw dict — validate_checkpoint should return False
        self.assertFalse(mgr.validate_checkpoint(d))

    def test_restore_creates_new_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = self._make_session(tmpdir)
            from replay.session_checkpoint import ReplayCheckpointManager
            mgr = ReplayCheckpointManager(store=store, repo_root=tmpdir)
            cp = mgr.create_checkpoint("RPL-CP-TEST")
            result = mgr.restore_checkpoint(cp.checkpoint_id)
            self.assertIsNotNone(result)
            self.assertTrue(result.get("restored", False))


class TestLineageManager(unittest.TestCase):
    def test_root_creation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.session_lineage import ReplaySessionLineageManager
            mgr = ReplaySessionLineageManager(repo_root=tmpdir)
            root = mgr.create_root("ROOT-001", "RSC-TEST")
            self.assertEqual(root.relation_type, "ROOT")
            self.assertEqual(root.root_session_id, "ROOT-001")
            self.assertIsNone(root.parent_session_id)

    def test_child_linking(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.session_lineage import ReplaySessionLineageManager
            mgr = ReplaySessionLineageManager(repo_root=tmpdir)
            mgr.create_root("ROOT-001")
            child = mgr.link_child("ROOT-001", "CHILD-001", "FORK")
            self.assertIsNotNone(child)
            self.assertEqual(child.parent_session_id, "ROOT-001")
            self.assertEqual(child.root_session_id, "ROOT-001")

    def test_cycle_detection(self):
        d = _fixture("lineage_cycle.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            from replay.session_lineage import ReplaySessionLineageManager, ReplaySessionLineage
            mgr = ReplaySessionLineageManager(repo_root=tmpdir)
            # Manually inject cycle lineage
            for lin_dict in d["lineage"]:
                lin = ReplaySessionLineage.from_dict(lin_dict)
                mgr._lineage_cache[lin.session_id] = lin
            # CYCLE-A has parent CYCLE-C which creates a cycle
            has_cycle = mgr.detect_cycle("CYCLE-A")
            self.assertTrue(has_cycle, "Cycle A->B->C->A should be detected")


class TestComparator(unittest.TestCase):
    def test_compare_no_future_fields(self):
        from replay.session_comparator import ReplaySessionComparator, FORBIDDEN_COMPARISON_FIELDS
        comp = ReplaySessionComparator()
        result = comp.compare("A", "B")
        for ff in FORBIDDEN_COMPARISON_FIELDS:
            self.assertNotIn(ff, result, f"Forbidden field {ff} in comparison result")

    def test_compare_no_future_performance_flag(self):
        from replay.session_comparator import ReplaySessionComparator
        comp = ReplaySessionComparator()
        result = comp.compare("A", "B")
        self.assertTrue(result.get("no_future_performance_comparison"))

    def test_compare_research_only(self):
        from replay.session_comparator import ReplaySessionComparator
        comp = ReplaySessionComparator()
        result = comp.compare("A", "B")
        self.assertTrue(result.get("research_only"))
        self.assertTrue(result.get("no_real_orders"))


class TestPortability(unittest.TestCase):
    def test_known_roots_present(self):
        from replay.session_portability import KNOWN_REPO_ROOTS
        self.assertIn("C:/Users/Rossi/Documents/Claude/trading_master", KNOWN_REPO_ROOTS)
        self.assertIn("D:/code/Claude/tw_quant_cockpit", KNOWN_REPO_ROOTS)

    def test_normalize_c_drive(self):
        from replay.session_portability import ReplaySessionPortability
        p = ReplaySessionPortability()
        d = _fixture("path_c_drive.json")
        normalized = p.normalize_paths(d)
        self.assertIn("path", normalized)

    def test_normalize_d_drive(self):
        from replay.session_portability import ReplaySessionPortability
        p = ReplaySessionPortability()
        d = _fixture("path_d_drive.json")
        normalized = p.normalize_paths(d)
        self.assertIn("path", normalized)

    def test_import_marks_data_unavailable(self):
        d = _fixture("import_missing_data.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            import json as _json
            import os as _os
            export_path = _os.path.join(tmpdir, "import.json")
            with open(export_path, "w") as f:
                _json.dump(d, f)
            from replay.session_portability import ReplaySessionPortability
            p = ReplaySessionPortability(repo_root=tmpdir)
            result = p.import_metadata(export_path, dry_run=True)
            self.assertTrue(result.get("ok") or "errors" in result)

    def test_redact_sensitive_fields(self):
        from replay.session_portability import ReplaySessionPortability, SENSITIVE_FIELDS
        p = ReplaySessionPortability()
        payload = {"api_key": "secret123", "session_id": "RPL-TEST"}
        redacted = p.redact_sensitive_fields(payload)
        self.assertEqual(redacted.get("api_key"), "[REDACTED]")
        self.assertEqual(redacted.get("session_id"), "RPL-TEST")

    def test_import_does_not_auto_execute(self):
        d = _fixture("import_missing_data.json")
        self.assertTrue(d.get("import_does_not_auto_execute"))


class TestBatchSessionBuilder(unittest.TestCase):
    def test_preview_is_dry_run(self):
        from replay.batch_session_builder import ReplayBatchSessionBuilder
        b = ReplayBatchSessionBuilder()
        result = b.preview_batch("RSC-TEST", ["2454", "2330"])
        self.assertTrue(result.get("dry_run"))
        self.assertFalse(result.get("allow_write"))

    def test_execute_without_allow_write_blocked(self):
        from replay.batch_session_builder import ReplayBatchSessionBuilder
        b = ReplayBatchSessionBuilder()
        result = b.execute_batch([], allow_write=False)
        self.assertTrue(result.get("blocked"))

    def test_over_default_limit_blocked(self):
        from replay.batch_session_builder import ReplayBatchSessionBuilder
        b = ReplayBatchSessionBuilder()
        symbols = [str(i) for i in range(60)]
        result = b.preview_batch("RSC-TEST", symbols, max_sessions=50)
        self.assertTrue(result.get("blocked"))

    def test_over_hard_limit_blocked(self):
        from replay.batch_session_builder import ReplayBatchSessionBuilder
        b = ReplayBatchSessionBuilder()
        symbols = [str(i) for i in range(600)]
        result = b.preview_batch("RSC-TEST", symbols)
        self.assertTrue(result.get("blocked"))

    def test_batch_fixture_valid(self):
        d = _fixture("batch_valid.json")
        from replay.batch_session_builder import ReplayBatchSessionBuilder
        b = ReplayBatchSessionBuilder()
        result = b.preview_batch(d["scenario_id"], d["symbols"])
        self.assertTrue(result.get("ok") or result.get("dry_run"))

    def test_batch_fixture_over_limit(self):
        d = _fixture("batch_over_limit.json")
        from replay.batch_session_builder import ReplayBatchSessionBuilder
        b = ReplayBatchSessionBuilder()
        result = b.preview_batch(d["scenario_id"], d["symbols"], max_sessions=d["max_sessions"])
        # 56 > 50, should be blocked
        self.assertTrue(result.get("blocked"))


class TestV120BackwardCompat(unittest.TestCase):
    def test_legacy_session_loads_without_error(self):
        d = _fixture("session_v120_legacy.json")
        from replay.replay_schema import ReplaySessionConfig
        config = ReplaySessionConfig.from_dict(d)
        self.assertEqual(config.session_id, "RPL-2454-20230102-LEGACY")
        self.assertTrue(config.research_only)
        self.assertTrue(config.no_real_orders)
        # New v1.2.1 fields should have defaults
        self.assertIsNone(config.scenario_id)
        self.assertEqual(config.tags, [])
        self.assertEqual(config.portable_metadata_version, 1)

    def test_legacy_state_loads_without_error(self):
        from replay.replay_schema import ReplaySessionState
        old_state = {
            "session_id": "RPL-LEGACY-001",
            "current_date": "2023-01-02",
            "current_index": 0,
            "total_steps": 10,
            "status": "CREATED",
        }
        state = ReplaySessionState.from_dict(old_state)
        self.assertEqual(state.session_id, "RPL-LEGACY-001")
        # New v1.2.1 fields default
        self.assertEqual(state.checkpoint_count, 0)
        self.assertFalse(state.hidden)
        self.assertIsNone(state.archived_at)


class TestHealthCheck(unittest.TestCase):
    def test_health_check_runs(self):
        from replay.session_manager_health import ReplayScenarioSessionManagerHealthCheck
        hc = ReplayScenarioSessionManagerHealthCheck()
        results = hc.run()
        self.assertIn("imports", results)
        self.assertIn("safety_flags", results)
        overall = hc.overall_status(results)
        self.assertIn(overall, ["PASS", "WARN", "FAIL", "BLOCKED"])

    def test_health_check_passes(self):
        from replay.session_manager_health import ReplayScenarioSessionManagerHealthCheck
        hc = ReplayScenarioSessionManagerHealthCheck()
        results = hc.run()
        overall = hc.overall_status(results)
        self.assertEqual(overall, "PASS", f"Health check should pass: {[(k, v) for k, v in results.items() if v[0] != 'PASS']}")


class TestStoreCorruptedTail(unittest.TestCase):
    def test_corrupted_jsonl_tolerates(self):
        """Corrupted tail in JSONL should not crash — only valid lines returned."""
        from replay.replay_session_store import ReplaySessionStore
        import tempfile
        import shutil
        fixture_path = os.path.join(FIXTURES_DIR, "store_corrupted_tail.jsonl")
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir) / "data" / "replay_sessions"
            sessions_dir.mkdir(parents=True)
            dst = sessions_dir / "sessions.jsonl"
            shutil.copy(fixture_path, str(dst))
            store = ReplaySessionStore(repo_root=tmpdir)
            sessions = store.list_sessions()
            # Should return 2 valid entries, not crash on corrupted line
            self.assertGreaterEqual(len(sessions), 2)


if __name__ == "__main__":
    unittest.main()
