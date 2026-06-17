"""
gui/replay_strategy_timeline_dialog.py — Timeline dialog v1.2.4.
[!] Research Only. No Real Orders.
"""
from __future__ import annotations
import logging
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStrategyTimelineDialog:
    """Dialog showing signal timeline. Research Only."""
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, timeline_data=None, parent=None):
        self.timeline_data = timeline_data or []
        try:
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
            self._dialog = QDialog(parent)
            self._dialog.setWindowTitle("Strategy Signal Timeline")
            layout = QVBoxLayout(self._dialog)
            layout.addWidget(QLabel(f"Timeline records: {len(self.timeline_data)}"))
            layout.addWidget(QLabel("[!] Research Only. Not Investment Advice."))
            bb = QDialogButtonBox(QDialogButtonBox.Ok)
            bb.accepted.connect(self._dialog.accept)
            layout.addWidget(bb)
        except Exception as exc:
            logger.warning("Qt unavailable: %s", exc)

    def exec(self):
        if hasattr(self, "_dialog"):
            return self._dialog.exec()
