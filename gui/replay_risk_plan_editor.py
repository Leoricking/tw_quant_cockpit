"""
gui/replay_risk_plan_editor.py — ReplayRiskPlanEditor v1.2.2
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
        QTextEdit, QLineEdit, QDoubleSpinBox,
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False

if HAS_QT:
    class ReplayRiskPlanEditor(QWidget):
        """Risk plan editor widget. [!] Simulation Only."""
        def __init__(self, parent=None, risk_plan: Optional[Dict[str, Any]] = None):
            super().__init__(parent)
            self._risk_plan = risk_plan or {}
            self._build_ui()

        def _build_ui(self):
            layout = QVBoxLayout(self)

            row1 = QHBoxLayout()
            row1.addWidget(QLabel("Stop Type:"))
            self._stop_type = QComboBox()
            self._stop_type.addItems([
                "NONE", "HARD_STOP", "CLOSE_CONFIRM", "SUPPORT_BREAK",
                "MA_BREAK", "TIME_STOP", "VOLATILITY_STOP", "MANUAL_REVIEW",
            ])
            row1.addWidget(self._stop_type)
            layout.addLayout(row1)

            layout.addWidget(QLabel("Stop Price Note:"))
            self._stop_note = QLineEdit()
            layout.addWidget(self._stop_note)

            row2 = QHBoxLayout()
            row2.addWidget(QLabel("Target Type:"))
            self._target_type = QComboBox()
            self._target_type.addItems([
                "NONE", "FIXED_PRICE", "RESISTANCE", "TRAILING",
                "SCALE_OUT", "TIME_BASED", "MANUAL_REVIEW",
            ])
            row2.addWidget(self._target_type)
            layout.addLayout(row2)

            layout.addWidget(QLabel("Target Price Note:"))
            self._target_note = QLineEdit()
            layout.addWidget(self._target_note)

            layout.addWidget(QLabel("Max Risk Note:"))
            self._max_risk_note = QLineEdit()
            layout.addWidget(self._max_risk_note)

            layout.addWidget(QLabel("Position Sizing Note:"))
            self._position_note = QLineEdit()
            layout.addWidget(self._position_note)

            layout.addWidget(QLabel("Notes:"))
            self._notes = QTextEdit()
            self._notes.setMaximumHeight(60)
            layout.addWidget(self._notes)

        def get_data(self) -> Dict[str, Any]:
            return {
                "stop_type": self._stop_type.currentText(),
                "stop_price_note": self._stop_note.text(),
                "target_type": self._target_type.currentText(),
                "target_price_note": self._target_note.text(),
                "max_risk_note": self._max_risk_note.text(),
                "position_sizing_note": self._position_note.text(),
                "notes": self._notes.toPlainText(),
                "simulation_only": True,
            }
else:
    class ReplayRiskPlanEditor:
        no_real_orders = True
        def __init__(self, *args, **kwargs): pass
