"""
gui/replay_session_lineage_dialog.py — Session Lineage dialog v1.2.8

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplaySessionLineageDialog:
    """
    Visualizes session lineage tree: root, forks, duplicates, challenges,
    imports, restores. No cycles allowed.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    LINEAGE_TYPES = ["root", "fork", "duplicate", "challenge", "import", "restore"]

    def __init__(self, session_id: Optional[str] = None) -> None:
        self._session_id = session_id

    def _get_lineage_registry(self) -> Optional[Any]:
        try:
            from replay.session_lineage_registry import ReplaySessionLineageRegistry
            return ReplaySessionLineageRegistry()
        except Exception as exc:
            logger.warning("SessionLineageRegistry unavailable: %s", exc)
            return None

    def get_ancestors(self, session_id: str) -> List[str]:
        slr = self._get_lineage_registry()
        if slr is None:
            return []
        try:
            return slr.ancestors(session_id)
        except Exception as exc:
            logger.warning("get_ancestors failed: %s", exc)
            return []

    def get_descendants(self, session_id: str) -> List[str]:
        slr = self._get_lineage_registry()
        if slr is None:
            return []
        try:
            return slr.descendants(session_id)
        except Exception as exc:
            logger.warning("get_descendants failed: %s", exc)
            return []

    def get_root(self, session_id: str) -> Optional[str]:
        slr = self._get_lineage_registry()
        if slr is None:
            return None
        try:
            return slr.root(session_id)
        except Exception as exc:
            logger.warning("get_root failed: %s", exc)
            return None

    def render_tree(self, session_id: str) -> str:
        slr = self._get_lineage_registry()
        if slr is None:
            return f"[Lineage unavailable for {session_id}]"
        try:
            return slr.render_tree(session_id)
        except Exception as exc:
            logger.warning("render_tree failed: %s", exc)
            return f"[Tree render failed: {exc}]"

    def validate_no_cycle(self, session_id: str) -> Dict[str, Any]:
        slr = self._get_lineage_registry()
        if slr is None:
            return {"ok": False, "reason": "LineageRegistry unavailable"}
        try:
            ok = slr.validate_no_cycle(session_id)
            return {"ok": ok, "session_id": session_id}
        except Exception as exc:
            logger.warning("validate_no_cycle failed: %s", exc)
            return {"ok": False, "reason": str(exc)}
