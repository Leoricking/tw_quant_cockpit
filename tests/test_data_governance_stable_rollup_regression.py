"""
tests/test_data_governance_stable_rollup_regression.py
Regression tests for Data Governance Stable Rollup v1.1.9

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Uses TST symbols only. Fixed test clock. Isolated tmpdir.
[!] Does NOT write to production stores.
"""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

# Fixed test clock
TEST_CLOCK = datetime(2026, 1, 15, 9, 0, 0, tzinfo=timezone.utc)
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "governance_rollup"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fixture(name: str) -> Path:
    return FIXTURES_DIR / name


def _load_json(name: str) -> dict:
    with open(_fixture(name), "r", encoding="utf-8") as f:
        return json.load(f)


# ===========================================================================
# rollup_schema: dataclass instantiation and to_dict/from_dict
# ===========================================================================

class TestRollupSchema:
    def test_module_consistency_result_instantiation(self):
        from governance_rollup.rollup_schema import ModuleConsistencyResult
        result = ModuleConsistencyResult(
            module_name="universe",
            available=True,
            schema_version="1.1.9",
            expected_version="1.1.9",
        )
        assert result.module_name == "universe"
        assert result.research_only is True
        assert result.no_real_orders is True

    def test_module_consistency_result_to_dict_from_dict(self):
        from governance_rollup.rollup_schema import ModuleConsistencyResult
        r = ModuleConsistencyResult(module_name="test", available=True,
                                     schema_version="1.1.9")
        d = r.to_dict()
        assert d["module_name"] == "test"
        assert d["research_only"] is True
        r2 = ModuleConsistencyResult.from_dict(d)
        assert r2.module_name == "test"
        assert r2.research_only is True

    def test_store_inventory_record_instantiation(self):
        from governance_rollup.rollup_schema import StoreInventoryRecord
        rec = StoreInventoryRecord(
            store_id="TEST_STORE",
            module_name="universe",
            exists=True,
            readable=True,
        )
        assert rec.store_id == "TEST_STORE"
        assert rec.corruption_detected is False

    def test_store_inventory_record_to_dict_from_dict(self):
        from governance_rollup.rollup_schema import StoreInventoryRecord
        rec = StoreInventoryRecord(store_id="S1", module_name="test", exists=True)
        d = rec.to_dict()
        assert d["store_id"] == "S1"
        rec2 = StoreInventoryRecord.from_dict(d)
        assert rec2.store_id == "S1"

    def test_recovery_plan_instantiation(self):
        from governance_rollup.rollup_schema import RecoveryPlan
        plan = RecoveryPlan(plan_id="PLAN-001", store_id="S1", module_name="test")
        assert plan.dry_run is True
        assert plan.requires_allow_write is True

    def test_recovery_plan_to_dict_from_dict(self):
        from governance_rollup.rollup_schema import RecoveryPlan
        plan = RecoveryPlan(plan_id="PLAN-001", store_id="S1", module_name="test")
        d = plan.to_dict()
        assert d["dry_run"] is True
        plan2 = RecoveryPlan.from_dict(d)
        assert plan2.plan_id == "PLAN-001"
        assert plan2.dry_run is True

    def test_cross_module_consistency_summary_to_dict_from_dict(self):
        from governance_rollup.rollup_schema import CrossModuleConsistencySummary
        s = CrossModuleConsistencySummary(modules_checked=5, modules_pass=4)
        d = s.to_dict()
        assert d["research_only"] is True
        s2 = CrossModuleConsistencySummary.from_dict(d)
        assert s2.modules_checked == 5
        assert s2.research_only is True

    def test_stable_rollup_summary_to_dict_from_dict(self):
        from governance_rollup.rollup_schema import StableRollupSummary
        s = StableRollupSummary(overall_status="PASS", stable_ready=True)
        d = s.to_dict()
        assert d["version"] == "1.1.9"
        assert d["research_only"] is True
        assert d["no_real_orders"] is True
        s2 = StableRollupSummary.from_dict(d)
        assert s2.overall_status == "PASS"
        assert s2.stable_ready is True


