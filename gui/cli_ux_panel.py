"""
gui/cli_ux_panel.py — CLIUXPanel for TW Quant Cockpit v0.5.1.

PySide6 GUI panel for CLI Alias / Command UX Polish.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No broker connection. No order execution. Display only.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView,
        QTabWidget, QTextEdit, QFrame, QLineEdit, QMessageBox,
        QSizePolicy,
    )
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Stub when PySide6 is unavailable
# ---------------------------------------------------------------------------

if not _PYSIDE6_AVAILABLE:
    class CLIUXPanel:  # type: ignore
        """Stub CLIUXPanel when PySide6 is not available."""

        read_only:          bool = True
        no_real_orders:     bool = True
        production_blocked: bool = True
        real_order_ready:   bool = False

else:
    # -----------------------------------------------------------------------
    # Background workers
    # -----------------------------------------------------------------------

    class _RegistryWorker(QThread):
        finished = Signal(list)
        error    = Signal(str)

        def run(self):
            try:
                from gui.cli_ux_adapter import CLIUXAdapter
                data = CLIUXAdapter().build_registry()
                self.finished.emit(data)
            except Exception as exc:
                self.error.emit(str(exc))

    class _AliasWorker(QThread):
        finished = Signal(list)
        error    = Signal(str)

        def run(self):
            try:
                from gui.cli_ux_adapter import CLIUXAdapter
                data = CLIUXAdapter().build_alias_map()
                self.finished.emit(data)
            except Exception as exc:
                self.error.emit(str(exc))

    class _SummaryWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def run(self):
            try:
                from gui.cli_ux_adapter import CLIUXAdapter
                data = CLIUXAdapter().load_latest_summary()
                self.finished.emit(data)
            except Exception as exc:
                self.error.emit(str(exc))

    class _ReportWorker(QThread):
        finished = Signal(str)
        error    = Signal(str)

        def __init__(self, mode: str = "real"):
            super().__init__()
            self._mode = mode

        def run(self):
            try:
                from gui.cli_ux_adapter import CLIUXAdapter
                path = CLIUXAdapter().generate_report(mode=self._mode)
                self.finished.emit(path or "")
            except Exception as exc:
                self.error.emit(str(exc))

    class _ExamplesWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def run(self):
            try:
                from gui.cli_ux_adapter import CLIUXAdapter
                data = CLIUXAdapter().get_all_examples()
                self.finished.emit(data)
            except Exception as exc:
                self.error.emit(str(exc))

    # -----------------------------------------------------------------------
    # Main panel
    # -----------------------------------------------------------------------

    class CLIUXPanel(QWidget):
        """
        CLI Alias / Command UX Polish panel for TW Quant Cockpit v0.5.1.

        Sections:
          A. Header / Safety Banner
          B. Summary Cards row
          C. Tab widget:
               1. Command Registry  — table of all commands
               2. Alias Map         — table of all aliases
               3. Help Examples     — usage examples by group
               4. Search/Discovery  — keyword search UI
               5. Audit Log         — text log of last audit
          D. Action buttons: Refresh, Generate Report, Open Latest Report

        Safety:
          No real orders. No broker. No execution.
          All data is read-only research output.
        """

        read_only:          bool = True
        no_real_orders:     bool = True
        production_blocked: bool = True
        real_order_ready:   bool = False

        def __init__(self, parent=None) -> None:
            super().__init__(parent)
            self._registry_worker:  _RegistryWorker  = None
            self._alias_worker:     _AliasWorker     = None
            self._summary_worker:   _SummaryWorker   = None
            self._report_worker:    _ReportWorker    = None
            self._examples_worker:  _ExamplesWorker  = None
            self._last_summary: dict = {}
            self._setup_ui()

        # ------------------------------------------------------------------
        # UI setup
        # ------------------------------------------------------------------

        def _setup_ui(self) -> None:
            layout = QVBoxLayout(self)
            layout.setSpacing(6)
            layout.setContentsMargins(8, 8, 8, 8)

            # A. Safety banner
            layout.addWidget(self._make_safety_banner())

            # B. Summary cards
            self._summary_layout = self._make_summary_bar()
            layout.addLayout(self._summary_layout)

            # C. Tab widget
            self._tabs = QTabWidget()
            self._tabs.setTabPosition(QTabWidget.North)

            # Tab 1: Command Registry
            self._registry_table = self._make_table([
                "Command", "Category", "Purpose", "Aliases", "Safety", "Legacy",
            ])
            self._tabs.addTab(self._registry_table, "Command Registry")

            # Tab 2: Alias Map
            self._alias_table = self._make_table([
                "Alias", "Target", "Category", "Enabled", "Conflict", "Safety",
            ])
            self._tabs.addTab(self._alias_table, "Alias Map")

            # Tab 3: Help Examples
            self._examples_table = self._make_table([
                "Category", "Example", "Notes",
            ])
            self._tabs.addTab(self._examples_table, "Help Examples")

            # Tab 4: Search / Discovery
            search_widget = self._make_search_tab()
            self._tabs.addTab(search_widget, "Search / Discovery")

            # Tab 5: Audit Log
            self._audit_log = QTextEdit()
            self._audit_log.setReadOnly(True)
            self._audit_log.setPlaceholderText(
                "CLI UX audit log will appear here after refresh…"
            )
            self._audit_log.setStyleSheet("background:#0d1117; color:#c9d1d9; font-family:monospace;")
            self._tabs.addTab(self._audit_log, "Audit Log")

            layout.addWidget(self._tabs)

            # D. Action buttons
            layout.addLayout(self._make_button_bar())

        def _make_safety_banner(self) -> QLabel:
            banner = QLabel(
                "[!] CLI UX Polish  v0.5.1   |   Research Only   |   "
                "No Real Orders   |   Production Trading: BLOCKED"
            )
            banner.setAlignment(Qt.AlignCenter)
            banner.setStyleSheet(
                "background:#1e3a5f; color:white; font-weight:bold; "
                "padding:6px; border-radius:4px;"
            )
            return banner

        def _make_summary_bar(self) -> QHBoxLayout:
            bar = QHBoxLayout()
            self._card_commands  = self._make_card("Commands",       "—")
            self._card_aliases   = self._make_card("Aliases",        "—")
            self._card_categories = self._make_card("Categories",    "—")
            self._card_conflicts = self._make_card("Conflicts",      "—")
            self._card_missing   = self._make_card("Missing Examples", "—")
            self._card_safety    = self._make_card("Safety Status",  "—")
            for card in (
                self._card_commands, self._card_aliases, self._card_categories,
                self._card_conflicts, self._card_missing, self._card_safety,
            ):
                bar.addWidget(card)
            return bar

        def _make_card(self, label: str, value: str) -> QFrame:
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setStyleSheet("background:#1e1e2e; border-radius:4px; padding:4px;")
            v = QVBoxLayout(frame)
            v.setSpacing(2)
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color:#a0a0c0; font-size:10px;")
            val = QLabel(value)
            val.setAlignment(Qt.AlignCenter)
            val.setStyleSheet("color:#e0e0ff; font-size:14px; font-weight:bold;")
            val.setObjectName(f"card_{label.lower().replace(' ', '_')}")
            v.addWidget(lbl)
            v.addWidget(val)
            return frame

        def _make_table(self, headers: list) -> QTableWidget:
            table = QTableWidget(0, len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.horizontalHeader().setStretchLastSection(True)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectRows)
            table.setAlternatingRowColors(True)
            table.setStyleSheet(
                "QTableWidget { background:#0d1117; color:#c9d1d9; gridline-color:#30363d; }"
                "QHeaderView::section { background:#161b22; color:#8b949e; font-weight:bold; }"
                "QTableWidget::item:alternate { background:#161b22; }"
            )
            return table

        def _make_search_tab(self) -> QWidget:
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setSpacing(6)

            # Search bar
            search_bar = QHBoxLayout()
            self._search_input = QLineEdit()
            self._search_input.setPlaceholderText("Enter keyword to search commands…")
            self._search_input.setStyleSheet(
                "background:#161b22; color:#c9d1d9; border:1px solid #30363d; "
                "border-radius:4px; padding:4px;"
            )
            self._btn_search = QPushButton("Search")
            self._btn_search.setStyleSheet(
                "background:#1f6feb; color:white; font-weight:bold; "
                "border-radius:4px; padding:4px 12px;"
            )
            self._btn_search.clicked.connect(self._on_search)
            self._search_input.returnPressed.connect(self._on_search)
            search_bar.addWidget(self._search_input)
            search_bar.addWidget(self._btn_search)
            layout.addLayout(search_bar)

            # Results table
            self._search_table = self._make_table([
                "Command", "Category", "Purpose", "Aliases",
            ])
            layout.addWidget(self._search_table)
            return widget

        def _make_button_bar(self) -> QHBoxLayout:
            bar = QHBoxLayout()
            self._btn_refresh = QPushButton("Refresh")
            self._btn_report  = QPushButton("Generate Report")
            self._btn_open    = QPushButton("Open Latest Report")
            self._lbl_status  = QLabel("Ready")
            self._lbl_status.setStyleSheet("color:#8b949e; font-size:11px;")

            for btn in (self._btn_refresh, self._btn_report, self._btn_open):
                btn.setStyleSheet(
                    "background:#21262d; color:#c9d1d9; border:1px solid #30363d; "
                    "border-radius:4px; padding:4px 10px;"
                )

            self._btn_refresh.clicked.connect(self._on_refresh)
            self._btn_report.clicked.connect(self._on_generate_report)
            self._btn_open.clicked.connect(self._on_open_latest_report)

            bar.addWidget(self._btn_refresh)
            bar.addWidget(self._btn_report)
            bar.addWidget(self._btn_open)
            bar.addStretch()
            bar.addWidget(self._lbl_status)
            return bar

        # ------------------------------------------------------------------
        # Actions
        # ------------------------------------------------------------------

        def _on_refresh(self) -> None:
            self._set_status("Refreshing…")
            self._load_summary()
            self._load_registry()
            self._load_aliases()
            self._load_examples()

        def _on_generate_report(self) -> None:
            self._set_status("Generating report…")
            self._btn_report.setEnabled(False)
            self._report_worker = _ReportWorker(mode="real")
            self._report_worker.finished.connect(self._on_report_done)
            self._report_worker.error.connect(self._on_worker_error)
            self._report_worker.start()

        def _on_open_latest_report(self) -> None:
            try:
                from gui.cli_ux_adapter import CLIUXAdapter
                path = CLIUXAdapter().load_latest_report_path()
                if path and os.path.exists(path):
                    import subprocess, sys
                    if sys.platform.startswith("win"):
                        os.startfile(path)  # type: ignore[attr-defined]
                    else:
                        subprocess.Popen(["xdg-open", path])
                    self._set_status(f"Opened: {os.path.basename(path)}")
                else:
                    self._set_status("No report found. Generate one first.")
            except Exception as exc:
                self._set_status(f"Error: {exc}")

        def _on_search(self) -> None:
            keyword = self._search_input.text().strip()
            if not keyword:
                return
            try:
                from gui.cli_ux_adapter import CLIUXAdapter
                results = CLIUXAdapter().search_commands(keyword)
                self._populate_search_table(results)
                self._set_status(f"Search '{keyword}': {len(results)} results")
            except Exception as exc:
                self._set_status(f"Search error: {exc}")

        # ------------------------------------------------------------------
        # Data loaders
        # ------------------------------------------------------------------

        def _load_summary(self) -> None:
            self._summary_worker = _SummaryWorker()
            self._summary_worker.finished.connect(self._on_summary_loaded)
            self._summary_worker.error.connect(self._on_worker_error)
            self._summary_worker.start()

        def _load_registry(self) -> None:
            self._registry_worker = _RegistryWorker()
            self._registry_worker.finished.connect(self._on_registry_loaded)
            self._registry_worker.error.connect(self._on_worker_error)
            self._registry_worker.start()

        def _load_aliases(self) -> None:
            self._alias_worker = _AliasWorker()
            self._alias_worker.finished.connect(self._on_aliases_loaded)
            self._alias_worker.error.connect(self._on_worker_error)
            self._alias_worker.start()

        def _load_examples(self) -> None:
            self._examples_worker = _ExamplesWorker()
            self._examples_worker.finished.connect(self._on_examples_loaded)
            self._examples_worker.error.connect(self._on_worker_error)
            self._examples_worker.start()

        # ------------------------------------------------------------------
        # Callbacks
        # ------------------------------------------------------------------

        def _on_summary_loaded(self, data: dict) -> None:
            self._last_summary = data
            self._update_cards(data)
            self._update_audit_log(data)
            self._set_status("Summary loaded.")

        def _on_registry_loaded(self, rows: list) -> None:
            table = self._registry_table
            table.setRowCount(0)
            for row in rows:
                r = table.rowCount()
                table.insertRow(r)
                table.setItem(r, 0, QTableWidgetItem(row.get("name", "")))
                table.setItem(r, 1, QTableWidgetItem(row.get("category", "")))
                table.setItem(r, 2, QTableWidgetItem(row.get("purpose", "")))
                table.setItem(r, 3, QTableWidgetItem(row.get("aliases", "")))
                table.setItem(r, 4, QTableWidgetItem(row.get("safety_level", "")))
                table.setItem(r, 5, QTableWidgetItem(
                    "Legacy" if row.get("legacy") else ""
                ))
            self._set_status(f"Registry: {len(rows)} commands loaded.")

        def _on_aliases_loaded(self, rows: list) -> None:
            table = self._alias_table
            table.setRowCount(0)
            for row in rows:
                r = table.rowCount()
                table.insertRow(r)
                table.setItem(r, 0, QTableWidgetItem(row.get("alias", "")))
                table.setItem(r, 1, QTableWidgetItem(row.get("target_command", "")))
                table.setItem(r, 2, QTableWidgetItem(row.get("category", "")))
                table.setItem(r, 3, QTableWidgetItem(
                    "✓" if row.get("enabled") else "✗"
                ))
                table.setItem(r, 4, QTableWidgetItem(
                    "⚠" if row.get("conflict") else "—"
                ))
                table.setItem(r, 5, QTableWidgetItem(row.get("safety_level", "")))
            self._set_status(f"Alias map: {len(rows)} aliases loaded.")

        def _on_examples_loaded(self, data: dict) -> None:
            table = self._examples_table
            table.setRowCount(0)
            for category, examples in data.items():
                for ex in examples:
                    r = table.rowCount()
                    table.insertRow(r)
                    table.setItem(r, 0, QTableWidgetItem(category))
                    table.setItem(r, 1, QTableWidgetItem(ex.get("example", "")))
                    table.setItem(r, 2, QTableWidgetItem(ex.get("notes", "")))
            self._set_status("Examples loaded.")

        def _on_report_done(self, path: str) -> None:
            self._btn_report.setEnabled(True)
            if path:
                self._set_status(f"Report: {os.path.basename(path)}")
                self._audit_log.append(f"[Report] Generated: {path}")
            else:
                self._set_status("Report generation failed.")
            self._load_summary()

        def _on_worker_error(self, msg: str) -> None:
            logger.error("CLIUXPanel worker error: %s", msg)
            self._btn_report.setEnabled(True)
            self._set_status(f"Error: {msg}")
            self._audit_log.append(f"[Error] {msg}")

        def _populate_search_table(self, results: list) -> None:
            table = self._search_table
            table.setRowCount(0)
            for row in results:
                r = table.rowCount()
                table.insertRow(r)
                table.setItem(r, 0, QTableWidgetItem(row.get("command", "")))
                table.setItem(r, 1, QTableWidgetItem(row.get("category", "")))
                table.setItem(r, 2, QTableWidgetItem(row.get("purpose", "")))
                table.setItem(r, 3, QTableWidgetItem(row.get("aliases", "")))

        # ------------------------------------------------------------------
        # UI helpers
        # ------------------------------------------------------------------

        def _update_cards(self, data: dict) -> None:
            def _find_card_val(frame: QFrame) -> QLabel:
                for child in frame.findChildren(QLabel):
                    if child.objectName().startswith("card_"):
                        return child
                return frame.findChildren(QLabel)[-1]

            _find_card_val(self._card_commands).setText(
                str(data.get("commands_count", "—"))
            )
            _find_card_val(self._card_aliases).setText(
                str(data.get("alias_count", "—"))
            )
            _find_card_val(self._card_categories).setText(
                str(data.get("categories_count", "—"))
            )
            _find_card_val(self._card_conflicts).setText(
                str(data.get("conflict_count", "—"))
            )
            _find_card_val(self._card_missing).setText(
                str(data.get("missing_examples_count", "—"))
            )
            safety = data.get("safety_status", "—")
            val_lbl = _find_card_val(self._card_safety)
            val_lbl.setText(safety)
            val_lbl.setStyleSheet(
                "color:#3fb950; font-size:14px; font-weight:bold;"
                if safety == "PASS"
                else "color:#f85149; font-size:14px; font-weight:bold;"
            )

        def _update_audit_log(self, data: dict) -> None:
            lines = [
                "=== CLI UX Audit Summary ===",
                f"Commands    : {data.get('commands_count', '?')}",
                f"Aliases     : {data.get('alias_count', '?')}",
                f"Categories  : {data.get('categories_count', '?')}",
                f"Conflicts   : {data.get('conflict_count', '?')}",
                f"Missing Ex. : {data.get('missing_examples_count', '?')}",
                f"Safety      : {data.get('safety_status', '?')}",
                f"read_only          = {data.get('read_only', True)}",
                f"no_real_orders     = {data.get('no_real_orders', True)}",
                f"production_blocked = {data.get('production_blocked', True)}",
                "",
                "By Category:",
            ]
            for cat, count in sorted(data.get("by_category", {}).items()):
                lines.append(f"  {cat:<22} {count:>3} commands")
            self._audit_log.setPlainText("\n".join(lines))

        def _set_status(self, msg: str) -> None:
            self._lbl_status.setText(msg)
