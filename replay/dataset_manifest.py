"""
replay/dataset_manifest.py — ReplayDatasetManifestBuilder v1.2.8

Builds, loads, saves, normalizes, and validates dataset manifests.
Manifests use relative paths only and record all coverage metadata.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from replay.dataset_registry_schema import (
    ReplayDatasetManifest, ReplayDatasetFileEntry,
    DatasetMode, DatasetQualification, DatasetStatus, FileLogicalRole,
)
from replay.dataset_fingerprint import ReplayDatasetFingerprint

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

_FINGERPRINTER = ReplayDatasetFingerprint()


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class ReplayDatasetManifestBuilder:
    """
    Builds and manages dataset manifests.

    Manifests record real/mock mode, source, schema, files, hashes,
    relative paths, symbols, timeframes, date range, row counts,
    qualification, PIT status, and warnings.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def build(
        self,
        dataset_id: str,
        dataset_name: str,
        dataset_path: str,
        mode: str = DatasetMode.MOCK.value,
        source_type: str = "MANUAL",
        source_name: str = "",
        schema_version: str = "1.0",
    ) -> ReplayDatasetManifest:
        """Build a manifest from a dataset directory."""
        base = Path(dataset_path)
        files = self.collect_files(dataset_path)
        symbols = self.collect_symbols(files)
        timeframes = self.collect_timeframes(files)
        field_names = self.collect_fields(files)
        row_count = sum(f.row_count for f in files)
        file_count = len(files)
        total_bytes = sum(f.size_bytes for f in files)
        rel_paths = [f.relative_path for f in files]
        warnings = []
        if mode == DatasetMode.MOCK.value:
            warnings.append("DEMO_ONLY: dataset is MOCK")
        ts = _now_utc()
        manifest = ReplayDatasetManifest(
            dataset_id=dataset_id,
            dataset_name=dataset_name,
            schema_version=schema_version,
            mode=mode,
            source_type=source_type,
            source_name=source_name,
            created_at=ts,
            updated_at=ts,
            symbols=symbols,
            timeframes=timeframes,
            row_count=row_count,
            file_count=file_count,
            total_size_bytes=total_bytes,
            field_names=field_names,
            relative_paths=rel_paths,
            files=files,
            warnings=warnings,
            status=DatasetStatus.ACTIVE.value,
        )
        manifest.qualification = self._derive_qualification(manifest)
        manifest.manifest_hash = self._hash_manifest(manifest)
        manifest.fingerprint   = _FINGERPRINTER.calculate_manifest_fingerprint(
            self._to_dict(manifest)
        )
        return manifest

    def load(self, manifest_path: str) -> ReplayDatasetManifest:
        """Load manifest from JSON file."""
        with open(manifest_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        files_raw = data.pop("files", [])
        files = [
            ReplayDatasetFileEntry(**{
                k: v for k, v in f.items()
                if k in ReplayDatasetFileEntry.__dataclass_fields__
            })
            for f in files_raw
        ]
        manifest = ReplayDatasetManifest(
            **{k: v for k, v in data.items()
               if k in ReplayDatasetManifest.__dataclass_fields__}
        )
        manifest.files = files
        return manifest

    def save(self, manifest: ReplayDatasetManifest, output_path: str, allow_write: bool = False) -> None:
        """Save manifest to JSON. Requires allow_write=True."""
        if not allow_write:
            logger.warning("[ManifestBuilder] save blocked: allow_write=False")
            return
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(self._to_dict(manifest), fh, ensure_ascii=False, indent=2)

    def normalize(self, manifest: ReplayDatasetManifest) -> ReplayDatasetManifest:
        """Normalize paths to relative."""
        manifest.relative_paths = [p.replace("\\", "/") for p in manifest.relative_paths]
        for f in manifest.files:
            f.relative_path = f.relative_path.replace("\\", "/")
        return manifest

    def validate(self, manifest: ReplayDatasetManifest) -> List[str]:
        """Return list of validation warnings (empty = OK)."""
        warnings = []
        if not manifest.dataset_id:
            warnings.append("MISSING dataset_id")
        if not manifest.symbols:
            warnings.append("WARN: no symbols listed")
        if not manifest.timeframes:
            warnings.append("WARN: no timeframes listed")
        if manifest.mode == DatasetMode.MOCK.value:
            warnings.append("DEMO_ONLY: mock dataset")
        if manifest.qualification == DatasetQualification.BLOCKED.value:
            warnings.append("BLOCKED: dataset is blocked")
        for f in manifest.files:
            if f.required and not f.present:
                warnings.append(f"MISSING required file: {f.relative_path}")
        return warnings

    def collect_files(self, dataset_path: str) -> List[ReplayDatasetFileEntry]:
        """Scan directory for dataset files."""
        entries = []
        base = Path(dataset_path)
        if not base.exists():
            return entries
        for p in sorted(base.rglob("*")):
            if p.is_file() and not p.name.startswith("."):
                rel = str(p.relative_to(base)).replace("\\", "/")
                size = p.stat().st_size
                entries.append(ReplayDatasetFileEntry(
                    file_id=hashlib.sha256(rel.encode()).hexdigest()[:12],
                    relative_path=rel,
                    logical_role=self._guess_role(p.name),
                    file_type=p.suffix.lstrip(".").upper() or "UNKNOWN",
                    size_bytes=size,
                    present=True,
                ))
        return entries

    def collect_symbols(self, files: List[ReplayDatasetFileEntry]) -> List[str]:
        """Extract symbol list from file names (heuristic)."""
        symbols = set()
        for f in files:
            parts = Path(f.relative_path).stem.split("_")
            for p in parts:
                if p.isdigit() and len(p) == 4:
                    symbols.add(p)
        return sorted(symbols) or ["TST"]

    def collect_timeframes(self, files: List[ReplayDatasetFileEntry]) -> List[str]:
        """Extract timeframe list from file names (heuristic)."""
        tfs = set()
        known = {"D1", "M60", "M20", "M15", "M5", "M1", "W1"}
        for f in files:
            stem = Path(f.relative_path).stem.upper()
            for tf in known:
                if tf in stem:
                    tfs.add(tf)
        return sorted(tfs) or ["D1"]

    def collect_fields(self, files: List[ReplayDatasetFileEntry]) -> List[str]:
        """Standard OHLCV fields (placeholder)."""
        return ["open", "high", "low", "close", "volume"]

    def calculate_coverage(self, manifest: ReplayDatasetManifest) -> Dict[str, Any]:
        return {
            "symbols":    manifest.symbols,
            "timeframes": manifest.timeframes,
            "fields":     manifest.field_names,
            "files":      manifest.file_count,
            "rows":       manifest.row_count,
        }

    def calculate_hashes(self, files: List[ReplayDatasetFileEntry]) -> Dict[str, str]:
        return {f.relative_path: f.content_hash for f in files}

    def build_warnings(self, manifest: ReplayDatasetManifest) -> List[str]:
        return self.validate(manifest)

    def summary(self, manifest: ReplayDatasetManifest) -> str:
        return (
            f"Dataset: {manifest.dataset_id} v{manifest.dataset_version} | "
            f"Mode: {manifest.mode} | Qual: {manifest.qualification} | "
            f"Files: {manifest.file_count} | Rows: {manifest.row_count} | "
            f"Symbols: {manifest.symbols} | Timeframes: {manifest.timeframes}"
        )

    # ------------------------------------------------------------------ #

    def _guess_role(self, filename: str) -> str:
        fn = filename.lower()
        if "daily" in fn or "_d1" in fn:
            return FileLogicalRole.DAILY_OHLCV.value
        if "intraday" in fn or any(tf in fn for tf in ["m60", "m20", "m15", "m5", "m1"]):
            return FileLogicalRole.INTRADAY_OHLCV.value
        if "meta" in fn:
            return FileLogicalRole.METADATA.value
        if "calendar" in fn:
            return FileLogicalRole.CALENDAR.value
        return FileLogicalRole.OTHER.value

    def _derive_qualification(self, manifest: ReplayDatasetManifest) -> str:
        if manifest.mode == DatasetMode.MOCK.value:
            return DatasetQualification.MOCK_DEMO_ONLY.value
        if not manifest.symbols or not manifest.timeframes:
            return DatasetQualification.INSUFFICIENT.value
        if not manifest.point_in_time_verified:
            return DatasetQualification.REAL_UNVERIFIED.value
        return DatasetQualification.VERIFIED_REAL.value

    def _hash_manifest(self, manifest: ReplayDatasetManifest) -> str:
        d = self._to_dict(manifest)
        d.pop("manifest_hash", None)
        d.pop("fingerprint", None)
        return hashlib.sha256(
            json.dumps(d, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()

    def _to_dict(self, manifest: ReplayDatasetManifest) -> Dict[str, Any]:
        import dataclasses
        d = dataclasses.asdict(manifest)
        return d