# ===========================================================================
# schema_normalizer
# ===========================================================================

class TestSchemaNormalizer:
    def setup_method(self):
        from governance_rollup.schema_normalizer import GovernanceSchemaNormalizer
        self.normalizer = GovernanceSchemaNormalizer()

    def test_normalize_symbol_uppercase(self):
        assert self.normalizer.normalize_symbol("tst001") == "TST001"

    def test_normalize_symbol_strips_whitespace(self):
        assert self.normalizer.normalize_symbol("  TST002  ") == "TST002"

    def test_normalize_symbol_none(self):
        assert self.normalizer.normalize_symbol(None) == "UNKNOWN"

    def test_normalize_symbol_empty(self):
        assert self.normalizer.normalize_symbol("") == "UNKNOWN"

    def test_normalize_qualification_demo_only_stays(self):
        """DEMO_ONLY must NOT be promoted to FORMALLY_QUALIFIED."""
        result = self.normalizer.normalize_qualification("DEMO_ONLY")
        assert result == "DEMO_ONLY"

    def test_normalize_qualification_blocked_stays(self):
        """BLOCKED must NOT be reclassified."""
        result = self.normalizer.normalize_qualification("BLOCKED")
        assert result == "BLOCKED"

    def test_normalize_qualification_formally_qualified(self):
        result = self.normalizer.normalize_qualification("FORMALLY_QUALIFIED")
        assert result == "FORMALLY_QUALIFIED"

    def test_normalize_qualification_not_qualified(self):
        result = self.normalizer.normalize_qualification("NOT_QUALIFIED")
        assert result == "NOT_QUALIFIED"

    def test_normalize_qualification_unknown(self):
        result = self.normalizer.normalize_qualification("SOME_UNKNOWN_VALUE")
        assert result == "UNKNOWN"

    def test_normalize_tier_research30(self):
        assert self.normalizer.normalize_tier("research30") == "research30"
        assert self.normalizer.normalize_tier("top30") == "research30"

    def test_normalize_tier_unknown(self):
        assert self.normalizer.normalize_tier("invalid_tier") == "UNKNOWN"

    def test_normalize_bool_strict(self):
        """Missing bool must NOT be treated as True."""
        assert self.normalizer.normalize_bool(None) is None
        assert self.normalizer.normalize_bool(True) is True
        assert self.normalizer.normalize_bool(False) is False
        assert self.normalizer.normalize_bool("maybe") is None

    def test_normalize_timestamp_iso(self):
        result = self.normalizer.normalize_timestamp("2026-01-15T09:00:00")
        assert result is not None
        assert "2026" in result

    def test_normalize_timestamp_none(self):
        result = self.normalizer.normalize_timestamp(None)
        assert result is None

    def test_validate_normalized_impossible_state(self):
        record = {"status": "BLOCKED", "qualification": "FORMALLY_QUALIFIED"}
        result = self.normalizer.validate_normalized(record)
        assert result["valid"] is False
        assert any("BLOCKED" in i and "FORMALLY_QUALIFIED" in i
                   for i in result["issues"])

    def test_validate_normalized_no_real_orders_false(self):
        record = {"no_real_orders": False}
        result = self.normalizer.validate_normalized(record)
        assert result["valid"] is False

    def test_unknown_fields_preserved(self):
        """Unknown fields must be preserved, not dropped."""
        data = _load_json("unknown_fields.json")
        normalized = self.normalizer.normalize_record(data, "test_schema")
        assert "unknown_field_xyz" in normalized
        assert normalized["unknown_field_xyz"] == "keep_me"


# ===========================================================================
# path_normalizer
# ===========================================================================

