"""
gui/evidence_graph_panel.py — Research Intelligence Evidence Graph Panel v0.9.1

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
        QApplication, QTabWidget, QCheckBox,
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
    "REVIEW_RISK", "REVIEW_EARNINGS", "REVIEW_CHIPS", "BUILD_WATCHLIST", "DO_NOT_CHASE",
])
_FORBIDDEN_TOKENS = frozenset([
    "BUY", "SELL", "ORDER", "EXECUTE", "SUBMIT_ORDER", "AUTO_TRADE", "REAL_TRADE"
])

# Quality label colors
_QUALITY_COLORS = {
    "STRONG_EVIDENCE":   "#00AA44",
    "PARTIAL_EVIDENCE":  "#CCAA00",
    "NEEDS_DATA":        "#CC6600",
    "NEEDS_BACKTEST":    "#CC6600",
    "CONFLICTED":        "#CC0000",
    "ORPHANED":          "#CC0000",
}

# Severity colors for gaps
_SEVERITY_COLORS = {
    "HIGH":   "#CC0000",
    "MEDIUM": "#CC6600",
    "LOW":    "#CCAA00",
}


def _sanitize_step(text: str) -> str:
    """Remove any forbidden trading action tokens from next-step text."""
    upper = text.upper()
    for tok in _FORBIDDEN_TOKENS:
        if tok in upper:
            return "REVIEW"
    return text


def _to_dict(obj) -> dict:
    """Coerce an object or dict to a plain dict."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return {}


# ---------------------------------------------------------------------------
# Background workers
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


