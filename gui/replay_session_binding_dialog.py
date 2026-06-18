"""
gui/replay_session_binding_dialog.py — Session Binding dialog v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
[!] Session-Dataset binding locked after session creation.
[!] COMPLETED sessions cannot be directly rebound.
[!] AUTO_SESSION_REBIND_ENABLED = False
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
AUTO_SESSION_REBIND_ENABLED = False


class ReplaySessionBindingDialog:
    """
    Preview and execute session-dataset binding and rebinding.
    execute() blocked without allow_write=True.
    COMPLETED sessions cannot be directly rebound.

    [!] Research Only. No Real Orders. Not Investment Advice.
    [!] Binding locked after session creation.
    """

    RESEARCH_ONLY           = True
    NO_REAL_ORDERS          = True
    AUTO_SESSION_REBIND_ENABLED = False

    def bind_preview(self, session_id: str, dataset_id: str,
                     dataset_version: str = "") -> Dict[str, Any]:
        try:
            from replay.session_dataset_binding import ReplaySessionDatasetBinder
            binder = ReplaySessionDatasetBinder()
            return binder.bind_preview(session_id, dataset_id,
                                       dataset_version=dataset_version)
        except Exception as exc:
            logger.warning("bind_preview failed: %s", exc)
            return {"blocked": True, "reason": str(exc)}

    def bind_execute(self, session_id: str, dataset_id: str,
                     dataset_version: str = "") -> Dict[str, Any]:
        """GUI always shows blocked — execute requires allow_write=True at CLI level."""
        return {
            "blocked":    True,
            "reason":     "Binding must be executed via CLI with --execute --allow-write",
            "session_id": session_id,
            "dataset_id": dataset_id,
            "research_only": True,
        }

    def rebind_preview(self, session_id: str, new_dataset_id: str,
                       new_dataset_version: str = "") -> Dict[str, Any]:
        try:
            from replay.session_dataset_binding import ReplaySessionDatasetBinder
            binder = ReplaySessionDatasetBinder()
            return binder.rebind_preview(session_id, new_dataset_id,
                                         new_dataset_version=new_dataset_version)
        except Exception as exc:
            logger.warning("rebind_preview failed: %s", exc)
            return {"blocked": True, "reason": str(exc)}

    def rebind_execute(self, session_id: str, new_dataset_id: str,
                       new_dataset_version: str = "") -> Dict[str, Any]:
        """GUI always shows blocked — execute requires allow_write=True at CLI level."""
        return {
            "blocked":        True,
            "reason":         "Rebind must be executed via CLI with --execute --allow-write",
            "session_id":     session_id,
            "new_dataset_id": new_dataset_id,
            "research_only":  True,
        }
