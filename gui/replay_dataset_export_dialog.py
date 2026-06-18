"""
gui/replay_dataset_export_dialog.py — Dataset Export dialog v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] Export requires explicit preview + execute + allow-write.
[!] Packages must never contain secrets or absolute paths.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayDatasetExportDialog:
    """
    Preview and execute dataset package export.
    execute() blocked without allow_write=True.
    Does not auto-overwrite existing packages.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] RELATIVE_ONLY path mode enforced. No secrets.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self) -> None:
        self._last_preview: Optional[Dict[str, Any]] = None

    def preview(self, dataset_id: str, output_path: str = "") -> Dict[str, Any]:
        try:
            from replay.dataset_exporter import ReplayDatasetExporter
            result = ReplayDatasetExporter().preview(dataset_id, output_path=output_path)
            self._last_preview = result
            return result
        except Exception as exc:
            logger.warning("export preview failed: %s", exc)
            return {"blocked": True, "reason": str(exc)}

    def execute(self, dataset_id: str, output_path: str = "") -> Dict[str, Any]:
        """Always show blocked message — execute requires allow_write=True at CLI level."""
        return {
            "blocked":    True,
            "reason":     "Export must be executed via CLI with --execute --allow-write",
            "dataset_id": dataset_id,
            "research_only": True,
        }

    def get_last_preview(self) -> Optional[Dict[str, Any]]:
        return self._last_preview
