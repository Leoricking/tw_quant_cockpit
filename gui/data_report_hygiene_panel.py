"""
gui/data_report_hygiene_panel.py — DataReportHygienePanel for TW Quant Cockpit v1.0.2.

PySide6 panel for Data & Report Hygiene review.
Review-only. No automatic deletion. No automatic archive. No real orders.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Data Cleanup is Review Only. Archive Suggestions Only.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_DATA_REPORT_HYGIENE_AVAILABLE = False

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
        QTableWidgetItem, QPushButton, QTabWidget, QLineEdit,
        QComboBox, QCheckBox, QHeaderView, QSizePolicy, QApplication,
        QMessageBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QFont, QColor
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — DataReportHygienePanel running as stub")


if _PYSIDE6_OK:

    class _HygieneScanWorker(QThread):
        """Background worker for hygiene scan."""
        scan_done    = Signal(object, object, object, object)
        scan_error   = Signal(str)

        def __init__(self, mode: str = "real", project_root: str = ".") -> None:
            super().__init__()
            self._mode         = mode
            self._project_root = project_root

        def run(self) -> None:
            try:
                import os
                from maintenance.data_report_hygiene_engine import DataReportHygieneEngine
                engine = DataReportHygieneEngine(project_root=self._project_root)
                inventory, manifests, summary, suggestions = engine.run(mode=self._mode)
                self.scan_done.emit(inventory, manifests, summary, suggestions)
            except Exception as exc:
                self.scan_error.emit(str(exc))

    class DataReportHygienePanel(QWidget):
        """Data & Report Hygiene review panel.

        [!] Research Only. No Real Orders. Data Cleanup Review Only.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True
        review_only        = True

        def __init__(self, mode: str = "real", project_root: str = ".", parent=None) -> None:
            super().__init__(parent)
            self._mode         = mode
            self._project_root = project_root
            self._worker: _HygieneScanWorker | None = None
            self._inventory  = []
            self._manifests  = []
            self._summary    = None
            self._suggestions = []
            self._build_ui()

        def _build_ui(self) -> None:
            root_layout = QVBoxLayout(self)
            root_layout.setContentsMargins(6, 6, 6, 6)

            # Safety banner
            banner = QLabel(
                "Data & Report Hygiene  |  Review Only  |  No automatic deletion  |  "
                "No automatic archive  |  No Real Orders  |  Production Trading BLOCKED"
            )
            banner.setStyleSheet(
                "background:#1a1a2e;color:#e0e0e0;font-weight:bold;padding:6px;"
            )
            banner.setAlignment(Qt.AlignCenter)
            root_layout.addWidget(banner)

            # Summary cards row
            self._summary_row = QHBoxLayout()
            self._cards: dict[str, QLabel] = {}
            for label in [
                "Total Items", "Runtime Outputs", "Git-tracked Runtime",
                "Missing Gitignore", "Stale Reports", "Large Files",
                "Warnings", "Blocked",
            ]:
                card = QLabel(f"{label}\n—")
                card.setAlignment(Qt.AlignCenter)
                card.setStyleSheet(
                    "background:#16213e;color:#a0c4ff;border:1px solid #333;padding:6px;"
                )
                card.setMinimumWidth(100)
                self._cards[label] = card
                self._summary_row.addWidget(card)
            root_layout.addLayout(self._summary_row)

            # Filters
            filter_row = QHBoxLayout()
            self._kw_filter = QLineEdit()
            self._kw_filter.setPlaceholderText("Keyword filter…")
            self._kw_filter.textChanged.connect(self._apply_filters)
            filter_row.addWidget(QLabel("Keyword:"))
            filter_row.addWidget(self._kw_filter)

            self._cat_filter = QComboBox()
            self._cat_filter.addItems([
                "All Categories", "REPORT", "BACKTEST_RESULT", "DATABASE",
                "SPREADSHEET", "JSON_OUTPUT", "LOG", "CACHE", "UNKNOWN",
            ])
            self._cat_filter.currentIndexChanged.connect(self._apply_filters)
            filter_row.addWidget(QLabel("Category:"))
            filter_row.addWidget(self._cat_filter)

            self._sev_filter = QComboBox()
            self._sev_filter.addItems(["All Severity", "INFO", "LOW", "MEDIUM", "HIGH", "BLOCKED"])
            self._sev_filter.currentIndexChanged.connect(self._apply_filters)
            filter_row.addWidget(QLabel("Severity:"))
            filter_row.addWidget(self._sev_filter)

            self._git_tracked_cb = QCheckBox("Git-tracked only")
            self._git_tracked_cb.stateChanged.connect(self._apply_filters)
            self._missing_ig_cb  = QCheckBox("Missing gitignore only")
            self._missing_ig_cb.stateChanged.connect(self._apply_filters)
            self._stale_cb       = QCheckBox("Stale only")
            self._stale_cb.stateChanged.connect(self._apply_filters)
            self._large_cb       = QCheckBox("Large only")
            self._large_cb.stateChanged.connect(self._apply_filters)
            filter_row.addWidget(self._git_tracked_cb)
            filter_row.addWidget(self._missing_ig_cb)
            filter_row.addWidget(self._stale_cb)
            filter_row.addWidget(self._large_cb)
            root_layout.addLayout(filter_row)

            # Tab widget
            self._tabs = QTabWidget()
            self._inv_table      = self._make_table(
                ["Item ID", "Path", "Category", "Age(d)", "Size(B)", "Severity", "Action"]
            )
            self._reports_table  = self._make_table(
                ["Report ID", "Path", "Type", "Module", "Latest", "Ignored"]
            )
            self._gitignore_table = self._make_table(["Pattern", "Covered"])
            self._tracked_table  = self._make_table(["Tracked Runtime File"])
            self._stale_table    = self._make_table(
                ["Path", "Category", "Age(d)", "Size(B)", "Severity"]
            )
            self._explain_table  = self._make_table(
                ["Field", "Value"]
            )

            self._tabs.addTab(self._inv_table,       "Inventory")
            self._tabs.addTab(self._reports_table,   "Reports")
            self._tabs.addTab(self._gitignore_table, "Gitignore Coverage")
            self._tabs.addTab(self._tracked_table,   "Tracked Runtime Outputs")
            self._tabs.addTab(self._stale_table,     "Stale / Large Files")
            self._tabs.addTab(self._explain_table,   "Explanation")
            root_layout.addWidget(self._tabs)

            # Empty state
            self._empty_label = QLabel(
                "No hygiene data yet. Run Hygiene Scan to begin."
            )
            self._empty_label.setAlignment(Qt.AlignCenter)
            self._empty_label.setStyleSheet("color:#888;font-size:14px;padding:20px;")
            root_layout.addWidget(self._empty_label)

            # Buttons
            btn_row = QHBoxLayout()
            self._scan_btn    = QPushButton("Run Hygiene Scan")
            self._report_btn  = QPushButton("Generate Hygiene Report")
            self._refresh_btn = QPushButton("Refresh")
            self._copy_btn    = QPushButton("Copy Review Suggestion")
            self._gitignore_copy_btn = QPushButton("Copy Gitignore Suggestion")

            self._scan_btn.clicked.connect(self._on_run_scan)
            self._report_btn.clicked.connect(self._on_generate_report)
            self._refresh_btn.clicked.connect(self._on_refresh)
            self._copy_btn.clicked.connect(self._on_copy_suggestion)
            self._gitignore_copy_btn.clicked.connect(self._on_copy_gitignore)

            for btn in [self._scan_btn, self._report_btn, self._refresh_btn,
                        self._copy_btn, self._gitignore_copy_btn]:
                btn_row.addWidget(btn)
            root_layout.addLayout(btn_row)

        # ------------------------------------------------------------------
        # Slots
        # ------------------------------------------------------------------

        def _on_run_scan(self) -> None:
            self._scan_btn.setEnabled(False)
            self._scan_btn.setText("Scanning…")
            import os
            root = self._project_root if os.path.isabs(self._project_root) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self._worker = _HygieneScanWorker(mode=self._mode, project_root=root)
            self._worker.scan_done.connect(self._on_scan_done)
            self._worker.scan_error.connect(self._on_scan_error)
            self._worker.start()

        def _on_scan_done(self, inventory, manifests, summary, suggestions) -> None:
            self._inventory   = inventory
            self._manifests   = manifests
            self._summary     = summary
            self._suggestions = suggestions
            self._scan_btn.setEnabled(True)
            self._scan_btn.setText("Run Hygiene Scan")
            self._empty_label.hide()
            self._refresh_cards()
            self._apply_filters()
            self._refresh_reports_table()
            self._refresh_gitignore_table()
            self._refresh_tracked_table()
            self._refresh_stale_table()

        def _on_scan_error(self, msg: str) -> None:
            self._scan_btn.setEnabled(True)
            self._scan_btn.setText("Run Hygiene Scan")
            QMessageBox.warning(self, "Hygiene Scan Error", f"Scan failed: {msg}")

        def _on_generate_report(self) -> None:
            try:
                from reports.data_report_hygiene_report import DataReportHygieneReportBuilder
                import os
                root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                builder = DataReportHygieneReportBuilder()
                path    = builder.build(mode=self._mode, project_root=root)
                QMessageBox.information(self, "Report Generated", f"Report saved:\n{path}")
            except Exception as exc:
                QMessageBox.warning(self, "Report Error", str(exc))

        def _on_refresh(self) -> None:
            try:
                from maintenance.data_report_hygiene_store import DataReportHygieneStore
                store = DataReportHygieneStore()
                self._inventory  = store.load_latest_inventory()
                self._manifests  = store.load_latest_report_manifest()
                self._summary    = store.load_latest_summary()
                self._empty_label.hide()
                self._refresh_cards()
                self._apply_filters()
            except Exception as exc:
                logger.warning("Refresh failed: %s", exc)

        def _on_copy_suggestion(self) -> None:
            if not self._suggestions:
                return
            text = "\n".join(
                f"[{s['action']}] {s['item_id']}: {s['reason']}"
                for s in self._suggestions[:10]
            )
            QApplication.clipboard().setText(text)

        def _on_copy_gitignore(self) -> None:
            try:
                from maintenance.data_report_hygiene_engine import DataReportHygieneEngine
                import os
                root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                engine   = DataReportHygieneEngine(project_root=root)
                coverage = engine.scan_gitignore_coverage()
                missing  = [p for p, v in coverage.items() if not v]
                if missing:
                    text = "\n".join(f"# Add to .gitignore:\n{p}" for p in missing)
                else:
                    text = "# All key gitignore patterns are covered."
                QApplication.clipboard().setText(text)
            except Exception as exc:
                logger.warning("Copy gitignore failed: %s", exc)

        # ------------------------------------------------------------------
        # UI helpers
        # ------------------------------------------------------------------

        def _make_table(self, headers) -> QTableWidget:
            t = QTableWidget(0, len(headers))
            t.setHorizontalHeaderLabels(headers)
            t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            t.setEditTriggers(QTableWidget.NoEditTriggers)
            t.setSelectionBehavior(QTableWidget.SelectRows)
            return t

        def _refresh_cards(self) -> None:
            if not self._summary:
                return
            s = self._summary
            mapping = {
                "Total Items":       str(s.total_items),
                "Runtime Outputs":   str(s.runtime_outputs),
                "Git-tracked Runtime": str(s.git_tracked_runtime_outputs),
                "Missing Gitignore": str(s.missing_gitignore_rules),
                "Stale Reports":     str(s.stale_reports),
                "Large Files":       str(s.large_files),
                "Warnings":          str(s.warning_count),
                "Blocked":           str(s.blocked_count),
            }
            for label, val in mapping.items():
                if label in self._cards:
                    self._cards[label].setText(f"{label}\n{val}")

        def _apply_filters(self) -> None:
            kw      = self._kw_filter.text().lower()
            cat     = self._cat_filter.currentText()
            sev     = self._sev_filter.currentText()
            tracked = self._git_tracked_cb.isChecked()
            missing = self._missing_ig_cb.isChecked()
            stale   = self._stale_cb.isChecked()
            large   = self._large_cb.isChecked()

            filtered = list(self._inventory)
            if kw:
                filtered = [i for i in filtered if kw in i.path.lower() or kw in i.category.lower()]
            if cat != "All Categories":
                filtered = [i for i in filtered if i.category == cat]
            if sev != "All Severity":
                filtered = [i for i in filtered if i.severity == sev]
            if tracked:
                filtered = [i for i in filtered if i.is_git_tracked]
            if missing:
                filtered = [i for i in filtered if not i.is_git_ignored and i.is_runtime_output]
            if stale:
                filtered = [i for i in filtered if i.age_days > 30]
            if large:
                filtered = [i for i in filtered if i.size_bytes > 5 * 1024 * 1024]

            self._inv_table.setRowCount(len(filtered))
            for row, item in enumerate(filtered):
                for col, val in enumerate([
                    item.item_id[:40], item.path[-60:], item.category,
                    str(item.age_days), str(item.size_bytes),
                    item.severity, item.action_hint,
                ]):
                    self._inv_table.setItem(row, col, QTableWidgetItem(val))

        def _refresh_reports_table(self) -> None:
            self._reports_table.setRowCount(len(self._manifests))
            for row, m in enumerate(self._manifests):
                for col, val in enumerate([
                    m.report_id[:40], m.report_path[-50:], m.report_type[:30],
                    m.module[:20], str(m.is_latest), str(m.is_git_ignored),
                ]):
                    self._reports_table.setItem(row, col, QTableWidgetItem(val))

        def _refresh_gitignore_table(self) -> None:
            try:
                from maintenance.data_report_hygiene_engine import DataReportHygieneEngine
                import os
                root     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                engine   = DataReportHygieneEngine(project_root=root)
                coverage = engine.scan_gitignore_coverage()
                self._gitignore_table.setRowCount(len(coverage))
                for row, (pat, covered) in enumerate(coverage.items()):
                    self._gitignore_table.setItem(row, 0, QTableWidgetItem(pat))
                    self._gitignore_table.setItem(row, 1, QTableWidgetItem(str(covered)))
            except Exception as exc:
                logger.warning("gitignore table refresh: %s", exc)

        def _refresh_tracked_table(self) -> None:
            try:
                from maintenance.data_report_hygiene_engine import DataReportHygieneEngine
                import os
                root    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                engine  = DataReportHygieneEngine(project_root=root)
                tracked = engine.scan_git_tracked_runtime_outputs()
                self._tracked_table.setRowCount(len(tracked))
                for row, f in enumerate(tracked):
                    self._tracked_table.setItem(row, 0, QTableWidgetItem(f))
            except Exception as exc:
                logger.warning("tracked table refresh: %s", exc)

        def _refresh_stale_table(self) -> None:
            from maintenance.data_report_hygiene_engine import _STALE_DAYS, _LARGE_BYTES
            stale = [i for i in self._inventory if i.age_days > _STALE_DAYS]
            large = [i for i in self._inventory if i.size_bytes > _LARGE_BYTES]
            combined = list({i.item_id: i for i in stale + large}.values())
            self._stale_table.setRowCount(len(combined))
            for row, item in enumerate(combined):
                for col, val in enumerate([
                    item.path[-60:], item.category,
                    str(item.age_days), str(item.size_bytes), item.severity,
                ]):
                    self._stale_table.setItem(row, col, QTableWidgetItem(val))

        def closeEvent(self, event) -> None:
            if self._worker and self._worker.isRunning():
                self._worker.quit()
                self._worker.wait()
            super().closeEvent(event)

    _DATA_REPORT_HYGIENE_AVAILABLE = True

else:
    # Stub class when PySide6 is unavailable
    class DataReportHygienePanel:  # type: ignore[no-redef]
        """Stub: PySide6 not available."""
        read_only          = True
        no_real_orders     = True
        production_blocked = True
        review_only        = True

        def __init__(self, *args, **kwargs) -> None:
            pass
