"""
gui/knowledge_base_search_panel.py — Knowledge Base Search Panel for TW Quant Cockpit v1.0.7.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Search does not enable trading. Broker Execution Disabled.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_KNOWLEDGE_BASE_SEARCH_PANEL_AVAILABLE = False

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
        QComboBox, QSpinBox, QTableWidget, QTableWidgetItem,
        QTextEdit, QPushButton, QHeaderView, QSizePolicy, QApplication,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.debug("PySide6 not available; KnowledgeBaseSearchPanel will not be created")

if _PYSIDE6_AVAILABLE:
    _KNOWLEDGE_BASE_SEARCH_PANEL_AVAILABLE = True

    class _IndexWorker(QThread):
        """Background thread for building the KB index."""
        finished = Signal(list)
        error = Signal(str)

        def __init__(self, parent=None) -> None:
            super().__init__(parent)

        def run(self) -> None:
            try:
                from knowledge_base.kb_search_engine import KnowledgeBaseSearchEngine
                engine = KnowledgeBaseSearchEngine()
                items = engine.ensure_index(rebuild=True)
                self.finished.emit(items)
            except Exception as exc:
                self.error.emit(str(exc))

    class _SearchWorker(QThread):
        """Background thread for running a search."""
        finished = Signal(list)
        error = Signal(str)

        def __init__(self, query: str, category: str, module: str, limit: int, parent=None) -> None:
            super().__init__(parent)
            self._query    = query
            self._category = category or None
            self._module   = module or None
            self._limit    = limit

        def run(self) -> None:
            try:
                from knowledge_base.kb_search_engine import KnowledgeBaseSearchEngine
                engine = KnowledgeBaseSearchEngine()
                results = engine.search(
                    query=self._query,
                    category=self._category,
                    module=self._module,
                    limit=self._limit,
                )
                self.finished.emit(results)
            except Exception as exc:
                self.error.emit(str(exc))

    class KnowledgeBaseSearchPanel(QWidget):
        """Knowledge Base Search Panel for TW Quant Cockpit v1.0.7.

        [!] Research Only. No Real Orders. Production Trading: BLOCKED.
        [!] Search does not enable trading. Broker Execution Disabled.
        """

        no_real_orders     = True
        broker_disabled    = True
        research_only      = True
        production_blocked = True

        _TABLE_COLUMNS = ["Title", "Category", "Module", "Score", "Path", "Safe Next Step"]

        def __init__(self, parent=None) -> None:
            super().__init__(parent)
            self._results = []
            self._items   = []
            self._worker  = None
            self._init_ui()

        # ------------------------------------------------------------------
        # UI setup
        # ------------------------------------------------------------------

        def _init_ui(self) -> None:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(6, 6, 6, 6)

            # A. Safety Banner
            banner = QLabel(
                "Research Only  |  No Real Orders  |  Production Trading BLOCKED  |  Search does not enable trading"
            )
            banner.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setBold(True)
            banner.setFont(font)
            banner.setStyleSheet("background-color: #fff3cd; color: #856404; padding: 4px; border-radius: 3px;")
            layout.addWidget(banner)

            # B. Search Bar
            search_row = QHBoxLayout()
            self._query_edit = QLineEdit()
            self._query_edit.setPlaceholderText("Enter search query...")
            self._query_edit.returnPressed.connect(self._on_search)
            search_row.addWidget(QLabel("Query:"))
            search_row.addWidget(self._query_edit, 3)

            self._category_combo = QComboBox()
            self._category_combo.addItems([
                "", "DOC", "EXAMPLE", "TEMPLATE", "REPORT",
                "STRATEGY_MEMORY", "EVIDENCE_GRAPH", "REGRESSION",
                "GUI", "DATA_HYGIENE", "WORKFLOW", "SAFETY", "RELEASE",
            ])
            search_row.addWidget(QLabel("Category:"))
            search_row.addWidget(self._category_combo)

            self._module_edit = QLineEdit()
            self._module_edit.setPlaceholderText("Module filter...")
            search_row.addWidget(QLabel("Module:"))
            search_row.addWidget(self._module_edit)

            self._limit_spin = QSpinBox()
            self._limit_spin.setMinimum(1)
            self._limit_spin.setMaximum(200)
            self._limit_spin.setValue(20)
            search_row.addWidget(QLabel("Limit:"))
            search_row.addWidget(self._limit_spin)

            layout.addLayout(search_row)

            # C. Results Table
            self._table = QTableWidget(0, len(self._TABLE_COLUMNS))
            self._table.setHorizontalHeaderLabels(self._TABLE_COLUMNS)
            self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._table.setSelectionBehavior(QTableWidget.SelectRows)
            self._table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._table.setAlternatingRowColors(True)
            self._table.currentRowChanged.connect(self._on_row_changed)
            layout.addWidget(self._table)

            # D. Detail panel
            self._detail = QTextEdit()
            self._detail.setReadOnly(True)
            self._detail.setMaximumHeight(150)
            self._detail.setPlaceholderText(
                "Select a result to see details.\n"
                "[!] Research Only. No Real Orders. Search does not enable trading."
            )
            layout.addWidget(self._detail)

            # E. Buttons
            btn_row = QHBoxLayout()
            self._btn_build = QPushButton("Build Index")
            self._btn_build.clicked.connect(self._on_build_index)
            self._btn_search = QPushButton("Search")
            self._btn_search.clicked.connect(self._on_search)
            self._btn_refresh = QPushButton("Refresh")
            self._btn_refresh.clicked.connect(self._on_refresh)
            self._btn_copy_summary = QPushButton("Copy Safe Summary")
            self._btn_copy_summary.clicked.connect(self._on_copy_safe_summary)
            self._btn_copy_path = QPushButton("Copy File Path")
            self._btn_copy_path.clicked.connect(self._on_copy_file_path)

            for btn in [
                self._btn_build, self._btn_search, self._btn_refresh,
                self._btn_copy_summary, self._btn_copy_path,
            ]:
                btn_row.addWidget(btn)

            layout.addLayout(btn_row)

            # Status label
            self._status_label = QLabel("[!] Research Only. No Real Orders. No broker execution.")
            self._status_label.setStyleSheet("color: gray; font-size: 10px;")
            layout.addWidget(self._status_label)

        # ------------------------------------------------------------------
        # Slots
        # ------------------------------------------------------------------

        def _on_build_index(self) -> None:
            self._status_label.setText("Building index... (background)")
            self._btn_build.setEnabled(False)
            self._worker = _IndexWorker(self)
            self._worker.finished.connect(self._on_index_built)
            self._worker.error.connect(self._on_worker_error)
            self._worker.start()

        def _on_index_built(self, items) -> None:
            self._items = items
            self._status_label.setText(
                f"Index built: {len(items)} items. [!] Research Only. No Real Orders."
            )
            self._btn_build.setEnabled(True)

        def _on_search(self) -> None:
            query    = self._query_edit.text().strip()
            category = self._category_combo.currentText().strip()
            module   = self._module_edit.text().strip()
            limit    = self._limit_spin.value()
            self._status_label.setText(f"Searching for '{query}'...")
            self._btn_search.setEnabled(False)
            self._worker = _SearchWorker(query, category, module, limit, self)
            self._worker.finished.connect(self._on_search_done)
            self._worker.error.connect(self._on_worker_error)
            self._worker.start()

        def _on_search_done(self, results) -> None:
            self._results = results
            self._populate_table(results)
            self._btn_search.setEnabled(True)
            self._status_label.setText(
                f"Found {len(results)} result(s). [!] Research Only. No Real Orders."
            )

        def _on_refresh(self) -> None:
            self._table.setRowCount(0)
            self._detail.clear()
            self._results = []
            self._status_label.setText("[!] Cleared. Research Only. No Real Orders.")

        def _on_copy_safe_summary(self) -> None:
            try:
                from knowledge_base.kb_search_engine import KnowledgeBaseSearchEngine
                engine = KnowledgeBaseSearchEngine()
                summary = engine.build_safe_summary(self._results)
                clipboard = QApplication.clipboard()
                clipboard.setText(summary)
                self._status_label.setText("Safe summary copied. [!] No Real Orders.")
            except Exception as exc:
                self._status_label.setText(f"Copy failed: {exc}")

        def _on_copy_file_path(self) -> None:
            row = self._table.currentRow()
            if row < 0 or row >= len(self._results):
                self._status_label.setText("No row selected.")
                return
            result = self._results[row]
            clipboard = QApplication.clipboard()
            clipboard.setText(result.path)
            self._status_label.setText(f"Path copied: {result.path}")

        def _on_row_changed(self, row: int) -> None:
            if row < 0 or row >= len(self._results):
                self._detail.clear()
                return
            r = self._results[row]
            self._detail.setPlainText(
                f"Title:         {r.title}\n"
                f"Category:      {r.category}\n"
                f"Module:        {r.module}\n"
                f"Score:         {r.score:.1f}\n"
                f"Match Type:    {r.match_type}\n"
                f"Safe Next Step: {r.safe_next_step}\n"
                f"Path:          {r.path}\n"
                f"Excerpt:\n{r.excerpt[:300]}\n\n"
                f"[!] No Real Orders. Research Only. Search does not enable trading."
            )

        def _on_worker_error(self, msg: str) -> None:
            self._status_label.setText(f"[WARN] {msg}")
            self._btn_build.setEnabled(True)
            self._btn_search.setEnabled(True)

        # ------------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------------

        def _populate_table(self, results) -> None:
            self._table.setRowCount(0)
            if not results:
                self._detail.setPlainText("No results found.\n[!] Research Only. No Real Orders.")
                return
            for i, r in enumerate(results):
                self._table.insertRow(i)
                self._table.setItem(i, 0, QTableWidgetItem(r.title))
                self._table.setItem(i, 1, QTableWidgetItem(r.category))
                self._table.setItem(i, 2, QTableWidgetItem(r.module))
                self._table.setItem(i, 3, QTableWidgetItem(f"{r.score:.1f}"))
                self._table.setItem(i, 4, QTableWidgetItem(r.path))
                self._table.setItem(i, 5, QTableWidgetItem(r.safe_next_step))

else:
    # Fallback stub when PySide6 is not available
    class KnowledgeBaseSearchPanel:  # type: ignore[no-redef]
        """Stub panel — PySide6 not available."""
        no_real_orders     = True
        broker_disabled    = True
        research_only      = True
        production_blocked = True

        def __init__(self, *args, **kwargs) -> None:
            raise ImportError(
                "KnowledgeBaseSearchPanel requires PySide6. "
                "Run: pip install PySide6"
            )
