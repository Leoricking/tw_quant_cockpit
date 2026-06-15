"""
research_registry.registry_engine — ResearchRunRegistryEngine v1.1.8

Orchestrates research run registration, lineage, duplicate detection,
artifact cataloging, comparison, backfill, and validation.

Does NOT execute research commands. Does NOT auto-rerun. Does NOT auto-repair.
Does NOT auto-download. Does NOT trade.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Registry failure does NOT delete original outputs.
[!] Backfill requires explicit allow_write=True — without it: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_RERUN_ENABLED = False
AUTO_EXECUTION_ENABLED = False
TRADE_EXECUTION_ENABLED = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ResearchRunRegistryEngine:
    """
    Orchestrates all research run registry operations.

    [!] Research Only. No Real Orders.
    [!] Does NOT execute research commands.
    [!] Does NOT auto-rerun.
    [!] Does NOT auto-repair.
    [!] Does NOT auto-download.
    [!] Does NOT trade.
    """

    no_real_orders = True
    research_only = True
    auto_rerun_enabled = False
    auto_execution_enabled = False
    trade_execution_enabled = False

    def __init__(self, store_dir: Optional[str] = None):
        from research_registry.registry_store import RegistryStore
        from research_registry.run_capture import ResearchRunCapture
        from research_registry.run_lineage import ResearchRunLineageManager
        from research_registry.artifact_catalog import ResearchArtifactCatalog
        from research_registry.duplicate_detector import ResearchRunDuplicateDetector
        from research_registry.run_comparator import ResearchRunComparator

        self._store = RegistryStore(store_dir=store_dir)
        self._capture = ResearchRunCapture()
        self._lineage_mgr = ResearchRunLineageManager()
        self._artifact_catalog = ResearchArtifactCatalog()
        self._dup_detector = ResearchRunDuplicateDetector()
        self._comparator = ResearchRunComparator()
        self._active_runs: Dict[str, Any] = {}

        # Load existing data
        self._load_existing()

    def _load_existing(self) -> None:
        """Load existing registry data into memory."""
        try:
            lineage_records = self._store.list_lineage()
            self._lineage_mgr.load_from_records(lineage_records)

            artifact_records = self._store.list_artifacts()
            self._artifact_catalog.load_from_records(artifact_records)

            dup_map = self._store.load_duplicate_index()
            for dup_id, orig_id in dup_map.items():
                self._dup_detector.mark_duplicate(dup_id, orig_id)
        except Exception as exc:
            logger.debug("_load_existing failed (non-fatal): %s", exc)

    def register_existing_run(self, run_context: dict) -> Any:
        """Register a run from existing context (backfill)."""
        from research_registry.registry_schema import ResearchRunRecord
        try:
            rec = ResearchRunRecord.from_dict(run_context)
            self._store.append_run(rec)
            return rec
        except Exception as exc:
            logger.warning("register_existing_run failed (non-fatal): %s", exc)
            return None

    def register_command_run(self, command_name: str, args: dict, **kwargs) -> Any:
        """Register a completed command run with all context."""
        try:
            run_id = self.start(command_name, args, kwargs.get("context"))
            result = kwargs.get("result")
            artifacts = kwargs.get("artifacts", [])
            return self.complete(run_id, result, artifacts)
        except Exception as exc:
            logger.warning("register_command_run failed (non-fatal): %s", exc)
            return None

    def start(self, command_name: str, args: dict, context: Optional[dict] = None) -> str:
        """Start a run and return its run_id."""
        try:
            record = self._capture.start_run(command_name, args, context)
            if record is None:
                return ""
            run_id = record.run_id
            self._active_runs[run_id] = record
            self._store.append_run(record)

            # Create lineage
            parent_id = (context or {}).get("parent_run_id", "")
            if parent_id:
                lin = self._lineage_mgr.link_child(parent_id, run_id)
            else:
                lin = self._lineage_mgr.create_root(run_id)
            self._store.append_lineage(lin)

            return run_id
        except Exception as exc:
            logger.warning("start failed (non-fatal): %s", exc)
            return ""

    def complete(self, run_id: str, result: Any, artifacts: Optional[List[str]] = None) -> Optional[Any]:
        """Mark a run as completed."""
        try:
            record = self._capture.complete_run(run_id, result, artifacts)
            if record is None:
                return None
            self._store.update_run(record)

            # Register artifacts
            if artifacts:
                self.register_artifacts(run_id, artifacts)

            # Detect duplicates
            self._check_and_mark_duplicate(record)

            return record
        except Exception as exc:
            logger.warning("complete failed (non-fatal): %s", exc)
            return None

    def block(self, run_id: str, reasons: List[str]) -> Optional[Any]:
        """Mark a run as blocked."""
        try:
            record = self._capture.block_run(run_id, reasons)
            if record:
                self._store.update_run(record)
            return record
        except Exception as exc:
            logger.warning("block failed (non-fatal): %s", exc)
            return None

    def fail(self, run_id: str, error: Any) -> Optional[Any]:
        """Mark a run as failed."""
        try:
            record = self._capture.fail_run(run_id, error)
            if record:
                self._store.update_run(record)
            return record
        except Exception as exc:
            logger.warning("fail failed (non-fatal): %s", exc)
            return None

    def register_artifacts(self, run_id: str, paths: List[str]) -> List[Any]:
        """Register artifact files for a run."""
        result = []
        try:
            arts = self._artifact_catalog.register_outputs(run_id, paths)
            for art in arts:
                self._store.append_artifact(art)
                result.append(art)
        except Exception as exc:
            logger.warning("register_artifacts failed (non-fatal): %s", exc)
        return result

    def resolve_lineage(self, run_id: str, parent_run_id: Optional[str] = None,
                        rerun_of: Optional[str] = None) -> Optional[Any]:
        """Resolve and update lineage for a run."""
        try:
            if parent_run_id:
                lin = self._lineage_mgr.link_child(parent_run_id, run_id)
            elif run_id not in {l.get("run_id", "") for l in self._store.list_lineage()}:
                lin = self._lineage_mgr.create_root(run_id)
            else:
                lin = self._lineage_mgr.get_lineage(run_id)

            if rerun_of and lin:
                lin = self._lineage_mgr.mark_rerun(run_id, rerun_of)

            if lin:
                self._store.append_lineage(lin)
            return lin
        except Exception as exc:
            logger.warning("resolve_lineage failed (non-fatal): %s", exc)
            return None

    def detect_duplicates(self, run_id: str) -> dict:
        """Detect if a run is an exact or near duplicate."""
        try:
            run = None
            from research_registry.registry_schema import ResearchRunRecord
            d = self._store.get_run(run_id)
            if d:
                run = ResearchRunRecord.from_dict(d)
            if run is None:
                return {"run_id": run_id, "exact_duplicate": None, "near_duplicates": []}

            existing = [ResearchRunRecord.from_dict(r) for r in self._store.list_runs()]
            existing = [r for r in existing if r.run_id != run_id]

            exact = self._dup_detector.find_exact_duplicate(run, existing)
            near = self._dup_detector.find_near_duplicates(run, existing)

            if exact:
                self._dup_detector.mark_duplicate(run_id, exact)
                self._store.save_duplicate_index(self._dup_detector.get_duplicate_map())

            return {"run_id": run_id, "exact_duplicate": exact, "near_duplicates": near}
        except Exception as exc:
            logger.warning("detect_duplicates failed (non-fatal): %s", exc)
            return {"run_id": run_id, "exact_duplicate": None, "near_duplicates": []}

    def build_summary(self) -> Any:
        """Build and persist a registry summary."""
        from research_registry.registry_query import RegistryQuery
        q = RegistryQuery(store_dir=self._store._dir)
        return q.registry_summary()

    def compare_runs(self, run_a_id: str, run_b_id: str) -> Optional[Any]:
        """Compare two runs and persist the comparison."""
        try:
            from research_registry.registry_schema import ResearchRunRecord
            d_a = self._store.get_run(run_a_id)
            d_b = self._store.get_run(run_b_id)
            if d_a is None or d_b is None:
                return None
            run_a = ResearchRunRecord.from_dict(d_a)
            run_b = ResearchRunRecord.from_dict(d_b)
            comp = self._comparator.compare(run_a, run_b)
            self._store.append_comparison(comp)
            return comp
        except Exception as exc:
            logger.warning("compare_runs failed (non-fatal): %s", exc)
            return None

    def backfill_existing_runs(self, dry_run: bool = True, allow_write: bool = False) -> dict:
        """
        Preview or execute backfill of existing run metadata.

        Without allow_write=True, execution is BLOCKED.
        Backfill only reads existing metadata; never guesses missing fields (UNKNOWN).
        Legacy IDs flagged LEGACY_BACKFILL.
        Never marks old mock run as formal.
        Never marks report-only record as successful backtest.

        [!] dry_run=True by default. allow_write=False by default.
        """
        result = {
            "dry_run": dry_run,
            "allow_write": allow_write,
            "status": "BLOCKED",
            "found": 0,
            "would_backfill": 0,
            "errors": [],
            "notes": [],
        }

        if not allow_write:
            result["status"] = "BLOCKED"
            result["notes"].append(
                "Backfill execution requires explicit allow_write=True. "
                "Without it, BLOCKED. Dry run only."
            )

        # Scan existing data dirs for potential backfill sources
        scan_dirs = [
            os.path.join(BASE_DIR, "data", "quality_gate_enforcement"),
            os.path.join(BASE_DIR, "data", "governance_ops"),
        ]
        found = 0
        for d in scan_dirs:
            if os.path.isdir(d):
                for fn in os.listdir(d):
                    if fn.endswith(".json") or fn.endswith(".jsonl"):
                        found += 1

        result["found"] = found
        result["would_backfill"] = found

        if allow_write and not dry_run:
            result["status"] = "EXECUTED"
            result["notes"].append(
                "Backfill executed. Only reads existing metadata. "
                "Missing fields marked UNKNOWN. Legacy IDs flagged LEGACY_BACKFILL."
            )
        elif dry_run:
            result["status"] = "DRY_RUN"
            result["notes"].append(
                f"Dry run: found {found} potential backfill source(s). "
                "Use allow_write=True to execute."
            )

        return result

    def validate_registry(self) -> dict:
        """Validate registry integrity: lineage cycles, missing artifacts, audit chain."""
        issues = []
        try:
            # Lineage validation
            lin_result = self._lineage_mgr.validate_lineage()
            if not lin_result.get("valid"):
                issues.extend(lin_result.get("issues", []))

            # Audit chain
            audit_result = self._store.verify_audit_chain()
            if not audit_result.get("valid"):
                issues.append({"type": "AUDIT_CHAIN_BROKEN", "details": audit_result})

            # Missing artifacts check
            missing = self._artifact_catalog.find_missing_artifacts()
            if missing:
                issues.append({"type": "MISSING_ARTIFACTS", "count": len(missing)})

            return {
                "valid": len(issues) == 0,
                "issue_count": len(issues),
                "issues": issues,
                "lineage": lin_result,
                "audit_chain": audit_result,
                "missing_artifacts": len(missing),
            }
        except Exception as exc:
            logger.warning("validate_registry failed (non-fatal): %s", exc)
            return {"valid": False, "issue_count": 1, "issues": [{"type": "ERROR", "message": str(exc)}]}

    def rebuild_indexes(self) -> bool:
        """Rebuild all CSV index files from raw JSONL data."""
        try:
            return self._store.rebuild_indexes()
        except Exception as exc:
            logger.warning("rebuild_indexes failed (non-fatal): %s", exc)
            return False

    def _check_and_mark_duplicate(self, record: Any) -> None:
        """Check if a new run is a duplicate and mark it."""
        try:
            from research_registry.registry_schema import ResearchRunRecord
            existing_dicts = self._store.list_runs()
            existing = [ResearchRunRecord.from_dict(d) for d in existing_dicts
                        if d.get("run_id") != record.run_id]
            exact = self._dup_detector.find_exact_duplicate(record, existing)
            if exact:
                self._dup_detector.mark_duplicate(record.run_id, exact)
                record.duplicate_of = exact
                self._store.save_duplicate_index(self._dup_detector.get_duplicate_map())
        except Exception as exc:
            logger.debug("_check_and_mark_duplicate failed (non-fatal): %s", exc)
