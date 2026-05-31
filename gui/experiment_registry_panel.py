"""
gui/experiment_registry_panel.py — ExperimentRegistryPanel PySide6 widget (v0.3.29).
[!] Research Only. Backtest Only. No Real Orders. Production Trading: BLOCKED.
"""

import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QComboBox,
        QSplitter, QGroupBox, QMessageBox, QHeaderView, QFrame, QSizePolicy,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QObject
    from PySide6.QtGui import QFont, QColor
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available; ExperimentRegistryPanel will be a stub.")


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class ExperimentWorker(QObject):
        """
        Background worker for long-running experiment registry operations.
        Emits finished(dict) when the task is done.
        """
        finished = Signal(dict)

        def __init__(self, adapter, parent=None):
            super().__init__(parent)
            self._adapter = adapter
            self._task = None
            self._kwargs = {}

        def run_task(self, task_name: str, **kwargs):
            """Set up task then call run() from a QThread."""
            self._task = task_name
            self._kwargs = kwargs

        def run(self):
            """Execute the configured task."""
            result = {"task": self._task, "status": "error", "error": "Unknown task"}
            try:
                task = self._task
                kw = self._kwargs
                a = self._adapter

                if task == "create_experiment":
                    result = a.create_experiment(**kw)
                    result["task"] = task
                elif task == "register_latest":
                    result = a.register_latest_run(**kw)
                    result["task"] = task
                elif task == "list_experiments":
                    result = a.list_experiments(**kw)
                    result["task"] = task
                elif task == "get_detail":
                    result = a.get_experiment_detail(**kw)
                    result["task"] = task
                elif task == "build_notebook":
                    result = a.build_notebook(**kw)
                    result["task"] = task
                elif task == "generate_report":
                    result = a.generate_report()
                    result["task"] = task
                elif task == "compare":
                    result = a.compare(**kw)
                    result["task"] = task
                elif task == "build_snapshots":
                    result = a.build_snapshots(**kw)
                    result["task"] = task
                else:
                    result = {"task": task, "status": "error", "error": f"Unknown task: {task}"}
            except Exception as exc:
                logger.exception("ExperimentWorker.run task=%s failed", self._task)
                result = {"task": self._task, "status": "error", "error": str(exc)}
            finally:
                self.finished.emit(result)


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class ExperimentRegistryPanel(QWidget):
        """
        GUI panel for Research Notebook / Experiment Registry (v0.3.29).
        [!] Research Only. Backtest Only. No Real Orders. Production Trading: BLOCKED.
        """

        read_only: bool = True
        no_real_orders: bool = True
        production_blocked: bool = True

        def __init__(self, mode: str = "real", parent=None):
            super().__init__(parent)
            self._mode = mode
            self._adapter = None
            self._thread = None
            self._worker = None
            self._experiments = []
            self._selected_experiment_id = ""
            self._current_detail = {}

            self._init_adapter()
            self._build_ui()
            self.refresh_experiments()

        # ------------------------------------------------------------------
        # Setup
        # ------------------------------------------------------------------

        def _init_adapter(self):
            try:
                from gui.experiment_registry_adapter import ExperimentRegistryAdapter
                self._adapter = ExperimentRegistryAdapter()
            except Exception:
                logger.exception("Failed to initialise ExperimentRegistryAdapter")
                self._adapter = None

        def _build_ui(self):
            root = QVBoxLayout(self)
            root.setContentsMargins(8, 8, 8, 8)
            root.setSpacing(6)

            # A. Header / Safety banner
            root.addLayout(self._build_header())

            # B. Summary cards
            root.addLayout(self._build_summary_cards())

            # Main content splitter
            splitter = QSplitter(Qt.Vertical)

            # C. Experiment table
            exp_group = QGroupBox("Experiments")
            exp_layout = QVBoxLayout(exp_group)
            self._exp_table = self._build_experiment_table()
            exp_layout.addWidget(self._exp_table)
            splitter.addWidget(exp_group)

            # D. Snapshot table
            snap_group = QGroupBox("Snapshots (selected experiment)")
            snap_layout = QVBoxLayout(snap_group)
            self._snap_table = self._build_snapshot_table()
            snap_layout.addWidget(self._snap_table)
            splitter.addWidget(snap_group)

            splitter.setSizes([300, 160])
            root.addWidget(splitter)

            # E. Compare panel
            root.addLayout(self._build_compare_panel())

            # F. Notebook preview
            nb_group = QGroupBox("Notebook Preview")
            nb_layout = QVBoxLayout(nb_group)
            self._notebook_text = QTextEdit()
            self._notebook_text.setReadOnly(True)
            self._notebook_text.setPlaceholderText("Select an experiment and click 'Build Notebook' to preview.")
            self._notebook_text.setMinimumHeight(140)
            nb_layout.addWidget(self._notebook_text)
            root.addWidget(nb_group)

            # G. Action buttons
            root.addLayout(self._build_action_buttons())

        def _build_header(self) -> QHBoxLayout:
            layout = QVBoxLayout()

            title_font = QFont()
            title_font.setPointSize(13)
            title_font.setBold(True)

            title = QLabel("Research Notebook / Experiment Registry")
            title.setFont(title_font)
            layout.addWidget(title)

            banner = QLabel(
                "⚠  Research Only  |  Backtest Only  |  No Real Orders  |  "
                f"Production Trading: BLOCKED  |  Mode: {self._mode}"
            )
            banner.setStyleSheet(
                "color: #fff; background-color: #c0392b; padding: 4px 8px; "
                "border-radius: 3px; font-weight: bold;"
            )
            banner.setWordWrap(True)
            layout.addWidget(banner)

            wrapper = QHBoxLayout()
            wrapper.addLayout(layout)
            wrapper.addStretch()
            return wrapper

        def _build_summary_cards(self) -> QHBoxLayout:
            layout = QHBoxLayout()
            layout.setSpacing(8)

            self._card_total = self._make_card("Total", "0")
            self._card_completed = self._make_card("Completed", "0")
            self._card_partial = self._make_card("Partial", "0")
            self._card_failed = self._make_card("Failed", "0")
            self._card_latest = self._make_card("Latest", "—")
            self._card_reports = self._make_card("Reports", "—")

            for card in (
                self._card_total, self._card_completed, self._card_partial,
                self._card_failed, self._card_latest, self._card_reports,
            ):
                layout.addWidget(card)
            layout.addStretch()
            return layout

        def _make_card(self, title: str, value: str) -> QFrame:
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setFixedWidth(110)
            frame.setFixedHeight(56)
            inner = QVBoxLayout(frame)
            inner.setContentsMargins(6, 4, 6, 4)
            lbl_title = QLabel(title)
            lbl_title.setStyleSheet("font-size: 10px; color: #666;")
            lbl_value = QLabel(value)
            lbl_value.setStyleSheet("font-size: 14px; font-weight: bold;")
            lbl_value.setObjectName(f"card_val_{title.lower().replace(' ', '_')}")
            inner.addWidget(lbl_title)
            inner.addWidget(lbl_value)
            return frame

        def _find_card_label(self, frame: QFrame) -> QLabel:
            for child in frame.findChildren(QLabel):
                if child.objectName().startswith("card_val_"):
                    return child
            return None

        def _build_experiment_table(self) -> QTableWidget:
            columns = [
                "Experiment ID", "Name", "Type", "Mode",
                "Profile", "Status", "Created At", "Universe", "Notes",
            ]
            table = QTableWidget(0, len(columns))
            table.setHorizontalHeaderLabels(columns)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectRows)
            table.setSelectionMode(QTableWidget.SingleSelection)
            table.setSortingEnabled(True)
            table.horizontalHeader().setStretchLastSection(True)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
            table.verticalHeader().setVisible(False)
            table.itemSelectionChanged.connect(self._on_experiment_selected)
            return table

        def _build_snapshot_table(self) -> QTableWidget:
            columns = ["Snapshot Type", "Exists", "Summary", "Source", "Warning"]
            table = QTableWidget(0, len(columns))
            table.setHorizontalHeaderLabels(columns)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectRows)
            table.horizontalHeader().setStretchLastSection(True)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
            table.verticalHeader().setVisible(False)
            return table

        def _build_compare_panel(self) -> QHBoxLayout:
            layout = QHBoxLayout()
            layout.setSpacing(6)

            lbl = QLabel("Compare:")
            layout.addWidget(lbl)

            self._compare_a = QComboBox()
            self._compare_a.setMinimumWidth(220)
            self._compare_a.setPlaceholderText("Experiment A")
            layout.addWidget(self._compare_a)

            lbl_vs = QLabel("vs.")
            layout.addWidget(lbl_vs)

            self._compare_b = QComboBox()
            self._compare_b.setMinimumWidth(220)
            self._compare_b.setPlaceholderText("Experiment B")
            layout.addWidget(self._compare_b)

            btn_compare = QPushButton("Compare")
            btn_compare.clicked.connect(self._on_compare_clicked)
            layout.addWidget(btn_compare)

            layout.addStretch()

            # Diff area below (we put it in a group box, added to root later)
            self._compare_text = QTextEdit()
            self._compare_text.setReadOnly(True)
            self._compare_text.setPlaceholderText("Comparison result will appear here.")
            self._compare_text.setMaximumHeight(120)
            layout.addWidget(self._compare_text)

            return layout

        def _build_action_buttons(self) -> QHBoxLayout:
            layout = QHBoxLayout()
            layout.setSpacing(6)

            buttons = [
                ("Create Experiment", self._on_create_experiment),
                ("Register Latest Run", self._on_register_latest),
                ("Build Snapshots", self._on_build_snapshots),
                ("Build Notebook", self._on_build_notebook),
                ("Generate Report", self._on_generate_report),
                ("Compare Selected", self._on_compare_clicked),
                ("Refresh", self.refresh_experiments),
                ("Open Folder", self._on_open_folder),
            ]
            for label, slot in buttons:
                btn = QPushButton(label)
                btn.clicked.connect(slot)
                layout.addWidget(btn)

            layout.addStretch()
            return layout

        # ------------------------------------------------------------------
        # Public: refresh
        # ------------------------------------------------------------------

        def refresh_experiments(self):
            """Reload experiment list from registry."""
            self._run_worker("list_experiments", limit=50)

        # ------------------------------------------------------------------
        # Worker orchestration
        # ------------------------------------------------------------------

        def _run_worker(self, task_name: str, **kwargs):
            """Start a background worker for the given task."""
            if not self._adapter:
                self._show_error("Adapter not available. Check logs.")
                return
            # Stop any existing thread
            self._stop_worker()

            self._thread = QThread(self)
            self._worker = ExperimentWorker(self._adapter)
            self._worker.moveToThread(self._thread)
            self._worker.run_task(task_name, **kwargs)
            self._worker.finished.connect(self._on_worker_finished)
            self._thread.started.connect(self._worker.run)
            self._worker.finished.connect(self._thread.quit)
            self._thread.start()

        def _stop_worker(self):
            """Gracefully stop any running worker thread."""
            if self._thread and self._thread.isRunning():
                try:
                    self._thread.quit()
                    self._thread.wait(2000)
                except Exception:
                    pass

        def _on_worker_finished(self, result: dict):
            """Dispatch finished worker result to the appropriate handler."""
            try:
                task = result.get("task", "")
                if task == "list_experiments":
                    self._handle_list_result(result)
                elif task == "create_experiment":
                    self._handle_create_result(result)
                elif task == "register_latest":
                    self._handle_register_result(result)
                elif task == "get_detail":
                    self._handle_detail_result(result)
                elif task == "build_notebook":
                    self._handle_notebook_result(result)
                elif task == "generate_report":
                    self._handle_report_result(result)
                elif task == "compare":
                    self._handle_compare_result(result)
                elif task == "build_snapshots":
                    self._handle_snapshots_result(result)
            except Exception:
                logger.exception("_on_worker_finished dispatch failed")

        # ------------------------------------------------------------------
        # Result handlers
        # ------------------------------------------------------------------

        def _handle_list_result(self, result: dict):
            experiments = result.get("experiments", [])
            self._experiments = experiments
            self._populate_experiment_table(experiments)
            self._populate_compare_combos(experiments)
            self._update_summary_cards(experiments)

        def _handle_create_result(self, result: dict):
            if result.get("status") == "ok":
                eid = result.get("experiment_id", "")
                self._show_info(f"Experiment created: {eid}")
            else:
                self._show_error(f"Create failed: {result.get('error', '—')}")
            self.refresh_experiments()

        def _handle_register_result(self, result: dict):
            if result.get("status") == "ok":
                self._show_info(result.get("message", "Registered."))
            else:
                self._show_error(f"Register failed: {result.get('error', '—')}")
            self.refresh_experiments()

        def _handle_detail_result(self, result: dict):
            if result.get("status") != "ok":
                logger.warning("get_detail returned error: %s", result.get("error"))
                return
            self._current_detail = result
            self._populate_snapshot_table(result.get("snapshots", {}))

        def _handle_notebook_result(self, result: dict):
            if result.get("status") == "ok":
                path = result.get("path", "")
                self._show_info(f"Notebook written to:\n{path}")
                # Load and display notebook content
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    self._notebook_text.setPlainText(content)
                except Exception:
                    pass
            else:
                self._show_error(f"Notebook build failed: {result.get('error', '—')}")

        def _handle_report_result(self, result: dict):
            if result.get("status") == "ok":
                self._show_info(f"Report generated:\n{result.get('path', '')}")
            else:
                self._show_error(f"Report failed: {result.get('error', '—')}")

        def _handle_compare_result(self, result: dict):
            if result.get("status") != "ok":
                self._compare_text.setPlainText(
                    f"Compare failed: {result.get('error', '—')}"
                )
                return
            comparison = result.get("comparison", {})
            lines = []
            lines.append("[!] Research Only. No Real Orders.\n")
            summary = comparison.get("summary", {})
            lines.append(f"Best: {summary.get('best_experiment_id', '—')}")
            lines.append(f"Recommendation: {summary.get('recommendation', '—')}")
            for pair in comparison.get("pairs", []):
                lines.append(
                    f"\n{pair.get('left_id', '?')} → {pair.get('right_id', '?')}: "
                    f"{pair.get('overall_direction', '?')}"
                )
                for score_key, score_val in pair.get("scores", {}).items():
                    d = score_val.get("direction", "?")
                    lv = score_val.get("left_value")
                    rv = score_val.get("right_value")
                    lines.append(f"  {score_key}: {lv} → {rv} ({d})")
            self._compare_text.setPlainText("\n".join(lines))

        def _handle_snapshots_result(self, result: dict):
            if result.get("status") == "ok":
                saved = result.get("saved_count", 0)
                eid = result.get("experiment_id", "")
                self._show_info(f"Built {saved} snapshots for {eid}.")
            else:
                self._show_error(f"Snapshot build failed: {result.get('error', '—')}")
            # Reload detail for the experiment
            if self._selected_experiment_id:
                self._run_worker("get_detail", experiment_id=self._selected_experiment_id)

        # ------------------------------------------------------------------
        # Table population
        # ------------------------------------------------------------------

        def _populate_experiment_table(self, experiments: list):
            self._exp_table.setSortingEnabled(False)
            self._exp_table.setRowCount(0)

            if not experiments:
                self._exp_table.setRowCount(1)
                placeholder = QTableWidgetItem(
                    "No experiments yet. Use 'Create Experiment' to start."
                )
                placeholder.setForeground(QColor("#888"))
                self._exp_table.setItem(0, 0, placeholder)
                self._exp_table.setSortingEnabled(True)
                return

            for row, exp in enumerate(experiments):
                self._exp_table.insertRow(row)
                values = [
                    exp.get("experiment_id", ""),
                    exp.get("experiment_name", ""),
                    exp.get("experiment_type", ""),
                    exp.get("mode", ""),
                    exp.get("profile", ""),
                    exp.get("status", ""),
                    exp.get("created_at", "")[:19],
                    exp.get("universe_name", ""),
                    ", ".join(exp.get("tags", [])),
                ]
                for col, val in enumerate(values):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self._exp_table.setItem(row, col, item)

                # Colour status
                status_item = self._exp_table.item(row, 5)
                if status_item:
                    status = exp.get("status", "")
                    if status == "COMPLETED":
                        status_item.setForeground(QColor("#27ae60"))
                    elif status == "FAILED":
                        status_item.setForeground(QColor("#c0392b"))
                    elif status == "RUNNING":
                        status_item.setForeground(QColor("#2980b9"))

            self._exp_table.setSortingEnabled(True)

        def _populate_snapshot_table(self, snapshots: dict):
            known_types = [
                "config", "universe", "data_quality", "provider_reliability",
                "rule_governance", "backtest", "signal_quality", "portfolio",
                "intraday", "reports",
            ]
            # Include any extra types found in the data
            all_types = list(known_types)
            for k in snapshots:
                if k not in all_types:
                    all_types.append(k)

            self._snap_table.setRowCount(0)
            for row, snap_type in enumerate(all_types):
                self._snap_table.insertRow(row)
                snap = snapshots.get(snap_type)
                exists = "Yes" if snap else "No"
                summary_str = ""
                source_str = ""
                warning_str = ""
                if snap:
                    s = snap.get("summary", {})
                    summary_str = "; ".join(
                        f"{k}={v}" for k, v in list(s.items())[:3]
                    )
                    src = snap.get("source_files", snap.get("path", ""))
                    if isinstance(src, list):
                        source_str = src[0] if src else ""
                    else:
                        source_str = str(src)
                    warnings = snap.get("warnings", [])
                    warning_str = "; ".join(warnings) if warnings else ""

                for col, val in enumerate([snap_type, exists, summary_str, source_str, warning_str]):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    if col == 1 and val == "No":
                        item.setForeground(QColor("#aaa"))
                    self._snap_table.setItem(row, col, item)

        def _populate_compare_combos(self, experiments: list):
            ids = [e.get("experiment_id", "") for e in experiments]
            self._compare_a.blockSignals(True)
            self._compare_b.blockSignals(True)
            self._compare_a.clear()
            self._compare_b.clear()
            for eid in ids:
                self._compare_a.addItem(eid)
                self._compare_b.addItem(eid)
            if len(ids) >= 2:
                self._compare_a.setCurrentIndex(1)
                self._compare_b.setCurrentIndex(0)
            self._compare_a.blockSignals(False)
            self._compare_b.blockSignals(False)

        def _update_summary_cards(self, experiments: list):
            try:
                total = len(experiments)
                completed = sum(1 for e in experiments if e.get("status") == "COMPLETED")
                partial = sum(1 for e in experiments if e.get("status") == "PARTIAL")
                failed = sum(1 for e in experiments if e.get("status") == "FAILED")
                latest = experiments[0].get("experiment_id", "—") if experiments else "—"

                # Report count
                report_count = 0
                try:
                    import glob as _glob
                    rpts = _glob.glob(
                        os.path.join(BASE_DIR, "reports", "experiment_registry_report_*.md")
                    )
                    report_count = len(rpts)
                except Exception:
                    pass

                def _set_card(frame, val):
                    lbl = self._find_card_label(frame)
                    if lbl:
                        lbl.setText(str(val))

                _set_card(self._card_total, total)
                _set_card(self._card_completed, completed)
                _set_card(self._card_partial, partial)
                _set_card(self._card_failed, failed)
                _set_card(self._card_latest, latest[:20] if latest else "—")
                _set_card(self._card_reports, report_count)

            except Exception:
                logger.exception("_update_summary_cards failed")

        # ------------------------------------------------------------------
        # Slots
        # ------------------------------------------------------------------

        def _on_experiment_selected(self):
            try:
                rows = self._exp_table.selectedItems()
                if not rows:
                    return
                row = self._exp_table.currentRow()
                eid_item = self._exp_table.item(row, 0)
                if eid_item is None:
                    return
                eid = eid_item.text()
                if not eid or eid.startswith("No experiments"):
                    return
                self._selected_experiment_id = eid
                self._run_worker("get_detail", experiment_id=eid)
            except Exception:
                logger.exception("_on_experiment_selected failed")

        def _on_create_experiment(self):
            self._run_worker(
                "create_experiment",
                name="New Research",
                experiment_type="daily_research",
                mode=self._mode,
                profile="standard",
            )

        def _on_register_latest(self):
            self._run_worker("register_latest", mode=self._mode)

        def _on_build_snapshots(self):
            eid = self._selected_experiment_id or "latest"
            self._run_worker("build_snapshots", experiment_id=eid)

        def _on_build_notebook(self):
            eid = self._selected_experiment_id or "latest"
            self._run_worker("build_notebook", experiment_id=eid)

        def _on_generate_report(self):
            self._run_worker("generate_report")

        def _on_compare_clicked(self):
            id_a = self._compare_a.currentText()
            id_b = self._compare_b.currentText()
            if not id_a or not id_b:
                self._show_error("Select two experiments to compare.")
                return
            if id_a == id_b:
                self._show_error("Select two different experiments.")
                return
            self._run_worker("compare", experiment_ids=[id_a, id_b])

        def _on_open_folder(self):
            try:
                experiments_dir = os.path.join(BASE_DIR, "experiments")
                os.startfile(experiments_dir)
            except Exception as exc:
                logger.warning("open_folder failed: %s", exc)
                self._show_info(f"Experiments folder: {os.path.join(BASE_DIR, 'experiments')}")

        # ------------------------------------------------------------------
        # Dialogs
        # ------------------------------------------------------------------

        def _show_info(self, msg: str):
            QMessageBox.information(self, "Experiment Registry", msg)

        def _show_error(self, msg: str):
            QMessageBox.warning(self, "Experiment Registry — Error", msg)

        # ------------------------------------------------------------------
        # Cleanup
        # ------------------------------------------------------------------

        def closeEvent(self, event):
            """Stop any running worker thread before closing."""
            self._stop_worker()
            super().closeEvent(event)

else:
    # Stub class when PySide6 is unavailable
    class ExperimentRegistryPanel:  # type: ignore
        """
        Stub for ExperimentRegistryPanel when PySide6 is not installed.
        [!] Research Only. No Real Orders. Production Trading: BLOCKED.
        """
        read_only: bool = True
        no_real_orders: bool = True
        production_blocked: bool = True

        def __init__(self, mode="real", parent=None):
            logger.warning(
                "ExperimentRegistryPanel: PySide6 not available. GUI panel is a stub."
            )

    class ExperimentWorker:  # type: ignore
        """Stub for ExperimentWorker when PySide6 is not installed."""
        def __init__(self, adapter=None, parent=None):
            pass
