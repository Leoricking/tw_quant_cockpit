"""
replay/dataset_exporter.py — ReplayDatasetExporter v1.2.8

Exports replay datasets as portable packages.
Preview by default. Execute requires allow_write=True.
Does not auto-overwrite existing packages.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

from replay.dataset_package import ReplayDatasetPackage
from replay.dataset_portability import MANIFEST_ONLY, METADATA_ONLY, FULL_PORTABLE

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

_PACKAGE = ReplayDatasetPackage()


class ReplayDatasetExporter:
    """
    Exports datasets as portable packages.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def preview(
        self,
        dataset_id: str,
        package_type: str = MANIFEST_ONLY,
        session_ids: Optional[List[str]] = None,
        output_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Preview export without writing anything."""
        manifest = _PACKAGE.build_manifest(
            dataset_ids=[dataset_id],
            session_ids=session_ids or [],
            package_type=package_type,
        )
        return {
            "action":       "EXPORT_PREVIEW",
            "dataset_id":   dataset_id,
            "package_type": package_type,
            "package_id":   manifest["package_id"],
            "included_files": manifest["included_files"],
            "excluded_files": manifest["excluded_files"],
            "total_size":   manifest["total_size"],
            "qualification": manifest["qualification"],
            "path_mode":    manifest["path_mode"],
            "warnings":     manifest["warnings"],
            "note":         "Run with --execute --allow-write to export.",
        }

    def execute(
        self,
        dataset_id: str,
        package_type: str = MANIFEST_ONLY,
        output_dir: str = "data/replay_registry/exports",
        allow_write: bool = False,
        session_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Execute export. Blocked without allow_write."""
        if not allow_write:
            return {
                "blocked": True,
                "reason":  "BLOCKED because --allow-write is required",
                "preview": self.preview(dataset_id, package_type, session_ids, output_dir),
            }
        manifest = _PACKAGE.build_manifest(
            dataset_ids=[dataset_id],
            session_ids=session_ids or [],
            package_type=package_type,
        )
        package_path = os.path.join(output_dir, f"{manifest['package_id']}.json")
        if os.path.exists(package_path):
            return {
                "status": "BLOCKED",
                "reason": f"Package already exists: {package_path}. No auto-overwrite.",
            }
        os.makedirs(output_dir, exist_ok=True)
        import json
        with open(package_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
        return {
            "status":       "EXPORTED",
            "package_path": package_path,
            "package_id":   manifest["package_id"],
            "package_type": package_type,
            "dataset_id":   dataset_id,
        }
