"""
gui/replay_session_manager_adapter.py — ReplaySessionManagerAdapter v1.2.1

Adapter connecting the session manager panel to the backend.

[!] Research Only. No Real Orders. Replay Training Only.
[!] No Auto Play All, No Auto Decision, No Auto Score, No Buy/Sell Order, No Broker Login.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

RESEARCH_ONLY = True
NO_REAL_ORDERS = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReplaySessionManagerAdapter:
    """
    Adapter for session manager GUI panel.
    [!] Research Only. No Real Orders.
    """

    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, repo_root: Optional[str] = None):
        self._repo_root = repo_root or BASE_DIR
        self._mgr = None
        self._cp_mgr = None
        self._comparator = None
        self._portability = None
        self._initialized = False

    def _ensure_init(self):
        if self._initialized:
            return
        try:
            from replay.session_manager import ReplaySessionManager
            from replay.session_checkpoint import ReplayCheckpointManager
            from replay.session_comparator import ReplaySessionComparator
            from replay.session_portability import ReplaySessionPortability
            from replay.replay_session_store import ReplaySessionStore
            store = ReplaySessionStore(repo_root=self._repo_root)
            self._mgr = ReplaySessionManager(store=store, repo_root=self._repo_root)
            self._cp_mgr = ReplayCheckpointManager(store=store, repo_root=self._repo_root)
            self._comparator = ReplaySessionComparator(store=store, repo_root=self._repo_root)
            self._portability = ReplaySessionPortability(store=store, repo_root=self._repo_root)
            self._initialized = True
        except Exception as exc:
            logger.warning("[SessionManagerAdapter] Init failed: %s", exc)

    def list_sessions(self, include_hidden: bool = False, include_archived: bool = False) -> List[Dict]:
        self._ensure_init()
        if self._mgr:
            return self._mgr.list_sessions(include_hidden=include_hidden, include_archived=include_archived)
        return []

    def get_session(self, session_id: str) -> Optional[Dict]:
        self._ensure_init()
        if self._mgr:
            return self._mgr.get_session(session_id)
        return None

    def search_sessions(self, query: str) -> List[Dict]:
        self._ensure_init()
        if self._mgr:
            return self._mgr.search_sessions(query)
        return []

    def filter_sessions(self, **kwargs) -> List[Dict]:
        self._ensure_init()
        if self._mgr:
            return self._mgr.filter_sessions(**kwargs)
        return []

    def session_summary(self, session_id: str) -> Dict:
        self._ensure_init()
        if self._mgr:
            return self._mgr.session_summary(session_id)
        return {}

    def create_checkpoint(self, session_id: str, note: str = "") -> Optional[Dict]:
        self._ensure_init()
        if self._cp_mgr:
            cp = self._cp_mgr.create_checkpoint(session_id, note=note)
            return cp.to_dict() if cp else None
        return None

    def list_checkpoints(self, session_id: str) -> List[Dict]:
        self._ensure_init()
        if self._cp_mgr:
            return self._cp_mgr.list_checkpoints(session_id)
        return []

    def restore_checkpoint(self, checkpoint_id: str) -> Optional[Dict]:
        self._ensure_init()
        if self._cp_mgr:
            return self._cp_mgr.restore_checkpoint(checkpoint_id)
        return None

    def fork_session(self, session_id: str, checkpoint_id: Optional[str] = None, new_name: Optional[str] = None) -> Optional[Dict]:
        self._ensure_init()
        if self._mgr:
            state = self._mgr.fork_session(session_id, checkpoint_id=checkpoint_id, new_name=new_name)
            return {"session_id": state.session_id} if state else None
        return None

    def duplicate_session(self, session_id: str, new_name: Optional[str] = None) -> Optional[Dict]:
        self._ensure_init()
        if self._mgr:
            state = self._mgr.duplicate_session(session_id, new_name=new_name)
            return {"session_id": state.session_id} if state else None
        return None

    def archive_session(self, session_id: str) -> bool:
        self._ensure_init()
        if self._mgr:
            return self._mgr.archive_session(session_id) is not None
        return False

    def restore_session(self, session_id: str) -> bool:
        self._ensure_init()
        if self._mgr:
            return self._mgr.restore_session(session_id) is not None
        return False

    def hide_session(self, session_id: str) -> bool:
        self._ensure_init()
        if self._mgr:
            return self._mgr.delete_from_view(session_id)
        return False

    def compare_sessions(self, session_a: str, session_b: str) -> Optional[Dict]:
        self._ensure_init()
        if self._comparator:
            return self._comparator.compare(session_a, session_b)
        return None

    def export_session(self, session_id: str, output_path: Optional[str] = None) -> Optional[str]:
        self._ensure_init()
        if self._portability:
            return self._portability.export_metadata(session_id, output_path)
        return None

    def import_session(self, path: str, dry_run: bool = True) -> Dict:
        self._ensure_init()
        if self._portability:
            return self._portability.import_metadata(path, dry_run=dry_run)
        return {"ok": False, "error": "portability not available"}

    def generate_report(self) -> Dict:
        self._ensure_init()
        try:
            from reports.replay_session_manager_report import ReplaySessionManagerReportBuilder
            builder = ReplaySessionManagerReportBuilder(repo_root=self._repo_root)
            content = builder.build(session_manager=self._mgr)
            fpath = builder.save(content)
            return {"ok": True, "path": fpath}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
