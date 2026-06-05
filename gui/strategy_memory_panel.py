"""
gui/strategy_memory_panel.py — StrategyMemoryPanel v0.8.1

PySide6 GUI tab for Strategy Research Memory.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
[!] ACCEPTED = Research conclusion accepted. NOT trading enabled.
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
    "[!] Research Only  |  No Real Orders  |  Production Trading BLOCKED  |  Not Investment Advice  "
    "|  ACCEPTED means research accepted, not trading enabled"
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

_ALL_SOURCE_MODULES = [
    "", "research_intelligence", "strategy_knowledge", "rule_governance",
    "replay_training", "portfolio_journal", "data_coverage", "report_pack",
    "regression", "stable_release", "research_coach", "backtest_coach", "manual",
]

# Safety tooltip for status action buttons
_STATUS_ACTION_TOOLTIP = (
    "Only updates strategy memory status.\n"
    "Does NOT enable trading or strategy execution.\n"
    "ACCEPTED = Research conclusion accepted. NOT a buy/sell signal."
)


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

            # Summary cards — v0.8.1: expanded card set
            self._summary_group = QGroupBox("Summary")
            summary_layout = QHBoxLayout(self._summary_group)
            self._card_labels: dict = {}
            for label in ["Total", "Active", "Needs Action", "Validation Queue",
                          "Repeated", "P0", "P1", "Blocked Cmds"]:
                card = QLabel(f"{label}\n—")
                card.setAlignment(Qt.AlignCenter)
                card.setStyleSheet(
                    "background: #1a1a2e; color: #aaaacc; padding: 6px; border-radius: 4px; min-width: 70px;"
                )
                card.setFont(QFont("monospace", 9))
                summary_layout.addWidget(card)
                self._card_labels[label] = card
            layout.addWidget(self._summary_group)

            # Filter controls — v0.8.1: extended
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

            # v0.8.1 new filters
            self._source_combo = QComboBox()
            self._source_combo.addItems(_ALL_SOURCE_MODULES)
            filter_layout.addWidget(QLabel("Source:"))
            filter_layout.addWidget(self._source_combo)

            try:
                from PySide6.QtWidgets import QCheckBox
                self._active_only_cb = QCheckBox("Active Only")
                filter_layout.addWidget(self._active_only_cb)
                self._needs_action_cb = QCheckBox("Needs Action")
                filter_layout.addWidget(self._needs_action_cb)
                self._include_archived_cb = QCheckBox("Incl. Archived")
                filter_layout.addWidget(self._include_archived_cb)
            except Exception:
                self._active_only_cb = None
                self._needs_action_cb = None
                self._include_archived_cb = None

            search_btn = QPushButton("Search")
            search_btn.clicked.connect(self._on_search)
            filter_layout.addWidget(search_btn)
            layout.addWidget(filter_group)

            # Main splitter: memory table + detail
            splitter = QSplitter(Qt.Vertical)

            # Memory table — v0.8.1: extended columns
            table_group = QGroupBox("Memories")
            table_layout = QVBoxLayout(table_group)
            self._memory_table = QTableWidget()
            self._memory_table.setColumnCount(10)
            self._memory_table.setHorizontalHeaderLabels([
                "Priority", "Status", "Type", "Title",
                "Source", "Symbols", "Seen", "Last Seen",
                "Needs Action", "Validation Ready",
            ])
            self._memory_table.horizontalHeader().setStretchLastSection(False)
            self._memory_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
            self._memory_table.setSelectionBehavior(QTableWidget.SelectRows)
            self._memory_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._memory_table.itemSelectionChanged.connect(self._on_memory_selected)
            table_layout.addWidget(self._memory_table)
            splitter.addWidget(table_group)

            # Detail panel — v0.8.1: tabbed detail with Safety tab
            detail_tabs = QTabWidget()

            # Summary tab
            summary_widget = QWidget()
            summary_layout = QVBoxLayout(summary_widget)
            self._detail_text = QTextEdit()
            self._detail_text.setReadOnly(True)
            self._detail_text.setPlaceholderText("Select a memory to view details.")
            summary_layout.addWidget(self._detail_text)
            detail_tabs.addTab(summary_widget, "Summary")

            # Hypothesis tab
            hyp_widget = QWidget()
            hyp_layout = QVBoxLayout(hyp_widget)
            self._hyp_text = QTextEdit()
            self._hyp_text.setReadOnly(True)
            hyp_layout.addWidget(self._hyp_text)
            detail_tabs.addTab(hyp_widget, "Hypothesis")

            # Evidence tab
            ev_widget = QWidget()
            ev_layout = QVBoxLayout(ev_widget)
            self._ev_text = QTextEdit()
            self._ev_text.setReadOnly(True)
            ev_layout.addWidget(self._ev_text)
            detail_tabs.addTab(ev_widget, "Evidence")

            # Validation tab
            val_widget = QWidget()
            val_layout = QVBoxLayout(val_widget)
            self._val_text = QTextEdit()
            self._val_text.setReadOnly(True)
            val_layout.addWidget(self._val_text)
            detail_tabs.addTab(val_widget, "Validation")

            # Commands tab
            cmd_widget = QWidget()
            cmd_layout = QVBoxLayout(cmd_widget)
            self._cmd_text = QTextEdit()
            self._cmd_text.setReadOnly(True)
            self._cmd_text.setPlaceholderText("Suggested safe commands will appear here.")
            cmd_layout.addWidget(self._cmd_text)
            detail_tabs.addTab(cmd_widget, "Commands")

            # Links tab
            links_widget = QWidget()
            links_layout = QVBoxLayout(links_widget)
            self._links_table = QTableWidget()
            self._links_table.setColumnCount(5)
            self._links_table.setHorizontalHeaderLabels([
                "Relation", "Source", "Target", "Why Linked", "Next Step",
            ])
            self._links_table.horizontalHeader().setStretchLastSection(True)
            self._links_table.setEditTriggers(QTableWidget.NoEditTriggers)
            links_layout.addWidget(self._links_table)
            detail_tabs.addTab(links_widget, "Links")

            # Safety tab
            safety_widget = QWidget()
            safety_layout = QVBoxLayout(safety_widget)
            safety_lbl = QLabel(
                "SAFETY NOTICE\n\n"
                "ACCEPTED does not enable trading or strategy execution.\n"
                "All memory statuses are research workflow states only.\n"
                "No real orders. Production Trading BLOCKED.\n"
                "Not Investment Advice."
            )
            safety_lbl.setStyleSheet(
                "background: #220000; color: #FF8888; font-weight: bold; padding: 10px; border-radius: 4px;"
            )
            safety_lbl.setWordWrap(True)
            safety_layout.addWidget(safety_lbl)
            safety_layout.addStretch(1)
            detail_tabs.addTab(safety_widget, "Safety")

            splitter.addWidget(detail_tabs)
            layout.addWidget(splitter, 1)

            # Action buttons row 1
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

            layout.addLayout(btn_layout)

            # Status action buttons row — v0.8.1 with research-only tooltips
            status_btn_layout = QHBoxLayout()
            _status_actions = [
                ("Set REVIEWING",           "REVIEWING"),
                ("Set VALIDATING",          "VALIDATING"),
                ("Set NEEDS_MORE_EVIDENCE", "NEEDS_MORE_EVIDENCE"),
                ("Set ACCEPTED",            "ACCEPTED"),
                ("Set REJECTED",            "REJECTED"),
                ("Archive",                 "ARCHIVED"),
            ]
            for btn_label, target_status in _status_actions:
                sbtn = QPushButton(btn_label)
                sbtn.setToolTip(_STATUS_ACTION_TOOLTIP)
                sbtn.clicked.connect(
                    lambda checked=False, s=target_status: self._on_set_status(s)
                )
                status_btn_layout.addWidget(sbtn)

            layout.addLayout(status_btn_layout)

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
            """Populate memory table — v0.8.1: P0/P1 first, ARCHIVED hidden by default."""
            self._memory_table.setRowCount(0)
            # Sort: P0/P1 first, then by status order
            priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
            status_order = {"NEW": 0, "REVIEWING": 1, "VALIDATING": 2,
                            "NEEDS_MORE_EVIDENCE": 3, "ACCEPTED": 4, "REJECTED": 5, "ARCHIVED": 6}
            # Hide archived by default (unless include_archived checked)
            show_archived = False
            if self._include_archived_cb is not None:
                try:
                    show_archived = self._include_archived_cb.isChecked()
                except Exception:
                    pass
            filtered = [m for m in memories if show_archived or not str(m.get("archived", "")).lower() in ("true", "1")]
            sorted_mems = sorted(
                filtered,
                key=lambda m: (
                    priority_order.get(str(m.get("priority", "P3")), 9),
                    status_order.get(str(m.get("status", "NEW")), 9),
                )
            )
            for row_data in sorted_mems:
                row = self._memory_table.rowCount()
                self._memory_table.insertRow(row)
                syms = row_data.get("related_symbols", "")
                if isinstance(syms, list):
                    syms = ",".join(syms)
                na = str(row_data.get("needs_action", "")).lower() in ("true", "1")
                vr = str(row_data.get("validation_ready", "")).lower() in ("true", "1")
                cols = [
                    row_data.get("priority", ""),
                    row_data.get("status", ""),
                    row_data.get("memory_type", ""),
                    row_data.get("title", ""),
                    row_data.get("source_module", ""),
                    str(syms)[:20],
                    str(row_data.get("seen_count", 1)),
                    str(row_data.get("last_seen_at", ""))[:10],
                    "YES" if na else "",
                    "YES" if vr else "",
                ]
                for col, val in enumerate(cols):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    # Store memory_id in UserRole for lookup
                    if col == 0:
                        item.setData(Qt.UserRole, row_data.get("memory_id", ""))
                    pri = row_data.get("priority", "")
                    if col == 0 and pri in _PRI_COLORS:
                        item.setForeground(QColor(_PRI_COLORS[pri]))
                    st = row_data.get("status", "")
                    if col == 1 and st in _STATUS_COLORS:
                        item.setForeground(QColor(_STATUS_COLORS[st]))
                    self._memory_table.setItem(row, col, item)

        def _populate_links_table(self, links: list):
            """Populate links table — v0.8.1: Why Linked and Next Step columns."""
            self._links_table.setRowCount(0)
            for lk in links:
                row = self._links_table.rowCount()
                self._links_table.insertRow(row)
                target_disp = lk.get("target_title", "") or lk.get("target_id", "")
                cols = [
                    lk.get("relation_type", ""),
                    lk.get("source_memory_id", ""),
                    str(target_disp)[:40],
                    lk.get("why_linked", lk.get("description", ""))[:60],
                    lk.get("suggested_next_step", "")[:50],
                ]
                for col, val in enumerate(cols):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self._links_table.setItem(row, col, item)

        def _update_summary_cards(self, summary: dict):
            """Update summary cards — v0.8.1: extended card set."""
            memories = self._memories
            needs_action_count = sum(1 for m in memories if str(m.get("needs_action", "")).lower() in ("true", "1"))
            val_queue_count = sum(1 for m in memories if not str(m.get("archived", "")).lower() in ("true", "1") and (
                m.get("status") in ("VALIDATING", "REVIEWING") or
                (m.get("validation_plan") and m.get("status") in ("NEW", "REVIEWING"))
            ))
            repeated_count = sum(1 for m in memories if int(m.get("seen_count", 1) or 1) > 1 and
                                  not str(m.get("archived", "")).lower() in ("true", "1"))
            blocked_cmd_count = sum(int(m.get("blocked_command_count", 0) or 0) for m in memories)
            mapping = {
                "Total": str(summary.get("total_memories", "—")),
                "Active": str(summary.get("active_count", "—")),
                "Needs Action": str(needs_action_count),
                "Validation Queue": str(val_queue_count),
                "Repeated": str(repeated_count),
                "P0": str(summary.get("p0_count", "—")),
                "P1": str(summary.get("p1_count", "—")),
                "Blocked Cmds": str(blocked_cmd_count),
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
            if row < 0:
                return
            try:
                # find actual memory by memory_id from UserRole in col 0
                mem_id_item = self._memory_table.item(row, 0)
                if not mem_id_item:
                    return
                mem_id = mem_id_item.data(Qt.UserRole) or mem_id_item.text()
                mem = next((m for m in self._memories if m.get("memory_id") == mem_id), None)
                if not mem:
                    return
                # --- Summary tab ---
                lines = [
                    f"Memory ID:        {mem.get('memory_id', '')}",
                    f"Type:             {mem.get('memory_type', '')}",
                    f"Priority:         {mem.get('priority', '')}",
                    f"Status:           {mem.get('status', '')}",
                    f"Source:           {mem.get('source_module', '')}",
                    f"Confidence:       {mem.get('confidence', '')}",
                    f"Seen:             {mem.get('seen_count', 1)}x",
                    f"Last Seen:        {str(mem.get('last_seen_at', ''))[:10]}",
                    f"Created:          {str(mem.get('created_at', ''))[:10]}",
                    f"Last Action At:   {str(mem.get('last_action_at', ''))[:10]}",
                    f"Needs Action:     {'YES' if str(mem.get('needs_action','')).lower() in ('true','1') else 'NO'}",
                    f"Validation Ready: {'YES' if str(mem.get('validation_ready','')).lower() in ('true','1') else 'NO'}",
                    "",
                    f"Title:            {mem.get('title', '')}",
                    f"Summary:          {mem.get('summary', '')}",
                    "",
                    f"Status Hint:      {mem.get('status_hint', '')}",
                    f"Next Step:        {mem.get('next_step', '')}",
                    "",
                    f"Risk Notes:       {mem.get('risk_notes', '')}",
                    f"Symbols:          {mem.get('related_symbols', '')}",
                    f"Rules:            {mem.get('related_rules', '')}",
                    "",
                    "[!] Research Only. No Real Orders. Production Trading BLOCKED.",
                    "[!] ACCEPTED = Research conclusion. NOT a trading signal.",
                ]
                self._detail_text.setPlainText("\n".join(lines))
                # --- Hypothesis tab ---
                self._hyp_text.setPlainText(
                    f"Hypothesis:\n{mem.get('hypothesis', '') or '(none)'}\n\n"
                    f"Summary:\n{mem.get('summary', '') or '(none)'}"
                )
                # --- Evidence tab ---
                self._ev_text.setPlainText(
                    f"Evidence:\n{mem.get('evidence', '') or '(none)'}\n\n"
                    f"Seen Count: {mem.get('seen_count', 1)}"
                )
                # --- Validation tab ---
                self._val_text.setPlainText(
                    f"Validation Plan:\n{mem.get('validation_plan', '') or '(none)'}\n\n"
                    f"Status:          {mem.get('status', '')}\n"
                    f"Validation Ready: {'YES' if str(mem.get('validation_ready','')).lower() in ('true','1') else 'NO'}"
                )
                # --- Commands tab ---
                cmds = mem.get("suggested_commands", "")
                if isinstance(cmds, str):
                    cmds = [c for c in cmds.split("|") if c]
                cmd_lines = [
                    "Suggested Safe Commands (Research Only — no trading actions):",
                    "",
                ]
                for cmd in cmds:
                    # Guard: skip commands with forbidden keywords
                    forbidden = any(kw in cmd.upper() for kw in ["BUY", "SELL", "ORDER", "EXECUTE"])
                    if not forbidden:
                        cmd_lines.append(f"  {cmd}")
                if not cmds:
                    cmd_lines.append("  (none)")
                cmd_lines += ["", "[!] All commands are research-only read operations."]
                self._cmd_text.setPlainText("\n".join(cmd_lines))
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
                # v0.8.1 new filters
                src = self._source_combo.currentText()
                if src:
                    filters["source_module"] = src
                if self._active_only_cb is not None:
                    try:
                        if self._active_only_cb.isChecked():
                            filters["active_only"] = True
                    except Exception:
                        pass
                if self._needs_action_cb is not None:
                    try:
                        if self._needs_action_cb.isChecked():
                            filters["needs_action"] = True
                    except Exception:
                        pass
                if self._include_archived_cb is not None:
                    try:
                        if self._include_archived_cb.isChecked():
                            filters["include_archived"] = True
                    except Exception:
                        pass
                results = adapter.search_advanced(**filters)
                self._memories = results
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
            """Legacy update status using status filter combo."""
            row = self._memory_table.currentRow()
            if row < 0:
                self._status_lbl.setText("Select a memory first.")
                return
            mem_id_item = self._memory_table.item(row, 0)
            if not mem_id_item:
                return
            mem_id = mem_id_item.data(Qt.UserRole) or mem_id_item.text()
            status = self._status_combo.currentText()
            if not status:
                self._status_lbl.setText("Select a status in the filter first.")
                return
            self._do_update_status(mem_id, status)

        def _on_set_status(self, status: str):
            """Set status via status action button — v0.8.1."""
            row = self._memory_table.currentRow()
            if row < 0:
                self._status_lbl.setText("Select a memory first.")
                return
            mem_id_item = self._memory_table.item(row, 0)
            if not mem_id_item:
                return
            mem_id = mem_id_item.data(Qt.UserRole) or mem_id_item.text()
            self._do_update_status(mem_id, status)

        def _do_update_status(self, mem_id: str, status: str):
            """Shared update status implementation with research-only reminder."""
            try:
                from gui.strategy_memory_adapter import StrategyMemoryAdapter
                adapter = StrategyMemoryAdapter()
                ok = adapter.update_status(mem_id, status)
                if ok:
                    msg = (
                        f"Updated {mem_id} → {status}. "
                        f"[!] Research Only. Does NOT enable trading."
                    )
                    self._status_lbl.setText(msg)
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
            mem_id = mem_id_item.data(Qt.UserRole) or mem_id_item.text()
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

        def closeEvent(self, event):
            """Ensure QThread cleanup on close — v0.8.1."""
            if self._worker and self._worker.isRunning():
                self._worker.quit()
                self._worker.wait()
            super().closeEvent(event)


else:
    # PySide6 not available — stub class
    class StrategyMemoryPanel:
        """Stub StrategyMemoryPanel — PySide6 not available."""
        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, *args, **kwargs):
            pass
