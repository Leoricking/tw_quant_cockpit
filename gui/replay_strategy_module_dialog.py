"""
gui/replay_strategy_module_dialog.py — Module detail dialog v1.2.4.
[!] Research Only. No Real Orders.
"""
from __future__ import annotations
import logging
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStrategyModuleDialog:
    """Dialog showing full module detail. Research Only."""
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, module_data=None, parent=None):
        self.module_data = module_data or {}
        try:
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
            self._dialog = QDialog(parent)
            self._dialog.setWindowTitle(f"Module: {self.module_data.get('module_name', 'Unknown')}")
            layout = QVBoxLayout(self._dialog)
            layout.addWidget(QLabel(f"Signal: {self.module_data.get('signal', '')}"))
            layout.addWidget(QLabel(f"Score: {self.module_data.get('score', '')}"))
            layout.addWidget(QLabel(f"Warning: {self.module_data.get('warning', '')}"))
            layout.addWidget(QLabel("[!] Research Only. Not Investment Advice."))
            bb = QDialogButtonBox(QDialogButtonBox.Ok)
            bb.accepted.connect(self._dialog.accept)
            layout.addWidget(bb)
        except Exception as exc:
            logger.warning("Qt unavailable: %s", exc)

    def exec(self):
        if hasattr(self, "_dialog"):
            return self._dialog.exec()