class TestPathNormalizer:
    def setup_method(self):
        from governance_rollup.path_normalizer import CrossMachinePathNormalizer
        self.normalizer = CrossMachinePathNormalizer()

    def test_d_drive_path_classification(self):
        data = _load_json("path_d_drive.json")
        result = self.normalizer.to_repo_relative(data["path"])
        assert result["classification"] in (
            "CROSS_MACHINE_REPO_RELATIVE", "REPO_RELATIVE", "EXTERNAL_LOCAL_PATH"
        )
        # Should have relative path extracted
        if result["classification"] == "CROSS_MACHINE_REPO_RELATIVE":
            assert result["relative_path"] is not None

    def test_c_drive_path_classification(self):
        data = _load_json("path_c_drive.json")
        result = self.normalizer.to_repo_relative(data["path"])
        assert result["classification"] in (
            "REPO_RELATIVE", "CROSS_MACHINE_REPO_RELATIVE", "EXTERNAL_LOCAL_PATH"
        )

    def test_external_path_classification(self):
        data = _load_json("path_external.json")
        result = self.normalizer.to_repo_relative(data["path"])
        assert result["classification"] == "EXTERNAL_LOCAL_PATH"
        assert result["relative_path"] is None

    def test_relative_path_classification(self):
        result = self.normalizer.to_repo_relative("data/test/file.jsonl")
        assert result["classification"] == "ALREADY_RELATIVE"

    def test_normalize_separator(self):
        result = self.normalizer.normalize_separator("D:\\code\\Claude\\test.json")
        assert "\\" not in result
        assert "/" in result

    def test_portable_path_record(self):
        record = self.normalizer.portable_path_record("data/test/file.jsonl")
        assert record["classification"] == "ALREADY_RELATIVE"
        assert record["portable"] is True

    def test_portable_path_external(self):
        record = self.normalizer.portable_path_record("C:/Users/Rossi/Desktop/file.csv")
        assert record["classification"] == "EXTERNAL_LOCAL_PATH"
        assert record["portable"] is False


# ===========================================================================
# store_inventory
# ===========================================================================

class TestStoreInventory:
    def test_discover_stores_returns_list(self):
        from governance_rollup.store_inventory import GovernanceStoreInventory
        inv = GovernanceStoreInventory()
        stores = inv.discover_stores()
        assert isinstance(stores, list)

    def test_classify_store_jsonl(self):
        from governance_rollup.store_inventory import GovernanceStoreInventory
        from governance_rollup.rollup_schema import STORE_TYPE_JSONL
        inv = GovernanceStoreInventory()
        path = Path("some_file.jsonl")
        assert inv.classify_store(path) == STORE_TYPE_JSONL

    def test_classify_store_json(self):
        from governance_rollup.store_inventory import GovernanceStoreInventory
        from governance_rollup.rollup_schema import STORE_TYPE_JSON
        inv = GovernanceStoreInventory()
        assert inv.classify_store(Path("file.json")) == STORE_TYPE_JSON

    def test_classify_store_csv(self):
        from governance_rollup.store_inventory import GovernanceStoreInventory
        from governance_rollup.rollup_schema import STORE_TYPE_CSV
        inv = GovernanceStoreInventory()
        assert inv.classify_store(Path("file.csv")) == STORE_TYPE_CSV

    def test_inspect_store_existing(self, tmp_path):
        from governance_rollup.store_inventory import GovernanceStoreInventory
        inv = GovernanceStoreInventory(base_dir=tmp_path)
        store_file = tmp_path / "test_store.jsonl"
        store_file.write_text('{"id": "1"}\n', encoding="utf-8")
        record = inv.inspect_store(store_file)
        assert record.exists is True
        assert record.readable is True
        assert record.store_type == "JSONL"

    def test_count_records_jsonl(self, tmp_path):
        from governance_rollup.store_inventory import GovernanceStoreInventory
        inv = GovernanceStoreInventory()
        f = tmp_path / "test.jsonl"
        f.write_text('{"a": 1}\n{"b": 2}\n{"c": 3}\n', encoding="utf-8")
        count = inv.count_records(f)
        assert count == 3

    def test_does_not_scan_env(self):
        """Inventory should never include .env files."""
        from governance_rollup.store_inventory import GovernanceStoreInventory
        inv = GovernanceStoreInventory()
        stores = inv.discover_stores()
        for path in stores:
            assert ".env" not in str(path).lower() or "env.example" in str(path).lower()


