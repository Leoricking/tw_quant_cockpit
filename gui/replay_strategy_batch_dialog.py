"""
gui/replay_strategy_batch_dialog.py — Batch processing dialog v1.2.4.
[!] Research Only. No Real Orders. Requires --allow-write to execute.
"""
from __future__ import annotations
import logging
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStrategyBatchDialog:
    """Batch processing dialog with timing display. Research Only."""
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, sessions=None, parent=None):
        self.sessions = sessions or []
        try:
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QProgressBar
            self._dialog = QDialog(parent)
            self._dialog.setWindowTitle("Strategy Replay Batch")
            layout = QVBoxLayout(self._dialog)
            layout.addWidget(QLabel(f"Sessions: {len(self.sessions)}"))
            layout.addWidget(QLabel("Elapsed Time  : 00:00:00"))
            layout.addWidget(QLabel("Items         : 0"))
            layout.addWidget(QLabel("Completed     : 0"))
            layout.addWidget(QLabel("Failed        : 0"))
            layout.addWidget(QLabel("Status        : READY"))
            layout.addWidget(QLabel("[!] Requires --allow-write to execute."))
            layout.addWidget(QLabel("[!] Research Only. Not Investment Advice."))
            bb = QDialogButtonBox(QDialogButtonBox.Close)
            bb.rejected.connect(self._dialog.reject)
            layout.addWidget(bb)
        except Exception as exc:
            logger.warning("Qt unavailable: %s", exc)

    def exec(self):
        if hasattr(self, "_dialog"):
            return self._dialog.exec()
