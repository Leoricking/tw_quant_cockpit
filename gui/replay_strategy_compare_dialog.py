"""
gui/replay_strategy_compare_dialog.py — Comparison dialog v1.2.4.
[!] Research Only. No Real Orders. No forward return before outcome reveal.
"""
from __future__ import annotations
import logging
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStrategyCompareDialog:
    """Dialog for date/session comparison. Research Only."""
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, comparison_data=None, parent=None):
        self.comparison_data = comparison_data or {}
        try:
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
            self._dialog = QDialog(parent)
            self._dialog.setWindowTitle("Strategy Snapshot Comparison")
            layout = QVBoxLayout(self._dialog)
            layout.addWidget(QLabel(f"Date A: {self.comparison_data.get('date_a', '')}"))
            layout.addWidget(QLabel(f"Date B: {self.comparison_data.get('date_b', '')}"))
            changes = self.comparison_data.get("module_changes", [])
            layout.addWidget(QLabel(f"Module changes: {len(changes)}"))
            layout.addWidget(QLabel("[!] No forward return before outcome reveal."))
            layout.addWidget(QLabel("[!] Research Only. Not Investment Advice."))
            bb = QDialogButtonBox(QDialogButtonBox.Ok)
            bb.accepted.connect(self._dialog.accept)
            layout.addWidget(bb)
        except Exception as exc:
            logger.warning("Qt unavailable: %s", exc)

    def exec(self):
        if hasattr(self, "_dialog"):
            return self._dialog.exec()
