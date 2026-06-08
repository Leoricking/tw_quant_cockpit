"""
gui/evidence_graph_panel.py — Research Intelligence Evidence Graph Panel v0.8.3

PySide6 GUI tab for the Evidence Graph.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Does NOT display BUY/SELL/ORDER. Does NOT connect broker. Does NOT auto-trade.
[!] Copy Suggested Next Step only copies safe research commands.
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QSplitter,
        QTextEdit, QComboBox, QLineEdit, QGroupBox, QSizePolicy,
        QApplication,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6 = True
except ImportError:
    _PYSIDE6 = False
    logger.warning("PySide6 not available — EvidenceGraphPanel degraded")

    # Minimal stubs so the module imports without crashing
    class QWidget:  # type: ignore
        def __init__(self, *a, **kw): pass
    class QThread:  # type: ignore
        def __init__(self, *a, **kw): pass
        def start(self): pass
        def quit(self): pass
        def wait(self, *a): pass
        class Signal:
            def __init__(self, *a): pass
            def emit(self, *a): pass
            def connect(self, *a): pass


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Allowed next-step values (safe research only)
_SAFE_NEXT_STEPS = frozenset([
    "REVIEW", "TRACE_EVIDENCE", "VALIDATE", "BACKTEST_MORE",
    "PRACTICE_REPLAY", "REVIEW_JOURNAL", "FIX_DATA", "READ_REPORT", "WAIT",
])
_FORBIDDEN_TOKENS = frozenset([
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE"
])


def _sanitize_step(text: str) -> str:
    """Remove any forbidden trading action tokens from next-step text."""
    upper = text.upper()
    for tok in _FORBIDDEN_TOKENS:
        if tok in upper:
            return "REVIEW"
    return text


# ---------------------------------------------------------------------------
# Background worker
# ---------------------------------------------------------------------------

class _GraphWorker(QThread if _PYSIDE6 else object):
    """Runs evidence graph build in a background thread."""

    if _PYSIDE6:
        finished = Signal(dict)
        error    = Signal(str)

    def __init__(self, adapter, mode: str = "real") -> None:
        if _PYSIDE6:
            super().__init__()
        self._adapter = adapter
        self._mode    = mode

    def run(self) -> None:
        try:
            result = self._adapter.build_graph(mode=self._mode)
            if _PYSIDE6:
                self.finished.emit(result)
        except Exception as exc:
            if _PYSIDE6:
                self.error.emit(str(exc))


class _ReportWorker(QThread if _PYSIDE6 else object):
    """Generates the evidence graph report in background."""

    if _PYSIDE6:
        finished = Signal(str)
        error    = Signal(str)

    def __init__(self, adapter, mode: str = "real") -> None:
        if _PYSIDE6:
            super().__init__()
        self._adapter = adapter
        self._mode    = mode

    def run(self) -> None:
        try:
            path = self._adapter.generate_report(mode=self._mode)
            if _PYSIDE6:
                self.finished.emit(path)
        except Exception as exc:
            if _PYSIDE6:
                self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

class EvidenceGraphPanel(QWidget):
    """Research Intelligence Evidence Graph GUI panel.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, parent=None) -> None:
        if _PYSIDE6:
            super().__init__(parent)
            self._build_ui()
        self._adapter = None
        self._worker  = None
        self._rep_worker = None
        self._nodes   = []
        self._edges   = []
        self._threads_data = []
        self._load_adapter()
        if _PYSIDE6:
            self._refresh_from_store()

    def _load_adapter(self) -> None:
        try:
            from gui.evidence_graph_adapter import EvidenceGraphAdapter
            self._adapter = EvidenceGraphAdapter()
        except Exception as exc:
            logger.warning("[EvidenceGraphPanel] adapter load failed: %s", exc)
            self._adapter = None

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)

        # A. Safety header
        header = QLabel(
            "Research Intelligence Evidence Graph  |  "
            "Research Only  |  No Real Orders  |  Production Trading BLOCKED  |  Not Investment Advice"
        )
        header.setStyleSheet("color: #FF8800; font-weight: bold; padding: 4px;")
        main_layout.addWidget(header)

        # B. Summary cards row
        summary_group = QGroupBox("Graph Summary")
        summary_layout = QHBoxLayout(summary_group)
        self._card_nodes        = self._make_card("Nodes", "—")
        self._card_edges        = self._make_card("Edges", "—")
        self._card_threads      = self._make_card("Threads", "—")
        self._card_orphans      = self._make_card("Orphans", "—")
        self._card_contradicts  = self._make_card("Contradictions", "—")
        self._card_req_data     = self._make_card("Req. Data", "—")
        self._card_req_bt       = self._make_card("Req. Backtest", "—")
        self._card_req_replay   = self._make_card("Req. Replay", "—")
        self._card_status       = self._make_card("Status", "—")
        for card in [self._card_nodes, self._card_edges, self._card_threads,
                     self._card_orphans, self._card_contradicts, self._card_req_data,
                     self._card_req_bt, self._card_req_replay, self._card_status]:
            summary_layout.addWidget(card)
        main_layout.addWidget(summary_group)

        # G. Filters row
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout(filter_group)

        self._filter_type = QComboBox()
        self._filter_type.addItem("All Types")
        from evidence_graph.evidence_graph_schema import ALL_NODE_TYPES
        for t in ALL_NODE_TYPES:
            self._filter_type.addItem(t)
        self._filter_type.currentTextChanged.connect(self._apply_filters)

        self._filter_module = QComboBox()
        self._filter_module.addItem("All Modules")
        for mod in ["research_intelligence", "strategy_memory", "backtest_coach",
                    "training_metrics", "replay_training", "portfolio_journal",
                    "data_coverage", "report_pack", "regression", "rule_governance"]:
            self._filter_module.addItem(mod)
        self._filter_module.currentTextChanged.connect(self._apply_filters)

        self._filter_keyword = QLineEdit()
        self._filter_keyword.setPlaceholderText("Keyword search…")
        self._filter_keyword.textChanged.connect(self._apply_filters)

        filter_layout.addWidget(QLabel("Type:"))
        filter_layout.addWidget(self._filter_type)
        filter_layout.addWidget(QLabel("Module:"))
        filter_layout.addWidget(self._filter_module)
        filter_layout.addWidget(QLabel("Keyword:"))
        filter_layout.addWidget(self._filter_keyword)
        main_layout.addWidget(filter_group)

        # Splitter: left=tables, right=detail
        splitter = QSplitter(Qt.Horizontal)

        # Left: tab widget with Node/Edge/Thread tables
        from PySide6.QtWidgets import QTabWidget
        left_tabs = QTabWidget()

        # C. Node table
        self._node_table = QTableWidget(0, 7)
        self._node_table.setHorizontalHeaderLabels(
            ["Node Type", "Title", "Source", "Priority", "Confidence", "Symbols", "Status"]
        )
        self._node_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._node_table.setSelectionBehavior(QTableWidget.SelectRows)
        self._node_table.selectionModel().selectionChanged.connect(self._on_node_selected)
        left_tabs.addTab(self._node_table, "Nodes")

        # D. Edge table
        self._edge_table = QTableWidget(0, 5)
        self._edge_table.setHorizontalHeaderLabels(
            ["Relation", "Source Node", "Target Node", "Confidence", "Suggested Next Step"]
        )
        self._edge_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_tabs.addTab(self._edge_table, "Edges")

        # E. Thread table
        self._thread_table = QTableWidget(0, 4)
        self._thread_table.setHorizontalHeaderLabels(
            ["Thread", "Key Nodes", "Evidence Path", "Next Step"]
        )
        self._thread_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_tabs.addTab(self._thread_table, "Evidence Threads")

        splitter.addWidget(left_tabs)

        # F. Detail panel
        detail_group = QGroupBox("Node Detail")
        detail_layout = QVBoxLayout(detail_group)
        self._detail_text = QTextEdit()
        self._detail_text.setReadOnly(True)
        self._detail_text.setPlaceholderText("Select a node to view details…")
        detail_layout.addWidget(self._detail_text)

        # Copy suggested next step button
        self._copy_btn = QPushButton("Copy Suggested Next Step")
        self._copy_btn.clicked.connect(self._on_copy_next_step)
        self._copy_btn.setToolTip(
            "Copies only safe research commands (REVIEW, VALIDATE, BACKTEST_MORE, etc.)"
        )
        detail_layout.addWidget(self._copy_btn)
        self._current_next_step = ""
        splitter.addWidget(detail_group)

        splitter.setSizes([700, 300])
        main_layout.addWidget(splitter)

        # H. Actions bar
        action_layout = QHBoxLayout()
        self._build_btn  = QPushButton("Build Graph")
        self._report_btn = QPushButton("Generate Report")
        self._refresh_btn = QPushButton("Refresh")
        self._status_lbl = QLabel("Ready")

        self._build_btn.clicked.connect(self._on_build)
        self._report_btn.clicked.connect(self._on_report)
        self._refresh_btn.clicked.connect(self._refresh_from_store)

        action_layout.addWidget(self._build_btn)
        action_layout.addWidget(self._report_btn)
        action_layout.addWidget(self._refresh_btn)
        action_layout.addWidget(self._status_lbl)
        action_layout.addStretch()
        action_layout.addWidget(QLabel("[!] Research Only  |  No Real Orders"))
        main_layout.addLayout(action_layout)

    def _make_card(self, label: str, value: str) -> QGroupBox:
        box    = QGroupBox(label)
        layout = QVBoxLayout(box)
        lbl    = QLabel(value)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(lbl)
        box.setProperty("_value_label", lbl)
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return box

    def _set_card(self, card: QGroupBox, value: str) -> None:
        lbl: QLabel = card.property("_value_label")
        if lbl:
            lbl.setText(value)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _on_build(self) -> None:
        if not self._adapter or not _PYSIDE6:
            return
        self._status_lbl.setText("Building graph…")
        self._build_btn.setEnabled(False)
        self._worker = _GraphWorker(self._adapter, mode="real")
        self._worker.finished.connect(self._on_build_done)
        self._worker.error.connect(self._on_worker_error)
        self._worker.start()

    def _on_build_done(self, result: dict) -> None:
        self._build_btn.setEnabled(True)
        self._nodes        = result.get("nodes", [])
        self._edges        = result.get("edges", [])
        self._threads_data = result.get("threads", [])
        summary            = result.get("summary")
        self._update_summary_cards(summary, len(self._threads_data))
        self._populate_node_table(self._nodes)
        self._populate_edge_table(self._edges)
        self._populate_thread_table(self._threads_data)
        self._status_lbl.setText(
            f"Graph built: {len(self._nodes)} nodes, {len(self._edges)} edges"
        )

    def _on_report(self) -> None:
        if not self._adapter or not _PYSIDE6:
            return
        self._status_lbl.setText("Generating report…")
        self._report_btn.setEnabled(False)
        self._rep_worker = _ReportWorker(self._adapter, mode="real")
        self._rep_worker.finished.connect(self._on_report_done)
        self._rep_worker.error.connect(self._on_worker_error)
        self._rep_worker.start()

    def _on_report_done(self, path: str) -> None:
        self._report_btn.setEnabled(True)
        self._status_lbl.setText(f"Report: {os.path.basename(path)}")

    def _on_worker_error(self, msg: str) -> None:
        self._build_btn.setEnabled(True)
        self._report_btn.setEnabled(True)
        self._status_lbl.setText(f"Error: {msg[:80]}")

    def _refresh_from_store(self) -> None:
        if not self._adapter:
            return
        self._nodes        = self._adapter.load_nodes()
        self._edges        = self._adapter.load_edges()
        self._threads_data = self._adapter.load_threads()
        summary            = self._adapter.load_latest_summary()
        if _PYSIDE6:
            self._update_summary_cards(summary, len(self._threads_data))
            self._populate_node_table(self._nodes)
            self._populate_edge_table(self._edges)
            self._populate_thread_table(self._threads_data)
            self._status_lbl.setText(
                f"Loaded: {len(self._nodes)} nodes, {len(self._edges)} edges"
                if self._nodes else "No data — click Build Graph"
            )

    def _apply_filters(self) -> None:
        if not _PYSIDE6:
            return
        type_filter   = self._filter_type.currentText()
        module_filter = self._filter_module.currentText()
        keyword       = self._filter_keyword.text().lower()

        filtered = list(self._nodes)
        if type_filter and type_filter != "All Types":
            filtered = [n for n in filtered if n.node_type == type_filter]
        if module_filter and module_filter != "All Modules":
            filtered = [n for n in filtered if n.source_module == module_filter]
        if keyword:
            filtered = [n for n in filtered
                        if keyword in n.title.lower() or keyword in n.summary.lower()]
        self._populate_node_table(filtered)

    def _on_node_selected(self) -> None:
        if not _PYSIDE6:
            return
        rows = self._node_table.selectedItems()
        if not rows:
            return
        row = self._node_table.currentRow()
        node_id = self._node_table.item(row, 1)
        if not node_id:
            return
        title = node_id.text()
        # Find matching node
        found = None
        for n in self._nodes:
            if n.title[:80] == title:
                found = n
                break
        if not found:
            return
        neighbors = self._adapter.get_neighbors(found.node_id) if self._adapter else []
        detail = self._format_node_detail(found, neighbors)
        self._detail_text.setPlainText(detail)
        # Extract next step from edges
        self._current_next_step = "REVIEW"
        for e in self._edges:
            if e.source_node_id == found.node_id and e.suggested_next_step:
                self._current_next_step = _sanitize_step(e.suggested_next_step)
                break

    def _on_copy_next_step(self) -> None:
        if not _PYSIDE6:
            return
        safe = _sanitize_step(self._current_next_step) if self._current_next_step else "REVIEW"
        clipboard = QApplication.clipboard()
        clipboard.setText(safe)
        self._status_lbl.setText(f"Copied: {safe}")

    # ------------------------------------------------------------------
    # Populate tables
    # ------------------------------------------------------------------

    def _update_summary_cards(self, summary, thread_count: int) -> None:
        if not _PYSIDE6:
            return
        if summary is None:
            return
        self._set_card(self._card_nodes,       str(summary.total_nodes))
        self._set_card(self._card_edges,       str(summary.total_edges))
        self._set_card(self._card_threads,     str(thread_count))
        self._set_card(self._card_orphans,     str(summary.orphan_node_count))
        self._set_card(self._card_contradicts, str(summary.contradiction_count))
        self._set_card(self._card_req_data,    str(summary.requires_data_count))
        self._set_card(self._card_req_bt,      str(summary.requires_backtest_count))
        self._set_card(self._card_req_replay,  str(summary.requires_replay_count))
        self._set_card(self._card_status,      summary.overall_status)

    def _populate_node_table(self, nodes) -> None:
        if not _PYSIDE6:
            return
        self._node_table.setRowCount(0)
        for n in nodes:
            r = self._node_table.rowCount()
            self._node_table.insertRow(r)
            self._node_table.setItem(r, 0, QTableWidgetItem(n.node_type))
            self._node_table.setItem(r, 1, QTableWidgetItem(n.title[:80]))
            self._node_table.setItem(r, 2, QTableWidgetItem(n.source_module))
            self._node_table.setItem(r, 3, QTableWidgetItem(n.priority))
            self._node_table.setItem(r, 4, QTableWidgetItem(f"{n.confidence:.2f}"))
            self._node_table.setItem(r, 5, QTableWidgetItem(", ".join(n.related_symbols[:3])))
            self._node_table.setItem(r, 6, QTableWidgetItem(n.status))

    def _populate_edge_table(self, edges) -> None:
        if not _PYSIDE6:
            return
        self._edge_table.setRowCount(0)
        for e in edges:
            r = self._edge_table.rowCount()
            self._edge_table.insertRow(r)
            self._edge_table.setItem(r, 0, QTableWidgetItem(e.relation_type))
            self._edge_table.setItem(r, 1, QTableWidgetItem(e.source_node_id[:20]))
            self._edge_table.setItem(r, 2, QTableWidgetItem(e.target_node_id[:20]))
            self._edge_table.setItem(r, 3, QTableWidgetItem(f"{e.confidence:.2f}"))
            step = _sanitize_step(e.suggested_next_step) if e.suggested_next_step else ""
            self._edge_table.setItem(r, 4, QTableWidgetItem(step))

    def _populate_thread_table(self, threads) -> None:
        if not _PYSIDE6:
            return
        self._thread_table.setRowCount(0)
        for t in threads:
            r = self._thread_table.rowCount()
            self._thread_table.insertRow(r)
            self._thread_table.setItem(r, 0, QTableWidgetItem(t.get("anchor_title", "")[:60]))
            key_nodes = t.get("key_nodes", [])
            if isinstance(key_nodes, list):
                key_nodes_str = ", ".join(str(x) for x in key_nodes[:4])
            else:
                key_nodes_str = str(key_nodes)
            self._thread_table.setItem(r, 1, QTableWidgetItem(key_nodes_str[:60]))
            self._thread_table.setItem(r, 2, QTableWidgetItem(t.get("evidence_path", "")[:60]))
            step = _sanitize_step(str(t.get("suggested_next_step", "REVIEW")))
            self._thread_table.setItem(r, 3, QTableWidgetItem(step))

    def _format_node_detail(self, node, neighbors) -> str:
        lines = [
            f"=== Node Detail ===",
            f"ID:      {node.node_id}",
            f"Type:    {node.node_type}",
            f"Title:   {node.title}",
            f"Source:  {node.source_module} / {node.source_ref}",
            f"Status:  {node.status}",
            f"Conf:    {node.confidence:.2f}",
            f"Priority:{node.priority}",
            f"",
            f"Summary:",
            f"{node.summary}",
            f"",
        ]
        if node.evidence_text:
            lines += [f"Evidence:", node.evidence_text, ""]
        if node.related_symbols:
            lines += [f"Symbols: {', '.join(node.related_symbols)}"]
        if node.related_strategies:
            lines += [f"Strategies: {', '.join(node.related_strategies)}"]
        if neighbors:
            lines += [f"", f"Neighbors ({len(neighbors)}):"]
            for nb in neighbors[:5]:
                lines += [f"  - [{nb.node_type}] {nb.title[:60]}"]
        lines += [
            f"",
            f"[!] Research Only. No Real Orders. Production Trading BLOCKED.",
            f"[!] Not Investment Advice.",
        ]
        return "\n".join(lines)

    def closeEvent(self, event) -> None:
        """Clean up QThreads on close to avoid QThread destroyed warning."""
        for worker in (self._worker, self._rep_worker):
            if worker is not None and _PYSIDE6:
                try:
                    worker.quit()
                    worker.wait(2000)
                except Exception:
                    pass
        if _PYSIDE6:
            super().closeEvent(event)
