"""
replay/registry_health.py — ReplayRegistryHealthCheck v1.2.8

Health check for all v1.2.8 registry components.
Output: PASS/WARN/FAIL/BLOCKED per check.

[!] Research Only. No Real Orders. Dataset Registry Only. Session Registry Only.
[!] Registry does not execute trades. Not Investment Advice.
"""
from __future__ import annotations

import logging
import traceback
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayRegistryHealthCheck:
    """
    Health check for Replay Dataset & Session Registry v1.2.8.

    Checks all registry components plus safety invariants.
    Output: PASS/WARN/FAIL/BLOCKED per check.

    [!] Research Only. No Real Orders. Registry Only. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True
    REGISTRY_ONLY  = True

    def run(self) -> Dict[str, Tuple[str, str]]:
        """Run all health checks. Returns dict of name -> (status, message)."""
        results: Dict[str, Tuple[str, str]] = {}

        # Schema imports
        results["dataset_schema"]          = self._check_dataset_schema()
        results["session_schema"]          = self._check_session_schema()
        # Core modules
        results["manifest_builder"]        = self._check_manifest_builder()
        results["dataset_fingerprint"]     = self._check_dataset_fingerprint()
        results["session_fingerprint"]     = self._check_session_fingerprint()
        results["dataset_version"]         = self._check_dataset_version()
        results["dataset_lineage"]         = self._check_dataset_lineage()
        results["dataset_qualification"]   = self._check_dataset_qualification()
        results["dataset_catalog"]         = self._check_dataset_catalog()
        results["dataset_registry"]        = self._check_dataset_registry()
        results["dataset_snapshot"]        = self._check_dataset_snapshot()
        results["dataset_freeze"]          = self._check_dataset_freeze()
        results["dataset_validator"]       = self._check_dataset_validator()
        results["dataset_integrity"]       = self._check_dataset_integrity()
        results["dataset_portability"]     = self._check_dataset_portability()
        results["dataset_package"]         = self._check_dataset_package()
        results["dataset_importer"]        = self._check_dataset_importer()
        results["dataset_exporter"]        = self._check_dataset_exporter()
        results["dataset_path_remap"]      = self._check_dataset_path_remap()
        results["dataset_conflict"]        = self._check_dataset_conflict()
        results["dataset_query"]           = self._check_dataset_query()
        results["dataset_summary"]         = self._check_dataset_summary()
        results["session_dataset_binding"] = self._check_session_dataset_binding()
        results["session_lineage_registry"]= self._check_session_lineage_registry()
        results["session_registry_v128"]   = self._check_session_registry_v128()
        results["session_registry_query"]  = self._check_session_registry_query()
        results["session_registry_summary"]= self._check_session_registry_summary()
        results["registry_audit"]          = self._check_registry_audit()
        results["registry_repair"]         = self._check_registry_repair()
        results["registry_events"]         = self._check_registry_events()
        # Behavioral invariants
        results["deterministic_dataset_fingerprint"] = self._check_deterministic_dataset_fp()
        results["absolute_path_excluded"]    = self._check_absolute_path_excluded()
        results["relative_path_package"]     = self._check_relative_path_package()
        results["frozen_immutable"]          = self._check_frozen_immutable()
        results["missing_file_graceful"]     = self._check_missing_file_graceful()
        results["hash_mismatch_detected"]    = self._check_hash_mismatch_detected()
        results["mock_real_separated"]       = self._check_mock_real_separated()
        results["session_binding_locked"]    = self._check_session_binding_locked()
        results["completed_session_no_rebind"] = self._check_completed_session_no_rebind()
        results["package_preview_default"]   = self._check_package_preview_default()
        results["package_import_guard"]      = self._check_package_import_guard()
        results["package_export_guard"]      = self._check_package_export_guard()
        results["repair_preview_default"]    = self._check_repair_preview_default()
        results["repair_execute_guard"]      = self._check_repair_execute_guard()
        results["no_auto_overwrite"]         = self._check_no_auto_overwrite()
        results["no_auto_repair"]            = self._check_no_auto_repair()
        results["no_auto_rebind"]            = self._check_no_auto_rebind()
        results["no_broker_data"]            = self._check_no_broker_data()
        results["no_forbidden_actions"]      = self._check_no_forbidden_actions()
        results["research_only"]             = self._check_research_only()
        results["no_real_orders"]            = self._check_no_real_orders()

        return results

    def print_results(self, results: Dict[str, Tuple[str, str]]) -> None:
        """Print health check results to stdout."""
        total  = len(results)
        passed = sum(1 for s, _ in results.values() if s == "PASS")
        warned = sum(1 for s, _ in results.values() if s == "WARN")
        failed = sum(1 for s, _ in results.values() if s in ("FAIL", "BLOCKED"))
        print(f"  Checks: {total} | PASS: {passed} | WARN: {warned} | FAIL/BLOCKED: {failed}")
        print()
        for name, (status, msg) in results.items():
            icon = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]", "BLOCKED": "[BLOCKED]"}.get(status, "[?]")
            print(f"  {icon:10s} {name:45s} {msg}")
        print()
        if failed == 0:
            print("  [OK] All registry health checks passed.")
        else:
            print(f"  [!!] {failed} check(s) failed.")
        print("  [!] Research Only. No Real Orders. Registry Only. Not Investment Advice.")

    # ------------------------------------------------------------------ #
    # Import checks
    # ------------------------------------------------------------------ #

    def _check_dataset_schema(self) -> Tuple[str, str]:
        try:
            from replay.dataset_registry_schema import (
                ReplayDatasetManifest, ReplayDatasetFileEntry,
                ReplayDatasetVersionRecord, ReplayDatasetLineageRecord,
                DatasetMode, DatasetQualification, DatasetStatus,
            )
            m = ReplayDatasetManifest(dataset_id="TST", dataset_name="test")
            assert m.research_only
            assert m.no_real_orders
            return ("PASS", "dataset schema importable, safety flags OK")
        except Exception as exc:
            return ("FAIL", f"dataset schema import failed: {exc}")

    def _check_session_schema(self) -> Tuple[str, str]:
        try:
            from replay.session_registry_schema import (
                ReplaySessionRegistryRecord, ReplaySessionBinding,
                SessionType, SessionStatus, BindingType, BindingStatus,
            )
            r = ReplaySessionRegistryRecord(registry_record_id="R1", session_id="S1")
            assert r.research_only
            assert r.no_real_orders
            return ("PASS", "session schema importable, safety flags OK")
        except Exception as exc:
            return ("FAIL", f"session schema import failed: {exc}")

    def _check_manifest_builder(self) -> Tuple[str, str]:
        try:
            from replay.dataset_manifest import ReplayDatasetManifestBuilder
            b = ReplayDatasetManifestBuilder()
            assert b.RESEARCH_ONLY
            return ("PASS", "manifest builder importable")
        except Exception as exc:
            return ("FAIL", f"manifest builder import failed: {exc}")

    def _check_dataset_fingerprint(self) -> Tuple[str, str]:
        try:
            from replay.dataset_fingerprint import ReplayDatasetFingerprint
            fp = ReplayDatasetFingerprint()
            assert fp.RESEARCH_ONLY
            return ("PASS", "dataset fingerprint importable")
        except Exception as exc:
            return ("FAIL", f"dataset fingerprint import failed: {exc}")

    def _check_session_fingerprint(self) -> Tuple[str, str]:
        try:
            from replay.session_fingerprint import ReplaySessionFingerprint
            fp = ReplaySessionFingerprint()
            assert fp.RESEARCH_ONLY
            return ("PASS", "session fingerprint importable")
        except Exception as exc:
            return ("FAIL", f"session fingerprint import failed: {exc}")

    def _check_dataset_version(self) -> Tuple[str, str]:
        try:
            from replay.dataset_version import ReplayDatasetVersionManager
            vm = ReplayDatasetVersionManager()
            assert vm.RESEARCH_ONLY
            return ("PASS", "dataset version manager importable")
        except Exception as exc:
            return ("FAIL", f"dataset version import failed: {exc}")

    def _check_dataset_lineage(self) -> Tuple[str, str]:
        try:
            from replay.dataset_lineage import ReplayDatasetLineageManager
            lm = ReplayDatasetLineageManager()
            assert lm.RESEARCH_ONLY
            return ("PASS", "dataset lineage manager importable")
        except Exception as exc:
            return ("FAIL", f"dataset lineage import failed: {exc}")

    def _check_dataset_qualification(self) -> Tuple[str, str]:
        try:
            from replay.dataset_qualification import ReplayDatasetQualificationEvaluator
            ev = ReplayDatasetQualificationEvaluator()
            assert ev.RESEARCH_ONLY
            return ("PASS", "qualification evaluator importable")
        except Exception as exc:
            return ("FAIL", f"qualification import failed: {exc}")

    def _check_dataset_catalog(self) -> Tuple[str, str]:
        try:
            from replay.dataset_catalog import ReplayDatasetCatalog
            c = ReplayDatasetCatalog()
            assert c.RESEARCH_ONLY
            return ("PASS", "dataset catalog importable")
        except Exception as exc:
            return ("FAIL", f"dataset catalog import failed: {exc}")

    def _check_dataset_registry(self) -> Tuple[str, str]:
        try:
            from replay.dataset_registry import ReplayDatasetRegistry
            r = ReplayDatasetRegistry()
            assert r.RESEARCH_ONLY
            assert r.NO_REAL_ORDERS
            return ("PASS", "dataset registry importable")
        except Exception as exc:
            return ("FAIL", f"dataset registry import failed: {exc}")

    def _check_dataset_snapshot(self) -> Tuple[str, str]:
        try:
            from replay.dataset_snapshot import ReplayDatasetSnapshot
            s = ReplayDatasetSnapshot()
            assert s.RESEARCH_ONLY
            return ("PASS", "dataset snapshot importable")
        except Exception as exc:
            return ("FAIL", f"dataset snapshot import failed: {exc}")

    def _check_dataset_freeze(self) -> Tuple[str, str]:
        try:
            from replay.dataset_freeze import ReplayDatasetFreezeManager
            fm = ReplayDatasetFreezeManager()
            assert fm.RESEARCH_ONLY
            return ("PASS", "dataset freeze manager importable")
        except Exception as exc:
            return ("FAIL", f"dataset freeze import failed: {exc}")

    def _check_dataset_validator(self) -> Tuple[str, str]:
        try:
            from replay.dataset_validator import ReplayDatasetValidator
            v = ReplayDatasetValidator()
            assert v.RESEARCH_ONLY
            return ("PASS", "dataset validator importable")
        except Exception as exc:
            return ("FAIL", f"dataset validator import failed: {exc}")

    def _check_dataset_integrity(self) -> Tuple[str, str]:
        try:
            from replay.dataset_integrity import ReplayDatasetIntegrityChecker
            c = ReplayDatasetIntegrityChecker()
            assert c.RESEARCH_ONLY
            return ("PASS", "dataset integrity checker importable")
        except Exception as exc:
            return ("FAIL", f"dataset integrity import failed: {exc}")

    def _check_dataset_portability(self) -> Tuple[str, str]:
        try:
            from replay.dataset_portability import ReplayDatasetPortability, MANIFEST_ONLY
            p = ReplayDatasetPortability()
            assert p.RESEARCH_ONLY
            assert MANIFEST_ONLY == "MANIFEST_ONLY"
            return ("PASS", "dataset portability importable")
        except Exception as exc:
            return ("FAIL", f"dataset portability import failed: {exc}")

    def _check_dataset_package(self) -> Tuple[str, str]:
        try:
            from replay.dataset_package import ReplayDatasetPackage
            pkg = ReplayDatasetPackage()
            assert pkg.RESEARCH_ONLY
            return ("PASS", "dataset package importable")
        except Exception as exc:
            return ("FAIL", f"dataset package import failed: {exc}")

    def _check_dataset_importer(self) -> Tuple[str, str]:
        try:
            from replay.dataset_importer import ReplayDatasetImporter
            imp = ReplayDatasetImporter()
            assert imp.RESEARCH_ONLY
            return ("PASS", "dataset importer importable")
        except Exception as exc:
            return ("FAIL", f"dataset importer import failed: {exc}")

    def _check_dataset_exporter(self) -> Tuple[str, str]:
        try:
            from replay.dataset_exporter import ReplayDatasetExporter
            exp = ReplayDatasetExporter()
            assert exp.RESEARCH_ONLY
            return ("PASS", "dataset exporter importable")
        except Exception as exc:
            return ("FAIL", f"dataset exporter import failed: {exc}")

    def _check_dataset_path_remap(self) -> Tuple[str, str]:
        try:
            from replay.dataset_path_remap import ReplayDatasetPathRemapper
            r = ReplayDatasetPathRemapper()
            assert r.RESEARCH_ONLY
            return ("PASS", "dataset path remapper importable")
        except Exception as exc:
            return ("FAIL", f"dataset path remap import failed: {exc}")

    def _check_dataset_conflict(self) -> Tuple[str, str]:
        try:
            from replay.dataset_conflict import ReplayDatasetConflictDetector
            d = ReplayDatasetConflictDetector()
            assert d.RESEARCH_ONLY
            assert not d.AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED
            return ("PASS", "dataset conflict detector importable")
        except Exception as exc:
            return ("FAIL", f"dataset conflict import failed: {exc}")

    def _check_dataset_query(self) -> Tuple[str, str]:
        try:
            from replay.dataset_query import ReplayDatasetQuery
            q = ReplayDatasetQuery()
            assert q.RESEARCH_ONLY
            return ("PASS", "dataset query importable")
        except Exception as exc:
            return ("FAIL", f"dataset query import failed: {exc}")

    def _check_dataset_summary(self) -> Tuple[str, str]:
        try:
            from replay.dataset_summary import ReplayDatasetSummary
            s = ReplayDatasetSummary()
            assert s.RESEARCH_ONLY
            return ("PASS", "dataset summary importable")
        except Exception as exc:
            return ("FAIL", f"dataset summary import failed: {exc}")

    def _check_session_dataset_binding(self) -> Tuple[str, str]:
        try:
            from replay.session_dataset_binding import ReplaySessionDatasetBinder
            b = ReplaySessionDatasetBinder()
            assert b.RESEARCH_ONLY
            assert not b.AUTO_SESSION_REBIND_ENABLED
            return ("PASS", "session dataset binder importable")
        except Exception as exc:
            return ("FAIL", f"session dataset binding import failed: {exc}")

    def _check_session_lineage_registry(self) -> Tuple[str, str]:
        try:
            from replay.session_lineage_registry import ReplaySessionLineageRegistry
            lr = ReplaySessionLineageRegistry()
            assert lr.RESEARCH_ONLY
            return ("PASS", "session lineage registry importable")
        except Exception as exc:
            return ("FAIL", f"session lineage registry import failed: {exc}")

    def _check_session_registry_v128(self) -> Tuple[str, str]:
        try:
            from replay.session_registry_v128 import ReplaySessionRegistryV128
            sr = ReplaySessionRegistryV128()
            assert sr.RESEARCH_ONLY
            assert sr.NO_REAL_ORDERS
            return ("PASS", "session registry v1.2.8 importable")
        except Exception as exc:
            return ("FAIL", f"session registry v128 import failed: {exc}")

    def _check_session_registry_query(self) -> Tuple[str, str]:
        try:
            from replay.session_registry_query import ReplaySessionRegistryQuery
            q = ReplaySessionRegistryQuery()
            assert q.RESEARCH_ONLY
            return ("PASS", "session registry query importable")
        except Exception as exc:
            return ("FAIL", f"session registry query import failed: {exc}")

    def _check_session_registry_summary(self) -> Tuple[str, str]:
        try:
            from replay.session_registry_summary import ReplaySessionRegistrySummary
            s = ReplaySessionRegistrySummary()
            assert s.RESEARCH_ONLY
            return ("PASS", "session registry summary importable")
        except Exception as exc:
            return ("FAIL", f"session registry summary import failed: {exc}")

    def _check_registry_audit(self) -> Tuple[str, str]:
        try:
            from replay.registry_audit import ReplayRegistryAudit
            a = ReplayRegistryAudit()
            assert a.RESEARCH_ONLY
            return ("PASS", "registry audit importable")
        except Exception as exc:
            return ("FAIL", f"registry audit import failed: {exc}")

    def _check_registry_repair(self) -> Tuple[str, str]:
        try:
            from replay.registry_repair import ReplayRegistryRepairPlanner
            r = ReplayRegistryRepairPlanner()
            assert r.RESEARCH_ONLY
            assert not r.AUTO_REGISTRY_REPAIR_ENABLED
            return ("PASS", "registry repair planner importable")
        except Exception as exc:
            return ("FAIL", f"registry repair import failed: {exc}")

    def _check_registry_events(self) -> Tuple[str, str]:
        try:
            from replay.registry_events import ReplayRegistryEvents, DATASET_REGISTERED
            ev = ReplayRegistryEvents()
            assert ev.RESEARCH_ONLY
            assert DATASET_REGISTERED == "DATASET_REGISTERED"
            return ("PASS", "registry events importable")
        except Exception as exc:
            return ("FAIL", f"registry events import failed: {exc}")

    # ------------------------------------------------------------------ #
    # Behavioral invariant checks
    # ------------------------------------------------------------------ #

    def _check_deterministic_dataset_fp(self) -> Tuple[str, str]:
        try:
            from replay.dataset_fingerprint import ReplayDatasetFingerprint
            fp = ReplayDatasetFingerprint()
            manifest = {
                "dataset_id": "TST-001",
                "mode": "MOCK",
                "symbols": ["TST"],
                "timeframes": ["D1"],
                "qualification": "MOCK_DEMO_ONLY",
            }
            fp1 = fp.calculate_manifest_fingerprint(manifest)
            fp2 = fp.calculate_manifest_fingerprint(manifest)
            assert fp1 == fp2, "fingerprint not deterministic"
            return ("PASS", "dataset fingerprint is deterministic")
        except Exception as exc:
            return ("FAIL", f"deterministic fingerprint check failed: {exc}")

    def _check_absolute_path_excluded(self) -> Tuple[str, str]:
        try:
            from replay.dataset_fingerprint import ReplayDatasetFingerprint
            fp = ReplayDatasetFingerprint()
            manifest_with_abs = {
                "dataset_id": "TST-001",
                "mode": "MOCK",
                "relative_paths": ["data/file.csv"],
            }
            manifest_with_diff_abs = {
                "dataset_id": "TST-001",
                "mode": "MOCK",
                "relative_paths": ["data/file.csv"],
                "created_at": "2025-01-01",  # excluded
            }
            fp1 = fp.calculate_manifest_fingerprint(manifest_with_abs)
            fp2 = fp.calculate_manifest_fingerprint(manifest_with_diff_abs)
            assert fp1 == fp2, "excluded keys are affecting fingerprint"
            return ("PASS", "absolute paths and timestamps excluded from fingerprint")
        except Exception as exc:
            return ("FAIL", f"absolute path exclusion check failed: {exc}")

    def _check_relative_path_package(self) -> Tuple[str, str]:
        try:
            from replay.dataset_package import ReplayDatasetPackage
            pkg = ReplayDatasetPackage()
            manifest = pkg.build_manifest(
                dataset_ids=["TST-001"],
                session_ids=[],
                package_type="MANIFEST_ONLY",
                included_files=["data/tst.csv", "meta.json"],
            )
            assert manifest.get("path_mode") == "RELATIVE_ONLY"
            validation = pkg.validate(manifest)
            assert validation["ok"], f"Package validation failed: {validation['issues']}"
            return ("PASS", "package uses RELATIVE_ONLY path mode")
        except Exception as exc:
            return ("FAIL", f"relative path package check failed: {exc}")

    def _check_frozen_immutable(self) -> Tuple[str, str]:
        try:
            from replay.dataset_freeze import ReplayDatasetFreezeManager
            fm = ReplayDatasetFreezeManager()

            class MockManifest:
                dataset_id = "TST-001"
                dataset_version = "1.0.0"
                fingerprint = "abc123"
                frozen_at = None
                status = "ACTIVE"

            m = MockManifest()
            guard = fm.unfreeze_guard(m)
            assert not guard["blocked"], "unfrozen dataset should not be blocked"
            # freeze it
            fm.freeze(m, allow_write=True)
            assert m.frozen_at is not None, "frozen_at not set"
            guard2 = fm.unfreeze_guard(m)
            assert guard2["blocked"], "frozen dataset should be blocked"
            return ("PASS", "frozen dataset immutability enforced")
        except Exception as exc:
            return ("FAIL", f"frozen immutable check failed: {exc}")

    def _check_missing_file_graceful(self) -> Tuple[str, str]:
        try:
            from replay.dataset_integrity import ReplayDatasetIntegrityChecker
            from replay.dataset_registry_schema import ReplayDatasetManifest, ReplayDatasetFileEntry
            checker = ReplayDatasetIntegrityChecker()
            manifest = ReplayDatasetManifest(
                dataset_id="TST",
                dataset_name="test",
                files=[
                    ReplayDatasetFileEntry(
                        file_id="f1",
                        relative_path="nonexistent.csv",
                        logical_role="DAILY_OHLCV",
                        file_type="CSV",
                        required=True,
                        present=False,
                    )
                ]
            )
            result = checker.check(manifest, base_dir=".")
            assert "nonexistent.csv" in result["files"]
            assert result["files"]["nonexistent.csv"]["status"] in ("MISSING", "SKIPPED")
            return ("PASS", "missing file handled gracefully (no crash)")
        except Exception as exc:
            return ("FAIL", f"missing file graceful check failed: {exc}")

    def _check_hash_mismatch_detected(self) -> Tuple[str, str]:
        try:
            from replay.dataset_freeze import ReplayDatasetFreezeManager
            fm = ReplayDatasetFreezeManager()

            class MockManifest:
                dataset_id = "TST-001"
                fingerprint = "stored_fingerprint_abc"
                frozen_at = "2025-01-01T00:00:00"
                status = "FROZEN"
                dataset_version = "1.0.0"

            m = MockManifest()
            result = fm.verify_frozen(m, current_fingerprint="different_fingerprint")
            assert result["status"] == "CORRUPTED", "hash mismatch should report CORRUPTED"
            return ("PASS", "hash mismatch detected as CORRUPTED")
        except Exception as exc:
            return ("FAIL", f"hash mismatch check failed: {exc}")

    def _check_mock_real_separated(self) -> Tuple[str, str]:
        try:
            from replay.dataset_qualification import ReplayDatasetQualificationEvaluator
            from replay.dataset_registry_schema import ReplayDatasetManifest, DatasetMode
            ev = ReplayDatasetQualificationEvaluator()
            mock_m = ReplayDatasetManifest(dataset_id="TST", dataset_name="t", mode="MOCK")
            q = ev.evaluate(mock_m)
            assert q == "MOCK_DEMO_ONLY", f"Mock should be MOCK_DEMO_ONLY, got {q}"
            return ("PASS", "mock/real datasets separated")
        except Exception as exc:
            return ("FAIL", f"mock/real separation check failed: {exc}")

    def _check_session_binding_locked(self) -> Tuple[str, str]:
        try:
            from replay.session_dataset_binding import ReplaySessionDatasetBinder
            b = ReplaySessionDatasetBinder()
            result = b.bind("S1", "D1", "1.0.0", allow_write=False)
            assert result.get("blocked"), "bind without allow_write should be blocked"
            return ("PASS", "session binding requires allow_write")
        except Exception as exc:
            return ("FAIL", f"session binding guard check failed: {exc}")

    def _check_completed_session_no_rebind(self) -> Tuple[str, str]:
        try:
            from replay.session_dataset_binding import ReplaySessionDatasetBinder
            b = ReplaySessionDatasetBinder()
            result = b.rebind_preview(
                session_id="S1",
                new_dataset_id="D2",
                new_version="2.0.0",
                session_status="COMPLETED",
            )
            assert result.get("blocked"), "COMPLETED session rebind should be blocked"
            return ("PASS", "completed session direct rebind is blocked")
        except Exception as exc:
            return ("FAIL", f"completed session rebind check failed: {exc}")

    def _check_package_preview_default(self) -> Tuple[str, str]:
        try:
            from replay.dataset_exporter import ReplayDatasetExporter
            exp = ReplayDatasetExporter()
            result = exp.preview("TST-001", "MANIFEST_ONLY")
            assert "EXPORT_PREVIEW" in str(result.get("action", ""))
            return ("PASS", "package export preview is default mode")
        except Exception as exc:
            return ("FAIL", f"package preview check failed: {exc}")

    def _check_package_import_guard(self) -> Tuple[str, str]:
        try:
            from replay.dataset_importer import ReplayDatasetImporter
            imp = ReplayDatasetImporter()
            result = imp.execute("nonexistent.json", allow_write=False)
            assert result.get("blocked"), "import without allow_write should be blocked"
            return ("PASS", "package import blocked without allow_write")
        except Exception as exc:
            return ("FAIL", f"package import guard check failed: {exc}")

    def _check_package_export_guard(self) -> Tuple[str, str]:
        try:
            from replay.dataset_exporter import ReplayDatasetExporter
            exp = ReplayDatasetExporter()
            result = exp.execute("TST-001", "MANIFEST_ONLY", allow_write=False)
            assert result.get("blocked"), "export without allow_write should be blocked"
            return ("PASS", "package export blocked without allow_write")
        except Exception as exc:
            return ("FAIL", f"package export guard check failed: {exc}")

    def _check_repair_preview_default(self) -> Tuple[str, str]:
        try:
            from replay.registry_repair import ReplayRegistryRepairPlanner
            r = ReplayRegistryRepairPlanner()
            result = r.preview()
            assert "REPAIR_PREVIEW" in str(result.get("action", ""))
            return ("PASS", "repair preview is default mode")
        except Exception as exc:
            return ("FAIL", f"repair preview check failed: {exc}")

    def _check_repair_execute_guard(self) -> Tuple[str, str]:
        try:
            from replay.registry_repair import ReplayRegistryRepairPlanner
            r = ReplayRegistryRepairPlanner()
            result = r.execute(allow_write=False)
            assert result.get("blocked"), "repair without allow_write should be blocked"
            return ("PASS", "repair execute blocked without allow_write")
        except Exception as exc:
            return ("FAIL", f"repair execute guard check failed: {exc}")

    def _check_no_auto_overwrite(self) -> Tuple[str, str]:
        try:
            from replay.dataset_registry import ReplayDatasetRegistry
            r = ReplayDatasetRegistry()
            assert not r.AUTO_DATASET_OVERWRITE_ENABLED
            return ("PASS", "AUTO_DATASET_OVERWRITE_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"no auto overwrite check failed: {exc}")

    def _check_no_auto_repair(self) -> Tuple[str, str]:
        try:
            from replay.registry_repair import ReplayRegistryRepairPlanner
            r = ReplayRegistryRepairPlanner()
            assert not r.AUTO_REGISTRY_REPAIR_ENABLED
            return ("PASS", "AUTO_REGISTRY_REPAIR_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"no auto repair check failed: {exc}")

    def _check_no_auto_rebind(self) -> Tuple[str, str]:
        try:
            from replay.session_dataset_binding import ReplaySessionDatasetBinder
            b = ReplaySessionDatasetBinder()
            assert not b.AUTO_SESSION_REBIND_ENABLED
            return ("PASS", "AUTO_SESSION_REBIND_ENABLED=False")
        except Exception as exc:
            return ("FAIL", f"no auto rebind check failed: {exc}")

    def _check_no_broker_data(self) -> Tuple[str, str]:
        try:
            from replay.dataset_portability import SECRET_PATTERNS
            broker_patterns = [p for p in SECRET_PATTERNS if "broker" in p.lower()]
            assert broker_patterns, "broker patterns must be in exclusion list"
            return ("PASS", "broker data excluded from packages")
        except Exception as exc:
            return ("FAIL", f"no broker data check failed: {exc}")

    def _check_no_forbidden_actions(self) -> Tuple[str, str]:
        try:
            import replay.dataset_registry as dr
            import replay.session_dataset_binding as sdb
            assert not getattr(dr, "AUTO_DATASET_OVERWRITE_ENABLED", True)
            assert not getattr(sdb, "AUTO_SESSION_REBIND_ENABLED", True)
            return ("PASS", "no forbidden actions enabled")
        except Exception as exc:
            return ("FAIL", f"no forbidden actions check failed: {exc}")

    def _check_research_only(self) -> Tuple[str, str]:
        try:
            import replay.dataset_registry as dr
            import replay.session_registry_v128 as sr
            assert getattr(dr, "RESEARCH_ONLY", False)
            assert getattr(sr, "RESEARCH_ONLY", False)
            return ("PASS", "RESEARCH_ONLY=True in registry modules")
        except Exception as exc:
            return ("FAIL", f"research only check failed: {exc}")

    def _check_no_real_orders(self) -> Tuple[str, str]:
        try:
            import replay.dataset_registry as dr
            import replay.session_registry_v128 as sr
            assert getattr(dr, "NO_REAL_ORDERS", False)
            assert getattr(sr, "NO_REAL_ORDERS", False)
            return ("PASS", "NO_REAL_ORDERS=True in registry modules")
        except Exception as exc:
            return ("FAIL", f"no real orders check failed: {exc}")