# ===========================================================================
# store_validator
# ===========================================================================

class TestStoreValidator:
    def test_valid_jsonl(self):
        from governance_rollup.store_validator import GovernanceStoreValidator
        validator = GovernanceStoreValidator()
        result = validator.validate_jsonl(_fixture("valid_store.jsonl"))
        assert result["valid"] is True
        assert result["status"] == "VALID"

    def test_corrupted_tail_detection(self):
        """Corrupted last line = CORRUPTED_TAIL, NOT truncated."""
        from governance_rollup.store_validator import GovernanceStoreValidator
        validator = GovernanceStoreValidator()
        result = validator.validate_jsonl(_fixture("corrupted_tail.jsonl"))
        assert result["corrupted_tail"] is True
        assert result["status"] == "CORRUPTED_TAIL"
        assert result["valid"] is False

    def test_corrupted_middle_detection(self):
        """Middle corruption = CORRUPTED_MIDDLE."""
        from governance_rollup.store_validator import GovernanceStoreValidator
        validator = GovernanceStoreValidator()
        result = validator.validate_jsonl(_fixture("corrupted_middle.jsonl"))
        assert result["corrupted_middle"] is True
        assert result["status"] == "CORRUPTED_MIDDLE"

    def test_valid_json(self, tmp_path):
        from governance_rollup.store_validator import GovernanceStoreValidator
        validator = GovernanceStoreValidator()
        f = tmp_path / "test.json"
        f.write_text('{"key": "value"}', encoding="utf-8")
        result = validator.validate_json(f)
        assert result["valid"] is True

    def test_malformed_json(self, tmp_path):
        from governance_rollup.store_validator import GovernanceStoreValidator
        validator = GovernanceStoreValidator()
        f = tmp_path / "bad.json"
        f.write_text('{bad json}', encoding="utf-8")
        result = validator.validate_json(f)
        assert result["valid"] is False
        assert "MALFORMED" in result["status"]

    def test_validate_safety_flags_pass(self):
        from governance_rollup.store_validator import GovernanceStoreValidator
        validator = GovernanceStoreValidator()
        result = validator.validate_safety_flags(
            {"research_only": True, "no_real_orders": True}
        )
        assert result["valid"] is True

    def test_validate_safety_flags_fail(self):
        from governance_rollup.store_validator import GovernanceStoreValidator
        data = _load_json("safety_mismatch.json")
        validator = GovernanceStoreValidator()
        result = validator.validate_safety_flags(data)
        assert result["valid"] is False


# ===========================================================================
# store_recovery
# ===========================================================================

class TestStoreRecovery:
    def test_preview_dry_run(self):
        """Preview must be dry-run only, no writes."""
        from governance_rollup.store_recovery import GovernanceStoreRecoveryPlanner
        planner = GovernanceStoreRecoveryPlanner()
        plan = planner.plan({"path": "test.jsonl", "status": "CORRUPTED_TAIL",
                              "store_id": "TEST", "module_name": "test"})
        preview = planner.preview(plan.plan_id)
        assert preview["dry_run"] is True
        assert preview["status"] != "COMPLETED"

    def test_execute_without_allow_write_blocked(self):
        """Execute without allow_write must be BLOCKED."""
        from governance_rollup.store_recovery import GovernanceStoreRecoveryPlanner
        planner = GovernanceStoreRecoveryPlanner()
        plan = planner.plan({"path": "test.jsonl", "status": "CORRUPTED_TAIL",
                              "store_id": "TEST", "module_name": "test"})
        result = planner.execute(plan.plan_id, allow_write=False)
        assert result["status"] == "BLOCKED"

    def test_rebuild_state_blocked_without_allow_write(self):
        from governance_rollup.store_recovery import GovernanceStoreRecoveryPlanner
        planner = GovernanceStoreRecoveryPlanner()
        result = planner.rebuild_state("/tmp/test.json", allow_write=False)
        assert result.get("status") == "BLOCKED"

    def test_rollback_blocked_without_allow_write(self):
        from governance_rollup.store_recovery import GovernanceStoreRecoveryPlanner
        planner = GovernanceStoreRecoveryPlanner()
        result = planner.rollback_recovery("/tmp/bak.bak", "/tmp/target.json",
                                            allow_write=False)
        assert result.get("status") == "BLOCKED"


