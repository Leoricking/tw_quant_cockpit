"""
gui/local_research_assistant_panel.py — Local Research Assistant Panel for TW Quant Cockpit v1.0.8.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No external API. Local assistant does not enable trading.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_PYSIDE6_AVAILABLE = False
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
        QComboBox, QSpinBox, QTextEdit, QTableWidget, QTableWidgetItem,
        QPushButton, QHeaderView, QSizePolicy, QGroupBox, QSplitter,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QFont, QColor
    _PYSIDE6_AVAILABLE = True
except ImportError:
    pass

_SAFETY_BANNER = (
    "Research Only  |  No Real Orders  |  External API Disabled  |  "
    "Assistant does not enable trading"
)

_CATEGORIES = [
    "", "strategy_validation", "evidence_graph", "crash_reversal",
    "data_hygiene", "regression_hardening", "documentation", "knowledge_base",
]


if _PYSIDE6_AVAILABLE:

    class _AskWorker(QThread):
        """Background thread for asking the local assistant."""

        result_ready = Signal(object)
        error_occurred = Signal(str)

        def __init__(self, question: str, category: str, module: str, limit: int) -> None:
            super().__init__()
            self._question = question
            self._category = category or None
            self._module = module or None
            self._limit = limit

        def run(self) -> None:
            try:
                from local_assistant.local_assistant_engine import LocalResearchAssistantEngine
                engine = LocalResearchAssistantEngine()
                answer = engine.ask(
                    question=self._question,
                    category=self._category,
                    module=self._module,
                    limit=self._limit,
                )
                self.result_ready.emit(answer)
            except Exception as exc:
                self.error_occurred.emit(str(exc))

    class LocalResearchAssistantPanel(QWidget):
        """Local Research Assistant Panel.

        A. Safety Banner
        B. Ask Box: question, category filter, module filter, limit
        C. Answer area
        D. Sources Table
        E. Module Routes Table
        F. Buttons: Ask, Refresh KB, Copy Safe Answer, Copy Safe Next Steps, Copy Source Paths

        [!] Research Only. No Real Orders. External API Disabled.
        [!] No broker/trading buttons.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, parent=None) -> None:
            super().__init__(parent)
            self._worker = None
            self._current_answer = None
            self._build_ui()

        def _build_ui(self) -> None:
            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(8, 8, 8, 8)
            main_layout.setSpacing(6)

            # A. Safety Banner
            banner = QLabel(_SAFETY_BANNER)
            banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
            banner.setStyleSheet(
                "background-color: #1a3a1a; color: #80ff80; font-weight: bold; "
                "padding: 6px; border-radius: 4px;"
            )
            main_layout.addWidget(banner)

            # B. Ask Box
            ask_group = QGroupBox("Ask Local Research Assistant")
            ask_layout = QVBoxLayout(ask_group)

            # Question input
            q_row = QHBoxLayout()
            q_row.addWidget(QLabel("Question:"))
            self._question_edit = QLineEdit()
            self._question_edit.setPlaceholderText(
                "Enter research question (e.g. 'strategy validation', 'crash reversal')"
            )
            self._question_edit.returnPressed.connect(self._on_ask)
            q_row.addWidget(self._question_edit)
            ask_layout.addLayout(q_row)

            # Filters row
            filters_row = QHBoxLayout()
            filters_row.addWidget(QLabel("Category:"))
            self._category_combo = QComboBox()
            self._category_combo.addItems(_CATEGORIES)
            filters_row.addWidget(self._category_combo)

            filters_row.addWidget(QLabel("Module:"))
            self._module_edit = QLineEdit()
            self._module_edit.setPlaceholderText("(optional)")
            self._module_edit.setMaximumWidth(160)
            filters_row.addWidget(self._module_edit)

            filters_row.addWidget(QLabel("Limit:"))
            self._limit_spin = QSpinBox()
            self._limit_spin.setRange(1, 50)
            self._limit_spin.setValue(8)
            self._limit_spin.setMaximumWidth(60)
            filters_row.addWidget(self._limit_spin)
            filters_row.addStretch()
            ask_layout.addLayout(filters_row)

            main_layout.addWidget(ask_group)

            # F. Buttons
            btn_row = QHBoxLayout()
            self._btn_ask = QPushButton("Ask")
            self._btn_ask.setStyleSheet("font-weight: bold; background: #1a4a1a; color: #80ff80;")
            self._btn_ask.clicked.connect(self._on_ask)
            btn_row.addWidget(self._btn_ask)

            self._btn_refresh = QPushButton("Refresh KB")
            self._btn_refresh.clicked.connect(self._on_refresh_kb)
            btn_row.addWidget(self._btn_refresh)

            self._btn_copy_answer = QPushButton("Copy Safe Answer")
            self._btn_copy_answer.clicked.connect(self._on_copy_answer)
            btn_row.addWidget(self._btn_copy_answer)

            self._btn_copy_steps = QPushButton("Copy Safe Next Steps")
            self._btn_copy_steps.clicked.connect(self._on_copy_steps)
            btn_row.addWidget(self._btn_copy_steps)

            self._btn_copy_paths = QPushButton("Copy Source Paths")
            self._btn_copy_paths.clicked.connect(self._on_copy_paths)
            btn_row.addWidget(self._btn_copy_paths)

            btn_row.addStretch()
            main_layout.addLayout(btn_row)

            # Status label
            self._status_label = QLabel("Ready. Enter a question and click Ask.")
            self._status_label.setStyleSheet("color: #aaaaaa; font-style: italic;")
            main_layout.addWidget(self._status_label)

            # Splitter: Answer + Sources + Routes
            splitter = QSplitter(Qt.Orientation.Vertical)

            # C. Answer area
            answer_group = QGroupBox("Answer")
            answer_layout = QVBoxLayout(answer_group)
            self._answer_edit = QTextEdit()
            self._answer_edit.setReadOnly(True)
            self._answer_edit.setPlaceholderText(
                "Answer will appear here.\n\n"
                "[!] Research Only. No Real Orders. Local assistant does not enable trading."
            )
            answer_layout.addWidget(self._answer_edit)
            splitter.addWidget(answer_group)

            # D. Sources Table
            sources_group = QGroupBox("Sources")
            sources_layout = QVBoxLayout(sources_group)
            self._sources_table = QTableWidget(0, 5)
            self._sources_table.setHorizontalHeaderLabels(
                ["Title", "Category", "Module", "Score", "Path"]
            )
            self._sources_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self._sources_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            sources_layout.addWidget(self._sources_table)
            splitter.addWidget(sources_group)

            # E. Module Routes Table
            routes_group = QGroupBox("Module Routes")
            routes_layout = QVBoxLayout(routes_group)
            self._routes_table = QTableWidget(0, 4)
            self._routes_table.setHorizontalHeaderLabels(
                ["Module", "Reason", "Suggested CLI", "Safe Action"]
            )
            self._routes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self._routes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            routes_layout.addWidget(self._routes_table)
            splitter.addWidget(routes_group)

            splitter.setSizes([250, 150, 120])
            main_layout.addWidget(splitter, 1)

        def _on_ask(self) -> None:
            question = self._question_edit.text().strip()
            if not question:
                self._status_label.setText("Please enter a question.")
                return
            category = self._category_combo.currentText()
            module = self._module_edit.text().strip()
            limit = self._limit_spin.value()

            self._btn_ask.setEnabled(False)
            self._status_label.setText(f"Asking: '{question}' ...")
            self._answer_edit.clear()
            self._sources_table.setRowCount(0)
            self._routes_table.setRowCount(0)

            self._worker = _AskWorker(
                question=question,
                category=category,
                module=module,
                limit=limit,
            )
            self._worker.result_ready.connect(self._on_answer_ready)
            self._worker.error_occurred.connect(self._on_ask_error)
            self._worker.start()

        def _on_answer_ready(self, answer) -> None:
            self._current_answer = answer
            self._btn_ask.setEnabled(True)
            self._status_label.setText(
                f"Status: {answer.status} | Confidence: {answer.confidence} | "
                f"Sources: {len(answer.sources)}"
            )
            self._answer_edit.setPlainText(answer.answer)

            # Populate sources table
            self._sources_table.setRowCount(len(answer.sources))
            for i, src in enumerate(answer.sources):
                self._sources_table.setItem(i, 0, QTableWidgetItem(src.title))
                self._sources_table.setItem(i, 1, QTableWidgetItem(src.category))
                self._sources_table.setItem(i, 2, QTableWidgetItem(src.module))
                self._sources_table.setItem(i, 3, QTableWidgetItem(f"{src.score:.3f}"))
                self._sources_table.setItem(i, 4, QTableWidgetItem(src.path))

            # Populate routes table
            self._routes_table.setRowCount(len(answer.module_routes))
            for i, route in enumerate(answer.module_routes):
                self._routes_table.setItem(i, 0, QTableWidgetItem(route.module))
                self._routes_table.setItem(i, 1, QTableWidgetItem(route.reason))
                cli_str = "; ".join(route.suggested_cli[:2])
                self._routes_table.setItem(i, 2, QTableWidgetItem(cli_str))
                self._routes_table.setItem(i, 3, QTableWidgetItem(route.safe_action))

        def _on_ask_error(self, error_msg: str) -> None:
            self._btn_ask.setEnabled(True)
            self._status_label.setText(f"Error: {error_msg}")
            self._answer_edit.setPlainText(
                f"[ERROR] {error_msg}\n\n"
                "[!] Research Only. No Real Orders. Local assistant does not enable trading."
            )

        def _on_refresh_kb(self) -> None:
            self._status_label.setText("Refreshing KB index ...")
            try:
                from knowledge_base.kb_search_engine import KnowledgeBaseSearchEngine
                engine = KnowledgeBaseSearchEngine()
                engine.ensure_index()
                self._status_label.setText("KB index refreshed.")
            except Exception as exc:
                self._status_label.setText(f"KB refresh: {exc}")

        def _on_copy_answer(self) -> None:
            if self._current_answer:
                try:
                    from PySide6.QtWidgets import QApplication
                    QApplication.clipboard().setText(self._current_answer.answer)
                    self._status_label.setText("Safe answer copied to clipboard.")
                except Exception as exc:
                    self._status_label.setText(f"Copy failed: {exc}")

        def _on_copy_steps(self) -> None:
            if self._current_answer:
                try:
                    from PySide6.QtWidgets import QApplication
                    steps_text = "\n".join(
                        f"[{s.action}] {s.description}"
                        for s in self._current_answer.safe_next_steps
                    )
                    QApplication.clipboard().setText(steps_text)
                    self._status_label.setText("Safe next steps copied to clipboard.")
                except Exception as exc:
                    self._status_label.setText(f"Copy failed: {exc}")

        def _on_copy_paths(self) -> None:
            if self._current_answer:
                try:
                    from PySide6.QtWidgets import QApplication
                    paths_text = "\n".join(s.path for s in self._current_answer.sources)
                    QApplication.clipboard().setText(paths_text)
                    self._status_label.setText("Source paths copied to clipboard.")
                except Exception as exc:
                    self._status_label.setText(f"Copy failed: {exc}")

else:
    # Graceful fallback when PySide6 is not available
    class LocalResearchAssistantPanel:  # type: ignore[no-redef]
        """Stub LocalResearchAssistantPanel (PySide6 not available).

        [!] Research Only. No Real Orders. Local assistant does not enable trading.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, parent=None) -> None:
            logger.warning(
                "LocalResearchAssistantPanel: PySide6 not available. "
                "Panel is a no-op stub. [!] Research Only. No Real Orders."
            )
