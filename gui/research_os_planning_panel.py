"""
gui/research_os_planning_panel.py — Research OS Planning GUI panel (v0.5.0).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations
import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit,
        QGroupBox, QSplitter, QHeaderView, QFrame,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QFont, QColor
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

if _PYSIDE6_AVAILABLE:

    class _OSAuditWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def run(self):
            try:
                from gui.research_os_planning_adapter import ResearchOSPlanningAdapter
                adapter = ResearchOSPlanningAdapter()
                result  = adapter.run_audit()
                self.finished.emit(result)
            except Exception as exc:  # noqa: BLE001
                self.error.emit(str(exc))

    class _OSReportWorker(QThread):
        finished = Signal(str)
        error    = Signal(str)

        def __init__(self, mode: str = "real"):
            super().__init__()
            self.mode = mode

        def run(self):
            try:
                from gui.research_os_planning_adapter import ResearchOSPlanningAdapter
                adapter = ResearchOSPlanningAdapter()
                path    = adapter.generate_report(mode=self.mode)
                self.finished.emit(path or "")
            except Exception as exc:  # noqa: BLE001
                self.error.emit(str(exc))

    class ResearchOSPlanningPanel(QWidget):
        """Research OS Planning & Stabilization panel for v0.5.0."""

        read_only          = True
        no_real_orders     = True
        production_blocked = True
        real_order_ready   = False

        def __init__(self, parent=None):
            super().__init__(parent)
            self._setup_ui()

        # --------------------------------------------------------------
        def _setup_ui(self):
            root = QVBoxLayout(self)
            root.setContentsMargins(8, 8, 8, 8)

            # Safety banner
            banner = QLabel(
                "[!] Research Only | No Real Orders | Production BLOCKED | "
                "real_order_ready=False | v0.5.0 Research OS Planning"
            )
            banner.setStyleSheet(
                "background:#1a1a2e; color:#e94560; font-weight:bold; padding:6px;"
            )
            banner.setAlignment(Qt.AlignCenter)
            root.addWidget(banner)

            # Summary cards row
            cards_box = QGroupBox("OS Inventory Summary")
            cards_layout = QHBoxLayout(cards_box)
            self._lbl_modules   = self._make_card("Modules",   "—")
            self._lbl_cli       = self._make_card("CLI Cmds",  "—")
            self._lbl_gui_tabs  = self._make_card("GUI Tabs",  "—")
            self._lbl_coverage  = self._make_card("Reg. Cov.", "—")
            self._lbl_safety    = self._make_card("Safety",    "—")
            for card in (self._lbl_modules, self._lbl_cli, self._lbl_gui_tabs,
                         self._lbl_coverage, self._lbl_safety):
                cards_layout.addWidget(card)
            root.addWidget(cards_box)

            # Controls
            ctrl_layout = QHBoxLayout()
            self._btn_audit   = QPushButton("Run OS Audit")
            self._btn_report  = QPushButton("Generate Report")
            self._btn_refresh = QPushButton("Refresh Summary")
            self._lbl_status  = QLabel("Ready.")
            self._btn_audit.clicked.connect(self._on_run_audit)
            self._btn_report.clicked.connect(self._on_generate_report)
            self._btn_refresh.clicked.connect(self._on_refresh)
            for btn in (self._btn_audit, self._btn_report, self._btn_refresh):
                ctrl_layout.addWidget(btn)
            ctrl_layout.addWidget(self._lbl_status)
            ctrl_layout.addStretch()
            root.addLayout(ctrl_layout)

            # Tab widget for detailed views
            tabs = QTabWidget()

            # Module inventory tab
            self._module_table = self._make_table(
                ["Module", "Package", "Category", "Maturity", "CLI", "GUI", "Report"]
            )
            tabs.addTab(self._module_table, "Modules")

            # CLI inventory tab
            self._cli_table = self._make_table(
                ["Command", "Category", "Help"]
            )
            tabs.addTab(self._cli_table, "CLI Commands")

            # GUI tab inventory
            self._gui_table = self._make_table(
                ["Tab Name", "Group", "Panel Class", "Version"]
            )
            tabs.addTab(self._gui_table, "GUI Tabs")

            # Regression audit tab
            self._reg_table = self._make_table(
                ["Module", "Command Test", "Import Test", "GUI Test", "Report Test", "Safety Test", "Status"]
            )
            tabs.addTab(self._reg_table, "Regression Audit")

            # Safety matrix tab
            self._safety_table = self._make_table(
                ["Module", "read_only", "no_real_orders", "prod_blocked", "real_order_ready", "Compliant"]
            )
            tabs.addTab(self._safety_table, "Safety Matrix")

            # Report log tab
            self._report_log = QTextEdit()
            self._report_log.setReadOnly(True)
            self._report_log.setPlaceholderText(
                "Click 'Run OS Audit' or 'Generate Report' to populate this log."
            )
            self._report_log.setFont(QFont("Courier New", 9))
            tabs.addTab(self._report_log, "Audit Log")

            root.addWidget(tabs)

            # Try to load cached summary on open
            self._on_refresh()

        # --------------------------------------------------------------
        def _make_card(self, title: str, value: str) -> QGroupBox:
            box = QGroupBox(title)
            lay = QVBoxLayout(box)
            lbl = QLabel(value)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(QFont("Arial", 14, QFont.Bold))
            lay.addWidget(lbl)
            box._value_label = lbl  # type: ignore[attr-defined]
            return box

        def _set_card(self, card: QGroupBox, value: str):
            card._value_label.setText(value)  # type: ignore[attr-defined]

        def _make_table(self, headers: list[str]) -> QTableWidget:
            tbl = QTableWidget(0, len(headers))
            tbl.setHorizontalHeaderLabels(headers)
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tbl.setEditTriggers(QTableWidget.NoEditTriggers)
            tbl.setSelectionBehavior(QTableWidget.SelectRows)
            return tbl

        # --------------------------------------------------------------
        def _on_run_audit(self):
            self._lbl_status.setText("Running OS audit...")
            self._btn_audit.setEnabled(False)
            self._worker = _OSAuditWorker()
            self._worker.finished.connect(self._on_audit_done)
            self._worker.error.connect(self._on_error)
            self._worker.start()

        def _on_generate_report(self):
            self._lbl_status.setText("Generating report...")
            self._btn_report.setEnabled(False)
            self._rpt_worker = _OSReportWorker(mode="real")
            self._rpt_worker.finished.connect(self._on_report_done)
            self._rpt_worker.error.connect(self._on_error)
            self._rpt_worker.start()

        def _on_refresh(self):
            try:
                from gui.research_os_planning_adapter import ResearchOSPlanningAdapter
                adapter  = ResearchOSPlanningAdapter()
                summary  = adapter.load_latest_summary()
                if summary:
                    self._populate_summary_cards(summary)
                    self._lbl_status.setText("Summary loaded from cache.")
            except Exception as exc:  # noqa: BLE001
                self._lbl_status.setText(f"Refresh: {exc}")

        # --------------------------------------------------------------
        def _on_audit_done(self, result: dict):
            self._btn_audit.setEnabled(True)
            self._lbl_status.setText("Audit complete.")
            self._populate_summary_cards(result)
            self._populate_module_table(result.get("modules", []))
            self._populate_cli_table(result.get("cli_commands", []))
            self._populate_gui_table(result.get("gui_tabs", []))
            self._populate_reg_table(result.get("regression_rows", []))
            self._populate_safety_table(result.get("safety_rows", []))
            self._report_log.append("[Audit complete]")
            for k, v in result.items():
                if not isinstance(v, list):
                    self._report_log.append(f"  {k}: {v}")

        def _on_report_done(self, path: str):
            self._btn_report.setEnabled(True)
            msg = f"Report generated: {path}" if path else "Report generation returned no path."
            self._lbl_status.setText(msg)
            self._report_log.append(msg)

        def _on_error(self, msg: str):
            self._btn_audit.setEnabled(True)
            self._btn_report.setEnabled(True)
            self._lbl_status.setText(f"Error: {msg}")
            self._report_log.append(f"[ERROR] {msg}")

        # --------------------------------------------------------------
        def _populate_summary_cards(self, data: dict):
            self._set_card(self._lbl_modules,  str(data.get("total_modules",  "—")))
            self._set_card(self._lbl_cli,       str(data.get("total_commands", "—")))
            self._set_card(self._lbl_gui_tabs,  str(data.get("total_tabs",    "—")))
            cov = data.get("coverage_score", data.get("regression_coverage", "—"))
            self._set_card(self._lbl_coverage, str(cov))
            safe = data.get("safety_score", data.get("safety_compliant", "—"))
            self._set_card(self._lbl_safety, str(safe))

        def _populate_module_table(self, rows: list[dict]):
            self._module_table.setRowCount(0)
            for row in rows:
                r = self._module_table.rowCount()
                self._module_table.insertRow(r)
                vals = [
                    row.get("module_name", ""),
                    row.get("package",     ""),
                    row.get("category",    ""),
                    row.get("maturity",    ""),
                    "Y" if row.get("cli_commands") else "—",
                    "Y" if row.get("gui_tab")      else "—",
                    "Y" if row.get("report")       else "—",
                ]
                for c, v in enumerate(vals):
                    self._module_table.setItem(r, c, QTableWidgetItem(str(v)))

        def _populate_cli_table(self, rows: list[dict]):
            self._cli_table.setRowCount(0)
            for row in rows:
                r = self._cli_table.rowCount()
                self._cli_table.insertRow(r)
                vals = [
                    row.get("command",  ""),
                    row.get("category", ""),
                    row.get("help",     ""),
                ]
                for c, v in enumerate(vals):
                    self._cli_table.setItem(r, c, QTableWidgetItem(str(v)))

        def _populate_gui_table(self, rows: list[dict]):
            self._gui_table.setRowCount(0)
            for row in rows:
                r = self._gui_table.rowCount()
                self._gui_table.insertRow(r)
                vals = [
                    row.get("tab_name",    ""),
                    row.get("group",       ""),
                    row.get("panel_class", ""),
                    row.get("version",     ""),
                ]
                for c, v in enumerate(vals):
                    self._gui_table.setItem(r, c, QTableWidgetItem(str(v)))

        def _populate_reg_table(self, rows: list[dict]):
            self._reg_table.setRowCount(0)
            for row in rows:
                r = self._reg_table.rowCount()
                self._reg_table.insertRow(r)
                vals = [
                    row.get("module",      ""),
                    row.get("cmd_test",    ""),
                    row.get("import_test", ""),
                    row.get("gui_test",    ""),
                    row.get("report_test", ""),
                    row.get("safety_test", ""),
                    row.get("status",      ""),
                ]
                for c, v in enumerate(vals):
                    item = QTableWidgetItem(str(v))
                    if str(v).lower() in ("pass", "covered", "y"):
                        item.setForeground(QColor("#00b300"))
                    elif str(v).lower() in ("fail", "gap", "n"):
                        item.setForeground(QColor("#e94560"))
                    self._reg_table.setItem(r, c, item)

        def _populate_safety_table(self, rows: list[dict]):
            self._safety_table.setRowCount(0)
            for row in rows:
                r = self._safety_table.rowCount()
                self._safety_table.insertRow(r)
                vals = [
                    row.get("module",           ""),
                    str(row.get("read_only",          "")),
                    str(row.get("no_real_orders",     "")),
                    str(row.get("production_blocked", "")),
                    str(row.get("real_order_ready",   "")),
                    row.get("compliant", ""),
                ]
                for c, v in enumerate(vals):
                    item = QTableWidgetItem(str(v))
                    if str(v).lower() in ("true", "pass", "y"):
                        item.setForeground(QColor("#00b300"))
                    elif str(v).lower() in ("false", "fail", "n"):
                        item.setForeground(QColor("#e94560"))
                    self._safety_table.setItem(r, c, item)

else:
    # Fallback stub when PySide6 not available
    class ResearchOSPlanningPanel:  # type: ignore[no-redef]
        """Stub — PySide6 not available."""
        read_only          = True
        no_real_orders     = True
        production_blocked = True
        real_order_ready   = False

        def __init__(self, parent=None):
            raise ImportError("PySide6 is required for ResearchOSPlanningPanel.")
