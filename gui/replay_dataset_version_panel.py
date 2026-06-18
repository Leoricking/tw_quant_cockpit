"""
gui/replay_dataset_version_panel.py — Dataset Version panel v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetVersionPanel:
    """
    Displays version history for a dataset. Frozen versions shown with lock icon.
    Create-version requires explicit preview + execute.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    COLUMNS = ["version", "status", "frozen", "fingerprint", "created_at", "notes"]

    def __init__(self, dataset_id: Optional[str] = None) -> None:
        self._dataset_id = dataset_id

    def _get_version_manager(self) -> Optional[Any]:
        try:
            from replay.dataset_version import ReplayDatasetVersionManager
            return ReplayDatasetVersionManager()
        except Exception as exc:
            logger.warning("VersionManager unavailable: %s", exc)
            return None

    def list_versions(self, dataset_id: str) -> List[Dict[str, Any]]:
        vm = self._get_version_manager()
        if vm is None:
            return []
        try:
            return vm.list_versions(dataset_id)
        except Exception as exc:
            logger.warning("list_versions failed: %s", exc)
            return []

    def preview_create_version(self, dataset_id: str, notes: str = "") -> Dict[str, Any]:
        vm = self._get_version_manager()
        if vm is None:
            return {"blocked": True, "reason": "VersionManager unavailable"}
        try:
            return vm.create_version_preview(dataset_id, notes=notes)
        except Exception as exc:
            logger.warning("preview_create_version failed: %s", exc)
            return {"blocked": True, "reason": str(exc)}

    def freeze_version_preview(self, dataset_id: str, version: str) -> Dict[str, Any]:
        try:
            from replay.dataset_freeze import ReplayDatasetFreezeManager
            return ReplayDatasetFreezeManager().freeze_preview(dataset_id, version)
        except Exception as exc:
            logger.warning("freeze_version_preview failed: %s", exc)
            return {"blocked": True, "reason": str(exc)}

    def summary(self, dataset_id: str) -> Dict[str, Any]:
        versions = self.list_versions(dataset_id)
        frozen   = [v for v in versions if v.get("frozen")]
        return {
            "dataset_id":     dataset_id,
            "total_versions": len(versions),
            "frozen_count":   len(frozen),
            "research_only":  True,
        }
