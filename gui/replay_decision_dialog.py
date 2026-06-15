"""
gui/replay_decision_dialog.py — ReplayDecisionDialog v1.2.0

Dialog for recording a replay training decision.
Action buttons, price, position %, stop, target, confidence, reasons, notes.
Prominently shows SIMULATION DECISION ONLY warning.

[!] Research Only. No Real Orders. Replay Training Only.
[!] SIMULATION DECISION ONLY — NO ORDER WILL BE SENT.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QLineEdit, QComboBox, QFormLayout, QFrame, QSpinBox,
        QDialogButtonBox, QTextEdit, QGroupBox, QDoubleSpinBox,
    )
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False


VALID_ACTIONS = ["WATCH", "WAIT", "ENTER", "ADD", "HOLD", "REDUCE", "EXIT", "STOP", "SKIP"]


if not _PYSIDE6_OK:
    class ReplayDecisionDialog:
        """Stub when PySide6 unavailable."""
        def __init__(self, *args, **kwargs):
            logger.warning("[ReplayDecisionDialog] PySide6 not available — stub mode")

        def get_values(self):
            return None
else:
    class ReplayDecisionDialog(QDialog):
        """
        Dialog for recording a replay training decision.
        [!] SIMULATION DECISION ONLY — NO ORDER WILL BE SENT.
        [!] Research Only. No Real Orders. Replay Training Only.
        """

        NO_REAL_ORDERS = True
        RESEARCH_ONLY = True
        SIMULATION_DECISION_ONLY = True

        def __init__(self, parent=None, replay_date: str = "", symbol: str = ""):
            super().__init__(parent)
            self.setWindowTitle("Record Replay Decision — SIMULATION ONLY")
            self.setMinimumWidth(520)
            self._replay_date = replay_date
            self._symbol = symbol
            self._setup_ui()

        def _setup_ui(self):
            layout = QVBoxLayout(self)

            # SIMULATION DECISION ONLY warning — prominent
            sim_banner = QLabel(
                "⚠ SIMULATION DECISION ONLY — NO ORDER WILL BE SENT\n"
                "Research Only | No Real Orders | Not Investment Advice"
            )
            sim_banner.setStyleSheet(
                "background-color: #fff3cd; color: #856404; font-weight: bold; "
                "font-size: 12px; padding: 8px; border: 1px solid #ffc107;"
            )
            sim_banner.setAlignment(Qt.AlignCenter)
            sim_banner.setWordWrap(True)
            layout.addWidget(sim_banner)

            # Context info
            if self._symbol or self._replay_date:
                ctx = QLabel(f"Symbol: {self._symbol}  |  Date: {self._replay_date}")
                ctx.setStyleSheet("font-weight: bold; color: #333;")
                layout.addWidget(ctx)

            # Action buttons
            action_group = QGroupBox("Action (choose one)")
            action_layout = QHBoxLayout(action_group)
            self._action_combo = QComboBox()
            self._action_combo.addItems(VALID_ACTIONS)
            action_layout.addWidget(QLabel("Action:"))
            action_layout.addWidget(self._action_combo)
            layout.addWidget(action_group)

            # Form fields
            form = QFormLayout()

            self._price_edit = QLineEdit()
            self._price_edit.setPlaceholderText("Optional planned price")
            form.addRow("Planned Price:", self._price_edit)

            self._position_pct_spin = QDoubleSpinBox()
            self._position_pct_spin.setRange(0, 100)
            self._position_pct_spin.setValue(0)
            self._position_pct_spin.setSuffix(" %")
            form.addRow("Position % (0=not set):", self._position_pct_spin)

            self._stop_edit = QLineEdit()
            self._stop_edit.setPlaceholderText("Optional stop price")
            form.addRow("Stop Price:", self._stop_edit)

            self._target_edit = QLineEdit()
            self._target_edit.setPlaceholderText("Optional target price")
            form.addRow("Target Price:", self._target_edit)

            self._confidence_spin = QSpinBox()
            self._confidence_spin.setRange(0, 100)
            self._confidence_spin.setValue(50)
            self._confidence_spin.setSuffix(" %")
            form.addRow("Confidence:", self._confidence_spin)

            self._reasons_edit = QLineEdit()
            self._reasons_edit.setPlaceholderText("Comma-separated reasons")
            form.addRow("Reasons:", self._reasons_edit)

            self._notes_edit = QTextEdit()
            self._notes_edit.setMaximumHeight(80)
            self._notes_edit.setPlaceholderText("Optional notes")
            form.addRow("Notes:", self._notes_edit)

            layout.addLayout(form)

            # Simulation-only reminder at bottom
            reminder = QLabel("This is a simulation decision. No order will be placed.")
            reminder.setStyleSheet("color: #666; font-size: 10px; font-style: italic;")
            layout.addWidget(reminder)

            # Buttons
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(self.accept)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)

        def get_values(self):
            """Return dict of decision values."""
            reasons_text = self._reasons_edit.text().strip()
            reasons = [r.strip() for r in reasons_text.split(",") if r.strip()] if reasons_text else []

            def _safe_float(text):
                try:
                    v = float(text.strip())
                    return v if v > 0 else None
                except Exception:
                    return None

            position_pct = self._position_pct_spin.value()

            return {
                "action": self._action_combo.currentText(),
                "planned_price": _safe_float(self._price_edit.text()),
                "planned_position_pct": position_pct if position_pct > 0 else None,
                "stop_price": _safe_float(self._stop_edit.text()),
                "target_price": _safe_float(self._target_edit.text()),
                "confidence": self._confidence_spin.value(),
                "reasons": reasons,
                "notes": self._notes_edit.toPlainText().strip(),
                "simulation_decision_only": True,
                "no_real_orders": True,
                "research_only": True,
            }