# ===========================================================================
# index_rebuilder
# ===========================================================================

class TestIndexRebuilder:
    def test_supported_indexes(self):
        from governance_rollup.index_rebuilder import GovernanceIndexRebuilder
        rebuilder = GovernanceIndexRebuilder()
        indexes = rebuilder.supported_indexes()
        assert "research_registry" in indexes
        assert len(indexes) > 0

    def test_preview_rebuild_dry_run(self):
        from governance_rollup.index_rebuilder import GovernanceIndexRebuilder
        rebuilder = GovernanceIndexRebuilder()
        preview = rebuilder.preview_rebuild("research_registry")
        assert preview["dry_run"] is True

    def test_rebuild_without_allow_write_dry_run_only(self):
        """Rebuild without allow_write must be dry-run only (not execute)."""
        from governance_rollup.index_rebuilder import GovernanceIndexRebuilder
        rebuilder = GovernanceIndexRebuilder()
        result = rebuilder.rebuild("research_registry", allow_write=False)
        # Must not have written anything
        assert result.get("dry_run") is True or result.get("status") == "DRY_RUN_ONLY"

    def test_rebuild_unsupported_module(self):
        from governance_rollup.index_rebuilder import GovernanceIndexRebuilder
        rebuilder = GovernanceIndexRebuilder()
        result = rebuilder.rebuild("totally_unknown_module", allow_write=False)
        assert result.get("status") == "UNSUPPORTED"


# ===========================================================================
# metadata_migrator
# ===========================================================================

class TestMetadataMigrator:
    def test_detect_version_explicit(self):
        from governance_rollup.metadata_migrator import GovernanceMetadataMigrator
        migrator = GovernanceMetadataMigrator()
        record = {"schema_version": "1.1.5", "gate_enforcement": True}
        assert migrator.detect_version(record) == "1.1.5"

    def test_detect_version_heuristic(self):
        from governance_rollup.metadata_migrator import GovernanceMetadataMigrator
        migrator = GovernanceMetadataMigrator()
        record = _load_json("schema_v110.json")
        version = migrator.detect_version(record)
        assert version in ("1.1.0", "UNKNOWN")

    def test_preview_migration_dry_run(self):
        from governance_rollup.metadata_migrator import GovernanceMetadataMigrator
        migrator = GovernanceMetadataMigrator()
        preview = migrator.preview_migration("test_module")
        assert preview["dry_run"] is True

    def test_execute_without_allow_write_blocked(self):
        """Migration without allow_write must be BLOCKED."""
        from governance_rollup.metadata_migrator import GovernanceMetadataMigrator
        migrator = GovernanceMetadataMigrator()
        result = migrator.execute_migration("test_module", allow_write=False)
        assert result["status"] == "BLOCKED"

    def test_rollback_blocked_without_allow_write(self):
        from governance_rollup.metadata_migrator import GovernanceMetadataMigrator
        migrator = GovernanceMetadataMigrator()
        result = migrator.rollback_migration("/tmp/bak.bak", "/tmp/target.json",
                                              allow_write=False)
        assert result["status"] == "BLOCKED"

    def test_forbidden_ohlcv_not_migrated(self, tmp_path):
        """OHLCV financial fields must NEVER be migrated."""
        from governance_rollup.metadata_migrator import GovernanceMetadataMigrator
        migrator = GovernanceMetadataMigrator()
        src = tmp_path / "test.json"
        src.write_text(
            json.dumps({"close": 100.0, "volume": 5000, "symbol": "TST001"}),
            encoding="utf-8",
        )
        dest = tmp_path / "test_migrated.json"
        result = migrator.migrate_copy(str(src), str(dest))
        if result.get("success"):
            with open(dest, "r", encoding="utf-8") as f:
                migrated = json.load(f)
            # close and volume should be preserved but not modified
            if isinstance(migrated, list):
                migrated = migrated[0]
            assert migrated.get("close") == 100.0
            assert migrated.get("volume") == 5000


