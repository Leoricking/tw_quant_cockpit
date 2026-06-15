"""
gui/replay_decision_journal_adapter.py — ReplayDecisionJournalAdapter v1.2.2

Bridges DecisionJournalManager and ReplayDecisionJournalPanel.
[!] Research Only. No Real Orders.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PyQt5.QtCore import QObject, pyqtSignal
    HAS_QT = True
except ImportError:
    HAS_QT = False


if HAS_QT:
    class ReplayDecisionJournalAdapter(QObject):
        """
        Adapter between DecisionJournalManager and the GUI panel.

        [!] Research Only. No Real Orders. Simulation Decision Only.
        """

        entry_created = pyqtSignal(dict)
        entry_revised = pyqtSignal(dict)
        entry_archived = pyqtSignal(str)
        entries_loaded = pyqtSignal(list)
        error_occurred = pyqtSignal(str)

        def __init__(self, manager=None, parent=None, repo_root: str = ""):
            super().__init__(parent)
            self._manager = manager
            if manager is None:
                try:
                    from replay.decision_journal_manager import DecisionJournalManager
                    self._manager = DecisionJournalManager(repo_root=repo_root)
                except Exception as exc:
                    logger.warning("Could not init manager: %s", exc)

        def create_entry(self, session_id: str, decision_id: str, **kwargs) -> Optional[Dict[str, Any]]:
            """Create a new journal entry and emit signal."""
            try:
                if self._manager:
                    entry = self._manager.create_entry(
                        session_id=session_id,
                        decision_id=decision_id,
                        replay_date=kwargs.get("replay_date", ""),
                        **{k: v for k, v in kwargs.items() if k != "replay_date"},
                    )
                    self.entry_created.emit(entry.to_dict())
                    return entry.to_dict()
            except Exception as exc:
                self.error_occurred.emit(str(exc))
            return None

        def revise_entry(self, entry_id: str, reason: str, field_changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
            """Create a revision and emit signal."""
            try:
                if self._manager:
                    rev = self._manager.revise_entry(entry_id, reason=reason, field_changes=field_changes)
                    if rev:
                        self.entry_revised.emit(rev.to_dict())
                        return rev.to_dict()
            except Exception as exc:
                self.error_occurred.emit(str(exc))
            return None

        def archive_entry(self, entry_id: str) -> bool:
            """Archive entry and emit signal."""
            try:
                if self._manager:
                    result = self._manager.archive_entry(entry_id)
                    if result:
                        self.entry_archived.emit(entry_id)
                        return True
            except Exception as exc:
                self.error_occurred.emit(str(exc))
            return False

        def load_entries(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
            """Load entries and emit signal."""
            try:
                if self._manager:
                    entries = self._manager.list_entries(session_id=session_id)
                    entry_dicts = [e if isinstance(e, dict) else e for e in entries]
                    self.entries_loaded.emit(entry_dicts)
                    return entry_dicts
            except Exception as exc:
                self.error_occurred.emit(str(exc))
            return []

else:
    class ReplayDecisionJournalAdapter:
        """Headless stub."""
        no_real_orders = True

        def __init__(self, *args, **kwargs):
            pass
