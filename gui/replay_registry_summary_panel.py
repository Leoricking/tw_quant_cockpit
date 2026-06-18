"""
gui/replay_registry_summary_panel.py — Registry Summary panel v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayRegistrySummaryPanel:
    """
    Displays combined dataset + session registry summary statistics and health.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self) -> None:
        self._adapter: Optional[Any] = None

    def _get_adapter(self) -> Optional[Any]:
        if self._adapter is None:
            try:
                from gui.replay_registry_adapter import ReplayRegistryGUIAdapter
                self._adapter = ReplayRegistryGUIAdapter()
            except Exception as exc:
                logger.warning("Adapter unavailable: %s", exc)
        return self._adapter

    def get_dataset_summary(self) -> Dict[str, Any]:
        adapter = self._get_adapter()
        if adapter is None:
            return {"status": "UNAVAILABLE"}
        return adapter.dataset_summary()

    def get_session_summary(self) -> Dict[str, Any]:
        adapter = self._get_adapter()
        if adapter is None:
            return {"status": "UNAVAILABLE"}
        return adapter.session_summary()

    def get_health_summary(self) -> Dict[str, Any]:
        adapter = self._get_adapter()
        if adapter is None:
            return {"ok": False, "status": "UNAVAILABLE"}
        return adapter.registry_health()

    def get_repair_summary(self) -> Dict[str, Any]:
        adapter = self._get_adapter()
        if adapter is None:
            return {"issues_found": 0, "status": "UNAVAILABLE"}
        preview = adapter.repair_preview()
        return {
            "issues_found":  preview.get("issues_found", 0),
            "blocked_count": preview.get("blocked_count", 0),
            "safe_count":    preview.get("safe_count", 0),
        }

    def full_summary(self) -> Dict[str, Any]:
        return {
            "datasets":      self.get_dataset_summary(),
            "sessions":      self.get_session_summary(),
            "health":        self.get_health_summary(),
            "repair":        self.get_repair_summary(),
            "research_only": True,
            "no_real_orders": True,
            "version":       "1.2.8",
        }