# ===========================================================================
# consistency_checker: impossible state detection
# ===========================================================================

class TestConsistencyChecker:
    def test_impossible_state_blocked_formally_qualified(self):
        """BLOCKED + FORMALLY_QUALIFIED is an impossible state."""
        data = _load_json("impossible_qualification.json")
        assert data["status"] == "BLOCKED"
        assert data["qualification"] == "FORMALLY_QUALIFIED"
        # Verify the normalizer catches this
        from governance_rollup.schema_normalizer import GovernanceSchemaNormalizer
        normalizer = GovernanceSchemaNormalizer()
        result = normalizer.validate_normalized(data)
        assert result["valid"] is False
        assert any("BLOCKED" in i and "FORMALLY_QUALIFIED" in i for i in result["issues"])

    def test_impossible_state_no_real_orders_false(self):
        """no_real_orders=False is a safety mismatch."""
        data = _load_json("safety_mismatch.json")
        assert data["no_real_orders"] is False
        from governance_rollup.schema_normalizer import GovernanceSchemaNormalizer
        normalizer = GovernanceSchemaNormalizer()
        result = normalizer.validate_normalized(data)
        assert result["valid"] is False

    def test_check_safety_flags_runs(self):
        from governance_rollup.consistency_checker import CrossModuleConsistencyChecker
        checker = CrossModuleConsistencyChecker()
        result = checker.check_safety_flags()
        assert "issues" in result
        assert "modules_checked" in result

    def test_check_impossible_states_runs(self):
        from governance_rollup.consistency_checker import CrossModuleConsistencyChecker
        checker = CrossModuleConsistencyChecker()
        result = checker.check_impossible_states()
        assert "impossible_states" in result
        assert "count" in result

    def test_run_all_returns_summary(self):
        from governance_rollup.consistency_checker import CrossModuleConsistencyChecker
        from governance_rollup.rollup_schema import CrossModuleConsistencySummary
        checker = CrossModuleConsistencyChecker()
        summary = checker.run_all()
        assert isinstance(summary, CrossModuleConsistencySummary)
        assert summary.research_only is True
        assert summary.no_real_orders is True


# ===========================================================================
# health_aggregator
# ===========================================================================

class TestHealthAggregator:
    def test_import_health_aggregator(self):
        from governance_rollup.health_aggregator import GovernanceHealthAggregator
        agg = GovernanceHealthAggregator()
        assert agg.RESEARCH_ONLY is True
        assert agg.NO_REAL_ORDERS is True

    def test_health_commands_defined(self):
        from governance_rollup.health_aggregator import GovernanceHealthAggregator
        agg = GovernanceHealthAggregator()
        assert len(agg.HEALTH_COMMANDS) > 0

    def test_known_warning_not_fail(self):
        from governance_rollup.health_aggregator import GovernanceHealthAggregator
        agg = GovernanceHealthAggregator()
        # "no real orders" is a known warning, must not cause FAIL
        assert agg.known_warning_policy("test_module", "no real orders") is True
        assert agg.known_warning_policy("test_module", "BLOCKED: allow_write=False") is True

    def test_run_all_returns_dict(self):
        from governance_rollup.health_aggregator import GovernanceHealthAggregator
        agg = GovernanceHealthAggregator()
        result = agg.run_all(mode="real")
        assert isinstance(result, dict)
        assert "overall_status" in result
        assert result.get("research_only") is True


# ===========================================================================
# rollup_engine: run returns StableRollupSummary
# ===========================================================================

