"""
gui/replay_journal_compare_dialog.py — ReplayJournalCompareDialog v1.2.2
[!] Research Only. No Real Orders.
[!] FORBIDDEN fields NOT shown: realized_return, future_return, hindsight_score, final_result.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True

try:
    from PyQt5.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTextEdit, QLineEdit, QSplitter,
    )
    from PyQt5.QtCore import Qt
    HAS_QT = True
except ImportError:
    HAS_QT = False

FORBIDDEN_DISPLAY_FIELDS = [
    "realized_return", "future_return", "hindsight_score",
    "final_result", "future_max_gain", "future_max_loss",
]

if HAS_QT:
    class ReplayJournalCompareDialog(QDialog):
        """
        Side-by-side comparison of two journal entries.
        [!] Forbidden performance fields never shown.
        """
        def __init__(self, parent=None, manager=None, entry_a: Optional[Dict[str, Any]] = None, entry_b: Optional[Dict[str, Any]] = None):
            super().__init__(parent)
            self._manager = manager
            self._entry_a = entry_a or {}
            self._entry_b = entry_b or {}
            self.setWindowTitle("Journal Entry Comparison v1.2.2")
            self.setMinimumSize(900, 600)
            self._build_ui()

        def _build_ui(self):
            layout = QVBoxLayout(self)

            banner = QLabel(
                "RESEARCH ONLY | SIMULATION DECISION ONLY | "
                "No performance data | No future results"
            )
            banner.setStyleSheet("background: #1a1a2e; color: #ff9; padding: 4px; font-size: 10px;")
            layout.addWidget(banner)

            # Entry selectors
            sel_layout = QHBoxLayout()
            sel_layout.addWidget(QLabel("Entry A ID:"))
            self._entry_a_input = QLineEdit(self._entry_a.get("journal_entry_id", ""))
            sel_layout.addWidget(self._entry_a_input)
            sel_layout.addWidget(QLabel("Entry B ID:"))
            self._entry_b_input = QLineEdit(self._entry_b.get("journal_entry_id", ""))
            sel_layout.addWidget(self._entry_b_input)
            self._btn_compare = QPushButton("Compare")
            self._btn_compare.clicked.connect(self._do_compare)
            sel_layout.addWidget(self._btn_compare)
            layout.addLayout(sel_layout)

            # Side-by-side
            splitter = QSplitter(Qt.Horizontal)
            self._left_text = QTextEdit()
            self._left_text.setReadOnly(True)
            splitter.addWidget(self._left_text)
            self._right_text = QTextEdit()
            self._right_text.setReadOnly(True)
            splitter.addWidget(self._right_text)
            layout.addWidget(splitter)

            # Diff
            layout.addWidget(QLabel("Differences:"))
            self._diff_text = QTextEdit()
            self._diff_text.setReadOnly(True)
            self._diff_text.setMaximumHeight(150)
            layout.addWidget(self._diff_text)

            btn_layout = QHBoxLayout()
            self._btn_close = QPushButton("Close")
            self._btn_close.clicked.connect(self.accept)
            btn_layout.addWidget(self._btn_close)
            layout.addLayout(btn_layout)

            if self._entry_a and self._entry_b:
                self._do_compare()

        def _do_compare(self):
            entry_a_id = self._entry_a_input.text()
            entry_b_id = self._entry_b_input.text()

            if self._manager and entry_a_id and entry_b_id:
                ea = self._manager.get_entry(entry_a_id) or self._entry_a
                eb = self._manager.get_entry(entry_b_id) or self._entry_b
            else:
                ea = self._entry_a
                eb = self._entry_b

            safe_a = {k: v for k, v in ea.items() if k not in FORBIDDEN_DISPLAY_FIELDS}
            safe_b = {k: v for k, v in eb.items() if k not in FORBIDDEN_DISPLAY_FIELDS}

            self._left_text.setPlainText(self._format_entry(safe_a, "Entry A"))
            self._right_text.setPlainText(self._format_entry(safe_b, "Entry B"))

            from replay.decision_comparator import DecisionJournalComparator
            cmp = DecisionJournalComparator()
            try:
                result = cmp.compare_entries(safe_a, safe_b)
                diff_lines = []
                for fld, vals in result.get("differences", {}).items():
                    diff_lines.append(f"{fld}: A={vals.get('entry_a')} | B={vals.get('entry_b')}")
                self._diff_text.setPlainText("\n".join(diff_lines) if diff_lines else "No differences found.")
            except Exception as exc:
                self._diff_text.setPlainText(f"Compare error: {exc}")

        def _format_entry(self, entry: Dict[str, Any], label: str) -> str:
            lines = [f"=== {label} ==="]
            show_fields = [
                "journal_entry_id", "action", "replay_date", "symbol",
                "confidence", "status", "decision_reason", "tags",
                "pre_decision_notes", "post_decision_notes",
            ]
            for fld in show_fields:
                if fld in entry:
                    lines.append(f"{fld}: {entry[fld]}")
            return "\n".join(lines)
else:
    class ReplayJournalCompareDialog:
        no_real_orders = True
        def __init__(self, *args, **kwargs): pass
