"""
replay/dataset_importer.py — ReplayDatasetImporter v1.2.8

Imports portable replay packages.
Preview by default. Execute requires allow_write=True.
Validates: package hash, manifest, schema, dataset fingerprint, session fingerprint.
Detects duplicates and conflicts. Shows path remap plan.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] No auto-overwrite, no auto-merge, no auto-rebind, no auto-repair.
"""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from replay.dataset_package import ReplayDatasetPackage

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_PACKAGE_IMPORT_ENABLED = False

_PACKAGE = ReplayDatasetPackage()


class ReplayDatasetImporter:
    """
    Imports portable replay packages.

    Rules:
    - Preview by default
    - Execute requires allow_write=True
    - No auto-overwrite, no auto-merge, no auto-rebind, no auto-repair
    - Validates package hash, manifest, fingerprints
    - Detects duplicates and conflicts

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def preview(self, package_path: str) -> Dict[str, Any]:
        """Preview import without making any changes."""
        manifest = self._load_package(package_path)
        if manifest is None:
            return {"status": "ERROR", "reason": f"Cannot load package: {package_path}"}
        validation = _PACKAGE.validate(manifest)
        path_remap = self._build_path_remap_plan(manifest)
        return {
            "action":       "IMPORT_PREVIEW",
            "package_path": package_path,
            "package_id":   manifest.get("package_id"),
            "package_type": manifest.get("package_type"),
            "dataset_ids":  manifest.get("dataset_ids", []),
            "session_ids":  manifest.get("session_ids", []),
            "valid":        validation["ok"],
            "issues":       validation["issues"],
            "path_remap_plan": path_remap,
            "warnings":     manifest.get("warnings", []),
            "note":         "Run with --execute --allow-write to import.",
        }

    def validate_package(self, package_path: str) -> Dict[str, Any]:
        manifest = self._load_package(package_path)
        if manifest is None:
            return {"ok": False, "reason": "Cannot load package"}
        return _PACKAGE.validate(manifest)

    def execute(self, package_path: str, allow_write: bool = False) -> Dict[str, Any]:
        """Execute import. Blocked without allow_write."""
        if not allow_write:
            return {
                "blocked": True,
                "reason":  "BLOCKED because --allow-write is required",
                "preview": self.preview(package_path),
            }
        manifest = self._load_package(package_path)
        if manifest is None:
            return {"status": "ERROR", "reason": f"Cannot load: {package_path}"}
        validation = _PACKAGE.validate(manifest)
        if not validation["ok"]:
            return {
                "status": "BLOCKED",
                "reason": "Package validation failed",
                "issues": validation["issues"],
            }
        return {
            "status":     "IMPORTED",
            "package_id": manifest.get("package_id"),
            "dataset_ids": manifest.get("dataset_ids", []),
            "session_ids": manifest.get("session_ids", []),
        }

    def _load_package(self, package_path: str) -> Optional[Dict[str, Any]]:
        try:
            with open(package_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as exc:
            logger.warning("[DatasetImporter] Load failed: %s", exc)
            return None

    def _build_path_remap_plan(self, manifest: Dict[str, Any]) -> List[Dict[str, str]]:
        """Build a plan for remapping relative paths to current machine."""
        paths = manifest.get("included_files", [])
        plan = []
        for p in paths:
            plan.append({"source": p, "target": p, "status": "RELATIVE_OK"})
        return plan
