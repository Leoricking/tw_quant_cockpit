"""
gui/replay_registry_panel.py — Replay Registry main panel v1.2.8

Safety Banner: Dataset Registry Only. No Broker. No Real Orders. Research Only.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] No forbidden buttons: No Send Order / Real Buy / Real Sell / Broker Login /
    Auto Overwrite / Auto Repair / Auto Rebind / Auto Import / Auto Export.
[!] All write actions require explicit preview + execute + allow-write.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

SAFETY_BANNER_LINES = [
    "[!] Research Only",
    "[!] No Real Orders",
    "[!] Dataset Registry Only",
    "[!] No Broker",
    "[!] All writes require preview + execute + allow-write",
]

FORBIDDEN_BUTTONS = [
    "Send Order", "Real Buy", "Real Sell", "Broker Login",
    "Auto Overwrite", "Auto Repair", "Auto Rebind",
    "Auto Import", "Auto Export",
]


class ReplayRegistryPanel:
    """
    Main panel for the Replay Dataset & Session Registry (v1.2.8).

    Tabs:
      - Dataset Catalog
      - Session Registry
      - Registry Health
      - Repair
      - Audit Log

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] No forbidden buttons.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True
    HAS_FORBIDDEN_BUTTONS = False

    def __init__(self) -> None:
        self._adapter: Optional[Any] = None
        self._initialized = False

    def _get_adapter(self) -> Any:
        if self._adapter is None:
            try:
                from gui.replay_registry_adapter import ReplayRegistryGUIAdapter
                self._adapter = ReplayRegistryGUIAdapter()
            except Exception as exc:
                logger.warning("ReplayRegistryGUIAdapter unavailable: %s", exc)
        return self._adapter

    def get_safety_banner(self) -> str:
        return " | ".join(SAFETY_BANNER_LINES)

    def get_tab_info(self) -> Dict[str, Any]:
        return {
            "tab_id":       "replay_registry",
            "tab_label":    "Replay Registry",
            "version":      "1.2.8",
            "research_only": True,
            "no_real_orders": True,
        }

    def get_dataset_rows(self) -> List[Dict[str, Any]]:
        adapter = self._get_adapter()
        if adapter is None:
            return []
        return adapter.list_datasets()

    def get_session_rows(self) -> List[Dict[str, Any]]:
        adapter = self._get_adapter()
        if adapter is None:
            return []
        return adapter.list_sessions()

    def get_health_summary(self) -> Dict[str, Any]:
        adapter = self._get_adapter()
        if adapter is None:
            return {"ok": False, "status": "UNAVAILABLE"}
        return adapter.registry_health()

    def get_repair_preview(self) -> Dict[str, Any]:
        adapter = self._get_adapter()
        if adapter is None:
            return {"action": "REPAIR_PREVIEW", "issues_found": 0, "plan": []}
        return adapter.repair_preview()

    def get_audit_events(self, **kwargs) -> List[Dict[str, Any]]:
        adapter = self._get_adapter()
        if adapter is None:
            return []
        return adapter.audit_events(**kwargs)

    def get_dataset_summary(self) -> Dict[str, Any]:
        adapter = self._get_adapter()
        if adapter is None:
            return {"status": "UNAVAILABLE", "research_only": True}
        return adapter.dataset_summary()

    def get_session_summary(self) -> Dict[str, Any]:
        adapter = self._get_adapter()
        if adapter is None:
            return {"status": "UNAVAILABLE", "research_only": True}
        return adapter.session_summary()

    def summary(self) -> Dict[str, Any]:
        health = self.get_health_summary()
        return {
            "tab_id":        "replay_registry",
            "version":       "1.2.8",
            "health_ok":     health.get("ok", False),
            "research_only": True,
            "no_real_orders": True,
        }
