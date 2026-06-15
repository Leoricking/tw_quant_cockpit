"""
research_registry.artifact_catalog — ResearchArtifactCatalog v1.1.8

Catalogs run output artifacts. Never moves or deletes files. Only records metadata.
Prefers repo-relative paths. SHA-256 checksum with configurable size limit.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] NEVER moves, deletes, or modifies artifacts.
"""
from __future__ import annotations

import hashlib
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default size limit for checksum computation (100 MB)
DEFAULT_CHECKSUM_SIZE_LIMIT = 100 * 1024 * 1024

_EXT_TYPE_MAP = {
    ".csv": "CSV",
    ".json": "JSON",
    ".jsonl": "JSONL",
    ".md": "MARKDOWN",
    ".html": "HTML",
    ".htm": "HTML",
    ".png": "PNG",
    ".jpg": "PNG",
    ".jpeg": "PNG",
    ".pdf": "PDF",
    ".db": "SQLITE",
    ".sqlite": "SQLITE",
    ".sqlite3": "SQLITE",
    ".log": "LOG",
    ".txt": "LOG",
}


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _repo_relative(path: str) -> str:
    """Convert absolute path to repo-relative if possible."""
    try:
        abs_path = os.path.abspath(path)
        base = os.path.abspath(BASE_DIR)
        if abs_path.startswith(base):
            rel = os.path.relpath(abs_path, base)
            return rel.replace("\\", "/")
    except Exception:
        pass
    return path


