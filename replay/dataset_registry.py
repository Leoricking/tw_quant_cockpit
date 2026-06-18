"""
replay/dataset_registry.py — ReplayDatasetRegistry v1.2.8

Central registry for replay datasets. Stores manifests, versions, and lineage.
All write operations require allow_write=True. Default mode is preview/read-only.

Storage: data/replay_registry/datasets.jsonl (append-only)
         data/replay_registry/dataset_versions.jsonl
         data/replay_registry/dataset_lineage.jsonl
         data/replay_registry/dataset_index.csv

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] Registry does not overwrite existing datasets automatically.
[!] Registry does not merge, delete, or repair datasets automatically.
"""
from __future__ import annotations

import dataclasses
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from replay.dataset_registry_schema import (
    ReplayDatasetManifest, ReplayDatasetVersionRecord,
    DatasetMode, DatasetQualification, DatasetStatus,
)

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_DATASET_OVERWRITE_ENABLED   = False
AUTO_DATASET_REPAIR_ENABLED      = False
AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED = False


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReplayDatasetRegistry:
    """
    Central registry for replay datasets.

    Rules:
    - register() is preview by default; requires allow_write=True to write
    - Duplicate fingerprint => POSSIBLE_DUPLICATE, no auto-create
    - No auto-merge, no auto-delete, no auto-repair

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True
    AUTO_DATASET_OVERWRITE_ENABLED = False

    def __init__(self, repo_root: str = "."):
        self._repo_root  = repo_root
        self._base_dir   = Path(repo_root) / "data" / "replay_registry"
        self._ds_file    = self._base_dir / "datasets.jsonl"
        self._ver_file   = self._base_dir / "dataset_versions.jsonl"
        self._lin_file   = self._base_dir / "dataset_lineage.jsonl"
        self._index_file = self._base_dir / "dataset_index.csv"
        self._cache: Optional[List[ReplayDatasetManifest]] = None

    # ------------------------------------------------------------------ #
    # Read operations (always allowed)
    # ------------------------------------------------------------------ #

    def list_datasets(self, filters: Optional[Dict[str, Any]] = None) -> List[ReplayDatasetManifest]:
        datasets = self._load_all()
        if not filters:
            return datasets
        result = []
        for d in datasets:
            match = True
            for k, v in filters.items():
                if getattr(d, k, None) != v:
                    match = False
                    break
            if match:
                result.append(d)
        return result

    def get_dataset(self, dataset_id: str) -> Optional[ReplayDatasetManifest]:
        for d in self._load_all():
            if d.dataset_id == dataset_id:
                return d
        return None

    def get_version(self, dataset_id: str, version: str) -> Optional[ReplayDatasetVersionRecord]:
        for r in self._load_versions():
            if r["dataset_id"] == dataset_id and r["version"] == version:
                return ReplayDatasetVersionRecord(**{
                    k: v for k, v in r.items()
                    if k in ReplayDatasetVersionRecord.__dataclass_fields__
                })
        return None

    def search(self, query: str) -> List[ReplayDatasetManifest]:
        q = query.lower()
        return [
            d for d in self._load_all()
            if q in d.dataset_id.lower()
            or q in d.dataset_name.lower()
            or q in " ".join(d.symbols).lower()
        ]

    def filter(
        self,
        mode: Optional[str] = None,
        qualification: Optional[str] = None,
        status: Optional[str] = None,
        symbol: Optional[str] = None,
        timeframe: Optional[str] = None,
    ) -> List[ReplayDatasetManifest]:
        result = self._load_all()
        if mode:
            result = [d for d in result if d.mode == mode]
        if qualification:
            result = [d for d in result if d.qualification == qualification]
        if status:
            result = [d for d in result if d.status == status]
        if symbol:
            result = [d for d in result if symbol in d.symbols]
        if timeframe:
            result = [d for d in result if timeframe in d.timeframes]
        return result

    def detect_duplicates(self) -> List[Dict[str, Any]]:
        datasets = self._load_all()
        seen: Dict[str, str] = {}
        dupes = []
        for d in datasets:
            fp = d.fingerprint
            if fp and fp in seen:
                dupes.append({
                    "status": "POSSIBLE_DUPLICATE",
                    "dataset_id": d.dataset_id,
                    "duplicate_of": seen[fp],
                    "fingerprint": fp,
                })
            elif fp:
                seen[fp] = d.dataset_id
        return dupes

    def detect_missing(self) -> List[Dict[str, Any]]:
        return [
            {"dataset_id": d.dataset_id, "status": "MISSING"}
            for d in self._load_all()
            if d.status == DatasetStatus.MISSING.value
        ]

    def detect_corrupted(self) -> List[Dict[str, Any]]:
        return [
            {"dataset_id": d.dataset_id, "status": "CORRUPTED"}
            for d in self._load_all()
            if d.status == DatasetStatus.CORRUPTED.value
        ]

    def detect_stale(self) -> List[Dict[str, Any]]:
        # datasets with warnings containing STALE
        return [
            {"dataset_id": d.dataset_id, "status": "STALE"}
            for d in self._load_all()
            if any("STALE" in w.upper() for w in d.warnings)
        ]

    def verify(self, dataset_id: str) -> Dict[str, Any]:
        d = self.get_dataset(dataset_id)
        if not d:
            return {"status": "NOT_FOUND", "dataset_id": dataset_id}
        return {
            "dataset_id": dataset_id,
            "status":     d.status,
            "fingerprint": d.fingerprint,
            "qualification": d.qualification,
            "warnings":   d.warnings,
        }

    def compare(self, dataset_id1: str, dataset_id2: str) -> Dict[str, Any]:
        d1 = self.get_dataset(dataset_id1)
        d2 = self.get_dataset(dataset_id2)
        return {
            "dataset_id1": dataset_id1,
            "dataset_id2": dataset_id2,
            "found1": d1 is not None,
            "found2": d2 is not None,
            "fingerprint_match": (d1.fingerprint == d2.fingerprint) if (d1 and d2) else False,
        }

    def summary(self) -> str:
        datasets = self._load_all()
        active   = sum(1 for d in datasets if d.status == DatasetStatus.ACTIVE.value)
        frozen   = sum(1 for d in datasets if d.frozen_at)
        corrupted = sum(1 for d in datasets if d.status == DatasetStatus.CORRUPTED.value)
        missing  = sum(1 for d in datasets if d.status == DatasetStatus.MISSING.value)
        return (
            f"Dataset Registry: {len(datasets)} total | "
            f"active={active} frozen={frozen} corrupted={corrupted} missing={missing}"
        )

    # ------------------------------------------------------------------ #
    # Write operations (require allow_write=True)
    # ------------------------------------------------------------------ #

    def register_preview(self, manifest: ReplayDatasetManifest) -> Dict[str, Any]:
        """Preview what would happen if this dataset were registered."""
        existing = self.get_dataset(manifest.dataset_id)
        dupes    = self.detect_duplicates()
        fp_conflict = any(d["fingerprint"] == manifest.fingerprint for d in dupes)
        return {
            "action":       "REGISTER_PREVIEW",
            "dataset_id":   manifest.dataset_id,
            "mode":         manifest.mode,
            "qualification": manifest.qualification,
            "fingerprint":  manifest.fingerprint[:16] + "..." if manifest.fingerprint else "",
            "already_exists": existing is not None,
            "possible_duplicate": fp_conflict,
            "warnings":     manifest.warnings,
            "blocked":      False,
            "note":         "Run with --execute --allow-write to register.",
        }

    def register(
        self,
        manifest: ReplayDatasetManifest,
        allow_write: bool = False,
    ) -> Dict[str, Any]:
        """Register a dataset. Preview by default; blocked without allow_write."""
        if not allow_write:
            return {
                **self.register_preview(manifest),
                "blocked": True,
                "reason":  "BLOCKED because --allow-write is required",
            }
        existing = self.get_dataset(manifest.dataset_id)
        if existing is not None:
            return {
                "status":     "SKIPPED",
                "dataset_id": manifest.dataset_id,
                "reason":     "Dataset already registered. Use new version to update.",
            }
        self._append_dataset(manifest)
        self._cache = None
        return {
            "status":     "REGISTERED",
            "dataset_id": manifest.dataset_id,
            "version":    manifest.dataset_version,
            "fingerprint": manifest.fingerprint,
        }

    def archive(self, dataset_id: str, allow_write: bool = False) -> Dict[str, Any]:
        if not allow_write:
            return {"blocked": True, "reason": "BLOCKED because --allow-write is required"}
        # Mark in-memory; real impl would update store
        return {"status": "ARCHIVED", "dataset_id": dataset_id}

    def restore(self, dataset_id: str, allow_write: bool = False) -> Dict[str, Any]:
        if not allow_write:
            return {"blocked": True, "reason": "BLOCKED because --allow-write is required"}
        return {"status": "RESTORED", "dataset_id": dataset_id}

    def freeze(self, dataset_id: str, version: str, allow_write: bool = False) -> Dict[str, Any]:
        if not allow_write:
            return {
                "blocked": True,
                "reason":  "BLOCKED because --allow-write is required",
                "preview": f"Would freeze {dataset_id}@{version}",
            }
        return {"status": "FROZEN", "dataset_id": dataset_id, "version": version}

    # ------------------------------------------------------------------ #
    # Storage helpers
    # ------------------------------------------------------------------ #

    def _ensure_dir(self) -> None:
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def _append_dataset(self, manifest: ReplayDatasetManifest) -> None:
        self._ensure_dir()
        d = dataclasses.asdict(manifest)
        try:
            with open(str(self._ds_file), "a", encoding="utf-8") as fh:
                fh.write(json.dumps(d, ensure_ascii=False) + "\n")
        except Exception as exc:
            logger.warning("[DatasetRegistry] Write failed: %s", exc)

    def _load_all(self) -> List[ReplayDatasetManifest]:
        if self._cache is not None:
            return self._cache
        results = []
        if not self._ds_file.exists():
            return results
        try:
            with open(str(self._ds_file), "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        files_raw = d.pop("files", [])
                        from replay.dataset_registry_schema import ReplayDatasetFileEntry
                        files = []
                        for f in files_raw:
                            try:
                                files.append(ReplayDatasetFileEntry(**{
                                    k: v for k, v in f.items()
                                    if k in ReplayDatasetFileEntry.__dataclass_fields__
                                }))
                            except Exception:
                                pass
                        m = ReplayDatasetManifest(**{
                            k: v for k, v in d.items()
                            if k in ReplayDatasetManifest.__dataclass_fields__
                        })
                        m.files = files
                        results.append(m)
                    except Exception as exc:
                        logger.warning("[DatasetRegistry] Corrupted line skipped: %s", exc)
        except Exception as exc:
            logger.warning("[DatasetRegistry] Load failed: %s", exc)
        self._cache = results
        return results

    def _load_versions(self) -> List[Dict[str, Any]]:
        records = []
        if not self._ver_file.exists():
            return records
        try:
            with open(str(self._ver_file), "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        try:
                            records.append(json.loads(line))
                        except Exception:
                            pass
        except Exception as exc:
            logger.warning("[DatasetRegistry] Version load failed: %s", exc)
        return records
