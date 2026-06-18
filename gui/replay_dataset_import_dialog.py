"""
gui/replay_dataset_import_dialog.py — Dataset Import dialog v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] Import requires explicit preview + execute + allow-write.
[!] AUTO_PACKAGE_IMPORT_ENABLED = False
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_PACKAGE_IMPORT_ENABLED = False


class ReplayDatasetImportDialog:
    """
    Preview and execute dataset package import.
    execute() blocked without allow_write=True.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] Auto import is disabled.
    """

    RESEARCH_ONLY            = True
    NO_REAL_ORDERS           = True
    AUTO_PACKAGE_IMPORT_ENABLED = False

    def __init__(self) -> None:
        self._last_preview: Optional[Dict[str, Any]] = None

    def preview(self, package_path: str) -> Dict[str, Any]:
        try:
            from replay.dataset_importer import ReplayDatasetImporter
            result = ReplayDatasetImporter().preview(package_path)
            self._last_preview = result
            return result
        except Exception as exc:
            logger.warning("import preview failed: %s", exc)
            return {"blocked": True, "reason": str(exc)}

    def execute(self, package_path: str) -> Dict[str, Any]:
        """Always show blocked message — execute requires allow_write=True at CLI level."""
        return {
            "blocked": True,
            "reason":  "Import must be executed via CLI with --execute --allow-write",
            "package_path": package_path,
            "research_only": True,
        }

    def get_last_preview(self) -> Optional[Dict[str, Any]]:
        return self._last_preview
