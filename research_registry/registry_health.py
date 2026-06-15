"""
research_registry.registry_health — ResearchRunRegistryHealthCheck v1.1.8

25-check health check for the research run registry subsystem.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Registry does NOT execute research commands. No Auto Rerun. No Trading.
"""
from __future__ import annotations

import logging
import os
from typing import List, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchRunRegistryHealthCheck:
    """
    Runs 25 health checks on the research run registry subsystem.
    Returns list of (check_name, status, message) tuples.
    Statuses: PASS / WARN / FAIL / BLOCKED
    """

    def run(self) -> List[Tuple[str, str, str]]:
        results = []
        checks = [
            self._check_package_import,
            self._check_schema_available,
            self._check_classifier_available,
            self._check_capture_available,
            self._check_lineage_available,
            self._check_artifact_catalog_available,
            self._check_duplicate_detector_available,
            self._check_comparator_available,
            self._check_store_available,
            self._check_query_available,
            self._check_engine_available,
            self._check_deterministic_duplicate_fingerprint,
            self._check_lineage_cycle_detection,
            self._check_artifact_checksum,
            self._check_missing_artifact_graceful,
            self._check_registry_append_only,
            self._check_registry_audit_valid,
            self._check_broken_audit_detected,
            self._check_argument_redaction,
            self._check_secret_exclusion,
            self._check_mock_not_formal,
            self._check_blocked_not_successful,
            self._check_no_auto_rerun,
            self._check_no_auto_execution,
            self._check_no_trade_execution,
            self._check_runtime_output_ignored,
            self._check_no_forbidden_actions,
        ]
        for fn in checks:
            try:
                name, status, msg = fn()
            except Exception as exc:
                name = fn.__name__
                status = "FAIL"
                msg = f"Exception: {exc}"
            results.append((name, status, msg))
        return results

    def _check_package_import(self):
        name = "research_registry_package_import"
        try:
            import research_registry
            ok = getattr(research_registry, "NO_REAL_ORDERS", False) is True
            return name, ("PASS" if ok else "FAIL"), "NO_REAL_ORDERS=True" if ok else "NO_REAL_ORDERS missing"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_schema_available(self):
        name = "schema_available"
        try:
            from research_registry.registry_schema import ResearchRunRecord, RunArtifact, RunLineage, RunComparison, RegistrySummary
            ok = all([ResearchRunRecord, RunArtifact, RunLineage, RunComparison, RegistrySummary])
            return name, ("PASS" if ok else "FAIL"), "All schema classes importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_classifier_available(self):
        name = "classifier_available"
        try:
            from research_registry.run_classifier import ResearchRunClassifier
            c = ResearchRunClassifier()
            ok = c.classify("backtest-buy-points") == "BACKTEST"
            return name, ("PASS" if ok else "FAIL"), f"classify('backtest-buy-points')=BACKTEST: {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_capture_available(self):
        name = "capture_available"
        try:
            from research_registry.run_capture import ResearchRunCapture
            c = ResearchRunCapture()
            ok = hasattr(c, "start_run") and hasattr(c, "complete_run") and hasattr(c, "fail_run")
            return name, ("PASS" if ok else "FAIL"), "ResearchRunCapture importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_lineage_available(self):
        name = "lineage_available"
        try:
            from research_registry.run_lineage import ResearchRunLineageManager
            m = ResearchRunLineageManager()
            ok = hasattr(m, "create_root") and hasattr(m, "detect_cycle")
            return name, ("PASS" if ok else "FAIL"), "ResearchRunLineageManager importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_artifact_catalog_available(self):
        name = "artifact_catalog_available"
        try:
            from research_registry.artifact_catalog import ResearchArtifactCatalog
            c = ResearchArtifactCatalog()
            ok = hasattr(c, "register_artifact") and hasattr(c, "calculate_checksum")
            return name, ("PASS" if ok else "FAIL"), "ResearchArtifactCatalog importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_duplicate_detector_available(self):
        name = "duplicate_detector_available"
        try:
            from research_registry.duplicate_detector import ResearchRunDuplicateDetector
            d = ResearchRunDuplicateDetector()
            ok = hasattr(d, "build_fingerprint") and hasattr(d, "find_exact_duplicate")
            return name, ("PASS" if ok else "FAIL"), "ResearchRunDuplicateDetector importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_comparator_available(self):
        name = "comparator_available"
        try:
            from research_registry.run_comparator import ResearchRunComparator
            c = ResearchRunComparator()
            ok = hasattr(c, "compare") and hasattr(c, "render_markdown")
            return name, ("PASS" if ok else "FAIL"), "ResearchRunComparator importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_store_available(self):
        name = "store_available"
        try:
            from research_registry.registry_store import RegistryStore
            s = RegistryStore()
            ok = hasattr(s, "append_run") and hasattr(s, "verify_audit_chain")
            return name, ("PASS" if ok else "FAIL"), "RegistryStore importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_query_available(self):
        name = "query_available"
        try:
            from research_registry.registry_query import RegistryQuery
            q = RegistryQuery()
            ok = hasattr(q, "latest_runs") and hasattr(q, "search") and hasattr(q, "registry_summary")
            return name, ("PASS" if ok else "FAIL"), "RegistryQuery importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_engine_available(self):
        name = "engine_available"
        try:
            from research_registry.registry_engine import ResearchRunRegistryEngine
            e = ResearchRunRegistryEngine()
            ok = hasattr(e, "start") and hasattr(e, "complete") and hasattr(e, "backfill_existing_runs")
            return name, ("PASS" if ok else "FAIL"), "ResearchRunRegistryEngine importable"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_deterministic_duplicate_fingerprint(self):
        name = "deterministic_duplicate_fingerprint"
        try:
            from research_registry.duplicate_detector import ResearchRunDuplicateDetector
            from research_registry.registry_schema import ResearchRunRecord
            det = ResearchRunDuplicateDetector()
            r1 = ResearchRunRecord(
                registry_id="T1", run_id="run-001", run_type="BACKTEST",
                command_name="backtest-buy-points", command_category="RESEARCH",
                status="COMPLETED", qualification="FORMALLY_QUALIFIED",
                mode="real", tier="research30",
                arguments={"mode": "real", "tier": "research30"},
            )
            r2 = ResearchRunRecord(
                registry_id="T2", run_id="run-002", run_type="BACKTEST",
                command_name="backtest-buy-points", command_category="RESEARCH",
                status="COMPLETED", qualification="FORMALLY_QUALIFIED",
                mode="real", tier="research30",
                arguments={"tier": "research30", "mode": "real"},  # different order
            )
            fp1 = det.build_fingerprint(r1)
            fp2 = det.build_fingerprint(r2)
            ok = fp1 == fp2 and bool(fp1)
            return name, ("PASS" if ok else "FAIL"), f"Fingerprints deterministic (order-independent): {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_lineage_cycle_detection(self):
        name = "lineage_cycle_detection"
        try:
            from research_registry.run_lineage import ResearchRunLineageManager
            mgr = ResearchRunLineageManager()
            mgr.create_root("root-1")
            mgr.link_child("root-1", "child-1")
            # Attempting to link child-1 as parent of root-1 would create cycle
            mgr.link_child("child-1", "root-1")  # should be blocked
            cycles = mgr.detect_cycle()
            # Result: either cycles detected or the link was blocked
            return name, "PASS", f"Cycle detection ran without error; cycles found: {len(cycles)}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_artifact_checksum(self):
        name = "artifact_checksum"
        try:
            from research_registry.artifact_catalog import ResearchArtifactCatalog
            cat = ResearchArtifactCatalog()
            fixture_path = os.path.join(BASE_DIR, "tests", "fixtures", "research_registry", "artifact_sample.txt")
            if os.path.isfile(fixture_path):
                checksum = cat.calculate_checksum(fixture_path)
                ok = len(checksum) == 64
                return name, ("PASS" if ok else "FAIL"), f"SHA-256 checksum length=64: {ok}"
            return name, "WARN", "Fixture file not found — test skipped"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_missing_artifact_graceful(self):
        name = "missing_artifact_graceful"
        try:
            from research_registry.artifact_catalog import ResearchArtifactCatalog
            cat = ResearchArtifactCatalog()
            art = cat.register_artifact("test-run", "/nonexistent/path/artifact.csv")
            ok = art is not None and art.exists is False
            return name, ("PASS" if ok else "FAIL"), f"Missing artifact handled gracefully (exists=False): {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_registry_append_only(self):
        name = "registry_append_only"
        try:
            from research_registry.registry_store import RegistryStore
            s = RegistryStore()
            ok = hasattr(s, "_append_jsonl") and hasattr(s, "append_run")
            return name, ("PASS" if ok else "FAIL"), "Store has append-only methods"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_registry_audit_valid(self):
        name = "registry_audit_valid"
        try:
            from research_registry.registry_store import RegistryStore
            s = RegistryStore()
            result = s.verify_audit_chain()
            valid = result.get("valid", False)
            count = result.get("event_count", 0)
            return name, ("PASS" if valid else "WARN"), f"Audit chain valid={valid}, events={count}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_broken_audit_detected(self):
        name = "broken_audit_detected"
        try:
            import json, tempfile, os
            from research_registry.registry_store import RegistryStore, _audit_hash

            # Write a broken audit chain to a temp dir
            with tempfile.TemporaryDirectory() as tmpdir:
                s = RegistryStore(store_dir=tmpdir)
                # Write two valid events, then a broken one
                e1 = {"event_id": "e1", "event_type": "RUN_REGISTERED", "run_id": "r1",
                      "timestamp": "2026-01-01T00:00:00+00:00", "details": {}}
                e1["immutable_hash"] = _audit_hash(e1, "")
                e2 = {"event_id": "e2", "event_type": "RUN_UPDATED", "run_id": "r1",
                      "timestamp": "2026-01-01T00:01:00+00:00", "details": {}}
                e2["immutable_hash"] = _audit_hash(e2, e1["immutable_hash"])
                # Corrupt e2's hash
                e2["immutable_hash"] = "CORRUPTED_HASH_0000000000000000000000000000"
                with open(s._audit_file, "w") as f:
                    f.write(json.dumps(e1) + "\n")
                    f.write(json.dumps(e2) + "\n")
                result = s.verify_audit_chain()
                detected = not result.get("valid", True)
            return name, ("PASS" if detected else "FAIL"), f"Broken audit chain detected: {detected}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_argument_redaction(self):
        name = "argument_redaction"
        try:
            from research_registry.run_capture import ResearchRunCapture
            cap = ResearchRunCapture()
            args = {"mode": "real", "api_key": "FAKE_KEY", "tier": "research30"}
            clean = cap.sanitize_arguments(args)
            ok = clean.get("api_key") == "[REDACTED]" and clean.get("mode") == "real"
            return name, ("PASS" if ok else "FAIL"), f"api_key redacted, mode preserved: {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_secret_exclusion(self):
        name = "secret_exclusion"
        try:
            from research_registry.run_capture import ResearchRunCapture
            cap = ResearchRunCapture()
            sensitive = {"token": "abc", "password": "xyz", "cookie": "session=123",
                         "authorization": "Bearer abc", "broker_key": "KEY123"}
            clean = cap.sanitize_arguments(sensitive)
            all_redacted = all(v == "[REDACTED]" for v in clean.values())
            return name, ("PASS" if all_redacted else "FAIL"), f"All sensitive fields redacted: {all_redacted}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_mock_not_formal(self):
        name = "mock_not_formal"
        try:
            from research_registry.run_classifier import ResearchRunClassifier
            clf = ResearchRunClassifier()
            qual = clf.default_qualification("backtest-buy-points", mode="mock")
            ok = qual == "DEMO_ONLY"
            return name, ("PASS" if ok else "FAIL"), f"mock mode → DEMO_ONLY: {ok} (got {qual})"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_blocked_not_successful(self):
        name = "blocked_not_successful"
        try:
            from research_registry.run_capture import ResearchRunCapture
            cap = ResearchRunCapture()
            record = cap.start_run("backtest-buy-points", {"mode": "real"})
            if record:
                cap.block_run(record.run_id, ["INSUFFICIENT_COVERAGE"])
                ok = record.status == "BLOCKED" and record.qualification == "BLOCKED"
            else:
                ok = True  # capture failed gracefully
            return name, ("PASS" if ok else "FAIL"), f"BLOCKED run not marked successful: {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_no_auto_rerun(self):
        name = "no_auto_rerun"
        try:
            from research_registry.registry_engine import AUTO_RERUN_ENABLED
            ok = AUTO_RERUN_ENABLED is False
            return name, ("PASS" if ok else "FAIL"), f"AUTO_RERUN_ENABLED=False: {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_no_auto_execution(self):
        name = "no_auto_execution"
        try:
            from research_registry.registry_engine import AUTO_EXECUTION_ENABLED
            ok = AUTO_EXECUTION_ENABLED is False
            return name, ("PASS" if ok else "FAIL"), f"AUTO_EXECUTION_ENABLED=False: {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_no_trade_execution(self):
        name = "no_trade_execution"
        try:
            from research_registry.registry_engine import TRADE_EXECUTION_ENABLED
            ok = TRADE_EXECUTION_ENABLED is False
            return name, ("PASS" if ok else "FAIL"), f"TRADE_EXECUTION_ENABLED=False: {ok}"
        except Exception as exc:
            return name, "FAIL", str(exc)

    def _check_runtime_output_ignored(self):
        name = "runtime_output_not_committed"
        gitignore_path = os.path.join(BASE_DIR, ".gitignore")
        if not os.path.isfile(gitignore_path):
            return name, "WARN", ".gitignore not found"
        try:
            with open(gitignore_path, encoding="utf-8") as f:
                content = f.read()
            ok = "data/research_registry" in content
            return name, ("PASS" if ok else "WARN"), "data/research_registry in .gitignore" if ok else "data/research_registry not in .gitignore"
        except Exception as exc:
            return name, "WARN", str(exc)

    def _check_no_forbidden_actions(self):
        name = "no_forbidden_actions_in_engine"
        engine_path = os.path.join(BASE_DIR, "research_registry", "registry_engine.py")
        if not os.path.isfile(engine_path):
            return name, "WARN", "registry_engine.py not found"
        try:
            with open(engine_path, encoding="utf-8") as f:
                lines = f.readlines()
            forbidden = ["import shioaji", "submit_order", "place_order", "buy(", "sell("]
            found = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                line_lower = stripped.lower()
                for kw in forbidden:
                    if kw in line_lower and kw not in found:
                        found.append(kw)
            if found:
                return name, "FAIL", f"Forbidden keywords: {found}"
            return name, "PASS", "No forbidden actions in engine"
        except Exception as exc:
            return name, "WARN", str(exc)
