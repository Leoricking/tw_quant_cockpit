"""
gui/replay_dataset_lineage_dialog.py — Dataset Lineage dialog v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetLineageDialog:
    """
    Visualizes dataset lineage tree: ancestors, descendants, root.
    Detects cycles. No cycles allowed.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, dataset_id: Optional[str] = None) -> None:
        self._dataset_id = dataset_id
        self._lineage_manager: Optional[Any] = None

    def _get_lineage_manager(self) -> Optional[Any]:
        if self._lineage_manager is None:
            try:
                from replay.dataset_lineage import ReplayDatasetLineageManager
                self._lineage_manager = ReplayDatasetLineageManager()
            except Exception as exc:
                logger.warning("LineageManager unavailable: %s", exc)
        return self._lineage_manager

    def get_ancestors(self, dataset_id: str) -> List[str]:
        lm = self._get_lineage_manager()
        if lm is None:
            return []
        try:
            return lm.ancestors(dataset_id)
        except Exception as exc:
            logger.warning("get_ancestors failed: %s", exc)
            return []

    def get_descendants(self, dataset_id: str) -> List[str]:
        lm = self._get_lineage_manager()
        if lm is None:
            return []
        try:
            return lm.descendants(dataset_id)
        except Exception as exc:
            logger.warning("get_descendants failed: %s", exc)
            return []

    def get_root(self, dataset_id: str) -> Optional[str]:
        lm = self._get_lineage_manager()
        if lm is None:
            return None
        try:
            return lm.root(dataset_id)
        except Exception as exc:
            logger.warning("get_root failed: %s", exc)
            return None

    def render_tree(self, dataset_id: str) -> str:
        lm = self._get_lineage_manager()
        if lm is None:
            return f"[Lineage unavailable for {dataset_id}]"
        try:
            return lm.render_tree(dataset_id)
        except Exception as exc:
            logger.warning("render_tree failed: %s", exc)
            return f"[Tree render failed: {exc}]"

    def validate_no_cycle(self, dataset_id: str) -> Dict[str, Any]:
        lm = self._get_lineage_manager()
        if lm is None:
            return {"ok": False, "reason": "LineageManager unavailable"}
        try:
            ok = lm.validate_no_cycle(dataset_id)
            return {"ok": ok, "dataset_id": dataset_id}
        except Exception as exc:
            logger.warning("validate_no_cycle failed: %s", exc)
            return {"ok": False, "reason": str(exc)}
