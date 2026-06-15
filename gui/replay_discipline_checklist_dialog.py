"""
gui/replay_discipline_checklist_dialog.py — ReplayDisciplineChecklistDialog v1.2.2
[!] Research Only. No Real Orders. Simulation Decision Only.
[!] Checklist records discipline only. No auto scoring. No trading trigger.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True

try:
    from PyQt5.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QComboBox, QTextEdit, QWidget,
    )
    from PyQt5.QtCore import Qt
    HAS_QT = True
except ImportError:
    HAS_QT = False

if HAS_QT:
    class ReplayDisciplineChecklistDialog(QDialog):
        """
        Discipline checklist dialog.
        [!] Records discipline process only. No trading signals.
        """
        def __init__(self, parent=None, items: Optional[List[Dict[str, Any]]] = None, entry_id: str = ""):
            super().__init__(parent)
            self._items = items or []
            self._entry_id = entry_id
            self._responses: Dict[str, bool] = {}
            self.setWindowTitle("Discipline Checklist v1.2.2")
            self.setMinimumSize(600, 400)
            self._build_ui()

        def _build_ui(self):
            layout = QVBoxLayout(self)

            banner = QLabel("SIMULATION DECISION ONLY — Discipline checklist records process. No trading trigger.")
            banner.setStyleSheet("background: #222; color: #ff9; padding: 4px; font-size: 10px;")
            layout.addWidget(banner)

            layout.addWidget(QLabel(f"Checklist for: {self._entry_id or 'New Entry'}"))

            # Table
            self._table = QTableWidget()
            self._table.setColumnCount(4)
            self._table.setHorizontalHeaderLabels(["Item ID", "Category", "Description", "Pass?"])
            self._table.setRowCount(len(self._items))
            for row, item in enumerate(self._items):
                self._table.setItem(row, 0, QTableWidgetItem(item.get("item_id", item.get("id", ""))))
                self._table.setItem(row, 1, QTableWidgetItem(item.get("category", "")))
                label = item.get("label", item.get("text", ""))
                req = " [REQUIRED]" if item.get("required", False) else ""
                self._table.setItem(row, 2, QTableWidgetItem(f"{label}{req}"))
                chk_combo = QComboBox()
                chk_combo.addItems(["—", "Yes", "No", "Skip"])
                self._table.setCellWidget(row, 3, chk_combo)
            self._table.horizontalHeader().setStretchLastSection(True)
            layout.addWidget(self._table)

            # Stats
            self._stats_label = QLabel("Pass: 0 / 0")
            layout.addWidget(self._stats_label)

            btn_layout = QHBoxLayout()
            self._btn_submit = QPushButton("Submit Checklist")
            self._btn_submit.clicked.connect(self._on_submit)
            btn_layout.addWidget(self._btn_submit)
            self._btn_cancel = QPushButton("Cancel")
            self._btn_cancel.clicked.connect(self.reject)
            btn_layout.addWidget(self._btn_cancel)
            layout.addLayout(btn_layout)

        def _on_submit(self):
            passed = 0
            total = self._table.rowCount()
            for row in range(total):
                item_id_item = self._table.item(row, 0)
                combo = self._table.cellWidget(row, 3)
                if item_id_item and combo:
                    item_id = item_id_item.text()
                    val = combo.currentText()
                    self._responses[item_id] = (val == "Yes")
                    if val == "Yes":
                        passed += 1
            self._stats_label.setText(f"Pass: {passed} / {total}")
            self.accept()

        def get_responses(self) -> Dict[str, bool]:
            return self._responses
else:
    class ReplayDisciplineChecklistDialog:
        no_real_orders = True
        def __init__(self, *args, **kwargs): pass
        def get_responses(self): return {}