class ResearchArtifactCatalog:
    """
    Catalogs run output artifacts by recording metadata only.

    [!] Research Only. No Real Orders.
    [!] NEVER moves, deletes, or modifies artifacts.
    [!] Prefer repo-relative paths. Machine-specific absolute paths tagged local_path.
    """

    no_real_orders = True
    research_only = True

    def __init__(self, checksum_size_limit: int = DEFAULT_CHECKSUM_SIZE_LIMIT):
        self._artifacts: Dict[str, dict] = {}
        self._run_artifacts: Dict[str, List[str]] = {}
        self._checksum_size_limit = checksum_size_limit

    def discover_artifacts(self, run_context: dict) -> List[Any]:
        """Discover artifacts from a run context dict."""
        from research_registry.registry_schema import RunArtifact
        result = []
        try:
            paths = run_context.get("output_files", []) or run_context.get("artifacts", [])
            run_id = run_context.get("run_id", "")
            for path in paths:
                art = self.register_artifact(run_id, path)
                if art:
                    result.append(art)
        except Exception as exc:
            logger.warning("discover_artifacts failed (non-fatal): %s", exc)
        return result

    def register_artifact(self, run_id: str, path: str, artifact_type: Optional[str] = None) -> Optional[Any]:
        """Register an artifact by path and return RunArtifact."""
        from research_registry.registry_schema import RunArtifact
        try:
            if not path:
                return None

            artifact_id = _new_uuid()
            rel_path = _repo_relative(path)
            filename = os.path.basename(path)
            ext = os.path.splitext(filename)[1].lower()
            a_type = artifact_type or self.detect_artifact_type(path)

            abs_path = path if os.path.isabs(path) else os.path.join(BASE_DIR, path)
            exists = os.path.isfile(abs_path)
            size_bytes = 0
            checksum = ""
            created_at = ""
            modified_at = ""

            if exists:
                try:
                    stat = os.stat(abs_path)
                    size_bytes = stat.st_size
                    created_at = datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).isoformat()
                    modified_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
                    if size_bytes <= self._checksum_size_limit:
                        checksum = self.calculate_checksum(abs_path)
                except Exception:
                    pass

            art = RunArtifact(
                artifact_id=artifact_id,
                run_id=run_id,
                artifact_type=a_type,
                path=rel_path,
                filename=filename,
                extension=ext,
                exists=exists,
                size_bytes=size_bytes,
                checksum=checksum,
                created_at=created_at,
                modified_at=modified_at,
                metadata={"local_path": path if os.path.isabs(path) else ""},
            )

            self._artifacts[artifact_id] = art.to_dict()
            if run_id not in self._run_artifacts:
                self._run_artifacts[run_id] = []
            self._run_artifacts[run_id].append(artifact_id)

            return art
        except Exception as exc:
            logger.warning("register_artifact failed (non-fatal): %s", exc)
            return None

    def register_outputs(self, run_id: str, paths: List[str]) -> List[Any]:
        """Register multiple artifacts for a run."""
        result = []
        for path in (paths or []):
            art = self.register_artifact(run_id, path)
            if art:
                result.append(art)
        return result

    def detect_artifact_type(self, path: str) -> str:
        """Detect artifact type from file extension."""
        ext = os.path.splitext(path)[1].lower()
        return _EXT_TYPE_MAP.get(ext, "OTHER")

    def calculate_checksum(self, path: str) -> str:
        """Calculate SHA-256 checksum of a file."""
        try:
            h = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception as exc:
            logger.debug("calculate_checksum failed for %s (non-fatal): %s", path, exc)
            return ""

    def validate_artifact(self, path: str) -> dict:
        """Validate an artifact: check existence, compute checksum."""
        result = {"path": path, "exists": False, "size_bytes": 0, "checksum": "", "valid": False}
        try:
            abs_path = path if os.path.isabs(path) else os.path.join(BASE_DIR, path)
            result["exists"] = os.path.isfile(abs_path)
            if result["exists"]:
                stat = os.stat(abs_path)
                result["size_bytes"] = stat.st_size
                if stat.st_size <= self._checksum_size_limit:
                    result["checksum"] = self.calculate_checksum(abs_path)
                result["valid"] = True
        except Exception as exc:
            result["error"] = str(exc)
        return result

    def list_artifacts(self, run_id: str) -> List[Any]:
        """Return list of RunArtifact for a run."""
        from research_registry.registry_schema import RunArtifact
        art_ids = self._run_artifacts.get(run_id, [])
        result = []
        for aid in art_ids:
            d = self._artifacts.get(aid)
            if d:
                result.append(RunArtifact.from_dict(d))
        return result

    def find_missing_artifacts(self) -> List[Any]:
        """Return list of RunArtifact where exists=False."""
        from research_registry.registry_schema import RunArtifact
        result = []
        for d in self._artifacts.values():
            if not d.get("exists", False):
                result.append(RunArtifact.from_dict(d))
        return result

    def compare_artifacts(self, run_a: str, run_b: str) -> dict:
        """Compare artifact sets for two runs."""
        arts_a = {a.filename: a for a in self.list_artifacts(run_a)}
        arts_b = {a.filename: a for a in self.list_artifacts(run_b)}

        only_in_a = [f for f in arts_a if f not in arts_b]
        only_in_b = [f for f in arts_b if f not in arts_a]
        shared = [f for f in arts_a if f in arts_b]
        checksum_matches = [f for f in shared if arts_a[f].checksum and arts_b[f].checksum and arts_a[f].checksum == arts_b[f].checksum]
        checksum_mismatches = [f for f in shared if arts_a[f].checksum and arts_b[f].checksum and arts_a[f].checksum != arts_b[f].checksum]

        return {
            "only_in_a": only_in_a,
            "only_in_b": only_in_b,
            "shared": shared,
            "checksum_matches": checksum_matches,
            "checksum_mismatches": checksum_mismatches,
        }

    def artifact_summary(self, run_id: str) -> dict:
        """Return summary of artifacts for a run."""
        arts = self.list_artifacts(run_id)
        return {
            "run_id": run_id,
            "total": len(arts),
            "existing": sum(1 for a in arts if a.exists),
            "missing": sum(1 for a in arts if not a.exists),
            "total_size_bytes": sum(a.size_bytes for a in arts),
            "with_checksum": sum(1 for a in arts if a.checksum),
        }

    def get_artifact(self, artifact_id: str) -> Optional[Any]:
        """Return a RunArtifact by artifact_id."""
        from research_registry.registry_schema import RunArtifact
        d = self._artifacts.get(artifact_id)
        if d:
            return RunArtifact.from_dict(d)
        return None

    def load_from_records(self, artifact_records: List[dict]) -> None:
        """Load artifact records from a list of dicts."""
        for rec in artifact_records:
            aid = rec.get("artifact_id", "")
            run_id = rec.get("run_id", "")
            if aid:
                self._artifacts[aid] = rec
                if run_id:
                    if run_id not in self._run_artifacts:
                        self._run_artifacts[run_id] = []
                    if aid not in self._run_artifacts[run_id]:
                        self._run_artifacts[run_id].append(aid)

    def all_artifacts(self) -> List[dict]:
        """Return all artifact records as list of dicts."""
        return list(self._artifacts.values())
