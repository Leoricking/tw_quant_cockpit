"""
gui/research_run_registry_panel.py — ResearchRunRegistryPanel v1.1.8

PySide6/PyQt5 panel for Research Run Registry.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] NO Run Now, NO Auto Rerun, NO Delete Run, NO Broker, NO Trading.
[!] Open Artifact Folder: local path only.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QTabWidget, QGroupBox,
        QSplitter, QScrollArea, QMessageBox, QHeaderView,
        QApplication, QFrame, QLineEdit, QComboBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QTimer
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


def _make_stub_panel(title: str = "Research Run Registry"):
    class StubPanel:
        def __init__(self, *args, **kwargs):
            logger.info("%s: PySide6 not available, panel is a stub.", title)
    return StubPanel


if not _PYSIDE6_AVAILABLE:
    ResearchRunRegistryPanel = _make_stub_panel()
else:
    class _RegistryRefreshWorker(QThread):
        """Background worker for registry data refresh."""
        finished = Signal(dict)
        error = Signal(str)

        def __init__(self, parent=None):
            super().__init__(parent)

        def run(self):
            try:
                from research_registry.registry_query import RegistryQuery
                q = RegistryQuery()
                summary = q.registry_summary()
                runs = q.latest_runs(limit=50)
                self.finished.emit({
                    "summary": summary,
                    "runs": runs,
                    "error": None,
                })
            except Exception as exc:
                logger.warning("_RegistryRefreshWorker error: %s", exc)
                self.error.emit(str(exc))

    class ResearchRunRegistryPanel(QWidget):
        """
        Research Run Registry panel.

        Sections:
        A. Safety Banner
        B. Summary Cards
        C. Run Table
        D. Filters
        E. Run Detail
        F. Artifacts
        G. Lineage
        H. Comparison
        I. Buttons

        [!] Research Only. No Real Orders.
        [!] NO Run Now, NO Auto Rerun, NO Delete Run, NO Broker, NO Trading.
        """

        no_real_orders = True
        research_only = True

        def __init__(self, parent=None):
            super().__init__(parent)
            self._runs = []
            self._summary = None
            self._selected_run = None
            self._worker = None
            self._init_ui()
            self._refresh()

        def _init_ui(self):
            layout = QVBoxLayout(self)

            # A. Safety Banner
            banner = QLabel(
                "[!] Research Only  |  No Real Orders  |  Registry Does NOT Execute Runs  "
                "|  Auto Rerun DISABLED  |  Broker DISABLED  |  Trading DISABLED"
            )
            banner.setStyleSheet("background:#2a2a2a;color:#FFD700;padding:6px;font-weight:bold;")
            banner.setAlignment(Qt.AlignCenter)
            layout.addWidget(banner)

            title = QLabel("Research Run Registry v1.1.8")
            title.setStyleSheet("font-size:16px;font-weight:bold;padding:4px;")
            layout.addWidget(title)

            # B. Summary Cards
            summary_group = QGroupBox("Registry Summary")
            summary_layout = QHBoxLayout(summary_group)
            self._card_labels = {}
            for card_name in ["Total", "Completed", "Warnings", "Blocked", "Failed",
                               "Formal", "Observational", "Demo", "Duplicates", "Missing Artifacts"]:
                card = QLabel(f"{card_name}\n—")
                card.setAlignment(Qt.AlignCenter)
                card.setStyleSheet("background:#1e1e1e;color:#fff;padding:8px;border:1px solid #444;min-width:80px;")
                self._card_labels[card_name] = card
                summary_layout.addWidget(card)
            layout.addWidget(summary_group)

            # D. Filters
            filter_group = QGroupBox("Filters")
            filter_layout = QHBoxLayout(filter_group)
            filter_layout.addWidget(QLabel("Search:"))
            self._search_box = QLineEdit()
            self._search_box.setPlaceholderText("Search run_id, command, symbol, version...")
            self._search_box.textChanged.connect(self._apply_filters)
            filter_layout.addWidget(self._search_box)
            filter_layout.addWidget(QLabel("Status:"))
            self._status_filter = QComboBox()
            self._status_filter.addItems(["All", "COMPLETED", "RUNNING", "BLOCKED", "FAILED", "CANCELLED"])
            self._status_filter.currentTextChanged.connect(self._apply_filters)
            filter_layout.addWidget(self._status_filter)
            filter_layout.addWidget(QLabel("Qualification:"))
            self._qual_filter = QComboBox()
            self._qual_filter.addItems(["All", "FORMALLY_QUALIFIED", "OBSERVATIONAL_ONLY", "DEMO_ONLY", "BLOCKED", "UNKNOWN"])
            self._qual_filter.currentTextChanged.connect(self._apply_filters)
            filter_layout.addWidget(self._qual_filter)
            layout.addWidget(filter_group)

            # Main splitter
            splitter = QSplitter(Qt.Horizontal)

            # C. Run Table
            table_widget = QWidget()
            table_layout = QVBoxLayout(table_widget)
            self._run_table = QTableWidget()
            self._run_table.setColumnCount(7)
            self._run_table.setHorizontalHeaderLabels(
                ["Run ID", "Type", "Command", "Status", "Qualification", "Version", "Started"]
            )
            self._run_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self._run_table.setSelectionBehavior(QTableWidget.SelectRows)
            self._run_table.itemSelectionChanged.connect(self._on_run_selected)
            table_layout.addWidget(self._run_table)
            splitter.addWidget(table_widget)

            # Right panel — detail tabs
            detail_tabs = QTabWidget()

            # E. Run Detail
            detail_widget = QWidget()
            detail_layout = QVBoxLayout(detail_widget)
            self._detail_text = QLabel("Select a run to view details.")
            self._detail_text.setWordWrap(True)
            self._detail_text.setAlignment(Qt.AlignTop)
            scroll = QScrollArea()
            scroll.setWidget(self._detail_text)
            scroll.setWidgetResizable(True)
            detail_layout.addWidget(scroll)
            detail_tabs.addTab(detail_widget, "Run Detail")

            # F. Artifacts
            art_widget = QWidget()
            art_layout = QVBoxLayout(art_widget)
            self._artifact_table = QTableWidget()
            self._artifact_table.setColumnCount(5)
            self._artifact_table.setHorizontalHeaderLabels(["Type", "Filename", "Path", "Exists", "Checksum"])
            self._artifact_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            art_layout.addWidget(self._artifact_table)
            detail_tabs.addTab(art_widget, "Artifacts")

            # G. Lineage
            lin_widget = QWidget()
            lin_layout = QVBoxLayout(lin_widget)
            self._lineage_text = QLabel("Select a run to view lineage.")
            self._lineage_text.setWordWrap(True)
            self._lineage_text.setAlignment(Qt.AlignTop)
            lin_layout.addWidget(self._lineage_text)
            detail_tabs.addTab(lin_widget, "Lineage")

            # H. Comparison
            cmp_widget = QWidget()
            cmp_layout = QVBoxLayout(cmp_widget)
            cmp_layout.addWidget(QLabel("Run A ID:"))
            self._cmp_run_a = QLineEdit()
            cmp_layout.addWidget(self._cmp_run_a)
            cmp_layout.addWidget(QLabel("Run B ID:"))
            self._cmp_run_b = QLineEdit()
            cmp_layout.addWidget(self._cmp_run_b)
            btn_compare = QPushButton("Compare Runs")
            btn_compare.clicked.connect(self._on_compare)
            cmp_layout.addWidget(btn_compare)
            self._compare_result = QLabel("")
            self._compare_result.setWordWrap(True)
            self._compare_result.setAlignment(Qt.AlignTop)
            cmp_layout.addWidget(self._compare_result)
            detail_tabs.addTab(cmp_widget, "Compare")

            splitter.addWidget(detail_tabs)
            splitter.setSizes([500, 400])
            layout.addWidget(splitter)

            # I. Buttons
            btn_layout = QHBoxLayout()
            btn_refresh = QPushButton("Refresh")
            btn_refresh.clicked.connect(self._refresh)
            btn_layout.addWidget(btn_refresh)

            btn_copy_id = QPushButton("Copy Run ID")
            btn_copy_id.clicked.connect(self._copy_run_id)
            btn_layout.addWidget(btn_copy_id)

            btn_copy_hash = QPushButton("Copy Hash")
            btn_copy_hash.clicked.connect(self._copy_hash)
            btn_layout.addWidget(btn_copy_hash)

            btn_verify = QPushButton("Verify Run")
            btn_verify.clicked.connect(self._verify_run)
            btn_layout.addWidget(btn_verify)

            btn_report = QPushButton("Build Registry Report")
            btn_report.clicked.connect(self._build_report)
            btn_layout.addWidget(btn_report)

            btn_backfill = QPushButton("Preview Backfill")
            btn_backfill.clicked.connect(self._preview_backfill)
            btn_layout.addWidget(btn_backfill)

            layout.addLayout(btn_layout)

            safety = QLabel("[!] NO Run Now  |  NO Auto Rerun  |  NO Delete  |  NO Broker  |  NO Trading")
            safety.setStyleSheet("color:#FF6B6B;font-size:11px;padding:2px;")
            safety.setAlignment(Qt.AlignCenter)
            layout.addWidget(safety)

        def _refresh(self):
            if self._worker and self._worker.isRunning():
                return
            self._worker = _RegistryRefreshWorker()
            self._worker.finished.connect(self._on_refresh_finished)
            self._worker.error.connect(self._on_refresh_error)
            self._worker.start()

        def _on_refresh_finished(self, data: dict):
            self._runs = data.get("runs", [])
            self._summary = data.get("summary")
            self._update_summary_cards()
            self._populate_run_table(self._runs)

        def _on_refresh_error(self, msg: str):
            logger.warning("Registry panel refresh error: %s", msg)
            QMessageBox.warning(self, "Registry Warning", f"Registry data unavailable: {msg}\n\n[!] Research Only. No Real Orders.")

        def _update_summary_cards(self):
            if self._summary is None:
                return
            mapping = {
                "Total": self._summary.total_runs,
                "Completed": self._summary.completed_runs,
                "Warnings": self._summary.warning_runs,
                "Blocked": self._summary.blocked_runs,
                "Failed": self._summary.failed_runs,
                "Formal": self._summary.formal_runs,
                "Observational": self._summary.observational_runs,
                "Demo": self._summary.demo_runs,
                "Duplicates": self._summary.duplicate_runs,
                "Missing Artifacts": self._summary.missing_artifact_runs,
            }
            for name, val in mapping.items():
                if name in self._card_labels:
                    self._card_labels[name].setText(f"{name}\n{val}")

        def _populate_run_table(self, runs):
            self._run_table.setRowCount(0)
            for i, r in enumerate(runs):
                self._run_table.insertRow(i)
                self._run_table.setItem(i, 0, QTableWidgetItem(r.run_id[:16]))
                self._run_table.setItem(i, 1, QTableWidgetItem(r.run_type))
                self._run_table.setItem(i, 2, QTableWidgetItem(r.command_name))
                self._run_table.setItem(i, 3, QTableWidgetItem(r.status))
                self._run_table.setItem(i, 4, QTableWidgetItem(r.qualification))
                self._run_table.setItem(i, 5, QTableWidgetItem(r.code_version))
                self._run_table.setItem(i, 6, QTableWidgetItem((r.started_at or "")[:19]))

        def _apply_filters(self):
            query = self._search_box.text().lower().strip()
            status_filter = self._status_filter.currentText()
            qual_filter = self._qual_filter.currentText()

            filtered = self._runs
            if query:
                filtered = [r for r in filtered if
                    query in r.run_id.lower() or
                    query in r.command_name.lower() or
                    query in (r.code_version or "").lower() or
                    query in (r.status or "").lower() or
                    any(query in s.lower() for s in r.included_symbols)]
            if status_filter != "All":
                filtered = [r for r in filtered if r.status == status_filter]
            if qual_filter != "All":
                filtered = [r for r in filtered if r.qualification == qual_filter]

            self._populate_run_table(filtered)

        def _on_run_selected(self):
            rows = self._run_table.selectedItems()
            if not rows:
                return
            row = self._run_table.currentRow()
            if row < 0 or row >= len(self._runs):
                return
            # Find matching run by run_id displayed
            run_id_prefix = self._run_table.item(row, 0).text() if self._run_table.item(row, 0) else ""
            run = next((r for r in self._runs if r.run_id.startswith(run_id_prefix)), None)
            if run:
                self._selected_run = run
                self._show_run_detail(run)
                self._show_artifacts(run)
                self._show_lineage(run)

        def _show_run_detail(self, run):
            text = (
                f"<b>Run ID:</b> {run.run_id}<br>"
                f"<b>Registry ID:</b> {run.registry_id}<br>"
                f"<b>Type:</b> {run.run_type}<br>"
                f"<b>Command:</b> {run.command_name}<br>"
                f"<b>Status:</b> {run.status}<br>"
                f"<b>Qualification:</b> {run.qualification}<br>"
                f"<b>Mode:</b> {run.mode}<br>"
                f"<b>Tier:</b> {run.tier}<br>"
                f"<b>Started:</b> {run.started_at}<br>"
                f"<b>Duration:</b> {run.duration_seconds:.1f}s<br>"
                f"<b>Version:</b> {run.code_version}<br>"
                f"<b>Git Commit:</b> {run.git_commit}<br>"
                f"<b>Included Symbols:</b> {run.included_symbols}<br>"
                f"<b>Override Used:</b> {run.override_used}<br>"
                f"<b>Warnings:</b> {run.warning_count}<br>"
                f"<b>Errors:</b> {run.error_count}<br>"
                f"<b>Blocked Reasons:</b> {run.blocked_reason_codes}<br>"
                f"<b>Notes:</b> {run.notes}<br>"
                f"<br><i>[!] Research Only. No Real Orders.</i>"
            )
            self._detail_text.setText(text)

        def _show_artifacts(self, run):
            try:
                from research_registry.registry_query import RegistryQuery
                q = RegistryQuery()
                arts = q.run_artifacts(run.run_id)
                self._artifact_table.setRowCount(0)
                for i, a in enumerate(arts):
                    self._artifact_table.insertRow(i)
                    self._artifact_table.setItem(i, 0, QTableWidgetItem(a.artifact_type))
                    self._artifact_table.setItem(i, 1, QTableWidgetItem(a.filename))
                    self._artifact_table.setItem(i, 2, QTableWidgetItem(a.path))
                    self._artifact_table.setItem(i, 3, QTableWidgetItem("Yes" if a.exists else "MISSING"))
                    self._artifact_table.setItem(i, 4, QTableWidgetItem((a.checksum or "")[:12]))
                    if not a.exists:
                        for col in range(5):
                            item = self._artifact_table.item(i, col)
                            if item:
                                item.setBackground(QColor("#3a1a1a"))
            except Exception as exc:
                logger.debug("_show_artifacts error (non-fatal): %s", exc)

        def _show_lineage(self, run):
            try:
                from research_registry.registry_query import RegistryQuery
                q = RegistryQuery()
                lin = q.run_lineage(run.run_id)
                if lin:
                    self._lineage_text.setText(
                        f"<b>Run ID:</b> {lin.run_id}<br>"
                        f"<b>Relation Type:</b> {lin.relation_type}<br>"
                        f"<b>Parent:</b> {lin.parent_run_id or '(root)'}<br>"
                        f"<b>Root:</b> {lin.root_run_id}<br>"
                        f"<b>Rerun Of:</b> {lin.rerun_of or '—'}<br>"
                        f"<b>Duplicate Of:</b> {lin.duplicate_of or '—'}<br>"
                        f"<b>Depth:</b> {lin.lineage_depth}<br>"
                        f"<b>Children:</b> {lin.children_run_ids}"
                    )
                else:
                    self._lineage_text.setText("No lineage found for this run.")
            except Exception as exc:
                self._lineage_text.setText(f"Lineage unavailable: {exc}")

        def _on_compare(self):
            run_a = self._cmp_run_a.text().strip()
            run_b = self._cmp_run_b.text().strip()
            if not run_a or not run_b:
                self._compare_result.setText("Enter both Run A and Run B IDs.")
                return
            try:
                from research_registry.registry_engine import ResearchRunRegistryEngine
                from research_registry.run_comparator import ResearchRunComparator
                engine = ResearchRunRegistryEngine()
                comp = engine.compare_runs(run_a, run_b)
                if comp is None:
                    self._compare_result.setText("Could not compare (one or both runs not found).")
                else:
                    comparator = ResearchRunComparator()
                    self._compare_result.setText(comparator.summarize(comp).replace("\n", "<br>"))
            except Exception as exc:
                self._compare_result.setText(f"Compare error: {exc}")

        def _copy_run_id(self):
            if self._selected_run:
                QApplication.clipboard().setText(self._selected_run.run_id)

        def _copy_hash(self):
            if self._selected_run:
                QApplication.clipboard().setText(self._selected_run.reproducibility_hash or "")

        def _verify_run(self):
            try:
                from research_registry.registry_engine import ResearchRunRegistryEngine
                engine = ResearchRunRegistryEngine()
                result = engine.validate_registry()
                msg = f"Valid: {result.get('valid')}\nIssues: {result.get('issue_count', 0)}\n[!] Research Only. No Real Orders."
                QMessageBox.information(self, "Registry Validation", msg)
            except Exception as exc:
                QMessageBox.warning(self, "Verify Error", str(exc))

        def _build_report(self):
            try:
                from reports.research_run_registry_report import ResearchRunRegistryReportBuilder
                builder = ResearchRunRegistryReportBuilder()
                path = builder.build()
                if path:
                    QMessageBox.information(self, "Report Built", f"Report written to:\n{path}\n\n[!] Research Only. No Real Orders.")
                else:
                    QMessageBox.warning(self, "Report Failed", "Report builder returned empty path.")
            except Exception as exc:
                QMessageBox.warning(self, "Report Error", str(exc))

        def _preview_backfill(self):
            try:
                from research_registry.registry_engine import ResearchRunRegistryEngine
                engine = ResearchRunRegistryEngine()
                result = engine.backfill_existing_runs(dry_run=True, allow_write=False)
                msg = (
                    f"Status: {result.get('status')}\n"
                    f"Found: {result.get('found', 0)} sources\n"
                    f"Notes: {'; '.join(result.get('notes', []))}\n"
                    "[!] Research Only. Backfill requires allow_write=True to execute."
                )
                QMessageBox.information(self, "Backfill Preview", msg)
            except Exception as exc:
                QMessageBox.warning(self, "Backfill Error", str(exc))
