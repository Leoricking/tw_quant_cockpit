"""
gui/replay_dataset_detail_dialog.py — Dataset Detail dialog v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetDetailDialog:
    """
    Displays full dataset detail: manifest, versions, lineage, validation,
    integrity, fingerprint, qualification.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, dataset_id: Optional[str] = None) -> None:
        self._dataset_id = dataset_id
        self._registry: Optional[Any] = None

    def _get_registry(self) -> Optional[Any]:
        if self._registry is None:
            try:
                from replay.dataset_registry import ReplayDatasetRegistry
                self._registry = ReplayDatasetRegistry()
            except Exception as exc:
                logger.warning("DatasetRegistry unavailable: %s", exc)
        return self._registry

    def load(self, dataset_id: str) -> Dict[str, Any]:
        self._dataset_id = dataset_id
        reg = self._get_registry()
        if reg is None:
            return {"error": "Registry unavailable", "dataset_id": dataset_id}
        try:
            d = reg.get_dataset(dataset_id)
            return vars(d) if d and hasattr(d, "__dict__") else (d or {})
        except Exception as exc:
            logger.warning("load failed: %s", exc)
            return {"error": str(exc), "dataset_id": dataset_id}

    def get_versions(self, dataset_id: str) -> List[Dict[str, Any]]:
        try:
            from replay.dataset_version import ReplayDatasetVersionManager
            vm = ReplayDatasetVersionManager()
            return vm.list_versions(dataset_id)
        except Exception as exc:
            logger.warning("get_versions failed: %s", exc)
            return []

    def get_lineage(self, dataset_id: str) -> Dict[str, Any]:
        try:
            from replay.dataset_lineage import ReplayDatasetLineageManager
            lm = ReplayDatasetLineageManager()
            return {
                "ancestors":   lm.ancestors(dataset_id),
                "descendants": lm.descendants(dataset_id),
                "root":        lm.root(dataset_id),
            }
        except Exception as exc:
            logger.warning("get_lineage failed: %s", exc)
            return {}

    def get_validation(self, dataset_id: str) -> Dict[str, Any]:
        try:
            from replay.dataset_validator import ReplayDatasetValidator
            reg = self._get_registry()
            if reg is None:
                return {}
            d = reg.get_dataset(dataset_id)
            if d is None:
                return {}
            return ReplayDatasetValidator().validate(d)
        except Exception as exc:
            logger.warning("get_validation failed: %s", exc)
            return {}

    def get_integrity(self, dataset_id: str) -> Dict[str, Any]:
        try:
            from replay.dataset_integrity import ReplayDatasetIntegrityChecker
            reg = self._get_registry()
            if reg is None:
                return {}
            d = reg.get_dataset(dataset_id)
            if d is None:
                return {}
            return ReplayDatasetIntegrityChecker().check(d)
        except Exception as exc:
            logger.warning("get_integrity failed: %s", exc)
            return {}

    def get_tab_sections(self) -> List[str]:
        return ["Overview", "Versions", "Lineage", "Validation", "Integrity", "Fingerprint"]
