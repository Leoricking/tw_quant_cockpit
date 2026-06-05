"""
gui/strategy_memory_panel.py — StrategyMemoryPanel v0.7.2

PySide6 GUI tab for Strategy Research Memory.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QGroupBox,
        QTextEdit, QHeaderView, QSplitter, QTabWidget, QSizePolicy,
        QLineEdit, QApplication,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — StrategyMemoryPanel will not render.")

_SAFETY_BANNER = (
    "[!] Research Only  |  No Real Orders  |  Production Trading BLOCKED  |  Not Investment Advice"
)

_PRI_COLORS = {
    "P0": "#FF4444",
    "P1": "#FFAA00",
    "P2": "#AACC00",
    "P3": "#4488FF",
}

_STATUS_COLORS = {
    "NEW":                "#AAAAFF",
    "REVIEWING":          "#FFCC44",
    "VALIDATING":         "#FFAA00",
    "ACCEPTED":           "#44CC44",
    "REJECTED":           "#FF4444",
    "ARCHIVED":           "#888888",
    "NEEDS_MORE_EVIDENCE": "#FF8800",
}

_ALL_MEMORY_TYPES = [
    "", "STRATEGY_HYPOTHESIS", "RULE_CANDIDATE", "REPLAY_MISTAKE_PATTERN",
    "JOURNAL_PATTERN", "DATA_GAP", "REPORT_GAP", "REGRESSION_RISK",
    "PROVIDER_LIMITATION", "RESEARCH_CONCLUSION", "FOLLOW_UP_TASK",
]

_ALL_STATUSES = [
    "", "NEW", "REVIEWING", "VALIDATING", "ACCEPTED",
    "REJECTED", "ARCHIVED", "NEEDS_MORE_EVIDENCE",
]

_ALL_PRIORITIES = ["", "P0", "P1", "P2", "P3"]


if _PYSIDE6_OK:

    class StrategyMemoryWorker(QThread):
        """Background thread for strategy memory extraction."""

        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode = mode

        def run(self):
            try:
                from gui.strategy_memory_adapter import StrategyMemoryAdapter
                adapter = StrategyMemoryAdapter()
                result = adapter.run_memory_extraction(mode=self._mode)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class StrategyMemoryPanel(QWidget):
        """
        PySide6 panel for Strategy Research Memory.

        [!] Research Only. No Real Orders. Production Trading BLOCKED.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, parent=None):
            super().__init__(parent)
            self._memories: List[dict] = []
            self._links: List[dict] = []
            self._worker: Optional[StrategyMemoryWorker] = None
            self._setup_ui()
            self._refresh_data()

        def _setup_ui(self):
            layout = QVBoxLayout(self)
            layout.setContentsMargins(6, 6, 6, 6)
            layout.setSpacing(4)

            # Safety banner
            banner = QLabel(_SAFETY_BANNER)
            banner.setStyleSheet(
                "background: #220000; color: #FF8888; font-weight: bold; padding: 4px; border-radius: 3px;"
            )
            banner.setAlignment(Qt.AlignCenter)
            layout.addWidget(banner)

            # Summary cards
            self._summary_group = QGroupBox("Summary")
            summary_layout = QHBoxLayout(self._summary_group)
            self._card_labels: dict = {}
            for label in ["Total", "Active", "New", "Reviewing", "Validating",
                          "Needs Evidence", "P0", "P1"]:
                card = QLabel(f"{label}\n—")
                card.setAlignment(Qt.AlignCenter)
                card.setStyleSheet(
                    "background: #1a1a2e; color: #aaaacc; padding: 6px; border-radius: 4px; min-width: 60px;"
                )
                card.setFont(QFont("monospace", 9))
                summary_layout.addWidget(card)
                self._card_labels[label] = card
            layout.addWidget(self._summary_group)

            # Filter controls
            filter_group = QGroupBox("Filters")
            filter_layout = QHBoxLayout(filter_group)
            self._keyword_edit = QLineEdit()
            self._keyword_edit.setPlaceholderText("Keyword...")
            filter_layout.addWidget(QLabel("Keyword:"))
            filter_layout.addWidget(self._keyword_edit)

            self._type_combo = QComboBox()
            self._type_combo.addItems(_ALL_MEMORY_TYPES)
            filter_layout.addWidget(QLabel("Type:"))
            filter_layout.addWidget(self._type_combo)

            self._status_combo = QComboBox()
            self._status_combo.addItems(_ALL_STATUSES)
            filter_layout.addWidget(QLabel("Status:"))
            filter_layout.addWidget(self._status_combo)

            self._priority_combo = QComboBox()
            self._priority_combo.addItems(_ALL_PRIORITIES)
            filter_layout.addWidget(QLabel("Priority:"))
            filter_layout.addWidget(self._priority_combo)

            self._symbol_edit = QLineEdit()
            self._symbol_edit.setPlaceholderText("Symbol...")
            filter_layout.addWidget(QLabel("Symbol:"))
            filter_layout.addWidget(self._symbol_edit)

            search_btn = QPushButton("Search")
            search_btn.clicked.connect(self._on_search)
            filter_layout.addWidget(search_btn)
            layout.addWidget(filter_group)

            # Main splitter: memory table + detail
            splitter = QSplitter(Qt.Vertical)

            # Memory table
            table_group = QGroupBox("Memories")
            table_layout = QVBoxLayout(table_group)
            self._memory_table = QTableWidget()
            self._memory_table.setColumnCount(8)
            self._memory_table.setHorizontalHeaderLabels([
                "Memory ID", "Type", "Priority", "Status",
                "Title", "Source", "Seen", "Last Seen",
            ])
            self._memory_table.horizontalHeader().setStretchLastSection(False)
            self._memory_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
            self._memory_table.setSelectionBehavior(QTableWidget.SelectRows)
            self._memory_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._memory_table.itemSelectionChanged.connect(self._on_memory_selected)
            table_layout.addWidget(self._memory_table)
            splitter.addWidget(table_group)

            # Detail panel
            detail_tabs = QTabWidget()

            # Memory detail tab
            detail_widget = QWidget()
            detail_layout = QVBoxLayout(detail_widget)
            self._detail_text = QTextEdit()
            self._detail_text.setReadOnly(True)
            self._detail_text.setPlaceholderText("Select a memory to view details.")
            detail_layout.addWidget(self._detail_text)
            detail_tabs.addTab(detail_widget, "Memory Detail")

            # Links tab
            links_widget = QWidget()
            links_layout = QVBoxLayout(links_widget)
            self._links_table = QTableWidget()
            self._links_table.setColumnCount(5)
            self._links_table.setHorizontalHeaderLabels([
                "Link ID", "Source", "Relation", "Target", "Description",
            ])
            self._links_table.horizontalHeader().setStretchLastSection(True)
            self._links_table.setEditTriggers(QTableWidget.NoEditTriggers)
            links_layout.addWidget(self._links_table)
            detail_tabs.addTab(links_widget, "Links")

            splitter.addWidget(detail_tabs)
            layout.addWidget(splitter, 1)

            # Action buttons
            btn_layout = QHBoxLayout()
            run_btn = QPushButton("Run Memory Extraction")
            run_btn.clicked.connect(self._on_run_extraction)
            btn_layout.addWidget(run_btn)

            report_btn = QPushButton("Generate Report")
            report_btn.clicked.connect(self._on_generate_report)
            btn_layout.addWidget(report_btn)

            refresh_btn = QPushButton("Refresh")
            refresh_btn.clicked.connect(self._refresh_data)
            btn_layout.addWidget(refresh_btn)

            self._status_lbl = QLabel("[!] Research Only. No Real Orders.")
            self._status_lbl.setStyleSheet("color: #888888; font-size: 9px;")
            btn_layout.addWidget(self._status_lbl)

            update_status_btn = QPushButton("Update Status")
            update_status_btn.clicked.connect(self._on_update_status)
            btn_layout.addWidget(update_status_btn)

            archive_btn = QPushButton("Archive Memory")
            archive_btn.clicked.connect(self._on_archive_memory)
            btn_layout.addWidget(archive_btn)

            layout.addLayout(btn_layout)

        def _refresh_data(self):
            try:
                from gui.strategy_memory_adapter import StrategyMemoryAdapter
                adapter = StrategyMemoryAdapter()
                self._memories = adapter.load_memories()
                self._links = adapter.load_links()
                summary_result = adapter.load_latest_summary()
                self._populate_table(self._memories)
                self._populate_links_table(self._links)
                if summary_result.get("ok"):
                    self._update_summary_cards(summary_result.get("summary", {}))
            except Exception as exc:
                self._status_lbl.setText(f"Refresh error: {exc}")

        def _populate_table(self, memories: list):
            self._memory_table.setRowCount(0)
            for row_data in memories:
                row = self._memory_table.rowCount()
                self._memory_table.insertRow(row)
                cols = [
                    row_data.get("memory_id", ""),
                    row_data.get("memory_type", ""),
                    row_data.get("priority", ""),
                    row_data.get("status", ""),
                    row_data.get("title", ""),
                    row_data.get("source_module", ""),
                    str(row_data.get("seen_count", 1)),
                    str(row_data.get("last_seen_at", ""))[:10],
                ]
                for col, val in enumerate(cols):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    # Color by priority
                    pri = row_data.get("priority", "")
                    if col == 2 and pri in _PRI_COLORS:
                        item.setForeground(QColor(_PRI_COLORS[pri]))
                    # Color by status
                    st = row_data.get("status", "")
                    if col == 3 and st in _STATUS_COLORS:
                        item.setForeground(QColor(_STATUS_COLORS[st]))
                    self._memory_table.setItem(row, col, item)

        def _populate_links_table(self, links: list):
            self._links_table.setRowCount(0)
            for lk in links:
                row = self._links_table.rowCount()
                self._links_table.insertRow(row)
                cols = [
                    lk.get("link_id", ""),
                    lk.get("source_memory_id", ""),
                    lk.get("relation_type", ""),
                    lk.get("target_id", ""),
                    lk.get("description", ""),
                ]
                for col, val in enumerate(cols):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self._links_table.setItem(row, col, item)

        def _update_summary_cards(self, summary: dict):
            mapping = {
                "Total": str(summary.get("total_memories", "—")),
                "Active": str(summary.get("active_count", "—")),
                "New": str(summary.get("new_count", "—")),
                "Reviewing": str(summary.get("reviewing_count", "—")),
                "Validating": str(summary.get("validating_count", "—")),
                "Needs Evidence": str(summary.get("needs_more_evidence_count", "—")),
                "P0": str(summary.get("p0_count", "—")),
                "P1": str(summary.get("p1_count", "—")),
            }
            for label, val in mapping.items():
                lbl = self._card_labels.get(label)
                if lbl:
                    lbl.setText(f"{label}\n{val}")

        def _on_memory_selected(self):
            rows = self._memory_table.selectedItems()
            if not rows:
                return
            row = self._memory_table.currentRow()
            if row < 0 or row >= len(self._memories):
                return
            try:
                # find actual memory by memory_id from table
                mem_id_item = self._memory_table.item(row, 0)
                if not mem_id_item:
                    return
                mem_id = mem_id_item.text()
                mem = next((m for m in self._memories if m.get("memory_id") == mem_id), None)
                if not mem:
                    return
                lines = [
                    f"Memory ID:     {mem.get('memory_id', '')}",
                    f"Type:          {mem.get('memory_type', '')}",
                    f"Priority:      {mem.get('priority', '')}",
                    f"Status:        {mem.get('status', '')}",
                    f"Source:        {mem.get('source_module', '')}",
                    f"Confidence:    {mem.get('confidence', '')}",
                    f"Seen:          {mem.get('seen_count', 1)}x",
                    f"Last Seen:     {str(mem.get('last_seen_at', ''))[:10]}",
                    f"Created:       {str(mem.get('created_at', ''))[:10]}",
                    "",
                    f"Title:         {mem.get('title', '')}",
                    f"Summary:       {mem.get('summary', '')}",
                    "",
                    f"Hypothesis:    {mem.get('hypothesis', '')}",
                    f"Evidence:      {mem.get('evidence', '')}",
                    f"Validation:    {mem.get('validation_plan', '')}",
                    "",
                    f"Suggested Commands:",
                ]
                cmds = mem.get("suggested_commands", "")
                if isinstance(cmds, str):
                    cmds = [c for c in cmds.split("|") if c]
                for cmd in cmds:
                    lines.append(f"  {cmd}")
                lines += [
                    "",
                    f"Risk Notes:    {mem.get('risk_notes', '')}",
                    f"Symbols:       {mem.get('related_symbols', '')}",
                    f"Rules:         {mem.get('related_rules', '')}",
                    "",
                    "[!] Research Only. No Real Orders. Production Trading BLOCKED.",
                ]
                self._detail_text.setPlainText("\n".join(lines))
            except Exception as exc:
                self._detail_text.setPlainText(f"Error loading detail: {exc}")

        def _on_search(self):
            try:
                from gui.strategy_memory_adapter import StrategyMemoryAdapter
                adapter = StrategyMemoryAdapter()
                filters = {}
                kw = self._keyword_edit.text().strip()
                if kw:
                    filters["keyword"] = kw
                t = self._type_combo.currentText()
                if t:
                    filters["memory_type"] = t
                s = self._status_combo.currentText()
                if s:
                    filters["status"] = s
                p = self._priority_combo.currentText()
                if p:
                    filters["priority"] = p
                sym = self._symbol_edit.text().strip()
                if sym:
                    filters["symbol"] = sym
                results = adapter.search_memories(**filters)
                self._populate_table(results)
                self._status_lbl.setText(f"{len(results)} results. [!] Research Only.")
            except Exception as exc:
                self._status_lbl.setText(f"Search error: {exc}")

        def _on_run_extraction(self):
            if self._worker and self._worker.isRunning():
                return
            self._status_lbl.setText("Running extraction... [!] Research Only.")
            self._worker = StrategyMemoryWorker(mode="real")
            self._worker.finished.connect(self._on_extraction_done)
            self._worker.error.connect(self._on_extraction_error)
            self._worker.start()

        def _on_extraction_done(self, result: dict):
            count = result.get("memory_count", 0)
            self._status_lbl.setText(
                f"Extraction done: {count} memories. [!] Research Only. No Real Orders."
            )
            self._refresh_data()

        def _on_extraction_error(self, err: str):
            self._status_lbl.setText(f"Extraction error: {err}")

        def _on_generate_report(self):
            try:
                from gui.strategy_memory_adapter import StrategyMemoryAdapter
                adapter = StrategyMemoryAdapter()
                result = adapter.generate_report(mode="real")
                if result.get("ok"):
                    path = result.get("report_path", "")
                    self._status_lbl.setText(f"Report: {path} | [!] Research Only.")
                else:
                    self._status_lbl.setText(f"Report error: {result.get('error', 'unknown')}")
            except Exception as exc:
                self._status_lbl.setText(f"Report error: {exc}")

        def _on_update_status(self):
            row = self._memory_table.currentRow()
            if row < 0:
                self._status_lbl.setText("Select a memory first.")
                return
            mem_id_item = self._memory_table.item(row, 0)
            if not mem_id_item:
                return
            mem_id = mem_id_item.text()
            # Simple dialog: use status combo to set status
            status = self._status_combo.currentText()
            if not status:
                self._status_lbl.setText("Select a status in the filter first.")
                return
            try:
                from gui.strategy_memory_adapter import StrategyMemoryAdapter
                adapter = StrategyMemoryAdapter()
                ok = adapter.update_status(mem_id, status)
                if ok:
                    self._status_lbl.setText(f"Updated {mem_id} → {status}. [!] Research Only.")
                    self._refresh_data()
                else:
                    self._status_lbl.setText(f"Memory {mem_id} not found.")
            except Exception as exc:
                self._status_lbl.setText(f"Update error: {exc}")

        def _on_archive_memory(self):
            row = self._memory_table.currentRow()
            if row < 0:
                self._status_lbl.setText("Select a memory first.")
                return
            mem_id_item = self._memory_table.item(row, 0)
            if not mem_id_item:
                return
            mem_id = mem_id_item.text()
            try:
                from gui.strategy_memory_adapter import StrategyMemoryAdapter
                adapter = StrategyMemoryAdapter()
                ok = adapter.archive_memory(mem_id)
                if ok:
                    self._status_lbl.setText(f"Archived {mem_id}. [!] Research Only.")
                    self._refresh_data()
                else:
                    self._status_lbl.setText(f"Memory {mem_id} not found.")
            except Exception as exc:
                self._status_lbl.setText(f"Archive error: {exc}")


else:
    # PySide6 not available — stub class
    class StrategyMemoryPanel:
        """Stub StrategyMemoryPanel — PySide6 not available."""
        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, *args, **kwargs):
            pass
