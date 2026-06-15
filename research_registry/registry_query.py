"""
research_registry.registry_query — RegistryQuery v1.1.8

Query API for the research run registry.
Supports search by run_id, command, symbol, version, commit, qualification,
status, reason code, artifact filename.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RegistryQuery:
    """
    Query API for the research run registry.

    [!] Research Only. No Real Orders.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, store_dir: Optional[str] = None):
        from research_registry.registry_store import RegistryStore
        self._store = RegistryStore(store_dir=store_dir)

    def _load_records(self) -> List[Any]:
        """Load all run records as ResearchRunRecord objects."""
        from research_registry.registry_schema import ResearchRunRecord
        runs = self._store.list_runs()
        return [ResearchRunRecord.from_dict(r) for r in runs]

    def latest_runs(self, limit: int = 20) -> List[Any]:
        """Return the most recent N runs."""
        records = self._load_records()
        records_sorted = sorted(records, key=lambda r: r.started_at or "", reverse=True)
        return records_sorted[:limit]

    def get_run(self, run_id: str) -> Optional[Any]:
        """Return a single run by run_id."""
        from research_registry.registry_schema import ResearchRunRecord
        d = self._store.get_run(run_id)
        if d:
            return ResearchRunRecord.from_dict(d)
        return None

    def get_run_by_registry_id(self, registry_id: str) -> Optional[Any]:
        """Return a single run by registry_id."""
        from research_registry.registry_schema import ResearchRunRecord
        d = self._store.get_run_by_registry_id(registry_id)
        if d:
            return ResearchRunRecord.from_dict(d)
        return None

    def latest_successful(self, command_name: Optional[str] = None) -> Optional[Any]:
        """Return the latest COMPLETED run (optionally filtered by command)."""
        records = self._load_records()
        filtered = [r for r in records if r.status in ("COMPLETED", "COMPLETED_WITH_WARNINGS")]
        if command_name:
            filtered = [r for r in filtered if r.command_name == command_name]
        if not filtered:
            return None
        return max(filtered, key=lambda r: r.started_at or "")

    def latest_formal(self, command_name: Optional[str] = None) -> Optional[Any]:
        """Return the latest FORMALLY_QUALIFIED run."""
        records = self._load_records()
        filtered = [r for r in records if r.qualification == "FORMALLY_QUALIFIED"]
        if command_name:
            filtered = [r for r in filtered if r.command_name == command_name]
        if not filtered:
            return None
        return max(filtered, key=lambda r: r.started_at or "")

    def latest_observational(self, command_name: Optional[str] = None) -> Optional[Any]:
        """Return the latest OBSERVATIONAL_ONLY run."""
        records = self._load_records()
        filtered = [r for r in records if r.qualification == "OBSERVATIONAL_ONLY"]
        if command_name:
            filtered = [r for r in filtered if r.command_name == command_name]
        if not filtered:
            return None
        return max(filtered, key=lambda r: r.started_at or "")

    def list_by_type(self, run_type: str) -> List[Any]:
        return [r for r in self._load_records() if r.run_type == run_type]

    def list_by_command(self, command_name: str) -> List[Any]:
        return [r for r in self._load_records() if r.command_name == command_name]

    def list_by_status(self, status: str) -> List[Any]:
        return [r for r in self._load_records() if r.status == status]

    def list_by_qualification(self, qualification: str) -> List[Any]:
        return [r for r in self._load_records() if r.qualification == qualification]

    def list_by_version(self, version: str) -> List[Any]:
        return [r for r in self._load_records() if r.code_version == version]

    def list_by_commit(self, commit: str) -> List[Any]:
        return [r for r in self._load_records() if r.git_commit == commit]

    def list_by_symbol(self, symbol: str) -> List[Any]:
        return [r for r in self._load_records()
                if symbol in r.requested_symbols
                or symbol in r.included_symbols
                or symbol == r.stock]

    def list_blocked(self) -> List[Any]:
        return [r for r in self._load_records() if r.status == "BLOCKED"]

    def list_failed(self) -> List[Any]:
        return [r for r in self._load_records() if r.status == "FAILED"]

    def list_duplicates(self) -> List[Any]:
        return [r for r in self._load_records() if r.duplicate_of]

    def list_overridden(self) -> List[Any]:
        return [r for r in self._load_records() if r.override_used]

    def list_missing_artifacts(self) -> List[Any]:
        """Return runs that have output_artifact_ids but missing artifacts."""
        from research_registry.registry_schema import RunArtifact
        all_artifacts = self._store.list_artifacts()
        missing_run_ids = set()
        for art_d in all_artifacts:
            art = RunArtifact.from_dict(art_d)
            if not art.exists:
                missing_run_ids.add(art.run_id)

        # Also include runs with output_artifact_ids that have no artifact records at all
        runs = self._load_records()
        all_artifact_run_ids = {a.get("run_id", "") for a in all_artifacts}
        for r in runs:
            if r.output_artifact_ids and r.run_id not in all_artifact_run_ids:
                missing_run_ids.add(r.run_id)

        return [r for r in runs if r.run_id in missing_run_ids]

    def list_non_qualified(self) -> List[Any]:
        return [r for r in self._load_records()
                if r.qualification in ("NOT_QUALIFIED", "UNKNOWN", "BLOCKED")]

    def run_artifacts(self, run_id: str) -> List[Any]:
        """Return artifacts for a run."""
        from research_registry.registry_schema import RunArtifact
        return [RunArtifact.from_dict(a) for a in self._store.list_run_artifacts(run_id)]

    def run_lineage(self, run_id: str) -> Optional[Any]:
        """Return lineage record for a run."""
        from research_registry.registry_schema import RunLineage
        lineage_records = self._store.list_lineage()
        for lin in lineage_records:
            if lin.get("run_id") == run_id:
                return RunLineage.from_dict(lin)
        return None

    def search(self, query: str) -> List[Any]:
        """
        Search runs by query string.
        Supports: run_id, command, symbol, version, commit, qualification,
                  status, reason_code, artifact_filename.
        """
        if not query:
            return self._load_records()

        query_lower = query.lower().strip()
        runs = self._load_records()
        result = []

        # Gather artifact filenames per run_id for searching
        artifacts = self._store.list_artifacts()
        artifact_filenames: Dict[str, List[str]] = {}
        for art in artifacts:
            run_id = art.get("run_id", "")
            fn = art.get("filename", "").lower()
            if run_id:
                artifact_filenames.setdefault(run_id, []).append(fn)

        for r in runs:
            if any([
                query_lower in r.run_id.lower(),
                query_lower in r.registry_id.lower(),
                query_lower in r.command_name.lower(),
                query_lower in (r.code_version or "").lower(),
                query_lower in (r.git_commit or "").lower(),
                query_lower in (r.git_tag or "").lower(),
                query_lower in (r.qualification or "").lower(),
                query_lower in (r.status or "").lower(),
                query_lower in (r.stock or "").lower(),
                any(query_lower in s.lower() for s in r.requested_symbols),
                any(query_lower in s.lower() for s in r.included_symbols),
                any(query_lower in rc.lower() for rc in r.blocked_reason_codes),
                any(query_lower in fn for fn in artifact_filenames.get(r.run_id, [])),
            ]):
                result.append(r)

        return result

    def compare(self, run_a_id: str, run_b_id: str) -> Optional[Any]:
        """Compare two runs and return RunComparison."""
        run_a = self.get_run(run_a_id)
        run_b = self.get_run(run_b_id)
        if run_a is None or run_b is None:
            return None
        from research_registry.run_comparator import ResearchRunComparator
        comparator = ResearchRunComparator()
        comp = comparator.compare(run_a, run_b)
        self._store.append_comparison(comp)
        return comp

    def registry_summary(self) -> Any:
        """Return RegistrySummary from the store or compute from runs."""
        from research_registry.registry_schema import RegistrySummary
        from datetime import datetime, timezone

        try:
            runs = self._load_records()

            latest_successful: Dict[str, str] = {}
            for r in runs:
                if r.status in ("COMPLETED", "COMPLETED_WITH_WARNINGS"):
                    cmd = r.command_name
                    current = latest_successful.get(cmd, "")
                    if not current or r.started_at > current:
                        latest_successful[cmd] = r.started_at

            # Count missing artifacts
            missing_artifact_runs = len(self.list_missing_artifacts())

            summary = RegistrySummary(
                generated_at=datetime.now(timezone.utc).isoformat(),
                total_runs=len(runs),
                completed_runs=sum(1 for r in runs if r.status in ("COMPLETED", "COMPLETED_WITH_WARNINGS")),
                warning_runs=sum(1 for r in runs if r.status == "COMPLETED_WITH_WARNINGS"),
                blocked_runs=sum(1 for r in runs if r.status == "BLOCKED"),
                failed_runs=sum(1 for r in runs if r.status == "FAILED"),
                formal_runs=sum(1 for r in runs if r.qualification == "FORMALLY_QUALIFIED"),
                observational_runs=sum(1 for r in runs if r.qualification == "OBSERVATIONAL_ONLY"),
                demo_runs=sum(1 for r in runs if r.qualification == "DEMO_ONLY"),
                non_qualified_runs=sum(1 for r in runs if r.qualification in ("NOT_QUALIFIED", "UNKNOWN")),
                duplicate_runs=sum(1 for r in runs if r.duplicate_of),
                overridden_runs=sum(1 for r in runs if r.override_used),
                missing_artifact_runs=missing_artifact_runs,
                reproducibility_verified_runs=sum(1 for r in runs if r.reproducibility_hash),
                latest_successful_runs=latest_successful,
            )
            self._store.save_summary(summary)
            return summary
        except Exception as exc:
            logger.warning("registry_summary failed (non-fatal): %s", exc)
            return RegistrySummary(generated_at=datetime.now(timezone.utc).isoformat())
