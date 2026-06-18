"""
gui/replay_session_registry_detail_dialog.py — Session Registry Detail dialog v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplaySessionRegistryDetailDialog:
    """
    Displays full session detail: binding, fingerprint, lineage, status history.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, session_id: Optional[str] = None) -> None:
        self._session_id = session_id

    def _get_registry(self) -> Optional[Any]:
        try:
            from replay.session_registry_v128 import ReplaySessionRegistryV128
            return ReplaySessionRegistryV128()
        except Exception as exc:
            logger.warning("SessionRegistry unavailable: %s", exc)
            return None

    def load(self, session_id: str) -> Dict[str, Any]:
        self._session_id = session_id
        reg = self._get_registry()
        if reg is None:
            return {"error": "Registry unavailable", "session_id": session_id}
        try:
            s = reg.get(session_id)
            return vars(s) if s and hasattr(s, "__dict__") else (s or {})
        except Exception as exc:
            logger.warning("load failed: %s", exc)
            return {"error": str(exc), "session_id": session_id}

    def get_bindings(self, session_id: str) -> List[Dict[str, Any]]:
        try:
            from replay.session_dataset_binding import ReplaySessionDatasetBinder
            binder = ReplaySessionDatasetBinder()
            return binder.list_bindings(session_id)
        except Exception as exc:
            logger.warning("get_bindings failed: %s", exc)
            return []

    def get_lineage(self, session_id: str) -> Dict[str, Any]:
        try:
            from replay.session_lineage_registry import ReplaySessionLineageRegistry
            slr = ReplaySessionLineageRegistry()
            return {
                "ancestors":   slr.ancestors(session_id),
                "descendants": slr.descendants(session_id),
                "root":        slr.root(session_id),
            }
        except Exception as exc:
            logger.warning("get_lineage failed: %s", exc)
            return {}

    def verify(self, session_id: str) -> Dict[str, Any]:
        reg = self._get_registry()
        if reg is None:
            return {"ok": False, "reason": "Registry unavailable"}
        try:
            return reg.verify_session(session_id)
        except Exception as exc:
            logger.warning("verify failed: %s", exc)
            return {"ok": False, "reason": str(exc)}

    def get_tab_sections(self) -> List[str]:
        return ["Overview", "Binding", "Fingerprint", "Lineage", "Verification"]
