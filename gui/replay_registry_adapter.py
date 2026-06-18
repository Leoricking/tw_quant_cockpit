"""
gui/replay_registry_adapter.py — Replay Registry GUI adapter v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayRegistryGUIAdapter:
    """
    Lazy-loads registry backend objects for GUI panels.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self) -> None:
        self._dataset_registry: Optional[Any] = None
        self._session_registry: Optional[Any] = None
        self._health: Optional[Any] = None
        self._repair: Optional[Any] = None
        self._audit: Optional[Any] = None

    # ------------------------------------------------------------------ #
    # Dataset Registry

    def get_dataset_registry(self) -> Optional[Any]:
        if self._dataset_registry is None:
            try:
                from replay.dataset_registry import ReplayDatasetRegistry
                self._dataset_registry = ReplayDatasetRegistry()
            except Exception as exc:
                logger.warning("DatasetRegistry unavailable: %s", exc)
        return self._dataset_registry

    def list_datasets(self) -> List[Dict[str, Any]]:
        reg = self.get_dataset_registry()
        if reg is None:
            return []
        try:
            return [vars(d) if hasattr(d, "__dict__") else d
                    for d in reg.list_datasets()]
        except Exception as exc:
            logger.warning("list_datasets failed: %s", exc)
            return []

    def get_dataset(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        reg = self.get_dataset_registry()
        if reg is None:
            return None
        try:
            d = reg.get_dataset(dataset_id)
            return vars(d) if d and hasattr(d, "__dict__") else d
        except Exception as exc:
            logger.warning("get_dataset failed: %s", exc)
            return None

    def dataset_summary(self) -> Dict[str, Any]:
        try:
            from replay.dataset_summary import ReplayDatasetSummary
            return ReplayDatasetSummary().full_summary(self.get_dataset_registry())
        except Exception as exc:
            logger.warning("dataset_summary failed: %s", exc)
            return {"status": "UNAVAILABLE", "research_only": True}

    # ------------------------------------------------------------------ #
    # Session Registry

    def get_session_registry(self) -> Optional[Any]:
        if self._session_registry is None:
            try:
                from replay.session_registry_v128 import ReplaySessionRegistryV128
                self._session_registry = ReplaySessionRegistryV128()
            except Exception as exc:
                logger.warning("SessionRegistry unavailable: %s", exc)
        return self._session_registry

    def list_sessions(self) -> List[Dict[str, Any]]:
        reg = self.get_session_registry()
        if reg is None:
            return []
        try:
            return [vars(s) if hasattr(s, "__dict__") else s
                    for s in reg.list()]
        except Exception as exc:
            logger.warning("list_sessions failed: %s", exc)
            return []

    def session_summary(self) -> Dict[str, Any]:
        try:
            from replay.session_registry_summary import ReplaySessionRegistrySummary
            return ReplaySessionRegistrySummary().full_summary(self.get_session_registry())
        except Exception as exc:
            logger.warning("session_summary failed: %s", exc)
            return {"status": "UNAVAILABLE", "research_only": True}

    # ------------------------------------------------------------------ #
    # Health

    def registry_health(self) -> Dict[str, Any]:
        try:
            from replay.registry_health import ReplayRegistryHealthCheck
            hc = ReplayRegistryHealthCheck()
            results = hc.run()
            passed  = sum(1 for v in results.values() if v[0] == "PASS")
            failed  = sum(1 for v in results.values() if v[0] == "FAIL")
            warned  = sum(1 for v in results.values() if v[0] == "WARN")
            blocked = sum(1 for v in results.values() if v[0] == "BLOCKED")
            return {
                "results": results,
                "passed": passed,
                "failed": failed,
                "warned": warned,
                "blocked": blocked,
                "ok": failed == 0 and blocked == 0,
            }
        except Exception as exc:
            logger.warning("registry_health failed: %s", exc)
            return {"status": "UNAVAILABLE", "ok": False}

    # ------------------------------------------------------------------ #
    # Repair

    def repair_preview(self) -> Dict[str, Any]:
        try:
            from replay.registry_repair import ReplayRegistryRepairPlanner
            planner = ReplayRegistryRepairPlanner()
            return planner.preview(
                dataset_registry=self.get_dataset_registry(),
                session_registry=self.get_session_registry(),
            )
        except Exception as exc:
            logger.warning("repair_preview failed: %s", exc)
            return {"status": "UNAVAILABLE"}

    # ------------------------------------------------------------------ #
    # Audit

    def audit_events(self, **kwargs) -> List[Dict[str, Any]]:
        try:
            from replay.registry_events import ReplayRegistryEvents
            return ReplayRegistryEvents().list_events(**kwargs)
        except Exception as exc:
            logger.warning("audit_events failed: %s", exc)
            return []