class TestRollupEngine:
    def test_run_returns_stable_rollup_summary(self, tmp_path):
        """Engine run must return a StableRollupSummary."""
        from governance_rollup.stable_rollup_engine import DataGovernanceStableRollupEngine
        from governance_rollup.rollup_schema import StableRollupSummary
        engine = DataGovernanceStableRollupEngine()
        summary = engine.run(mode="real")
        assert isinstance(summary, StableRollupSummary)
        assert summary.version == "1.1.9"
        assert summary.research_only is True
        assert summary.no_real_orders is True

    def test_engine_safety_constants(self):
        from governance_rollup.stable_rollup_engine import DataGovernanceStableRollupEngine
        engine = DataGovernanceStableRollupEngine()
        assert engine.RESEARCH_ONLY is True
        assert engine.NO_REAL_ORDERS is True


# ===========================================================================
# safety checks: no trade execution, no auto repair, no auto import
# ===========================================================================

class TestSafetyGuards:
    def test_no_trade_execution(self):
        import governance_rollup
        assert getattr(governance_rollup, "TRADE_EXECUTION_ENABLED", True) is False

    def test_no_auto_repair(self):
        import governance_rollup
        assert getattr(governance_rollup, "AUTO_STORE_REPAIR_ENABLED", True) is False
        assert getattr(governance_rollup, "AUTO_DATA_REPAIR_ENABLED", True) is False

    def test_no_auto_import(self):
        import governance_rollup
        assert getattr(governance_rollup, "AUTO_DATA_IMPORT_ENABLED", True) is False

    def test_no_auto_download(self):
        import governance_rollup
        assert getattr(governance_rollup, "AUTO_DATA_DOWNLOAD_ENABLED", True) is False

    def test_no_real_orders(self):
        import governance_rollup
        assert getattr(governance_rollup, "NO_REAL_ORDERS", False) is True

    def test_research_only(self):
        import governance_rollup
        assert getattr(governance_rollup, "RESEARCH_ONLY", False) is True

    def test_store_recovery_planner_no_auto(self):
        """Recovery planner must NOT auto-execute without allow_write."""
        from governance_rollup.store_recovery import GovernanceStoreRecoveryPlanner
        planner = GovernanceStoreRecoveryPlanner()
        result = planner.execute("nonexistent", allow_write=False)
        assert result["status"] == "BLOCKED"

    def test_metadata_migrator_no_auto(self):
        """Migrator must NOT auto-execute without allow_write."""
        from governance_rollup.metadata_migrator import GovernanceMetadataMigrator
        migrator = GovernanceMetadataMigrator()
        result = migrator.execute_migration("test", allow_write=False)
        assert result["status"] == "BLOCKED"

    def test_index_rebuilder_no_auto_write(self):
        """Index rebuilder must NOT write without allow_write."""
        from governance_rollup.index_rebuilder import GovernanceIndexRebuilder
        rebuilder = GovernanceIndexRebuilder()
        result = rebuilder.rebuild("research_registry", allow_write=False)
        assert result.get("dry_run") is True or result.get("status") == "DRY_RUN_ONLY"

    def test_rollup_store_runtime_files_not_committed(self):
        """Runtime output files should be excluded from git."""
        gitignore = Path(__file__).parent.parent / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text(encoding="utf-8", errors="replace")
            assert "data/governance_rollup/" in content


# ===========================================================================
# rollup_schema: from_dict roundtrip from fixture files
# ===========================================================================

class TestFixtureRoundtrip:
    def test_rollup_a_fixture_roundtrip(self):
        from governance_rollup.rollup_schema import StableRollupSummary
        data = _load_json("rollup_a.json")
        s = StableRollupSummary.from_dict(data)
        assert s.overall_status == "PASS"
        assert s.stable_ready is True
        assert s.research_only is True
        assert s.no_real_orders is True

    def test_rollup_b_fixture_roundtrip(self):
        from governance_rollup.rollup_schema import StableRollupSummary
        data = _load_json("rollup_b.json")
        s = StableRollupSummary.from_dict(data)
        assert s.overall_status == "WARN"
        assert s.stable_ready is True
        assert len(s.known_warnings) > 0