class _SearchWorker(QThread if _PYSIDE6 else object):
    """Runs search/filter queries in background."""

    if _PYSIDE6:
        finished = Signal(dict)
        error    = Signal(str)

    def __init__(self, adapter, filters: dict) -> None:
        if _PYSIDE6:
            super().__init__()
        self._adapter = adapter
        self._filters = filters

    def run(self) -> None:
        try:
            result = {}
            a = self._adapter
            kw        = self._filters.get("keyword") or None
            q_label   = self._filters.get("quality_label") or None
            module    = self._filters.get("source_module") or None
            gap_type  = self._filters.get("gap_type") or None
            crash_only = self._filters.get("crash_only", False)

            if crash_only:
                result["threads"] = a.get_crash_reversal_threads() if a else []
            else:
                result["threads"] = a.search_threads(
                    keyword=kw, quality_label=q_label, source_module=module
                ) if a else []

            result["gaps"] = a.search_gaps(
                gap_type=gap_type, keyword=kw, source_module=module
            ) if a else []

            if _PYSIDE6:
                self.finished.emit(result)
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
        self._search_worker = None
        self._nodes   = []
        self._edges   = []
        self._threads_data = []
        self._gaps_data = []
        self._crash_threads = []
        self._current_next_step = ""
        self._current_detail_id = ""
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

        # B. Summary cards row (10 cards)
        summary_group = QGroupBox("Graph Summary")
        summary_layout = QHBoxLayout(summary_group)
        self._card_nodes        = self._make_card("Nodes", "—")
        self._card_edges        = self._make_card("Edges", "—")
        self._card_threads      = self._make_card("Threads", "—")
        self._card_strong       = self._make_card("Strong", "—")
        self._card_needs_data   = self._make_card("Needs Data", "—")
        self._card_needs_bt     = self._make_card("Needs Backtest", "—")
        self._card_crash        = self._make_card("Crash Rev.", "—")
        self._card_gaps         = self._make_card("Gaps", "—")
        self._card_contradicts  = self._make_card("Contradictions", "—")
        self._card_orphans      = self._make_card("Orphans", "—")
        for card in [
            self._card_nodes, self._card_edges, self._card_threads,
            self._card_strong, self._card_needs_data, self._card_needs_bt,
            self._card_crash, self._card_gaps, self._card_contradicts,
            self._card_orphans,
        ]:
            summary_layout.addWidget(card)
        main_layout.addWidget(summary_group)

        # C. Filters row
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout(filter_group)

        self._filter_type = QComboBox()
        self._filter_type.addItem("All Types")
        try:
            from evidence_graph.evidence_graph_schema import ALL_NODE_TYPES
            for t in ALL_NODE_TYPES:
                self._filter_type.addItem(t)
        except Exception:
            pass
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

        self._filter_quality = QComboBox()
        self._filter_quality.addItems([
            "All Quality", "STRONG_EVIDENCE", "PARTIAL_EVIDENCE",
            "NEEDS_DATA", "NEEDS_BACKTEST", "CONFLICTED", "ORPHANED",
        ])
        self._filter_quality.currentTextChanged.connect(self._apply_filters)

        self._filter_gap_type = QComboBox()
        self._filter_gap_type.addItems([
            "All Gap Types", "ORPHAN_NODE", "REQUIRES_DATA",
            "REQUIRES_BACKTEST", "REQUIRES_REPLAY", "CONTRADICTION",
        ])
        self._filter_gap_type.currentTextChanged.connect(self._apply_filters)

        self._chk_crash_only    = QCheckBox("Crash Reversal Only")
        self._chk_show_orphans  = QCheckBox("Show Orphans")
        self._chk_show_contrads = QCheckBox("Show Contradictions")

        self._chk_crash_only.stateChanged.connect(self._apply_filters)
        self._chk_show_orphans.stateChanged.connect(self._apply_filters)
        self._chk_show_contrads.stateChanged.connect(self._apply_filters)

        filter_layout.addWidget(QLabel("Type:"))
        filter_layout.addWidget(self._filter_type)
        filter_layout.addWidget(QLabel("Module:"))
        filter_layout.addWidget(self._filter_module)
        filter_layout.addWidget(QLabel("Keyword:"))
        filter_layout.addWidget(self._filter_keyword)
        filter_layout.addWidget(QLabel("Quality:"))
        filter_layout.addWidget(self._filter_quality)
        filter_layout.addWidget(QLabel("Gap:"))
        filter_layout.addWidget(self._filter_gap_type)
        filter_layout.addWidget(self._chk_crash_only)
        filter_layout.addWidget(self._chk_show_orphans)
        filter_layout.addWidget(self._chk_show_contrads)
        main_layout.addWidget(filter_group)

        # Splitter: left=tabs, right=detail
        splitter = QSplitter(Qt.Horizontal)

        # Left: 6-tab widget
        left_tabs = QTabWidget()
        self._left_tabs = left_tabs

        # Tab 1: Evidence Threads (enhanced)
        self._thread_table = QTableWidget(0, 6)
        self._thread_table.setHorizontalHeaderLabels(
            ["Quality", "Thread", "Nodes", "Edges", "Source Modules", "Suggested Next Step"]
        )
        self._thread_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._thread_table.setSelectionBehavior(QTableWidget.SelectRows)
        self._thread_table.selectionModel().selectionChanged.connect(self._on_thread_selected)
        left_tabs.addTab(self._thread_table, "Evidence Threads")

        # Tab 2: Crash Reversal Chain (NEW)
        self._crash_table = QTableWidget(0, 5)
        self._crash_table.setHorizontalHeaderLabels(
            ["Stage", "Node", "Evidence Quality", "Risk Context", "Next Step"]
        )
        self._crash_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._crash_table.setSelectionBehavior(QTableWidget.SelectRows)
        self._crash_table.selectionModel().selectionChanged.connect(self._on_crash_row_selected)
        left_tabs.addTab(self._crash_table, "Crash Reversal Chain")

        # Tab 3: Nodes (enhanced)
        self._node_table = QTableWidget(0, 7)
        self._node_table.setHorizontalHeaderLabels(
            ["Node Type", "Title", "Source", "Group", "Confidence", "Orphan", "Gap Tags"]
        )
        self._node_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._node_table.setSelectionBehavior(QTableWidget.SelectRows)
        self._node_table.selectionModel().selectionChanged.connect(self._on_node_selected)
        left_tabs.addTab(self._node_table, "Nodes")

        # Tab 4: Edges (enhanced)
        self._edge_table = QTableWidget(0, 5)
        self._edge_table.setHorizontalHeaderLabels(
            ["Relation", "Source", "Target", "Confidence", "Safety Label"]
        )
        self._edge_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_tabs.addTab(self._edge_table, "Edges")

        # Tab 5: Graph Gaps (NEW)
        self._gaps_table = QTableWidget(0, 5)
        self._gaps_table.setHorizontalHeaderLabels(
            ["Gap Type", "Title", "Severity", "Source", "Suggested Next Step"]
        )
        self._gaps_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._gaps_table.setSelectionBehavior(QTableWidget.SelectRows)
        self._gaps_table.selectionModel().selectionChanged.connect(self._on_gap_selected)
        left_tabs.addTab(self._gaps_table, "Graph Gaps")

        # Tab 6: Detail / Explanation (NEW) — shown in right panel, but also a tab for mobile
        self._detail_tab_text = QTextEdit()
        self._detail_tab_text.setReadOnly(True)
        self._detail_tab_text.setPlaceholderText(
            "Select a node, thread, or gap in any other tab to see explanation here."
        )
        left_tabs.addTab(self._detail_tab_text, "Detail / Explanation")

        splitter.addWidget(left_tabs)

        # Right: Detail panel
        detail_group = QGroupBox("Detail")
        detail_layout = QVBoxLayout(detail_group)
        self._detail_text = QTextEdit()
        self._detail_text.setReadOnly(True)
        self._detail_text.setPlaceholderText("Select a node, thread, or gap to view details…")
        detail_layout.addWidget(self._detail_text)

        # Action buttons in detail panel
        detail_btn_layout = QHBoxLayout()
        self._copy_btn = QPushButton("Copy Suggested Next Step")
        self._copy_btn.clicked.connect(self._on_copy_next_step)
        self._copy_btn.setToolTip(
            "Copies only safe research commands (REVIEW, VALIDATE, BACKTEST_MORE, etc.)"
        )
        self._copy_evidence_btn = QPushButton("Copy Evidence Path")
        self._copy_evidence_btn.clicked.connect(self._copy_evidence_path)
        self._copy_evidence_btn.setToolTip("Copies the evidence path text for the selected item.")

        detail_btn_layout.addWidget(self._copy_btn)
        detail_btn_layout.addWidget(self._copy_evidence_btn)
        detail_layout.addLayout(detail_btn_layout)
        splitter.addWidget(detail_group)

        splitter.setSizes([700, 300])
        main_layout.addWidget(splitter)

        # D. Actions bar
        action_layout = QHBoxLayout()
        self._build_btn   = QPushButton("Build Graph")
        self._report_btn  = QPushButton("Generate Report")
        self._refresh_btn = QPushButton("Refresh")
        self._search_btn  = QPushButton("Search")
        self._status_lbl  = QLabel("Ready")

        self._build_btn.clicked.connect(self._on_build)
        self._report_btn.clicked.connect(self._on_report)
        self._refresh_btn.clicked.connect(self._refresh_from_store)
        self._search_btn.clicked.connect(self._run_search)

        action_layout.addWidget(self._build_btn)
        action_layout.addWidget(self._report_btn)
        action_layout.addWidget(self._refresh_btn)
        action_layout.addWidget(self._search_btn)
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
        # Load gaps and crash threads after build
        self._gaps_data     = self._adapter.load_gaps() if self._adapter else []
        self._crash_threads = self._adapter.get_crash_reversal_threads() if self._adapter else []
        self._update_summary_cards(summary, self._threads_data, self._gaps_data, self._crash_threads)
        self._populate_thread_table(self._threads_data)
        self._populate_crash_reversal_tab(self._crash_threads)
        self._populate_node_table(self._nodes)
        self._populate_edge_table(self._edges)
        self._populate_gaps_tab(self._gaps_data)
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
        self._gaps_data    = self._adapter.load_gaps()
        self._crash_threads = self._adapter.get_crash_reversal_threads()
        summary            = self._adapter.load_latest_summary()
        if _PYSIDE6:
            self._update_summary_cards(summary, self._threads_data, self._gaps_data, self._crash_threads)
            self._populate_thread_table(self._threads_data)
            self._populate_crash_reversal_tab(self._crash_threads)
            self._populate_node_table(self._nodes)
            self._populate_edge_table(self._edges)
            self._populate_gaps_tab(self._gaps_data)
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
        show_orphans  = self._chk_show_orphans.isChecked()
        show_contrads = self._chk_show_contrads.isChecked()
        crash_only    = self._chk_crash_only.isChecked()

        filtered = list(self._nodes)
        if type_filter and type_filter != "All Types":
            filtered = [n for n in filtered if getattr(n, 'node_type', '') == type_filter]
        if module_filter and module_filter != "All Modules":
            filtered = [n for n in filtered if getattr(n, 'source_module', '') == module_filter]
        if keyword:
            filtered = [n for n in filtered
                        if keyword in getattr(n, 'title', '').lower()
                        or keyword in getattr(n, 'summary', '').lower()]
        if show_orphans:
            filtered = [n for n in filtered if getattr(n, 'is_orphan', False)]
        if show_contrads:
            filtered = [n for n in filtered if getattr(n, 'status', '') == 'CONTRADICTED']
        if crash_only:
            filtered = [n for n in filtered
                        if 'crash' in getattr(n, 'title', '').lower()
                        or 'reversal' in getattr(n, 'title', '').lower()]
        self._populate_node_table(filtered)

    def _run_search(self) -> None:
        """Run async search/filter for threads and gaps."""
        if not self._adapter or not _PYSIDE6:
            return
        quality = self._filter_quality.currentText()
        gap_t   = self._filter_gap_type.currentText()
        filters = {
            "keyword":       self._filter_keyword.text() or None,
            "quality_label": quality if quality != "All Quality" else None,
            "source_module": self._filter_module.currentText() if self._filter_module.currentText() != "All Modules" else None,
            "gap_type":      gap_t if gap_t != "All Gap Types" else None,
            "crash_only":    self._chk_crash_only.isChecked(),
        }
        self._status_lbl.setText("Searching…")
        self._search_btn.setEnabled(False)
        self._search_worker = _SearchWorker(self._adapter, filters)
        self._search_worker.finished.connect(self._on_search_done)
        self._search_worker.error.connect(self._on_search_error)
        self._search_worker.start()

    def _on_search_done(self, result: dict) -> None:
        self._search_btn.setEnabled(True)
        threads = result.get("threads", [])
        gaps    = result.get("gaps", [])
        self._populate_thread_table(threads)
        self._populate_gaps_tab(gaps)
        self._status_lbl.setText(
            f"Search done: {len(threads)} threads, {len(gaps)} gaps"
        )

    def _on_search_error(self, msg: str) -> None:
        self._search_btn.setEnabled(True)
        self._status_lbl.setText(f"Search error: {msg[:80]}")

    def _on_node_selected(self) -> None:
        if not _PYSIDE6:
            return
        rows = self._node_table.selectedItems()
        if not rows:
            return
        row = self._node_table.currentRow()
        title_item = self._node_table.item(row, 1)
        if not title_item:
            return
        title = title_item.text()
        found = None
        for n in self._nodes:
            if getattr(n, 'title', '')[:80] == title:
                found = n
                break
        if not found:
            return
        self._current_detail_id = getattr(found, 'node_id', '')
        neighbors = self._adapter.get_neighbors(found.node_id) if self._adapter else []
        detail = self._format_node_detail(found, neighbors)
        self._detail_text.setPlainText(detail)
        self._detail_tab_text.setPlainText(detail)
        # Extract next step from edges
        self._current_next_step = "REVIEW"
        for e in self._edges:
            if getattr(e, 'source_node_id', '') == found.node_id and getattr(e, 'suggested_next_step', ''):
                self._current_next_step = _sanitize_step(e.suggested_next_step)
                break

    def _on_thread_selected(self) -> None:
        if not _PYSIDE6:
            return
        row = self._thread_table.currentRow()
        if row < 0:
            return
        title_item = self._thread_table.item(row, 1)
        if not title_item:
            return
        # Try to find in threads_data
        thread_title = title_item.text()
        found = None
        for t in self._threads_data:
            td = _to_dict(t)
            if td.get("anchor_title", "")[:60] == thread_title or td.get("thread_id", "") == thread_title:
                found = td
                break
        if found is None:
            return
        self._current_detail_id = found.get("thread_id", "")
        step = _sanitize_step(str(found.get("suggested_next_step", "REVIEW")))
        self._current_next_step = step
        detail = self._format_thread_detail(found)
        self._detail_text.setPlainText(detail)
        self._detail_tab_text.setPlainText(detail)

    def _on_crash_row_selected(self) -> None:
        if not _PYSIDE6:
            return
        row = self._crash_table.currentRow()
        if row < 0:
            return
        node_item = self._crash_table.item(row, 1)
        if not node_item:
            return
        node_text = node_item.text()
        # Find thread in crash_threads
        found = None
        for t in self._crash_threads:
            td = _to_dict(t)
            anchor = td.get("anchor_title", "")
            if anchor[:50] == node_text or td.get("thread_id", "") == node_text:
                found = td
                break
        if found:
            self._current_detail_id = found.get("thread_id", "")
            detail = self._format_thread_detail(found)
            self._detail_text.setPlainText(detail)
            self._detail_tab_text.setPlainText(detail)
            self._current_next_step = _sanitize_step(str(found.get("suggested_next_step", "REVIEW")))

    def _on_gap_selected(self) -> None:
        if not _PYSIDE6:
            return
        row = self._gaps_table.currentRow()
        if row < 0:
            return
        title_item = self._gaps_table.item(row, 1)
        if not title_item:
            return
        gap_title = title_item.text()
        found = None
        for g in self._gaps_data:
            gd = _to_dict(g)
            if gd.get("title", "")[:60] == gap_title:
                found = gd
                break
        if found is None:
            return
        self._current_detail_id = found.get("gap_id", "")
        detail = self._format_gap_detail(found)
        self._detail_text.setPlainText(detail)
        self._detail_tab_text.setPlainText(detail)
        self._current_next_step = _sanitize_step(str(found.get("suggested_next_step", "REVIEW")))

    def _on_copy_next_step(self) -> None:
        if not _PYSIDE6:
            return
        safe = _sanitize_step(self._current_next_step) if self._current_next_step else "REVIEW"
        clipboard = QApplication.clipboard()
        clipboard.setText(safe)
        self._status_lbl.setText(f"Copied: {safe}")

    def _copy_evidence_path(self) -> None:
        """Copy evidence path from detail text."""
        if not _PYSIDE6:
            return
        text = self._detail_text.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self._status_lbl.setText("Evidence path copied.")

    def _copy_safe_next_step(self, node_or_thread_id: str = "") -> str:
        """Return safe next step string for an id."""
        if self._adapter and node_or_thread_id:
            step = self._adapter.copy_safe_next_step(node_or_thread_id)
        else:
            step = self._current_next_step or "REVIEW"
        return _sanitize_step(step)

    # ------------------------------------------------------------------
    # Populate tables
    # ------------------------------------------------------------------

    def _update_summary_cards(self, summary, threads, gaps, crash_threads) -> None:
        if not _PYSIDE6:
            return
        thread_count = len(threads) if threads else 0
        gaps_count   = len(gaps)    if gaps    else 0
        crash_count  = len(crash_threads) if crash_threads else 0

        # Count quality labels in threads
        strong_count     = 0
        needs_data_count = 0
        needs_bt_count   = 0
        for t in (threads or []):
            td = _to_dict(t)
            ql = td.get("quality_label", "")
            if ql == "STRONG_EVIDENCE":
                strong_count += 1
            elif ql == "NEEDS_DATA":
                needs_data_count += 1
            elif ql == "NEEDS_BACKTEST":
                needs_bt_count += 1

        if summary is not None:
            self._set_card(self._card_nodes,      str(getattr(summary, 'total_nodes', '—')))
            self._set_card(self._card_edges,      str(getattr(summary, 'total_edges', '—')))
            self._set_card(self._card_orphans,    str(getattr(summary, 'orphan_node_count', '—')))
            self._set_card(self._card_contradicts, str(getattr(summary, 'contradiction_count', '—')))

        self._set_card(self._card_threads,    str(thread_count))
        self._set_card(self._card_strong,     str(strong_count))
        self._set_card(self._card_needs_data, str(needs_data_count))
        self._set_card(self._card_needs_bt,   str(needs_bt_count))
        self._set_card(self._card_crash,      str(crash_count))
        self._set_card(self._card_gaps,       str(gaps_count))

    def _populate_thread_table(self, threads) -> None:
        if not _PYSIDE6:
            return
        self._thread_table.setRowCount(0)
        for t in threads:
            td = _to_dict(t)
            r  = self._thread_table.rowCount()
            self._thread_table.insertRow(r)

            quality = td.get("quality_label", "")
            q_item  = QTableWidgetItem(quality)
            color   = _QUALITY_COLORS.get(quality)
            if color:
                q_item.setForeground(QColor(color))
            self._thread_table.setItem(r, 0, q_item)

            self._thread_table.setItem(r, 1, QTableWidgetItem(td.get("anchor_title", "")[:60]))

            key_nodes = td.get("key_nodes", [])
            if isinstance(key_nodes, list):
                key_nodes_str = str(len(key_nodes))
            else:
                key_nodes_str = str(key_nodes)
            self._thread_table.setItem(r, 2, QTableWidgetItem(key_nodes_str))

            edges_val = td.get("edge_count", td.get("edges", ""))
            self._thread_table.setItem(r, 3, QTableWidgetItem(str(edges_val)))

            mods = td.get("source_modules", td.get("source_module", ""))
            if isinstance(mods, list):
                mods = ", ".join(mods[:3])
            self._thread_table.setItem(r, 4, QTableWidgetItem(str(mods)[:60]))

            step = _sanitize_step(str(td.get("suggested_next_step", "REVIEW")))
            self._thread_table.setItem(r, 5, QTableWidgetItem(step))

    def _populate_crash_reversal_tab(self, crash_threads) -> None:
        if not _PYSIDE6:
            return
        self._crash_table.setRowCount(0)
        if not crash_threads:
            self._crash_table.insertRow(0)
            item = QTableWidgetItem(
                "Run Build Graph first — Crash Reversal evidence chain will appear here"
            )
            item.setForeground(QColor("#888888"))
            self._crash_table.setItem(0, 0, item)
            return
        for i, t in enumerate(crash_threads):
            td = _to_dict(t)
            r  = self._crash_table.rowCount()
            self._crash_table.insertRow(r)
            self._crash_table.setItem(r, 0, QTableWidgetItem(str(i + 1)))
            self._crash_table.setItem(r, 1, QTableWidgetItem(td.get("anchor_title", "")[:50]))
            quality = td.get("quality_label", "")
            q_item  = QTableWidgetItem(quality)
            color   = _QUALITY_COLORS.get(quality)
            if color:
                q_item.setForeground(QColor(color))
            self._crash_table.setItem(r, 2, q_item)
            risk_ctx = td.get("risk_context", td.get("summary", ""))
            self._crash_table.setItem(r, 3, QTableWidgetItem(str(risk_ctx)[:60]))
            step = _sanitize_step(str(td.get("suggested_next_step", "REVIEW")))
            self._crash_table.setItem(r, 4, QTableWidgetItem(step))

    def _populate_node_table(self, nodes) -> None:
        if not _PYSIDE6:
            return
        self._node_table.setRowCount(0)
        for n in nodes:
            r = self._node_table.rowCount()
            self._node_table.insertRow(r)
            self._node_table.setItem(r, 0, QTableWidgetItem(getattr(n, 'node_type', '')))
            self._node_table.setItem(r, 1, QTableWidgetItem(getattr(n, 'title', '')[:80]))
            self._node_table.setItem(r, 2, QTableWidgetItem(getattr(n, 'source_module', '')))
            self._node_table.setItem(r, 3, QTableWidgetItem(
                getattr(n, 'group', getattr(n, 'priority', ''))
            ))
            conf = getattr(n, 'confidence', 0.0)
            self._node_table.setItem(r, 4, QTableWidgetItem(f"{conf:.2f}"))
            is_orphan = getattr(n, 'is_orphan', False)
            self._node_table.setItem(r, 5, QTableWidgetItem("Yes" if is_orphan else "No"))
            gap_tags = getattr(n, 'gap_tags', getattr(n, 'tags', []))
            if isinstance(gap_tags, list):
                gap_tags = ", ".join(gap_tags[:3])
            self._node_table.setItem(r, 6, QTableWidgetItem(str(gap_tags)))

    def _populate_edge_table(self, edges) -> None:
        if not _PYSIDE6:
            return
        self._edge_table.setRowCount(0)
        for e in edges:
            r = self._edge_table.rowCount()
            self._edge_table.insertRow(r)
            self._edge_table.setItem(r, 0, QTableWidgetItem(getattr(e, 'relation_type', '')))
            self._edge_table.setItem(r, 1, QTableWidgetItem(getattr(e, 'source_node_id', '')[:20]))
            self._edge_table.setItem(r, 2, QTableWidgetItem(getattr(e, 'target_node_id', '')[:20]))
            conf = getattr(e, 'confidence', 0.0)
            self._edge_table.setItem(r, 3, QTableWidgetItem(f"{conf:.2f}"))
            # Safety label — show sanitized step or safety annotation
            safety = getattr(e, 'safety_label', getattr(e, 'suggested_next_step', ''))
            if safety:
                safety = _sanitize_step(str(safety))
            self._edge_table.setItem(r, 4, QTableWidgetItem(safety))

    def _populate_gaps_tab(self, gaps) -> None:
        if not _PYSIDE6:
            return
        self._gaps_table.setRowCount(0)
        if not gaps:
            self._gaps_table.insertRow(0)
            item = QTableWidgetItem("No graph gaps found.")
            item.setForeground(QColor("#888888"))
            self._gaps_table.setItem(0, 0, item)
            return
        for g in gaps:
            gd = _to_dict(g)
            r  = self._gaps_table.rowCount()
            self._gaps_table.insertRow(r)
            self._gaps_table.setItem(r, 0, QTableWidgetItem(gd.get("gap_type", "")))
            self._gaps_table.setItem(r, 1, QTableWidgetItem(gd.get("title", "")[:60]))
            severity = gd.get("severity", "")
            sev_item = QTableWidgetItem(severity)
            sev_color = _SEVERITY_COLORS.get(severity.upper() if severity else "")
            if sev_color:
                sev_item.setForeground(QColor(sev_color))
            self._gaps_table.setItem(r, 2, sev_item)
            self._gaps_table.setItem(r, 3, QTableWidgetItem(gd.get("source_module", gd.get("source", ""))[:40]))
            step = _sanitize_step(str(gd.get("suggested_next_step", "REVIEW")))
            self._gaps_table.setItem(r, 4, QTableWidgetItem(step))

    # ------------------------------------------------------------------
    # Detail formatters
    # ------------------------------------------------------------------

    def _show_detail(self, text: str) -> None:
        """Show text in both detail panel and detail tab."""
        if _PYSIDE6:
            self._detail_text.setPlainText(text)
            self._detail_tab_text.setPlainText(text)

    def _format_node_detail(self, node, neighbors) -> str:
        lines = [
            "=== Node Detail ===",
            f"ID:      {getattr(node, 'node_id', '')}",
            f"Type:    {getattr(node, 'node_type', '')}",
            f"Title:   {getattr(node, 'title', '')}",
            f"Source:  {getattr(node, 'source_module', '')} / {getattr(node, 'source_ref', '')}",
            f"Status:  {getattr(node, 'status', '')}",
            f"Conf:    {getattr(node, 'confidence', 0.0):.2f}",
            f"Group:   {getattr(node, 'group', getattr(node, 'priority', ''))}",
            f"Orphan:  {'Yes' if getattr(node, 'is_orphan', False) else 'No'}",
            "",
            "Summary:",
            f"{getattr(node, 'summary', '')}",
            "",
        ]
        ev = getattr(node, 'evidence_text', '')
        if ev:
            lines += ["Evidence:", ev, ""]
        syms = getattr(node, 'related_symbols', [])
        if syms:
            lines += [f"Symbols: {', '.join(syms)}"]
        strats = getattr(node, 'related_strategies', [])
        if strats:
            lines += [f"Strategies: {', '.join(strats)}"]
        gap_tags = getattr(node, 'gap_tags', getattr(node, 'tags', []))
        if gap_tags:
            if isinstance(gap_tags, list):
                gap_tags = ", ".join(gap_tags)
            lines += [f"Gap Tags: {gap_tags}"]
        if neighbors:
            lines += ["", f"Neighbors ({len(neighbors)}):"]
            for nb in neighbors[:5]:
                lines += [f"  - [{getattr(nb, 'node_type', '')}] {getattr(nb, 'title', '')[:60]}"]
        lines += [
            "",
            "Why this node exists: evidence collected by source module during graph build.",
            "What to do next (safe only): see Suggested Next Step.",
            "",
            "[!] Research Only. No Real Orders. Production Trading BLOCKED.",
            "[!] Not Investment Advice.",
        ]
        return "\n".join(lines)

    def _format_thread_detail(self, td: dict) -> str:
        step = _sanitize_step(str(td.get("suggested_next_step", "REVIEW")))
        key_nodes = td.get("key_nodes", [])
        if isinstance(key_nodes, list):
            key_nodes_str = "\n".join(f"  - {k}" for k in key_nodes[:10])
        else:
            key_nodes_str = str(key_nodes)
        lines = [
            "=== Evidence Thread ===",
            f"ID:           {td.get('thread_id', '')}",
            f"Anchor:       {td.get('anchor_title', '')}",
            f"Quality:      {td.get('quality_label', '')}",
            f"Source Mods:  {td.get('source_modules', td.get('source_module', ''))}",
            "",
            "Key Nodes:",
            key_nodes_str,
            "",
            f"Evidence Path: {td.get('evidence_path', '')}",
            "",
            f"Summary: {td.get('summary', '')}",
            "",
            f"Suggested Next Step (safe): {step}",
            "",
            "[!] Research Only. No Real Orders. Production Trading BLOCKED.",
            "[!] Not Investment Advice.",
        ]
        return "\n".join(lines)

    def _format_gap_detail(self, gd: dict) -> str:
        step = _sanitize_step(str(gd.get("suggested_next_step", "REVIEW")))
        lines = [
            "=== Graph Gap ===",
            f"Gap ID:    {gd.get('gap_id', '')}",
            f"Type:      {gd.get('gap_type', '')}",
            f"Title:     {gd.get('title', '')}",
            f"Severity:  {gd.get('severity', '')}",
            f"Source:    {gd.get('source_module', gd.get('source', ''))}",
            "",
            f"Description: {gd.get('description', gd.get('summary', ''))}",
            "",
            f"Suggested Next Step (safe): {step}",
            "",
            "[!] Research Only. No Real Orders. Production Trading BLOCKED.",
            "[!] Not Investment Advice.",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def closeEvent(self, event) -> None:
        """Clean up QThreads on close to avoid QThread destroyed warning."""
        for worker in (self._worker, self._rep_worker, self._search_worker):
            if worker is not None and _PYSIDE6:
                try:
                    worker.quit()
                    worker.wait(2000)
                except Exception:
                    pass
        if _PYSIDE6:
            super().closeEvent(event)
