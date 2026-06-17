"""
gui/replay_strategy_conflict_dialog.py — Conflict detail dialog v1.2.4.
[!] Research Only. No Real Orders. Conflicts never auto-block decisions.
"""
from __future__ import annotations
import logging
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True
CONFLICT_NEVER_AUTO_BLOCKS_DECISION = True


class ReplayStrategyConflictDialog:
    """Dialog showing conflict details. Informational only. Research Only."""
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, conflicts=None, parent=None):
        self.conflicts = conflicts or []
        try:
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
            self._dialog = QDialog(parent)
            self._dialog.setWindowTitle("Strategy Conflicts (Informational Only)")
            layout = QVBoxLayout(self._dialog)
            layout.addWidget(QLabel(f"Conflicts detected: {len(self.conflicts)}"))
            layout.addWidget(QLabel("[!] Conflicts are informational only. Never auto-block decisions."))
            layout.addWidget(QLabel("[!] Research Only. Not Investment Advice."))
            bb = QDialogButtonBox(QDialogButtonBox.Ok)
            bb.accepted.connect(self._dialog.accept)
            layout.addWidget(bb)
        except Exception as exc:
            logger.warning("Qt unavailable: %s", exc)

    def exec(self):
        if hasattr(self, "_dialog"):
            return self._dialog.exec()
