"""gui/stable_release_panel.py — StableReleasePanel for v0.6.0 Research OS Stable Release.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice.
[!] Actions run in QThread to avoid GUI freeze.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QFrame,
        QLineEdit, QComboBox, QScrollArea, QSizePolicy, QMessageBox,
        QTextEdit,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — StableReleasePanel will be a stub")


# ---------------------------------------------------------------------------
# Worker threads
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class _ChecklistWorker(QThread):
        finished = Signal(dict)

        def __init__(self, mode: str, adapter):
            super().__init__()
            self._mode    = mode
            self._adapter = adapter

        def run(self):
            try:
                result = self._adapter.run_checklist(self._mode)
            except Exception as exc:
                result = {"ok": False, "error": str(exc), "overall_status": "ERROR",
                          "checks": [], "total_checks": 0, "pass_count": 0,
                          "warning_count": 0, "fail_count": 0}
            self.finished.emit(result)

    class _CapabilityWorker(QThread):
        finished = Signal(dict)

        def __init__(self, adapter):
            super().__init__()
            self._adapter = adapter

        def run(self):
            try:
                result = self._adapter.build_capability_matrix()
            except Exception as exc:
                result = {"ok": False, "error": str(exc), "total": 0, "capabilities": []}
            self.finished.emit(result)

    class _ManifestWorker(QThread):
        finished = Signal(dict)

        def __init__(self, version: str, adapter):
            super().__init__()
            self._version = version
            self._adapter = adapter

        def run(self):
            try:
                result = self._adapter.build_manifest(self._version)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _ReportWorker(QThread):
        finished = Signal(dict)

        def __init__(self, mode: str, adapter):
            super().__init__()
            self._mode    = mode
            self._adapter = adapter

        def run(self):
            try:
                result = self._adapter.generate_report(self._mode)
            except Exception as exc:
                result = {"ok": False, "error": str(exc), "report_path": "", "status": "ERROR"}
            self.finished.emit(result)


# ---------------------------------------------------------------------------
# Panel
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class StableReleasePanel(QWidget):
        """GUI panel for Research OS Stable Release v0.6.0.

        [!] Research Only. No Real Orders. Production Trading: BLOCKED.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        _BANNER_TEXT = (
            "[!] Research OS Stable Release v0.6.0 | Research Only | "
            "No Real Orders | Production Trading BLOCKED"
        )
        _NOTE_TEXT = (
            "Note: Report Pack optional missing does not fail stable release. "
            "ENV_LIMITED provider reports require provider tokens."
        )

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode = mode
            self._adapter = None
            self._checklist_worker   = None
            self._capability_worker  = None
            self._manifest_worker    = None
            self._report_worker      = None
            self._last_report_path   = ""
            self._last_manifest_path = ""

            self._init_adapter()
            self._build_ui()
            self._refresh_data()

        # ------------------------------------------------------------------
        # Adapter
        # ------------------------------------------------------------------

        def _init_adapter(self):
            try:
                from gui.stable_release_adapter import StableReleaseAdapter
                self._adapter = StableReleaseAdapter()
            except Exception as exc:
                logger.warning("StableReleaseAdapter unavailable: %s", exc)
                self._adapter = None

        # ------------------------------------------------------------------
        # UI Setup
        # ------------------------------------------------------------------

        def _build_ui(self):
            main_layout = QVBoxLayout(self)
            main_layout.setSpacing(8)
            main_layout.setContentsMargins(8, 8, 8, 8)

            # Safety banner
            banner = QLabel(self._BANNER_TEXT)
            banner.setStyleSheet(
                "background:#b71c1c; color:white; font-weight:bold; padding:6px; border-radius:4px;"
            )
            banner.setWordWrap(True)
            main_layout.addWidget(banner)

            # Explanatory note
            note = QLabel(self._NOTE_TEXT)
            note.setStyleSheet(
                "background:#1a3a1a; color:#c8e6c9; font-size:11px; padding:4px; border-radius:3px;"
            )
            note.setWordWrap(True)
            main_layout.addWidget(note)

            # Summary cards
            main_layout.addWidget(self._build_summary_group())

            # Buttons
            main_layout.addWidget(self._build_buttons_group())

            # Scrollable content area
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)
            scroll_layout.setSpacing(8)

            scroll_layout.addWidget(self._build_capability_group())
            scroll_layout.addWidget(self._build_checklist_group())
            scroll_layout.addWidget(self._build_limitations_group())
            scroll_layout.addWidget(self._build_manifest_group())
            scroll_layout.addStretch(1)

            scroll.setWidget(scroll_widget)
            main_layout.addWidget(scroll)

        def _build_summary_group(self) -> QGroupBox:
            grp = QGroupBox("v0.6.0 Summary")
            layout = QHBoxLayout(grp)

            self._lbl_version    = QLabel("Version: v0.6.0")
            self._lbl_total      = QLabel("Capabilities: —")
            self._lbl_stable     = QLabel("Stable: —")
            self._lbl_warnings   = QLabel("Warnings: —")
            self._lbl_checklist  = QLabel("Checklist: —")
            self._lbl_safety     = QLabel("Safety: BLOCKED")
            self._lbl_safety.setStyleSheet("color:red; font-weight:bold;")

            for lbl in [
                self._lbl_version, self._lbl_total, self._lbl_stable,
                self._lbl_warnings, self._lbl_checklist, self._lbl_safety,
            ]:
                lbl.setFrameStyle(QFrame.Shape.StyledPanel)
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl.setMinimumWidth(120)
                lbl.setContentsMargins(6, 4, 6, 4)
                layout.addWidget(lbl)

            return grp

        def _build_buttons_group(self) -> QGroupBox:
            grp = QGroupBox("Actions")
            layout = QHBoxLayout(grp)

            self._btn_checklist   = QPushButton("Run Stable Checklist")
            self._btn_report      = QPushButton("Generate Stable Release Report")
            self._btn_manifest    = QPushButton("Build Release Manifest")
            self._btn_open_report = QPushButton("Open Latest Report")
            self._btn_refresh     = QPushButton("Refresh")

            self._btn_checklist.clicked.connect(self._on_run_checklist)
            self._btn_report.clicked.connect(self._on_generate_report)
            self._btn_manifest.clicked.connect(self._on_build_manifest)
            self._btn_open_report.clicked.connect(self._on_open_report)
            self._btn_refresh.clicked.connect(self._refresh_data)

            for btn in [
                self._btn_checklist, self._btn_report, self._btn_manifest,
                self._btn_open_report, self._btn_refresh,
            ]:
                layout.addWidget(btn)

            return grp

        def _build_capability_group(self) -> QGroupBox:
            grp = QGroupBox("Capability Matrix")
            layout = QVBoxLayout(grp)

            cols = ["Capability", "Category", "Status", "CLI", "GUI", "Reports", "Regression", "Notes"]
            self._cap_table = QTableWidget(0, len(cols))
            self._cap_table.setHorizontalHeaderLabels(cols)
            self._cap_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self._cap_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self._cap_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self._cap_table.setMinimumHeight(180)

            layout.addWidget(self._cap_table)
            return grp

        def _build_checklist_group(self) -> QGroupBox:
            grp = QGroupBox("Stable Release Checklist")
            layout = QVBoxLayout(grp)

            self._lbl_checklist_status = QLabel("Status: Not yet run")
            layout.addWidget(self._lbl_checklist_status)

            cols = ["Check", "Category", "Status", "Detail", "Suggested Fix"]
            self._chk_table = QTableWidget(0, len(cols))
            self._chk_table.setHorizontalHeaderLabels(cols)
            self._chk_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self._chk_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self._chk_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self._chk_table.setMinimumHeight(160)

            layout.addWidget(self._chk_table)
            return grp

        def _build_limitations_group(self) -> QGroupBox:
            grp = QGroupBox("Known Limitations")
            layout = QVBoxLayout(grp)

            cols = ["ID", "Limitation", "Impact", "Workaround"]
            self._lim_table = QTableWidget(0, len(cols))
            self._lim_table.setHorizontalHeaderLabels(cols)
            self._lim_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self._lim_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self._lim_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self._lim_table.setMinimumHeight(140)

            layout.addWidget(self._lim_table)
            return grp

        def _build_manifest_group(self) -> QGroupBox:
            grp = QGroupBox("Release Manifest")
            layout = QVBoxLayout(grp)

            self._lbl_manifest_path = QLabel("Manifest: (not yet built)")
            self._lbl_report_path   = QLabel("Report: (not yet generated)")
            self._lbl_tag           = QLabel("Tag: v0.6.0")
            self._lbl_commit        = QLabel("Commit: —")

            for lbl in [
                self._lbl_manifest_path, self._lbl_report_path,
                self._lbl_tag, self._lbl_commit,
            ]:
                lbl.setWordWrap(True)
                layout.addWidget(lbl)

            return grp

        # ------------------------------------------------------------------
        # Data refresh
        # ------------------------------------------------------------------

        def _refresh_data(self):
            """Refresh capability matrix and limitations in background."""
            if self._adapter is None:
                return
            # Load capabilities
            self._capability_worker = _CapabilityWorker(self._adapter)
            self._capability_worker.finished.connect(self._on_capability_loaded)
            self._capability_worker.start()
            # Load latest paths
            self._update_manifest_labels()

        def _update_manifest_labels(self):
            if self._adapter is None:
                return
            try:
                mp = self._adapter.load_latest_manifest_path()
                rp = self._adapter.load_latest_report_path()
                if mp:
                    self._last_manifest_path = mp
                    self._lbl_manifest_path.setText(f"Manifest: {mp}")
                if rp:
                    self._last_report_path = rp
                    self._lbl_report_path.setText(f"Report: {rp}")
                # Load limitations
                lims = self._adapter.load_limitations()
                self._populate_limitations_table(lims)
            except Exception as exc:
                logger.warning("StableReleasePanel update_manifest_labels error: %s", exc)

        # ------------------------------------------------------------------
        # Button handlers
        # ------------------------------------------------------------------

        def _on_run_checklist(self):
            if self._adapter is None:
                QMessageBox.warning(self, "Error", "StableReleaseAdapter not available.")
                return
            self._btn_checklist.setEnabled(False)
            self._btn_checklist.setText("Running…")
            self._checklist_worker = _ChecklistWorker(self._mode, self._adapter)
            self._checklist_worker.finished.connect(self._on_checklist_done)
            self._checklist_worker.start()

        def _on_checklist_done(self, result: dict):
            self._btn_checklist.setEnabled(True)
            self._btn_checklist.setText("Run Stable Checklist")
            self._populate_checklist_table(result)

        def _on_generate_report(self):
            if self._adapter is None:
                QMessageBox.warning(self, "Error", "StableReleaseAdapter not available.")
                return
            self._btn_report.setEnabled(False)
            self._btn_report.setText("Generating…")
            self._report_worker = _ReportWorker(self._mode, self._adapter)
            self._report_worker.finished.connect(self._on_report_done)
            self._report_worker.start()

        def _on_report_done(self, result: dict):
            self._btn_report.setEnabled(True)
            self._btn_report.setText("Generate Stable Release Report")
            rp = result.get("report_path", "")
            if rp:
                self._last_report_path = rp
                self._lbl_report_path.setText(f"Report: {rp}")
            status = result.get("status", "ERROR")
            QMessageBox.information(
                self, "Report Done",
                f"Status: {status}\nPath: {rp or 'N/A'}\n\n"
                "[!] Research Only | No Real Orders | Production BLOCKED"
            )

        def _on_build_manifest(self):
            if self._adapter is None:
                QMessageBox.warning(self, "Error", "StableReleaseAdapter not available.")
                return
            self._btn_manifest.setEnabled(False)
            self._btn_manifest.setText("Building…")
            self._manifest_worker = _ManifestWorker("v0.6.0", self._adapter)
            self._manifest_worker.finished.connect(self._on_manifest_done)
            self._manifest_worker.start()

        def _on_manifest_done(self, result: dict):
            self._btn_manifest.setEnabled(True)
            self._btn_manifest.setText("Build Release Manifest")
            mp = result.get("json_path", "")
            if mp:
                self._last_manifest_path = mp
                self._lbl_manifest_path.setText(f"Manifest: {mp}")
            commit = result.get("commit_hash", "—")
            self._lbl_commit.setText(f"Commit: {commit}")
            QMessageBox.information(
                self, "Manifest Built",
                f"Manifest: {mp or 'N/A'}\n\n"
                "[!] Research Only | No Real Orders | Production BLOCKED"
            )

        def _on_open_report(self):
            path = self._last_report_path
            if not path:
                path = self._adapter.load_latest_report_path() if self._adapter else ""
            if not path or not os.path.isfile(path):
                QMessageBox.information(self, "No Report", "No stable release report found. Generate one first.")
                return
            try:
                import subprocess, sys
                if sys.platform == "win32":
                    subprocess.Popen(["notepad", path])
                else:
                    subprocess.Popen(["xdg-open", path])
            except Exception as exc:
                QMessageBox.warning(self, "Open Error", f"Cannot open report: {exc}")

        # ------------------------------------------------------------------
        # Table population
        # ------------------------------------------------------------------

        def _on_capability_loaded(self, result: dict):
            caps = result.get("capabilities", [])
            total   = result.get("total", 0)
            stable  = result.get("stable_count", 0)
            usable  = result.get("usable_count", 0)
            warnings = result.get("usable_count", 0) + result.get("experimental_count", 0)

            self._lbl_total.setText(f"Capabilities: {total}")
            self._lbl_stable.setText(f"Stable: {stable}")
            self._lbl_warnings.setText(f"USABLE/Exp: {warnings}")

            self._cap_table.setRowCount(0)
            for c in caps:
                row = self._cap_table.rowCount()
                self._cap_table.insertRow(row)
                cli = "Yes" if c.get("cli_commands") else "No"
                gui = "Yes" if c.get("gui_tabs") else "No"
                rpt = "Yes" if c.get("reports") else "No"
                reg = "Yes" if c.get("regression_coverage") else "No"
                lims = "; ".join(c.get("known_limitations", []))[:40]
                values = [
                    c.get("name", ""),
                    c.get("category", ""),
                    c.get("status", ""),
                    cli, gui, rpt, reg,
                    lims,
                ]
                for col, val in enumerate(values):
                    item = QTableWidgetItem(str(val))
                    if c.get("status") == "STABLE":
                        item.setForeground(QColor("#2e7d32"))
                    elif c.get("status") == "BLOCKED":
                        item.setForeground(QColor("#b71c1c"))
                    elif c.get("status") in ("USABLE", "PARTIAL"):
                        item.setForeground(QColor("#e65100"))
                    self._cap_table.setItem(row, col, item)

        def _populate_checklist_table(self, result: dict):
            checks  = result.get("checks", [])
            overall = result.get("overall_status", "UNKNOWN")
            total   = result.get("total_checks", 0)
            passed  = result.get("pass_count", 0)
            warned  = result.get("warning_count", 0)
            failed  = result.get("fail_count", 0)

            self._lbl_checklist.setText(f"Checklist: {overall}")
            self._lbl_checklist_status.setText(
                f"Status: {overall} | Total: {total} | Pass: {passed} | Warn: {warned} | Fail: {failed}"
            )

            self._chk_table.setRowCount(0)
            for c in checks:
                row = self._chk_table.rowCount()
                self._chk_table.insertRow(row)
                values = [
                    c.get("name", ""),
                    c.get("category", ""),
                    c.get("status", ""),
                    (c.get("detail", "") or "")[:80],
                    (c.get("suggested_fix", "") or "")[:60],
                ]
                for col, val in enumerate(values):
                    item = QTableWidgetItem(str(val))
                    status = c.get("status", "")
                    if status == "PASS":
                        item.setForeground(QColor("#2e7d32"))
                    elif status == "FAIL":
                        item.setForeground(QColor("#b71c1c"))
                    elif status == "WARN":
                        item.setForeground(QColor("#e65100"))
                    self._chk_table.setItem(row, col, item)

        def _populate_limitations_table(self, limitations: list):
            self._lim_table.setRowCount(0)
            for lim in limitations:
                row = self._lim_table.rowCount()
                self._lim_table.insertRow(row)
                values = [
                    lim.get("id", ""),
                    lim.get("name", ""),
                    lim.get("impact", ""),
                    (lim.get("workaround", "") or "")[:80],
                ]
                for col, val in enumerate(values):
                    item = QTableWidgetItem(str(val))
                    impact = lim.get("impact", "")
                    if impact == "HIGH":
                        item.setForeground(QColor("#b71c1c"))
                    elif impact == "MEDIUM":
                        item.setForeground(QColor("#e65100"))
                    self._lim_table.setItem(row, col, item)


else:
    # Stub class when PySide6 is not available
    class StableReleasePanel:  # type: ignore[no-redef]
        """Stub StableReleasePanel — PySide6 not available."""

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, mode: str = "real", parent=None):
            logger.warning(
                "StableReleasePanel: PySide6 not available. Panel is a no-op stub. "
                "[!] Research Only | No Real Orders | Production BLOCKED"
            )
