"""
gui/replay_strategy_rule_review_dialog.py — Rule review dialog v1.2.4.
[!] Research Only. No Real Orders. All reviews start as SUGGESTED.
"""
from __future__ import annotations
import logging
logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True
RESEARCH_ONLY = True


class ReplayStrategyRuleReviewDialog:
    """Dialog for rule review. Confirm/Dismiss/Override/Reopen/Add Note. Research Only."""
    RESEARCH_ONLY = True
    NO_REAL_ORDERS = True

    def __init__(self, review_data=None, parent=None):
        self.review_data = review_data or {}
        try:
            from PySide6.QtWidgets import (
                QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QPushButton, QHBoxLayout
            )
            self._dialog = QDialog(parent)
            self._dialog.setWindowTitle("Strategy Rule Review")
            layout = QVBoxLayout(self._dialog)
            layout.addWidget(QLabel(f"Review ID: {self.review_data.get('review_id', '')}"))
            layout.addWidget(QLabel(f"Module: {self.review_data.get('module_name', '')}"))
            layout.addWidget(QLabel(f"Status: {self.review_data.get('status', 'SUGGESTED')}"))
            layout.addWidget(QLabel("[!] All reviews start as SUGGESTED. System cannot auto-confirm."))
            layout.addWidget(QLabel("[!] Research Only. Not Investment Advice."))
            btn_row = QHBoxLayout()
            for label in ["Confirm", "Dismiss", "Override", "Reopen", "Add Note"]:
                btn = QPushButton(label)
                btn_row.addWidget(btn)
            layout.addLayout(btn_row)
            bb = QDialogButtonBox(QDialogButtonBox.Close)
            bb.rejected.connect(self._dialog.reject)
            layout.addWidget(bb)
        except Exception as exc:
            logger.warning("Qt unavailable: %s", exc)

    def exec(self):
        if hasattr(self, "_dialog"):
            return self._dialog.exec()
