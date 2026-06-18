"""
gui/replay_dataset_package_dialog.py — Dataset Package dialog v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] Packages must never contain secrets, .env, API tokens, broker credentials,
    absolute paths.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetPackageDialog:
    """
    Build and validate portable dataset packages.
    path_mode always RELATIVE_ONLY.
    Scans for secrets and absolute paths automatically.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] RELATIVE_ONLY path mode. No secrets, no broker credentials.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True
    PATH_MODE      = "RELATIVE_ONLY"

    def __init__(self, dataset_id: Optional[str] = None) -> None:
        self._dataset_id = dataset_id

    def build_package_manifest(self, dataset_id: str) -> Dict[str, Any]:
        try:
            from replay.dataset_registry import ReplayDatasetRegistry
            from replay.dataset_package import ReplayDatasetPackage
            reg = ReplayDatasetRegistry()
            d   = reg.get_dataset(dataset_id)
            if d is None:
                return {"error": f"Dataset {dataset_id!r} not found"}
            pkg = ReplayDatasetPackage()
            return pkg.build_manifest(d)
        except Exception as exc:
            logger.warning("build_package_manifest failed: %s", exc)
            return {"error": str(exc)}

    def validate_package(self, dataset_id: str) -> Dict[str, Any]:
        try:
            from replay.dataset_registry import ReplayDatasetRegistry
            from replay.dataset_package import ReplayDatasetPackage
            reg = ReplayDatasetRegistry()
            d   = reg.get_dataset(dataset_id)
            if d is None:
                return {"error": f"Dataset {dataset_id!r} not found"}
            pkg = ReplayDatasetPackage()
            return pkg.validate(d)
        except Exception as exc:
            logger.warning("validate_package failed: %s", exc)
            return {"error": str(exc)}

    def export_preview(self, dataset_id: str, output_path: str = "") -> Dict[str, Any]:
        try:
            from replay.dataset_exporter import ReplayDatasetExporter
            return ReplayDatasetExporter().preview(dataset_id, output_path=output_path)
        except Exception as exc:
            logger.warning("export_preview failed: %s", exc)
            return {"blocked": True, "reason": str(exc)}
