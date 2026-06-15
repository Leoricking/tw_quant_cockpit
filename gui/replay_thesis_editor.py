"""
gui/replay_thesis_editor.py — ReplayThesisEditor v1.2.2
[!] Research Only. No Real Orders. Simulation Decision Only.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True

try:
    from PyQt5.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
        QTextEdit, QLineEdit, QGroupBox,
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False

if HAS_QT:
    class ReplayThesisEditor(QWidget):
        """Trade thesis editor widget. [!] Simulation Only."""
        def __init__(self, parent=None, thesis: Optional[Dict[str, Any]] = None):
            super().__init__(parent)
            self._thesis = thesis or {}
            self._build_ui()

        def _build_ui(self):
            layout = QVBoxLayout(self)
            row = QHBoxLayout()
            row.addWidget(QLabel("Setup Type:"))
            self._setup_combo = QComboBox()
            self._setup_combo.addItems([
                "FREE_FORM", "BREAKOUT", "PULLBACK", "BOTTOM_REVERSAL",
                "TREND_FOLLOWING", "MOMENTUM", "SECTOR_ROTATION",
                "FUNDAMENTAL_TURNAROUND", "RISK_REDUCTION",
                "NO_CHASE", "NO_PANIC_SELL", "OTHER",
            ])
            row.addWidget(self._setup_combo)
            row.addWidget(QLabel("Time Horizon:"))
            self._horizon_combo = QComboBox()
            self._horizon_combo.addItems(["UNDEFINED", "INTRADAY", "SHORT", "SWING", "MID", "LONG"])
            row.addWidget(self._horizon_combo)
            layout.addLayout(row)

            layout.addWidget(QLabel("Summary:"))
            self._summary = QTextEdit()
            self._summary.setMaximumHeight(80)
            layout.addWidget(self._summary)

            layout.addWidget(QLabel("Key Triggers (one per line):"))
            self._triggers = QTextEdit()
            self._triggers.setMaximumHeight(60)
            layout.addWidget(self._triggers)

            layout.addWidget(QLabel("Invalidation Conditions (one per line):"))
            self._invalidation = QTextEdit()
            self._invalidation.setMaximumHeight(60)
            layout.addWidget(self._invalidation)

            layout.addWidget(QLabel("Notes:"))
            self._notes = QTextEdit()
            self._notes.setMaximumHeight(60)
            layout.addWidget(self._notes)

        def get_data(self) -> Dict[str, Any]:
            return {
                "setup_type": self._setup_combo.currentText(),
                "time_horizon": self._horizon_combo.currentText(),
                "summary": self._summary.toPlainText(),
                "key_triggers": [t.strip() for t in self._triggers.toPlainText().splitlines() if t.strip()],
                "invalidation_conditions": [t.strip() for t in self._invalidation.toPlainText().splitlines() if t.strip()],
                "notes": self._notes.toPlainText(),
                "simulation_only": True,
            }
else:
    class ReplayThesisEditor:
        no_real_orders = True
        def __init__(self, *args, **kwargs): pass
